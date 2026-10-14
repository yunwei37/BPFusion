import os,pathlib,json,subprocess,sys,signal,traceback,time,importlib.util,datetime
root=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path('/workspaces/repository');os.chdir(repo)
model,pair,condition,stage=sys.argv[1:];pair=int(pair)
assert condition in ('ordinary','profiled') and stage in ('preflight','full')
count=8 if stage=='preflight' else 20
cfg=json.loads((root/'models.json').read_text())[model]
pool={(tuple(r['prompt']),r['gen']):{tuple(s) for s in r['sequences']} for r in cfg['frozen_model']['references']}
key=stage+'_'+model+'_p'+str(pair)+'_'+condition
d=root/key;d.mkdir()
(d/'vllm_graph_uring_loop').write_text((root/'adapter.py').read_text())
(d/'vllm_graph_uring_loop.so').symlink_to(repo/'build/vllm_graph_uring_loop.so')
spec=importlib.util.spec_from_file_location('client',repo/'bench/resident_dispatch.py');clientmod=importlib.util.module_from_spec(spec);spec.loader.exec_module(clientmod)
env=dict(os.environ,PATH=str(root/'runtime/bin')+':'+os.environ['PATH'],LD_LIBRARY_PATH=str(root/'libbpf_install/usr/lib64'),VLLM_ENABLE_V1_MULTIPROCESSING='0',BF_DIAGNOSTIC_PROFILE='1' if condition=='profiled' else '0',BF_BIND='127.0.0.1')
os.environ['BF_BIND']='127.0.0.1'
rawpath=root/(key+'.jsonl');logpath=d/'server.stdout'
raw=rawpath.open('x',buffering=1)
def emit(event,**kw):raw.write(json.dumps(dict(event=event,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw))+'\n')
emit('metadata',model=model,pair=pair,condition=condition,stage=stage,requests=count,warmups=4,prompts=cfg['prompts'],checkpoint=cfg['model'],frozen_model=cfg['frozen_model'],source=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),driver_source=pathlib.Path(__file__).read_text(),adapter_source=(root/'adapter.py').read_text(),client_source=(repo/'bench/resident_dispatch.py').read_text(),library=str((d/'vllm_graph_uring_loop.so').resolve()),library_stat=dict(size=(d/'vllm_graph_uring_loop.so').stat().st_size,inode=(d/'vllm_graph_uring_loop.so').stat().st_ino))
attached=False;p=None;code=1
try:
 assert not pathlib.Path('/sys/module/bfusion_tx').exists()
 assert not pathlib.Path('/sys/fs/bpf/bpfusion_ctl').exists()
 r=subprocess.run(['./build/bpfusion_load','stream-uring-attach'],env=env,capture_output=True,text=True)
 emit('attach',exit=r.returncode,stdout=r.stdout,stderr=r.stderr);assert r.returncode==0;attached=True
 cmd=[str(root/'runtime/bin/python'),str(d/'vllm_graph_uring_loop'),cfg['model'],'300']
 with logpath.open('w') as log:p=subprocess.Popen(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 emit('start',pid=p.pid,command=cmd)
 print('CASE_START',key,p.pid,flush=True)
 while 'resident vLLM ready' not in logpath.read_text():
  assert p.poll() is None,logpath.read_text()[-2000:]
  time.sleep(.1)
 emit('ready',pid=p.pid)
 with clientmod.connect() as client:
  for index in range(count):
   ids=cfg['prompts'][index%4]
   row=clientmod.request(client,ids,None,gen=1)
   assert tuple(row['tokens']) in pool[(tuple(ids),1)],row
   emit('request',index=index,case=index%4,input_ids=ids,input_tokens=len(ids),warmup=index<4,**row)
 p.terminate();status=p.wait();log=logpath.read_text()
 emit('executor',pid=p.pid,exit=status,stdout=log)
 assert status==0 and 'graph_error=0' in log and 'admitted='+str(count)+' retired='+str(count) in log and 'max_active=1' in log
 ring=json.loads(next(l[7:] for l in log.splitlines() if l.startswith('RESULT ')))
 assert ring['head']==ring['completed']==count and ring['accepted']==ring['closed']==1
 assert ring['sqhead']==ring['sqtail'] and ring['cqhead']==ring['cqtail']
 assert all(ring[k]==0 for k in ('pending','error','reserved','dropped','overflow','trace_overflow'))
 emit('ring',counters=ring)
 if condition=='profiled':
  assert (d/'trace.json.gz').exists()
  emit('trace',path=str(d/'trace.json.gz'),bytes=(d/'trace.json.gz').stat().st_size)
 code=0
except BaseException as error:
 emit('failure',error=repr(error),traceback=traceback.format_exc());traceback.print_exc()
finally:
 if p is not None and p.poll() is None:
  p.terminate();emit('cleanup_server',exit=p.wait())
 if attached:
  r=subprocess.run(['./build/bpfusion_load','stream-detach'],env=env,capture_output=True,text=True)
  emit('detach',exit=r.returncode,stdout=r.stdout,stderr=r.stderr)
  for name in ('bpfusion_ctl','bpfusion_stats','bpfusion_db'):pathlib.Path('/sys/fs/bpf',name).unlink(missing_ok=True)
  if r.returncode:code=1
 emit('terminal',exit=code);raw.close()
print('CASE_TERMINAL',key,code,flush=True)
raise SystemExit(code)
