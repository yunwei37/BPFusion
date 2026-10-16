# Independent plan review — kernel creator CPU profile

2026-10-16 UTC. Fresh review, round 1. Read the current plan, docs/evaluation.md,
findings0066/0071/0072, docs/background-related-work.md, the package/source
metadata in this directory, and official Linux perf-record documentation.
No experiment execution, source modification, runtime change or Git action.

## Verdict

Scientific admission passes as **supporting mechanism diagnosis**. There is
one narrow executability correction required before real preflight: freeze an
actual runnable command and the collection/decoding argv in this same plan.
The present directory contains plan.md and package metadata, but no launcher;
the plan names future runnable commands/scripts only as outputs. This prevents
checking whether the promised thread, timing window, period weights and self /
children reports will actually be collected. It is not a request for another
baseline, workload, repetition matrix or profiling feature.

## Required correction

Add the real PowerShell launch invocation (or a runnable inline command), its
existing client/server/observer paths, and the concrete perf record/report/script
commands, with ordinary runtime substitutions for the discovered creator TID
and output directory. Ensure record actually preserves sample periods; the
chosen argv should express cpu-clock:k, 499Hz, callchain recording, the creator
TID only, no inheritance, and a named perf.data. State how successful profiler
attachment precedes measured client submission after the eight checked warmups,
and how terminal client drain leads to profiler stop/wait and decoding. Both
preflight and full invocation must resolve to the fixed 128-attempt or
11520-attempt per-path schedules rather than the old multi-block matrix.
Name the self and children report invocations and the script export that
retains periods and callchains. This is the missing executable specification,
not a requirement to add a new experiment-control interface.

No new scientific plan or materially different expected answer is requested.
Once that correction exists, use the planned real preflight to establish
permissions, kernel symbols, actual callchains, loss reporting and cleanup.
A permissions/symbol/attach failure remains instrumentation failure, not an
outcome supporting either mechanism. Do not change host settings to force it.

## Concern-by-concern assessment

**Hypothesis and evidence effect.** Sampling the current dominant creator
thread directly distinguishes on-CPU coordination from actual TCP/BPF work
within that thread. It does not identify off-CPU wait, all service CPU, exclusive
softirq cost, GPU cycles or a fraction of end-to-end latency. The plan states
those limits. Scheduling-heavy, TCP-heavy, mixed and unresolvable outcomes lead
to different next repair decisions without declaring a serving win. A stack
profile motivates a source mechanism and matched intervention; it cannot itself
prove avoidability or causality.

**Admission, nonredundancy and alternative use.** 0072 already establishes
remaining adverse group CPU (1.695749 versus 0.732280ms/attempt) after lifetime
repair. 0071 supplies a pre-repair fault boundary; 0066 predates both repaired
source and current remote operating point. Existing aggregate/thread CPU
records cannot reconstruct sampled instruction stacks. Reprofiling the repaired
source therefore adds an independent discriminator. It is a stronger runnable
next step than unchanged throughput repeats or arbitrary tuning, and is honestly
supporting work rather than a new headline result or preparation receipt.

**Baseline and workload fairness.** Efficient native epoll is the credible
matched alternative to removing the steady userspace worker. It has the same
resident computation, model, mixed scheduler, capacity, NODELAY, prompts,
outputs and arrival offsets. Keeping the failed global-close variant out avoids
confounding this attribution with the already settled reclamation fault. The
existing official vLLM reference addresses a separate whole-service comparison;
rerunning it adds no value to this creator-thread question. One sequential pair
is sufficient for diagnostic attribution, with no general performance or
transport-effect uncertainty estimate. The plan correctly retains finite-set
output disagreements and forbids favorable oracle changes.

**Metrics, correctness and interpretation.** Standard perf self and inclusive
sample-period distributions are appropriate primaries; they overlap and must
not be added. Report raw symbols, weighted sample totals, observed period
behavior, loss and unknown/truncated stacks. The explicit single-category rule
can summarize stacks, while raw callchains remain authoritative and ambiguous
samples stay unknown. Sampling fractions describe captured on-CPU kernel work,
not wall time or a partition of historical marginal P99s. Client tails and
resources are validity context under profiler/observer exposure, not new
unprofiled gains. Fixed oracle, timeout, full drain, all failures and existing
source-native checks are sufficient within the stated unchanged-source scope.

**Execution, completion and cost.** The matrix is bounded and clear: two real
128-attempt preflight paths, then one native/kernel pair with 11520 attempts per
path over 60s offered schedules and terminal drain, checked warmups excluded.
The original 60s per-I/O timeout means total wall time can exceed offered-load
duration; no wall deadline should silently truncate it. Private official perf
package extraction and owned disposable-client cleanup preserve the declared
runtime/source boundary. Preflight should test the actual full path and stop
at the stated attempt limit; a self-test is insufficient. Raw perf.data,
decoded reports, client/resources, source/argv and terminals support an
independent result review once the missing commands are fixed.

## Nonblocking clarification

In perf's documentation, --call-graph fp selects the userspace unwind method;
kernel callchain unwinding follows the running kernel's configured unwinder.
Describe this accurately in the result and verify actual kernel callchains in
preflight. No kernel rebuild or additional profiling mode is requested.

Primary reference checked:
[Linux v6.12 perf-record documentation](https://github.com/torvalds/linux/blob/v6.12/tools/perf/Documentation/perf-record.txt).
The plan also cites the official perf-report documentation for report semantics.


## Follow-up 1 — concrete collection path

2026-10-16 UTC. Reread the amended plan and archived run_cpu_profile.ps1,
cpu_profile_record.py, cpu_profile_archive.py, cpu_profile_analysis.py and
cpu_profile_server.py. This is the first follow-up to the same review; no new
experiment or GPU/client/runtime action was performed by this reviewer.

**Verdict: the required correction is addressed. No remaining scientific or
executability blocker before the planned real preflight.**

The plan now supplies the PowerShell invocation and points to an inspectable
launcher. The launcher runs exactly native then kernel, performs the existing
eight checked warmups, starts observer/perf afterward, uses the dedicated
128-offset prefix for preflight or original full offsets, waits for the actual
client command to terminate, and stops/waits for perf, observer and server
before client transfer. It does not substitute the old 32-request client
preflight or old multi-block schedule. The server uses the ordinary16 build
and existing lifecycle/model/input path; the count-only analysis adapter
requires exactly two pair0/rate192 cells and does not fabricate intervals.

The record argv names cpu-clock:k, frequency499, callchain recording, actual
server creator TID, no inheritance and the data path. Period retention is
satisfied by frequency mode: upstream perf evsel configuration sets
PERF_SAMPLE_PERIOD when attr.freq is enabled, so a redundant explicit --period
flag is unnecessary. The script decoder requests period and full callchains;
self/children reports are separate, and header/raw dumps retain the data needed
to inspect loss and configuration. Reviewed primary source:
[Linux v6.12 perf evsel configuration](https://github.com/torvalds/linux/blob/v6.12/tools/perf/util/evsel.c#L1124).

As already planned, process-alive/readiness checks are setup evidence only.
The real preflight must establish actual target samples, useful kernel
symbols/callchains, periods/loss and terminal cleanup before the full pair.
Unknown stacks or inadequate samples remain unresolved diagnostic evidence,
not a reason to reinterpret failure as a favorable mechanism result. The
kernel-unwinder wording correction is nonblocking and does not change the
collection protocol or expected answer.

Admission, baseline fairness, fixed correctness/oracle/timeouts and narrow
supporting interpretation from the initial review remain unchanged. No extra
baseline, repeated performance matrix, source optimization or host-setting
change is requested.
