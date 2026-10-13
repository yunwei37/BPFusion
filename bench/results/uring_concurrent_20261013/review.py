import datetime,json,os,re,struct
root=os.path.dirname(os.path.abspath(__file__))
oracle=json.load(open(root+"/model/oracle.json"))
report={"observed_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Root self-review; functional qualification, not independent paper review/performance evidence.","runs":[]}
cases=[("preflight","qwen","model/qwen.preflight_retry.results.json"),
       ("mixed","qwen","model/qwen.concurrent.results.json"),("mixed","smol","model/smol.concurrent.results.json"),
       ("long","qwen","model/alllong/qwen.alllong.results.json"),("long","smol","model/alllong/smol.alllong.results.json"),
       ("lifecycle","qwen","model/lifecycle/qwen.results.json"),("lifecycle","smol","model/lifecycle/smol.results.json"),
       ("production","qwen","production/qwen.results.json"),("production","smol","production/smol.results.json")]
full_tokens=partial_tokens=0
for kind,name,file in cases:
    r=json.load(open(root+"/"+file));s=r["native_stats"];refs=oracle["models"][name]["rows"]
    assert r["pass"] and r["exit"]==0 and not r["remaining_pins"]
    assert s["error"]==s["pending"]==s["reserved"]==s["dropped"]==s["overflow"]==s["trace_overflow"]==0
    assert s["accepted"]==s["closed"] and s["completed"]==s["head"]==len(r["rows"])==len(r["replies"])
    assert s["sqhead"]==s["sqtail"]==s["cqhead"]==s["cqtail"]
    assert r["start"]>oracle["frozen_at"] and r["oracle_frozen_at"]==oracle["frozen_at"]
    bystamp={x["client_ns"]:x for x in r["replies"]};assert len(bystamp)==len(r["rows"])
    normal=partial=rejects=0;seen_seq=[]
    for row in r["rows"]:
        key=row["case"];ref=refs[key];request=bytes.fromhex(row["request_hex"])
        body=request.split(b"\r\n\r\n",1)[1] if row["protocol"]=="http" else request
        magic,np,ng,pad,stamp=struct.unpack("<IIIIQ",body[:24])
        ids=list(struct.unpack("<"+"I"*np,body[24:]))
        assert magic==0x514c4d51 and pad==0 and stamp==row["client_ns"] and ids==row["prompt"] and ng==row["gen"]
        reply=bystamp[stamp];assert reply["gen"]==ng
        seen_seq.append(reply["seq"])
        raw=bytes.fromhex(row["reply_hex"])
        data=raw
        if raw and row["protocol"]=="http":
            header,data=raw.split(b"\r\n\r\n",1)
            if row.get("invalid"):
                assert header.startswith(b"HTTP/1.1 400 Bad Request\r\n") and b"Content-Length: 0" in header and data==b""
            else:
                assert header.startswith(b"HTTP/1.1 200 OK\r\n") and b"Content-Length: "+str(ng*4).encode() in header
        if row.get("invalid"):
            rejects+=1
            if row["protocol"]=="binary":assert raw==b"" and reply["aborted"]==1
            else:assert reply["aborted"]==0 and reply["bytes"]==len(raw)
        else:
            assert ids==ref["prompt"] and ng==ref["gen"]
            expected=struct.pack("<"+"I"*ng,*ref["tokens"])
            if row.get("partial"):
                assert data==expected[:4] and reply["aborted"]==1
                extra=bytes.fromhex(row.get("post_stop_extra_hex",""))
                assert extra==expected[4:4+len(extra)]
                partial+=1
            else:
                assert data==expected and reply["aborted"]==0 and reply["bytes"]==len(raw)
                normal+=ng
                if kind in ("mixed","long","preflight"):
                    assert sum(c["bytes"] for c in row["chunks"])==ng*4
        assert reply["sends"]>=reply["early"]
    assert sorted(seen_seq)==list(range(len(r["rows"])))
    bpf=r["bpf_stats"]["stdout"]
    for label,value in [("stream publish",s["completed"]),("sockhash linked",s["accepted"]),("sockhash failed",0),("llm busy",0),("parser invalid",0)]:
        assert re.search(r"^"+re.escape(label)+r"\s+"+str(value)+r"$",bpf,re.M),(file,label)
    assert re.search(r"^(?:published|uring recycled)\s+"+str(s["completed"])+r"$",bpf,re.M)
    assert "llm_reserved=0x0" in bpf and len(re.findall(r"^llm\[\d\]: state=0 ",bpf,re.M))==8
    assert "graph_error=0 banks=8" in r["stdout"] and "ring_bound=1 capacity=4096 sq=8192 cq=16384" in r["stdout"]
    if kind in ("mixed","long"):
        assert s["max_connections"]==s["max_requests"]==8
        assert normal==(780 if kind=="mixed" else 1536)
    if kind in ("lifecycle","production"):assert rejects==2 and partial==2 and normal==130 and s["aborted"]==3
    if kind=="preflight":assert normal==66 and s["accepted"]==25
    trace=os.path.dirname(file)+"/"+os.path.basename(file).replace(".results.json",".strace")
    lines=open(root+"/"+trace).read().splitlines()
    start=r["ready_time_ns"]/1e9
    endmarks=[float(m.group(1)) for line in lines if "SIGTERM" in line and (m:=re.match(str(r["native_pid"])+r"\s+([\d.]+)\s+",line))]
    assert len(endmarks)==1
    serving=[l for l in lines if (m:=re.match(r"\d+\s+([\d.]+)\s+",l)) and start<=float(m.group(1))<=endmarks[0]]
    syscalls={n:sum(bool(re.search(r"\b"+n+r"\(",l)) for l in serving) for n in
              ("accept","accept4","recvfrom","recvmsg","sendto","sendmsg","io_uring_enter")}
    assert all(v==0 for v in syscalls.values()),(file,syscalls)
    assert sum("io_uring_setup(" in l for l in lines)==1 and sum("io_uring_enter(" in l for l in lines)==2
    report["runs"].append({"kind":kind,"model":name,"start":r["start"],"end":r["end"],"requests":len(r["rows"]),
        "complete_exact_tokens":normal,"checked_partial_prefix_tokens":partial,"intentional_rejections":rejects,
        "abandoned_or_stopped_requests":s["aborted"],"accepted_and_closed":s["accepted"],"wire_send_bytes":s["bytes"],
        "queue_positions":s["sqtail"],"max_connections":s["max_connections"],"max_requests":s["max_requests"],
        "native_after_ready_syscalls":syscalls})
    full_tokens+=normal;partial_tokens+=partial
assert json.load(open(root+"/initial_binding/model_qwen.preflight.results.json"))["pass"] is False
assert json.load(open(root+"/ring_control.json"))["control"]["exit"]==0
assert "foreign_did_not_recycle=1" in json.load(open(root+"/ring_control.json"))["control"]["stdout"]
assert json.load(open(root+"/default_mode_qualification.json"))["exit"]==0
assert not any(n.startswith("bpfusion_uring") for n in json.load(open(root+"/default_mode_qualification.json"))["pins"])
assert json.load(open(root+"/production_build.json"))["exit"]==0
report["complete_exact_tokens"]=full_tokens
report["checked_partial_prefix_tokens"]=partial_tokens
report["limitations"]=["three waves of <=8 outstanding requests; no overload/backpressure proof",
 "128-entry trace is diagnostic only; serving continues beyond it but long-run trace-overflow behavior untested",
 "no latency/throughput/CPU claim and no optimized-vLLM integration",
 "no induced partial-send or GPU/device-error qualification"]
if not os.path.exists(root+"/review.json"):open(root+"/review.json","w").write(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
