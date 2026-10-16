from pathlib import Path
import subprocess,json,os,datetime
t=Path('/tmp/bpfusion-mixed-batching-pa97uj6t');r=Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
cmd=['make', '-f', '/tmp/bpfusion-mixed-batching-pa97uj6t/mixed.Makefile', 'BUILD=/tmp/bpfusion-mixed-batching-pa97uj6t/build_mixed', 'VLLM_PYTHON=/tmp/bpfusion-mixed-batching-pa97uj6t/runtime/bin/python', 'CPPFLAGS=-DBF_LLM_SLOTS=16 -I/workspaces/repository/executor', '/tmp/bpfusion-mixed-batching-pa97uj6t/build_mixed/vllm_graph_uring_loop_trace.so', '/tmp/bpfusion-mixed-batching-pa97uj6t/build_mixed/vllm_graph_user_network_wait_trace.so']
with (t/'trace_rebuild.stdout').open('x') as out,(t/'trace_rebuild.stderr').open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
(t/'trace_rebuild.exit.json').write_text(json.dumps(dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
raise SystemExit(z.returncode)
