# Fresh result review: CQ progress before SQ submission

Reviewed independently after full timing on 2026-10-14 UTC. This report makes no source, plan, oracle, paper or infrastructure edits and launches no serving run. The reviewer read the admitted plan and round-one review, frozen source and commands, raw timing/qualification evidence, source-native driver/client/backend/analyzer, BPF loop, loader/transport and native wait implementation. The reviewer replayed both timing analyzers and all four strict analyzers, then separately reconstructed request timing, every process-block contrast and interval directly from raw observations.

## Separate judgments

- **Run status: valid**, complete for the admitted finite local adapter/workload contract.
- **Tested hypothesis: inconclusive.** All four predeclared native primary intervals cross zero. No verified client-delivery gain from the CQ-before-submit intervention is established.
- **Research value: supporting.** This is a new matched source intervention with a genuine former-loop control; it bounds a plausible coordination explanation. Qualification and publication are dependencies, not extra research contributions.
- **Paper impact: mechanism or workload boundary**, adding scoped evidence to the retained ordinary-serving question. There is no formal paper RQ/thesis here and no direct thesis challenge.
- **Next paper decision:** close unchanged timing, publish the full mixed/negative/inconclusive record, and do not promote this as a demonstrated performance optimization or native superiority. A further redesign needs a new causal discriminator with higher value than repeated small loop variants; optimized cross-node/service acceptance remains an unresolved alternative identified by the plan. This review does not authorize another experiment, scope change or code rollback.

## Completion, commands and execution history

Frozen timing source is d45b82f255c2b4afc452ba482b90b092c52e08bc on the original /workspaces/repository/main. source_frozen.json records publication before timing and only unrelated tools/setup_env.sh left untracked. Both raw metadata commits equal this source. Embedded driver, client, Python backend and native CUDA source are byte-identical to files read during review. The implementation diff from f5a555d is confined to BPF snapshot selection, bootstrap object selection and corresponding Makefile targets for these source paths; model source is unchanged.

The archived performance_pipeline.py binds the actual original Workspace, temporary pinned environment, two exact checkpoint snapshots, frozen-reference path and source-native commands. Both actual benchmark child exits and both analyzer exits in performance_status.json are zero. Each raw file independently ends with terminal exit_code 0. All 36 executor exits are zero and executor_terminal.success is true; each admits and retires 264 requests, with graph_error 0. No failed timing executor, omitted cell or replacement is observed.

Per model: 18 executors, all six permutations of (uring_loop, userspace, uring_loop_after), four rotated cells gen1/gen64 x c1/c8, 64 measured requests per cell. Independently checked all 72 cell coordinates, exact request indices 0..63, permutation order and pair modulo-four cell rotation. Per model there are 4608 measured requests/149760 tokens and 144 excluded, checked gen1 warmups. Combined: 144 cells, 9216 measured requests/299520 tokens plus 288 warmups; raw totals including warmups are 9504 requests/299808 tokens. Warmups are excluded from timing/CPU metric construction. No outlier or failed row was removed to create a favorable mean.

Real preflight and full strict/HF qualification occurred before the source freeze/timing. The first preflight succeeds; no retry/deviation is recorded for this experiment. All four strict raw analyzers replay at exit 0 with stdout byte-identical to the archived analyses, covering all 12 strict executors, 7464 requests/266688 valid tokens, 3108 intentional rejects and 60000 empty connections. HF candidate lifecycle records pass both unchanged 32-request/652 checked complete-or-prefix-token cases, 13 closes and 3 expected aborts per model. These are validation dependencies, not performance results.

Timing begins at 04:20:06 UTC, Qwen runs first and Smol begins at 04:29:44 UTC; final Smol raw terminal is 04:38:29 UTC. There is no overlap or restarted/replaced benchmark in the recorded sequence. performance_observation_disconnect.json records local SSH observation session 48829 exit 1 at 04:34:46 with unknown transport cause; reconnection identifies the original remote pipeline PID 282080 and Smol driver PID 286552 still live. Later real child exits, full raw terminals and all analysis outputs establish experiment completion. The remote wrapper exit itself remains unobserved and must not be described as zero. This is an observation-channel failure, not evidence that a benchmark client failed. Conversely, the available record cannot prove that it had absolutely no scheduling/measurement impact.

