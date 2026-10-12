#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Matched token-ID BPFusion versus official vLLM benchmark."""
import argparse, http.client, json, math, os, secrets, signal, socket
import statistics, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path("/workspaces/repository")
TEMP=Path("/tmp/bpfusion-vllm-uapngodu")
MODEL="/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"
sys.path.insert(0,str(ROOT/"bench"))
from resident_dispatch import request as native_request, connect as native_connect, command, gpu_state
TICK=os.sysconf("SC_CLK_TCK")

def group_cpu(pgid):
    values={}
    for p in Path("/proc").glob("[0-9]*/stat"):
        try:
            a=p.read_text().rsplit(") ",1)[1].split()
            if int(a[2])==pgid: values[int(p.parent.name)]=(int(a[11])+int(a[12]))/TICK
        except (OSError,ValueError,IndexError): pass
    return values

def external_connect():
    c=http.client.HTTPConnection("127.0.0.1",39404,timeout=60)
    c.connect(); c.sock.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
    return c

def external_request(client,ids,expected,key):
    body=json.dumps({"token_ids":ids,"return_token_ids":True,"stream":True,
      "sampling_params":{"max_tokens":len(expected),"temperature":0.0,
                         "ignore_eos":True,"detokenize":False}},separators=(",",":")).encode()
    headers={"Content-Type":"application/json","Authorization":"Bearer "+key}
    start=time.monotonic_ns()
    client.request("POST","/inference/v1/generate",body,headers)
    response=client.getresponse()
    assert response.status==200,(response.status,response.read().decode())
    assert "text/event-stream" in response.getheader("Content-Type","")
    pending=b"";actual=[];arrivals=[];frames=[];done=False;prompt=None;finish=None
    while not done:
        data=response.read1(4096); arrived=time.monotonic_ns()
        assert data,"stream ended without DONE"
        pending+=data
        while b"\n\n" in pending:
            frame,pending=pending.split(b"\n\n",1)
            payload=b"\n".join(line[6:] for line in frame.splitlines() if line.startswith(b"data: "))
            if not payload: continue
            if payload==b"[DONE]": done=True;continue
            obj=json.loads(payload)
            if "prompt_token_ids" in obj: prompt=obj["prompt_token_ids"]
            for choice in obj["choices"]:
                assert choice["index"]==0,choice
                tokens=choice.get("token_ids") or []
                assert all(type(t)==int and 0<=t<151936 for t in tokens),tokens
                actual.extend(tokens);arrivals.extend([arrived]*len(tokens))
                if choice.get("finish_reason") is not None: finish=choice["finish_reason"]
            frames.append({"arrival_ns":arrived,"response":obj})
    tail=response.read(); assert not pending.strip() and not tail.strip(),(pending,tail)
    assert prompt==ids,(prompt,ids)
    assert len(actual)==len(expected),(actual,expected)
    assert finish=="length",finish
    return {"start_ns":start,"arrival_ns":arrivals,"tokens":actual,"exact_reference":actual==expected,
      "first_mismatch":next((i for i,(a,b) in enumerate(zip(actual,expected)) if a!=b),None),
      "ttft_ms":(arrivals[0]-start)/1e6,"latency_ms":(arrivals[-1]-start)/1e6,
      "tpot_ms":(arrivals[-1]-arrivals[0])/(len(expected)-1)/1e6 if len(expected)>1 else None,
      "frames":frames}

def one(client,mode,ids,expected,key):
    if mode=="vllm": return external_request(client,ids,expected,key)
    r=native_request(client,ids,expected);r.update(exact_reference=True,first_mismatch=None)
    return r

def connect(mode):
    return external_connect() if mode=="vllm" else native_connect()

def cell(pid,mode,cases,gen,concurrency,count,rows,key):
    ready=threading.Barrier(concurrency+1);start_barrier=threading.Barrier(concurrency+1)
    def worker(worker_id):
        c=connect(mode)
        try:
            ready.wait(timeout=60);start_barrier.wait(timeout=60)
            for i in range(worker_id,count,concurrency):
                idx=i%len(cases);ids,expected=cases[idx]
                r=one(c,mode,ids,expected[:gen],key);r.update(index=i,case=idx);rows.append(r)
        finally: c.close()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures=[pool.submit(worker,i) for i in range(concurrency)]
        ready.wait(timeout=60);before=group_cpu(pid);start=time.monotonic_ns()
        start_barrier.wait(timeout=60)
        for f in futures:f.result()
        finish=time.monotonic_ns();after=group_cpu(pid)
    assert before.keys()==after.keys(),("process tree changed",before,after)
    first=min(r["start_ns"] for r in rows);last=max(r["arrival_ns"][-1] for r in rows)
    return {"window_ns":finish-start,"process_group_cpu_s":sum(after.values())-sum(before.values()),
      "cpu_before":before,"cpu_after":after,"output_tokens_per_s":count*gen/((last-first)/1e9)}

