#!/usr/bin/env python3
"""Recompute the isolated gen1/c8 observation using real client and trace records."""
import pathlib,json,re,statistics,collections,sys
from analysis import analyze
t=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).parent
asset=json.loads((t/'frozen_references.json').read_text());reports=[]
files=[t/name for name in ['probe_smollm_ordinary.jsonl','probe_smollm_trace.jsonl','probe_qwen_ordinary.jsonl','probe_qwen_trace.jsonl']]
for path in files:
 base=analyze(path)
 records=[json.loads(line) for line in path.open()]
 meta=next(x for x in records if x['event']=='metadata')
 assert meta['backend']=='vllm' and meta['matrix']==[[1,8]] and meta['requests_per_cell']==32 and meta['warmups_per_executor']==8
 frozen=next(x for x in asset['models'].values() if x['model']==meta['model'])
 pool={(tuple(x['prompt']),x['gen']):{tuple(y) for y in x['sequences']} for x in frozen['references']}
 for mode in meta['modes']:
  requests=[x for x in records if x['event']=='request' and x['mode']==mode]
  warm=[x for x in requests if x['kind']=='warmup'];measured=[x for x in requests if x['kind']=='measured']
  assert len(warm)==8 and len(measured)==32 and len(requests)==40
  assert len({x['client_ns'] for x in requests})==40
  for x in requests:
   assert not x['bad'] and x['gen']==len(x['tokens'])==1
   assert tuple(x['tokens']) in pool[(tuple(x['input_ids']),1)]
  executor=next(x for x in records if x['event']=='executor' and x['mode']==mode)
  counters={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',executor['stdout'].split('resident vLLM stopped:',1)[1].splitlines()[0])}
  assert counters['admitted']==counters['retired']==40 and counters['trace_overflows']==counters['graph_error']==0
  row=dict(file=path.name,model=meta['model'],mode=mode,condition='ordinary' if meta['untraced'] else 'trace',
           total_model_rounds=counters['device_graph_launches'],measured_model_rounds=counters['device_graph_launches']-8,
           client_ttft_ms=statistics.mean(x['ttft_ms'] for x in measured),measured_requests=32,warmups=8)
  if not meta['untraced']:
   prefix=path.with_suffix('').with_name(path.stem+'_p0_'+mode)
   events=[json.loads(line) for line in pathlib.Path(str(prefix)+'.gpu.jsonl').open()]
   assert events[-1]['event']=='terminal' and events[-1]['overflows']==0
   admissions=[x for x in events if x['event']=='admission'];computes=[x for x in events if x['event']=='compute'];releases=[x for x in events if x['event']=='release']
   by_marker={x['client_ns']:x for x in admissions};assert len(by_marker)==len(admissions)==40
   warm_ids={by_marker[x['client_ns']]['id'] for x in warm};measured_ids={by_marker[x['client_ns']]['id'] for x in measured}
   assert not warm_ids&measured_ids and len(warm_ids)==8 and len(measured_ids)==32
   assert len(computes)==counters['device_graph_launches']
   assert all(x['batch']==len(x['request_ids'])==len(x['tokens']) for x in computes)
   compute_counts=collections.Counter(i for x in computes for i in x['request_ids'])
   assert compute_counts==collections.Counter({x['id']:1 for x in admissions})
   release_counts=collections.Counter(i for x in releases for i in x['request_ids'])
   assert release_counts==compute_counts
   warm_rounds=[x for x in computes if set(x['request_ids'])&warm_ids]
   measured_rounds=[x for x in computes if set(x['request_ids'])&measured_ids]
   assert len(warm_rounds)==8 and all(x['batch']==1 and set(x['request_ids'])<=warm_ids for x in warm_rounds)
   assert all(set(x['request_ids'])<=measured_ids for x in measured_rounds)
   assert len(measured_rounds)==row['measured_model_rounds']
   assert sum(x['batch'] for x in measured_rounds)==32
   row.update(measured_batch_sizes=[x['batch'] for x in measured_rounds],
              measured_round_request_ids=[x['request_ids'] for x in measured_rounds],
              measured_request_ids=sorted(measured_ids),warmup_request_ids=sorted(warm_ids),
              measured_release_batches=[x['batch'] for x in releases if set(x['request_ids'])&measured_ids])
  reports.append(row)
report=dict(scope='one process per condition; descriptive instrumentation sensitivity; no ordinary full-matrix mediation proof',rows=reports)
(t/'probe.analysis.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
