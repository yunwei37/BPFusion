# Independent result review: active admission wait

2026-10-16 UTC. Fresh RESULT REVIEW under research-experiment-design.
Only this report is written. The ordinary fifteen-cell matrix and its one
separately planned post-matrix candidate perf context are complete. The
profiled context remains separate from the unprofiled primary estimate.

## Judgments on the completed primary matrix

- Run status: **valid** for the declared finite remote workload and measured scopes.
- Tested hypothesis: **supported** for lower owned process-group CPU per all
  attempts, candidate versus before. Delivery improvement is **inconclusive**
  versus before; candidate throughput/completion P99 remain **adverse** versus
  the main native epoll competitor.
- Research value: **supporting** mechanism evidence, not a new headline
  throughput result or a dependency-only readiness check.
- Paper impact: **additional RQ evidence / mechanism and workload boundary**.
  This bounds coordination cost in the retained same-compute serving question;
  it does not directly challenge or establish the whole thesis.
- Next decision: retain the measured CPU repair if the engineering owner accepts
  its stated scope and preserves the adverse native rows. Keep native as the
  main causal competitor. No unchanged rerun, new baseline, timer sweep or
  expanded model matrix is scientifically required to trust this result.

No concrete scientific-validity blocker was found in the primary run. Source
adoption, documentation and cleanup are the owner's separate delivery steps;
the source was still a one-line WIP when examined.

## Independent raw arithmetic and completion audit

Read plan, plan review, qualification, preflight, result, reproduce, runner,
server/analysis/plot sources, relevant resource/client sources, canonical BPF,
GPU I/O progress and native epoll wait source. I did not rely only on the
provided analyzer or its replay assertion.

I independently decoded every main client/resource archive with separate
arithmetic and compared 345 per-cell scalar values, then recomputed every
one of the **46 paired effects and nominal t(df=4) intervals**. All match the
published analysis within numerical precision. The independent calculation
uses the original client timestamps, all-attempt CPU/resource denominators,
linear quantiles and five paired block differences.

All fifteen streams contain exactly indices0..11519, all successful with
64 in-range token IDs and monotone receive stamps. There are **172800
successes, 11059200 measured tokens, zero transport/protocol/close failures**,
plus120 checked, excluded, one-token warmups. The same frozen config and
client source occur in all fifteen cells. Each block's complete arrival
offset list is identical across its three conditions; request prompt and
schedule assignments match. No cross-host clock subtraction is performed.

The five rotating process orders match the plan. All fifteen server terminal
receipts exit0 with empty pin lists; each process finishes before the next
starts. Kernel terminals show11528 admissions/completions including warmups,
empty pending/reserved, drained SQ/CQ, no dropped/overflow/error and model
graph_error0. Their128-entry diagnostic reply record truncates as expected
(trace_overflow11400); this is not complete per-token execution tracing and
is not represented as such. Native logs confirm actual epoll_pwait2,60us
active waits, deadline/socket idle waiting, eventfd shutdown and11528
admissions/retirements. Native did not fail to engage its intended mechanism.

The acquisition/replay analysis outputs are byte-identical and both stderr
files are empty. I also reran both default-eight protocol archive analyses:
both exit0 and match their archived replay bytes with empty stderr.

## Numerical conclusions

Condition means (before / candidate / native) are:

| Metric | Before | Candidate | Native |
|---|---:|---:|---:|
| owned group CPU ms/attempt |1.701533854|0.625738952|0.769310595|
| delivered tokens/s |11625.993483|11626.456625|11646.715245|
| connect completion P99 ms |3395.012682|3394.068796|3295.820195|
| connect TTFT P99 ms |3309.362226|3308.568885|3211.721535|
| client receive-gap P99 ms |4.370018774|3.993355600|4.288793310|

The fixed primary candidate-minus-before CPU effect is
**-1.075794902ms/attempt,95% nominal interval[-1.222796781,-0.928793023]**.
Candidate-minus-native CPU is
**-0.143571643[-0.182094255,-0.105049030]**.
The reported63.22% and18.66% reductions are ratios of these condition means,
not confidence bounds or exclusive-host savings.

Candidate-minus-before TPS is+0.463142062[-8.973088629,9.899372752];
completion P99 is-0.943885998ms[-44.277690293,42.389918297];
receive-gap P99 is-0.376663174ms[-1.216713639,0.463387291].
These do not prove speed improvement, equality or noninferiority.

Candidate-minus-native TPS is **-20.258619989[-30.272903313,-10.244336665]**;
completion P99 is **+98.248600860ms[48.699983495,147.797218225]**;
TTFT P99 is+96.847350804ms[47.583732969,146.110968639].
Those adverse rows must accompany any CPU-efficiency conclusion.
Candidate-minus-native receive-gap P99 remains inconclusive:
-0.295437710ms[-0.669311659,0.078436239].

