# Current optimized short-input latency localization

With the unchanged optimized vLLM backend and module-free kernel loop,
profiled local gen1/c1 requests show about a millisecond in the model-kernel
span. Ordinary-serving stage allocation remains unproved.
The full ordinary/profiling comparison completes both models, five paired
process blocks each, with400 checked requests/400 tokens (320 measured,
80 excluded checked warmups). It supports bounded current-backend localization,
not a transport speedup or an arithmetic-specific bottleneck diagnosis.

## Question and actual execution

Retain finding0030's question: why do2/5/8-token inputs retain millisecond
first-token latency? Old0030 measured older HF computation; logical current
traces cannot reconstruct missing optimized GPU kernel durations.
The [plan](../../bench/results/optimized_latency_profile_20261014/plan.md) and
[fresh plan review](../../bench/results/optimized_latency_profile_20261014/plan-review.md)
admit supporting evidence. There is no new formal paper RQ or scored metric.

Frozen full source9b3cf6a2f0014c70010b801cb4a9d082e078a267 reuses one actual
ordinary vllm_graph_uring_loop.so (size197248,inode265295) in every condition.
Model arithmetic, packed/prefix policies, timer60000ns, FP16 checkpoints,
vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17, wire and native code remain
unchanged. No BF_TRACE or steady userspace request worker is added.
The ordinary condition is an instrumentation ablation, not a serving baseline.

Standard PyTorch/CUPTI HES/device-graph activities surround only native serve,
after model loading/graph capture. All actual enable statuses are0.
Source-native request/connect uses the same four literal prompts per model,
one persistent loopback HTTP connection, gen1/c1. Startup, connect and CPU
text tokenization are outside these reported request intervals.
Pre-observation whole-output references remain byte-identical and every reply
matches one complete frozen sequence. Current batch/KV trajectory replay and
task-quality/general-model qualification are not established.

All20 actual drivers and model children exit0; one host launch/executor,
all400 admitted/retired, maxactive1, graph errors0, accepted=closed1/case,
independently drained SQ/CQ, pending/error/reserved/drop/overflow0.
Every request activity group has the recursive actual graph kernel count,
unique instantiated graph/node IDs and expected memcpy coverage:
Qwen271 kernels/request; Smol307 for query2 and337 for query5/8.
All10 profile traces cover60050 model kernels and200 model graph memcpy
records; long-lived dispatch/io_network activities are retained but excluded
from model spans. No missing activity is synthesized.

## Complete observed durations

Five process means per condition; milliseconds. GPU columns belong only to
the profiled condition. Model span is first-to-last model kernel duration;
union counts occupied model-kernel intervals, excluding intervening gaps.

| Model | Ordinary client TTFT | Profiled client TTFT | Profiled model span | Kernel union | Span minus union |
|---|---:|---:|---:|---:|---:|
| Qwen2.5-0.5B | 1.469674 | 1.462109 | 1.274584 | 1.134866 | 0.139717 |
| SmolLM2-135M | 1.188709 | 1.244535 | 1.043885 | 0.874085 | 0.169800 |

Profiled model spans are about87%/84% of the corresponding client durations.
These are internal descriptions, not ordinary-serving fractions or utilization.
Occupied kernel intervals are smaller; spans contain inter-kernel gaps and
sampling/head work. Neither duration identifies memory bandwidth, FLOPs, graph
launch overhead, network time or the cause of gaps independently.

Instrumentation effect is ordinary-minus-profiled TTFT, nominal paired t95
df4 over five process blocks, not a speedup or an equivalence test.

| Model | Mean effect ms | Nominal t95 |
|---|---:|---|
| Qwen | +0.007565 | [-0.018504,0.033634] |
| Smol | -0.055826 | [-0.130579,0.018926] |

Both intervals cross zero, which does not establish zero overhead. Smol's
pair4 effect is-0.153720ms and remains included. Profiled-to-ordinary transfer
is uncertain; reporting exact ordinary sub-stage fractions would be unjustified.

