"""Saved-data supplementary client-observed token-gap tails; not a new primary."""
from pathlib import Path
import json,statistics,sys,math
r=Path(sys.argv[1])
def pct(values,q):
 a=sorted(values);x=(len(a)-1)*q;i=math.floor(x);j=math.ceil(x)
 return a[i]+(a[j]-a[i])*(x-i) if a else None
cells=[]
for model in ['qwen','smol']:
 groups={}
 for line in (r/('full_'+model+'.jsonl')).open():
  x=json.loads(line)
  if x.get('event') in ['request','request_error'] and x.get('kind')=='measured':
   groups.setdefault((x['pair'],x['mode'],x['rate']),[]).append(x)
 for (pair,mode,rate),rows in sorted(groups.items()):
  assert len(rows)==256
  good=[x for x in rows if x['event']=='request']
  gaps=[];worst=[]
  for x in good:
   a=x['arrival_ns'];assert len(a)==64 and a==sorted(a)
   g=[(b-a)/1e6 for a,b in zip(a,a[1:])]
   gaps.extend(g);worst.append(max(g))
  cells.append(dict(model=model,pair=pair,mode=mode,rate=rate,attempts=len(rows),failures=len(rows)-len(good),
   observed_gaps=len(gaps),zero_gaps=sum(x==0 for x in gaps),
   client_gap_p95_ms=pct(gaps,.95),client_gap_p99_ms=pct(gaps,.99),
   per_request_max_client_gap_p95_ms=pct(worst,.95),per_request_max_client_gap_p99_ms=pct(worst,.99)))
assert len(cells)==40
aggregates=[]
for model in ['qwen','smol']:
 for mode in ['uring_loop','userspace']:
  for rate in [64,96]:
   chosen=[x for x in cells if (x['model'],x['mode'],x['rate'])==(model,mode,rate)]
   assert len(chosen)==5
   aggregates.append(dict(model=model,mode=mode,rate=rate,
    block_means={k:statistics.mean(x[k] for x in chosen) for k in chosen[0] if k.endswith('_ms')},
    attempts=sum(x['attempts'] for x in chosen),failures=sum(x['failures'] for x in chosen),
    observed_gaps=sum(x['observed_gaps'] for x in chosen),zero_gaps=sum(x['zero_gaps'] for x in chosen)))
print(json.dumps(dict(scope='Exploratory saved-data supplement requested during full collection; not a changed primary or separately collected experiment. Token arrival timestamps are recv observations: multiple token IDs in one recv share a timestamp. Gaps include client scheduling and network buffering, not isolated GPU decode time. Per-cell pooled gap quantiles weight each token transition equally; per-request maximum-gap quantiles weight requests equally. Aggregates are means of five block statistics, not pooled percentiles. Failed requests remain in denominators; conditional gaps do not assign finite latency to failures.',cells=cells,aggregates=aggregates),indent=2))
