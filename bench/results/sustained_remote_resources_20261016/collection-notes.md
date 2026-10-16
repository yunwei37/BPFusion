# Collection observations; full matrix still active

2026-10-16 UTC. These are acquisition notes, not a completed result or cause proof.

At the first two192/s kernel cells, retained outcomes are10694/11520 successes
with826 read TimeoutErrors, and10705/11520 with815 read TimeoutErrors.
Corresponding native cells both11520/11520 succeed. No failure is excluded.
First kernel failures have no observed output token and wait the declared60s
read-operation timeout. Failed requests censor successful tails.

The first kernel server reaches4096 connections despite client max in-flight
1678. Its ring reports no pending/error/drop/overflow at terminal, but admission
count is lower than received frames by the failure count. Ring drop0 therefore
does not establish that every received request entered the model queue.

Source inspection identifies a candidate: executor/io_uring_tcp.h314-315 closes
an EOF/dead connection only when global llm_queued is0 (plus other safety
conditions). This can retain already-finished connections during a sustained
backlog. The sockops insertion into4096-entry streams bumps counter13 on failure.
A connection-capacity/map-insertion mechanism remains a hypothesis until direct
counter/lifetime evidence is acquired. No source, timer, capacity or scheduling
condition is changed during this matrix.

Owned checkpoint/analysis exposure is retained. A read-only CPU scan and gzip
archival of three terminal executors ran during the then-active pair1 kernel96
cell around11:31UTC, completing at the checkpoint.json observation time.
It is outside the attributed server group and adds host CPU/I/O exposure.
Do not claim a clean/exclusive hostCPU comparison; keep that secondary cell,
do not replace it. This checkpoint does not overlap those already completed
192/s cells. Future heavy archive/analysis is deferred to terminal to avoid
adding further acquisition noise. Shared foreign workloads continue unchanged.

All completed raw files stay in original TEMP; the partial durable archive
contains three complete executor prefixes. No partial prefix is full completion.

Additional bounded read-only snapshots are retained as full_p2_kernel.readonly_stats_1.json
and full_p3_kernel.readonly_stats_1.json in original TEMP. Pair2 during96/s has
sockhash_failed0/linked4549, page llm_queued0. Pair3 during192/s resource-bracket
elapsed61.58s has sockhash_failed835/linked10693, while generic drops remains0.
The latter counter read takes1.44ms; the former3.59ms, plus ordinary control exec
overhead. These are diagnostic exposure, not a source or workload change.
The failed insertion observation directly supplies a missing failure class,
but errno/capacity vs other insertion causes is not yet independently isolated.
The current full matrix still runs unchanged; no repair is substituted mid-run.
