"""Independent request-history reconstruction for upstream packed mixed graphs."""
import json
import numpy as np
import torch
from vllm.config.compilation import CUDAGraphMode
from vllm.forward_context import set_forward_context
from vllm.v1.worker.gpu.input_batch import InputBatch
from vllm.v1.worker.gpu.attn_utils import build_slot_mappings_by_layer
from vllm.v1.worker.gpu.sample.gumbel import gumbel_sample

@torch.inference_mode()
def audit(trace_path,runner,buf,bt,graphs,pages,rows,config,banks,limit):
    events=[json.loads(line) for line in trace_path.open()]
    assert events[-1]["event"]=="terminal" and events[-1]["overflows"]==0
    mapping=torch.arange(banks,dtype=torch.int32,device="cuda")
    temperatures=torch.zeros(banks,dtype=torch.float32,device="cuda")
    seeds=torch.zeros(banks,dtype=torch.int64,device="cuda")
    for fresh in [False,True]:
        # All caches belong to this one post-serving model bootstrap. Reset
        # values without changing tensor addresses used by captured graphs.
        for cache in runner.kv_caches:cache.zero_()
        torch.cuda.synchronize()
        requests={};owners={};released=set();checked=0;rounds=0;mixed_rounds=0
        fresh_log=trace_path.with_suffix(trace_path.suffix+".fresh_metadata.jsonl")
        log=fresh_log.open("w") if fresh else None
        with torch.inference_mode():
            try:
                for e in events:
                    if e["event"]=="admission":
                        rid=e["id"];physical=rid%banks
                        assert physical not in owners
                        owners[physical]=rid
                        bad=not(1<=e["query"]<=limit and 1<=e["gen"]<=limit) or any(x>=config.vocab_size for x in e["input_ids"])
                        assert bool(e["bad"])==bad
                        requests[rid]=dict(prompt=e["input_ids"],gen=e["gen"],bad=bad,client_ns=e["client_ns"],tokens=[])
                    elif e["event"]=="compute":
                        selected=e["request_ids"];batch=len(selected)
                        assert batch==e["batch"] and len(set(selected))==batch
                        packed=[];positions=[];slots=[];starts=[0];seqs=[];qlens=[];prefilling=[];prompts=[];computed=[]
                        for row,rid in enumerate(selected):
                            req=requests[rid];history=req["tokens"];prompt=req["prompt"];physical=rid%banks
                            assert owners[physical]==rid and rid not in released and not req["bad"]
                            assert len(history)<req["gen"]
                            if history:
                                values=[history[-1]];pos=[len(prompt)+len(history)-1];seq=pos[0]+1
                            else:values=prompt;pos=list(range(len(prompt)));seq=len(prompt)
                            packed+=values;positions+=pos;starts.append(len(packed))
                            slots+=[rows[physical][position//bt.kernel_block_sizes[0]]*bt.kernel_block_sizes[0]+position%bt.kernel_block_sizes[0] for position in pos]
                            seqs.append(seq);qlens.append(len(values));prefilling.append(not history);prompts.append(len(prompt));computed.append(seq-len(values))
                        count=len(packed);padded=min(count,banks)
                        assert count==e["input_tokens"] and batch<=padded
                        expected_query=max((len(requests[rid]["prompt"]) for rid in selected if not requests[rid]["tokens"]),default=0)
                        assert expected_query==e["query"]
                        is_mixed=any(prefilling) and not all(prefilling)
                        mixed_rounds+=is_mixed;rounds+=1
                        trailing=padded-batch
                        seqs+=[0]*trailing;qlens+=[0]*trailing;prefilling+=[False]*trailing;prompts+=[0]*trailing;computed+=[0]*trailing
                        starts+=[count]*trailing
                        if fresh:
                            ib=InputBatch.make_dummy(padded,count,buf,max_query_len=count)
                            ib.num_scheduled_tokens=np.array(qlens,dtype=np.int32)
                            ib.query_start_loc_np=np.array(starts,dtype=np.int32)
                            ib.seq_lens_cpu_upper_bound=torch.tensor(seqs,dtype=torch.int32,device="cpu")
                            ib.num_computed_tokens_np=np.array(computed,dtype=np.int32)
                            ib.prefill_len_np=np.array(prompts,dtype=np.int32)
                            ib.num_computed_prefill_tokens_np=np.array([0 if prefilling[i] else prompts[i] for i in range(padded)],dtype=np.int32)
                            ib.is_prefilling_np=np.array(prefilling,dtype=np.bool_)
                            ib.has_prefill=bool(any(prefilling));ib.decode_graph_eligible=not ib.has_prefill
                            ib.max_query_len=max(qlens)
                        buf.input_ids[:count].copy_(torch.tensor(packed,dtype=torch.int32,device="cuda"))
                        buf.positions[:count].copy_(torch.tensor(positions,dtype=torch.int64,device="cuda"))
                        buf.seq_lens[:padded].copy_(torch.tensor(seqs,dtype=torch.int32,device="cuda"))
                        buf.query_start_loc[:padded+1].copy_(torch.tensor(starts,dtype=torch.int32,device="cuda"))
                        buf.is_padding[:count].fill_(False)
                        bt.slot_mappings[0,:count].copy_(torch.tensor(slots,dtype=torch.int64,device="cuda"))
                        bt.input_block_tables[0][:padded].zero_()
                        for row,rid in enumerate(selected):
                            bt.input_block_tables[0][row,:pages.shape[1]].copy_(pages[rid%banks])
                        if fresh:
                            sm=bt.slot_mappings[:,:count]
                            metadata=runner.model_state.prepare_attn(ib,CUDAGraphMode.NONE,
                                tuple(table[:padded] for table in bt.input_block_tables),sm,
                                runner.attn_groups,runner.kv_cache_config,for_capture=False)
                            with set_forward_context(metadata,runner.vllm_config,num_tokens=count,
                                cudagraph_runtime_mode=CUDAGraphMode.NONE,
                                slot_mapping=build_slot_mappings_by_layer(sm,runner.kv_cache_config),
                                is_padding=buf.is_padding[:count]):
                                hidden=runner.model(input_ids=buf.input_ids[:count],
                                    positions=buf.positions[:count],intermediate_tensors=None,
                                    **runner.model_state.prepare_dummy_inputs(padded,count))
                            indices=torch.tensor([x-1 for x in starts[1:]],dtype=torch.int64,device="cuda")
                            logits=runner.get_model().compute_logits(hidden[indices])
                            output=gumbel_sample(logits,mapping[:padded],temperatures,seeds,
                                buf.positions[indices],apply_temperature=False,is_drafting=False)
                        else:
                            body,head,output=graphs[count];body.replay();head.replay()
                        actual=output.cpu().tolist()[:batch]
                        assert actual==e["tokens"],dict(fresh=fresh,event=e,expected=actual)
                        for rid,token in zip(selected,actual):requests[rid]["tokens"].append(token)
                        checked+=batch
                        if log:log.write(json.dumps(dict(event="fresh_metadata_compute",round=rounds,batch=batch,padded_requests=padded,input_tokens=count,query_lengths=qlens,sequence_lengths=seqs,mixed=is_mixed,request_ids=selected,tokens=actual,exact=True))+"\n")
                    elif e["event"]=="release":
                        selected=e["request_ids"]
                        assert selected==list(range(len(released),len(released)+len(selected)))
                        for rid in selected:
                            req=requests[rid]
                            assert req["bad"] or len(req["tokens"])==req["gen"]
                            assert rid not in released and owners.pop(rid%banks)==rid
                            released.add(rid)
                assert not owners and released==set(requests)
                if not fresh:
                    with trace_path.with_suffix(trace_path.suffix+".references.jsonl").open("w") as out:
                        for rid,req in requests.items():out.write(json.dumps(dict(id=rid,**req))+"\n")
                summary=dict(event="fresh_metadata_verified" if fresh else "vllm_reference_replay",requests=len(requests),checked_tokens=checked,rounds=rounds,mixed_rounds=mixed_rounds,exact=True)
                if log:log.write(json.dumps(summary)+"\n")
                print(json.dumps(summary),flush=True)
            finally:
                if log:log.close()
