import pathlib,json,subprocess,datetime
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y')
with (r/'preflight_native.driver.stdout').open('w') as out,(r/'preflight_native.driver.stderr').open('w') as err:
 p=subprocess.run(['/usr/bin/python3',str(r/'server_case.py'),'native'],stdout=out,stderr=err)
(r/'preflight_native.exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
