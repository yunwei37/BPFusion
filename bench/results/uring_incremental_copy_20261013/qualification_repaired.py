import os,pathlib,subprocess,json,datetime
os.chdir("/workspaces/repository")
r=pathlib.Path('/tmp/bpfusion-uring-copy-6wpl3780/repaired')
origin=r.parent
r.mkdir(exist_ok=True)
env=dict(os.environ,PATH=str(origin/"runtime/bin")+":"+os.environ["PATH"],VLLM_ENABLE_V1_MULTIPROCESSING="0")
models={'qwen': '/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775', 'smol': '/workspaces/.cache/huggingface/hub/models--HuggingFaceTB--SmolLM2-135M/snapshots/93efa2f097d58c2a74874c7e644dbc9b0cee75a2'}
base=[str(origin/"runtime/bin/python"),"bench/vllm_serving.py","--copy-comparison"]
fixed=["--untraced","--reference-path",str(origin/"frozen_references.json")]
commands=[("build",["make","probes","tools","vllm-graph-uring","vllm-graph-uring-full-copy","vllm-graph-user-network-wait","vllm-graph-trace","VLLM_PYTHON="+str(origin/"runtime/bin/python")]),("preflight",base+fixed+["--preflight","--model",models["qwen"],"--output",str(r/"preflight.jsonl")])]
commands += [(name+"_traced_correctness",base+["--correctness","--model",models[name],"--output",str(r/(name+"_traced_correctness.jsonl"))]) for name in ("qwen","smol")]
commands += [(name+"_correctness",base+fixed+["--correctness","--model",models[name],"--output",str(r/(name+"_correctness.jsonl"))]) for name in ("qwen","smol")]
commands += [("hf_build",["make","qwen-graph-uring"]),("hf_lifecycle",["python3",str(origin/"hf_repaired/pipeline.py")])]
(r/"qualification_commands.json").write_text(json.dumps(commands,indent=2))
status=[]
for name,cmd in commands:
 print("START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 with (r/(name+".stdout")).open("w") as out,(r/(name+".stderr")).open("w") as err:p=subprocess.run(cmd,stdout=out,stderr=err,env=dict(os.environ) if name.startswith("hf_") else env)
 record=dict(name=name,cmd=cmd,exit=p.returncode);status.append(record)
 if p.returncode==0 and name not in ("build","hf_build","hf_lifecycle"):
  with (r/(name+"_analysis.stdout")).open("w") as out,(r/(name+"_analysis.stderr")).open("w") as err:q=subprocess.run(["python3","bench/vllm_serving_analysis.py",str(r/(name+".jsonl"))],stdout=out,stderr=err,env=dict(os.environ) if name.startswith("hf_") else env)
  record["analysis_exit"]=q.returncode
 if p.returncode==0 and name=="hf_lifecycle":
  checked=json.loads((origin/"hf_repaired/pipeline.status.json").read_text())
  assert len(checked)==2 and all(x["exit"]==0 and x["pass"] for x in checked),checked
  record["lifecycle_verified"]=True
 (r/"qualification_status.json").write_text(json.dumps(status,indent=2));print(json.dumps(record),flush=True)
 if p.returncode or record.get("analysis_exit",0):break
print("QUALIFICATION_PIPELINE_TERMINAL",flush=True)
