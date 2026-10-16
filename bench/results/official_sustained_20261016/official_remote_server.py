#!/usr/bin/env python3
"""Bounded server lifecycle for the requested remote benchmark."""
from pathlib import Path
import argparse,datetime,http.client,json,os,signal,subprocess,time,traceback
t=Path(__file__).resolve().parent;r=Path("/workspaces/repository")
pins=["bpfusion_ctl","bpfusion_stats","bpfusion_db","bpfusion_streams","bpfusion_stream_link","bpfusion_uring_link","bpfusion_uring_owner","bpfusion_uring_bind_link","bpfusion_pending"]
def main(args):
 os.chdir(r);prefix=Path(args.prefix);assert not Path(str(prefix)+".server_started.json").exists()
 env=dict(os.environ,**json.loads((t/"environment.json").read_text()),BF_BIND=args.bind)
 build=Path(args.build);model=json.loads((t/"models.json").read_text())["qwen"];p=None;attached=False
 assert subprocess.check_output(["git","symbolic-ref","--short","HEAD"],text=True).strip()=="main"
 assert not list(Path("/sys/fs/bpf").glob("bpfusion*"))
 receipt=dict(mode=args.mode,pair=args.pair,bind=args.bind,build=str(build),source_commit=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
              started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),model=model,server_source=(r/"executor/vllm_mixed.cu").read_text(),
              network_sources={f:(r/f).read_text() for f in ["executor/io_uring_tcp.h","executor/userspace_tcp.h","bpf/include/bpfusion_queue.h"]},bpf_sources={f:(r/f).read_text() for f in ["bpf/fusion.bpf.c","bpf/uring_loop.bpf.c","bpf/include/bpfusion_admission.h"]})
 receipt["condition"]=args.mode if args.mode in ["native","official"] else "candidate"
 if receipt["condition"]=="candidate":
  source=t/"kernel_owned_tcp_prototype"
  receipt["server_source"]=(source/"vllm_mixed.cu").read_text()
  for name in ["kernel_tcp.h","kernel_tcp_state.h"]:
   receipt["network_sources"][name]=(source/name).read_text()
  receipt["bpf_sources"]["kernel_tcp.bpf.c"]=(source/"kernel_tcp.bpf.c").read_text()
 try:
  if args.mode=="kernel":
   cmd=[str(build/"bpfusion_load"),"stream-uring-attach"];z=subprocess.run(cmd,env=env,capture_output=True,text=True)
   receipt["attach"]=dict(command=cmd,exit=z.returncode,stdout=z.stdout,stderr=z.stderr);attached=True;assert z.returncode==0
  if args.mode=="official":
   env.pop("VLLM_ENABLE_V1_MULTIPROCESSING",None)
   env["VLLM_API_KEY"]=(t/"official_remote_key").read_text().strip()
   cmd=[str(t/"runtime/bin/vllm"),"serve",model,"--tokens-only","--dtype","half","--host",args.bind,"--port","39404"]
  else:cmd=[str(build/("vllm_mixed_uring_loop" if args.mode=="kernel" else "vllm_mixed_user_network_wait")),model,"600"]
  receipt["command"]=cmd
  with Path(str(prefix)+".server.stdout").open("x") as log:
   p=subprocess.Popen(cmd,env=env,cwd=r,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
   receipt["pid"]=p.pid;Path(str(prefix)+".server_started.json").write_text(json.dumps(receipt,indent=2))
   if args.mode=="official":
    while True:
     assert p.poll() is None,Path(str(prefix)+".server.stdout").read_text()[-5000:]
     try:
      c=http.client.HTTPConnection(args.bind,39404,timeout=2);c.request("GET","/health");response=c.getresponse();good=response.status==200;response.read();c.close()
      if good:break
     except (OSError,http.client.HTTPException):pass
     time.sleep(.1)
    auth=[]
    for token in [None,"invalid"]:
     c=http.client.HTTPConnection(args.bind,39404,timeout=60)
     c.request("POST","/inference/v1/generate",b"{}",{} if token is None else {"Authorization":"Bearer "+token})
     response=c.getresponse();auth.append(response.status);response.read();c.close()
    assert auth==[401,401],auth
    Path(str(prefix)+".official_ready.json").write_text(json.dumps(dict(missing=401,invalid=401)))
   receipt["exit"]=p.wait()
   if args.mode=="official":
    # vLLM parent can exit before EngineCore. Account for and clean its group.
    def members():
     result=[]
     for stat in Path("/proc").glob("[0-9]*/stat"):
      try:
       fields=stat.read_text().rsplit(") ",1)[1].split()
       if int(fields[2])==p.pid and fields[0]!="Z":result.append(int(stat.parent.name))
      except (OSError,ValueError):pass
     return result
    deadline=time.monotonic()+60
    while members() and time.monotonic()<deadline:time.sleep(.1)
    receipt["children_after_grace"]=members()
    if receipt["children_after_grace"]:
     receipt["forced_children"]=True
     os.killpg(p.pid,signal.SIGKILL)
     deadline=time.monotonic()+10
     while members() and time.monotonic()<deadline:time.sleep(.1)
    receipt["remaining_children"]=members()
    assert not receipt["remaining_children"]
 except BaseException as e:receipt["error"]=repr(e);receipt["traceback"]=traceback.format_exc()
 finally:
  if p is not None and p.poll() is None:
   os.killpg(p.pid,signal.SIGTERM)
   try:receipt["cleanup_exit"]=p.wait(timeout=60)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);receipt["cleanup_exit"]=p.wait();receipt["forced"]=True
  if attached:
   q=subprocess.run([str(build/"bpfusion_load"),"stats"],env=env,capture_output=True,text=True)
   receipt["final_bpf_stats"]=dict(exit=q.returncode,stdout=q.stdout,stderr=q.stderr)
   z=subprocess.run([str(build/"bpfusion_load"),"stream-detach"],env=env,capture_output=True,text=True)
   receipt["detach"]=dict(exit=z.returncode,stdout=z.stdout,stderr=z.stderr)
   for name in pins:(Path("/sys/fs/bpf")/name).unlink(missing_ok=True)
  receipt["terminal_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
  receipt["pins"]=[str(p) for p in Path("/sys/fs/bpf").glob("bpfusion*")]
  Path(str(prefix)+".server_terminal.json").write_text(json.dumps(receipt,indent=2))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--prefix",required=True);ap.add_argument("--bind",required=True);ap.add_argument("--build",required=True)
 ap.add_argument("--pair",type=int,required=True);ap.add_argument("--mode",choices=["kernel","native","official"],required=True);main(ap.parse_args())
