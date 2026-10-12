# Independent plan review: GPU-owned vLLM generation qualification

Read-only review on 2026-10-12 in the retained bpfusion-dev Workspace.
This report is the sole file written. No GPU execution, build, model/source/plan
edit, process intervention or Git action was performed.

## Verdict and decision value

Admit the planned implementation qualification. No scientific or API-level
executability blocker was found in the declared route. This is dependency
work inside optimized-backend integration, with zero independent paper value;
it must not be presented as serving performance or as the completed goal.

The previous FULL-body mirror cannot answer whether sampled output can feed
the next optimized decode without a CPU step loop. The new body+official
head/sampler+GPU metadata loop tests that missing transition directly.
Success permits GPU prefill/admission/queue lifecycle integration. Failure
localizes a real unsupported graph/state interface; it is not an optimized
serving loss or permission to replace the fixed reference. Repeating the
mirror or external-serving matrix would not resolve this next dependency.

The route preserves upstream model computation instead of starting another
model-arithmetic optimization campaign. A second baseline, more models,
new performance threshold or arbitrary workload expansion is not required
for this finite implementation qualification.

## Reviewed sources and established boundary

Read vllm_generation_plan_20261012.md completely, archived
vllm_reuse_qualify_20261012.py and vllm_reuse_bridge_20261012.cu,
vllm_reuse_result_review_20261012.md, the full frozen JSONL and the actual
installed source in:

 /tmp/bpfusion-vllm-reuse-j3k3go83/venv/lib/python3.12/site-packages/vllm

Independent CPU reconstruction of vllm_reuse_full_20261012.jsonl confirms:
19 reference groups,74 lanes,4736 reference IDs, every sequence length64.
All reference events precede references_frozen, which precedes any device
call. The1197 mirror calls all report host/device code0, entered1 and
bit-equal hidden outputs. This is real evidence for launchable FULL bodies,
not autonomous generation: official CPU sampling and metadata advancement
produced those earlier token trajectories. Restored CPU outputs alone
therefore remain insufficient for the new qualification.

The planned script/native generation implementation is not yet present in the
listed apparatus. This review admits its source-grounded design; it does not
claim a nonexistent generate_qualify.py has already run or prove its future
code correct. Its actual implementation/build/command must be retained and
real preflight must resolve runtime capture/launch compatibility.

## Official head and sampler seam

model_executor/models/qwen2.py:512-517 exposes compute_logits(hidden_states)
through the actual model logits processor and LM head.

v1/worker/gpu/sample/sampler.py:275-352 shows the official greedy path:
apply_sampling_params, top-k/top-p handling, then gumbel_sample when the
fused random-sampling path is not eligible. v1/worker/gpu/sample/gumbel.py:
326-381 exposes the callable with logits, expanded_idx_mapping, temperature,
seed and pos, plus explicit apply_temperature/is_drafting options.
Its temp0 branch is plain argmax. It returns actual int64 sampled IDs via
official reduction/gather operations. Thus capturing compute_logits plus
gumbel_sample is a valid upstream computation seam for the declared
temperature0/no-penalty/no-logit-processor request subset.

Do not silently assume a generic sampler equivalence: preserve the actual
temperature0 sampling-state rows, request mapping, tensor dtype/stride,
vocabulary and relevant flags from the official prepared group. Seeds have no
sampling effect at temp0 but their owner tensors still must remain valid.
This does not qualify arbitrary penalties, structured output, random
sampling, speculative decode or another architecture.

Persistent hidden output ownership exists in
v1/worker/gpu/cudagraph_utils.py:617-634; the model graph writes into
manager-owned hidden_states. ModelCudaGraphManager.run_fullgraph:751-764
returns the active prefix. Capture the official head on that real active
prefix, not a standalone copied/constant hidden tensor, and retain all head
capture/intermediate/sampled-output tensor owners until native destruction.

## Input, attention and KV interfaces

The actual InputBatch is a dataclass with request IDs, idx_mapping,
expanded_idx_mapping, query_start_loc, seq_lens, input_ids, positions,
logits_indices and padding/state information
(v1/worker/gpu/input_batch.py:39-119). It is not the older runner InputBatch
API. A mixed prompt group need not have trivial request-index ordering; use
the actual req_ids/idx_mapping and map GPU outputs back to frozen lane order.
The plan explicitly records row mapping, avoiding an assumed0..batch-1
scheduler ordering.

GPUModelRunner.prepare_attn in v1/worker/gpu/model_runner.py:1520-1538 gathers
block tables and computes slot mappings from prepared rows/positions.
BlockTables in v1/worker/gpu/block_table.py supplies:
- append_block_ids:117-137, with overwrite/append and allocator-block to
  kernel-block expansion;
- apply_staged_writes:139-151, publishing staged table content;
- gather_block_tables:153-180, staging request-state rows into persistent
  model input tables;
- compute_slot_mappings:195-224, with padding/CP/group rules;
- slot construction:324-366, based on the actual kernel block size and
  req_state_idx mapping.

Appending allocator IDs alone does not update the captured model's gathered
input table. Apply staged writes and gather the actual input rows before the
autonomous loop; retain those owners. For this ordinary single-GPU Qwen
condition, slot = actual block number * kernel block size + position offset,
but derive block/kernel sizes and row mapping from the actual API. Do not
reuse the ring slot count as an allocator/block-layout assumption or advance
slot_mapping by simple+1 across a page boundary.

