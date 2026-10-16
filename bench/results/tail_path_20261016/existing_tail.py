from pathlib import Path
import json,math,statistics
a=Path('/workspaces/repository/bench/results/mixed_batching_20261015')
rows=[json.loads(l) for l in (a/'full_qwen.jsonl').open()]
def q(v,p):return sorted(v)[min(len(v)-1,math.ceil(p*len(v))-1)]
out=[]
for mode in ['uring_loop_16_mixed','userspace_16_mixed']:
 for pair in range(5):
  rr=[x for x in rows if x.get('event')=='request' and x.get('rate')==192 and x.get('gen')==64 and x['mode']==mode and x['pair']==pair]
  assert len(rr)==256
  gaps=[dict(ms=(x['arrival_ns'][i]-x['arrival_ns'][i-1])/1e6,index=i,client_ns=x['client_ns']) for x in rr for i in range(1,64)]
  p99=q([z['ms'] for z in gaps],.99);tail=[z for z in gaps if z['ms']>=p99]
  out.append(dict(mode=mode,pair=pair,requests=len(rr),itl_count=len(gaps),itl_p99_ms=p99,
   final_gap_p99_ms=q([z['ms'] for z in gaps if z['index']==63],.99),
   interior_gap_p99_ms=q([z['ms'] for z in gaps if z['index']!=63],.99),
   zero_fraction=sum(z['ms']==0 for z in gaps)/len(gaps),
   p99_tail_count=len(tail),p99_tail_final_count=sum(z['index']==63 for z in tail),
   max_ms=max(z['ms'] for z in gaps),largest=sorted(gaps,key=lambda z:-z['ms'])[:20]))
print(json.dumps(dict(scope='Post-hoc existing-data discriminator; no phase timestamps or causal attribution.',blocks=out),indent=2))
