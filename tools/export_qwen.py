#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Export HF Qwen2 weights for the resident CUDA reference; weights stay outside Git."""
import argparse
import struct
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM

p = argparse.ArgumentParser()
p.add_argument("output")
p.add_argument("--model", default="Qwen/Qwen2.5-0.5B-Instruct")
a = p.parse_args()
m = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.float16).eval()
c = m.config
assert c.model_type == "qwen2" and c.tie_word_embeddings and c.hidden_act == "silu"
assert not c.use_sliding_window
rope = c.rope_parameters
assert rope['rope_type'] == 'default'
weights = m.state_dict()
path = Path(a.output)
path.parent.mkdir(parents=True, exist_ok=True)
with path.open('wb') as f:
    f.write(struct.pack('<6I2f', c.hidden_size, c.intermediate_size, c.num_hidden_layers,
                        c.num_attention_heads, c.num_key_value_heads, c.vocab_size,
                        c.rms_norm_eps, rope['rope_theta']))
    names = ['model.embed_tokens.weight']
    for i in range(c.num_hidden_layers):
        prefix = f'model.layers.{i}.'
        names += [prefix + name for name in (
            'input_layernorm.weight', 'self_attn.q_proj.weight', 'self_attn.q_proj.bias',
            'self_attn.k_proj.weight', 'self_attn.k_proj.bias',
            'self_attn.v_proj.weight', 'self_attn.v_proj.bias', 'self_attn.o_proj.weight',
            'post_attention_layernorm.weight', 'mlp.gate_proj.weight',
            'mlp.up_proj.weight', 'mlp.down_proj.weight')]
    names += ['model.norm.weight']
    for name in names:
        f.write(weights[name].detach().cpu().contiguous().numpy().tobytes())
print(f'exported {a.model}: {path.stat().st_size} bytes, config={c.hidden_size}/{c.intermediate_size}/{c.num_hidden_layers}/{c.num_attention_heads}/{c.num_key_value_heads}/{c.vocab_size}')
