import pathlib,os,json,subprocess,datetime
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
status=[]
for name,backend in [('smol','vllm'),('qwen','vllm')]:
 command=[str(t/'runtime/bin/python'),str(t/'lifecycle.py'),'loop',name,backend]
 key='lifecycle_'+backend+'_'+name
 with (t/(key+'.driver.stdout')).open('x') as out,(t/(key+'.driver.stderr')).open('x') as err:
  result=subprocess.run(command,env=env,stdout=out,stderr=err)
 doc=json.loads((t/key/(name+'.results.json')).read_text())
 status.append(dict(command=command,exit=result.returncode,pass_checks=doc['pass']))
 (t/'lifecycle.status.json').write_text(json.dumps(status,indent=2))
 if result.returncode or not doc['pass']:
  (t/'lifecycle.exit.json').write_text(json.dumps(dict(exit=1,status=status)))
  raise SystemExit(1)
(t/'lifecycle.exit.json').write_text(json.dumps(dict(exit=0,status=status,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
