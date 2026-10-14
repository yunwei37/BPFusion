import pathlib,os,json,subprocess,datetime
t=pathlib.Path(__file__).parent;repo=pathlib.Path('/workspaces/repository');os.chdir(repo)
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
command=['make','build/amk_graph_uring_loop.so','build/vllm_graph_uring_loop.so','VLLM_PYTHON='+str(t/'runtime/bin/python')]
with (t/'legacy_build.stdout').open('x') as out,(t/'legacy_build.stderr').open('x') as err:r=subprocess.run(command,env=env,stdout=out,stderr=err)
(t/'legacy_build.exit.json').write_text(json.dumps(dict(command=command,exit=r.returncode),indent=2))
if r.returncode:raise SystemExit(r.returncode)
asset=json.loads((t/'frozen_references.json').read_text());status=[]
for name,backend,model in [('amk_smol','amk',asset['models']['smol']['model']),('vllm_smol','vllm',asset['models']['smol']['model']),('vllm_qwen','vllm',asset['models']['qwen']['model'])]:
 prefix='legacy_compat_'+name
 command=[str(t/'runtime/bin/python'),str(t/'legacy_compat.py'),'--backend',backend,'--preflight','--loop-comparison','--untraced','--reference-path',str(t/'frozen_references.json'),'--model',model,'--output',str(t/(prefix+'.jsonl'))]
 with (t/(prefix+'.driver.stdout')).open('x') as out,(t/(prefix+'.driver.stderr')).open('x') as err:r=subprocess.run(command,env=env,stdout=out,stderr=err)
 status.append(dict(command=command,exit=r.returncode));print('LEGACY_TERMINAL',name,r.returncode,flush=True)
 if r.returncode:
  (t/'legacy_compat.exit.json').write_text(json.dumps(dict(exit=r.returncode,status=status)))
  raise SystemExit(r.returncode)
(t/'legacy_compat.exit.json').write_text(json.dumps(dict(exit=0,status=status,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
