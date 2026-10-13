# Fresh plan review: optimized stock TCP transport and worker cost

Reviewer: /root/vllm_uring_plan_review, original Workspace/main, 2026-10-13 UTC.
Read-only review; no files edited or serving runs executed.

## Round 1

Verdict: admit the experiment; scientific design acceptable, executable
adaptation and concrete command bindings pending.

Admission holds: finding0035 lacks stock transport/worker CPU and0041 is only
integration correctness. The changed completion/stock mechanism adds evidence
that prior raw cannot supply. Supporting local scope retains0035's question
and leaves0029's cross-node question unchanged. Positive/negative/mixed/null
outcomes change the allowed claim and next engineering action. Negative local
results bound these mechanisms, not the full goal. No broader matrix required.

Native timed epoll/nonblocking TCP is a credible main mechanism alternative;
module is a component control. Makefile uses the same packed/prefix flags,
upstream computation, precision, checkpoint/KV/wire/input/request budget.
Existing native wait and stock polling defaults are part of the tested cost/
latency tradeoff. A stock/module effect cannot exclusively identify polling:
submission, completion, ordering and synchronization also differ.

The pre-observation complete-sequence oracle avoids mixtures/tolerance/teacher
forcing/expansion, but does not establish current unobserved batch history.
An implementation returning a historically qualified sequence could pass.
0041's actual-history replay plus unchanged compute and ordinary strict
qualification justify the scoped timing design. New-sequence failures must
be retained/diagnosed separately without expanding this run's reference set.

Primary TTFT1/c1 and throughput64/c8 match the hypothesis. Client arrival and
complete-cell delivery boundaries are appropriate; initialization/connections
are excluded. Versioned official serving-client citation should complement
vLLM's engine/frontend metric documentation; formulas need not change.

POSIX process CPU plus live task identities count SQPOLL once in its server
thread group; module TX is separate. Archive read brackets and components.
Label known-worker CPU during the cell bracket divided by requests. It omits
networking work elsewhere and is not total service CPU, energy or pure
per-request inference CPU. Connection-close work within brackets is included.
CPU is secondary unless the claim specifically requires CPU/Pareto improvement.

Six balanced orders and paired blocks/df5 are appropriate; totals36 executors,
144 cells,9216 requests,299520 measured tokens,288 excluded warmups agree.
Shared host, deterministic temporal order and small block count remain limits.
Report all four primaries, negative/null effects and labeled secondary/control
results; no familywide/equivalence conclusion.

Pending executable defects in inspected snapshot:
1. Driver lacked transport-comparison/6 blocks/CPU snapshots; analyzer needed
stock classification, new family and df5.
2. Plan incorrectly said prior driver rotated cells; implement or correct.
3. Bind actual environment/frozen/model/output paths and child env before runs.

Completion must verify every expected executor/cell/request/reference/terminal/
ownership state. Archive source/header/build/commands/packages, retain failures
and handle continuity, fresh result review and final owned-resource cleanup.
No additional baseline/model/instrumentation requirement.

## Round 2

Reviewed revised plan, source diff, concrete pipeline/commands and both frozen
assets. Verdict: identified executable gaps resolved; proceed to real preflight
then ordinary strict qualification. No remaining result-invalidating defect.

Verified three modes, six complete performance permutations, one-block
preflight/strict, correct main/control comparisons and df5 with preserved
historical five-block path. Stock ordinary verification reads kernel page/
ring counters, queue equality and diagnostic truncation, not native-worker
counters. Cell rotation is identical across transports in each block.

Verified initial CPU snapshot after ready barrier, all raw/component deltas,
nonnegative arithmetic and sample brackets containing first send/last arrival.
Actual task snapshot requires stock SQPOLL. It is counted once through the
process clock; possible lane-close work and limited CPU scope are explicit.

Concrete pipeline/commands bind actual runtime, pinned checkpoints, frozen
asset/output paths, PATH and VLLM_ENABLE_V1_MULTIPROCESSING=0. Build/Qwen
preflight/both strict/analysis stop progression on failure. Runtime and archived
frozen assets match: Qwen17 keys/22 complete sequences,Smol17/19. No expansion.
Official versioned client citation added; git diff --check succeeds.

Before timed collection archive literal performance invocations with the same
frozen asset and validated main source. Historical reanalysis does not replace
real preflight/strict. Preserve any failures; do not alter workload/oracle/
timing to obtain a pass. No additional baselines/models/breadth demanded.
