#!/usr/bin/env python3
"""Descriptive all-attempt tail bounds; does not replace the frozen primary analysis.

An attempt with no observed first token is right-censored at observation end.
Its eventual first-token time is unknown; a timeout is never assigned an exact
latency. Completion is censored unless all requested tokens were observed.
Bounds use the same ordinary linear quantile definition as the main analysis.
"""
import argparse,json,math,collections
from pathlib import Path

def percentile(values,q):
    a=sorted(values);position=(len(a)-1)*q
    lo=math.floor(position);hi=math.ceil(position)
    if lo==hi:return a[lo]
    if math.isinf(a[hi]):return math.inf
    return a[lo]+(a[hi]-a[lo])*(position-lo)

def main(path):
    rows=[json.loads(line) for line in path.open()]
    assert rows[-1]["event"]=="terminal" and rows[-1]["exit_code"]==0
    cells=[r for r in rows if r["event"]=="cell"]
    attempts=[r for r in rows if r["event"] in ("request","request_error") and "rate" in r]
    total=0
    for cell in cells:
        chosen=[r for r in attempts if all(r[k]==cell[k] for k in ("pair","mode","rate"))]
        assert len(chosen)==cell["requests"]
        assert sorted(r["index"] for r in chosen)==list(range(cell["requests"]))
        result=dict(event="all_attempt_tail_bounds",pair=cell["pair"],mode=cell["mode"],rate=cell["rate"],
                    attempts=len(chosen),successful=cell["successful"],failed=cell["failed"],
                    error_types=dict(collections.Counter(r["error_type"] for r in chosen if r["event"]=="request_error")))
        for name,full in (("connect_ttft_ms",False),("connect_completion_ms",True)):
            lower=[];upper=[];censored=[]
            for row in chosen:
                times=row.get("arrival_ns",[])
                observed=bool(times) and (not full or len(times)==row["gen"])
                if observed:
                    value=(times[-1 if full else 0]-row["connect_begin_ns"])/1e6
                    lower.append(value);upper.append(value)
                else:
                    bound=(row["finish_ns"]-row["connect_begin_ns"])/1e6
                    lower.append(bound);upper.append(math.inf);censored.append(bound)
            result[name+"_observed"]=len(chosen)-len(censored)
            result[name+"_censored"]=len(censored)
            result[name+"_min_censor_ms"]=min(censored,default=None)
            result[name+"_max_censor_ms"]=max(censored,default=None)
            for q in (.95,.99):
                high=percentile(upper,q)
                result[name+"_p"+str(int(q*100))]=dict(lower_ms=percentile(lower,q),
                                                      upper_ms=None if math.isinf(high) else high,
                                                      upper_unbounded=math.isinf(high))
        print(json.dumps(result))
        total+=len(chosen)
    assert total==len(attempts)
    print(json.dumps(dict(event="coverage",cells=len(cells),attempts=total,
                          scope="Descriptive finite-sample identification bounds, not CIs or a changed primary metric.")))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("path",type=Path)
    main(parser.parse_args().path)
