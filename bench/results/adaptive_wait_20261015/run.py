import pathlib,os,subprocess,json,datetime,sys
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository')
stage=sys.argv[1];assert stage in ['setup','preflight','qualification','qualification_repaired','full']
env=dict(os.environ,**(json.loads((t/'environment.json').read_text()) if (t/'environment.json').exists() else {}));env.pop('VLLM_BATCH_INVARIANT',None)
py=str(t/'runtime/bin/python');commands=[]
if stage=='setup':commands=[dict(name='setup',command=['/usr/bin/python3',str(t/'setup.py')])]
else:
 models=json.loads((t/'models.json').read_text())
 if stage=='preflight':commands.append(dict(name='idle_deadline',command=['/usr/bin/python3',str(t/'idle_deadline.py')]))
 for model in (['qwen'] if stage=='preflight' else ['qwen','smol']):
  cmd=[py,str(t/'serving.py'),'--model',models[model],'--loop-comparison','--output',str(t/(stage+'_'+model+'.jsonl'))]
  if stage.startswith('qualification'):cmd+=['--correctness']
  if stage=='preflight':cmd+=['--preflight']
  commands.append(dict(name=stage+'_'+model,command=cmd))
  if stage.startswith('qualification'):commands.append(dict(name=('lifecycle_repaired_' if stage=='qualification_repaired' else 'lifecycle_')+model,command=[py,str(t/('lifecycle_repaired.py' if stage=='qualification_repaired' else 'lifecycle.py')),'loop',model]))
(t/(stage+'.commands.json')).write_text(json.dumps(commands,indent=2));statuses=[]
for item in commands:
 key=item['name'];print('START',key,flush=True)
 with (t/(key+'.driver.stdout')).open('x') as out,(t/(key+'.driver.stderr')).open('x') as err:z=subprocess.run(item['command'],cwd=r,env=env,stdout=out,stderr=err)
 status=dict(name=key,command=item['command'],exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if key.startswith('lifecycle_'):
  model=key.rsplit('_',1)[-1];p=t/(('lifecycle_repaired_' if stage=='qualification_repaired' else 'lifecycle_')+model+'_loop')/(model+'.results.json')
  status['lifecycle_pass']=p.exists() and json.loads(p.read_text()).get('pass') is True
 if key.startswith(stage+'_') and z.returncode==0:
  cmd=['/usr/bin/python3',str(t/'analysis.py'),str(t/(key+'.jsonl'))]
  with (t/(key+'.analysis.stdout')).open('x') as out,(t/(key+'.analysis.stderr')).open('x') as err:a=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
  status.update(analysis_command=cmd,analysis_exit=a.returncode)
 statuses.append(status);(t/(stage+'.statuses.json')).write_text(json.dumps(statuses,indent=2));print('TERMINAL',json.dumps(status),flush=True)
 if z.returncode or status.get('analysis_exit',0) or status.get('lifecycle_pass') is False:break
ok=len(statuses)==len(commands) and all(x['exit']==0 and x.get('analysis_exit',0)==0 and x.get('lifecycle_pass',True) for x in statuses)
(t/(stage+'.exit.json')).write_text(json.dumps(dict(exit=0 if ok else 1,completed=len(statuses),expected=len(commands),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(0 if ok else 1)
