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
# Build the unmodified current standalone control before the candidate edit.
control_cmd=['make','BUILD='+str(t/'control-build'),*[str(t/'control-build'/name) for name in ['vllm_graph_uring_loop.so','vllm_graph_uring_loop']],'VLLM_PYTHON='+str(t/'runtime/bin/python')]
with (t/'control_build.stdout').open('x') as out,(t/'control_build.stderr').open('x') as err:control_result=subprocess.run(control_cmd,cwd=repo,env=env,stdout=out,stderr=err)
(t/'control_build_status.json').write_text(json.dumps(dict(command=control_cmd,exit=control_result.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
if control_result.returncode:raise SystemExit(control_result.returncode)
assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],cwd=repo,text=True).strip()=='main'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()=='212a15775e924ea6b2447b3efa046ca6889022a8'
header=repo/'executor/io_uring_tcp.h';original=(t/'original_io_uring_tcp.h').read_text()
assert header.read_text()==original
lines=original.splitlines(keepends=True);indices=[i for i,line in enumerate(lines) if line.strip()=='#ifdef BF_IO_COALESCED'];assert len(indices)==10
for index in [0,1,3,4,5,6,7]:lines[indices[index]]='#if defined(BF_IO_COALESCED) || defined(BF_URING_BPF_LOOP)'+chr(10)
header.write_text(''.join(lines))
(t/'candidate.diff').write_text(subprocess.check_output(['git','diff','--','executor/io_uring_tcp.h'],cwd=repo,text=True))
paths=['Makefile','executor/vllm_graph.cu','executor/io_uring_tcp.h','executor/vllm_graph.py','executor/qwen_graph.cu','executor/amk_graph.py','executor/amk_graph.cu','executor/userspace_tcp.h','bpf/fusion.bpf.c','bpf/uring_loop.bpf.c','bpf/include/bpfusion_queue.h','bench/resident_dispatch.py']
for rel in paths:
 dst=t/'source_snapshot'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((repo/rel).read_bytes())
(t/'source_frozen.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),base_commit='212a15775e924ea6b2447b3efa046ca6889022a8',branch='main',captured_paths=paths,scope='seven existing publication conditionals; original control built before candidate edit, native/model math unchanged'),indent=2))
cmd=['make','BUILD='+str(t/'build'),*[str(t/'build'/name) for name in ['vllm_graph_user_network_wait.so','vllm_graph_user_network_wait','vllm_graph_uring_loop.so','vllm_graph_uring_loop','vllm_graph_uring_loop_trace.so','vllm_graph_uring_loop_trace']],'VLLM_PYTHON='+str(t/'runtime/bin/python')]
with (t/'build.stdout').open('x') as out,(t/'build.stderr').open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
(t/'build_status.json').write_text(json.dumps(dict(command=cmd,exit=p.returncode),indent=2))
with (t/'packages.json').open('w') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(t/'runtime/bin/python'),'list','--format=json'],stdout=out)
(t/'setup.exit.json').write_text(json.dumps(dict(exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(p.returncode)
