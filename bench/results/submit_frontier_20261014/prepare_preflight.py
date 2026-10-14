import pathlib,json,time,os,subprocess,datetime
t=pathlib.Path(__file__).parent;os.chdir('/workspaces/repository')
while not (t/'setup.exit.json').exists():
 setup=json.loads((t/'setup.pid.json').read_text())
 if not pathlib.Path('/proc/'+str(setup['pid'])).exists():
  raise RuntimeError('setup process ended without terminal receipt')
 time.sleep(1)
assert json.loads((t/'setup.exit.json').read_text())['exit']==0
for stage,command in [('candidate_prepare',['/usr/bin/python3',str(t/'prepare.py')]),('preflight1',['/usr/bin/python3',str(t/'run.py'),'preflight1'])]:
 with (t/(stage+'.wrapper.stdout')).open('x') as out,(t/(stage+'.wrapper.stderr')).open('x') as err:
  p=subprocess.Popen(command,stdout=out,stderr=err)
  (t/(stage+'.pid.json')).write_text(json.dumps(dict(pid=p.pid,command=command,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
  code=p.wait()
 (t/(stage+'.wrapper.exit.json')).write_text(json.dumps(dict(exit=code,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
 print(stage,code,flush=True)
 if code:raise SystemExit(code)
(t/'prepare_preflight.exit.json').write_text(json.dumps(dict(exit=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
