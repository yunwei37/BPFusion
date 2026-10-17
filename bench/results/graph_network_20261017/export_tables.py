"""Human-readable full tables; no new metric definition or sample selection."""
from pathlib import Path
import csv,json,sys
FIELDS=["tag","mode","operation","repeat","cores","offered_rate","seed","offered_seconds","duration_s",
"attempts","successes","failures","throughput","owned_group_cpu_ms_per_attempt","owned_group_cpu_ms_per_success",
"host_active_cpu_ms_per_attempt","idle_context_host_delta_ms_per_attempt","client_cpu_ms_per_attempt",
"observation_s","group_stable","service_affinity_verified","failure_aware_p99_ms",
"first_quarter_response_mean_ms","last_quarter_response_mean_ms"]
TAILS=["scheduled_response_ms","begin_response_ms","client_connection_wait_ms","timer_dispatch_lag_ms"]
STAT=["mean","p50","p90","p95","p99","p999","max"]
def main(a):
    for phase in ["client_dispatch_initial","screen","confirmation"]:
        rows=[]
        for p in sorted((a/phase).glob("*.metrics.json")):
            m=json.loads(p.read_text());row={k:m[k] for k in FIELDS}
            for tail in TAILS:
                for key in STAT:row[tail+"_"+key]=(m["latency"][tail] or {}).get(key)
            row["failure_types"]=json.dumps(m["failure_types"],sort_keys=True)
            row["sampled_affinity_masks"]=json.dumps(m["sampled_affinity_masks"])
            rows.append(row)
        if not rows:continue
        with (a/(phase+"_table.csv")).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
        print(phase,len(rows),sum(x["attempts"] for x in rows),sum(x["failures"] for x in rows))
if __name__=="__main__":main(Path(sys.argv[1]))
