#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Probe actual official vLLM FULL graphs with CUDA device launch."""
import argparse,ctypes,json,os,pathlib,sys,time,traceback,subprocess
ROOT=pathlib.Path("/workspaces/repository")
TEMP=pathlib.Path(__file__).resolve().parent
MODEL="/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"
parser=argparse.ArgumentParser();parser.add_argument("--preflight",action="store_true");parser.add_argument("--output",required=True)
args=parser.parse_args()
raw=pathlib.Path(args.output).open("w",buffering=1)
def emit(event,**kw):
 row=dict(event=event,utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),**kw)
 raw.write(json.dumps(row,separators=(",",":"))+"\n");return row
handles={};lib=None;llm=None;manager=None;original_run=None
try:
 import torch,vllm,transformers
 from vllm import LLM,SamplingParams
 source_meta=None
 for line in (ROOT/"bench/results/qwen_vllm_20261012.jsonl").open():
  row=json.loads(line)
  if row.get("event")=="metadata":source_meta=row;break
 assert source_meta
 cases=source_meta["cases"]
 groups=[dict(batch=1,cases=[0])] if args.preflight else [
  dict(batch=b,cases=[k]*b) for b in (1,2,4,8) for k in range(4)]
 if not args.preflight:
  groups += [dict(batch=b,cases=[i%4 for i in range(b)]) for b in (2,4,8)]
 original_graph=torch.cuda.CUDAGraph
 class KeptGraph(original_graph):
  def __new__(cls,keep_graph=False):
   return super().__new__(cls,True)
  def __init__(self,keep_graph=False):
   super().__init__(True)
 torch.cuda.CUDAGraph=KeptGraph
 emit("metadata",commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
      model=MODEL,torch=torch.__version__,torch_cuda=torch.version.cuda,vllm=vllm.__version__,
      transformers=transformers.__version__,preflight=args.preflight,groups=groups,
      params=dict(temperature=0.0,max_tokens=64,ignore_eos=True,detokenize=False),
      multiprocess=os.environ.get("VLLM_ENABLE_V1_MULTIPROCESSING"),
      qualifier_source=pathlib.Path(__file__).read_text(),bridge_source=(TEMP/"bridge.cu").read_text(),
      build_command=json.loads((TEMP/"build-command.json").read_text()))
 llm=LLM(model=MODEL,dtype="half")
 worker_wrapper=llm.llm_engine.model_executor.driver_worker
 worker=worker_wrapper.worker
 runner=worker.model_runner
 manager=runner.cudagraph_manager
 emit("owners",engine=type(llm.llm_engine).__module__+"."+type(llm.llm_engine).__name__,
      executor=type(llm.llm_engine.model_executor).__name__,worker=type(worker).__name__,
      runner=type(runner).__module__+"."+type(runner).__name__,manager=type(manager).__name__,
      graph_count=len(manager.graphs),input_buffer_owner=type(runner.input_buffers).__name__,
      model=type(runner.get_model()).__name__)
 params=SamplingParams(temperature=0.0,max_tokens=64,ignore_eos=True,detokenize=False)
 def generate(group):
  prompts=[{"prompt_token_ids":cases[k][0]} for k in group["cases"]]
  result=llm.generate(prompts,params,use_tqdm=False)
  assert len(result)==group["batch"]
  output=[list(r.outputs[0].token_ids) for r in result]
  assert all(len(tokens)==64 for tokens in output)
  return output
 references=[]
 for index,group in enumerate(groups):
  output=generate(group);references.append(output)
  emit("reference",group=index,condition=group,input_ids=[cases[k][0] for k in group["cases"]],
       output_ids=output,hf_exact=[out==cases[k][1] for k,out in zip(group["cases"],output)])
 torch.cuda.synchronize()
 emit("references_frozen",groups=len(references),lanes=sum(g["batch"] for g in groups),
      tokens=sum(g["batch"]*64 for g in groups))
 lib=ctypes.CDLL(str(TEMP/"bridge.so"),mode=os.RTLD_LOCAL|os.RTLD_DEEPBIND)
 lib.bf_catalog.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int),ctypes.c_int];lib.bf_catalog.restype=ctypes.c_int
 lib.bf_create.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_int)];lib.bf_create.restype=ctypes.c_int
 lib.bf_run.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)];lib.bf_run.restype=ctypes.c_int
 lib.bf_destroy.argtypes=[ctypes.c_void_p];lib.bf_destroy.restype=ctypes.c_int
 lib.bf_error.argtypes=[ctypes.c_int];lib.bf_error.restype=ctypes.c_char_p
 emit("runtime_maps",libraries=sorted(set(line.rsplit(" ",1)[-1] for line in pathlib.Path("/proc/self/maps").read_text().splitlines() if "libcudart" in line)))
 original_run=manager.run_fullgraph
 group_index=-1;calls=0;shape_counts={}
 def instrumented(desc):
  global calls
  output=original_run(desc)
  assert isinstance(output,torch.Tensor),type(output)
  assert output.dtype==torch.float16,output.dtype
  host=output.clone()
  torch.cuda.synchronize()
  assert bool(torch.isfinite(host).all())
  key=repr(desc);graph=manager.graphs[desc];stream=torch.cuda.current_stream()
  if key not in handles:
   raw_graph=graph.raw_cuda_graph();counts=(ctypes.c_int*32)()
   code=lib.bf_catalog(raw_graph,counts,32)
   emit("catalog",descriptor=key,raw_graph=raw_graph,code=code,counts=list(counts),
        output_ptr=output.data_ptr(),input_ptr=runner.input_buffers.input_ids.data_ptr(),
        stream=stream.cuda_stream)
   assert code==0 and counts[0]>0,(code,list(counts))
   handle=ctypes.c_void_p();stage=ctypes.c_int()
   code=lib.bf_create(raw_graph,stream.cuda_stream,ctypes.byref(handle),ctypes.byref(stage))
   emit("instantiate",descriptor=key,code=code,stage=stage.value,
        error=lib.bf_error(code).decode(),handle=handle.value)
   assert code==0,(code,stage.value)
   handles[key]=(handle,graph)
  output.fill_(float("nan"))
  torch.cuda.synchronize()
  poison=bool(torch.isnan(output).all());assert poison
  device_status=ctypes.c_int(-1);entered=ctypes.c_int(-1);stage=ctypes.c_int()
  code=lib.bf_run(handles[key][0],ctypes.byref(device_status),ctypes.byref(entered),ctypes.byref(stage))
  torch.cuda.synchronize()
  finite=bool(torch.isfinite(output).all())
  bits_equal=torch.equal(output.view(torch.int16),host.view(torch.int16))
  numeric_equal=torch.equal(output,host)
  calls+=1;shape_counts[str(desc.num_tokens)]=shape_counts.get(str(desc.num_tokens),0)+1
  emit("device_call",group=group_index,call=calls,descriptor=key,num_tokens=desc.num_tokens,
       num_reqs=desc.num_reqs,uniform_token_count=desc.uniform_token_count,
       code=code,stage=stage.value,device_status=device_status.value,entered=entered.value,
       poisoned=poison,finite=finite,bits_equal=bits_equal,numeric_equal=numeric_equal,
       elements=output.numel(),max_abs=float((output-host).abs().max().item()))
  # Restore the independent host result before official sampling, including failure.
  output.copy_(host);torch.cuda.synchronize()
  assert code==0 and device_status.value==0 and entered.value==1,(code,device_status.value,entered.value)
  assert finite and bits_equal,"native graph output mismatch"
  return output
 manager.run_fullgraph=instrumented
 for group_index,group in enumerate(groups):
  before=calls;output=generate(group);exact=output==references[group_index]
  emit("instrumented",group=group_index,condition=group,output_ids=output,reference_exact=exact,
       hf_exact=[out==cases[k][1] for k,out in zip(group["cases"],output)],
       device_calls=calls-before)
  assert exact and calls>before,(group_index,exact,calls-before)
 emit("complete",groups=len(groups),lanes=sum(g["batch"] for g in groups),
      cpu_loop_tokens=sum(g["batch"]*64 for g in groups),device_calls=calls,shape_counts=shape_counts,
      scope="FULL-body GPU mirror; upstream CPU scheduling/sampling and prefill remain")
except BaseException as exc:
 emit("failure",kind=type(exc).__name__,message=str(exc),traceback=traceback.format_exc())
 traceback.print_exc();sys.exit_code=1
else:sys.exit_code=0
finally:
 if manager is not None and original_run is not None:manager.run_fullgraph=original_run
 if lib is not None:
  for key,(handle,graph_owner) in handles.items():
   code=lib.bf_destroy(handle);emit("destroy",descriptor=key,code=code)
   if code:sys.exit_code=1
 emit("terminal",exit_code=getattr(sys,"exit_code",1))
 raw.close()
sys.exit(sys.exit_code)
