# Independent result review: adaptive kernel-loop wait

Review time: 2026-10-15 UTC. Scope: the completed run in this directory, its approved plan and source repair. The reviewer inspected the original Workspace main worktree and OS-TEMP artifacts, ran CPU-only analyses, and did not change application source, start a GPU workload, publish Git changes, or alter the user's objective.

## Separate judgments

- **Run status: valid for the repaired finite traced comparison.** The initial Qwen qualification is invalid as natural helper-stop/liveness evidence and remains a separately preserved failure. It is not silently included in the repaired result.
- **Tested hypothesis: contradicted as the full conjunction of lower process CPU and no adverse delivery.** The predeclared primary CPU component is supported in both models, with all five paired blocks lower. The Smol gen64/c8 fixed-pattern wall TPS is lower in all five paired blocks, with its nominal interval wholly below zero. Thus the experiment is a mixed CPU/delivery result, not an unqualified optimization win. This secondary result does not invalidate the primary CPU measurement or turn an otherwise completed run into an invalid experiment.
- **Research value: supporting.** It adds new intervention evidence that reducing idle heartbeat completions reduces this constructor's measured process cost, while exposing shutdown and delivery tradeoffs. Protocol/build/packaging work alone is dependency evidence.
- **Paper impact: mechanism or workload boundary.** It does not challenge a necessary thesis prediction or establish eBPF superiority, lower total service CPU, saturated throughput, arbitrary-backend support, or ordinary untraced numerical fidelity.
- **Next paper decision:** report the process-CPU saving together with the adverse Smol wall-delivery row and native-boundary results. Under the plan's stated mixed-result policy, retain original production behavior and archive the candidate rather than claiming a default latency/TPS improvement. A retained shared production patch would separately need the promised affected-constructor regressions; this result review is neither authority for selection nor for another experiment/review loop. The larger user goal remains open.

## What was inspected and recomputed

Read plan.md, the entire plan-review.md (including the after-submit counterexample, executable review and final source-local helper-stop follow-up), execution-notes.md, setup/run/rebuild/serving/analysis/idle/lifecycle sources, private Makefiles, all three production/private/original source differences, exact expanded commands/build logs/statuses/package records, preflight outputs, the first failed/manual-assisted qualification, repaired two-model protocol and lifecycle outputs, every full raw matrix file, corresponding graph traces and references via the analysis path, host receipts and preservation records.

CPU-only command:

```sh
/usr/bin/python3 /tmp/bpfusion-adaptive-wait-nwu1nulh/reviewer_recompute.py
```

The script reruns analysis.py on preflight_qwen, qualification_repaired_qwen, qualification_repaired_smol, full_qwen and full_smol. All five return zero and reproduce the saved analysis stdout/stderr byte-for-byte. The script separately derives metrics from raw request arrival timestamps, wall windows and process-clock snapshots; it independently matches **12 metric rows and all 78 signed contrasts**, including duplicate known-worker CPU and zero module-TX rows. It also recomputes p50/p99 and retains every outlier. See [complete recomputation tables and five-block differences](reviewer-recomputation.md), reviewer_recompute.py and the five *.reviewer.stdout/stderr pairs. No result is inferred merely from full.exit.json.

## Source and environment audit

The base is main d87b8e0bc1584123f2c0296ae13ab2dac999a2d6. Both private model CU files are byte-identical to unchanged executor/vllm_graph.cu; the saved Python upstream graph/history replay is byte-identical to current executor/vllm_graph.py. No model math/graph constructor change is present.

Original queue/BPF sources match HEAD. The private original io_uring header differs from HEAD only in the private BPF object pathname. Private candidate versus production-candidate differs only in its paired private object pathname. Current production source matched the three production-candidate snapshots during review. Quote-inclusion of io_uring_tcp.h beside each private CU plus the first variant queue include path resolves each model build against its intended headers. Original native computation is compiled from original CU/header paths. The expanded build logs actually show BF_TRACE for all measured conditions, BF_PAD_PREFILL and BF_PREFIX_RELEASE in both transports, and BF_USER_NETWORK/BF_USER_NETWORK_WAIT for native. Kernel-loop compile flags and the corresponding original/candidate BPF objects are distinct. The experiment's broad Makefile path substitutions are only demonstrated for these explicit targets, not a general alternative build system.

The existing io_uring_tcp.h.diff contains adapter noise: its old side is private original and its new side production candidate, so its object-path hunk is not a production behavior change. Preserve that raw file but use a HEAD-versus-production-candidate diff for an OSS production-patch description.

