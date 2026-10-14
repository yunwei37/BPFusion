import pathlib,json,os,subprocess,datetime
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y');repo=pathlib.Path('/workspaces/repository');record=json.loads((r/'common_build_status.json').read_text());env=dict(os.environ,**record['env_overrides'],BF_BIND='127.0.0.1',PYTHONUNBUFFERED='1')
status=[]
for condition in ['native','loop']:
 cmd=[str(r/'common_runtime/bin/python'),str(r/'amk_lifecycle2.py'),condition]
 with (r/('amk_lifecycle2_'+condition+'.stdout')).open('x') as out,(r/('amk_lifecycle2_'+condition+'.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
 result=json.loads((r/('amk_lifecycle2_'+condition)/'smol.results.json').read_text());status.append({'condition':condition,'exit':p.returncode,'pass':result['pass'],'command':cmd,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});(r/'amk_lifecycle2_status.json').write_text(json.dumps(status,indent=2))
 if p.returncode or not result['pass']:raise SystemExit(1)
(r/'amk_lifecycle2.exit.json').write_text(json.dumps({'exit':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
