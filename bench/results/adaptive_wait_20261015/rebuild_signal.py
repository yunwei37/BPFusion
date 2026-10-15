import pathlib,subprocess,json,datetime,os
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()));env.pop('VLLM_BATCH_INVARIANT',None)
cmd=json.loads((t/'candidate_build_status.json').read_text())['command']
with (t/'candidate_signal_rebuild.stdout').open('x') as out,(t/'candidate_signal_rebuild.stderr').open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
(t/'candidate_signal_rebuild_status.json').write_text(json.dumps(dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(z.returncode)
