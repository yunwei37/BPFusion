import os,pathlib,subprocess,json,datetime
os.chdir('/workspaces/repository')
r=pathlib.Path('/tmp/bpfusion-uring-copy-6wpl3780')
env=dict(os.environ,PATH=str(r/'runtime/bin')+':'+os.environ['PATH'],VLLM_ENABLE_V1_MULTIPROCESSING='0')
commands=[
('gpu_build',['make','vllm-graph-uring','vllm-graph-uring-full-copy','VLLM_PYTHON='+str(r/'runtime/bin/python')]),
('bpf_build',['clang','-O2','-g','-target','bpf','-mcpu=v3','-D__TARGET_ARCH_x86','-I/usr/include/x86_64-linux-gnu','-Ibpf/include','-Wall','-Werror','-Wno-missing-declarations','-Wno-unused-value','-c',str(r/'fusion_kernel_diagnostic.bpf.c'),'-o','build/fusion.bpf.o']),
('smol_kernel_diagnostic',[str(r/'runtime/bin/python'),'bench/vllm_serving.py','--copy-comparison','--correctness','--model','/workspaces/.cache/huggingface/hub/models--HuggingFaceTB--SmolLM2-135M/snapshots/93efa2f097d58c2a74874c7e644dbc9b0cee75a2','--output',str(r/'smol_kernel_diagnostic.jsonl')])]
status=[]
try:
 for name,cmd in commands:
  print('START',name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
  with (r/(name+'.stdout')).open('w') as out,(r/(name+'.stderr')).open('w') as err:q=subprocess.run(cmd,stdout=out,stderr=err,env=env)
  status.append(dict(name=name,cmd=cmd,exit=q.returncode))
  (r/'kernel_diagnostic_status.json').write_text(json.dumps(status,indent=2))
  print(name,q.returncode,flush=True)
  if q.returncode:break
finally:
 trace=pathlib.Path('/sys/kernel/tracing/trace').read_text()
 (r/'kernel_diagnostic_trace.txt').write_text(chr(10).join(l for l in trace.splitlines() if 'bfdiag ' in l)+chr(10))
 with (r/'bpf_restore.stdout').open('w') as out,(r/'bpf_restore.stderr').open('w') as err:q=subprocess.run(['make','-B','probes'],stdout=out,stderr=err,env=env)
 status.append(dict(name='bpf_restore',exit=q.returncode))
 (r/'kernel_diagnostic_status.json').write_text(json.dumps(status,indent=2))
 print('KERNEL_DIAGNOSTIC_TERMINAL',flush=True)
