"""Static research figures from retained metrics and full successful tails."""
from pathlib import Path
import gzip,json,sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
K="#b24a35";N="#27658c"
def save(a,name,fig):
    fig.savefig(a/(name+".png"),dpi=160);fig.savefig(a/(name+".pdf"));plt.close(fig)
def main(a):
    rows=[json.loads(x.read_text()) for x in sorted((a/"screen").glob("*.metrics.json"))]
    config=[(1,0),(16,0),(256,0),(1,1),(1,2)]
    for op in ["matmul","fft"]:
        fig,axes=plt.subplots(5,3,figsize=(12,17),layout="constrained")
        for i,(repeat,cores) in enumerate(config):
            for mode,color in [("kernel",K),("native",N)]:
                data=sorted([x for x in rows if x["operation"]==op and x["repeat"]==repeat and x["cores"]==cores and x["mode"]==mode],key=lambda x:x["offered_rate"])
                for j,getter in enumerate([lambda x:x["owned_group_cpu_ms_per_attempt"]*1000,lambda x:(x["latency"]["scheduled_response_ms"] or {}).get("p99",np.nan),lambda x:x["throughput"]]):
                    ax=axes[i,j];ax.plot([x["offered_rate"] for x in data],[getter(x) for x in data],color=color,marker="o",label=mode)
                    ax.set_xscale("log");ax.set_yscale("log");ax.grid(True,alpha=.2);ax.set_xlabel("Offered requests/s")
            axes[i,0].set_ylabel("Group CPU / attempt (us)")
            axes[i,1].set_ylabel("Scheduled-response P99 (ms)")
            axes[i,2].set_ylabel("Delivered requests/s")
            rates=sorted({x["offered_rate"] for x in rows if x["operation"]==op and x["repeat"]==repeat and x["cores"]==cores})
            axes[i,2].plot(rates,rates,":",color="0.5",label="offered")
            for ax in axes[i]:ax.set_title("repetitions %d; service CPUs %s"%(repeat,cores or "unrestricted"))
        axes[0,0].legend();axes[0,2].legend()
        fig.suptitle(op+": exploratory single-cell screening; CPU is group accounting\nSame 8-slot GPU executor; remote g10 client; shared lab host; all failures retained")
        save(a,"screen_"+op,fig)
    summary=json.loads((a/"confirmation_summary.json").read_text());count=len(summary["cells"])
    fig,axes=plt.subplots(2,count,figsize=(5*count,8),squeeze=False,layout="constrained")
    for index,item in enumerate(summary["cells"]):
        c=item["cell"];ax=axes[0,index]
        for mode,color in [("kernel",K),("native",N)]:
            pool=[];failed=0
            for pair in range(5):
                p=a/"confirmation"/("confirm_s%d_p%d_%s.latency_ecdf.json.gz"%(index,pair,mode))
                obj=json.loads(gzip.decompress(p.read_bytes()));v=np.asarray(obj["scheduled_response_ms"])
                pool.append(v);failed+=obj["failures"]
                if len(v):
                    y=1-np.arange(1,len(v)+1)/len(v);ax.plot(v[y>0],y[y>0],color=color,alpha=.17,lw=.5)
            v=np.sort(np.concatenate(pool));y=1-np.arange(1,len(v)+1)/len(v)
            ax.plot(v[y>0],y[y>0],color=color,label=mode+"; failures "+str(failed))
        ax.set_xscale("log");ax.set_yscale("log");ax.set_xlabel("Scheduled-response latency (ms)")
        ax.set_ylabel("P(successful latency > x)");ax.grid(True,alpha=.2);ax.legend(fontsize=8)
        ax.set_title("%s repeat%d CPU%s @ %d/s"%(c["operation"],c["repeat"],c["cores"] or "all",c["rate"]))
        ax=axes[1,index]
        for pos,(metric,label) in enumerate([("group_cpu","group CPU"),("scheduled_p99","P99"),("throughput","throughput"),("host_active_cpu","shared-host CPU")]):
            effect=item["effects"][metric]
            if effect is None:continue
            v=effect["geometric_ratio"];lo,hi=effect["t95_ratio"]
            ax.errorbar(v,pos,xerr=[[v-lo],[hi-v]],fmt="o",capsize=4,color="0.15")
        ax.set_yticks(range(4),["group CPU","P99","throughput","shared-host CPU"])
        ax.set_xscale("log");ax.axvline(1,color="0.5")
        ax.set_xlabel("Kernel / native ratio; nominal paired t95, df4");ax.grid(True,axis="x",alpha=.2)
        bounds=ax.get_xlim();ticks=[v for v in [.25,.5,1,2,4,8] if bounds[0]<=v<=bounds[1]]
        ax.set_xticks(ticks,[format(v,"g") for v in ticks]);ax.minorticks_off()
    fig.suptitle("New-seed five-pair confirmation; thin curves = individual cells\nSuccess-conditional tails; counts include every scheduled attempt; no multiplicity guarantee")
    save(a,"confirmation",fig)
    print(json.dumps(dict(matplotlib=matplotlib.__version__,numpy=np.__version__,figures=["screen_matmul","screen_fft","confirmation"])))
if __name__=="__main__":main(Path(sys.argv[1]))
