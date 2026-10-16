from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path("/workspaces/repository")
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
build=t/"controller_stage_build16"
cmd=["make","-f",str(t/"controller_stage.Makefile"),"BUILD="+str(build),
     "CPPFLAGS=-DBF_LLM_SLOTS=16 -I/workspaces/repository/executor",
     "VLLM_PYTHON="+str(t/"runtime/bin/python"),"vllm-mixed-trace",
     str(build/"bpfusion_load"),str(build/"fusion.bpf.o")]
with (t/"controller_stage_build_r1.stdout").open("x") as o,(t/"controller_stage_build_r1.stderr").open("x") as e:
 z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
(t/"controller_stage_build_r1.exit.json").write_text(json.dumps(dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(z.returncode)
