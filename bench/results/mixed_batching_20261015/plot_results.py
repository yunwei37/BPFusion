from pathlib import Path
import json,statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
t=Path(__file__).resolve().parent
modes=["uring_loop_16_original","userspace_16_original","uring_loop_16_mixed","userspace_16_mixed"]
labels=["Kernel original","Native original","Kernel mixed","Native mixed"]
colors=["#9a6324","#66758c","#007b83","#a43f83"]
metrics=[("tpot_ms_mean","Mean request TPOT (ms)"),("output_tokens_per_s","Delivered output (token/s)"),("connect_ttft_ms_p99","TTFT P99 (ms)"),("connect_completion_ms_p99","Completion P99 (ms)"),("itl_ms_p99","Adjacent-token ITL P99 (ms)")]
data={}
fig,axes=plt.subplots(5,2,figsize=(12,16),layout="constrained")
for col,model in enumerate(["qwen","smol"]):
 rows=[json.loads(s) for s in (t/("full_"+model+".analysis.stdout")).read_text().splitlines()]
 data[model]=rows
 cells=[x for x in rows if x["event"]=="cell_metrics"]
 for row,(field,title) in enumerate(metrics):
  ax=axes[row,col]
  for j,(mode,label,color) in enumerate(zip(modes,labels,colors)):
   xs=[];ys=[]
   for rate in [96,192]:
    values=[x[field] for x in cells if x["mode"]==mode and x["rate"]==rate]
    x=[96,192].index(rate)+(j-1.5)*.1
    ax.scatter([x+(i-2)*.009 for i in range(5)],values,color=color,alpha=.45,s=15)
    xs.append(x);ys.append(statistics.mean(values))
   ax.plot(xs,ys,marker="o",color=color,label=label,linewidth=1)
  ax.set_xticks([0,1],["96 req/s","192 req/s"]);ax.set_ylabel(title);ax.grid(axis="y",alpha=.2)
  if row==0:ax.set_title("Qwen2.5-0.5B" if model=="qwen" else "SmolLM2-135M")
axes[0,0].legend(fontsize=8)
fig.suptitle("Packed mixed scheduling; all paths BF_TRACE, 16 banks\nDots: five blocks; lines: block means. No general eBPF superiority.",fontsize=12)
fig.savefig(t/"mixed_batching_results.png",dpi=160)
fig.savefig(t/"mixed_batching_results.pdf")
(t/"mixed_batching_results.data.json").write_text(json.dumps(data,indent=2))
