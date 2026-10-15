import pathlib,json,gzip,sys
t=pathlib.Path(sys.argv[1])
rows=[]
for p in sorted(t.glob('full_*.jsonl')):
 rr=[json.loads(l) for l in p.open()];m=rr[0]
 if m['condition']!='profiled':continue
 d=t/p.stem;log=next(x for x in rr if x['event']=='executor')['stdout']
 cat=json.loads(next(l.split(' ',1)[1] for l in log.splitlines() if l.startswith('GRAPH_CATALOGUE ')))['graphs'];lookup={(x['input_tokens'],x['batch']):x for x in cat}
 cs=[json.loads(l) for l in (d/'model.gpu.jsonl').open()];cs=[x for x in cs if x['event']=='compute']
 ev=json.load(gzip.open(d/'trace.json.gz','rt'))['traceEvents']
 models=sorted((x for x in ev if x.get('cat')=='kernel' and not x.get('name','').startswith(('dispatch(','io_network(','io_initialize('))),key=lambda x:x['ts'])
 expected=sum(sum(lookup[(x['query'],x['batch'])][k].get('0',0) for k in ['body_node_types','head_node_types']) for x in cs)
 out={'case':p.stem,'model':m['model'],'pair':m['pair'],'path':m['path'],'actual_model_kernels':len(models),'expected_model_kernels':expected,'difference':len(models)-expected,'rounds':len(cs)}
 for kind,name in [(1,'gpu_memcpy'),(2,'gpu_memset')]:
  e=sum(sum(lookup[(x['query'],x['batch'])][k].get(str(kind),0) for k in ['body_node_types','head_node_types']) for x in cs)
  a=sum(x.get('cat')==name and x.get('args',{}).get('graph id',0)!=0 for x in ev)
  out[name]={'expected':e,'actual':a}
 rows.append(out)
print(json.dumps(rows))
