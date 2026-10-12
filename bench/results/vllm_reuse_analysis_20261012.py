#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Reconstruct the completed official vLLM graph-reuse qualification."""
import collections,json,pathlib
base=pathlib.Path(__file__).resolve().parent
rows=[json.loads(line) for line in (base/"vllm_reuse_full_20261012.jsonl").open()]
refs={r["group"]:r for r in rows if r["event"]=="reference"}
observed={r["group"]:r for r in rows if r["event"]=="instrumented"}
assert set(refs)==set(observed)==set(range(19))
assert all(observed[i]["output_ids"]==refs[i]["output_ids"] for i in refs)
assert all(observed[i]["reference_exact"] for i in refs)
calls=[r for r in rows if r["event"]=="device_call"]
assert len(calls)==1197
for r in calls:
 assert r["code"]==r["device_status"]==0 and r["entered"]==1
 assert r["poisoned"] and r["finite"] and r["bits_equal"] and r["numeric_equal"]
 assert r["max_abs"]==0
shape_counts=dict(collections.Counter(str(r["num_tokens"]) for r in calls))
assert shape_counts=={"1":252,"2":315,"4":315,"8":315}
assert all(sum(r["group"]==i for r in calls)==63==observed[i]["device_calls"] for i in refs)
for phase in (refs,observed):
 assert sum(len(r["output_ids"]) for r in phase.values())==74
 assert all(len(seq)==64 for r in phase.values() for seq in r["output_ids"])
catalogs=[r for r in rows if r["event"]=="catalog"]
assert len(catalogs)==4 and all(r["code"]==0 and r["counts"][0]>0 for r in catalogs)
assert all(not any(r["counts"][2:]) for r in catalogs)
assert len([r for r in rows if r["event"]=="instantiate" and r["code"]==0])==4
assert len([r for r in rows if r["event"]=="destroy" and r["code"]==0])==4
assert rows[-1]["event"]=="terminal" and rows[-1]["exit_code"]==0
assert json.loads((base/"vllm_reuse_full-status_20261012.json").read_text())["exit_code"]==0
assert not any(r["event"]=="failure" for r in rows)
print(json.dumps(dict(groups=19,lanes=74,cpu_loop_tokens_per_phase=4736,
 device_calls=len(calls),shape_counts=shape_counts,
 checked_active_fp16_elements=sum(r["elements"] for r in calls),
 native_handles=4,official_sequence_exact=74,
 hf_eager_sequence_exact=sum(sum(r["hf_exact"]) for r in refs.values()),
 scope="GPU FULL-body mirror; upstream CPU loop still generates sequences"),indent=2))
