from pathlib import Path
from collections import defaultdict,Counter
from bisect import bisect_right
import gzip
import json,re,sys,math
def q(v,p):return sorted(v)[min(len(v)-1,math.ceil(len(v)*p)-1)]
def stats(v):return dict(n=len(v),p50=q(v,.5),p95=q(v,.95),p99=q(v,.99),maximum=max(v)) if v else dict(n=0)
def open_text(path):
 p=Path(path)
 return p.open() if p.exists() else gzip.open(str(p)+'.gz','rt')
def parse(path):
 pat=re.compile(r'^(.*?)\[(\d+)\].*?\s(\d+\.\d+):\s+([^:]+):\s*(.*)$')
 ev=[]
 for l in open_text(path):
  if not l.strip() or l.startswith('#'):continue
  for call in ['sendmsg','recvfrom']:
   if ': sys_'+call+' -> ' in l:l=l.replace(': sys_'+call+' -> ',': sys_exit_'+call+': result=')
   elif ': sys_'+call+'(' in l:l=l.replace(': sys_'+call+'(',': sys_enter_'+call+': (')
  z=pat.match(l);assert z,l
  lead,cpu,ts,event,body=z.groups();pid=re.search(r'-(\d+)\s*$',lead.strip());assert pid,l
  ev.append(dict(ns=round(float(ts)*1e9),pid=int(pid.group(1)),cpu=int(cpu),event=event,body=body))
 return sorted(ev,key=lambda x:x['ns'])
