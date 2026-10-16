# GPU-local immutable peer identity: experiment plan

2026-10-16 UTC. Base main9341a194442cd3ac1994869219f44c1dac136783.
Scope contract: change only immutable TCP peer identity storage in the existing
GPU I/O controller; retain reused model arithmetic, BPF/admission/wait/lifetime
policy, native transport, shared ABI, default8, timers and host settings.

## Retained question and admission

The retained user objective is ordinary Linux TCP/HTTP + eBPF admission/shared
queue -> resident real-model GPU -> asynchronous kernel TCP reply, without a
steady userspace request worker, improving throughput/latency while reusing
existing model computation. No formal paper/RQ/idea-story exists here and none
is introduced or rewritten. This is one supporting mechanism intervention
within that serving-path throughput/latency question.

Read current README/evaluation/architecture, closest-work map and findings0054,
0066,0072,0073,0074 before admission. The complete0074 result removed substantial
BPF coordination CPU: group0.626 versus native0.769ms/attempt. It did not
increase throughput (candidate-before+0.463[-8.973,9.899]tokens/s);
native remains faster by20.259[10.244,30.273]tokens/s with completionP99
lower by98.249[48.700,147.797]ms. Repeating that unchanged comparison cannot
answer the remaining speed question. Its full raw data already answer CPU
efficiency and bound its saturation performance; no resampling to obtain a win.

Current source repeatedly scans active GPU IoConn entries to join BPF slots
by peer address/port. Each comparison obtains peer identity from the
host-mapped ACCEPT sockaddr buffer; EOF pending-hash lookup reads it again.
At current sustained192/s the process has hundreds of simultaneous peers.
Identity is immutable for each completed ACCEPT until that entry is reused.
This is a concrete source-level remaining transport cost, not proof of its
measured bottleneck or physical PCIe mediation.

Largest credible story: backend-independent GPU driver metadata handling can
recover measurable same-compute delivery capacity after host coordination is
efficient. Positive primary evidence could justify a tiny transport repair;
a native win would add bounded same-compute speed evidence. A negative or
inconclusive result rejects source retention for performance, preserves the
CPU-only boundary and rules out this simple placement constructor under the
tested load. An adverse result rejects it as a tradeoff unless a correctness
need emerges independently. None establishes arbitrary-model speed or general
eBPF superiority. This is supporting, not a new headline contribution.

Why this next experiment: it directly intervenes on a known repeated mapped
read in the slower path with no model changes. Earlier0054 moved regular
IoStats accounting,0054's primary was inconclusive and its source was rejected;
0066 cached a close-scan condition and was also rejected. Neither copied
immutable per-ACCEPT peer identity or used the current sustained mixed/
reclamation/active-wait constructor. Reanalysis cannot measure an unexecuted
counterfactual. A timer sweep, more models without a causal intervention,
or another official-vLLM run would not identify this remaining mechanism.
A fresh low-load resource matrix would extend the CPU operating envelope,
but is less direct for the user's outstanding speed/root-cause question.

## Primary sources and method

Reuse the existing real server, source-native frozen TCP benchmark,
gamma arrival schedules and official model graphs; no toy kernel/server.
CUDA zero-copy guidance on discrete GPU mapped memory motivates minimizing
repeated reads and suggests device-local caching when rereading. This is
guidance, not a measurement of this controller:
https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#zero-copy
https://docs.nvidia.com/cuda/archive/13.0.1/cuda-c-programming-guide/index.html#mapped-memory
The latter also requires host/device access synchronization.
Delivered output TPS and client TTFT/TPOT definitions follow the existing
vLLM benchmark metric convention, with our finite token-ID wire/window:
https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics
CPU/resource and quantile definitions remain exactly the existing0074 analysis.
No source is evidence of an established local bottleneck.

## Intervention and baselines

