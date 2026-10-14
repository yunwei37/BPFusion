import pathlib,json,gzip,statistics,math,sys
root=pathlib.Path(sys.argv[1]);stage=sys.argv[2]
results=[]
def union(events):
 intervals=sorted((e['ts'],e['ts']+e['dur']) for e in events)
 left,right=intervals[0];total=0
 for a,b in intervals[1:]:
  if a<=right:right=max(right,b)
  else:total+=right-left;left,right=a,b
 return total+right-left
for path in sorted(root.glob(stage+'_*.jsonl')):
 records=[json.loads(l) for l in path.open()]
 meta=records[0];assert meta['event']=='metadata'
 assert records[-1]['event']=='terminal' and records[-1]['exit']==0
 assert not any(r['event']=='failure' for r in records)
 exe=next(r for r in records if r['event']=='executor');assert exe['exit']==0
 rows=[r for r in records if r['event']=='request']
 assert [r['index'] for r in rows]==list(range(meta['requests']))
 assert [r['warmup'] for r in rows]==[True]*4+[False]*(meta['requests']-4)
 pool={(tuple(r['prompt']),r['gen']):{tuple(x) for x in r['sequences']} for r in meta['frozen_model']['references']}
 for r in rows:
  assert r['input_ids']==meta['prompts'][r['case']]
  assert tuple(r['tokens']) in pool[(tuple(r['input_ids']),1)]
  assert len(r['arrival_ns'])==1 and r['ttft_ms']==(r['arrival_ns'][0]-r['start_ns'])/1e6
  assert r['tpot_ms'] is None
 measured=[r for r in rows if not r['warmup']]
 result=dict(model=meta['model'],pair=meta['pair'],condition=meta['condition'],requests=len(rows),measured=len(measured),ttft_ms=statistics.mean(r['ttft_ms'] for r in measured),source=meta['source'],library_stat=meta['library_stat'])
 if meta['condition']=='profiled':
  log=exe['stdout']
  setup=json.loads(next(l.split(' ',1)[1] for l in log.splitlines() if l.startswith('CUPTI_SETUP ')))
  assert setup['device_graph_status']==setup['driver_status']==setup['hardware_trace_status']==0
  catalogue=json.loads(next(l.split(' ',1)[1] for l in log.splitlines() if l.startswith('GRAPH_CATALOGUE ')))['graphs']
  counts={r['input_tokens']:r['body_node_types'].get('0',0)+r['head_node_types'].get('0',0) for r in catalogue}
  tracepath=pathlib.Path(next(r for r in records if r['event']=='trace')['path'])
  trace=json.load(gzip.open(tracepath,'rt'));events=trace['traceEvents']
  model_events=sorted((e for e in events if e.get('cat')=='kernel' and not e.get('name','').startswith(('dispatch(','io_network('))),key=lambda e:e['ts'])
  assert len(model_events)==sum(counts[r['input_tokens']] for r in rows),(path,len(model_events),counts)
  expected_memory={kind:sum(sum(c[k].get(str(kind),0) for k in ['body_node_types','head_node_types']) for r in rows for c in catalogue if c['input_tokens']==r['input_tokens']) for kind in [1,2]}
  actual_memory={1:sum(e.get('cat')=='gpu_memcpy' and e.get('args',{}).get('graph id',0)!=0 for e in events),2:sum(e.get('cat')=='gpu_memset' and e.get('args',{}).get('graph id',0)!=0 for e in events)}
  assert actual_memory==expected_memory,(path,expected_memory,actual_memory)
  anchors=[json.loads(l.split(' ',1)[1]) for l in log.splitlines() if l.startswith('CLOCK_ANCHOR ')]
  bounds=[]
  for anchor in anchors:
   found=[e for e in events if e.get('name')=='BPFusion_clock_anchor_'+anchor['label']]
   assert len(found)==1
   e=found[0];begin=e['ts']*1000;end=(e['ts']+e['dur'])*1000
   low=max(begin-anchor['inside_ns'],end-anchor['after_ns'])
   high=min(begin-anchor['before_ns'],end-anchor['inside_ns'])
   assert low<=high
   bounds.append(dict(label=anchor['label'],low_ns=low,high_ns=high))
  assert len(bounds)==2
  low=max(b['low_ns'] for b in bounds);high=min(b['high_ns'] for b in bounds)
  assert low<=high
  pos=0;timeline=[]
  for r in rows:
   count=counts[r['input_tokens']];group=model_events[pos:pos+count];pos+=count
   assert count>0 and len(group)==count
   ids={(e['args']['graph id'],e['args']['graph node id']) for e in group}
   assert len(ids)==count,(path,r['index'],'nonunique graph/node records')
   first=min(e['ts'] for e in group)*1000;last=max(e['ts']+e['dur'] for e in group)*1000
   # Compatibility is weaker than a proved GPU/CPU clock bias bound.
   low=max(low,last-r['arrival_ns'][0]);high=min(high,first-r['start_ns'])
   span=(last-first)/1e6;un=union(group)/1000
   assert span>=un-1e-9
   timeline.append(dict(model=meta['model'],pair=meta['pair'],index=r['index'],warmup=r['warmup'],input_tokens=r['input_tokens'],kernels=count,ttft_ms=r['ttft_ms'],model_kernel_span_ms=span,kernel_sum_ms=sum(e['dur'] for e in group)/1000,kernel_union_ms=un,span_minus_union_ms=span-un))
  assert pos==len(model_events) and low<=high,(path,'causal clock compatibility',low,high)
  mt=[r for r in timeline if not r['warmup']]
  for k in ['model_kernel_span_ms','kernel_sum_ms','kernel_union_ms','span_minus_union_ms']:result[k]=statistics.mean(r[k] for r in mt)
  result['profiled_span_fraction']=result['model_kernel_span_ms']/result['ttft_ms']
  result.update(model_kernel_records=len(model_events),memory_counts=actual_memory,cpu_anchor_bounds=bounds,compatible_offset_ns=[low,high],clock_scope='compatibility only; no independent GPU bias guarantee')
  with (path.parent/(path.stem+'.timeline.jsonl')).open('w') as f:
   for r in timeline:f.write(json.dumps(r)+'\n')
 results.append(result);print(json.dumps(dict(event='case_metrics',**result)))
