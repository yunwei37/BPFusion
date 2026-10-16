from pathlib import Path
import json,subprocess,os,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
make=t/'fixed.Makefile';make.write_text((r/'Makefile').read_text().replace('executor/vllm_graph.cu',str(t/'fixed_sources/vllm_graph.cu')))
statuses=[]
for banks in [8,16]:
 build=t/('build_fixed'+str(banks));names=['vllm_graph_uring_loop','vllm_graph_user_network_wait','vllm_graph_uring_loop_trace','vllm_graph_user_network_wait_trace']
 cmd=['make','-f',str(make),'BUILD='+str(build),'VLLM_PYTHON='+str(t/'runtime/bin/python'),'CPPFLAGS='+('-DBF_LLM_SLOTS=16 ' if banks==16 else '')+'-I'+str(r/'executor')]
 cmd += [str(build/'fusion.bpf.o'),str(build/'uring_loop.bpf.o'),str(build/'bpfusion_load')]+[str(build/(n+s)) for n in names for s in ['.so','']]
 with (t/('fixed_build'+str(banks)+'.stdout')).open('x') as out,(t/('fixed_build'+str(banks)+'.stderr')).open('x') as err:z=subprocess.run(cmd,cwd=r,env=env,stdout=out,stderr=err)
 statuses.append(dict(banks=banks,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));(t/'fixed_build.statuses.json').write_text(json.dumps(statuses,indent=2))
 if z.returncode:break
 for n in names:
  p=build/n;p.unlink();p.symlink_to(t/'mixed_vllm_graph.py')
ok=len(statuses)==2 and all(x['exit']==0 for x in statuses)
(t/'fixed_build.exit.json').write_text(json.dumps(dict(exit=0 if ok else 1)))
