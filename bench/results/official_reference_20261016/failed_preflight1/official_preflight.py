from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path("/workspaces/repository");d=t/"official";d.mkdir()
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
cmd=[str(t/"runtime/bin/python"),str(t/"official_reference.py"),"--output",str(d/"preflight.jsonl"),"--preflight"]
with (d/"preflight.stdout").open("x") as o,(d/"preflight.stderr").open("x") as e:z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
rec=dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
if z.returncode==0:
 ac=["/usr/bin/python3",str(t/"official_analysis.py"),str(d/"preflight.jsonl")]
 with (d/"preflight.analysis.stdout").open("x") as o,(d/"preflight.analysis.stderr").open("x") as e:az=subprocess.run(ac,cwd=r,stdout=o,stderr=e)
 rec.update(analysis_command=ac,analysis_exit=az.returncode)
(t/"official_preflight.exit.json").write_text(json.dumps(rec,indent=2))
