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

Next decision for finding0025: retain all negative estimates and crossing-zero
intervals and close that unchanged matrix.

The subsequent [header/first-token coalescing comparison](findings/0026-coalesced-network.md)
is also complete. Its [reviewed plan](../bench/results/coalesced_network_plan_20261011.md)
tests whether removing the native request/reply worker improves client latency
or throughput after both transports coalesce output, using identical resident
HF computation, oracle and default TCP. This supporting experiment adds a
common transport optimization to the previous component comparison, rather
than repeating unchanged source or tuning model math.

The first full attempt failed on admission; its partial prefix remains
separate. The repaired source passes strict graph/legacy bridge qualification
and fresh native preflights before frozen cc07226 full collection. Both retry1
models complete:80 cells,5120 exact measured requests,166400 tokens and20 normal
executors. [Native analysis and independent reconstruction](../bench/results/coalesced_network_analysis_20261011.stdout.txt)
and [fresh result review with correction](../bench/results/coalesced_network_result_review_20261011.md)
reconstruct coverage, token agreement, metrics, order, counters and cleanup.

Primary user-minus-kernel gen1/client1 TTFT:
Smol-0.130363 ms [-0.490798,0.230071], Qwen-0.042867 ms [-0.116078,0.030344].
Primary kernel-minus-user gen64/client8 TPS:
Smol+1.229153 [-9.310734,11.769040], Qwen+78.277177 [-132.336242,288.890597].
All four nominal five-pair t95 intervals cross zero: neither superiority nor
equivalence. The Qwen user pair3 throughput cell additionally overlaps a
verified global OOM; its paired kernel cell occurs about80 s later. Preserve
all samples and the unchanged descriptive estimates. Unequal exposure prevents
Qwen transport-only attribution; no kernel robustness claim follows.
The initial reviewer's no-host-fault statement is withdrawn.

Run status: valid completed raw measurements and correctness. Tested hypothesis:
inconclusive. Research value: supporting. Paper impact: mechanism/workload
boundary. Close this matrix; the next load-bearing performance uncertainty is
service-attributed host work and sensitivity under explicitly matched/measured
interference. Existing process/global CPU counters cannot resolve that question.

No causal old/new coalescing speedup, external SOTA or novelty claim follows.
Passive traces retain ACK-delayed short-response delivery. Strong external
serving, physical networking, full text processing and online batching remain
open. Continue the full retained objective with reused compute.


The next [timed native control experiment](findings/0027-timed-network-control.md)
tests whether bounded executor-plus-TX CPU savings survive an efficient native
request/reply worker while retaining identical FP16 HF computation. Planned
role: supporting. Finding0026 cannot supply the absent condition/counter
through reanalysis. Fresh plan review passes; four strict real-model
regressions and six three-mode preflight executors pass. These dependencies
do not answer the performance hypothesis.

Full collection is pending:120 cells,7680 measured requests,249600 tokens,
30 normal executors across both models. Primary CPU microseconds/request at
gen64/clients8 accompany standard TTFT/TPS and nominal five-pair intervals.
The sum excludes RX/softirq/BPF/TCP outside TX; no total host/service CPU
claim is permitted.

An unrelated GPU-SMT candidate Job ends on ENOSPC at10:34:41UTC during
qualification, before all preflight cells/full collection. Subsequent reads
confirm the original SGLang process is absent. BPFusion issued no stop/restart
or other-PVC mutation. The environment receipt preserves observations;
earlier shared-SGLang performance does not transfer to this host condition.
Independent full-result review and interpretation remain pending.
