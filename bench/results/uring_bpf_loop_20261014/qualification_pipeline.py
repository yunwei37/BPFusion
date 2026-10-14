import pathlib,os,json,subprocess,datetime
repo=pathlib.Path("/workspaces/repository");os.chdir(repo)
root=pathlib.Path("/tmp/bpfusion-uring-loop-frmz3lrm")
preflight=json.loads((root/"preflight_retry2_status.json").read_text())
assert preflight["exit"]==preflight["analysis_exit"]==0
libdir=json.loads((root/"libbpf_dependency.json").read_text())["runtime_lib_dir"]
base_env=dict(os.environ,LD_LIBRARY_PATH=libdir+(":"+os.environ["LD_LIBRARY_PATH"] if os.environ.get("LD_LIBRARY_PATH") else ""))
env=dict(base_env,PATH=str(root/"runtime/bin")+":"+os.environ["PATH"],VLLM_ENABLE_V1_MULTIPROCESSING="0")
commands=json.loads((root/"qualification_commands.json").read_text())[1:]
commands += [["hf_build",["make","qwen-graph-uring-loop"]],["hf_lifecycle",["/usr/bin/python3",str(root/"hf_loop/pipeline.py")]]]
(root/"qualification_complete_commands.json").write_text(json.dumps(commands,indent=2))
records=[]
for name,cmd in commands:
 print("QUALIFICATION_START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 selected_env=base_env if name.startswith("hf_") else env
 with (root/(name+".stdout")).open("w") as a,(root/(name+".stderr")).open("w") as b:p=subprocess.run(cmd,stdout=a,stderr=b,env=selected_env)
 record={"name":name,"cmd":cmd,"exit":p.returncode};records.append(record)
 if p.returncode==0 and not name.startswith("hf_"):
  with (root/(name+"_analysis.stdout")).open("w") as a,(root/(name+"_analysis.stderr")).open("w") as b:q=subprocess.run(["python3","bench/vllm_serving_analysis.py",str(root/(name+".jsonl"))],stdout=a,stderr=b,env=selected_env)
  record["analysis_exit"]=q.returncode
 if p.returncode==0 and name=="hf_lifecycle":
  checks=json.loads((root/"hf_loop/pipeline.status.json").read_text())
  record["hf_lifecycle_pass"]=len(checks)==2 and all(r["exit"]==0 and r["pass"] for r in checks)
 (root/"qualification_status.json").write_text(json.dumps(records,indent=2))
 print(json.dumps(record),flush=True)
 if p.returncode or record.get("analysis_exit",0) or record.get("hf_lifecycle_pass") is False:break
print("QUALIFICATION_PIPELINE_TERMINAL",flush=True)
