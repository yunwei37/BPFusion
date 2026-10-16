# Current mixed controller stage-time discriminator

## Research Question
Retain the user objective: improve latency/TPS for ordinary Linux TCP/eBPF to
resident reused-model GPU and kernel TCP replies, without a steady userspace
request worker. No formal paper RQ/thesis contract exists. Specific uncertainty:
does the remaining same-executor native delivery advantage accompany longer
observed model-dispatcher residence, or intervals outside that controller?
Separately, where does the concurrently running GPU network CTA spend time? This is localization before choosing another source intervention.

## Paper-Value Admission
Role supporting, with a consequential implementation choice. Findings0072/0074
repair actual lifetime and CPU faults yet retain a roughly20tokens/s native
capacity advantage at192/s.0075 rejects peer caching. The reviewer argument is
that moving network progression onto the GPU can affect execution through concurrent
resource use as well as explicit dispatch work. Full raw server round counts cannot recover durations; native
can execute more rounds and still deliver faster.0050/0054/0057 precede packed mixed
execution and recent repairs;0057's CUPTI decomposition additionally misses
activities in two cells.0066 measures publication/network intervals, not this
current independent-network and model-controller budgets. No existing valid raw data answers it.

The largest credible story is a measured boundary of host-control removal,
with a justified next intervention, not a new compute engine. A material dispatch difference selects a controller-specific avoidability test;
a large independent network-stage budget identifies a distinct investigation
candidate. An absent/inconclusive dispatch difference closes this primary
without ruling out network-CTA interference; graph/admission availability and
actual model service remain possible. Mixed/perturbation-dominated evidence closes this
constructor diagnosis without speed claims. Best alternative is a matched
CUPTI model-kernel timeline. Source-level brackets directly observe current dispatch and network stages without the prior missing-child-activity problem, and answer a
narrower actionable question before paying for broad profiling. They cannot
attribute model kernels, PCIe stalls, occupancy or exact historical6.36ms.

## Expected And Alternative Outcomes
Expected: concurrent network progression may accompany longer observed GPU
dispatch residence despite shared arithmetic. Alternative: actual trajectory/
round count or graph scheduling/model execution outside observed dispatch
accounts for the capacity association. Neither constructor association is an
exclusive causal intervention.
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
libraries use identical dispatch timing source. Actual loop I/O remains the
independent io_network CTA on its existing nonblocking CUDA stream; no
BF_IO_COALESCED/BF_CHAINED_DISPATCH flag is added. Extend private device-local
Control and IoState counters, not the shared page ABI. Existing logical traces/replay are retained unchanged.
Within each dispatch loop iteration record GPU globaltimer brackets around:
(1) completed output publication/release, (2) admission/packing, (3) actual
device graph-launch API calls. Accumulate launching, nonlaunching and final
stop iterations separately. Record prior launch-call end/bookkeeping anchor
to next dispatch entry in the same clock domain: this outside-dispatch interval
includes child model/head execution, graph scheduling, CTA return and unbracketed
bookkeeping; it is not pure model-kernel duration.

Independently bracket the actual io_progress sections: CQ drain, slot/peer claim,
response preparation/submission, connection receive/reclamation/accept, timer/
publication/final checks, and existing final nanosleep. Keep its original
single-thread execution, sleep duration, all early/shutdown branches and
memory protocol. Accumulate device-local IoState counters by had-owned-request
(seen != next_final at entry or after claim/send), no-owned-request, and stopping.
The classification uses existing local state and is not a claim that all other
iterations are idle or outside the client window. Preserve all iterations;
whole-process counts include startup/warmups/loaded-idle/shutdown. At finish,
after original network-stream synchronization, download private counters.

Network durations run concurrently with dispatch/model and MUST NOT be added
to dispatch durations or allocated as request latency. A network stage residence
is not exclusive GPU busy time: polling/sleep/memory stalls are included.
Record actual model launches, input-token histogram, completed replies, counter
identities and trace overflows. No negative residual is clipped, no marginal
P99 sum is a decomposition. Timer reads/counter writes/BF_TRACE change codegen
and resource use; equal instrumentation does not prove neutral/equal overhead.

Primary diagnostic contrast: loop-minus-native mean observed active controller
duration per model-launching iteration (publication+pack+launch brackets),
nominal paired95%t(df4) across five process blocks. Report separate dispatch/network stage sums/counts,
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
Positive dispatch effect supports a stage-specific avoidability investigation;
negative/inconclusive evidence closes this primary without excluding concurrent
network interference or actual model effects. Network-stage associations alone
do not demonstrate avoidability or authorize automatic sleep deletion.
Observed network sleep cost is overlap/residence evidence, not inline dispatch
stall. It may motivate a separately justified progression-policy discriminator,
but no sleep change is authorized by a timing association alone or performed
within this diagnostic. Source selection needs a separate uninstrumented matched
performance comparison. Neither source timer value nor stage percent proves
exclusive resource or old6.36ms attribution. No formal paper files are edited.


## Revision1 before any build or measurement
Initial review found that the ordinary mixed build does not enable
BF_IO_COALESCED: io_progress in dispatch is compiled out and uring_start starts
an independent io_network CTA. The initial inline interpretation/prepared source
were not built or run. Their exact plan/source remain in unexecuted_revision0.
This revision observes the actual independent constructor, keeps the main
question and four-condition schedule, and freezes dispatch-only residence as
primary with concurrent network budget kept separate. No new coalesced flag,
policy change, favorable-result reinterpretation or measurement exclusion.
