# Long-output GPU service-time discriminator

## Research Question
Retain the user objective: improve latency/TPS for ordinary Linux TCP/eBPF to
resident reused-model GPU and kernel TCP replies, with no steady userspace
request worker. There is no formal paper RQ/thesis in this repository.
Uncertainty: does the remaining long-output native gap accompany longer actual
model execution per round, or more rounds/inter-round availability gaps?

## Paper-Value Admission
Planned role supporting, potentially decisive for the next implementation
choice. Strongest reject argument: CPU-worker removal shifts coordination onto
GPU resources and can lose to an efficient proxy despite identical arithmetic.
Findings0054/0056 both fail local optimization selection;0055 preserves native
loss and contradicts simple aggregate-round explanations.0047 covers c1/gen1
only.0043 incremental copying is inconclusive. None contains matched gen64/c8
model-kernel timings or actual current batch trajectories. Existing raw data
cannot synthesize these missing durations.

A longer model-service interval suggests reusable execution/resource scheduling
work; equal service time but gaps/round inflation suggests progression/admission
work. Mixed or perturbation-dominated data prohibit exclusive cause and close
this diagnosis without tuning. A generic text/backend adapter is the best
alternative for OSS acceptance, but does not discriminate this measured gap.
A SENDMSG recopy intervention is premature without a demonstrated copy cost.
This experiment beats another unchanged speed matrix or model arithmetic tuning.
No headline performance benefit is promised.

## Expected And Alternative Outcomes
Expected: standalone I/O may perturb GPU model service or scheduling relative
to native. Alternative: profiled model durations are similar and the difference
lies in availability/batch histories or instrumentation. Current evidence does
not warrant choosing among these before measurement.
All duration/batch differences are descriptive constructor bundles, not isolated
occupancy, PCIe, memory-bandwidth or FLOP mediation.

## Published Precedent And Real Assets
Use current main458145f, existing source-native vLLM trace targets and clients,
same pinned vLLM0.31.0/Torch2.13cu129/Transformers5.17 checkpoints and FP16.
Reuse0047 PyTorch/CUPTI hardware/device-graph tracing around native serve only,
after bootstrap capture. Official APIs:
https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html
https://docs.pytorch.org/docs/stable/profiler.html
Client TPS/TTFT/TPOT concepts follow official vLLM benchmarking:
https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics
Standard kernel start/end/duration activities give model union/span/gaps.
These internal diagnostic decompositions are not new scored metrics.
Temporary adapter extends read-only graph catalogue to query0/2/5/8,batch1..8.
Production source/ABI/timer/arithmetic/defaults remain unchanged.

## Comparison
Current independent GPU io_uring BPF loop versus efficient native timed
epoll_pwait2 TCP, both with identical reused model computation.
Native is the one main competing orchestration mechanism; published different
hardware results cannot settle this matched local duration comparison.
Each path has unprofiled and profiled conditions using the same actual traced
library: profiling ablation, not another main baseline.
BF_TRACE is enabled equally in all four conditions to authenticate actual
batch/query/history and replay reused graphs in a fresh unprofiled bootstrap process after the serving child exits. Thus the
unprofiled condition is still logically traced. Ordinary untraced0055/0056
remain prior evidence only; this does not prove BF_TRACE neutrality or an exact
ordinary serving decomposition. A profiling contrast crossing zero is not
zero overhead/equivalence. No native penalty or path-specific tuning.

## Workloads And Metrics
Two fixed FP16 models, existing four prompts, gen64/c8;8 sequential checked
gen1 warmups/executor. Preflight Qwen8 measured requests/512tokens in each
of4 conditions. Full32 measured requests/2048tokens/executor,5 paired blocks,
2models*2paths*2profiling states=40 executors1280 measured requests81920 tokens
plus320warmups. Preopened eight connections and source-native closed-loop lanes.
Alternate model/path/profile order and retain exact expanded commands.

Primary paper-facing output remains client TPS, interpreted together with
profiled model-kernel intervals. Diagnostic table: per-path whole-workload model
union/span, sum kernel duration, count of actual rounds/batch histogram, per-round
span/union stratified by query/batch, and inter-round gaps. Profile comparisons
use five paired process blocks, nominal t95df4; no pooled request replication,
arbitrary cutoff, hidden exclusion, equivalence, familywise or pure causal claim.
Kernel durations are offset-independent. CPU anchors are compatibility only;
do not subtract CPU/client absolute timestamps into GPU substage durations.
Model gaps can include requests/availability/model dispatcher/network scheduling;
they are not pure transport time.

