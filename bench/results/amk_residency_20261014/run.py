import pathlib,os,json,subprocess,datetime,sys
t=pathlib.Path(__file__).parent;repo=pathlib.Path('/workspaces/repository');kind=sys.argv[1]
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
cfg=json.loads((t/'smol_frozen.json').read_text())
command=[str(t/'runtime/bin/python'),str(t/'residency_serving.py'),'--loop-comparison','--untraced','--reference-path',str(t/'frozen_references.json'),'--model',cfg['model'],'--output',str(t/(kind+'.jsonl'))]
if kind.startswith('preflight'):command+=['--preflight']
(t/(kind+'.command.json')).write_text(json.dumps(dict(command=command,cwd=str(repo),env_overrides=json.loads((t/'environment.json').read_text()),source=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()),indent=2))
with (t/(kind+'.driver.stdout')).open('x') as out,(t/(kind+'.driver.stderr')).open('x') as err:
 result=subprocess.run(command,cwd=repo,env=env,stdout=out,stderr=err)
(t/(kind+'.exit.json')).write_text(json.dumps(dict(exit=result.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
raise SystemExit(result.returncode)
