from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).resolve().parent;r=Path('/workspaces/repository')
env=dict(os.environ,**json.loads((t/'environment.json').read_text()))
statuses=[]
for banks in [16,8]:
 build=t/('nodelaybuild'+str(banks))
 cmd=['make','-f',str(t/'nodelay.Makefile'),'BUILD='+str(build),'VLLM_PYTHON='+str(t/'runtime/bin/python')]
 if banks==16:cmd+=['CPPFLAGS=-DBF_LLM_SLOTS=16']
 cmd+=['vllm-mixed-uring-loop','vllm-mixed-user-network-wait','vllm-mixed-trace',str(build/'bpfusion_load'),str(build/'fusion.bpf.o')]
 with (t/('nodelay_build'+str(banks)+'.stdout')).open('x') as o,(t/('nodelay_build'+str(banks)+'.stderr')).open('x') as e:z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
 statuses.append(dict(banks=banks,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 (t/'nodelay_build.statuses.json').write_text(json.dumps(statuses,indent=2))
 if z.returncode:break
(t/'nodelay_build.exit.json').write_text(json.dumps(dict(exit=0 if len(statuses)==2 and all(x['exit']==0 for x in statuses) else 1)))