[Per-query descriptive grouping](../../bench/results/optimized_latency_profile_20261014/prompt_summary.json)
retains the real prompt mix rather than treating all requests as replicates.
Even query2 has Qwen1.306583ms and Smol1.158677ms model spans. Smol query2
has fewer kernels yet a longer span than query5/8 (1.010916/0.995030ms).
A shorter input or fewer kernels alone is not a speed guarantee. These fixed
prompts do not independently isolate a causal input-length effect.

CPU anchors provide clock compatibility intervals only, not an independently
proved GPU/CPU bias. Model durations are offset-independent; TTFT minus span
is an unresolved composite, not pure ingress/TCP/tail latency. Cross-node
finding0046's3ms-scale observations are a different topology and run, not
a measured current network stage obtained by subtraction.

## Failures and environment

The initial Qwen real preflight completes16 checked requests across both
conditions with2168 profile kernels/8 graph memcpy records. Its separate
[report](../../bench/results/optimized_latency_profile_20261014/preflight-report.md)
retains a driver warning and read-only diagnosis.

Before the second full process launches, an observation wrapper construction
raises NameError. It is repaired before any affected model/cell starts; the
first normal ordinary case is retained and no timing cell restarts.
Initial archive replay also selects its own derived timeline as raw input.
Preserve that failed replay; input discovery now skips only derived timelines
and prefers each case's adjacent archived trace. Metric/oracle/grouping logic
is unchanged. Final archive replay matches original full analysis byte-for-byte.
[Execution notes](../../bench/results/optimized_latency_profile_20261014/execution-notes.md)
retain these source-native adapter/reproduction corrections.

Actual host kernel/GPU/memory observations bracket all20 executors (40 records).
They retain11 same NVRM0x56 refcnt warnings, one preflight and every full
profiled bootstrap. NVIDIA's official status table maps0x56 to unsupported;
the failed reference's purpose/cause and timing influence remain unproved.
No new selected Xid/OOM/storage/BUG or GPU recovery action is observed.
Available host memory remains at least112034280kB and boot unchanged.
This is not a clean journal, continuous isolation or proof warnings are harmless.
The older05:28 OOM/storage fault remains recorded but is outside this matrix.

## Review, reproduction and project decision

The [independent result review](../../bench/results/optimized_latency_profile_20261014/result-review.md)
judges the finite shared-host run valid, the observed profiled-region ranking
supported, ordinary-serving transfer inconclusive, and value supporting.
It independently audits raw replies, traces, per-request graph/node/name and
memcpy patterns, host brackets, frozen references and replay. No direct thesis
challenge or ordinary-serving causal stage allocation is established.

[Final restoration](../../bench/results/optimized_latency_profile_20261014/final_restoration.json)
removes only the owned TEMP and9 named builds. Original Workspace/PVC/boot,
base packages,Coder processes,default HF library and unrelated WIP remain.
No own module/pins/GPU app remains at the observed endpoint. Full archive
replay after TEMP removal exits0 and matches original analysis byte-for-byte.

The [archive](../../bench/results/optimized_latency_profile_20261014/) contains
commands, pinned dependencies, unmodified backend source, necessary adapter,
all raw requests, actual exits, standard traces, catalogues and host brackets.
Replay after historical TEMP removal from repository root:

    python3 bench/results/optimized_latency_profile_20261014/analysis.py bench/results/optimized_latency_profile_20261014 full

The next backend work should reuse existing optimized/fused execution interfaces
where useful, preserving the same backend in transport comparisons. This
diagnosis does not authorize a model-specific arithmetic optimization campaign
or establish that a megakernel integration would improve delivery.
No unchanged CQ/timer/copy sweep follows. General text/protocol/backend support,
long-output/SLO/full CPU attribution and reliable performance advantage remain
open under the retained objective.
