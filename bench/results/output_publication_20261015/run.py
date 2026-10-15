import pathlib,json,os,subprocess,datetime,sys
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository')
stage=sys.argv[1];assert stage in ['preflight','qualification','lifecycle','full']
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
models=json.loads((t/'frozen_references.json').read_text())['models']
get=lambda n:next(x['model'] for x in models.values() if ('SmolLM' if n=='smol' else 'Qwen') in x['model'])
commands=[]
if stage=='lifecycle':
 for name in ['smol','qwen']:
  for path in ['loop','native']:commands.append({'name':stage+'_'+name+'_'+path,'command':[str(t/'runtime/bin/python'),str(t/'lifecycle.py'),path,name]})
else:
 for name in (['qwen'] if stage=='preflight' else ['qwen','smol']):
  cmd=[str(t/'runtime/bin/python'),str(t/'serving.py'),'--model',get(name),'--loop-comparison','--output',str(t/(stage+'_'+name+'.jsonl'))]
  if stage=='qualification':cmd+=['--correctness']
  else:cmd+=['--untraced','--reference-path',str(t/'frozen_references.json')]
  if stage=='preflight':cmd+=['--preflight']
  commands.append({'name':stage+'_'+name,'command':cmd})
(t/(stage+'.commands.json')).write_text(json.dumps(commands,indent=2))
statuses=[]
for item in commands:
 key=item['name']
 with (t/(key+'.driver.stdout')).open('x') as out,(t/(key+'.driver.stderr')).open('x') as err:z=subprocess.run(item['command'],cwd=r,env=env,stdout=out,stderr=err)
 status={'name':key,'command':item['command'],'exit':z.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 if z.returncode==0 and stage!='lifecycle':
  cmd=['python3',str(t/'analysis.py'),str(t/(key+'.jsonl'))]
  with (t/(key+'.analysis.stdout')).open('x') as out,(t/(key+'.analysis.stderr')).open('x') as err:a=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
  status['analysis_command']=cmd;status['analysis_exit']=a.returncode
 if stage=='lifecycle' and z.returncode==0:
  p=t/('lifecycle_'+item['command'][-1]+'_'+item['command'][-2])/(item['command'][-1]+'.results.json')
  status['result_pass']=json.loads(p.read_text())['pass']
 statuses.append(status);(t/(stage+'.statuses.json')).write_text(json.dumps(statuses,indent=2))
 print('TERMINAL',key,json.dumps(status),flush=True)
 if z.returncode or status.get('analysis_exit',0) or not status.get('result_pass',True):break
ok=len(statuses)==len(commands) and all(x['exit']==0 and x.get('analysis_exit',0)==0 and x.get('result_pass',True) for x in statuses)
(t/(stage+'.exit.json')).write_text(json.dumps({'exit':0 if ok else 1,'completed':len(statuses),'expected':len(commands),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
raise SystemExit(0 if ok else 1)
