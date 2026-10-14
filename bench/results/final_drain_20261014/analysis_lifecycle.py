import pathlib,json,re,datetime,sys
p=pathlib.Path(sys.argv[1]);reports=[]
for name in ['smol','qwen']:
 x=json.loads((p/('lifecycle_vllm_'+name)/(name+'.results.json')).read_text())
 assert x['pass'] and x['exit']==0 and not any(x['model_errors'])
 assert not x['remaining_pins'] and len(x['rows'])==32
 s=x['native_stats'];assert s['accepted']==s['closed']==13 and s['head']==s['completed']==32 and s['aborted']==3
 assert all(s[k]==0 for k in ['pending','error','reserved','dropped','overflow','trace_overflow'])
 assert s['sqhead']==s['sqtail'] and s['cqhead']==s['cqtail']
 b=x['bpf_stats'];assert b['exit']==0 and not b['stderr']
 assert re.search(r'^uring recycled\s+32$',b['stdout'],re.M)
 assert re.search(r'^llm_head=32$',b['stdout'],re.M)
 assert re.search(r'^llm_reserved=0x0$',b['stdout'],re.M)
 slots=re.findall(r'^llm\[(\d+)\]: state=(\d+)',b['stdout'],re.M)
 assert sorted((int(i),int(state)) for i,state in slots)==[(i,0) for i in range(8)]
 assert 'CLEANUP ring_connections_buffers_released' in x['stdout']
 assert 'network=coalesced GPU dispatcher; shutdown-only network worker' in x['stdout']
 assert sum(r['checked_tokens'] for r in x['rows'])==652
 reports.append(dict(model=name,checked_complete_or_prefix_tokens=652,physical_model_slots=slots,admission_bitmap='0x0',native_stats=s,
  model_counters=next(l for l in x['stdout'].splitlines() if l.startswith('resident vLLM stopped:'))))
print(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),models=reports,
 quiescence_evidence='Successful shutdown and retained source setting model_quiesced before shutdown-only worker; no direct live sampling of that field after I/O state was freed.'),indent=2))
