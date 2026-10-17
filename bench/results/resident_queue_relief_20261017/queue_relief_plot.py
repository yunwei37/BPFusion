from pathlib import Path
import json,sys,statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
a=Path(sys.argv[1]);root=a/"queue_relief_full"
cells=[json.loads(l) for l in (root/"analysis.stdout").read_text().splitlines() if json.loads(l)["event"]=="cell_metrics"]
assert len(cells)==15
conditions=["before","native","official"];labels=["Resident16","Resident32","Official vLLM"]
colors=["#777777","#2067b2","#27865c"]
fig,axes=plt.subplots(2,2,figsize=(12.6,8.2),layout="constrained")
for ax,(metric,title) in zip([axes[0,0],axes[0,1],axes[1,1]],[("output_tokens_per_s","Delivered tokens/s"),("connect_completion_ms_p99","Client completion P99 (ms)"),("owned_group_cpu_ms_per_attempt","Owned group CPU (ms/attempt)")]):
 for block in range(5):
  ax.plot(range(3),[next(x[metric] for x in cells if x["pair"]==block and x["condition"]==c) for c in conditions],color="#aaaaaa",alpha=.5,linewidth=.8)
 for i,c in enumerate(conditions):
  values=[x[metric] for x in cells if x["condition"]==c];valid=[v for v in values if v is not None]
  ax.scatter([i]*len(valid),valid,color=colors[i],s=24)
  if valid:ax.plot([i-.13,i+.13],[statistics.mean(valid)]*2,color=colors[i],linewidth=3)
 ax.set_xticks(range(3),labels,rotation=15);ax.set_ylabel(title);ax.grid(axis="y",alpha=.2);ax.spines[["top","right"]].set_visible(False)
 if metric=="output_tokens_per_s":ax.axhline(192*64,color="#aa5555",linestyle=":",linewidth=1,label="Offered12288tokens/s");ax.legend(fontsize=8)
 if metric=="owned_group_cpu_ms_per_attempt":ax.set_ylim(bottom=0)
buckets=[json.loads(l) for l in (a/"full_queue_buckets.jsonl").read_text().splitlines()]
ax=axes[1,0];xs=[5,15,25,35,45,55]
for c,label,color in zip(conditions,labels,colors):
 for block in range(5):ax.plot(xs,[next(x["ttft_mean_ms"] for x in buckets if x["pair"]==block and x["condition"]==c and x["begin_s"]==begin) for begin in range(0,60,10)],color=color,alpha=.2,linewidth=.7)
 ax.plot(xs,[statistics.mean(x["ttft_mean_ms"] for x in buckets if x["condition"]==c and x["begin_s"]==begin) for begin in range(0,60,10)],color=color,label=label,linewidth=2)
ax.set_xlabel("Original arrival bucket midpoint (s)");ax.set_ylabel("Mean client TTFT (ms)");ax.grid(alpha=.2);ax.spines[["top","right"]].set_visible(False);ax.legend(fontsize=8)
fig.suptitle("Qwen FP16 / RTX 5090, remote192requests/s: shared capacity repair",fontsize=14)
fig.savefig(a/"queue_relief_comparison.png",dpi=160);fig.savefig(a/"queue_relief_comparison.pdf")
