#!/usr/bin/env python3
"""Failure-aware empirical completions; failed responses never become 60s samples."""
import argparse,gzip,json
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def read(p):
 with gzip.open(p,"rt") as f:
  for s in f:yield json.loads(s)
def main(args):
 root=Path(args.directory);groups=defaultdict(list)
 for p in sorted(root.glob("full_p*_*.client.jsonl.gz")):
  meta=None;done=[];fail=[];count=0
  for x in read(p):
   if x["event"]=="client_metadata":meta=x
   if x["event"]=="request":
    count+=1
    if x["outcome"]=="success":done.append((x["arrival_ns"][-1]-x["connect_begin_ns"])/1e9)
    else:fail.append((x["finish_ns"]-x["connect_begin_ns"])/1e9)
  groups[meta["rate"],meta["mode"]].append(dict(pair=meta["pair"],completed=done,failed=fail,attempts=count))
 assert all(len(groups[r,m])==5 for r in [96,192] for m in ["kernel","native"])
 colors={"kernel":"#2764a5","native":"#c76322"}
 fig,axes=plt.subplots(2,1,figsize=(8,7),constrained_layout=True)
 for ax,rate in zip(axes,[96,192]):
  xmax=0
  for mode in ["kernel","native"]:
   blocks=groups[rate,mode];total=sum(x["attempts"] for x in blocks);bad=sum(len(x["failed"]) for x in blocks)
   for b in blocks:
    a=np.sort(b["completed"]);ax.step(a,np.arange(1,len(a)+1)/b["attempts"]*100,where="post",color=colors[mode],alpha=.16,lw=.8)
    xmax=max(xmax,max(b["completed"]+b["failed"],default=0))
   a=np.sort([v for b in blocks for v in b["completed"]])
   ax.step(a,np.arange(1,len(a)+1)/total*100,where="post",color=colors[mode],lw=1.6,label=f"{mode}: {bad}/{total} failed")
   if len(a):ax.hlines(len(a)/total*100,a[-1],xmax,color=colors[mode],lw=1,linestyle=":")
  ax.set_xscale("log");ax.set_ylim(0,100);ax.set_title(f"Qwen2.5-0.5B, offered {rate} requests/s, five blocks")
  ax.set_xlabel("Connection-origin completion time (seconds)")
  ax.set_ylabel("% of all attempts completed");ax.grid(alpha=.18);ax.legend(loc="lower right")
 fig.suptitle("Sustained remote delivery: completion mass retains failures")
 fig.savefig(root/"completion_ecdf.png",dpi=180);fig.savefig(root/"completion_ecdf.pdf");plt.close(fig)
 metrics=[("owned_group_cpu_ms_per_attempt","Owned group CPU (ms/attempt)"),("server_host_active_cpu_s_per_attempt","Whole host active CPU (s/attempt)"),("device_energy_J_per_attempt","Whole device energy (J/attempt)")]
 analysis=[json.loads(s) for s in (root/"analysis.stdout").read_text().splitlines()]
 cells=[x for x in analysis if x["event"]=="cell_metrics"]
 fig,axes=plt.subplots(2,3,figsize=(12,6),constrained_layout=True)
 for row,rate in enumerate([96,192]):
  for col,(metric,label) in enumerate(metrics):
   ax=axes[row,col]
   for pair in range(5):
    values=[next(x[metric] for x in cells if x["pair"]==pair and x["mode"]==mode and x["rate"]==rate) for mode in ["kernel","native"]]
    if all(x is not None for x in values):ax.plot([0,1],values,"o-",color="#777777",alpha=.6,lw=.7,ms=3)
   ax.set_xticks([0,1],["kernel","native"]);ax.set_ylabel(label);ax.set_title(f"{rate}/s");ax.grid(axis="y",alpha=.18)
 fig.suptitle("Five paired blocks; group/host/device views are not additive")
 fig.savefig(root/"resource_pairs.png",dpi=180);fig.savefig(root/"resource_pairs.pdf");plt.close(fig)
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("directory");main(ap.parse_args())
