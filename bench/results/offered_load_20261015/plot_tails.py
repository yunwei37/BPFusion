#!/usr/bin/env python3
"""Plot complete offered-load tail bounds and delivery failures, all attempts."""
import argparse,json,statistics
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main(directory):
    fig,axes=plt.subplots(2,2,figsize=(10,7),sharex="col",gridspec_kw={"height_ratios":[2,1]})
    colors={"uring_loop":"#bf3d35","userspace":"#2874a6"}
    labels={"uring_loop":"Kernel/eBPF","userspace":"Native TCP"}
    summary=[];largest_failure=0.0
    for col,(model,title) in enumerate((("qwen","Qwen2.5-0.5B"),("smol","SmolLM2-135M"))):
        source=directory/("full_"+model+".tail_bounds.stdout")
        records=[json.loads(line) for line in source.open()]
        cells=[r for r in records if r["event"]=="all_attempt_tail_bounds"]
        assert len(cells)==40
        top,bottom=axes[0,col],axes[1,col]
        top.set_title(title);top.set_yscale("log");top.set_ylim(.5,180000)
        for mode in colors:
            for rate in (4,32,64,96):
                selected=sorted((r for r in cells if r["mode"]==mode and r["rate"]==rate),key=lambda r:r["pair"])
                assert len(selected)==5
                failures=sum(r["failed"] for r in selected);attempts=sum(r["attempts"] for r in selected)
                lower=[];unbounded=[]
                for index,row in enumerate(selected):
                    bound=row["connect_ttft_ms_p99"]
                    value=bound["lower_ms"];unknown=bound["upper_unbounded"]
                    if not unknown:assert abs(value-bound["upper_ms"])<1e-9
                    offset=(index-2)*.6+(-.4 if mode=="uring_loop" else .4)
                    top.scatter(rate+offset,value,color=colors[mode],s=24,marker="^" if unknown else "o",alpha=.8)
                    lower.append(value);unbounded.append(unknown)
                percentage=failures/attempts*100;largest_failure=max(largest_failure,percentage)
                bottom.plot(rate,percentage,"o",color=colors[mode],markersize=5)
                if mode=="uring_loop":bottom.annotate(f"{percentage:.3g}%",(rate,percentage),xytext=(0,7),textcoords="offset points",ha="center",fontsize=8,color=colors[mode])
                summary.append(dict(model=model,mode=mode,rate=rate,attempts=attempts,failures=failures,
                                    p99_lower_ms=lower,p99_upper_unbounded=unbounded))
            bottom.plot([],[],color=colors[mode],marker="o",label=labels[mode])
        top.axhline(60000,color="#777777",linestyle=":",linewidth=.8)
        top.text(6,80000,"60 s socket timeout",fontsize=8,color="#555555")
        bottom.set_xlim(0,103);bottom.set_xticks([4,32,64,96])
        bottom.set_xlabel("Offered requests/s")
        for axis in (top,bottom):
            axis.grid(True,axis="y",alpha=.2)
            axis.spines[["top","right"]].set_visible(False)
        if col==0:
            top.set_ylabel("First-token P99 (ms, log scale)")
            bottom.set_ylabel("Failed attempts (%)")
        bottom.legend(frameon=False,fontsize=8,loc="upper left")
    for axis in axes[1]:axis.set_ylim(-1,max(5,largest_failure*1.2))
    fig.suptitle("All-attempt tail latency and delivery failures",fontsize=13)
    fig.text(.5,.015,"Five paired blocks/model; 256 attempts/cell; 64 output tokens. Each top point is one block.\n"
             "Triangles show a lower bound with unknown upper tail, not a completed latency. No performance win is established.",
             ha="center",fontsize=8)
    fig.tight_layout(rect=(0,.07,1,.95))
    fig.savefig(directory/"offered_load_tails.png",dpi=180)
    fig.savefig(directory/"offered_load_tails.pdf")
    (directory/"offered_load_tails.data.json").write_text(json.dumps(summary,indent=2))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("directory",type=Path)
    main(parser.parse_args().directory)