performance_start/end.json report the same boot ID, original base package versions and no own residual app/module/pins at endpoints. Initial loadavg is 13.54/14.21/14.79. The timing-bracket journal receipt exits 0 but returns only '-- No entries --'; this does not establish no unlogged faults or continuous resource isolation. No continuous host/GPU exclusive-use claim is warranted. Final apparatus restoration is still pending this review and must have its own receipt; it does not change already-complete numerical evidence.

## Mechanism and independent baseline audit

Candidate and former-loop are built from the same bpf/uring_loop.bpf.c. Candidate samples CQ tail before SQ head/tail sampling and bpf_io_uring_submit_sqes, and waits for the saved tail plus one during service. BF_IO_CQ_AFTER_SUBMIT restores the exact former post-submission tail-plus-one behavior. Both preserve current-tail/no-sleep quiesced cleanup. executor/io_uring_tcp.h selects the corresponding object only at bootstrap. The archived compiled dispatch and GPU io_network SASS identity receipt reports 428852 and 461984 characters respectively, byte-identical candidate/control. This establishes matched GPU implementations; it does not establish identical request arrival, batching, KV history or graph count.

The source-backed possibility is real: upstream [loop.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c) compares cq_wait_idx to CQ tail and waits only while progress is still required; [io_uring.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.c) completes submission-state processing. This motivates the intervention but no run-time counter here measures how many avoidable sleeps occurred. No exclusive cause of prior 0044 delivery loss or direct proof of recovered waits can be inferred.

The main baseline is source-native timed-epoll TCP with the same packed/prefix vLLM model computation, not full external vLLM HTTP service or SOTA. All 12 timing baseline logs explicitly engage epoll_pwait2 timeout_ns=60000; full strict traces after ready show actual accept4, recvfrom and sendmsg. For Qwen traced native counts are 5146/12826/22374; Smol 5147/12829/22305. Baseline admits/retires every expected request normally and did not fail or run with different model math/information. The reviewer found no avoidable interface failure that could be counted as a candidate win.

Former-loop is a component control, not an independent main competitor. Both loop variants use SINGLE_ISSUER/DEFER_TASKRUN without SQPOLL. After-ready strict traces for both models/variants show exactly one steady zero-submit io_uring_enter, no steady userspace accept/receive/send calls; a separate post-SIGTERM cleanup entry is not a steady request worker. Timing task inventories contain no iou-sqp thread in either variant. HF shows the same one-steady-entry pattern. GPU completion/controller arithmetic, timer and wire remain common. SQ head equals SQ tail and CQ head equals CQ tail at termination with pending/error/reserved/drop/overflow zero; SQ and CQ counts need not equal under multishot. The separate ring trace_overflow=136 for 264 timing requests is the expected fixed 128-entry diagnostic capacity; it is not a CQ overflow or numerical BF_TRACE loss (trace_overflows=0).

All conditions share vLLM 0.31.0, Torch 2.13+cu129, Transformers 5.17, FP16, checkpoint revisions, prompts and temporary libbpf 1.6.3. Common dependencies are archived. Native waits and multishot timer both have nominal 60000 ns settings, which do not imply identical real wake spacing. Source intervention intentionally changes completion coordination, not the timer or backend. Scope is same-compute local low-concurrency adapter delivery, not identical concurrent batch trajectories, arbitrary model portability or full HTTP service acceptance.

## Numerical fidelity and leakage

frozen_references.json is byte-identical to finding 0044's asset, with frozen_at 2026-10-13T04:16:47.805543+00:00 before these outputs. Qwen has 17 prompt/gen keys and 22 qualified whole sequences; Smol 17 keys/19 sequences. The reviewer independently checked every valid ordinary response against its exact whole-sequence set, including warmups. There is no tokenwise union, post-observation expansion, tolerance or replacement. Raw frozen-reference metadata equals the archived asset. These references derive from prior independent upstream graph trajectory replay; the traced backend separately replays actual captured histories and asserts its independently computed output against recorded tokens.

