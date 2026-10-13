import datetime,json,os,re,socket,struct,subprocess,time
os.chdir("/workspaces/repository")
root=os.path.dirname(os.path.abspath(__file__))
base=os.path.dirname(root)
import sys,signal
name=sys.argv[1]
oracle=json.load(open(root+"/oracle.json"))["models"][name]
assert len(oracle["rows"])==12
paths=json.load(open(root+"/model_paths.json"))
pins=["bpfusion_ctl","bpfusion_stats","bpfusion_db","bpfusion_streams","bpfusion_stream_link","bpfusion_uring_link"]
assert not any(os.path.exists("/sys/fs/bpf/"+n) for n in pins),"preserve existing owner"
result={"model":name,"oracle_frozen_at":json.load(open(root+"/oracle.json"))["frozen_at"],"started":datetime.datetime.now(datetime.timezone.utc).isoformat()}
p=None
try:
    attached=subprocess.run([base+"/loader","stream-attach"],text=True,capture_output=True)
    result["attach"]={"exit":attached.returncode,"stdout":attached.stdout,"stderr":attached.stderr}
    assert attached.returncode==0,result["attach"]
    cmd=["strace","-f","-ttt","-o",root+"/"+name+".strace","-e",
         "trace=accept,accept4,recvfrom,recvmsg,sendto,sendmsg,io_uring_setup,io_uring_enter,io_uring_register,close",
         "python3",root+"/qwen_graph.py",paths[name],"180"]
    stderr_file=open(root+"/"+name+".native.stderr","w")
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=stderr_file,text=True)
    lines=[]
    while True:
        line=p.stdout.readline();lines.append(line)
        if line.startswith("NET_READY "):
            native_pid=int(re.search(r"pid=(\d+)",line).group(1));result["native_pid"]=native_pid;break
        if not line:raise RuntimeError("native failed before READY")
    result["ready_time_ns"]=time.time_ns()
    time.sleep(2.2)
    client=socket.create_connection(("127.0.0.1",39403),timeout=10);client.settimeout(10)
    result["client_tuple"]=client.getsockname()
    prompts=[1,2,5,8,16,31,63,64,2,5,8,1]
    rows=[]
    for cycle,np in enumerate(prompts):
        if cycle<8:time.sleep(2.2)
        inputs=list(range(77+cycle,77+cycle+np))
        body=struct.pack("<IIIIQ",0x514c4d51,np,1,0,1000+cycle)+struct.pack("<"+"I"*np,*inputs)
        request=body
        if cycle%2:
            request=b"POST /generate HTTP/1.1\r\nContent-Type: application/octet-stream\r\nContent-Length: "+str(len(body)).encode()+b"\r\n\r\n"+body
        split=1 if cycle%2==0 else len(request)-len(body)+7
        sent_ns=time.time_ns();client.sendall(request[:split]);time.sleep(.001);client.sendall(request[split:])
        received=bytearray()
        if cycle%2:
            while not received.endswith(b"\r\n\r\n"):
                part=client.recv(1)
                if not part:raise RuntimeError("early header EOF")
                received.extend(part)
        header=bytes(received)
        data=bytearray()
        while len(data)<4:
            part=client.recv(4-len(data))
            if not part:raise RuntimeError("early token EOF")
            data.extend(part)
        received.extend(data)
        expected_header=(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 4\r\n\r\n" if cycle%2 else b"")
        assert inputs==oracle["rows"][cycle]["prompt"]
        expected=expected_header+struct.pack("<I",oracle["rows"][cycle]["tokens"][0])
        rows.append({"cycle":cycle,"prompt":inputs,"protocol":"http" if cycle%2 else "binary",
                     "split":split,"sent_ns":sent_ns,"request_hex":request.hex(),"reply_hex":received.hex(),
                     "expected_hex":expected.hex(),"exact":bytes(received)==expected})
    client.shutdown(socket.SHUT_WR)
    result["clean_eof"]=client.recv(1)==b"";client.close()
    os.kill(native_pid,signal.SIGTERM)
    tail,_=p.communicate(timeout=30)
    stderr_file.close();err=open(root+"/"+name+".native.stderr").read()
    result.update({"cmd":cmd,"exit":p.returncode,"stdout":"".join(lines)+tail,"stderr":err,"rows":rows})
    stats=subprocess.run(["build/bpfusion_load","stats"],text=True,capture_output=True)
    result["bpf_stats"]={"exit":stats.returncode,"stdout":stats.stdout,"stderr":stats.stderr}
    result["native_stats"]=next(json.loads(l[7:]) for l in result["stdout"].splitlines() if l.startswith("RESULT "))
    s=result["native_stats"]
    result["pass"]=bool(s["status"]==0 and s["accepted"]==s["closed"]==s["eof"]==1
        and s["received"]==s["sent"]==s["head"]==12 and s["reserved"]==s["dropped"]==s["overflow"]==0
        and s["sq_head"]==s["sq_tail"]==s["cq_head"]==s["cq_tail"]==28
        and s["idle_observed"]==9 and all(r["exact"] for r in rows) and result["clean_eof"]
        and p.returncode==0 and "CLEANUP " in result["stdout"])
except Exception as e:
    result["error"]=repr(e)
    if p and p.poll() is None:
        # The finite diagnostic kernel has its own timeout; preserve its real terminal output.
        tail,_=p.communicate(timeout=30);stderr_file.close();err=open(root+"/"+name+".native.stderr").read();result.update({"exit":p.returncode,"stdout":"".join(lines)+tail,"stderr":err})
    result["pass"]=False
finally:
    result["finished"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result["cleanup_pins"]=[]
    for name in pins:
        path="/sys/fs/bpf/"+name
        if os.path.exists(path):os.unlink(path);result["cleanup_pins"].append(name)
    result["remaining_pins"]=[n for n in pins if os.path.exists("/sys/fs/bpf/"+n)]
    open(root+"/"+name+".results.json","w").write(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ("rows","stdout","stderr")},indent=2),flush=True)
    print(result.get("stdout","")[-1400:],flush=True)
    print(result.get("stderr","")[-1200:],flush=True)
    print("DIAGNOSIS_TERMINAL",flush=True)
