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
  sec=(cell["end_ns"]-cell["epoch_ns"])/1e9
  delivered=sum(len(x["tokens"]) for x in good);partial=sum(len(x["tokens"]) for x in bad)
  result=dict(event="cell_metrics",pair=meta["pair"],mode=meta["mode"],condition=re.search(r"_p[0-9]+_(LI|NI|L|N)_r",p.name).group(1),rate=meta["rate"],attempts=n,successes=len(good),failures=len(bad),
    failure_fraction=len(bad)/n,failure_censored=bool(bad),failure_types=[x.get("error_type") for x in bad],invalid_outcomes=sum(x.get("error_kind")=="protocol_or_validation" for x in bad),
    partial_tokens=partial,output_tokens=delivered,duration_s=sec,output_tokens_per_s=delivered/sec,all_observed_tokens_per_s=(delivered+partial)/sec,
    request_throughput=len(good)/sec,reference_set_matches=sum(x["reference_set_match"] for x in good),max_in_flight=cell["max_in_flight"],
    close_errors=sum("close_error" in x for x in attempts),client_cpu_ms_per_attempt=(cell["client_process_cpu_ns"]-meta["process_cpu_ns"])/n/1e6)
  gaps=[(b-a)/1e6 for x in good for a,b in zip(x["arrival_ns"],x["arrival_ns"][1:])]
  result["client_token_gap_zero_fraction"]=sum(x==0 for x in gaps)/len(gaps) if gaps else None
  metrics={
   "connect_completion_ms":[(x["arrival_ns"][-1]-x["connect_begin_ns"])/1e6 for x in good],
   "connect_ttft_ms":[(x["arrival_ns"][0]-x["connect_begin_ns"])/1e6 for x in good],
   "send_completion_ms":[(x["arrival_ns"][-1]-x["start_ns"])/1e6 for x in good],
   "send_ttft_ms":[(x["arrival_ns"][0]-x["start_ns"])/1e6 for x in good],
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
  prefix=base.removesuffix("_r192");condition=result["condition"]
  receipt=json.loads(Path(prefix+".server_terminal.json").read_text())
  assert receipt.get("exit")==0 and not receipt.get("pins") and receipt["condition"]==condition
  text=Path(prefix+".server.stdout").read_text()
  stop=re.search(r"resident vLLM stopped: launches=1 device_graph_launches=(\d+) graph_error=(\d+) max_active=(\d+) admitted=(\d+) retired=(\d+) trace_overflows=(\d+) release_rounds=(\d+) max_release=(\d+) device_launch_calls=(\d+)",text)
  assert stop and all(int(stop.group(i))==0 for i in [2,6])
  assert int(stop.group(4))==int(stop.group(5))==n+8 and int(stop.group(9))==2*int(stop.group(1))
  result["device_graph_launches"]=int(stop.group(1));result["counters_include_warmups"]=True
  if condition in ["LI","NI"]:
   stage=[json.loads(x) for x in text.splitlines() if x.startswith('{"event":"controller_stage_time"')]
   assert len(stage)==1;stage=stage[0]
   assert stage["clock_bad"]==0 and stage["counts"][0]==stage["launches"]==result["device_graph_launches"]==sum(stage["input_histogram"].values())
   assert stage["outside_count"]==stage["launches"] and stage["counts"][2]==1
   assert all(x>=0 for row in stage["stage_ns"] for x in row)
   gpu=rows(prefix+".gpu.jsonl");assert gpu[-1]["event"]=="terminal" and gpu[-1]["overflows"]==0
   comp=[x for x in gpu if x["event"]=="compute"];ad=[x for x in gpu if x["event"]=="admission"];release=[x for x in gpu if x["event"]=="release"]
   assert len(comp)==stage["launches"] and len(ad)==n+8 and sorted(x["id"] for x in ad)==list(range(n+8))
   assert [rid for x in release for rid in x["request_ids"]]==list(range(n+8))
   hist={}
   for e in comp:hist[str(e["input_tokens"])]=hist.get(str(e["input_tokens"]),0)+1
   assert hist==stage["input_histogram"]
   ref=rows(prefix+".gpu.jsonl.references.jsonl")
   assert len(ref)==n+8
   refs={x["client_ns"]:x for x in ref};assert len(refs)==n+8
   warm=[x for x in rows(prefix+".warmup.jsonl") if x["event"]=="warmup"]
   assert len(warm)==8
   for client in attempts+warm:
    ref=refs[client["client_ns"]];assert ref["prompt"]==client["input_ids"] and ref["gen"]==client["gen"] and ref["tokens"]==client["tokens"] and not ref["bad"]
   fresh=rows(prefix+".gpu.jsonl.fresh_metadata.jsonl");assert fresh[-1]["event"]=="fresh_metadata_verified" and fresh[-1]["exact"]
   assert fresh[-1]["requests"]==n+8 and fresh[-1]["rounds"]==stage["launches"] and fresh[-1]["checked_tokens"]==n*64+8
   assert len(fresh)-1==stage["launches"]
   summaries=[json.loads(x) for x in text.splitlines() if x.startswith('{"event": "vllm_reference_replay"') or x.startswith('{"event": "fresh_metadata_verified"')]
   assert len(summaries)==2 and all(x["exact"] and x["requests"]==n+8 and x["checked_tokens"]==n*64+8 for x in summaries)
   result["controller_stages"]=stage
   result["controller_active_ns_per_round"]=sum(stage["stage_ns"][0])/stage["counts"][0]
   result["outside_ns_per_round"]=stage["outside_ns"]/stage["outside_count"]
   result["finite_dual_replay_tokens"]=n*64+8
   network=[json.loads(x) for x in text.splitlines() if x.startswith('{"event":"network_stage_time"')]
   if condition=="LI":
    assert len(network)==1 and all(x>0 for x in network[0]["counts"])
    assert all(x>=0 for row in network[0]["stage_ns"] for x in row)
    result["network_stages"]=network[0]
   else:assert not network
  print(json.dumps(result));out.append(result)
 if args.preflight:assert len(out)==4 and {(x["pair"],x["condition"],x["rate"]) for x in out}=={(0,m,192) for m in ["L","LI","N","NI"]}
 if not args.preflight:assert len(out)==20 and {(x["pair"],x["condition"],x["rate"]) for x in out}=={(p,m,192) for p in range(5) for m in ["L","LI","N","NI"]}
 for left,right in [("LI","NI"),("LI","L"),("NI","N"),("L","N")]:
  for metric in list(dict.fromkeys(["controller_active_ns_per_round","outside_ns_per_round","failure_fraction","connect_completion_ms_p99","server_host_active_cpu_s_per_attempt","owned_group_cpu_ms_per_attempt","workspace_cgroup_cpu_ms_per_attempt","device_energy_J_per_attempt","output_tokens_per_s","client_token_gap_ms_p99"]+[prefix+suffix for prefix in ["connect_ttft_ms","connect_completion_ms","tpot_ms","client_scheduling_lag_ms"] for suffix in ["_mean","_p50","_p95","_p99"]])):
   a=sorted([x for x in out if x["condition"]==left],key=lambda x:x["pair"])
   b=sorted([x for x in out if x["condition"]==right],key=lambda x:x["pair"])
   if not a or not b:continue
   assert [x["pair"] for x in a]==[x["pair"] for x in b]
   effects=[x.get(metric)-y.get(metric) if x.get(metric) is not None and y.get(metric) is not None else None for x,y in zip(a,b)]
   valid=bool(effects) and all(x is not None for x in effects);mean=statistics.mean(effects) if valid else None
   margin=2.776445105*statistics.stdev(effects)/math.sqrt(5) if valid and len(effects)==5 else None
   print(json.dumps(dict(event="paired",contrast=left+" minus "+right,rate=192,metric=metric,effects=effects,signed_mean=mean,signed_t95=[mean-margin,mean+margin] if margin is not None else None,
      primary=left=="LI" and right=="NI" and metric=="controller_active_ns_per_round",
      failure_censored=any(x["failure_censored"] for x in a+b),scope="five paired process blocks; conditional success tails, no equivalence or exclusive-host attribution")))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("directory");ap.add_argument("--preflight",action="store_true");main(ap.parse_args())
