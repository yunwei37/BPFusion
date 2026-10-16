#!/usr/bin/env python3
"""Bounded server lifecycle for the requested remote benchmark."""
from pathlib import Path
import argparse,datetime,json,os,signal,subprocess,time,traceback
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
              network_sources={f:(r/f).read_text() for f in ["executor/io_uring_tcp.h","executor/userspace_tcp.h","bpf/include/bpfusion_queue.h"]})
 try:
  if args.mode=="kernel":
   cmd=[str(build/"bpfusion_load"),"stream-uring-attach"];z=subprocess.run(cmd,env=env,capture_output=True,text=True)
   receipt["attach"]=dict(command=cmd,exit=z.returncode,stdout=z.stdout,stderr=z.stderr);attached=True;assert z.returncode==0
  cmd=[str(build/("vllm_mixed_uring_loop" if args.mode=="kernel" else "vllm_mixed_user_network_wait")),model,"600"]
  receipt["command"]=cmd
  with Path(str(prefix)+".server.stdout").open("x") as log:
   p=subprocess.Popen(cmd,env=env,cwd=r,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
   receipt["pid"]=p.pid;Path(str(prefix)+".server_started.json").write_text(json.dumps(receipt,indent=2))
   receipt["exit"]=p.wait()
 except BaseException as e:receipt["error"]=repr(e);receipt["traceback"]=traceback.format_exc()
 finally:
  if p is not None and p.poll() is None:
   os.killpg(p.pid,signal.SIGTERM)
   try:receipt["cleanup_exit"]=p.wait(timeout=60)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);receipt["cleanup_exit"]=p.wait();receipt["forced"]=True
  if attached:
   z=subprocess.run([str(build/"bpfusion_load"),"stream-detach"],env=env,capture_output=True,text=True)
   receipt["detach"]=dict(exit=z.returncode,stdout=z.stdout,stderr=z.stderr)
   for name in pins:(Path("/sys/fs/bpf")/name).unlink(missing_ok=True)
  receipt["terminal_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
  receipt["pins"]=[str(p) for p in Path("/sys/fs/bpf").glob("bpfusion*")]
  Path(str(prefix)+".server_terminal.json").write_text(json.dumps(receipt,indent=2))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--prefix",required=True);ap.add_argument("--bind",required=True);ap.add_argument("--build",required=True)
 ap.add_argument("--pair",type=int,required=True);ap.add_argument("--mode",choices=["kernel","native"],required=True);main(ap.parse_args())
