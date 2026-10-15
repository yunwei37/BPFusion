import pathlib,os,subprocess,json,datetime,sys
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository')
stage=sys.argv[1];assert stage in ['setup','reference','preflight','qualification','full']
env=dict(os.environ,**(json.loads((t/'environment.json').read_text()) if (t/'environment.json').exists() else {}))
py=str(t/'runtime/bin/python')
commands=[]
if stage=='setup':commands=[dict(name='setup',command=['/usr/bin/python3',str(t/'setup.py')])]
elif stage=='reference':
 for model in ['qwen','smol']:commands.append(dict(name='reference_'+model,command=[py,str(t/'reference.py'),model]))
else:
 asset=json.loads((t/'frozen_references.json').read_text())
 for model in (['qwen'] if stage=='preflight' else ['qwen','smol']):
  cmd=[py,str(t/'serving.py'),'--model',asset['models'][model]['model'],'--loop-comparison','--reference-path',str(t/'frozen_references.json'),'--output',str(t/(stage+'_'+model+'.jsonl'))]
  if stage=='qualification':cmd+=['--correctness']
  else:cmd+=['--untraced']
  if stage=='preflight':cmd+=['--preflight']
  commands.append(dict(name=stage+'_'+model,command=cmd))
(t/(stage+'.commands.json')).write_text(json.dumps(commands,indent=2))
statuses=[]
for item in commands:
 key=item['name'];print('START',key,flush=True)
 with (t/(key+'.driver.stdout')).open('x') as out,(t/(key+'.driver.stderr')).open('x') as err:z=subprocess.run(item['command'],cwd=r,env=env,stdout=out,stderr=err)
 status=dict(name=key,command=item['command'],exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if stage in ['preflight','qualification','full'] and z.returncode==0:
  cmd=['/usr/bin/python3',str(t/'analysis.py'),str(t/(key+'.jsonl'))]
  with (t/(key+'.analysis.stdout')).open('x') as out,(t/(key+'.analysis.stderr')).open('x') as err:a=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
  status.update(analysis_command=cmd,analysis_exit=a.returncode)
 statuses.append(status);(t/(stage+'.statuses.json')).write_text(json.dumps(statuses,indent=2));print('TERMINAL',json.dumps(status),flush=True)
 if z.returncode or status.get('analysis_exit',0):break
ok=len(statuses)==len(commands) and all(x['exit']==0 and x.get('analysis_exit',0)==0 for x in statuses)
if stage=='reference' and ok:
 asset=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_commit='3cb7685f368195a1d398ca9639a143df99e64a28',models={model:json.loads((t/(model+'.frozen.json')).read_text()) for model in ['qwen','smol']},precision='fp16',scope='exactly one independently generated official same-mode sequence per prompt; official widths1..8 forward/reverse checked before BPFusion observation')
 (t/'frozen_references.json').write_text(json.dumps(asset,indent=2))
(t/(stage+'.exit.json')).write_text(json.dumps(dict(exit=0 if ok else 1,completed=len(statuses),expected=len(commands),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(0 if ok else 1)
