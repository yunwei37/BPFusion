# Fresh result review: reused AMK serving experiment

Observation: 2026-10-14. Fresh independent review of the completed experiment; production files, model arithmetic, oracle, experiment matrix and infrastructure were not changed. The report is written only into the experiment's existing owned temporary directory.

## Separate judgments

- Run status: **valid for the predeclared finite frozen whole-output-set serving/performance comparison**. The full matrix is complete. Exact eager-HF equivalence remains failed and must not be advertised as passed.
- Tested hypothesis: **contradicted in the tested implementation and workload**. This reused AMK graph backend reduces neither primary latency nor primary throughput relative to current optimized vLLM loop; its kernel-loop transport also loses to its same-computation efficient native TCP control.
- Research value: **supporting**. The integration establishes a reusable backend option and supplies a meaningful negative backend/control comparison. Native CUDA compilation, graph API probes and packaging alone remain dependency work.
- Paper impact: **mechanism or workload boundary**, with additional evidence toward the retained performance/reuse question. This is not a direct thesis challenge to arbitrary eBPF services or every possible fused backend.
- Next paper decision: retain optimized vLLM as the measured faster backend and describe AMK as an optional qualified finite-set integration, with its exact diagnostic failure and large performance losses visible. Close this unchanged candidate performance matrix; do not launch favorable repeats or a model-specific arithmetic tuning campaign. A causal concurrency discriminator is optional and requires its own scientific rationale.

The retained question is whether an existing whole-model backend can reduce serving latency/increase throughput while preserving real checkpoint semantics and autonomous Linux TCP/eBPF service. No formal RQ was invented or renamed. This experiment does not establish the full project's generic text/model/SLO/performance acceptance.

## Reviewed evidence and independent checks

Read plan.md and the complete plan-review.md (ADMIT and same-review clarification), integration-execution-notes.md, qualification-notes.md, frozen references and source records, failed and successful native/device graph probes, strict eager-HF failure, protocol/lifecycle adapters and raw receipts, matched serving/analysis drivers, full command/wrapper/raw/analysis/exit records, actual AMK bootstrap/builder, unchanged qwen_graph dispatcher and existing network implementations, vLLM bootstrap/capture source, build/runtime logs and four full actual-host observations.

Authoritative archive: /workspaces/repository/bench/results/megakernel_reuse_20261014.
Frozen source: 1b84139575541d989588aa5b99ac078a0f3f397e.
Upstream AMK: 884534c4d2dbed4381576f81a79ae97feca53c34.
Checkpoint: HuggingFaceTB/SmolLM2-135M revision93efa2f097d58c2a74874c7e644dbc9b0cee75a2.

Independent Python arithmetic, separate from matched_analysis.py, checked:

1. Full metadata embeds actual driver/client/vLLM backend/native/AMK backend/builder/dispatcher bytes equal to the current frozen files.
2. The AMK frozen_references.json is byte-identical to the pre-observation0045 artifact, not a newly candidate-generated pool.
3. Every one of3960 complete outputs matches an independently established allowed whole sequence; no tokenwise mixing is allowed.
4. All arrival-derived TTFT, completion and TPOT fields, all60 per-cell first/last timestamps and throughput, and all60 worker CPU brackets are consistent with raw records.
5. All12 aggregate latency means/nearest-rank p50/p99 rows and all52 paired differences/nominal t95 intervals recompute. The analyzer uses t4=2.776445105, the usual critical value rounded; this has no material numerical effect.
6. Protocol cases independently have622 requests/path,259 rejected/path and22224 output tokens/path, with independent frozen output membership.
7. All103 upstream py/cu/cuh/cpp/h files still equal the pinned tar archive bytes.

I did not rerun serving, alter an oracle, recapture a model graph or manufacture missing performance records.

## Completion and exclusions