This is bounded numerical evidence: ordinary current batch and KV trajectories are unobserved. Request-index-matched whole-output agreement is Qwen 1482/1536 versus native and 1482/1536 versus former-loop; Smol 1500/1536 versus native and 1499/1536 versus former-loop. Exact same outputs across concurrent implementations are therefore not established, even though all are individually in the prequalified set and use the same algorithms. Neither task quality, universal numerical correctness nor current ordinary trajectory replay follows.

## Metric reconstruction and uncertainty

Both timing analyzers replay at exit 0 with stdout byte-identical to archives and no stderr. Independently, TTFT and completion are recomputed from start_ns/arrival_ns; TPOT from first/last arrivals over gen-minus-one. TPS is each cell's count*gen divided by last arrival minus first start, then the six process-cell values are averaged. CPU is reconstructed from bracketing process CPU clocks; all bracket windows enclose the corresponding observed client interval. These independent computations match every source-native paired estimate and nominal interval. Floating operation order in an independent TPOT expression changes only roundoff; the source-native exact-order check matches every raw value.

Pair is the process-block unit; requests are not treated as independent statistical replicates. Six paired differences form each nominal two-sided t interval, df 5, critical 2.570581835636305. All four primary intervals are reported, without familywise claim, equivalence, noninferiority threshold or overall score. Six blocks on one host/time window are a small finite sample and do not eliminate temporal confounding. Balanced transport permutations and cell rotations reduce order bias but do not prove isolation.

Positive effects below favor candidate: TTFT/completion/TPOT/CPU are baseline-minus-candidate, TPS is candidate-minus-baseline.
## Four predeclared primary native effects

| Model | Metric / cell | Favorable effect | Nominal t95 | Judgment |
|---|---|---:|---|---|
| qwen | ttft_ms, gen1/c8 | -0.073753625 | [-0.192305624, 0.044798374] | inconclusive |
| qwen | tokens_per_s, gen64/c8 | -116.887239445 | [-261.334557894, 27.560079005] | inconclusive |
| smol | ttft_ms, gen1/c8 | 0.050052042 | [-0.116827823, 0.216931906] | inconclusive |
| smol | tokens_per_s, gen64/c8 | 78.800847252 | [-129.197723183, 286.799417687] | inconclusive |

Qwen primary points favor native; Smol primary points favor candidate. All cross zero. The hypothesis is inconclusive, neither disproven in every metric nor supported by a demonstrated primary gain. These results cannot be described as equivalent performance. Qwen long-output TPS is about 2.49% below native by point estimate, Smol about 1.47% above, without a reliable primary interval in either direction.

## Component and secondary results, including all negative estimates

The following complete effect table retains every primary/secondary delivery effect and known-worker CPU effect for every cell and both comparisons. CPU values are expressed in ms/request; negative CPU effects mean higher candidate CPU cost. Executor CPU and known-worker CPU are identical here, since no custom TX module is present; separate module TX CPU is exactly zero by construction, not total kernel TCP cost zero.

### qwen: all paired effects

