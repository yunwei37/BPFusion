import pathlib,subprocess,json,datetime,os
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository')
assert json.loads((t/'full.exit.json').read_text())['exit']==0
env=dict(os.environ,**json.loads((t/'environment.json').read_text()));env.pop('VLLM_BATCH_INVARIANT',None)
base_env=dict(os.environ,LD_LIBRARY_PATH=env['LD_LIBRARY_PATH'])
py=str(t/'runtime/bin/python');models=json.loads((t/'models.json').read_text())
saved=json.loads((t/'candidate_build_status.json').read_text())['command']
# Reuse the source-native compiler options; add only the affected existing targets.
cmd=saved[:saved.index(str(t/'candidate-build/uring_loop.bpf.o'))]
cmd[cmd.index('-f')+1]=str(t/'candidate/Makefile.compat')
names=['vllm_graph_uring_loop_coalesced_trace','vllm_graph_uring_loop_coalesced','vllm_graph_uring_loop_after_trace','vllm_graph_uring_loop_after','qwen_graph_uring_loop']
cmd += [str(t/'candidate-build/uring_loop_after.bpf.o')]+[str(t/'candidate-build'/(name+suffix)) for name in names for suffix in ['.so','']]
commands=[dict(name='compat_build',command=cmd,kind='build')]
for model in ['qwen','smol']:
 commands.append(dict(name='compat_hf_'+model,command=['/usr/bin/python3',str(t/'compat_hf_loop/driver.py'),model],kind='hf',model=model))
for variant in ['coalesced','after']:
 for model in ['qwen','smol']:
  key='compat_'+variant+'_'+model
  commands.append(dict(name=key,command=[py,str(t/('serving_'+variant+'.py')),'--model',models[model],'--loop-comparison','--correctness','--output',str(t/(key+'.jsonl'))],kind='protocol'))
  commands.append(dict(name='compat_'+variant+'_lifecycle_'+model,command=[py,str(t/('compat_'+variant+'_lifecycle.py')),'loop',model],kind='lifecycle',variant=variant,model=model))
(t/'compatibility.commands.json').write_text(json.dumps(commands,indent=2));records=[]
for item in commands:
 name=item['name'];print('START',name,flush=True)
 with (t/(name+'.driver.stdout')).open('x') as out,(t/(name+'.driver.stderr')).open('x') as err:
  z=subprocess.run(item['command'],cwd=r,env=base_env if item['kind']=='hf' else env,stdout=out,stderr=err)
 row=dict(name=name,kind=item['kind'],command=item['command'],exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if item['kind']=='protocol' and z.returncode==0:
  cmd=['/usr/bin/python3',str(t/'analysis.py'),str(t/(name+'.jsonl'))]
  with (t/(name+'.analysis.stdout')).open('x') as out,(t/(name+'.analysis.stderr')).open('x') as err:a=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
  row.update(analysis_command=cmd,analysis_exit=a.returncode)
 if item['kind'] in ['hf','lifecycle']:
  model=item['model'];p=(t/'compat_hf_loop' if item['kind']=='hf' else t/('compat_'+item['variant']+'_lifecycle_'+model+'_loop'))/(model+'.results.json')
  row['result_path']=str(p);row['pass']=p.exists() and json.loads(p.read_text()).get('pass') is True
 records.append(row);(t/'compatibility.statuses.json').write_text(json.dumps(records,indent=2));print('TERMINAL',json.dumps(row),flush=True)
 if z.returncode or row.get('analysis_exit',0) or row.get('pass',True) is False:break
ok=len(records)==len(commands) and all(x['exit']==0 and x.get('analysis_exit',0)==0 and x.get('pass',True) for x in records)
(t/'compatibility.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1,completed=len(records),expected=len(commands),utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(0 if ok else 1)
