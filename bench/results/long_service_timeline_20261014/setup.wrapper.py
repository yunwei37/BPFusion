import pathlib,subprocess,json,datetime
p=pathlib.Path('/tmp/bpfusion-long-service-timeline-bk7zo7qp')
cmd=['python3', '/tmp/bpfusion-long-service-timeline-bk7zo7qp/setup.py']
with (p/'setup.stdout').open('x') as out,(p/'setup.stderr').open('x') as err:r=subprocess.run(cmd,stdout=out,stderr=err,cwd='/workspaces/repository')
(p/'setup.wrapper.exit.json').write_text(json.dumps(dict(command=cmd,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2)+'\n')
