# 0074: active admission waiting reduces process-group CPU
2026-10-16 UTC.
[Plan/review](../../bench/results/active_admission_wait_20261016/plan.md),
[complete result](../../bench/results/active_admission_wait_20261016/result.md),
[independent result review](../../bench/results/active_admission_wait_20261016/result-review.md),
[ordinary-source adoption](../../bench/results/active_admission_wait_20261016/source-integration.md).

## Question and controlled change

Within the retained same-compute serving throughput/latency question,
finding0073 identified BPF loop coordination as a material creator-thread
CPU cost. This intervention tests its avoidability: restrict the
admitted != admission_seen immediate-return exception to may_idle. Active
execution can then wait for the next CQ/timer event; idle admission wakeup
behavior stays immediate. Timer60us, GPU computation, default8 slots, ABI,
native transport and host settings are unchanged. This is supporting causal
mechanism evidence; it does not claim a new model optimization.

The unmodified before kernel is a component ablation. Efficient C++ epoll
with the same resident GPU executor is the main competitor. Official vLLM
remains the separate whole-service reference in finding0069; its broader
protocol/scheduler/KV differences do not isolate this BPF condition.

## Complete five-block remote comparison

Normal16 builds, Qwen2.5-0.5B-Instruct FP16, same RTX5090, fixed four-prompt
pool/gen64,192 offered requests/s for60s plus complete drain. All15 cells
finish: each condition57600/57600 successes,3686400 measured tokens; total
172800 requests/11059200 tokens plus120 excluded checked warmup tokens.
No profiler runs in this matrix. Zero observed failures is not a
rare-failure bound. All752 finite reference-pool disagreements are retained;
protocol success is not exact full-run model fidelity.

| Mean of five cell statistics | Before kernel | Adopted active wait | Native epoll |
|---|---:|---:|---:|
| Owned group CPU ms/attempt |1.701534|0.625739|0.769311|
| Delivered tokens/s |11625.993|11626.457|11646.715|
| Connect completion P99 ms |3395.013|3394.069|3295.820|
| Connect TTFT P99 ms |3309.362|3308.569|3211.722|
| Client receive-gap P99 ms |4.370019|3.993356|4.288793|

The fixed primary candidate-minus-before group CPU effect is
-1.075795ms/attempt, nominal paired95%t(df4) interval[-1.222797,-0.928793].
Candidate-minus-native is-0.143572[-0.182094,-0.105049].
Ratios of condition means are63.22% and18.66% lower respectively.
This supports group-CPU efficiency under this workload.

Candidate-before throughput+0.463[-8.973,9.899]tokens/s,
completionP99-0.944[-44.278,42.390]ms and
receive-gapP99-0.376663[-1.216714,0.463387]ms are inconclusive.
No speed improvement, equivalence or noninferiority follows.
Candidate-native throughput-20.259[-30.273,-10.244]tokens/s and
completionP99+98.249[48.700,147.797]ms remain adverse.
Receive-gapP99-0.295438[-0.669312,0.078436]ms is inconclusive.
All46 promised contrasts and per-cell distributions remain in the archive,
without multiplicity correction. Native's speed advantage is not omitted.

The offered12288tokens/s exceeds delivery for all conditions. Accumulating
queueing plausibly amplifies a small capacity difference into request P99;
that is a load/capacity inference, not an exact stage partition. Client gaps
also include coalescing and scheduling and are not GPU-generation intervals.

## Mechanism context and limits

A separately planned post-matrix creator-TID perf cell completes11520
requests and retains26 finite-reference disagreements. Official perf records
3427 samples,6.867735416s period sum, no loss/throttle records. The observed
coordination/map categories contain501/3427 samples (14.6192%), compared with
7146/10086 (70.8507%) in0073. This is consistent with reduced coordination.
These noncontemporaneous profiled cells are context, not a paired speed
estimate or additive time decomposition. Unknown kernel leaf3 and at least
one unknown frame2896/3427 limit ancestry. See
[profile](../../bench/results/active_admission_wait_20261016/profile.md).

Group CPU includes io-wq time in the service TGID once. Kernel threads,
softirq, cgroup, observer and device views remain separate; shared host/device
totals do not establish exclusive total-CPU or energy savings. No foreign
workload was stopped. The historical14.72 vs8.36ms (+6.36ms) token-gap P99
was not reproduced by later matched controls even before this change; this
result does not explain or fix exactly that old marginal quantile.

## Engineering decision

Adopt the exact normally built candidate as a CPU repair. Default8/explicit16
builds and all4 before/candidate GPU SASS comparisons pass; intended BPF-only
difference and object bindings are checked. Two-model default8 protocol/
dual replay, ordinary idle/reset/partial-stop and cuBLAS/cuFFT checks pass.
Finite concurrency checks do not prove arbitrary backend/model stability.
The independent review validates the run and supporting CPU hypothesis with
native speed losses retained. Original Workspace sessions and foreign WIP
remain; bounded client Job/Pod, own GPU applications and BPF pins are gone.
The broader throughput/latency objective remains open.