Full raw ends terminal exit0 at2026-10-14T08:55:35Z. It has15 starts,15 ready records,15 actual executor exit0 records,15 verified records and15 successful executor-terminal records; no failure event. Five process blocks contain all three paths, all four(gen,c) cells,64 measured requests/cell. There are3840 measured requests and124800 measured output tokens, plus120 checked excluded gen1 warmups (8/executor). No failed baseline is counted as a candidate win.

The three-path order is the first five permutations of the declared mode order; same-AMK relative order is3/2, as documented. Cell order rotates by block; all paths within a block use the same cell order. Prompt selection is identical by request index. Gen64/c8 lanes align prompt index modulo4, an inherent fixed workload structure shared by all paths; this is not a broad distribution of natural arrivals.

Full source was frozen before collection, and the command explicitly invokes that archived matched_serving.py with the common runtime and fixed reference path. Independent preflight covered all three paths with40 requests/1048 tokens each and max-active8 for both AMK paths. Earlier base-runtime c1/c8 smoke checks are dependencies, not appended as performance repetitions. Protocol and lifecycle qualification precede full collection. Neither failed setup nor strict diagnostic output was silently removed.

Finite reply diagnostic buffers store128 entries. Every full loop executor records264 requests and trace_overflow136. This is explicitly accounted diagnostic truncation, not SQ/CQ overflow, packet loss or missing client samples. Full client metrics and complete outputs remain recorded for every request. Per-request kernel reply-event auditing is consequently incomplete after128 entries and must not be claimed complete. vLLM model trace_overflows0 with ordinary tracing disabled is not proof of current trajectory replay.

## Actual computation and autonomous mechanism

Both AMK transports use the same original persistent AMK cubin/program, cpasync0 variant, eight private banks, discovered170 SM schedule, graph tables and qwen_graph resident dispatcher. The default upstream target named rtx5090 describes an82-SM laptop; the integration discovers actual card SM count instead of using that wrong geometry. Earlier82-SM dependency probes are not mixed into the170-SM timing matrix.

amk_graph.py performs checkpoint loading, graph lowering, table initialization, cubin extraction and graph construction at bootstrap. Each bank has190 unique raw graphs. The builder assembles the unchanged upstream POD, patches actual request token IDs on-device, sequences request-time prefill model calls at positions0..prompt-1, then decodes at the corresponding positions. Outputs are sampled by upstream AMK and converted to the existing int64 graph-result ABI. No request answers or precomputed prompt KV replace computation.

The integration deliberately uses upstream persistent K=1 nodes per token so existing dispatcher system-scope produced/DONE and final-CQ ownership remain valid. It is NOT AMK's advertised single finite K-token launch throughout a whole request. Safe per-token publication is integrated, but any claimed whole-generation launch elimination or ideal AMK K-token performance would exceed this evidence.

Dispatcher acquires shared queue state, copies real prompt input, launches each private child graph and tail-resumes after its child graphs finish. It publishes output then produced with a system fence, holds final completion until FIFO reclamation, and preserves private KV ownership across slot reuse. Source and recorded launches1, device_graph_launches8328, graph_error0, banks8, max_active8 for every AMK full executor establish actual device-controlled model work; all eight argument-update error cells are zero.

Loop attaches real sockops/parser/verdict and sleepable io_uring struct_ops, maps kernel/GPU shared state and runs a separate io_network GPU kernel. It has no custom bfusion_tx module. Qualification syscall traces after readiness and before shutdown show zero accept4/recvfrom/sendmsg and one io_uring_enter for loop; efficient native engages these network syscalls and epoll_pwait2. This is meaningful autonomous-path evidence, not absence of all CPU/kernel work. Kernel TCP, BPF loop/timers and deferred task work still consume CPU.

All full loop runs have accepted=closed19, head=completed=received264, pending/error/reserved/dropped/overflow0, independent SQ head=tail and CQ head=tail. Native has published=completed264,rejected0. Final BPF stats show reserved0 and every slot free. Normal shutdown/cancellation and detach are recorded. The paths really engage their intended mechanisms.

max_active8 denotes eight active private child graphs/requests; it does not prove eight cooperative model kernels execute simultaneously or occupy particular SMs.