All declared mean/P50/P95/P99 TTFT, completion, TPOT and scheduling-lag
contrasts are present, not just favorable selected tails. There is one
predeclared primary; intervals for other contrasts are nominal and not
multiplicity-adjusted. Five paired blocks, fixed nonrandom rotating order
and shared-host temporal variation limit generalization. Zero observed
failures is finite evidence, not a rare-failure guarantee.

The load requests12288 output tokens/s, exceeding measured delivered TPS.
The backlog and roughly3.3s request P99 are compatible with accumulating
queueing near saturation. This is an inference, not a measured partition of
every queue stage. Client receive-gap quantiles contain coalescing and client
scheduling, and cannot be relabeled GPU-generation ITL.

## Correctness, sources and competing baseline

All fifteen actual source receipts match for model source, both network
headers, shared queue, fusion BPF and admission header. The intended loop
snapshots differ by exactly the may_idle conjunction and canonical source
matches candidate. Artifact HEAD is correctly distinguished from source
adoption.

I independently ran cuobjdump on the immutable before and normal candidate
libraries: both transports' GPU SASS streams are equal at8 and16 slots
(all four comparisons). I independently compared llvm-objdump -dr output:
fusion instructions/relocations equal at8/16; intended loop objects differ.
All four before/candidate loop libraries contain their own expected absolute
BPF-object BUILD binding. Normal Make receipts exit0 and preserve nvcc -dc;
there is no private source-rewrite build adapter. This addresses source/build
fairness without assuming that artifact HEAD alone proves a binary.

Native is an appropriate main competitor for this intervention: efficient
C++ epoll with the same resident model computation, weights, offered arrivals,
slots and socket option. Before is a component ablation/control. Different
network ownership can alter batching/release timing, so same code does not
imply identical dynamic batches; the reported arithmetic does not claim that.
Official vLLM remains the separate whole-service reference already recorded
in0069, with its broader differences; no extra rerun is needed for this branch
hypothesis.

Finite reference-pool disagreements are correctly retained:
before296,candidate223,native233,**752 total**. I independently checked each
flag against its frozen sequence pool. These are successful protocol responses
but not exact full-run model-fidelity proof. No pool was expanded from these
outputs, no timeout changed, and no mismatch was silently excluded.

Default-eight Qwen/Smol protocol qualification has640 outcomes each,
259 intended rejects each, actual batches1..8 and23376 exactly replayed
tokens each. Reader-only gzip changes between acquisition/archive analyzers
do not alter their arithmetic or oracle. Ordinary lifecycle records each
have144 outcomes, exit0, model_errors[0], empty remaining pins:
Qwen877 checked tokens/163 partial, Smol925/211 partial, each47 explicitly
unobserved cancellations. Partial and unobserved cancellation cases are
honestly bounded and are not treated as completed-token fidelity evidence.

The four ordinary graph records each have182 checks and pass. The analytic
cuBLAS8x8 matmul and length32 complex FFT oracles are computed independently
of the server output; invalid framing/reuse/half-close/reset/stop checks are
retained. This is useful finite shared-loop qualification, not arbitrary
backend stability or arbitrary model support.

## Wait semantics and engineering risk

Checked the actual source against primary upstream
[loop.c](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/io_uring/loop.c)
and [bpf-ops.c](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/io_uring/bpf-ops.c).
Upstream checks the requested CQ index after the BPF callback and SQ
submission, sleeping when the requested index exceeds current CQ tail,
subject to pending work/check_cq rechecks. The active candidate requests a
next CQ event despite unacknowledged admission, avoiding the previous
forced immediate iteration. Existing60us multishot timer remains a wake
source;60us is not a bound on service scheduling latency.

Idle-mode immediate admission handling remains. GPU marks possible idle
timer state before SQ publication and confirms mode on timeout-update CQ
processing; admission acknowledgment follows its progress iteration.
The BPF snapshot-before-SQ ordering and stop/quiescence handling are
unchanged. I found no concrete new lost-wakeup or shutdown counterexample.
Source reasoning plus repeated finite idle/cancel/protocol checks is adequate
for this narrow repair; it is not exhaustive concurrency proof.

## Resources, exposure and scope

The primary uses process CPU clocks for owned group members; endpoint
identity checks pass. I additionally checked every recorded sample: process
group membership remains stable within each cell. Visible io-wq thread status
has the creator's TGID in all kernel cells; their time is included once in
that process clock. Their separately displayed thread scheduler runtime must
not be added again.