KVCacheManager.allocate_slots is the real reservation seam
(v1/core/kv_cache_manager.py:371-403,496-614). It accounts for the request's
computed boundary, existing/prefix blocks and available pool; it returns
new blocks or None. Reserve the future range through the real scheduler
request while CPU progression is paused, handle None as a retained failure,
and publish returned blocks through BlockTables. Allocation has cache
side-effects and caps committed prefix cache at request.num_tokens
(:603-614). Preserve allocator ownership; do not fabricate block IDs,
release them early, or manually mark ungenerated future tokens computed.

At the first FULL hook the scheduler may already have advanced the request's
optimistic computed counter for the currently scheduled decode. Therefore
derive the required reservation from actual positions/counters, not only
the constant63. Log initial/final positions, seq_lens, block rows, sizes,
slot mapping and allocator request boundary as planned. For prompt lengthP,
the63 child computations consume positionsP..P+62; recording the precise
post-final metadata update convention prevents an off-by-one interpretation.

DefaultModelState.prepare_attn in
v1/worker/gpu/model_states/default.py:169-234 passes seq_lens, block tables,
slot mappings and positions into real attention metadata. FULL capture sets
the static max_seq_len to max_model_len (:197-199), which supports replay at
increasing context length without shrinking the capture-time bound.
This is not a guarantee that every captured auxiliary metadata tensor updates
itself. The inspected FlashAttention builder may construct scheduler metadata
when aot_schedule is enabled; identify the actual selected path. Fixed
batch/query layout can remain fixed, but every changing captured metadata
buffer must read the GPU-updated value.

Prior catalogs include memcpy nodes (25 for batch1,1 for batches2/4/8).
A launchable graph does not prove those copies will preserve device-advanced
inputs/metadata on repeated replay. Inspect their actual source/destination or
otherwise show the loop's complete trajectory uses the intended updated
state. This is an implementation hazard and a discriminating failure cause,
not a request to strip memcpy/model nodes or change the independent oracle.

## Ordering, native loop and contamination control

The composed child must order actual body before actual head/sampler through
an explicit graph dependency. The parent must consume sampled IDs only after
the child execution environment completes, then publish input IDs and
metadata before its next child launch. CUDA tail launch supplies the same
fork/join completion seam used in the qualified bodies; merely using
FireAndForget without the join would leave a race.

New parent executable needs device-launch capability, upload and correct
runtime linkage before it can tail-launch itself. The old mirror bridge's
parent was instantiated with flags0 because it never device-launched that
parent. Reusing that constructor unchanged would break the planned loop.
This is a concrete implementation requirement, not a detected existing code
defect because generation bridge implementation is not yet present.

Plan counts are coherent: one host parent launch per group,63 composed child
launches,64 parent entries (initial launch plus final completion tail).
The token array must contain the actual CPU-prefill token1 followed by63
new GPU sampled tokens/lane; sampled IDs must become next input IDs.
Frozen future tokens may be used only for comparison, never supplied as the
GPU input trajectory. No host read, CPU sampler, per-token reservation or
submission may occur inside the native generation loop.

After completion, restore the pre-loop prepared input/position/seq_len/
slot metadata and saved official hidden output before official CPU sampling
resumes. Warmup/capture must not overwrite the saved bootstrap state.
Restore any additional live buffer modified by the chosen metadata/sampler
implementation; retaining an InputBatch Python object alone is not restoring
its tensor storage. Existing prompt/past KV must remain untouched; future
KV may be overwritten by the continuing official trajectory. Allocation
ownership remains official until the request ends.

Both independently read native output arrays and the continuing official
64-token sequence must match the previously frozen group reference. Native
agreement detects generation/math/state error; continuing CPU agreement
checks observed contamination. Neither substitutes for the other. Continuing
agreement is finite trajectory evidence, not proof that all cache bytes or
other-model state are unchanged.

## Execution, counts, scope and next step

Use the actual existing temporary venv and apparatus. The plan's preflight
command is one real64-token group, followed by the same source/native path
for all19 groups. Full expected coverage:
-19 groups and74 lanes;
-4736 output IDs checked against the frozen references;
-4662 IDs generated after CPU bootstrap by autonomous loops;
-1197 composed child launches and1216 parent entries across groups;
-19 host parent launches, all statuses retained, all native owners destroyed.

The already-qualified mirror/source-native reference can be reused; no new
reference generation after observing prototype outputs, tolerance, prompt
exclusion or precision change is justified. HF eager agreement stays separate.
Finite/in-range outputs, full arrays and exact reference agreement matter;
launch counts alone cannot qualify autonomous generation.

The actual build must preserve the previously successful explicit graph
construction and loaded-runtime linkage. Destroy native handles before raw
body/head graphs, model/KV/input/output owners release, including on a failed
or partially constructed attempt. Retain all partial outputs, failed
commands/statuses and the exact implemented source. The existing apparatus
has a mixed-toolkit/runtime boundary, already recorded in the mirror review;
success here would remain an empirical artifact qualification.

No serving latency/TPS, variable online batching, autonomous prefill/admission,
kernel queue/TCP, total CPU/energy, other-model or entire-goal completion
claim follows. After real native sequence qualification, implement the
missing GPU prefill/admission and lifecycle and attach the existing kernel
queue/TCP route; then compare genuinely identical compute backends.

Run status: planned implementation; new generation loop untested.
Hypothesis: untested.
Research value: dependency-only inside admitted optimized-backend integration.
Paper impact: optimized-backend implementation boundary.
Next decision: implement this source-native seam and real preflight, preserving
all negative evidence; no unclosed plan-level blocker or added approval gate.
