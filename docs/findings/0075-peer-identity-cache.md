# 0075: immutable peer identity does not establish a speed benefit

2026-10-16 UTC.
[Plan](../../bench/results/peer_identity_cache_20261016/plan.md),
[plan review](../../bench/results/peer_identity_cache_20261016/plan-review.md),
[complete result and raw data](../../bench/results/peer_identity_cache_20261016/result.md),
[independent result review](../../bench/results/peer_identity_cache_20261016/result-review.md),
[source selection](../../bench/results/peer_identity_cache_20261016/selection.md).

## Question and comparison

Within the retained same-compute serving throughput/latency question, test
whether caching accepted peer address/port in existing device-local IoConn
instead of repeatedly reading mapped sockaddr improves delivered throughput.
The candidate copies identity only after successful ACCEPT completion and
uses the unchanged peer scan and EOF pending-bucket lookup. Existing entry
stride grows naturally by8bytes; controller layout/code generation changes
are part of the intervention. No allocation, table, ABI, timer, worker,
model arithmetic, default capacity or persistent runtime setting changes.
This supporting experiment supplies a previously absent placement ablation;
it does not measure exclusive PCIe cost or introduce a new model kernel.

Before is the adopted0074 active-admission-wait kernel, a component ablation.
Efficient native C++ epoll with the same GPU executor is the main competitor.
The separate official vLLM whole-service reference remains finding0069.
Normal default8/explicit16 builds, unchanged BPF instructions/relocations,
unchanged native GPU SASS, two-model replay/cancellation and finite cuBLAS/
cuFFT numerical checks precede full collection. Candidate controller SASS
may differ. Actual immutable source/binary bindings are archived.

## Complete matched remote result

Qwen2.5-0.5B-Instruct FP16, same RTX5090, mixed16 slots, four frozen short
prompts,64 output tokens,192 offered requests/s for60s plus full drain.
Five frozen process orders each contain before/candidate/native. All15
cells finish:172800 successes/172800 attempts and11059200 measured tokens,
plus120 excluded checked warmup tokens. No timeout/protocol/close error.
All643 finite-reference-pool disagreements remain flags; protocol success
is not exact full-run model fidelity or a rare-failure bound.

| Mean of five cell statistics | Before kernel | Peer cache | Native epoll |
|---|---:|---:|---:|
| Delivered tokens/s |11623.357|11624.747|11644.018|
| Connect completion P99 ms |3413.676|3407.237|3302.366|
| Connect TTFT P99 ms |3329.269|3322.922|3217.555|
| Client receive-gap P99 ms |4.551023|4.724972|4.605981|
| Owned group CPU ms/attempt |0.627792|0.642501|0.779964|

The fixed primary candidate-minus-before throughput effect is
+1.390100488tokens/s, nominal paired95%t(df4) interval
[-2.910413831,+5.690614807]: **inconclusive**.
CompletionP99-6.439[-33.151,+20.273]ms, receive-gapP99
+0.173950[-0.749591,+1.097491]ms and groupCPU
+0.014708[-0.008151,+0.037568]ms/attempt also cross zero.
This establishes neither equality nor noninferiority.

Candidate-minus-native throughput is-19.271234[-22.505645,-16.036823]tokens/s
and completionP99+104.870610[74.187469,135.553751]ms: both adverse.
GroupCPU is lower by0.137463[0.114250,0.160676]ms/attempt; this advantage
already exists in the before path after0074 and is not a cache benefit.
All46 predeclared contrasts and cell distributions remain in the raw archive;
secondary intervals are nominal without multiplicity correction.

## Interpretation and source decision

The fresh result review independently recomputes all15 cells/46 contrasts,
checks normal builds, actual native engagement, source/binary equality controls,
archive replay, cache lifetime and finite correctness scope. Run status is
valid; primary inconclusive; research value supporting; impact a tested
mechanism/workload boundary. The cache is rejected under the fixed decision.
Only our uncommitted header was restored byte-for-byte to the already-selected
0074 source. No flag, larger N, unchanged favorable rerun or commit undo.

Offered12288tokens/s exceeds delivery; accumulating backlog is a plausible
reason a small capacity difference affects seconds-long completion tails,
not a measured allocation of internal stage time. Client receive timestamps
include batching/scheduling. The historical14.72 vs8.36ms (+6.36ms) token-gap
P99 was not reproduced by later matched controls even before changes; this
result does not partition or claim to repair that old marginal quantile.

Owned group CPU includes its io-wq once. Cgroup, shared host IRQ/softirq,
observer and GPU-energy views overlap and contain retained other work;
whole-service total CPU/energy savings are unproven. The setup-only missing
offset-file preflight failure and unchanged successful retry remain archived.
All full cells remain; no oracle/timeout/pool change. The bounded client
Job/Pod are gone, no GPU applications/pins remain, and original Workspace
sessions/foreign WIP are preserved in cleanup receipts.

Next decision: retain0074, close this cache comparison and investigate a
distinct cause of the remaining native speed advantage using current evidence
before admitting another run. The full throughput/latency objective is open.
