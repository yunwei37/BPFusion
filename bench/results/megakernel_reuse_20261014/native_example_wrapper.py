import pathlib,subprocess,json,datetime,os
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y')
record=json.loads((r/'native_example_command.json').read_text())
env=dict(os.environ,**record['env_overrides'])
with (r/'native_example.stdout').open('w') as out,(r/'native_example.stderr').open('w') as err:
 p=subprocess.run(record['command'],cwd=record['cwd'],env=env,stdout=out,stderr=err)
(r/'native_example.exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
