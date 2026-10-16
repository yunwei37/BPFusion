# Current mixed controller stage-time discriminator

## Research Question
Retain the user objective: improve latency/TPS for ordinary Linux TCP/eBPF to
resident reused-model GPU and kernel TCP replies, without a steady userspace
request worker. No formal paper RQ/thesis contract exists. Specific uncertainty:
does the remaining same-executor native delivery advantage accompany material
GPU controller time spent advancing inline I/O, or intervals outside that
controller? This is localization before choosing another source intervention.

## Paper-Value Admission
Role supporting, with a consequential implementation choice. Findings0072/0074
repair actual lifetime and CPU faults yet retain a roughly20tokens/s native
capacity advantage at192/s.0075 rejects peer caching. The reviewer argument is
that moving network progression onto the GPU shifts cost onto the execution
critical path. Full raw server round counts cannot recover durations; native
can execute more rounds and still deliver faster.0054/0057 precede packed mixed
execution and recent repairs;0057's CUPTI decomposition additionally misses
activities in two cells.0066 measures publication/network intervals, not this
current inline controller-stage budget. No existing valid raw data answers it.

The largest credible story is a measured boundary of host-control removal,
with a justified next intervention, not a new compute engine. A material inline
I/O budget motivates its avoidability test; an absent/inconclusive difference
rejects further blind controller caches and shifts investigation to graph/
admission availability. Mixed/perturbation-dominated evidence closes this
constructor diagnosis without speed claims. Best alternative is a matched
CUPTI model-kernel timeline. Source-level brackets directly observe the current
inline stage without the prior missing-child-activity problem, and answer a
narrower actionable question before paying for broad profiling. They cannot
attribute model kernels, PCIe stalls, occupancy or exact historical6.36ms.

## Expected And Alternative Outcomes
Expected: inline I/O adds observable GPU controller work while model arithmetic
is reused. Alternative: actual trajectory/round count or graph scheduling
outside observed controller accounts for the remaining capacity association.
Short or mixed controller differences, or large profiling perturbation,
contradict using these stages to explain ordinary-serving speed. Source
brackets are observations of an instrumented constructor, not a causal removal.

## Published Precedent And Real Assets
Reuse source-native mixed Make targets, vLLM0.31/Torch2.13cu129/Transformers5.17,
Qwen pinned revision7ae557604adf67be50417f59c2c2f167def9a775, FP16, RTX5090.
PTX globaltimer provides a predefined nanosecond register, target-specific and
intended for tools:
https://docs.nvidia.com/cuda/parallel-thread-execution/#special-registers-globaltimer-globaltimer-lo-globaltimer-hi
CUDA documents nanosleep as approximate, not an exact1000ns charge:
https://docs.nvidia.com/cuda/archive/13.2.2/cuda-programming-guide/05-appendices/cpp-language-extensions.html
Use only differences within the GPU clock domain; no host/client subtraction.
Client throughput/TTFT/TPOT follow the established vLLM terminology:
https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics
Custom glue is private source timing brackets/counters and analysis, not an
experiment-control API or new runtime option. No CUPTI/profiler installation.

## Comparison
Selected0074 loop versus efficient native C++ epoll with the SAME mixed GPU
executor; native is the one main competing mechanism. Citation cannot answer
the current matched GPU time. Each has ordinary untraced and instrumented
conditions. Instrumented conditions enable existing BF_TRACE plus GPU-stage
brackets equally; ordinary conditions are the existing selected normal builds,
a combined-instrumentation ablation, not a second competitor. No host setting,
timer60us, socket NODELAY, model/capture policy, ABI or slot16 change.
Official vLLM0069 remains an external whole-service reference and cannot isolate
this internal controller question; no extra baseline is needed here.

## Instrumentation And Fixed Scopes
Private copy of vllm_mixed.cu only, compiled with the normal Make rule's -dc,
flags/includes/device-link and selected io_uring_tcp.h. Both instrumented
libraries use identical timing source; loop-only inline io_progress remains
its existing constructor difference. Extend private Control with counters,
not shared page ABI. Existing logical traces/replay are retained unchanged.
Within each dispatch loop iteration record GPU globaltimer brackets around:
(1) completed output publication/release, (2) inline io_progress (native no-op
bracket), (3) admission/packing, (4) actual device graph-launch API calls.
The existing final io_progress nanosleep remains; separately bracket it using
a private header copy, without removing/changing the sleep or return policy.

