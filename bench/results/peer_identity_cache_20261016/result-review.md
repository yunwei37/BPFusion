# Independent result review: immutable peer identity

Reviewed 2026-10-16 UTC after all fifteen full cells and acquisition/CPU
archive analyses completed. This is the single fresh result review of this
completed immutable run. No new GPU execution, build, runtime/configuration
change, source edit, Git action, workload or favorable rerun was performed.

## Judgments and decision

- Run status: **valid** for the declared finite constructor comparison.
- Tested primary hypothesis: **inconclusive**. The interval for the fixed
  candidate-minus-before delivered throughput effect crosses zero.
- Research value: **supporting**, a nonredundant bounded mechanism result.
- Paper impact: **mechanism/workload boundary**, additional serving-path
  evidence; neither a direct thesis challenge nor a whole-RQ answer.
- Next decision: follow the predeclared source decision: restore the adopted
  0074 header, archive this candidate and retain the existing CPU-efficiency
  conclusion and unresolved speed disadvantage. Do not retain a flag or add
  unchanged repetitions to seek significance.

I found no scientific, fairness, executability or concrete new cache-lifetime
defect that invalidates the completed experiment. Publication and disposable client cleanup remain delivery actions, not
unperformed measurement or reasons to reinterpret the primary. After the
arithmetic audit, the owner restored only the uncommitted canonical header
to the archived before source under the predeclared decision. A final direct
byte comparison confirms that restoration; archived candidate data are intact.

## Independent arithmetic and completion

I read plan.md, the complete plan-review.md, qualification.md, preflight.md,
preflight-deviation.md, result.md, reproduce.md, both full header snapshots,
candidate.diff, acquisition/archived readers, normal build logs, source/argv
receipts, raw client/resource archives, finite lifecycle/trace/graph artifacts
and the plotting source. No repository-level AGENTS.md/CLAUDE.md was present;
the original Workspace/main/foreign-WIP boundaries supplied to this task apply.

Independently parsed all fifteen archived client and active-resource gzip
files, rather than importing the experiment analyzer to obtain the numbers.
Verified complete index sets 0..11519, terminal status, all successful
64-token responses, scheduling stamps, frozen pool flags, stable process
identities and resource brackets. Recomputed all per-cell metrics used by the
46 predeclared paired contrasts: TTFT, completion, TPOT and scheduling-lag
mean/P50/P95/P99; client receive-gap P99; delivered TPS; failures; group CPU;
Workspace cgroup CPU; shared host active CPU and device energy. Recomputed
every paired block effect, mean and nominal t95(df4) interval using the fixed
2.776445105 coefficient. All match analysis.stdout within floating arithmetic.

All15 client exits and server terminals are0, all terminals have empty pins.
The observed process order exactly matches the five frozen orders. All15
eight-request warmup archives contain successful checked gen1 responses and
are excluded from the measured172800 attempts. Per condition there are
57600 successes/57600 attempts and3686400 tokens; total11059200 measured
tokens plus120 warmup tokens. No missing, excluded or replaced full cell;
no transport/protocol/close error or timeout. Zero observations do not prove
a rare-failure rate guarantee.

Frozen reference disagreements independently total235 before,180 candidate,
228 native,643 overall. Each stored boolean matches membership in the
unchanged frozen pool. They remain flags, not exact full-run fidelity evidence
and not discarded failures. No observed output was used to expand the pool.
The two-model traced qualification provides the separate finite exact check.

The primary is:

    candidate - before delivered TPS:
    +1.390100488 [-2.910413831, +5.690614807]

This is inconclusive, not equality or noninferiority. The main competitor
contrast remains adverse:

    candidate - native delivered TPS:
    -19.271234036 [-22.505644825, -16.036823248]

    candidate - native connect-completion P99 ms:
    +104.870609988 [74.187468727, 135.553751249]

Every reported summary-table mean and signed-effect/CI table row recomputes
from the raw archives. Candidate-before completion P99, receive-gap P99,
group CPU, host CPU and device energy intervals also cross zero. Candidate
group CPU is lower than native (-0.137463240ms/attempt, interval
[-0.160676277,-0.114250203]); that advantage already exists in the adopted
before path and is not a new cache benefit. The single primary and nominal
unadjusted secondary intervals are correctly distinguished.

