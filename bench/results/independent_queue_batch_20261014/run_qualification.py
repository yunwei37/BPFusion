import pathlib,os,json,subprocess,datetime,sys
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
asset=json.loads((t/'frozen_references.json').read_text())
smol=next(v['model'] for v in asset['models'].values() if 'SmolLM' in v['model'])
qwen=next(v['model'] for v in asset['models'].values() if 'Qwen' in v['model'])
commands=[]
for name,backend,model in [('vllm_smol','vllm',smol),('vllm_qwen','vllm',qwen)]:
 prefix='qualification_'+name
 command=[str(t/'runtime/bin/python'),str(t/'qualification.py'),'--backend',backend,'--loop-comparison','--correctness','--reference-path',str(t/'frozen_references.json'),'--model',model,'--output',str(t/(prefix+'.jsonl'))]
 if backend=='amk':command+=['--untraced']
 commands.append(dict(command=command,name=name))
 with (t/(prefix+'.driver.stdout')).open('x') as out,(t/(prefix+'.driver.stderr')).open('x') as err:
  result=subprocess.run(command,env=env,stdout=out,stderr=err)
 (t/(prefix+'.exit.json')).write_text(json.dumps(dict(exit=result.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
 print('QUALIFICATION_TERMINAL',prefix,result.returncode,flush=True)
 if result.returncode:
  (t/'qualification.exit.json').write_text(json.dumps(dict(exit=result.returncode,commands=commands)))
  raise SystemExit(result.returncode)
(t/'qualification.exit.json').write_text(json.dumps(dict(exit=0,commands=commands),indent=2))
