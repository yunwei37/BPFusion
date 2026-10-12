# Independent combined result review: completed FIFO-prefix release

Reviewed 2026-10-12T23:23:20Z by the fresh `completion_release_result_review` reviewer. This is the single completed-run review of both models together. The reviewer read source/setup before completion, then independently reconstructed the complete durable matrix; it started no serving process, altered no experiment/source, excluded no row, and wrote only this report.

Run status: **valid, complete** for the planned traced serving/replay contract. Tested hypothesis: **supported for gen1/eight-client delivery latency in both tested checkpoints and both transports, under the recorded shared-host exposure**. Research value: **supporting**. Paper impact: **scheduler/mechanism and workload boundary**, not a direct thesis challenge. Next paper decision: retain the measured prefix-release adaptation after the separately required ordinary untraced checks; close this matrix without favorable reruns. No fault-free or isolated transport causal claim follows.

## Contract, artifacts and source audit

The [plan](completion_release_plan_20261012.md) and [fresh plan review](completion_release_plan_review_20261012.md) define the hypothesis: publish the already-complete consecutive FIFO prefix without waiting between releases for local TX reclamation, preserving final-token protection and per-slot reservation. `docs/evaluation.md` contains no formal paper RQ/thesis; `docs/idea-story.md` is absent. This review uses that retained concrete hypothesis and does not invent or rename an RQ.

All evidence is in [completion_release_20261012/](completion_release_20261012/): `pipeline_commands.json` contains the actual sequential commands and exact five changed source snapshots; `build_command.json`, build stdout/status, runtime record, real preflight, both strict files, both full files, executor stdout, GPU traces, independently advanced host references, native analyses, output diagnostics and final receipts are retained. The original source was main617c28ad84e884773764d8390038abb42549803e. Qwen full records that HEAD; Smol records publication6754b051e0a38421cf486e6399ad2e2a3ddc8058. Every embedded driver/backend/native source and the original five-file pipeline snapshots equal the serving source reviewed here. This publication-only HEAD transition is disclosed provenance, not a treatment or oracle change.

The build log resolves all actual padded serial/prefix kernel/native binaries and macros. Both treatments use BF_PAD_PREFILL and BF_TRACE, unchanged upstream graph/head math/catalogue/KV/precision, and the same existing60000ns timed native network wait. BF_PREFIX_RELEASE is the release-policy difference. Python3.12.3/Torch2.13.0+cu129 is recorded in both full metadata; the retained temporary vLLM0.31/Transformers5.17 runtime is the same qualification runtime. The original base runtime remains Torch2.14.1+cu130/Transformers5.19, per the owner receipt. No changed model arithmetic, BPF/module/wire ABI, persistent service or scheduler is inferred.

Source audit: executor/vllm_graph.cu:57–71 consumes every completed child-graph/head row before phase2, and resets batch before release. Prefix release:74–97 drains only consecutive phase2 records, uses a system fence before DONE, clears only local phase and records logical IDs from local retired counters; it never rereads freed shared-slot metadata or clears reservation bits. The serial #else still performs the original single publication plus global reclamation wait. Admission:98–115 requires PENDING and an unused local record. Body→head graph dependency and device graph tail relaunch are unchanged. [CUDA12.9.1 tail-launch semantics](https://docs.nvidia.com/cuda/archive/12.9.1/cuda-c-programming-guide/index.html#tail-launch) support the completion-before-next-dispatch ordering; source and actual reuse traces jointly qualify this bounded implementation.

Kernel module/bfusion_tx.c:155–159 and native executor/userspace_tcp.h:104–109 still withhold the final token until DONE. Kernel:201–224 and native:119–124 finish old slot accesses, publish FREE and clear only that reservation last. Kernel same-peer earlier-response ordering and native one-outstanding-slot-per-peer ordering remain. DONE departure is local send acceptance/reclamation, **not remote TCP acknowledgement**. Prefix release does not eliminate FIFO blocking behind an unfinished older GPU request or a slow same-peer send.

## Completion and correctness

