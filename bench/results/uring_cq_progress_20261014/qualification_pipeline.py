import pathlib,os,json,subprocess,datetime
os.chdir('/workspaces/repository')
root=pathlib.Path('/tmp/bpfusion-uring-cq-progress-jf93e9xn')
base_env=dict(os.environ,LD_LIBRARY_PATH=str(root/'libbpf_install/usr/lib64'))
env=dict(base_env,PATH=str(root/'runtime/bin')+':'+os.environ['PATH'],VLLM_ENABLE_V1_MULTIPROCESSING='0')
commands=json.loads((root/'qualification_commands.json').read_text())
commands += [['hf_build',['make','qwen-graph-uring-loop']],['hf_lifecycle',['/usr/bin/python3',str(root/'hf_loop/pipeline.py')]]]
(root/'qualification_complete_commands.json').write_text(json.dumps(commands,indent=2))
records=[]
for name,cmd in commands:
    print('QUALIFICATION_START',name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
    chosen=base_env if name.startswith('hf_') else env
    with (root/(name+'.stdout')).open('w') as a,(root/(name+'.stderr')).open('w') as b:p=subprocess.run(cmd,env=chosen,stdout=a,stderr=b)
    row=dict(name=name,cmd=cmd,exit=p.returncode);records.append(row)
    if p.returncode==0 and not name.startswith('hf_'):
        with (root/(name+'_analysis.stdout')).open('w') as a,(root/(name+'_analysis.stderr')).open('w') as b:q=subprocess.run(['/usr/bin/python3','bench/vllm_serving_analysis.py',str(root/(name+'.jsonl'))],env=chosen,stdout=a,stderr=b)
        row['analysis_exit']=q.returncode
    if p.returncode==0 and name=='hf_lifecycle':
        hf=json.loads((root/'hf_loop/pipeline.status.json').read_text())
        row['hf_lifecycle_pass']=len(hf)==2 and all(x['exit']==0 and x['pass'] for x in hf)
    (root/'qualification_status.json').write_text(json.dumps(records,indent=2));print(json.dumps(row),flush=True)
    if p.returncode or row.get('analysis_exit',0) or row.get('hf_lifecycle_pass') is False:break
print('QUALIFICATION_PIPELINE_TERMINAL',flush=True)
