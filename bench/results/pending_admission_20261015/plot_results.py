import pathlib,json,statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=pathlib.Path(__file__).resolve().parent
models=[('qwen','Qwen2.5-0.5B'),('smol','SmolLM2-135M')]
modes=[('uring_loop','Kernel + FIFO','#c43c39',-3),('userspace','Native events','#176b9f',3)]
rates=[4,64,96];allcells=[];allpaired=[];coverages=[];aggregates=[]
fig,axes=plt.subplots(2,2,figsize=(13.2,7.4),sharex='col',layout='constrained')
for col,(key,label) in enumerate(models):
 rows=[json.loads(x) for x in (r/('full_'+key+'.analysis.stdout')).read_text().splitlines()]
 cells=[dict(model=key,**x) for x in rows if x['event']=='cell_metrics']
 assert len(cells)==30 and all(x['failures']==0 for x in cells)
 allcells.extend(cells);allpaired.extend(dict(model=key,**x) for x in rows if x['event']=='paired')
 coverages.extend(dict(model=key,**x) for x in rows if x['event']=='coverage')
 axes[0,col].set_title(label)
 for mode,name,color,offset in modes:
  values={metric:[] for metric in ['connect_ttft_ms_p99','executor_cpu_ms_per_attempt']}
  for rate in rates:
   selected=sorted([x for x in cells if x['mode']==mode and x['rate']==rate],key=lambda x:x['pair'])
   assert [x['pair'] for x in selected]==list(range(5))
   means={metric:statistics.mean(x[metric] for x in selected) for metric in selected[0] if isinstance(selected[0][metric],(int,float)) and metric not in ['pair','rate']}
   aggregates.append(dict(model=key,mode=mode,rate=rate,attempts=sum(x['attempts'] for x in selected),failures=0,block_means=means))
   for row,metric in enumerate(values):
    ys=[x[metric] for x in selected];values[metric].append(statistics.mean(ys))
    axes[row,col].scatter([rate+offset+(i-2)*.65 for i in range(5)],ys,s=19,color=color,alpha=.7,zorder=3)
  for row,metric in enumerate(values):
   axes[row,col].plot([x+offset for x in rates],values[metric],color=color,marker='D',markersize=5,linewidth=1.5,label=name,zorder=4)
 for row in range(2):
  ax=axes[row,col];ax.axvspan(58,70,color='#888888',alpha=.08,zorder=0)
  ax.set_xlim(-4,104);ax.set_xticks(rates);ax.grid(axis='y',alpha=.22);ax.spines[['top','right']].set_visible(False)
 axes[0,col].set_yscale('log')
 axes[1,col].set_ylim(bottom=0)
 axes[1,col].set_xlabel('Configured request rate (requests/s)')
axes[0,0].set_ylabel('Connect-inclusive TTFT P99 (ms)')
axes[1,0].set_ylabel('Executor process CPU (ms/attempt)')
axes[0,0].legend(frameon=False)
fig.suptitle('Pending-admission comparison: all 15,360 measured requests completed',fontsize=13)
fig.supxlabel('256 attempts/cell; 5 paired blocks. Small points: blocks; diamonds: means. Shared CPU host; partial CPU accounting.',fontsize=9)
fig.savefig(r/'pending_admission_results.png',dpi=170)
fig.savefig(r/'pending_admission_results.pdf')
(r/'pending_admission_results.data.json').write_text(json.dumps(dict(scope='Complete finite shared-host collection; means of block metrics, not pooled P99 or total service CPU. Shaded rate64 is the fixed primary condition. No failed measured requests.',cells=allcells,paired=allpaired,coverage=coverages,aggregates=aggregates),indent=2))
print(json.dumps(dict(cells=len(allcells),paired=len(allpaired),aggregates=len(aggregates),measured_attempts=sum(x['attempts'] for x in coverages))))
