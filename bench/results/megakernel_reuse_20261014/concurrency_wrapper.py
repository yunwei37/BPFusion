import pathlib,json,subprocess,datetime
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y')
for condition in ['native','loop']:
 key='concurrency_'+condition
 with (r/(key+'.driver.stdout')).open('x') as out,(r/(key+'.driver.stderr')).open('x') as err:
  p=subprocess.run(['/usr/bin/python3',str(r/'concurrency_case.py'),condition],stdout=out,stderr=err)
 (r/(key+'.exit.json')).write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
 if p.returncode:raise SystemExit(p.returncode)
