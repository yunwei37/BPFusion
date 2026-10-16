# Independent result review: two-pair streaming-tail diagnostic

Review observed 2026-10-16 UTC in the original bpfusion-dev Workspace. Scope:
the completed timestamp diagnostic, not the later repair comparison, ordinary
source adoption, complete resource accounting, remote-load evaluation or
external official-server reference. No serving source, model, GPU execution,
host setting or another owner's work was changed by this review.

## Verdict, hypothesis and decision

**Valid supporting diagnostic; the overall repair/confirmation task remains
incomplete.** Both planned pairs complete with usable full timeline coverage
and exact recorded replay. The evidence locates substantial delay after GPU
token production, including creator-thread runnable waiting before submission
and client receive/scheduling delay. It contradicts an explanation consisting
primarily of slow model rounds or io-wq execution of these SEND operations.

It does not allocate the historical6.359661 ms difference into exclusive
components, prove exclusive CPU/softirq cost, establish a production speedup,
or identify a fully tested transport repair. The instrumented adverse direction
persists twice; its magnitude is not a new estimate replacing0065. No source
fix or default adoption should be inferred from this review.

This is useful new mechanism evidence for the user's existing service-latency
objective. The largest uncertainty is now avoidable queue/progress work and
submission scheduling, plus the local client's observation boundary. It is
reasonable to inspect and test a concrete implementation defect there. An
unchanged resource-only run or model-specific arithmetic optimization would
not answer this newly located uncertainty.

## Independent audit performed

