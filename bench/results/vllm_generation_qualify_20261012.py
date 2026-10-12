#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Qualify autonomous decode with actual vLLM body/head/sampling graphs."""
import argparse,ctypes,json,os,pathlib,subprocess,sys,time,traceback
ROOT=pathlib.Path("/workspaces/repository");TEMP=pathlib.Path(__file__).resolve().parent
MODEL="/workspaces/.cache/huggingface/hub/models--Qwen--Qwen2.5-0.5B-Instruct/snapshots/7ae557604adf67be50417f59c2c2f167def9a775"
ap=argparse.ArgumentParser();ap.add_argument("--preflight",action="store_true");ap.add_argument("--output",required=True);args=ap.parse_args()
raw=pathlib.Path(args.output).open("w",buffering=1)
def emit(event,**kw):
 raw.write(json.dumps(dict(event=event,utc=time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),**kw),separators=(",",":"))+"\n")
handles={};llm=runner=manager=lib=None;old_full=old_prepare=None;exit_code=1
try:
 import torch,vllm,transformers
 from vllm import LLM,SamplingParams
 from vllm.v1.worker.gpu.sample.gumbel import gumbel_sample
 cases=None
 for line in (ROOT/"bench/results/qwen_vllm_20261012.jsonl").open():
  row=json.loads(line)
  if row.get("event")=="metadata":cases=row["cases"];break
 ref_rows=[json.loads(line) for line in (ROOT/"bench/results/vllm_reuse_full_20261012.jsonl").open()]
 refs={r["group"]:r for r in ref_rows if r["event"]=="reference"}
 selected=[0] if args.preflight else list(range(19))
 Original=torch.cuda.CUDAGraph
 class KeptGraph(Original):
  def __new__(cls,keep_graph=False):return super().__new__(cls,True)
  def __init__(self,keep_graph=False):super().__init__(True)
 torch.cuda.CUDAGraph=KeptGraph
 emit("metadata",commit=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
      model=MODEL,torch=torch.__version__,torch_cuda=torch.version.cuda,vllm=vllm.__version__,
      transformers=transformers.__version__,groups=selected,preflight=args.preflight,
      reference_source="bench/results/vllm_reuse_full_20261012.jsonl",
      qualifier_source=pathlib.Path(__file__).read_text(),native_source=(TEMP/"generate.cu").read_text(),
      build_commands=json.loads((TEMP/"generation-build-command.json").read_text()))
 llm=LLM(model=MODEL,dtype="half")
 runner=llm.llm_engine.model_executor.driver_worker.worker.model_runner
 manager=runner.cudagraph_manager;core=llm.llm_engine.engine_core.engine_core
 scheduler=core.scheduler;kv=scheduler.kv_cache_manager;bt=runner.block_tables;buf=runner.input_buffers
 assert bt.num_kv_cache_groups==1 and bt.cp_size==1
 emit("owners",runner=type(runner).__name__,manager=type(manager).__name__,model=type(runner.get_model()).__name__,
      kv_manager=type(kv).__name__,block_sizes=bt.block_sizes,kernel_block_sizes=bt.kernel_block_sizes,
      blocks_per_kv_block=bt.blocks_per_kv_block)
 lib=ctypes.CDLL(str(TEMP/"generate.so"),mode=os.RTLD_LOCAL|os.RTLD_DEEPBIND)
 lib.gen_create.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.POINTER(ctypes.c_ulonglong),
   ctypes.c_uint,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint,ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_int)]
 lib.gen_create.restype=ctypes.c_int
 lib.gen_run.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_uint),ctypes.POINTER(ctypes.c_int),ctypes.POINTER(ctypes.c_int)]
 lib.gen_run.restype=ctypes.c_int;lib.gen_destroy.argtypes=[ctypes.c_void_p];lib.gen_destroy.restype=ctypes.c_int
 lib.gen_error.argtypes=[ctypes.c_int];lib.gen_error.restype=ctypes.c_char_p
 prepared=None;active_group=-1;native_rows={};seen=set()
 old_prepare=runner.prepare_inputs
 def retain_inputs(*a,**kw):
  global prepared
  prepared=old_prepare(*a,**kw);return prepared
 runner.prepare_inputs=retain_inputs
 old_full=manager.run_fullgraph
 def generation_probe(desc):
  official=old_full(desc)
  if active_group in seen:return official
  seen.add(active_group)
  batch=refs[active_group]["condition"]["batch"]
  ib=prepared;assert ib is not None and ib.num_reqs==batch and desc.num_tokens==batch and desc.num_reqs==batch
  assert isinstance(official,torch.Tensor) and official.dtype==torch.float16
  host=official.clone()
  saved=[x.clone() for x in (buf.input_ids[:batch],buf.positions[:batch],buf.seq_lens[:batch],bt.slot_mappings[0,:batch])]
  torch.cuda.synchronize()
  initial=[x.cpu().tolist() for x in saved]
  blocks=[];reqids=list(ib.req_ids)
  external_reqids=[llm.llm_engine.output_processor.request_states[rid].external_req_id for rid in reqids]
  for rid,req_index in zip(reqids,ib.idx_mapping_np.tolist()):
   request=scheduler.requests[rid]
   new=kv.allocate_slots(request,num_new_tokens=63)
   assert new is not None,"upstream KV reservation failed"
   ids=kv.get_block_ids(rid);blocks.append(ids[0])
   bt.append_block_ids(int(req_index),ids,overwrite=True)
  bt.apply_staged_writes();bt.gather_block_tables(ib.idx_mapping,desc.num_reqs)
  torch.cuda.synchronize()
  for position,ids in zip(initial[1],blocks):
   assert len(ids)*bt.block_sizes[0]>position+62,(position,len(ids),bt.block_sizes)
  key=repr(desc)
  if key not in handles:
   indices=torch.arange(batch,dtype=torch.int64,device="cuda")
   mapping=torch.arange(batch,dtype=torch.int32,device="cuda")
   temperatures=torch.zeros(batch,dtype=torch.float32,device="cuda")
   seeds=torch.zeros(batch,dtype=torch.int64,device="cuda")
   stream=torch.cuda.Stream()
   def sample():
    logits=runner.get_model().compute_logits(manager.hidden_states[:batch][indices])
    sampled=gumbel_sample(logits,mapping,temperatures,seeds,buf.positions[:batch],
                          apply_temperature=False,is_drafting=False)
    return logits,sampled
   with torch.inference_mode(),torch.cuda.stream(stream):
    logits,sampled=sample()
   stream.synchronize();head=torch.cuda.CUDAGraph(keep_graph=True)
   with torch.inference_mode(),torch.cuda.graph(head,stream=stream):
    logits,sampled=sample()
   stream.synchronize()
   output=torch.empty((batch,64),dtype=torch.int64,device="cuda")
   pointer_values=[buf.input_ids.data_ptr(),buf.positions.data_ptr(),buf.seq_lens.data_ptr(),
    bt.slot_mappings[0].data_ptr(),bt.input_block_tables[0].data_ptr(),sampled.data_ptr(),output.data_ptr()]
   pointers=(ctypes.c_ulonglong*7)(*pointer_values);handle=ctypes.c_void_p();stage=ctypes.c_int()
   body=manager.graphs[desc]
   code=lib.gen_create(body.raw_cuda_graph(),head.raw_cuda_graph(),torch.cuda.current_stream().cuda_stream,
    pointers,batch,64,bt.kernel_block_sizes[0],bt.input_block_tables[0].stride(0),ctypes.byref(handle),ctypes.byref(stage))
   emit("instantiate",descriptor=key,code=code,stage=stage.value,error=lib.gen_error(code).decode(),
        pointers=pointer_values,body=body.raw_cuda_graph(),head=head.raw_cuda_graph())
   assert code==0,(code,stage.value)
   handles[key]=(handle,body,head,logits,sampled,output,indices,mapping,temperatures,seeds)
  output=handles[key][5];counters=(ctypes.c_uint*3)();error=ctypes.c_int(-1);stage=ctypes.c_int()
  start=time.monotonic_ns()
  try:
   code=lib.gen_run(handles[key][0],counters,ctypes.byref(error),ctypes.byref(stage))
   elapsed=time.monotonic_ns()-start
   torch.cuda.synchronize()
   actual=output.cpu().tolist()
   final_positions=buf.positions[:batch].cpu().tolist()
   final_seq_lens=buf.seq_lens[:batch].cpu().tolist()
   final_slots=bt.slot_mappings[0,:batch].cpu().tolist()
   native_rows[active_group]=(external_reqids,actual)
   emit("native",group=active_group,descriptor=key,request_ids=reqids,
        external_request_ids=external_reqids,input_ids=[scheduler.requests[rid].prompt_token_ids for rid in reqids],
        initial_input_ids=initial[0],initial_positions=initial[1],initial_seq_lens=initial[2],
        initial_slot_mapping=initial[3],block_ids=blocks,output_ids=actual,
        final_positions=final_positions,final_seq_lens=final_seq_lens,final_slot_mapping=final_slots,
        code=code,stage=stage.value,device_error=error.value,child_launches=counters[0],
        parent_calls=counters[1],token_writes=counters[2],host_parent_launches=1,loop_host_duration_ns=elapsed)
   assert code==0 and error.value==0,(code,error.value,stage.value)
   assert list(counters)==[63,64,batch*64],list(counters)
   assert final_positions==[p+62 for p in initial[1]]
   assert final_seq_lens==[s+62 for s in initial[2]]
  finally:
   for destination,source in zip((buf.input_ids[:batch],buf.positions[:batch],buf.seq_lens[:batch],bt.slot_mappings[0,:batch]),saved):
    destination.copy_(source)
   official.copy_(host);torch.cuda.synchronize()
  return official
 manager.run_fullgraph=generation_probe
 params=SamplingParams(temperature=0.0,max_tokens=64,ignore_eos=True,detokenize=False)
 for active_group in selected:
  ref=refs[active_group];condition=ref["condition"]
  inputs=[{"prompt_token_ids":cases[k][0]} for k in condition["cases"]]
  results=llm.generate(inputs,params,use_tqdm=False)
  continuing=[list(r.outputs[0].token_ids) for r in results]
  reqids,actual=native_rows[active_group];mapping=dict(zip(reqids,actual))
  ordered=[mapping[r.request_id] for r in results]
  exact=ordered==ref["output_ids"];host_exact=continuing==ref["output_ids"]
  emit("group",group=active_group,condition=condition,output_ids=ordered,
       reference_exact=exact,continuing_cpu_ids=continuing,continuing_cpu_exact=host_exact,
       hf_exact=[out==cases[k][1] for k,out in zip(condition["cases"],ordered)])
  assert exact and host_exact,(active_group,exact,host_exact)
 emit("complete",groups=len(selected),lanes=sum(refs[i]["condition"]["batch"] for i in selected),
      checked_tokens=sum(refs[i]["condition"]["batch"]*64 for i in selected),
      native_generated_tokens=sum(refs[i]["condition"]["batch"]*63 for i in selected),
      host_parent_launches=len(selected),child_launches=63*len(selected))
 exit_code=0
except BaseException as exc:
 emit("failure",kind=type(exc).__name__,message=str(exc),traceback=traceback.format_exc())
 traceback.print_exc()
finally:
 if manager is not None and old_full is not None:manager.run_fullgraph=old_full
 if runner is not None and old_prepare is not None:runner.prepare_inputs=old_prepare
 if lib is not None:
  for key,owners in handles.items():
   code=lib.gen_destroy(owners[0]);emit("destroy",descriptor=key,code=code)
   if code:exit_code=1
 emit("terminal",exit_code=exit_code);raw.close()
sys.exit(exit_code)
