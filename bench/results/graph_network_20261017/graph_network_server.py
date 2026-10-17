#!/usr/bin/env python3
"""Bounded private lifecycle for a matched graph-network measurement."""
from pathlib import Path
import argparse,datetime,json,os,signal,subprocess,time,traceback
def main(args):
 r=Path("/workspaces/repository");t=Path(args.runtime);prefix=Path(args.prefix)
 env=dict(os.environ,**json.loads((t/"environment.json").read_text()),BF_BIND=args.bind)
 build=Path(args.build) if args.build else t/"graph_nodelay_build8";p=None;attached=False
 pins=["bpfusion_ctl","bpfusion_stats","bpfusion_db","bpfusion_streams","bpfusion_stream_link",
       "bpfusion_uring_link","bpfusion_uring_owner","bpfusion_uring_bind_link","bpfusion_pending"]
 assert subprocess.check_output(["git","symbolic-ref","--short","HEAD"],cwd=r,text=True).strip()=="main"
 assert not list(Path("/sys/fs/bpf").glob("bpfusion*"))
 allowed=sorted(os.sched_getaffinity(0));affinity=allowed if args.cores==0 else allowed[:args.cores]
 assert len(affinity)==(len(allowed) if args.cores==0 else args.cores)
 receipt=dict(mode=args.mode,operation=args.operation,repeat=args.repeat,cores=args.cores,
  allowed_cpus=allowed,service_affinity=affinity,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
  source_commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=r,text=True).strip(),
  sources={f:(r/f).read_text() for f in ["examples/torch_graph_server.py","executor/graph_server.cu",
    "executor/graph_backend.h","executor/userspace_tcp.h","executor/kernel_tcp.h","bpf/kernel_tcp.bpf.c",
    "bpf/fusion.bpf.c","bpf/include/kernel_tcp_state.h","bpf/include/bpfusion_queue.h"]})
 snapshot=build/"graph_source_snapshot.cu"
 if snapshot.exists():receipt["sources"]["executor/graph_server.cu"]=snapshot.read_text()
 receipt["build"]=str(build)
 try:
  if args.mode=="kernel":
   z=subprocess.run([str(build/"bpfusion_load"),"stream-uring-attach"],cwd=r,env=env,capture_output=True,text=True)
   receipt["attach"]=dict(exit=z.returncode,stdout=z.stdout,stderr=z.stderr);attached=True;assert z.returncode==0
  lib=build/("graph_server_kernel_network.so" if args.mode=="kernel" else "graph_server_user_network_wait.so")
  cmd=[str(t/"runtime/bin/python"),str(r/"examples/torch_graph_server.py"),str(lib),args.operation,
       "--repeat",str(args.repeat),"--seconds","600"]
  if args.cores:cmd=["taskset","-c",",".join(map(str,affinity)),*cmd]
  receipt["command"]=cmd
  with Path(str(prefix)+".server.stdout").open("x") as out:
   p=subprocess.Popen(cmd,cwd=r,env=env,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
   receipt["pid"]=p.pid;Path(str(prefix)+".server_started.json").write_text(json.dumps(receipt,indent=2))
   receipt["exit"]=p.wait()
 except BaseException as e:receipt.update(error=repr(e),traceback=traceback.format_exc())
 finally:
  if p is not None and p.poll() is None:
   os.killpg(p.pid,signal.SIGTERM)
   try:receipt["cleanup_exit"]=p.wait(timeout=30)
   except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);receipt["cleanup_exit"]=p.wait();receipt["forced"]=True
  if attached:
   z=subprocess.run([str(build/"bpfusion_load"),"stats"],cwd=r,env=env,capture_output=True,text=True)
   receipt["final_bpf_stats"]=dict(exit=z.returncode,stdout=z.stdout,stderr=z.stderr)
   z=subprocess.run([str(build/"bpfusion_load"),"stream-detach"],cwd=r,env=env,capture_output=True,text=True)
   receipt["detach"]=dict(exit=z.returncode,stdout=z.stdout,stderr=z.stderr)
   for name in pins:(Path("/sys/fs/bpf")/name).unlink(missing_ok=True)
  receipt["terminal_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
  receipt["remaining_pins"]=[p.name for p in Path("/sys/fs/bpf").glob("bpfusion*")]
  Path(str(prefix)+".server_terminal.json").write_text(json.dumps(receipt,indent=2))
if __name__=="__main__":
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--runtime",required=True)
 ap.add_argument("--prefix",required=True);ap.add_argument("--bind",required=True)
 ap.add_argument("--mode",choices=["kernel","native"],required=True)
 ap.add_argument("--operation",choices=["matmul","fft"],required=True)
 ap.add_argument("--build");ap.add_argument("--repeat",type=int,default=1);ap.add_argument("--cores",type=int,default=0)
 main(ap.parse_args())
