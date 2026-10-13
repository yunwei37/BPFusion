import os,pathlib,subprocess,json,datetime,sys
os.chdir("/workspaces/repository")
r=pathlib.Path("/tmp/bpfusion-uring-copy-6wpl3780")
base_env=dict(os.environ)
env=dict(base_env,PATH=str(r/"runtime/bin")+":"+base_env["PATH"],VLLM_ENABLE_V1_MULTIPROCESSING="0")
models={"qwen":"/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775","smol":"/workspaces/.cache/huggingface/hub/models--HuggingFaceTB--SmolLM2-135M/snapshots/93efa2f097d58c2a74874c7e644dbc9b0cee75a2"}
base=[str(r/"runtime/bin/python"),"bench/vllm_serving.py","--copy-comparison"]
fixed=["--untraced","--reference-path",str(r/"frozen_references.json")]
commands=[("smol_plain_traced_correctness",base+["--correctness","--model",models["smol"],"--output",str(r/"smol_plain_traced_correctness.jsonl")])]
commands += [(name+"_plain_correctness",base+fixed+["--correctness","--model",models[name],"--output",str(r/(name+"_plain_correctness.jsonl"))]) for name in ("qwen","smol")]
commands += [("hf_build",["make","qwen-graph-uring"]),("hf_lifecycle",["/usr/bin/python3",str(r/"hf_regression/pipeline.py")])]
(r/"qualification_continuation_commands.json").write_text(json.dumps(commands,indent=2))
status=[]
for name,cmd in commands:
 print("START",name,datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
 child_env=base_env if name.startswith("hf_") else env
 with (r/(name+".stdout")).open("w") as out,(r/(name+".stderr")).open("w") as err:p=subprocess.run(cmd,stdout=out,stderr=err,env=child_env)
 rec=dict(name=name,cmd=cmd,exit=p.returncode);status.append(rec)
 if p.returncode==0 and not name.startswith("hf_"):
  with (r/(name+"_analysis.stdout")).open("w") as out,(r/(name+"_analysis.stderr")).open("w") as err:q=subprocess.run(["/usr/bin/python3","bench/vllm_serving_analysis.py",str(r/(name+".jsonl"))],stdout=out,stderr=err,env=base_env)
  rec["analysis_exit"]=q.returncode
 if p.returncode==0 and name=="hf_lifecycle":
  checked=json.loads((r/"hf_regression/pipeline.status.json").read_text())
  rec["lifecycle_verified"]=len(checked)==2 and all(x["exit"]==0 and x["pass"] for x in checked)
 (r/"qualification_continuation_status.json").write_text(json.dumps(status,indent=2));print(json.dumps(rec),flush=True)
 if p.returncode or rec.get("analysis_exit",0) or rec.get("lifecycle_verified",True)==False:break
print("QUALIFICATION_CONTINUATION_TERMINAL",flush=True)
