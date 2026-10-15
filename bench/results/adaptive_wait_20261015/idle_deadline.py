import pathlib,subprocess,os,json,time,signal,datetime
t=pathlib.Path(__file__).resolve().parent;r=pathlib.Path('/workspaces/repository');os.chdir(r)
env=dict(os.environ,**json.loads((t/'environment.json').read_text()));env.pop('VLLM_BATCH_INVARIANT',None)
model=json.loads((t/'models.json').read_text())['qwen']
p=None;attached=False;result={'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'service_seconds':2,'post_ready_bound_s':15};code=1
try:
 assert not pathlib.Path('/sys/fs/bpf/bpfusion_ctl').exists()
 z=subprocess.run(['./build/bpfusion_load','stream-uring-attach'],capture_output=True,text=True)
 result['attach']={'exit':z.returncode,'stdout':z.stdout,'stderr':z.stderr};assert z.returncode==0;attached=True
 cmd=[str(t/'candidate-build/vllm_graph_uring_loop_trace'),model,'2','--trace-output',str(t/'idle_deadline.gpu.jsonl'),'--trace-requests','1'];result['command']=cmd
 logpath=t/'idle_deadline.executor.stdout'
 with logpath.open('x') as out:p=subprocess.Popen(cmd,cwd=r,env=env,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
 result['pid']=p.pid
 while 'resident vLLM ready' not in logpath.read_text():
  if p.poll() is not None:raise RuntimeError('executor failed before ready')
  time.sleep(.1)
 ready=time.monotonic_ns();result['ready_observed_ns']=ready
 try:status=p.wait(timeout=15)
 except subprocess.TimeoutExpired:
  result['deadline_hang']=True;raise
 result['exit']=status;result['ready_to_process_exit_s']=(time.monotonic_ns()-ready)/1e9
 log=logpath.read_text();result['stdout']=log
 assert status==0 and 'graph_error=0' in log and 'CLEANUP ring_connections_buffers_released' in log
 counters=json.loads(next(line[7:] for line in log.splitlines() if line.startswith('RESULT ')));result['counters']=counters
 assert all(counters[k]==0 for k in ['accepted','closed','received','completed','pending','error','head','reserved','dropped','overflow','trace_count','trace_overflow'])
 assert counters['sqhead']==counters['sqtail'] and counters['cqhead']==counters['cqtail']
 trace=[json.loads(line) for line in (t/'idle_deadline.gpu.jsonl').open()]
 assert trace[-1]['event']=='terminal' and trace[-1]['overflows']==0 and not any(e['event']=='admission' for e in trace)
 assert not pathlib.Path(str(t/'idle_deadline.gpu.jsonl')+'.references.jsonl').read_text()
 code=0
except BaseException as exc:
 result['failure']=repr(exc)
finally:
 if p is not None and p.poll() is None:
  os.killpg(p.pid,signal.SIGTERM)
  try:p.wait(timeout=30)
  except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
  result['cleanup_exit']=p.returncode
 if attached:
  z=subprocess.run(['./build/bpfusion_load','stats'],capture_output=True,text=True);result['final_stats']={'exit':z.returncode,'stdout':z.stdout,'stderr':z.stderr}
  z=subprocess.run(['./build/bpfusion_load','stream-detach'],capture_output=True,text=True);result['detach']={'exit':z.returncode,'stdout':z.stdout,'stderr':z.stderr}
  for name in ['bpfusion_ctl','bpfusion_stats','bpfusion_db']:pathlib.Path('/sys/fs/bpf',name).unlink(missing_ok=True)
 result.update(exit_code=code,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 (t/'idle_deadline.result.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='stdout'}),flush=True)
raise SystemExit(code)
