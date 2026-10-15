from pathlib import Path
from collections import Counter
import json,statistics,sys
a=Path(sys.argv[1]);rows=[]
for model in ['qwen','smol']:
 clients=[json.loads(z) for z in (a/('full_'+model+'.jsonl')).open()]
 markers={x['client_ns']:x['rate'] for x in clients if x.get('event')=='request' and x.get('kind')=='measured'}
 for pair in range(5):
  for mode in ['uring_loop','userspace']:
   events=[json.loads(z) for z in (a/f'full_{model}_p{pair}_{mode}.gpu.jsonl').open()]
   rates={x['id']:markers.get(x['client_ns']) for x in events if x['event']=='admission'}
   hist={rate:Counter() for rate in [64,96]};prefill={rate:Counter() for rate in [64,96]}
   for x in events:
    if x['event']!='compute':continue
    chosen={rates[i] for i in x['request_ids']};assert len(chosen)==1
    rate=next(iter(chosen))
    if rate is not None:(hist if x['query']==0 else prefill)[rate][x['batch']]+=1
   for rate in [64,96]:
    h=hist[rate];p=prefill[rate];tokens=sum(b*n for b,n in h.items())
    assert tokens==256*63
    rows.append(dict(model=model,pair=pair,mode=mode,rate=rate,decode_hist=dict(h),prefill_hist=dict(p),decode_rounds=sum(h.values()),decode_tokens=tokens,full_width_decode_rounds=h[8],mean_decode_batch=tokens/sum(h.values())))
aggregate=[]
for model in ['qwen','smol']:
 for mode in ['uring_loop','userspace']:
  for rate in [64,96]:
   chosen=[x for x in rows if (x['model'],x['mode'],x['rate'])==(model,mode,rate)]
   aggregate.append(dict(model=model,mode=mode,rate=rate,mean_block_decode_batch=statistics.mean(x['mean_decode_batch'] for x in chosen),decode_rounds=sum(x['decode_rounds'] for x in chosen),full_width_decode_rounds=sum(x['full_width_decode_rounds'] for x in chosen),prefill_rounds=sum(sum(x['prefill_hist'].values()) for x in chosen)))
print(json.dumps(dict(scope='Saved logical batch counts from complete0063; not time occupancy, GPU utilization or new performance measurement.',cells=rows,aggregate=aggregate),indent=2))
