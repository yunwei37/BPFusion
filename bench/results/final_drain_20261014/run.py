import pathlib,os,json,subprocess,datetime,sys
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
kind=sys.argv[1];assert kind in ['preflight1','preflight2','preflight3','full']
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
asset=json.loads((t/'frozen_references.json').read_text())
models=[('smol',next(v['model'] for v in asset['models'].values() if 'SmolLM' in v['model'])),('qwen',next(v['model'] for v in asset['models'].values() if 'Qwen' in v['model']))]
commands=[]
for block in range(1 if kind.startswith('preflight') else 5):
 for subset in (['short','transfer'] if block%2==0 else ['transfer','short']):
  for name,model in (models if block%2==0 else models[::-1]):
   prefix=kind+'_'+subset+'_'+name+'_b'+str(block)
   command=[str(t/'runtime/bin/python'),str(t/(subset+'_serving.py')),'--backend','vllm','--block',str(block),'--loop-comparison','--untraced','--reference-path',str(t/'frozen_references.json'),'--model',model,'--output',str(t/(prefix+'.jsonl'))]
   if kind.startswith('preflight'):command+=['--preflight']
   commands.append(dict(command=command,model=name,backend='vllm',block=block,subset=subset,output=prefix+'.jsonl'))
(t/(kind+'.commands.json')).write_text(json.dumps(commands,indent=2))
for item in commands:
 prefix=pathlib.Path(item['output']).stem;command=item['command']
 with (t/(prefix+'.driver.stdout')).open('x') as out,(t/(prefix+'.driver.stderr')).open('x') as err:
  result=subprocess.run(command,env=env,stdout=out,stderr=err)
 (t/(prefix+'.exit.json')).write_text(json.dumps(dict(exit=result.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
 print('DRIVER_TERMINAL',prefix,result.returncode,flush=True)
 if result.returncode:
  (t/(kind+'.exit.json')).write_text(json.dumps(dict(exit=result.returncode,failed=prefix,commands=commands),indent=2));raise SystemExit(result.returncode)
(t/(kind+'.exit.json')).write_text(json.dumps(dict(exit=0,commands=commands,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