Proposed candidate.diff and both headers are archived before implementation.
Append addr_be (u32) and port_be (u16, plus natural padding) to existing
device-local IoConn. After a successful ACCEPT CQ is consumed, copy that
sockaddr identity once before linking the connection into active. Existing
request peer scan and EOF pending-bucket lookup use these cached immutable
fields. Keep the same linear list, source TCP sockaddr buffer, fd/generation/
close/cancel ownership and pending reference ordering. Aggregate initialization
zeros appended fields on reuse. No hash table, worker, helper, new allocation,
flag, ABI or persistent entity; the existing device IoConn allocation grows
by its natural per-entry8bytes. Failed ACCEPT never enters active.
CQs are acquired through the existing mapped-ring protocol; identity reads
retain the same system-memory visibility context as the old lookup.
Finite qualification must cover reuse/fragmentation/half-close/reset/stop.

Before is exactly adopted0074 ordinary active_wait_sourcebuild8/16, with
their selected active-wait BPF objects; it is a component ablation, not a
second main baseline. Candidate normal peer_identity_sourcebuild8/16 changes
only this header. Efficient native epoll from active_wait_sourcebuild16
is the single main competitor: identical reused model computation/precision/
weights/prompts/capacity/socket option. It represents a credible efficient
CPU orchestration answer; a native win prevents a faster-server claim.
Its earlier numbers cannot substitute for contemporaneous paired comparison
under this intervention. Official vLLM finding0069 is a separate whole-service
reference with protocol/KV/scheduler differences; citation suffices here.
No extra weak or unavailable external baselines are admitted.

GPU controller/parent code generation and IoConn layout can change; these
are part of the constructor. Do not claim whole-library SASS equality for
candidate kernel or exclusive PCIe mediation. Model implementation/graph
capture source and native GPU SASS must remain unchanged. Both BPF programs,
shared ABI and all native source/normal object bindings must match controls.
Receipts capture the correct immutable before versus candidate header;
current artifact HEAD alone does not prove a measured binary/source.

## Qualification and actual commands

All source/build/tests remain in existing yunwei356/bpfusion-dev
/workspaces/repository. Keep original PIDs1/10909 and foreign tools/setup_env.sh,
source main only; no replacement Workspace, branch or checkout. Before private
builds remain immutable. Apply archived candidate to canonical header as
uncommitted experiment WIP only; source retention waits for result decision.

Normal Make commands with existing pinned private runtime:
make BUILD=/tmp/bpfusion-mixed-integration-n4cog5c6/peer_identity_sourcebuild8
VLLM_PYTHON=/tmp/bpfusion-mixed-integration-n4cog5c6/runtime/bin/python
vllm-mixed-uring-loop vllm-mixed-user-network-wait vllm-mixed-trace
<BUILD>/bpfusion_load <BUILD>/fusion.bpf.o
Repeat separate peer_identity_sourcebuild16 with CPPFLAGS=-DBF_LLM_SLOTS=16.
Use documented environment.json and no private source/NVCC rewriting.
Archive argv/stdout/stderr under build_records, never ignored build/.

Reuse unchanged native finite qualification0074. Candidate default8 runs
the existing Qwen/Smol protocol + source-native and independent graph dual
replay with fixed oracles, including actual batches1..8, framing/reject/reuse/
half-close/reset. Run existing ordinary two-model loop lifecycle including
2.2s idle transitions, queued/reset and mid-output stop; preserve partial/
unobserved cancellations as such. Existing cuBLAS8x8/cuFFT32 graph cases on
loop/native qualify the shared header's finite generic usage. Reuse analytic
oracles; no new broad backend claim. These are folded dependencies, not
independent paper results. Compile shared HF/AMK consumers only if normal
dependencies are available; record unqualified runtime honestly.

Recreate only the same bounded disposable remote client Job through its
existing recorded manifest/path, same image/no caps/no node pin, retaining
the established anti-affinity that avoids the real GPU server. This benchmark
authorizes test-local recreation and deletion, not retained infrastructure.
Discover current Job/Pod UID/IP/node; verify source schedules/config frozen.
No public endpoint or retained service. Record baseline/mutation/cleanup.

Fresh review, then at most3 real preflight attempts:
run_peer_identity_matrix.ps1 -ClientPod <owned-client> -ServerIP <Workspace-IP>
-Preflight. Each before/candidate/native128 actual attempts, same block0 gamma
prefix192/s,8 excluded checked gen1 warmups per server, full terminal drain,
actual observers/tails/oracle/errors. Only source/runtime/metric defects
justify affected retries; preserve all failed/invalid attempts and reasons.
No primary inference from preflight.

