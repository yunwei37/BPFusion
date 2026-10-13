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

Primary user-minus-kernel gen 1/clients1 TTFT:
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

Primary user-minus-kernel gen 1/client1 TTFT:
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

Timed-control-minus-resident gen 1/client1 TTFT:
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


The [cross-node comparison](findings/0029-cross-node-network.md) is now complete
on frozen eaa9c8e source:80 cells,5120 exact measured requests,166400 tokens
and20 normal executors. Its efficient userspace alternative uses the same
resident HF computation. Native direct analysis passes; the fresh independent
review and all raw evidence are linked from the finding. Both per-model primary
TTFT1/c1 and TPS64/c8 nominal paired t95 intervals contain zero.

Run status: complete; tested hypothesis: inconclusive; research role: supporting;
paper impact: network/workload boundary. The actual path is flannel/Tailscale over
Ethernet,not bare-NIC/GPUDirect. Server/total CPU is not measured. All rows are
retained and the temporary client Job/Pod and own server resources are removed;
the original Workspace remains Ready. Close this unchanged matrix. Full-service
CPU attribution/interference, strong official serving, full text/API, broader
qualified backends and online batching remain under the retained objective.

The [short-input latency diagnosis](findings/0030-short-input-latency.md)
completes 40 exact gen 1 replies and full model-node trace coverage on
unchanged 9954855 source. Sixteen measured profiled-loopback requests/model
place 95.48%/91.69% of TTFT inside the existing Smol/Qwen captured model
region. Run valid/complete; hypothesis narrowly supported; role dependency-only.
Tiny ingress-to-GPU stages are unresolved within clock calibration, and
profiling/shared-device conditions prevent exact attribution of the previous
cross-node 3 ms. Qualify reused faster compute before another same-backend
serving comparison. The retained system/performance goal remains open.

