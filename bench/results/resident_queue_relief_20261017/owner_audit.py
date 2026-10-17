"""Owner-only independent-code recomputation of the completed fixed matrix."""
from pathlib import Path
import argparse,gzip,json,math,re,statistics
def read(p):
 with gzip.open(p,"rt") if p.suffix==".gz" else p.open() as f:return [json.loads(l) for l in f]
def close(a,b):assert math.isclose(a,b,rel_tol=2e-12,abs_tol=2e-7),(a,b)
def main(root):
 rows=read(root/"analysis.stdout");cells={(x["pair"],x["condition"]):x for x in rows if x["event"]=="cell_metrics"}
 assert len(cells)==15
 expected_source=(root.parent/"official_remote_client.py").read_text()
 recomputed={};frame_count=0;total=0;resources=[];buckets=[]
 for p in sorted(root.glob("*.client.jsonl.gz")):
  pair,condition=re.search(r"_p([0-4])_(before|native|official)_r192",p.name).groups();pair=int(pair)
  data=read(p);meta=data[0];cell=next(x for x in data if x["event"]=="cell");schedule=next(x for x in data if x["event"]=="arrival_schedule")
  requests=[x for x in data if x["event"]=="request"];good=[x for x in requests if x["outcome"]=="success"]
  assert len(requests)==11520 and sorted(x["index"] for x in requests)==list(range(11520))
  assert meta["source"]==expected_source and len(meta["worker_metadata"])==4
  assert all(w["source"]==expected_source for w in meta["worker_metadata"])
  assert all(x["scheduled_ns"]==schedule["scheduled_ns"][x["index"]] for x in requests)
  assert cell["end_ns"]==max(x["closed_ns"] for x in requests)
  for x in good:
   assert x["input_ids"]==meta["config"]["prompts"][x["index"]%4]
   assert len(x["tokens"])==len(x["arrival_ns"])==64
   assert all(type(v)==int and 0<=v<meta["config"]["frozen_model"]["vocab"] for v in x["tokens"])
   if condition=="official":
    ids=[];times=[];prompt=None;finish=None
    for stamp,payload in x["frames"]:
     obj=json.loads(payload.encode("utf-8","surrogateescape"));frame_count+=1
     if "prompt_token_ids" in obj:prompt=obj["prompt_token_ids"]
     for choice in obj["choices"]:
      assert choice["index"]==0
      tok=choice.get("token_ids") or [];ids.extend(tok);times.extend([stamp]*len(tok))
      if choice.get("finish_reason") is not None:finish=choice["finish_reason"]
    assert ids==x["tokens"] and times==x["arrival_ns"] and prompt==x["input_ids"] and finish=="length"
  completion=[(x["arrival_ns"][-1]-x["connect_begin_ns"])/1e6 for x in good]
  ttft=[(x["arrival_ns"][0]-x["connect_begin_ns"])/1e6 for x in good]
  lag=[(x["task_start_ns"]-x["scheduled_ns"])/1e6 for x in requests]
  gap=[(b-a)/1e6 for x in good for a,b in zip(x["arrival_ns"],x["arrival_ns"][1:])]
  m=dict(output_tokens_per_s=sum(len(x["tokens"]) for x in good)/((max(x["closed_ns"] for x in requests)-cell["epoch_ns"])/1e9),
   connect_completion_ms_p99=statistics.quantiles(completion,n=100,method="inclusive")[98],
   connect_ttft_ms_p99=statistics.quantiles(ttft,n=100,method="inclusive")[98],
   client_scheduling_lag_ms_p99=statistics.quantiles(lag,n=100,method="inclusive")[98],
   client_token_gap_ms_p99=statistics.quantiles(gap,n=100,method="inclusive")[98])
  series={"connect_completion_ms":completion,"connect_ttft_ms":ttft,
   "client_scheduling_lag_ms":lag,
   "tpot_ms":[(x["arrival_ns"][-1]-x["arrival_ns"][0])/63/1e6 for x in good]}
  for key,values in series.items():
   m[key+"_mean"]=statistics.mean(values)
   percentiles=statistics.quantiles(values,n=100,method="inclusive")
   for percentile in [50,95,99]:m[key+"_p"+str(percentile)]=percentiles[percentile-1]
  m["failure_fraction"]=(len(requests)-len(good))/len(requests)
  total+=len(requests)
  for begin in range(0,60,10):
   selected=[x for x in good if begin<=(x["scheduled_ns"]-cell["epoch_ns"])/1e9<begin+10]
   buckets.append(dict(pair=pair,condition=condition,begin_s=begin,requests=len(selected),
    ttft_mean_ms=statistics.mean((x["arrival_ns"][0]-x["connect_begin_ns"])/1e6 for x in selected),
    generation_span_mean_ms=statistics.mean((x["arrival_ns"][-1]-x["arrival_ns"][0])/1e6 for x in selected)))
  obs=read(p.with_name(p.name.removesuffix(".client.jsonl.gz")+".resources.jsonl.gz"))
  samples=[x for x in obs if x["event"]=="sample"];first=samples[0]["process_group"]
  stable=all(set(x["process_group"])==set(first) and all(x["process_group"][pid]["stat"].rsplit(") ",1)[1].split()[19]==first[pid]["stat"].rsplit(") ",1)[1].split()[19] for pid in first) for x in samples)
  gpu_owned=all(all(str(app["pid"]) in x["process_group"] for app in x["device"]["compute_apps"]) for x in samples)
  first,last=samples[0],samples[-1];tick=obs[0]["clock_tick"];n=len(requests)
  ca=[int(v) for v in first["host"]["stat"].splitlines()[0].split()[1:]]
  cb=[int(v) for v in last["host"]["stat"].splitlines()[0].split()[1:]]
  m["server_host_active_cpu_s_per_attempt"]=sum(cb[i]-ca[i] for i in [0,1,2,5,6])/tick/n
  ga,gb=first["process_group"],last["process_group"]
  stable_ends=set(ga)==set(gb) and all(ga[pid]["stat"].rsplit(") ",1)[1].split()[19]==gb[pid]["stat"].rsplit(") ",1)[1].split()[19] for pid in ga)
  m["owned_group_cpu_ms_per_attempt"]=(sum(v["cpu_ns"] for v in gb.values())-sum(v["cpu_ns"] for v in ga.values()))/n/1e6 if stable_ends else None
  def usage(x):
   value=x["cgroup"]["cpu.stat"]
   return dict((line.split()[0],int(line.split()[1])) for line in value.splitlines()) if isinstance(value,str) else None
  aa,bb=usage(first),usage(last)
  m["workspace_cgroup_cpu_ms_per_attempt"]=(bb["usage_usec"]-aa["usage_usec"])/n/1000 if aa and bb else None
  ea,eb=first["device"]["energy_mJ"],last["device"]["energy_mJ"]
  m["device_energy_J_per_attempt"]=(eb-ea)/1000/n if isinstance(ea,int) and isinstance(eb,int) and eb>=ea else None
  for k,v in m.items():
   if v is None:assert cells[pair,condition][k] is None
   else:close(v,cells[pair,condition][k])
  recomputed[pair,condition]=m
  resources.append(dict(pair=pair,condition=condition,samples=len(samples),all_sample_group_stable=stable,all_sample_gpu_apps_owned=gpu_owned))
 assert set(recomputed)==set(cells)
 compared=0
 for x in rows:
  if x["event"]!="paired" or x["metric"] not in next(iter(recomputed.values())):continue
  left,right=x["contrast"].split(" minus ");metric=x["metric"]
  delta=[recomputed[p,left][metric]-recomputed[p,right][metric] if recomputed[p,left][metric] is not None and recomputed[p,right][metric] is not None else None for p in range(5)]
  if any(v is None for v in delta):
   assert x["signed_mean"] is None and x["signed_t95"] is None
   assert x["effects"]==delta
   compared+=1;continue
  mean=statistics.mean(delta);margin=2.776445105*statistics.stdev(delta)/math.sqrt(5)
  for aa,bb in zip(delta,x["effects"]):close(aa,bb)
  close(mean,x["signed_mean"]);close(mean-margin,x["signed_t95"][0]);close(mean+margin,x["signed_t95"][1]);compared+=1
 assert compared==69,compared
 (root.parent/"full_queue_buckets.jsonl").write_text("".join(json.dumps(x)+"\n" for x in buckets))
 (root.parent/"owner_audit_resources.jsonl").write_text("".join(json.dumps(x)+"\n" for x in resources))
 text=f"""# Owner-only result audit

This thread alone recomputed {total} attempts across15cells and decoded every
one of {frame_count} retained official SSEJSONdata payloads. No delegated/
independent-person review is claimed. Python statistics.quantiles(inclusive)
independently reproduces every paired metric's per-cell completion/TTFT/TPOT/
lag summaries and receivegapP99; original closed/epoch times reproduce throughput.
Resourceclock/cgroup/host/device deltas are separately rebuilt from raw samples.
All {compared} paired effects/nominalt95 intervals are recalculated from these
cell values. Missing metrics stay unavailable,never zero. The separate full
archive replay also preserves all acquisition-analysis rows byte-for-byte.

All raw indices/common schedules,4worker source snapshots,token counts/ranges,
official prompt/finish/token/arrival reconstruction and last-close denominator
pass. Observed protocol failures and finite-pool disagreement flags are not
deleted or used to redefine correctness. SSEdata payloads are retained,not
every wire byte/comment/DONEliteral. Correctness is finite,not universal parity.

All-sample stablegroup cases: {sum(x['all_sample_group_stable'] for x in resources)}/15.
All-sample GPUapp ownership cases: {sum(x['all_sample_gpu_apps_owned'] for x in resources)}/15.
Per-case observations are preserved in owner_audit_resources.jsonl. Nested
group/cgroup/host/thread/device views do not give exclusive total attribution.
This audit does not erase residualclientlag/protocol/scheduling differences
or make fixed-load delivery a maximumcapacity claim. Formal interpretation,
all adverse metrics,figure check and actualcleanup remain in result.md.
"""
 (root.parent/"owner-audit.md").write_text(text)
 print(text)
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("directory",type=Path);main(ap.parse_args().directory)
