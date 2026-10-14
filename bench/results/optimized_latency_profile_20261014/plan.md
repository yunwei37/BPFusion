# Current optimized backend short-input latency localization

## Question and admission
Retain finding0030's short-input question: why does the current two-model
backend still have millisecond first-token latency for only2/5/8 input tokens?
The selected scope is now the qualified optimized vLLM backend and module-free
kernel loop, not old HF computation. No formal paper RQ or new thesis.
Planned role supporting mechanism localization; profiling setup itself is a
dependency, not an independent performance contribution.

Old0030 localizes the older HF backend; current ordinary0044/0045/0046 have
no per-model-kernel timestamp records. Their traces record logical batches and
outputs, not GPU execution durations. Reanalysis cannot produce the missing
current-backend timeline. Unchanged delivery repeats, more tiny CQ/timer
variations and single-model operator tuning have lower decision value.
Largest credible story is locating the remaining current-backend TTFT budget
so the next reusable backend/transport intervention targets an actual bottleneck,
without attributing upstream computation gains to eBPF.

Hypothesis: current optimized graph model execution still occupies the major
part of the short-input first-token interval; remaining publication/delivery/
dispatch latency is smaller. Competing explanation: graph coordination,
transport wakeup or profiling perturbation explains much of that interval.
If model execution dominates, prioritize reusable graph/megakernel integration;
if it does not, investigate the observed remaining path before arithmetic work.
If instrumentation changes latency substantially or coverage cannot qualify,
report that limitation and do not transfer a profiled fraction to ordinary
serving. No exclusive memory/FLOP/host-launch/transport causal diagnosis or
precise microsecond claim follows from a span or inter-kernel gap.

Best alternative is a generic text/protocol adapter or new completion-notification
mechanism. Both address eventual acceptance, but neither is yet grounded in
where the current latency budget lies. One current timeline with an explicit
profiling control is the stronger immediate discriminator. Close this diagnosis
after its full result; do not turn profiling into a tuning sweep.

## Actual system and official technique
Original yunwei356/bpfusion-dev /workspaces/repository/main, source56befc1,
RTX5090/Linux7.3rc3, same pinned checkpoint paths and FP16 upstream
vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17 and temporary common libbpf1.6.3.
Use existing ordinary vllm_graph_uring_loop library; no production source,
model arithmetic, queue/wire/timer or host-driver change.

Reuse0030's PyTorch/CUPTI Hardware Event System/device-graph tracing.
Configure device graph collection before CUDA init, hardware timestamps after
cuInit but before context creation. Assert actual setup statuses and no prior
CUDA context. Profile only the native serve interval after bootstrap graph
capture. Export standard Chrome traces through torch.profiler.
Official definitions/requirements:
https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html
https://docs.pytorch.org/docs/stable/profiler.html
TTFT follows existing source-native client and official serving metric:
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py

Necessary temporary bootstrap adapter fixes its repository/library path and
wraps serve in profiler for the profiled condition. Both conditions use the
same actual ordinary native .so, prompts, upstream graphs and workload.
Source-native graph catalogue recursively counts model body/head kernel nodes
for actual query lengths and batch1 before serving. It does not alter graphs
or model computation. No BF_TRACE or new steady host request worker is added.

## Comparisons and fidelity
Profiled kernel-loop serving is the diagnostic condition. The sole ordinary
same-library condition is an instrumentation ablation, not a main serving
baseline or an external competitor. Efficient native comparisons are already
qualified; adding another network baseline cannot identify this current model
span and is dropped here. No superiority/SOTA claim is made.
Both conditions preserve the same checkpoint/revision/precision/metadata/KV/
model head/greedy computation and60000ns timer.

Use0045's byte-identical pre-observation whole-output sets, the same four
literal prompts (Qwen lengths5/8/5/2,Smol5/8/5/2),gen1,c1,one persistent
loopback HTTP connection. Each valid reply must match one exact complete
frozen sequence for its prompt/gen; no set expansion or tokenwise union.
Current ordinary batch/KV histories remain unobserved; no task-quality claim.

