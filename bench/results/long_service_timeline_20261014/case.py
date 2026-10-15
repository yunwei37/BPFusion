import os,pathlib,json,subprocess,sys,time,importlib.util,datetime,threading,traceback,re
from concurrent.futures import ThreadPoolExecutor
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository');os.chdir(r)
model,pair,path,condition,stage=sys.argv[1:];pair=int(pair)
assert path in ['loop','native'] and condition in ['unprofiled','profiled'] and stage in ['preflight','full']
count=8 if stage=='preflight' else 32
cfg=json.loads((t/'models.json').read_text())[model];key=f'{stage}_{model}_p{pair}_{path}_{condition}'
d=t/key;d.mkdir();entry='vllm_graph_uring_loop_trace' if path=='loop' else 'vllm_graph_user_network_wait_trace'
(d/entry).write_text((t/'adapter.py').read_text());(d/(entry+'.so')).symlink_to(t/'build'/(entry+'.so'))
spec=importlib.util.spec_from_file_location('client',r/'bench/resident_dispatch.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
env=dict(os.environ,PATH=str(t/'runtime/bin')+':'+os.environ['PATH'],LD_LIBRARY_PATH=str(t/'libbpf_install/usr/lib64'),TORCH_EXTENSIONS_DIR=str(t/'cuda_extensions'),VLLM_ENABLE_V1_MULTIPROCESSING='0',BF_DIAGNOSTIC_PROFILE='1' if condition=='profiled' else '0',BF_BIND='127.0.0.1')
os.environ['BF_BIND']='127.0.0.1'
raw=(t/(key+'.jsonl')).open('x',buffering=1);lock=threading.Lock()
def emit(event,**kw):
 with lock:raw.write(json.dumps(dict(event=event,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),**kw))+'\n')
emit('metadata',model=model,pair=pair,path=path,condition=condition,stage=stage,requests=count,warmups=8,prompts=cfg['prompts'],frozen_model=cfg['frozen_model'],source=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),driver_source=pathlib.Path(__file__).read_text(),adapter_source=(t/'adapter.py').read_text(),client_source=(r/'bench/resident_dispatch.py').read_text(),library=str((d/(entry+'.so')).resolve()),library_stat={'size':(d/(entry+'.so')).stat().st_size,'inode':(d/(entry+'.so')).stat().st_ino})
pool={(tuple(x['prompt']),x['gen']):{tuple(s) for s in x['sequences']} for x in cfg['frozen_model']['references']}
p=None;attached=False;code=1;logpath=d/'server.stdout';gpu=d/'model.gpu.jsonl'
try:
 assert not pathlib.Path('/sys/module/bfusion_tx').exists() and not pathlib.Path('/sys/fs/bpf/bpfusion_ctl').exists()
 if path=='loop':
  a=subprocess.run(['./build/bpfusion_load','stream-uring-attach'],env=env,capture_output=True,text=True);emit('attach',exit=a.returncode,stdout=a.stdout,stderr=a.stderr);assert a.returncode==0;attached=True
 cmd=[str(t/'runtime/bin/python'),str(d/entry),cfg['model'],'300','--trace-output',str(gpu),'--trace-requests',str(count+8)]
 with logpath.open('w') as out:p=subprocess.Popen(cmd,env=env,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
 emit('start',pid=p.pid,command=cmd);print('START',key,p.pid,flush=True)
 while 'resident vLLM ready' not in logpath.read_text():
  assert p.poll() is None,logpath.read_text()[-6000:]
  time.sleep(.1)
 emit('ready',pid=p.pid)
 with c.connect() as client:
  for i in range(8):
   ids=cfg['prompts'][i%4];row=c.request(client,ids,None,gen=1);assert tuple(row['tokens']) in pool[(tuple(ids),1)]
   emit('request',index=i,input_ids=ids,gen=1,warmup=True,**row)
 ready=threading.Barrier(9);start=threading.Barrier(9);rows=[]
 def lane(i):
  with c.connect() as client:
   ready.wait(timeout=60);start.wait(timeout=60)
   for index in range(i,count,8):
    ids=cfg['prompts'][index%4];row=c.request(client,ids,None,gen=64);assert tuple(row['tokens']) in pool[(tuple(ids),64)]
    rows.append(row);emit('request',index=index+8,input_ids=ids,gen=64,warmup=False,**row)
 with ThreadPoolExecutor(max_workers=8) as workers:
  fs=[workers.submit(lane,i) for i in range(8)];ready.wait(timeout=60);before=c.worker_cpu_snapshot(p.pid);start.wait(timeout=60)
  for f in fs:f.result()
 after=c.worker_cpu_snapshot(p.pid)
 emit('cell',first_ns=min(x['start_ns'] for x in rows),last_ns=max(x['arrival_ns'][-1] for x in rows),requests=count,tokens=count*64,**c.worker_cpu_delta(before,after))
 p.terminate();status=p.wait();log=logpath.read_text();emit('executor',pid=p.pid,exit=status,stdout=log)
 assert status==0 and 'graph_error=0' in log and f'admitted={count+8} retired={count+8}' in log
 if path=='loop':
  stats=json.loads(next(l[7:] for l in log.splitlines() if l.startswith('RESULT ')))
  assert stats['head']==stats['completed']==count+8 and stats['accepted']==stats['closed']==9
  assert all(stats[k]==0 for k in ['pending','error','reserved','dropped','overflow','trace_overflow'])
  assert stats['sqhead']==stats['sqtail'] and stats['cqhead']==stats['cqtail']
  emit('ring',counters=stats)
 else:
  stats={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',next(l for l in log.splitlines() if l.startswith('userspace TCP stopped:')))}
  assert stats=={'accepted':9,'published':count+8,'completed':count+8,'rejected':0}
  emit('native_tcp',counters=stats)
 assert gpu.exists()
 replay_entry=d/'vllm_graph_replay';replay_entry.write_text((t/'replay.py').read_text());replay_entry.with_suffix('.so').symlink_to(t/'build'/(entry+'.so'))
 replay_command=[str(t/'runtime/bin/python'),str(replay_entry),cfg['model'],'0','--trace-output',str(gpu),'--trace-requests',str(count+8)]
 replay_result=subprocess.run(replay_command,env=env,capture_output=True,text=True)
 (d/'replay.stdout').write_text(replay_result.stdout);(d/'replay.stderr').write_text(replay_result.stderr)
 emit('replay',command=replay_command,exit=replay_result.returncode,stdout=replay_result.stdout,stderr=replay_result.stderr)
 assert replay_result.returncode==0 and pathlib.Path(str(gpu)+'.references.jsonl').exists()
 emit('model_trace',path=str(gpu))
 if condition=='profiled':assert (d/'trace.json.gz').exists();emit('trace',path=str(d/'trace.json.gz'))
 code=0
except BaseException as e:emit('failure',error=repr(e),traceback=traceback.format_exc());traceback.print_exc()
finally:
 if p is not None and p.poll() is None:p.terminate();emit('cleanup_server',exit=p.wait())
 if attached:
  a=subprocess.run(['./build/bpfusion_load','stream-detach'],env=env,capture_output=True,text=True);emit('detach',exit=a.returncode,stdout=a.stdout,stderr=a.stderr)
  for n in ['bpfusion_ctl','bpfusion_stats','bpfusion_db']:pathlib.Path('/sys/fs/bpf',n).unlink(missing_ok=True)
  if a.returncode:code=1
 emit('terminal',exit=code);raw.close()
print('TERMINAL',key,code,flush=True)
raise SystemExit(code)
