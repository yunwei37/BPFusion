# GPU-owned generation using official vLLM computation

The retained objective is the full eBPF/kernel-queue/GPU/kernel-TCP service,
with upstream computation and improved throughput/latency. The complete
FULL-body reuse qualification establishes real GPU graph launch for batch
1/2/4/8. It does not generate tokens autonomously, because sampling and
metadata advancement still belong to the upstream CPU loop.

This is the next necessary implementation qualification inside optimized
backend integration, with zero independent paper value. No paper RQ is
invented. A successful GPU-owned decode loop permits the queue adapter;
failure identifies the actual missing computation/state interface. Repeating
the completed mirror or external-serving matrix cannot answer this question.

## Fixed computation and independent control

Use the same pinned vLLM0.31.0/Torch2.13+cu129/Transformers5.17 environment,
Qwen2.5-0.5B FP16 checkpoint and original Workspace/main. Keep vLLM default
optimized model/attention/compilation. Retain raw graph definitions and use
the supported test-local in-process engine as in the completed qualification.

Reuse the already independently frozen19-group reference matrix:
batch1/2/4/8, four homogeneous prompts each and cycling mixed prompts at
batch2/4/8,74 lanes,64 output tokens/lane. Check complete native GPU outputs
against those official host sequences. HF eager agreement remains separate.
Do not replace the reference with the prototype's output or fit a tolerance.

Bootstrap through official prefill and first-token sampling. At the first FULL
decode, retain the prepared InputBatch/owners; reserve future KV blocks through
the actual upstream KVCacheManager, publish them through its BlockTables API.
No custom page allocator or CPU per-token reservation. Record actual block
IDs, sizes, row mapping, initial/final positions, seq_lens and slot mappings.

Capture the actual model.compute_logits and upstream gumbel_sample using
greedy temperature0, no penalties/logit processors and the existing persistent
hidden states. This adds the official output head/sampler to the qualified
FULL body, without authoring model math or replacing attention/sampling.

A native CUDA graph composes body and head with explicit dependency. A GPU
parent dispatches it, reads sampled tokens, advances input_ids/positions/
seq_lens/slot_mappings, and tail-launches itself until all63 remaining tokens
finish. The first output token is CPU-prefill bootstrap;63 new tokens/lane
must come from the autonomous GPU loop. One host parent launch per group,
63 child launches and64 parent invocations are expected, with all errors
retained. Actual token arrays are copied/read only after the loop finishes.

After the loop, restore the original prepared metadata and saved official
hidden states before the upstream CPU sampler resumes. Reserved blocks remain
owned by the official request allocator. Future KV positions are overwritten
by subsequent official steps; existing prompt/past KV must not be changed.
Require the continuing official64-token sequence to match its frozen control
as an additional state-contamination check. This restored CPU sequence alone
cannot qualify the native loop: its independent GPU token array must match too.

## Execution and scope

Apparatus remains inside /tmp/bpfusion-vllm-reuse-j3k3go83 in the original
bpfusion-dev Workspace. Real command:
venv/bin/python generate_qualify.py --preflight --output generation_preflight.jsonl
then the same command without --preflight for all19 groups.

Use actual loaded runtime linkage, explicit CUDA graph construction, owner
lifetimes and device-error accounting proven by the prior interface repair.
Keep CPU submission outside the GPU step loop. Destroy native handles before
model/KV/graph/output owners release; preserve negative/partial attempts.

Preflight uses one real64-token group. Complete matrix has19 groups,74 lanes,
4736 checked output tokens,of which4662 are generated after CPU bootstrap
inside autonomous device loops. Record parent/child counts,status,all output
arrays and continuing official outputs. No performance threshold or new
runtime tuning is introduced. This qualification does not establish kernel
network integration, worker-free prefill/admission, variable online batching,
total CPU/energy, other models, or a serving latency/TPS win.

Archive ordinary source/build/command/status/raw outputs and analysis under
bench/results/vllm_generation_*. Fresh plan and result review apply.
After qualification, finish GPU prefill/admission/slot lifecycle and connect
the existing kernel queue/TCP path; compare the identical compute backend
against the efficient userspace path. Keep the full retained goal open.

## Preflight interface repair

The first native loop completed63 child launches/64 parent invocations, but
the qualifier then failed to join internal randomized request IDs with public
output IDs. Its output and exit1 remain archived. Use the existing official
OutputProcessor.request_states[rid].external_req_id mapping captured while
the request is live; do not disable randomization or parse IDs. Computation,
inputs,reference,checks and native source are unchanged. The corrected real
preflight and complete matrix both retain launching-parent wait exit0.
