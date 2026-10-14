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

## Chained device-dispatch candidate

[Finding0036](findings/0036-tail-chain.md) integrates an opt-in scheduling
candidate that uses1 device launch/model-step instead of2 while reusing the
same upstream computation and transports. Fresh plan review admits the causal
A/B; eight strict executors finish4976 requests/177792 exact independently
replayed tokens,2072 intended rejects and40000 empty connects,all batch sizes.
Traced real preflight passes160 requests/4192 tokens. The complete ordinary
untraced four-condition matrix passes40 executors/160 cells/10240 measured
requests/332800 tokens plus320 checked warmups. All eight predeclared primary
TTFT1/c1 and TPS64/c8 candidate-gain intervals cross zero, as do recorded
secondary/control intervals. Preserve negative throughput estimates and close
this unchanged candidate; ordinary separate dispatch remains the default.
Finite-set fidelity does not reconstruct unobserved batch trajectories. The
first baseline setup's global-OOM/NotReady window stays archived. The [fresh combined result review](../bench/results/tail_chain_result_review_20261012.md)
admits valid/complete supporting evidence with an inconclusive prediction.
Owned runtime/build output is removed with final restoration receipt; no
default-adoption/general speedup follows.

## Stock io_uring TCP feasibility

[Finding0037](findings/0037-stock-io-uring.md) closes a component diagnosis,
not a paper performance experiment. The original RTX5090/Linux7.3rc3 supports
GPU-written NO_MMAP SQPOLL SEND/RECV queues. Idle SEND alone stalls; a pending
receive completion wakes the poller. Eight cold request/reply cycles deliver
32768 exact client bytes,256 consumed send completions and GPU-observed EOF,
with no runtime explicit userspace wake or network calls. Initial bootstrap/
compile failures remain archived. Root self-review reconstructs actual bytes,
queue counters and syscall counts; no independent experiment review is claimed.
Production eBPF/model/module source and defaults remain unchanged. Complete
accept/FD/sockmap/HTTP/model integration and CPU/performance value remain open.

## Finite io_uring/sockmap real-model integration

[Finding0038](findings/0038-io-uring-sockmap-models.md) qualifies a temporary
single-connection/gen1 integration with unchanged eBPF admission and HF
computation. Qwen/Smol each deliver12 exact pre-observation oracle tokens via
GPU-owned ACCEPT/RECV/SEND/CLOSE,without bfusion_tx. Kernel completion eBPF
reclaims reservations,avoiding unsupported GPU/CPU map RMW. Fragmented binary/
HTTP,prompt1..64,cold wake,reuse,EOF and terminal all-FREE/reserved0 pass.
After-ready native all-thread network/wake calls are0. Initial compile and
post-delivery reporting failures remain; Qwen is preserved rather than rerun.
Root replay self-review passes; no independent experiment review or timing
claim. Fixture completion tags/connections/output length are finite; broader
streaming/concurrency/abort ownership and performance remain open. Production
source/defaults are unchanged,and owned temporary runtime/pins are removed.

## Finite io_uring real-model streaming

[Finding0039](findings/0039-io-uring-streaming.md) extends the same temporary
path to exact1/64-token outputs,Qwen/Smol12requests390tokens each. Full greedy
HF sequences freeze before observation; all780 served tokens match. Each long
request records63 intermediate sends and one tagged final send; actual clients
receive42–64 body chunks. BPF recycles only final complete sends,with all
slots FREE,reserved0 and normal GPU EOF/CLOSE. Native after-ready networking/
wake calls are0. Root replay self-review and both drivers/pipeline pass0; no
independent result review or latency/throughput/CPU benefit follows. Production
source/defaults remain unchanged. Concurrent/general ring ownership,abort/
backpressure/rejection and optimized-backend integration remain open.

## Multi-connection io_uring implementation

