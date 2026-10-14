# Independent RESULT REVIEW — coalesced GPU network progression

One fresh reviewer under research-experiment-design RESULT REVIEW. Read-only source, raw-data, native disassembly and offline numerical review in the original Workspace. No source/plan edit, new build, serving/GPU experiment or publication action by this reviewer. Only this report is written. Paths below are relative to /tmp/bpfusion-coalesced-network-0pls_22b unless explicitly named otherwise.

## Separate judgments

- Run status: **valid and complete for the declared finite shared-host comparison**. All 45 executors/180 cells terminate successfully with raw correctness, counters and metric reconstruction matching. The missing in-run host observation is a disclosed monitoring deviation that limits environmental attribution, rather than erasing terminal/client evidence.
- Tested hypothesis: **contradicted as a common-driver preservation claim, with narrow AMK recovery supported**. Coalescing recovers most AMK gen64/c8 throughput loss but retains a native gap, worsens AMK gen1/c1 latency, and regresses both current vLLM gen64/c8 transfers. This is the predeclared mixed outcome and blocks a universal default.
- Research value: **supporting**. A new actual implementation discriminator after0049; qualification/build/provenance is dependency work only.
- Paper impact: **additional retained-question evidence with a constructor/backend/workload boundary**. The repository has no formal paper RQ or thesis contract. No direct thesis challenge or proof of0049 overlap mediation follows.
- Next paper decision: report the common-driver tradeoff, keep coalescing an explicit optional experimental path, and retain efficient native/current optimized vLLM as competing delivery evidence. Do not call this zero overhead, noninferior, a universal optimum, or completion of the generic Linux TCP/HTTP/eBPF/shared-queue/real-model/async-TX objective. Legacy compatibility evidence is a publication dependency, not an added primary baseline.

## Retained question and evidence reviewed

The approved plan asks whether advancing existing asynchronous network work from the GPU model dispatcher between model-graph rounds removes tested AMK c8 loss while preserving correct worker-free service and efficient current vLLM delivery. Its success/mixed/negative decisions are retained. docs/evaluation.md, finding0030 and findings0048/0049 preserve the objective: remove the CPU request path while retaining efficient reusable real-model GPU execution. This one finite component result cannot stand in for that whole goal.

Read plan.md and the whole plan-review.md/follow-up; full.command.json/full.source.json/full.exit.json; all 15 full_*_b*.jsonl; all 45 exact stdout logs, wrappers and driver receipts; matched_serving.py/run.py/analysis.py/full.analysis.json and analysis receipts; candidate/original CUDA/header snapshots and actual native loaders/client/shared sources; upstream AMK snapshot/archive; original/native/candidate build receipts and libraries; allthree selected qualification raws and vLLM graph/reference traces; allthree lifecycle byte-output/strace/source/receipts; both bounded mechanism traces/observers and receipt; actual full-before/late-observer host records; and later legacy compatibility artifacts. This is the one independent result review, without a desired verdict or another reviewer.

## Completion and commands

Source freeze is main6f15068d591f7e53469b233ae44799990866a5ea at 10:57:40.845029 UTC. Every full metadata commit matches; Workspace remains at that source during review. Full terminates11:21:02.742303 UTC, exit0. All 15 driver exits/raw terminals, all 45 executor exits/executor-terminal success records and wrapper terminals agree. Wrapper and all full driver stderr are empty. No failed full cell or substituted successful prefix is excluded.

Independent counting gives45 executors/180 cells/5760 measured requests/187200 measured output tokens plus 360 checked excluded gen1 warmups/360 tokens. Each executor has 136 replies/4168 tokens:128 measured/4160 tokens plus 8 warmups. Each cell contains 32 unique indices0..31. Startup, compilation, warmups, connection establishment, profiling and shutdown are outside the measured throughput window. A lane retains its TCP connection across its32/concurrency requests in the cell.

Actual outer wrapper is /usr/bin/python3 run.py full in /workspaces/repository; the plan's runtime-Python wrapper is an equivalent standard-library orchestrator. Every inner command uses TEMP/runtime/bin/python matched_serving.py --backend BACKEND --block B --loop-comparison --untraced --reference-path TEMP/frozen_references.json --model SNAPSHOT --output TEMP/full_WORKLOAD_bB.jsonl. All 15 frozen expanded commands equal the terminal commands. Actual starts select build/amk_graph or build/vllm_graph suffixed _uring_loop_original, _uring_loop_coalesced or _user_network_wait, same snapshot and300-second argument. Primary collection has no strace/profiler/BF_TRACE.

All paths inherit the same archived overrides: PATH to TEMP runtime and /usr/local/cuda/bin; PYTHONPATH pinned AMK884534c4; TORCH_EXTENSIONS_DIR owned TEMP cache; CUDA_HOME /usr/local/cuda; LD_LIBRARY_PATH owned TEMP libbpf; BF_BIND127.0.0.1; PYTHONUNBUFFERED1; VLLM_ENABLE_V1_MULTIPROCESSING0. Override/package/runtime receipts are preserved; no complete per-process dump of every ambient variable is claimed. Smol revision 93efa2f097d58c2a74874c7e644dbc9b0cee75a2 and Qwen revision 7ae557604adf67be50417f59c2c2f167def9a775 are pinned local FP16 snapshots. Four prompts match across transports per workload. AMK has 8 private banks, K1/cpasync0, actual/program170 SMs; vLLM keeps current optimized graphs/packing/prefix release/KV policy.