## Complete matrix and fixed interpretation

After successful preflight, run same command without -Preflight.
Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775,
FP16, same RTX5090 and pinned0074 runtime, mixed16 slots, four frozen prompts,
gen64. Five paired blocks; each condition11520 arrivals at192/s for60s,
original gamma offsets blockseed20261015+block, full drain. Eight checked
gen1 warmups per process excluded. Each condition57600 attempts if complete.
Rotating orders as0074:
0 before/candidate/native;1 native/candidate/before;
2 candidate/before/native;3 native/before/candidate;
4 before/native/candidate.
No profiler in full or preflight, no source/oracle/metric/timeout changes.
Existing60s per-I/O timeout stays. All failures/partial tokens/invalid outcomes
and client scheduling lag remain; do not turn timeout into a completed60s
latency or omit unsuccessful attempts. Frozen sequence-pool mismatches remain
flags and no pool is expanded from observed outputs.

Fixed primary: candidate-minus-before delivered output tokens/s, higher
better, computed from all successful measured output tokens over the actual
first-launch to full-drain client window. Report partial observed token/s
separately. Quantiles of successful requests stay failure-censored when any
failure exists. Compute the five paired block effects and nominal95%t(df4)
interval, coefficient2.776445105. Positive lower bound supports this
constructor's delivery benefit; negative upper bound contradicts; interval
crossing0 is inconclusive, never equivalence/noninferiority or an invitation
to increase N until it passes. Only one primary, no multiplicity correction.

Report candidate-native delivery as the main competitor contrast alongside
the ablation primary. Retain all46 paired contrasts: TTFT/completion mean,
P50/P95/P99, TPOT mean/P50/P95/P99, receive-gapP99, client scheduling lag,
failure fraction, groupCPU/all attempts, shared host/device costs as0074.
Client gaps include receive coalescing/scheduling, not GPU-generation stamps.
All-attempt outcomes, max in-flight, protocol/close errors and finite pool
disagreements stay. A positive primary with adverse before latency/CPU is a
tradeoff; disclose it and do not claim broad faster/cheaper serving.
A significant native loss stays a native loss even with an ablation gain.
No exact historical6.36ms decomposition is claimed.

Same resource_observer and separate5s loaded-idle bracket per process;
owned-group CPU includes io-wq in TGID once, never add nested thread runtime.
Host/cgroup/softirq/device/observer are shared/context views, not exclusive
service cost. Preserve unrelated load, do not tune affinity/frequency/settings.
Record actual exposure. Client transfer/compression after server stop before
next cell; aggregate analysis/plot/publication after complete matrix.
No own heavy Git/archive work during measured brackets. Source and expanded
commands frozen before first full cell.

## Closure and decision

Run every admitted cell to terminal; preserve failures/exclusions/deviations
and affected invalid runs. Archive commands/source/builds/oracles/raw outcomes,
CPU-only byte-identical replay and one figure with all fifteen paired points,
means and numeric adverse native rows. Fresh result reviewer independently
checks completion/metrics/baseline engagement/uncertainty/correctness/scope.
No perf microbenchmark or extra model sweep is necessary to decide this
hypothesis; mechanism interpretation remains the constructor intervention.

If primary is inconclusive/adverse, keep the original adopted0074 header and
archive this candidate; do not undo a commit or preserve an unjustified flag.
A supported benefit plus valid lifetime checks may justify retention with
native/secondary limits explicit. Any failure of correctness/fairness
invalidates affected performance, never changes the oracle to pass.
Research value supporting and local mechanism/workload impact, not a general
thesis verdict. Full project speed objective remains open unless broader
matched evidence actually establishes it.

Commit/push completed steps main as user requested, own paths only.
Delete the bounded Job/Pod after original data recovered, no pins/GPU servers,
preserve original Workspace/PIDs/WIP. Do not create a scheduler/control layer
or formal RQ. No paper/idea-story/user-instruction document is edited.
