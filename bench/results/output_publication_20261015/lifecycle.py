import datetime,json,os,re,signal,socket,struct,subprocess,sys,time
os.chdir("/workspaces/repository")
condition=sys.argv[1];assert condition in ["native","loop"]
name=sys.argv[2];assert name in ["smol","qwen"]
root=os.path.join(os.path.dirname(os.path.abspath(__file__)),"lifecycle_"+name+"_"+condition);base=os.path.dirname(root)
os.makedirs(root,exist_ok=False)
cfg=json.load(open(base+"/"+name+"_frozen.json"));asset=json.load(open(base+"/frozen_references.json"))
oracle_doc={"frozen_at":"pre-observation0045: "+asset["source_commit"]};paths={name:cfg["model"]};vocab=cfg["frozen_model"]["vocab"]
reference_pool={(tuple(r["prompt"]),r["gen"]):{tuple(s) for s in r["sequences"]} for r in cfg["frozen_model"]["references"]}
cases=[(0,1),(0,64),(1,1),(1,64),(2,64),(3,64),(0,64),(2,64)]
oracle={"rows":[dict(prompt=cfg["prompts"][case],gen=gen,tokens=list(sorted(reference_pool[tuple(cfg["prompts"][case]),gen])[0])) for case,gen in cases]}
pins=["bpfusion_ctl","bpfusion_stats","bpfusion_db","bpfusion_streams","bpfusion_stream_link",
      "bpfusion_uring_link","bpfusion_uring_owner","bpfusion_uring_bind_link"]
