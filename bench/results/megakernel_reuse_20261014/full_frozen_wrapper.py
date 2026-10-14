import pathlib,json,subprocess,datetime,os,sys
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y');repo=pathlib.Path('/workspaces/repository');kind=sys.argv[1];assert kind in ['preflight','full']
record=json.loads((r/'common_build_status.json').read_text());env=dict(os.environ,**record['env_overrides'],BF_BIND='127.0.0.1',PYTHONUNBUFFERED='1')
cfg=json.loads((r/'smol_frozen.json').read_text());cmd=[str(r/'common_runtime/bin/python'),str(repo/'bench/results/megakernel_reuse_20261014/matched_serving.py'),'--loop-comparison','--untraced','--reference-path',str(r/'frozen_references.json'),'--model',cfg['model'],'--output',str(r/(kind+'.jsonl'))]
if kind=='preflight':cmd+=['--preflight']
(r/(kind+'.command.json')).write_text(json.dumps({'command':cmd,'cwd':str(repo),'env_overrides':record['env_overrides'],'source':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()}))
with (r/(kind+'.driver.stdout')).open('x') as out,(r/(kind+'.driver.stderr')).open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
(r/(kind+'.exit.json')).write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
if p.returncode:raise SystemExit(p.returncode)
cmd=['/usr/bin/python3',str(repo/'bench/results/megakernel_reuse_20261014/matched_analysis.py'),str(r/(kind+'.jsonl'))]
with (r/(kind+'.analysis.stdout')).open('x') as out,(r/(kind+'.analysis.stderr')).open('x') as err:p=subprocess.run(cmd,stdout=out,stderr=err)
(r/(kind+'.analysis.exit.json')).write_text(json.dumps({'command':cmd,'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
raise SystemExit(p.returncode)
