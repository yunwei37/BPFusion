from pathlib import Path
import json,sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
root=Path(sys.argv[1])
rows=[json.loads(l) for l in (root/"analysis.stdout").read_text().splitlines()]
cells=[x for x in rows if x["event"]=="cell_metrics"]
assert len(cells)==15 and all(len([x for x in cells if x["condition"]==c])==5 for c in ["candidate","native","official"])
conditions=["candidate","native","official"];labels=["BPF network","Native epoll","Official vLLM"]
colors=["#2067b2","#d67b2c","#27865c"]
fig,axes=plt.subplots(2,2,figsize=(12.6,8.2),layout="constrained")
panels=[("output_tokens_per_s","Delivered tokens/s"),("connect_completion_ms_p99","Client completion P99 (ms)"),("owned_group_cpu_ms_per_attempt","Owned group CPU (ms/attempt)"),("client_token_gap_ms_p99","Client receive-gap P99 (ms)")]
for ax,(metric,title) in zip(axes.flat,panels):
 for block in range(5):
  values=[next(x[metric] for x in cells if x["condition"]==c and x["pair"]==block) for c in conditions]
  ax.plot(range(3),values,color="#aaaaaa",alpha=.5,linewidth=.8,zorder=1)
 for index,c in enumerate(conditions):
  values=[x[metric] for x in sorted(cells,key=lambda q:q["pair"]) if x["condition"]==c]
  ax.scatter([index]*5,values,color=colors[index],s=24,alpha=.8,zorder=2)
  valid=[x for x in values if x is not None]
  if valid:ax.plot([index-.13,index+.13],[sum(valid)/len(valid)]*2,color=colors[index],linewidth=3,zorder=3)
  if len(valid)!=5:ax.text(index,.95,str(len(valid))+"/5 available",transform=ax.get_xaxis_transform(),ha="center",fontsize=8)
 ax.set_xticks(range(3),labels,rotation=15)
 ax.set_ylabel(title);ax.grid(axis="y",alpha=.2);ax.spines[["top","right"]].set_visible(False)
 if metric=="owned_group_cpu_ms_per_attempt":ax.set_ylim(bottom=0)
fig.suptitle("Qwen FP16 / RTX 5090, remote192 requests/s: five paired blocks",fontsize=15)
fig.savefig(root/"official_remote_comparison.png",dpi=160)
fig.savefig(root/"official_remote_comparison.pdf")
