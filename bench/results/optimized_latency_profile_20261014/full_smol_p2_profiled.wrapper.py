import pathlib,subprocess,json,datetime
r=pathlib.Path('/tmp/bpfusion-optimized-latency-profile-bk8ztoin')
cmd=['/usr/bin/python3',str(r/'case.py'),'smol','2','profiled','full']
with (r/'full_smol_p2_profiled.driver.stdout').open('w') as out,(r/'full_smol_p2_profiled.driver.stderr').open('w') as err:
 p=subprocess.run(cmd,stdout=out,stderr=err)
(r/'full_smol_p2_profiled.exit.json').write_text(json.dumps({'cmd':cmd,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
