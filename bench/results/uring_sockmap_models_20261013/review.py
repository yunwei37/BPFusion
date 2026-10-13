import datetime,difflib,json,os,re,struct
root=os.path.dirname(os.path.abspath(__file__))
report={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Root self-review of finite single-connection integration; no independent review or performance inference.","cases":[]}
oracle=json.load(open(root+"/model/oracle.json"))
for name,path,reference in [("echo",root+"/results.json",None),
                            ("qwen",root+"/model/qwen.results.json",oracle["models"]["qwen"]),
                            ("smol",root+"/model/smol.results.json",oracle["models"]["smol"])]:
    r=json.load(open(path));s=r["native_stats"]
    assert r["pass"] and r["exit"]==0 and r["clean_eof"] and not r["remaining_pins"]
    assert s["status"]==0 and s["accepted"]==s["closed"]==s["eof"]==1
    assert s["received"]==s["sent"]==s["head"]==12
    assert s["sq_head"]==s["sq_tail"]==s["cq_head"]==s["cq_tail"]==28
    assert s["idle_observed"]==9 and s["reserved"]==s["dropped"]==s["overflow"]==0
    assert "host_native_atomic=0" in r["stdout"] and "CLEANUP " in r["stdout"]
    total=0
    for row in r["rows"]:
        i=row["cycle"];request=bytes.fromhex(row["request_hex"]);response=bytes.fromhex(row["reply_hex"])
        body=request
        if row["protocol"]=="http":
            header,body=request.split(b"\r\n\r\n",1)
            assert b"Content-Length: "+str(len(body)).encode() in header
        magic,np,ng,pad,client_ns=struct.unpack("<IIIIQ",body[:24])
        ids=list(struct.unpack("<"+"I"*np,body[24:]))
        assert magic==0x514c4d51 and ng==1 and pad==0 and client_ns==1000+i and ids==row["prompt"]
        token=ids[-1]+1
        if reference:
            expected_row=reference["rows"][i];assert expected_row["prompt"]==ids and expected_row["gen"]==1
            token=expected_row["tokens"][0]
        prefix=(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: 4\r\n\r\n" if i%2 else b"")
        assert response==prefix+struct.pack("<I",token)
        total+=len(response)
    assert len(r["rows"])==12 and total==s["bytes"]==516
    bpf=r["bpf_stats"]["stdout"]
    for label,value in [("published",12),("stream publish",12),("sockhash linked",1),
                        ("sockhash failed",0),("llm busy",0),("parser invalid",0)]:
        assert re.search(r"^"+re.escape(label)+r"\s+"+str(value)+r"$",bpf,re.M),(label,bpf)
    assert "llm_reserved=0x0" in bpf and len(re.findall(r"^llm\[\d\]: state=0 ",bpf,re.M))==8
    trace_path=root+"/native.strace" if name=="echo" else root+"/model/"+name+".strace"
    trace=open(trace_path).read().splitlines()
    start=r["ready_time_ns"]/1e9
    if name=="echo":end=float("inf")
    else:
        marker=[float(m.group(1)) for l in trace if "SIGTERM" in l
                and (m:=re.match(str(r["native_pid"])+r"\s+([\d.]+)\s+",l))]
        assert len(marker)==1,marker
        end=marker[0];assert end>start
        assert "launches=1 device_graph_launches=12 graph_error=0 banks=8 max_active=1" in r["stdout"]
        assert r["oracle_frozen_at"]==oracle["frozen_at"] and r["started"]>oracle["frozen_at"]
    serving=[l for l in trace if (m:=re.match(r"\d+\s+([\d.]+)\s+",l)) and start<=float(m.group(1))<=end]
    calls={n:sum(bool(re.search(r"\b"+n+r"\(",l)) for l in serving) for n in
           ["accept","accept4","recvfrom","recvmsg","sendto","sendmsg","io_uring_enter"]}
    assert all(v==0 for v in calls.values()),(name,calls)
    setup_count=sum("io_uring_setup(" in l for l in trace)
    wake_count=sum("io_uring_enter(" in l for l in trace)
    assert setup_count==wake_count==1,(name,setup_count,wake_count)
    report["cases"].append({"name":name,"requests":12,"exact_client_bytes":total,
        "model_tokens":12 if reference else 0,"all_queue_positions":28,
        "post_ready_network_and_wake_calls":calls,"bootstrap_setup":1,"bootstrap_wake":1,
        "idle_flag_observations":9,"all_slots_free":True,"reservation_zero":True,"eof_and_gpu_close":True})
header=open(root+"/model/uring_network.h").read()
assert "atomicAnd_system" not in header and "atomicCAS" not in header
identity=json.load(open(root+"/model/source_identity.json"))
assert identity["device_model_dispatch_identical"] and identity["bpf_core_identical"]
report["source_identity"]=identity
report["limitations"]=["finite 12-request tags and one connection per native process",
 "gen1 only; no concurrent requests, streaming long generation or rejection/disconnect qualification",
 "no latency/throughput/CPU cost measurement; fixture idle/fragmentation and tracing",
 "global tracepoint with fixture-specific tags is not a production ring ownership design"]
if not os.path.exists(root+"/review.json"):
    open(root+"/review.json","w").write(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
