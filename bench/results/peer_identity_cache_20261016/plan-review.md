# Independent plan review: GPU-local immutable peer identity

Reviewed 2026-10-16 UTC, before application/build/measurement. Role: supporting
intervention within the retained serving throughput/latency objective.

## Decision

Proceed to the declared qualification, real preflight and complete matrix.
I found no scientific or executable defect that would invalidate the proposed
comparison, and no concrete new cache-lifetime or ordering counterexample in
the archived candidate. This is a plan assessment, not a claim that the cache
is correct in all executions or that it improves performance. No additional
baseline, workload, profiler run or review round is required by this review.

## Evidence examined

Read plan.md, candidate.diff and both complete controller-header snapshots;
the current canonical executor/io_uring_tcp.h byte-matches the before snapshot
and its exact unified diff matches candidate.diff. Also read README, current
architecture/evaluation conclusions, the closest-work/baseline map, and findings
0054,0066,0074. Inspected normal Make recipes, allocation, initialization,
ACCEPT/CQ draining, request matching, close/reuse, stop/cancel and pending hash
source. No repository-level or parent /workspaces AGENTS.md/CLAUDE.md was present;
the supplied original-Workspace/main/foreign-work boundaries apply.

0054 moved regular IoStats accounting using a separate device allocation and
shared-control split; its primary throughput evidence was inconclusive and its
source was rejected. 0066 memoized repeated close-guard scans; its primary
evidence was inconclusive and it was rejected. Those do not estimate this
immutable accepted-peer placement constructor. 0074 establishes a CPU repair
while leaving a measured native throughput/completion-tail disadvantage.
The new proposal does not reopen any unchanged experiment.

## Admission and competing explanations

The intervention is relevant to the outstanding speed question: the current
active-list join repeatedly reads accepted peer address/port from a mapped
host buffer, whereas the containing connection list already resides in device
memory. A small, direct counterfactual tests whether moving those immutable
reads is useful after the CPU-coordination repair. Existing raw results cannot
supply that unexecuted counterfactual. This is a reasonable strongest runnable
next discriminator among the alternatives described in the plan, rather than
a guarantee that static read frequency identifies the dominant bottleneck.

Success and failure change the source decision. A supported primary gain can
justify this bounded transport constructor; an inconclusive/adverse result
rejects performance-driven retention and preserves the CPU-only boundary.
A native win prevents a faster-than-native claim even if the ablation improves.
A lower-load cost matrix would answer a different question; another unchanged
vLLM run or model sweep does not discriminate this read placement. No need to
add those as conditions for execution.

This is supporting evidence, not independent model arithmetic novelty, a
general eBPF win, or a precise explanation of the historical 6.36ms marginal
P99 difference. Source-level location changes, IoConn stride and resulting GPU
controller/parent code generation all belong to the intervention. A gain would
not isolate physical PCIe transfers. The plan explicitly keeps model source/
capture/precision and native GPU code unchanged, while allowing changed
candidate-controller code generation; that attribution is appropriate.

## Baselines, endpoint and uncertainty

Efficient native C++ timed epoll with identical reused GPU computation is a
credible main competitor and may win. Before is correctly labeled the
component ablation. Its old numbers do not replace contemporary pairing.
Official vLLM is already a whole-service external reference, with stated
scheduler/protocol/KV differences; citing it here is sufficient. Additional
incompatible direct-NIC or weak CPU rows are unnecessary.

The fixed primary candidate-minus-before delivered output tokens/s over the
actual full client window is a recognizable throughput endpoint. Five paired
blocks, frozen gamma schedules and explicit three-path orders are executable
and sufficient for this narrow constructor decision. The nominal t95(df4)
interval and single-primary rule are explicit. Crossing zero remains
inconclusive, not equivalence; collecting more until a win is prohibited.
Rotated orders are not a perfectly balanced six-permutation design and five
blocks provide limited protection against shared-host drift, but these are
stated limits rather than invalidating defects.

