# Active admission wait: remove redundant immediate kernel-loop iterations
2026-10-16 UTC. Same retained serving RQ: removing a steady userspace network
worker around unchanged resident GPU computation, seeking useful latency/TPS
and resource behavior against efficient native epoll. No thesis/RQ rewrite.

## Admission / decisive uncertainty
Finding0072 fixes EOF retention but native remains faster and group CPU lower.
The complete current creator kernel profile (result review in progress in
../kernel_cpu_profile_20261016/) has10086 samples/20.2124s periods:43.8132%
loop coordination and27.0375% BPF maps without observed socket ancestors.
It selects synchronization over speculative model or TCP changes; sampled
fractions alone do not establish avoidability or per-request latency.
Prior adaptive-idle wait0060 changed idle heartbeat; queue-publication0056 and
close-scan0066 test different mechanisms. None measures this active admission
acknowledgment branch on the repaired mixed16 remote workload. Existing data
cannot supply its missing intervention.

Largest credible positive story: kernel-owned serving can remove avoidable
coordination CPU with useful matched delivery, making worker removal meaningful
as a resource design. Negative/mixed result bounds that constructor and retains
native adverse evidence; it does not demand new model math or thesis revision.
Supporting mechanism role. This direct one-condition discriminator outranks
empty-queue-only helper skips, more timer values/external baseline rows or
unchanged load repeats. It is not a standalone proof of generic eBPF novelty.

## Exact candidate and ownership argument
Only bpf/uring_loop.bpf.c changes:
if(admitted!=admission_seen)wait=observed;
becomes
if(may_idle && admitted!=admission_seen)wait=observed;

Default60000ns active multishot timeout, idle deadline updates, GPU code,
model arithmetic/graphs, TCP, admission order/counters, EOF repair, ABI,
shutdown and all host settings stay unchanged. No flag/target/controller.
GPU progresses independently; active timer provides another CQE if no SQE
completion arrives. Immediate admission polling is retained when may_idle=1
because the timer can be at the distant deadline. That protects new work
before GPU has seen admission and published its active timer update.
may_idle is sampled before SQ tail as before, preserving visibility ordering.
Initial timer is active; successful GPU timer-update CQ handling publishes
its new mode. Stop/deadline/model-quiesced code is unchanged. A positive CPU
effect still does not prove all old sampled time was this branch.
Kernel loop semantics:
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c

Keep before/candidate source snapshots. Existing normal-source8/16 before
builds are immutable controls. Candidate is built by normal Make from the
canonical main WIP one-line edit into its own OS-TEMP BUILD dirs; no private
nvcc source-rewrite adapter. Confirm GPU instruction streams equal before and
fusion/header unchanged; only the intended loop BPF instructions differ.
Do not claim source adoption before qualification, full result and review.

## Integrated comparison and primary effect
Main competitor: efficient C++ epoll native, same mixed QwenFP16 executor,
weights/revision,16 slots,NODELAY,gen64,four frozen prompts and private network.
Current kernel is component before control, not another strongest baseline.
Candidate differs only by active admission waiting. Official vLLM0069 is cited
for whole-service level; no repeat solely to increase baseline count.

Five paired blocks,192rps60s,11520 attempts/cell, same block gamma schedules
seed20261015+block; three-condition order:
before/candidate/native; native/candidate/before; candidate/before/native;
native/before/candidate; before/native/candidate.
All15 cells/172800 attempts plus120 excluded checked gen1 warmups. Full terminal
drain, original60s per-I/O timeout, every failure and client scheduling lag stay.
Single operating point directly addresses the observed adverse cost/delivery;
no additional low-load/model sweep solely for breadth.

Primary candidate-minus-before owned-group CPU milliseconds/all attempts,
nominal paired t95df4. CPU includes same-TGID io-wq once. Negative upper bound
supports lower measured owned CPU; interval crossing zero is inconclusive,
positive lower bound adverse. Candidate/native is the strongest competing
resource outcome. Complete shared host/softirq/cgroup/device views remain
nested observations, not exclusive attribution. Standard process CPU accounting:
https://docs.kernel.org/admin-guide/cgroup-v2.html#cpu

Predeclared secondary delivered tokens/s, connect TTFT/completion P50/P95/P99,
client receive-gapP99, TPOT, scheduling lag, failure fraction and all-attempt
resource/energy contrasts, candidate-before/native. Use unchanged source-native
metric definitions and frozen reference-set flags. Benchmark definitions:
https://github.com/vllm-project/vllm/blob/main/docs/benchmarking/cli.md
Report each signed effect/nominal interval including adverse outcomes. Success
tails censor failed completions, not failure rates/throughput/resource costs.
Do not convert timeouts to completed60s or conflate receive grouping with GPU ITL.

