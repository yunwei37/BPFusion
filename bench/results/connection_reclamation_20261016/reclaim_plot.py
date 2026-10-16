#!/usr/bin/env python3
from pathlib import Path
import argparse,gzip,json,collections
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ap=argparse.ArgumentParser();ap.add_argument("directory");args=ap.parse_args();root=Path(args.directory)
groups=collections.defaultdict(list)
for p in sorted(root.glob("*.client.jsonl.gz")):
 condition=p.name.split("_p",1)[1].split("_",1)[1].split("_r",1)[0]
 rows=[json.loads(x) for x in gzip.open(p,"rt")]
 requests=[x for x in rows if x["event"]=="request"]
 groups[condition].append(dict(n=len(requests),times=[(x["arrival_ns"][-1]-x["connect_begin_ns"])/1e9 for x in requests if x["outcome"]=="success"],failures=sum(x["outcome"]!="success" for x in requests)))
assert set(groups)=={"global","local","native"} and all(len(v)==5 for v in groups.values())
colors={"global":"#777777","local":"#2764a5","native":"#c76322"}
fig,ax=plt.subplots(figsize=(8,4.8),constrained_layout=True)
for condition,blocks in groups.items():
 for b in blocks:
  v=np.sort(b["times"]);ax.step(v,np.arange(1,len(v)+1)/b["n"]*100,where="post",color=colors[condition],alpha=.18,lw=.7)
 v=np.sort([x for b in blocks for x in b["times"]]);n=sum(b["n"] for b in blocks);bad=sum(b["failures"] for b in blocks)
 ax.step(v,np.arange(1,len(v)+1)/n*100,where="post",color=colors[condition],lw=1.6,label=f"{condition}: {bad}/{n} failed")
 ax.hlines(len(v)/n*100,v[-1],65,color=colors[condition],linestyle=":",lw=1)
ax.set_xscale("log");ax.set_ylim(0,100);ax.set_xlabel("Connection-origin completion time (seconds)")
ax.set_ylabel("% of all attempts completed");ax.set_title("Qwen192/s: global guard ablation, local guard, native")
ax.legend(loc="lower right");ax.grid(alpha=.18);fig.savefig(root/"completion_ecdf.png",dpi=180);fig.savefig(root/"completion_ecdf.pdf")
