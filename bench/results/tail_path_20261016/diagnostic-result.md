# Complete diagnostic: submission runqueue delay and client delivery gaps

This is the completed two-pair timestamp diagnostic admitted inplan.md,
not the later confirmatory repair comparison. No serving fix/default or
speedup is selected yet. The original user's throughput/latency goal remains.

## Completion and correctness
Four executors,1024 measured gen64 requests/65536 measured tokens,32 excluded
gen1 warmups,1056 total replies/65568 tokens. Every request succeeds.
Actual graph/head history and independently reconstructed fresh attention
metadata both replay exactly for every executor. All graph/ring errors and logical/timeline/ftrace loss counters
are zero, ownership retires completely, kernel SEND submission/CQ byte ranges
join, all256 client host-TID markers/executor and all336 received bytes/request
reconcile, and all retained full trace CPU buffers report zero overruns/drops.
The legacy128-entry network admission sample reports trace_overflow=136 for
264 admissions, as expected. That sample is truncated; complete joins use
full logical/timeline/ftrace records and client data, not that legacy sample.

The first full prefix is failed for kernel trace overruns, not counted as a
completed pair or dropped from the evidence. It and the bounded buffer/cleanup
repair are retained infailed_full_trace_overrun/ andfull-trace-repair.md.
Successful rerun covers the entire original two-pair diagnostic. Ftrace uses
an owned32768KiB/CPU instance (temporary768MiB across24 CPUs), removed on finish.
No global tracer, other workload, host scheduling or CPU setting changes.

Full sources before the buffer repair are indiagnostic_full_sources/;
actual repaired collection sources are indiagnostic_full_sources_buffer_repair/.
The latter code does not change model/operators/network policy from0065;
it adds private timestamp and tracing observation. The original default8
candidate and its qualification are separately retained. The standalone
scheduler attribution and gzip-aware replay are CPU analysis additions with
the original frozen analyzer retained. No measured sample or oracle changes.

## What is actually located
The instrumented kernel/native ITLP99 is7.278825/4.378572ms inpair0 and
9.918235/5.573179ms inpair1. This preserves the adverse direction twice,
but instrumentation, time and two process blocks prevent replacing0065's
five-block14.72/8.36ms result or allocating its6.36ms difference.

The slowest1% client gaps have GPU production-gap medians1.466/1.378ms in
the two kernel runs; their delivery-age-change medians are8.182/12.078ms.
Thus the large observed gaps are primarily after production in these traces,
rather than slow model rounds. Arrival gaps can exceed marginal P99 and
delivery-age change is signed; these are same-gap identities, not a sum of
marginal stage percentiles.

Descriptive diagnostic quantiles use nearest rank; confirmation retains0065's linear-percentile implementation. Per-token stage P99,each run separately:

| Stage | Kernel pair0 | Kernel pair1 |
|---|---:|---:|
| GPU publication -> send SQE, estimated ms |6.392320|4.722432|
| SQE publication -> kernel submit, estimated ms |3.467520|4.515952|
| Kernel submit -> send completion, ms |0.110000|0.109000|
| Completion -> GPU consumption, estimated ms |0.744680|0.519800|
| Previous GPU progress iteration -> send, ms |1.033216|0.780736|
| Send completion -> client recv exit, ms |8.159000|14.005000|

These rows overlap in time and repeat sends across covered tokens; never add
them or treat16384 correlated tokens as independent process repetitions.
Kernel send completion is not a NIC wire timestamp or receipt by the client.
Receive can precede send completion on local TCP:773/665 kernel-run token
arrivals precede CQ timestamps (min-0.959424/-5.788530ms), and903/785 recv-exit
intervals are nonpositive. Signed residuals remain; CQ is not a mandatory
causal predecessor of receive. Scheduler summaries treat a nonpositive
boundary window as empty, not as measured positive CPU wait.
SQ-to-kernel negative estimates (2275/2245 token associations, min-7.528/
-8.136us) are within the stated alignment bracket, as are native publication-
to-send negatives. They are retained, not clipped out of latency distributions.

The SQ-to-kernel thread's runnable-but-not-running state P99 is2.812/4.439ms,
versus sleeping0.049/0.048ms and running0.124/0.132ms. These are associated
same-thread state intervals, not exclusive service CPU attribution. They
locate a large delay before the creator executes the BPF submission step:
a published GPU SQE cannot submit itself while the creator waits for CPU.
All matched SEND operations have zero io-wq queue events. Other accept/receive
operations do use io-wq; do not claim that the service has no io-wq work.
The actual send execution interval is usually much smaller than the waiting
and client-delivery intervals, with rare maxima retained.

Client receive and scheduling associations separate additional delay:
post-recv-exit to Python arrival-record P99 is1.238/3.294ms in kernel runs
and1.009/1.537ms in native. Kernel completion -> recv exit P99 is8.159/14.005ms;
client runnable state in those intervals has P993.442/4.691ms and sleeping
6.494/11.139ms. Sleeping can mean socket wait or interpreter synchronization;
these traces alone do not allocate it exclusively to TCP/softirq/GIL.
A count of softirq events is not its exclusive service cost.
The complete per-token/syscall/state rows preserve all larger outliers.

The host one-second snapshot has many busyrepl processes in another Pod,
and desktop CPU work. Prior0065 global counters are near24-core busy with
large client scheduling lag. Neither snapshot proves continuous historical
exposure or exclusive cause. The full scheduler timeline establishes actual
thread waiting in the diagnostic, without pausing or reconfiguring others.
The bounded kernel journal read08:21..08:53 returns no selectedNVRM/Xid/GPU/
IOMMU fault line, alongside an endpoint empty GPU process list; this is not
a continuous exclusivity or universal fault-clean claim.

## Clocks and limits
GPU globaltimer and CPU CLOCK_MONOTONIC are never directly subtracted.
Start/end16-sample synchronized calibration brackets have nonempty per-phase
offset intersections. Selected bracket widths yield10.94..12.125us half-width
including1us trace print allowance; endpoint offset changes are2.901..5.293us.
Cross-domain estimates assume affine interpolation across the short serve;
sub-bracket effects remain unresolved. Full joins check causal bounds.
Native same-clock send/syscall and all scheduler durations do not use GPU
alignment. Independent review must assess this actual scope.

Official implementation references:
- https://docs.kernel.org/trace/ftrace.html
- https://github.com/torvalds/linux/blob/v7.3-rc3/include/trace/events/io_uring.h
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.c
- https://docs.nvidia.com/cuda/parallel-thread-execution/#special-registers-globaltimer

## Decision still pending
The demonstrated submission delay is largely CPU runnable waiting, not an
io-wq SEND stall or evidence for model-specific kernel optimization.
The GPU's one-send-in-flight/request also propagates delayed completion into
later token publication-to-send waiting. A transport intervention must target
that actual mechanism or an independently observed avoidable queueing rule,
then pass ordinary8 cancellation/ownership and the planned five-block matched
before/after/native comparison. No arbitrary timer/affinity/priority tuning,
foreign-process termination or unsupported fix is implied by diagnosis.
Resource totals, sustained remote load, official current vLLM server reference,
generic backend validation and ordinary source adoption remain open.
