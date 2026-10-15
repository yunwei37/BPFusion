import pathlib,json,re,sys
p=pathlib.Path(sys.argv[1]);reports=[]
for name in ['smol','qwen']:
 for path in ['loop','native']:
  x=json.loads((p/('lifecycle_'+name+'_'+path)/(name+'.results.json')).read_text())
  assert x['pass'] and x['exit']==0 and x['model_errors']==[0] and not x['remaining_pins']
  assert len(x['rows'])==32 and sum(z['checked_tokens'] for z in x['rows'])==652
  assert all(z['exact'] for z in x['rows'])
  s=x['native_stats']
  if path=='loop':
   assert s['accepted']==s['closed']==13 and s['head']==s['completed']==32 and s['aborted']==3
   assert all(s[k]==0 for k in ['pending','error','reserved','dropped','overflow','trace_overflow'])
   assert s['sqhead']==s['sqtail'] and s['cqhead']==s['cqtail']
   b=x['bpf_stats'];assert b['exit']==0 and not b['stderr']
   for pattern in [r'^uring recycled\s+32$',r'^llm_head=32$',r'^llm_reserved=0x0$']:assert re.search(pattern,b['stdout'],re.M)
   assert sorted((int(i),int(v)) for i,v in re.findall(r'^llm\[(\d+)\]: state=(\d+)',b['stdout'],re.M))==[(i,0) for i in range(8)]
   assert 'CLEANUP ring_connections_buffers_released' in x['stdout']
  else:assert s=={'accepted':13,'published':32,'completed':31,'rejected':10}
  reports.append({'model':name,'path':path,'checked_complete_or_prefix_tokens':652,'native_stats':s,'model_errors':x['model_errors']})
print(json.dumps(reports,indent=2))
