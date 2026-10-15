import pathlib,subprocess,json,datetime
t=pathlib.Path(__file__).parent
with (t/'setup.stdout').open('x') as out,(t/'setup.stderr').open('x') as err:z=subprocess.run(['python3',str(t/'setup.py')],stdout=out,stderr=err)
(t/'setup.wrapper.exit.json').write_text(json.dumps({'exit':z.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