| Baseline | Gen/c | Metric | Favorable effect | Nominal t95 |
|---|---|---|---:|---|
| userspace | 1/1 | ttft_ms | -0.037965690 | [-0.122053663, 0.046122283] |
| userspace | 1/1 | completion_ms | -0.037965690 | [-0.122053663, 0.046122283] |
| userspace | 1/1 | tokens_per_s | -19.819270151 | [-65.574447459, 25.935907157] |
| userspace | 1/1 | CPU ms/request | -0.004324247 | [-0.011056297, 0.002407802] |
| uring_loop_after | 1/1 | ttft_ms | -0.040522169 | [-0.102602546, 0.021558208] |
| uring_loop_after | 1/1 | completion_ms | -0.040522169 | [-0.102602546, 0.021558208] |
| uring_loop_after | 1/1 | tokens_per_s | -21.118666929 | [-54.105986148, 11.868652291] |
| uring_loop_after | 1/1 | CPU ms/request | -0.003142484 | [-0.008505440, 0.002220471] |
| userspace | 64/1 | ttft_ms | 0.006717018 | [-0.054261076, 0.067695112] |
| userspace | 64/1 | completion_ms | -0.171663854 | [-1.738068012, 1.394740304] |
| userspace | 64/1 | tokens_per_s | -1.802891575 | [-17.695171684, 14.089388534] |
| userspace | 64/1 | tpot_ms | -0.002831442 | [-0.026735322, 0.021072437] |
| userspace | 64/1 | CPU ms/request | -0.509075229 | [-0.587849961, -0.430300497] |
| uring_loop_after | 64/1 | ttft_ms | 0.006686016 | [-0.061447421, 0.074819453] |
| uring_loop_after | 64/1 | completion_ms | -0.041505622 | [-1.395113189, 1.312101945] |
| uring_loop_after | 64/1 | tokens_per_s | -0.434478078 | [-14.133880451, 13.264924296] |
| uring_loop_after | 64/1 | tpot_ms | -0.000764947 | [-0.021195957, 0.019666064] |
| uring_loop_after | 64/1 | CPU ms/request | 0.029529802 | [-0.076629273, 0.135688877] |
| userspace | 1/8 | ttft_ms | -0.073753625 | [-0.192305624, 0.044798374] |
| userspace | 1/8 | completion_ms | -0.073753625 | [-0.192305624, 0.044798374] |
| userspace | 1/8 | tokens_per_s | -167.590019477 | [-260.945626003, -74.234412952] |
| userspace | 1/8 | CPU ms/request | 0.002317688 | [-0.001081202, 0.005716577] |
| uring_loop_after | 1/8 | ttft_ms | 0.021149464 | [-0.154021974, 0.196320901] |
| uring_loop_after | 1/8 | completion_ms | 0.021149464 | [-0.154021974, 0.196320901] |
| uring_loop_after | 1/8 | tokens_per_s | 5.812739254 | [-167.308155679, 178.933634188] |
| uring_loop_after | 1/8 | CPU ms/request | 0.000713510 | [-0.002481277, 0.003908298] |
| userspace | 64/8 | ttft_ms | -0.039427018 | [-0.216585497, 0.137731460] |
| userspace | 64/8 | completion_ms | -2.625217516 | [-6.122125848, 0.871690816] |
| userspace | 64/8 | tokens_per_s | -116.887239445 | [-261.334557894, 27.560079005] |
| userspace | 64/8 | tpot_ms | -0.041044294 | [-0.095005727, 0.012917140] |
| userspace | 64/8 | CPU ms/request | -0.060560951 | [-0.108529213, -0.012592688] |
| uring_loop_after | 64/8 | ttft_ms | -0.106719430 | [-0.182103109, -0.031335750] |
| uring_loop_after | 64/8 | completion_ms | -1.643827917 | [-4.710320326, 1.422664492] |
| uring_loop_after | 64/8 | tokens_per_s | -64.543136128 | [-192.914598880, 63.828326623] |
| uring_loop_after | 64/8 | tpot_ms | -0.024398547 | [-0.073031930, 0.024234835] |
| uring_loop_after | 64/8 | CPU ms/request | 0.006686911 | [-0.020917626, 0.034291449] |

### smol: all paired effects

