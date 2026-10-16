from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
statuses=[]
for name in ['qwen','smol']:
 for condition in ['loop','native']:
  cmd=[str(t/'runtime/bin/python'),str(t/'ordinary_lifecycle.py'),condition,name,'8','vllm']
  tag=name+'_'+condition
  print('START',tag,flush=True)
  with (t/('ordinary_'+tag+'.stdout')).open('x') as out,(t/('ordinary_'+tag+'.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
  f=t/('lifecycle_vllm_'+name+'_8_'+condition)/(name+'.results.json')
  result=json.loads(f.read_text()) if f.exists() else {}
  rec=dict(name=name,condition=condition,command=cmd,exit=z.returncode,passed=result.get('pass',False),utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
  statuses.append(rec);(t/'ordinary.statuses.json').write_text(json.dumps(statuses,indent=2));print('TERMINAL',rec,flush=True)
  assert not list(Path('/sys/fs/bpf').glob('bpfusion*'))
ok=len(statuses)==4 and all(x['exit']==0 and x['passed'] for x in statuses)
(t/'ordinary.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