## Correctness scope and failure receipts

The fixed pool was established before AMK observations from independent HF/upstream trajectory replay, precisionfp16, checkpoint-specific prompts/whole sequences. It contains17 Smol prompt/gen entries, each with one or two whole alternatives. The plan already allowed this independently computed finite set. This is not a circular answer-from-candidate oracle.

All AMK measured gen64 outputs are stable per prompt and identical across the two transports. vLLM has two allowed whole alternatives on two of the four gen64 prompts; three-path numerical trajectories are therefore not byte-identical for every request. Identical checkpoint/precision/prompts/gen budget and independent allowed outputs make this a bounded practical backend comparison, not identical arithmetic/history evidence across AMK and vLLM.

A stronger independently recomputed eager-HF exact diagnostic remains FAILED: third long output diverges at zero-based index16 (17th token). Both official170-SM AMK per-step and finite persistent native calls exactly reproduce the server's divergent sequence, and that sequence is already in the old pool. This localizes that example's discrepancy to a reproducible computation-backend difference rather than a newly networking-created result; it does not establish the numerical cause, guarantee all server histories, or repair exact equivalence. Native diagnostic was on the earlier base runtime, while the final common-runtime full run checks the fixed pool. No new common-runtime exact trajectory/logit parity claim follows.

Retained failures include original F32 official example host C++17/Torch C++20 incompatibility, failed initial CUDA graph dependency signature build, direct device graph probe wrapper reporting801 (precise origin not independently established), non-executable first strict launch, stronger eager-HF mismatch, and first native lifecycle predicate passfalse. Parent-graph probe subsequently validates actual GPU scalar patching; CPU-preloaded prefix in that probe alone is not request-time GPU-prefill proof. Actual server/protocol evidence supplies the latter.

Protocol qualification preserves fragmentation, prompt lengths through64, concurrency1..8, mixed lengths, wrap/reject cycles, invalid first/last tokens, pipelining, half-close and binary reject/after-reject cases. These cover44,448 output tokens and1,244 requests across the two AMK paths. Lifecycle has eight2.2-second idle gaps, invalid HTTP/binary handling, reset after first token, a later whole output, and stop while generation/receive/accept are pending; both final paths pass with zero graph/update errors and removed own pins.

Lifecycle adapter changes the older exact lifecycle oracle to the explicitly declared fixed pool; partial abort/stop checks compare a prefix of one already-frozen whole sequence. This is a documented weaker numerical scope, not stronger current-trajectory equivalence. The first native lifecycle predicate incorrectly expected32 completed transmissions despite stopping the final output after one token. Source userspace loop stops before CUDA quiescence, so published32/completed31 is the appropriate count for that workload. Archived diff shows the repair changes only expected completion and output directory, and repeats the affected native workload; loop cancellation semantics appropriately differ.

## Baseline and runtime fairness

Same-AMK native is a credible efficient transport/control alternative, not a Python per-token loop. It uses the same resident GPU dispatcher/model graphs/private-bank policy, with60us epoll_pwait2 completion waiting. Loop differs in queue mapping, compiled transport/dispatcher library, additional GPU network kernel, BPF/io_uring progress and TCP handling. Model compute kernel/program matches, but full serving GPU workload and compiler output do not. An AMK-loop/native difference can be assigned only to these implemented serving/control alternatives collectively, not eBPF instruction cost or TCP alone. Possible model/network scheduling interference remains part of the measured design, not an excluded excuse.

vLLM loop is the current optimized BPFusion reusable vLLM graph backend, not a stock vLLM HTTP endpoint. It retains captured tensor batches1..8, queries1..64, padded prefill and prefix release. Bootstrap uses128-context eight-slot protocol sizing and65 KV blocks (23,961,600 cache bytes); it is not artificially forced into batch1 to favor AMK. AMK uses eight private model/buffer banks and no tensor batch aggregation, an inherent backend integration policy difference, not equal memory-footprint or equal GPU scheduling across backends. These practical computation differences prevent an AMK/vLLM contrast from isolating fusion alone.

