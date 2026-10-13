# Fresh combined result review: ordinary untraced optimized serving

Reviewed 2026-10-13 after both full model stages and analyses terminated successfully, by the fresh default_untraced_result_review reviewer in the original bpfusion-dev Workspace. This is the single combined result review. The reviewer started no model or serving process, changed no production or benchmark source, modified no plan or frozen reference, and wrote only this report.

- Run status: **valid and complete for the admitted finite-output-set qualification and ordinary untraced client comparison**.
- Tested hypothesis: **inconclusive** for the proposed kernel advantage in all four predeclared model/primary combinations.
- Research value: **supporting**; the setup/build/strict checks are integrated dependencies, not additional contributions.
- Paper impact: **implementation and workload boundary / additional serving evidence**, not a direct thesis challenge.
- Next paper decision: close this unchanged ordinary-default comparison. Report the observed performance and failure to establish a primary transport gain. Retain the complete-output-set limitation. A higher-value next question can address full-service CPU attribution, physical delivery or a competing optimized host scheduler; this result does not authorize or require another unchanged timing run.

## Scope, sources and actual completion

The [admitted plan](default_untraced_plan_20261012.md), [fresh plan review](default_untraced_plan_review_20261012.md), prior completed release qualification, current driver/analyzer/native/backend/Makefile/client/userspace network implementation and the complete [durable archive](default_untraced_20261012/) were inspected. The retained full Linux TCP/HTTP/eBPF/shared-queue/resident-inference/kernel-TX objective is unchanged. No formal paper RQ/thesis exists; this review does not invent one or declare the entire objective complete.

The ordinary source base is bd6a0a010a5bff19155e2941afd4a0fed3960277. Makefile, executor/vllm_graph.cu, executor/vllm_graph.py, executor/userspace_tcp.h, shared queue header and module/bfusion_tx.c are byte-identical to that qualified commit. The retry pipeline's five source snapshots equal current files. The first setup snapshot differs from the retry driver only by the documented batches=None logging repair. Every strict metadata source equals the retry snapshot. Build stdout records ordinary vllm_graph and vllm_graph_user_network_wait compiled with BF_PAD_PREFILL and BF_PREFIX_RELEASE, and neither with BF_TRACE; the native control additionally has BF_USER_NETWORK/BF_USER_NETWORK_WAIT. No .gpu.jsonl file was produced. A nominal trace-path string remains in raw start metadata but is never passed as a trace argument; it is not an observed GPU trajectory.

Actual setup/commands/environment/source snapshots and resolved packages are retained. The temporary venv resolves vLLM0.31.0, Torch2.13.0+cu129 and Transformers5.17.0. Build links the actual CUDA12 runtime from that venv; the original base runtime remains Torch2.14.1+cu130/Transformers5.19.0. Both pinned checkpoints use FP16, the same official FULL model/head/greedy graph catalogue, eight-slot cache budget, packed prefill and prefix release. Each executor log independently shows the complete520-graph catalogue for batches1..8 and query lengths1..64. The native alternative engages the60000ns epoll_pwait2 wait. It is a matched mechanism control, not an official external vLLM server baseline.

Both architectures execute five alternating process pairs in order kernel/user, user/kernel, kernel/user, user/kernel, kernel/user. Qwen full raw terminal is23:55:40UTC; its driver and analysis statuses are0 at the same timestamp. Smol raw terminal is00:00:30UTC; driver and analysis statuses are0 at00:00:31UTC. Full scope is20 executors,80 cells,5120 measured requests/166400 tokens and160 checked gen1 warmups. Each executor has264 requests/8328 tokens. No full-run failure, excluded process/block/request, favorable retry or missing cell was found. All outliers remain in the means and quantiles. Every owned temp top-level artifact was checked byte-identical to its durable copy; at this inspection the archive contains77 files.

The initial venv ensurepip failure occurred before serving and is retained. The official without-pip/pip --python retry succeeds. The initial preflight's kernel executor serves40 requests/1048 tokens, meets membership/counters/page checks and stops normally, but the driver then fails on undefined traced-only batches in a PASS log before the native condition. That failed raw/status/stdout/source is retained. The sole repair sets batches=None; no numerical reference, workload, timing, model, native/backend or oracle changes. The whole preflight retry passes both transports/all four cells with80 requests/2096 tokens and analysis0. There is no pool expansion after observation.

