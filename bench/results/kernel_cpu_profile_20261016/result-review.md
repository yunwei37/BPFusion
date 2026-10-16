# Independent result review: original creator-CPU profile

2026-10-16 UTC. One fresh RESULT REVIEW under research-experiment-design.
This review covers the frozen original preflight/full diagnostic acquisition,
not any subsequent waiting-policy candidate. Only this review file is written;
no source, runtime, GPU, Job or Git publication action is taken.

## Separate judgments

- **run status: valid** for the declared creator-TID kernel-CPU diagnosis.
- **tested hypothesis: supported** for concentration of the sampled creator's
  CPU in loop coordination/admission-map work rather than predominantly actual
  socket/network processing. The stronger word **avoidable**, a causal effect
  of `admitted!=admission_seen`, and any improvement from changing that branch
  remain **inconclusive**: there is no intervention in this acquisition.
- **research value: supporting**. This supplies the missing current-source
  instruction/callchain discriminator; it is neither a headline serving result
  nor another infrastructure-readiness receipt.
- **paper impact: mechanism or workload boundary**. It localizes a tested
  implementation's remaining cost, without a direct thesis challenge or an
  answer to the whole retained RQ.
- **next paper decision:** prioritize a source-grounded coordination/waiting
  discriminator if it remains the highest-value next work. Retain efficient
  native as the main same-compute competitor and the prior adverse resource
  result. Do not adopt a change or assert a serving advantage from profiling.

The retained question is whether removing the steady userspace request worker
improves real delivery/resources with reused matched model computation. No
formal RQ/thesis contract is invented or renamed. This profile alone cannot
establish that broad benefit.

## Required correction to the result report

Correct the collection chronology. `run_cpu_profile.ps1` stops perf, observer
and server, then transfers that cell's warmup/client raw data before starting
the next cell. Its call to `cpu_profile_archive.py` occurs **after the whole
native/kernel foreach loop**, and that adapter performs the large perf decode
and durable repository archive. Therefore the result sentence saying the
large decode/archive ran "before the next cell" is inaccurate. Describe
per-cell post-stop client transfer and final post-both-cells decode/archive
separately. This does not invalidate sampling or require rerunning: those
operations did not overlap a measured server. Raw data existed in the original
Workspace temp directory before final archival. No scientific correction,
extra baseline, new repetition or instrumentation replacement is required.

## Material inspected and independent replay

Read plan.md, all plan-review discussion, preflight.md, result.md,
source-context.md, record/archive/server/launcher scripts, profile_summary.py,
both original and count-adapted analyses, remote client, resource observer,
package metadata, all raw full/preflight client/resource/warmup streams,
server/perf/decode terminal receipts, perf self/inclusive/header/dump/script
artifacts and gzip-native perf.data. Also read the ordinary-source build argv,
logs, SASS equality and lifecycle integration receipts from
`../connection_reclamation_20261016/source_integration/`, current evaluation
history and the captured original source snapshots.

Both serving analyses execute successfully against the archived raw paths and
reproduce analysis.stdout byte-for-byte with empty stderr. The only analysis
changes are 32-to-128 preflight count, exact two-cell matrix validation and
removal of the old five-block interval computation. Metric and outcome logic
is unchanged. Independently computed client quantiles, delivered tokens,
durations and endpoint group CPU agree with the report. Profile-summary
objects reproduce semantically, including every symbol/period/category. Byte
order among equal-weight inclusive symbols can vary because the script uses
a Python set; that does not change any value or reported claim.

I independently parsed the decompressed native perf.data record headers and
sample payloads, rather than trusting only perf's decoded summary. All four
files have valid PERFILE2 data extents. Binary sample counts, sole target
PID/TID, periods and raw callchain record sizes agree with decoded scripts.
There are no PERF_RECORD_LOST, LOST_SAMPLES, THROTTLE or UNTHROTTLE records in
these data sections. The standard reports independently report lost samples0.
Zero observed loss is not proof against all sampling bias.

## Completion, correctness and deviations

