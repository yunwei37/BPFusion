from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path("/workspaces/repository");d=t/"official_full";d.mkdir()
assert json.loads((t/"official_preflight2.exit.json").read_text())["analysis_exit"]==0
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
cmd=[str(t/"runtime/bin/python"),str(t/"official_reference.py"),"--output",str(d/"full.jsonl")]
print("START full",flush=True)
with (d/"full.stdout").open("x") as o,(d/"full.stderr").open("x") as e:z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
rec=dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
if z.returncode==0:
 ac=["/usr/bin/python3",str(t/"official_analysis.py"),str(d/"full.jsonl")]
 with (d/"full.analysis.stdout").open("x") as o,(d/"full.analysis.stderr").open("x") as e:az=subprocess.run(ac,cwd=r,stdout=o,stderr=e)
 rec.update(analysis_command=ac,analysis_exit=az.returncode)
(t/"official_full.exit.json").write_text(json.dumps(rec,indent=2));print("TERMINAL",rec,flush=True)