All-attempt failures, partial observations, fixed per-I/O timeout/full drain,
finite-pool disagreements and failure-censored success quantiles are retained.
The declared 46 contrasts include client scheduling, TTFT/completion/TPOT,
receive-gap P99, CPU and resource views; adverse native and before rows cannot
be replaced by favorable secondary metrics. The overloaded offered workload
can amplify small capacity differences into queueing tails; these are service
tails under that workload, not intrinsic per-operation latency. Shared host/
device readings and nested thread views are correctly separated from exclusive
cost and cannot prove total resource or energy savings.

Fixed two-model trace/independent replay plus ordinary lifecycle and graph
oracles qualify finite behavior. Frozen sequence-pool membership in the full
run is weaker than fresh trajectory-level fidelity; the plan retains this
boundary and does not expand the pool from observed outputs.

## Controller lifetime and visibility inspection

The cache is in the existing cudaMalloc connection array; the size expression
uses sizeof(IoConn), so appending two fields grows the existing allocation by
8 bytes per entry under the ordinary ABI. There is no second allocation,
shared-page ABI change, lookup table, worker, flag or timer.

The single network-controller thread obtains CQ tail with the existing
ld.acquire.sys operation and memory clobber before reading CQEs and the ACCEPT
sockaddr. Candidate copying occurs only for successful ACCEPT, before that
entry is linked into active. Failed ACCEPT returns to free and never exposes
a cached peer. Existing aggregate initialization at startup and at accept
submission value-initializes the appended fields; successful reuse overwrites
both before publication. No mapped-peer writer for an active accepted entry
was found: receive data occupies offsets 0..4095, sockaddr starts at4096,
length is at4112 and stride4160. Subsequent accepts only reuse free entries.

Close completion/removal, receive cancellation, generation progression and
the free-list rule are unchanged. A cached peer is used only while its entry
is active. EOF bucket computation retains the same raw network-order u32/u16
values and the same bf_pending_bucket function; pending acquire then fresh
head observation remain intact. Hash collisions remain conservative delays,
not newly changed ownership. Tuple-only identity and any earlier reuse
assumptions are inherited; this change does not claim to solve arbitrary
identity-generation races.

Upstream Linux io_accept calls do_accept with the supplied address pointers
before recording successful completion; io_commit_cqring publishes CQ tail
with a release store. The candidate therefore uses the existing CQ visibility
protocol at the natural completion point. This source ordering does not by
itself establish every cross-device coherency/platform guarantee. CUDA's
mapped-memory guidance requires synchronization and is not a proof of this
custom persistent ring. The plan appropriately relies on the already-tested
platform protocol plus real reuse/reset/idle/stop qualification, without
claiming a new universal memory-model proof. I found no new earlier unsynchronized
read or mutable-address use introduced by caching.

## Execution and closure

The normal Make targets and dependencies exist, including independent8/16
output directories and trace/native builds; the header is a declared dependency.
Qualification, actual real-model preflight, all15 terminal full cells, immutable
before objects, frozen sources/expanded commands, raw/replay/figure and
post-stop collection are specified. A runner named in a plan still needs
materialization and real preflight; its absence at proposal time is not a
scientific blocker. No measurement is authorized by this review outside that
plan. No need for an extra microbenchmark to decide the constructor effect.

Proceed using the planned original Workspace and bounded remote client,
preserving original sessions/foreign work and cleaning the client afterwards.
Source retention remains conditional on the fixed result, not this review.
Only this review file was written; no builds, GPU work, Job/runtime/source
changes or Git actions were performed.

## Primary sources checked

- [NVIDIA CUDA Best Practices, zero copy](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#zero-copy):
  motivates avoiding repeated mapped reads on discrete GPUs; establishes no
  local speedup or transaction count.
- [CUDA13.0.1 Programming Guide, mapped memory](https://docs.nvidia.com/cuda/archive/13.0.1/cuda-c-programming-guide/index.html#mapped-memory):
  shared mapped accesses require synchronization; this is a boundary on the
  guarantee, not proof of the custom ring.
- [Linux7.3-rc3 io_uring/net.c, io_accept](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/net.c):
  address-using accept precedes completion result.
- [Linux7.3-rc3 io_uring/io_uring.h, io_commit_cqring](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.h):
  CQ-tail release publication.
