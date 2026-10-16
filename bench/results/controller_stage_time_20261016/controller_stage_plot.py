from pathlib import Path
import json,sys,statistics
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);rows=[json.loads(x) for x in (root/"analysis.stdout").read_text().splitlines()]
cells=[x for x in rows if x["event"]=="cell_metrics"]
assert len(cells)==20 and {(x["pair"],x["condition"]) for x in cells}=={(i,c) for i in range(5) for c in ["L","LI","N","NI"]}
by={(x["pair"],x["condition"]):x for x in cells}
fig,axes=plt.subplots(2,2,figsize=(13.2,8.8),layout="constrained")
colors={"L":"#2166ac","LI":"#67a9cf","N":"#b35806","NI":"#f1a340"}
def paired(ax,conditions,metric,scale,label):
 for block in range(5):
  if len(conditions)==4:
   for left,right in [(0,1),(2,3)]:
    ax.plot([left,right],[by[block,conditions[i]][metric]*scale for i in [left,right]],color="#999999",alpha=.45,lw=.8,zorder=1)
  else:ax.plot(range(len(conditions)),[by[block,c][metric]*scale for c in conditions],color="#999999",alpha=.45,lw=.8,zorder=1)
 for i,c in enumerate(conditions):
  values=[by[block,c][metric]*scale for block in range(5)]
  ax.scatter([i]*5,values,color=colors[c],s=26,alpha=.9,zorder=2)
  mean=statistics.mean(values);ax.plot([i-.14,i+.14],[mean,mean],color=colors[c],lw=3,zorder=3)
 ax.set_xticks(range(len(conditions)),conditions);ax.set_ylabel(label)
 ax.grid(axis="y",alpha=.2);ax.spines[["top","right"]].set_visible(False)
paired(axes[0,0],["L","LI","N","NI"],"output_tokens_per_s",1,"Delivered output tokens/s")
axes[0,0].set_title("A  Ordinary and instrumented delivery",loc="left",fontsize=11)
paired(axes[0,1],["LI","NI"],"controller_active_ns_per_round",.001,"Observed dispatch brackets / launch (us)")
axes[0,1].set_title("B  Publication + packing + launch API",loc="left",fontsize=11)
paired(axes[1,0],["LI","NI"],"outside_ns_per_round",.001,"Outside-dispatch interval / launch (us)")
axes[1,0].set_title("C  Includes model/head, scheduling and return",loc="left",fontsize=11)
ax=axes[1,1];stages=["CQ","Claim","Reply","Connections","Timer/publish","Sleep"]
palette=["#4477aa","#66ccee","#228833","#ccbb44","#ee6677","#aa3377"]
bottom=[0.0]*5
for part,(label,color) in enumerate(zip(stages,palette)):
 values=[by[block,"LI"]["network_stages"]["stage_ns"][0][part]/by[block,"LI"]["network_stages"]["counts"][0]*.001 for block in range(5)]
 ax.bar(range(5),values,bottom=bottom,color=color,label=label,width=.68)
 bottom=[x+y for x,y in zip(bottom,values)]
ax.set_xticks(range(5),[f"Block {i}" for i in range(5)])
ax.set_ylabel("Observed network brackets / owned iteration (us)")
ax.set_title("D  Independent I/O CTA; concurrent with B/C",loc="left",fontsize=11)
ax.grid(axis="y",alpha=.2);ax.spines[["top","right"]].set_visible(False)
ax.legend(ncol=3,loc="upper center",bbox_to_anchor=(.5,-.11),frameon=False,fontsize=8)
fig.suptitle("Qwen, remote192/s: five matched process blocks\nL/N ordinary loop/native; LI/NI instrumented loop/native",fontsize=13)
fig.savefig(root/"controller_stage_comparison.png",dpi=160)
fig.savefig(root/"controller_stage_comparison.pdf")