Build0 and real preflight0 precede strict/full collection. Preflight serves16 real eight-client requests/520 exact replayed tokens; gen1 release rounds are1 then7 requests, gen64 releases8 together, with real mixed prefill. Eight strict executors then each complete622 requests/22224 tokens/259 intentional rejections/5000 empty connections, all actual batches1..8, fragmented prompts and length edges, wrap/reuse, mixed1/64, persistent/pipeline/half-close, invalid IDs/binary EOF and helper-thread stop. Total strict coverage is4976 requests/177792 tokens/2072 intentional rejections/40000 empty connections. Strict and analysis exits are0. Each kernel after-ready network trace has zero accept/recv/send calls; each native trace engages the intended calls. All four kernel strict page snapshots show reserved0/all8 FREE; native source-backed stop counters show622 published=completed and259 rejects, rather than a separately retained native raw page snapshot.

Both full stages are terminal0: Qwen22:49:35–23:02:11UTC, Smol23:02:16–23:13:33UTC. All40 executors exit0,160 cells contain10240 measured requests/332800 measured tokens, and320 checked one-token warmups are retained but excluded from performance. No failure, exclusion, favorable rerun or duplicate full executor appears. All40 trace terminals have zero overflow/graph error and264 admissions=retirements; actual graphs and release counters match trace event counts. Every20 kernel full page snapshot shows reserved0/all8 FREE; every20 native stop record shows264 published=completed/rejected0.

Independent reconstruction joined client marker→admission→logical ID→compute→release→reference. Every received byte sequence equals its independently advanced host replay and compute trace; release is exactly once in FIFO ID order after the last required compute, and before physical slot reuse. The request-derived66-event bound covers admission+at most64 computes+release. Replay builds history from its own graph output, not served-token teacher forcing; it uses independently advanced metadata. Reusing the upstream graph/math oracle deliberately tests queue/scheduler integration, not upstream task quality or mathematical correctness against an unrelated implementation.

The serial component control engaged max-prefix1 in every executor and receives the same fresh strict qualification/instrumentation. Prefix engaged actual multi-release in every executor, and the primary cells are separately joined below. Both use the identical graph catalogue/precision/KV budget/client request counts. The efficient native transport is a transport control, not an external SOTA model-serving baseline. No avoidable baseline interface failure is counted as a candidate win; these comparisons have the roles declared in the plan.

## Independent metric and uncertainty reconstruction

