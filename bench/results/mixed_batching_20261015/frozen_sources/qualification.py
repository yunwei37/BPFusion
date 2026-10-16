from pathlib import Path
import subprocess,json,os,datetime,sys
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
name=sys.argv[1];assert name in ['qwen','smol']
env=dict(os.environ,**json.loads((t/'environment.json').read_text()));env.pop('VLLM_BATCH_INVARIANT',None)
models=json.loads((t/'models.json').read_text());py=str(t/'runtime/bin/python')
tag='protocol_'+name
cmd=[py,str(t/'load.py'),'--model',models[name],'--correctness','--output',str(t/(tag+'.jsonl'))]
with (t/(tag+'.driver.stdout')).open('x') as out,(t/(tag+'.driver.stderr')).open('x') as err:
 z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
status=dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
if z.returncode==0:
 with (t/(tag+'.analysis.stdout')).open('x') as out,(t/(tag+'.analysis.stderr')).open('x') as err:
  q=subprocess.run(['/usr/bin/python3',str(t/'protocol_analysis.py'),str(t/(tag+'.jsonl'))],stdout=out,stderr=err)
 status['analysis_exit']=q.returncode
(t/(tag+'.exit.json')).write_text(json.dumps(status,indent=2))
print(json.dumps(status),flush=True)
raise SystemExit(0 if status['exit']==status.get('analysis_exit',1)==0 else 1)
