from pathlib import Path
import os,subprocess,json,datetime,urllib.request,tarfile
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=r,text=True).strip()=='main'
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def stat(p):
 s=p.lstat();return dict(inode=s.st_ino,size=s.st_size,mtime_ns=s.st_mtime_ns,symlink=os.readlink(p) if p.is_symlink() else None)
preserved=json.loads((t/'entry.json').read_text())['preserved']
assert {n:stat(r/n) for n in preserved}==preserved
(t/'base_packages_before.json').write_text(subprocess.check_output(['/usr/bin/python3','-c','import torch,transformers,numpy,json;print(json.dumps(dict(torch=torch.__version__,transformers=transformers.__version__,numpy=numpy.__version__)))'],text=True))
(t/'coder_before.json').write_text(json.dumps({str(pid):Path('/proc/'+str(pid)+'/stat').read_text() for pid in [1,10909]},indent=2))
commands=[['/usr/bin/python3','-m','venv','--without-pip',str(t/'runtime')],
 ['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'install','vllm==0.31.0','torch==2.13.0+cu129','transformers==5.17.0','numpy==2.3.5','cuda-python==12.9.7','cuda-bindings==12.9.9','--extra-index-url','https://download.pytorch.org/whl/cu129']]
statuses=[]
for i,cmd in enumerate(commands):
 with (t/f'install_{i}.stdout').open('x') as out,(t/f'install_{i}.stderr').open('x') as err:z=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
 statuses.append(dict(command=cmd,exit=z.returncode,utc=stamp()));(t/'install_status.json').write_text(json.dumps(statuses,indent=2))
 if z.returncode:raise SystemExit(z.returncode)
url='https://codeload.github.com/libbpf/libbpf/tar.gz/refs/tags/v1.6.3';urllib.request.urlretrieve(url,t/'libbpf.tar.gz')
with tarfile.open(t/'libbpf.tar.gz') as tf:tf.extractall(t,filter='data')
cmd=['make','-C',str(t/'libbpf-1.6.3/src'),'DESTDIR='+str(t/'libbpf_install'),'install']
with (t/'libbpf_build.stdout').open('x') as out,(t/'libbpf_build.stderr').open('x') as err:z=subprocess.run(cmd,stdout=out,stderr=err)
(t/'libbpf_dependency.json').write_text(json.dumps(dict(url=url,command=cmd,exit=z.returncode),indent=2))
if z.returncode:raise SystemExit(z.returncode)
env=dict(os.environ,PATH=str(t/'runtime/bin')+':/usr/local/cuda/bin:'+os.environ['PATH'],TORCH_EXTENSIONS_DIR=str(t/'cuda_extensions'),CUDA_HOME='/usr/local/cuda',LD_LIBRARY_PATH=str(t/'libbpf_install/usr/lib64'),PYTHONUNBUFFERED='1',VLLM_ENABLE_V1_MULTIPROCESSING='0',PYTHONPATH=str(r/'executor'))
env.pop('VLLM_BATCH_INVARIANT',None)
(t/'environment.json').write_text(json.dumps({k:env[k] for k in ['PATH','TORCH_EXTENSIONS_DIR','CUDA_HOME','LD_LIBRARY_PATH','PYTHONUNBUFFERED','VLLM_ENABLE_V1_MULTIPROCESSING','PYTHONPATH']},indent=2))

builds=[]
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()==json.loads((t/'entry.json').read_text())['source_parent']
for variant in ['original','mixed']:
 build=t/('build_'+variant)
 makefile=t/(variant+'.Makefile')
 makefile.write_text((r/'Makefile').read_text().replace('executor/vllm_graph.cu',str(t/(variant+'_vllm_graph.cu'))))
 names=['vllm_graph_uring_loop_trace','vllm_graph_user_network_wait_trace']
 cmd=['make','-f',str(makefile),'BUILD='+str(build),'VLLM_PYTHON='+str(t/'runtime/bin/python'),
      'CPPFLAGS=-DBF_LLM_SLOTS=16 -I'+str(r/'executor')]
 cmd += [str(build/'fusion.bpf.o'),str(build/'uring_loop.bpf.o'),str(build/'bpfusion_load')]+[str(build/(n+suffix)) for n in names for suffix in ['.so','']]
 with (t/('build_'+variant+'.stdout')).open('x') as out,(t/('build_'+variant+'.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 builds.append(dict(variant=variant,command=cmd,exit=z.returncode,utc=stamp()))
 (t/'build_status.json').write_text(json.dumps(builds,indent=2))
 if z.returncode:raise SystemExit(z.returncode)
 for name in names:
  (build/name).unlink()
  (build/name).symlink_to(t/(variant+'_vllm_graph.py'))
assert (r/'executor/vllm_graph.cu').read_bytes()==(t/'original_vllm_graph.cu').read_bytes()
with (t/'packages.json').open('w') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'list','--format=json'],stdout=out,check=True)
old=json.loads((r/'bench/results/batch_capacity_integration_20261015/packages.json').read_text());new=json.loads((t/'packages.json').read_text())
aa={x['name'].lower():x['version'] for x in old};bb={x['name'].lower():x['version'] for x in new}
delta={k:[aa.get(k),bb.get(k)] for k in sorted(aa.keys()|bb.keys()) if aa.get(k)!=bb.get(k)}
(t/'package_comparison.json').write_text(json.dumps(delta,indent=2))
assert not delta,delta
assert {n:stat(r/n) for n in preserved}==preserved
(t/'setup.exit.json').write_text(json.dumps(dict(exit=0,utc=stamp()),indent=2))
