#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Capture HF decoder graphs at bootstrap; native GPU dispatch owns requests."""
import ctypes
import struct
import sys
from pathlib import Path
import numpy as np
import torch
from transformers import AutoConfig,AutoModelForCausalLM
from transformers.models.qwen2.modeling_qwen2 import Qwen2RotaryEmbedding
from transformers.cache_utils import Cache,DynamicLayer
from transformers.masking_utils import create_causal_mask


class SharedLayer(DynamicLayer):
    """A graph owns fixed offsets; GPU copies append into the shared KV buffers."""
    def __init__(self,key,value,pos):
        super().__init__()
        self.storage_key,self.storage_value=key,value
        self.keys,self.values=key[:,:,:pos],value[:,:,:pos]
        self.is_initialized=True

    def update(self,key_states,value_states,*args,**kwargs):
        pos=self.keys.shape[-2];end=pos+key_states.shape[-2]
        self.storage_key[:,:,pos:end].copy_(key_states)
        self.storage_value[:,:,pos:end].copy_(value_states)
        self.keys,self.values=self.storage_key[:,:,:end],self.storage_value[:,:,:end]
        return self.keys,self.values


def load_model(path):
    if not Path(path).is_file() and not str(path).endswith('.bin'):
        return AutoModelForCausalLM.from_pretrained(path,dtype=torch.float16,attn_implementation='eager').to('cuda').eval()
    with open(path,'rb') as f:header=struct.unpack('<6I2f',f.read(32))
    config=AutoConfig.from_pretrained('Qwen/Qwen2.5-0.5B-Instruct')
    dimensions=(config.hidden_size,config.intermediate_size,config.num_hidden_layers,config.num_attention_heads,config.num_key_value_heads,config.vocab_size)
    if tuple(header[:6])!=dimensions or np.float32(config.rms_norm_eps)!=header[6] or config.rope_parameters['rope_theta']!=header[7]:
        raise ValueError('weight/config layout mismatch')
    with torch.device('meta'):
        model=AutoModelForCausalLM.from_config(config,dtype=torch.float16,attn_implementation='eager')
    model.to_empty(device='cuda')
    # to_empty leaves buffers uninitialized; rebuild the real CPU RoPE initializer.
    model.model.rotary_emb=Qwen2RotaryEmbedding(config).to('cuda')
    weights=np.memmap(path,dtype=np.float16,offset=32,mode='r');cursor=0
    def copy(parameter):
        nonlocal cursor
        n=parameter.numel()
        data=np.array(weights[cursor:cursor+n]).reshape(tuple(parameter.shape))
        parameter.copy_(torch.from_numpy(data).to('cuda'));cursor+=n
    copy(model.model.embed_tokens.weight)
    for layer in model.model.layers:
        copy(layer.input_layernorm.weight)
        for projection in [layer.self_attn.q_proj,layer.self_attn.k_proj,layer.self_attn.v_proj]:
            copy(projection.weight);copy(projection.bias)
        copy(layer.self_attn.o_proj.weight);copy(layer.post_attention_layernorm.weight)
        for projection in [layer.mlp.gate_proj,layer.mlp.up_proj,layer.mlp.down_proj]:copy(projection.weight)
    copy(model.model.norm.weight)
    if cursor!=weights.size:raise ValueError('weight layout mismatch')
    model.tie_weights()
    return model.eval()


