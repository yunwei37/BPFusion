#!/usr/bin/env python3
import json,os,pathlib,signal,subprocess,sys,time,traceback
ROOT=pathlib.Path("/workspaces/repository");TEMP=pathlib.Path(__file__).resolve().parent
MODEL="/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"
os.chdir(ROOT);sys.path.insert(0,str(ROOT/"bench"))
from resident_dispatch import request,connect
raw=(TEMP/"preflight.jsonl").open("w",buffering=1)
def emit(event,**kw):raw.write(json.dumps(dict(event=event,utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),**kw))+"\n")
p=None;attached=False;exit_code=1
try:
 assert not pathlib.Path("/sys/module/bfusion_tx").exists()
 assert not pathlib.Path("/sys/fs/bpf/bpfusion_ctl").exists()
 cases=None
 for line in (ROOT/"bench/results/qwen_vllm_20261012.jsonl").open():
  row=json.loads(line)
  if row["event"]=="metadata":cases=row["cases"];break
 r=subprocess.run(["make","VLLM_PYTHON="+str(TEMP/"venv/bin/python"),"vllm-graph-trace"],capture_output=True,text=True)
 (TEMP/"build.stdout.txt").write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
 r=subprocess.run(["./build/bpfusion_load","stream-attach"],capture_output=True,text=True)
 emit("attach",code=r.returncode,stdout=r.stdout,stderr=r.stderr);assert r.returncode==0;attached=True
 env=os.environ.copy();env["PATH"]=str(TEMP/"venv/bin")+":"+env.get("PATH","")
 env["VLLM_ENABLE_V1_MULTIPROCESSING"]="0";env["HF_HOME"]="/workspaces/.cache/huggingface"
 trace=TEMP/"preflight_gpu.jsonl"
 cmd=["./build/vllm_graph_trace",MODEL,"--trace-output",str(trace),"--trace-requests","1"]
 emit("metadata",command=cmd,driver_source=pathlib.Path(__file__).read_text(),client_source=(ROOT/"bench/resident_dispatch.py").read_text(),
      backend_source=(ROOT/"executor/vllm_graph.py").read_text(),native_source=(ROOT/"executor/vllm_graph.cu").read_text(),
      commit=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip())
 logpath=TEMP/"preflight_server.stdout.txt"
 with logpath.open("w") as log:p=subprocess.Popen(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 (TEMP/"preflight_server.pid").write_text(str(p.pid));print("SERVER_PID",p.pid,flush=True)
 while "resident vLLM ready" not in logpath.read_text():
  if p.poll() is not None:raise RuntimeError(logpath.read_text()[-5000:])
  time.sleep(.1)
 emit("ready",pid=p.pid)
 with connect() as client:result=request(client,cases[0][0],None,gen=64)
 emit("request",input_ids=cases[0][0],gen=64,**result)
 p.terminate();code=p.wait();emit("executor",wait_exit_code=code,stdout=logpath.read_text());assert code==0
 references=[json.loads(l) for l in pathlib.Path(str(trace)+".references.jsonl").open()]
 assert len(references)==1 and not references[0]["bad"]
 ref=references[0]
 assert ref["client_ns"]==result["client_ns"] and ref["prompt"]==cases[0][0] and ref["gen"]==64
 assert ref["tokens"]==result["tokens"]
 emit("verified",tokens=64,reference=ref)
 exit_code=0
except BaseException as exc:
 emit("failure",kind=type(exc).__name__,message=str(exc),traceback=traceback.format_exc());traceback.print_exc()
finally:
 if p is not None and p.poll() is None:
  p.terminate();emit("cleanup_executor",wait_exit_code=p.wait())
 if attached:
  r=subprocess.run(["./build/bpfusion_load","stream-detach"],capture_output=True,text=True);emit("detach",code=r.returncode,stdout=r.stdout,stderr=r.stderr)
  for name in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):
   path=pathlib.Path("/sys/fs/bpf")/name
   if path.exists():path.unlink()
 emit("terminal",exit_code=exit_code);raw.close()
sys.exit(exit_code)
