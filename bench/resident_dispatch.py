#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Matched real-Qwen dispatch ablation on the existing token HTTP path."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import math
import os
from pathlib import Path
import platform
import socket
import statistics
import struct
import subprocess
import sys
import tempfile
import threading
import time

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tests"))
from resident_qwen import oracle_cases


def command(*args):
    return subprocess.check_output(args,text=True,stderr=subprocess.STDOUT).strip()


def cpu_seconds(pid):
    fields=Path(f"/proc/{pid}/stat").read_text().rsplit(") ",1)[1].split()
    return (int(fields[11])+int(fields[12]))/os.sysconf("SC_CLK_TCK")


def gpu_state():
    return command("nvidia-smi","--query-gpu=timestamp,name,clocks.sm,clocks.mem,temperature.gpu,power.draw,utilization.gpu","--format=csv,noheader,nounits")


def request(client,ids,expected):
    body=struct.pack("<IIIIQ",0x514c4d51,len(ids),len(expected),0,time.monotonic_ns())+struct.pack(f"<{len(ids)}I",*ids)
    wire=f"POST /generate HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(body)}\r\n\r\n".encode()+body
    start=time.monotonic_ns()
    client.sendall(wire)
    header=b""; data=b""; arrivals=[]
    while len(data)<4*len(expected):
        chunk=client.recv(4096)
        arrived=time.monotonic_ns()
        assert chunk,"short reply"
        if header is not None:
            header+=chunk
            if b"\r\n\r\n" not in header: continue
            head,chunk=header.split(b"\r\n\r\n",1)
            assert head.startswith(b"HTTP/1.1 200 OK\r\n"),head
            assert f"Content-Length: {4*len(expected)}".encode() in head,head
            header=None
        data+=chunk
        arrivals.extend([arrived]*((len(data)//4)-len(arrivals)))
    assert len(data)==4*len(expected),data
    actual=list(struct.unpack(f"<{len(expected)}I",data))
    assert actual==expected,(ids,actual,expected)
    return {"start_ns":start,"arrival_ns":arrivals,"tokens":actual,
            "ttft_ms":(arrivals[0]-start)/1e6,
            "latency_ms":(arrivals[-1]-start)/1e6,
            "tpot_ms":(arrivals[-1]-arrivals[0])/(len(expected)-1)/1e6 if len(expected)>1 else None}


def connect():
    client=socket.create_connection(("127.0.0.1",39403),timeout=60)
    client.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,1)
    return client


def cell(pid,cases,gen,concurrency,count,rows):
    # Connections and thread creation precede both the timer and CPU window.
    barrier=threading.Barrier(concurrency+1)
    ready=threading.Barrier(concurrency+1)
    def worker(worker_id):
        with connect() as client:
            ready.wait(timeout=60)
            barrier.wait(timeout=60)
            for index in range(worker_id,count,concurrency):
                case=index%len(cases); ids,expected=cases[case]
                row=request(client,ids,expected[:gen]); row.update(index=index,case=case)
                rows.append(row)
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures=[pool.submit(worker,i) for i in range(concurrency)]
        ready.wait(timeout=60)
        before=cpu_seconds(pid); start=time.monotonic_ns()
        barrier.wait(timeout=60)
        for future in futures: future.result()
        finish=time.monotonic_ns(); after=cpu_seconds(pid)
    first=min(row["start_ns"] for row in rows)
    last=max(row["arrival_ns"][-1] for row in rows)
    return {
        "window_ns":finish-start,"executor_cpu_s":after-before,
        "output_tokens_per_s":count*gen/((last-first)/1e9)}


def analyze(path):
    records=[json.loads(line) for line in Path(path).read_text().splitlines()]
    meta=next(row for row in records if row["event"]=="metadata")
    cells=[row for row in records if row["event"]=="cell"]
    samples=[row for row in records if row["event"]=="request"]
    expected_cells=meta["repetitions"]*2*len(meta["matrix"])
    assert len(cells)==expected_cells,(len(cells),expected_cells)
    assert len(samples)==expected_cells*meta["requests_per_cell"]
    assert len([row for row in records if row["event"]=="executor"])==2*meta["repetitions"]
    for row in samples:
        assert row["tokens"]==meta["cases"][row["case"]][1][:row["gen"]],row
        assert row["ttft_ms"]==(row["arrival_ns"][0]-row["start_ns"])/1e6,row
    for block in cells:
        selected=[row for row in samples if all(row[key]==block[key] for key in ("pair","mode","gen","concurrency"))]
        assert sorted(row["index"] for row in selected)==list(range(meta["requests_per_cell"])),block
    def percentile(values,q):
        ordered=sorted(values); pos=(len(ordered)-1)*q
        low=math.floor(pos); high=math.ceil(pos)
        return ordered[low]+(ordered[high]-ordered[low])*(pos-low)
    for gen,concurrency in meta["matrix"]:
        pair_means={}
        for mode in ("resident","host-launch"):
            selected=[row for row in samples if row["mode"]==mode and row["gen"]==gen and row["concurrency"]==concurrency]
            selected_cells=[row for row in cells if row["mode"]==mode and row["gen"]==gen and row["concurrency"]==concurrency]
            ttft=[row["ttft_ms"] for row in selected]
            tpot=[row["tpot_ms"] for row in selected if row["tpot_ms"] is not None]
            pair_means[mode]=[statistics.mean(row["ttft_ms"] for row in selected if row["pair"]==pair) for pair in range(meta["repetitions"])]
            print(json.dumps({"mode":mode,"gen":gen,"concurrency":concurrency,"requests":len(selected),
                "ttft_mean_ms":statistics.mean(ttft),"ttft_p50_ms":percentile(ttft,.5),"ttft_p99_ms":percentile(ttft,.99),
                "tpot_mean_ms":statistics.mean(tpot) if tpot else None,
                "executor_cpu_s_per_cell":[row["executor_cpu_s"] for row in selected_cells],
                "tokens_per_s":[row["output_tokens_per_s"] for row in selected_cells]}))
        differences=[host-resident for host,resident in zip(pair_means["host-launch"],pair_means["resident"])]
        mean=statistics.mean(differences)
        # Five independent paired process blocks; Student t, df=4, two-sided 95%.
        margin=2.776445105*statistics.stdev(differences)/math.sqrt(5) if len(differences)==5 else None
        print(json.dumps({"gen":gen,"concurrency":concurrency,"paired_host_minus_resident_ttft_ms":differences,
            "difference_mean_ms":mean,"difference_t95_ms":[mean-margin,mean+margin] if margin is not None else None}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True)
    parser.add_argument("--preflight",action="store_true")
    parser.add_argument("--gen",type=int,default=8,choices=range(2,65),help="long output length; paired with one-token requests")
    parser.add_argument("--analyze",action="store_true")
    parser.add_argument("--resident-executor",default="./build/qwen")
    parser.add_argument("--host-executor",default="./build/qwen_host_launch")
    args=parser.parse_args()
    if args.analyze: analyze(args.output); return
    cases,_=oracle_cases(args.gen)
    matrix=[(1,1)] if args.preflight else [(1,1),(args.gen,1),(1,8),(args.gen,8)]
    repetitions=1 if args.preflight else 5
    count=4 if args.preflight else 64
    output=Path(args.output); output.parent.mkdir(parents=True,exist_ok=True)
    with output.open("x") as raw:
        def emit(event,**values):
            raw.write(json.dumps({"event":event,**values})+"\n"); raw.flush()
        import torch, transformers
        emit("metadata",utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),commit=command("git","rev-parse","HEAD"),
             executors={"resident":args.resident_executor,"host-launch":args.host_executor},
             kernel=platform.release(),torch=torch.__version__,transformers=transformers.__version__,
             nvcc=command("/usr/local/cuda/bin/nvcc","--version"),gpu=gpu_state(),cpu_tick_hz=os.sysconf("SC_CLK_TCK"),
             cases=cases,matrix=matrix,repetitions=repetitions,requests_per_cell=count,
             timing="client monotonic; tokens completed in one recv share arrival timestamp; process CPU excludes kernel TX/softirq")
        for pair in range(repetitions):
            modes=("resident","host-launch") if pair%2==0 else ("host-launch","resident")
            cells=matrix[pair%len(matrix):]+matrix[:pair%len(matrix)]
            for mode in modes:
                executor=None
                with tempfile.TemporaryDirectory(prefix="bpfusion-dispatch-") as tmp:
                    logpath=Path(tmp)/"executor.log"
                    try:
                        command("./build/bpfusion_load","stream-attach")
                        binary=args.resident_executor if mode=="resident" else args.host_executor
                        with logpath.open("w") as log:
                            executor=subprocess.Popen([binary,"/workspaces/.cache/bpfusion/qwen25-05b-fp16.bin","300"],stdout=log,stderr=subprocess.STDOUT)
                        started=time.monotonic()
                        while "resident Qwen ready" not in logpath.read_text():
                            assert executor.poll() is None and time.monotonic()-started<60,logpath.read_text()
                            time.sleep(.05)
                        with connect() as client:
                            for gen in (1,args.gen):
                                for ids,expected in cases: request(client,ids,expected[:gen])
                        before=cpu_seconds(executor.pid); idle_start=time.monotonic_ns(); time.sleep(1)
                        emit("idle",pair=pair,mode=mode,window_ns=time.monotonic_ns()-idle_start,executor_cpu_s=cpu_seconds(executor.pid)-before)
                        for gen,concurrency in cells:
                            gpu_before=gpu_state()
                            rows=[]
                            try:
                                summary=cell(executor.pid,cases,gen,concurrency,count,rows)
                            finally:
                                for row in sorted(rows,key=lambda row:row["index"]):
                                    emit("request",pair=pair,mode=mode,gen=gen,concurrency=concurrency,**row)
                            gpu_after=gpu_state()
                            emit("cell",pair=pair,mode=mode,gen=gen,concurrency=concurrency,requests=count,
                                 gpu_before=gpu_before,gpu_after=gpu_after,**summary)
                            print(f"pair={pair} mode={mode} gen={gen} c={concurrency} requests={count} exact_tokens={count*gen} cpu_s={summary['executor_cpu_s']:.3f}",flush=True)
                        executor.terminate(); assert executor.wait(timeout=60)==0,logpath.read_text()
                        log=logpath.read_text(); launches=1 if mode=="resident" else 8+count*len(matrix)
                        assert f"dispatch={mode} launches={launches}" in log,log
                        emit("executor",pair=pair,mode=mode,log=log,stats=command("./build/bpfusion_load","stats"))
                    except Exception as error:
                        emit("failure",pair=pair,mode=mode,error=repr(error),
                             log=logpath.read_text() if logpath.exists() else "",
                             stats=command("./build/bpfusion_load","stats"))
                        raise
                    finally:
                        if executor is not None and executor.poll() is None:
                            executor.terminate(); executor.wait(timeout=60)
                        command("./build/bpfusion_load","stream-detach")
                        command("./build/bpfusion_load","detach","lo")
                        for name in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):
                            Path("/sys/fs/bpf",name).unlink(missing_ok=True)
    analyze(output)


if __name__=="__main__": main()
