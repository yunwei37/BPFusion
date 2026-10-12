# Short inputs still traverse the captured model graph

This diagnosis answers why the current two-model backend still has millisecond
first-token latency for inputs of only 2/5/8 tokens. The captured model execution
region dominates the instrumented local measurement. It selects the next
backend investigation; it is not a standalone paper result or serving speedup.

## Conditions and completion

Production source is unchanged main 9954855859fdc14b7f38dc2ec21768b4fc054f02.
Two sequential resident kernel-network executors reuse the current FP16 HF
computation and cached checkpoints on the original RTX 5090 Workspace.
One persistent loopback HTTP connection, one client and gen 1 are used.
Each model has four declared warmups followed by sixteen measured requests;
all forty actual first tokens match the archived independent eager-HF oracle.
Both executors exit normally, with one host launch, twenty device graph
launches, zero graph errors, eight banks and max_active=1.

Temporary adapters add CUPTI device-graph tracing, torch.profiler export,
source graph-node catalogues and CPU monotonic clock anchors around the
existing native serve call. Native computation, module, BPF ABI and transport
settings are unchanged. The driver and adapter sources are embedded in raw
metadata; the actual corrected analyzer is archived separately for replay.

## Measured localization

Means below exclude only the four declared warmups per model. These are
profiled loopback measurements, not the earlier cross-node comparison.

| Model | Input tokens | Requests | Client TTFT, ms | First-to-last model kernel span, ms | Kernel nodes/request |
|---|---:|---:|---:|---:|---:|
| SmolLM2-135M | 2 | 4 | 3.227111 | 3.041962 | 1460 |
| SmolLM2-135M | 5 | 8 | 3.113097 | 2.994598 | 1490 |
| SmolLM2-135M | 8 | 4 | 3.116806 | 2.971194 | 1490 |
| Qwen2.5-0.5B | 2 | 4 | 2.419906 | 2.188481 | 808 |
| Qwen2.5-0.5B | 5 | 8 | 2.408797 | 2.216517 | 808 |
| Qwen2.5-0.5B | 8 | 4 | 2.410336 | 2.224490 | 808 |

Across sixteen measured requests, Smol TTFT is 3.142528 ms and model span
3.000588 ms, or 95.48%. Qwen TTFT is 2.411959 ms and model span 2.211501 ms,
or 91.69%. Complete source-node/trace coverage and independent reconstruction
support this localization:29650 Smol and 16160 Qwen model-kernel records
across all forty requests, plus all twenty Qwen graph memset activities.

A short input still traverses all transformer layers, the output head and
greedy selection. Shortening the token dimension from 8 to 2 does not remove
those operations. CUDA Graph avoids repeated host submission but retains
the many individual GPU kernels; it is not automatic megakernel fusion.
Parameter count alone does not rank this backend's short-request latency.

Mean kernel-only interval unions are 2.238712 ms and 1.796659 ms. The remaining
0.761876 ms and0.414842 ms inside the respective model spans are cumulative
inter-kernel gaps. The trace does not distinguish scheduling, dependencies,
instrumentation or other causes for each gap; these are not established
pure host-launch overhead or memory-bandwidth/FLOP bottlenecks. Qwen's
internal memset averages 0.3904 us and is inside the span but outside the
kernel-only union. Dispatcher activity is excluded, so union is not GPU
utilization.

Mean last-model-kernel to client arrival estimates are 0.124545 ms and
0.181419 ms. They combine tail dispatch/output publication, kernel polling,
TCP and client receive. Sampling argmax is already inside the captured graph;
this residual cannot be called pure network/TX time.

## Clock and profiling limits

CPU anchor intersections have half-widths 17.6035 us for Smol and 16.4225 us
for Qwen. Mean ingress-to-first-kernel midpoint estimates 4.565 us and 2.688 us
are unresolved within those bounds. Qwen request indices 7/11 retain signed
negative midpoint estimates within the uncertainty; they are not physical
negative delays. The independent reviewer additionally finds one common
offset compatible with all request causal boundaries.

The retained initial analysis failure came from demanding causal ordering
for every conservative allowed offset. The correction checks compatibility,
retains signed estimates, and changes neither raw data nor oracle. GPU model
spans are offset-independent. CPU anchors do not separately measure CUPTI
GPU-to-common-axis synchronization error, and profiling/pacing can change
durations. No precise microsecond dispatch claim follows.

The host journal contains NVRM refcntRequestReference_IMPL warnings before
each model completes; their relation to latency is unknown. All requests,
native exits and trace coverage pass. Endpoint GPU reads do not prove
continuous device isolation or absence of timing interference.

Do not subtract this local profiled result from the older cross-node means
to invent network overhead. The earlier same-compute kernel/userspace
comparison remains inconclusive: its primary TTFT and throughput intervals
contain zero. This diagnosis has no userspace baseline and does not resolve
concurrent throughput, shared-weight batching or total service CPU.

## Next decision and artifacts

Prioritize qualifying an existing faster backend, then use that identical
backend in both serving paths. Keep the contribution in eBPF-driven request
admission, GPU handoff, completion and response delivery; backend arithmetic
improvements cannot be attributed to eBPF. Avoid another unchanged network
matrix or an open-ended single-model arithmetic optimization campaign.

- [Plan](../../bench/results/short_input_latency_plan_20261012.md)
  and [independent plan review](../../bench/results/short_input_latency_plan_review_20261012.md).
- [Raw requests, sources and logs](../../bench/results/short_input_latency_20261012.jsonl).
- [Smol Chrome trace](../../bench/results/short_input_latency_smol_20261012.json.gz)
  and [Qwen Chrome trace](../../bench/results/short_input_latency_qwen_20261012.json.gz).
- [Replay analyzer](../../bench/results/short_input_latency_analysis_20261012.py),
  [successful output](../../bench/results/short_input_latency_analysis_20261012.txt),
  [initial failure](../../bench/results/short_input_latency_analysis_initial_20261012.txt)
  and [per-request stages](../../bench/results/short_input_latency_stages_20261012.jsonl).
- [Independent result review](../../bench/results/short_input_latency_result_review_20261012.md)
  and [restoration audit](../../bench/results/short_input_latency_restoration_20261012.json).

From the repository root, replay with
`python3 bench/results/short_input_latency_analysis_20261012.py`.
The analyzer reconstructs all forty requests and regenerates the stage JSONL.
Both original model processes and the driver are absent; own module/pins
are absent and successful nvidia-smi finds no compute applications.
Temporary apparatus is removed after archiving. Unrelated
`tools/setup_env.sh` is preserved.
