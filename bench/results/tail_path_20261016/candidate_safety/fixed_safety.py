from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
assert json.loads((t/'fixed_build.exit.json').read_text())['exit']==0
assert json.loads((t/'ordinary.exit.json').read_text())['exit']==0
env=dict(os.environ,**json.loads((t/'environment.json').read_text()));models=json.loads((t/'models.json').read_text())
statuses=[]
for name in ['qwen','smol']:
 cmd=[str(t/'runtime/bin/python'),str(t/'fixed_protocol_load.py'),'--model',models[name],'--output',str(t/(name+'_fixed_protocol8.jsonl')),'--correctness','--banks','8']
 with (t/(name+'_fixed_protocol8.stdout')).open('x') as out,(t/(name+'_fixed_protocol8.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 rec=dict(name=name,stage='protocol',command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if z.returncode==0:
  ac=['/usr/bin/python3',str(t/'protocol_analysis.py'),str(t/(name+'_fixed_protocol8.jsonl'))]
  with (t/(name+'_fixed_protocol8.analysis.stdout')).open('x') as out,(t/(name+'_fixed_protocol8.analysis.stderr')).open('x') as err:zz=subprocess.run(ac,cwd=r,stdout=out,stderr=err)
  rec.update(analysis_command=ac,analysis_exit=zz.returncode)
 statuses.append(rec);(t/'fixed_safety.statuses.json').write_text(json.dumps(statuses,indent=2));print('TERMINAL',rec,flush=True)
 if z.returncode or rec.get('analysis_exit',0):break
 cmd=[str(t/'runtime/bin/python'),str(t/'fixed_ordinary_lifecycle.py'),'loop',name,'8','vllm']
 with (t/('fixed_ordinary_'+name+'.stdout')).open('x') as out,(t/('fixed_ordinary_'+name+'.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 result=json.loads((t/('lifecycle_fixed_vllm_'+name+'_8_loop')/(name+'.results.json')).read_text())
 rec=dict(name=name,stage='ordinary',command=cmd,exit=z.returncode,passed=result['pass'],utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 statuses.append(rec);(t/'fixed_safety.statuses.json').write_text(json.dumps(statuses,indent=2));print('TERMINAL',rec,flush=True)
 if z.returncode or not result['pass']:break
ok=len(statuses)==4 and all(x['exit']==0 and x.get('analysis_exit',0)==0 and x.get('passed',True) for x in statuses)
(t/'fixed_safety.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
