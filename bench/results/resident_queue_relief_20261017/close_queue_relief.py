from pathlib import Path
import subprocess,json,os,datetime
r=Path("/workspaces/repository");t=Path("/tmp/bpfusion-mixed-integration-n4cog5c6");a=r/"bench/results/resident_queue_relief_20261017";root=a/"queue_relief_full"
assert json.loads((root/"analysis_exit.json").read_text())["exit"]==0
env=dict(os.environ,PYTHONDONTWRITEBYTECODE="1")
def run(name,cmd):
 with (a/(name+".stdout")).open("x") as o,(a/(name+".stderr")).open("x") as e:
  z=subprocess.run(cmd,env=env,stdout=o,stderr=e,cwd=r)
 (a/(name+".exit.json")).write_text(json.dumps(dict(command=cmd,exit=z.returncode)))
 assert z.returncode==0,(a/(name+".stderr")).read_text()[-3000:]
 print("PASS",name,flush=True)
run("full_archive_replay",["/usr/bin/python3",str(a/"queue_relief_analysis.py"),str(root)])
same=(a/"full_archive_replay.stdout").read_bytes()==(root/"analysis.stdout").read_bytes()
assert same and not (a/"full_archive_replay.stderr").read_bytes()
(a/"full_archive_replay.json").write_text(json.dumps(dict(byte_identical=same,stderr_empty=True),indent=2))
run("owner_audit",["/usr/bin/python3",str(a/"owner_audit.py"),str(root)])
run("resource_context",["/usr/bin/python3",str(a/"resource_context.py"),str(root)])
sources=[];frozen="f7ac3d00e99d9c7d176144b0a85ed827e2a2dc26"
for p in root.glob("*.server_started.json"):
 m=json.loads(p.read_text())
 assert m["server_source"]==subprocess.check_output(["git","show",frozen+":executor/vllm_mixed.cu"],cwd=r,text=True)
 for group in ["network_sources","bpf_sources"]:
  for path,source in m[group].items():
   assert source==subprocess.check_output(["git","show",frozen+":"+path],cwd=r,text=True),path
 sources.append(dict(file=p.name,metadata_commit=m["source_commit"],frozen_serving_sources_equal=True))
assert len(sources)==15
codepaths=["executor","bpf","Makefile","examples/torch_graph_server.py"]
changed=subprocess.check_output(["git","diff","--name-only",frozen,"--",*codepaths],cwd=r,text=True)
assert not changed,changed
(a/"source_freeze_audit.json").write_text(json.dumps(dict(frozen=frozen,cells=sources,current_source_diff_empty=True),indent=2))
env.update(json.loads((t/"environment.json").read_text()));env["PYTHONPATH"]=str(t/"plot_runtime")
run("queue_relief_plot",[str(t/"runtime/bin/python"),str(a/"queue_relief_plot.py"),str(a)])
print("TERMINAL queue relief archive/source/owner audits",flush=True)
