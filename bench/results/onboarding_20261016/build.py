from pathlib import Path
import os,subprocess,json,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
env=dict(os.environ,PATH=str(t/'runtime/bin')+':/usr/local/cuda/bin:'+os.environ['PATH'],LD_LIBRARY_PATH=str(t/'libbpf_install/usr/lib64'),CUDA_HOME='/usr/local/cuda',VLLM_ENABLE_V1_MULTIPROCESSING='0',PYTHONUNBUFFERED='1')
env.pop('VLLM_BATCH_INVARIANT',None)
(t/'environment.json').write_text(json.dumps({k:env[k] for k in ['PATH','LD_LIBRARY_PATH','CUDA_HOME','VLLM_ENABLE_V1_MULTIPROCESSING','PYTHONUNBUFFERED']},indent=2))
cmd=['make','BUILD='+str(t/'build'),'VLLM_PYTHON='+str(t/'runtime/bin/python'),str(t/'build/fusion.bpf.o'),str(t/'build/bpfusion_load'),'vllm-graph-uring-loop','vllm-graph-user-network-wait']
with (t/'build.stdout').open('x') as out,(t/'build.stderr').open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
(t/'build.exit.json').write_text(json.dumps(dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(z.returncode)
