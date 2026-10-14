import pathlib,os,subprocess,json,datetime,urllib.request,tarfile
repo=pathlib.Path('/workspaces/repository');r=pathlib.Path('/tmp/bpfusion-coalesced-network-0pls_22b');records=[]
source={'repo':'RightNow-AI/AutoMegaKernel','revision':'884534c4d2dbed4381576f81a79ae97feca53c34','url':'https://codeload.github.com/RightNow-AI/AutoMegaKernel/tar.gz/884534c4d2dbed4381576f81a79ae97feca53c34'}
urllib.request.urlretrieve(source['url'],r/'upstream.tar.gz')
with tarfile.open(r/'upstream.tar.gz') as tf:tf.extractall(r,filter='data')
(r/'source_setup.json').write_text(json.dumps(source,indent=2))
commands=[['/usr/bin/python3','-m','venv','--without-pip',str(r/'runtime')],['/usr/bin/python3','-m','pip','--python',str(r/'runtime/bin/python'),'install','vllm==0.31.0','torch==2.13.0+cu129','transformers==5.17.0','--extra-index-url','https://download.pytorch.org/whl/cu129']]
for i,cmd in enumerate(commands):
 with (r/('install_'+str(i)+'.stdout')).open('x') as out,(r/('install_'+str(i)+'.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=repo,stdout=out,stderr=err)
 records.append({'command':cmd,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});(r/'install_status.json').write_text(json.dumps(records,indent=2))
 if p.returncode:raise SystemExit(p.returncode)
url='https://codeload.github.com/libbpf/libbpf/tar.gz/refs/tags/v1.6.3';urllib.request.urlretrieve(url,r/'libbpf.tar.gz')
with tarfile.open(r/'libbpf.tar.gz') as tf:tf.extractall(r,filter='data')
cmd=['make','-C',str(r/'libbpf-1.6.3/src'),'DESTDIR='+str(r/'libbpf_install'),'install']
with (r/'libbpf_build.stdout').open('x') as out,(r/'libbpf_build.stderr').open('x') as err:p=subprocess.run(cmd,stdout=out,stderr=err)
(r/'libbpf_dependency.json').write_text(json.dumps({'url':url,'command':cmd,'exit':p.returncode},indent=2))
if p.returncode:raise SystemExit(p.returncode)
env=dict(os.environ,PATH=str(r/'runtime/bin')+':/usr/local/cuda/bin:'+os.environ['PATH'],PYTHONPATH=str(r/'AutoMegaKernel-884534c4d2dbed4381576f81a79ae97feca53c34'),TORCH_EXTENSIONS_DIR=str(r/'cuda_extensions'),CUDA_HOME='/usr/local/cuda',LD_LIBRARY_PATH=str(r/'libbpf_install/usr/lib64'),BF_BIND='127.0.0.1',PYTHONUNBUFFERED='1')
(r/'environment.json').write_text(json.dumps({k:env[k] for k in ['PATH','PYTHONPATH','TORCH_EXTENSIONS_DIR','CUDA_HOME','LD_LIBRARY_PATH','BF_BIND','PYTHONUNBUFFERED']},indent=2))
cmd=['make','amk-graph-uring-loop','amk-graph-user-network-wait','AMK_PYTHON='+str(r/'runtime/bin/python')]
with (r/'build.stdout').open('x') as out,(r/'build.stderr').open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
(r/'build_status.json').write_text(json.dumps({'command':cmd,'exit':p.returncode},indent=2))
with (r/'packages.json').open('x') as out:subprocess.run(['/usr/bin/python3','-m','pip','--python',str(r/'runtime/bin/python'),'list','--format=json'],stdout=out)
(r/'setup.exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
raise SystemExit(p.returncode)
