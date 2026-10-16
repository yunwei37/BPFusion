from pathlib import Path
import json,subprocess,time,os
t=Path(__file__).resolve().parent
while not (t/"reclaim_acceptance.exit.json").exists():time.sleep(.2)
assert json.loads((t/"reclaim_acceptance.exit.json").read_text())["exit"]==0
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
statuses=[]
for name,args in [("collision",[str(t/"runtime/bin/python"),str(t/"reclaim_collision.py"),"loop","qwen","8","vllm"]),("generic",[str(t/"runtime/bin/python"),str(t/"reclaim_graph_acceptance.py")])]:
 print("START",name,flush=True)
 with (t/("reclaim_extra_"+name+".stdout")).open("x") as o,(t/("reclaim_extra_"+name+".stderr")).open("x") as e:
  z=subprocess.run(args,cwd="/workspaces/repository",env=env,stdout=o,stderr=e)
 if name=="collision":
  value=json.loads((t/"collision_reclaim_vllm_qwen_8_loop/qwen.results.json").read_text())
  passed=value.get("pass",False)
 else:passed=z.returncode==0
 statuses.append(dict(name=name,command=args,exit=z.returncode,passed=passed))
 (t/"reclaim_extra_qualification.statuses.json").write_text(json.dumps(statuses,indent=2))
 print("TERMINAL",statuses[-1],flush=True)
 if z.returncode or not passed:break
(t/"reclaim_extra_qualification.exit.json").write_text(json.dumps(dict(exit=0 if len(statuses)==2 and all(x["exit"]==0 and x["passed"] for x in statuses) else 1)))
