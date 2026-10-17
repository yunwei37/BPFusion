"""Nested resource accounting from the original observation windows."""
from pathlib import Path
import gzip,json,sys
def lines(p):return [json.loads(x) for x in gzip.decompress(p.read_bytes()).splitlines()]
def fields(v):return v["stat"].rsplit(") ",1)[1].split()
def kv(text):return {k:int(v) for k,v in (x.split() for x in text.splitlines())}
def psi(text):
    return {x.split()[0]:int(next(y.split("=",1)[1] for y in x.split()[1:] if y.startswith("total="))) for x in text.splitlines()}
def cell(p):
    m=json.loads(p.read_text());prefix=p.with_name(p.name.removesuffix(".metrics.json"))
    rows=lines(Path(str(prefix)+".resources.jsonl.gz"));samples=[x for x in rows if x["event"]=="sample"]
    a,b=samples[0],samples[-1];tick=rows[0]["clock_tick"];attempts=m["attempts"]
    details=[x for x in samples if "service_threads" in x];ta,tb=details[0]["service_threads"],details[-1]["service_threads"]
    threads=[]
    for tid in sorted(set(ta)&set(tb),key=int):
        x,y=ta[tid],tb[tid];fa,fb=fields(x),fields(y)
        if fa[19]!=fb[19]:continue
        sa,sb=map(int,x["schedstat"].split()[0:2]),map(int,y["schedstat"].split()[0:2])
        sa,sb=list(sa),list(sb)
        threads.append(dict(tid=tid,name=y["stat"].split("(",1)[1].rsplit(")",1)[0],
            user_ms=(int(fb[11])-int(fa[11]))/tick*1000,
            system_ms=(int(fb[12])-int(fa[12]))/tick*1000,
            sched_runtime_ms=(sb[0]-sa[0])/1e6,sched_runqueue_wait_ms=(sb[1]-sa[1])/1e6))
    ca,cb=kv(a["cgroup"]["cpu.stat"]),kv(b["cgroup"]["cpu.stat"])
    cg={k:cb[k]-ca[k] for k in set(ca)&set(cb)}
    pa,pb=psi(a["host"]["pressure/cpu"]),psi(b["host"]["pressure/cpu"])
    tick_parts={}
    for label,index in [("user",11),("system",12)]:
        value=sum(int(fields(v)[index]) for v in b["process_group"].values())-sum(int(fields(v)[index]) for v in a["process_group"].values())
        tick_parts[label]=value/tick*1000/attempts
    intervals=[x for x in samples if not x["device"]]
    durations=[(x["sample_end_ns"]-x["sample_begin_ns"])/1e6 for x in intervals]
    detail_durations=[(x["sample_end_ns"]-x["sample_begin_ns"])/1e6 for x in intervals if "service_threads" in x]
    mask=m["sampled_affinity_masks"]
    gpu=[s["device"] for s in samples if s["device"]]
    return dict(tag=m["tag"],operation=m["operation"],repeat=m["repeat"],cores=m["cores"],mode=m["mode"],
      rate=m["offered_rate"],attempts=attempts,failures=m["failures"],
      owned_group_cpu_ms_per_attempt=m["owned_group_cpu_ms_per_attempt"],
      host_active_cpu_ms_per_attempt=m["host_active_cpu_ms_per_attempt"],
      host_classes_ms_per_attempt={k:v/attempts for k,v in m["host_cpu_ms_by_class"].items()},
      group_tick_cpu_ms_per_attempt=tick_parts,
      observer_interval_sample_duration_ms=dict(mean=sum(durations)/len(durations),max=max(durations),
        detail_max=max(detail_durations) if detail_durations else None,count=len(durations)),
      observer_cpu_ms_per_attempt=(b["observer_cpu_ns"]-a["observer_cpu_ns"])/1e6/attempts,
      sampled_masks=mask,observed_service_threads=threads,
      boundary_service_thread_changes=dict(first_only=sorted(set(ta)-set(tb)),last_only=sorted(set(tb)-set(ta))),
      cgroup_cpu_delta=cg,cgroup_cpu_max=b["cgroup"]["cpu.max"],cgroup_cpu_weight=b["cgroup"]["cpu.weight"],
      host_cpu_pressure_delta_us={k:pb[k]-pa[k] for k in pa},
      adjacent_idle_host_cpu_ms_per_s=m["idle_host_active_cpu_ms_per_s"],
      idle_context_host_delta_ms_per_attempt=m["idle_context_host_delta_ms_per_attempt"],
      boundary_gpu=gpu,interval_gpu_unknown=True,
      visible_kernel_workers_union=sorted({k for x in details for k in x["visible_kernel_workers"]}),
      window_seconds=m["observation_s"],
      scope="TGID exact CPU, sampled TIDs and cgroup/host are nested. TID tick counts miss short lifetimes. io-wq charged TGID may overlap. IRQ/softirq are whole host. Visible kernel workers incomplete; empty is unknown. Do not sum scopes.")
def main(a):
    out=dict(cells=[cell(p) for phase in ["client_dispatch_initial","screen","confirmation"] for p in sorted((a/phase).glob("*.metrics.json"))])
    (a/"resource_ledger.json").write_text(json.dumps(out,indent=2))
    print(json.dumps(dict(cells=len(out["cells"]),max_cgroup_throttled_us=max(x["cgroup_cpu_delta"].get("throttled_usec",0) for x in out["cells"]))))
if __name__=="__main__":main(Path(sys.argv[1]))
