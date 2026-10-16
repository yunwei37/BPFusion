from pathlib import Path
import argparse,subprocess,json,time,os
ap=argparse.ArgumentParser();ap.add_argument("pid",type=int);ap.add_argument("output");args=ap.parse_args()
t=Path("/tmp/bpfusion-mixed-integration-n4cog5c6");begin=time.monotonic_ns()
z=subprocess.run([str(t/"errno_build16/bpfusion_load"),"stats"],capture_output=True,text=True)
row=dict(begin_ns=begin,stats_exit=z.returncode,stats_stdout=z.stdout,stats_stderr=z.stderr,pid=args.pid,owned_fd={})
for p in Path("/proc/"+str(args.pid)+"/fd").iterdir():
 try:
  target=os.readlink(p)
  if target.startswith("socket:"):row["owned_fd"][p.name]=target
 except OSError:pass
row["tcp"]=[s for s in Path("/proc/net/tcp").read_text().splitlines()[1:] if s.split()[1].endswith(":99EB")]
for name in ["syscall","stack","stat","schedstat","status"]:
 try:row[name]=Path("/proc/"+str(args.pid)+"/"+name).read_text()
 except OSError as e:row[name]=repr(e)
row["end_ns"]=time.monotonic_ns();Path(args.output).write_text(json.dumps(row,indent=2));print("snapshot",len(row["owned_fd"]),len(row["tcp"]),row["end_ns"]-begin)
