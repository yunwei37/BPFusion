import pathlib,json,subprocess,os,time,datetime
t=pathlib.Path(__file__).parent;os.chdir('/workspaces/repository')
while not (t/'prepare_preflight.exit.json').exists():
 if not pathlib.Path('/proc/365085').exists():raise RuntimeError('same preflight handle ended without terminal receipt')
 time.sleep(1)
assert json.loads((t/'prepare_preflight.exit.json').read_text())['exit']==0
steps=[('preflight1.analysis',['/usr/bin/python3',str(t/'analysis.py'),str(t),'preflight1']),
       ('qualification',['/usr/bin/python3',str(t/'run_qualification.py')]),
       ('lifecycle',['/usr/bin/python3',str(t/'run_lifecycle.py')]),
       ('probe',['/usr/bin/python3',str(t/'run_probe.py')]),
       ('probe.analysis',['/usr/bin/python3',str(t/'probe_analysis.py'),str(t)])]
for stage,command in steps:
 with (t/(stage+'.wrapper.stdout')).open('x') as out,(t/(stage+'.wrapper.stderr')).open('x') as err:
  p=subprocess.Popen(command,stdout=out,stderr=err)
  (t/(stage+'.pid.json')).write_text(json.dumps(dict(pid=p.pid,command=command,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
  code=p.wait()
 (t/(stage+'.wrapper.exit.json')).write_text(json.dumps(dict(exit=code,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
 print(stage,code,flush=True)
 if code:raise SystemExit(code)
(t/'qualification_probe.exit.json').write_text(json.dumps(dict(exit=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
