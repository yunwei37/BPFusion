import os,pathlib,subprocess,json,datetime
os.chdir("/workspaces/repository")
r=pathlib.Path("/tmp/bpfusion-vllm-uring-q26fqorc")
env=dict(os.environ,PATH=str(r/"runtime/bin")+":"+os.environ["PATH"],VLLM_ENABLE_V1_MULTIPROCESSING="0")
models={'qwen': '/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775', 'smol': '/workspaces/.cache/huggingface/hub/models--HuggingFaceTB--SmolLM2-135M/snapshots/93efa2f097d58c2a74874c7e644dbc9b0cee75a2'}
base=[str(r/"runtime/bin/python"),"bench/vllm_serving.py","--transport-comparison","--untraced","--reference-path",str(r/"transport_frozen_references.json")]
commands=[("transport_build",["make","vllm-graph","vllm-graph-user-network-wait","vllm-graph-uring","VLLM_PYTHON="+str(r/"runtime/bin/python")]),
 ("transport_preflight",base+["--preflight","--model",models["qwen"],"--output",str(r/"transport_preflight.jsonl")])]
commands += [(name+"_transport_correctness",base+["--correctness","--model",models[name],"--output",str(r/(name+"_transport_correctness.jsonl"))]) for name in ("qwen","smol")]
(r/"transport_qualification_commands.json").write_text(json.dumps(commands,indent=2))
status=[]
for name,cmd in commands:
 print("START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 with (r/(name+".stdout")).open("w") as out,(r/(name+".stderr")).open("w") as err:p=subprocess.run(cmd,stdout=out,stderr=err,env=env)
 record=dict(name=name,cmd=cmd,exit=p.returncode);status.append(record)
 if p.returncode==0 and name!="transport_build":
  analysis=["python3","bench/vllm_serving_analysis.py",str(r/(name+".jsonl"))]
  with (r/(name+"_analysis.stdout")).open("w") as out,(r/(name+"_analysis.stderr")).open("w") as err:q=subprocess.run(analysis,stdout=out,stderr=err,env=env)
  record["analysis_exit"]=q.returncode
 (r/"transport_qualification_status.json").write_text(json.dumps(status,indent=2));print(json.dumps(record),flush=True)
 if p.returncode or record.get("analysis_exit",0):break
print("QUALIFICATION_PIPELINE_TERMINAL",flush=True)
