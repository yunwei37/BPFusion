# Fresh result review: sustained remote delivery and observable resources

2026-10-16 UTC. Independent review of the admitted plan and plan review,
collection notes, actual client/server/observer/orchestration code, frozen
arrival arrays, preflight, static CUDA resource reports, actual client placement,
and the complete authoritative TEMP/remote_full data. No load or GPU run,
source change, client Job mutation or Git action was performed. This reviewer
writes only this file. The repository has no formal paper RQ; the retained
question is whether removing the steady userspace network worker improves
remote delivery or resources with the same resident real-model executor.

## Separate judgments

- Run status: **valid completed observations**, including the serving failures.
  This is a failure-retaining instrumented comparison of this source and these
  two operating points, not a successful reliability qualification.
- Tested hypothesis: **contradicted at 192 requests/s for a performance/resource
  advantage of the current kernel implementation**. At 96 requests/s latency
  and whole-host resource contrasts are inconclusive; process-group CPU is
  adverse to kernel. Exclusive total service CPU/energy saving remains
  inconclusive because host/device attribution is incomplete.
- Research value: **supporting**. This adds sustained different-node failure
  and cost behavior absent from earlier short local and finite remote runs.
- Paper impact: **additional RQ evidence and a source/workload boundary**.
  Neither all eBPF architectures nor a formal thesis is falsified.
- Next paper decision: retain and publish this adverse matrix unchanged. Do not
  claim a useful kernel operating range or total-resource saving from it.
  Investigating the observed admission/insertion/lifetime failure is the
  relevant next causal discriminator. This review does not authorize source
  changes, prescribe a capacity increase, or declare its cause proved.

## Completion, source and baseline engagement

All 10 servers, 20 planned cells and 172800 measured attempts are represented,
with exactly 5760 or 11520 distinct indexed requests per cell. All 80 separate
gen1 warmups succeed and match their frozen finite references. All client
executions terminate with exit0; exit0 describes collection completion and
does not erase failed requests.

Both transports use Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775,
FP16, 16 model slots, the same four prompts and gen64 budget. All ten embedded
server/network source receipts are identical to the selected source; git shows
no executor/BPF/Makefile delta between selected2c0cf7b and acquisition HEAD6a6ac6e.
Both source listeners set checked TCP_NODELAY. Ordinary, non-BF_TRACE builds
and the model scheduler are engaged in both paths. Each terminal model report
has graph_error0, admitted=retired and max_active16. This is the credible
efficient timed-epoll causal competitor, not an intentionally busy or dummy
baseline. The already completed official vLLM reference is a separate
whole-service comparison; it is not silently mixed into these component rows.

Actual client receipt places the Python3.12.12 load generator on g10/IP10.42.6.217
and server on lab/IP10.42.1.238, with actual image ID and zero restarts.
This is the declared different-node cluster TCP path, not a bare ConnectX/NIC
or GPUDirect result. No cross-host monotonic-clock subtraction is used.

I independently checked every archived frozen offset against every cell,
including identical kernel/native schedules for all ten block/rate keys.
Alternating path/rate orders are implemented in the retained orchestrator.
There is no per-request OS thread or project concurrency cap. The client
retains scheduled, task-start, connect, send, receive, finish and close stamps.
All 20 client executable receipts have exit0.

## Independent numerical replay and correctness limits

I independently reconstructed every cell mean, P50, P95 and P99 for connect-
and send-origin TTFT/completion, scheduled-origin TTFT/completion, TPOT, token
receive gaps, positive receive gaps and all-attempt client scheduling lag.
I also reconstructed counts, durations, throughput, zero-gap fractions, the
process-group/cgroup/whole-host/energy/observer deltas, and all 14 paired effect
arrays, means and nominal t95 intervals. They agree with analysis.stdout
within floating arithmetic tolerance. Connect-origin primary completion uses
last token arrival minus connect_begin_ns, as required by the reviewed plan;
the stored send-origin latency_ms is not substituted.

There are 168874 successful responses and 3926 failures, delivering10807936
successful output tokens. Every success has exactly64 in-vocabulary integer
IDs, matching token/timestamp counts, a valid200/octet response and declared
256-byte body. Every failure is a retained kernel192 read TimeoutError with
zero observed tokens; no failed prefix or byte is silently converted into
successful output. From send_done to failure, observed waits span60.000066847
to60.021990800 seconds. Per-operation timeout semantics are preserved.

The unchanged pre-observation finite reference set matches167126 of168874
successes:1748 disagreements remain. Disagreements by rate/path are:

