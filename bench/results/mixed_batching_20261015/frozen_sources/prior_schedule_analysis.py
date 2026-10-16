from pathlib import Path
import json,collections,statistics,sys
a=Path(sys.argv[1]);out=Path(sys.argv[2]);records=[]
for model in ['qwen','smol']:
 for trace in sorted(a.glob('full_'+model+'_p*_*.gpu.jsonl')):
  req={};counts=collections.Counter()
  for line in trace.open():
   e=json.loads(line)
   if e['event']=='admission':req[e['id']]=dict(gen=e['gen'],k=0,bad=e['bad'])
   elif e['event']=='compute':
    counts['rounds']+=1
    if e['query']:
     counts['prefill_rounds']+=1
     d=[rid for rid,x in req.items() if not x['bad'] and 0<x['k']<x['gen']]
     if d:counts['prefill_with_deferred_decode']+=1;counts['deferred_decode_request_steps']+=len(d)
     counts['prefill_rows']+=e['batch']
    else:counts['decode_rounds']+=1;counts['decode_rows']+=e['batch']
    for rid in e['request_ids']:req[rid]['k']+=1
   elif e['event']=='release':
    for rid in e['request_ids']:del req[rid]
  assert not req
  records.append(dict(model=model,trace=trace.name,**dict(counts)))
summaries=[]
for model in ['qwen','smol']:
 for mode in ['uring_loop','userspace']:
  for banks in [8,16]:
   rows=[x for x in records if x['model']==model and x['trace'].endswith('_'+mode+'_'+str(banks)+'.gpu.jsonl')]
   assert len(rows)==5
   summaries.append(dict(model=model,mode=mode,banks=banks,blocks=5,**{k:statistics.mean(x.get(k,0) for x in rows) for k in ['rounds','prefill_rounds','prefill_with_deferred_decode','deferred_decode_request_steps','decode_rows']}))
doc=dict(scope='Post-hoc logical counts from all40 saved0064 traces; two rate cells combined plus8 gen1 warmups per executor. Counts do not measure GPU duration,causation,ordinary performance or a new intervention.',records=records,summaries=summaries)
out.write_text(json.dumps(doc,indent=2));print(json.dumps(summaries))
