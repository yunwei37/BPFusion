from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
old=Path('/tmp/bpfusion-pending-admission-t4hv6ezt')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
statuses=[]
commands=[('build_validation',json.loads((t/'build_command.json').read_text())['command']),
 ('shared_adapter_build',['make','BUILD='+str(t/'build'),'VLLM_PYTHON='+str(old/'runtime/bin/python'),str(t/'build/qwen_graph_uring_loop.so'),str(t/'build/qwen_graph_user_network_wait.so'),str(t/'build/amk_graph_uring_loop_coalesced.so'),str(t/'build/vllm_graph_uring_loop_after_trace.so')])]
models=json.loads((t/'models.json').read_text())
for m in ['qwen','smol']:
 commands.append(('protocol_'+m,[str(old/'runtime/bin/python'),str(t/'load.py'),'--model',models[m],'--correctness','--output',str(t/('protocol_'+m+'.jsonl'))]))
(t/'commands.json').write_text(json.dumps(commands,indent=2))
for name,cmd in commands:
 print('START',name,flush=True)
 with (t/(name+'.stdout')).open('x') as out,(t/(name+'.stderr')).open('x') as err:
  p=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 row={'name':name,'command':cmd,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 if name.startswith('protocol_') and p.returncode==0:
  analysis=['/usr/bin/python3',str(t/'protocol_analysis.py'),str(t/(name+'.jsonl'))]
  with (t/(name+'.analysis.stdout')).open('x') as out,(t/(name+'.analysis.stderr')).open('x') as err:
   q=subprocess.run(analysis,cwd=r,stdout=out,stderr=err)
  row.update(analysis_exit=q.returncode,analysis_command=analysis)
 statuses.append(row);(t/'statuses.json').write_text(json.dumps(statuses,indent=2));print('DONE',json.dumps(row),flush=True)
 if row['exit'] or row.get('analysis_exit',0):break
ok=len(statuses)==len(commands) and all(x['exit']==0 and x.get('analysis_exit',0)==0 for x in statuses)
(t/'exit.json').write_text(json.dumps({'exit':0 if ok else 1,'completed':len(statuses),'expected':len(commands),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
raise SystemExit(0 if ok else 1)
