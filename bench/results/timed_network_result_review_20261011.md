# Independent result review: CPU-efficient native network control

Fresh reviewer: /root/timed_network_result_review,2026-10-11.
Read-only review; no source or experiment mutation. Report returned to the
root and saved after the complete frozen-source run.

**Run status: valid for the declared component comparison.**
**Tested hypothesis: contradicted by the observed comparison against the timed userspace control.**
**Research value: supporting.**
**Paper impact: mechanism and workload boundary.**

Removing the steady userspace request worker did not reduce the measured
executor-process plus kernel-TX-task CPU in this matrix. Both models used
less of this bounded CPU measure with the native timed epoll worker.
The measurements do not establish a transport-only causal effect, total
service CPU, or failure of the broader BPFusion objective.

The next decision should be to publish this negative boundary, retire the
busy-loop comparison as evidence of an advantage over efficient CPU
orchestration, and select the next experiment by its ability to distinguish
kernel networking overhead from competing explanations. No model arithmetic
optimization campaign follows from this result.

## Completion, provenance and correctness

I inspected the approved plan, both raw files, full command log, combined
native analysis, environment receipt, benchmark, oracle, graph loader/dispatcher,
native network worker and TX module.

The full run used frozen revision9f091f95d6bc359871a10c74077f1d9af35d5caa.
Both raw metadata records identify that revision. The inspected implementation
paths have no current source diff.

The native commands finished normally:

- SmolLM2 command: exit0 at11:16:19.820639UTC.
- Qwen command: exit0 at11:36:20.399156UTC.
- Full wrapper: completed exit0 at11:36:20.399220UTC.

| Coverage | Per model | Combined |
|---|---:|---:|
| Measured cells | 60 | 120 |
| Measured requests | 3840 | 7680 |
| Exact output tokens | 124800 | 249600 |
| Normal executor receipts | 15 | 30 |
| Idle observations | 15 | 30 |

There are no failure records, missing cells, duplicated cell keys, excluded
requests or selectively retried pairs. Every cell has indices0-63 exactly
once and16 requests from each of the four prompt cases.

All7680 responses match the eager-HF oracle prefix recorded in their model's
metadata. The oracle generates expected tokens independently before execution;
request packets carry input IDs and the requested generation length, not
expected output IDs. Correctness is therefore not defined circularly by the
resident executor's output.

I recomputed every request's TTFT, completion time and TPOT from its raw
timestamps, every cell's output tokens/s from first request start through
final token arrival, all native aggregate statistics and all paired estimates.
They match the saved native analysis. This establishes exact greedy correctness
for the tested prompts and lengths, not a general model-quality evaluation.

## Mechanism and control engagement

All30 executor logs report dispatch=resident, launches=1,
device_graph_launches=8580,graph_error=0,banks=8,max_active=8.
The8580 steps include260 warmup model steps plus8320 measured model steps
per executor.

I independently dumped the three current libraries' dispatcher SASS.
Their768 instruction rows compare equal. The graph loader and model
computation are shared; neither userspace control introduces a Python token loop.

All20 userspace executors have the intended busy/timed wait marker,
published=264,completed=264,rejected=0. The kernel TX module is absent by
the native runner's assertions and TX CPU snapshots are zero throughout.
Timed epoll uses a nominal60000ns timeout; readiness can wake it earlier
and GPU completions are examined after the wait. It engages the efficient
alternative but does not establish optimal waiting or equivalence to
usleep_range(60,120).

All10 resident queue receipts show264 publications, no parser invalid requests,
sockhash failures or admission drops,llm_head=264,zero reservations and all
eight slots FREE. Read-only host journal reconstruction finds all10 resident
unloads in the full interval. Each records bytes=55176,completed=264,
abandoned=0,retries=0,accepted=19,closed=19. Byte total agrees with8580
four-byte output tokens plus264 HTTP response headers. These establish actual
TX completion and connection reclamation beyond GPU output alone.

Strict qualification has four exit0 runs:1340 valid requests,81728 exact
tokens,1036 rejections, with prompt edges, concurrent reuse,pipelining,
half-close,invalid-token recovery and cleanup. Qualification/preflight are
dependencies, not separate performance results.

## CPU measurement audit

All150 idle/cell CPU observations reconstruct: raw before/after counters
produce saved component deltas; both are nonnegative; their sum equals
known_worker_cpu_ns; read brackets are ordered. Every measured request starts
after the before-read bracket and finishes before the after-read bracket.

| Model | Before read | After read |
|---|---:|---:|
| SmolLM2 | 40.230-110.563us | 83.640-260.932us |
| Qwen | 40.698-93.938us | 88.570-227.835us |

These are sequential reads around a request window, not atomic nanosecond
aligned measurements. Connection establishment and thread construction precede
the measured window; teardown/reclamation accounting is not guaranteed
identical between conditions.

The measure includes all executor-process threads plus CPU charged to the
kernel TX task. It excludes RX/softirq/BPF/TCP outside that task, client CPU
and GPU execution. It must not be called total service CPU or total CPU
removed by eBPF.

