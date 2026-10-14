import pathlib,json,os,subprocess,datetime
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y');record=json.loads((r/'amk_build_status.json').read_text());env=dict(os.environ,**record['env_overrides'])
with (r/'native170_diagnostic.stdout').open('x') as out,(r/'native170_diagnostic.stderr').open('x') as err:p=subprocess.run(['/usr/bin/python3',str(r/'native170_diagnostic.py')],env=env,stdout=out,stderr=err)
(r/'native170_diagnostic.exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
