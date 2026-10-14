import pathlib,subprocess,json,datetime
p=pathlib.Path('/tmp/bpfusion-independent-batch-a3l3l2uo')
cmd=['python3', '/tmp/bpfusion-independent-batch-a3l3l2uo/run.py', 'preflight1']
with (p/'preflight1.stdout').open('x') as out,(p/'preflight1.stderr').open('x') as err:r=subprocess.run(cmd,stdout=out,stderr=err,cwd='/workspaces/repository')
(p/'preflight1.wrapper.exit.json').write_text(json.dumps(dict(command=cmd,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
