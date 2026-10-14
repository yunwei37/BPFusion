import pathlib,subprocess,json,datetime
p=pathlib.Path('/tmp/bpfusion-independent-batch-a3l3l2uo')
cmd=['python3', '/tmp/bpfusion-independent-batch-a3l3l2uo/run_qualification.py']
with (p/'qualification.stdout').open('x') as out,(p/'qualification.stderr').open('x') as err:r=subprocess.run(cmd,stdout=out,stderr=err,cwd='/workspaces/repository')
(p/'qualification.wrapper.exit.json').write_text(json.dumps(dict(command=cmd,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
