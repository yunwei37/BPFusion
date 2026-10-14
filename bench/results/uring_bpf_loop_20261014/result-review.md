# Independent result review: sleepable eBPF/io_uring loop

Reviewed 2026-10-14 after terminal collection by fresh reviewer /root/uring_bpf_loop_result_review under research-experiment-design. Analysis ran only in the retained yunwei356/bpfusion-dev Workspace, /workspaces/repository, main. No serving rerun, source edit, oracle change, infrastructure change or publication was performed by this reviewer.

## Separate judgments

- **Run status: valid and complete within the declared finite protocol.** Both performance source-native analysis replays exit0 and match archived stdout byte for byte. All four traced/ordinary strict analyses also replay exit0 and match archived stdout byte for byte. No defect found invalidating the matched main comparison or component control.
- **Tested hypothesis: CPU replacement benefit supported; delivery mixed.** Loop reduces known-worker CPU against SQPOLL for both models. Neither gen1/c1 TTFT primary establishes improvement against native. Qwen gen64/c8 throughput contradicts improvement; Smol throughput is inconclusive. CPU benefit is not a latency/TPS win.
- **Research value: supporting.** This coordination intervention resolves the measured SQPOLL worker-cost uncertainty that prior copy-only evidence could not. Qualification is dependency evidence, not an independent scientific contribution.
- **Paper impact: mechanism/workload boundary and additional local evidence.** The plan introduces no formal paper RQ. This is not a direct thesis challenge or arbitrary-model/SOTA result.
- **Next paper decision:** close this completed comparison and publish all six primary intervals and the negative delivery result. Retain the loop as an optional qualified transport. Do not claim loop superiority over native, equivalence, total CPU savings or universal model support. Further work needs a distinct causal discriminator or the unresolved deployment question, not repetition until favorable.

## Contract and source reviewed

The selected local question is retained verbatim:

> what client latency/throughput does the ordinary packed/prefix adapter deliver against the efficient native network alternative after BF_TRACE is removed?

The integrated hypothesis replaces SQPOLL coordination with an upstream sleepable eBPF/io_uring loop, testing known-worker CPU for long eight-client output and resulting delivery against efficient native TCP. Candidate uring_loop is compared with native userspace as the main competing mechanism and incremental SQPOLL uring as a component control. It is not an official-vLLM-server comparison.

I read the archived plan and plan review, qualification history, source/runtime receipts, source-native bench and analyzer, resident_dispatch CPU reader, Makefile build conditions, vllm_graph Python/CUDA integration, io_uring_tcp transport, uring_loop BPF callback, finding0044 and relevant evaluation context. I subsequently inspected the root's proposed completed-results append to finding0044. All its numerical means, six primary intervals, percentage statements and scoped interpretation agree with independently reconstructed evidence. Its pending independent-review/restoration wording is honest at the time of that append; evaluation and README still require synchronization.

DEFER_TASKRUN, single-issuer execution, task-work scheduling, timer CQ traffic and BPF loop change together. This experiment measures the complete coordination replacement, not exclusively eBPF, syscall elimination or polling overhead. Upstream BPF operations require DEFER_TASKRUN and reject SQPOLL/IOPOLL; the implemented submit/wait callback matches that mechanism. See [upstream BPF operations](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c) and [kernel loop](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c).

## Completion, frozen source and deviations

Authoritative timing source remains ddc444c393a38be2ffbabf372d22e139e4aa4bc3 on main during review. source_frozen.json records publication03:08:12.757809UTC and only the pre-existing untracked tools/setup_env.sh before timing. Raw metadata for both models identifies that commit, FP16 and Torch2.13.0+cu129. Captured driver, client, backend Python and native CUDA source exactly match current files. Common pinned runtime is vLLM0.31.0, Torch2.13+cu129, Transformers5.17; all three conditions share the temporary libbpf1.6.3 library path and VLLM_ENABLE_V1_MULTIPROCESSING=0.

