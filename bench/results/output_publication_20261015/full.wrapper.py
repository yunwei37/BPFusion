import pathlib,subprocess,json,datetime
t=pathlib.Path(__file__).parent;stage='full'
with (t/(stage+'.stdout')).open('x') as out,(t/(stage+'.stderr')).open('x') as err:z=subprocess.run(['python3',str(t/'run.py'),stage],stdout=out,stderr=err)
(t/(stage+'.wrapper.exit.json')).write_text(json.dumps({'exit':z.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