[Finding0040](findings/0040-io-uring-concurrent.md) adds the optional normal
HF build target and actual-ring correlation,with PID-namespace repair and
a foreign-ring negative control. Both models pass24 mixed/eight-client
requests780tokens and24 all-gen64 requests1536tokens each. Lifecycle and
fresh production artifacts pass rejection/reuse,RST and in-flight SIGTERM,
all slots FREE,reserved/pending/error0. Across repaired preflight/eight runs,
5218 complete tokens plus8 prefix tokens are checked; abandoned outputs stay
separate. Source versions/initial failure remain. Root self-review and public
build tests pass; default loader creates no new hooks/maps. No timing/CPU or
independent-review claim. Optimized-backend integration and matched benefit,
overload/backpressure/partial-send/device-error/extended operation remain open.

## Optimized stock-TCP integration qualification

[Finding0041](findings/0041-vllm-io-uring.md) connects the shared GPU-owned
io_uring transport to unchanged upstream packed/prefix vLLM computation. Both
models pass622 strict requests/22224 independently replayed valid tokens each,
all batches1..8, wrap/mixed/pipeline-half-close/rejections and teardown. Final
ring/BPF counters have no drops, pending work or reservations; all native
serving network/wake syscall counts are0. Initial Qwen mixed-workload timeout
at607 requests stays separate; no missing-request drop count was captured.
Shared EOF/FIFO-final repairs also pass the unchanged two-model HF lifecycle
driver. Root reconstruction passes; no fresh independent scientific review
or performance/CPU/novelty claim. Role dependency-only, necessary setup for
the next matched optimized transport comparison. The existing module default
and original Workspace/base runtime/WIP remain unchanged. Temporary runtime
retained for the following benchmark, with post-run no-process/module/pin
evidence; complete resource removal remains pending that benchmark.

## Completed optimized stock transport comparison

[Finding0042](findings/0042-vllm-io-uring-performance.md) closes the reviewed
local ordinary-serving comparison with unchanged optimized compute. Real
preflight and six ordinary strict executors pass before frozen e709293 full
collection. All36 executors/144 cells/9216 measured requests/299520 tokens plus
288 checked excluded warmups complete without failed/excluded/retried timing
cells. [Fresh independent result review](../bench/results/vllm_uring_performance_20261013/result-review.md)
reconstructs raw schedules, output-set membership, arrival metrics, counter
arithmetic, mechanism engagement and paired effects; both analyzer replays
match archived stdout exactly.

Four nominal six-block primary effects favor stock when positive: Qwen TTFT
-0.040512ms[-0.109705,0.028680], Smol +0.081197[-0.025390,0.187784]; Qwen
TPS -155.453340[-289.449821,-21.456859], Smol -69.722741[-344.364089,204.918607].
Qwen long throughput contradicts gain; other primaries are inconclusive, not
equivalent. Report all four, with no familywide/SOTA claim.

Secondary known-worker CPU64/c8 is stock14.212284/native0.442915ms per request
for Qwen and12.040271/0.394414 for Smol. CPU brackets include process threads
with actual SQPOLL once plus separate module TX where present, not all Linux
networking or total service CPU. Stock cost rises approximately32/31 times;
absence of userspace socket calls does not remove kernel CPU work. BF_TRACE
model tracing is off, while stock's first128 network diagnostic records and
aggregate counters remain measured implementation costs. Complete-output-set
fidelity is weaker than replay of the current unobserved batch trajectory.

Run valid/complete, hypothesis inconclusive overall with a negative Qwen
throughput cell, research value supporting, impact mechanism/workload boundary
and additional local evidence. The separate cross-node question is unchanged.
Close this matrix and retain the module default/optional stock path. Removing
repeated prefix copying is a specific next transport candidate; this run does
not establish the cause of the throughput loss. No unchanged rerun or
model-specific arithmetic campaign is justified by these results.

[Final restoration](../bench/results/vllm_uring_performance_20261013/final_restoration.json)
removes the test runtime and26 owned build outputs after review, with no own
model process/module/pins/GPU app and original boot/base/Workspace/Coder/WIP
retained. Actual raw, package/build/source/commands, frozen references,
qualification, bounded journal and endpoints remain retrievable.

## Incremental stock output-copy investigation

