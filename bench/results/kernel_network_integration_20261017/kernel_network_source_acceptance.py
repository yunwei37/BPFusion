from pathlib import Path
import subprocess,json,os,datetime,time
t=Path(__file__).resolve().parent;r=Path("/workspaces/repository")
env=dict(os.environ,**json.loads((t/"environment.json").read_text()))
models=json.loads((t/"models.json").read_text());statuses=[]
for name in ["qwen","smol"]:
 cmd=[str(t/"runtime/bin/python"),str(t/"kernel_network_source_protocol_load.py"),"--model",models[name],"--output",str(t/(name+"_kernel_network_source_protocol8.jsonl")),"--correctness","--banks","8"]
 print("START protocol",name,flush=True)
 with (t/(name+"_kernel_network_source_protocol8.stdout")).open("x") as o,(t/(name+"_kernel_network_source_protocol8.stderr")).open("x") as e:z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
 rec=dict(stage="protocol",model=name,command=cmd,exit=z.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 if z.returncode==0:
  ac=["/usr/bin/python3",str(t/"protocol_analysis.py"),str(t/(name+"_kernel_network_source_protocol8.jsonl"))]
  with (t/(name+"_kernel_network_source_protocol8.analysis.stdout")).open("x") as o,(t/(name+"_kernel_network_source_protocol8.analysis.stderr")).open("x") as e:az=subprocess.run(ac,cwd=r,stdout=o,stderr=e)
  rec.update(analysis_command=ac,analysis_exit=az.returncode)
 statuses.append(rec);(t/"kernel_network_source_acceptance.statuses.json").write_text(json.dumps(statuses,indent=2));print("TERMINAL",rec,flush=True)
 if z.returncode or rec.get("analysis_exit",0):break
 for condition in ["loop"]:
  cmd=[str(t/"runtime/bin/python"),str(t/"kernel_network_source_lifecycle.py"),condition,name,"8","vllm"]
  print("START ordinary",name,condition,flush=True)
  tag=name+"_"+condition
  with (t/("kernel_network_source_ordinary_"+tag+".stdout")).open("x") as o,(t/("kernel_network_source_ordinary_"+tag+".stderr")).open("x") as e:z=subprocess.run(cmd,cwd=r,env=env,stdout=o,stderr=e)
  p=t/("lifecycle_kernel_network_source_vllm_"+name+"_8_"+condition)/(name+".results.json")
  result=json.loads(p.read_text()) if p.exists() else {}
  rec=dict(stage="ordinary",model=name,condition=condition,command=cmd,exit=z.returncode,passed=result.get("pass",False),utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
  statuses.append(rec);(t/"kernel_network_source_acceptance.statuses.json").write_text(json.dumps(statuses,indent=2));print("TERMINAL",rec,flush=True)
  assert not list(Path("/sys/fs/bpf").glob("bpfusion*"))
  if z.returncode or not rec["passed"]:break
 if any(x["exit"] or x.get("analysis_exit",0) or x.get("passed",True)==False for x in statuses):break
ok=len(statuses)==4 and all(x["exit"]==0 and x.get("analysis_exit",0)==0 and x.get("passed",True) for x in statuses)
(t/"kernel_network_source_acceptance.exit.json").write_text(json.dumps(dict(exit=0 if ok else 1,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())))
raise SystemExit(0 if ok else 1)
