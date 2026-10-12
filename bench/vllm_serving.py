#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Real vLLM graph TCP correctness and matched serving-policy comparison."""
import argparse,ctypes,json,math,os,re,signal,socket,statistics,struct,subprocess,sys,threading,time,traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from resident_dispatch import connect,request
from transformers import AutoConfig,AutoTokenizer

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model",required=True);ap.add_argument("--output",required=True)
    ap.add_argument("--correctness",action="store_true")
    comparisons=ap.add_mutually_exclusive_group()
    comparisons.add_argument("--packing-comparison",action="store_true")
    comparisons.add_argument("--release-comparison",action="store_true")
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1];os.chdir(root)
    output=Path(args.output).resolve();output.parent.mkdir(parents=True,exist_ok=True)
    assert not output.exists(),output
    raw=output.open("w",buffering=1);lock=threading.Lock()
    def emit(event,**kw):
        with lock:raw.write(json.dumps(dict(event=event,utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),**kw))+"\n")
    tok=AutoTokenizer.from_pretrained(args.model);config=AutoConfig.from_pretrained(args.model)
    prompts=[tok(text).input_ids for text in ("The capital of France is","What is 2 plus 2?","Write a short greeting.","Linux is")]
    modes=("serial-kernel","prefix-kernel","serial-userspace","prefix-userspace") if args.release_comparison else (("packed-kernel","packed-userspace") if args.correctness and args.packing_comparison else (
        ("grouped-kernel","packed-kernel","grouped-userspace","packed-userspace") if args.packing_comparison else ("kernel","userspace")))
    matrix=((1,1),(64,1),(1,8),(64,8));repetitions=1 if args.correctness else 5
    emit("metadata",model=args.model,vocab=config.vocab_size,prompts=prompts,precision="fp16",
         modes=modes,matrix=matrix,repetitions=repetitions,requests_per_cell=64,warmups_per_executor=8,
         correctness=args.correctness,comparison="release" if args.release_comparison else ("packing" if args.packing_comparison else "transport"),trace_condition="both transports identically BF_TRACE",
         commit=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip(),
         driver_source=Path(__file__).read_text(),client_source=(root/"bench/resident_dispatch.py").read_text(),
         backend_source=(root/"executor/vllm_graph.py").read_text(),native_source=(root/"executor/vllm_graph.cu").read_text(),
         python=sys.version,torch=subprocess.check_output(["python3","-c","import torch;print(torch.__version__)"],text=True).strip())
    frozen={}
    if args.packing_comparison or args.release_comparison:
        for previous in (root/"bench/results/vllm_server_20261012").glob("*_correctness.jsonl"):
            previous_meta=next(json.loads(line) for line in previous.open() if json.loads(line)["event"]=="metadata")
            if previous_meta["model"]!=args.model:continue
            reference=previous.with_name(previous.stem+"_p0_kernel.gpu.jsonl.references.jsonl")
            first=[json.loads(line) for line in reference.open()][:10]
            frozen={tuple(row["prompt"]):row["tokens"] for row in first}
            emit("frozen_unpadded_reference",path=str(reference),references=first)
    exit_code=1
    try:
        for pair in range(repetitions):
            order=modes if len(modes)==2 or (pair//2)%2==0 else modes[2:]+modes[:2]
            for mode in (order if pair%2==0 else order[::-1]):
                kernel_mode=mode.endswith("kernel")
                assert not Path("/sys/module/bfusion_tx").exists()
                assert not Path("/sys/fs/bpf/bpfusion_ctl").exists()
                p=None;attached=False;rows=[];success=False
                prefix=output.with_suffix("").with_name(output.stem+f"_p{pair}_{mode}")
                trace=Path(str(prefix)+".gpu.jsonl");logpath=Path(str(prefix)+".stdout.txt")
                nettrace=Path(str(prefix)+".network.txt")
                budget=(3*10+sum(range(1,9))+8*32*2+8*4+6+4+2) if args.correctness else 264
                binary=(("vllm_graph" if mode.startswith("prefix") else "vllm_graph_padded") if args.release_comparison
                        else ("vllm_graph_padded" if mode.startswith("packed") else "vllm_graph_grouped") if args.packing_comparison
                        else "vllm_graph")+("" if kernel_mode else "_user_network_wait")+"_trace"
                command=["./build/"+binary,
                    args.model,"300","--trace-output",str(trace),"--trace-requests",str(budget)]
                if args.correctness:command=["strace","-D","-f","-e","trace=network,write","-o",str(nettrace),*command]
                try:
                    if kernel_mode:
                        r=subprocess.run(["./build/bpfusion_load","stream-attach"],capture_output=True,text=True)
                        emit("attach",pair=pair,mode=mode,code=r.returncode,stdout=r.stdout,stderr=r.stderr)
                        assert r.returncode==0;attached=True
                    with logpath.open("w") as log:p=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                    emit("start",pair=pair,mode=mode,pid=p.pid,command=command,trace=str(trace))
                    print(f"START pair={pair} mode={mode} pid={p.pid}",flush=True)
                    while "resident vLLM ready" not in logpath.read_text():
                        if p.poll() is not None:raise RuntimeError(logpath.read_text()[-6000:])
                        time.sleep(.1)
                    emit("ready",pair=pair,mode=mode,pid=p.pid)
                    def keep(row,kind):
                        row=dict(row,kind=kind);rows.append(row)
                        emit("request",pair=pair,mode=mode,**row)
                        return row
                    def wire(ids,gen,http=True):
                        marker=time.monotonic_ns()
                        payload=struct.pack("<IIIIQ",0x514c4d51,len(ids),gen,0,marker)+struct.pack(f"<{len(ids)}I",*ids)
                        body=(f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(payload)}\r\n\r\n".encode()+payload) if http else payload
                        return marker,body
                    def receive(client,ids,gen,marker,http=True,bad=False):
                        head=b""
                        if http:
                            while not head.endswith(b"\r\n\r\n"):
                                chunk=client.recv(1);assert chunk,"short HTTP header";head+=chunk
                            status=b"400 Bad Request" if bad else b"200 OK"
                            assert head.startswith(b"HTTP/1.1 "+status+b"\r\n"),head
                            count=0 if bad else gen*4
                            assert f"Content-Length: {count}\r\n".encode() in head,head
                        elif bad:
                            assert client.recv(1)==b"","binary rejection must close"
                            count=0
                        else:count=gen*4
                        data=b""
                        while len(data)<count:
                            chunk=client.recv(count-len(data));assert chunk,"short body";data+=chunk
                        tokens=list(struct.unpack(f"<{count//4}I",data))
                        return dict(client_ns=marker,input_ids=ids,gen=gen,bad=bad,tokens=tokens,http=http)
                    def exchange(ids,gen,kind,http=True,split=False,bad=False,client=None):
                        own=client is None
                        if own:client=connect()
                        try:
                            marker,data=wire(ids,gen,http)
                            if split:
                                for byte in data:client.sendall(bytes([byte]));time.sleep(.001)
                            else:client.sendall(data)
                            return keep(receive(client,ids,gen,marker,http,bad),kind)
                        finally:
                            if own:client.close()
                    if args.correctness:
                        for _ in range(5000):connect().close()
                        emit("empty_connections",pair=pair,mode=mode,count=5000)
                        cases=prompts+[(prompts[0]*math.ceil(n/len(prompts[0])))[:n] for n in (1,15,16,17,32,64)]
                        for repeat in range(3):
                            for ids in cases:exchange(ids,64,"fragmented",http=repeat==1,split=True)
                        def concurrent(count,iterations,kind,mixed=False,reject=False):
                            barrier=threading.Barrier(count)
                            def lane(i):
                                with connect() as client:
                                    barrier.wait(timeout=60)
                                    for repeat in range(iterations):
                                        ids=cases[(i+repeat)%len(cases)]
                                        gen=1 if mixed and (i+repeat)%2 else 64
                                        if reject:
                                            invalid=ids.copy();invalid[0]=config.vocab_size
                                            exchange(invalid,gen,kind+"_reject",bad=True,client=client)
                                        exchange(ids,gen,kind,client=client)
                            with ThreadPoolExecutor(max_workers=count) as pool:
                                futures=[pool.submit(lane,i) for i in range(count)]
                                for future in futures:future.result()
                        # Every client concurrency count is exercised; report actual GPU batches.
                        for count in range(1,9):concurrent(count,1,"concurrency_"+str(count))
                        concurrent(8,32,"wrap",reject=True)
                        concurrent(8,4,"mixed",mixed=True)
                        with connect() as client:
                            sent=[]
                            for i in range(6):
                                ids=cases[i%len(cases)];marker,data=wire(ids,64);client.sendall(data);sent.append((ids,marker))
                            client.shutdown(socket.SHUT_WR)
                            for ids,marker in sent:keep(receive(client,ids,64,marker),"pipeline_halfclose")
                        bad_last=prompts[0].copy();bad_last[-1]=config.vocab_size
                        bad_first=prompts[0].copy();bad_first[0]=0xffffffff
                        with connect() as client:
                            sent=[]
                            for ids,bad in ((bad_last,True),(prompts[0],False),(bad_first,True),(prompts[0],False)):
                                marker,data=wire(ids,64);client.sendall(data);sent.append((ids,marker,bad))
                            for ids,marker,bad in sent:keep(receive(client,ids,64,marker,bad=bad),"pipeline_reject")
                        exchange(bad_first,64,"binary_reject",http=False,bad=True)
                        exchange(prompts[0],64,"after_reject",http=False)
                    else:
                        with connect() as client:
                            for i in range(8):
                                ids=prompts[i%len(prompts)]
                                keep(dict(request(client,ids,None,gen=1),input_ids=ids,gen=1,bad=False),"warmup")
                        for gen,concurrency in matrix:
                            barrier=threading.Barrier(concurrency+1);ready=threading.Barrier(concurrency+1)
                            selected=[]
                            def lane(i):
                                with connect() as client:
                                    ready.wait(timeout=60);barrier.wait(timeout=60)
                                    for index in range(i,64,concurrency):
                                        ids=prompts[index%len(prompts)]
                                        row=dict(request(client,ids,None,gen=gen),input_ids=ids,gen=gen,bad=False,index=index,concurrency=concurrency)
                                        selected.append(row)
                            with ThreadPoolExecutor(max_workers=concurrency) as pool:
                                futures=[pool.submit(lane,i) for i in range(concurrency)]
                                ready.wait(timeout=60);barrier.wait(timeout=60)
                                for future in futures:future.result()
                            first=min(row["start_ns"] for row in selected);last=max(row["arrival_ns"][-1] for row in selected)
                            for row in selected:keep(row,"measured")
                            emit("cell",pair=pair,mode=mode,gen=gen,concurrency=concurrency,
                                requests=64,tokens=64*gen,first_ns=first,last_ns=last,output_tokens_per_s=64*gen/((last-first)/1e9))
                    if args.correctness:
                        tids=[int(t.name) for t in Path(f"/proc/{p.pid}/task").iterdir() if int(t.name)!=p.pid]
                        assert tids
                        ret=ctypes.CDLL(None).tgkill(p.pid,tids[0],signal.SIGTERM);assert ret==0
                        emit("helper_signal",pair=pair,mode=mode,pid=p.pid,tid=tids[0])
                    else:p.terminate()
                    code=p.wait();log=logpath.read_text()
                    emit("executor",pair=pair,mode=mode,exit_code=code,stdout=log)
                    assert code==0 and "graph_error=0" in log and "launches=1 " in log,log[-6000:]
                    refs=[json.loads(line) for line in Path(str(trace)+".references.jsonl").open()]
                    assert len(rows)==len(refs),(len(rows),len(refs))
                    by_marker={row["client_ns"]:row for row in refs};assert len(by_marker)==len(refs)
                    checked=0
                    for row in rows:
                        ref=by_marker.pop(row["client_ns"])
                        assert ref["prompt"]==row["input_ids"] and ref["gen"]==row["gen"] and bool(ref["bad"])==row["bad"],(row,ref)
                        assert ref["tokens"]==row["tokens"],(row,ref)
                        checked+=len(row["tokens"])
                    assert not by_marker
                    if frozen:
                        known=[row for row in rows if not row["bad"] and tuple(row["input_ids"]) in frozen]
                        emit("unpadded_fidelity_diagnostic",pair=pair,mode=mode,sequences=len(known),
                            equal_sequences=sum(row["tokens"]==frozen[tuple(row["input_ids"])][:row["gen"]] for row in known),
                            first_token_equal=sum(row["tokens"][0]==frozen[tuple(row["input_ids"])][0] for row in known))
                    events=[json.loads(line) for line in trace.open()]
                    assert events[-1]["overflows"]==0
                    if args.release_comparison:
                        releases=[e for e in events if e["event"]=="release"]
                        assert sum(e["batch"] for e in releases)==len(rows)
                        actual_max=max(e["batch"] for e in releases)
                        assert actual_max==1 if mode.startswith("serial") else actual_max>1
                        emit("release_verified",pair=pair,mode=mode,rounds=len(releases),max_prefix=actual_max)
                    batches=sorted({e["batch"] for e in events if e["event"]=="compute"})
                    queries=sorted({e["query"] for e in events if e["event"]=="compute"})
                    emit("verified",pair=pair,mode=mode,requests=len(rows),tokens=checked,
                        rejections=sum(row["bad"] for row in rows),actual_batches=batches,actual_queries=queries,reference_path=str(trace)+".references.jsonl")
                    if args.correctness:
                        network=nettrace.read_text();assert "resident vLLM ready" in network
                        active=network.split("resident vLLM ready",1)[1]
                        calls=r"\b(?:accept4?|recvfrom|recvmsg|recvmmsg|sendto|sendmsg|sendmmsg)\("
                        if kernel_mode:assert not re.search(calls,active),active
                        else:
                            for call in ("accept4","recvfrom","sendmsg"):assert re.search(r"\b"+call+r"\(",active),call
                        emit("network_verified",pair=pair,mode=mode,trace_path=str(nettrace))
                    if kernel_mode:
                        r=subprocess.run(["./build/bpfusion_load","stats"],capture_output=True,text=True)
                        emit("stats",pair=pair,mode=mode,code=r.returncode,stdout=r.stdout,stderr=r.stderr);assert r.returncode==0
                    assert not Path("/sys/module/bfusion_tx").exists()
                    print(f"PASS pair={pair} mode={mode} requests={len(rows)} tokens={checked} batches={batches}",flush=True)
                    success=True
                finally:
                    if p is not None and p.poll() is None:p.terminate();emit("cleanup_executor",pair=pair,mode=mode,exit_code=p.wait())
                    if attached:
                        r=subprocess.run(["./build/bpfusion_load","stream-detach"],capture_output=True,text=True)
                        emit("detach",pair=pair,mode=mode,code=r.returncode,stdout=r.stdout,stderr=r.stderr)
                        for name in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):Path("/sys/fs/bpf",name).unlink(missing_ok=True)
                    emit("executor_terminal",pair=pair,mode=mode,success=success)
        exit_code=0
    except BaseException as exc:
        emit("failure",kind=type(exc).__name__,message=str(exc),traceback=traceback.format_exc());traceback.print_exc()
    finally:emit("terminal",exit_code=exit_code);raw.close()
    sys.exit(exit_code)
if __name__=="__main__":main()
