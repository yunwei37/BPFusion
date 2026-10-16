from pathlib import Path
import concurrent.futures,ctypes,datetime,json,os,re,signal,socket,struct,subprocess,sys,time
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
out=t/'active_wait_graph_acceptance';out.mkdir()
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
def oracle(operation,index):
    if operation=='matmul':
        x=[float((k*11+index*3)%7-3) for k in range(64)]
        w=[float(k%7-3) for k in range(64)]
        y=[sum(x[8*i+k]*w[8*k+j] for k in range(8)) for i in range(8) for j in range(8)]
    else:
        v=float(index%3+1);x=[0.0]*64;y=[0.0]*64
        kind=index%4
        if kind==0:pass
        elif kind==1:
            x[0]=v
            for k in range(32):y[2*k]=v
        elif kind==2:
            for k in range(32):x[2*k]=v
            y[0]=32*v
        else:
            for k in range(32):x[2*k]=v if k%2==0 else -v
            y[32]=32*v
    return struct.pack('<64f',*x),y
def wire(payload,ni=64,no=64,http=False):
    body=struct.pack('<IIIIQ',0x514c4d51,ni,no,0,time.monotonic_ns())+payload[:4*ni]
    return b'POST /generate HTTP/1.1\r\nContent-Length: '+str(len(body)).encode()+b'\r\n\r\n'+body if http else body
def conn():
    c=socket.create_connection(('127.0.0.1',39403),15);c.settimeout(15);return c
def exact(c,n):
    data=bytearray()
    while len(data)<n:
        q=c.recv(n-len(data))
        assert q,('early EOF',n,len(data));data+=q
    return bytes(data)
def header(c):
    data=bytearray()
    while not data.endswith(b'\r\n\r\n'):data+=exact(c,1)
    return bytes(data)
