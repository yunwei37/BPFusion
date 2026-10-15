import pathlib,os,subprocess,json,datetime,urllib.request,tarfile
repo=pathlib.Path('/workspaces/repository');t=pathlib.Path(__file__).parent;records=[]
commands=[['/usr/bin/python3','-m','venv','--without-pip',str(t/'runtime')],['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'install','vllm==0.31.0','torch==2.13.0+cu129','transformers==5.17.0','--extra-index-url','https://download.pytorch.org/whl/cu129']]
for i,cmd in enumerate(commands):
 with (t/('install_'+str(i)+'.stdout')).open('x') as out,(t/('install_'+str(i)+'.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=repo,stdout=out,stderr=err)
 records.append(dict(command=cmd,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));(t/'install_status.json').write_text(json.dumps(records,indent=2))
 if p.returncode:raise SystemExit(p.returncode)
url='https://codeload.github.com/libbpf/libbpf/tar.gz/refs/tags/v1.6.3';urllib.request.urlretrieve(url,t/'libbpf.tar.gz')
with tarfile.open(t/'libbpf.tar.gz') as tf:tf.extractall(t,filter='data')
cmd=['make','-C',str(t/'libbpf-1.6.3/src'),'DESTDIR='+str(t/'libbpf_install'),'install']
with (t/'libbpf_build.stdout').open('x') as out,(t/'libbpf_build.stderr').open('x') as err:p=subprocess.run(cmd,stdout=out,stderr=err)
(t/'libbpf_dependency.json').write_text(json.dumps(dict(url=url,command=cmd,exit=p.returncode),indent=2))
if p.returncode:raise SystemExit(p.returncode)
env=dict(os.environ,PATH=str(t/'runtime/bin')+':/usr/local/cuda/bin:'+os.environ['PATH'],TORCH_EXTENSIONS_DIR=str(t/'cuda_extensions'),CUDA_HOME='/usr/local/cuda',LD_LIBRARY_PATH=str(t/'libbpf_install/usr/lib64'),PYTHONUNBUFFERED='1',VLLM_ENABLE_V1_MULTIPROCESSING='0')
(t/'environment.json').write_text(json.dumps({k:env[k] for k in ['PATH','TORCH_EXTENSIONS_DIR','CUDA_HOME','LD_LIBRARY_PATH','PYTHONUNBUFFERED','VLLM_ENABLE_V1_MULTIPROCESSING']},indent=2))
names=['vllm_graph_uring_loop_trace.so','vllm_graph_uring_loop_trace','vllm_graph_user_network_wait_trace.so','vllm_graph_user_network_wait_trace']
cmd=['make','BUILD='+str(t/'build'),*[str(t/'build'/name) for name in names],'VLLM_PYTHON='+str(t/'runtime/bin/python')]
with (t/'build.stdout').open('x') as out,(t/'build.stderr').open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
(t/'build_status.json').write_text(json.dumps(dict(command=cmd,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
with (t/'packages.json').open('w') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'list','--format=json'],stdout=out)
(t/'setup.exit.json').write_text(json.dumps(dict(exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(p.returncode)
