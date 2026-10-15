#!/usr/bin/env python3
"""Recompute source-native offered-load outcomes and standard linear percentiles."""
import argparse,json,math,re,statistics
from pathlib import Path

def percentile(values,q):
    if not values:return None
    a=sorted(values);x=(len(a)-1)*q;i=math.floor(x);j=math.ceil(x)
    return a[i]+(a[j]-a[i])*(x-i)

def main(path):
    rows=[json.loads(s) for s in path.open()]
    meta=next(r for r in rows if r["event"]=="metadata")
    assert rows[-1]["event"]=="terminal" and rows[-1]["exit_code"]==0
    assert not any(r["event"] in ("failure","request_invalid") for r in rows)
    reps=1 if meta["preflight"] else 5
    count=16 if meta["preflight"] else 256
    matrix=[[64,4],[64,64]] if meta["preflight"] else [[64,4],[64,32],[64,64],[64,96]]
    assert not meta["correctness"] and meta["repetitions"]==reps
    assert meta["requests_per_cell"]==count and meta["matrix"]==matrix
    assert meta["modes"]==["uring_loop","userspace"]
    cells=[];total_attempts=total_success=total_tokens=0
    for pair in range(reps):
        order=meta["modes"] if pair%2==0 else meta["modes"][::-1]
        assert [r["mode"] for r in rows if r["event"]=="start" and r["pair"]==pair]==order
        for mode in meta["modes"]:
            selected=[r for r in rows if r.get("pair")==pair and r.get("mode")==mode]
            executor=next(r for r in selected if r["event"]=="executor")
            assert executor["exit_code"]==0
            log=executor["stdout"]
            assert "graph_error=0" in log and "launches=1 " in log and "trace_overflows=0" in log
            assert next(r for r in selected if r["event"]=="executor_terminal")["success"]
            prefix=path.with_suffix("").with_name(path.stem+f"_p{pair}_{mode}")
            refs=[json.loads(s) for s in Path(str(prefix)+".gpu.jsonl.references.jsonl").open()]
            events=[json.loads(s) for s in Path(str(prefix)+".gpu.jsonl").open()]
            assert events[-1]["event"]=="terminal" and events[-1]["overflows"]==0
            by_marker={r["client_ns"]:r for r in refs};assert len(by_marker)==len(refs)
            requests=[r for r in selected if r["event"]=="request"]
            errors=[r for r in selected if r["event"]=="request_error"]
            assert sum(r["kind"]=="warmup" for r in requests)==8
            seen=set()
            for row in requests+errors:
                marker=row.get("client_ns")
                if marker is not None:assert marker not in seen;seen.add(marker)
                ref=by_marker.pop(marker,None)
                if row["event"]=="request":
                    assert ref is not None and ref["prompt"]==row["input_ids"] and ref["gen"]==row["gen"]
                    assert not ref["bad"] and ref["tokens"]==row["tokens"]
                    assert len(row["tokens"])==row["gen"] and len(row["arrival_ns"])==row["gen"]
                    assert row["arrival_ns"]==sorted(row["arrival_ns"])
                    assert row["ttft_ms"]==(row["arrival_ns"][0]-row["start_ns"])/1e6
                    assert row["latency_ms"]==(row["arrival_ns"][-1]-row["start_ns"])/1e6
                elif ref is not None:
                    assert ref["prompt"]==row["input_ids"] and ref["gen"]==row["gen"] and not ref["bad"]
                    partial=row.get("tokens",[]);assert partial==ref["tokens"][:len(partial)]
                else:assert not row.get("tokens"),row
            assert not by_marker
            # Upstream replay exits within executor Python before its exit0 above.
            counters={k:int(v) for k,v in re.findall(r"(\w+)=(\d+)",log.split("resident vLLM stopped:",1)[1].splitlines()[0])}
            assert counters["admitted"]==counters["retired"]==len(refs)
            assert counters["graph_error"]==counters["trace_overflows"]==0
            if mode=="uring_loop":
                ring=json.loads(next(line[7:] for line in log.splitlines() if line.startswith("RESULT ")))
                assert ring["head"]==ring["completed"]==len(refs)
                assert ring["accepted"]==ring["closed"]
                assert all(ring[k]==0 for k in ("error","pending","reserved","dropped","overflow"))
                assert ring["sqhead"]==ring["sqtail"] and ring["cqhead"]==ring["cqtail"]
                stats=next(r for r in selected if r["event"]=="stats")
                assert stats["code"]==0 and "llm_reserved=0x0" in stats["stdout"]
                assert sorted(re.findall(r"llm\[(\d+)\]: state=(\d+)",stats["stdout"]))==[(str(i),"0") for i in range(8)]
            else:
                assert "idle=socket_or_deadline shutdown=eventfd" in log
                n=re.search(r"userspace TCP stopped: accepted=(\d+) published=(\d+) completed=(\d+) rejected=(\d+)",log)
                assert n and int(n[2])==int(n[3])==len(refs) and int(n[4])==0
            expected=matrix[pair%len(matrix):]+matrix[:pair%len(matrix)]
            actual=[r for r in selected if r["event"]=="cell"]
            assert [[r["gen"],r["rate"]] for r in actual]==expected
            for cell in actual:
                rate=cell["rate"];attempts=[r for r in requests+errors if r.get("rate")==rate]
                assert sorted(r["index"] for r in attempts)==list(range(count))
                schedule=next(r for r in selected if r["event"]=="arrival_schedule" and r["rate"]==rate)
                assert len(schedule["scheduled_ns"])==count
                assert schedule["scheduled_ns"]==sorted(schedule["scheduled_ns"])
                assert abs(schedule["scheduled_ns"][-1]-schedule["epoch_ns"]-int(count/rate*1e9))<=1
                same_schedule=next(r for r in rows if r["event"]=="arrival_schedule" and r["pair"]==pair and r["rate"]==rate)
                assert [n-schedule["epoch_ns"] for n in schedule["scheduled_ns"]]==[n-same_schedule["epoch_ns"] for n in same_schedule["scheduled_ns"]]
                good=[r for r in attempts if r["event"]=="request"];bad=[r for r in attempts if r["event"]=="request_error"]
                assert cell["requests"]==len(attempts)==count and cell["successful"]==len(good) and cell["failed"]==len(bad)
                assert cell["tokens"]==sum(len(r["tokens"]) for r in good)
                for row in attempts:
                    assert row["scheduled_ns"]==schedule["scheduled_ns"][row["index"]]
                    assert row["thread_start_ns"]>=row["scheduled_ns"]
                    assert row["connect_begin_ns"]>=row["thread_start_ns"] and row["finish_ns"]>=row["connect_begin_ns"]
                for row in good:
                    assert row["connect_end_ns"]>=row["connect_begin_ns"] and row["start_ns"]>=row["connect_end_ns"]
                    assert row["connect_ttft_ms"]==(row["arrival_ns"][0]-row["connect_begin_ns"])/1e6
                    assert row["connect_completion_ms"]==(row["arrival_ns"][-1]-row["connect_begin_ns"])/1e6
                    assert row["scheduled_ttft_ms"]==(row["arrival_ns"][0]-row["scheduled_ns"])/1e6
                    assert row["scheduled_completion_ms"]==(row["arrival_ns"][-1]-row["scheduled_ns"])/1e6
                    assert row["tpot_ms"]==(row["arrival_ns"][-1]-row["arrival_ns"][0])/63/1e6
                duration=(cell["end_ns"]-cell["begin_ns"])/1e9;assert duration>0
                assert cell["output_tokens_per_s"]==cell["tokens"]/duration
                result=dict(event="cell_metrics",pair=pair,mode=mode,rate=rate,attempts=count,
                            successes=len(good),failures=len(bad),request_throughput=len(good)/duration,
                            output_tokens_per_s=cell["tokens"]/duration,executor_cpu_ms_per_attempt=cell["executor_clock_cpu_ns"]/count/1e6,
                            max_in_flight=cell["max_in_flight"],duration_s=duration,
                            scheduling_lag_p99_ms=percentile([(r["thread_start_ns"]-r["scheduled_ns"])/1e6 for r in attempts],.99),
                            failure_types=[r["error_type"] for r in bad])
                for field in ("connect_ttft_ms","connect_completion_ms","scheduled_ttft_ms","scheduled_completion_ms","ttft_ms","latency_ms","tpot_ms"):
                    values=[r[field] for r in good]
                    for q in (.5,.95,.99):result[field+"_p"+str(int(q*100))]=percentile(values,q)
                    result[field+"_mean"]=statistics.mean(values) if values else None
                print(json.dumps(result));cells.append(result)
                total_attempts+=count;total_success+=len(good);total_tokens+=cell["tokens"]
    assert len(cells)==reps*2*len(matrix)
    print(json.dumps(dict(event="coverage",executors=reps*2,cells=len(cells),attempts=total_attempts,successes=total_success,
                          failures=total_attempts-total_success,successful_measured_tokens=total_tokens,warmups=reps*2*8)))
    for _,rate in matrix:
        a=[c for c in cells if c["mode"]=="uring_loop" and c["rate"]==rate]
        b=[c for c in cells if c["mode"]=="userspace" and c["rate"]==rate]
        for field in ("connect_ttft_ms_p99","connect_completion_ms_p99","scheduled_ttft_ms_p99","request_throughput","output_tokens_per_s","executor_cpu_ms_per_attempt"):
            effects=[x[field]-y[field] if x[field] is not None and y[field] is not None else None for x,y in zip(a,b)]
            valid=all(v is not None for v in effects)
            mean=statistics.mean(effects) if valid else None
            margin=2.776445105*statistics.stdev(effects)/math.sqrt(5) if valid and reps==5 else None
            censored=any(c["failures"] for c in a+b)
            print(json.dumps(dict(event="paired",rate=rate,metric=field,effects=effects,signed_mean=mean,
                                 signed_t95=[mean-margin,mean+margin] if margin is not None else None,
                                 failed_request_censoring=censored,primary=(rate==64 and field=="connect_ttft_ms_p99"))))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("path",type=Path);main(p.parse_args().path)