Full acquisition contains exactly two planned cells, native then kernel,
11520 attempts each; all23040 succeed and produce1474560 measured tokens.
All indices and full frozen offsets are retained, ending at60000000000ns.
Each cell has eight excluded, successful, exact-reference gen1 warmups. The
single real preflight contains128 attempts per path, all256 successful, plus
its own eight warmups per path. Its offsets are the same128-element prefix.
No failed, partial, replaced, excluded or timed-out measured request appears.
Acquisition checks fixed HTTP status/length, exact output count and vocabulary;
raw response headers show HTTP200 and Content-Length256 for the measured
64-token outputs. The60s per-I/O timeout, full asynchronous drain and original
finite-reference oracle were preserved.

The finite-set mismatch flag remains visible: full kernel21 and native2;
preflight kernel0 and native1. These successes establish protocol-valid
outputs, not full-run exact numerical parity. The oracle is a preexisting
frozen reference pool and was not enlarged to match these results. Earlier
source qualification is complementary evidence, not permission to count
these23 disagreements as verified-equal outputs.

Both full server processes exit0, graph_error0, admitted=retired=11528;
native pending queue at stop0, kernel queued0/reserved0, insertion failures0,
first insertion errno0, detach0 and final owned pins empty. Profiler children
receive the recorded intentional post-drain SIGINT and return-2 after flushing;
they are not mislabeled successful exit0. All ten full decode commands and
both full clients exit0; the same preflight terminals are present. Decoder
stderr is empty; missing optional tips.txt is not a decode failure.
The disposable client Job's retained ownership/cleanup is explicitly deferred
to the ensuing bounded qualification; profile acquisition is complete, while
that broader lifecycle is not yet closed.

No unrecorded scientific deviation or affected comparison requiring a rerun
was found. Final archival timing differs from the prose as described above.

## Primary metric audit

Official perf6.12.95 records cpu-clock:k, requested499Hz, --tid actual creator,
--no-inherit and callchains. Header sample_type explicitly includes PERIOD.
The running kernel is7.3.0-070300rc3-generic; fp is the userspace unwind mode,
not a claim that the kernel was built with frame pointers.

| Raw quantity | Kernel | Native |
|---|---:|---:|
|Full binary/decoded samples|10086|2455|
|Sole creator PID/TID|765351|764893|
|Every observed sample period ns|2004008|2004008|
|Sum of observed periods s|20.212424688|4.919839640|
|Unknown kernel leaf samples|144|1|
|At least one unknown kernel frame|9404|1|
|Decoded kernel depth range|7--84|2--76|

Preflight binary counts are41 kernel/24 native, also with2004008ns periods and
correct sole creator targets. The totals are sampled on-CPU context, not exact
CPU accounting or elapsed request time. Independently observed creator
system-time deltas20.24s kernel/5.21s native have different resource brackets;
they corroborate scope but must not be equated with perf period sums.

All mutually exclusive descriptive categories reproduce:

|Category|Kernel samples / fraction|Native samples / fraction|
|---|---:|---:|
|Loop coordination, other|4419 /43.8132%|0 /0%|
|BPF map without observed socket ancestor|2727 /27.0375%|0 /0%|
|Socket/network/softirq ancestor|2693 /26.7004%|2075 /84.5214%|
|Scheduler without observed socket ancestor|103 /1.0212%|135 /5.4990%|
|Unknown leaf|144 /1.4277%|1 /0.0407%|
|Other kernel|0 /0%|244 /9.9389%|

Thus7146/10086=70.8507% is a valid summary **under the disclosed observed-stack
classifier**. It is not70.8507% pure spin, proven unnecessary work, complete
causal ancestry, all service CPU or client latency. Unknown leaves take
precedence and are not silently allocated; actual network ancestors take
precedence over loop callers. BPF-map work can be required admission work.
Unknown frames in93.2382% of kernel samples materially limit complete ancestry
claims even though named leaves are useful. The result already states this
limitation and retains raw frames.

