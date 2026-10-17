from pathlib import Path
import subprocess,json,os,datetime
t=Path(__file__).parent;r=Path("/workspaces/repository");b=t/"kernel_network_graph8"
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
cmd=["make","-f",str(t/"kernel_network_graph_draft/Makefile"),"BUILD="+str(b),"CPPFLAGS=-I"+str(t/"kernel_owned_tcp_prototype")+" -I"+str(r/"executor"),"graph-server-uring-loop","graph-server-user-network-wait",str(b/"fusion.bpf.o"),str(b/"bpfusion_load")]
with (t/"kernel_network_graph_build.stdout").open("x") as o,(t/"kernel_network_graph_build.stderr").open("x") as e:z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
(t/"kernel_network_graph_build.exit.json").write_text(json.dumps(dict(command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()),indent=2))