def stop(p):
    if p.poll() is None or group_cpu(p.pid):
        try: os.killpg(p.pid,signal.SIGTERM)
        except ProcessLookupError: pass
    try: exitcode=p.wait(timeout=60)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid,signal.SIGKILL);p.wait();raise
    # The engine child may outlive the API parent briefly after group SIGTERM.
    deadline=time.monotonic()+60
    while group_cpu(p.pid) and time.monotonic()<deadline: time.sleep(.1)
    remaining=group_cpu(p.pid)
    if remaining:
        try: os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError: pass
        raise AssertionError(("forced owned child-group cleanup",p.pid,remaining))
    return exitcode

def analyze(path):
    records=[json.loads(l) for l in Path(path).read_text().splitlines()]
    meta=records[0];rows=[r for r in records if r["event"]=="request"]
    cells=[r for r in records if r["event"]=="cell"]
    assert not [r for r in records if r["event"]=="failure"]
    assert len(cells)==meta["repetitions"]*2*len(meta["matrix"])
    assert len(rows)==len(cells)*meta["requests_per_cell"]
    assert len([r for r in records if r["event"]=="executor"])==2*meta["repetitions"]
    for c in cells:
        selected=[r for r in rows if all(r[k]==c[k] for k in ("pair","mode","gen","concurrency"))]
        assert sorted(r["index"] for r in selected)==list(range(meta["requests_per_cell"]))
        assert [sum(r["case"]==i for r in selected) for i in range(4)]==[meta["requests_per_cell"]//4]*4
        for r in selected:
            expected=meta["cases"][r["case"]][1][:r["gen"]]
            assert len(r["tokens"])==r["gen"] and len(r["arrival_ns"])==r["gen"]
            assert all(0<=t<meta["vocab"] for t in r["tokens"])
            assert r["exact_reference"]==(r["tokens"]==expected)
            if r["mode"]=="bpfusion":assert r["exact_reference"]
            assert r["arrival_ns"]==sorted(r["arrival_ns"])
            assert r["ttft_ms"]==(r["arrival_ns"][0]-r["start_ns"])/1e6
            assert r["latency_ms"]==(r["arrival_ns"][-1]-r["start_ns"])/1e6
            if r["gen"]>1:assert r["tpot_ms"]==(r["arrival_ns"][-1]-r["arrival_ns"][0])/(r["gen"]-1)/1e6
        rate=len(selected)*c["gen"]/((max(r["arrival_ns"][-1] for r in selected)-min(r["start_ns"] for r in selected))/1e9)
        assert c["output_tokens_per_s"]==rate
    print(json.dumps({"records":len(records),"cells":len(cells),"requests":len(rows),
       "actual_tokens":sum(len(r["tokens"]) for r in rows),
       "reference_matches_by_mode":{m:sum(r["exact_reference"] for r in rows if r["mode"]==m) for m in ("bpfusion","vllm")}}))
    for gen,conc in meta["matrix"]:
        for metric in ("output_tokens_per_s","ttft_ms","tpot_ms","latency_ms"):
            if gen==1 and metric=="tpot_ms":continue
            means={}
            for m in ("bpfusion","vllm"):
                means[m]=[]
                for pair in range(meta["repetitions"]):
                    selected=[r for r in (cells if metric=="output_tokens_per_s" else rows) if (r["pair"],r["mode"],r["gen"],r["concurrency"])==(pair,m,gen,conc)]
                    means[m].append(statistics.mean(r[metric] for r in selected))
            diff=[a-b if metric=="output_tokens_per_s" else b-a for a,b in zip(means["bpfusion"],means["vllm"])]
            avg=statistics.mean(diff);margin=2.776445105*statistics.stdev(diff)/math.sqrt(5) if len(diff)==5 else None
            print(json.dumps({"gen":gen,"concurrency":conc,"metric":metric,"block_means":means,
              "means":{m:statistics.mean(v) for m,v in means.items()},"gain":avg,
              "paired_gains":diff,"nominal_t95_gain":[avg-margin,avg+margin] if margin is not None else None}))

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("--output",required=True)
    ap.add_argument("--preflight",action="store_true");ap.add_argument("--analyze",action="store_true")
    ap.add_argument("--gpu-memory-utilization",type=float)
    args=ap.parse_args();os.chdir(ROOT)
    if args.analyze:analyze(args.output);return
    assert command("git","symbolic-ref","--short","HEAD")=="main"
    ref=json.loads((ROOT/"bench/results/qwen_paired_kv_20261010.jsonl").read_text().splitlines()[0])
    cases=ref["cases"];assert len(cases)==4 and all(len(v[1])==64 for v in cases)
    matrix=[(1,1),(64,1),(1,8),(64,8)];count=8 if args.preflight else 64
    reps=1 if args.preflight else 5
    cmd=[str(TEMP/"venv/bin/vllm"),"serve",MODEL,"--tokens-only","--dtype","half","--host","127.0.0.1","--port","39404"]
    if args.gpu_memory_utilization is not None:cmd+=["--gpu-memory-utilization",str(args.gpu_memory_utilization)]
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("x") as raw:
        def emit(event,**values):
            raw.write(json.dumps({"event":event,**values})+"\n");raw.flush()
        emit("metadata",utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),commit=command("git","rev-parse","HEAD"),
             cases=cases,vocab=151936,matrix=matrix,repetitions=reps,requests_per_cell=count,vllm_command=cmd,
             reference_source="bench/results/qwen_paired_kv_20261010.jsonl",gpu=gpu_state(),cpu_tick_hz=TICK,
             driver_source=Path(__file__).read_text(),weight_match=json.loads((ROOT/"bench/results/qwen_vllm_weight_match_20261012.json").read_text()),
             production_sources={p:(ROOT/p).read_text() for p in ['executor/qwen_graph.py', 'executor/qwen_graph.cu', 'module/bfusion_tx.c', 'bpf/fusion.bpf.c', 'bpf/include/bpfusion_queue.h']},
             scope="shared-GPU token-only binary HTTP vs JSON/SSE; output agreement separately reported; no total-host CPU claim")
        for pair in range(reps):
            modes=("vllm","bpfusion") if args.preflight or pair%2 else ("bpfusion","vllm")
            order=matrix[pair%4:]+matrix[:pair%4]
            for mode in modes:
                p=None;key=secrets.token_urlsafe(32)
                logpath=TEMP/(target.stem+f"-pair{pair}-{mode}.log")
                try:
                    if mode=="bpfusion":command("./build/bpfusion_load","stream-attach")
                    env=os.environ.copy();env["HF_HOME"]="/workspaces/.cache/huggingface"
                    if mode=="vllm":
                        env["VLLM_API_KEY"]=key
                        env["PATH"]=str(TEMP/"venv/bin")+":"+env["PATH"]
                    start=time.monotonic()
                    with logpath.open("x") as log:
                        p=subprocess.Popen(cmd if mode=="vllm" else [str(ROOT/"build/qwen_graph"),"/workspaces/.cache/bpfusion/qwen25-05b-fp16.bin","300"],stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True)
                    print(f"START pair={pair} mode={mode} owned_pgid={p.pid} log={logpath}",flush=True)
                    while True:
                        assert p.poll() is None,logpath.read_text()
                        if mode=="bpfusion":
                            if "resident Qwen ready" in logpath.read_text():break
                        else:
                            try:
                                c=external_connect();c.request("GET","/health");r=c.getresponse();ok=r.status==200;r.read();c.close()
                                if ok:break
                            except (OSError,http.client.HTTPException):pass
                        time.sleep(.1)
                    startup=time.monotonic()-start
                    if mode=="vllm":
                        for token in (None,"invalid"):
                            c=external_connect();headers={} if token is None else {"Authorization":"Bearer "+token}
                            c.request("POST","/inference/v1/generate",b"{}",headers)
                            r=c.getresponse();assert r.status==401,r.status;r.read();c.close()
                        emit("authentication",pair=pair,mode=mode,missing=401,invalid=401)
                    c=connect(mode)
                    try:
                        for gen in (1,64):
                            for i,(ids,expected) in enumerate(cases):
                                r=one(c,mode,ids,expected[:gen],key)
                                emit("warmup",pair=pair,mode=mode,case=i,gen=gen,**r)
                    finally:c.close()
                    before=group_cpu(p.pid);t=time.monotonic_ns();time.sleep(1);after=group_cpu(p.pid)
                    emit("idle",pair=pair,mode=mode,window_ns=time.monotonic_ns()-t,
                         cpu_before=before,cpu_after=after,process_group_cpu_s=sum(after.values())-sum(before.values()))
                    for gen,conc in order:
                        rows=[];gpu_before=gpu_state()
                        try:summary=cell(p.pid,mode,cases,gen,conc,count,rows,key)
                        finally:
                            for r in sorted(rows,key=lambda r:r["index"]):emit("request",pair=pair,mode=mode,gen=gen,concurrency=conc,**r)
                        emit("cell",pair=pair,mode=mode,gen=gen,concurrency=conc,requests=count,gpu_before=gpu_before,gpu_after=gpu_state(),**summary)
                        print(f"pair={pair} mode={mode} gen={gen} c={conc} requests={len(rows)} reference_matches={sum(r['exact_reference'] for r in rows)} tps={summary['output_tokens_per_s']:.3f}",flush=True)
                    exitcode=stop(p);log=logpath.read_text()
                    assert exitcode in (0,-signal.SIGTERM),(exitcode,log)
                    stats=command("./build/bpfusion_load","stats") if mode=="bpfusion" else None
                    if mode=="bpfusion":
                        assert "dispatch=resident launches=1" in log and "graph_error=0" in log,log
                    emit("executor",pair=pair,mode=mode,exit=exitcode,startup_s=startup,log=log,stats=stats)
                except Exception as error:
                    emit("failure",pair=pair,mode=mode,error=repr(error),log=logpath.read_text() if logpath.exists() else "")
                    raise
                finally:
                    if p is not None and (p.poll() is None or group_cpu(p.pid)):stop(p)
                    if mode=="bpfusion":
                        command("./build/bpfusion_load","stream-detach");command("./build/bpfusion_load","detach","lo")
                        for name in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):Path("/sys/fs/bpf",name).unlink(missing_ok=True)
    analyze(target)
if __name__=="__main__":main()
