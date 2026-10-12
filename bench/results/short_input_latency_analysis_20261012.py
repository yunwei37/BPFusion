#!/usr/bin/env python3
"""Native-request and standard Chrome-trace latency reconstruction."""
import pathlib,json,gzip,statistics,math
root=pathlib.Path('/workspaces/repository')
rows=[json.loads(x) for x in (root/'bench/results/short_input_latency_20261012.jsonl').read_text().splitlines()]
assert rows[-1]=={'event':'terminal','exit':0}
assert not any(r['event']=='failure' for r in rows)
all_results=[]
for name in ['smol','qwen']:
 rr=[r for r in rows if r['event']=='request' and r['model']==name]
 assert [r['index'] for r in rr]==list(range(20))
 assert [r['warmup'] for r in rr]==[True]*4+[False]*16
 log=next(r['log'] for r in rows if r['event']=='executor' and r['model']==name)
 assert 'launches=1 device_graph_launches=20 graph_error=0 banks=8 max_active=1' in log
 catalogue=json.loads(next(l.split(' ',1)[1] for l in log.splitlines() if l.startswith('GRAPH_CATALOGUE ')))
 counts={(c['bank'],c['input_tokens']):c['node_types'].get('0',0) for c in catalogue}
 anchors=[json.loads(l.split(' ',1)[1]) for l in log.splitlines() if l.startswith('CLOCK_ANCHOR ')]
 trace=json.load(gzip.open(root/f'bench/results/short_input_latency_{name}_20261012.json.gz','rt'))
 events=trace['traceEvents']
 bounds=[]
 for a in anchors:
  matches=[e for e in events if e.get('name')=='BPFusion_clock_anchor_'+a['label']]
  assert len(matches)==1
  e=matches[0];begin=e['ts']*1000;end=(e['ts']+e['dur'])*1000
  low=max(begin-a['inside_ns'],end-a['after_ns'])
  high=min(begin-a['before_ns'],end-a['inside_ns'])
  assert low<=high,(name,a,low,high)
  bounds.append(dict(label=a['label'],low_ns=low,high_ns=high))
 low=max(b['low_ns'] for b in bounds);high=min(b['high_ns'] for b in bounds)
 assert low<=high,(name,bounds)
 offset=(low+high)/2
 model=sorted((e for e in events if e.get('cat')=='kernel' and not e.get('name','').startswith('dispatch(')),key=lambda e:e['ts'])
 position=0;result=[]
 for r in rr:
  expected=counts[(r['queue']['slot'],r['input_tokens'])]
  group=model[position:position+expected];position+=expected
  assert len(group)==expected
  assert len({e['args']['graph node id'] for e in group})==expected
  assert len({e['args']['graph id'] for e in group})==1
  gpu_begin=min(e['ts'] for e in group)*1000-offset
  gpu_end=max(e['ts']+e['dur'] for e in group)*1000-offset
  # Independent calibration bounds need causal compatibility; unresolved small stages remain signed estimates with bounds.
  assert gpu_begin+(high-low)/2>=r['queue']['ingress_ns'],(name,r['index'],'GPU starts before ingress',gpu_begin,r['queue'])
  assert gpu_end-(high-low)/2<=r['arrival_ns'][0],(name,r['index'],'GPU ends after client reply')
  intervals=sorted((e['ts'],e['ts']+e['dur']) for e in group)
  left,right=intervals[0];union=0
  for a,b in intervals[1:]:
   if a<=right:right=max(right,b)
   else:union+=right-left;left,right=a,b
  union+=right-left
  stages={'send_to_ingress_ms':(r['queue']['ingress_ns']-r['start_ns'])/1e6,
          'ingress_to_gpu_ms':(gpu_begin-r['queue']['ingress_ns'])/1e6,
          'gpu_model_span_ms':(gpu_end-gpu_begin)/1e6,
          'gpu_to_client_ms':(r['arrival_ns'][0]-gpu_end)/1e6}
  assert abs(sum(stages.values())-r['ttft_ms'])<1e-7
  item=dict(model=name,index=r['index'],case=r['case'],warmup=r['warmup'],input_tokens=r['input_tokens'],model_kernels=expected,ttft_ms=r['ttft_ms'],kernel_duration_sum_ms=sum(e['dur'] for e in group)/1000,kernel_interval_union_ms=union/1000,stage_offset_half_width_us=(high-low)/2000,**stages)
  result.append(item)
 assert position==len(model),(name,position,len(model))
 all_results.extend(result)
 print(json.dumps({'model':name,'complete_requests':len(rr),'measured_requests':16,'model_kernel_records':len(model),'anchor_bounds':bounds,'common_offset_ns':[low,high],'anchor_half_width_us':(high-low)/2000}))
 measured=[r for r in result if not r['warmup']]
 for length in [2,5,8,None]:
  selection=[r for r in measured if length is None or r['input_tokens']==length]
  values={k:statistics.mean(r[k] for r in selection) for k in ['ttft_ms','model_kernels','send_to_ingress_ms','ingress_to_gpu_ms','gpu_model_span_ms','gpu_to_client_ms','kernel_duration_sum_ms','kernel_interval_union_ms']}
  values['gpu_span_fraction']=values['gpu_model_span_ms']/values['ttft_ms']
  print(json.dumps({'model':name,'input_tokens':length,'requests':len(selection),**values}))
(root/'bench/results/short_input_latency_stages_20261012.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in all_results))
