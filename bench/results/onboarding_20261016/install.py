from pathlib import Path
import subprocess,json,os,datetime
t=Path('/tmp/bpfusion-onboarding-z51zvfh3');r=Path('/workspaces/repository')
commands=[['/usr/bin/python3','-m','venv','--without-pip',str(t/'runtime')],
 ['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'install','-r',str(r/'requirements.txt')]]
records=[]
for i,cmd in enumerate(commands):
 with (t/f'install_{i}.stdout').open('x') as out,(t/f'install_{i}.stderr').open('x') as err:
  z=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
 records.append(dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 (t/'install_status.json').write_text(json.dumps(records,indent=2))
 if z.returncode:raise SystemExit(z.returncode)
(t/'install.exit.json').write_text(json.dumps(dict(exit=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
