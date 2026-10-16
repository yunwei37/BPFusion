#!/usr/bin/env python3
"""CPU replay: client all-attempt tails and non-additive resource ledger."""
from pathlib import Path
import argparse,gzip,json,math,statistics,re
def rows(p):
 p=Path(p)
 if not p.exists():p=Path(str(p)+".gz")
 return [json.loads(x) for x in (gzip.open(p,"rt").read() if str(p).endswith(".gz") else p.read_text()).splitlines()]
def q(v,p):
 if not v:return None
 v=sorted(v);x=(len(v)-1)*p;a=int(x);b=math.ceil(x);return v[a]+(v[b]-v[a])*(x-a)
def kv(s):
 if not isinstance(s,str):return None
 return {line.split()[0]:int(line.split()[1]) for line in s.splitlines() if len(line.split())==2}
def main(args):
 root=Path(args.directory);out=[]
 files=sorted(set([p.with_suffix("") if p.suffix==".gz" else p for p in root.glob("*.client.jsonl*")]))
 for p in files:
  raw=rows(p);meta=raw[0];assert meta["event"]=="client_metadata"
  assert raw[-1]["event"]=="client_terminal" and raw[-1]["exit"]==0
  attempts=[x for x in raw if x["event"]=="request"]
  if not attempts:continue
  cell=next(x for x in raw if x["event"]=="cell");schedule=next(x for x in raw if x["event"]=="arrival_schedule")
  n=128 if args.preflight else meta["rate"]*60
  assert sorted(x["index"] for x in attempts)==list(range(n)) and cell["attempts"]==n
  good=[x for x in attempts if x["outcome"]=="success"];bad=[x for x in attempts if x["outcome"]!="success"]
  assert cell["successes"]==len(good) and cell["failures"]==len(bad)
  frozen=meta["config"];pool={(tuple(x["prompt"]),x["gen"]):x["sequences"] for x in frozen["frozen_model"]["references"]}
  for x in attempts:
   assert x["input_ids"]==frozen["prompts"][x["index"]%4] and x["gen"]==64
   assert x["scheduled_ns"]==schedule["scheduled_ns"][x["index"]]
   assert x["arrival_ns"]==sorted(x["arrival_ns"]) and len(x["arrival_ns"])==len(x["tokens"])
   if x["outcome"]!="success":continue
   assert len(x["tokens"])==64 and all(type(v)==int and 0<=v<frozen["frozen_model"]["vocab"] for v in x["tokens"])
   assert x["reference_set_match"]==(x["tokens"] in pool[tuple(x["input_ids"]),64])
  if meta.get("workers"):
   worker_count=meta["workers"]
   assert len(meta["worker_files"])==worker_count and len(cell["worker_cells"])==worker_count
   worker_raw=[rows(root/name) for name in meta["worker_files"]]
   assert all(w[-1]["event"]=="client_terminal" and w[-1]["exit"]==0 for w in worker_raw)
   joined=sorted([x for w in worker_raw for x in w if x["event"]=="request"],key=lambda x:x["index"])
   assert joined==sorted(attempts,key=lambda x:x["index"])
   worker_schedules=[next(x for x in w if x["event"]=="arrival_schedule") for w in worker_raw]
   assert all(x["mono_ns"]<cell["epoch_ns"] for x in worker_schedules)
   assert all({k:v for k,v in x.items() if k!="mono_ns"}=={k:v for k,v in schedule.items() if k!="mono_ns"} for x in worker_schedules)
   assert all([x["index"] for x in sorted([x for x in w if x["event"]=="request"],key=lambda x:x["index"])]==list(range(i,n,worker_count)) for i,w in enumerate(worker_raw))
   actual_cells=[next(x for x in w if x["event"]=="cell") for w in worker_raw]
   assert cell["worker_cells"]==actual_cells
   assert cell["child_cpu_ns"]==sum(c["client_process_cpu_ns"]-w[0]["process_cpu_ns"] for c,w in zip(actual_cells,worker_raw))
   assert cell["end_ns"]==max(x["closed_ns"] for x in attempts)
   assert cell["client_cpu_ns"]==cell["child_cpu_ns"]+cell["supervisor_cpu_ns"]
  sec=(cell["end_ns"]-cell["epoch_ns"])/1e9
  delivered=sum(len(x["tokens"]) for x in good);partial=sum(len(x["tokens"]) for x in bad)
  result=dict(event="cell_metrics",pair=meta["pair"],mode=meta["mode"],condition=re.search(r"_p[0-9]+_(candidate|native|official)_r",p.name).group(1),rate=meta["rate"],attempts=n,successes=len(good),failures=len(bad),
    failure_fraction=len(bad)/n,failure_censored=bool(bad),failure_types=[x.get("error_type") for x in bad],invalid_outcomes=sum(x.get("error_kind")=="protocol_or_validation" for x in bad),
    partial_tokens=partial,output_tokens=delivered,duration_s=sec,output_tokens_per_s=delivered/sec,all_observed_tokens_per_s=(delivered+partial)/sec,
    request_throughput=len(good)/sec,reference_set_matches=sum(x["reference_set_match"] for x in good),max_in_flight=cell["max_in_flight"],
    close_errors=sum("close_error" in x for x in attempts),client_cpu_ms_per_attempt=(cell["client_cpu_ns"] if "client_cpu_ns" in cell else cell["client_process_cpu_ns"]-meta["process_cpu_ns"])/n/1e6)
  gaps=[(b-a)/1e6 for x in good for a,b in zip(x["arrival_ns"],x["arrival_ns"][1:])]
  result["client_token_gap_zero_fraction"]=sum(x==0 for x in gaps)/len(gaps) if gaps else None
  metrics={
   "connect_completion_ms":[(x["arrival_ns"][-1]-x["connect_begin_ns"])/1e6 for x in good],
   "connect_ttft_ms":[(x["arrival_ns"][0]-x["connect_begin_ns"])/1e6 for x in good],
   "send_completion_ms":[(x["arrival_ns"][-1]-x["start_ns"])/1e6 for x in good] if meta["mode"]!="official" else [],
   "send_ttft_ms":[(x["arrival_ns"][0]-x["start_ns"])/1e6 for x in good] if meta["mode"]!="official" else [],
   "tpot_ms":[(x["arrival_ns"][-1]-x["arrival_ns"][0])/63/1e6 for x in good],
   "client_token_gap_ms":gaps,"positive_receive_gap_ms":[x for x in gaps if x>0],
   "client_scheduling_lag_ms":[(x["task_start_ns"]-x["scheduled_ns"])/1e6 for x in attempts],
   "scheduled_completion_ms":[(x["arrival_ns"][-1]-x["scheduled_ns"])/1e6 for x in good],
   "scheduled_ttft_ms":[(x["arrival_ns"][0]-x["scheduled_ns"])/1e6 for x in good]}
  for name,v in metrics.items():
   result[name+"_mean"]=statistics.mean(v) if v else None
   for fraction in [.5,.95,.99]:result[name+"_p"+str(int(fraction*100))]=q(v,fraction)
  base=str(p).removesuffix(".client.jsonl");obs=rows(base+".resources.jsonl")
  assert obs[-1]["event"]=="observer_terminal"
  samples=[x for x in obs if x["event"]=="sample"];first,last=samples[0],samples[-1]
  tick=obs[0]["clock_tick"]
  def ticks(x):return list(map(int,x["host"]["stat"].splitlines()[0].split()[1:]))
  a,b=ticks(first),ticks(last);delta=[v-u for u,v in zip(a,b)];assert min(delta)>=0
  result["server_host_active_cpu_s_per_attempt"]=sum(delta[i] for i in [0,1,2,5,6])/tick/n
  result["server_host_cpu_seconds_by_class"]={name:delta[i]/tick for i,name in enumerate(["user","nice","system","idle","iowait","irq","softirq","steal","guest","guest_nice"]) if i<len(delta)}
  aa,bb=first["process_group"],last["process_group"]
  stable=aa.keys()==bb.keys() and all(aa[k]["stat"].rsplit(") ",1)[1].split()[19]==bb[k]["stat"].rsplit(") ",1)[1].split()[19] for k in aa)
  result["service_group_stable"]=stable
  result["owned_group_cpu_ms_per_attempt"]=(sum(x["cpu_ns"] for x in bb.values())-sum(x["cpu_ns"] for x in aa.values()))/n/1e6 if stable else None
  ca,cb=kv(first["cgroup"]["cpu.stat"]),kv(last["cgroup"]["cpu.stat"])
  result["workspace_cgroup_cpu_ms_per_attempt"]=(cb["usage_usec"]-ca["usage_usec"])/n/1000 if ca and cb else None
  ea,eb=first["device"]["energy_mJ"],last["device"]["energy_mJ"]
  result["device_energy_J_per_attempt"]=(eb-ea)/1000/n if isinstance(ea,int) and isinstance(eb,int) and eb>=ea else None
  result["resource_bracket_s"]=(last["sample_end_ns"]-first["sample_begin_ns"])/1e9
  result["observer_cpu_ms_per_attempt"]=(last["observer_cpu_ns"]-first["observer_cpu_ns"])/n/1e6
  result["resource_samples"]=len(samples);result["device_app_sets"]=[x["device"]["compute_apps"] for x in samples]
  result["resource_scope"]="host/device and Workspace totals include other work; nested group/cgroup/host never summed. Remote control execution included in server bracket."
  server_base=str(p).split("_r192.client.jsonl")[0]
  terminal=json.loads(Path(server_base+".server_terminal.json").read_text())
  assert terminal.get("exit")==0 and not terminal.get("error") and not terminal.get("forced") and not terminal.get("pins"),terminal
  client_exit=json.loads(Path(base+".client_exit.json").read_text());assert client_exit["exit"]==0
  warm=rows(server_base+".warmup.jsonl")
  checked=[x for x in warm if x["event"]=="warmup"]
  assert warm[-1]["event"]=="client_terminal" and warm[-1]["exit"]==0
  assert len(checked)==8 and all(x["gen"]==1 and len(x["tokens"])==1 and x["outcome"]=="success" and x["reference_set_match"] for x in checked)
  counters={}
  if result["condition"]!="official":
   log=Path(server_base+".server.stdout").read_text()
   stopped=log.split("resident vLLM stopped:",1)[1].splitlines()[0]
   counters={k:int(v) for k,v in re.findall(r"(\w+)=(\d+)",stopped)}
   assert counters["graph_error"]==counters["trace_overflows"]==0
   if not bad:assert counters["admitted"]==counters["retired"]==len(good)+8
   if result["condition"]!="native":
    net=json.loads(next(x[7:] for x in log.splitlines() if x.startswith("RESULT ")))
    assert net["completed"]==net["head"] and net["accepted"]==net["closed"]
    if not bad:assert net["head"]==counters["admitted"]
    result["network_counters"]=net
    assert net["pending"]==net["error"]==net["reserved"]==net["dropped"]==net["overflow"]==0
    assert net["sqhead"]==net["sqtail"] and net["cqhead"]==net["cqtail"]
    assert terminal["detach"]["exit"]==0 and terminal["final_bpf_stats"]["exit"]==0
  else:
   assert not terminal.get("remaining_children")
   ready=json.loads(Path(server_base+".official_ready.json").read_text());assert ready==dict(missing=401,invalid=401)
  result["checked_excluded_warmups"]=len(checked)
  result["server_counters"]=counters
  print(json.dumps(result));out.append(result)
 if args.preflight:assert len(out)==3 and {x["condition"] for x in out}=={"candidate","native","official"}
 if not args.preflight:assert len(out)==15 and {(x["pair"],x["condition"],x["rate"]) for x in out}=={(p,m,192) for p in range(5) for m in ["candidate","native","official"]}
 for left,right in [("native","official"),("candidate","native"),("candidate","official")]:
  for metric in list(dict.fromkeys(["failure_fraction","connect_completion_ms_p99","server_host_active_cpu_s_per_attempt","owned_group_cpu_ms_per_attempt","workspace_cgroup_cpu_ms_per_attempt","device_energy_J_per_attempt","output_tokens_per_s","client_token_gap_ms_p99"]+[prefix+suffix for prefix in ["connect_ttft_ms","connect_completion_ms","tpot_ms","client_scheduling_lag_ms"] for suffix in ["_mean","_p50","_p95","_p99"]])):
   a=sorted([x for x in out if x["condition"]==left],key=lambda x:x["pair"])
   b=sorted([x for x in out if x["condition"]==right],key=lambda x:x["pair"])
   if not a or not b:continue
   assert [x["pair"] for x in a]==[x["pair"] for x in b]
   effects=[x[metric]-y[metric] if x[metric] is not None and y[metric] is not None else None for x,y in zip(a,b)]
   valid=bool(effects) and all(x is not None for x in effects);mean=statistics.mean(effects) if valid else None
   margin=2.776445105*statistics.stdev(effects)/math.sqrt(5) if valid and len(effects)==5 else None
   print(json.dumps(dict(event="paired",contrast=left+" minus "+right,rate=192,metric=metric,effects=effects,signed_mean=mean,signed_t95=[mean-margin,mean+margin] if margin is not None else None,
      primary=left=="native" and right=="official" and metric=="output_tokens_per_s",
      failure_censored=any(x["failure_censored"] for x in a+b),scope="five paired process blocks; conditional success tails, no equivalence or exclusive-host attribution")))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("directory");ap.add_argument("--preflight",action="store_true");main(ap.parse_args())