Host IRQ/softirq, cgroup, observer CPU and device energy remain nested or
shared context, not exclusive service attribution. The observer itself is
outside the service group and separately recorded. Loaded-idle brackets are
separate from active resource accounting. Shared host/device totals do not
prove whole-machine or energy savings; their reported paired intervals are
inconclusive. Unseen workers and asynchronous activity outside the group
remain a limitation of the primary scope.

Runner chronology puts client compression/transfer and per-cell archive work
after the server stops and before the next cell, with large aggregate
analysis/plotting after the matrix. It does not overlap those operations with
its own measured server. Source/build/model qualification precedes acquisition.
The retained foreign work is acknowledged; the experiment does not claim an
exclusive host or device, randomized scheduling, or a production SLO.

The supplied three-panel figure uses all fifteen cells, individual block
points/paired lines and condition means. I inspected the rendered PNG; labels,
units, values and visible adverse native TPS are consistent. Its receive-gap
mean does not override the inconclusive paired interval. The numeric table
retains adverse completion P99 even though that metric is not a plot panel.

## Independently audited post-matrix profile context

The separately planned diagnostic is terminal, using the same normal
candidate16 build and same block0 workload. I independently decoded the raw
PERFILE2 binary headers and every data record, then cross-checked script
samples and the classifier counts. The binary contains3427 SAMPLE records,
creator PID/TID777745 only, each period2004008ns, period sum
**6.867735416s**. There are **no LOST, LOST_SAMPLES, THROTTLE or UNTHROTTLE
records**. This establishes the retained capture's loss accounting, not absence
of sampling or unwinder bias. All five standard decode receipts exit0 with
empty stderr. The record exit-2 is the planned post-drain SIGINT and normal
capture stderr, not an unreported serving failure.

The independently parsed mutually exclusive categories are:
socket/network/softirq2752(80.303472%), loop coordination469(13.685439%),
scheduler171(4.989787%), BPF maps without observed socket ancestor32(0.933761%),
unknown leaf3(0.087540%). Their counts sum to3427. At least one unknown kernel
frame occurs in2896 samples(84.505398%); unresolved ancestors remain in every
fraction's denominator. Network ancestry can include unrelated packet work
in creator context; no category is exhaustive exclusive branch attribution.

The old0073 capture has10086 samples,7146 coordination/maps samples
(70.850684%),20.212424688s period sum and2693 network/softirq samples.
Candidate has501 coordination/maps samples(14.619200%) and2752 network/softirq
samples. That descriptive shift is consistent with removal of redundant
coordination. It is **not** a contemporaneous paired profile, a confidence
interval for branch cycles, a new speed estimate or additive allocation of
historical client-tail latency. Kernel unwinding controls kernel frames;
the userspace fp option does not force kernel frame-pointer unwinding.

I separately checked the diagnostic raw serving stream:11520 complete
requests/737280 tokens,26 retained frozen-pool disagreements, terminal0,
source snapshot matches the intended candidate, no pins/graph or ring errors.
Independent raw arithmetic gives group CPU0.668507358ms/attempt,
TPS11621.261864, completionP993462.194977ms and receive-gapP993.960040ms.
Serving archive replay is byte-identical. These numbers are context under
profiling exposure, not replacements for any of the fifteen main cells.

The diagnostic followed terminal publication, checked warmup, profile start,
client drain, intentional profile stop, observer/server stop, then transfer and
offline decode/archive. This reviewer paused heavy replay/decompression while
the diagnostic ran. No new oracle, timeout or selected favorable replacement
was introduced. profile.md accurately preserves all these limits.

## Scope audit and remaining delivery

Production scope is one BPF condition, with no new timer flag, ABI, model math,
dispatcher, persistent helper or configuration layer. Normal builds,
acquisition scripts and raw archives are necessary experiment material rather
than runtime scaffolding or independent scientific contributions. In the
reviewed change I found no project-authored promotion/control interface or
new persistent infrastructure. The existing disposable remote client remains
a bounded experiment resource and must be removed on closure as planned.

The old14.72 versus8.36ms token-gap P99 was not reproduced by later matched
controls even before this edit. This result neither allocates that historical
6.36ms additively among stages nor proves that exact tail regression fixed.
Shared NODELAY, per-peer EOF repair, this CPU coordination repair and mixed
GPU scheduling are separate mechanisms. Report the direct intervention result
and remaining native speed advantage plainly.

No scientific repair or additional measurement is required for this completed
run. The optional diagnostic is incorporated without changing the primary
judgments or promoting its profiled cell into the performance estimate. This
same result review is now complete. Source retention and clean commit/push/
temporary Job cleanup remain the owner's tasks.
