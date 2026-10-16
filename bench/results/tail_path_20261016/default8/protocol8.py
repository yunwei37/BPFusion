from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()));models=json.loads((t/'models.json').read_text())
statuses=[]
for name in ['qwen','smol']:
 cmd=[str(t/'runtime/bin/python'),str(t/'load.py'),'--model',models[name],'--output',str(t/(name+'_protocol8.jsonl')),'--correctness','--banks','8']
 print('START',name,flush=True)
 with (t/(name+'_protocol8.stdout')).open('x') as out,(t/(name+'_protocol8.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 rec=dict(name=name,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if z.returncode==0:
  ac=['/usr/bin/python3',str(t/'protocol_analysis.py'),str(t/(name+'_protocol8.jsonl'))]
  with (t/(name+'_protocol8.analysis.stdout')).open('x') as out,(t/(name+'_protocol8.analysis.stderr')).open('x') as err:az=subprocess.run(ac,cwd=r,stdout=out,stderr=err)
  rec.update(analysis=ac,analysis_exit=az.returncode)
 statuses.append(rec);(t/'protocol8.statuses.json').write_text(json.dumps(statuses,indent=2));print('TERMINAL',rec,flush=True)
 if z.returncode or rec.get('analysis_exit',0):break
ok=len(statuses)==2 and all(x['exit']==0 and x.get('analysis_exit',0)==0 for x in statuses)
(t/'protocol8.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
