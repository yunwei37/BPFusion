import pathlib,os,json,subprocess,datetime,gzip,sys
t=pathlib.Path(__file__).parent;repo=pathlib.Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()),BF_DIAGNOSTIC_PROFILE='1')
cfg=json.loads((t/'smol_frozen.json').read_text())
status=[]
for backend in ['amk','vllm']:
 prefix='mechanism_'+backend
 command=[str(t/'runtime/bin/python'),str(t/'observed_serving.py'),'--backend',backend,'--loop-comparison','--preflight','--untraced','--reference-path',str(t/'frozen_references.json'),'--model',cfg['model'],'--output',str(t/(prefix+'.jsonl'))]
 with (t/(prefix+'.driver.stdout')).open('x') as out,(t/(prefix+'.driver.stderr')).open('x') as err:
  result=subprocess.run(command,cwd=repo,env=env,stdout=out,stderr=err)
 status.append(dict(command=command,exit=result.returncode))
 if result.returncode:
  (t/'mechanism.exit.json').write_text(json.dumps(dict(exit=result.returncode,status=status)))
  raise SystemExit(result.returncode)
 case=t/(prefix+'_p0_uring_loop_coalesced')
 trace=json.loads(gzip.open(case/'trace.json.gz','rt').read())
 kernels=[e for e in trace['traceEvents'] if e.get('cat')=='kernel']
 io=[e for e in kernels if e['name'].startswith('io_network(')]
 init=[e for e in kernels if e['name'].startswith('io_initialize(')]
 models=[e for e in kernels if not any(e['name'].startswith(n) for n in ['io_network(','io_initialize(','dispatch('])]
 assert len(io)==len(init)==1,(backend,len(io),len(init))
 assert models and init[0]['ts']+init[0]['dur']<=min(e['ts'] for e in models)
 assert io[0]['ts']>=max(e['ts']+e['dur'] for e in models)
 status[-1].update(network_kernel=io[0],initialize_kernel=init[0],model_activity_records=len(models),
                   network_after_model_region=True,scope='independent network worker absence during observed model execution; no graph identity/overlap mediator claim')
(t/'mechanism.exit.json').write_text(json.dumps(dict(exit=0,status=status,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
