from pathlib import Path
import subprocess,json,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
statuses=[]
for name in ['setup','qualification','preflight','full']:
 cmd=['/usr/bin/python3','-u',str(t/(name+'.py'))]
 print('START',name,flush=True)
 with (t/(name+'.wrapper.stdout')).open('x') as out,(t/(name+'.wrapper.stderr')).open('x') as err:
  p=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
 x=dict(stage=name,command=cmd,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 statuses.append(x);(t/'all.statuses.json').write_text(json.dumps(statuses,indent=2));print('TERMINAL',json.dumps(x),flush=True)
 if p.returncode:break
ok=len(statuses)==4 and all(x['exit']==0 for x in statuses)
(t/'all.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,completed=len(statuses),expected=4,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(0 if ok else 1)