O=old loop,N=native,C=coalesced. Model/cell order reverses on odd blocks. Every raw start/cell matches:

|Block|Model order|Path order|gen/concurrency cells|
|---:|---|---|---|
|0|AMKSmol,vLLMSmol,vLLMQwen|O,N,C|1/1,64/1,1/8,64/8|
|1|vLLMQwen,vLLMSmol,AMKSmol|O,C,N|64/8,1/8,64/1,1/1|
|2|AMKSmol,vLLMSmol,vLLMQwen|N,O,C|1/1,64/1,1/8,64/8|
|3|vLLMQwen,vLLMSmol,AMKSmol|N,C,O|64/8,1/8,64/1,1/1|
|4|AMKSmol,vLLMSmol,vLLMQwen|C,O,N|1/1,64/1,1/8,64/8|

Five of six deterministic permutations are used, without randomization or perfect counterbalance. Missing C,N,O leaves residual order/drift confounding. Five process blocks, not5760 requests, are replication units.

## Baseline fairness and unchanged computation

Efficient native epoll is the single main competing mechanism. It actually engages, with136 published/completed and0 rejected per full executor. Compile guards exclude network GPU code. Its dispatcher SASS is identical to the old dispatcher within each backend. Candidate does not beat native on the AMK primary cell. This is a fair matched competitor, not a deliberately broken proxy.

Old loop is a necessary current-practice/component control. original_saved.json captures pre-edit main 82d31c8a1ac61d5d8be57119ab1684a90e4c23fd; allthree saved header/CUDA sources exactly match git show82d31c8. Actual old binaries were saved before shared-header changes. Makefile.original rebuilds those old snapshots, not the new refactored noncoalesced source. Loader selection uses unresolved argv0-derived .so names, so each _uring_loop_original start actually loads the original-named library despite a symlinked common Python loader.

Read-only cuobjdump independently verifies reconstructed originals equal saved old normalized SASS: AMK2 functions/2776 instruction lines, vLLM2/3872. This proves GPU dispatcher/network instruction identity, not whole-host ELF equality or universal model semantics. Original and candidate preserve the ordinary native build flags; vLLM retains BF_PAD_PREFILL/BF_PREFIX_RELEASE and existing CUDART linkage. AMK/vLLM compiler/CUDART differences prevent networking-only cross-backend attribution; within-workload comparisons are fair.

executor/amk_graph.py, executor/amk_graph.cu, executor/vllm_graph.py, executor/userspace_tcp.h, bench/resident_dispatch.py, bpf/uring_loop.bpf.c and queue ABI are byte-unchanged against82d31c8. All 181 archive files in the pinned AMK unpacked snapshot match upstream bytes, preserving full VM/arithmetic/source_cuda, not only an eBPF instruction fragment. All full metadata source/driver/client copies match their owning sources. No arithmetic optimization, parser/BPF/ABI/timer/queue relaxation or expanded reference explains the effect.

This changes state allocation/loading, bookkeeping residence, network launch/lifetime/progress cadence, admission timing and dispatcher footprint together. Realized vLLM batches can differ despite unchanged batching algorithm. This is a collective actual-driver intervention, not a pure occupancy intervention or identical observed trajectories.

## Metrics and uncertainty

Reviewer-authored independent offline arithmetic reconstructs all 180 cells from raw start_ns/arrival_ns: TTFT=first arrival-send; completion=final arrival-send; TPOT=(final-first)/(gen-1); TPS=tokens/(max final arrival-min send). All 108 effects and five block differences recompute and agree with full.analysis.json to <1e-9 absolute numerical error. Gen1 TPOT stays undefined. CPU deltas and enclosing brackets were independently checked.

TTFT/TPOT terminology agrees with the [official vLLM benchmark documentation](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics), checked during review. TPS denominator is the stated finite cell window, not official whole-run duration. Tokens in one recv share timestamps; no exact server token-spacing claim follows.

Intervals are nominal paired t95, n5/df4, half-width2.776445105*sd(d)/sqrt5. These describe process-block variation, with no request independence, multiple-comparison correction, randomized-host generalization, equivalence/noninferiority cutoff or SLO assertion. Positive latency is slower; positive TPS is faster. Primary labels follow the reviewed plan, without post-hoc selection. Primary/transfer tables and all secondary cells/contrasts follow below.

## Correctness and engagement

All 5760 measured outputs/360 warmups meet unchanged independent pre-observation0045 complete-output pools. JSON exactly matches retained AMK-residency/megakernel-reuse/CQ-progress assets, source 8323c32 and2026-10-12/13 timestamps/additional independent upstream replay sources. These are finite set-membership checks, not arbitrary-input parity/current untraced batch-KV correctness. No output-generated or expanded oracle. The stronger old AMK eager-HF gen64 greeting mismatch at token16 remains failed.

All full io_uring executors have 136 head/completed, accepted=closed, pending/error/reserved/dropped/overflow/aborted0, independent SQhead=SQtail/CQhead=CQtail, eight FREE queue slots/reservations0, graph_error0 and one host root launch. AMK has 4168 token steps/eight zero bank errors; vLLM admitted=retired136/trace_overflows0. Network diagnostic trace_count136/expected8 overflow beyond 128 is retained; it is not queue loss. All 45 separate stdout logs exactly match embedded raw executor stdout. Cleanup and detach records pass.

