import os,pathlib,subprocess,json,datetime,sys
root=pathlib.Path("/tmp/bpfusion-tail-chain-cwekbdzh")
os.chdir('/workspaces/repository')
env=dict(os.environ,PATH=str(root/'venv/bin')+':'+os.environ['PATH'],VLLM_ENABLE_V1_MULTIPROCESSING='0',HF_HOME='/workspaces/.cache/huggingface')
python=str(root/'venv/bin/python')
base=json.loads(pathlib.Path('bench/results/default_untraced_20261012/frozen_references.json').read_text())
models={name:m['model'] for name,m in base['models'].items()}
commands={}
def run(label,command):
 commands[label]=command
 (root/'pipeline_commands.json').write_text(json.dumps(commands,indent=2)+'\n')
 print('START',label,flush=True)
 with (root/(label+'.stdout.txt')).open('w') as log:
  result=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT)
 (root/(label+'.status.json')).write_text(json.dumps({'exit_code':result.returncode,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})+'\n')
 print('TERMINAL',label,result.returncode,flush=True)
 assert result.returncode==0,(label,result.returncode)
def serving(label,model,flags):
 run(label+'_driver',[python,'bench/vllm_serving.py','--dispatch-comparison','--model',model,'--output',str(root/(label+'.jsonl')),*flags])
 run(label+'_analysis',[python,'bench/vllm_serving_analysis.py',str(root/(label+'.jsonl'))])
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
(root/'sources.json').write_text(json.dumps({path:pathlib.Path(path).read_text() for path in ['Makefile','executor/vllm_graph.cu','executor/vllm_graph.py','executor/userspace_tcp.h','bench/vllm_serving.py','bench/vllm_serving_analysis.py','bench/resident_dispatch.py']},indent=2)+'\n')
(root/'pipeline_environment.json').write_text(json.dumps({k:env[k] for k in ['PATH','VLLM_ENABLE_V1_MULTIPROCESSING','HF_HOME']},indent=2)+'\n')
run('build',['make','VLLM_PYTHON='+python,'vllm-graph','vllm-graph-user-network-wait','vllm-graph-trace','vllm-graph-chained'])
serving('traced_preflight',models['qwen'],['--preflight'])
for name,model in models.items():serving(name+'_correctness',model,['--correctness'])
# Freeze only independently replayed references, before any untraced observation.
for name,model in base['models'].items():
 pool={(tuple(r['prompt']),r['gen']):{tuple(seq) for seq in r['sequences']} for r in model['references']}
 files=sorted(root.glob(name+'_correctness_p0_*.gpu.jsonl.references.jsonl'))
 if name=='qwen':files+=sorted(root.glob('traced_preflight_p0_*.gpu.jsonl.references.jsonl'))
 assert len(files)==(8 if name=='qwen' else 4)
 added=0
 for file in files:
  for line in file.open():
   r=json.loads(line)
   if not r['bad']:
    assert len(r['tokens'])==r['gen']
    pool.setdefault((tuple(r['prompt']),r['gen']),set()).add(tuple(r['tokens']))
  added+=1
 model['references']=[{'prompt':list(prompt),'gen':gen,'sequences':[list(seq) for seq in sorted(values)]} for (prompt,gen),values in sorted(pool.items())]
 model['source_files']+=list(map(str,files))
 model['precision']='fp16'
base['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
base['scope']='pre-observation qualified complete-output-set fidelity; prior0034 plus current independently replayed strict/traced preflight; current untraced batch trajectory unobserved'
base['source_commit']=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
base['source_snapshot']='sources.json'
(root/'frozen_references.json').write_text(json.dumps(base,indent=2)+'\n')
print('FROZEN_BEFORE_UNTRACED',base['utc'],flush=True)
flags=['--untraced','--reference-path',str(root/'frozen_references.json')]
serving('untraced_preflight',models['qwen'],[*flags,'--preflight'])
for name,model in models.items():serving(name+'_performance',model,flags)
print('PIPELINE_COMPLETE',flush=True)
