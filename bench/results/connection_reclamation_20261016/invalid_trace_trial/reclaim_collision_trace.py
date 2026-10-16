import datetime,json,os,re,signal,socket,struct,subprocess,sys,time
os.chdir("/workspaces/repository")
condition=sys.argv[1];assert condition in ("native","loop")
name=sys.argv[2];assert name in ["smol","qwen"]
banks=int(sys.argv[3]);assert banks in (8,16)
backend=sys.argv[4];assert backend=="vllm"
root=os.path.join(os.path.dirname(os.path.abspath(__file__)),"collision_trace_reclaim_"+backend+"_"+name+"_"+str(banks)+"_"+condition);base=os.path.dirname(root)
os.makedirs(root,exist_ok=False)
if backend=="hf":
    oracle_doc=json.load(open(base+"/hf_oracle.json"));oracle=oracle_doc["models"][name]
    paths=json.load(open(base+"/hf_model_paths.json"));vocab=json.load(open(paths[name]+"/config.json"))["vocab_size"]
    reference_pool={(tuple(row["prompt"]),row["gen"]):{tuple(row["tokens"])} for row in oracle["rows"]}
else:
    cfg=json.load(open(base+"/"+name+"_frozen.json"));asset=json.load(open(base+"/frozen_references.json"))
    oracle_doc={"frozen_at":asset["frozen_at"]};paths={name:cfg["model"]};vocab=cfg["frozen_model"]["vocab"]
    reference_pool={(tuple(row["prompt"]),row["gen"]):{tuple(seq) for seq in row["sequences"]} for row in cfg["frozen_model"]["references"]}
    cases=[(0,1),(0,64),(1,1),(1,64),(2,64),(3,64),(0,64),(2,64)]
    oracle={"rows":[dict(prompt=cfg["prompts"][case],gen=gen,tokens=list(sorted(reference_pool[tuple(cfg["prompts"][case]),gen])[0])) for case,gen in cases]}
pins=["bpfusion_ctl","bpfusion_stats","bpfusion_db","bpfusion_streams","bpfusion_stream_link",
      "bpfusion_uring_link","bpfusion_uring_owner","bpfusion_uring_bind_link","bpfusion_pending"]
