#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Predeclared ordinary transfer round/CQ analysis; no GPU execution."""
import json,math,re,statistics,sys
from pathlib import Path

def main():
    root=Path(sys.argv[1]);rows=[]
    files=sorted(root.glob("full_transfer_*.jsonl"))
    assert len(files)==10
    for path in files:
        records=[json.loads(line) for line in path.open()]
        meta=next(x for x in records if x["event"]=="metadata")
        assert meta["matrix"]==[[1,1],[64,1],[64,8]]
        assert meta["requests_per_cell"]==32 and meta["warmups_per_executor"]==8
        assert records[-1]["event"]=="terminal" and records[-1]["exit_code"]==0
        for executor in [x for x in records if x["event"]=="executor"]:
            mode=executor["mode"]
            requests=[x for x in records if x["event"]=="request" and x["mode"]==mode]
            assert len(requests)==104 and all(not x["bad"] and len(x["tokens"])==x["gen"] for x in requests)
            groups=[[x for x in requests if x["kind"]=="warmup"]]
            groups += [[x for x in requests if x["kind"]=="measured" and (x["gen"],x["concurrency"])==(g,1)] for g in [1,64]]
            assert [len(g) for g in groups]==[8,32,32]
            for group in groups:
                ordered=sorted(group,key=lambda x:x["start_ns"])
                assert all(a["arrival_ns"][-1]<=b["start_ns"] for a,b in zip(ordered,ordered[1:]))
            serial_rounds=sum(x["gen"] for group in groups for x in group)
            assert serial_rounds==2088
            counters={k:int(v) for k,v in re.findall(r"(\w+)=(\d+)",executor["stdout"].split("resident vLLM stopped:",1)[1].splitlines()[0])}
            assert counters["admitted"]==counters["retired"]==104 and counters["graph_error"]==0
            long_rounds=counters["device_graph_launches"]-serial_rounds
            assert 256<=long_rounds<=2048
            cell=next(x for x in records if x["event"]=="cell" and x["mode"]==mode and (x["gen"],x["concurrency"])==(64,8))
            selected=[x for x in requests if x["kind"]=="measured" and (x["gen"],x["concurrency"])==(64,8)]
            assert len(selected)==32 and cell["first_ns"]==min(x["start_ns"] for x in selected)
            assert cell["last_ns"]==max(x["arrival_ns"][-1] for x in selected)
            tps=2048/((cell["last_ns"]-cell["first_ns"])/1e9)
            assert tps==cell["output_tokens_per_s"]
            row=dict(model=meta["model"],block=meta["block"],mode=mode,
                     total_model_rounds=counters["device_graph_launches"],
                     deducted_serial_rounds=serial_rounds,long_c8_model_rounds=long_rounds,tokens_per_s=tps)
            if mode!="userspace":
                ring=json.loads(next(line[7:] for line in executor["stdout"].splitlines() if line.startswith("RESULT ")))
                assert ring["sqhead"]==ring["sqtail"] and ring["cqhead"]==ring["cqtail"]
                assert all(ring[k]==0 for k in ["pending","error","dropped","overflow"])
                row.update(whole_transfer_sq=ring["sqtail"],whole_transfer_cq=ring["cqtail"],
                           whole_transfer_extra_multishot_cq=ring["cqtail"]-ring["sqtail"],
                           whole_transfer_extra_cq_fraction=(ring["cqtail"]-ring["sqtail"])/ring["cqtail"])
            rows.append(row)
    summaries=[];effects=[]
    for model in sorted({x["model"] for x in rows}):
        for mode in ["uring_loop_coalesced","userspace","uring_loop"]:
            selected=sorted([x for x in rows if (x["model"],x["mode"])==(model,mode)],key=lambda x:x["block"])
            assert [x["block"] for x in selected]==list(range(5))
            summaries.append(dict(model=model,mode=mode,rounds=[x["long_c8_model_rounds"] for x in selected],
                                  mean_rounds=statistics.mean(x["long_c8_model_rounds"] for x in selected),
                                  mean_tokens_per_s=statistics.mean(x["tokens_per_s"] for x in selected)))
        for control in ["uring_loop_coalesced","userspace"]:
            differences=[]
            for block in range(5):
                def one(mode):
                    return next(x for x in rows if (x["model"],x["block"],x["mode"])==(model,block,mode))["long_c8_model_rounds"]
                differences.append(one("uring_loop")-one(control))
            mean=statistics.mean(differences);half=2.776445105*statistics.stdev(differences)/math.sqrt(5)
            effects.append(dict(model=model,candidate_minus=control,round_differences=differences,mean=mean,t95=[mean-half,mean+half]))
    print(json.dumps(dict(scope="predeclared secondary ordinary transfer counters; not isolated GPU time or primary performance evidence",
                          rows=rows,summaries=summaries,round_effects=effects),indent=2))
if __name__=="__main__":main()
