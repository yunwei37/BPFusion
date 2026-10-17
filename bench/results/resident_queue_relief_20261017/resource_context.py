from pathlib import Path
import json,gzip,sys,re
root=Path(sys.argv[1])
metrics=[json.loads(l) for l in (root/"analysis.stdout").read_text().splitlines()]
cells={(x["pair"],x["condition"]):x for x in metrics if x["event"]=="cell_metrics"}
assert len(cells)==15
def read(path):
 with gzip.open(path,"rt") if path.suffix==".gz" else path.open() as f:return [json.loads(x) for x in f]
def stat(text):return text.rsplit(") ",1)[1].split()
def cpu_stat_delta(first,last,tick):
 a,b=stat(first),stat(last)
 assert a[19]==b[19]
 return dict(user_s=(int(b[11])-int(a[11]))/tick,system_s=(int(b[12])-int(a[12]))/tick)
for p in sorted(root.glob("*_r192.resources.jsonl.gz")):
 match=re.search(r"_p([0-9]+)_(before|native|official)_r",p.name)
 pair,condition=int(match[1]),match[2];m=cells[pair,condition]
 rows=read(p);meta=rows[0];samples=[x for x in rows if x["event"]=="sample"];first,last=samples[0],samples[-1]
 assert "service_threads" in first and "service_threads" in last
 n=m["attempts"];tick=meta["clock_tick"];ga,gb=first["process_group"],last["process_group"]
 stable=ga.keys()==gb.keys() and all(stat(ga[k]["stat"])[19]==stat(gb[k]["stat"])[19] for k in ga)
 user=system=None
 if stable:
  values=[cpu_stat_delta(ga[k]["stat"],gb[k]["stat"],tick) for k in ga]
  user=sum(x["user_s"] for x in values)*1000/n;system=sum(x["system_s"] for x in values)*1000/n
 ta,tb=first["service_threads"],last["service_threads"];thread_rows=[]
 for tid in sorted(ta.keys()&tb.keys(),key=int):
  if stat(ta[tid]["stat"])[19]!=stat(tb[tid]["stat"])[19]:continue
  cpu=cpu_stat_delta(ta[tid]["stat"],tb[tid]["stat"],tick)
  sa,sb=[list(map(int,x[tid]["schedstat"].split())) for x in [ta,tb]]
  runtime=(sb[0]-sa[0]) if sa and sb else None
  wait=(sb[1]-sa[1]) if len(sa)>1 and len(sb)>1 else None
  thread_rows.append(dict(tid=tid,comm=tb[tid]["comm"].strip(),user_ms_per_attempt=cpu["user_s"]*1000/n,
    system_ms_per_attempt=cpu["system_s"]*1000/n,sched_runtime_ms_per_attempt=runtime/n/1e6 if runtime is not None else None,
    sched_runnable_wait_ms_per_attempt=wait/n/1e6 if wait is not None else None,
    note="stable primary-server thread only; runnable wait is not request latency"))
 io=[x for x in thread_rows if x["comm"].startswith(("iou-wrk","io-wq"))]
 host_softirq_ms=m["server_host_cpu_seconds_by_class"]["softirq"]*1000/n
 print(json.dumps(dict(event="resource_context",pair=pair,condition=condition,attempts=n,group_stable=stable,
   owned_group_cpu_ms_per_attempt=m["owned_group_cpu_ms_per_attempt"],owned_group_user_ms_per_attempt=user,
   owned_group_system_ms_per_attempt=system,clock_tick_Hz=tick,
   primary_thread_count_first=len(ta),primary_thread_count_last=len(tb),stable_primary_threads=thread_rows,
   observed_owned_iowq_threads=io,owned_iowq_scope="included in owned TGID/process CPU where charged; no visible thread is unknown, not zero",
   visible_kernel_workers_first=list(first.get("visible_kernel_workers",{})),
   visible_kernel_workers_last=list(last.get("visible_kernel_workers",{})),
   host_softirq_ms_per_attempt_unattributed=host_softirq_ms,
   gpu_energy_J_per_attempt=m["device_energy_J_per_attempt"],gpu_server_counters=m["server_counters"],
   client_peak_inflight=m["max_in_flight"],client_cpu_ms_per_attempt=m["client_cpu_ms_per_attempt"],
   scope="Posthoc resource ledger from fixed raw samples; group/system/thread subsets overlap and never sum with cgroup/host. IRQ/softirq/device are shared. Controller counters are work volume, not critical-path GPU time.")))
