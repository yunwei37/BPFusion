import datetime,json,os,re,subprocess
root=os.path.dirname(os.path.abspath(__file__))
expected=lambda cycles:bytes((frame*17+i)%251 for frame in range(cycles*32) for i in range(128))
review={"time":datetime.datetime.now(datetime.timezone.utc).isoformat(),"cases":[]}
for directory in ("initial","","receive_wake"):
    path=os.path.join(root,directory)
    for result in json.load(open(path+"/results.json")):
        mode=result["mode"];s=result["stats"];data=bytes.fromhex(result["client_hex"])
        trace=open(path+"/"+mode+".strace").read()
        calls={name:len(re.findall(r"\b"+name+r"\(",trace)) for name in
               ("accept","accept4","recvfrom","recvmsg","sendto","sendmsg","io_uring_setup","io_uring_enter","shutdown")}
        assert calls["accept"]==1 and calls["io_uring_setup"]==1
        assert sum(calls[k] for k in ("accept4","recvfrom","recvmsg","sendto","sendmsg"))==0
        has_bootstrap=directory!="initial"
        expected_enters=int(has_bootstrap)+(mode=="idle-wake")
        assert calls["io_uring_enter"]==expected_enters,(directory,mode,calls)
        if directory=="initial" and mode=="hot" or mode=="idle":
            assert data==b"" and s["status"]==1 and s["completed"]==0 and s["flags_before"]&1 and s["flags_after"]&1
            outcome="idle GPU submission did not complete; client received zero bytes"
        else:
            assert data==expected(1) and s["status"]==0 and s["bytes"]==4096
            assert s["submitted"]==s["completed"]==32
            assert s["sq_head"]==s["sq_tail"] and s["cq_head"]==s["cq_tail"]
            outcome="exact 4096 client bytes; all GPU send completions consumed"
        assert result["exit"]==0 and result["client_error"] is None and "CLEANUP " in result["stdout"]
        assert s["dropped"]==s["overflow"]==0
        review["cases"].append({"directory":directory,"mode":mode,"outcome":outcome,
                                "client_bytes":len(data),"syscalls":calls,"wrapper_expected_outcome":result["expected_outcome"]})
r=json.load(open(root+"/receive_cycles/results.json"));s=r["stats"]
expected_data=bytes((frame*17+i+77+cycle)%251 for cycle in range(8)
                    for frame in range(cycle*32,(cycle+1)*32) for i in range(128))
assert bytes.fromhex(r["client_hex"])==expected_data and r["client_bytes"]==32768 and r["pass"]
assert s["status"]==0 and s["submitted"]==s["completed"]==256 and s["bytes"]==32768
assert s["sq_head"]==s["sq_tail"]==s["cq_head"]==s["cq_tail"]==266
assert s["cpu_wakes"]==s["dropped"]==s["overflow"]==0
assert "idle_observed=8 gpu_recv_armed=8 eof=1" in r["stdout"]
assert len(r["cycles"])==8 and all(c["exact"] for c in r["cycles"])
trace=open(root+"/receive_cycles/cycles.strace").read()
calls={name:len(re.findall(r"\b"+name+r"\(",trace)) for name in
       ("accept","accept4","recvfrom","recvmsg","sendto","sendmsg","io_uring_setup","io_uring_enter","shutdown")}
assert calls["accept"]==calls["io_uring_setup"]==calls["io_uring_enter"]==calls["shutdown"]==1
assert sum(calls[k] for k in ("accept4","recvfrom","recvmsg","sendto","sendmsg"))==0
review["cycles"]={"exact_bytes":32768,"tx_completions":256,"receive_requests":8,"idle_flag_observations":8,
                  "eof":True,"syscalls":calls,"all_queue_positions":266}
review["scope"]="Component diagnosis, one bootstrapped loopback TCP connection; no eBPF, HTTP, inference or performance claim. Root self-review, not an independent agent review."
if not os.path.exists(root+"/review.json"):
    open(root+"/review.json","w").write(json.dumps(review,indent=2))
print(json.dumps(review,indent=2))
