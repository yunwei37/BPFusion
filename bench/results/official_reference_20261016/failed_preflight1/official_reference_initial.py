#!/usr/bin/env python3
"""Current whole-service official reference; same-executor transport controls."""
from pathlib import Path
import argparse,concurrent.futures,ctypes,datetime,http.client,json,math,os,re,secrets,signal,socket,statistics,subprocess,sys,threading,time,traceback
import numpy as np
import importlib.metadata
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
sys.path.insert(0,str(t/'confirm'))
from resident_dispatch import request as native_request
from official_api import external_request
orders=[['kernel','native','official'],['native','official','kernel'],['official','kernel','native'],['official','native','kernel'],['native','kernel','official']]
pins=['bpfusion_ctl','bpfusion_stats','bpfusion_db','bpfusion_streams','bpfusion_stream_link','bpfusion_uring_link','bpfusion_uring_owner','bpfusion_uring_bind_link','bpfusion_pending']
libc=ctypes.CDLL(None)
libc.clock_getcpuclockid.argtypes=[ctypes.c_int,ctypes.POINTER(ctypes.c_int)]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def group_cpu(group):
    result={}
    for p in Path('/proc').glob('[0-9]*/stat'):
        try:
            raw=p.read_text();fields=raw.rsplit(') ',1)[1].split()
            if int(fields[2])!=group:continue
            clock=ctypes.c_int();error=libc.clock_getcpuclockid(int(p.parent.name),ctypes.byref(clock))
            if error:continue
            result[p.parent.name]=dict(cpu_ns=time.clock_gettime_ns(clock.value),stat=raw)
        except (OSError,ValueError,ProcessLookupError):pass
    return result
def connect(mode):
    if mode=='official':
        c=http.client.HTTPConnection('127.0.0.1',39404,timeout=60)
        c.connect();c.sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1);return c
    c=socket.create_connection(('127.0.0.1',39403),timeout=60)
    c.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1);return c
