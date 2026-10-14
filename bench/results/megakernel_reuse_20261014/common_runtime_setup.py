import pathlib,json,subprocess,datetime,os
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y');repo=pathlib.Path('/workspaces/repository');records=[]
cmds=[['/usr/bin/python3','-m','venv','--without-pip',str(r/'common_runtime')],['/usr/bin/python3','-m','pip','--python',str(r/'common_runtime/bin/python'),'install','vllm==0.31.0','torch==2.13.0+cu129','transformers==5.17.0','--extra-index-url','https://download.pytorch.org/whl/cu129']]
for i,cmd in enumerate(cmds):
 with (r/('common_install_'+str(i)+'.stdout')).open('x') as out,(r/('common_install_'+str(i)+'.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=repo,stdout=out,stderr=err)
 records.append(dict(command=cmd,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));(r/'common_install_status.json').write_text(json.dumps(records,indent=2))
 if p.returncode:raise SystemExit(p.returncode)
env=dict(os.environ,PATH=str(r/'common_runtime/bin')+':/usr/local/cuda/bin:'+os.environ['PATH'],LD_LIBRARY_PATH=str(r/'libbpf_install/usr/lib64'),VLLM_ENABLE_V1_MULTIPROCESSING='0',PYTHONPATH=str(r/'AutoMegaKernel-884534c4d2dbed4381576f81a79ae97feca53c34'),TORCH_EXTENSIONS_DIR=str(r/'common_cuda_extensions'),CUDA_HOME='/usr/local/cuda')
cmd=['make','vllm-graph-uring-loop','VLLM_PYTHON='+str(r/'common_runtime/bin/python')]
with (r/'common_build.stdout').open('x') as out,(r/'common_build.stderr').open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
(r/'common_build_status.json').write_text(json.dumps({'command':cmd,'exit':p.returncode,'env_overrides':{k:env[k] for k in ['PATH','LD_LIBRARY_PATH','VLLM_ENABLE_V1_MULTIPROCESSING','PYTHONPATH','TORCH_EXTENSIONS_DIR','CUDA_HOME']},'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
with (r/'common_packages.json').open('x') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(r/'common_runtime/bin/python'),'list','--format=json'],stdout=out)
(r/'common_setup.exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
raise SystemExit(p.returncode)
