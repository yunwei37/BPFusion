# 0021: real-Qwen compute diagnostics and last-position logits

Finding [0020](0020-graph-dispatch.md) completes the whole-request dispatch
ablation. It does not detect a broad TTFT advantage and exposes serial
queueing at eight clients. The next engineering work targets actual computation
and batching while preserving the unchanged independent eager-fp16 oracle.
This diagnostic is not a new paper experiment or competitive serving result.

## Reproduction and scope

The raw profile files include the exact temporary diagnostic Python script
and command. The capture source in these pairs is the pre-optimization
`779e2f3` version (also unchanged from `e3f272e`). To reproduce against a later
checkout without changing main, load it with
`git show 779e2f3:executor/qwen_graph.py` in the diagnostic instead of reading
the current file; retain the documented native graph library and dependencies. It reads the original graph-capture source, captures all 190
model graphs, and replaces the native serve call with ordinary host graph
replays. The original exported real weights, HF operations, cache construction,
copy-back and device argmax are retained. Actual prompt token IDs populate the
input buffer; decode prefixes are prepared by the preceding model graphs.
Five sampled shapes cover prefill lengths 5/64 and decode positions 16/64/126.
Each has ten warm replays, thirty CUDA-event samples and a separate
[PyTorch profiler](https://docs.pytorch.org/docs/2.14/profiler.html) replay.

These timings exclude TCP, GPU-tail scheduling and kernel TX. Samples are
correlated repetitions in one process per variant, run sequentially rather
than paired/randomized process blocks. GPU clocks/power were not integrated
for these profiles. Do not turn their differences into a causal serving
speedup, stable tail estimate or energy result. Profiler event counts describe
CUDA device events, including any device copies, rather than CPU launches.

## SDPA candidate rejected by the fixed oracle

The bounded candidate used official
[HF SDPA](https://huggingface.co/docs/transformers/en/attention_interface)
and `logits_to_keep=1`. The
[eager profile](../../bench/results/qwen_compute_eager_profile_20261010.txt)
and [candidate profile](../../bench/results/qwen_compute_sdpa_profile_20261010.txt)
record decode-position64 event means of 2.7433 and 2.5625 ms and 1,245/1,077
CUDA device events. These are diagnostic observations, not an accepted
end-to-end improvement.

The [combined candidate regression](../../bench/results/qwen_sdpa_last_logits_correctness_20261010.txt)
failed the first 64-token prompt. Isolating changes showed that
[SDPA alone](../../bench/results/qwen_sdpa_only_correctness_20261010.txt)
also failed: output14 (zero-based13) was 3283 instead of oracle304.
It completed the TCP reply with graph_error=0 and clean teardown; this was
an output mismatch, not admission failure. The exact source delta was only
`attn_implementation='eager'` to `'sdpa'`; the combined candidate also used
last-position logits. No SDPA change is retained, and no oracle or precision
criterion was weakened. This failure bounds the tested backend against the
chosen exact oracle; it does not prove SDPA is generally incorrect.

## Retained change: compute only the needed logits

The actual HF forward supports `logits_to_keep`, slicing hidden states before
its vocabulary projection. The executor consumes only the last-position
argmax. The sole production change passes `logits_to_keep=1` to that forward;
attention remains eager, KV/precision/dispatcher/protocol are unchanged.

The isolated
[original profile](../../bench/results/qwen_eager_last_logits_profile_20261010.txt)
and [last-position profile](../../bench/results/qwen_last_logits_last_logits_profile_20261010.txt)
record the following post-capture PyTorch counters:

| capture variant | CUDA allocated bytes | CUDA reserved bytes | held logits bytes |
|---|---:|---:|---:|
| all positions | 1,839,313,920 | 2,669,674,496 | 670,341,632 |
| last position | 1,218,157,568 | 1,537,212,416 | 57,735,680 |

Allocated memory falls by **621,156,352 bytes**, about 0.62 GB. These counters
cover PyTorch-owned allocations at the same capture phase, not total GPU or
native device-graph memory. The held-logits reduction is expected from keeping
190 final-position rows rather than 2,206 rows across the catalogue.
This removes unused outputs and supplies a material memory benefit for future
batching; it is not evidence that batching already runs.

The isolated event timings were 2.5981/2.6054 ms for prefill5,
3.1337/3.1175 ms for prefill64 and 2.7400/2.7408 ms for decode-position64
(original/last-position). No latency benefit is claimed from these observations.
Finding0020's measured serving numbers precede this source change; they are
not relabeled as fresh measurements of the optimized version.

Both complete strict gen64 candidate regressions passed the original oracle:
[resident](../../bench/results/qwen_last_logits_correctness_20261010.txt) and
[host-launch](../../bench/results/qwen_last_logits_host_correctness_20261010.txt),
**303 valid requests / 19,392 exact tokens / 259 rejections per mode**,
5,000 empty connections, eight concurrent clients, reject-to-valid reuse,
pipeline/ring wrap/half-close, zero admission drops, graph_error=0, expected
host/model launch counts, all-thread network-syscall checks and clean module/pin
teardown. The temporary candidate differed from the retained script by exactly
this forward argument and used the matched native libraries from0020.

## Default RMSNorm fusion probe

The next bounded candidate compiled only the existing `Qwen2RMSNorm.forward`
with default `torch.compile`, leaving eager attention and the original model
operations around it. Its
[real gen64 regression](../../bench/results/qwen_compiled_norm_default_correctness_20261010.txt)
reached the server and returned all64 tokens with graph_error=0, but failed
at output14 of the first prompt, also3283 instead of oracle304. Network trace
and clean module/pin teardown passed. This is a failed default candidate, not
an accepted performance result. No compiler change is retained.

The installed PyTorch2.14.1 Inductor source documents that fusion may remove
fp16 downcast/upcast boundaries and provides `emulate_precision_casts` to
preserve them. That is a concrete reason to test this existing compiler option
in the temporary candidate after the default failure. It is not proof that
cast removal caused this output mismatch, nor permission to change the oracle.
The [precision-preserving regression](../../bench/results/qwen_compiled_norm_precision_correctness_20261010.txt)
also completed all64 tokens but failed at the same output14 (3283 instead of
304), with graph_error=0, passing network trace and clean module/pin teardown.
The default candidate used the pre-last-position-logits source; this second
candidate used the retained last-position argument and
`torch.compile(Qwen2RMSNorm.forward, options={"emulate_precision_casts": True})`.
Neither compiler candidate is retained. These failures do not identify which
change in arithmetic caused the divergence, and no speedup is claimed.

The full serving goal remains active. Reduce the remaining pointwise/cache
work and serial queueing, measure an accepted compute improvement on real TCP,
and complete text, optimized serving, total-host-cost and physical-NIC evidence.


## New pointwise candidate: preserve RoPE casts while fusing operations

The complete concurrent-service comparison in finding0023 establishes a local
throughput/queueing improvement, with slower per-request TPOT and inconclusive
single-client effects. Existing profiles show many small pointwise/copy events
in each decode graph. RMSNorm and SDPA accuracy failures above remain closed;
this candidate instead compiles only the existing HF apply_rotary_pos_emb.
Its operations rotate/negate, multiply and add without a reduction or a
projection/batch-shape change. torch.compile uses the default backend/mode,
with emulate_precision_casts=True to preserve the existing fp16 boundaries.
No oracle, norm, attention, projection, KV, graph-bank ownership, native
scheduler, page/module or transport changes are included.

[Exact temporary candidate source/delta](../../bench/results/qwen_compiled_rope_candidate_20261010.txt)
records the two added capture-script lines at64b1e7e. Production source remains
unchanged pending default-native qualification and a matched serving result.
The [first GPU-only attempt](../../bench/results/qwen_compiled_rope_qualification_20261010.txt)
failed before candidate load/capture: the reused old probe library does not
export the new service max_requests symbol. The wrapper already discovers its
two banks; removing that unused restype lookup is the only harness repair.
The [completed qualification](../../bench/results/qwen_compiled_rope_qualified_20261010.txt)
passes all12 two-bank groups/1,536 exact tokens, including ten gen64
prompt-edge cases and two mixed groups, with one host launch/128 model graphs/
error0 per group. This is GPU-controlled computation qualification, not a TCP
serving result or proof of general numerical equivalence.

Sequential one-process CUDA-event/profiler diagnostics preserve the exact
scripts: [baseline](../../bench/results/qwen_baseline_rope_profile_20261010.txt)
and [RoPE candidate](../../bench/results/qwen_rope_rope_profile_20261010.txt).
Each captures one bank with the same shared KV and samples five graph shapes
using ten warm/thirty measured host replays. They exclude TCP, native device
instantiation and GPU-tail scheduling. CUDA device events decrease by192 at
every sampled shape: prefill5 1197 ->1005, prefill64 1269 ->1077, decode
positions16/64/126 1149 ->957. Torch allocation/reservation/held logits are
unchanged at1,089,993,728 /1,518,338,048 /57,735,680 bytes. Event times are
sequential correlated diagnostics on a shared GPU; their differences do not
establish causal compute or serving speedup. A real paired service comparison
is necessary to decide whether to retain this candidate.

## RoPE serving comparison plan

This is supporting engineering evidence for the user's throughput/latency
objective; there is no paper RQ/thesis to invent. The unresolved question is
whether reducing pointwise model-graph work improves actual TPOT/throughput
with the qualified no-userspace-worker concurrent serving mechanism. Positive
matched effects justify retaining the small exact candidate; negative or
inconclusive effects leave the production capture unchanged and direct work
elsewhere. Finding0023 changed concurrency, not this model computation, and
its results cannot settle the RoPE effect. Repeating KV/dispatch or the closed
norm/SDPA candidates would add no answer. This is the strongest immediately
runnable component comparison; optimized serving remains a separate wider
service evaluation, not a condition for publishing this local result.

Baseline is the current concurrent private-bank capture at64b1e7e. Candidate
changes only the two qualified RoPE compile lines. Both discover eight banks,
share the identical native library (with the same checked temporary listener
TCP_NODELAY call), and use the same weights, model shapes/eager fp16 operations
outside RoPE, shared KV, independent batch1 oracle, GPU sampling, FIFO ring,
module and one host service launch. This is a current-practice/component
baseline, not a SOTA/optimized external server. The serial host control only
provides correctness coverage. [Adapter/raw source provenance](../../bench/results/qwen_compiled_rope_adapter_20261010.txt)
contains the exact renamed existing driver, common native source diff,
symlink targets, frozen capture-source delta and instantiated commands.

Before full collection, complete both default-native strict gen64/prompt-edge
TCP regressions and the real preflight. Keep every original oracle assertion,
request/shutdown timeout, trace/lifecycle check and metric; readiness remains
ready-or-process-exit as already qualified for bank capture. Use the owning
ephemeral compiler cache, without a permanent helper or configuration layer.
No candidate production change occurs before the complete comparison and
result review.

The fixed matrix is four real prompts, gen1/gen64, clients1/8, five alternating
paired process blocks with rotating matching cell order,64 requests/cell
(16 per prompt),eight excluded warmups/process and a separate one-second
idle CPU sample. Full result is40 cells,2,560 exact requests,83,200 measured
tokens and ten normal exits; each process must have one service launch,
8,580 device model graphs/error0,264 publications,zero admission/registration
errors,eight FREE slots,and clean module/hooks/pins. Default tests additionally
cover invalid input, mixed lengths, persistent reuse, pipeline and half-close.
The separate real preflight uses gen1/client1/four requests per engine and
establishes executability only.

Primary metrics are gen64 TPOT and total output TPS at clients1 and8,
following [NVIDIA definitions](https://docs.nvidia.com/nim/benchmarking/llm/metrics).
TPOT=(last-first)/63; TPS is all output tokens divided by first-send to
last-arrival. Assess all four primary effects separately using all five paired
blocks and nominal two-sided t95,df4,without familywise correction. Positive
means baseline-minus-RoPE TPOT or RoPE-minus-baseline TPS. A positive one and
inconclusive others is mixed support; report contradictions and tradeoffs
without selecting cells post-hoc or collapsing to a weighted score. TTFT,
completion,p99 descriptions,gen1,bootstrap and executor-PID/idle CPU remain
reported diagnostics. Supplementary completion analysis reuses stored
request timestamps; the barrier/future CPU window is intentionally broader
than the TPS denominator. Connection/thread creation and model/capture
bootstrap precede active measurement; record bootstrap separately.

Record GPU endpoint clocks/temperature/power/utilization and host residency
before/after; preserve the SGLang co-tenant. These coarse snapshots do not
prove isolation,within-window overlap,integrated energy or steady co-tenant
load. No fixed isolated percentage,physical-NIC,open-load,total-host/energy
or competitive-serving claim follows. Fresh read-only plan/result reviewers
assess validity and the declared narrow decision; no separate saved report is
claimed. Exact full/preflight commands and raw-result paths are in the adapter
raw. All sources/driver remain frozen during collection.


Default-native candidate qualification completed in both modes:
[resident](../../bench/results/qwen_compiled_rope_resident_correctness_20261010.txt)
and [serial host control](../../bench/results/qwen_compiled_rope_host_correctness_20261010.txt),
each335 valid requests /20,432 exact tokens /259 rejects,5,000 empty
connections, eight-client persistent invalid-to-valid reuse,32 mixed-length
requests,ordered pipeline,half-close,ring wrap,zero errors,eight FREE slots,
all-thread network trace and clean module/hooks/pins. Resident has one host
launch,banks8,max_active8; host control has594 host launches,banks1,max_active1.
The capture candidate remains temporary; this proves correctness at default
transport,not serving benefit.

Fresh read-only plan review admitted the frozen two-line candidate and matched
comparison, conditional on both strict qualifiers and real preflight passing.
Both qualifiers are now terminal and pass. Reviewer independently confirmed
source identity/common binary,independent oracle,all12 GPU groups,count/sign/
metric formulas,new decision value and minimal source growth. Preserve all
four primary effects and the shared-GPU/nominal-interval boundary; report
bootstrap separately with the already populated ephemeral compiler cache.
Result review must independently verify counters/FREE/cleanup. No separate
saved reviewer report is claimed.
