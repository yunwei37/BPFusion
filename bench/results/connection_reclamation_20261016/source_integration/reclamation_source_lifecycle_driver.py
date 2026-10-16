from pathlib import Path
import subprocess,json,os
t=Path(__file__).parent
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
out=[]
for condition in ["loop","native"]:
 with (t/("reclamation_source_lifecycle_"+condition+".stdout")).open("x") as o,(t/("reclamation_source_lifecycle_"+condition+".stderr")).open("x") as e:
  z=subprocess.run(["python3",str(t/"reclamation_source_ordinary_lifecycle.py"),condition,"qwen","8","vllm"],env=env,stdout=o,stderr=e)
 out.append(dict(condition=condition,exit=z.returncode))
 (t/"reclamation_source_lifecycle.statuses.json").write_text(json.dumps(out,indent=2))
(t/"reclamation_source_lifecycle.exit.json").write_text(json.dumps(dict(exit=0 if all(x["exit"]==0 for x in out) else 1)))