| Baseline | Gen/c | Metric | Favorable effect | Nominal t95 |
|---|---|---|---:|---|
| userspace | 1/1 | ttft_ms | 0.055868328 | [-0.028254837, 0.139991493] |
| userspace | 1/1 | completion_ms | 0.055868328 | [-0.028254837, 0.139991493] |
| userspace | 1/1 | tokens_per_s | 45.459034624 | [-24.101170912, 115.019240159] |
| userspace | 1/1 | CPU ms/request | -0.002826742 | [-0.011125917, 0.005472433] |
| uring_loop_after | 1/1 | ttft_ms | 0.048383576 | [-0.019555336, 0.116322487] |
| uring_loop_after | 1/1 | completion_ms | 0.048383576 | [-0.019555336, 0.116322487] |
| uring_loop_after | 1/1 | tokens_per_s | 41.144162957 | [-14.605076766, 96.893402679] |
| uring_loop_after | 1/1 | CPU ms/request | 0.004377984 | [-0.001962720, 0.010718689] |
| userspace | 64/1 | ttft_ms | 0.058103833 | [0.024077546, 0.092130121] |
| userspace | 64/1 | completion_ms | 0.011872872 | [-1.183979312, 1.207725057] |
| userspace | 64/1 | tokens_per_s | -0.174743571 | [-34.457380194, 34.107893051] |
| userspace | 64/1 | tpot_ms | -0.000733825 | [-0.019193964, 0.017726314] |
| userspace | 64/1 | CPU ms/request | -0.322279573 | [-0.393012162, -0.251546984] |
| uring_loop_after | 64/1 | ttft_ms | -0.003017081 | [-0.022685072, 0.016650910] |
| uring_loop_after | 64/1 | completion_ms | -0.095690148 | [-0.296334942, 0.104954646] |
| uring_loop_after | 64/1 | tokens_per_s | -2.808787524 | [-8.720232024, 3.102656977] |
| uring_loop_after | 64/1 | tpot_ms | -0.001471001 | [-0.004630798, 0.001688796] |
| uring_loop_after | 64/1 | CPU ms/request | -0.036555271 | [-0.114327310, 0.041216769] |
| userspace | 1/8 | ttft_ms | 0.050052042 | [-0.116827823, 0.216931906] |
| userspace | 1/8 | completion_ms | 0.050052042 | [-0.116827823, 0.216931906] |
| userspace | 1/8 | tokens_per_s | -89.366315118 | [-411.095108441, 232.362478204] |
| userspace | 1/8 | CPU ms/request | 0.001441250 | [-0.002695979, 0.005578479] |
| uring_loop_after | 1/8 | ttft_ms | 0.027858268 | [-0.013878212, 0.069594748] |
| uring_loop_after | 1/8 | completion_ms | 0.027858268 | [-0.013878212, 0.069594748] |
| uring_loop_after | 1/8 | tokens_per_s | -9.454436765 | [-98.496431291, 79.587557762] |
| uring_loop_after | 1/8 | CPU ms/request | -0.000782409 | [-0.005454734, 0.003889916] |
| userspace | 64/8 | ttft_ms | 0.045706430 | [-0.105093175, 0.196506034] |
| userspace | 64/8 | completion_ms | 1.533792094 | [-2.163146994, 5.230731181] |
| userspace | 64/8 | tokens_per_s | 78.800847252 | [-129.197723183, 286.799417687] |
| userspace | 64/8 | tpot_ms | 0.023620407 | [-0.033840651, 0.081081466] |
| userspace | 64/8 | CPU ms/request | -0.053962385 | [-0.086375321, -0.021549450] |
| uring_loop_after | 64/8 | ttft_ms | 0.019340865 | [-0.082533597, 0.121215327] |
| uring_loop_after | 64/8 | completion_ms | 0.902252753 | [-1.237765781, 3.042271286] |
| uring_loop_after | 64/8 | tokens_per_s | 56.167848198 | [-55.068776910, 167.404473307] |
| uring_loop_after | 64/8 | tpot_ms | 0.014014474 | [-0.019842579, 0.047871528] |
| uring_loop_after | 64/8 | CPU ms/request | 0.011231599 | [-0.030776988, 0.053240186] |

At nominal intervals, Qwen gen1/c8 TPS is lower than native by 167.590019 token/s [74.234413, 260.945626] (approximately 5.45% by point estimate), despite gen1/c8 TTFT being primary-inconclusive. Candidate Qwen gen64/c8 TTFT is worse than former-loop by 0.106719 ms [0.031336, 0.182103], a negative component result that must not be hidden by the theory. Smol gen64/c1 TTFT improves over native by 0.058104 ms [0.024078, 0.092130], a secondary result that cannot replace the declared primaries or establish CQ-snapshot superiority: its same-cell before/after component interval crosses zero.

