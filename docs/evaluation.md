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


The [timed native control experiment](findings/0027-timed-network-control.md)
is complete. It tests whether executor-process-plus-TX CPU savings survive
an efficient native request/reply worker with identical FP16 HF computation.
Role: supporting. Finding0026 cannot supply the absent condition/counter
through reanalysis. The reviewed plan, strict regressions and real preflight
precede frozen9f091f9 collection; these dependencies have no independent
performance value.

[Fresh result review](../bench/results/timed_network_result_review_20261011.md)
independently reconstructs120 cells,7680 exact measured requests,249600 tokens,
30 normal executors, all150 CPU read brackets/components and native paired
statistics. Native analysis and full wrapper exit0; no failed/excluded/retried
full-run rows. Ten resident module unloads each report55176 bytes,264 completed,
zero abandoned/retries,19 accepted/closed sockets.

Primary control-minus-resident CPU at gen64/client8,us/request:
Smol timed-383.283 [-593.022,-173.544], Qwen timed-337.304 [-659.632,-14.976].
The bounded CPU-saving prediction is contradicted against this efficient
control in both tested checkpoints. Busy-control differences remain positive,
but do not establish superiority over efficient CPU orchestration.
The sum excludes RX/softirq/BPF/TCP outside TX; it is not total service CPU.

Timed-control-minus-resident gen1/client1 TTFT:
Smol+0.090901ms [-0.141011,0.322813], Qwen-0.026525ms [-0.059269,0.006218].
Resident-minus-timed gen64/client8 throughput:
Smol-2.488979 [-9.443425,4.465468], Qwen+2.632198 [-3.308572,8.572968] tokens/s.
All planned client intervals, including busy controls, cross zero; neither
superiority nor equivalence. All conditions use the same768-row dispatcher SASS.

The co-tenant Job ends on ENOSPC during qualification; a new SGLang scheduler
is observed immediately before full collection and alongside BPFusion at
10:56:58/11:14:58UTC. Its full-Qwen activity/residency is unknown. Retained
journal reads find no matching faults through the full interval, which does
not prove no interference. A delayed21:51UTC after-run read finds the same
boot, no own process/module/pins and an idle GPU; it cannot locate the SGLang
departure. Qwen global CPU/TX trends also forbid transport-only attribution.

Run status: valid. Tested bounded hypothesis: contradicted by the observed
efficient-control comparison. Client performance: inconclusive. Research
value: supporting. Paper impact: mechanism/workload boundary. Close this
matrix, publish the negative result, and locate/discriminate kernel
accept/drain/completion cost before selecting a transport change. No model
arithmetic campaign, general total-CPU/speed claim or external SOTA result
follows. Compute reuse, physical NIC, strong official serving comparison,
full text and online batching remain part of the full retained goal.


The [socket-readiness candidate](findings/0028-socket-readiness.md) tests the
next concrete request-path hypothesis after finding0027. Its reviewed plan
retains identical model computation and the efficient native control; the only
behavior change is avoiding accept/recv attempts when existing Linux poll
reports no input/EOF/error readiness. Role: supporting. Build and plan review
pass; both affected-kernel strict runs finish normally with670 valid requests,
40864 exact tokens and518 rejections. Current three-mode preflight also
completes: six normal executors,24 exact measured replies,both native analyses
exit0 and all12 idle/cell CPU brackets/components reconstruct. Full frozen-source
collection now completes120 cells,7680 exact requests,249600 tokens and30
normal executors. Both native analyses and fresh independent result review
pass; all150 idle/cell CPU rows reconstruct. Efficient-control-minus-kernel
CPU differences at gen64/c8 are Smol+182.142222[-60.833662,425.118106] and
Qwen+255.283197[-44.867063,555.433457]us/request,nominal five-pair t95.
Both cross zero; planned TTFT1/c1 and throughput64/c8 also cross zero.
Run valid/complete,hypothesis inconclusive,role supporting. No total CPU,
historical causal improvement or external SOTA follows. Close this matrix
without unchanged repeats; the old negative matrix remains separately closed.


The [cross-node comparison](findings/0029-cross-node-network.md) addresses
the untested real-network boundary without changing qualified computation.
Role supporting; strongest runnable alternative is efficient native timed
networking with the same resident graphs. Both bound-address kernel strict
suites,Qwen timed strict,and default-loopback compatibility pass. Four real
cross-node preflight executors complete16 exact measuredtokens and normal
exits; both direct client analyses pass. Packet/route receipts establish
Linux TCP over existing flannel/Tailscale and Ethernet,not bare-NIC or
GPUDirect. The80-cell full matrix and independent result review are pending;
preflight has dependency value only. Planned per-model primary effects are
TTFT1/c1 and TPS64/c8 with five paired nominal t95 intervals. Server/total CPU
is not measured by the remote client adapter. Strong official serving,total
CPU,full text/API,broader qualified backends and online batching remain open.
