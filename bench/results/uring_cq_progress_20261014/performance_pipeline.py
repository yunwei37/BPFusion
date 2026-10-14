import os,pathlib,subprocess,json,datetime
repo=pathlib.Path('/workspaces/repository');os.chdir(repo)
root=pathlib.Path('/tmp/bpfusion-uring-cq-progress-jf93e9xn')
env=dict(os.environ,PATH=str(root/'runtime/bin')+':'+os.environ['PATH'],LD_LIBRARY_PATH=str(root/'libbpf_install/usr/lib64'),VLLM_ENABLE_V1_MULTIPROCESSING='0')
paths=json.loads((root/'model/model_paths.json').read_text())
records=[]
for model in ('qwen','smol'):
    name=model+'_performance'
    cmd=[str(root/'runtime/bin/python'),'bench/vllm_serving.py','--loop-progress-comparison','--untraced','--reference-path',str(root/'frozen_references.json'),'--model',paths[model],'--output',str(root/(name+'.jsonl'))]
    print('PERFORMANCE_START',model,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
    with (root/(name+'.stdout')).open('w') as a,(root/(name+'.stderr')).open('w') as b:
        p=subprocess.run(cmd,env=env,stdout=a,stderr=b)
    row=dict(model=model,cmd=cmd,exit=p.returncode);records.append(row)
    if p.returncode==0:
        with (root/(name+'_analysis.stdout')).open('w') as a,(root/(name+'_analysis.stderr')).open('w') as b:
            q=subprocess.run(['/usr/bin/python3','bench/vllm_serving_analysis.py',str(root/(name+'.jsonl'))],env=env,stdout=a,stderr=b)
        row['analysis_exit']=q.returncode
    (root/'performance_status.json').write_text(json.dumps(records,indent=2))
    print(json.dumps(row),flush=True)
    if row['exit'] or row.get('analysis_exit',0):break
print('PERFORMANCE_PIPELINE_TERMINAL',flush=True)
