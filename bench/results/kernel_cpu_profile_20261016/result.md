# Creator kernel CPU: complete diagnostic pair
2026-10-16 UTC. Normal main source7495930, artifact revisions c09cd42/8a10829,
reclamation_sourcebuild16 ordinary executors, same lab5090/g10/QwenFP16/gen64.
Both planned60s/192rps cells are terminal:23040/23040 successes,1474560
measured tokens,16 excluded checked warmups. No request failure, exclusion,
replacement or changed oracle/timeout. Native then kernel is one diagnostic
pair, not repeated evidence of a performance effect.

## Primary sampled on-CPU distributions
Official perf6.12.95 cpu-clock:k requested499Hz, only actual creator TID.
Native2455 samples/4.919839640s total period; kernel10086/20.212424688s.
Every observed period2004008ns; self/children reports lost0.
These period sums describe sampled context, not exact process kernel CPU,
request latency or CPU exclusive of interrupts/softirq.
Raw perf.data, full decoded stacks, self/inclusive/header/event-dump reports,
all expanded commands and terminals are in cpu_profile_full/.
profile_summary.py provides descriptive mutually exclusive ancestor categories.

| Stack category | Kernel samples | Kernel weighted fraction | Native samples | Native weighted fraction |
|---|---:|---:|---:|---:|
|Loop coordination, other|4419|43.8132%|0|0%|
|BPF map, without socket ancestor|2727|27.0375%|0|0%|
|Socket/network/softirq ancestor|2693|26.7004%|2075|84.5214%|
|Scheduler, without socket ancestor|103|1.0212%|135|5.4990%|
|Unknown leaf|144|1.4277%|1|0.0407%|
|Other kernel|0|0%|244|9.9389%|

Thus70.8507% of kernel sampled periods lie in loop coordination or BPF maps
without an observed socket ancestor. This identifies a material coordination
cost, not proof that every sample is avoidable, spinning, or caused by a
specific branch. Kernel self symbols: __queue_map_get26.45%,
ktime_get_mono_fast_ns14.57%, __bpf_prog_exit_sleepable9.16%,
__bpf_prog_enter_sleepable7.09%, own uring_loop_step6.62%, nft_do_chain5.20%.
Raw exact per-symbol weights remain; rounded perf percentages are not added.

Kernel9404/10086 samples contain at least one unknown kernel frame, generally
between named BPF program and __io_run_loop (consistent with trampoline
context, but not positively resolved); native1/2455. This differs from unknown
LEAF samples144/1. Named leaf/caller observations are useful, but unknown frames
prevent a complete per-instruction ancestry proof. No hiding those samples.
Inclusive symbols overlap and are never summed. Networking/softirq may include
unrelated packets serviced in this current task's context.

## Serving/resource validity context (profiled, one pair)
| Metric | Kernel | Native |
|---|---:|---:|
|Attempts/successes|11520/11520|11520/11520|
|Delivered token/s|11633.295|11658.728|
|CompletionP99 ms|3409.273|3297.491|
|Client receive token-gapP99 ms|3.756|4.057|
|Owned group CPU ms/attempt|1.820360|0.784433|
|Finite frozen-set disagreements|21|2|

No confidence interval or superiority/equivalence claim follows from this
single profiled pair. The token-gap sign differs from prior five-block result;
keep both. Group CPU includes owned io-wq once. Observer/profiler/control,
shared host/device work and sequential-order exposure remain. Client gaps
are receive grouping, not GPU generation intervals. All23 finite-reference
disagreements remain; protocol-valid delivery is not full-run exact parity.
This source is already separately protocol/dual-replay qualified in0072.

## Cause selection and limits
[source context](source-context.md) shows the upstream __io_run_loop sleeps
only for a future CQ index. Own BPF requests current CQ index whenever
admitted!=admission_seen, even during an already-active60000ns timer epoch.
Repeated callbacks each perform clock reads, sleepable BPF enter/exit and
queue peek/reservation. The sample distribution selects this coordination/
admission acknowledgment branch as the next causal discriminator, ahead of
unmotivated network or model-arithmetic edits. It does not yet prove the
particular branch creates the excess or that changing it improves delivery.
A future active/idle-aware intervention must preserve idle wake/stop ownership,
qualify correctness and compare against both current and efficient native.

This does not partition the old unreproduced6.36ms marginal P99 difference,
measure off-CPU delay, GPU polling intervals, complete all-thread/host cost,
or prove CPU-free serving. No canonical source/default change is made.

## Execution, replay and lifecycle
One real preflight pair passed; all planned full acquisition/decode commands
are terminal. Both servers exit0, queues drain and owned pins empty. Final
kernel insertion failures/first errno0,11528 warmup+measured admissions retired.
Both perf recordings intentionally receive SIGINT after client full drain,
flush data and re-raise it (return-2). This is not reported as exit0.
All10 decode commands exit0. Standard report warns only missing optional
tips.txt in stdout; decoding stderr is empty. No instrumentation substitution.
Each client compression/transfer occurs after its server stops and before the
next cell. Large perf decode/archive runs once after BOTH cells have stopped;
no postmeasurement collection failure occurred here.
Primary serving archive replay is byte-identical, stderr empty.
[Independent result review](result-review.md) is complete: valid, supported
coordination-cost localization, supporting mechanism/workload evidence.
Specific branch avoidability and improvement remain unproven. The required
collection-chronology wording correction above is resolved by the owner.
Client Job is retained only for this bounded
diagnosis and ensuing repair qualification, with explicit cleanup on closure;
no persistent service or setting is retained.