All request timestamps, lengths, TTFT=(first complete-token arrival−send start), completion=(last arrival−send start), TPOT=(last−first)/(gen−1), cell throughput=64×gen/(last arrival−first send), finite320-request nearest-rank p50/p99,32 mode/cell metric rows and all84 paired metric rows reproduce the archived native analysis to <1e−8. Measurement points/formulas match the [official vLLM client benchmark definitions](https://github.com/vllm-project/vllm/blob/main/docs/benchmarking/cli.md) and [vLLM0.31 metric definitions](https://docs.vllm.ai/en/v0.31.0/design/metrics/); receive coalescing is part of client delivery timing, not a decode-kernel timer. Gen1 TTFT equals completion; gen1 TPOT is reported n/a.

Five process blocks, rather than64 requests within a cell, are the paired unit. The same order occurs for each model: block0 serial-kernel→prefix-kernel→serial-native→prefix-native; block1 reverse; block2 serial-native→prefix-native→serial-kernel→prefix-kernel; block3 reverse; block4 repeats block0. Intervals use mean difference±2.776445105×sample SD/√5 (nominal t95,df4). These are small-sample nominal intervals, not multiplicity-adjusted universal inference or equivalence tests. All five differences and every outlier remain in raw/analysis; no additional independent repetitions are manufactured from pooled requests.

Primary serial-minus-prefix gen1/c8 mean TTFT,ms:

| Model | Transport | Serial | Prefix | Gain [nominal t95] | Five paired gains |
| --- | --- | --- | --- | --- | --- |
| qwen | kernel | 8.821412 | 2.595630 | +6.225782 [6.106539, 6.345024] | 6.325975, 6.312548, 6.093431, 6.211041, 6.185915 |
| qwen | userspace | 8.892217 | 2.520429 | +6.371787 [6.025879, 6.717696] | 6.279494, 6.242995, 6.859743, 6.314578, 6.162127 |
| smol | kernel | 7.050603 | 1.891055 | +5.159548 [5.107920, 5.211176] | 5.225644, 5.140353, 5.135789, 5.122034, 5.173920 |
| smol | userspace | 6.939086 | 2.013869 | +4.925218 [4.701560, 5.148875] | 4.714734, 4.798027, 5.123460, 5.095636, 4.894231 |

All four primary intervals are wholly positive and every individual primary pair is positive. This supports the declared narrow release-policy prediction, not a general eBPF-only gain. Candidate net throughput on the same gen1/c8 cells also improves; the tables below retain every secondary effect.

## Mechanism engagement and tradeoffs

Primary arrays below are blocks0..4. Every primary request is joined to its actual release round and actual compute. The source policy change accompanies56..58→15..17 prefill graphs; it permits sustained real batching in the tested closed loop rather than merely a long-output max-prefix counter. More packed padding is also retained. These counts support the batching explanation but do not estimate a separate local-reclamation micro-cost or a formal mediated-effect fraction.

| Model | Mode | Release rounds | Max prefix | Requests in multi-release | Prefill graphs | Mixed-prefill graphs | Padding tokens |
| --- | --- | --- | --- | --- | --- | --- | --- |
| qwen | serial-kernel | 64, 64, 64, 64, 64 | 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0 | 58, 58, 57, 58, 58 | 2, 2, 1, 1, 2 | 24, 18, 24, 18, 18 |
| qwen | prefix-kernel | 16, 16, 17, 16, 16 | 6, 7, 8, 8, 7 | 64, 56, 55, 56, 59 | 16, 16, 17, 16, 16 | 16, 8, 8, 8, 8 | 192, 144, 168, 162, 159 |
| qwen | serial-userspace | 64, 64, 64, 64, 64 | 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0 | 58, 57, 58, 58, 57 | 2, 2, 2, 1, 2 | 24, 24, 18, 18, 27 |
| qwen | prefix-userspace | 16, 15, 16, 16, 16 | 8, 8, 5, 5, 7 | 56, 57, 64, 64, 56 | 16, 15, 16, 16, 16 | 8, 8, 16, 16, 8 | 150, 192, 120, 192, 144 |
| smol | serial-kernel | 64, 64, 64, 64, 64 | 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0 | 58, 58, 58, 58, 58 | 2, 1, 1, 1, 1 | 18, 18, 21, 21, 24 |
| smol | prefix-kernel | 16, 16, 16, 16, 16 | 7, 8, 8, 8, 8 | 56, 61, 57, 57, 61 | 16, 16, 16, 16, 16 | 8, 13, 9, 8, 8 | 168, 153, 174, 165, 159 |
| smol | serial-userspace | 64, 64, 64, 64, 64 | 1, 1, 1, 1, 1 | 0, 0, 0, 0, 0 | 57, 56, 58, 58, 58 | 3, 2, 2, 1, 2 | 21, 30, 18, 21, 24 |
| smol | prefix-userspace | 16, 17, 17, 16, 16 | 7, 7, 6, 7, 7 | 61, 56, 63, 62, 56 | 16, 17, 17, 16, 16 | 13, 8, 16, 14, 8 | 144, 156, 87, 138, 168 |

Secondary release effects below use serial−prefix for latency/TPOT/completion and prefix−serial for TPS. Positive favors prefix. All estimates, including negative point estimates, remain:

| Model | Transport | gen/c | TTFT ms [t95] | Completion ms [t95] | TPS [t95] | TPOT ms [t95] |
| --- | --- | --- | --- | --- | --- | --- |
| qwen | kernel | 1/1 | +0.037398 [-0.032968, 0.107765] | +0.037398 [-0.032968, 0.107765] | +18.156161 [-13.834219, 50.146541] | n/a |
| qwen | kernel | 64/1 | -0.031636 [-0.119245, 0.055974] | -0.920100 [-2.467103, 0.626903] | -9.353294 [-25.070630, 6.364042] | -0.014103 [-0.037360, 0.009155] |
| qwen | kernel | 1/8 | +6.225782 [6.106539, 6.345024] | +6.225782 [6.106539, 6.345024] | +2045.074844 [1897.464483, 2192.685204] | n/a |
| qwen | kernel | 64/8 | -0.046382 [-0.157172, 0.064409] | -1.658312 [-5.714324, 2.397699] | -67.017607 [-235.461512, 101.426298] | -0.025586 [-0.088391, 0.037218] |
| qwen | userspace | 1/1 | +0.022801 [-0.039319, 0.084921] | +0.022801 [-0.039319, 0.084921] | +10.266826 [-20.034032, 40.567685] | n/a |
| qwen | userspace | 64/1 | +0.014039 [-0.087127, 0.115205] | +0.464705 [-0.809867, 1.739276] | +4.720493 [-8.241062, 17.682049] | +0.007153 [-0.011609, 0.025916] |
| qwen | userspace | 1/8 | +6.371787 [6.025879, 6.717696] | +6.371787 [6.025879, 6.717696] | +2161.058315 [2077.897904, 2244.218726] | n/a |
| qwen | userspace | 64/8 | +0.134686 [-0.059663, 0.329034] | +1.695985 [-2.166354, 5.558324] | +69.166831 [-91.566563, 229.900226] | +0.024783 [-0.034506, 0.084071] |
| smol | kernel | 1/1 | +0.010223 [-0.023340, 0.043785] | +0.010223 [-0.023340, 0.043785] | +6.884203 [-19.646635, 33.415042] | n/a |
| smol | kernel | 64/1 | -0.008484 [-0.054542, 0.037574] | +0.006542 [-0.022398, 0.035483] | +0.220961 [-0.672087, 1.114008] | +0.000239 [-0.000569, 0.001046] |
| smol | kernel | 1/8 | +5.159548 [5.107920, 5.211176] | +5.159548 [5.107920, 5.211176] | +2869.034019 [2821.074091, 2916.993946] | n/a |
| smol | kernel | 64/8 | -0.070497 [-0.203320, 0.062326] | +1.040834 [0.598909, 1.482758] | +63.503572 [37.600568, 89.406575] | +0.017640 [0.011267, 0.024013] |
| smol | userspace | 1/1 | -0.012370 [-0.071840, 0.047099] | -0.012370 [-0.071840, 0.047099] | -11.554750 [-55.432195, 32.322694] | n/a |
| smol | userspace | 64/1 | -0.055264 [-0.134050, 0.023523] | -1.139779 [-3.066486, 0.786928] | -32.632644 [-87.750698, 22.485409] | -0.017215 [-0.046585, 0.012156] |
| smol | userspace | 1/8 | +4.925218 [4.701560, 5.148875] | +4.925218 [4.701560, 5.148875] | +2631.327383 [2369.434107, 2893.220659] | n/a |
| smol | userspace | 64/8 | -0.083918 [-0.290425, 0.122589] | -2.601941 [-7.892867, 2.688984] | -142.187187 [-439.267112, 154.892739] | -0.039969 [-0.121973, 0.042035] |

All c1 release-policy intervals cross0. All Qwen gen64 release intervals cross0; kernel long-output point estimates favor serial. Smol kernel gen64/c8 completion/TPS/TPOT intervals favor prefix, while its TTFT crosses0. Smol native gen64/c1 andc8 have negative completion/TPS/TPOT point estimates with intervals crossing0, including slow blocks0/4; retain them. No throughput equivalence or universal long-output benefit follows.

Transport controls under the prefix policy use native−kernel for latency/TPOT/completion and kernel−native for TPS. Positive favors kernel. These are secondary observed comparisons, subject to the exposure limitation below:

| Model | gen/c | TTFT ms [t95] | Completion ms [t95] | TPS [t95] | TPOT ms [t95] |
| --- | --- | --- | --- | --- | --- |
| qwen | 1/1 | +0.015544 [-0.012906, 0.043995] | +0.015544 [-0.012906, 0.043995] | +8.700239 [-5.075374, 22.475852] | n/a |
| qwen | 64/1 | -0.035463 [-0.111755, 0.040829] | -0.917068 [-2.456166, 0.622030] | -9.329290 [-24.950970, 6.292391] | -0.013994 [-0.037255, 0.009268] |
| qwen | 1/8 | -0.075200 [-0.158507, 0.008106] | -0.075200 [-0.158507, 0.008106] | -113.905197 [-268.311897, 40.501503] | n/a |
| qwen | 64/8 | -0.095339 [-0.173682, -0.016997] | -2.298094 [-6.626609, 2.030421] | -94.198338 [-276.939757, 88.543080] | -0.034964 [-0.102528, 0.032600] |
| smol | 1/1 | +0.058183 [0.014773, 0.101593] | +0.058183 [0.014773, 0.101593] | +42.196342 [8.157839, 76.234846] | n/a |
| smol | 64/1 | +0.067541 [-0.001032, 0.136115] | +1.130798 [-0.738697, 3.000293] | +32.320771 [-21.052867, 85.694408] | +0.016877 [-0.011844, 0.045598] |
| smol | 1/8 | +0.122814 [-0.039366, 0.284993] | +0.122814 [-0.039366, 0.284993] | +211.564794 [-59.437195, 482.566782] | n/a |
| smol | 64/8 | +0.080449 [-0.052344, 0.213242] | +3.446721 [-1.529726, 8.423167] | +195.974968 [-80.589620, 472.539557] | +0.053433 [-0.024285, 0.131150] |

Qwen prefix gen64/c8 TTFT nominally favors native by0.095339ms (kernel-favoring interval−0.173682..−0.016997); Smol prefix gen1/c1 TTFT nominally favors kernel by0.058183ms [0.014773,0.101593], with TPS also positive. Every other prefix transport interval crosses0. These opposite bounded outcomes cannot support a broad kernel/eBPF speed claim or syscall-only attribution.

## Numerical fidelity, host exposure and restoration

All c1 serial/prefix and prefix transport output comparisons match320/320 complete sequences. Concurrent outputs can differ with actual FP16 tensor shapes/batching even though every actual sequence matches its own independent graph replay. The independently recomputed concurrent agreement counts are:

| Model | Baseline→candidate | gen/c | Identical full sequences/320 | Identical first tokens/320 |
| --- | --- | --- | --- | --- |
| qwen | serial-kernel→prefix-kernel | 1/8 | 264 | 264 |
| qwen | serial-kernel→prefix-kernel | 64/8 | 287 | 287 |
| qwen | serial-userspace→prefix-userspace | 1/8 | 248 | 248 |
| qwen | serial-userspace→prefix-userspace | 64/8 | 284 | 284 |
| qwen | prefix-kernel→prefix-userspace | 1/8 | 301 | 301 |
| qwen | prefix-kernel→prefix-userspace | 64/8 | 295 | 295 |
| smol | serial-kernel→prefix-kernel | 1/8 | 320 | 320 |
| smol | serial-kernel→prefix-kernel | 64/8 | 290 | 320 |
| smol | serial-userspace→prefix-userspace | 1/8 | 320 | 320 |
| smol | serial-userspace→prefix-userspace | 64/8 | 288 | 320 |
| smol | prefix-kernel→prefix-userspace | 1/8 | 320 | 320 |
| smol | prefix-kernel→prefix-userspace | 64/8 | 286 | 320 |

Frozen unpadded reference diagnostics remain distinct from replay success. The strict counts are out of363 known valid sequences per executor; full totals are out of1320 including40 warmups per mode. No task-quality, batch invariance or output-equivalence claim follows:

| Model | Mode | Strict full sequence matches/363 | Strict first matches/363 | Full frozen sequence matches/1320 | Full frozen first matches/1320 |
| --- | --- | --- | --- | --- | --- |
| qwen | serial-kernel | 319 | 353 | 1173 | 1253 |
| qwen | prefix-kernel | 312 | 347 | 1116 | 1196 |
| qwen | serial-userspace | 310 | 343 | 1178 | 1258 |
| qwen | prefix-userspace | 319 | 352 | 1096 | 1176 |
| smol | serial-kernel | 314 | 363 | 1184 | 1320 |
| smol | prefix-kernel | 310 | 363 | 1174 | 1320 |
| smol | serial-userspace | 316 | 363 | 1188 | 1320 |
| smol | prefix-userspace | 309 | 363 | 1190 | 1320 |

The retained [host journal](completion_release_20261012/performance_host_journal.json) reports a **global OOM at23:06:50UTC**, killing unrelated Lean49PreparedB(pid2832007,anon-rss39,212,700kB), plus connection ping timeouts; reaping completes23:06:52. This falls within Smol block1 serial-kernel bootstrap(start23:06:10,ready23:07:07), after the paired prefix-kernel executor ended23:06:10. The fault precedes that serial ready/measured interval, so it is not a failed measured request or grounds to silently drop block1. However, host pressure before/after the kill is not continuously measured and exposure is unequal. Preserve the unchanged five-pair estimates; do not claim fault-free host operation, continuous GPU isolation, transport robustness, or an exact isolated treatment effect. No same-fault match is recorded in Qwen’s earlier interval, which is not proof of no shared interference. The narrow observed primary support and source/cell mechanism evidence remain, with this causal-attribution limitation explicit.

At23:17:55UTC the [owner receipt](completion_release_20261012/performance_owner_receipt.json) records the same boot04dc0087-5ccc-4c46-9997-b9a92f0e5167/kernel7.3.0-070300rc3-generic, no own serving process/module/pins and no current GPU application. [Workspace receipt](completion_release_20261012/performance_workspace_receipt.txt) records original UID3e8994f8-77ba-4a73-a3a5-35ed69a0a8a2 Running/Ready,zero restarts,on lab. This is post-run restoration evidence, not continuous isolation evidence. The pinned temporary runtime/build artifacts are deliberately retained for the immediate qualified default checks; base runtime/model cache/original owners and unrelated tools/setup_env.sh remain preserved.

## Full descriptive metrics and next decision

Each row contains320 measured requests. Means and finite-request quantiles are descriptive; TPS is the mean of five actual cell-throughput values. The largest retained TTFT samples are Qwen11.336110ms(block0 serial-kernel gen1/c8,index25) and Smol9.051891ms(block1 serial-native gen1/c8,index34); neither is excluded.

| Model | Mode | gen/c | Mean TTFT ms | p50 TTFT ms | p99 TTFT ms | Mean completion ms | Mean TPOT ms | Mean TPS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| qwen | serial-kernel | 1/1 | 1.464290 | 1.420679 | 2.639252 | 1.464290 | n/a | 676.623393 |
| qwen | prefix-kernel | 1/1 | 1.426892 | 1.404036 | 2.434130 | 1.426892 | n/a | 694.779554 |
| qwen | serial-userspace | 1/1 | 1.465237 | 1.433516 | 2.405510 | 1.465237 | n/a | 675.812489 |
| qwen | prefix-userspace | 1/1 | 1.442436 | 1.411694 | 2.265199 | 1.442436 | n/a | 686.079315 |
| qwen | serial-kernel | 64/1 | 1.374687 | 1.312102 | 2.459874 | 78.181241 | 1.219152 | 818.171720 |
| qwen | prefix-kernel | 64/1 | 1.406323 | 1.383493 | 2.233302 | 79.101341 | 1.233254 | 808.818426 |
| qwen | serial-userspace | 64/1 | 1.384899 | 1.355285 | 2.075194 | 78.648977 | 1.226414 | 813.427223 |
| qwen | prefix-userspace | 64/1 | 1.370860 | 1.317588 | 2.441835 | 78.184272 | 1.219261 | 818.147716 |
| qwen | serial-kernel | 1/8 | 8.821412 | 9.672046 | 10.816890 | 8.821412 | n/a | 893.394072 |
| qwen | prefix-kernel | 1/8 | 2.595630 | 2.628357 | 3.961812 | 2.595630 | n/a | 2938.468915 |
| qwen | serial-userspace | 1/8 | 8.892217 | 9.671301 | 11.089086 | 8.892217 | n/a | 891.315797 |
| qwen | prefix-userspace | 1/8 | 2.520429 | 2.550669 | 3.259822 | 2.520429 | n/a | 3052.374112 |
| qwen | serial-kernel | 64/8 | 2.210103 | 2.365839 | 3.048140 | 108.738193 | 1.690922 | 4704.210548 |
| qwen | prefix-kernel | 64/8 | 2.256484 | 2.425704 | 3.052496 | 110.396506 | 1.716508 | 4637.192941 |
| qwen | serial-userspace | 64/8 | 2.295831 | 2.419658 | 3.570456 | 109.794396 | 1.706326 | 4662.224448 |
| qwen | prefix-userspace | 64/8 | 2.161145 | 2.279826 | 3.199466 | 108.098412 | 1.681544 | 4731.391279 |
| smol | serial-kernel | 1/1 | 1.189327 | 1.158980 | 1.873420 | 1.189327 | n/a | 831.062911 |
| smol | prefix-kernel | 1/1 | 1.179105 | 1.161246 | 1.832375 | 1.179105 | n/a | 837.947115 |
| smol | serial-userspace | 1/1 | 1.224917 | 1.197895 | 2.152129 | 1.224917 | n/a | 807.305523 |
| smol | prefix-userspace | 1/1 | 1.237288 | 1.225889 | 1.912751 | 1.237288 | n/a | 795.750772 |
| smol | serial-kernel | 64/1 | 1.111007 | 1.066056 | 1.670018 | 45.960007 | 0.711889 | 1391.342501 |
| smol | prefix-kernel | 64/1 | 1.119492 | 1.096093 | 1.417831 | 45.953465 | 0.711650 | 1391.563462 |
| smol | serial-userspace | 64/1 | 1.131769 | 1.123813 | 1.636490 | 45.944484 | 0.711313 | 1391.875335 |
| smol | prefix-userspace | 64/1 | 1.187033 | 1.162380 | 1.591519 | 47.084263 | 0.728527 | 1359.242691 |
| smol | serial-kernel | 1/8 | 7.050603 | 7.688284 | 8.405044 | 7.050603 | n/a | 1115.012197 |
| smol | prefix-kernel | 1/8 | 1.891055 | 1.943718 | 2.764498 | 1.891055 | n/a | 3984.046216 |
| smol | serial-userspace | 1/8 | 6.939086 | 7.668322 | 8.330107 | 6.939086 | n/a | 1141.154039 |
| smol | prefix-userspace | 1/8 | 2.013869 | 2.009332 | 2.871605 | 2.013869 | n/a | 3772.481422 |
| smol | serial-kernel | 64/8 | 1.684107 | 1.784314 | 2.405375 | 92.402984 | 1.439982 | 5535.610626 |
| smol | prefix-kernel | 64/8 | 1.754604 | 1.902884 | 2.655025 | 91.362150 | 1.422342 | 5599.114198 |
| smol | serial-userspace | 64/8 | 1.751136 | 1.828293 | 2.536225 | 92.206930 | 1.435806 | 5545.326416 |
| smol | prefix-userspace | 64/8 | 1.835053 | 1.896750 | 2.971645 | 94.808871 | 1.475775 | 5403.139230 |

This completed comparison adds supporting scheduler evidence beyond the closed packing study. It supports the qualified prefix-release behavior for the tested short concurrent token-ID HTTP workloads. Minimal default adoption can use the already-qualified packed/prefix mechanism while preserving explicit serial/grouped reproduction controls, provided the actual ordinary untraced source/binary paths receive the planned real output/lifecycle checks. Those checks are a subsequent adoption qualification, not another outcome of this traced matrix. Dynamic untraced timing remains unqualified. Do not repeat this unchanged matrix to remove inconvenient rows or improve intervals.

The broader retained full-service objective stays open. This experiment proves neither external SOTA/novelty nor arbitrary-model support, text/API/task quality, total CPU/energy, physical-NIC performance, no-userspace implementation beyond the qualified path, or a universal eBPF gain. No scientific blocker was found within the stated traced/replay contract; the disclosed host exposure and FP16 trajectory differences limit attribution and scope rather than disappear on publication.
