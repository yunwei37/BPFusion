import pathlib,subprocess,json,datetime,os
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y')
record=json.loads((r/'fp16_probe_command.json').read_text())
env=dict(os.environ,**record['env_overrides'])
with (r/'fp16_probe.stdout').open('w') as out,(r/'fp16_probe.stderr').open('w') as err:
 p=subprocess.run(record['command'],cwd=record['cwd'],env=env,stdout=out,stderr=err)
(r/'fp16_probe.exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
