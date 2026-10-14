import pathlib,os,json,subprocess,datetime,sys
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
kind=sys.argv[1];assert kind in ['preflight1','preflight2','preflight3','full']
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
asset=json.loads((t/'frozen_references.json').read_text())
smol=next(v['model'] for v in asset['models'].values() if 'SmolLM' in v['model'])
qwen=next(v['model'] for v in asset['models'].values() if 'Qwen' in v['model'])
models=[('amk_smol','amk',smol),('vllm_smol','vllm',smol),('vllm_qwen','vllm',qwen)]
commands=[]
for block in range(1 if kind.startswith('preflight') else 5):
 for name,backend,model in (models if block%2==0 else models[::-1]):
  prefix=kind+'_'+name+'_b'+str(block)
  command=[str(t/'runtime/bin/python'),str(t/'matched_serving.py'),'--backend',backend,'--block',str(block),'--loop-comparison','--untraced','--reference-path',str(t/'frozen_references.json'),'--model',model,'--output',str(t/(prefix+'.jsonl'))]
  if kind.startswith('preflight'):command+=['--preflight']
  commands.append(dict(command=command,model=name,backend=backend,block=block,output=prefix+'.jsonl'))
  with (t/(prefix+'.driver.stdout')).open('x') as out,(t/(prefix+'.driver.stderr')).open('x') as err:
   result=subprocess.run(command,env=env,stdout=out,stderr=err)
  (t/(prefix+'.exit.json')).write_text(json.dumps(dict(exit=result.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
  print('DRIVER_TERMINAL',prefix,result.returncode,flush=True)
  if result.returncode:
   (t/(kind+'.exit.json')).write_text(json.dumps(dict(exit=result.returncode,failed=prefix,commands=commands)))
   raise SystemExit(result.returncode)
(t/(kind+'.exit.json')).write_text(json.dumps(dict(exit=0,commands=commands,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
