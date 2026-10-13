import datetime,json,os,re,struct
root=os.path.dirname(os.path.abspath(__file__))
oracle=json.load(open(root+"/model/oracle.json"))
report={"time":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Root self-review of finite streaming integration, not performance or independent review.","models":[]}
for name in ("qwen","smol"):
    r=json.load(open(root+"/model/"+name+".results.json"));s=r["native_stats"];ref=oracle["models"][name]
    assert r["pass"] and r["exit"]==0 and r["clean_eof"] and not r["remaining_pins"]
    assert r["oracle_frozen_at"]==oracle["frozen_at"] and r["started"]>oracle["frozen_at"]
    assert s["status"]==s["dropped"]==s["overflow"]==s["reserved"]==0
    assert s["accepted"]==s["closed"]==s["eof"]==1 and s["received"]==s["head"]==12
    assert s["sq_head"]==s["sq_tail"]==s["cq_head"]==s["cq_tail"]==s["sent"]+16
    tokens=wirebytes=longs=early=finals=0;client_chunks=[]
    for row,expected,device in zip(r["rows"],ref["rows"],r["stream_records"]):
        i=row["cycle"];raw=bytes.fromhex(row["request_hex"]);body=raw
        if i%2:
            hdr,body=raw.split(b"\r\n\r\n",1);assert b"Content-Length: "+str(len(body)).encode() in hdr
        magic,np,ng,pad,stamp=struct.unpack("<IIIIQ",body[:24])
        ids=list(struct.unpack("<"+"I"*np,body[24:]));assert ids==expected["prompt"]==row["prompt"]
        assert magic==0x514c4d51 and pad==0 and stamp==1000+i and ng==expected["gen"]==row["gen"]
        prefix=(b"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: "+str(ng*4).encode()+b"\r\n\r\n" if i%2 else b"")
        expected_wire=prefix+struct.pack("<"+"I"*ng,*expected["tokens"])
        assert bytes.fromhex(row["reply_hex"])==expected_wire
        assert sum(c["bytes"] for c in row["chunks"])==ng*4
        assert [c["arrived_ns"] for c in row["chunks"]]==sorted(c["arrived_ns"] for c in row["chunks"])
        assert device["sequence"]==i and device["gen"]==ng and device["last_produced"]==ng
        assert device["bytes"]==len(expected_wire) and device["sends"]==device["early"]+device["finals"]
        assert device["finals"]>=1 and device["first_produced"]<=ng
        if ng==64:
            assert device["early"]>0
            longs+=1;client_chunks.append({"sequence":i,"chunks":len(row["chunks"]),
                "first_before_last":row["chunks"][0]["arrived_ns"]<row["chunks"][-1]["arrived_ns"]})
        tokens+=ng;wirebytes+=len(expected_wire);early+=device["early"];finals+=device["finals"]
    assert len(r["rows"])==len(r["stream_records"])==12 and tokens==390 and longs==6
    assert wirebytes==s["bytes"]==2036 and sum(x["sends"] for x in r["stream_records"])==s["sent"]
    bpf=r["bpf_stats"]["stdout"]
    for label,value in [("published",12),("stream publish",12),("sockhash linked",1),("sockhash failed",0),("llm busy",0),("parser invalid",0)]:
        assert re.search(r"^"+re.escape(label)+r"\s+"+str(value)+r"$",bpf,re.M)
    assert "llm_reserved=0x0" in bpf and len(re.findall(r"^llm\[\d\]: state=0 ",bpf,re.M))==8
    assert "launches=1 device_graph_launches=390 graph_error=0 banks=8 max_active=1" in r["stdout"]
    lines=open(root+"/model/"+name+".strace").read().splitlines()
    markers=[float(m.group(1)) for l in lines if "SIGTERM" in l and (m:=re.match(str(r["native_pid"])+r"\s+([\d.]+)\s+",l))]
    assert len(markers)==1
    start=r["ready_time_ns"]/1e9;end=markers[0]
    serving=[l for l in lines if (m:=re.match(r"\d+\s+([\d.]+)\s+",l)) and start<=float(m.group(1))<=end]
    calls={n:sum(bool(re.search(r"\b"+n+r"\(",l)) for l in serving) for n in
           ("accept","accept4","recvfrom","recvmsg","sendto","sendmsg","io_uring_enter")}
    assert all(v==0 for v in calls.values()),calls
    assert sum("io_uring_setup(" in l for l in lines)==sum("io_uring_enter(" in l for l in lines)==1
    report["models"].append({"name":name,"requests":12,"exact_tokens":tokens,"exact_wire_bytes":wirebytes,
        "gen64_requests":longs,"successful_sends_from_pre_DONE_observation":early,"final_send_completions":finals,
        "sends":s["sent"],"queue_positions":s["sq_tail"],"reservation_zero":True,"all_slots_free":True,
        "client_long_output_chunks":client_chunks,"after_ready_syscalls":calls,
        "start":r["started"],"end":r["finished"]})
report["oracle_frozen_at"]=oracle["frozen_at"]
report["limitations"]=["finite tags/one connection; no concurrency/backpressure/abort qualification",
 "no timing/CPU benefit comparison; synthetic cold/fragmented workload and strace",
 "only the existing HF backend, not optimized vLLM integration"]
if not os.path.exists(root+"/review.json"):open(root+"/review.json","w").write(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
