#!/usr/bin/env python3
import os,pathlib,subprocess,json,time,traceback,threading
from concurrent.futures import ThreadPoolExecutor
ROOT=pathlib.Path("/workspaces/repository");TEMP=pathlib.Path(__file__).resolve().parent
os.chdir(ROOT)
import sys
sys.path.insert(0,str(ROOT/"bench"))
from resident_dispatch import request,connect
MODEL="/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"
meta=next(json.loads(line) for line in (ROOT/"bench/results/vllm_server_20261012/qwen_correctness.jsonl").open() if json.loads(line)["event"]=="metadata")
cases=meta["prompts"]
baseline=[json.loads(line) for line in (ROOT/"bench/results/vllm_server_20261012/qwen_correctness_p0_kernel.gpu.jsonl.references.jsonl").open()][:10]
raw=(TEMP/"preflight.jsonl").open("w",buffering=1)
def emit(event,**kw):raw.write(json.dumps(dict(event=event,utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),**kw))+"\n")
p=None;attached=False;code=1
try:
 assert not pathlib.Path("/sys/module/bfusion_tx").exists()
 assert not pathlib.Path("/sys/fs/bpf/bpfusion_ctl").exists()
 r=subprocess.run(["./build/bpfusion_load","stream-attach"],capture_output=True,text=True);assert r.returncode==0;attached=True
 emit("attach",code=r.returncode,stdout=r.stdout,stderr=r.stderr)
 env=dict(os.environ,PATH=str(TEMP/"venv/bin")+":"+os.environ["PATH"],VLLM_ENABLE_V1_MULTIPROCESSING="0",HF_HOME="/workspaces/.cache/huggingface")
 trace=TEMP/"preflight_gpu.jsonl";logpath=TEMP/"preflight_server.stdout.txt"
 cmd=["./build/vllm_graph_padded_trace",MODEL,"300","--trace-output",str(trace),"--trace-requests","8"]
 emit("metadata",command=cmd,model=MODEL,baseline=baseline,
  driver_source=pathlib.Path(__file__).read_text(),native_source=(ROOT/"executor/vllm_graph.cu").read_text(),backend_source=(ROOT/"executor/vllm_graph.py").read_text())
 with logpath.open("w") as log:p=subprocess.Popen(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 print("SERVER_PID",p.pid,flush=True)
 while "resident vLLM ready" not in logpath.read_text():
  if p.poll() is not None:raise RuntimeError(logpath.read_text()[-6000:])
  time.sleep(.1)
 barrier=threading.Barrier(8);rows=[]
 def lane(i):
  with connect() as client:
   barrier.wait(timeout=60)
   row=dict(request(client,cases[i%4],None,gen=64),input_ids=cases[i%4],gen=64)
   rows.append(row)
 with ThreadPoolExecutor(max_workers=8) as pool:
  futures=[pool.submit(lane,i) for i in range(8)]
  for future in futures:future.result()
 for row in rows:emit("request",**row)
 p.terminate();wait=p.wait();emit("executor",exit_code=wait,stdout=logpath.read_text());assert wait==0
 refs=[json.loads(line) for line in pathlib.Path(str(trace)+".references.jsonl").open()]
 assert len(refs)==len(rows)==8
 by_marker={r["client_ns"]:r for r in refs}
 for row in rows:
  ref=by_marker.pop(row["client_ns"])
  assert row["input_ids"]==ref["prompt"] and row["tokens"]==ref["tokens"] and ref["gen"]==64 and not ref["bad"]
 assert not by_marker
 events=[json.loads(line) for line in trace.open()]
 admissions={r["id"]:r for r in events if r["event"]=="admission"}
 mixed=[r for r in events if r["event"]=="compute" and r["query"] and len({admissions[i]["query"] for i in r["request_ids"]})>1]
 assert mixed,"mixed-length packing was not exercised"
 frozen={tuple(r["prompt"]):r["tokens"] for r in baseline}
 emit("unpadded_fidelity_diagnostic",sequences=8,equal_sequences=sum(row["tokens"]==frozen[tuple(row["input_ids"])] for row in rows),
  first_token_equal=sum(row["tokens"][0]==frozen[tuple(row["input_ids"])][0] for row in rows))
 emit("verified",requests=8,tokens=512,mixed_prefills=mixed)
 code=0
except BaseException as exc:
 emit("failure",kind=type(exc).__name__,message=str(exc),traceback=traceback.format_exc());traceback.print_exc()
finally:
 if p is not None and p.poll() is None:p.terminate();emit("cleanup_executor",exit_code=p.wait())
 if attached:
  r=subprocess.run(["./build/bpfusion_load","stream-detach"],capture_output=True,text=True);emit("detach",code=r.returncode,stdout=r.stdout,stderr=r.stderr)
  for name in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):pathlib.Path("/sys/fs/bpf",name).unlink(missing_ok=True)
 emit("terminal",exit_code=code);raw.close()
sys.exit(code)
