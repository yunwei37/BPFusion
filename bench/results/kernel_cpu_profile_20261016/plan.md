# Kernel-loop CPU attribution at the repaired remote operating point

2026-10-16 UTC. Supporting diagnosis within the retained serving RQ: does
removing the steady userspace request worker improve real delivery/resources
with matched reused model execution? No formal thesis/RQ contract exists and
none is invented or changed.

## Admission / next decision
Finding0072 fixes EOF retention but current kernel/native groupCPU is
1.695749/0.732280ms per attempt; repaired kernel creator system CPU alone is
17.64--20.20s per cell versus native4.48--5.08s. Finite observed io-wq runtime
is small, not proof of zero worker cost. Old0066 profiles predate mixed/EOF
repairs and cannot identify present instruction cost. Existing full raw
resource data identify the thread but contain no sampled instruction stack.

The load-bearing uncertainty is avoidable kernel coordination/wait work
versus actual TCP/BPF admission/data handling. A kernel scheduling/queue wait
dominated profile selects that source for the next repair; a TCP-dominated
profile contradicts this expectation and selects data-path work or records
intrinsic remaining cost; unknown symbols/small samples mean unresolved, not
a winning optimization. Mixed findings retain all categories. This bounded
supporting mechanism evidence changes the next implementation choice; it is
not another throughput contribution or a headline model optimization.
It outranks arbitrary timer/layout sweeps, more external baselines and
unchanged load repeats. Official vLLM already supplies the external reference.

## Hypothesis, comparison and scopes
Expected avoidable CPU burns in the kernel BPF-loop/CQ/SQ coordination rather
than io-wq. Profile both current ordinary paths: canonical main7495930 normal
Make16 builds, same GPU/model/mixed scheduler/NODELAY/EOF repair. Main competitor
is efficient C++ epoll with identical resident compute. No broken global
ablation or more baseline rows. Model arithmetic and all source remain unchanged.
One native then kernel pair,192rps60s,11520 attempts each, same frozen four
prompts and64 outputs, gamma offset seed20261015 (block0), original60s per-I/O
timeout, full drain,8 excluded checked gen1 warmups each. This is diagnostic,
not five-block evidence of throughput/cost improvement or causality by sampling.
The existing frozen finite-set disagreement flag stays visible; no pool expansion.

Use official Linux perf6.12.95 cpu-clock:k at499Hz, call-graph fp, only the
actual creator TID (--tid, --no-inherit), from after warmup to full client drain.
This targets the dominant thread; it cannot account for all workers, remote
softirq, off-CPU sleep or GPU cycles. Preserve period weights and callchains,
self and inclusive CPU distributions separately; they overlap and are not added.
At most one top-level stack category assigned per sample by explicit Linux
ancestor grouping: BPF loop synchronization/wait (excluding nested actual socket
data handling), BPF map/admission, TCP/socket operation, generic scheduling,
other/unknown. Raw ungrouped symbols are authoritative. Do not relabel spinlock
samples as pure network wait without callchain support.

Primary diagnostic is sampled on-CPU kernel distribution/call stacks, not
an inferred partition of old6.36ms clientP99. Present sample count/lost events,
unknown symbols and actual CPU-clock periods. Perf's own standard self/children
semantics:
https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-record.txt
https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-report.txt
Secondary actual client throughput/tails/failures/scheduling lag and existing
resource observer retain validity context only. Profiling overhead and shared
work mean no observer-free performance gain or exclusive totalCPU inference.
The fraction of samples is not the fraction of end-to-end wall latency.

## Execution, preflight, collection and cleanup
Private official Debian perf package and matching libraries are extracted only
under original Workspace OS TEMP, not installed globally. No sysctl, kernel,
permission, host or model setting changes. Record exact URLs/versions. Existing
full images/runtime/model weights stay unchanged. Recreate only the same
bounded disposable remote client Job through its existing benchmark path,
no persistent service/scheduler/Workspace. No foreign workloads interrupted.
Current source main and original Coder PIDs/starttimes/WIP must stay.

Real preflight uses same actual normal16 kernel/native pair with128 attempts
each at192rps, same input/output/oracle, and the actual perf record/report/script
path. At most3 preflights. Verify attach/sample/symbol/loss/terminal cleanup and
all expected request outcomes; fail instrumentation explicitly if unavailable.
A tiny perf self-test alone is not this real preflight. After executable
preflight, run both planned full60s cells to terminal, retain all failed/partial/
unknown data. No favorable unrecorded replacement or changed oracle/timeouts.
Reuse existing remote_async_client.py, remote_server lifecycle,
resource_observer.py, remote_analysis.py; adapt only build/provenance/profile
lifecycle and fixed single-pair schedule. Separate profiler env from server.

Raw outputs under this directory, actual runnable PowerShell command and scripts,
native perf.data (lossless gzip), decoded script, self/inclusive reports, exact
source/commands/terminals, client/resources and CPU replay. One result report
and fresh independent result review. Commit/push each completed step as authorized.
Delete owned client Job and perf processes after bounded work; retain no helpers.
No canonical code optimization is adopted from an attractive sampled profile:
first reproduce a specific source mechanism and test a matched intervention.

## Concrete commands prepared before execution

From spark-manage, with the owned temporary client Pod name discovered after
its existing Job becomes Ready:
powershell -File <OS-TEMP>/run_cpu_profile.ps1 -ClientPod <owned-pod> -ServerIP
<current-Workspace-PodIP> -Preflight
then the identical command without -Preflight. Actual script is archived here.
Preflight uses the original gamma schedule's first128 offsets, not the old
client --preflight option (which selects32); both paths receive identical128.
cpu_profile_record.py records:
perf record -e cpu-clock:k -F499 --call-graph fp --tid SERVER_PID
--no-inherit --no-buildid --no-buildid-cache -o PREFIX.perf.data.
cpu_profile_archive.py executes perf report self and children, perf script
with period/event/symbol/DSO fields, header and raw-event dump (including loss).
cpu_profile_analysis.py is a count/matrix-only adapter of remote_analysis.py:
128 preflight /11520 full and exactly native/kernel pair0/rate192; no fabricated
five-block interval is emitted. Metric definitions and outcome checks unchanged.
Client/resource scripts and unmodified source lifecycle basis are archived.
Client raw transfer/compression is after owned server stop in this diagnostic,
and all raw outputs are archived before starting another measured process.

Kernel callchain unwinding follows the running kernel configuration. The fp
option selects userspace callchain mode; it does not force kernel frame pointers.