Model snapshot revisions are Qwen2.5-0.5B-Instruct 7ae557604adf67be50417f59c2c2f167def9a775 and SmolLM2-135M 93efa2f097d58c2a74874c7e644dbc9b0cee75a2. Exact executable/model/reference/output bindings are in performance_status.json and performance_pipeline.py. They run the source-native --loop-comparison --untraced --reference-path command, Qwen then Smol, without model overlap. Both execution/analysis exits are0. Start/end bracket is03:08:41.811725–03:27:43.905073UTC; raw terminal events are Qwen03:18:17 and Smol03:27:08.

Independent raw inspection reconstructs36 distinct normal executors,18/model; all six permutations of(loop,native,stock) exactly once/model; all four planned cell rotations;144 cells with64 measured requests each;9216 measured requests and299520 measured tokens. All measured cell indices0..63 occur exactly once. Each executor has256 measured and8 checked excluded warmups, totaling288 excluded warmup requests/tokens. There are no failed, replaced, skipped, retried or outlier-excluded timing cells. Negative effects and extreme observations remain.

Pre-performance repairs are preserved. First preflight fails before requests because old libbpf lacks struct_ops shadow initialization data; common temporary upstream libbpf1.6.3 corrects it. Second delivers40 loop replies but cannot retire its multishot timer; explicit TIMEOUT_REMOVE repairs ownership. Third/final admitted preflight completes120 requests/3144 checked tokens. Separately balancing SQ and CQ is necessary for multishot semantics and does not relax wire/oracle/pending/error/lifecycle checks. Initial HF launcher mapping selects the default library; the archived failed wrapper remains. After adding the omitted loop name, the identical affected HF workload succeeds. None of these failures is counted as a performance win; all precede frozen timing.

## Correctness and actual mechanism engagement

All12 strict vLLM executors cover7464 requests,266688 valid tokens,3108 intended rejects and60000 empty connections. All four strict analyzer replays exit0 and exactly reproduce archived stdout. Traced protocols reconstruct actual upstream batch/KV history, with batches1..8, fragmentation, prompt/block boundaries, reuse/wrap, mixed pacing, pipeline/half-close, rejection, subsequent valid traffic and helper-thread SIGTERM. Ordinary qualification retains the frozen complete-output-set contract.

Independent after-ready, before-first-SIGTERM inspection of all12 network logs shows:
- Loop: exactly one io_uring_enter entry per trace, no userspace accept4/recvfrom/sendmsg.
- SQPOLL: zero steady entries and no such socket calls.
- Native: actual accept4,recvfrom,sendmsg in every trace, engaging intended native networking. Each trace includes5147–5154 accepts and tens of thousands of receive/send calls.

Every timed stock task list has exactly one iou-sqp task; every loop/native task list has zero. Qualification traces establish mechanisms, while ordinary timing is untraced; it must not be described as having timed per-request syscall tracing. Its selected binaries, source captures, worker identities and counters support the same mechanism.

Corrected HF idle/lifecycle tests pass32 requests/652 independently checked complete or prefix tokens per model,13 accepted/closed sockets and3 expected aborts. HF traces/audit show one steady loop entry and separate cleanup entry, no steady userspace socket calls, and SINGLE_ISSUER|DEFER_TASKRUN without SQPOLL. This supports reuse by a second computation adapter, not arbitrary models.

The frozen numerical asset is byte-identical to0043's asset and predates this run: Qwen17 prompt/gen keys22 whole sequences; Smol17/19. Every timed valid complete reply matches one exact qualified sequence. References originate in prior independent upstream trajectory replay rather than current candidate output; no tolerance, tokenwise union, post-observation expansion or missing-reply retry is used.

This finite pre-observation contract is weaker than current ordinary trajectory replay. Actual ordinary batching/KV histories are unobserved. Indexed gen64/c8 whole-output equality loop/native is351/384 Qwen and346/384 Smol; loop/stock is342/384 for each. These differences do not fail the predeclared contract but rule out identical concurrent-output trajectory claims. No task-quality or universal correctness claim follows.

Compiled loop/stock model-dispatch SASS is byte-identical at428852 characters each. Native shares the same packed-prefill/FIFO-prefix algorithms, checkpoint/KV/head/greedy capture adapter and upstream model computation through Makefile/source. Transport and host lifecycle differ. Reused arithmetic does not imply identical timing-dependent batch histories or GPU utilization.

