#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Recompute complete traced vLLM serving evidence and paired client metrics."""
import argparse,json,math,re,statistics
from collections import Counter
from pathlib import Path

def analyze(path):
    records=[json.loads(line) for line in path.open()]
    meta=next(r for r in records if r["event"]=="metadata")
    assert records[-1]["event"]=="terminal" and records[-1]["exit_code"]==0
    assert not any(r["event"]=="failure" for r in records)
    expected={(pair,mode) for pair in range(meta["repetitions"]) for mode in meta["modes"]}
    executors=[r for r in records if r["event"]=="executor"]
    verified=[r for r in records if r["event"]=="verified"]
    assert {(r["pair"],r["mode"]) for r in executors}==expected and len(executors)==len(expected)
    assert len(verified)==len(expected)
    total_tokens=0;total_requests=0;all_batches=set()
    frozen_pool={}
    if meta.get("untraced"):
        frozen=next(r for r in records if r["event"]=="frozen_complete_references")["model"]
        assert frozen["model"]==meta["model"] and frozen["vocab"]==meta["vocab"] and frozen["precision"]=="fp16"
        frozen_pool={(tuple(r["prompt"]),r["gen"]):{tuple(s) for s in r["sequences"]} for r in frozen["references"]}
    for pair,mode in sorted(expected):
        executor=next(r for r in executors if (r["pair"],r["mode"])==(pair,mode))
        assert executor["exit_code"]==0 and "graph_error=0" in executor["stdout"]
        assert "launches=1 " in executor["stdout"] and "trace_overflows=0" in executor["stdout"]
        requests=[r for r in records if r["event"]=="request" and (r["pair"],r["mode"])==(pair,mode)]
        if meta.get("untraced"):
            computes=[];admissions=[];release_summary={}
            for row in requests:
                assert len(row["tokens"])==(0 if row["bad"] else row["gen"])
                if not row["bad"]:assert tuple(row["tokens"]) in frozen_pool[(tuple(row["input_ids"]),row["gen"])]
                if "arrival_ns" in row:
                    assert len(row["arrival_ns"])==row["gen"] and row["arrival_ns"]==sorted(row["arrival_ns"])
                    assert row["ttft_ms"]==(row["arrival_ns"][0]-row["start_ns"])/1e6
                    assert row["latency_ms"]==(row["arrival_ns"][-1]-row["start_ns"])/1e6
                    assert row["tpot_ms"]==((row["arrival_ns"][-1]-row["arrival_ns"][0])/(row["gen"]-1)/1e6 if row["gen"]>1 else None)
            counters={k:int(v) for k,v in re.findall(r"(\w+)=(\d+)",executor["stdout"].split("resident vLLM stopped:",1)[1].splitlines()[0])}
            assert counters["admitted"]==counters["retired"]==len(requests)
            assert counters["graph_error"]==counters["trace_overflows"]==0
            v=next(r for r in verified if (r["pair"],r["mode"])==(pair,mode))
            assert v["native_counters"]==counters and v["tokens"]==sum(len(r["tokens"]) for r in requests)
            if mode.endswith("kernel"):
                stats=next(r for r in records if r["event"]=="stats" and (r["pair"],r["mode"])==(pair,mode))
                assert stats["code"]==0 and "llm_reserved=0x0" in stats["stdout"]
                assert f"llm_head={len(requests)}\n" in stats["stdout"]
                assert sorted(re.findall(r"llm\[(\d+)\]: state=(\d+)",stats["stdout"]))==[(str(i),"0") for i in range(8)]
            else:
                n=re.search(r"userspace TCP stopped: accepted=(\d+) published=(\d+) completed=(\d+) rejected=(\d+)",executor["stdout"])
                assert n and int(n[2])==int(n[3])==len(requests) and int(n[4])==sum(r["bad"] for r in requests)
            release_summary=dict(native_counters=counters,reference_scope=v["reference_scope"])
        else:
            prefix=path.with_suffix("").with_name(path.stem+f"_p{pair}_{mode}")
            refs=[json.loads(line) for line in Path(str(prefix)+".gpu.jsonl.references.jsonl").open()]
            by_marker={r["client_ns"]:r for r in refs}
            assert len(refs)==len(requests)==len(by_marker)
            for row in requests:
                ref=by_marker.pop(row["client_ns"])
                assert row["input_ids"]==ref["prompt"] and row["gen"]==ref["gen"] and row["bad"]==bool(ref["bad"])
                assert row["tokens"]==ref["tokens"],(row,ref)
                if "arrival_ns" in row:
                    assert len(row["tokens"])==row["gen"]==len(row["arrival_ns"])
                    assert row["arrival_ns"]==sorted(row["arrival_ns"])
                    assert row["ttft_ms"]==(row["arrival_ns"][0]-row["start_ns"])/1e6
                    assert row["latency_ms"]==(row["arrival_ns"][-1]-row["start_ns"])/1e6
                    assert row["tpot_ms"]==((row["arrival_ns"][-1]-row["arrival_ns"][0])/(row["gen"]-1)/1e6 if row["gen"]>1 else None)
            assert not by_marker
            events=[json.loads(line) for line in Path(str(prefix)+".gpu.jsonl").open()]
            assert events[-1]["event"]=="terminal" and events[-1]["overflows"]==0
            admissions=[r for r in events if r["event"]=="admission"]
            computes=[r for r in events if r["event"]=="compute"]
            assert len(admissions)==len(requests)
            admissions_by_marker={r["client_ns"]:r for r in admissions}
            by_id={r["id"]:r for r in refs};trace_tokens={key:[] for key in by_id}
            for row in requests:
                a=admissions_by_marker[row["client_ns"]]
                assert a["input_ids"]==row["input_ids"] and a["gen"]==row["gen"] and bool(a["bad"])==row["bad"]
            for event in computes:
                assert event["batch"]==len(event["request_ids"])==len(event["tokens"])
                for request_id,token in zip(event["request_ids"],event["tokens"]):trace_tokens[request_id].append(token)
            assert all(trace_tokens[key]==value["tokens"] for key,value in by_id.items())
            assert sum(len(r["tokens"]) for r in requests)==sum(e["batch"] for e in computes)
            releases=[e for e in events if e["event"]=="release"];release_summary={}
            if releases:
                owners={};emitted=Counter();released=[]
                for event in events:
                    if event["event"]=="admission":
                        physical=event["id"]%8;assert physical not in owners
                        owners[physical]=event["id"]
                    elif event["event"]=="compute":
                        for request_id in event["request_ids"]:
                            assert owners[request_id%8]==request_id and request_id not in released
                            emitted[request_id]+=1
                    elif event["event"]=="release":
                        ids=event["request_ids"];assert len(ids)==event["batch"]
                        assert ids==list(range(len(released),len(released)+len(ids)))
                        for request_id in ids:
                            assert owners.pop(request_id%8)==request_id
                            assert emitted[request_id]==len(by_id[request_id]["tokens"])
                            released.append(request_id)
                assert not owners and set(released)==set(by_id)
                release_summary=dict(release_rounds=len(releases),max_release=max(e["batch"] for e in releases))
                if meta.get("comparison")=="release":
                    assert release_summary["max_release"]==1 if mode.startswith("serial") else release_summary["max_release"]>1
                clients={ref["id"]:next(row for row in requests if row["client_ns"]==ref["client_ns"]) for ref in refs}
                for gen,c in meta["matrix"] if not meta["correctness"] else []:
                    ids={rid for rid,row in clients.items() if row["kind"]=="measured" and (row["gen"],row["concurrency"])==(gen,c)}
                    selected=[e for e in releases if any(rid in ids for rid in e["request_ids"])]
                    assert sum(sum(rid in ids for rid in e["request_ids"]) for e in selected)==meta.get("requests_per_cell",64)
                    print(json.dumps(dict(event="cell_release",pair=pair,mode=mode,gen=gen,concurrency=c,
                        release_rounds=len(selected),max_prefix=max(e["batch"] for e in selected),
                        multi_release_requests=sum(sum(rid in ids for rid in e["request_ids"]) for e in selected if e["batch"]>1))))
        if meta.get("comparison")=="dispatch":
            d=next(r for r in records if r["event"]=="dispatch_verified" and (r["pair"],r["mode"])==(pair,mode))
            counters={k:int(v) for k,v in re.findall(r"(\w+)=(\d+)",executor["stdout"].split("resident vLLM stopped:",1)[1].splitlines()[0])}
            assert d["model_steps"]==counters["device_graph_launches"]
            assert d["device_launch_calls"]==counters["device_launch_calls"]==d["model_steps"]*(1 if mode.startswith("chained") else 2)
            if not meta.get("untraced"):assert d["model_steps"]==len(computes)
        total_tokens+=sum(len(r["tokens"]) for r in requests);total_requests+=len(requests)
        all_batches.update(e["batch"] for e in computes)
        if meta["correctness"]:
            assert len(requests)==622 and sum(r["bad"] for r in requests)==259
            assert sum(len(r["tokens"]) for r in requests)==22224
            assert any(r["kind"]=="pipeline_halfclose" for r in requests)
            assert any(r["kind"]=="binary_reject" for r in requests)
            assert len([r for r in records if r["event"]=="network_verified" and (r["pair"],r["mode"])==(pair,mode)])==1
        print(json.dumps(dict(event="verified_executor",pair=pair,mode=mode,requests=len(requests),
            tokens=sum(len(r["tokens"]) for r in requests),rejections=sum(r["bad"] for r in requests),
            actual_batches=sorted({e["batch"] for e in computes}) if not meta.get("untraced") else None,graphs=len(computes) if not meta.get("untraced") else None,
            prefill_graphs=sum(bool(e["query"]) for e in computes) if not meta.get("untraced") else None,decode_graphs=sum(not e["query"] for e in computes) if not meta.get("untraced") else None,
            real_prompt_tokens=sum(len(a["input_ids"]) for a in admissions if not a["bad"]) if not meta.get("untraced") else None,
            padded_query_tokens=(sum(e["query"]*e["batch"] for e in computes if e["query"])-sum(len(a["input_ids"]) for a in admissions if not a["bad"])) if not meta.get("untraced") else None,**release_summary)))
    print(json.dumps(dict(event="coverage",requests=total_requests,tokens=total_tokens,actual_batches=sorted(all_batches) if not meta.get("untraced") else None)))
    if meta["correctness"] or meta.get("preflight"):return
    count=meta.get("requests_per_cell",64)
    samples=[r for r in records if r["event"]=="request" and r["kind"]=="measured"]
    warmups=[r for r in records if r["event"]=="request" and r["kind"]=="warmup"]
    cells=[r for r in records if r["event"]=="cell"]
    assert len(samples)==meta["repetitions"]*len(meta["modes"])*len(meta["matrix"])*count
    assert len(cells)==meta["repetitions"]*len(meta["modes"])*len(meta["matrix"])
    assert len(warmups)==len(expected)*8
    summaries={}
    for pair,mode in sorted(expected):
        for gen,c in meta["matrix"]:
            selected=[r for r in samples if (r["pair"],r["mode"],r["gen"],r["concurrency"])==(pair,mode,gen,c)]
            assert sorted(r["index"] for r in selected)==list(range(count))
            cell=next(r for r in cells if (r["pair"],r["mode"],r["gen"],r["concurrency"])==(pair,mode,gen,c))
            first=min(r["start_ns"] for r in selected);last=max(r["arrival_ns"][-1] for r in selected)
            assert cell["first_ns"]==first and cell["last_ns"]==last and cell["requests"]==count and cell["tokens"]==count*gen
            tps=count*gen/((last-first)/1e9);assert tps==cell["output_tokens_per_s"]
            summaries[pair,mode,gen,c]=dict(ttft_ms=statistics.mean(r["ttft_ms"] for r in selected),
                completion_ms=statistics.mean(r["latency_ms"] for r in selected),tokens_per_s=tps,
                tpot_ms=statistics.mean(r["tpot_ms"] for r in selected) if gen>1 else None)
    for gen,c in meta["matrix"]:
        for mode in meta["modes"]:
            selected=[r for r in samples if (r["mode"],r["gen"],r["concurrency"])==(mode,gen,c)]
            quantile=lambda values,q:sorted(values)[math.ceil(len(values)*q)-1]
            print(json.dumps(dict(event="metric",mode=mode,gen=gen,concurrency=c,requests=len(selected),
                ttft_mean_ms=statistics.mean(r["ttft_ms"] for r in selected),
                ttft_p50_ms=quantile([r["ttft_ms"] for r in selected],.5),
                ttft_p99_ms=quantile([r["ttft_ms"] for r in selected],.99),
                tpot_mean_ms=statistics.mean(r["tpot_ms"] for r in selected) if gen>1 else None,
                completion_mean_ms=statistics.mean(r["latency_ms"] for r in selected),
                tokens_per_s=statistics.mean(summaries[pair,mode,gen,c]["tokens_per_s"] for pair in range(meta["repetitions"])))))
        comparisons=[("userspace","kernel","kernel")] if len(meta["modes"])==2 else ([
            ("separate-kernel","chained-kernel","dispatch"),
            ("separate-userspace","chained-userspace","dispatch"),
            ("chained-userspace","chained-kernel","kernel")] if meta.get("comparison")=="dispatch" else [
            ("serial-kernel","prefix-kernel","release"),
            ("serial-userspace","prefix-userspace","release"),
            ("prefix-userspace","prefix-kernel","kernel")] if meta.get("comparison")=="release" else [
            ("grouped-kernel","packed-kernel","packing"),
            ("grouped-userspace","packed-userspace","packing"),
            ("packed-userspace","packed-kernel","kernel")])
        for baseline,candidate,favors in comparisons:
            for metric in ("ttft_ms","completion_ms","tokens_per_s")+(("tpot_ms",) if gen>1 else ()):
                sign=1 if metric=="tokens_per_s" else -1
                differences=[sign*(summaries[pair,candidate,gen,c][metric]-summaries[pair,baseline,gen,c][metric])
                             for pair in range(meta["repetitions"])]
                mean=statistics.mean(differences);assert len(differences)==5
                margin=2.776445105*statistics.stdev(differences)/math.sqrt(5)
                print(json.dumps(dict(event="paired_difference_favoring_"+favors,baseline=baseline,candidate=candidate,
                    metric=metric,gen=gen,concurrency=c,differences=differences,mean=mean,nominal_t95=[mean-margin,mean+margin])))
if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument("path",type=Path);args=ap.parse_args();analyze(args.path)