if stage=='full':
 assert {(r['model'],r['pair'],r['condition']) for r in results}=={(m,p,c) for m in ['qwen','smol'] for p in range(5) for c in ['ordinary','profiled']}
 assert len({r['source'] for r in results})==1
 assert len({(r['library_stat']['size'],r['library_stat']['inode']) for r in results})==1
 for model in ['qwen','smol']:
  selected=[r for r in results if r['model']==model]
  for condition in ['ordinary','profiled']:
   rr=[r for r in selected if r['condition']==condition]
   keys=['ttft_ms']+(['model_kernel_span_ms','kernel_sum_ms','kernel_union_ms','span_minus_union_ms'] if condition=='profiled' else [])
   print(json.dumps(dict(event='model_mean',model=model,condition=condition,**{k:statistics.mean(r[k] for r in rr) for k in keys})))
  diffs=[next(r['ttft_ms'] for r in selected if r['pair']==p and r['condition']=='ordinary')-next(r['ttft_ms'] for r in selected if r['pair']==p and r['condition']=='profiled') for p in range(5)]
  mean=statistics.mean(diffs);margin=2.7764451051977987*statistics.stdev(diffs)/math.sqrt(5)
  print(json.dumps(dict(event='profiling_effect_ordinary_minus_profiled',model=model,differences=diffs,mean_ms=mean,nominal_t95=[mean-margin,mean+margin])))
print(json.dumps(dict(event='analysis_terminal',exit=0,cases=len(results))))
