import pathlib,os,subprocess,json,urllib.request,tarfile,datetime
os.chdir('/workspaces/repository')
root=pathlib.Path('/tmp/bpfusion-optimized-cross-node-nk49zfoa')
records=[]
commands=[['/usr/bin/python3','-m','venv','--without-pip',str(root/'runtime')],
 ['/usr/bin/python3','-m','pip','--python',str(root/'runtime/bin/python'),'install','vllm==0.31.0','torch==2.13.0+cu129','transformers==5.17.0','--extra-index-url','https://download.pytorch.org/whl/cu129']]
for i,cmd in enumerate(commands):
 with (root/('install_'+str(i)+'.stdout')).open('w') as a,(root/('install_'+str(i)+'.stderr')).open('w') as b:
  r=subprocess.run(cmd,stdout=a,stderr=b)
 records.append(dict(cmd=cmd,exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 (root/'install_status.json').write_text(json.dumps(records,indent=2))
 if r.returncode:raise SystemExit(r.returncode)
url='https://codeload.github.com/libbpf/libbpf/tar.gz/refs/tags/v1.6.3'
urllib.request.urlretrieve(url,root/'libbpf.tar.gz')
with tarfile.open(root/'libbpf.tar.gz') as t:t.extractall(root,filter='data')
cmd=['make','-C',str(root/'libbpf-1.6.3/src'),'DESTDIR='+str(root/'libbpf_install'),'install']
with (root/'libbpf_build.stdout').open('w') as a,(root/'libbpf_build.stderr').open('w') as b:r=subprocess.run(cmd,stdout=a,stderr=b)
(root/'libbpf_dependency.json').write_text(json.dumps(dict(url=url,cmd=cmd,exit=r.returncode),indent=2))
if r.returncode:raise SystemExit(r.returncode)
env=dict(os.environ,PATH=str(root/'runtime/bin')+':'+os.environ['PATH'],LD_LIBRARY_PATH=str(root/'libbpf_install/usr/lib64'),VLLM_ENABLE_V1_MULTIPROCESSING='0')
cmd=['make','vllm-graph-uring-loop','vllm-graph-user-network-wait','VLLM_PYTHON='+str(root/'runtime/bin/python')]
with (root/'build.stdout').open('w') as a,(root/'build.stderr').open('w') as b:r=subprocess.run(cmd,env=env,stdout=a,stderr=b)
(root/'build_status.json').write_text(json.dumps(dict(cmd=cmd,exit=r.returncode),indent=2))
with (root/'resolved_packages.json').open('w') as a:subprocess.run([str(root/'runtime/bin/python'),'-m','pip','list','--format=json'],stdout=a)
(root/'setup_terminal.json').write_text(json.dumps(dict(exit=r.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