## Independent finite-output-set and strict audit

The frozen asset timestamp23:36:58UTC precedes the first serving observation and identifies bd6a0a0. I reconstructed its complete unions directly from all24 prior independent reference files per model: each supplies6732 valid complete sequences and1036 intentionally rejected empty outputs. The unions equal the asset exactly:17 prompt/generation keys with22 distinct sequences for Qwen and19 for Smol. Model path, vocabulary and FP16 identity match current metadata. Neither current experiment output nor tokenwise mixtures contribute to the pool.

Every valid request in the successful preflight, four strict executors and20 full timing executors was independently checked against one complete sequence for its exact input and generation length. All pass. Bad outputs remain empty. This is a fixed, pre-observation qualified complete-output set. It is **not independent replay of the current untraced batching/cache/metadata trajectory**. A wrong trajectory producing a previously qualified alternative complete sequence could pass. Prior traced source qualification supports the unchanged implementation separately; these untraced records do not recreate it or prove universal numerical correctness, batch invariance, task quality or arbitrary-model support.

All four strict runs independently contain622 requests,22224 tokens,259 intentional rejects and5000 empty connects, totaling2488/88896/1036/20000. Each has30 fragmented prompt/block-edge requests, concurrency1..8,256 invalid/valid wrap pairs,32 mixed-length requests, six pipelined half-close replies, mixed invalid/valid HTTP pipeline, binary EOF rejection followed by valid binary response, and helper-thread SIGTERM with native exit0. Each transport has342 valid HTTP replies,258 invalid HTTP replies,21 valid binary replies and one intentional binary rejection. Driver source checks status/header/body length and binary EOF; raw retains parsed token bytes/inputs and errors rather than a complete packet capture.

After-ready all-thread strace independently shows no accept/recv/send-family calls in either kernel strict run. Native Qwen contains5153 accept4,12830 recvfrom and22378 sendmsg calls; Smol contains5152/12833/22322. This supports the absence of a steady userspace request worker in this strict scope and engagement of the native mechanism. It does not measure total host CPU or exclude kernel worker CPU. Kernel strict pages show head622, reserved0 and all eight FREE slots; native published=completed622 and rejected259. All four aggregate admitted=retired622, launches1, graph errors/trace overflows0, max_active8/max_release8. Kernel detach succeeds, and module teardown occurs before each executor terminal. Intentional binary EOF remains a protocol rejection, not a dropped valid request.

Full-run aggregate counters also pass independently: launches1, admitted=retired264, max_active8/max_release8 and errors/overflows0 in all20 executors; every kernel page has head264/reserved0/eight FREE, every native published=completed264/rejected0, all exits/detaches0. These are whole-executor totals. They do not locate release batching or activity in individual cells and cannot substitute for per-request ownership/graph replay.

## Independently recomputed client results

I reconstructed all80 cells from raw requests, exact index coverage0..63, input/gen, start/arrival timestamps and first/last cell bounds. Every timestamp-derived TTFT/completion/TPOT formula, throughput, finite p50/p99 and five-pair effect equals the archived analyzer output. Warmups are excluded from timed cells but included in fixed membership. Client token timestamps include TCP, polling and receive coalescing; they are not GPU-ready timestamps. Capture/bootstrap and connection establishment are outside request timing.

Below K/U means ordinary kernel/native user. Each cell has320 measured requests per transport across five process blocks. Throughput is the mean of five cell-window token/s values, not pooled token/s.

| Model | Output/client count | TTFT K/U ms | Completion K/U ms | TPOT K/U ms | Throughput K/U token/s |
| --- | --- | ---: | ---: | ---: | ---: |
| Qwen |1/1|1.429292 /1.406550|1.429292 /1.406550|n/a|692.702 /704.174|
| Qwen |64/1|1.326702 /1.320161|78.031029 /78.050122|1.217529 /1.217936|819.765 /819.562|
| Qwen |1/8|2.475763 /2.480569|2.475763 /2.480569|n/a|3123.462 /3098.626|
| Qwen |64/8|2.170073 /2.159406|107.646454 /107.588372|1.674228 /1.673476|4752.623 /4755.702|
| Smol |1/1|1.206509 /1.201046|1.206509 /1.201046|n/a|818.011 /823.565|
| Smol |64/1|1.114949 /1.140662|45.949603 /45.935751|0.711661 /0.711033|1391.768 /1392.196|
| Smol |1/8|1.945366 /1.903253|1.945366 /1.903253|n/a|3963.465 /4041.512|
| Smol |64/8|1.750315 /1.740009|91.607218 /91.787001|1.426300 /1.429317|5583.713 /5571.513|