Selected candidate qualification: three actual executors,622 actions/22224 output tokens/259 intentional rejects plus 5000 empty connections each. Fragmentation, c1..8,256 wrap accepts/256 wrap rejects,32 mixed, pipeline halfclose/reject, binary reject and after-reject valid input are exercised. Both vLLM traces independently replay upstream history with physical-bank ownership/release checks, batch 1..8/query 0/1/2/5/8/15/16/17/32/64, terminal/overflows0. AMK stays pool-scoped. Strace after NET_READY shows io_uring_enter and no userspace accept/recv/send worker calls; this is observed process behavior, not zero host kernel work.

Allthree lifecycle reply_hex traces were independently decoded:32 rows/10 rejects/652 complete-or-prefix checked tokens each, HTTP/binary reuse, repeated2.2s idle, binary EOF, RST after first token and inflight SIGTERM with pending accept/receive. Exit0,13 accepted=closed,32 completions/3 intended aborts, zero model errors, all pending/error/reserved/drop/overflow0, empty independent SQ/CQ and no remaining owned pins. A stopped generation's valid first-token prefix is not a64-token completion claim.

Both bounded CUPTI/Torch traces show one io_initialize and one io_network after observed model execution. AMK4062 kernel activities/1048 selected token activities/596 dispatchers; vLLM191483 kernel activities/596 dispatchers. Network begins about 180.224/146.688us after last non-network activity and lasts32.608/29.696us, both 1x1 grid/block. Observer sources enable device-graph/HW activity before initialization. Evidence supports no independent steady network kernel during observed model execution and shutdown-only draining. It does not establish graph-node identity/bank-position/model overlap mediation or current untraced performance trajectories. Profiled timings are not primary data.

Source inspection retains all mutable connection/request/generation/timeout/cancellation state in durable IoState initialized once. io_progress runs on idle/admission and result paths and returns while cancellation awaits CQ. Root synchronization precedes model_quiesced/shutdown worker and host drain; freeing follows drain/device synchronization. Existing60us timeout/BPF loop rule remain. No discovered qualified-candidate defect invalidates this bounded result; no universal correctness proof follows.

## Code growth and legacy source impact

|Backend|Native/old dispatcher instructions|Candidate dispatcher|Old network|Shutdown network|Initialize|
|---|---:|---:|---:|---:|---:|
|AMK|768|2328|2008|1432|56|
|vLLM|1864|3536|2008|1432|56|

AMK dispatcher triples; vLLM grows 89.7%. Instruction counts are implementation evidence, not proportional runtime or eBPF-only performance claims. Bigger dispatch footprint/work, global state traffic, delayed CQ service during model rounds and changed admission/batching are competing explanations not causally separated here.

The shared-header refactor affects every BF_URING_NETWORK consumer even without BF_IO_COALESCED: IoState pointer/heap storage, separate synchronized initialization and persistent io_progress loop. The optional flag guards dispatcher progress and absence of steady launch, not the entire header refactor. Ordinary loop/SQPOLL/full-copy/loop-after targets may therefore differ from old code despite old names; native is outside header scope. The captured old full control remains valid and must never be swapped for a refactored rebuild.

Owning-agent legacy_build.exit.json and legacy_compat.exit.json now report successful actual ordinary refactored uring_loop checks for AMKSmol/vLLMSmol/vLLMQwen, terminal 11:40:07.279211 UTC,40 replies/1048 tokens each. Reviewer audited raws/commands/oracle/queues offline. This resolves the immediate ordinary-loop compatibility dependency in that finite scope. It is not another primary baseline, performance finding, full strict lifecycle qualification of every header variant or proof of all existing consumers. No all-legacy qualification claim is warranted.

## Health and remaining boundaries

Actual full.host_before.json10:57:32.829225 and full.host_late_observer.json11:33:04.653599 UTC are successful host lab GPU/journal reads, same boot04dc0087-5ccc-4c46-9997-b9a92f0e5167. Both contain identical33 historical NVRM status0x56 warnings, latest10:50:43 before full, with no new selected line by late observation. Recovery action None/no listed compute app; MemAvailable 116093676/120162848kB at endpoints. Driver 610.57.04/inherited400W versus575W default is recorded, not changed here.

There was no successful in-run host snapshot. Late observer follows full terminal 11:21:02 and cannot be renamed in-run. Owner may add full-after-review receipt; it is not yet certified here and cannot retroactively repair that gap. Selected warnings do not prove harmlessness, constant clocks/thermals, every-fault absence, host isolation or no shared activity. These are attribution/external-validity limitations; finite terminal/output evidence remains valid.

No blocking full-completion, arithmetic, engaged-main-baseline, relaxed-oracle or candidate protocol/lifecycle defect was found. Final publication/restoration/health records belong to the owner. Stronger failed AMK eager-HF parity, arbitrary prompts/models, capacity/SLO, total CPU/energy, overlap mediation, isolation and the complete retained serving objective remain outside acceptance. Useful next paper change is the backend-dependent common-driver boundary; no thesis/idea rewrite is triggered. Optional redesign needs a new discriminator and meaningful decision value, not unchanged timer/profile repetition. This review grants no experiment authority.

