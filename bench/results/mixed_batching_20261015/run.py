from pathlib import Path
import subprocess,json,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
steps=[('preflight',['/usr/bin/python3',str(t/'preflight.py')]),
       ('qualification_qwen',['/usr/bin/python3',str(t/'qualification.py'),'qwen']),
       ('qualification_smol',['/usr/bin/python3',str(t/'qualification.py'),'smol']),
       ('full',['/usr/bin/python3',str(t/'full.py')])]
statuses=[]
for tag,cmd in steps:
 print('START',tag,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 with (t/(tag+'.wrapper.stdout')).open('x') as out,(t/(tag+'.wrapper.stderr')).open('x') as err:
  z=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
 rec=dict(stage=tag,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 statuses.append(rec);(t/'run.statuses.json').write_text(json.dumps(statuses,indent=2))
 print('TERMINAL',json.dumps(rec),flush=True)
 if z.returncode:break
ok=len(statuses)==len(steps) and all(x['exit']==0 for x in statuses)
(t/'run.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),completed=len(statuses),expected=len(steps)),indent=2))
raise SystemExit(0 if ok else 1)
