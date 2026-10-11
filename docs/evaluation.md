# Evaluation status

The repository has no formal paper RQ or thesis contract. The retained user
objective is a complete Linux TCP/HTTP + eBPF/shared queue to resident
real-model inference and asynchronous kernel TX, with reproducible matched
correctness and throughput/latency evidence. Do not substitute model arithmetic
tuning or a component result for that complete goal.

The [native userspace network comparison](findings/0025-native-userspace-network.md)
is complete and valid as a supporting component ablation. It tests kernel
request/reply versus a native epoll control with identical resident HF graph
computation. Finding0024 lacks that native network condition, so the new
comparison fills independent evidence rather than repeating its dispatch test.

The [plan review](../bench/results/userspace_network_plan_review_20261011.md),
strict real-model regressions and preflights precede the committed-source full
run. [Fresh result review](../bench/results/userspace_network_result_review_20261011.md)
independently reconstructs80 cells,5120 requests,166400 exact measured tokens,
20 normal exits, order, metrics, counters and cleanup. No failed/excluded row
or required scientific repair. Commands and all raw/result tables are linked
from the finding.

Primary user-minus-kernel gen1/clients1 TTFT:
Smol1.054ms [0.949,1.160], Qwen1.107ms [0.923,1.292].
Primary kernel-minus-user gen64/clients8 TPS:
Smol-5.899 [-13.040,1.242], Qwen-3.194 [-10.281,3.894].
These five-pair nominal t95 intervals narrowly support single-client one-token
latency; concurrent long-output throughput is inconclusive, not equivalent.

Research value is supporting evidence; paper impact is a transport/workload
boundary, not an external SOTA result or novelty proof. Polling, write grouping
and page backing change with transport, preventing syscall-only attribution.
Loopback/token-ID HTTP, short prompts, two small checkpoints and a shared GPU
limit scope. Executor CPU excludes kernel TX/softirq; global CPU is descriptive.
No attributed total CPU, energy, physical-NIC or full-goal completion claim.

Next decision: retain all negative estimates and crossing-zero intervals;
close the unchanged matrix. [Header/first-token coalescing](findings/0026-coalesced-network.md)
now passes all four strict regressions, passive diagnostics and two native real
preflights. The [reviewed next comparison](../bench/results/coalesced_network_plan_20261011.md)
uses both optimized transports with unchanged compute, oracle and TCP defaults.
Its full matrix remains uncollected; no new performance claim follows from
qualification. This fair kernel-versus-user comparison does not establish a
causal old/new optimization effect, which requires a separately matched
before/after run. Passive traces show header/first-token coalescing but retain
ACK-followed delivery gaps for the remaining short response. Strong external
serving, attributed host cost and real-NIC evidence remain open.