Timed counters balance264 completed/head requests per executor, accepted/closed connections, pending/error/reservations/drops/overflow0 and final FREE request slots. Loop SQ and CQ each drain separately; stock single-shot totals remain all equal. trace_overflow136 deliberately records the first128 network diagnostic capacity for264 requests; it is distinct from zero model-trace/CQ overflow. Candidate and stock retain these measured diagnostic/counter costs with BF_TRACE model tracing off.

## Independent recomputation and all six primaries

I independently derive TTFT from(first arrival−start)/1e6, each TPS from64*gen/(last arrival−first start), and CPU/request from(after−before process clock)/64. All requests/cells are present. Six paired process blocks, not pooled requests, form uncertainty units. Nominal two-sided t95 uses df5, critical2.570581835636305/sqrt6. Direct arithmetic reproduces all six means and endpoints, separately from the source-native analyzer replay.

Positive favors loop. CPU below is converted to ms/request.

|Model|Primary effect|Estimate|Nominal paired95% interval|Judgment|
|---|---|---:|---|---|
|Qwen|native−loop TTFT gen1/c1 ms|−0.009686133|[−0.071448451,+0.052076186]|inconclusive|
|Smol|native−loop TTFT gen1/c1 ms|+0.032660357|[−0.042744825,+0.108065539]|inconclusive|
|Qwen|loop−native TPS gen64/c8|−75.848884|[−119.599452,−32.098316]|gain contradicted|
|Smol|loop−native TPS gen64/c8|+21.356192|[−108.669300,+151.381683]|inconclusive|
|Qwen|stock−loop CPU gen64/c8 ms/request|+13.649411245|[+13.218862765,+14.079959725]|CPU benefit supported|
|Smol|stock−loop CPU gen64/c8 ms/request|+11.580469063|[+11.071859003,+12.089079122]|CPU benefit supported|

Qwen TPS block differences are all negative:−51.759237,−51.016944,−29.466833,−136.802822,−70.258019,−115.789450. Smol differences are mixed:−37.054603,−62.155145,+152.234644,+206.033790,−70.993542,−59.927994. Two favorable Smol blocks cannot establish superiority over its four negative blocks. Largest TTFT block effects Qwen−0.118767ms and Smol+0.149533ms remain included. No outlier removal is found.

These are six nominal intervals without familywide correction/superiority. Crossing zero proves neither equivalence nor absence of an effect. CPU support cannot serve as a composite performance win.

|Model|Condition|gen1/c1 TTFT ms|gen64/c8 TPS|gen64/c8 CPU ms/request|
|---|---|---:|---:|---:|
|Qwen|loop|1.378481|4605.364822|0.572526|
|Qwen|native|1.368795|4681.213707|0.491585|
|Qwen|stock|1.337637|4536.448200|14.221937|
|Smol|loop|1.104221|5471.373930|0.482410|
|Smol|native|1.136882|5450.017739|0.426647|
|Smol|stock|1.111258|5348.630357|12.062879|

TPS means average six cell rates, not one ratio pooling unrelated startups. Qwen loss is approximately1.62% of native TPS. Loop CPU means are about96% below stock. These descriptive percentages match the proposed finding.

## CPU boundaries and negative secondary evidence

The source reader obtains CLOCK_PROCESS_CPUTIME_ID for the actual executor PID, counting all process threads once, including the actual SQPOLL task and creator's kernel CPU. Separate bfusion_tx CPU is0 in all conditions. This agrees with the [process clock definition](https://man7.org/linux/man-pages/man3/clock_gettime.3.html). It excludes RX/softirq/BPF/TCP work elsewhere, client CPU and energy; it is not total service CPU or exclusive component attribution.

Gen64/c8 mean process-CPU/client-wall core fractions are Qwen loop/native/stock0.041201/0.035942/1.007356 and Smol0.041233/0.036284/1.006784. Stock-to-loop CPU/request ratios are about24.84/25.01. These are secondary descriptive boundaries, not whole-host savings.