Independent leaf counts verify __queue_map_get2668, ktime_get_mono_fast_ns1470,
__bpf_prog_exit_sleepable924, __bpf_prog_enter_sleepable715, own
uring_loop_step668 and nft_do_chain524; their reported26.45/14.57/9.16/7.09/
6.62/5.20% are correctly rounded. Inclusive totals overlap and are not added.
No figure or number in the report partitions an earlier marginal6.36ms P99.

## Independent baseline and source audit

The sole main comparison is the efficient native C++ epoll_pwait2 path, not
busy epoll and not the broken global-reclamation variant. Its raw log confirms
active60000ns waits, socket/deadline idle waits, eventfd shutdown and eligible
FIFO admission; all11528 warmup+measured admissions complete. It successfully
engages the intended alternative mechanism. Its sampled sendmsg/TCP stacks
and ordinary Make16 BF_USER_NETWORK/BF_USER_NETWORK_WAIT flags corroborate it.
No avoidable baseline interface failure is counted as a kernel benefit.

Both modes use the same recorded Qwen snapshot,16 banks,64 generated tokens,
four frozen prompts, full arrival offsets, model executor/scheduler and
source snapshots. All seven captured code/header snapshots match canonical
7495930 byte-for-byte; native and kernel snapshots are identical to each
other. Preflight artifact HEADc09cd42 and full HEAD8a10829 reflect subsequent
record commits, not source substitution. Ordinary build receipts include
nvcc -dc and the actual normal transport-specific flags, avoiding the prior
private-adapter build failure. These existing source/build receipts support
matched computation; they do not remove finite-reference disagreements or
turn this into a fidelity experiment.

An external vLLM rerun would not identify the current dominant creator's
instructions. The repaired current source has changed since the old profile,
and prior aggregate CPU records cannot reconstruct these callchains. This
profile is nonredundant supporting evidence for choosing the next mechanism
discriminator. No extra baseline or workload is necessary for this narrow role.

## Serving context, uncertainty and source interpretation

Independent raw replay confirms kernel/native, respectively:
11633.294880/11658.727921token/s over actual full-drain durations
63.376713787/63.238460062s; connect-begin-to-last-receive P99
3409.273341/3297.491485ms; client receive token-gapP99
3.756343/4.057193ms; endpoint owned-group CPU1.820360/0.784433ms per attempt.
These are the report's rounded numbers. Scheduling-lagP99 is8.155845/
10.019097ms and resource brackets70.840431/72.331987s. The observer itself
consumes0.405724/0.412307ms per attempt. Whole host/device/Workspace totals
include other work, and nested ledgers are not added; owned io-wq is not added
again to process group CPU. A creator-only profile cannot make an all-worker
or exclusive-host cost claim.

One ordered profiled pair has no replication-based uncertainty estimate or
counterbalanced order. There is no unprofiled overhead control, and perf's
cost can differ with the sampled path. Remote client receive grouping,
client scheduling, shared work, timing brackets and control/observer exposure
limit tails and resource comparisons. Lower kernel token-gapP99 here does not
overrule the opposite sign in earlier five-block evidence. No superiority,
equivalence, rare-failure reliability or model-quality claim follows.

The frozen source and upstream kernel semantics support a plausible next
causal discriminator. The own loop requests current CQ when admitted differs
from admission_seen; upstream subtracts CQ tail and schedules only when the
remaining target is positive. Submission itself can execute socket work
synchronously. I checked the primary upstream
[loop implementation](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c)
and [BPF submission implementation](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c).
This explains why observed clock/BPF enter/exit/queue leaves warrant inspecting
coordination, and why a __io_run_loop ancestor cannot mean pure waiting. It
still does not identify a sampled branch, measure admission-ack waiting, or
prove that relaxing waits preserves idle wakes, shutdown and correctness.
Those are intervention questions outside this reviewed original acquisition.

The appropriate paper treatment is a narrow mechanism localization that
motivates subsequent matched work, preserving the adverse native comparison
and all stated fidelity/observer limits. The single required report correction
is documentary chronology; this review does not authorize additional runs or
source adoption.
