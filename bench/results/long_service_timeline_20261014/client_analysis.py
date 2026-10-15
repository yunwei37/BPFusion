# Client-only post-hoc reconstruction; fixed full analyzer preserved and failing.
import pathlib,json,gzip,statistics,math,sys,collections
t=pathlib.Path(sys.argv[1]);stage=sys.argv[2];results=[]
def read(p):return [json.loads(l) for l in p.open()]
def union(events):
 intervals=sorted((e['ts'],e['ts']+e['dur']) for e in events)
 assert intervals
 a,b=intervals[0];total=0
 for c,d in intervals[1:]:
  if c<=b:b=max(b,d)
  else:total+=b-a;a,b=c,d
 return total+b-a
for p in sorted(t.glob(stage+'_*.jsonl')):
 records=read(p);meta=records[0];assert meta['event']=='metadata'
 assert records[-1]['event']=='terminal' and records[-1]['exit']==0 and not any(x['event']=='failure' for x in records)
 rows=[x for x in records if x['event']=='request'];assert len(rows)==meta['requests']+8
 assert sorted(x['index'] for x in rows)==list(range(meta['requests']+8))
 pool={(tuple(x['prompt']),x['gen']):{tuple(s) for s in x['sequences']} for x in meta['frozen_model']['references']}
 for row in rows:
  assert tuple(row['tokens']) in pool[(tuple(row['input_ids']),row['gen'])]
  assert len(row['tokens'])==len(row['arrival_ns'])==row['gen']
 exe=next(x for x in records if x['event']=='executor');assert exe['exit']==0
 replay=next(x for x in records if x['event']=='replay');assert replay['exit']==0
 logfile=exe['stdout'];d=t/p.stem
 gpu=read(d/'model.gpu.jsonl');refs=read(d/'model.gpu.jsonl.references.jsonl')
 assert gpu[-1]['event']=='terminal' and gpu[-1]['overflows']==0
 clients={x['client_ns']:x for x in rows};admit={};history={};owners={};released=set();computes=[]
 for x in gpu:
  if x['event']=='admission':
   assert not x['bad'] and x['client_ns'] in clients and x['id']%8 not in owners
   row=clients[x['client_ns']];assert x['input_ids']==row['input_ids'] and x['gen']==row['gen']
   admit[x['id']]=x;history[x['id']]=[];owners[x['id']%8]=x['id']
  elif x['event']=='compute':
   assert len(x['request_ids'])==len(x['tokens'])==x['batch']
   if x['query']:assert x['query']==max(len(admit[i]['input_ids']) for i in x['request_ids'])
   for i,token in zip(x['request_ids'],x['tokens']):
    assert i not in released and owners[i%8]==i
    if x['query']:assert not history[i]
    else:assert history[i]
    history[i].append(token)
   computes.append(x)
  elif x['event']=='release':
   assert x['request_ids']==list(range(len(released),len(released)+x['batch']))
   for i in x['request_ids']:
    assert len(history[i])==admit[i]['gen'];assert owners.pop(i%8)==i;released.add(i)
 assert not owners and len(released)==len(admit)==len(rows)==len(refs)
 for x in refs:
  assert x['tokens']==history[x['id']]==clients[x['client_ns']]['tokens'] and x['prompt']==admit[x['id']]['input_ids']
 selected=[x for x in computes if all(not clients[admit[i]['client_ns']]['warmup'] for i in x['request_ids'])]
 assert sum(x['batch'] for x in selected)==meta['requests']*64
 measured=[x for x in rows if not x['warmup']]
 cell=next(x for x in records if x['event']=='cell')
 assert cell['first_ns']==min(x['start_ns'] for x in measured) and cell['last_ns']==max(x['arrival_ns'][-1] for x in measured)
 result={k:meta[k] for k in ['model','pair','path','condition']}
 result.update(requests=len(rows),measured_requests=len(measured),tps=len(measured)*64/((cell['last_ns']-cell['first_ns'])/1e9),ttft_ms=statistics.mean(x['ttft_ms'] for x in measured),completion_ms=statistics.mean((x['arrival_ns'][-1]-x['start_ns'])/1e6 for x in measured),rounds=len(selected),batch_histogram=dict(collections.Counter(x['batch'] for x in selected)))
 results.append(result)
expected=4 if stage=='preflight' else 40;assert len(results)==expected
effects=[]
if stage=='full':
 for model in ['qwen','smol']:
  for condition in ['unprofiled','profiled']:
   metrics=['tps','ttft_ms','completion_ms','rounds']
   for metric in metrics:
    diffs=[next(x[metric] for x in results if (x['model'],x['pair'],x['path'],x['condition'])==(model,p,'loop',condition))-next(x[metric] for x in results if (x['model'],x['pair'],x['path'],x['condition'])==(model,p,'native',condition)) for p in range(5)]
    mean=statistics.mean(diffs);margin=2.7764451051977987*statistics.stdev(diffs)/math.sqrt(5)
    effects.append(dict(model=model,condition=condition,contrast='loop-native',metric=metric,differences=diffs,mean=mean,nominal_t95=[mean-margin,mean+margin]))
  for path in ['loop','native']:
   for metric in ['tps','ttft_ms','completion_ms','rounds']:
    diffs=[next(x[metric] for x in results if (x['model'],x['pair'],x['path'],x['condition'])==(model,p,path,'profiled'))-next(x[metric] for x in results if (x['model'],x['pair'],x['path'],x['condition'])==(model,p,path,'unprofiled')) for p in range(5)]
    mean=statistics.mean(diffs);margin=2.7764451051977987*statistics.stdev(diffs)/math.sqrt(5)
    effects.append(dict(model=model,path=path,contrast='profiled-unprofiled',metric=metric,differences=diffs,mean=mean,nominal_t95=[mean-margin,mean+margin]))
out=dict(stage=stage,cases=results,effects=effects,exit=0,scope='Post-hoc client and logical-trajectory reconstruction only. Full GPU decomposition analyzer remains failed; no profile durations or repaired coverage claim.')
(t/(stage+'.client.analysis.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