The [AlpinDale native-backend qualification](findings/0023-batch-execution-qualification.md#alpindale-rtx5090-qwen-qualification-complete-numerical-rejection)
completes32 sequences/2048 tokens on unchanged CUDA/binding source. Both
predeclared theta conditions fail all16 sequences against both HF references,
while generation modes and repeats agree. Native build passes; strict backend
qualification fails. Role dependency-only; no independent serving result.
Close this candidate without numerical tuning. The retained performance and
reusable-backend objective remains open.

The [official optimized-serving comparison](findings/0031-optimized-serving.md)
completes40 cells/2560 measured requests/83200 tokens on frozen production442ab45.
Ten launching parents return wait exit0; primary replay and planned secondary
analysis exit0. Official shutdown force-kills EngineCore children and native
HF shutdown logs SubprocPool unclean exit; all receipts are retained.
BPFusion gen64/c1 TTFT2.185ms versus vLLM8.954ms, while gen64/c8
throughput1407.718 versus4713.694 tokens/s and TPOT5.593 versus1.501ms.
Five-pair intervals and all other metrics are linked. BPF matches1280/1280
reference sequences; vLLM838/1280, so there is no identical-output superiority
or eBPF causal claim. Run complete; effects mixed; role supporting; broader
goal open. Qualify optimized compute/batching reuse before another identical-
backend serving-path comparison. Independent result review and restoration
are linked from the finding.

The [official FULL-graph integration qualification](findings/0031-optimized-serving.md#optimized-backend-integration-actual-full-graph-reuse)
completes19 groups/74 lanes,1197 actual GPU launches across batch1/2/4/8,
and4177152 finite bit-identical FP16 output elements after NaN poisoning.
All74 complete CPU-loop sequences match frozen official references; HF eager
agreement36/74 remains separate. Fresh result review admits valid/complete
FULL-body device launch; role dependency-only, no serving/performance claim.
Three failed setup attempts and the fourth repair are retained. Next implement
GPU-owned generation and prefill/queue/lifetime integration; full goal open.

The [GPU-owned optimized decode qualification](findings/0031-optimized-serving.md#optimized-backend-integration-gpu-owned-decode-and-sampling)
completes19 groups/74 lanes and4736 exact official-reference output IDs,
including4662 GPU-sampled tokens after74 CPU-prefill seeds. Device-owned
metadata/slot advancement,1197 child launches/1216 parent invocations and
19 host parent submissions engage; restored official CPU trajectories also
match. Role dependency-only, no serving/performance claim. Official KV
reservation and prefill still need replacement by bootstrap-owned slots and
GPU request admission before kernel-queue integration. Full goal open.

## Actual optimized kernel-queue integration

Finding0032 integrates upstream model/head graphs into GPU-owned new-request
prefill and tensor-batched decode through the existing eBPF queue/kernel TCP.
The supporting comparison tests matched optimized computation against efficient
native timed-epoll networking; it adds online prefill/admission/lifetime and
tensor-batching evidence beyond the earlier CPU-prefilled generation probe.
The initial OOM and wrong import failures precede requests and remain archived.
Queue-derived KV allocation/context bounds are necessary bootstrap deviations;
both modes use them and no earlier default-context qualification transfers.

Strict traced service qualification is complete for both models/transports:
2488 requests/88896 exact replayed tokens,1036 intended rejections,all batch
counts1..8,fragmentation/reuse/wrap/pipeline/half-close/helper-thread shutdown.
This is dependency evidence within the integrated comparison, not an independent
paper result or a task-quality/model-math oracle. All actual client output bytes
match independently advanced host replay of the same upstream graphs.
The five-pair full performance matrix is complete:80 cells/5120 measured
requests/166400 measured tokens,20 normal executor waits and two complete
replay analyses. Smol kernel/user TTFT1.201405/1.222876ms and TPS5358.410/5363.427;
Qwen1.473674/1.432418ms and4576.218/4630.119. All primary paired t95 intervals
contain zero; superiority and equivalence remain unproven. This is supporting
mechanism/workload-boundary evidence, not a paper RQ or novelty proof.
Actual concurrent batch trajectories and some greedy outputs differ between
transports; every actual sequence matches its own independent host replay.
Both modes use identical BF_TRACE; default untraced and new cross-node timing,
total CPU and arbitrary-backend support remain unqualified. [Fresh combined result review](../bench/results/vllm_server_result_review_20261012.md)
admits valid/complete supporting evidence and no blocker within the traced
contract. Owner restoration verifies no processes/module/pins/GPU applications,
unchanged base runtime and removal of owned temporary/build artifacts; original
Workspace UID is Running/Ready with zero restarts. The full goal remains active:
no untraced/physical-path/total-CPU/general-backend claim follows. Close this
unchanged matrix and select a causal discriminator for broader acceptance. See the [plan](../bench/results/vllm_server_plan_20261012.md),
[plan review](../bench/results/vllm_server_plan_review_20261012.md) and
[integration finding](findings/0032-vllm-kernel-serving.md).

## Mixed-length prefill packing

Finding0033 admits a supporting causal comparison of grouped versus packed
GPU prefill with unchanged upstream arithmetic/catalogue and transport.
It tests the exposed gen1/eight-client queueing cost, rather than repeating
the inconclusive transport matrix. Source-backed bottom-right attention and
negative-slot cache semantics motivate the candidate; actual service and
independent metadata replay validate it. Semantic setup verifies631488 active
FP16 hidden elements bit-identical against compact unpadded query metadata at
the same total tensor shape. Default untraced single-client qualification adds
160 real requests/5200 exact frozen-upstream tokens, with no broader timing claim.
The complete160-cell/four-condition/two-model matrix passes10240 measured
requests/332800 tokens plus320 checked warmups. Qwen kernel primary packing
gain is0.158787ms with nominal paired t95[0.017962,0.299612]; other three
primary intervals cross0. All gen64/c8 TTFT intervals are positive, with
reported TPS/completion/TPOT tradeoffs. All packed transport TTFT/TPS intervals
cross0. Keep every outlier and distinguish real policy effects from eBPF gains. See [plan](../bench/results/prefill_packing_plan_20261012.md),
[plan review](../bench/results/prefill_packing_plan_review_20261012.md) and
[finding](findings/0033-prefill-packing.md). Preserve all ordinary unpadded
fidelity differences and actual batch trajectories. The goal remains active.


## Completed FIFO-prefix release

[Finding0034](findings/0034-completion-release.md) closes the supporting release
comparison after the [fresh combined result review](../bench/results/completion_release_result_review_20261012.md).
All160 cells/40 executors pass10240 measured requests/332800 tokens plus320
checked warmups. Strict coverage additionally passes4976 requests/177792 tokens,
all batch sizes and protocol/reuse/rejection/lifecycle controls.
Gen1/c8 serial-minus-prefix TTFT gains are Qwen kernel6.225782ms
[6.106539,6.345024],native6.371787[6.025879,6.717696];Smol kernel5.159548
[5.107920,5.211176],native4.925218[4.701560,5.148875],nominal paired t95 df4.
Request-joined releases/prefills support the scheduler mechanism in each primary
cell. This common benefit is not eBPF-only. C1 and long-output tradeoffs,opposing
transport exceptions,FP16 sequence divergences and host OOM/bootstrap unequal
exposure remain in the complete result; no clean-host/universal advantage follows.

The ordinary adapter adopts the exact qualified packed/prefix policy after
fresh review. All12 mapped binaries rebuild; real untraced default c1 edge/gen1/64
checks pass160 requests/5200 frozen-upstream tokens. Explicit packed-serial and
grouped-serial controls remain; current driver mappings preserve their roles.
No source-math change or transfer of traced timing to untraced serving follows.
Run valid/complete,narrow observed prediction supported,role supporting,
paper impact mechanism/workload boundary. Close the unchanged matrix; full
retained acceptance remains open for broader dynamic-untraced/CPU/general
backend/service evidence. Do not count build/archive/checks as new paper results.


## Ordinary untraced comparison

[Finding0035](findings/0035-default-untraced.md) and the
[fresh combined review](../bench/results/default_untraced_result_review_20261012.md)
close the current ordinary adapter comparison. All20 executors/80 cells pass5120
measured requests/166400 tokens plus160 checked warmups; strict2488 requests/
88896 tokens/1036 intended rejections complete. Initial ensurepip/log-variable
failures remain separate,with fixed reference values and actual repaired source.
Pre-observation complete sequence sets independently derive from finding0034.
Every output passes exact prompt/gen whole-sequence membership. This qualifies
finite output-set/lifecycle fidelity with unchanged production code,not current
unobserved batching replay,task quality or batch invariance.

All four primary untraced kernel transport TTFT1/c1 and TPS64/c8 nominal paired
intervals include0. Qwen gains-0.022742ms[-0.066119,0.020636] and-3.079500tokens/s
[-16.750507,10.591507];Smol values and every secondary are in the complete
finding/raw/review. Run valid/complete;prediction inconclusive;role supporting;
impact implementation/workload boundary. Earlier traced scheduler gains remain
separate. Close this unchanged ordinary matrix; no general superiority,
equivalence,total CPU/energy,physical-NIC or arbitrary-service claim follows.
