from pathlib import Path
import subprocess,json,os,time,datetime,re,signal
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
py=str(t/'runtime/bin/python');build=t/'build'
models=[('qwen','Qwen/Qwen2.5-0.5B-Instruct','7ae557604adf67be50417f59c2c2f167def9a775'),
 ('smol','HuggingFaceTB/SmolLM2-135M','93efa2f097d58c2a74874c7e644dbc9b0cee75a2')]
env['HF_HOME']='/workspaces/.cache/huggingface'
statuses=[]
def stamp():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(tag,cmd):
 with (t/(tag+'.stdout')).open('x') as out,(t/(tag+'.stderr')).open('x') as err:
  z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 record=dict(tag=tag,command=cmd,exit=z.returncode,utc=stamp())
 statuses.append(record);(t/'commands.json').write_text(json.dumps(statuses,indent=2))
 print(json.dumps(record),flush=True)
 return z.returncode
assert not Path('/sys/module/bfusion_tx').exists()
assert not Path('/sys/fs/bpf/bpfusion_ctl').exists()
exit_code=1
try:
 for name,repo,revision in models:
  tag='download_'+name
  cmd=[py,'-c','from huggingface_hub import snapshot_download; print(snapshot_download('+repr(repo)+',revision='+repr(revision)+'))']
  assert run(tag,cmd)==0
  model=(t/(tag+'.stdout')).read_text().splitlines()[-1].strip()
  assert Path(model).is_dir()
  for mode in ['kernel','native']:
   tag=name+'_'+mode
   attached=False;p=None
   try:
    if mode=='kernel':
     assert run(tag+'_attach',[str(build/'bpfusion_load'),'stream-uring-attach'])==0;attached=True
    binary=build/('vllm_graph_uring_loop' if mode=='kernel' else 'vllm_graph_user_network_wait')
    command=[str(binary),model,'120']
    with (t/(tag+'.server.stdout')).open('x') as out:
     p=subprocess.Popen(command,cwd=r,env=env,stdout=out,stderr=subprocess.STDOUT)
    (t/(tag+'.server.process.json')).write_text(json.dumps(dict(command=command,pid=p.pid,utc=stamp()),indent=2))
    while 'resident vLLM ready:' not in (t/(tag+'.server.stdout')).read_text():
     if p.poll() is not None:raise RuntimeError('server exited before ready: '+tag)
     time.sleep(.2)
    print('READY',tag,p.pid,flush=True)
    for http,gen in [(True,1),(True,32),(False,32)]:
     client_tag=tag+('_http' if http else '_tcp')+'_gen'+str(gen)
     cmd=[py,str(r/'tools/llm_tcp_client.py'),'--model',model,'--gen',str(gen),'--rounds','1']+(['--http'] if http else [])
     assert run(client_tag,cmd)==0
     output=(t/(client_tag+'.stdout')).read_text()
     assert 'text:' in output and 'TCP reply TTFT us:' in output
     if gen==1:assert 'TPOT: n/a (one output token)' in output
    http=(t/(tag+'_http_gen32.stdout')).read_text().splitlines()[0]
    tcp=(t/(tag+'_tcp_gen32.stdout')).read_text().splitlines()[0]
    assert http==tcp
    p.send_signal(signal.SIGTERM);returncode=p.wait()
    assert returncode==0,(tag,returncode)
    log=(t/(tag+'.server.stdout')).read_text()
    assert 'graph_error=0' in log and 'admitted=3 retired=3' in log
    if mode=='kernel':
     assert 'CLEANUP ring_connections_buffers_released' in log
     assert run(tag+'_stats',[str(build/'bpfusion_load'),'stats'])==0
     stats=(t/(tag+'_stats.stdout')).read_text()
     assert 'llm_reserved=0x0' in stats and 'llm_queued=0' in stats
    statuses.append(dict(tag=tag+'_server',exit=returncode,requests=3,output_tokens=65,utc=stamp()))
    (t/'commands.json').write_text(json.dumps(statuses,indent=2))
    print('PASS',tag,flush=True)
   finally:
    if p is not None and p.poll() is None:p.terminate();p.wait()
    if attached:
     run(tag+'_detach',[str(build/'bpfusion_load'),'stream-detach'])
     for n in ['bpfusion_ctl','bpfusion_stats','bpfusion_db']:Path('/sys/fs/bpf',n).unlink(missing_ok=True)
 assert run('invalid_gen',[py,str(r/'tools/llm_tcp_client.py'),'--gen','0'])==2
 assert run('invalid_rounds',[py,str(r/'tools/llm_tcp_client.py'),'--rounds','0'])==2
 exit_code=0
finally:
 (t/'run.exit.json').write_text(json.dumps(dict(exit=exit_code,utc=stamp()),indent=2))
raise SystemExit(exit_code)