All before/after throughput intervals cross zero. At gen64/c8, Qwen before/after TPS effect is -64.543136 [-192.914599, 63.828327]; Smol +56.167848 [-55.068777, 167.404473]. All before/after CPU intervals cross zero. Component data therefore does not establish a robust overall delivery or CPU benefit from the isolated change.

Process CPU is higher than native for both long-output cells in both models. Gen64/c8 candidate/native/former costs are Qwen 0.550996/0.490435/0.557682 ms/request; Smol 0.489155/0.435193/0.500387. Native-minus-candidate long-output CPU intervals are wholly negative. At gen64/c1 the same costs are Qwen 2.831195/2.322120/2.860725 and Smol 1.701385/1.379105/1.664830. The nominal before/after CPU differences are inconclusive, so prior 0044's approximately 96% SQPOLL reduction must not be attributed to this new snapshot change or recalculated by combining unmatched sessions.

CPU attribution is limited to CLOCK_PROCESS_CPUTIME_ID brackets for the executor (all its threads, including creator-task kernel work once). It excludes client CPU, RX/softirq/BPF/TCP work elsewhere and energy. Timer CQ activity is real and substantial; complete timing CQ totals range 104587..107090 for Qwen candidate and 103924..107090 former, 69338..71543 for Smol candidate and 69229..71535 former. These counts do not isolate needless waits or total CPU, and cannot prove the timer is the exclusive bottleneck.

## Descriptive distribution table and retained extremes

P50/P99 below are pooled finite-sample nearest-rank TTFT descriptions, without paired confidence intervals. They are not robust tail-latency or superiority claims.

| Model | Mode | Gen/c | TTFT mean ms | P50 ms | P99 ms | Completion mean ms | TPS | CPU ms/request |
|---|---|---|---:|---:|---:|---:|---:|---:|
| qwen | uring_loop | 1/1 | 1.411831 | 1.397251 | 1.577620 | 1.411831 | 700.803706 | 0.058166 |
| qwen | userspace | 1/1 | 1.373866 | 1.342898 | 2.150564 | 1.373866 | 720.622976 | 0.053841 |
| qwen | uring_loop_after | 1/1 | 1.371309 | 1.350448 | 1.710331 | 1.371309 | 721.922373 | 0.055023 |
| qwen | uring_loop | 64/1 | 1.352493 | 1.339704 | 1.570113 | 78.699128 | 812.884300 | 2.831195 |
| qwen | userspace | 64/1 | 1.359210 | 1.302829 | 2.906988 | 78.527464 | 814.687191 | 2.322120 |
| qwen | uring_loop_after | 64/1 | 1.359179 | 1.327065 | 1.638974 | 78.657623 | 813.318778 | 2.860725 |
| qwen | uring_loop | 1/8 | 2.595156 | 2.668428 | 3.390669 | 2.595156 | 2906.184698 | 0.021380 |
| qwen | userspace | 1/8 | 2.521403 | 2.520582 | 3.306305 | 2.521403 | 3073.774717 | 0.023698 |
| qwen | uring_loop_after | 1/8 | 2.616306 | 2.641200 | 5.378489 | 2.616306 | 2900.371958 | 0.022094 |
| qwen | uring_loop | 64/8 | 2.343578 | 2.451862 | 3.814316 | 111.684560 | 4576.208668 | 0.550996 |
| qwen | userspace | 64/8 | 2.304151 | 2.386280 | 5.246592 | 109.059342 | 4693.095908 | 0.490435 |
| qwen | uring_loop_after | 64/8 | 2.236858 | 2.371420 | 2.990216 | 110.040732 | 4640.751804 | 0.557682 |
| smol | uring_loop | 1/1 | 1.112269 | 1.108686 | 1.444975 | 1.112269 | 891.993742 | 0.046875 |
| smol | userspace | 1/1 | 1.168137 | 1.139633 | 1.460684 | 1.168137 | 846.534708 | 0.044048 |
| smol | uring_loop_after | 1/1 | 1.160652 | 1.135878 | 1.440932 | 1.160652 | 850.849579 | 0.051253 |
| smol | uring_loop | 64/1 | 1.101647 | 1.093430 | 1.351081 | 46.472307 | 1376.091522 | 1.701385 |
| smol | userspace | 64/1 | 1.159751 | 1.156288 | 1.418745 | 46.484179 | 1376.266266 | 1.379105 |
| smol | uring_loop_after | 64/1 | 1.098630 | 1.081315 | 1.322387 | 46.376616 | 1378.900310 | 1.664830 |
| smol | uring_loop | 1/8 | 1.994043 | 2.030916 | 2.551455 | 1.994043 | 3701.153548 | 0.019770 |
| smol | userspace | 1/8 | 2.044095 | 2.056792 | 2.653759 | 2.044095 | 3790.519863 | 0.021211 |
| smol | uring_loop_after | 1/8 | 2.021901 | 2.073108 | 2.558133 | 2.021901 | 3710.607985 | 0.018988 |
| smol | uring_loop | 64/8 | 1.767404 | 1.883453 | 2.420294 | 93.816342 | 5453.524713 | 0.489155 |
| smol | userspace | 64/8 | 1.813111 | 1.853541 | 3.497854 | 95.350134 | 5374.723866 | 0.435193 |
| smol | uring_loop_after | 64/8 | 1.786745 | 1.913007 | 2.569255 | 94.718594 | 5397.356865 | 0.500387 |