def stop(p):
    try:os.killpg(p.pid,signal.SIGTERM)
    except ProcessLookupError:pass
    forced=False
    try:code=p.wait(timeout=60)
    except subprocess.TimeoutExpired:
        forced=True;os.killpg(p.pid,signal.SIGKILL);code=p.wait()
    deadline=time.monotonic()+60
    while group_cpu(p.pid) and time.monotonic()<deadline:time.sleep(.1)
    remaining=group_cpu(p.pid)
    if remaining:
        forced=True
        try:os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError:pass
    return dict(exit=code,forced=forced,remaining=remaining,utc=utc())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--preflight',action='store_true')
    args=ap.parse_args();os.chdir(r)
    assert subprocess.check_output(['git','symbolic-ref','--short','HEAD'],text=True).strip()=='main'
    args.output.parent.mkdir(parents=True,exist_ok=True)
    frozen=json.loads((t/'qwen_frozen.json').read_text());prompts=frozen['prompts'];vocab=frozen['frozen_model']['vocab']
    pools={(tuple(row['prompt']),row['gen']):row['sequences'] for row in frozen['frozen_model']['references']}
    env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
    official_env=dict(env);official_env.pop('VLLM_ENABLE_V1_MULTIPROCESSING',None)
    official_env['PATH']=str(t/'runtime/bin')+':'+official_env['PATH']
    model=json.loads((t/'models.json').read_text())['qwen']
    official_cmd=[str(t/'runtime/bin/vllm'),'serve',model,'--tokens-only','--dtype','half','--host','127.0.0.1','--port','39404']
    count=16 if args.preflight else 256;reps=1 if args.preflight else 5
    raw=args.output.open('x',buffering=1);lock=threading.Lock()
    def emit(event,**row):
        with lock:raw.write(json.dumps(dict(event=event,utc=utc(),**row))+'\n')
    emit('metadata',preflight=args.preflight,repetitions=reps,count=count,modes=['kernel','native','official'],orders=orders,prompts=prompts,vocab=vocab,gen=64,model=model,
         revision='7ae557604adf67be50417f59c2c2f167def9a775',official_command=official_cmd,source_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
         reference_pool=frozen['frozen_model'],driver_source=Path(__file__).read_text(),api_source=(t/'official_api.py').read_text(),
         sources={f:(r/f).read_text() for f in ['executor/vllm_mixed.cu','executor/vllm_mixed.py','executor/mixed_replay.py','executor/io_uring_tcp.h','executor/userspace_tcp.h','bpf/include/bpfusion_queue.h','Makefile']},
         runtime_versions={n:importlib.metadata.version(n) for n in ['vllm','torch','transformers','numpy']},boot_id=Path('/proc/sys/kernel/random/boot_id').read_text().strip(),
         gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,uuid,driver_version,memory.total,power.limit','--format=csv,noheader,nounits'],text=True).strip(),
         scope='whole-service fixed token budget; official API/compute/cache/capacity differ; no identical-output or total-resource claim')
    all_attempts=0;all_good=0;status=1
    try:
      for pair in range(reps):
       for mode in orders[pair]:
        assert not list(Path('/sys/fs/bpf').glob('bpfusion*'))
        prefix=args.output.with_name(args.output.stem+f'_p{pair}_{mode}')
        key=secrets.token_urlsafe(32);child_env=dict(official_env if mode=='official' else env)
        if mode=='official':child_env['VLLM_API_KEY']=key
        directory=t/'sourcebuild16';p=None;log=None
        try:
            if mode=='kernel':
                z=subprocess.run([str(directory/'bpfusion_load'),'stream-uring-attach'],text=True,capture_output=True)
                emit('attach',pair=pair,mode=mode,exit=z.returncode,stdout=z.stdout,stderr=z.stderr);assert z.returncode==0
            cmd=official_cmd if mode=='official' else [str(directory/('vllm_mixed_uring_loop' if mode=='kernel' else 'vllm_mixed_user_network_wait')),model,'600']
            path=prefix.with_suffix('.server.txt');log=path.open('x')
            p=subprocess.Popen(cmd,cwd=r,env=child_env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
            emit('start',pair=pair,mode=mode,pid=p.pid,command=cmd,log=str(path));print('START',pair,mode,p.pid,flush=True)
            while True:
                assert p.poll() is None,(mode,path.read_text()[-8000:])
                if mode=='official':
                    try:
                        c=connect(mode);c.request('GET','/health');resp=c.getresponse();good=resp.status==200;resp.read();c.close()
                        if good:break
                    except (OSError,http.client.HTTPException):pass
                elif 'resident vLLM ready:' in path.read_text():break
                time.sleep(.1)
            emit('ready',pair=pair,mode=mode,pid=p.pid,host_exposure={name:Path('/proc/'+name).read_text() for name in ['loadavg','pressure/cpu','stat']})
            if mode=='official':
                for token in [None,'invalid']:
                    c=connect(mode);headers={} if token is None else {'Authorization':'Bearer '+token}
                    c.request('POST','/inference/v1/generate',b'{}',headers);resp=c.getresponse()
                    assert resp.status==401;resp.read();c.close()
                emit('authentication',pair=pair,mode=mode,missing=401,invalid=401)
            def run(c,index,gen,observed):
                ids=prompts[index%4];want=pools[tuple(ids),gen][0]
                row=external_request(c,ids,want,key,observed) if mode=='official' else native_request(c,ids,None,gen=gen,observed=observed)
                assert len(row['tokens'])==gen and all(type(x)==int and 0<=x<vocab for x in row['tokens'])
                row.update(input_ids=ids,gen=gen,reference_set_match=list(row['tokens']) in pools[tuple(ids),gen])
                return row
            c=connect(mode)
            try:
                for i in range(8):emit('warmup',pair=pair,mode=mode,index=i,**run(c,i,1,{}))
            finally:c.close()
            for regime in (['offered192','closed16'] if pair%2==0 else ['closed16','offered192']):
                attempts=[];state=threading.Lock();active=0;peak=0
                def attempt(index,client=None,due=None):
                    nonlocal active,peak
                    thread_start=time.monotonic_ns();row=dict(index=index,gen=64,input_ids=prompts[index%4],thread_start_ns=thread_start)
                    if due is not None:row['scheduled_ns']=due
                    observed={};owned=client is None
                    with state:active+=1;peak=max(peak,active)
                    try:
                        row['connection_reused']=not owned
                        if owned:
                            row['connect_begin_ns']=time.monotonic_ns();client=connect(mode)
                            row['connect_end_ns']=time.monotonic_ns()
                        row.update(run(client,index,64,observed));row['outcome']='success'
                    except BaseException as error:
                        row.update(observed,outcome='error',error_type=type(error).__name__,error=str(error),error_kind='transport' if isinstance(error,(OSError,http.client.HTTPException)) else 'protocol_or_validation')
                    finally:
                        row['finish_ns']=time.monotonic_ns()
                        if owned and client is not None:client.close()
                        with state:active-=1;attempts.append(row)
                    return row
                if regime=='offered192':
                    rng=np.random.RandomState(20261015+pair)
                    delays=np.cumsum([rng.gamma(shape=1.0,scale=1.0/192) for _ in range(count)])
                    delays*= (count/192)/delays[-1]
                    before=group_cpu(p.pid);epoch=time.monotonic_ns();scheduled=[epoch+int(x*1e9) for x in delays]
                    emit('arrival_schedule',pair=pair,mode=mode,regime=regime,epoch_ns=epoch,scheduled_ns=scheduled,seed=20261015+pair)
                    threads=[]
                    for i,due in enumerate(scheduled):
                        delay=(due-time.monotonic_ns())/1e9
                        if delay>0:time.sleep(delay)
                        th=threading.Thread(target=attempt,args=(i,None,due));threads.append(th);th.start()
                    for th in threads:th.join()
                    end=time.monotonic_ns();after=group_cpu(p.pid)
                else:
                    ready=threading.Barrier(17);start=threading.Barrier(17)
                    def lane(lane_id):
                        c=connect(mode)
                        try:
                            ready.wait(timeout=60);start.wait(timeout=60)
                            for i in range(lane_id,count,16):attempt(i,c)
                        finally:c.close()
                    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
                        futures=[pool.submit(lane,i) for i in range(16)]
                        ready.wait(timeout=60);before=group_cpu(p.pid);epoch=time.monotonic_ns();start.wait(timeout=60)
                        for future in futures:future.result()
                        end=time.monotonic_ns();after=group_cpu(p.pid)
                assert len(attempts)==count and active==0
                for row in sorted(attempts,key=lambda x:x['index']):emit('request',pair=pair,mode=mode,regime=regime,**row)
                good=[x for x in attempts if x['outcome']=='success']
                group_stable=before.keys()==after.keys()
                cpu=sum(x['cpu_ns'] for x in after.values())-sum(x['cpu_ns'] for x in before.values()) if group_stable else None
                emit('cell',pair=pair,mode=mode,regime=regime,attempts=count,successes=len(good),failures=count-len(good),begin_ns=epoch,end_ns=end,
                     output_tokens=sum(len(x['tokens']) for x in good),partial_tokens=sum(len(x.get('tokens',[])) for x in attempts if x['outcome']!='success'),max_in_flight=peak,cpu_before=before,cpu_after=after,process_group_stable=group_stable,process_group_cpu_ns=cpu)
                all_attempts+=count;all_good+=len(good)
            receipt=stop(p);emit('executor',pair=pair,mode=mode,**receipt,stdout=path.read_text())
            if mode!='official':assert receipt['exit']==0 and 'graph_error=0' in path.read_text()
            p=None;print('PASS',pair,mode,flush=True)
        finally:
            if p is not None:emit('cleanup',pair=pair,mode=mode,**stop(p))
            if log:log.close()
            if mode=='kernel':
                z=subprocess.run([str(directory/'bpfusion_load'),'stream-detach'],text=True,capture_output=True)
                emit('detach',pair=pair,mode=mode,exit=z.returncode,stdout=z.stdout,stderr=z.stderr)
                for name in pins:
                    q=Path('/sys/fs/bpf')/name
                    if q.exists():q.unlink()
      status=0
    except BaseException as error:
        emit('failure',error_type=type(error).__name__,error=str(error),traceback=traceback.format_exc());traceback.print_exc()
    finally:
        emit('terminal',exit=status,attempts=all_attempts,successes=all_good,failures=all_attempts-all_good);raw.close()
    raise SystemExit(status)
if __name__=='__main__':main()