The predeclared primary effects are user-minus-kernel gen1/c1 TTFT and kernel-minus-user gen64/c8 throughput. Positive favors kernel. Nominal two-sided t95 uses five process-level paired differences, df4;320 within-cell requests are not320 independent repetitions.

| Model / primary | Paired gain | Nominal t95 | Judgment |
| --- | ---: | --- | --- |
| Qwen gen1/c1 TTFT ms |−0.022742|[−0.066119,0.020636]|inconclusive|
| Smol gen1/c1 TTFT ms |−0.005463|[−0.042637,0.031712]|inconclusive|
| Qwen gen64/c8 token/s |−3.079500|[−16.750507,10.591507]|inconclusive|
| Smol gen64/c8 token/s |12.199812|[−10.879697,35.279321]|inconclusive|

The five TTFT primary gains are Qwen[−0.063983,0.018375,−0.053020,−0.015003,−0.000078]ms and Smol[−0.000902,−0.054493,0.010434,0.024632,−0.006986]ms. The five throughput primary gains are Qwen[−13.293294,15.573316,−3.461162,−6.957496,−7.258863]token/s and Smol[36.263880,19.260577,12.786462,−14.834104,7.522245]token/s. No primary supports superiority or equivalence.

All secondary completion/TPOT/throughput intervals and c8 TTFT intervals contain0. The two gen64/c1 TTFT secondary intervals are small and opposite: Qwen gain−0.006540[−0.013005,−0.0000755]ms favors native; Smol gain0.025713[0.006852,0.044574]ms favors kernel. Keep them secondary, without a multiplicity-adjusted/general transport claim. The archived analyzers retain every exact mean, p50/p99, individual pair difference and interval; this table does not replace raw precision.

Cross-transport complete-output agreement was separately reconstructed by pair/input/gen/client/index: both models c1 are320/320 for both lengths; Qwen c8 is297/320 forgen1 and294/320 forgen64; Smol c8 is320/320 forgen1 and299/320 forgen64. Smolgen64/c8 first tokens agree320/320 despite later differences. Every complete output independently belongs to the frozen set. Therefore claim matched compute policy and finite-set fidelity, not identical-output scheduling.

## Lifecycle, environmental limits and interpretation

The durable owner receipt at00:01:46UTC shows no GPU application, no bfusion_tx module or listed bpfusion pins, unchanged base runtime/kernel/boot identity and original Coder PIDs1/10909 retained. Workspace receipt shows original UID3e8994f8-77ba-4a73-a3a5-35ed69a0a8a2, Running/Ready, zero restarts onlab. The bounded kernel-journal receipt23:36:58→00:01:51UTC has no listed fault matches. These receipts do not demonstrate continuous exclusive GPU/host use, complete co-tenant activity, physical network delivery, or no interference. Model runs are sequential and have different exposure windows. Client source defaults to local TCP; this experiment provides no remote-NIC acceptance.

At review, only owned temporary runtime/build output remains for final inspection; the root owns subsequent cleanup and its final receipt. Do not call those artifacts removed before that receipt. No source/model cache/Workspace replacement, base-runtime mutation, unrelated WIP modification or persistent service is part of this experiment.

Ordinary performance is now measured directly, rather than inferred from traced candidates. The model/frontend improvements previously qualified remain usable, but this run establishes no reliable primary latency/throughput advantage from choosing the kernel transport. The small opposing secondary TTFT effects and nonidentical concurrent outputs reinforce the bounded interpretation. Do not subtract prior traced measurements to infer a causal tracing overhead, attribute shared GPU-policy gains to eBPF, claim a megakernel/arithmetical optimization, call the native mechanism an external SOTA baseline, or declare the entire retained objective complete.
