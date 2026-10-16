from pathlib import Path
import subprocess,os,json,gzip,sys
t=Path(__file__).parent;r=Path("/workspaces/repository");directory=Path(sys.argv[1]);stage=directory.name
a=r/"bench/results/kernel_cpu_profile_20261016"/stage;a.mkdir(exist_ok=True)
env=dict(os.environ,**json.loads((t/"perf_runtime/environment.json").read_text()),PAGER="cat",PERF_PAGER="cat",LC_ALL="C")
perf=str(t/"perf_runtime/usr/bin/perf")
for data in directory.glob("*.perf.data"):
 prefix=str(data).removesuffix(".perf.data")
 commands=[
  ("perf_self.txt",["report","--stdio","--no-children","--call-graph","none","--percent-limit","0","-i",str(data)]),
  ("perf_children.txt",["report","--stdio","--children","--call-graph","none","--percent-limit","0","-i",str(data)]),
  ("perf_script.txt",["script","-F","comm,pid,tid,time,period,event,ip,sym,dso","-i",str(data)]),
  ("perf_header.txt",["report","--stdio","--header-only","-i",str(data)]),
  ("perf_dump.txt",["script","-D","-i",str(data)])]
 records=[]
 for suffix,args in commands:
  with Path(prefix+"."+suffix).open("x") as o,Path(prefix+"."+suffix+".stderr").open("x") as e:
   z=subprocess.run([perf,*args],env=env,stdout=o,stderr=e)
  records.append(dict(command=[perf,*args],exit=z.returncode))
  assert z.returncode==0,records[-1]
 Path(prefix+".decode.json").write_text(json.dumps(records,indent=2))
for f in directory.iterdir():
 if not f.is_file():continue
 raw=f.read_bytes()
 if f.name.endswith(".gz"):(a/f.name).write_bytes(raw)
 elif len(raw)>100000 or f.name.endswith((".perf.data",".jsonl")):
  (a/(f.name+".gz")).write_bytes(gzip.compress(raw,mtime=0))
 else:(a/f.name).write_bytes(raw)
cmd=["/usr/bin/python3",str(t/"cpu_profile_analysis.py"),str(a)]
if "preflight" in stage:cmd+=["--preflight"]
with (a/"analysis.stdout").open("x") as o,(a/"analysis.stderr").open("x") as e:z=subprocess.run(cmd,stdout=o,stderr=e)
(a/"analysis_exit.json").write_text(json.dumps(dict(command=cmd,exit=z.returncode)))
assert z.returncode==0
print("archived",stage,len(list(a.iterdir())),flush=True)