Correctness: fixed pre-observation whole-output pools for actual ordinary
client replies; current BF_TRACE tokens/admissions/release and same-graph KV/
history replay in that separate bootstrap must exactly agree, trace overflows0, no graph/transport errors,
admitted=retired=warm+measured, physical slot ownership and queues drain.
The older stronger AMK eager-HF failure remains failed; this reused graph replay
is not a fresh arithmetic oracle or arbitrary-backend acceptance.
Every profiled compute event must have exactly its recursive graph kernel
count, unique graph/node identities within each round and ordered query/batch
correspondence. Memcpy/memset coverage is checked as whole-serve counts only,
not independent per-round memory-node identity. This scope clarification follows
the fresh plan review and changes no recipe, metric, oracle or expected answer. Missing activities invalidate decomposition;
never synthesize missing events or trim a slow block to pass.
Profiler setup actual statuses must0 before CUDA initialization/context.

## Planned Runs
| Group | Workload | Paths | Repetition | Decision |
|---|---|---|---:|---|
| Real preflight | Qwen gen64/c8,8 requests+8 warmups | loop/native x unprofiled/profiled |1| complete trace/fidelity executable |
| Full matched discriminator |2models gen64/c8,32 requests+8 warmups|same4conditions|5| choose model service vs availability follow-up or inconclusive |

## Execution
Original Workspace only, main; private OS TEMP builds/runtime/libbpf.
Source-native targets vllm_graph_uring_loop_trace and
vllm_graph_user_network_wait_trace. Reuse root BPF loader/object read-only;
preserve existing trace artifacts/tools/setup_env.sh/Coder/base packages.
Command: python3 TEMP/run.py preflight; python3 TEMP/analysis.py TEMP preflight;
then python3 TEMP/run.py full; python3 TEMP/analysis.py TEMP full.
Full completion requires40 executor/driver exits0, all client/trace/replay/
coverage checks and fixed analysis, then fresh independent result review.
No oracle/metric/timeout alterations to pass. Failures/deviations retained.
Sparse host before/during/after retain old warning/400W context; no continuous
isolation claim. Cost roughly40–70min common serving plus fresh-replay bootstrap/collection, not a deadline.
TEMP and archive names are recorded alongside this plan before execution.

## Interpretation And Reproducibility
Report signed path and profiling effects with every block and batch stratum.
Increased model durations support only a constructor-level service-time
association; similar durations with more rounds/gaps favor availability/history.
Mixed/inconclusive or large perturbation restricts transfer and gives no default
change. No absolute CPU/GPU bias, dynamic PCIe, SLO/capacity, total CPU/energy
or universal backend claim. Source-neutral diagnosis adds no production change.
Close this matrix after review; archive recipes/current sources/full raw traces/
replay/host/preservation; remove only ownedTEMP; commit/push main with honest
finding/evaluation and public receipts. Whole project goal remains active.

TEMP=/tmp/bpfusion-long-service-timeline-bk7zo7qp
Archive=bench/results/long_service_timeline_20261014


## Real preflight failure and repair, revision1
First Qwen loop/unprofiled passes. Native/profiled serves all16 replies/520tokens
and exports trace, then exits SIGSEGV/-11 during cudaMemcpyAsync in existing
post-profiler KV/history replay. Therefore preflight1 fails; it is not a pass
or native win. Host remains same boot, empty compute apps, no own pins/module;
one new NVRM0x56 warning at profiler bootstrap is preserved. The complete cause
of the segfault is not established and is not labeled a repaired driver fault.

Move the unchanged source-native graph/KV/history replay to a fresh unprofiled
bootstrap after the serving child exits, equally for all four conditions.
The serving observation adapter omits its in-process replay; current production
bootstrap plus original replay body is copied privately with only serve skipped.
No new CLI/interface, arithmetic, token expectation, trace coverage, metric or
timeout is added/relaxed. Driver and analyzer require both serving and fresh
replay exit0. Extra bootstrap cost is recorded; profiling still covers serving
only. This changes oracle execution placement and is an explicit operational
plan deviation, not a result-dependent weakening. New valid comparisons need
the revised path; retain first attempt raw artifacts and rerun all four preflight
conditions as preflight2 before full collection. Do not overwrite first attempt.

## Analyzer initialization classification clarification
Second preflight completes all4 serving and fresh replay children0. The first
CPU analysis finds exactly one extra loop kernel: source-native io_initialize.
uring_start synchronizes this one-thread state initializer before NET_READY;
it is neither model math nor a measured request. Original0047 predates that
current constructor. Record it with dispatch/io_network as non-model work,
requiring exactly1 loop/0native initializer with graph/node0, grid/block1 and
end before first model kernel. Preserve all raw activities and failed analyzer
receipt. This corrects the observation adapter classification, not a tolerance,
missing-record imputation, oracle or metric change. Reanalyze the unchanged
second-preflight raw results; no serving rerun follows this CPU-only repair.