| Rate | Kernel disagreements / successes | Native disagreements / successes |
| --- | ---: | ---: |
| 96 | 517 / 28800 | 519 / 28800 |
| 192 | 484 / 53674 | 228 / 57600 |

The raw check is independent of observed output and was not expanded. This
establishes finite-reference agreement rates and protocol validity, not strict
current-hidden-batch replay or numerical parity across transports. No overall
model-quality or exact-output-equivalence claim follows. The failures and
disagreements cannot support superiority for the proposed method. They do not
erase the valid narrower observation that this implementation drops work and
has worse delivery/resource behavior under the measured192/s workload.

## Failure-aware delivery result

The five kernel192 failure counts are826,815,763,835,687, totaling3926/57600
(6.816%); all five matched native192 cells succeed11520/11520. All ten96/s
cells succeed5760/5760. No failed or unfavorable cell is excluded or replaced.

The following are means of five cell estimates, not pooled P99s:

| Rate | Path | Success-only connect completion P99 ms | Receive-gap P99 ms | Successful token/s including drain |
| --- | --- | ---: | ---: | ---: |
| 96 | kernel | 113.933306 | 3.504357 | 6134.431051 |
| 96 | native | 133.447438 | 3.433428 | 6133.913012 |
| 192 | kernel | 5901.402738 | 8.533018 | 7622.918951 |
| 192 | native | 3330.029438 | 4.214421 | 11637.947341 |

At192/s, kernel-minus-native conditional completionP99 is
+2571.373300ms, nominal paired t95[+1990.360255,+3152.386346].
Receive-gapP99 is+4.318597ms[+3.957999,+4.679196].
Successful token throughput is-4015.028390token/s
[-4813.552494,-3216.504285]. These descriptive paired estimates retain the
failed cells and their drain. At96/s the completionP99 estimate is
-19.514132ms[-78.514119,+39.485854] and throughput+0.518039token/s
[-0.492912,+1.528991]: neither superiority nor equivalence.

Because over1% of kernel192 attempts fail, its success-only P99 is emphatically
**not an all-attempt response P99**. A failure is not a completed60-second
request. The empirical completion-mass figure correctly divides completions by
all attempts and leaves a missing mass; it must retain the failure label and
must not suggest that its plateau is successful completion. Receive gaps
coalesce tokens stamped by the same client read; they are not the official
vLLM stream-output ITL. These observation metrics cannot decompose GPU,
kernel and client causes additively.

192/s exceeds the observed successful native output capacity and causes
seconds of queueing in both paths. It remains the predeclared load, not an
invalid workload to discard. The kernel failures, longer drain and worse
performance are measured behavior of this implementation under that load,
not proof that the GPU's arithmetic alone causes the transport difference.

## Resource ledger, units and exposure

All30 observer streams terminate, with stable owned-group identities in
every sample and no owning-cgroup oom/oom_kill counter increase. Group CPU is
read from process CPU clocks, host CPU from100-Hz /proc/stat deltas and cgroup
usage from microsecond counters. I independently verified the unit conversions
and selected host active classes user+nice+system+irq+softirq. Idle/iowait/steal
are reported separately. NVML cumulative energy converts millijoules to joules,
not watts. It is device-wide. All samples list one compute application, the
owned server; that does not prove exclusive whole-device activity or driver
cost attribution.

Resource brackets include the requested client run/drain plus remote control
overhead. They average62.755/62.785s(kernel/native) at96 and93.541/66.243s at192.
The kernel192 range reaches109.657s. Per-attempt normalization uses all
attempts, including failures, and therefore is not cost per equal useful
output. Secondary per-success/per-token normalizations retain the full
numerator; they do not isolate only-success work.

| Rate | Path | Owned group ms/attempt | Whole host active s/attempt | Device J/attempt |
| --- | --- | ---: | ---: | ---: |
| 96 | kernel | 1.020526 | 0.195078 | 3.098930 |
| 96 | native | 0.879790 | 0.195062 | 3.112075 |
| 192 | kernel | 4.808438 | 0.147282 | 2.011795 |
| 192 | native | 0.923340 | 0.105390 | 1.720603 |

