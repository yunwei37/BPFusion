import os,pathlib,json,subprocess,sys,datetime
os.chdir('/workspaces/repository')
root=pathlib.Path('/tmp/bpfusion-optimized-cross-node-nk49zfoa')
model,pair,mode,stage=sys.argv[1:];pair=int(pair)
assert mode in ('uring_loop','userspace') and stage in ('preflight','full')
config=json.loads((root/'models.json').read_text())[model]
prefix=root/(stage+'_'+model+'_p'+str(pair)+'_'+mode)
env=dict(os.environ,PATH=str(root/'runtime/bin')+':'+os.environ['PATH'],LD_LIBRARY_PATH=str(root/'libbpf_install/usr/lib64'),VLLM_ENABLE_V1_MULTIPROCESSING='0',BF_BIND='10.42.1.238')
assert not pathlib.Path('/sys/module/bfusion_tx').exists()
assert not pathlib.Path('/sys/fs/bpf/bpfusion_ctl').exists()
attached=False
receipt=dict(model=model,pair=pair,mode=mode,stage=stage,source=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
try:
 if mode=='uring_loop':
  cmd=['./build/bpfusion_load','stream-uring-attach']
  r=subprocess.run(cmd,env=env,capture_output=True,text=True)
  receipt['attach']=dict(cmd=cmd,exit=r.returncode,stdout=r.stdout,stderr=r.stderr)
  assert r.returncode==0;attached=True
 binary='vllm_graph_uring_loop' if mode=='uring_loop' else 'vllm_graph_user_network_wait'
 cmd=['./build/'+binary,config['model'],'300']
 if stage=='preflight':cmd=['strace','-D','-f','-e','trace=network,write,io_uring_enter','-o',str(prefix)+'.network.txt',*cmd]
 receipt['cmd']=cmd
 with pathlib.Path(str(prefix)+'.server.stdout').open('w') as a:
  p=subprocess.Popen(cmd,env=env,stdout=a,stderr=subprocess.STDOUT,start_new_session=True)
  receipt['pid']=p.pid
  pathlib.Path(str(prefix)+'.server_started.json').write_text(json.dumps(receipt,indent=2))
  receipt['exit']=p.wait()
finally:
 if attached:
  cmd=['./build/bpfusion_load','stream-detach']
  r=subprocess.run(cmd,env=env,capture_output=True,text=True)
  receipt['detach']=dict(cmd=cmd,exit=r.returncode,stdout=r.stdout,stderr=r.stderr)
  for name in ('bpfusion_ctl','bpfusion_stats','bpfusion_db'):pathlib.Path('/sys/fs/bpf',name).unlink(missing_ok=True)
 receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
 pathlib.Path(str(prefix)+'.server_terminal.json').write_text(json.dumps(receipt,indent=2))