## Primary CPU results

Gen64,eight closed-loop clients,64 requests/cell,five paired process blocks.

| Model | Resident process + TX us/request | Busy us/request | Timed us/request |
|---|---:|---:|---:|
| SmolLM2-135M | 2011.566 | 69234.891 | 1628.283 |
| Qwen2.5-0.5B | 2319.134 | 93524.886 | 1981.831 |

Resident totals are dominated by TX. Mean process/TX components are
44.603/1966.963us for Smol and60.104/2259.031us for Qwen.

Paired difference is control minus resident; negative favors the control.

| Model | Control | Mean us/request difference | Nominal paired t95 |
|---|---|---:|---:|
| SmolLM2 | Busy | +67223.325 | [66775.581,67671.069] |
| SmolLM2 | Timed | -383.283 | [-593.022,-173.544] |
| Qwen | Busy | +91205.752 | [89877.246,92534.257] |
| Qwen | Timed | -337.304 | [-659.632,-14.976] |

All five timed differences are negative per model:
Smol -424.350,-97.323,-529.735,-385.708,-479.299us;
Qwen -631.529,-606.104,-202.729,-102.616,-143.540us.

The CPU-saving prediction is contradicted against the efficient control
in this workload. The advantage against busy polling is real for this bounded
measure, but cannot sustain superiority over efficient orchestration.

## Planned latency and throughput

TTFT gen1/client1, control minus resident, milliseconds:

| Model | Control | Mean difference | Nominal paired t95 |
|---|---|---:|---:|
| SmolLM2 | Busy | -0.090135 | [-0.268859,0.088589] |
| SmolLM2 | Timed | +0.090901 | [-0.141011,0.322813] |
| Qwen | Busy | -0.017408 | [-0.037196,0.002381] |
| Qwen | Timed | -0.026525 | [-0.059269,0.006218] |

Mean TTFT resident/busy/timed:
Smol5.457946/5.367811/5.548847ms;
Qwen4.073155/4.055747/4.046629ms.

Throughput gen64/client8, resident minus control, output tokens/s:

| Model | Control | Mean difference | Nominal paired t95 |
|---|---|---:|---:|
| SmolLM2 | Busy | -6.368173 | [-15.373800,2.637453] |
| SmolLM2 | Timed | -2.488979 | [-9.443425,4.465468] |
| Qwen | Busy | +3.320190 | [-6.397947,13.038327] |
| Qwen | Timed | +2.632198 | [-3.308572,8.572968] |

Mean throughput resident/busy/timed:
Smol918.517/924.885/921.006;
Qwen688.077/684.757/685.445.

Every planned TTFT/throughput interval crosses zero: inconclusive for advantage,
not equivalence, noninferiority or a Pareto relationship.

## Fairness, uncertainty and event exposure

The controls engage intended mechanisms without observed interface failure
or extra model-compute budget. They are same-compute component controls,
not external SOTA serving baselines.

Mode/cell order matches the native plan:
R,U,W;R,W,U;W,R,U;W,U,R;U,W,R.
Cells rotate between process blocks. Five of six permutations, no randomization,
and no guarantee of independence from shared-host drift.

Full collection starts after a new SGLang scheduler observed10:51:29UTC.
It remains observed on the same GPU at10:56:58 and11:14:58UTC. Its residency
or activity throughout Qwen is unknown. The21:51UTC empty-GPU receipt is
delayed and cannot determine when it left.

The retained retrospective journal query has no matching fault lines in
the requested later full interval. This does not establish no interference
or constant co-tenant activity.

GPU clocks/power/global CPU vary. Qwen resident gen64/client8 global CPU work
decreases from34.59/36.69s in the first two blocks to17.67/17.02/17.38s later.
This shows an environment/workload trend, not its cause; TX also changes.
Retain paired measurements without attributing the entire difference to
transport alone.

Intervals use five process-block differences, nominal two-sided Student t95,
df4. Requests within a cell are not independent replicates. No family-wide
correction or basis to treat nominal intervals as a general causal property.

## Publication and next decision

Supported statement: on tested loopback,fixed-compute workloads,the timed
native userspace control uses less executor-process-plus-TX-task CPU than the
resident eBPF/kernel path atgen64/client8; planned TTFT/throughput remain
inconclusive.

No lower total service CPU,generally faster eBPF path,isolated GPU,
constant SGLang exposure,SGLang/NanoFlow superiority,general models,
physical NIC,text processing,continuous batching or direct thesis challenge.

This adds supporting evidence by answering the missing efficient-control
question and including TX-task CPU. Publish negative results and uncertainty
without changing the hypothesis/discarding pairs. A future kernel-efficiency
experiment is useful only with a new causal discriminator, such as accept/drain
versus completion polling, and when it outranks remaining physical-network or
strongest-external-comparison work. This review does not authorize or require
a rerun or redesign.
