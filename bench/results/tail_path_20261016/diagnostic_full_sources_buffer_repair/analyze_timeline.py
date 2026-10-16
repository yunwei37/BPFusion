from pathlib import Path
from collections import defaultdict,Counter,deque
import json,sys,re,math,statistics
def quantile(v,p):
 assert v
 return sorted(v)[min(len(v)-1,math.ceil(len(v)*p)-1)]
def summary(v):
 return dict(n=len(v),p50=quantile(v,.5),p95=quantile(v,.95),p99=quantile(v,.99),maximum=max(v)) if v else dict(n=0)
def analyze(raw_path):
 raw_path=Path(raw_path);rows=[json.loads(l) for l in raw_path.open()]
 meta=next(x for x in rows if x['event']=='metadata')
 out=[]
 for start in [x for x in rows if x['event']=='start']:
  pair,mode=start['pair'],start['mode']
  prefix=raw_path.with_suffix('').with_name(raw_path.stem+f'_p{pair}_{mode}')
  tp=Path(str(prefix)+'.gpu.jsonl.timeline.jsonl')
  timeline=[json.loads(l) for l in tp.open()]
  term=timeline[-1];assert term['event']=='terminal' and term['gpu_count']<=term['capacity'] and term['cpu_overflow']==0
  assert sum(x.get('clock')=='gpu_globaltimer' for x in timeline)==term['gpu_count']
  assert sum(x.get('clock')=='host_monotonic' for x in timeline)==term['cpu_count']
  calibration={}
  for kind in [100,101]:
   cc=[x for x in timeline if x.get('kind')==kind];assert len(cc)==16
   assert all(x['client_ns']<=x['previous_ns'] for x in cc)
   b=min(cc,key=lambda x:x['previous_ns']-x['client_ns'])
   calibration[kind]=dict(gpu=b['ns'],low=b['client_ns']-b['ns'],high=b['previous_ns']-b['ns'],
     width_ns=b['previous_ns']-b['client_ns'])
  b0,b1=calibration[100],calibration[101];assert b1['gpu']>b0['gpu']
  def offset(g):
   alpha=(g-b0['gpu'])/(b1['gpu']-b0['gpu'])
   assert -.01<=alpha<=1.01,(g,b0,b1)
   center0=(b0['low']+b0['high'])/2;center1=(b1['low']+b1['high'])/2
   return center0*(1-alpha)+center1*alpha
  def host(x):return x['ns']+offset(x['ns']) if x['clock']=='gpu_globaltimer' else x['ns']
  uncertainty=max(b0['width_ns'],b1['width_ns'])/2+1000
  refs=[json.loads(l) for l in Path(str(prefix)+'.gpu.jsonl.references.jsonl').open()]
  requests=[x for x in rows if x.get('event')=='request' and x['pair']==pair and x['mode']==mode and x.get('kind')=='measured']
  errors=[x for x in rows if x.get('event') in ['request_error','request_invalid'] and x['pair']==pair and x['mode']==mode]
  wanted={x['client_ns']:x for x in requests};assert len(wanted)==len(requests)
  publications=defaultdict(dict);launches=defaultdict(dict)
  for x in timeline:
   if x.get('kind')==1:
    assert x['offset'] not in publications[x['client_ns']]
    publications[x['client_ns']][x['offset']]=x
   elif x.get('kind')==2:
    assert x['offset'] not in launches[x['client_ns']]
    launches[x['client_ns']][x['offset']]=x
  for ref in refs:
   p=publications[ref['client_ns']];launch=launches[ref['client_ns']]
   assert set(p)==set(launch)==set(range(ref['gen'])),(ref['id'],len(p),len(launch))
   assert all(p[i]['ns']>=launch[i]['ns'] for i in p)
  gpu=mode.startswith('uring')
  network=[x for x in timeline if x.get('kind') in [3,4]]
  network.sort(key=lambda x:x['ns'])
  sends=[];pending=defaultdict(deque)
  for x in network:
   key=(x['client_ns'],x['tag']) if gpu else x['client_ns']
   if x['kind']==3:pending[key].append(x)
   else:
    assert pending[key],('CQ without GPU/CPU submission',x)
    sub=pending[key].popleft()
    assert sub['offset']==x['offset'] and sub['header']==x['header']
    assert x['ns']>=sub['ns']
    assert x['result']<=sub['length']
    sends.append(dict(sub=sub,cq=x))
  assert not any(pending.values()),[(k,len(v)) for k,v in pending.items() if v]
  ftrace_meta=json.loads(Path(str(prefix)+'.ftrace.json').read_text())
  assert ftrace_meta['reader_error'] is None
  for cpu,txt in ftrace_meta['stats'].items():
   for line in txt.splitlines():
    k,sep,v=line.partition(':')
    if k.strip() in ['overrun','commit overrun','dropped events']:assert int(v)==0,(cpu,k,v)
  events=[];unparsed=[]
  pattern=re.compile(r'^(.*?)\[(\d+)\].*?\s(\d+\.\d+):\s+([^:]+):\s*(.*)$')
  with Path(str(prefix)+'.ftrace.txt').open() as h:
   for line in h:
    if not line.strip() or line.startswith('#'):continue
    if ': sys_sendmsg -> ' in line:line=line.replace(': sys_sendmsg -> ',': sys_exit_sendmsg: result=')
    elif ': sys_sendmsg(' in line:line=line.replace(': sys_sendmsg(',': sys_enter_sendmsg: (')
    elif ': sys_recvfrom -> ' in line:line=line.replace(': sys_recvfrom -> ',': sys_exit_recvfrom: result=')
    elif ': sys_recvfrom(' in line:line=line.replace(': sys_recvfrom(',': sys_enter_recvfrom: (')
    z=pattern.match(line)
    if not z:unparsed.append(line);continue
    lead,cpu,stamp,event,body=z.groups()
    ns=round(float(stamp)*1e9)
    pid_match=re.search(r'-(\d+)\s*$',lead.strip())
    events.append(dict(ns=ns,cpu=int(cpu),pid=int(pid_match.group(1)) if pid_match else None,event=event,body=body))
  assert not unparsed,unparsed[:3]
  kernel_by_tag=defaultdict(list);active={};async_by_req=defaultdict(list)
  for e in events:
   if e['event'] in ['io_uring_submit_req','io_uring_complete','io_uring_queue_async_work']:
    z=re.search(r'ring (\S+), (?:req|request) (\S+), user_data 0x([0-9a-f]+)',e['body'])
    assert z,e
    ring,req,tag=z.groups();tag=int(tag,16)
    if not (tag>>56==3 or tag>>48==0xbff0):continue
    key=(ring,req)
    if e['event']=='io_uring_submit_req':
     assert key not in active,(key,active.get(key),e)
     active[key]=dict(sub=e,tag=tag,async_work=[])
    elif e['event']=='io_uring_queue_async_work':
     assert key in active,(key,e)
     active[key]['async_work'].append(e)
    else:
     assert key in active,(key,e)
     item=active.pop(key);assert item['tag']==tag
     item['cq']=e;item['result']=int(re.search(r'result (-?\d+)',e['body']).group(1))
     kernel_by_tag[tag].append(item)
  if gpu:
   measured_sends=[s for s in sends if s['sub']['client_ns'] in wanted]
   for s in measured_sends:
    tag=s['sub']['tag'];assert kernel_by_tag[tag],('missing kernel send',tag,s)
    k=kernel_by_tag[tag].pop(0);assert k['result']==s['cq']['result'],(k,s)
    s['kernel']=k
    assert k['sub']['ns']+uncertainty>=s['sub']['begin_ns']+offset(s['sub']['begin_ns']),('SQ/CPU causal mismatch',s,uncertainty)
    assert host(s['cq'])+uncertainty>=k['cq']['ns'],('CQ causal mismatch',s,uncertainty)
   assert not any(kernel_by_tag.values()),'unmatched kernel send events'
   assert not active,'incomplete measured kernel sends'
  by_client=defaultdict(list)
  for s in sends:
   if s['cq']['result']>0:by_client[s['sub']['client_ns']].append(s)
  token_rows=[];gap_rows=[]
  for marker,row in wanted.items():
   assert len(row['arrival_ns'])==len(row['tokens'])==64
   pub=publications[marker];launch=launches[marker]
   assert len(pub)==64
   for i in range(64):
    candidates=[s for s in by_client[marker] if s['sub']['offset']<s['sub']['header']+(i+1)*4<=s['sub']['offset']+s['cq']['result']]
    assert len(candidates)==1,(marker,i,len(candidates))
    s=candidates[0];p=pub[i];a=row['arrival_ns'][i]
    z=dict(client_ns=marker,index=i,arrival_ns=a,production_gpu_ns=p['ns'],production_host_estimate_ns=host(p),
     launch_to_publication_ms=(p['ns']-launch[i]['ns'])/1e6,
     publication_to_send_estimate_ms=(host(s['sub'])-host(p))/1e6,
     send_to_consumed_ms=(s['cq']['ns']-s['sub']['ns'])/1e6,
     delivery_age_estimate_ms=(a-host(p))/1e6,send=s)
    if gpu:
     k=s['kernel']
     z.update(sq_to_kernel_estimate_ms=(k['sub']['ns']-host(s['sub']))/1e6,
       kernel_submit_to_complete_ms=(k['cq']['ns']-k['sub']['ns'])/1e6,
       complete_to_gpu_consumed_estimate_ms=(host(s['cq'])-k['cq']['ns'])/1e6,
       client_after_kernel_complete_ms=(a-k['cq']['ns'])/1e6,
       io_wq_queued=len(k['async_work']),
       previous_gpu_progress_gap_ms=(s['sub']['ns']-s['sub']['previous_ns'])/1e6)
    token_rows.append(z)
    if i:
     prev=pub[i-1];itl=(a-row['arrival_ns'][i-1])/1e6;pgap=(p['ns']-prev['ns'])/1e6
     gap_rows.append(dict(client_ns=marker,index=i,itl_ms=itl,production_gap_ms=pgap,
      delivery_age_change_estimate_ms=itl-(host(p)-host(prev))/1e6,token=z))
  threshold=quantile([x['itl_ms'] for x in gap_rows],.99)
  tail=[x for x in gap_rows if x['itl_ms']>=threshold]
  token_fields=['launch_to_publication_ms','publication_to_send_estimate_ms','send_to_consumed_ms','delivery_age_estimate_ms']
  if gpu:token_fields+=['sq_to_kernel_estimate_ms','kernel_submit_to_complete_ms','complete_to_gpu_consumed_estimate_ms','client_after_kernel_complete_ms','previous_gpu_progress_gap_ms']
  report=dict(pair=pair,mode=mode,requests=len(requests),errors=errors,calibration=calibration,
   clock_alignment_assumption='Affine interpolation between measured start/end calibration brackets; interval estimates below error bound unresolved.',
   alignment_half_width_ns=uncertainty,offset_drift_ns=(b1['low']+b1['high']-b0['low']-b0['high'])/2,
   events=Counter(x['event'] for x in events),gpu_terminal=term,itl_p99_ms=threshold,
   stages={k:summary([x[k] for x in token_rows]) for k in token_fields},
   p99_tail=dict(n=len(tail),production_gap_ms=summary([x['production_gap_ms'] for x in tail]),
    delivery_age_change_estimate_ms=summary([x['delivery_age_change_estimate_ms'] for x in tail])),
   largest_gaps=sorted(gap_rows,key=lambda x:-x['itl_ms'])[:30])
  Path(str(prefix)+'.timeline.tokens.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in token_rows))
  Path(str(prefix)+'.timeline.gaps.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in gap_rows))
  out.append(report)
 result=dict(scope='Causal timeline diagnostic; instrumented paths are not performance claims.',runs=out)
 Path(str(raw_path)+'.timeline.analysis.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
if __name__=='__main__':analyze(sys.argv[1])
