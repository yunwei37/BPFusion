import pathlib,os,subprocess,json,datetime,urllib.request,tarfile
r=pathlib.Path('/workspaces/repository');t=pathlib.Path(__file__).resolve().parent
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
records=[]
commands=[['/usr/bin/python3','-m','venv','--without-pip',str(t/'runtime')],['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'install','vllm==0.31.0','torch==2.13.0+cu129','transformers==5.17.0','--extra-index-url','https://download.pytorch.org/whl/cu129']]
for i,cmd in enumerate(commands):
 with (t/f'install_{i}.stdout').open('x') as out,(t/f'install_{i}.stderr').open('x') as err:z=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
 records.append({'command':cmd,'exit':z.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});(t/'install_status.json').write_text(json.dumps(records,indent=2))
 if z.returncode:raise SystemExit(z.returncode)
url='https://codeload.github.com/libbpf/libbpf/tar.gz/refs/tags/v1.6.3';urllib.request.urlretrieve(url,t/'libbpf.tar.gz')
with tarfile.open(t/'libbpf.tar.gz') as tf:tf.extractall(t,filter='data')
cmd=['make','-C',str(t/'libbpf-1.6.3/src'),'DESTDIR='+str(t/'libbpf_install'),'install']
with (t/'libbpf_build.stdout').open('x') as out,(t/'libbpf_build.stderr').open('x') as err:z=subprocess.run(cmd,stdout=out,stderr=err)
(t/'libbpf_dependency.json').write_text(json.dumps({'url':url,'command':cmd,'exit':z.returncode},indent=2))
if z.returncode:raise SystemExit(z.returncode)
env=dict(os.environ,PATH=str(t/'runtime/bin')+':/usr/local/cuda/bin:'+os.environ['PATH'],TORCH_EXTENSIONS_DIR=str(t/'cuda_extensions'),CUDA_HOME='/usr/local/cuda',LD_LIBRARY_PATH=str(t/'libbpf_install/usr/lib64'),PYTHONUNBUFFERED='1',VLLM_ENABLE_V1_MULTIPROCESSING='0')
(t/'environment.json').write_text(json.dumps({k:env[k] for k in ['PATH','TORCH_EXTENSIONS_DIR','CUDA_HOME','LD_LIBRARY_PATH','PYTHONUNBUFFERED','VLLM_ENABLE_V1_MULTIPROCESSING']},indent=2))
make=(r/'Makefile').read_text()
(t/'Makefile.original').write_text(make.replace('executor/vllm_graph.cu',str(t/'original_vllm_graph.cu')))
names=['vllm_graph_uring_loop','vllm_graph_uring_loop_trace','vllm_graph_user_network_wait','vllm_graph_user_network_wait_trace']
builds=[]
for label in ['original','candidate']:
 directory=t/(label+'-build')
 cmd=['make']+(['-f',str(t/'Makefile.original')] if label=='original' else [])+['BUILD='+str(directory),'NVCC=/usr/local/cuda/bin/nvcc -I/workspaces/repository/executor','VLLM_PYTHON='+str(t/'runtime/bin/python')]+[str(directory/(name+suffix)) for name in names for suffix in ['.so','']]
 with (t/(label+'.build.stdout')).open('x') as out,(t/(label+'.build.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 builds.append({'label':label,'command':cmd,'exit':z.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});(t/'build_status.json').write_text(json.dumps(builds,indent=2))
 if z.returncode:raise SystemExit(z.returncode)
 assert (r/'executor/vllm_graph.cu').read_bytes()==(t/'candidate_vllm_graph.cu').read_bytes()
with (t/'packages.json').open('w') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'list','--format=json'],stdout=out,check=True)
(t/'setup.exit.json').write_text(json.dumps({'exit':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