I also ran the archived full analyzer with PYTHONDONTWRITEBYTECODE=1:
exit0, empty stderr, byte-identical acquisition stdout. This corroborates the
independent arithmetic and is not a replacement for it.

## Main baseline and controlled intervention

Before is the adopted0074 active_wait_sourcebuild16 component ablation.
Efficient native C++ timed epoll from that same build is the main competitor;
the candidate uses peer_identity_sourcebuild16. All15 receipts identify
the correct immutable header snapshot rather than claiming the current Git
HEAD describes a selected binary. Each condition has identical model source,
model path/revision, weights/FP16, prompts, capacity16, model/capture code,
native implementation, shared ABI, BPF sources and timer/socket policy.

Directly compared normal8/16 BPF disassembly with relocation information:
both fusion.bpf.o and uring_loop.bpf.o equal their adopted before controls.
Direct cuobjdump comparisons confirm native GPU SASS equality at both
capacities. The candidate kernel libraries contain their intended absolute
BUILD/uring_loop.bpf.o binding. Normal Make logs include nvcc -dc, device
link and native linking; no private command rewriting is substituted.
Candidate GPU controller code and IoConn layout may differ, as the plan
permits; whole candidate-kernel SASS equality is not asserted.

Native baseline engagement is real: all five logs report epoll_pwait2 with
60000ns active timeout and socket/deadline idle wait, eventfd shutdown,
eligible_frame_fifo admission and queued_at_stop=0. Each records11528
accepted/published/completed requests, including8 excluded warmups, with
zero rejected. Contemporary matched delivery/CPU/tail observations therefore
do not obtain a proposed-method win from a broken, spinning or unengaged
native baseline. The official vLLM comparison is not silently substituted:
finding0069 remains the separate whole-service external reference with
protocol/KV/scheduler differences. Another baseline is unnecessary to decide
this intervention.

At source inspection the one production WIP byte-matched the archived
candidate, five lines added and five removed. It adds two immutable fields with natural8-byte struct
growth to the existing IoConn allocation, leaving the existing linear lookup.
No new allocation, table, service, worker, option, shared ABI, timer/default
capacity or policy entity. Most new files are ordinary frozen experiment
sources/logs/readers needed to run and reproduce this comparison, not runtime
scaffolding or an independent scientific contribution.

## Cache visibility and lifetime

The CQ consumer observes the existing system-acquire CQ-tail protocol before
reading successful ACCEPT results. Only e.res>=0 copies raw sockaddr IPv4
address/port, then links the entry into active. Failed accepts return to free
without becoming visible in active. Initial and per-accept aggregate
initialization zero the appended members. The sockaddr region starts at4096,
outside the4096-byte receive data area; ordinary receive does not overwrite it.

Upstream [Linux7.3-rc3 io_accept](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/net.c)
supplies address pointers to do_accept before recording a successful result;
[io_commit_cqring](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.h)
publishes CQ tail with a release store. The cache retains the existing
platform synchronization context. This source ordering is not a universal
proof of cross-device mapped-memory coherence; the finite tests exercise
the already-used platform protocol.

Cached identity is constant while the entry remains active. It is used by
the same peer-list match and same network-order pending-bucket function.
Close completion/removal precedes free-list reuse; receive ownership,
generation progression and cancellation ordering are unchanged. EOF still
acquires pending before freshly observing head, and hash collisions remain
conservative. The candidate does not fix or newly claim arbitrary
tuple-generation/reuse correctness. I found no concrete newly introduced
read-before-ACCEPT, stale cached identity or premature EOF-reclaim path in
the examined change. No such counterexample is supplied by the finite tests;
absence of one is not a universal proof.

The constructor moves reads, changes stride and changes generated controller
code together. A positive or negative measured result cannot identify
exclusive PCIe mediation or prove those mapped reads dominate cost.

## Qualification, independent oracles and deviations

Both archived two-model protocol analyses rerun successfully with
PYTHONDONTWRITEBYTECODE=1 and byte-identical stdout. Inspected the reader diffs:
only gzip fallback/input plumbing differs from acquisition versions; fixed
oracle/mathematical logic is unchanged. Derived trace/reference/metadata
paths are rooted in the passed archive prefix; missing plain files resolve
to the actual archived gzip files, not their original /tmp counterparts.
No GPU work or live original raw file is consumed by these CPU replays.
Qwen/Smol each validate640 outcomes,259 rejects,23376 dual-replayed tokens
and actual batches1..8:1280/518/46752 combined.

