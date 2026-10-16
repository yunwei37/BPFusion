#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Bootstrap upstream vLLM graphs; native GPU owns online request execution."""
import argparse,ctypes,json,math,os,sys
from pathlib import Path
import torch
OriginalGraph=torch.cuda.CUDAGraph
class KeptGraph(OriginalGraph):
    def __new__(cls,keep_graph=False):return super().__new__(cls,True)
    def __init__(self,keep_graph=False):super().__init__(True)
torch.cuda.CUDAGraph=KeptGraph
from vllm import LLM
from vllm.config.compilation import CUDAGraphMode
from vllm.v1.worker.gpu.cudagraph_utils import ModelCudaGraphManager,BatchExecutionDescriptor
from vllm.v1.worker.gpu.sample.gumbel import gumbel_sample

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("model");ap.add_argument("seconds",type=int,nargs="?",default=60)
    ap.add_argument("--trace-output");ap.add_argument("--trace-requests",type=int,default=0)
    args=ap.parse_args()
    root=Path("/workspaces/repository")
    entry=Path(sys.argv[0]).absolute()
    library=entry.with_suffix(".so") if entry.name.startswith("vllm_graph") and entry.suffix!=".py" else root/"build/vllm_graph.so"
    trace_path=Path(args.trace_output).resolve() if args.trace_output else None
    os.chdir(root)
    lib=ctypes.CDLL(str(library),mode=os.RTLD_LOCAL|os.RTLD_DEEPBIND)
    lib.max_tokens.restype=ctypes.c_uint;lib.max_requests.restype=ctypes.c_uint
    limit=lib.max_tokens();banks=lib.max_requests()
    assert os.environ.get("VLLM_ENABLE_V1_MULTIPROCESSING")=="0","in-process bootstrap required for graph ownership"
    # The shared protocol owns eight slots, each at most prompt+output tokens.
    # Size their cache from the actual loaded upstream layer specs, including
    # the allocator's null block, before its ordinary initialization/profile.
    from vllm.v1.worker.gpu_worker import Worker
    from vllm.v1.kv_cache_interface import FullAttentionSpec
    original_memory=Worker.determine_available_memory
    def queue_memory(worker):
        specs=worker.get_kv_cache_spec()
        assert specs and all(type(spec) is FullAttentionSpec for spec in specs.values()),"full-attention cache required"
        block_sizes={spec.block_size for spec in specs.values()}
        assert len(block_sizes)==1,"uniform cache group required"
        needed_blocks=1+banks*math.ceil(2*limit/next(iter(block_sizes)))
        cache_bytes=needed_blocks*sum(spec.page_size_bytes for spec in specs.values())
        worker.cache_config.kv_cache_memory_bytes=cache_bytes
        print(json.dumps(dict(event="vllm_protocol_cache",context_tokens=2*limit,
            banks=banks,needed_blocks=needed_blocks,cache_bytes=cache_bytes,
            specs={name:dict(block_size=spec.block_size,page_size_bytes=spec.page_size_bytes)
                   for name,spec in specs.items()})),flush=True)
        return original_memory(worker)
    Worker.determine_available_memory=queue_memory
    try:
        llm=LLM(model=args.model,dtype="half",max_model_len=2*limit)
    finally:
        Worker.determine_available_memory=original_memory
    runner=llm.llm_engine.model_executor.driver_worker.worker.model_runner
    bt=runner.block_tables;buf=runner.input_buffers;config=runner.model_config.hf_config
    assert bt.num_kv_cache_groups==1 and bt.cp_size==1 and not runner.use_aux_hidden_state_outputs
    size=(limit+1)*banks;graphs={};managers=[]
    mapping=torch.arange(banks,dtype=torch.int32,device="cuda")
    temperatures=torch.zeros(banks,dtype=torch.float32,device="cuda")
    seeds=torch.zeros(banks,dtype=torch.int64,device="cuda")
    stream=torch.cuda.Stream()
    with torch.inference_mode():
        for query in range(1,limit+1):
            manager=ModelCudaGraphManager(runner.vllm_config,runner.device,
                CUDAGraphMode.FULL_AND_PIECEWISE,decode_query_len=query)
            manager._capture_descs={CUDAGraphMode.FULL:[
                BatchExecutionDescriptor(cg_mode=CUDAGraphMode.FULL,num_tokens=query*batch,
                    num_reqs=batch,uniform_token_count=query)
                for batch in range(banks,0,-1)]}
            manager.capture(runner.model,runner.model_state,buf,runner.intermediate_tensors,
                bt,runner.attn_groups,runner.kv_cache_config,progress_bar_desc=f"Prefill query={query}")
            managers.append(manager)
            for batch in range(1,banks+1):
                desc=next(d for d in manager.graphs if d.num_reqs==batch)
                indices=torch.arange(query-1,query*batch,query,dtype=torch.int64,device="cuda")
                def sample():
                    hidden=manager.hidden_states[indices]
                    logits=runner.get_model().compute_logits(hidden)
                    return gumbel_sample(logits,mapping[:batch],temperatures,seeds,
                        buf.positions[indices],apply_temperature=False,is_drafting=False)
                stream.wait_stream(torch.cuda.current_stream())
                with torch.cuda.stream(stream):warm=sample()
                stream.synchronize()
                head=torch.cuda.CUDAGraph(keep_graph=True)
                with torch.cuda.graph(head,stream=stream,pool=manager.pool):output=sample()
                stream.synchronize()
                index=query*banks+batch-1
                graphs[index]=(manager.graphs[desc],head,output,indices)
            print(f"captured vLLM query={query}/{limit} batches1..{banks}",flush=True)
    for batch in range(1,banks+1):graphs[batch-1]=graphs[banks+batch-1]
    pool=llm.llm_engine.engine_core.engine_core.scheduler.kv_cache_manager.block_pool
    blocks_per_request=math.ceil(2*limit/bt.block_sizes[0])
    blocks=pool.get_new_blocks(banks*blocks_per_request)
    try:
        expansion=bt.blocks_per_kv_block[0]
        rows=[[block.block_id*expansion+k
               for block in blocks[i*blocks_per_request:(i+1)*blocks_per_request]
               for k in range(expansion)] for i in range(banks)]
        pages=torch.tensor(rows,dtype=torch.int32,device="cuda")
        pointer_values=[buf.input_ids.data_ptr(),buf.positions.data_ptr(),buf.seq_lens.data_ptr(),
            buf.query_start_loc.data_ptr(),buf.is_padding.data_ptr(),bt.slot_mappings[0].data_ptr(),
            bt.input_block_tables[0].data_ptr(),pages.data_ptr()]
        emit=dict(event="vllm_bootstrap",model=args.model,block_sizes=bt.block_sizes,
            kernel_block_sizes=bt.kernel_block_sizes,pages=rows,graph_count=len(graphs),
            captured_batches=list(range(1,banks+1)),captured_queries=list(range(1,limit+1)))
        print(json.dumps(emit),flush=True)
        ptr=ctypes.POINTER(ctypes.c_ulonglong)
        lib.serve.argtypes=[ptr,ptr,ptr,ptr]+[ctypes.c_uint]*8+[ctypes.c_char_p]
        lib.serve.restype=ctypes.c_int
        bodies=(ctypes.c_ulonglong*size)(*(graphs[i][0].raw_cuda_graph() for i in range(size)))
        head_raw=(ctypes.c_ulonglong*size)(*(graphs[i][1].raw_cuda_graph() for i in range(size)))
        outputs=(ctypes.c_ulonglong*size)(*(graphs[i][2].data_ptr() for i in range(size)))
        pointers=(ctypes.c_ulonglong*8)(*pointer_values)
        status=lib.serve(bodies,head_raw,outputs,pointers,bt.input_block_tables[0].stride(0),
            bt.kernel_block_sizes[0],pages.shape[1],config.vocab_size,config.num_hidden_layers,
            config.hidden_size,args.seconds,args.trace_requests,str(trace_path).encode() if trace_path else None)
        if status:raise RuntimeError(f"native serve failed: {status}")
        if trace_path:
            records=[json.loads(line) for line in trace_path.open()]
            assert records[-1]["event"]=="terminal" and records[-1]["overflows"]==0
            requests={};checked=0;released=set();owners={}
            release_trace=any(event["event"]=="release" for event in records)
            with trace_path.with_suffix(trace_path.suffix+".references.jsonl").open("w") as references,torch.inference_mode():
                for event in records:
                    if event["event"]=="admission":
                        if release_trace:
                            physical=event["id"]%banks;assert physical not in owners,event
                            owners[physical]=event["id"]
                        bad=not(1<=event["query"]<=limit and 1<=event["gen"]<=limit) or any(token>=config.vocab_size for token in event["input_ids"])
                        assert bool(event["bad"])==bad,event
                        requests[event["id"]]=dict(prompt=event["input_ids"],gen=event["gen"],
                            bad=bad,client_ns=event["client_ns"],tokens=[])
                    elif event["event"]=="compute":
                        query=event["query"];batch=event["batch"];length=query or 1
                        ids=event["request_ids"];packed=[];positions=[];lens=[];slot_ids=[];padding=[]
                        if query:assert query==max(len(requests[rid]["prompt"]) for rid in ids)
                        for row,request_id in enumerate(ids):
                            request=requests[request_id];assert not request["bad"]
                            if release_trace:assert request_id not in released and owners[request_id%banks]==request_id
                            prompt=request["prompt"];history=request["tokens"];physical=request_id%banks
                            if query:
                                assert not history and len(prompt)<=query
                                pad=query-len(prompt)
                                values=[0]*pad+prompt;pos=[0]*pad+list(range(len(prompt)));seq=len(prompt)
                            else:
                                assert history and len(history)<request["gen"]
                                pad=0;values=[history[-1]];pos=[len(prompt)+len(history)-1];seq=pos[0]+1
                            packed+=values;positions+=pos;lens.append(seq)
                            slots=[rows[physical][p//bt.kernel_block_sizes[0]]*bt.kernel_block_sizes[0]+p%bt.kernel_block_sizes[0] for p in pos[pad:]]
                            slot_ids+=[-1]*pad+slots;padding+=[True]*pad+[False]*(length-pad)
                            bt.input_block_tables[0][row,:pages.shape[1]].copy_(pages[physical])
                        count=length*batch
                        buf.input_ids[:count].copy_(torch.tensor(packed,dtype=torch.int32,device="cuda"))
                        buf.positions[:count].copy_(torch.tensor(positions,dtype=torch.int64,device="cuda"))
                        buf.seq_lens[:batch].copy_(torch.tensor(lens,dtype=torch.int32,device="cuda"))
                        buf.query_start_loc[:batch+1].copy_(torch.arange(batch+1,dtype=torch.int32,device="cuda")*length)
                        buf.is_padding[:count].copy_(torch.tensor(padding,dtype=torch.bool,device="cuda"))
                        bt.slot_mappings[0,:count].copy_(torch.tensor(slot_ids,dtype=torch.int64,device="cuda"))
                        index=query*banks+batch-1
                        body,head,output,indices=graphs[index];body.replay();head.replay()
                        actual=output.cpu().tolist()
                        assert actual==event["tokens"],(event,actual)
                        for request_id,token in zip(ids,actual):requests[request_id]["tokens"].append(token)
                        checked+=batch
                    elif event["event"]=="release":
                        ids=event["request_ids"];assert len(ids)==event["batch"]
                        assert ids==list(range(len(released),len(released)+len(ids))),event
                        for request_id in ids:
                            request=requests[request_id]
                            assert request["bad"] or len(request["tokens"])==request["gen"],event
                            assert request_id not in released and owners.pop(request_id%banks)==request_id
                            released.add(request_id)
                if release_trace:assert not owners and released==set(requests)
                for request_id,request in requests.items():
                    assert request["bad"] or len(request["tokens"])==request["gen"],(request_id,request)
                    references.write(json.dumps(dict(id=request_id,**request))+"\n")
            print(json.dumps(dict(event="vllm_reference_replay",requests=len(requests),
                checked_tokens=checked,reference_file=str(trace_path)+".references.jsonl")),flush=True)
    finally:
        torch.cuda.synchronize();pool.free_blocks(blocks)

if __name__=="__main__":main()
