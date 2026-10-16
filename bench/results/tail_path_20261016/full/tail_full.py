from pathlib import Path
import subprocess,json,os,datetime,sys
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
assert json.loads((t/'tail_preflight.status.json').read_text())['exit']==0
assert json.loads((t/'tail_preflight.analysis.retry1.json').read_text())['exit']==0
assert not list(Path('/sys/fs/bpf').glob('bpfusion*'))
archive=r/'bench/results/tail_path_20261016';frozen=archive/'diagnostic_full_sources_buffer_repair';frozen.mkdir()
for n in ['tail_diagnostic.py','analyze_timeline.py','tail_ftrace.py','resident_dispatch.py','mixed_vllm_graph.py','mixed_replay.py','timeline.Makefile','environment.json','timeline_build_command.json','preflight-deviations.md']:
 (frozen/n).write_bytes((t/n).read_bytes())
for f in (t/'diagnostic_sources').iterdir():(frozen/f.name).write_bytes(f.read_bytes())
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
cmd=[str(t/'runtime/bin/python'),str(t/'tail_diagnostic.py'),'--model',json.loads((t/'models.json').read_text())['qwen'],'--output',str(t/'tail_full.jsonl'),'--banks','16']
with (t/'tail_full.stdout').open('x') as out,(t/'tail_full.stderr').open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
status=dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
if z.returncode==0:
 ac=['/usr/bin/python3',str(t/'analyze_timeline.py'),str(t/'tail_full.jsonl')]
 with (t/'tail_full.analysis.stdout').open('x') as out,(t/'tail_full.analysis.stderr').open('x') as err:zz=subprocess.run(ac,cwd=r,stdout=out,stderr=err)
 status.update(analysis_command=ac,analysis_exit=zz.returncode)
(t/'tail_full.status.json').write_text(json.dumps(status,indent=2));print('TERMINAL',status,flush=True)
sys.exit(z.returncode or status.get('analysis_exit',0))