CPU improvement alone is not a speedup. A lower CPU result with higher P99 or
lower TPS is a tradeoff; a crossing-zero delivery interval is neither parity
nor noninferiority. Do not rescue an adverse speed row with CPU. Any source
retention decision must preserve all delivery evidence and explicit limited
claims, not silently change timer or correctness to make it pass.
No simultaneous/multiplicity-adjusted inference or production SLO guarantee.

## Executable setup / qualification / real preflight
Original yunwei356/bpfusion-dev Workspace and lab5090; existing bounded
bpfusion-sustained-client-20261016 on g10. Source main only, retain original
Coder PIDs1/10909 and unrelated tools/setup_env.sh; no foreign work stopped.

Normal candidate command in /workspaces/repository with documented private
runtime environment:
make BUILD=/tmp/bpfusion-mixed-integration-n4cog5c6/active_wait_sourcebuild8
VLLM_PYTHON=/tmp/bpfusion-mixed-integration-n4cog5c6/runtime/bin/python
vllm-mixed-uring-loop vllm-mixed-user-network-wait vllm-mixed-trace
<BUILD>/bpfusion_load <BUILD>/fusion.bpf.o
Repeat in separate active_wait_sourcebuild16 with CPPFLAGS=-DBF_LLM_SLOTS=16.
Before/native use unchanged reclamation_sourcebuild16. These are existing
normal Make targets; no application source or model engine runs locally.

Because only BPF waiting changes, reuse unchanged native qualification0072.
Run candidate default8 Qwen/Smol traced protocol and source-native dual replay
with existing verified_reclaim_acceptance/protocol adapters selecting only
candidate build/output prefix; candidate ordinary loop lifecycle on both
models covers repeated2.2s idle-to-active transitions, reuse, queuedRST and
mid-output stop. Fixed pool/dual replay/timeouts unchanged, no observed pool
expansion. Common BPF loop also requires existing cuBLAS/cuFFT transport
cases before adoption, not arbitrary-backend stability. Builds/protocol are
dependencies folded into this experiment, not independent research results.

Real remote preflight uses before/candidate/native normal16, each128 attempts
from identical block0 gamma prefix,8 excluded checked warmups, actual clients,
resource metrics and full terminal drain. At most3 preflights; source/runtime/
metric defects must be recorded, affected checks repeated. No profiler in
preflight/full performance cells. Execute actual run_active_wait_matrix.ps1
from spark-manage via existing kubectl-home:
powershell -File <OS-TEMP>/run_active_wait_matrix.ps1 -ClientPod <owned-client>
-ServerIP <current-Workspace-PodIP> -Preflight
then the same command without -Preflight. All adapted source/expanded commands,
actual conditions, normal build/source receipts and exact original offsets
are archived here before real preflight.

After ordinary matrix, one separately labeled candidate creator-TID perf cell
at same192rps60s may reuse cpu_profile_record.py and existing sampled original
profile to check whether coordination samples cease to dominate. This is
mechanism context under observer exposure, not a matched performance gain,
additional primary or favorable replacement cell. Raw samples/loss/unknowns
and all negative results remain.

## Completion / archive / cleanup
Run all admitted cells to terminal; fresh result review audits raw data and
every paper-facing number and separate baseline fairness. Archive clients,
resources, commands/sources/normal builds, qualification/replay, losses,
deviations and independent analysis. Reuse ordinary scripts; add no experiment
control schema, gate, persistent helper, daemon or orchestration wrapper.
Byte-identical archive CPU replay required before publication. Commit/push
completed steps directly main. Temporary client Job deletion on closure;
owned profiles/servers/pins cleaned, original Workspace/PVC/session untouched.
If candidate is rejected, restore selected source with forward-only handling;
do not reset/revert published commits or promote a prepared-only candidate.

## Prepared runner details
run_active_wait_matrix.ps1 is prepared from the existing lossless chunk-transfer
runner; before/candidate/native selectors and128-prefix preflight differ.
It retains a5s loaded-idle observer bracket per process, separate from active
CPU primary. Both warmup/measured client transfers now occur after server stop.
Source lifecycle captures the correct archived before/candidate loop source,
while model/network/header sources stay identical. active_wait_analysis.py
changes only count/condition names/primary marker from reclaim_analysis.py.
No engine, oracle, tail definition or timeout changes. The perf diagnostic's
temporary client and its existing128-prefix offsets file are reused.

Process CPU primary uses clock_getcpuclockid/clock_gettime, not cgroup CPU:
https://man7.org/linux/man-pages/man3/clock_getcpuclockid.3.html
The cgroup reference above defines only the nested secondary cgroup view.
All promised TTFT/completion/TPOT/scheduling-lag mean/P50/P95/P99 paired
contrasts are now emitted explicitly from the same per-cell scalar values;
one fixed CPU primary remains, all intervals nominal without multiplicity correction.