## Preflight and full workload
Real Qwen preflight runs ordinary and profiled paths, four checked gen1 warmups
plus four measured requests in each. Confirm client bytes,actual child exits,
single host launch,eight admitted/retired,no graph error,maxactive1,
independent SQ/CQ drain and zero pending/error/reservation/transport overflow.
Preflight profile must cover every model kernel/memset implied by actual graph
catalogues and every request, excluding dispatch/io_network controller events.
Retain actual library/CUPTI and trace metadata. At most three preflight attempts;
capture failures; never weaken missing-record or output checks to pass.

Full scope: both models,five paired process blocks alternating ordinary/
profiled order,20 requests/executor (four excluded checked warmups then16
measured),20 executors,400 complete requests/400 tokens,320 measured.
Rotate the same four prompts; ordinary/profiled prompt order stays matched.
No gen64,c8 or remote stage attribution is inferred from this single-lane
short-input experiment. It supports the latency part of the full objective;
long-output/SLO/generic protocol work remains open.

## Metrics and validity
Primary diagnostic outputs are per-request client TTFT, model first-to-last
GPU-kernel elapsed span, kernel-duration sum, union of model-kernel intervals,
and kernel count, grouped by prompt length and process. Model-span/TTFT ratio
and span-minus-union are internal localization descriptions, not a new scored
paper metric, pure utilization or a performance improvement. Use standard
CUPTI kernel start/end/duration records; the model span is offset-independent.
Exclude long-lived dispatcher and network-controller kernels. Validate expected
kernel cardinality/unique graph nodes and complete graph/request grouping.
No model span is synthesized if activity coverage fails.

CPU monotonic anchors around the whole serve call may help causal compatibility,
but do not prove a GPU/CPU common clock or fixed offset bias. Preserve signed
residuals/uncertainty; unresolved ingress/tail sub-stages remain unmeasured.
The primary model-duration and client-duration comparison uses durations,
not cross-clock absolute-time subtraction. Catalogue/timeline grouping and
causal compatibility must be checked; latency fractions remain profiled.

Ordinary-minus-profiled paired mean TTFT is an instrumentation effect,not
a candidate speedup. Five process blocks give nominal t95 df4; pooled requests
do not manufacture replicates. Keep every interval/outlier. No arbitrary
equivalence margin or post-hoc exclusion. Report profiling perturbation
alongside localization; an inconclusive effect is not zero overhead.
A very large perturbation or known host fault prevents generalizing the
profiled bottleneck ranking to ordinary serving, but does not erase observations.

## Execution and cleanup
TEMP=/tmp/bpfusion-optimized-latency-profile-bk8ztoin.
Archive=bench/results/optimized_latency_profile_20261014.
Build ordinary source-native target:
make vllm-graph-uring-loop VLLM_PYTHON=TEMP/runtime/bin/python
Temporary adapter symlinks the same actual ordinary library into per-executor
folders and preserves all model/serve arguments. Existing source-native
request/connect are reused with literal prompts and fixed references.
Driver and replay analyzer are archived before serving; they use ordinary
Markdown/raw/standard trace artifacts, not a new control schema or scheduler.
Concrete dependency/build/adapter/client invocations are recorded before run.

Publish one frozen source checkpoint after real preflight and before full run.
Complete both models/all blocks,retain all outputs/trace/coverage/exits,then
fresh independent result review and honest finding/evaluation/main commit/push.
Cleanup only owned TEMP and named builds; preserve original boot/PVC/Workspace/
Coder/default HF library/global caches/tools/setup_env.sh. No client Job or
persistent entity is needed for this loopback diagnosis.

Known prior host OOM at05:28:38 has ceased on current checks; available memory
about114GiB and original retained volume attached/healthy/rw. Before and after
each executor record GPU/memory and actual bounded kernel journal. A new
kernel/GPU/storage failure pauses serving mutations for owning-path diagnosis;
do not discard rows or stop unrelated workloads. Discrete health checks do not
prove continuous isolation. Estimated20–35min including dependency/bootstrap.
The retained full objective remains unfulfilled regardless of this diagnosis.
