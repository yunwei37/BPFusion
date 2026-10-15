import pathlib,os,subprocess,json,datetime,urllib.request,tarfile
r=pathlib.Path('/workspaces/repository');t=pathlib.Path(__file__).resolve().parent
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()=='9cfcf98a5dbda283c3e06474c74ca3aab59b65a6'
preserved=json.loads((r/'bench/results/output_publication_20261015/preserved_before.json').read_text())
def stat(p):
 s=p.lstat();return dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,symlink=os.readlink(p) if p.is_symlink() else None)
actual={n:stat(r/n) for n in preserved};assert actual==preserved
(t/'preserved_before.json').write_text(json.dumps(actual,indent=2))
(t/'base_packages_before.json').write_text(subprocess.check_output(['/usr/bin/python3','-c','import torch,transformers,numpy,json;print(json.dumps(dict(torch=torch.__version__,transformers=transformers.__version__,numpy=numpy.__version__)))'],text=True))
(t/'coder_before.json').write_text(json.dumps({str(pid):pathlib.Path('/proc/'+str(pid)+'/stat').read_text() for pid in [1,10909]},indent=2))
records=[]
commands=[['/usr/bin/python3','-m','venv','--without-pip',str(t/'runtime')],['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'install','vllm==0.31.0','torch==2.13.0+cu129','transformers==5.17.0','numpy==2.3.5','--extra-index-url','https://download.pytorch.org/whl/cu129']]
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
env.pop('VLLM_BATCH_INVARIANT',None)
for variant,names in [('kernel',['vllm_graph_uring_loop_trace','vllm_graph_uring_loop']),('native',['vllm_graph_user_network_wait_trace','vllm_graph_user_network_wait'])]:
 directory=t/(variant+'-build')
 cmd=['make','-f',str(t/variant/'Makefile'),'BUILD='+str(directory),
      'NVCC=/usr/local/cuda/bin/nvcc -I'+str(t/variant/'bpf/include')+' -I/workspaces/repository/executor',
      'BPF_CFLAGS=-O2 -g -target bpf -mcpu=v3 -D__TARGET_ARCH_x86 -I/usr/include/x86_64-linux-gnu -I'+str(t/variant/'bpf/include')+' -I/workspaces/repository/bpf/include -Wall -Werror -Wno-missing-declarations -Wno-unused-value',
      'VLLM_PYTHON='+str(t/'runtime/bin/python'),*( [str(directory/'uring_loop.bpf.o')] if variant=='kernel' else [] )]+[str(directory/(name+suffix)) for name in names for suffix in ['.so','']]
 with (t/(variant+'_build.stdout')).open('x') as out,(t/(variant+'_build.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 (t/(variant+'_build_status.json')).write_text(json.dumps({'command':cmd,'exit':z.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
 if z.returncode:raise SystemExit(z.returncode)
with (t/'packages.json').open('w') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'list','--format=json'],stdout=out,check=True)
assert {n:stat(r/n) for n in preserved}==preserved
(t/'setup.exit.json').write_text(json.dumps({'exit':0,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