Recorded private packages are vLLM 0.31.0, Torch 2.13.0+cu129, Transformers 5.17.0, NumPy 2.3.5, Triton 3.7.1 and FlashInfer 0.7.0.post1, with libbpf 1.6.3 and NVCC 13.0.88 in the declared setup path. Setup/build/rebuild exits are zero. Qwen and Smol model paths name the fixed revisions declared in the plan. The runner removes VLLM_BATCH_INVARIANT from its environment; the measured comparison uses default optimized FP16 graph computation with tracing, not finding0059's batch-invariant mode. No profiler is used for full performance cells.

The intervention adds cq_seen/timer_may_idle/now_ns only to the internal registered loop-control prefix; it does not change the model shared bf_page ABI or create a new map/public flag. Acknowledgement follows GPU CQ handling and SQ publication via system fence and release store. Before-submit BPF snapshots precede SQ sampling; while a long timer may be active, an unacknowledged CQ target prevents sleeping before the GPU can publish follow-up work. The existing after-submit macro excludes adaptive state/update/ack behavior and preserves its fixed-timer wait expression, addressing the plan review's concrete race by preserving that constructor. This is finite Linux/x86/CUDA evidence, not a portable memory-model proof.

The source keeps the 60 us active timer and updates the same multishot timer to remaining service lifetime only when model queues are idle. It accepts transient ENOENT/EALREADY update races, suppresses new updates while stopping and drains existing operations. The Linux 7.3-rc3 [loop source](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/io_uring/loop.c) and [timeout source](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/io_uring/timeout.c) support the CQ-index/signal waiting and timer-update interpretation. Sparse CQ counts support engagement: full candidate final CQ counts range 3340–5458 versus fixed-loop 92776–98309, while all ring endpoints drain. Counts include network/update/cleanup events and are not an exact attribution of timer CPU.

## Execution chronology and deviations

1. Pre-execution review preserved the existing after-submit behavior and corrected the plan's erroneous main-client timeout description to source-native 60 seconds. Lifecycle retained its separately existing 15-second sockets. These corrections preceded observation.
2. Setup completed. The first real preflight exercised all three Qwen conditions, both cells and the exact wave/gap measurement path. Each executor delivered 72 requests/2088 tokens (64 measured/2080 plus 8 warmups); total 216 requests/6264 tokens. Its analysis and all independent-history checks pass.
3. The separate actual-model empty 2-second service check exits naturally, with zero admissions and drained successful cleanup. The observed ready-to-Python-exit interval is 7.034972425 seconds within the fixed 15-second observation bound. That includes replay/teardown and does not establish an exact native 2-second deadline or quantify native deadline overshoot.
4. First qualification completed all 622 Qwen replies, but a SIGTERM delivered to a helper at 06:12:35 UTC left the owner in __io_run_loop. The saved 06:15:50.968793 receipt has empty CQ/SQ, an outstanding timeout and no natural terminal accounting. The wrapper was stopped and the owner explicitly signalled for cleanup. Subsequent raw PASS/exit0 proves output/accounting only after manual assistance, not natural helper-stop correctness. Do not erase this failure or call the first attempt fully qualified.
5. The source-local repair records the actual uring_wait owner TID, release-stores stop_requested and forwards SIGTERM via same-process tgkill only from a different TID. It adds no steady request worker. The private traced and untraced candidate libraries were actually rebuilt; rebuild status is zero at 06:18:08.020211 UTC. The after-submit variant excludes the new TID/forwarding path.
6. The repaired protocol uses distinct qualification_repaired paths and adds standard strace -ttt timestamps for evidence. Lifecycle_repaired differs from the archived/source-native lifecycle only in the output-directory prefix. It does not alter its frozen oracle or timeouts. Both repaired protocol/lifecycle suites pass naturally before full observation.
7. Full begins 06:30:47.875567 UTC; terminal wrapper is 06:55:14.755647 UTC. All 30 executors, 60 cells and both analyses complete with zero exits. No full performance cell came from the pre-repair source; first preflight remains explicitly pre-repair setup evidence. There is one preflight and a recorded failed qualification followed by affected source repair/rerun, not an output-oracle widening or favorable-result retry.

## Correctness and lifecycle audit

