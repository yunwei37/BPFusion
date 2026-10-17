#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Recompute per-cell tails and separate nested CPU scopes from retained raw data."""
from pathlib import Path
import argparse,gzip,json,math,statistics,struct
from collections import Counter

def read(p):
    with gzip.open(p,"rt") if p.suffix==".gz" else p.open() as f:
        return [json.loads(line) for line in f]
def quantile(v,q):
    if not v:return None
    v=sorted(v);x=(len(v)-1)*q;i=int(x);a=x-i
    return v[i] if not a else v[i]*(1-a)+v[i+1]*a
def summary(v):
    return dict(mean=statistics.mean(v),p50=quantile(v,.5),p90=quantile(v,.9),
                p95=quantile(v,.95),p99=quantile(v,.99),p999=quantile(v,.999),max=max(v)) if v else None
def cell(prefix):
    p=Path(str(prefix)+".client.jsonl.gz");rows=read(p);m=rows[0]
    requests=[x for x in rows if x["event"]=="request"]
    assert len(requests)==m["attempts"] and sorted(x["index"] for x in requests)==list(range(m["attempts"]))
    assert m["worker_exit"]==[0]*m["workers"]
    assert all(x["scheduled_ns"]==m["epoch_ns"]+m["offsets_ns"][x["index"]] and x["begin_ns"]>=x["scheduled_ns"] for x in requests)
    assert all(x["source"]==m["source"] for x in rows if x["event"]=="worker_metadata")
    expected={x["part"]:x["patterns"] for x in rows if x["event"]=="worker_metadata"}
    good=[x for x in requests if x["outcome"]=="success"]
    for x in good:
        assert len(bytes.fromhex(x["reply_hex"]))==256
        assert list(struct.unpack("<64f",bytes.fromhex(x["reply_hex"])))==expected[x["index"]%m["workers"]][x["pattern"]]["expected"]
        assert x["scheduled_ns"]==m["epoch_ns"]+m["offsets_ns"][x["index"]]
    tails={}
    for name,values in [
        ("scheduled_response_ms",[(x["complete_ns"]-x["scheduled_ns"])/1e6 for x in good]),
        ("begin_response_ms",[(x["complete_ns"]-x["begin_ns"])/1e6 for x in good]),
        ("client_connection_wait_ms",[(x["begin_ns"]-x["scheduled_ns"])/1e6 for x in requests]),
        ("timer_dispatch_lag_ms",[v[2]/1e6 for x in rows if x["event"]=="worker_terminal" for v in x["timer_lag"]])]:
        tails[name]=summary(values)
    failures=len(requests)-len(good)
    all_rank=(len(requests)-1)*.99
    successful_latencies=sorted((x["complete_ns"]-x["scheduled_ns"])/1e6 for x in good)
    if math.ceil(all_rank)>=len(successful_latencies):failure_aware_p99=None
    else:
        i=math.floor(all_rank);part=all_rank-i
        failure_aware_p99=successful_latencies[i] if not part else successful_latencies[i]*(1-part)+successful_latencies[i+1]*part
    duration=max(m["seconds"],(max(x["end_ns"] for x in requests)-m["epoch_ns"])/1e9)
    resources=read(Path(str(prefix)+".resources.jsonl.gz"));samples=[x for x in resources if x["event"]=="sample"]
    first,last=samples[0],samples[-1];tick=resources[0]["clock_tick"]
    ga,gb=first["process_group"],last["process_group"]
    def identity(v):return v["stat"].rsplit(") ",1)[1].split()[19]
    stable=set(ga)==set(gb) and all(identity(ga[k])==identity(gb[k]) for k in ga)
    cpu_ms=(sum(x["cpu_ns"] for x in gb.values())-sum(x["cpu_ns"] for x in ga.values()))/1e6 if stable else None
    a,b=[[int(z) for z in x["host"]["stat"].splitlines()[0].split()[1:]] for x in [first,last]]
    classes=dict(zip(["user","nice","system","idle","iowait","irq","softirq","steal","guest","guest_nice"],[(y-x)/tick*1000 for x,y in zip(a,b)]))
    host_active=sum(classes[k] for k in ["user","nice","system","irq","softirq"])
    receipt=json.loads(Path(str(prefix)+".server_terminal.json").read_text())
    assert receipt.get("exit")==0 and not receipt["remaining_pins"]
    log=Path(str(prefix)+".server.stdout").read_text()
    assert "graph_error=0" in log and "graph backend ready: abi=1 slots=8" in log
    counters=None
    if receipt["mode"]=="kernel":
        counters=json.loads(next(x[7:] for x in log.splitlines() if x.startswith("RESULT ")))
        assert all(counters[k]==0 for k in ["error","pending","reserved","dropped","overflow"])
        assert counters["accepted"]==counters["closed"]
        assert counters["sqhead"]==counters["sqtail"] and counters["cqhead"]==counters["cqtail"]
    idle_rows=read(Path(str(prefix)+".idle.resources.jsonl.gz"))
    idle=[x for x in idle_rows if x["event"]=="sample"]
    ia,ib=idle[0],idle[-1];idle_s=(ib["sample_end_ns"]-ia["sample_begin_ns"])/1e9
    xa,xb=[[int(z) for z in x["host"]["stat"].splitlines()[0].split()[1:]] for x in [ia,ib]]
    idle_host_ms=sum(xb[k]-xa[k] for k in [0,1,2,5,6])/tick*1000
    idle_group_ms=(sum(x["cpu_ns"] for x in ib["process_group"].values())-sum(x["cpu_ns"] for x in ia["process_group"].values()))/1e6 if set(ia["process_group"])==set(ib["process_group"]) else None
    observation_s=(last["sample_end_ns"]-first["sample_begin_ns"])/1e9
    requested=set(receipt["service_affinity"])
    def cpuset(text):
        result=set()
        for piece in text.split(","):
            a,sep,b=piece.partition("-")
            result.update(range(int(a),int(b)+1) if sep else [int(a)])
        return result
    actual_masks=[]
    for sample in samples:
        for tid,v in sample.get("service_threads",{}).items():
            text=next((line.split(":",1)[1].strip() for line in v["status"].splitlines() if line.startswith("Cpus_allowed_list:")),None)
            if text is not None:actual_masks.append(dict(tid=tid,allowed=text))
    affinity_verified=all(cpuset(v["allowed"])<=requested for v in actual_masks) and bool(actual_masks)
    metric=dict(event="cell",tag=prefix.name,mode=receipt["mode"],operation=receipt["operation"],
        repeat=receipt["repeat"],cores=receipt["cores"],affinity=receipt["service_affinity"],
        offered_rate=m["rate"],seed=m["seed"],offered_seconds=m["seconds"],duration_s=duration,
        attempts=len(requests),successes=len(good),failures=failures,throughput=len(good)/duration,
        failure_fraction=failures/len(requests),failure_types=dict(Counter(x["error"] for x in requests if x["outcome"]!="success")),latency=tails,
        first_quarter_response_mean_ms=statistics.mean((x["complete_ns"]-x["scheduled_ns"])/1e6 for x in good if x["index"]<len(requests)//4) if any(x["index"]<len(requests)//4 for x in good) else None,
        last_quarter_response_mean_ms=statistics.mean((x["complete_ns"]-x["scheduled_ns"])/1e6 for x in good if x["index"]>=3*len(requests)//4) if any(x["index"]>=3*len(requests)//4 for x in good) else None,
        failure_aware_p99_ms=failure_aware_p99,
        failure_aware_p99_status="unbounded_with_failed_requests_at_infinity" if failure_aware_p99 is None else "all_attempt_rank_with_failed_requests_at_infinity",
        service_affinity_verified=affinity_verified,sampled_affinity_masks=sorted(set(x["allowed"] for x in actual_masks)),
        group_stable=stable,owned_group_cpu_ms_per_attempt=cpu_ms/len(requests) if stable else None,
        owned_group_cpu_ms_per_success=cpu_ms/len(good) if stable and good else None,
        host_active_cpu_ms_per_attempt=host_active/len(requests),host_cpu_ms_by_class=classes,
        observation_s=(last["sample_end_ns"]-first["sample_begin_ns"])/1e9,
        client_cpu_ms_per_attempt=(rows[-1]["supervisor_cpu_ns"]/1e6+rows[-1]["child_cpu_s"]*1000)/len(requests),
        service_thread_affinity=[dict(tid=k,allowed=next((line.split(":",1)[1].strip() for line in v["status"].splitlines() if line.startswith("Cpus_allowed_list:")),None)) for k,v in last.get("service_threads",{}).items()],
        counters=counters,idle_window_s=idle_s,idle_host_active_cpu_ms_per_s=idle_host_ms/idle_s,
        idle_group_cpu_ms_per_s=idle_group_ms/idle_s if idle_group_ms is not None else None,
        idle_context_host_delta_ms_per_attempt=(host_active-idle_host_ms/idle_s*observation_s)/len(requests),
        idle_context_group_delta_ms_per_attempt=(cpu_ms-idle_group_ms/idle_s*observation_s)/len(requests) if stable and idle_group_ms is not None else None,
        scope="Process/group, cgroup and host overlap; host includes foreign tasks and observer.")
    ecdf=Path(str(prefix)+".latency_ecdf.json.gz")
    ecdf.write_bytes(gzip.compress(json.dumps(dict(
        scheduled_response_ms=sorted((x["complete_ns"]-x["scheduled_ns"])/1e6 for x in good),
        begin_response_ms=sorted((x["complete_ns"]-x["begin_ns"])/1e6 for x in good),
        failures=failures,attempts=len(requests)),separators=(",",":")).encode(),mtime=0))
    return metric

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("prefix",type=Path);args=ap.parse_args()
    result=cell(args.prefix)
    Path(str(args.prefix)+".metrics.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result))
