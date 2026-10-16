from pathlib import Path
import subprocess,json,os,shlex,time,datetime
t=Path(__file__).resolve().parent;r=Path("/workspaces/repository");src=t/"reclamation_source"
while not (t/"reclaim_preflight/reclaim_preflight_p0_global.server_terminal.json").exists():time.sleep(.2)
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
original=(t/"reclaim_make16.txt").read_text().replace(chr(92)+"\n"," ")
statuses=[]
for condition,banks in [("local",8),("local",16),("global",16)]:
 b=t/("verified_reclaim_"+condition+str(banks));b.mkdir()
 for line in original.splitlines():
  if not line.strip():continue
  line=line.replace(str(t/"reclaim_local16"),str(b))
  if banks==8:line=line.replace("-DBF_LLM_SLOTS=16","")
  cmd=shlex.split(line)
  if condition=="global" and any("vllm_mixed" in x and ("trace" in x or "user_network" in x) for x in cmd):continue
  if cmd[0] in ["clang","cc","/usr/local/cuda/bin/nvcc"] and ("-c" in cmd or "-dc" in cmd) or cmd[0]=="cc":
   if "-Ibpf/include" in cmd:
    i=cmd.index("-Ibpf/include");cmd[i:i]=["-I"+str(src),"-I"+str(r/"executor")]
   if condition=="global":cmd.insert(1,"-DBF_IO_GLOBAL_PENDING_GUARD")
   for i,x in enumerate(cmd):
    mapping={"bpf/fusion.bpf.c":"fusion.bpf.c","bpf/uring_loop.bpf.c":"uring_loop.bpf.c","tools/bpfusion_load.c":"bpfusion_load.c","executor/vllm_mixed.cu":"vllm_mixed.cu"}
    if x in mapping:cmd[i]=str(src/mapping[x])
  print("BUILD",condition,banks,cmd[-1],flush=True)
  with (b/"build.stdout").open("a") as o,(b/"build.stderr").open("a") as e:z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
  statuses.append(dict(condition=condition,banks=banks,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
  (t/"verified_reclaim_build.statuses.json").write_text(json.dumps(statuses,indent=2))
  if z.returncode:raise RuntimeError((b/"build.stderr").read_text()[-4000:])
(t/"verified_reclaim_build.exit.json").write_text(json.dumps(dict(exit=0)))
