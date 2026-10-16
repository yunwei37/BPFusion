#!/usr/bin/env python3
"""Secondary ledger: visible thread CPU lower bounds, idle and probe exposure."""
from pathlib import Path
import argparse,gzip,json
from collections import defaultdict
def load(p):return [json.loads(x) for x in (gzip.open(p,"rt").read() if str(p).endswith(".gz") else p.read_text()).splitlines()]
def main(root):
 for p in sorted(root.glob("*.resources.jsonl*")):
  rows=load(p);meta=rows[0];assert rows[-1]["event"]=="observer_terminal"
  ss=[x for x in rows if x["event"]=="sample"];a,b=ss[0],ss[-1];tick=meta["clock_tick"]
  duration=(b["sample_end_ns"]-a["sample_begin_ns"])/1e9
  per=defaultdict(list)
  for x in ss:
   for tid,v in x.get("service_threads",{}).items():per[tid].append((x["sample_begin_ns"],v))
  details=[];classes=defaultdict(lambda:dict(user_s=0,system_s=0,scheduler_runtime_s=0,threads=0))
  begin_ids=set(a.get("service_threads",{}));end_ids=set(b.get("service_threads",{}))
  for tid,values in per.items():
   first,last=values[0][1],values[-1][1];fa=first["stat"].rsplit(") ",1)[1].split();fb=last["stat"].rsplit(") ",1)[1].split()
   if fa[19]!=fb[19]:
    details.append(dict(tid=tid,unstable_starttime=True));continue
   user=(int(fb[11])-int(fa[11]))/tick;system=(int(fb[12])-int(fa[12]))/tick
   sched=(int(last["schedstat"].split()[0])-int(first["schedstat"].split()[0]))/1e9
   comm=last["comm"].strip();kind="creator" if int(tid)==meta["pid"] else "io_wq" if comm.startswith("iou-wrk") else "other_owned"
   cls=classes[kind];cls["user_s"]+=user;cls["system_s"]+=system;cls["scheduler_runtime_s"]+=sched;cls["threads"]+=1
   details.append(dict(tid=tid,comm=comm,kind=kind,user_s=user,system_s=system,scheduler_runtime_s=sched,at_begin=tid in begin_ids,at_end=tid in end_ids,samples=len(values),observed_span_s=(values[-1][0]-values[0][0])/1e9,
       tgid=next((s.split()[1] for s in last["status"].splitlines() if s.startswith("Tgid:")),None)))
  aa,bb=a["process_group"],b["process_group"];stable=aa.keys()==bb.keys() and all(aa[k]["stat"].rsplit(") ",1)[1].split()[19]==bb[k]["stat"].rsplit(") ",1)[1].split()[19] for k in aa)
  group=(sum(x["cpu_ns"] for x in bb.values())-sum(x["cpu_ns"] for x in aa.values()))/1e9 if stable else None
  ea,eb=a["device"]["energy_mJ"],b["device"]["energy_mJ"];energy=(eb-ea)/1000 if isinstance(ea,int) and isinstance(eb,int) and eb>=ea else None
  observer=(b["observer_cpu_ns"]-a["observer_cpu_ns"])/1e9
  cpu_a=list(map(int,a["host"]["stat"].splitlines()[0].split()[1:]));cpu_b=list(map(int,b["host"]["stat"].splitlines()[0].split()[1:]))
  active=sum(cpu_b[i]-cpu_a[i] for i in [0,1,2,5,6])/tick
  client=None;name=str(p).removesuffix(".gz").removesuffix(".resources.jsonl")
  client_path=Path(name+".client.jsonl.gz")
  if client_path.exists():
   cr=load(client_path);requests=[x for x in cr if x["event"]=="request"]
   successes=[x for x in requests if x["outcome"]=="success"];delivered=sum(len(x["tokens"]) for x in successes)
   client=dict(attempts=len(requests),successes=len(successes),failures=len(requests)-len(successes),delivered_success_tokens=delivered,
      total_group_cpu_s_per_success=group/len(successes) if group is not None and successes else None,
      total_group_cpu_ms_per_delivered_token=group*1000/delivered if group is not None and delivered else None,
      total_device_energy_J_per_success=energy/len(successes) if energy is not None and successes else None,
      total_device_energy_J_per_delivered_token=energy/delivered if energy is not None and delivered else None,
      scope="Total numerator retains failed-work/control/idle costs; dividing by successful outputs does not isolate only-success cost.")
  print(json.dumps(dict(client=client,file=p.name,duration_s=duration,group_cpu_s=group,group_cpu_s_per_s=group/duration if group is not None else None,host_active_cpu_s=active,
     device_energy_J=energy,device_mean_power_W=energy/duration if energy is not None else None,observer_cpu_s=observer,observer_cpu_s_per_s=observer/duration,
     classes=dict(classes),threads=details,interrupts_visible=bool(a["host"]["interrupts"].strip()) if isinstance(a["host"]["interrupts"],str) else False,
     scope="Visible thread tick/scheduler deltas are lower-bound detail, not additive to group/cgroup/host. A finite census can miss transient workers. IRQ attribution and shared device totals remain distinct.")))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("directory",type=Path);main(ap.parse_args().directory)
