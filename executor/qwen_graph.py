#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Capture Qwen at bootstrap; the native GPU graph dispatcher owns requests."""
import ctypes
import struct
import sys
from pathlib import Path
import numpy as np
import torch
from transformers import AutoConfig,AutoModelForCausalLM
from transformers.models.qwen2.modeling_qwen2 import Qwen2RotaryEmbedding
from transformers.cache_utils import DynamicCache
from transformers.masking_utils import create_causal_mask


def load_model(path):
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
    if len(sys.argv)<2:raise SystemExit('usage: qwen_graph.py WEIGHTS.bin [seconds]')
    seconds=int(sys.argv[2]) if len(sys.argv)>2 else 60
    lib=ctypes.CDLL(str(Path(__file__).resolve().parents[1]/'build/qwen_graph.so'))
    lib.max_tokens.restype=ctypes.c_uint
    limit=lib.max_tokens();context=2*limit
    with torch.no_grad():
        model=load_model(sys.argv[1]);config=model.config
        dim=config.hidden_size//config.num_attention_heads
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
                if pos==0:return None
                return DynamicCache(ddp_cache_data=[(k[:,:,:pos],v[:,:,:pos]) for k,v in zip(keys,values)],config=config)
            def forward():
                return model(inp,position_ids=positions,attention_mask={'full_attention':mask},past_key_values=cache(),use_cache=True)
            mask=create_causal_mask(config=config,inputs_embeds=model.model.embed_tokens(inp),attention_mask=None,past_key_values=cache(),position_ids=positions)
            stream.wait_stream(torch.cuda.current_stream())
            with torch.cuda.stream(stream):warm=forward()
            torch.cuda.current_stream().wait_stream(stream);torch.cuda.synchronize()
            graph=torch.cuda.CUDAGraph(keep_graph=True)
            with torch.cuda.graph(graph,stream=stream):
                output=forward()
                token=output.logits[:,-1,:].argmax(-1)
                for l,layer in enumerate(output.past_key_values.layers):
                    keys[l][:,:,:pos+count].copy_(layer.keys);values[l][:,:,:pos+count].copy_(layer.values)
            graphs.append(graph);selected.append(token);keepers.append((output,positions,mask,inp))
            if index%32==0:print(f'captured model graph {index}/{limit+context-2}',flush=True)
        torch.cuda.synchronize()
        lib.serve.argtypes=[ctypes.POINTER(ctypes.c_ulonglong),ctypes.POINTER(ctypes.c_ulonglong),ctypes.c_uint,ctypes.c_ulonglong,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint,ctypes.c_uint]
        lib.serve.restype=ctypes.c_int
        raw=(ctypes.c_ulonglong*len(graphs))(0,*(g.raw_cuda_graph() for g in graphs[1:]))
        out=(ctypes.c_ulonglong*len(selected))(0,*(t.data_ptr() for t in selected[1:]))
        status=lib.serve(raw,out,len(graphs),tokens.data_ptr(),config.vocab_size,config.num_hidden_layers,config.hidden_size,seconds)
        if status:raise SystemExit(status)


if __name__=='__main__':main()
