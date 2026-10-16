# Qwen192 streaming-tail diagnosis and repair

Observed start: 2026-10-16 UTC. Parent f56d0ee. Original Workspace only.

## Question and admission
Retain the user's complete Linux TCP/eBPF/shared-queue/resident reused-model
GPU/asynchronous TCP goal and its throughput/latency objective. No formal paper
RQ is invented. This supporting experiment asks why Qwen2.5-0.5B mixed
kernel-loop has worse client inter-token P99 at192 requests/s, and whether a
specific causally justified transport/queue repair reduces that cost.

The completed0065 five-block result is kernel14.723/native8.363ms (mean block
P99); the signed paired difference is6.359661[2.113625,10.605697]ms. Existing
logical traces lack timestamps, and the earlier0057 CUPTI decomposition is
incomplete. Another unchanged timing run cannot answer the mechanism.
The strongest next discriminator is a token-associated timeline, rather than
more compute tuning or resource-only measurements. Native is the main credible
competing implementation of the same service with the same computation.
An external official vLLM server comparison is also user-requested, but is a
separate whole-service reference, not this transport attribution.

Positive: locate and repair a concrete queue/submission/completion cause, then
retain the repair only if correctness and matched retest support it.
Negative/mixed/inconclusive: retain the adverse result and source unchanged
unless an independently correct defect repair is justified. Do not promise
a speedup or force a fix when evidence points to a workload or client boundary.

## Existing-data discriminator
Recompute all five Qwen192 mixed block ITL distributions from raw client
arrival timestamps, stratifying final token versus interior and receive
coalescing. Retain all256 attempts/block, errors, timeouts and client lag.
This is explicitly post-hoc diagnosis, not a new confirmatory effect estimate.
P99(kernel)-P99(native) is not decomposed by adding marginal stage P99s.

## Timestamp diagnostic
Use the exact qualified mixed candidate frozen in0065, explicit16 slots,
same pinned Qwen revision7ae55760/FP16/vLLM0.31.0, four existing prompts,
gen64,256 normalized gamma arrivals at192/s,8 excluded checked gen1 warmups.
Two paired process blocks, alternating loop/native order; same normalized
arrival seeds as0065. One32-arrival real preflight precedes the full diagnostic.

Add private conditional instrumentation only: GPU globaltimer stamps for
logical compute publication/dispatch, GPU I/O progress and send SQE/CQE with
request seq, client marker, byte offsets and result; CPU native send/scan
CLOCK_MONOTONIC stamps with the same associations. Capture GPU-to-host clock
offset brackets with host monotonic begin/end around synchronized calibration
kernels before and after serving. Preserve all brackets; report alignment
uncertainty, check drift and event causal consistency. Never subtract raw
unrelated clocks or resolve differences below calibration uncertainty.
Keep GPU-clock intervals in their own domain wherever possible.

A private tracefs instance uses mono clock and existing io_uring submit_req,
complete, queue_async_work plus sched_switch/wakeup and softirq entry/exit
events. Do not modify the global tracer or other instances. Preserve formats,
all CPU buffer overrun/drop stats and complete trace. Match ring/user_data and
host thread identities; unrelated global events are exposure, not attributed
service CPU. Missing/overwritten coverage invalidates affected decomposition.
If defaults cannot retain the finite trace, document the observed overflow
before a bounded buffer adjustment or streaming capture; preserve failed data.
Tracepoints report kernel submission/completion, not proof of NIC wire delivery.
For local sockets, client receive remains the actual delivery observation.

For each token, map GPU production -> GPU observation/SQE publication ->
kernel submission -> send CQ completion -> client arrival where observable.
Intermediate sends may include multiple tokens/partial bytes; reconstruct byte
coverage and actual CQ result, never assume one send per token. Separate
compute-production gaps, GPU poll/queue gaps, SQ-to-kernel delay, kernel send
interval, completion-consumption delay, and delivery/client scheduling residual.
Their critical-path intervals can overlap; do not claim an additive allocation
of the6.36ms marginal-quantile difference. Softirq/io-wq/scheduling explain
overlapping intervals only when associated causally; otherwise label unresolved.
All per-token/round data and failures remain available.

Instrumentation is a mechanism diagnostic, not replacement uninstrumented
performance evidence. Both paths have logical timestamp instrumentation;
different event frequencies can change overhead. Compare to original0065 and
later fresh equally BF_TRACE controls without timeline/ftrace. No CUPTI
complete-kernel-count dependency or model arithmetic change is introduced.

## Correctness and repair selection
Keep existing exact independent captured/history and source-native fresh
attention-metadata replay for every completed diagnostic trajectory. No token
tolerance or observed-output expansion. Validate complete ownership, zero
graph/trace/ring errors, successful shutdown and exact client responses.