results=[]
for operation in ['matmul','fft']:
 for transport in ['native','loop']:
    assert not list(Path('/sys/fs/bpf').glob('bpfusion*'))
    build=t/'active_wait_graph8'
    base=out/(operation+'_'+transport);base.mkdir()
    server=None;rows=[];streams=[]
    result=dict(operation=operation,transport=transport,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        if transport=='loop':
            z=subprocess.run([str(build/'bpfusion_load'),'stream-uring-attach'],cwd=r,text=True,capture_output=True)
            result['attach']=dict(exit=z.returncode,stdout=z.stdout,stderr=z.stderr);assert z.returncode==0,result['attach']
        lib=build/('graph_server_uring_loop.so' if transport=='loop' else 'graph_server_user_network_wait.so')
        cmd=[str(t/'runtime/bin/python'),str(r/'examples/torch_graph_server.py'),str(lib),operation,'--seconds','180']
        so=(base/'server.stdout').open('w');se=(base/'server.stderr').open('w')
        streams=[so,se];server=subprocess.Popen(cmd,cwd=r,env=env,stdout=so,stderr=se)
        deadline=time.monotonic()+90
        while 'graph backend ready:' not in (base/'server.stdout').read_text():
            assert server.poll() is None,(server.returncode,(base/'server.stderr').read_text())
            assert time.monotonic()<deadline,'startup timeout';time.sleep(.1)
        def request(index,http=False,client=None):
            c=client or conn();payload,want=oracle(operation,index);c.sendall(wire(payload,http=http))
            if http:
                h=header(c);assert h.startswith(b'HTTP/1.1 200 OK\r\n') and b'Content-Length: 256\r\n' in h
            data=exact(c,256);got=struct.unpack('<64f',data)
            assert list(got)==want,(index,got,want)
            if client is None:c.close()
            return dict(index=index,http=http,input_hex=payload.hex(),reply_hex=data.hex(),exact=True)
        # Independent analytic arithmetic oracle; no GPU output is an oracle.
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
            rows.extend(pool.map(lambda n:request(n,bool(n%2)),range(128)))
        c=conn()
        for n in range(8):rows.append(request(n,bool(n%2),c))
        time.sleep(2.2);rows.append(request(9,True,c))
        # Valid protocol shape but wrong backend size: reject and reuse HTTP.
        payload,_=oracle(operation,0);c.sendall(wire(payload,ni=63,http=True))
        h=header(c);assert h.startswith(b'HTTP/1.1 400 Bad Request\r\n') and b'Content-Length: 0\r\n' in h
        rows.append(dict(invalid='input_words63',http=True,reply_hex=h.hex(),status=400))
        rows.append(request(10,True,c));c.sendall(wire(payload,ni=63))
        assert c.recv(1)==b'';c.close();rows.append(dict(invalid='input_words63',http=False,status='EOF'))
        c=conn();rows.append(request(11,False,c));c.shutdown(socket.SHUT_WR);assert c.recv(1)==b'';c.close()
        # Pipeline crosses physical ring wrap and exercises FIFO ownership.
        c=conn();sent=[]
        for n in range(40):
            payload,want=oracle(operation,n);c.sendall(wire(payload));sent.append((n,payload,want))
        for n,payload,want in sent:
            data=exact(c,256);assert list(struct.unpack('<64f',data))==want
            rows.append(dict(index=n,pipeline=True,input_hex=payload.hex(),reply_hex=data.hex(),exact=True))
        c.close()
        # RST with outstanding work, followed by a successful fresh request.
        c=conn()
        for n in range(32):c.sendall(wire(oracle(operation,n)[0]))
        c.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack('ii',1,0));c.close()
        rows.append(request(12,True))
        # SIGTERM with already-written inputs and queued network operations.
        c=conn()
        for n in range(32):c.sendall(wire(oracle(operation,n)[0]))
        server.send_signal(signal.SIGTERM);observed=bytearray()
        try:
            while True:
                q=c.recv(8192)
                if not q:break
                observed+=q
        except ConnectionResetError:result['stop_reset']=True
        c.close()
        expected=b''.join(struct.pack('<64f',*oracle(operation,n)[1]) for n in range(32))
        # Signed zero is allowed by the numeric oracle. Full observed words are
        # checked numerically, with any trailing partial word kept verbatim.
        full=len(observed)//4
        assert len(observed)<=len(expected)
        assert struct.unpack('<'+'f'*full,observed[:full*4])==struct.unpack('<'+'f'*full,expected[:full*4])
        result.update(stop_observed_hex=observed.hex(),stop_expected_hex=expected.hex(),stop_partial_word_hex=observed[full*4:].hex())
        assert server.wait(timeout=30)==0
        log=(base/'server.stdout').read_text();assert 'graph_error=0' in log
        if transport=='loop':
            ring=json.loads(next(s[7:] for s in log.splitlines() if s.startswith('RESULT ')))
            assert all(ring[k]==0 for k in ['error','pending','reserved','dropped','overflow'])
            assert ring['sqhead']==ring['sqtail'] and ring['cqhead']==ring['cqtail']
            assert ring['accepted']==ring['closed'];result['ring']=ring
        result.update(passed=True,command=cmd,completed_checks=len(rows),rows=rows)
    except BaseException as e:
        result.update(passed=False,error=repr(e),rows=rows)
        raise
    finally:
        if server and server.poll() is None:
            server.send_signal(signal.SIGTERM)
            try:server.wait(timeout=30)
            except subprocess.TimeoutExpired:server.kill();server.wait()
        for f in streams:f.close()
        if transport=='loop':
            z=subprocess.run([str(build/'bpfusion_load'),'detach'],cwd=r,text=True,capture_output=True)
            result['detach']=dict(exit=z.returncode,stdout=z.stdout,stderr=z.stderr)
            for name in ['bpfusion_ctl', 'bpfusion_stats', 'bpfusion_db', 'bpfusion_streams', 'bpfusion_stream_link', 'bpfusion_uring_link', 'bpfusion_uring_owner', 'bpfusion_uring_bind_link', 'bpfusion_pending']:
                pin=Path('/sys/fs/bpf')/name
                if pin.exists():pin.unlink()
            result['remaining_pins']=[p.name for p in Path('/sys/fs/bpf').glob('bpfusion*')]
        (base/'result.json').write_text(json.dumps(result,indent=2))
        results.append(result)
        (out/'summary.json').write_text(json.dumps([{k:v for k,v in x.items() if k!='rows'} for x in results],indent=2))
    print('PASS',operation,transport,len(rows),flush=True)
