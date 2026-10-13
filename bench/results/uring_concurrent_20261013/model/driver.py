import datetime,json,os,re,signal,socket,struct,subprocess,sys,threading,time
from concurrent.futures import ThreadPoolExecutor
os.chdir("/workspaces/repository")
root=os.path.dirname(os.path.abspath(__file__));base=os.path.dirname(root);name=sys.argv[1]
mode=sys.argv[2] if len(sys.argv)>2 else "concurrent"
oracle_file=json.load(open(root+"/oracle.json"));oracle=oracle_file["models"][name]
paths=json.load(open(root+"/model_paths.json"))
pins=["bpfusion_ctl","bpfusion_stats","bpfusion_db","bpfusion_streams","bpfusion_stream_link",
      "bpfusion_uring_link","bpfusion_uring_owner","bpfusion_uring_bind_link"]
assert not any(os.path.exists("/sys/fs/bpf/"+n) for n in pins),"preserve active owner"
result={"model":name,"mode":mode,"start":datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "oracle_frozen_at":oracle_file["frozen_at"],"source_head":subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()}
p=None;native_pid=None;stderr_file=None;log=None
clients=[]
try:
    a=subprocess.run([base+"/loader","stream-attach"],text=True,capture_output=True)
    result["attach"]={"exit":a.returncode,"stdout":a.stdout,"stderr":a.stderr};assert a.returncode==0,result["attach"]
    cmd=["strace","-f","-ttt","-o",root+"/"+name+"."+mode+".strace","-e",
         "trace=accept,accept4,recvfrom,recvmsg,sendto,sendmsg,io_uring_setup,io_uring_enter,io_uring_register",
         "python3",root+"/qwen_graph.py",paths[name],"180"]
    stderr_file=open(root+"/"+name+"."+mode+".native.stderr","w")
    log=open(root+"/"+name+"."+mode+".native.stdout","w")
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=stderr_file,text=True);lines=[]
    while True:
        line=p.stdout.readline();lines.append(line);log.write(line);log.flush()
        if line.startswith("NET_READY "):
            native_pid=int(re.search(r"pid=(\d+)",line).group(1));break
        if not line:raise RuntimeError("native failed before READY")
    result["ready_time_ns"]=time.time_ns();result["native_pid"]=native_pid
    def connect():
        c=socket.create_connection(("127.0.0.1",39403),timeout=15);c.settimeout(15);return c
    # Observe idle wake with real connects/requests, not a keepalive producer.
    time.sleep(2.2)
    for _ in range(24):
        c=connect();c.shutdown(socket.SHUT_WR);assert c.recv(1)==b"";c.close()
    result["empty_connections"]=24
    count=8 if mode=="concurrent" else 1
    clients=[connect() for _ in range(count)]
    tuples=[list(c.getsockname()) for c in clients];result["client_tuples"]=tuples
    time.sleep(2.2)
    barrier=threading.Barrier(count,timeout=30)
    def worker(index):
        c=clients[index];rows=[]
        for wave in range(3):
            case=(wave*8+index)%12 if mode=="concurrent" else wave
            ref=oracle["rows"][case];ids=ref["prompt"];ng=ref["gen"];http=(index+wave)%2==1
            barrier.wait();stamp=time.monotonic_ns()
            body=struct.pack("<IIIIQ",0x514c4d51,len(ids),ng,0,stamp)+struct.pack("<"+"I"*len(ids),*ids)
            request=body
            if http:request=b"POST /generate HTTP/1.1\r\nContent-Length: "+str(len(body)).encode()+b"\r\n\r\n"+body
            split=1 if not http else len(request)-len(body)+7
            c.sendall(request[:split]);time.sleep(.001);c.sendall(request[split:])
            prefix=bytearray()
            if http:
                while not prefix.endswith(b"\r\n\r\n"):
                    part=c.recv(1)
                    if not part:raise RuntimeError("early HTTP EOF")
                    prefix.extend(part)
            data=bytearray();chunks=[]
            while len(data)<ng*4:
                part=c.recv(ng*4-len(data));chunks.append({"bytes":len(part),"arrived_ns":time.monotonic_ns()})
                if not part:raise RuntimeError("early token EOF")
                data.extend(part)
            expected_prefix=(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: "+str(ng*4).encode()+b"\r\n\r\n" if http else b"")
            expected=expected_prefix+struct.pack("<"+"I"*ng,*ref["tokens"])
            row={"connection":index,"wave":wave,"case":case,"client_ns":stamp,"protocol":"http" if http else "binary",
                 "prompt":ids,"gen":ng,"request_hex":request.hex(),"reply_hex":(prefix+data).hex(),
                 "expected_hex":expected.hex(),"exact":prefix+data==expected,"chunks":chunks}
            rows.append(row);assert row["exact"],row
            barrier.wait()
        c.shutdown(socket.SHUT_WR);assert c.recv(1)==b"","extra response";c.close()
        return rows
    with ThreadPoolExecutor(max_workers=count) as pool:
        batches=list(pool.map(worker,range(count)))
    result["rows"]=[r for batch in batches for r in batch]
    os.kill(native_pid,signal.SIGTERM);tail,_=p.communicate(timeout=30);log.write(tail);log.close();log=None
    stderr_file.close();stderr_file=None
    result.update({"cmd":cmd,"exit":p.returncode,"stdout":"".join(lines)+tail,
                   "stderr":open(root+"/"+name+"."+mode+".native.stderr").read()})
    result["native_stats"]=next(json.loads(l[7:]) for l in result["stdout"].splitlines() if l.startswith("RESULT "))
    result["replies"]=[json.loads(l[6:]) for l in result["stdout"].splitlines() if l.startswith("REPLY ")]
    b=subprocess.run(["build/bpfusion_load","stats"],text=True,capture_output=True)
    result["bpf_stats"]={"exit":b.returncode,"stdout":b.stdout,"stderr":b.stderr}
    s=result["native_stats"];N=count*3
    result["pass"]=bool(p.returncode==0 and s["error"]==s["aborted"]==s["pending"]==s["reserved"]==s["dropped"]==s["overflow"]==s["trace_overflow"]==0
        and s["accepted"]==s["closed"]==24+count and s["completed"]==s["head"]==N
        and s["sqhead"]==s["sqtail"]==s["cqhead"]==s["cqtail"]
        and s["bytes"]==sum(len(bytes.fromhex(r["reply_hex"])) for r in result["rows"])
        and s["max_connections"]>=count and (s["max_requests"]==8 if count==8 else True)
        and len(result["replies"])==N and all(r["exact"] for r in result["rows"])
        and "graph_error=0 banks=8" in result["stdout"])
except Exception as error:
    result["error"]=repr(error);result["pass"]=False
    for c in clients:
        try:c.close()
        except Exception:pass
    if p:
        if p.poll() is None and native_pid:os.kill(native_pid,signal.SIGTERM)
        tail,_=p.communicate(timeout=30)
        if log:log.write(tail);log.close();log=None
        if stderr_file:stderr_file.close();stderr_file=None
        result.update({"exit":p.returncode,"stdout":"".join(lines)+tail,
                       "stderr":open(root+"/"+name+"."+mode+".native.stderr").read()})
finally:
    if log:log.close()
    if stderr_file:stderr_file.close()
    result["end"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result["cleanup_pins"]=[]
    for pin in pins:
        path="/sys/fs/bpf/"+pin
        if os.path.exists(path):os.unlink(path);result["cleanup_pins"].append(pin)
    result["remaining_pins"]=[n for n in pins if os.path.exists("/sys/fs/bpf/"+n)]
    open(root+"/"+name+"."+mode+".results.json","w").write(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ("stdout","stderr","rows","replies")},indent=2),flush=True)
    print(result.get("stdout","")[-2000:],flush=True);print(result.get("stderr","")[-1200:],flush=True)
    print("CONCURRENT_DRIVER_TERMINAL",flush=True)