assert not any(os.path.exists("/sys/fs/bpf/"+n) for n in pins)
result={"model":name,"start":datetime.datetime.now(datetime.timezone.utc).isoformat(),"oracle_frozen_at":oracle_doc["frozen_at"]}
p=None;native_pid=None;clients=[];rows=[];streams=[]
try:
    if condition=="loop":
        a=subprocess.run([base+"/reclaim_local"+str(banks)+"/bpfusion_load","stream-uring-attach"],text=True,capture_output=True);assert a.returncode==0,(a.stdout,a.stderr)
        result["attach"]={"exit":a.returncode,"stdout":a.stdout,"stderr":a.stderr}
    cmd=["strace","-D","-f","-ttt","-o",root+"/"+name+".strace","-e",
         "trace=accept,accept4,recvfrom,recvmsg,sendto,sendmsg,io_uring_setup,io_uring_enter,io_uring_register",
         base+"/reclaim_local"+str(banks)+"/"+("vllm_mixed_uring_loop_trace" if condition=="loop" else "vllm_mixed_user_network_wait_trace"),paths[name],"180","--trace-output",root+"/"+name+".gpu.jsonl","--trace-requests","105"]
    err=open(root+"/"+name+".native.stderr","w");log=open(root+"/"+name+".native.stdout","w")
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=err,text=True);lines=[]
    while True:
        line=p.stdout.readline();lines.append(line);log.write(line);log.flush()
        if condition=="loop" and line.startswith("NET_READY "):native_pid=int(re.search(r"pid=(\d+)",line).group(1));break
        if condition=="native" and line.startswith("resident Qwen ready" if backend=="hf" else "resident vLLM ready"):native_pid=p.pid;break
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
        row.update({"reply_hex":(prefix+data).hex(),"checked_tokens":count,"partial":partial,"exact":False})
        allowed=reference_pool[tuple(ref["prompt"]),ref["gen"]]
        row["finite_reference_set_match"]=any(actual==sequence[:count] for sequence in allowed)
        assert all(0<=token<vocab for token in actual)
    assert condition=="loop" and banks==8
    import collections,select
    def bucket(port):
        word=int.from_bytes(socket.inet_aton("127.0.0.1"),"little") ^ ((socket.htons(port)<<16)|socket.htons(port))
        word^=word>>16;word=word*0x7feb352d&0xffffffff;word^=word>>15
        word=word*0x846ca68b&0xffffffff;word^=word>>16
        return word&4095
    pairs={};chosen=None
    for port in range(32000,61000):
        b=bucket(port)
        if b in pairs:
            ca=socket.socket();cp=socket.socket()
            try:
                for c,pn in [(ca,pairs[b]),(cp,port)]:
                    c.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);c.settimeout(15);c.bind(("127.0.0.1",pn))
                chosen=(ca,cp,pairs[b],port,b);break
            except OSError:ca.close();cp.close()
        else:pairs[b]=port
    assert chosen
    ce,cp,ep,pp,b=chosen;clients.extend([ce,cp]);ce.connect(("127.0.0.1",39403));cp.connect(("127.0.0.1",39403))
    while True:
        co=socket.socket();co.settimeout(15);co.bind(("127.0.0.1",0))
        if bucket(co.getsockname()[1])!=b:break
        co.close()
    co.connect(("127.0.0.1",39403));clients.append(co)
    er,ef=request(ce,0,http=False)
    pending=[request(cp,7,http=False) for _ in range(48)]
    unrelated=[request(co,7,http=False) for _ in range(48)]
    for c in [ce,cp,co]:c.shutdown(socket.SHUT_WR)
    def snapshot(port):
        z=subprocess.run([base+"/reclaim_read_peer","127.0.0.1",str(port)],capture_output=True,text=True)
        assert z.returncode==0,(z.stdout,z.stderr);return json.loads(z.stdout)
    deadline=time.monotonic()+15
    while True:
        ready=snapshot(ep)
        if ready["head"]+ready["queued"]==97:break
        assert time.monotonic()<deadline,ready
        time.sleep(.01)
    read(ce,er,ef)
    first=snapshot(ep);result["collision_pending"]=first
    assert first["bucket"]==b and first["pending"]>0 and first["queued"]>0,first
    # A colliding peer's reference defers close; it cannot make it early.
    assert not select.select([ce],[],[],0)[0],"premature EOF while colliding pending"
    for row,ref in pending:read(cp,row,ref)
    second=snapshot(ep);result["collision_drained"]=second
    assert second["pending"]==0 and second["queued"]>0,second
    # Unrelated backlog remains, but this EOF is now safe to recycle.
    assert ce.recv(1)==b"";ce.close()
    assert cp.recv(1)==b"";cp.close()
    reused=socket.socket();reused.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1);reused.settimeout(15)
    reused.bind(("127.0.0.1",ep));reused.connect(("127.0.0.1",39403));clients.append(reused)
    reuse=[request(reused,0,http=False) for _ in range(8)]
    reused.shutdown(socket.SHUT_WR)
    for row,ref in unrelated:read(co,row,ref)
    assert co.recv(1)==b"";co.close()
    for row,ref in reuse:read(reused,row,ref)
    assert reused.recv(1)==b"";reused.close()
    last=snapshot(ep);result["final_peer"]=last
    assert last["pending"]==last["queued"]==0,last
    result["ports"]={"early":ep,"colliding":pp,"bucket":b,"same_peer_reused":True}
    os.kill(native_pid,signal.SIGTERM)
    tail,_=p.communicate(timeout=30);log.write(tail);log.close();err.close()
    result.update({"cmd":cmd,"exit":p.returncode,"stdout":"".join(lines)+tail,"stderr":open(root+"/"+name+".native.stderr").read(),"rows":rows})
    from pathlib import Path
    trace=Path(root+"/"+name+".gpu.jsonl")
    refs=[json.loads(line) for line in Path(str(trace)+".references.jsonl").read_text().splitlines()]
    assert len(refs)==len(rows)==105 and len({x["client_ns"] for x in refs})==105
    assert '"event": "vllm_reference_replay"' in result["stdout"] and '"event": "fresh_metadata_verified"' in result["stdout"]
    by_stamp={x["client_ns"]:x for x in refs}
    for row in rows:
        model=by_stamp[row["client_ns"]]
        got=list(struct.unpack("<"+"I"*row["checked_tokens"],bytes.fromhex(row["reply_hex"])))
        assert model["prompt"]==row["prompt"] and model["gen"]==row["gen"] and got==model["tokens"],(row,model)
        row["exact"]=True;row["oracle"]="same trajectory independently dual-replayed"
    result["finite_reference_disagreements"]=sum(not x["finite_reference_set_match"] for x in rows)
    st=next(json.loads(x[7:]) for x in result["stdout"].splitlines() if x.startswith("RESULT "));result["native_stats"]=st
    result["pass"]=bool(p.returncode==0 and len(rows)==105 and all(x.get("exact") for x in rows) and st["accepted"]==st["closed"]==4 and st["head"]==st["completed"]==105 and st["pending"]==st["error"]==st["reserved"]==st["dropped"]==st["overflow"]==0 and st["sqhead"]==st["sqtail"] and st["cqhead"]==st["cqtail"] and "graph_error=0" in result["stdout"])
except Exception as e:
    result["error"]=repr(e);result["pass"]=False
    view=subprocess.run([base+"/reclaim_local"+str(banks)+"/bpfusion_load","stats"],capture_output=True,text=True)
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
