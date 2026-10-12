#!/usr/bin/env python3
"""Real untraced default TCP replies against frozen upstream batch1 sequences."""
import os,pathlib,subprocess,json,time,sys,traceback
ROOT=pathlib.Path("/workspaces/repository");TEMP=pathlib.Path(__file__).resolve().parent
os.chdir(ROOT);sys.path.insert(0,str(ROOT/"bench"))
from resident_dispatch import request,connect
raw=(TEMP/"untraced.jsonl").open("w",buffering=1)
def emit(event,**kw):raw.write(json.dumps(dict(event=event,utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),**kw))+"\n")
env=dict(os.environ,PATH=str(pathlib.Path("/tmp/bpfusion-padding-b45ull5p/venv/bin"))+":"+os.environ["PATH"],VLLM_ENABLE_V1_MULTIPROCESSING="0",HF_HOME="/workspaces/.cache/huggingface")
exit_code=1
try:
 for name in ("qwen","smol"):
  previous=ROOT/f"bench/results/vllm_server_20261012/{name}_correctness.jsonl"
  meta=next(json.loads(l) for l in previous.open() if json.loads(l)["event"]=="metadata")
  refs=[json.loads(l) for l in previous.with_name(previous.stem+"_p0_kernel.gpu.jsonl.references.jsonl").open()][:10]
  assert all(not r["bad"] and len(r["tokens"])==64 for r in refs)
  for mode in ("kernel","userspace"):
   p=None;attached=False
   try:
    assert not pathlib.Path("/sys/module/bfusion_tx").exists()
    assert not pathlib.Path("/sys/fs/bpf/bpfusion_ctl").exists()
    if mode=="kernel":
     r=subprocess.run(["./build/bpfusion_load","stream-attach"],capture_output=True,text=True);assert r.returncode==0;attached=True
     emit("attach",model=name,mode=mode,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
    cmd=["./build/vllm_graph" if mode=="kernel" else "./build/vllm_graph_user_network_wait",meta["model"],"300"]
    logpath=TEMP/f"{name}_untraced_{mode}.stdout.txt"
    emit("metadata",model=name,mode=mode,command=cmd,frozen_references=refs,
     source=pathlib.Path(__file__).read_text(),native_source=(ROOT/"executor/vllm_graph.cu").read_text(),backend_source=(ROOT/"executor/vllm_graph.py").read_text(),makefile=(ROOT/"Makefile").read_text())
    with logpath.open("w") as log:p=subprocess.Popen(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
    print("UNTRACED_PID",name,mode,p.pid,flush=True)
    while "resident vLLM ready" not in logpath.read_text():
     if p.poll() is not None:raise RuntimeError(logpath.read_text()[-6000:])
     time.sleep(.1)
    with connect() as client:
     for repeat in range(2):
      for gen in (1,64):
       for index,ref in enumerate(refs):
        result=request(client,ref["prompt"],ref["tokens"][:gen])
        emit("request",model=name,mode=mode,repeat=repeat,case=index,gen=gen,input_ids=ref["prompt"],**result)
    p.terminate();code=p.wait();log=logpath.read_text()
    emit("executor",model=name,mode=mode,exit_code=code,stdout=log)
    assert code==0 and "device_graph_launches=1300 graph_error=0 max_active=1 admitted=40 retired=40 trace_overflows=0" in log,log[-5000:]
    if mode=="kernel":
     r=subprocess.run(["./build/bpfusion_load","stats"],capture_output=True,text=True);assert r.returncode==0
     emit("stats",model=name,mode=mode,stdout=r.stdout,stderr=r.stderr)
    assert not pathlib.Path("/sys/module/bfusion_tx").exists()
    emit("verified",model=name,mode=mode,requests=40,tokens=1300)
    print("UNTRACED_PASS",name,mode,flush=True)
   finally:
    if p is not None and p.poll() is None:p.terminate();emit("cleanup_executor",model=name,mode=mode,exit_code=p.wait())
    if attached:
     r=subprocess.run(["./build/bpfusion_load","stream-detach"],capture_output=True,text=True)
     emit("detach",model=name,mode=mode,exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr)
     for pin in ("bpfusion_ctl","bpfusion_stats","bpfusion_db"):pathlib.Path("/sys/fs/bpf",pin).unlink(missing_ok=True)
 exit_code=0
except BaseException as exc:emit("failure",kind=type(exc).__name__,message=str(exc),traceback=traceback.format_exc());traceback.print_exc()
finally:emit("terminal",exit_code=exit_code);raw.close()
sys.exit(exit_code)