## Primary and backend-transfer results

|Workload|gen/c|Old TPS|Native TPS|Candidate TPS|Old TTFT ms|Native TTFT ms|Candidate TTFT ms|
|---|---|---:|---:|---:|---:|---:|---:|
|AMK Smol135M|1/1|54.349|54.747|52.938|18.368|18.233|18.855|
|AMK Smol135M|64/8|158.208|304.387|292.745|106.926|63.888|67.859|
|vLLM Smol135M|1/1|850.283|846.292|806.408|1.167|1.169|1.224|
|vLLM Smol135M|64/8|5592.135|5630.454|5070.858|1.810|1.828|2.041|
|vLLM Qwen0.5B|1/1|714.244|718.880|674.279|1.388|1.377|1.468|
|vLLM Qwen0.5B|64/8|4758.151|4806.615|4373.108|2.363|2.283|2.485|

AMK 64/8 TPS is recovery primary, native TPS/completion/TTFT measures remaining gap;1/1 TTFT is primary latency for allthree; vLLM 64/8 TPS/1/1 TTFT are independent transfers. Signed candidate-minus-control means [nominal df4 t95]:

|Workload|gen/c Metric|Control|Difference [t95]|
|---|---|---|---:|
|AMK Smol135M|1/1 ttft_ms|old|+0.487 [+0.464, +0.510]|
|AMK Smol135M|1/1 ttft_ms|native|+0.622 [+0.589, +0.655]|
|AMK Smol135M|64/8 tokens_per_s|old|+134.537 [+133.700, +135.375]|
|AMK Smol135M|64/8 ttft_ms|old|-39.067 [-42.665, -35.469]|
|AMK Smol135M|64/8 completion_ms|old|-1479.101 [-1484.477, -1473.726]|
|AMK Smol135M|64/8 tokens_per_s|native|-11.642 [-12.943, -10.341]|
|AMK Smol135M|64/8 ttft_ms|native|+3.971 [+0.591, +7.350]|
|AMK Smol135M|64/8 completion_ms|native|+66.283 [+58.896, +73.669]|
|vLLM Smol135M|1/1 ttft_ms|old|+0.058 [-0.002, +0.118]|
|vLLM Smol135M|1/1 ttft_ms|native|+0.055 [-0.015, +0.125]|
|vLLM Smol135M|64/8 tokens_per_s|old|-521.278 [-569.819, -472.736]|
|vLLM Smol135M|64/8 tokens_per_s|native|-559.597 [-627.946, -491.247]|
|vLLM Qwen0.5B|1/1 ttft_ms|old|+0.080 [-0.001, +0.160]|
|vLLM Qwen0.5B|1/1 ttft_ms|native|+0.091 [+0.028, +0.154]|
|vLLM Qwen0.5B|64/8 tokens_per_s|old|-385.043 [-411.625, -358.462]|
|vLLM Qwen0.5B|64/8 tokens_per_s|native|-433.508 [-471.168, -395.847]|

AMK TPS increases 85.04% relative to old mean TPS but remains 3.82% below native mean. These descriptive mean ratios are not extra causal/t-interval claims. Allfive primary TPS recovery/native-gap signs agree. Coalesced1/1 AMK TTFT is slower than both controls. Both vLLM 64/8 TPS losses agree in sign in allfive blocks versus each control; secondary completion rises 9.510/9.831ms versus old and9.948/10.607ms versus native. Both vLLM 1/1 TTFT intervals versus old straddle zero: unresolved, not demonstrated non-regression. Qwen1/1 TTFT versus native is positively resolved. Substantial AMK partial recovery plus vLLM regression is a real mixed tradeoff.

## Appendix A — all 36 declared cell means

CPU unit: known-worker microseconds/request.

