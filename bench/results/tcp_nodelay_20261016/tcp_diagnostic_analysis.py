#!/usr/bin/env python3
"""CPU-only own-socket/packet diagnostic; sampled holds are lower bounds."""
import argparse,gzip,json,math,statistics
from collections import defaultdict,Counter
from pathlib import Path
def lines(p):return gzip.open(p,"rt").read().splitlines() if str(p).endswith(".gz") else p.read_text().splitlines()
def q(v,p):
 if not v:return None
 v=sorted(v);a=(len(v)-1)*p;i=int(a);j=math.ceil(a);return v[i]+(v[j]-v[i])*(a-i)
def analyze(root):
 for p in sorted(root.glob("*.tcp.jsonl*")):
  rows=[json.loads(s) for s in lines(p)];assert rows[-1]["event"]=="observer_terminal"
  errors=[x for x in rows if x["event"].endswith("error")]
  sockets={x["fd"]:x for x in rows if x["event"]=="socket"}
  info=defaultdict(list);packets=[]
  for x in rows:
   if x["event"]=="tcp_info":info[x["fd"]].append(x)
   if x["event"]=="packet":packets.append(x)
  types=Counter(x["pkttype"] for x in packets)
  # lo IPv4 captures have only PACKET_HOST in this actual setup. If additional
  # packet types occur, keep raw but select one HOST delivery to avoid double count.
  selected=[x for x in packets if x["pkttype"]==0]
  flows=defaultdict(list)
  for x in selected:
   peer=x["dport"] if x["sport"]==39403 else x["sport"];flows[peer].append(x)
  holds=[];queued=0;steps=[]
  for fd,vals in info.items():
   start=last=sent=None
   for x in vals:
    if last is not None:steps.append((x["mono_ns"]-last["mono_ns"])/1e6)
    good=(x.get("notsent") or 0)>0 and (x.get("unacked") or 0)>0
    if good:
     queued+=1
     if start is None or sent!=x["bytes_sent"]:
      if start is not None:holds.append(dict(fd=fd,begin=start,end=last,lower_bound_ms=(last["mono_ns"]-start["mono_ns"])/1e6))
      start=x;sent=x["bytes_sent"]
     last=x
    elif start is not None:
     holds.append(dict(fd=fd,begin=start,end=last,lower_bound_ms=(last["mono_ns"]-start["mono_ns"])/1e6));start=last=sent=None
   if start is not None:holds.append(dict(fd=fd,begin=start,end=last,lower_bound_ms=(last["mono_ns"]-start["mono_ns"])/1e6))
  ack_delays=[];releases=[];episodes=[]
  for peer,ps in flows.items():
   ps.sort(key=lambda x:x["kernel_realtime_ns"])
   for i,x in enumerate(ps):
    if x["sport"]!=39403 or x["payload_len"]<=0:continue
    end=(x["seq"]+x["payload_len"])&0xffffffff
    follow=ps[i+1:]
    ack=next((v for v in follow if v["dport"]==39403 and v["flags"]&16 and ((v["ack"]-end)&0xffffffff)<0x80000000),None)
    if ack is None:continue
    send=next((v for v in follow if v["sport"]==39403 and v["payload_len"]>0),None)
    if send is not None and send["kernel_realtime_ns"]<ack["kernel_realtime_ns"]:continue
    delay=(ack["kernel_realtime_ns"]-x["kernel_realtime_ns"])/1e6;ack_delays.append(delay)
    release=(send["kernel_realtime_ns"]-ack["kernel_realtime_ns"])/1e3 if send is not None else None
    if release is not None:releases.append(release)
    episodes.append(dict(peer=peer,send=x,ack=ack,next_send=send,ack_delay_ms=delay,ack_to_next_send_us=release))
  longest=max(holds,key=lambda x:x["lower_bound_ms"]) if holds else None
  # Concrete longest hold includes packet neighborhood by userspace receive time.
  # Receive-time bounds may be delayed; kernel realtime gaps stay a separate clock.
  example=None
  if longest:
   fd=longest["fd"];peer=sockets[fd]["peer"][1]
   neighborhood=[x for x in flows[peer] if longest["begin"]["mono_ns"]-5000000<=x["seen_ns"]<=longest["end"]["mono_ns"]+8000000]
   example=dict(socket=sockets[fd],hold=longest,packets=neighborhood)
  out=dict(file=p.name,errors=errors,sockets=len(sockets),accepted_nodelay=sorted(set(x["nodelay"] for x in sockets.values() if x["peer"])),
    accepted_cork=sorted(set(x["cork"] for x in sockets.values() if x["peer"])),packets=len(packets),packet_types=dict(types),capture_terminal=rows[-1],
    info_samples=sum(map(len,info.values())),queued_and_unacked_samples=queued,holds=len(holds),
    hold_lower_bound_ms={"p50":q([x["lower_bound_ms"] for x in holds],.5),"p99":q([x["lower_bound_ms"] for x in holds],.99),"max":max((x["lower_bound_ms"] for x in holds),default=None)},
    no_intervening_server_data_ack_delay_ms={"count":len(ack_delays),"p50":q(ack_delays,.5),"p99":q(ack_delays,.99),"max":max(ack_delays,default=None)},
    longest_queued_example=example,
    scope="Diagnostic observation perturbs workload; sampled constant-bytes_sent holds lower-bound queued-data waiting. Packet kernel realtime and TCP_INFO userspace monotonic are distinct clocks; do not claim exact cross-clock stage sums.")
  print(json.dumps(out))
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("directory",type=Path);analyze(ap.parse_args().directory)
