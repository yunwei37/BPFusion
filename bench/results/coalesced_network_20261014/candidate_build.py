import pathlib,os,json,subprocess,datetime
repo=pathlib.Path('/workspaces/repository');os.chdir(repo);t=pathlib.Path(__file__).parent
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
command=['make','amk-graph-uring-coalesced','vllm-graph-uring-coalesced','AMK_PYTHON='+str(t/'runtime/bin/python'),'VLLM_PYTHON='+str(t/'runtime/bin/python')]
with (t/'candidate_build.stdout').open('x') as out,(t/'candidate_build.stderr').open('x') as err:r=subprocess.run(command,env=env,stdout=out,stderr=err)
(t/'candidate_build.exit.json').write_text(json.dumps(dict(command=command,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(r.returncode)