The main matrix does not derive its reference tokens from its served replies. After native serving, the unchanged Python backend independently reconstructs graph inputs, slot mappings and KV/history state using upstream graphs, compares every independently produced token to the trace, then appends those independently produced tokens to reference history. Actual trace batch/admission scheduling conditions the replay; this is not independent scheduling or proof of canonical unpadded output. The raw client rows then match marker, prompt, gen, bad flag and exact token sequences against those references. Release checks independently enforce physical-slot ownership, FIFO release order, emitted-token count and eventual release. Tracing matches across conditions; it can alter scheduling and limits all numerical conclusions to these traced executions.

Repaired protocol, each model:

- 622 requests, 22224 output tokens, 259 rejected requests, 5000 empty connections, requested concurrency 1 through 8, actual model batch union 1 through 8.
- Fragmented HTTP/binary inputs, mixed generations, wrap/reuse, pipelining, rejection/reuse and half-close are retained. Independent graph/history replay and CPU re-analysis pass.
- Qwen has 7077 graph steps/14154 launch calls/125 release rounds; Smol has 7013/14026/141. Max release is 8. Model graph_error and trace_overflows are zero.
- Both accept/close 5086 connections, complete/head 622 and drain pending/error/reserved/drop/overflow to zero, with equal SQ and CQ endpoints. The bounded reply diagnostic records only 128 detailed replies: trace_count 622/trace_overflow 494 is expected diagnostic truncation, not the separate model-trace overflow (zero). Never report every overflow counter as zero.
- The all-thread post-ready strace contains no accept/recv/send network syscalls and exactly one io_uring_enter before stop. No SQPOLL thread is present. This is direct engagement evidence for this protocol, not a claim that no host/kernel CPU executes.

Repaired helper-signal timing from raw strace, including tracing overhead:

|Model|helper SIGTERM|owner io_uring EINTR|native cleanup write|
|---|---|---|---|
|Qwen|06:21:20.916441|06:21:20.922440|06:21:21.173040|
|Smol|06:26:38.083275|06:26:38.086319|06:26:38.104667|

The owner's subsequent signal has its own process PID as sender, consistent with the forwarding source. Owner wake is about 6.0/3.0 ms after helper delivery in these traced runs; this is not an untraced shutdown-latency performance result.

Each separate repaired lifecycle has 32 requests/actions: 22 valid, 10 rejections, two deliberately partial/reset/stop replies, and 652 checked client tokens. I independently decoded saved request/reply hex, checked markers/prompts/generation/header lengths and compared complete/partial token bytes to the unchanged frozen sets. Both have accepted=closed=13, head=completed=32, aborted=3, zero error/pending/reserved/drop/overflow, equal SQ endpoints and equal CQ endpoints, 32 reply-accounting rows, graph_error=0 and no remaining pins. Reset/stop checks validate the retained prefix and cleanup; they do not claim every post-stop byte is canonically validated or full generation was delivered.

The lifecycle source is byte-identical to archived0058 before only its output-path rename. Frozen complete/prefix sets are not expanded. Passing this finite sequential/partial check does not repair0058's unresolved ordinary untraced concurrent frozen-pool mismatch.

Full counts recompute to 1920 measured requests/62400 measured tokens plus 240 checked warmups; including warmups 2160 requests/62640 tokens. Each executor has 72 requests/2088 tokens and terminal success. All full client rows have exactly the expected length and independent reference equality, all model traces terminate without overflow, all loop accepted connections close and resources drain. Aggregate actual batches span 1 through 8. Native executes the same model computation through its separate current network constructor; every native executor also has a valid trace/reference/terminal path.

Compatibility scripts for HF, after-submit and coalesced constructors are prepared but have not been run at this review point. This review does not promote their existence, parsing or the main matrix into compatibility success. AMK remains outside demonstrated support.

## Baseline fairness and what it can establish

The fixed loop is a component ablation. It is useful for the primary causal question about changing idle heartbeat behavior and must not be called the external SOTA competitor.

Native uses actual nonblocking TCP plus epoll_pwait2; the original header and compile logs confirm it is not a Python request dispatcher or busy-spin null. It engages the intended current userspace constructor, uses the same FP16 graphs, prompts, token budgets, quiet gaps and tracing, and completes every cell correctly. There is no observed avoidable baseline execution failure or unfair model information budget invalidating the finite native comparison.

However, native also uses the fixed 60000 ns epoll timeout **while idle**. Its measured CPU cost therefore contains an analogous avoidable idle polling policy. An adaptive/event-driven native design is a credible alternative not measured here. Thus candidate-versus-native lower CPU supports comparison with this exact timed-epoll implementation only; it cannot establish that idle savings uniquely need eBPF or that the candidate beats the strongest possible native coordination policy. Describing native generically as an optimized event-driven lower-bound competitor would overstate the evidence. Current native remains a useful delivery boundary; no additional baseline is required to preserve the scoped component result.

