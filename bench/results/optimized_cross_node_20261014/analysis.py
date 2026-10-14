#!/usr/bin/env python3
"""Direct native client metric recomputation; remote rows have no server CPU."""
import json,math,statistics,sys
from collections import Counter
from pathlib import Path

for path in sys.argv[1:]:
    rows=[json.loads(line) for line in Path(path).read_text().splitlines()]
    meta=next(r for r in rows if r["event"]=="metadata")
    cells=[r for r in rows if r["event"]=="cell"]
    samples=[r for r in rows if r["event"]=="request" and r["kind"]=="measured"]
    executors=[r for r in rows if r["event"]=="executor"]
    expected=meta["repetitions"]*len(meta["executors"])*len(meta["matrix"])
    assert len(cells)==expected and len(samples)==expected*meta["requests_per_cell"]
    assert len(executors)==meta["repetitions"]*len(meta["executors"])
    assert not any(r["event"]=="failure" for r in rows)
    assert rows[-1]["event"]=="terminal" and rows[-1]["exit_code"]==0
    assert all(r["exit_code"]==0 and r["client_exit"]==0 for r in executors)
    assert {(r["pair"],r["mode"]) for r in executors}=={(i,m) for i in range(meta["repetitions"]) for m in meta["executors"]}
    warm=[r for r in rows if r["event"]=="request" and r["kind"]=="warmup"]
    assert len(warm)==len(executors)*8
    for r in samples+warm:
        pool={(tuple(x["prompt"]),x["gen"]):{tuple(v) for v in x["sequences"]} for x in meta["frozen_model"]["references"]}
        assert tuple(r["tokens"]) in pool[(tuple(meta["prompts"][r["case"]]),r["gen"])]
        assert len(r["arrival_ns"])==r["gen"]
        assert r["arrival_ns"]==sorted(r["arrival_ns"])
        assert r["ttft_ms"]==(r["arrival_ns"][0]-r["start_ns"])/1e6
        assert r["latency_ms"]==(r["arrival_ns"][-1]-r["start_ns"])/1e6
        expected_tpot=(r["arrival_ns"][-1]-r["arrival_ns"][0])/(r["gen"]-1)/1e6 if r["gen"]>1 else None
        assert r["tpot_ms"]==expected_tpot
    for c in cells:
        ss=[r for r in samples if all(r[k]==c[k] for k in ("pair","mode","gen","concurrency"))]
        assert sorted(r["index"] for r in ss)==list(range(meta["requests_per_cell"]))
        assert Counter(r["case"] for r in ss)=={i:meta["requests_per_cell"]//len(meta["prompts"]) for i in range(len(meta["prompts"]))}
        first=min(r["start_ns"] for r in ss);last=max(r["arrival_ns"][-1] for r in ss)
        assert c["output_tokens_per_s"]==len(ss)*c["gen"]/((last-first)/1e9)
    print(json.dumps({"path":path,"complete_cells":len(cells),"exact_requests":len(samples),"exact_tokens":sum(len(r["tokens"]) for r in samples),"normal_executors":len(executors)}))
    for gen,concurrency in meta["matrix"]:
        for mode in meta["executors"]:
            ss=[r for r in samples if (r["mode"],r["gen"],r["concurrency"])==(mode,gen,concurrency)]
            cc=[r for r in cells if (r["mode"],r["gen"],r["concurrency"])==(mode,gen,concurrency)]
            values={"mode":mode,"gen":gen,"concurrency":concurrency,"output_tokens_per_s":statistics.mean(c["output_tokens_per_s"] for c in cc)}
            for metric in ("ttft_ms","latency_ms","tpot_ms"):
                vv=sorted(r[metric] for r in ss if r[metric] is not None)
                values[metric+"_mean"]=statistics.mean(vv) if vv else None
                for p in (.5,.95,.99):values[metric+"_p"+str(int(100*p))]=vv[math.ceil(p*len(vv))-1] if vv else None
            print(json.dumps(values))
        for metric in ("ttft_ms","output_tokens_per_s"):
            diffs=[]
            for pair in range(meta["repetitions"]):
                def value(mode):
                    rr=samples if metric=="ttft_ms" else cells
                    vv=[r[metric] for r in rr if (r["pair"],r["mode"],r["gen"],r["concurrency"])==(pair,mode,gen,concurrency)]
                    return statistics.mean(vv)
                diff=value("userspace")-value("uring_loop")
                diffs.append(diff if metric=="ttft_ms" else -diff)
            mean=statistics.mean(diffs)
            margin=2.7764451051977987*statistics.stdev(diffs)/math.sqrt(len(diffs)) if len(diffs)==5 else None
            print(json.dumps({"gen":gen,"concurrency":concurrency,"metric":metric,"direction":"control-minus-resident" if metric=="ttft_ms" else "resident-minus-control","paired_differences":diffs,"mean":mean,"nominal_t95_df4":[mean-margin,mean+margin] if margin is not None else None}))
