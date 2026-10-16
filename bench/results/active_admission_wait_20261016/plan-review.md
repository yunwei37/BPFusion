# Independent plan review: active admission wait

2026-10-16 UTC. Fresh PLAN REVIEW under research-experiment-design, before
canonical editing/building/running. Only this file is written.

## Verdict

**Proceed to the planned qualification and real preflight. No scientific or
executability defect found that invalidates this experiment.** This is approval
of an experiment path, not proof that its unrun candidate works or should be
adopted. No additional baseline, workload, operating point, timer sweep or
review round is required for this narrow hypothesis.

The fixed primary is candidate-minus-before owned-group CPU milliseconds per
all attempts. Lower CPU with worse delivery remains a tradeoff; adverse native
comparisons and inconclusive delivery intervals stay visible. The role is
supporting mechanism evidence toward the retained same-compute serving/resource
question, not a new RQ or generic eBPF claim.

## Material examined and admission

Read complete plan, exact before/candidate snapshots, all four prepared build,
server, PowerShell and analysis scripts, actual Make rules, canonical BPF,
io_uring_tcp.h and native epoll code. Archived/temporary Python scripts are
byte-identical at review time; snapshots differ only by may_idle condition,
canonical source still contains before expression, branch is main, unrelated
tools/setup_env.sh remains.

Read findings0060/0066/0072, evaluation and closest-work map; preceding CPU
profile plan/result/fresh review/source context. Spot-checked original full
raw client/resource terminals, perf argv/terminals and self reports: both
11520-attempt streams terminate, profiler exits are intentional -2, lost0 and
period sums20.212424688/4.919839640s remain. This is not a duplicate binary-level
result review of every original sample. Also inspected actual remote client,
resource observer and reused protocol/lifecycle/graph adapters.

Admission holds. Native currently beats the repaired kernel path; sampled
coordination/map concentration leaves its avoidability and this branch's
causal effect unknown. Old idle0060, queue0056, close-scan0066 and aggregate
resource data cannot reconstruct this intervention. Positive, adverse, mixed
and inconclusive effects yield different retention/paper decisions without
answering the whole RQ. This source-grounded discriminator outranks arbitrary
timer sweeps, unchanged repeats and weaker external rows.

## Waiting, publication and shutdown

Checked primary upstream
[loop.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c) and
[bpf-ops.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c).

With may_idle=0 the candidate asks for observed CQ tail plus one even while
admission is unacknowledged. Upstream sleeps only while that target exceeds
current CQ tail; SQ submission occurs before that comparison and can generate
completions. The existing active multishot timer provides another wake.
This plausibly reduces immediate callbacks; it does not prove the effect or
make60us an end-to-end scheduling bound.

Initialization starts the active timer. GPU sets timer_may_idle before
publishing an idle update and tracks successful timeout-update CQ processing.
BPF snapshots mode before SQ tail/submission as before. If the timer may be at
a distant idle deadline and admission is unacknowledged, immediate iteration
is retained. GPU publishes admission_seen after its progress iteration's SQ
publication. A newly submitted timer update also has its own completion wake.

No concrete new lost-wake or shutdown counterexample emerged. Existing
loop-owner signal forwarding, model_quiesced drain, timeout cancellation,
finished publication and EOF references are unchanged. Source reasoning is
not exhaustive proof: planned repeated2.2s idle transitions, reuse, queuedRST,
mid-output stop, protocol and independent dual replay are relevant finite
checks. The known after-submit ordering problem is avoided by preserving its
macro behavior. Generic graph transport checks before adoption are shared-loop
dependencies, not extra paper experiments.

## Baseline, metrics and correctness

Efficient native is the single main competitor: actual epoll_pwait2 uses60us
active waits, socket/deadline idle waits and eventfd shutdown. It is not busy
epoll. Before is a component control with repaired EOF behavior; official
vLLM0069 supplies broader context without answering this branch question.

Same weights/revision, mixed engine,16 slots, four prompts, gen64, network and
frozen gamma schedules support the stated isolation. Normal Make uses nvcc -dc
and embeds the selected BUILD path. Immutable before builds, source receipts
and GPU instruction equality address the prior private-adapter failure;
actual candidate receipts remain to be obtained.

All-attempt normalization and full terminal drain avoid success-only resource
accounting. Five paired blocks support the fixed nominal t95df4 analysis with
small-sample/order/shared-host limits. Same-TGID io-wq is already included once.
An unstable/missing endpoint group makes the primary inconclusive, not zero.
Host/cgroup/device totals remain nested observations.

The primary citation can be more precise without changing the metric:
observer uses process CPU clocks via
[clock_getcpuclockid](https://man7.org/linux/man-pages/man3/clock_getcpuclockid.3.html)
and [clock_gettime](https://man7.org/linux/man-pages/man2/clock_getres.2.html).
The plan's [cgroup CPU documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html#cpu)
defines the separate cgroup ledger, not that primary clock operation.

[vLLM metric documentation](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)
supplies terminology. Actual source-native timestamps define this frontend:
connect TTFT includes connection time; TPOT is first-to-last receive/63;
receive-gapP99 is grouping, not GPU generation intervals. Successful tails
censor failures; throughput/failure/resource rows retain all attempts.
Frozen-set disagreements stay visible and do not establish universal fidelity.
The oracle/pool, protocol checks and60s per-I/O timeout must remain fixed.

## Executability and completion

Normal8/16 commands and concrete runner selectors provide a runnable path in
the original Workspace. The build adapter executes from existing OS TEMP,
where environment.json/runtime live; its archive copy records provenance.
Before/native select reclamation_sourcebuild16; candidate selects its new
normal16 directory. Warmups precede observation;5s idle brackets are separate.
Real preflight uses128 prefix offsets. Full acquisition is15 cells/172800
attempts plus120 excluded checked warmups:15 minutes of arrivals plus idle
brackets, initialization, warmup, drain, qualification and archive.

Client transfer/compression follows server stop and precedes the next cell.
Chunk transfer preserves bytes. Terminal server/pin checks, matrix cardinality,
full raw archives and independent CPU replay form sufficient completion.
Runtime failures stay visible, with affected checks rerun after necessary
execution repairs. The optional separately exposed candidate profile cannot
replace an observer-free primary cell.

One nonblocking output-completeness detail remains: current analysis computes
per-cell TTFT, completionP50/P95/P99, TPOT and scheduling lag, but emits paired
contrasts for only its eight-metric list. The plan promises signed effects/
nominal intervals for other declared secondary rows too. Complete those from
the same retained data with fixed block pairing/t formula before the result
report; no new measurement, metric change or expanded matrix is needed.
Do not silently omit adverse rows. This does not invalidate the fixed primary
or block qualification/preflight.

The citation clarification and secondary output completion are reporting
details, not grounds for another unchanged-plan review. Proceed on the admitted
path and make retention a post-result decision using all observed tradeoffs.

## Same-review completion note

Before execution, the owner completed both nonblocking details. I inspected
the revised analysis: connect TTFT/completion, TPOT and scheduling-lag mean/
P50/P95/P99 contrasts use the same existing block formula and keep the one CPU
primary. The plan now cites the actual process CPU-clock interface separately
from cgroup accounting. Concrete kernel-only default8 protocol and loop
lifecycle adapters are archived. These complete the same admitted path;
verdict remains proceed, with no unresolved blocking issue. No new review
round or scientific change is implied.