Accumulate duration/count for model-launching iterations and nonlaunching
iterations separately; all idle work is preserved, not silently charged per
token. Final stop iteration is separately counted. Record actual model launches,
input-token histogram, completed replies, counters and trace overflows.
Record prior launch-call end to next dispatch entry in the same GPU clock:
this includes child model/head execution AND graph scheduling, and is explicitly
not pure model-kernel duration. No negative residual is clipped and no marginal
P99 sum is called a decomposition. Counter writes, timer read and BF_TRACE cost
are instrumentation overhead; balanced instrumentation does not prove neutrality.

Primary diagnostic contrast: loop-minus-native mean observed active controller
duration per model-launching iteration (publication+I/O+pack+launch brackets),
nominal paired95%t(df4) across five process blocks. Report stage sums/counts,
per-round means and each cell, outside-controller interval and actual rounds/
input-token distributions. This tests a constructor association; changing batch/
KV history prevents equal-work per-kernel attribution. Separately report complete
client TPS/TTFT/completion/receive-gapP99, all-attempt failures, scheduling lag,
TPOT and instrumentation-minus-ordinary effects. No primary change after data.
A positive diagnostic interval supports a controller difference, NOT its
avoidability or ordinary TPS gain. A zero-crossing interval is inconclusive,
not equality/noninferiority. No timing-based source adoption follows.

## Workload, Correctness And Planned Runs
One real checkpoint Qwen, same four frozen prompts, output64, slots16 and the
existing remote192/s gamma schedule. Eight sequential checked gen1 warmups per
process excluded from client metrics; internal whole-process counters explicitly
include them and startup/idle scopes. No unverified subtraction. Per-I/O60s
timeout/full drain unchanged. Existing frozen reference membership remains a
reported flag for untraced cells, not exact fidelity or hidden exclusion.
Instrumented cells also require exact source-native two-pass graph/KV/history
replay, complete admission/compute/release coverage and all client-token joins,
no graph error/trace overflow, ordered nonnegative clock brackets and exact
counter/round identities. Replay checks current trajectory, not fresh eager-HF
arithmetic parity. No pool/oracle/timeout changes to force a pass.

Real preflight: four conditions, unchanged first128 offsets of block0,128
measured responses/8192 tokens each plus8 warmups. Full: five blocks, four
conditions each with11520 scheduled attempts for60s plus full drain;20 cells,
230400 attempts/14745600 output tokens if all succeed. Existing frozen block
seeds20261015+block, identical offsets within block. Conditions are L ordinary,
LI instrumented loop, N ordinary native, NI instrumented native. Frozen orders:
block0 L,LI,NI,N; block1 N,NI,LI,L; block2 LI,N,L,NI;
block3 NI,L,N,LI; block4 L,NI,LI,N. Residual ordering/shared-host variation
remain limits. At most three real preflight attempts per skill. Full collection
never replaces a slower/failed valid cell. Expected acquisition cost20 model
bootstraps+60s workloads and post-serving instrumented replay; not a deadline.

## Execution And Completion
Owning Workspace only, private build source/Makefile under OS TEMP; capture actual
expanded commands and compare BPF instructions/relocations to selected before.
Existing remote client runs through the same bounded disposable Job owner path;
reuse unchanged client/config/offsets. No server overlap, profiler or heavy Git/
archive during a measured cell. Client raw compression/transfer follows server
stop. Reuse original resource observer for full comparable group/host context,
without claiming exclusive costs; no extra host task profiler.

Commands: python3 TEMP/controller_stage_build.py; Windows
run_controller_stage_matrix.ps1 -ClientPod <owned> -ServerIP <Workspace-IP>
-Preflight, then the same command without -Preflight. Frozen prepared scripts
are archived here before execution. Raw prefixes controller_stage_preflight
and controller_stage_full; acquisition analyzers and archive CPU replay kept.
Full completion requires every20 server/client terminal, all correctness/clock/
counter audits, fixed analysis, fresh independent result review and actual
owned-client cleanup. Failed/invalid prefixes and plan deviations stay.
Original sessions/PVC/foreign WIP preserved; main direct commit/push after
completed milestones. This source-neutral measurement changes no default.

## Interpretation
Target table/figure: all paired controller-stage durations and outside-controller
intervals with observed rounds, alongside ordinary/instrumented client speed.
Positive controller effect selects a stage-specific avoidability experiment;
negative/inconclusive evidence closes this localization and avoids blind caches.
Observed sleep cost may motivate removing only a redundant active-path sleep,
but no sleep change is authorized by a timing association alone or performed
within this diagnostic. Source selection needs a separate uninstrumented matched
performance comparison. Neither source timer value nor stage percent proves
exclusive resource or old6.36ms attribution. No formal paper files are edited.
