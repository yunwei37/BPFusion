import pathlib,os,json,subprocess,time,importlib.util,sys,traceback,datetime
repo=pathlib.Path('/workspaces/repository');r=pathlib.Path(__file__).parent;os.chdir(repo)
condition=sys.argv[1];assert condition in ['native','loop']
key='concurrency_'+condition;d=r/key;d.mkdir()
cfg=json.loads((r/'smol_frozen.json').read_text())
pool={(tuple(x['prompt']),x['gen']):{tuple(y) for y in x['sequences']} for x in cfg['frozen_model']['references']}
record=json.loads((r/'amk_build_status.json').read_text());env=dict(os.environ,**record['env_overrides'],BF_BIND='127.0.0.1',PYTHONUNBUFFERED='1')
os.environ['BF_BIND']='127.0.0.1'
spec=importlib.util.spec_from_file_location('client',repo/'bench/resident_dispatch.py');client=importlib.util.module_from_spec(spec);spec.loader.exec_module(client)
raw=(r/(key+'.jsonl')).open('x',buffering=1)
def emit(event,**fields):raw.write(json.dumps(dict(event=event,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**fields))+'\n')
emit('metadata',condition=condition,checkpoint=cfg['model'],prompts=cfg['prompts'],frozen_model=cfg['frozen_model'],source=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),bootstrap=(repo/'executor/amk_graph.py').read_text(),builder=(repo/'executor/amk_graph.cu').read_text(),driver=(repo/'executor/qwen_graph.cu').read_text(),case_source=pathlib.Path(__file__).read_text())
p=None;attached=False;code=1
try:
 assert not pathlib.Path('/sys/module/bfusion_tx').exists()
 assert not pathlib.Path('/sys/fs/bpf/bpfusion_ctl').exists()
 if condition=='loop':
  q=subprocess.run(['./build/bpfusion_load','stream-uring-attach'],env=env,capture_output=True,text=True)
  emit('attach',exit=q.returncode,stdout=q.stdout,stderr=q.stderr);assert q.returncode==0;attached=True
 name='amk_graph_uring_loop' if condition=='loop' else 'amk_graph_user_network_wait'
 cmd=['/usr/bin/python3',str(repo/'build'/name),cfg['model'],'300']
 with (d/'server.stdout').open('w') as log:p=subprocess.Popen(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 emit('start',pid=p.pid,command=cmd);print('SERVER_START',condition,p.pid,flush=True)
 while 'resident Qwen ready' not in (d/'server.stdout').read_text():
  assert p.poll() is None,(d/'server.stdout').read_text()[-2500:]
  time.sleep(.1)
 emit('ready',pid=p.pid);print('SERVER_READY',condition,p.pid,flush=True)
 import threading,concurrent.futures
 for wave,gen in enumerate([1,64,1]):
  gate=threading.Barrier(8)
  def worker(slot):
   ids=cfg['prompts'][slot%4]
   with client.connect() as sock:
    gate.wait(timeout=60)
    row=client.request(sock,ids,None,gen=gen)
   assert tuple(row['tokens']) in pool[(tuple(ids),gen)],row
   return dict(index=wave*8+slot,wave=wave,slot=slot,gen=gen,input_ids=ids,**row)
  with concurrent.futures.ThreadPoolExecutor(max_workers=8) as workers:
   for row in workers.map(worker,range(8)):emit('request',**row)
  emit('wave_done',wave=wave,gen=gen)
 p.terminate();status=p.wait();log=(d/'server.stdout').read_text()
 emit('executor',pid=p.pid,exit=status,stdout=log)
 assert status==0 and 'graph_error=0' in log and '"errors": [0, 0, 0, 0, 0, 0, 0, 0]' in log
 if condition=='loop':
  counters=json.loads(next(l[7:] for l in log.splitlines() if l.startswith('RESULT ')))
  assert counters['head']==counters['completed']==24 and counters['accepted']==counters['closed']==24
  assert counters['sqhead']==counters['sqtail'] and counters['cqhead']==counters['cqtail']
  assert all(counters[k]==0 for k in ['pending','error','reserved','dropped','overflow','trace_overflow'])
  assert counters['max_requests']>1,counters
  emit('ring',counters=counters)
 code=0
except BaseException as e:emit('failure',error=repr(e),traceback=traceback.format_exc());traceback.print_exc()
finally:
 if p is not None and p.poll() is None:p.terminate();emit('cleanup_server',exit=p.wait())
 if attached:
  q=subprocess.run(['./build/bpfusion_load','stream-detach'],env=env,capture_output=True,text=True)
  emit('detach',exit=q.returncode,stdout=q.stdout,stderr=q.stderr)
  for n in ['bpfusion_ctl','bpfusion_stats','bpfusion_db']:pathlib.Path('/sys/fs/bpf',n).unlink(missing_ok=True)
  if q.returncode:code=1
 emit('terminal',exit=code);raw.close()
print('CASE_TERMINAL',condition,code,flush=True)
raise SystemExit(code)