The repair is chosen only after diagnosis and documented in this same plan
with the measured causal mechanism and concrete source diff. Obtain the same
plan reviewer's focused follow-up before the confirmatory collection.
Do not sweep arbitrary timer, affinity, CPU/GPU settings or per-model kernels.
Default8 ordinary builds and mid-output cancellation are engineering acceptance
conditions for adopting mixed scheduling/repair, not paper-performance results.
Preserve canceled outputs as incomplete prefixes; never weaken the completed
trajectory oracle to call cancellation a complete correct response.

## Confirmatory repair comparison
After a concrete fix is frozen: before-fix loop, after-fix loop, and efficient
native with identical improved GPU model constructor at16 slots. All equally
BF_TRACE, no additional timeline/ftrace. Five paired process blocks, balanced
cyclic order of the three conditions, alternating rate order96/192.
Same Qwen model/prompts/gen64/256 attempts, seed schedules/timeouts as0065.
No replacement of unfavorable blocks. Primary: after-minus-before block ITLP99
at192/s, nominal paired t95df4, with signed comparison against native.
Report TPOT, TTFT/completion P50/P95/P99, delivered-window token/s, all failures,
timeouts, client scheduling lag and scheduled-origin latencies. Do not pool
requests across process blocks for the primary uncertainty. Crossing-zero
intervals establish neither superiority nor equivalence.
An adverse metric remains visible. Correctness/fairness failures invalidate
affected comparisons; throughput/other tails qualify any narrower improvement.
A transport source fix also needs the existing Smol/default8 regression path;
broader performance generality is not inferred without matched measurements.

## Commands, completion and restoration
Setup/build uses existing Make recipes and pinned requirements in owned
/tmp/bpfusion-mixed-integration-n4cog5c6; never overwrite original builds/WIP.
Private scripts/source/commands/raw timelines/analyses are archived here.
Runnable diagnostic entrypoint: runtime/bin/python tail_diagnostic.py.
Runnable independent analysis: /usr/bin/python3 analyze_timeline.py RAW.
The exact entrypoints are implemented and frozen before real preflight.
Full completion requires every fixed cell, exact replay and one fresh result
review terminal; a partial prefix is incomplete. Publish each validated step
on main, then the final experiment and review. Keep root README/evaluation
honest about candidate versus selected ordinary source.
Use the original Workspace and current GPU. Do not change services, host
settings, model arithmetic, credentials or other active sessions. Remove owned
trace instance/pins/processes and temporary env/builds after reference checks;
verify original path stats/Coder sessions/base packages and source status.

## Concrete repair proposal after diagnostic (2026-10-16 UTC)
The two-pair diagnostic and independent CPU analysis locate submission-thread
runnable waiting, plus GPU I/O iteration cost and client waiting. No source
fix can erase unrelated CPU runqueue/client waiting. The targeted removable
queue cost is repeated host-mapped admission loads in each connection's close
check. With only16 model slots, active connections peak245/160 because EOF
connections wait for global admission drain. A post-hoc kernel accept-minus-
close approximation shows per-progress median rising from0.103/0.132ms at
0..32 connections to0.654/0.527ms above128. This is association, not proof of
exclusive cause; kernel/GPU CQ consumption lag bounds the approximation.

Candidate in candidate-close-guard.diff adds a per-io_progress tri-state cached
guard. After one EOF/dead peer finds admission not drained, skip further
expensive host-mapped close checks for that scan. If the cached guard is true,
retain the entire original per-close predicate and live rechecks. This can
only conservatively postpone a close within a scan; it cannot authorize an
earlier close. Recompute on the next progress iteration. There is no timer,
priority, affinity, queue capacity, protocol, numerical or admission-order
change. Single-in-flight sends and FIFO retirement stay unchanged.

Freeze candidate and before Cu/Py plus both network headers and compile through
ordinary Make at8/16. Ordinary8 mid-output cancellation and exact traced8
protocol regression qualify safety. Before/fixed/native confirmatory collection
then uses the exact same mixed constructor and original clean client,
identical BF_TRACE on all3, explicit16 slots,96/192,256 attempts/cell,
8 warmups and5 paired process blocks. Source changes only the network close
scan. Names:uring_loop_16_before_mixed,uring_loop_16_fixed_mixed,
userspace_16_mixed. Per-block orders are[before,fixed,native],
[fixed,native,before],[native,before,fixed],[native,fixed,before],
[fixed,before,native]; rate order alternates. No timeline/ftrace is active.
Primary and uncertainty remain after-minus-before ITLP99 at192 with t95df4;
same-fixed-vs-native is reported alongside. All existing exact dual history/
fresh-metadata checks, errors, timeouts, lag and secondary metrics remain.

If the effect is inconclusive or adverse, do not call the candidate a fix for
the6.36ms or repeat a timer/model sweep. Retain the complete source/result and
use the diagnosed CPU/client limits to choose the next causal discriminator.
If supported, adopt only after ordinary source integration/regressions.
The complete resource/remote/official-server/generic-backend tasks remain.
