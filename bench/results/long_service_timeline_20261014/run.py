import pathlib,subprocess,sys,json,datetime
t=pathlib.Path(__file__).resolve().parent;stage=sys.argv[1];assert stage in ['preflight','full']
commands=[]
for pair in range(1 if stage=='preflight' else 5):
 for model in (['qwen'] if stage=='preflight' else (['qwen','smol'] if pair%2==0 else ['smol','qwen'])):
  order=[('loop','unprofiled'),('native','profiled'),('loop','profiled'),('native','unprofiled')]
  order=order[pair%4:]+order[:pair%4]
  for path,condition in order:commands.append([sys.executable,str(t/'case.py'),model,str(pair),path,condition,stage])
(t/(stage+'.commands.json')).write_text(json.dumps(commands,indent=2))
statuses=[]
for cmd in commands:
 key='_'.join([stage,cmd[2],'p'+cmd[3],cmd[4],cmd[5]])
 with (t/(key+'.driver.stdout')).open('x') as out,(t/(key+'.driver.stderr')).open('x') as err:p=subprocess.run(cmd,stdout=out,stderr=err)
 statuses.append({'command':cmd,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 (t/(stage+'.statuses.json')).write_text(json.dumps(statuses,indent=2))
 if p.returncode:break
code=0 if len(statuses)==len(commands) and all(x['exit']==0 for x in statuses) else 1
(t/(stage+'.exit.json')).write_text(json.dumps({'exit':code,'completed':len(statuses),'expected':len(commands),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
raise SystemExit(code)