All three final paths use temporary Torch2.13.0+cu129, Transformers5.17.0, vLLM0.31.0. Base packages remain unchanged. nvcc13 builds AMK source/builder; current vLLM host bridge deliberately links the qualified CUDA12.9 runtime. Same Torch version is not identical backend CUDA runtime/machine code. The deviation is explicit and supports a runnable practical-backend contrast; it cannot support a controlled compiler-only explanation.

The current vLLM baseline executes and completes normally, with full outputs independently accepted, actual model/capture metadata, root launch and device graph counts, admitted=retired264, max_active8 and release max8 in every executor. There is no evidence of a baseline launch/interface failure that could create a spurious candidate win. Bootstrap time, JIT cost, total graph/model memory and source-preservation receipts are outside measured TTFT/TPS and should be stated separately where relevant.

## Independently recomputed primary results

Means below aggregate five equal64-request cells; throughput is the arithmetic mean of each process cell's token count divided by first-send-to-last-token-arrival span.

| Path | gen1/c1 TTFT ms | gen64/c8 output tokens/s | gen64/c8 completion ms | gen64/c8 TPOT ms |
|---|---:|---:|---:|---:|
| AMK eBPF/io_uring loop |18.359762|158.094137|3227.807292|49.509141|
| Same AMK native epoll |18.245999|303.376970|1681.171440|25.667830|
| Current vLLM loop |1.157729|5352.502809|95.613233|1.488971|

Nominal95% paired t intervals across five PROCESS blocks (df4):

| Primary loss for AMK loop | Mean | Nominal95% interval |
|---|---:|---:|
| TTFT above same-AMK native, ms |0.113762|[0.082157,0.145368]|
| TPS below same-AMK native, tokens/s |145.282833|[144.512548,146.053118]|
| TTFT above current vLLM loop, ms |17.202033|[17.129829,17.274236]|
| TPS below current vLLM loop, tokens/s |5194.408672|[4919.608412,5469.208932]|

All four primary signs are negative for candidate in all five blocks. AMK-loop TTFT is15.86x current vLLM; long c8 throughput is52.11% same-AMK native and2.954% current vLLM. These large negative results cannot be presented as null benefits or eBPF speedups.

No warmups or failures enter these primary statistics. Five-block t intervals are nominal, assume block differences are suitably behaved, and provide neither familywise guarantees nor representative-tail/SLO evidence. Request-level sample counts do not create320 independent experimental replicates. Client arrivals timestamp a recv chunk; several tokens can share one timestamp. Throughput is closed-loop on localhost with pre-opened connections, not offered-load capacity, a cross-node network claim or tokenization-inclusive latency.

## Secondary evidence and CPU accounting

Other cells remain visible:

| Cell | AMK loop TTFT ms / TPS | Native AMK TTFT ms / TPS | vLLM loop TTFT ms / TPS |
|---|---|---|---|
| gen64/c1 |18.360066 /164.203653|18.253511 /165.099036|1.142646 /1350.398771|
| gen1/c8 |146.525321 /54.471042|136.578962 /58.421892|2.046907 /3635.925134|

Long c1 AMK loop completion389.720911ms versus native387.606368ms; paired completion loss2.114543ms. Long c8 completion loss1546.635852ms and TPOT loss23.841311ms. Gen1/c8 TTFT loss9.946359ms. AMK does not have a favorable hidden secondary tradeoff in these metrics.

Known-worker CPU ms/request, cells gen1/c1,gen64/c1,gen1/c8,gen64/c8 respectively:
- AMK loop:0.469528,9.881195,0.470225,10.256919.
- Native AMK:0.356263,7.470731,0.347875,4.447109.
- vLLM loop:0.045912,1.622923,0.017271,0.455297.