I read plan.md, plan-review.md, diagnostic-result.md, the preflight deviations,
the initial and repaired full source freezes, full-trace-repair.md, failed and
successful collection artifacts, host exposure and bounded journal snapshots,
and both analysis implementations. I opened the primary
[NVIDIA globaltimer documentation](https://docs.nvidia.com/cuda/parallel-thread-execution/#special-registers-globaltimer),
[Linux ftrace documentation](https://docs.kernel.org/trace/ftrace.html) and
[the declared kernel io_uring tracepoint definitions](https://github.com/torvalds/linux/blob/v7.3-rc3/include/trace/events/io_uring.h)
to check the observation boundaries.

Both published CPU analyses were rerun from lossless compressed archived
inputs in an owned /tmp directory. The regenerated timeline and scheduler
analysis JSONs exactly equal their archived counterparts. This includes all
four executors, not a selected favorable subset. Separately from those
analyzers, I recomputed all four nearest-rank ITL P99s from raw client arrivals,
reconstructed all264 request histories per executor from admission/compute/
release events, checked physical slot ownership and complete retirement,
matched every client reply to its reference, matched every compute row to the
fresh-metadata sidecar, and checked all eight calibration intersections.

Raw metadata's driver, client, independent replay and four instrumented source
strings exactly match diagnostic_full_sources_buffer_repair/. The live private
diagnostic source files match that freeze, and both actual launchers resolve
to the frozen mixed Python bootstrap. The frozen CUDA diff against0065 adds
observation only; the network diffs add timestamp records without changing
send/close policy or model arithmetic. Actual collection commands, pinned
Qwen revision, precision, slot count and environment are preserved. Small
actual compiler logs still present in the owned collection temp should be
archived before its eventual cleanup; no new execution is needed.

The independent reviewer did not rerun GPU numerical inference. Numerical
oracle evidence is the preserved successful captured replay and separate
source-native fresh-attention-metadata replay, whose source and complete
sidecars were audited rather than replacing them with client self-consistency.

## Completion, loss and ownership

The fixed four-executor order is loop/native, then native/loop, with256
measured gen64 requests and8 excluded gen1 warmups each. All1024 measured
attempts succeed, producing65536 measured tokens; total1056 successful replies
produce65568 tokens. There are no request-error/invalid outcomes to exclude.
Every executor has264 fully retired histories, zero logical graph/trace
overflow, and exact history/fresh-metadata correspondence. The full actual
batch ranges are retained rather than assuming identical trajectories.

The loop counters have accepted==closed==257, completed==head==264, empty
SQ/CQ, no pending/reserved/dropped/ring overflow, and no error. Both loop
RESULT records also have **trace_overflow=136** in the legacy128-record
admission sample. This is expected truncation of that separate diagnostic
sample, not loss of the complete logical/timeline/ftrace evidence. Therefore
the report's phrase "all trace errors are zero" must explicitly distinguish
these channels and retain the nonzero legacy field. It is not a correctness
failure under the declared, unchanged checker.

All96 successful per-CPU ftrace statistics have zero overrun, commit overrun
and dropped events; reader_error is null and all final entries counts are
zero. The retained failed prefix really has overwritten kernel events and is
properly excluded from complete decomposition, with its raw output and failure
preserved. The bounded private-instance buffer increase and cleanup exception
repair do not change the model, workload or oracle. Rerunning the entire
two-pair diagnostic after that instrumentation repair is appropriate.

Measured loop token byte joins cover15563 and15253 distinct SEND operations,
respectively. All have matched submission/completion identities and exact CQ
results, with zero associated io-wq queue events. Reused tags are paired in
order under the audited one-outstanding-send/request rule; they are not
mistaken for globally unique tags. All256 client markers per executor bind
host TID, fd and request; successful recv byte ranges reconcile each measured
80-byte HTTP header plus256-byte token body. Warmup replies have a different
shorter Content-Length header and are outside this336-byte assertion.

## Numbers and causal interpretation

All numerical values proposed in diagnostic-result.md reproduce at the stated
precision, including the two tail-subset medians, every stage-table P99,
creator/client scheduler-state P99s, post-recv Python timing, calibration
widths and offset changes. The directly recomputed ITL P99s are:

| Pair | Kernel loop, ms | Native, ms |
|---|---:|---:|
| 0 |7.278825|4.378572|
| 1 |9.918235|5.573179|

For the slowest1% of actual adjacent client gaps, kernel production-gap medians
are1.466240/1.378464 ms, versus signed delivery-age-change medians
8.181769/12.077832 ms. These are same-gap observations. They support the
post-production location in this diagnostic without adding marginal P99s.

SQ-to-kernel delay P99 is3.467520/4.515952 ms. In that same creator thread,
runnable-but-not-running state P99 is2.811728/4.438768 ms; running is
0.124/0.132 ms and sleeping0.048728/0.048408 ms. All reconstructed positive
intervals have zero unknown-state duration. These are associated thread
states, not exclusive service CPU work. They establish actual runqueue waiting
in the diagnostic; the earlier one-second host snapshot cannot by itself
identify its continuous cause. Rare sleeping/running maxima remain visible.

Kernel submit-to-complete P99 is0.110/0.109 ms, with a retained5.809 ms maximum
in pair1. This is not a NIC or receipt boundary. In fact,773/665 token
associations have client arrival before SEND completion, with signed residual
minima -0.959424/-5.788530 ms;903/785 completion-to-recv-exit intervals are
nonpositive. Local receive before send completion is valid. The signed raw
values are preserved, and nonpositive state intervals are explicitly labeled.
The report should make this ordering caveat explicit: send completion is not
a mandatory causal predecessor of the receive event, so these stages cannot
be interpreted as one universally serial additive path.

The reported positive completion-to-recv-exit P99s8.159/14.005 ms and client
runnable/sleeping associations are reproducible. Sleeping does not distinguish
socket wait, interpreter synchronization or other blocking without further
evidence. Softirq event counts/temporal overlap cannot assign an exclusive
service contribution. Zero io-wq queue events for matched SEND operations
does not mean the service does no io-wq work; accept/receive uses remain.

## Clock scope

Every start/end calibration phase has16 samples and a nonempty offset-bracket
intersection. Selected full bracket widths are18.233..22.250 us across runs;
the maximum endpoint half-width plus1 us trace-print allowance is
10.940..12.125 us. Midpoint endpoint changes2.901..5.2925 us reproduce.
Affine interpolation across the short serve is a disclosed assumption, not
continuous proof of GPU/host synchronization or of bounded within-run drift.

There are2275/2245 negative SQ-to-kernel estimates, minima -7.528/-8.136 us;
all are within the declared alignment uncertainty. Native publication-to-send
negatives also remain within that uncertainty. Timestamps are taken after
publication/SQE submission, so sub-bracket sign reversals are unresolved
rather than impossible event orderings. Same-GPU differences and host
scheduler/syscall differences avoid cross-clock alignment. Float arithmetic
at the large timer epoch has sub-microsecond granularity and cannot justify
the displayed sub-microsecond precision as measurement accuracy. The stated
millisecond-scale diagnosis is much larger than these bounds.

## Next decision and impact

No data-supported claim of a completed latency repair exists yet. The source's
one-send-in-flight rule explains how delayed completion consumption can hold
later bytes; it is a mechanism observation, not proof that permitting multiple
in-flight sends is safe or beneficial. Likewise, repeated mapped-host loads
inside per-connection close checks and globally retained completed connections
are concrete source-level candidates for avoidable progress work, but their
contribution is not measured by this completed freeze.

A targeted change preserving ownership, byte ordering, cancellation and model
computation can proceed through ordinary/default8 acceptance and the already
planned same-computation before/after/native five-block confirmation after the
plan reviewer's focused follow-up on the actual diff. No arbitrary affinity,
priority, timer tuning, foreign-workload termination, new model optimization
or broader baseline matrix is required by this diagnostic review. If a
correct intervention does not improve the finite matched result, retain that
outcome rather than manufacture a transport win.

The historical adverse6.36 ms result remains the performance evidence;
diagnostic evidence now narrows what should be repaired or ruled out. Complete
resource cost, sustained remote-load tails, official vLLM whole-service
reference and generic backend integration remain authorized open work after
the user's prioritized diagnosis/repair stage.
