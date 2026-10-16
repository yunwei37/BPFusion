from pathlib import Path
import subprocess,json,os,time,sys,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
print('WAIT default8 protocol validation',flush=True)
while not (t/'protocol8.exit.json').exists():time.sleep(1)
assert json.loads((t/'protocol8.exit.json').read_text())['exit']==0,(t/'protocol8.stdout').read_text()
assert not list(Path('/sys/fs/bpf').glob('bpfusion*'))
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
names=['vllm_graph_uring_loop_trace','vllm_graph_user_network_wait_trace']
for n in names:
 p=t/'build_timeline16'/n;p.unlink();p.symlink_to(t/'mixed_vllm_graph.py')
archive=r/'bench/results/tail_path_20261016'
frozen=archive/'diagnostic_preflight_sources';frozen.mkdir()
for n in ['tail_diagnostic.py','analyze_timeline.py','tail_ftrace.py','resident_dispatch.py','mixed_vllm_graph.py','mixed_replay.py','timeline.Makefile','environment.json','timeline_build_command.json']:
 (frozen/n).write_bytes((t/n).read_bytes())
for f in (t/'diagnostic_sources').iterdir():(frozen/f.name).write_bytes(f.read_bytes())
cmd=[str(t/'runtime/bin/python'),str(t/'tail_diagnostic.py'),'--model',json.loads((t/'models.json').read_text())['qwen'],'--output',str(t/'tail_preflight.jsonl'),'--preflight','--banks','16']
print('START',cmd,flush=True)
with (t/'tail_preflight.stdout').open('x') as out,(t/'tail_preflight.stderr').open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
status=dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
if z.returncode==0:
 cmd=['/usr/bin/python3',str(t/'analyze_timeline.py'),str(t/'tail_preflight.jsonl')]
 with (t/'tail_preflight.analysis.stdout').open('x') as out,(t/'tail_preflight.analysis.stderr').open('x') as err:zz=subprocess.run(cmd,cwd=r,stdout=out,stderr=err)
 status.update(analysis_command=cmd,analysis_exit=zz.returncode)
(t/'tail_preflight.status.json').write_text(json.dumps(status,indent=2));print('TERMINAL',status,flush=True)
sys.exit(z.returncode or status.get('analysis_exit',0))