def main():
    if len(sys.argv)<2:raise SystemExit('usage: qwen_graph.py WEIGHTS.bin|HF_MODEL [seconds]')
    seconds=int(sys.argv[2]) if len(sys.argv)>2 else 60
    entry=Path(sys.argv[0])
    library=entry.with_suffix('.so') if entry.name in ('qwen_graph','qwen_graph_host_launch','qwen_graph_user_network') else Path(__file__).resolve().parents[1]/'build/qwen_graph.so'
    lib=ctypes.CDLL(str(library))
    lib.max_tokens.restype=ctypes.c_uint
    lib.max_requests.restype=ctypes.c_uint
    limit=lib.max_tokens();context=2*limit;banks=[]
    with torch.no_grad():
        model=load_model(sys.argv[1]);config=model.config
        print(f'capturing model={config._name_or_path} type={config.model_type} fp16 eager',flush=True)
        from transformers.models.qwen2 import modeling_qwen2 as qwen2
        qwen2.apply_rotary_pos_emb=torch.compile(qwen2.apply_rotary_pos_emb,options={"emulate_precision_casts":True})
        @torch.compile(options={"emulate_precision_casts":True})
        def norm_finish(hidden_states,variance,weight,eps,input_dtype):
            return weight*(hidden_states*torch.rsqrt(variance+eps)).to(input_dtype)
        def norm_forward(self,hidden_states):
            input_dtype=hidden_states.dtype
            hidden_states=hidden_states.to(torch.float32)
            variance=hidden_states.pow(2).mean(-1,keepdim=True)
            return norm_finish(hidden_states,variance,self.weight,self.variance_epsilon,input_dtype)
        qwen2.Qwen2RMSNorm.forward=norm_forward
        dim=config.hidden_size//config.num_attention_heads
        for bank in range(lib.max_requests()):
            keys=[torch.zeros((1,config.num_key_value_heads,context,dim),dtype=torch.float16,device='cuda') for _ in model.model.layers]
            values=[torch.zeros_like(k) for k in keys]
            tokens=torch.zeros(limit,dtype=torch.long,device='cuda')
            graphs=[None];selected=[None];keepers=[]
            stream=torch.cuda.Stream();stream.wait_stream(torch.cuda.current_stream())
            for index in range(1,limit+context-1):
                count=index if index<=limit else 1
                pos=0 if index<=limit else index-limit
                inp=tokens[:count].reshape(1,count)
                positions=torch.arange(pos,pos+count,device='cuda').reshape(1,count)
                def cache():
                    return Cache(layers=[SharedLayer(k,v,pos) for k,v in zip(keys,values)])
                def forward():
                    return model(inp,position_ids=positions,attention_mask=mask,past_key_values=cache(),use_cache=True,logits_to_keep=1)
                mask=create_causal_mask(config=config,inputs_embeds=model.model.embed_tokens(inp),attention_mask=None,past_key_values=cache(),position_ids=positions)
                stream.wait_stream(torch.cuda.current_stream())
                with torch.cuda.stream(stream):warm=forward()
                torch.cuda.current_stream().wait_stream(stream);torch.cuda.synchronize()
                graph=torch.cuda.CUDAGraph(keep_graph=True)
                with torch.cuda.graph(graph,stream=stream):
                    output=forward()
                    token=output.logits[:,-1,:].argmax(-1)
                graphs.append(graph);selected.append(token);keepers.append((output,positions,mask,inp))
                if index%32==0:print(f'captured bank {bank} model graph {index}/{limit+context-2}',flush=True)
            torch.cuda.synchronize()
            banks.append((tokens,graphs,selected,keepers))
        lib.serve.argtypes=[ctypes.POINTER(ctypes.c_ulonglong),ctypes.POINTER(ctypes.c_ulonglong),ctypes.c_uint,ctypes.POINTER(ctypes.c_ulonglong),ctypes.c_uint,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint]
        lib.serve.restype=ctypes.c_int
        count=len(graphs);size=count*len(banks)
        raw=(ctypes.c_ulonglong*size)(*(g.raw_cuda_graph() if g else 0 for _,graphs,_,_ in banks for g in graphs))
        out=(ctypes.c_ulonglong*size)(*(t.data_ptr() if t is not None else 0 for _,_,selected,_ in banks for t in selected))
        inputs=(ctypes.c_ulonglong*len(banks))(*(tokens.data_ptr() for tokens,_,_,_ in banks))
        status=lib.serve(raw,out,count,inputs,config.vocab_size,config.num_hidden_layers,config.hidden_size,seconds)
        if status:raise SystemExit(status)


if __name__=='__main__':main()
