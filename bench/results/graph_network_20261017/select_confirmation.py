"""Deterministic screen-only selection; never use confirmation outcomes to retune."""
from pathlib import Path
import argparse,datetime,json
def main(root):
    groups={}
    for p in (root/"screen").glob("*.metrics.json"):
        m=json.loads(p.read_text());key=(m["operation"],m["repeat"],m["cores"],m["offered_rate"])
        assert m["mode"] not in groups.setdefault(key,{})
        groups[key][m["mode"]]=m
    eligible=[];all_rows=[]
    for key,paths in sorted(groups.items()):
        reasons=[]
        if set(paths)!={"kernel","native"}:reasons.append("unmatched rate")
        for mode,m in paths.items():
            if m["failures"]:reasons.append(mode+" failures")
            if m["throughput"]<.98*m["offered_rate"]:reasons.append(mode+" attained<98%")
            if not m["group_stable"] or m["owned_group_cpu_ms_per_attempt"] is None:reasons.append(mode+" unstable group")
            if not m["service_affinity_verified"]:reasons.append(mode+" affinity not verified")
            tail=m["latency"]["scheduled_response_ms"];timer=m["latency"]["timer_dispatch_lag_ms"]
            if tail is None or timer is None:reasons.append(mode+" missing complete tail/monitor")
            elif timer["p99"]>max(1,.1*tail["p99"]):reasons.append(mode+" timer-dispatch lag")
            if m["owned_group_cpu_ms_per_attempt"] is not None and m["owned_group_cpu_ms_per_attempt"]<=0:
                reasons.append(mode+" nonpositive measured CPU")
        item=dict(operation=key[0],repeat=key[1],cores=key[2],rate=key[3],eligible=not reasons,reasons=reasons)
        if not reasons:
            k,n=paths["kernel"],paths["native"]
            item["cpu_ratio"]=k["owned_group_cpu_ms_per_attempt"]/n["owned_group_cpu_ms_per_attempt"]
            item["p99_ratio"]=k["latency"]["scheduled_response_ms"]["p99"]/n["latency"]["scheduled_response_ms"]["p99"]
            eligible.append(item)
        all_rows.append(item)
    assert groups,"no complete screening data"
    selected=[]
    if eligible:
        for label,cores,metric in [("unrestricted_cpu",0,"cpu_ratio"),("unrestricted_tail",0,"p99_ratio"),("one_cpu",1,"cpu_ratio")]:
            candidates=[x for x in eligible if x["cores"]==cores]
            if not candidates:continue
            best=min(candidates,key=lambda x:(x[metric],x["repeat"],x["operation"],x["rate"]))
            key=(best["operation"],best["repeat"],best["cores"],best["rate"])
            if key not in [(x["operation"],x["repeat"],x["cores"],x["rate"]) for x in selected]:
                selected.append(dict(best,selection=label))
    if not selected:
        selected=[dict(operation=op,repeat=1,cores=cores,rate=1000,selection="prespecified negative-boundary fallback")
                  for op,cores in [("matmul",0),("fft",0),("matmul",1)]]
    result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=Path(__file__).read_text(),
                candidate_cells=all_rows,selected=selected,confirmation_seconds=20,pairs=5,
                seed_rule="420261017+selection_index*100+pair; identical both paths; distinct from screening",
                order_rule="kernel,native for even(pair+selection_index), native,kernel otherwise")
    (root/"confirmation_selection.json").write_text(json.dumps(result,indent=2))
    print(json.dumps(result))
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);main(ap.parse_args().root)
