from pathlib import Path
import json,statistics,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).resolve().parent
models=[('qwen','Qwen2.5-0.5B'),('smol','SmolLM2-135M')]
paths=[('uring_loop','Kernel FIFO','#c43c39',-.2),('userspace','Native eligible FIFO','#176b9f',.2)]
panels=[(192,'output_tokens_per_s','Delivered output (token/s)'),(96,'connect_ttft_ms_p99','Connect-inclusive TTFT P99 (ms)')]
cells=[];paired=[];coverage=[];aggregates=[]
fig,axes=plt.subplots(2,2,figsize=(11.5,7.4),layout='constrained')
for col,(key,label) in enumerate(models):
 rows=[json.loads(s) for s in (r/('full_'+key+'.analysis.stdout')).read_text().splitlines()]
 cs=[dict(model=key,**x) for x in rows if x['event']=='cell_metrics'];assert len(cs)==40
 cells.extend(cs);paired.extend(dict(model=key,**x) for x in rows if x['event']=='paired')
 coverage.extend(dict(model=key,**x) for x in rows if x['event']=='coverage')
 axes[0,col].set_title(label)
 for prefix,name,color,offset in paths:
  for row,(rate,field,ylabel) in enumerate(panels):
   means=[]
   for banks in [8,16]:
    mode=prefix+'_'+str(banks)
    chosen=sorted([x for x in cs if x['mode']==mode and x['rate']==rate],key=lambda x:x['pair'])
    assert [x['pair'] for x in chosen]==list(range(5))
    values=[x[field] for x in chosen]
    present=[(i,y) for i,y in enumerate(values) if y is not None]
    mean=statistics.mean(values) if len(present)==5 else None
    means.append(mean if mean is not None else math.nan)
    aggregates.append(dict(model=key,mode=mode,rate=rate,metric=field,mean_block_statistic=mean,
     block_values=values,attempts=sum(x['attempts'] for x in chosen),failures=sum(x['failures'] for x in chosen)))
    axes[row,col].scatter([banks+offset+(i-2)*.055 for i,y in present],[y for i,y in present],s=22,color=color,alpha=.75,zorder=3)
   axes[row,col].plot([8+offset,16+offset],means,color=color,marker='D',markersize=5,linewidth=1.4,label=name,zorder=4)
 for row in range(2):
  ax=axes[row,col];ax.set_xticks([8,16]);ax.set_xlim(7,17)
  ax.set_xlabel('Configured model-bank capacity')
  ax.grid(axis='y',alpha=.22);ax.spines[['top','right']].set_visible(False)
  ax.text(.02,.97,'192 req/s: primary capacity contrast' if row==0 else '96 req/s: secondary tail',transform=ax.transAxes,va='top',fontsize=9)
 axes[1,col].set_yscale('log')
axes[0,0].set_ylabel(panels[0][2]);axes[1,0].set_ylabel(panels[1][2])
axes[0,0].legend(frameon=False,loc='lower right')
attempts=sum(x['attempts'] for x in coverage);successes=sum(x['successes'] for x in coverage)
fig.suptitle('Batch capacity and delivery: '+str(successes)+'/'+str(attempts)+' measured requests completed',fontsize=13)
caption='256 attempts/cell; 5 paired blocks; gen64. Points: blocks; diamonds: means of block statistics. Shared CPU host.'
caption+=chr(10)+'Tail quantiles condition on successful replies; all failures and paired intervals remain in the accompanying data/report.'
fig.supxlabel(caption,fontsize=8.5)
fig.savefig(r/'batch_capacity_results.png',dpi=170);fig.savefig(r/'batch_capacity_results.pdf')
(r/'batch_capacity_results.data.json').write_text(json.dumps(dict(scope='Complete finite shared-host collection. Primary per-model kernel16-kernel8 deliveredTPS192/s;96/s TTFTP99 secondary. Means of block quantiles are not pooled quantiles. All failure denominators and paired effects retained.',cells=cells,paired=paired,coverage=coverage,plotted_aggregates=aggregates),indent=2))
print(json.dumps(dict(cells=len(cells),paired=len(paired),coverage=len(coverage),plotted_aggregates=len(aggregates),attempts=attempts,successes=successes)))
