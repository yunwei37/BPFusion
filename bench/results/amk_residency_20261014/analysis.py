#!/usr/bin/env python3
import pathlib,json,gzip,sys,statistics,math,collections
root=pathlib.Path(sys.argv[1]);raw=root/(sys.argv[2]+'.jsonl')
events=[json.loads(l) for l in raw.open()]
assert events[-1]['event']=='terminal' and events[-1]['exit_code']==0
meta=next(e for e in events if e['event']=='metadata')
prompts=meta['prompts'];warm_calls=sum(len(prompts[i%4]) for i in range(8))
measured_calls=sum(len(prompts[i%4])+63 for i in range(8))
def interval_metrics(es):
 points=[]
 for e in es:points.extend([(e['ts'],1),(e['ts']+e['dur'],-1)])
 points.sort(key=lambda x:(x[0],x[1]));active=peak=0;union=0;previous=points[0][0]
 for stamp,change in points:
  if active:union+=stamp-previous
  active+=change;peak=max(peak,active);previous=stamp
 assert active==0
 total=sum(e['dur'] for e in es)
 return dict(model_calls=len(es),max_overlapping=peak,sum_duration_ms=total/1000,occupied_union_ms=union/1000,
             overlap_ratio=total/union,model_span_ms=(points[-1][0]-points[0][0])/1000,
             mean_model_kernel_ms=statistics.mean(e['dur'] for e in es)/1000)
cases=[]
for exe in (e for e in events if e['event']=='executor'):
 pair,mode=exe['pair'],exe['mode']
 rs=[e for e in events if e['event']=='request' and e['pair']==pair and e['mode']==mode]
 cells=[e for e in events if e['event']=='cell' and e['pair']==pair and e['mode']==mode]
 assert len(rs)==24 and len(cells)==2 and exe['exit_code']==0
 case=dict(pair=pair,mode=mode,requests=len(rs),cells=[])
 for c in cells:
  selected=[r for r in rs if r['kind']=='measured' and r['gen']==c['gen'] and r['concurrency']==c['concurrency']]
  first=min(r['start_ns'] for r in selected);last=max(r['arrival_ns'][-1] for r in selected)
  tps=sum(len(r['tokens']) for r in selected)/((last-first)/1e9)
  assert abs(tps-c['output_tokens_per_s'])<1e-8
  row=dict(concurrency=c['concurrency'],tokens_per_s=tps,
           ttft_ms=statistics.mean((r['arrival_ns'][0]-r['start_ns'])/1e6 for r in selected),
           completion_ms=statistics.mean((r['arrival_ns'][-1]-r['start_ns'])/1e6 for r in selected))
  case['cells'].append(row)
 if mode.endswith('_profiled'):
  path=root/(raw.stem+f'_p{pair}_{mode}')
  trace=json.loads(gzip.open(path/'trace.json.gz','rt').read())
  catalogue=json.loads((path/'graph_catalogue.json').read_text())
  nodes={}
  for g in catalogue:
   for n in g['model_nodes']:
    assert n['node_id'] not in nodes
    nodes[n['node_id']]=dict(bank=g['bank'],index=g['index'],position=n['position'],geometry=g['geometry'])
  ks=[e for e in trace['traceEvents'] if e.get('cat')=='kernel']
  models=sorted([e for e in ks if 'amk_megakernel_persist' in e['name']],key=lambda e:e['ts'])
  assert len(models)==warm_calls+2*measured_calls,(mode,len(models),warm_calls+2*measured_calls)
  matched=sum(e['args'].get('graph node id') in nodes for e in models)
  # CUDA instantiation changes activity graph identities. Do not infer offsets.
  assert all(e['args']['grid']==[170,1,1] and e['args']['block']==[256,1,1] for e in models)
  case['timeline_status']='unsupported source-to-instantiated node identity; no per-bank/position/cell overlap attribution'
  case['catalogue_id_matches']=matched
  helpers=collections.Counter(e['name'] for e in ks if 'amk_megakernel_persist' not in e['name'])
  case['trace']=dict(model_calls=len(models),catalogued_model_nodes=len(nodes),helper_kernel_counts=dict(helpers))
 cases.append(case)
report=dict(source=meta['commit'],executors=len(cases),measured_requests=sum(len([e for e in events if e['event']=='request' and e['kind']=='measured']) for _ in [0]),cases=cases)
if len(cases)==30:
 effects=[]
 for pair in range(5):
  def row(mode,c):return next(x for case in cases if case['pair']==pair and case['mode']==mode for x in case['cells'] if x['concurrency']==c)
  effects.append(row('amk_park_ordinary',8)['tokens_per_s']-row('amk_userspace_ordinary',8)['tokens_per_s'])
 mean=statistics.mean(effects);half=2.776445105*statistics.stdev(effects)/math.sqrt(5)
 report['primary_park_minus_native_c8_tps']=dict(blocks=effects,mean=mean,t95=[mean-half,mean+half])
(root/(sys.argv[2]+'.analysis.json')).write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
