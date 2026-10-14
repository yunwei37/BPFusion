import pathlib,json,subprocess,datetime,os
d=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y/device_graph')
rec=json.loads((d/'command.json').read_text())
with (d/'stdout').open('w') as out,(d/'stderr').open('w') as err:
 p=subprocess.run(rec['command'],cwd=rec['cwd'],env=dict(os.environ,**rec['env_overrides']),stdout=out,stderr=err)
(d/'exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