Both ordinary default8 lifecycle raw records have144 outcomes, exit0,
model_errors[0], empty remaining_pins and pass=true. Independently checked
counts: Qwen869 checked complete/prefix tokens,155 partial; Smol925/211.
Each has66 explicitly partial rows and47 unobserved cancellations. The
source checks observed prefixes against the preexisting frozen reference
pool. Partial-header/zero-byte/reset/stop observations do not become complete
model outputs or independent token-fidelity proofs. Idle/active2.2s
transitions, reuse, half-close, reset, queued work and mid-output stop are
exercised; unchanged native qualification is explicitly reused.

All four graph raw cases contain182 checks and passed status. Recomputed
their ordinary numerical output independently: scalar8x8 matrix arithmetic
and a direct complex32-point DFT, not the GPU outputs or the acquisition
special-case FFT oracle. All agree. Stop observations are finite prefixes:
matmul native2816/8192bytes, loop2048/8192; FFT native256/8192, loop0/8192.
Their zero/partial nature remains explicit and does not invalidate the
ordinary completed numerical cases. This qualifies finite shared-header
cuBLAS/cuFFT usage only. HF is compile-only; absent optional AMK vm dependency
is correctly reported as unqualified, not an extra successful backend.

First preflight contains metadata and a FileNotFoundError before scheduling
any measured request. Its checked warmups and terminal records are retained;
it is not a successful before performance cell. The retry uses the unchanged
128-offset prefix, independently verified against the full frozen schedule.
All three retry client exits0 and384 successes are retained. Full client
source/config byte-match the prior0074 assets; each full block's offset
list matches the frozen original. Per-I/O60s timeout and full task drain are
unchanged. Setup-only failed Windows-path submission is disclosed, not a
measured result. These repairs do not alter the hypothesis or full-run metric.

## Resource, timing, figure and claim limits

Process group clocks include owned TGID CPU once; io-wq thread runtime is
a nested explanatory view, not extra CPU to sum. Cgroup, host/softirq/kernel
worker, observer and device totals overlap and contain retained other work.
Actual observer brackets exceed client windows, as the source/driver state.
Loaded-idle is separate; neither idle subtraction nor exclusive total service
CPU/energy attribution is invented. Observer overhead remains material and
comparable: roughly0.380-0.385ms/attempt across conditions, separately
recorded. This does not erase the measured group CPU contrast but bounds
whole-system cost interpretation.

All cells have the same frozen client/observer source and client Python
version. Server processes do not overlap; actual chronological order matches
the plan. The driver stops the server before client compression/transfer and
per-cell archive, then starts the next server. Aggregate analysis/plot runs
after all fifteen. Shared host/load and imperfectly balanced rotating order
remain limits, rather than being treated as exclusive controlled hardware.
The postmatrix receipt records no GPU applications/pins and original
PID1/PID10909 identities. Selected-source restoration was verified after the numerical audit;
temporary client deletion remains an owner closure action at this review.

Inspected the rendered PNG and plotting source. All15 observations appear,
with correct paired block connections, metric/unit labels and condition
order. Horizontal bars are arithmetic means, not CIs; no favorable plot-only
number contradicts the independently checked analysis or adverse native rows.
The cropped TPS scale is appropriate for displaying small measured
differences, with numeric paired intervals supplied in the report; it does
not establish significance by visual separation.

At192/s and64 outputs, offered demand12288tokens/s exceeds all delivered
rates. Accumulating backlog is compatible with seconds-long completion tails
and their sensitivity to small capacity differences, but this remains a
load/capacity inference, not measured internal-stage attribution. Client gap
stamps include receive batching and scheduling, not GPU-generation timing.
No decomposition or claimed repair of historical6.36ms follows. This result
also does not establish exclusive PCIe causality, equality, arbitrary backend
support, overall resource savings or a general eBPF speed advantage.

No additional baseline, model, profiler or unchanged review/run is necessary
to close this source decision. Optional title-spacing polish in the figure
does not block validity. The remaining useful closure is honest findings/docs publication and
owned-client cleanup; the predeclared source rejection has been applied.
