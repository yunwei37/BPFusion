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