Kernel-minus-native at192:
owned group+3.885098ms/attempt[+3.792477,+3.977719];
whole host active+0.041892CPU-s/attempt[+0.018807,+0.064978];
device+0.291191J/attempt[+0.177343,+0.405040].
At96, group+0.140736ms/attempt[+0.077826,+0.203645], while
whole-host and energy intervals cross zero. None is an exclusive total service
CPU/energy estimate. Longer kernel timeout/drain means more background/device
time is included in its integral. The whole host averages roughly18 active
CPU cores while the service group is much smaller, so host contrast cannot
be assigned to this socket or eBPF path.

The observed io-wq workers all report the server TGID, not separate service
processes. Their CPU is already inside the process/group clock and must never
be added again. Independent per-identity tick/schedstat reconstruction gives
kernel192 mean creator system time54.762s out of group55.393s; visible io-wq
scheduler runtime is only0.014279s. Native192 group is10.637s. This is useful
localization to creator/kernel execution, **not a proof of which kernel
function or loop is responsible**. A1-second finite census misses transient
workers and partial lifetimes; zero visible tick deltas are not zero work.
Softirq/IRQ counts/times are host observations; namespace-visible kthreads
cannot attribute all driver/softirq work. Parent/group, cgroup and host are
nested observations, not additive resource categories.

Sampling is instrumented, not free: mean cadence is about107ms, individual
sample windows reach37.331ms, and observer CPU averages4.49/4.48s at96,
6.05/4.63s at192. This is material compared with the96/s service group's
roughly5–6CPU-s. Equal instrumentation is a fair retained comparison but does
not establish zero latency impact. Counter reads within a sample are not
atomic simultaneous observations. Observer and control work remain explicit.

The5-second requested idle wait produces actual6.469/6.322s brackets.
Group idle CPU is0.043572/0.041286s and device mean power about105W for both
paths. No noisy idle subtraction yields an exclusive inference cost.
Compiled dispatcher40-register and additional IO48-register/168-stack-byte
reports are static footprints, not dynamic SM-time attribution or proof of
GPU saturation. The extra resident IO CTA's opportunity cost remains
unresolved by aggregate device energy/utilization.

## Failure mechanism and deviations

All kernel terminal reports have accepted=closed=received17288 (including
8warmups), no pending/error/drop/reserved/ring-overflow, drained SQ/CQ and
max_connections4096. Nevertheless admitted/completed is short by the exact
192-cell failure count. Thus generic ring drops0 and clean terminal shutdown
do not imply successful admission of every received request.

The retained pair3kernel192 read-only snapshot directly observes
sockhash_failed835, sockhash_linked10693 and llm_queued588. Its failed count
matches that cell's835 timeouts; its linked+failed11528 includes8warmups.
Pair2kernel96 snapshot has0failed and no queued backlog. This is evidence of
an insertion/admission failure class, not independent proof of its errno or
capacity/lifetime cause. The4096map bound, observed connection peak and the
source's global-backlog-dependent EOF close condition motivate a focused
lifetime/capacity discriminator. Do not relabel this hypothesis as a proved
root cause or simply raise capacity and assert resolution.

The declared mid-collection checkpoint scan/compression overlaps pair1kernel96
and can affect host/cgroup/I/O observations; that cell stays in the matrix.
The two read-only counter snapshots add small measured call durations plus
unmeasured control-exec exposure to their cells. No server/source/rate/oracle/
timeout change is made during the matrix. These departures reduce clean
attribution but do not justify favorable exclusions. Existing shared foreign
CPU load is retained. No full-window host/storage journal was available to
this reviewer; the preflight log alone does not prove full-window fault
absence. Stable replies and zero cgroup OOM deltas are narrower receipts.

## Archival, figures and cleanup scope

The full227-file authoritative TEMP set is present in the durable archive.
At review,226files compare byte-for-byte after decompression; details.stdout
is a new CPU replay whose only differences are the resource filename suffix
(.jsonl versus .jsonl.gz). All30parsed numerical/thread values are identical.
Preserve or explain that expected serialization difference rather than
describing the replay output as byte-identical raw output. All primary raw
client/resource/server data and analysis.stdout are byte-identical.

The prepared figure code uses all-attempt completion mass, retained block
curves and unaltered primary resource fields. Its underlying numbers are
reviewed here; final rendered layout is the publishing owner's check.
It must retain shared-host/device and conditional-tail qualifications.

All10 server terminal receipts have exit0, no forced cleanup, no remaining
owned pins and matched detach exit0 for kernel. The original client Job is
intentionally retained for a separately admitted immediate reliability
investigation, not forgotten as an unreported persistent service. Its final
removal and original-session/runtime cleanup remain the owner's pending
receipt. This review does not declare the entire project complete.
