#!/usr/bin/env python3
"""Descriptive period-weighted perf callchain summaries, not latency attribution."""
from pathlib import Path
import collections,gzip,json,re,sys
def text(p):return gzip.decompress(p.read_bytes()).decode() if p.suffix==".gz" else p.read_text()
def category(frames):
 names=[x[0] for x in frames]
 if not names or names[0]=="[unknown]":return "unknown_leaf"
 # An actual socket/network ancestor takes priority over its BPF-loop caller.
 network=("tcp_","__tcp_","ip_","__ip_","inet_","sock_","__sock","nft_","nf_","__nf_","br_","vxlan_","__dev_queue","netif_","__netif_")
 if any(n.startswith(network) or n in {"io_send","io_recv","io_accept","net_rx_action","handle_softirqs","__do_softirq","do_softirq.part.0","__napi_poll","process_backlog"} for n in names):return "socket_network_or_softirq"
 if any(n in {"__queue_map_get","queue_map_peek_elem","queue_map_pop_elem","queue_map_push_elem","array_map_lookup_elem","htab_map_lookup_elem"} or n.startswith("bpf_map_") for n in names):return "bpf_map_without_socket_ancestor"
 if any(n.startswith(("__schedule","finish_task_switch","schedule","try_to_wake_up","ttwu_")) for n in names):return "scheduler_without_socket_ancestor"
 if any(n in {"__io_run_loop","io_run_loop","io_cqring_wait"} or n.startswith(("bpf_prog_","__io_submit","io_submit","bpf_io_uring_")) for n in names):return "loop_coordination_other"
 return "other_kernel"
root=Path(sys.argv[1])
for f in sorted(root.glob("*.perf_script.txt*")):
 if f.name.endswith(".stderr"):continue
 raw=text(f);samples=[];selfs=collections.Counter();children=collections.Counter();counts=collections.Counter();weighted=collections.Counter()
 leaf_unknown=0;unknown_frame=0;kernel_depths=[];tids=set();periods=set()
 for block in raw.strip().split("\n\n"):
  lines=block.splitlines()
  if not lines:continue
  m=re.fullmatch(r"(.*?)\s+(\d+)/(\d+)\s+(\d+\.\d+):\s+(\d+) cpu-clock:k:\s*",lines[0])
  assert m,lines[0]
  period=int(m[5]);tids.add(int(m[3]));periods.add(period)
  frames=[]
  for l in lines[1:]:
   q=re.match(r"\s*([0-9a-f]+)\s+(.*?) \((.*?)\)\s*$",l);assert q,l
   # cpu-clock:k sampled IP is kernel; omit user ancestors in category/CPU table.
   if int(q[1],16)>=0xffff800000000000:frames.append((q[2],q[3]))
  assert frames,block
  cat=category(frames);counts[cat]+=1;weighted[cat]+=period
  selfs[frames[0]]+=period
  for frame in set(frames):children[frame]+=period
  leaf_unknown+=frames[0][0]=="[unknown]";unknown_frame+=any(x[0]=="[unknown]" for x in frames)
  kernel_depths.append(len(frames));samples.append(period)
 total=sum(samples)
 def symbols(c):return [dict(symbol=k[0],dso=k[1],period_ns=v,fraction=v/total) for k,v in c.most_common()]
 print(json.dumps(dict(file=f.name,samples=len(samples),period_ns_total=total,period_ns_values=sorted(periods),tids=sorted(tids),
   leaf_unknown_samples=leaf_unknown,any_kernel_unknown_frame_samples=unknown_frame,kernel_depth_min=min(kernel_depths),kernel_depth_max=max(kernel_depths),
   categories={k:dict(samples=counts[k],period_ns=v,fraction=v/total) for k,v in weighted.items()},
   self_symbols=symbols(selfs),inclusive_symbols=symbols(children),
   scope="Creator-TID on-CPU kernel samples only. Categories mutually exclusive by ancestor rule; inclusive symbols overlap. Network softirq can include unrelated packets. No latency, causality, total-service or observer-free gain inference.")))