def main(raw):
 raw=Path(raw);rows=[json.loads(l) for l in open_text(raw)]
 reports=[]
 for start in [x for x in rows if x['event']=='start']:
  pair,mode=start['pair'],start['mode']
  prefix=raw.with_suffix('').with_name(raw.stem+f'_p{pair}_{mode}')
  tokens=[json.loads(l) for l in open_text(str(prefix)+'.timeline.tokens.jsonl')]
  requests={x['client_ns']:x for x in rows if x.get('event')=='request' and x['pair']==pair and x['mode']==mode and x.get('kind')=='measured'}
  ev=parse(str(prefix)+'.ftrace.txt')
  markers={};trans=defaultdict(list);calls=defaultdict(list);pending={}
  for e in ev:
   pid=e['pid'];ns=e['ns'];event=e['event'];body=e['body']
   if event=='tracing_mark_write' and body.startswith('BF_CLIENT '):
    m=re.search(r'client_ns=(\d+) tid_ns=(\d+) fd=(\d+)',body);assert m,e
    marker,tid_ns,fd=map(int,m.groups());assert marker not in markers
    markers[marker]=dict(host_tid=pid,namespace_tid=tid_ns,fd=fd,marker_ns=ns)
   elif event=='sched_switch':
    m=re.search(r'prev_pid=(\d+).*?prev_state=(\S+).*?next_pid=(\d+)',body);assert m,e
    prev,state,nxt=m.groups();prev,nxt=int(prev),int(nxt)
    trans[prev].append((ns,'runnable' if state.startswith('R') else 'sleeping'))
    trans[nxt].append((ns,'running'))
   elif event=='sched_wakeup':
    m=re.search(r' pid=(\d+)',body);assert m,e
    target=int(m.group(1))
    if not trans[target] or trans[target][-1][1]!='running':trans[target].append((ns,'runnable'))
   elif event=='sys_enter_recvfrom':
    assert pid not in pending,('overlapping recvfrom',e,pending.get(pid))
    m=re.search(r'fd: (0x[0-9a-f]+|\d+)',body);assert m,e
    pending[pid]=dict(begin_ns=ns,fd=int(m.group(1),0))
   elif event=='sys_exit_recvfrom':
    call=pending.pop(pid,None)
    if call is not None:
     result=int(body.split('result=',1)[1],0)
     if result>=2**63:result-=2**64
     call.update(end_ns=ns,result=result);calls[pid].append(call)
  assert set(markers)==set(requests),(len(markers),len(requests),set(requests)-set(markers))
  def states(pid,begin,end):
   if end<=begin:return dict(negative_or_zero_interval_ns=end-begin)
   events=trans[pid];times=[x[0] for x in events]
   i=bisect_right(times,begin)-1;cursor=begin;out=Counter()
   state=events[i][1] if i>=0 else 'unknown'
   for j in range(i+1,len(events)):
    ts,nxt=events[j]
    if ts>=end:break
    out[state]+=ts-cursor;cursor=ts;state=nxt
   out[state]+=end-cursor
   assert sum(out.values())==end-begin
   return {k+'_ms':v/1e6 for k,v in out.items()}
  by_marker=defaultdict(list)
  for x in tokens:by_marker[x['client_ns']].append(x)
  result_tokens=[];sq_details=[]
  for marker,request in requests.items():
   identity=markers[marker];host_tid=identity['host_tid']
   relevant=[x for x in calls[host_tid] if x['fd']==identity['fd'] and identity['marker_ns']<=x['begin_ns']<=request['finish_ns']]
   received=0;ends=[]
   for call in relevant:
    if call['result']>0:
     begin=received;received+=call['result'];ends.append(dict(offset=begin,end=received,**call))
   header=by_marker[marker][0]['send']['sub']['header']
   assert received==header+64*4,(marker,received,header,len(relevant))
   for x in by_marker[marker]:
    i=x['index'];end=header+(i+1)*4
    covering=[call for call in ends if call['offset']<end<=call['end']];assert len(covering)==1,(marker,i,covering)
    call=covering[0];arrival=x['arrival_ns'];assert arrival+1000>=call['end_ns'],(marker,i,arrival,call)
    z=dict(client_ns=marker,index=i,host_tid=host_tid,arrival_ns=arrival,recv_exit_ns=call['end_ns'],
     after_recv_exit_ms=(arrival-call['end_ns'])/1e6,
     after_recv_states=states(host_tid,call['end_ns'],arrival),
     publication_to_arrival_ms=x['delivery_age_estimate_ms'])
    if mode.startswith('uring'):
     send=x['send'];kernel=send['kernel'];server_pid=kernel['sub']['pid']
     kcomplete=kernel['cq']['ns']
     z.update(kernel_complete_to_recv_exit_ms=(call['end_ns']-kcomplete)/1e6,
      kernel_complete_to_recv_states=states(host_tid,kcomplete,call['end_ns']),
      kernel_complete_to_client_arrival_states=states(host_tid,kcomplete,arrival),
      server_host_tid=server_pid)
     gpu_sq=kernel['sub']['ns']-x['sq_to_kernel_estimate_ms']*1e6
     z.update(sq_to_kernel_thread_states=states(server_pid,gpu_sq,kernel['sub']['ns']))
     sq_details.append(z)
    result_tokens.append(z)
  gaps=[]
  rt={(x['client_ns'],x['index']):x for x in result_tokens}
  for marker,request in requests.items():
   for i in range(1,64):
    now,prev=rt[marker,i],rt[marker,i-1]
    itl=(now['arrival_ns']-prev['arrival_ns'])/1e6
    gaps.append(dict(client_ns=marker,index=i,itl_ms=itl,
     kernel_recv_exit_gap_ms=(now['recv_exit_ns']-prev['recv_exit_ns'])/1e6,
     post_recv_age_change_ms=now['after_recv_exit_ms']-prev['after_recv_exit_ms'],
     current=now,previous=prev))
  threshold=q([x['itl_ms'] for x in gaps],.99);tail=[x for x in gaps if x['itl_ms']>=threshold]
  report=dict(pair=pair,mode=mode,clients=len(markers),tokens=len(result_tokens),itl_p99_ms=threshold,
   after_recv_exit_ms=stats([x['after_recv_exit_ms'] for x in result_tokens]),
   tail_kernel_recv_exit_gap_ms=stats([x['kernel_recv_exit_gap_ms'] for x in tail]),
   tail_post_recv_age_change_ms=stats([x['post_recv_age_change_ms'] for x in tail]),
   largest=sorted(gaps,key=lambda x:-x['itl_ms'])[:30],
   limitations='Scheduler state intervals are associated thread states, not exclusive CPU attribution. Sleeping can include socket wait or interpreter synchronization. GPU/CPU boundary states inherit clock calibration error. No marginal quantile additivity.')
  if sq_details:
   for field in ['kernel_complete_to_recv_exit_ms']:
    report[field]=stats([x[field] for x in sq_details])
   for field in ['sq_to_kernel_thread_states','kernel_complete_to_recv_states','after_recv_states']:
    report[field]={state:stats([x[field].get(state,0) for x in sq_details]) for state in ['running_ms','runnable_ms','sleeping_ms','unknown_ms']}
  reports.append(report)
  Path(str(prefix)+'.scheduler.tokens.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in result_tokens))
 result=dict(scope='Same-token client/syscall and scheduling association from the complete diagnostic; not an uninstrumented speed comparison.',runs=reports)
 Path(str(raw)+'.scheduler.analysis.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
if __name__=='__main__':main(sys.argv[1])