assert not any(os.path.exists("/sys/fs/bpf/"+n) for n in pins)
result={"model":name,"start":datetime.datetime.now(datetime.timezone.utc).isoformat(),"oracle_frozen_at":oracle_doc["frozen_at"]}
p=None;native_pid=None;clients=[];rows=[];streams=[]
try:
    if condition=="loop":
        a=subprocess.run(["build/bpfusion_load","stream-uring-attach"],text=True,capture_output=True);assert a.returncode==0,(a.stdout,a.stderr)
        result["attach"]={"exit":a.returncode,"stdout":a.stdout,"stderr":a.stderr}
    cmd=["strace","-D","-f","-ttt","-o",root+"/"+name+".strace","-e",
         "trace=accept,accept4,recvfrom,recvmsg,sendto,sendmsg,io_uring_setup,io_uring_enter,io_uring_register",
         base+"/candidate-build/vllm_graph_uring_loop" if condition=="loop" else base+"/candidate-build/vllm_graph_user_network_wait",paths[name],"180"]
    err=open(root+"/"+name+".native.stderr","w");log=open(root+"/"+name+".native.stdout","w")
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True);lines=[]
    while True:
        line=p.stdout.readline();lines.append(line);log.write(line);log.flush()
        if condition=="loop" and line.startswith("NET_READY "):native_pid=int(re.search(r"pid=(\d+)",line).group(1));break
        if condition=="native" and line.startswith("resident vLLM ready"):native_pid=p.pid;break
        if not line:raise RuntimeError("failed before READY")
    result["ready_time_ns"]=time.time_ns();result["native_pid"]=native_pid
    def connect():
        c=socket.create_connection(("127.0.0.1",39403),timeout=15);c.settimeout(15);clients.append(c);return c
    def request(c,case,http=True,invalid=False):
        ref=oracle["rows"][case];ids=[vocab] if invalid else ref["prompt"];gen=1 if invalid else ref["gen"]
        stamp=time.monotonic_ns()
        body=struct.pack("<IIIIQ",0x514c4d51,len(ids),gen,0,stamp)+struct.pack("<"+"I"*len(ids),*ids)
        wire=body
        if http:wire=b"POST /generate HTTP/1.1\r\nContent-Length: "+str(len(body)).encode()+b"\r\n\r\n"+body
        c.sendall(wire)
        row={"case":case,"protocol":"http" if http else "binary","invalid":invalid,"client_ns":stamp,"request_hex":wire.hex(),
             "peer":list(c.getsockname()),"gen":gen,"prompt":ids}
        rows.append(row);return row,ref
    def read(c,row,ref,partial=False):
        prefix=bytearray()
        if row["protocol"]=="http":
            while not prefix.endswith(b"\r\n\r\n"):
                part=c.recv(1)
                if not part:raise RuntimeError("early header EOF")
                prefix.extend(part)
        count=1 if partial else row["gen"];data=bytearray()
        while len(data)<4*count:
            part=c.recv(4*count-len(data))
            if not part:raise RuntimeError("early token EOF")
            data.extend(part)
        actual=tuple(struct.unpack("<"+"I"*count,data))
        allowed=reference_pool[tuple(ref["prompt"]),ref["gen"]]
        assert any(actual==sequence[:count] for sequence in allowed),(row,data.hex(),allowed)
        row.update({"reply_hex":(prefix+data).hex(),"checked_tokens":count,"partial":partial,"exact":True})
    for idle_repeat in range(8):
        time.sleep(2.2)
        c=connect();row,ref=request(c,0);read(c,row,ref)
        row,ref=request(c,0,invalid=True)
        header=bytearray()
        while not header.endswith(b"\r\n\r\n"):
            chunk=c.recv(1);assert chunk;header.extend(chunk)
        assert header.startswith(b"HTTP/1.1 400 Bad Request\r\n") and b"Content-Length: 0\r\n" in header
        row.update({"reply_hex":header.hex(),"status":400,"checked_tokens":0,"exact":True})
        row,ref=request(c,1);read(c,row,ref)
        c.shutdown(socket.SHUT_WR);assert c.recv(1)==b"";c.close()
    time.sleep(2.2)
    c=connect();row,ref=request(c,0);read(c,row,ref)
    row,ref=request(c,0,invalid=True)
    header=bytearray()
    while not header.endswith(b"\r\n\r\n"):
        chunk=c.recv(1);assert chunk;header.extend(chunk)
    assert header.startswith(b"HTTP/1.1 400 Bad Request\r\n") and b"Content-Length: 0\r\n" in header
    row.update({"reply_hex":header.hex(),"status":400,"checked_tokens":0,"exact":True})
    row,ref=request(c,1);read(c,row,ref)
    # Invalid binary request closes the reused connection and releases its slot.
    row,ref=request(c,0,http=False,invalid=True);assert c.recv(1)==b""
    row.update({"reply_hex":"","status":"EOF","checked_tokens":0,"exact":True});c.close()
    c=connect();row,ref=request(c,2,http=False);read(c,row,ref)
    c.shutdown(socket.SHUT_WR);assert c.recv(1)==b"";c.close()
    # Reset after a real first token; no host cancellation of inference.
    c=connect();row,ref=request(c,7,http=False);read(c,row,ref,partial=True)
    c.setsockopt(socket.SOL_SOCKET,socket.SO_LINGER,struct.pack("ii",1,0));c.close();row["action"]="RST"
    c=connect();row,ref=request(c,3);read(c,row,ref)
    c.shutdown(socket.SHUT_WR);assert c.recv(1)==b"";c.close()
    # Stop with a model generation plus accept/receive work pending.
    c=connect();row,ref=request(c,7);read(c,row,ref,partial=True);row["action"]="SIGTERM"
    os.kill(native_pid,signal.SIGTERM)
    remaining=bytearray()
    try:
        while True:
            chunk=c.recv(4096)
            if not chunk:break
            remaining.extend(chunk)
    except ConnectionResetError:
        row["stop_connection_reset"]=True
    row["post_stop_extra_hex"]=remaining.hex();c.close()
    tail,_=p.communicate(timeout=30);log.write(tail);log.close();err.close()
    result.update({"cmd":cmd,"exit":p.returncode,"stdout":"".join(lines)+tail,"stderr":open(root+"/"+name+".native.stderr").read(),"rows":rows})
    if condition=="native":
        result["model_errors"]=[int(re.search(r"resident vLLM stopped:.*graph_error=(\d+)",result["stdout"]).group(1))]
        values=re.search(r"userspace TCP stopped: accepted=(\d+) published=(\d+) completed=(\d+) rejected=(\d+)",result["stdout"])
        assert values,"missing native accounting"
        counts=dict(zip(["accepted","published","completed","rejected"],map(int,values.groups())));result["native_stats"]=counts
        result["pass"]=bool(p.returncode==0 and result["model_errors"]==[0] and counts["accepted"]==13 and counts["published"]==32 and counts["completed"]==31 and counts["rejected"]==10 and len(rows)==32 and all(row["exact"] for row in rows) and "graph_error=0" in result["stdout"])
    else:
        s=next(json.loads(l[7:]) for l in result["stdout"].splitlines() if l.startswith("RESULT "));result["native_stats"]=s
        result["replies"]=[json.loads(l[6:]) for l in result["stdout"].splitlines() if l.startswith("REPLY ")]
        b=subprocess.run(["build/bpfusion_load","stats"],text=True,capture_output=True)
        result["bpf_stats"]={"exit":b.returncode,"stdout":b.stdout,"stderr":b.stderr}
        result["model_errors"]=[int(re.search(r"resident vLLM stopped:.*graph_error=(\d+)",result["stdout"]).group(1))]
        result["pass"]=bool(result["model_errors"]==[0] and p.returncode==0 and s["error"]==s["pending"]==s["reserved"]==s["dropped"]==s["overflow"]==s["trace_overflow"]==0
             and s["accepted"]==s["closed"]==13 and s["head"]==s["completed"]==32 and s["aborted"]==3
             and s["sqhead"]==s["sqtail"] and s["cqhead"]==s["cqtail"]
             and len(rows)==32 and all(r["exact"] for r in rows)
             and "graph_error=0" in result["stdout"])