|Workload|gen/c|Path|TPS|TTFT ms|Completion ms|TPOT ms|CPU us/req|
|---|---|---|---:|---:|---:|---:|---:|
|AMK Smol135M|1/1|old|54.349|18.368|18.368|undefined|486.364|
|AMK Smol135M|1/1|native|54.747|18.233|18.233|undefined|355.808|
|AMK Smol135M|1/1|coalesced|52.938|18.855|18.855|undefined|425.392|
|AMK Smol135M|64/1|old|164.430|18.347|389.185|5.886|10046.885|
|AMK Smol135M|64/1|native|165.189|18.247|387.395|5.859|7486.433|
|AMK Smol135M|64/1|coalesced|159.471|18.833|401.288|6.071|9311.651|
|AMK Smol135M|1/8|old|53.800|147.891|147.891|undefined|485.489|
|AMK Smol135M|1/8|native|61.239|129.927|129.927|undefined|337.303|
|AMK Smol135M|1/8|coalesced|59.563|133.795|133.795|undefined|396.754|
|AMK Smol135M|64/8|old|158.208|106.926|3214.683|49.329|10328.844|
|AMK Smol135M|64/8|native|304.387|63.888|1669.299|25.483|4487.822|
|AMK Smol135M|64/8|coalesced|292.745|67.859|1735.582|26.472|5238.929|
|vLLM Smol135M|1/1|old|850.283|1.167|1.167|undefined|47.214|
|vLLM Smol135M|1/1|native|846.292|1.169|1.169|undefined|44.724|
|vLLM Smol135M|1/1|coalesced|806.408|1.224|1.224|undefined|43.438|
|vLLM Smol135M|64/1|old|1364.789|1.127|46.891|0.726|1599.802|
|vLLM Smol135M|64/1|native|1390.450|1.127|45.999|0.712|1304.583|
|vLLM Smol135M|64/1|coalesced|1315.300|1.157|48.629|0.754|1534.692|
|vLLM Smol135M|1/8|old|3610.341|2.037|2.037|undefined|20.114|
|vLLM Smol135M|1/8|native|3605.055|1.983|1.983|undefined|25.676|
|vLLM Smol135M|1/8|coalesced|1162.576|6.746|6.746|undefined|37.154|
|vLLM Smol135M|64/8|old|5592.135|1.810|91.345|1.421|466.684|
|vLLM Smol135M|64/8|native|5630.454|1.828|90.907|1.414|411.687|
|vLLM Smol135M|64/8|coalesced|5070.858|2.041|100.854|1.568|492.813|
|vLLM Qwen0.5B|1/1|old|714.244|1.388|1.388|undefined|53.947|
|vLLM Qwen0.5B|1/1|native|718.880|1.377|1.377|undefined|41.165|
|vLLM Qwen0.5B|1/1|coalesced|674.279|1.468|1.468|undefined|50.811|
|vLLM Qwen0.5B|64/1|old|817.914|1.345|78.214|1.220|2620.396|
|vLLM Qwen0.5B|64/1|native|820.210|1.312|77.995|1.217|2191.729|
|vLLM Qwen0.5B|64/1|coalesced|782.943|1.403|81.708|1.275|2568.876|
|vLLM Qwen0.5B|1/8|old|2818.799|2.635|2.635|undefined|24.109|
|vLLM Qwen0.5B|1/8|native|2869.424|2.605|2.605|undefined|25.158|
|vLLM Qwen0.5B|1/8|coalesced|956.380|8.251|8.251|undefined|45.369|
|vLLM Qwen0.5B|64/8|old|4758.151|2.363|107.151|1.663|522.322|
|vLLM Qwen0.5B|64/8|native|4806.615|2.283|106.375|1.652|463.529|
|vLLM Qwen0.5B|64/8|coalesced|4373.108|2.485|116.982|1.817|543.004|

Process clocks include all executor threads; known kernel-TX term is0 for these paths. Brackets contain the cell window plus nearby waiting/host work. Client CPU/RX/softirq/BPF/TCP outside the known counter and other-host work are excluded. This is not total service CPU/energy or zero CPU.

## Appendix B — all 108 effects and five paired block differences

TPS tok/s; latency/TPOT ms; CPU us/request. Secondary cells are retained, without new primary labels. Zero-crossing intervals do not establish equivalence.