The raw POSIX executor process CPU clock includes all process threads and kernel time charged to them. Before/after sampling fully brackets every cell, including some synchronization/teardown overhead. Kernel TX counter is0 because the custom module is absent, NOT because kernel TCP/BPF/io_uring costs are zero. Interrupts, softirq, other kernel tasks and all host/client CPU are not fully attributed. Thus the measured implementation also loses in known-worker CPU, but total CPU/energy conclusions remain unsupported.

## Environment and causal limits

Actual host records at08:41:45(before),08:48:28(mid),08:50:01(mid2),08:56:18(after) have the same boot ID04dc0087-5ccc-4c46-9997-b9a92f0e5167 and the same11 historical selected NVRM refcnt warnings (last06:42:21). No newly selected Xid/OOM/storage fault appears in these cumulative brackets; before/after compute-app queries are empty. Mid observations show a python GPU process; mid2 ownership maps host1642322 to namespace315127, original Workspace cgroup and the actual AMK loop executor. Earlier sampled host1639491 is gone when separately checked, so its ownership is unproven. Do not claim a continuously isolated GPU or harmlessness of prior warnings.

The known earlier05:28 OOM is outside this full window; it is not a reason to discard these rows. Discrete fault queries and shared-host memory/GPU snapshots bound environmental evidence but do not rule out unsampled interference or establish repeatability on another host.

Post-run resource inspection is source/compiler evidence only: persistent model REG106/STACK256/staticSHARED34448, separate GPU io_network REG40/STACK768/staticSHARED0, dispatcher REG38/staticSHARED0. These facts and the native c8 throughput increase versus loop's lack of increase make scheduling/co-residency a plausible competing explanation. They do not prove occupancy, simultaneous execution, causality, CPU bottleneck, memory-bandwidth limitation or scheduler serialization. Likewise steady ~18ms AMK TTFT is not independently decomposed into math, prefix graph chaining, cooperative synchronization or queue/network wait. No causal timeline was measured.

## Evidence defects and publication boundary

No defect invalidates the completed finite-set practical comparison. Material limits that must remain explicit:

- Exact eager-HF diagnostic is failed, not repaired by frozen-set success; generic semantics, arbitrary models and unobserved batch/KV trajectories remain unproved.
- Whole-request AMK K-token launch is replaced by K1 graphs; this is an integration of whole-model computation, not the ideal finite single-launch generation claim.
- Same-AMK transport comparison adds GPU networking and different compiled glue. It does not isolate only eBPF or TCP.
- vLLM and AMK use different computation/batching/memory/runtime linkage, so backend differences are not a pure fusion ablation.
- Full diagnostic reply traces truncate at128 entries/executor; complete client data survives.
- Discrete host brackets are not continuous isolation, and one transient mid GPU process's ownership is unverified.
- TTFT excludes connection creation/bootstrap/tokenization; no remote-network/SLO/total-CPU/task-quality result.
- Archive commands refer to an owned temporary runtime/source tree; clean reproduction must recreate that setup and point output paths to a fresh location. Existing archived analyzer paths support result replay directly; deleting TEMP must not be represented as leaving a ready installed AMK service.

The hypothesis's positive performance prediction is contradicted locally. Numerical fidelity strong enough for this fixed independent pool was obtained; exact semantic equivalence is not. The paper should retain these as two separate conclusions instead of asserting broad correctness or treating this optional backend as a production default.

## Optional next causal discriminator

If understanding the large c8 transport loss has higher decision value than another reusable backend, a newly justified matched timeline/co-residency control can distinguish model execution slowdown caused by the additional resident GPU network kernel from network progress/reclamation delay. It should retain exact same AMK arithmetic, request budgets, independent output checks and the observed negative matrix, and measure rather than infer model overlap/wait. This is a suggestion, not authority to start another experiment or require new infrastructure.

The result alone does not justify arithmetic edits, timer sweeps, more unchanged repeats, oracle expansion or a general conclusion that eBPF offload cannot help. It does justify keeping the faster vLLM backend, publishing the bounded AMK tradeoff honestly and routing subsequent work toward a distinct load-bearing uncertainty.
