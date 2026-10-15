# Post-collection exploratory ordering check; no GPU execution.
# Client stamps precede sends and are not kernel ingress timestamps.
from pathlib import Path
import json,sys
archive=Path(sys.argv[1])
rows=[]
for model in ['qwen','smol']:
 cells={}
 for line in (archive/('full_'+model+'.jsonl')).open():
  x=json.loads(line)
  if x.get('event')=='request' and x.get('kind')=='measured':
   cells.setdefault((x['pair'],x['mode'],x['rate']),[]).append(x)
 admissions={}
 for pair in range(5):
  for mode in ['uring_loop','userspace']:
   path=archive/('full_'+model+'_p'+str(pair)+'_'+mode+'.gpu.jsonl')
   admissions[pair,mode]={x['client_ns']:x['id'] for x in map(json.loads,path.open()) if x['event']=='admission'}
 for (pair,mode,rate),requests in sorted(cells.items()):
  assert len(requests)==256
  ordered=sorted(requests,key=lambda x:x['client_ns'])
  sequence=[admissions[pair,mode][x['client_ns']] for x in ordered]
  assert len(set(sequence))==256
  bypass=[sum(sequence[j]<value for j in range(i+1,len(sequence))) for i,value in enumerate(sequence)]
  worst=max(range(len(ordered)),key=lambda i:ordered[i]['connect_ttft_ms'])
  rows.append(dict(model=model,pair=pair,mode=mode,rate=rate,
   client_stamp_order_inversions=sum(bypass),
   max_later_stamp_admitted_first=max(bypass),
   worst_ttft_ms=ordered[worst]['connect_ttft_ms'],
   worst_ttft_later_stamp_admitted_first=bypass[worst]))
print(json.dumps(dict(scope='Exploratory post-review saved-data analysis. GPU model-admission order versus client stamp order, not exact ingress order or queue residence time. No causal or new primary claim.',cells=rows),indent=2))