|Workload|gen/c|Control|Metric|Mean [t95]|Block 0..4 differences|
|---|---|---|---|---:|---|
|AMK Smol135M|1/1|old|TPS|-1.411 [-1.473, -1.350]|-1.400, -1.471, -1.335, -1.424, -1.426|
|AMK Smol135M|1/1|old|TTFT|+0.487 [+0.464, +0.510]|+0.488, +0.506, +0.456, +0.492, +0.492|
|AMK Smol135M|1/1|old|completion|+0.487 [+0.464, +0.510]|+0.488, +0.506, +0.456, +0.492, +0.492|
|AMK Smol135M|1/1|old|CPU us/req|-60.972 [-103.925, -18.018]|-53.087, -79.796, -4.665, -92.895, -74.414|
|AMK Smol135M|1/1|native|TPS|-1.809 [-1.914, -1.704]|-1.847, -1.894, -1.781, -1.676, -1.848|
|AMK Smol135M|1/1|native|TTFT|+0.622 [+0.589, +0.655]|+0.636, +0.648, +0.608, +0.582, +0.636|
|AMK Smol135M|1/1|native|completion|+0.622 [+0.589, +0.655]|+0.636, +0.648, +0.608, +0.582, +0.636|
|AMK Smol135M|1/1|native|CPU us/req|+69.585 [+31.274, +107.895]|+88.962, +18.738, +79.604, +64.236, +96.383|
|AMK Smol135M|64/1|old|TPS|-4.959 [-5.015, -4.903]|-4.909, -4.962, -4.985, -5.017, -4.921|
|AMK Smol135M|64/1|old|TTFT|+0.487 [+0.470, +0.504]|+0.499, +0.481, +0.478, +0.503, +0.472|
|AMK Smol135M|64/1|old|completion|+12.103 [+11.970, +12.236]|+11.994, +12.091, +12.142, +12.264, +12.023|
|AMK Smol135M|64/1|old|CPU us/req|-735.234 [-901.805, -568.662]|-769.787, -600.406, -838.121, -588.970, -878.885|
|AMK Smol135M|64/1|old|TPOT|+0.184 [+0.182, +0.186]|+0.182, +0.184, +0.185, +0.187, +0.183|
|AMK Smol135M|64/1|native|TPS|-5.718 [-5.772, -5.665]|-5.666, -5.697, -5.717, -5.783, -5.729|
|AMK Smol135M|64/1|native|TTFT|+0.586 [+0.570, +0.602]|+0.607, +0.585, +0.585, +0.582, +0.571|
|AMK Smol135M|64/1|native|completion|+13.894 [+13.752, +14.035]|+13.783, +13.819, +13.863, +14.072, +13.930|
|AMK Smol135M|64/1|native|CPU us/req|+1825.219 [+1368.334, +2282.104]|+2072.243, +1603.388, +1361.561, +2289.655, +1799.247|
|AMK Smol135M|64/1|native|TPOT|+0.211 [+0.209, +0.214]|+0.209, +0.210, +0.211, +0.214, +0.212|
|AMK Smol135M|1/8|old|TPS|+5.763 [+5.091, +6.436]|+4.900, +5.647, +6.161, +5.847, +6.262|
|AMK Smol135M|1/8|old|TTFT|-14.096 [-15.565, -12.627]|-12.044, -14.555, -14.453, -14.335, -15.091|
|AMK Smol135M|1/8|old|completion|-14.096 [-15.565, -12.627]|-12.044, -14.555, -14.453, -14.335, -15.091|
|AMK Smol135M|1/8|old|CPU us/req|-88.734 [-109.980, -67.489]|-61.080, -99.155, -96.478, -83.662, -103.296|
|AMK Smol135M|1/8|native|TPS|-1.676 [-2.507, -0.844]|-2.726, -0.925, -1.665, -1.736, -1.327|
|AMK Smol135M|1/8|native|TTFT|+3.868 [+1.965, +5.772]|+6.341, +2.291, +3.915, +3.816, +2.979|
|AMK Smol135M|1/8|native|completion|+3.868 [+1.965, +5.772]|+6.341, +2.291, +3.915, +3.816, +2.979|
|AMK Smol135M|1/8|native|CPU us/req|+59.451 [+17.785, +101.117]|+113.567, +24.827, +49.249, +44.094, +65.518|
|AMK Smol135M|64/8|old|TPS|+134.537 [+133.700, +135.375]|+135.218, +134.989, +133.982, +133.667, +134.831|
|AMK Smol135M|64/8|old|TTFT|-39.067 [-42.665, -35.469]|-40.905, -40.700, -41.687, -34.991, -37.053|
|AMK Smol135M|64/8|old|completion|-1479.101 [-1484.477, -1473.726]|-1484.325, -1478.644, -1474.884, -1474.984, -1482.669|
|AMK Smol135M|64/8|old|CPU us/req|-5089.915 [-5180.821, -4999.009]|-5182.202, -5034.818, -5066.146, -5015.260, -5151.150|
|AMK Smol135M|64/8|old|TPOT|-22.858 [-22.953, -22.762]|-22.911, -22.825, -22.749, -22.857, -22.946|
|AMK Smol135M|64/8|native|TPS|-11.642 [-12.943, -10.341]|-10.771, -12.398, -11.725, -12.894, -10.423|
|AMK Smol135M|64/8|native|TTFT|+3.971 [+0.591, +7.350]|+2.304, +2.812, +2.349, +8.743, +3.644|
|AMK Smol135M|64/8|native|completion|+66.283 [+58.896, +73.669]|+61.236, +70.077, +67.088, +73.611, +59.402|
|AMK Smol135M|64/8|native|CPU us/req|+751.107 [+588.190, +914.025]|+671.891, +938.481, +840.415, +650.527, +654.221|
|AMK Smol135M|64/8|native|TPOT|+0.989 [+0.895, +1.083]|+0.935, +1.068, +1.028, +1.030, +0.885|
|vLLM Smol135M|1/1|old|TPS|-43.875 [-93.320, +5.571]|-32.552, +3.187, -29.050, -103.937, -57.021|
|vLLM Smol135M|1/1|old|TTFT|+0.058 [-0.002, +0.118]|+0.051, -0.009, +0.041, +0.120, +0.085|
|vLLM Smol135M|1/1|old|completion|+0.058 [-0.002, +0.118]|+0.051, -0.009, +0.041, +0.120, +0.085|
|vLLM Smol135M|1/1|old|CPU us/req|-3.776 [-8.635, +1.083]|-5.401, +1.086, -9.368, -3.287, -1.912|
|vLLM Smol135M|1/1|native|TPS|-39.884 [-93.710, +13.943]|+0.878, -0.373, -98.497, -68.381, -33.045|
|vLLM Smol135M|1/1|native|TTFT|+0.055 [-0.015, +0.125]|+0.006, +0.005, +0.140, +0.080, +0.046|
|vLLM Smol135M|1/1|native|completion|+0.055 [-0.015, +0.125]|+0.006, +0.005, +0.140, +0.080, +0.046|
|vLLM Smol135M|1/1|native|CPU us/req|-1.286 [-5.768, +3.195]|-5.013, +3.842, -4.421, -0.968, +0.129|
|vLLM Smol135M|64/1|old|TPS|-49.489 [-92.261, -6.717]|-64.407, +11.916, -68.596, -65.777, -60.581|
|vLLM Smol135M|64/1|old|TTFT|+0.030 [-0.026, +0.085]|+0.030, -0.046, +0.039, +0.052, +0.072|
|vLLM Smol135M|64/1|old|completion|+1.738 [+0.216, +3.260]|+2.278, -0.449, +2.408, +2.313, +2.139|
|vLLM Smol135M|64/1|old|CPU us/req|-65.110 [-169.007, +38.786]|-37.225, -117.287, -35.466, -176.445, +40.871|
|vLLM Smol135M|64/1|old|TPOT|+0.027 [+0.004, +0.050]|+0.036, -0.006, +0.038, +0.036, +0.033|
|vLLM Smol135M|64/1|native|TPS|-75.151 [-81.095, -69.206]|-82.202, -77.007, -71.309, -70.282, -74.954|
|vLLM Smol135M|64/1|native|TTFT|+0.030 [+0.003, +0.057]|+0.033, +0.033, -0.006, +0.055, +0.034|
|vLLM Smol135M|64/1|native|completion|+2.630 [+2.427, +2.832]|+2.866, +2.698, +2.500, +2.459, +2.626|
|vLLM Smol135M|64/1|native|CPU us/req|+230.109 [+138.882, +321.336]|+317.949, +270.582, +183.138, +131.457, +247.418|
|vLLM Smol135M|64/1|native|TPOT|+0.041 [+0.038, +0.044]|+0.045, +0.042, +0.040, +0.038, +0.041|
|vLLM Smol135M|1/8|old|TPS|-2447.765 [-2822.270, -2073.260]|-2480.704, -1939.753, -2564.038, -2743.003, -2511.328|
|vLLM Smol135M|1/8|old|TTFT|+4.709 [+4.080, +5.338]|+4.918, +3.916, +4.559, +5.253, +4.898|
|vLLM Smol135M|1/8|old|completion|+4.709 [+4.080, +5.338]|+4.918, +3.916, +4.559, +5.253, +4.898|
|vLLM Smol135M|1/8|old|CPU us/req|+17.040 [+15.317, +18.763]|+18.625, +15.006, +17.705, +16.390, +17.475|
|vLLM Smol135M|1/8|native|TPS|-2442.479 [-2809.718, -2075.241]|-2033.057, -2336.887, -2841.048, -2553.093, -2448.313|
|vLLM Smol135M|1/8|native|TTFT|+4.763 [+4.288, +5.237]|+4.895, +4.183, +4.594, +5.147, +4.995|
|vLLM Smol135M|1/8|native|completion|+4.763 [+4.288, +5.237]|+4.895, +4.183, +4.594, +5.147, +4.995|
|vLLM Smol135M|1/8|native|CPU us/req|+11.478 [+6.474, +16.483]|+10.047, +13.998, +12.053, +5.408, +15.884|
|vLLM Smol135M|64/8|old|TPS|-521.278 [-569.819, -472.736]|-508.717, -499.793, -571.231, -475.429, -551.218|
|vLLM Smol135M|64/8|old|TTFT|+0.231 [+0.140, +0.323]|+0.190, +0.230, +0.133, +0.287, +0.316|
|vLLM Smol135M|64/8|old|completion|+9.510 [+8.981, +10.039]|+8.798, +9.945, +9.624, +9.634, +9.547|
|vLLM Smol135M|64/8|old|CPU us/req|+26.129 [+0.614, +51.643]|+22.371, +52.164, +37.659, -2.871, +21.320|
|vLLM Smol135M|64/8|old|TPOT|+0.147 [+0.139, +0.155]|+0.137, +0.154, +0.151, +0.148, +0.147|
|vLLM Smol135M|64/8|native|TPS|-559.597 [-627.946, -491.247]|-576.867, -504.010, -568.252, -510.326, -638.526|
|vLLM Smol135M|64/8|native|TTFT|+0.213 [+0.026, +0.400]|+0.308, +0.135, +0.008, +0.218, +0.396|
|vLLM Smol135M|64/8|native|completion|+9.948 [+9.413, +10.483]|+9.501, +10.001, +9.572, +10.106, +10.558|
|vLLM Smol135M|64/8|native|CPU us/req|+81.125 [+39.387, +122.863]|+59.135, +117.160, +54.545, +56.148, +118.639|
|vLLM Smol135M|64/8|native|TPOT|+0.155 [+0.147, +0.162]|+0.146, +0.157, +0.152, +0.157, +0.161|
|vLLM Qwen0.5B|1/1|old|TPS|-39.965 [-82.769, +2.839]|-25.787, -64.022, -43.473, +10.728, -77.272|
|vLLM Qwen0.5B|1/1|old|TTFT|+0.080 [-0.001, +0.160]|+0.053, +0.107, +0.087, -0.012, +0.163|
|vLLM Qwen0.5B|1/1|old|completion|+0.080 [-0.001, +0.160]|+0.053, +0.107, +0.087, -0.012, +0.163|
|vLLM Qwen0.5B|1/1|old|CPU us/req|-3.136 [-13.401, +7.128]|-12.705, +2.485, -3.077, -9.637, +7.253|
|vLLM Qwen0.5B|1/1|native|TPS|-44.601 [-83.282, -5.921]|-49.354, -77.718, -46.571, +6.664, -56.027|
|vLLM Qwen0.5B|1/1|native|TTFT|+0.091 [+0.028, +0.154]|+0.102, +0.129, +0.092, +0.005, +0.127|
|vLLM Qwen0.5B|1/1|native|completion|+0.091 [+0.028, +0.154]|+0.102, +0.129, +0.092, +0.005, +0.127|
|vLLM Qwen0.5B|1/1|native|CPU us/req|+9.646 [+6.429, +12.864]|+14.038, +9.770, +7.538, +8.116, +8.769|
|vLLM Qwen0.5B|64/1|old|TPS|-34.971 [-35.847, -34.095]|-34.899, -36.062, -34.188, -35.131, -34.574|
|vLLM Qwen0.5B|64/1|old|TTFT|+0.058 [+0.029, +0.087]|+0.065, +0.078, +0.018, +0.058, +0.072|
|vLLM Qwen0.5B|64/1|old|completion|+3.494 [+3.411, +3.578]|+3.489, +3.595, +3.417, +3.514, +3.455|
|vLLM Qwen0.5B|64/1|old|CPU us/req|-51.520 [-136.160, +33.120]|-137.435, -36.195, -37.542, -90.938, +44.508|
|vLLM Qwen0.5B|64/1|old|TPOT|+0.055 [+0.053, +0.056]|+0.054, +0.056, +0.054, +0.055, +0.054|
|vLLM Qwen0.5B|64/1|native|TPS|-37.267 [-37.950, -36.585]|-37.023, -37.634, -36.683, -38.030, -36.967|
|vLLM Qwen0.5B|64/1|native|TTFT|+0.091 [+0.075, +0.108]|+0.094, +0.082, +0.084, +0.082, +0.114|
|vLLM Qwen0.5B|64/1|native|completion|+3.713 [+3.644, +3.781]|+3.691, +3.743, +3.653, +3.793, +3.684|
|vLLM Qwen0.5B|64/1|native|CPU us/req|+377.146 [+256.701, +497.591]|+372.138, +407.341, +479.017, +218.087, +409.148|
|vLLM Qwen0.5B|64/1|native|TPOT|+0.057 [+0.056, +0.059]|+0.057, +0.058, +0.057, +0.059, +0.057|
|vLLM Qwen0.5B|1/8|old|TPS|-1862.419 [-2133.643, -1591.195]|-2058.788, -1500.736, -1985.298, -1831.285, -1935.989|
|vLLM Qwen0.5B|1/8|old|TTFT|+5.616 [+4.934, +6.297]|+6.057, +4.922, +5.729, +6.188, +5.181|
|vLLM Qwen0.5B|1/8|old|completion|+5.616 [+4.934, +6.297]|+6.057, +4.922, +5.729, +6.188, +5.181|
|vLLM Qwen0.5B|1/8|old|CPU us/req|+21.260 [+13.688, +28.832]|+28.767, +17.864, +24.252, +22.542, +12.877|
|vLLM Qwen0.5B|1/8|native|TPS|-1913.044 [-2038.597, -1787.492]|-2008.812, -1769.566, -2011.787, -1894.167, -1880.889|
|vLLM Qwen0.5B|1/8|native|TTFT|+5.646 [+5.011, +6.281]|+6.032, +5.126, +5.772, +6.203, +5.097|
|vLLM Qwen0.5B|1/8|native|completion|+5.646 [+5.011, +6.281]|+6.032, +5.126, +5.772, +6.203, +5.097|
|vLLM Qwen0.5B|1/8|native|CPU us/req|+20.211 [+14.321, +26.100]|+22.155, +17.708, +17.058, +27.684, +16.449|
|vLLM Qwen0.5B|64/8|old|TPS|-385.043 [-411.625, -358.462]|-390.215, -384.797, -407.134, -393.369, -349.701|
|vLLM Qwen0.5B|64/8|old|TTFT|+0.123 [-0.036, +0.281]|+0.140, +0.066, +0.240, +0.233, -0.067|
|vLLM Qwen0.5B|64/8|old|completion|+9.831 [+8.879, +10.783]|+9.137, +10.296, +10.259, +10.583, +8.879|
|vLLM Qwen0.5B|64/8|old|CPU us/req|+20.682 [-1.378, +42.742]|+9.616, +24.855, +30.479, -3.381, +41.840|
|vLLM Qwen0.5B|64/8|old|TPOT|+0.154 [+0.141, +0.168]|+0.143, +0.162, +0.159, +0.164, +0.142|
|vLLM Qwen0.5B|64/8|native|TPS|-433.508 [-471.168, -395.847]|-419.441, -423.297, -483.029, -438.302, -403.469|
|vLLM Qwen0.5B|64/8|native|TTFT|+0.203 [+0.107, +0.298]|+0.301, +0.200, +0.137, +0.255, +0.120|
|vLLM Qwen0.5B|64/8|native|completion|+10.607 [+9.372, +11.842]|+9.826, +11.170, +11.209, +11.554, +9.277|
|vLLM Qwen0.5B|64/8|native|CPU us/req|+79.475 [+50.462, +108.487]|+54.216, +84.456, +63.437, +80.247, +115.017|
|vLLM Qwen0.5B|64/8|native|TPOT|+0.165 [+0.146, +0.185]|+0.151, +0.174, +0.176, +0.179, +0.145|

Ordinary analysis command: python3 analysis.py /tmp/bpfusion-coalesced-network-0pls_22b full. Reviewer did not call its writing main; read-only analyze calls audited all 15 full/selected qualification/three legacy records, and separate timestamp arithmetic reconstructed every effect here. Raw files/full.analysis.json preserve full precision; tables round for readability.