except Exception as e:
    result["error"]=repr(e);result["pass"]=False
    view=subprocess.run(["build/bpfusion_load","stats"],capture_output=True,text=True)
    result["failure_page"]={"exit":view.returncode,"stdout":view.stdout,"stderr":view.stderr}
    result["failure_tcp"]=[]
    for tcp_file in ("/proc/net/tcp","/proc/net/tcp6"):
        try:
            for line in open(tcp_file):
                fields=line.split()
                if len(fields)>3 and (fields[1].endswith(":99EB") or fields[2].endswith(":99EB")):
                    result["failure_tcp"].append({"file":tcp_file,"line":line.strip()})
        except OSError:pass
    if __import__("shutil").which("ss"):
        snap=subprocess.run(["ss","-tinp"],capture_output=True,text=True)
        result["failure_ss"]=snap.stdout
    result["failure_fdinfo"]={}
    if native_pid:
        for info in __import__("pathlib").Path("/proc/"+str(native_pid)+"/fdinfo").glob("*"):
            try:
                target=os.readlink("/proc/"+str(native_pid)+"/fd/"+info.name)
                if "io_uring" in target:result["failure_fdinfo"][info.name]={"target":target,"text":info.read_text()}
            except OSError:pass
        result["failure_tasks"]=[]
        for task in __import__("pathlib").Path("/proc/"+str(native_pid)+"/task").glob("*"):
            try:result["failure_tasks"].append({"tid":task.name,"comm":(task/"comm").read_text(),"stat":(task/"stat").read_text(),"wchan":(task/"wchan").read_text()})
            except OSError:pass
    for c in clients:
        try:c.close()
        except Exception:pass
    if p:
        if p.poll() is None and native_pid:os.kill(native_pid,signal.SIGTERM)
        tail,_=p.communicate(timeout=30);log.write(tail);log.close();err.close()
        result.update({"exit":p.returncode,"stdout":"".join(lines)+tail,"stderr":open(root+"/"+name+".native.stderr").read(),"rows":rows})
finally:
    result["end"]=datetime.datetime.now(datetime.timezone.utc).isoformat()
    for pin in pins:
        if os.path.exists("/sys/fs/bpf/"+pin):os.unlink("/sys/fs/bpf/"+pin)
    result["remaining_pins"]=[n for n in pins if os.path.exists("/sys/fs/bpf/"+n)]
    open(root+"/"+name+".results.json","w").write(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k not in ("cmd","stdout","stderr","rows","replies")},indent=2),flush=True)
    print(result.get("stdout","")[-2600:],flush=True);print(result.get("stderr","")[-1200:],flush=True)
    print("LIFECYCLE_DRIVER_TERMINAL",flush=True)