## Metric and uncertainty audit

Each cell sends four waves of eight requests, with three sleeps of at least one second. All 60 cells contain the four wave markers, exact indices 0–31, matching wave membership, and descriptive aggregate host ticks before/after. Gen1/c1 sends eight sequential requests per wave; gen64/c8 sends one per lane with the existing barrier.

Process CPU sampling brackets first-wave connection/thread setup through final-wave connection close and includes all three quiet gaps. It uses the POSIX all-thread process clock described in [clock_getcpuclockid](https://man7.org/linux/man-pages/man3/clock_getcpuclockid.3.html); it does not account for all softirq/RX/io-wq/host kernel work or establish energy. Module-TX counters are zero because that module is absent. The duplicate known_worker metric is exactly the process metric here, not a second independent saving.

Wall TPS is total delivered tokens divided by first send to final token, including the three gaps but excluding initial connection setup. It is achieved delivery under this chosen pattern, not saturated server throughput. TTFT, completion and TPOT use raw per-token receive timestamps; multiple tokens in one recv share an arrival time. Metrics follow standard client definitions linked in the [vLLM serving benchmark](https://docs.vllm.ai/en/stable/cli/bench/serve/), while using token-ID rather than text/SSE wire.

Five process blocks are the pairing unit. The code takes the first five of six condition permutations and alternates cell order; it is not a full six-permutation balance or randomization. The fixed order is not a perfect drift control. All intervals are nominal paired t95 with df4 and the recorded critical value, without multiplicity correction. Do not turn crossing-zero intervals into noninferiority or equivalence, or use 160 client requests as 160 independent process replications.

### Primary gen64/c8 result

All CPU units below are milliseconds of executor-process CPU per delivered request, including the quiet gaps.

|Model|adaptive|fixed loop|current native|adaptive minus fixed, nominal t95|adaptive minus native, nominal t95|
|---|---:|---:|---:|---|---|
|Qwen|1.021333369|3.030955281|2.878810894|−2.009621913 [−2.485737506, −1.533506319]|−1.857477525 [−2.292574234, −1.422380816]|
|Smol|0.888568744|2.980229106|2.733718444|−2.091660363 [−2.467929096, −1.715391629]|−1.845149700 [−2.438931647, −1.251367753]|

Ratios of condition means give about 66.3% and 70.2% less process CPU than fixed. They are descriptive ratios, not separately inferred percentage-effect intervals. All five primary signed block differences are negative in both models.

Gen1/c1 also shows lower CPU: adaptive/fixed/native Qwen 0.684932238/2.675999081/1.992245006 ms/request, Smol 0.605760063/2.593642250/2.085607781. Adaptive-minus-fixed is −1.991066844 [−2.454677069, −1.527456618] ms Qwen and −1.987882187 [−2.247494316, −1.728270059] ms Smol. Both adaptive-native CPU intervals are below zero. Fixed-native short CPU is adverse in both models. Long fixed-native CPU remains inconclusive.

### Delivery and negative evidence

|Model, gen/c|adaptive / fixed / native wall TPS|adaptive minus fixed, nominal t95|adaptive minus native, nominal t95|
|---|---|---|---|
|Qwen 1/1|10.458428019 / 10.454713109 / 10.472183238|+0.003714910 [−0.016385302, +0.023815122]|−0.013755219 [−0.052715460, +0.025205023]|
|Smol 1/1|10.469292458 / 10.476420566 / 10.486593079|−0.007128108 [−0.036816140, +0.022559925]|−0.017300621 [−0.053765774, +0.019164533]|
|Qwen 64/8|603.031063598 / 599.922170792 / 604.134198585|+3.108892806 [−0.104133311, +6.321918924]|−1.103134986 [−5.249688006, +3.043418033]|
|Smol 64/8|614.487674070 / 616.493500539 / 616.618516321|**−2.005826469 [−3.049774738, −0.961878201]**|−2.130842250 [−7.832161529, +3.570477029]|

The adverse Smol adaptive-fixed effect is approximately −0.325% of the fixed condition mean. All five signed differences are negative: −1.385245233, −1.462778688, −2.408882857, −3.306937093 and −1.465288476 token/s. It must remain visible despite its small magnitude and despite the primary CPU saving. This is a finite wall-pattern delivery effect; wave setup and fixed gaps are part of that metric. It is not proof of a 0.325% saturation-capacity loss or a uniquely identified kernel cause.

Qwen long completion improves versus fixed: −3.431751644 [−5.901725494, −0.961777793] ms, and TPOT −0.052596452 [−0.088580879, −0.016612026] ms. Its wall-TPS interval still crosses zero and must not be rounded into a throughput win. Smol long completion/TPOT are inconclusive. Every adaptive-native delivery interval crosses zero in both cells/models. All TTFT mean-effect intervals cross zero. Thus neither CPU saving nor absence of a significant TTFT difference proves latency equivalence or no penalty.

Short TTFT means adaptive/fixed/native: Qwen 1.538648175/1.630396169/1.505791513 ms, Smol 1.441838000/1.392865044/1.316085019. Long TTFT: Qwen 2.595954906/2.714130069/2.623918306 ms, Smol 2.349833081/2.580222975/2.188036963. The full appendix retains all p50/p99, completion, TPOT, CPU duplicate/zero rows and every contrast rather than selecting favorable metrics.

Outliers are retained: maximum measured TTFT Qwen adaptive 5.042805 ms (block1 short wave3 index24), fixed 8.111736 (block1 long wave2 index17), native 10.957796 (block1 long wave1 index11); Smol adaptive 8.893687 (block0 long wave2 index21), fixed 11.125984 (block3 short wave1 index11), native 7.195306 (block1 long wave3 index25). There is no post-hoc trimming. The predeclared first-by-client-start wave subset is recomputed descriptively in the appendix, without replacing the primary or fabricating a new inference.

## Host and preservation limits

At review, host_before.json is 05:57:59.101863 UTC with no compute application. host_full_early.json at 06:31:29.517814 maps host PID2600132 to container PID515761, the Qwen block0 adaptive executor started06:30:54 and ready06:31:31. host_full_smol.json at06:53:49.663522 maps host2715450 to container523071, the Smol block4 adaptive executor started06:53:36 and ready06:54:12. **Both during-full samples are bootstrap, before readiness**, not verified serving samples.

All three receipts identify the original Pod/container, same boot04dc0087-5ccc-4c46-9997-b9a92f0e5167, existing400W limit/default575W, and the same56 selected historical warning lines. They do not prove continuous GPU isolation, warning harmlessness, absence of all faults or unrelated CPU activity. Whole-host cell counters mix client/kernel/other work and remain descriptive. The subsequently saved host_after.json is actually timestamped07:04:12.724552 UTC, 537.968905 seconds (about8m58s) after the full wrapper terminal. I inspected it: no GPU compute application, identical boot,400W limit and exactly equal56-line selected historical warning array. This late sample is honest after-state evidence, not immediate or continuous isolation proof.

All eight retained build/setup paths match their pre-experiment inode, size, mtime and symlink records at review. Base packages remain Torch2.14.1+cu130/Transformers5.19.0/NumPy2.5.3. Coder PIDs1/10909 retain starttimes. No bpfusion bpffs pins remain. These are current preservation observations, not proof of final cleanup or public publication. During finalization, the owner recorded source-selection.json at07:05:41.765484 UTC selecting original behavior and preserving the candidate only as experimental evidence. I independently verified all three production paths are now byte-identical to HEAD and production-original; production-patch contains separate true HEAD-to-candidate diffs, while the earlier adapter-noise diffs remain preserved. Git status then contains only the owner's documentation work and unowned tools/setup_env.sh. Compatibility adapters remain unexecuted and are unnecessary for selecting an unretained patch; they provide no compatibility claim. Runtime/private build cleanup, final retained archive (planned bench/results/adaptive_wait_20261015/), honest docs and main commit/push remain the owner's closure actions. This reviewer did not perform them.

## Scientific interpretation

The largest defensible new evidence is that this idle-aware before-submit mechanism can substantially reduce partial process coordination cost in finite bursty traced serving. The actual helper-stop failure shows that removing idle heartbeat wakeups requires explicit owner wakeup. Smol's adverse fixed-pattern wall TPS prevents a blanket no-delivery-regression claim. Native's own fixed idle polling prevents attributing the CPU advantage to eBPF as a necessary mechanism.

Do not turn these results into a new model-kernel contribution, a generic low-latency service result, ordinary untraced equivalence, arbitrary-model support or a direct thesis challenge. No new GPU experiment is needed to establish the reported arithmetic or failure history. The supported CPU component and contrary delivery boundary should be returned together to the orchestrator without weakening the user goal.
