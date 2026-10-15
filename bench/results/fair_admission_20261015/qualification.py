from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
models=json.loads((t/'models.json').read_text());py=str(t/'runtime/bin/python')
commands=[('idle_native',['/usr/bin/python3',str(t/'idle_native.py')])]
for name in ['qwen','smol']:
 commands += [('protocol_'+name,[py,str(t/'load.py'),'--model',models[name],'--correctness','--output',str(t/('protocol_'+name+'.jsonl'))]),
              ('lifecycle_'+name+'_native',[py,str(t/'lifecycle.py'),'native',name])]
(t/'qualification.commands.json').write_text(json.dumps(commands,indent=2));statuses=[]
for name,cmd in commands:
 print('START',name,flush=True)
 with (t/(name+'.driver.stdout')).open('x') as out,(t/(name+'.driver.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 x=dict(name=name,command=cmd,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if name.startswith('protocol_') and p.returncode==0:
  analysis=['/usr/bin/python3',str(t/'protocol_analysis.py'),str(t/(name+'.jsonl'))]
  with (t/(name+'.analysis.stdout')).open('x') as out,(t/(name+'.analysis.stderr')).open('x') as err:q=subprocess.run(analysis,cwd=r,stdout=out,stderr=err)
  x.update(analysis_exit=q.returncode)
 if name.startswith('lifecycle_'):
  model=name.split('_')[1];f=t/name/(model+'.results.json');x['lifecycle_pass']=f.exists() and json.loads(f.read_text()).get('pass') is True
 statuses.append(x);(t/'qualification.statuses.json').write_text(json.dumps(statuses,indent=2));print('DONE',json.dumps(x),flush=True)
 if x['exit'] or x.get('analysis_exit',0) or x.get('lifecycle_pass') is False:break
ok=len(statuses)==len(commands) and all(x['exit']==0 and x.get('analysis_exit',0)==0 and x.get('lifecycle_pass',True) for x in statuses)
(t/'qualification.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,completed=len(statuses),expected=len(commands),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(0 if ok else 1)
