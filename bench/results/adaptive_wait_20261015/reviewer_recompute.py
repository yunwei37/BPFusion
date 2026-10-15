from pathlib import Path
import json,subprocess,statistics,math,collections,re,difflib,datetime,struct
p=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
def lines(f):return [json.loads(l) for l in (p/f).read_text().splitlines()]
runs=['preflight_qwen','qualification_repaired_qwen','qualification_repaired_smol','full_qwen','full_smol']
statuses=[]
for name in runs:
 z=subprocess.run(['/usr/bin/python3',str(p/'analysis.py'),str(p/(name+'.jsonl'))],cwd=r,capture_output=True)
 (p/(name+'.reviewer.stdout')).write_bytes(z.stdout);(p/(name+'.reviewer.stderr')).write_bytes(z.stderr)
 assert z.returncode==0,(name,z.stderr)
 assert z.stdout==(p/(name+'.analysis.stdout')).read_bytes() and z.stderr==(p/(name+'.analysis.stderr')).read_bytes(),name
 statuses.append(dict(name=name,exit=z.returncode,byte_equal=True))
report=['# Independent CPU recomputation','',datetime.datetime.now(datetime.timezone.utc).isoformat(),'','All five saved analyses rerun without model/GPU execution and reproduce stdout/stderr byte-for-byte.']
for model in ['qwen','smol']:
 raw=lines('full_'+model+'.jsonl');analysis=lines('full_'+model+'.analysis.stdout')
 meta=raw[0];assert meta['event']=='metadata'
 samples=[x for x in raw if x['event']=='request' and x['kind']=='measured']
 cells=[x for x in raw if x['event']=='cell'];summ={}
 for cell in cells:
  key=cell['pair'],cell['mode'],cell['gen'],cell['concurrency']
  rows=[x for x in samples if (x['pair'],x['mode'],x['gen'],x['concurrency'])==key]
  assert len(rows)==32
  first=min(x['start_ns'] for x in rows);last=max(x['arrival_ns'][-1] for x in rows)
  for x in rows:
   assert x['ttft_ms']==(x['arrival_ns'][0]-x['start_ns'])/1e6
   assert x['latency_ms']==(x['arrival_ns'][-1]-x['start_ns'])/1e6
  cpu=cell['worker_cpu_after']['executor_cpu_ns']-cell['worker_cpu_before']['executor_cpu_ns']
  summ[key]={'ttft_ms':statistics.mean((x['arrival_ns'][0]-x['start_ns'])/1e6 for x in rows),'completion_ms':statistics.mean((x['arrival_ns'][-1]-x['start_ns'])/1e6 for x in rows),'tokens_per_s':sum(len(x['tokens']) for x in rows)/((last-first)/1e9),'executor_cpu_s_per_request':cpu/1e9/len(rows),'known_worker_cpu_s_per_request':cpu/1e9/len(rows),'kernel_tx_cpu_s_per_request':0.0}
  if cell['gen']>1:summ[key]['tpot_ms']=statistics.mean((x['arrival_ns'][-1]-x['arrival_ns'][0])/(len(x['tokens'])-1)/1e6 for x in rows)
 checked=0
 for a in analysis:
  if a['event'].startswith('paired_difference'):
   diffs=[summ[i,a['candidate'],a['gen'],a['concurrency']][a['metric']]-summ[i,a['baseline'],a['gen'],a['concurrency']][a['metric']] for i in range(5)]
   mean=statistics.mean(diffs);margin=2.776445105*statistics.stdev(diffs)/math.sqrt(5);interval=[mean-margin,mean+margin]
   assert all(math.isclose(u,v,abs_tol=1e-11) for u,v in zip(diffs,a['candidate_minus_baseline']))
   assert math.isclose(mean,a['signed_mean'],abs_tol=1e-11) and all(math.isclose(u,v,abs_tol=1e-11) for u,v in zip(interval,a['signed_t95']))
   checked+=1
  elif a['event']=='metric':
   vals={k:statistics.mean(summ[i,a['mode'],a['gen'],a['concurrency']][k] for i in range(5)) for k in summ[0,a['mode'],a['gen'],a['concurrency']]}
   aliases={'ttft_ms':'ttft_mean_ms','completion_ms':'completion_mean_ms','tpot_ms':'tpot_mean_ms'}
   for k,v in vals.items():assert math.isclose(v,a[aliases.get(k,k)],abs_tol=1e-11)
   rr=[x for x in samples if x['mode']==a['mode'] and x['gen']==a['gen']]
   tt=sorted(x['ttft_ms'] for x in rr)
   assert tt[math.ceil(len(tt)*.5)-1]==a['ttft_p50_ms'] and tt[math.ceil(len(tt)*.99)-1]==a['ttft_p99_ms']
 report+=['',f'## {model}: all {checked} contrasts and six metric rows independently match','', '|gen/c|condition|CPU ms/request|TTFT ms|completion ms|TPOT ms|wall TPS|','|---|---|---:|---:|---:|---:|---:|']
 for a in analysis:
  if a['event']=='metric':report.append('|%s/%s|%s|%.9f|%.9f|%.9f|%s|%.9f|'%(a['gen'],a['concurrency'],a['mode'],a['executor_cpu_s_per_request']*1000,a['ttft_mean_ms'],a['completion_mean_ms'],str(a['tpot_mean_ms']),a['tokens_per_s']))
 report+=['','|gen/c|contrast|metric|signed mean|nominal t95|all five signed differences|','|---|---|---|---:|---|---|']
 for a in analysis:
  if a['event'].startswith('paired_difference'):report.append('|%s/%s|%s minus %s|%s|%.12g|%s|%s|'%(a['gen'],a['concurrency'],a['candidate'],a['baseline'],a['metric'],a['signed_mean'],a['signed_t95'],a['candidate_minus_baseline']))
 report+=['','### All longest-delivery requests (no exclusion)','']
 for mode in meta['modes']:
  rr=sorted([x for x in samples if x['mode']==mode],key=lambda x:x['latency_ms'],reverse=True)[:3]
  report.append(mode+': '+str([{k:x[k] for k in ['pair','gen','index','wave','ttft_ms','latency_ms']} for x in rr]))
 # predeclared first-by-client-start request per wave, descriptive only
 report+=['','### Predeclared cold subset, descriptive TTFT means','']
 for gen,c in meta['matrix']:
  for mode in meta['modes']:
   cold=[];other=[]
   for pair in range(5):
    for wave in range(4):
     rr=sorted([x for x in samples if (x['pair'],x['mode'],x['gen'],x['wave'])==(pair,mode,gen,wave)],key=lambda x:x['start_ns'])
     cold.append(rr[0]['ttft_ms']);other.extend(x['ttft_ms'] for x in rr[1:])
   report.append('%s/%s %s: first-start n=%d mean=%.9f; other n=%d mean=%.9f'%(gen,c,mode,len(cold),statistics.mean(cold),len(other),statistics.mean(other)))
 # whole host fields are present, aggregate first eight conventional fields excluding guest duplicate
 assert all(len(c['host_cpu_ticks_before'])==len(c['host_cpu_ticks_after'])==10 for c in cells)
 report+=['','All cells contain aggregate host ticks (descriptive, no exclusive attribution).']
(p/'reviewer-recomputation.md').write_text('\n'.join(report)+'\n')
print(json.dumps(dict(statuses=statuses,report='reviewer-recomputation.md')))