[Finding0043](findings/0043-uring-incremental-copy.md) tests whether skipping
fully sent prefixes improves ordinary gen64/c8 stock throughput, retaining the
local question and matched upstream compute. Native TCP is the main mechanism
alternative; the former full-copy loop is an ablation. Role supporting, with
setup/strict/lifecycle work dependency-only. Source intervention is small and
not answered by0042; SQPOLL/wakeup and optimized cross-node serving remain
higher-level open costs after this one comparison. Plan and fresh review are
linked from the finding. Initial half-close control failure and subsequent
passing diagnostics/stress are retained; cause unresolved. At that point qualification and timing were incomplete; the completed
comparison and verdict are recorded below.

A source-native HF idle reproduction subsequently captures genuine RECV
EAGAIN wrongly treated as connection death. Both copy conditions now share
EAGAIN/EINTR rearming, with all affected qualification rerunning. Final plan
follow-up retains the hypothesis and matched repaired full-copy ablation;
0042 historical means cannot measure this copy intervention. Repaired
three-path preflight, all twelve traced/ordinary strict executors and both
original HF lifecycle workloads pass. A later repeated-idle regression still
stalls before admission. A read-only psock snapshot captures divergent receive
cursors; a temporary same-socket ingress redirect passes both model idle
regressions. All twelve traced/ordinary protocol executors then pass with
the redirect candidate. The same redirect is adopted in production source;
both model default module compatibility workloads and final copy preflight pass. The subsequent completed matrix is reported below; none of this
dependency work itself establishes a throughput effect. Raw failures, diagnostics
and candidate passes are linked from finding0043.

The complete copy matrix now finishes36 executors/36 cells,9216 measured
requests/589824 tokens plus288 excluded checked warmups. All four primary TPS
intervals include zero for candidate/native and candidate/full-copy across
both models:tested hypothesis inconclusive, research value supporting, paper
impact local mechanism/workload boundary. Known-worker stock CPU remains
roughly27/30 times native. Exact values, all blocks, fidelity limits, commands
and fresh independent review are linked from finding0043. Close this comparison;
prioritize measured polling/wakeup costs or optimized cross-node delivery
instead of repeating unchanged copy cells or tuning model arithmetic. General
reliability, total CPU/energy, external SOTA and arbitrary-model claims remain
unproven. The late endpoint observation is separately dated from actual timing.

## Sleepable eBPF io_uring loop comparison in progress

[Finding0044](findings/0044-uring-bpf-loop.md) follows the high known-worker
CPU observed in finding0043 with an admitted supporting transport intervention.
The [plan](../bench/results/uring_bpf_loop_20261014/plan.md) and
[fresh plan review](../bench/results/uring_bpf_loop_20261014/plan-review.md)
retain the ordinary packed/prefix adapter's local question and compare the
same upstream model computation against efficient native TCP, with current
SQPOLL as a component control. No formal paper RQ is introduced.

The candidate uses upstream sleepable struct_ops, DEFER_TASKRUN and a standard
multishot timer; these change together, precluding exclusive eBPF/syscall/
polling attribution. Three primary paired effects/model cover gen1/c1 TTFT
against native,gen64/c8 TPS against native and gen64/c8 known-worker CPU
against stock. All six intervals will be reported; the latter excludes Linux
network work outside the process and is not total CPU or energy.

Third/final real preflight passes120 requests/3144 checked tokens across
three paths,with normal exit/analysis0. Two failed preflights are retained.
All12 vLLM strict executors pass7464 requests/266688 valid tokens,
3108 expected rejects and60000 empty connections. HF idle/lifecycle
qualification passes32 requests/652 complete/prefix tokens per model after
repairing an omitted launcher mapping that selected the default library
before requests. Failed initial records and successful affected retry remain.
Full qualification is complete;36-executor/144-cell timing remains pending. These checks have dependency value only; no new speed
or CPU claim follows.
Next decision depends on full matched effects and fresh result review;
backend arithmetic, reference sets and the retained project objective stay
unchanged.
