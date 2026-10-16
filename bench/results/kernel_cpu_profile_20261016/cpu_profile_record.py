from pathlib import Path
import argparse,subprocess,os,json,datetime
t=Path(__file__).parent
ap=argparse.ArgumentParser();ap.add_argument("--prefix",required=True);ap.add_argument("--pid",type=int,required=True);args=ap.parse_args()
prefix=Path(args.prefix);d=t/"perf_runtime"
env=dict(os.environ,**json.loads((d/"environment.json").read_text()))
cmd=[str(d/"usr/bin/perf"),"record","-e","cpu-clock:k","-F","499","--call-graph","fp","--tid",str(args.pid),"--no-inherit","--no-buildid","--no-buildid-cache","-o",str(prefix)+".perf.data"]
receipt=dict(command=cmd,target_pid=args.pid,started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
with Path(str(prefix)+".perf.stdout").open("x") as o,Path(str(prefix)+".perf.stderr").open("x") as e:
 p=subprocess.Popen(cmd,env=env,stdout=o,stderr=e)
 receipt["pid"]=p.pid
 Path(str(prefix)+".perf_started.json").write_text(json.dumps(receipt,indent=2))
 receipt["exit"]=p.wait()
receipt["terminal_utc"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
Path(str(prefix)+".perf_terminal.json").write_text(json.dumps(receipt,indent=2))
