"""Fixed five-pair confirmation of the screen-selected cells."""
from pathlib import Path
import argparse,json,math,statistics
def effect(values):
    logs=[math.log(a/b) for a,b in values]
    center=statistics.mean(logs);margin=2.776445105*statistics.stdev(logs)/math.sqrt(5)
    return dict(geometric_ratio=math.exp(center),t95_ratio=[math.exp(center-margin),math.exp(center+margin)],
                pairs=values,scope="nominal paired log-ratio t95,df4; selected cells, no multiplicity guarantee")
def main(root):
    selection=json.loads((root/"confirmation_selection.json").read_text());result=[]
    for index,selected in enumerate(selection["selected"]):
        cells={}
        for pair in range(5):
            for mode in ["kernel","native"]:
                p=root/"confirmation"/("confirm_s%d_p%d_%s.metrics.json"%(index,pair,mode))
                m=json.loads(p.read_text())
                assert (m["operation"],m["repeat"],m["cores"],m["offered_rate"])==(selected["operation"],selected["repeat"],selected["cores"],selected["rate"])
                assert m["seed"]==420261017+index*100+pair and m["offered_seconds"]==20
                cells[pair,mode]=m
        summary={}
        for metric,getter in [
            ("group_cpu",lambda x:x["owned_group_cpu_ms_per_attempt"]),
            ("host_active_cpu",lambda x:x["host_active_cpu_ms_per_attempt"]),
            ("scheduled_p99",lambda x:(x["latency"]["scheduled_response_ms"] or {}).get("p99")),
            ("begin_p99",lambda x:(x["latency"]["begin_response_ms"] or {}).get("p99")),
            ("throughput",lambda x:x["throughput"]),
            ("timer_dispatch_p99",lambda x:(x["latency"]["timer_dispatch_lag_ms"] or {}).get("p99"))]:
            values=[(getter(cells[p,"kernel"]),getter(cells[p,"native"])) for p in range(5)]
            summary[metric]=effect(values) if all(a is not None and b is not None and a>0 and b>0 for a,b in values) else None
        failures=sum(x["failures"] for x in cells.values())
        valid=not failures and all(x["group_stable"] and x["service_affinity_verified"] for x in cells.values())
        valid=valid and all(x["latency"]["timer_dispatch_lag_ms"]["p99"]<=max(1,.1*x["latency"]["scheduled_response_ms"]["p99"]) for x in cells.values())
        present=all(summary[k] is not None for k in ["group_cpu","scheduled_p99","throughput"])
        throughput_ok=present and summary["throughput"]["t95_ratio"][0]>=.98
        cpu_win=valid and throughput_ok and summary["group_cpu"]["t95_ratio"][1]<.90 and summary["scheduled_p99"]["t95_ratio"][1]<=1.05
        tail_win=valid and throughput_ok and summary["scheduled_p99"]["t95_ratio"][1]<.90 and summary["group_cpu"]["t95_ratio"][1]<=1.05
        host_increase=summary["host_active_cpu"] is not None and summary["host_active_cpu"]["t95_ratio"][0]>1
        result.append(dict(selection=index,cell=selected,valid_confirmation=bool(valid),failures=failures,
            effects=summary,cpu_criterion_met=bool(cpu_win),tail_criterion_met=bool(tail_win),
            shared_host_significant_increase=host_increase,
            claim_limit="Host totals include foreign tenants; no exclusive total-cost attribution. Process-accounting benefit alone does not establish net CPU saved."))
    output=dict(event="confirmation",source=Path(__file__).read_text(),cells=result,
                any_prespecified_local_advantage=any(x["cpu_criterion_met"] or x["tail_criterion_met"] for x in result))
    (root/"confirmation_summary.json").write_text(json.dumps(output,indent=2));print(json.dumps(output))
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument("root",type=Path);main(ap.parse_args().root)