Native is lower CPU than loop in both long eight-client cells. Secondary native-minus-loop CPU effects:
Qwen−0.080940529ms/request[−0.102990926,−0.058890131];
Smol−0.055763674[−0.079094642,−0.032432707].
Removing stock's poller therefore does not beat native's measured known-worker CPU.

Other negative secondary effects remain in archived analysis: both models' gen64/c1 throughput loses to native, and both models' gen1/c8 TTFT/TPS also lose on their nominal secondary intervals. Positive TTFT64/c1 effects cannot replace inconclusive TTFT1/c1 primaries. Stock-vs-loop delivery is a component contrast, not the headline baseline.

CPU clock brackets strictly surround measured cells; extra before/after padding spans0.307–1.413ms across conditions. Small setup/drain/read-bracket costs remain in clock differences, especially relevant to short gen1 secondary CPU. There is no empty-work subtraction or per-operation causal accounting.

## Limits, competing explanations and environmental evidence

Scope is one RTX5090/Linux7.3rc3, four short tokenized prompts, gen1/64, one/eight closed-loop clients and bounded protocol/KV. It is not broad production serving, official vLLM server comparison or cross-node latency. GPU transport-controller execution, timer/CQ traffic, task-work/submission scheduling and arrival-dependent batching may affect delivery. This run cannot choose an exclusive cause of Qwen loss. Nominal60us timer and native timed-epoll matching does not establish identical actual wake spacing or an optimal tuning value.

No continuous host isolation is proven. Start receipt shows loadavg13.11 and no GPU application at one observed moment. Same boot and no own module/pins/GPU app at03:27:43 endpoint do not rule out CPU interference. Actual timing-bracket kernel journal returns0 with '-- No entries --'; this is an empty receipt, not positive proof of no fault/interference. Paired all-order blocks mitigate order bias without quantifying arbitrary load. No source-specific failed baseline or unfair mechanism engagement is observed that invalidates this admitted local result.

## Paper decision and required follow-through

Publish completed raw evidence, this one result review and all six primaries. Update pending performance statements in evaluation/README/finding while preserving failures, fixed references, negative intervals and CPU/numerical scope. Root's proposed completed finding append is numerically and interpretively supported. Temporary runtime/build cleanup and final restoration remain the orchestrator's work; this reviewer did not remove apparatus.

The supported story is an optional upstream coordination mechanism that removes approximately one continuously active stock worker core within this finite workload, preserving GPU-owned networking without a steady userspace request worker or custom TX module on this host. Its performance story is a CPU tradeoff, not delivery superiority over efficient native. The consistently negative Qwen TPS is a real boundary.

Close unchanged timing. Any next experiment should discriminate a new cause or address the unresolved matched cross-node deployment question. Existing timer/queue counters may inform a causal prediction before an intervention; a favorable setting sweep cannot retroactively change this result. Backend integration evidence should stay separate from performance claims. This review does not itself authorize or require a redesign/model-specific arithmetic campaign.

## Evidence and reproduction

All reviewed experiment artifacts are in bench/results/uring_bpf_loop_20261014:
plan.md, plan-review.md, qualification.md, failed preflight/HF records,
hf_loop/pipeline.status.json, hf_network_audit.json, source_frozen.json,
runtime_environment.json, resolved_packages.json, libbpf_dependency.json,
model_dispatch_sass_identity_final.json, performance_status.json,
performance_pipeline.py, both performance raw JSONL and analysis outputs,
all executor outputs, frozen_references.json, performance_start/end.json and
performance_kernel_journal.json.

From /workspaces/repository, I executed:
    /usr/bin/python3 bench/vllm_serving_analysis.py bench/results/uring_bpf_loop_20261014/qwen_performance.jsonl
    /usr/bin/python3 bench/vllm_serving_analysis.py bench/results/uring_bpf_loop_20261014/smol_performance.jsonl
and both models' *_traced_correctness.jsonl and *_correctness.jsonl.
All six replay commands exit0, reproduce archived stdout byte for byte and have empty stderr. Additional direct raw arithmetic reconstructs all six primaries, request indices/permutations, CPU worker identity and brackets, frozen-reference identity and after-ready network trace engagement. No new model serving was run.
