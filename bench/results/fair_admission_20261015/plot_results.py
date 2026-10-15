import pathlib,json,statistics,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=pathlib.Path(__file__).resolve().parent
models=[('qwen','Qwen2.5-0.5B'),('smol','SmolLM2-135M')]
modes=[('uring_loop','Kernel FIFO','#c43c39',-2),('userspace','Native eligible FIFO','#176b9f',2)]
rates=[64,96];allcells=[];allpaired=[];coverages=[];aggregates=[]
metrics=['connect_ttft_ms_p99','connect_ttft_ms_p50']
fig,axes=plt.subplots(2,2,figsize=(11.5,7.4),sharex='col',layout='constrained')
for col,(key,label) in enumerate(models):
 rows=[json.loads(x) for x in (r/('full_'+key+'.analysis.stdout')).read_text().splitlines()]
 cells=[dict(model=key,**x) for x in rows if x['event']=='cell_metrics']
 assert len(cells)==20
 allcells.extend(cells);allpaired.extend(dict(model=key,**x) for x in rows if x['event']=='paired')
 coverages.extend(dict(model=key,**x) for x in rows if x['event']=='coverage')
 axes[0,col].set_title(label)
 for mode,name,color,offset in modes:
  values={metric:[] for metric in metrics}
  for rate in rates:
   selected=sorted([x for x in cells if x['mode']==mode and x['rate']==rate],key=lambda x:x['pair'])
   assert [x['pair'] for x in selected]==list(range(5))
   means={metric:statistics.mean(x[metric] for x in selected) if all(isinstance(x[metric],(int,float)) for x in selected) else None for metric in selected[0] if metric not in ['pair','rate','model','mode','event','failure_types']}
   aggregates.append(dict(model=key,mode=mode,rate=rate,attempts=sum(x['attempts'] for x in selected),failures=sum(x['failures'] for x in selected),block_means=means))
   for row,metric in enumerate(metrics):
    ys=[x[metric] for x in selected];present=[(i,y) for i,y in enumerate(ys) if y is not None]
    values[metric].append(statistics.mean(ys) if len(present)==5 else math.nan)
    axes[row,col].scatter([rate+offset+(i-2)*.4 for i,y in present],[y for i,y in present],s=20,color=color,alpha=.75,zorder=3)
  for row,metric in enumerate(metrics):
   axes[row,col].plot([x+offset for x in rates],values[metric],color=color,marker='D',markersize=5,linewidth=1.4,label=name,zorder=4)
 for row in range(2):
  ax=axes[row,col];ax.axvspan(90,102,color='#888888',alpha=.08,zorder=0)
  ax.set_xlim(57,103);ax.set_xticks(rates);ax.set_yscale('log')
  ax.grid(axis='y',alpha=.22);ax.spines[['top','right']].set_visible(False)
 axes[1,col].set_xlabel('Configured request rate (requests/s)')
axes[0,0].set_ylabel('Connect-inclusive TTFT P99 (ms)')
axes[1,0].set_ylabel('Connect-inclusive TTFT P50 (ms)')
axes[0,0].legend(frameon=False)
attempts=sum(x['attempts'] for x in coverages);successes=sum(x['successes'] for x in coverages)
fig.suptitle('Fair admission: '+str(successes)+'/'+str(attempts)+' measured requests completed',fontsize=13)
caption='256 attempts/cell; 5 paired blocks. Points: blocks; diamonds: means of block quantiles. Shared CPU host; shaded96/s is primary.'
caption+=chr(10)+'Quantiles use observed successful requests; failed-attempt counts are retained in the accompanying data.'
fig.supxlabel(caption,fontsize=8.5)
fig.savefig(r/'fair_admission_results.png',dpi=170)
fig.savefig(r/'fair_admission_results.pdf')
(r/'fair_admission_results.data.json').write_text(json.dumps(dict(scope='Complete finite shared-host collection; means of block statistics, not pooled percentiles. New fixed primary96/s;64/s secondary. Failed attempts stay in counts; failed-request censoring remains in paired analysis.',cells=allcells,paired=allpaired,coverage=coverages,aggregates=aggregates),indent=2))
print(json.dumps(dict(cells=len(allcells),paired=len(allpaired),aggregates=len(aggregates),measured_attempts=attempts,successes=successes)))
