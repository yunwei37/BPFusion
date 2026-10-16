from pathlib import Path
import subprocess,json,os,datetime
d=Path(__file__).resolve().parent;t=d.parent;r=Path("/workspaces/repository")
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
assert subprocess.check_output(["git","symbolic-ref","--short","HEAD"],cwd=r,text=True).strip()=="main"
statuses=[]
for banks in [8,16]:
 build=t/("kernel_owned_build"+str(banks))
 cmd=["make","-f",str(d/"Makefile"),"BUILD="+str(build),
      "CPPFLAGS=-DBF_LLM_SLOTS="+str(banks)+" -I"+str(d)+" -I/workspaces/repository/executor",
      "VLLM_PYTHON="+str(t/"runtime/bin/python"),"vllm-mixed-uring-loop",
      "vllm-mixed-user-network-wait","vllm-mixed-trace",
      str(build/"bpfusion_load"),str(build/"fusion.bpf.o")]
 with (d/("build"+str(banks)+".stdout")).open("x") as out,(d/("build"+str(banks)+".stderr")).open("x") as err:
  p=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 statuses.append(dict(banks=banks,command=cmd,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 (d/"build.statuses.json").write_text(json.dumps(statuses,indent=2))
 if p.returncode:break
raise SystemExit(0 if len(statuses)==2 and all(x["exit"]==0 for x in statuses) else 1)