All extremes remain. Overall measured TTFT maxima are Qwen candidate 4.220228 ms (pair3 gen1/c8 index8), native 5.692706 (pair4 gen64/c8 index32), former 5.454723 (pair0 gen1/c8 index35); Smol candidate 3.105172 (pair1 gen1/c8 index50), native 3.582923 (pair5 gen64/c8 index13), former 3.418807 (pair0 gen64/c8 index56). No cause is established from maxima alone.

Primary paired values, in process block order 0..5, are:
- qwen ttft_ms, gen1/c8: 0.012838063, -0.238662344, 0.015494063, 0.012526234, -0.055348297, -0.189369469.
- qwen tokens_per_s, gen64/c8: 18.611447204, -319.316629593, -259.229249505, -32.561218099, -44.111878300, -64.715908376.
- smol ttft_ms, gen1/c8: 0.310772938, 0.082515781, -0.037902687, 0.060525562, -0.172463750, 0.056864406.
- smol tokens_per_s, gen64/c8: 420.996094836, -45.914208735, -27.023315232, 221.227523257, -47.133454307, -49.347556308.

This preserves the large negative Qwen TPS pair1/2 (-319.316630/-259.229250) and large positive Smol pair0/3 (+420.996095/+221.227523). Smol's positive mean is not a consistent per-block win: four of six TPS differences are negative. Balanced ordering and retained outliers are preferable to post hoc exclusions, but the uncertainty and environmental limits remain.

## Claim routing and remaining uncertainty

Supported: finite qualification, source-isolated before/after implementation, normal raw completion, same upstream computation, no steady userspace request/socket worker in qualified loop traces, upstream module-free TCP path, and this matched finite set of delivery/CPU estimates.

Unsupported: primary native improvement; universal correctness/task quality; identical ordinary batching/KV/output trajectories; superiority to official external vLLM HTTP service; familywide or broad model superiority; elimination of CPU entirely; total system CPU or energy savings; measured recovery of a specific count of avoidable waits; an exclusive cause of prior losses; continuous host isolation; zero remote wrapper exit after SSH disconnect; completed apparatus cleanup before a separate restoration receipt.

At review time docs/findings/0045-uring-cq-progress.md and docs/evaluation.md still describe pending timing. They need honest completed/inconclusive wording and the four primary intervals, negative secondary/component evidence, CPU limits and observation-disconnect caveat. Those updates and final restoration/publication are delivery work for the parent, not an additional scientific run. The complete project objective remains unfulfilled and is not narrowed by this supporting result.
