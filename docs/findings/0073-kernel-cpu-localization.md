# 0073: creator kernel CPU localizes coordination work
2026-10-16 UTC. [Plan/review](../../bench/results/kernel_cpu_profile_20261016/plan.md),
[full result](../../bench/results/kernel_cpu_profile_20261016/result.md) and
[independent result review](../../bench/results/kernel_cpu_profile_20261016/result-review.md).

Same repaired ordinary16 QwenFP16/mixed executor, lab5090/g10,192rps60s,
native then kernel. Both11520/11520 succeed,1474560 measured tokens total,
16 excluded checked warmups. No source/default/model change. Official Linux
perf records only creator-TID on-CPU kernel samples at499Hz.
Kernel10086 versus native2455 samples,20.212425 versus4.919840s observed
period sums; no recorded loss/throttling. These are sampled context, not
exclusive process/kernel CPU, GPU cycles, off-CPU time or client latency.

Under the disclosed observed-ancestor classifier, kernel43.8132% is other
loop coordination and27.0375% BPF maps without socket ancestors, combined
70.8507%; socket/network/softirq26.7004%. Native network/softirq84.5214%.
Named leaves include queue-map get, clock and sleepable BPF enter/exit.
Unknown kernel leaf144/10086; at least one unknown frame9404/10086, limiting
full ancestry proof. Network softirq can include unrelated packets.
No sample is silently removed; self and inclusive distributions overlap.

This selects coordination as a meaningful next causal discriminator. Current
admission-unseen branch asks for already observed CQ even during active timer;
upstream kernel can immediately re-enter BPF. Profiling alone does not prove
that branch is avoidable, pure spin or the cause of excess resource cost.
A matched intervention is needed before retention or performance attribution.
The old6.36ms marginal tail gap is not partitioned.

Profiled serving TPS11633.295/11658.728, group CPU1.820360/0.784433ms/request
kernel/native remain context only: one ordered pair and profiler/observer
exposure do not support superiority or uncertainty/equivalence claims.
Client-gapP993.756/4.057ms reverses prior sign; retain both results.
All23 finite-reference disagreements stay. Protocol-valid is not exact
full-run parity. CPU serving replay, raw binary records/periods, source and
baseline fairness independently audit correctly; collection chronology prose
is corrected. Valid supporting localization, mechanism/workload boundary.
No canonical optimization is selected from this result.
