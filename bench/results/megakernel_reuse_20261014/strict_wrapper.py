import pathlib,json,subprocess,datetime,os
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y');repo=pathlib.Path('/workspaces/repository')
cfg=json.loads((r/'smol_frozen.json').read_text());record=json.loads((r/'amk_build_status.json').read_text())
for condition in ['native','loop']:
 key='strict_'+condition;case=r/key;case.mkdir()
 env=dict(os.environ,**record['env_overrides'],BF_BIND='127.0.0.1',PYTHONUNBUFFERED='1',AMK_CASE_DIR=str(case))
 name='amk_graph_user_network_wait' if condition=='native' else 'amk_graph_uring_loop'
 cmd=['/usr/bin/python3',str(r/'strict_adapter.py'),'--executor',str(repo/'build'/name),'--model',cfg['model'],'--gen','64','--prefill-edges']
 (r/(key+'.command.json')).write_text(json.dumps({'command':cmd,'cwd':str(repo),'env_overrides':record['env_overrides'],'case':str(case)}))
 with (r/(key+'.stdout')).open('x') as out,(r/(key+'.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
 (r/(key+'.exit.json')).write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
 if p.returncode:raise SystemExit(p.returncode)
