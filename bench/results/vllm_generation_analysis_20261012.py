#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reconstruct autonomous vLLM generation outputs and state progression."""
import collections,json,pathlib
base=pathlib.Path(__file__).resolve().parent
rows=[json.loads(l) for l in (base/"vllm_generation_full_20261012.jsonl").open()]
refrows=[json.loads(l) for l in (base/"vllm_reuse_full_20261012.jsonl").open()]
refs={r["group"]:r for r in refrows if r["event"]=="reference"}
native={r["group"]:r for r in rows if r["event"]=="native"}
groups={r["group"]:r for r in rows if r["event"]=="group"}
cases=None
for l in (base/"qwen_vllm_20261012.jsonl").open():
 r=json.loads(l)
 if r["event"]=="metadata":cases=r["cases"];break
owners=next(r for r in rows if r["event"]=="owners")
assert owners["block_sizes"]==owners["kernel_block_sizes"] and len(owners["block_sizes"])==1
size=owners["kernel_block_sizes"][0]
assert set(native)==set(groups)==set(refs)==set(range(19))
for i in refs:
 n=native[i];g=groups[i];ref=refs[i];batch=ref["condition"]["batch"]
 assert n["code"]==n["device_error"]==0
 assert (n["child_launches"],n["parent_calls"],n["token_writes"],n["host_parent_launches"])==(63,64,batch*64,1)
 assert len(n["output_ids"])==batch and all(len(x)==64 for x in n["output_ids"])
 assert len(set(n["external_request_ids"]))==batch
 expected=collections.defaultdict(list);actual=collections.defaultdict(list)
 for k,out in zip(ref["condition"]["cases"],ref["output_ids"]):expected[tuple(cases[k][0])].append(tuple(out))
 for prompt,out in zip(n["input_ids"],n["output_ids"]):actual[tuple(prompt)].append(tuple(out))
 assert {k:sorted(v) for k,v in actual.items()}=={k:sorted(v) for k,v in expected.items()}
 assert g["reference_exact"] and g["continuing_cpu_exact"]
 assert g["output_ids"]==g["continuing_cpu_ids"]==ref["output_ids"]
 for row,(out,prompt,p0,s0,p1,s1,slot0,slot1,blocks) in enumerate(zip(
   n["output_ids"],n["input_ids"],n["initial_positions"],n["initial_seq_lens"],
   n["final_positions"],n["final_seq_lens"],n["initial_slot_mapping"],
   n["final_slot_mapping"],n["block_ids"])):
  assert out[0]==n["initial_input_ids"][row]
  assert p0==len(prompt) and s0==p0+1
  assert p1==p0+62 and s1==s0+62
  assert len(blocks)*size>p1
  assert slot0==blocks[p0//size]*size+p0%size
  assert slot1==blocks[p1//size]*size+p1%size
assert len([r for r in rows if r["event"]=="instantiate" and r["code"]==0])==4
assert len([r for r in rows if r["event"]=="destroy" and r["code"]==0])==4
assert not any(r["event"]=="failure" for r in rows)
assert rows[-1]["event"]=="terminal" and rows[-1]["exit_code"]==0
assert json.loads((base/"vllm_generation_full-status_20261012.json").read_text())["exit_code"]==0
print(json.dumps(dict(groups=19,lanes=74,checked_tokens=4736,cpu_prefill_seed_tokens=74,
 gpu_generated_tokens=4662,host_parent_launches=19,child_launches=1197,parent_calls=1216,
 reference_exact_lanes=74,continuing_cpu_exact_lanes=74,
 hf_eager_exact_lanes=sum(sum(r["hf_exact"]) for r in groups.values()),
 scope="autonomous decode after CPU prefill; network integration unfinished"),indent=2))
