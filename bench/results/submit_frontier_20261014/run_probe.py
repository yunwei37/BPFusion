import pathlib,os,json,subprocess,datetime
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
asset=json.loads((t/'frozen_references.json').read_text());commands=[]
for label in ['SmolLM','Qwen']:
 model=next(v['model'] for v in asset['models'].values() if label in v['model'])
 for condition in ['ordinary','trace']:
  prefix='probe_'+label.lower()+'_'+condition
  cmd=[str(t/'runtime/bin/python'),str(t/'probe_serving.py'),'--backend','vllm','--block','0','--loop-comparison','--reference-path',str(t/'frozen_references.json'),'--model',model,'--output',str(t/(prefix+'.jsonl'))]
  if condition=='ordinary':cmd+=['--untraced']
  commands.append(dict(command=cmd,condition=condition,model=model))
  with (t/(prefix+'.driver.stdout')).open('x') as out,(t/(prefix+'.driver.stderr')).open('x') as err:
   r=subprocess.run(cmd,env=env,stdout=out,stderr=err)
  (t/(prefix+'.exit.json')).write_text(json.dumps(dict(exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
  print('PROBE_TERMINAL',prefix,r.returncode,flush=True)
  if r.returncode:
   (t/'probe.exit.json').write_text(json.dumps(dict(exit=r.returncode,commands=commands),indent=2));raise SystemExit(r.returncode)
(t/'probe.exit.json').write_text(json.dumps(dict(exit=0,commands=commands,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
