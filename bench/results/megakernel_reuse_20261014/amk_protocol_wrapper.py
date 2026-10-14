import pathlib,json,subprocess,datetime,os
r=pathlib.Path('/tmp/bpfusion-megakernel-reuse-oxfus39y');repo=pathlib.Path('/workspaces/repository')
status=json.loads((r/'common_setup.exit.json').read_text());assert status['exit']==0
record=json.loads((r/'common_build_status.json').read_text());env=dict(os.environ,**record['env_overrides'],BF_BIND='127.0.0.1',PYTHONUNBUFFERED='1')
cfg=json.loads((r/'smol_frozen.json').read_text())
cmd=[str(r/'common_runtime/bin/python'),str(r/'amk_serving_qualification.py'),'--loop-comparison','--untraced','--reference-path',str(r/'frozen_references.json'),'--correctness','--model',cfg['model'],'--output',str(r/'amk_protocol.jsonl')]
(r/'amk_protocol.command.json').write_text(json.dumps({'command':cmd,'cwd':str(repo),'env_overrides':record['env_overrides'],'oracle':'unchanged pre-observation0045 whole-output pools; stronger eager-HF failure retained separately'}))
with (r/'amk_protocol.stdout').open('x') as out,(r/'amk_protocol.stderr').open('x') as err:p=subprocess.run(cmd,cwd=repo,env=env,stdout=out,stderr=err)
(r/'amk_protocol.exit.json').write_text(json.dumps({'exit':p.returncode,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}))
raise SystemExit(p.returncode)
