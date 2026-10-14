# Independent result review: current reused-graph GPU I/O arrangements

Reviewer: fresh `/root/current_io_placement_result_review`. Reviewed UTC: 2026-10-14T20:46:06.999057+00:00. No desired verdict was supplied. This review followed the RESULT REVIEW requirements of `C:/Users/10678/.codex/skills/research-experiment-design/SKILL.md`. The reviewer performed read-only source/artifact inspection and independent standard-library CPU calculations in the original `yunwei356/bpfusion-dev` Workspace. No GPU run, build, install, source edit, cleanup, service change or Git publication was performed. The only written artifact is this report.

## Separate judgments

- **Run status: valid** for the predeclared finite, shared-host constructor comparison. The full matrix and integrated candidate qualification reached terminal status; no missing or selectively dropped measured cell was found.
- **Tested hypothesis: inconclusive overall**, with **supported Smol gen64/c8 recovery** and **inconclusive Qwen gen64/c8 recovery** against the coalesced component control. Do not turn the positive Smol row into a both-model result. Smol superiority over efficient userspace is contradicted locally; Qwen superiority over userspace is inconclusive.
- **Research value: supporting.** This resolves a current-constructor engineering choice for Smol and establishes a Qwen latency/uncertainty boundary. Setup, protocol and lifecycle checks are dependencies integrated into that result, not separate contributions.
- **Paper impact: mechanism or workload boundary**, adding finite evidence toward the retained question; no direct thesis challenge. No formal paper RQ or central-thesis contract exists here, and this review does not create one.
- **Next paper decision:** retain the existing standalone entry as the supported faster current route for Smol gen64/c8 under this runtime, while reporting its remaining native gap. Do not claim a universal default win or promote Qwen based on its positive mean. Preserve coalesced's Qwen short-output advantage. Close this unchanged comparison, record the mixed boundary, and route any next work to a distinct decision-relevant discriminator rather than another unchanged timing run. This review authorizes no implementation or runtime mutation.

## Question, evidence and execution

The retained user question is delivered latency/TPS for Linux TCP/HTTP + eBPF/sockmap -> kernel/GPU shared queue -> resident real-model GPU -> asynchronous kernel TCP replies without a steady userspace request worker, reusing upstream model arithmetic. The tested uncertainty is narrower: whether current `vllm_graph_uring_loop` recovers gen64/c8 throughput relative to current `vllm_graph_uring_loop_coalesced`, and its boundary against efficient native `vllm_graph_user_network_wait`.

I read `plan.md` and `plan-review.md` in full, all expanded `full.commands.json` commands, setup/run/short/transfer/qualification/lifecycle recipes, fixed analyses, all twenty full raw JSONLs, all sixty ordinary executor stdout files, driver stdout/stderr and exits, both protocol traces/GPU histories/reference files, both lifecycle directories and analyses, source snapshots and actual current source, frozen pools, package/build receipts and host observations. The ordinary driver embeds source/config/client/precision/model metadata; its actual sources match the captured files. Current main remains `048c204ed78e006f1e31cfa8a7fb4699b7429d06`; all twelve captured files are byte-equal to current source. Eight original protected paths remain equal to `preserved_before.json` in inode/size/mtime/symlink metadata. The untracked `tools/setup_env.sh` is untouched. Metadata equality is the preserved-path evidence; it is not a newly introduced hash acceptance gate.

The full run ends at `2026-10-14T19:14:43.986672+00:00` with exit0. All twenty declared drivers and sixty executors exit0. The integrated matrix contains120 measured cells,3840 measured requests and124800 measured output tokens. Eight checked gen1 warmups per executor contribute480 excluded warmup requests/tokens:4320 complete ordinary replies and125280 total ordinary tokens. The only ordinary exclusions are these predeclared warmups; no failing or adverse measured block was removed. Preflight1 completes4 drivers/12 executors/24 cells,192 measured requests/6240 tokens plus96 warmups. Setup, qualification, lifecycle, full and their fixed analyses all have terminal0 receipts. The delayed fixed full/long analyses complete at20:35:10 UTC; this does not change the earlier collection termination.

Commands use private runtime/build paths under this TEMP and the source-native Make targets. Ordinary three-path order uses five of six permutations; odd blocks reverse context/model/cell order. I checked actual starts/cell ordering against those rules. Private BUILD, adjacent-library resolution and selection of standalone for candidate qualification are declared recipe adaptations, not post-result source/metric/oracle changes. Qualification adds frozen membership alongside traced replay. No changed correctness threshold, timeout, model arithmetic, output pool or analysis criterion was found during collection. The coalesced-only stdout-marker requirement is absent for standalone exactly as admitted in the plan review; source/build branch selection plus actual execution establish the arrangement instead.

## Independent metric recomputation

I independently rebuilt each cell from raw client timestamps/tokens, rather than calling the producer analyzer or treating its summary as the result. For32 measured requests, output TPS = total received output tokens / (last token arrival - first request-send time). TTFT = first token arrival - request send. Completion = last token arrival - request send. For gen64, per-request TPOT = (last arrival - first arrival)/63, then mean across requests. I checked request index coverage, ordered arrival arrays, exact token counts, frozen whole-output membership, CPU sample bracketing and CPU-counter differences. All120 cell values, all24 process-block means, all72 signed paired effects and their t95 intervals match `full.analysis.json` to floating-point rounding (independently evaluated division order can differ in the last binary digit). `full.analysis.stdout` contains exactly the same completed report.

The inference unit is a paired process block, n=5. Each signed effect is standalone minus control; uncertainty is mean ±2.776445105 × sample SD / sqrt(5), df4. It is nominal paired t95, not familywise protection, a robust small-sample guarantee, equivalence or non-inferiority.32 requests per cell are not32 independent process replications. The official [vLLM metric documentation](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics), checked during this review, defines client TTFT and per-request TPOT consistently with these formulas. This custom token-ID finite client window remains different from a full official vLLM/OpenAI server benchmark. TCP chunk arrivals may assign identical times to several tokens; do not substitute ITL or device-token timing claims.

## Primary result and interpretation

| Model | Standalone TPS | Coalesced TPS | Native TPS | Standalone - coalesced, nominal t95 | Standalone - native, nominal t95 |
|---|---:|---:|---:|---:|---:|
| Smol |5566.111767|5175.049052|5619.007572|+391.062716 [102.619263,679.506168]|-52.895805 [-90.472152,-15.319458]|
| Qwen |4688.844650|4613.723184|4810.983074|+75.121467 [-144.333957,294.576890]|-122.138423 [-370.862461,126.585614]|

All figures are gen64/c8 client output token/s, averaged over five paired process blocks. Smol standalone is7.557% higher than coalesced's mean and0.941% lower than native's mean (descriptive ratio of means, not a separate inference). Its candidate-control TPS effect is positive in every block:633.096882,246.098746,229.210818,191.105722,655.801410. Its candidate-native effect is negative in every block:-56.469343,-16.080202,-77.292420,-28.501029,-86.136029. This supports a useful current Smol route selection while explicitly retaining the native gap.

Qwen is1.628% above coalesced's mean and2.539% below native's mean, but both primary intervals cross0. Against coalesced its blocks are104.210971,244.863030,156.007717,92.791351,-222.265736; the adverse fifth block remains in the result. Against native they are-113.090907,88.783680,-48.919923,-84.892925,-452.572043. Neither a generic Qwen improvement nor equivalence with native is established. Do not pool models or replace this uncertain primary result with favorable c1 latency.

The throughput/latency tradeoff is real. At gen1/c8 Qwen standalone TTFT is2.765961ms versus coalesced2.591148ms: +0.174813ms [0.015763,0.333864], adverse in all five blocks. Qwen gen1/c8 TPS against native is-146.719072 [-285.002636,-8.435509]. Smol gen1/c8 TTFT versus coalesced is+0.041449ms [-0.184346,0.267244], inconclusive. At gen64/c8 standalone known-worker CPU is higher than native for both models: Smol+45.240269us/request [29.876490,60.604048]; Qwen+111.798269us/request [77.037076,146.559461]. Qwen CPU versus coalesced is also adverse +46.124588us/request [14.166118,78.083057]. No claim of total host CPU elimination, energy savings or latency/throughput improvement at every cell survives these rows.

## Main baseline engagement and fairness

Native is the only main competing baseline; coalesced is a component control. Native represents ordinary efficient userspace request/reply processing, not a definitionally losing null control. The current `userspace_tcp.h` uses nonblocking accept/recv/sendmsg, vectored header+tokens, default server TCP buffering and `epoll_pwait2` with the existing nominal60000ns completion wait. Every ordinary native executor prints the timed-wait marker and reports the expected published/completed count (40 for short,104 for transfer), zero rejection,9 or11 accepted connections respectively. No native executor fails or misses the intended path. Actual Make/compiler receipts select `BF_USER_NETWORK`/`BF_USER_NETWORK_WAIT`; native has no GPU networking CTA or BPF-loop flags.

All three constructors load the same exact cached Smol revision93efa2f097d58c2a74874c7e644dbc9b0cee75a2 and Qwen revision7ae557604adf67be50417f59c2c2f167def9a775, use FP16 weights/KV and the same vLLM graph/bootstrap/dispatcher arithmetic, padded prefill, FIFO prefix release, eight slots, four prompts, output budgets/warmups, client parser and timing formulas. Fresh private libraries share vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0, NumPy2.3.5, libbpf1.6.3 and sm_120 compiler settings. No condition-specific numerical information or model budget advantage was found. Compiled instructions and complete serving GPU work are not identical; intended transport flags/resources differ. This is a fair matched local mechanism comparison, not proof of SOTA full-server superiority or every available CPU algorithm's optimum. Ordinary paths are untraced, so their CPU syscall engagement is source/build/stdout/accounting evidence rather than a separately collected ordinary syscall profile.

## Mechanism and counter audit

Source establishes standalone `io_network` running independently on a nonblocking CUDA stream with allocated durable `IoState`; model dispatch remains in its normal stream/graph. Coalesced calls `io_progress` in dispatch, batches CQ/SQ publication and delays idle admission until final replies and published SQ work drain; its network worker is shutdown-only. Therefore the intervention changes the whole constructor bundle: residency, state progression/access, publication frequency, admission and timing together. Neither the throughput effect nor source inspection isolates exclusive overlap, CTA occupancy, PCIe cost or GPU-time causation. Dynamic overlap was not profiled.

I independently parsed terminal model counters and subtracted8 serial warmup rounds for short contexts and2088 for transfer (8 warmups+32 serial gen1+32 serial gen64). Serial client start/last-arrival order is nonoverlapping, authenticating the subtraction. I recomputed all short rows/effects and all long rows, summaries, paired round effects and CQ-derived fields; they match the fixed outputs. Short c8 rounds: standalone8,8,8,8,9 for both models; coalesced Smol6,6,5,5,7 and Qwen6,6,6,5,6; native Smol8,8,8,9,8 and Qwen8,8,8,8,8. Standalone-minus-coalesced mean is+2.4 [1.719913,3.080087] rounds for each model.

Long c8 rounds: Smol standalone269,267,268,263,265, coalesced259,259,261,259,259, native261,260,261,261,261. Qwen standalone270,265,266,267,267, coalesced260,259,259,259,259, native260,262,260,260,261. Standalone-minus-coalesced round effects Smol+7 [4.223555,9.776445], Qwen+7.8 [5.958315,9.641685]; standalone-minus-native Smol+5.6 [2.483448,8.716552], Qwen+6.4 [3.283448,9.516552]. Smol's throughput improves despite more model rounds, refuting a fewer-round explanation for that gain, but not identifying which constructor difference causes it. Ordinary per-request batch/KV trajectories remain unobserved. Whole-transfer CQ-SQ excess includes multishot timeout traffic across all transfer cells; it is descriptive, not gen64/c8 exclusive cost, GPU time or causal mediation.

## Correctness, oracle independence and protocol

I reconstructed the frozen pools from their recorded prior reference files plus the admitted uring qualification sources. They match exactly:17 prompt/gen entries,19 complete sequences for Smol and22 for Qwen. Their timestamps predate this measurement, and all4320 ordinary outputs pass whole-sequence membership. The current candidate never expanded the oracle pool from its own observed output. Membership may accept more than one prior trajectory's complete sequence and does not identify current ordinary batch histories. This proves the declared finite output contract, not fresh eager-HF arithmetic equality, arbitrary prompts/model quality or independently reimplemented math.

For each model I independently matched all622 protocol client requests to actual admissions by timestamp, prompt, generation length and rejection; rebuilt compute-token histories; checked physical-slot ownership and FIFO release; and compared all complete client/reference/trace tokens. Both suites deliver22224 tokens,259 rejections,5000 empty connections and real compute batch sizes1..8. Cases include30 fragmented requests, concurrency1..8,256 wrap rejections+256 wrap accepts,32 mixed requests,6 pipeline/half-close,4 pipeline/rejection,1 invalid binary and1 post-rejection binary accept. Smol actual compute rounds7016 (202 prefill,6814 decode), Qwen6962 (203,6759); both contain5374 real prompt tokens. Padding counts3327/4052 and release rounds131/142 (max prefix8) independently match the reported analysis. The adapter replays actual batch/history/physical KV page inputs using the same reused graphs and checks tokens, an independent trajectory reconstruction but not an external eager arithmetic oracle.

Both actual protocol network transcripts show two bootstrap `io_uring_enter` calls before readiness, one unfinished steady `io_uring_enter(...,0,0,0,NULL,0)` spanning service, a SIGTERM delivered to a helper thread, and a later drain enter plus cleanup. After the `resident vLLM ready` marker there are no accept/recv/send-family host calls. I inspected the actual syscall lines, not only `network_verified`. GPU source plus current Make flags, successful model work, the BPF struct_ops ring loop and transcript support the finite no-steady-userspace-request-worker claim. Task snapshots contain no `iou-sqp` worker for loop targets. This does not mean zero host or kernel CPU.

Protocol terminal rings accept/close5086 connections each, complete/head622, abort1 (the intended invalid binary closure), pending/error/reserved/drop/overflow0 and separately drained SQ/CQ: Smol38171/203551, Qwen38207/241088. `trace_count=622,trace_overflow=494` is the fixed128-entry IoRecord reply diagnostic truncation, retained honestly; it is separate from the full GPU event trace's zero overflow and all622 client/reference histories. It is not permission to discard failing correctness events. Ordinary/lifecycle reply counts are within128 and report no such truncation.

The stronger older AMK fresh eager-HF equality remains **failed**. Current `docs/evaluation.md` and its retained finding0048 record that original upstream per-step/persistent controls reproduce the divergent sequence. This experiment does not run AMK or replace that oracle. Neither successful current vLLM pool membership nor traced reused-graph replay repairs the older AMK failure. Opposite AMK arrangement results remain a historical scope boundary rather than numbers merged into this vLLM dataset.

## Independent lifecycle wire and shutdown audit

For each model I decoded all32 `request_hex`/`reply_hex` records, independently of `exact=true`. HTTP request headers and Content-Length agree with actual binary payload lengths. The payload unpacks as little-endian magic0x514c4d51, n_prompt, n_gen, pad0, timestamp and token IDs; every field matches the associated row. HTTP success status200 and content length4×gen, rejection status400/content length0, binary invalid EOF, complete token counts and one-token RST/SIGTERM prefixes are all correct. Every decoded complete/prefix token sequence matches the corresponding frozen prompt/gen pool. No post-stop extra bytes are recorded for either model. I cross-matched all32 ring REPLY sequence/timestamp/gen records with the raw client requests, preserving aborts at seq27(binary reject),29(RST),31(SIGTERM).

Each lifecycle consists of19 complete successful HTTP replies,9 HTTP rejections,1 invalid binary EOF,1 successful binary reply,1 binary RST prefix and1 HTTP SIGTERM prefix; it checks652 complete-or-prefix tokens over13 actual client peers. The nine long idle/reconnect cycles and half-closes are retained in the driver/source and bytes. Full long-generation completion is not claimed for either intentionally interrupted action. Independent stdout/BPF parsing finds accepted=closed13, head=completed32, aborted3; pending/error/reserved/drop/overflow0; recycle32, llm_head32, reservation bitmap0 and all eight physical slots FREE. Model launch count654, admitted32/retired31 is intentional:31 retired model requests plus the shutdown-aborted admitted request, not32 completed model generations. SQ and CQ each empty separately: Smol740/315976, Qwen741/320506. No requirement of CQ=SQ is imposed because multishot CQ traffic is real.

Full lifecycle straces contain the two setup enters, one steady blocking enter ending EINTR at SIGTERM, and one drain enter. No request accept/recv/send-family host syscall occurs across the serving interval. The driver's `ready_time_ns` is recorded after reading NET_READY; the steady call can begin just before that observer timestamp, so I also inspected the full transcript/source rather than counting only starts after that timestamp. `CLEANUP ring_connections_buffers_released`, normal exit0 and zero remaining pins establish successful cleanup for these suites. Source synchronizes the model stream, publishes model_quiesced, drains until finished and synchronizes the I/O stream before releasing buffers/link/state. These are source plus successful-shutdown receipts, not a direct sample of quiescence fields after they were freed.

## Host context, failures and remaining limits

All five saved snapshots have boot_id04dc0087-5ccc-4c46-9997-b9a92f0e5167. Preflight18:35:19 shows one Python GPU app; before18:47:09 is empty; during18:49:33 and mid19:00:04 show one Python GPU app; after20:36:52 is empty. Host and container PID domains are different, and these sparse samples alone do not prove continuous app attribution or exclusivity. The after snapshot is82min8.158s after full terminal19:14:43.986672, so it is a delayed restoration observation rather than an immediate final-cell bracket. All snapshots retain the same33 selected historical NVRM reference warnings (06:22:53..10:50:43 UTC). No new selected fault is visible, but that is not a continuously clean journal or all-fault-free proof. RTX5090 snapshots consistently show existing400W power limit versus575W default; no reviewer/run power mutation is recorded. This common hardware condition bounds portability.

No scientific run failure or retry/exclusion within this admitted full matrix was found. Build stderr retains kernel-UAPI user-space warning diagnostics; executor logs retain ordinary vLLM precision/seed/bootstrap warnings. They are not silently removed or scored as wins. Historical AMK oracle failure, adverse Qwen fifth TPS block, Qwen short-output regression and native CPU/performance boundaries remain explicit. During independent review, two temporary CPU assertions were corrected for reviewer-only list-versus-tuple comparison and floating division associativity; a host-summary display attempted len on an integer and was corrected. These did not mutate artifacts, producer criteria or collected results and did not trigger a model rerun.

Inference is limited by n=5, five-of-six order imbalance, one machine/shared-host thermal/order drift, finite closed-loop32-request cells, four frozen prompts, two cached small models, token-ID HTTP/binary framing, max64 prompt/output and eight slots, chunk-level receive timestamps and untraced ordinary histories. The effective CPU metric is known executor process CPU plus recorded module TX CPU (zero module TX here); it excludes client CPU and does not comprehensively account BPF/softirq/io_uring/all network CPU. No offered-load capacity, p99/SLO, all-input math, eager-HF parity, energy, full text/API service, arbitrary model, remote transport or kernel-portability claim is established.

## Complete audited numerical appendices

The tables below reproduce the independently checked values. CPU units are microseconds of known-worker CPU per request. All effects are standalone-minus-control; positive latency/CPU means worse and positive TPS means better. Every mean, block and nominal interval remains in the raw machine-readable analysis, including negatives. No favorable subset is selected.

### All process-block means

|Model|gen|c|Path|TPS|TTFT ms|Completion ms|TPOT ms|CPU us/request|
|---|---:|---:|---|---:|---:|---:|---:|---:|
|Smol|1|1|uring_loop_coalesced|822.762030|1.202832|1.202832|n/a|45.218831|
|Smol|1|1|userspace|851.458521|1.166645|1.166645|n/a|42.887794|
|Smol|1|1|uring_loop|849.106279|1.165714|1.165714|n/a|47.546913|
|Smol|64|1|uring_loop_coalesced|1318.533709|1.193983|48.541950|0.751555|1524.890600|
|Smol|64|1|userspace|1386.580328|1.164933|46.123189|0.713623|1270.055344|
|Smol|64|1|uring_loop|1365.547587|1.130492|46.859540|0.725858|1550.363925|
|Smol|1|8|uring_loop_coalesced|3222.206516|2.179160|2.179160|n/a|18.320019|
|Smol|1|8|userspace|3439.363165|2.196005|2.196005|n/a|20.057394|
|Smol|1|8|uring_loop|3286.453311|2.220609|2.220609|n/a|20.824200|
|Smol|64|8|uring_loop_coalesced|5175.049052|2.097951|98.847750|1.535711|468.260475|
|Smol|64|8|userspace|5619.007572|1.860964|91.105200|1.416575|421.765950|
|Smol|64|8|uring_loop|5566.111767|1.871643|91.441205|1.421739|467.006219|
|Qwen|1|1|uring_loop_coalesced|651.913931|1.508744|1.508744|n/a|51.249494|
|Qwen|1|1|userspace|700.759679|1.412797|1.412797|n/a|46.447019|
|Qwen|1|1|uring_loop|705.106587|1.397471|1.397471|n/a|54.132613|
|Qwen|64|1|uring_loop_coalesced|794.615531|1.431789|80.518949|1.255352|2519.368419|
|Qwen|64|1|userspace|819.546317|1.344384|78.054457|1.217620|2095.774125|
|Qwen|64|1|uring_loop|812.796818|1.374591|78.713576|1.227603|2638.540187|
|Qwen|1|8|uring_loop_coalesced|2772.938170|2.591148|2.591148|n/a|19.178444|
|Qwen|1|8|userspace|2824.574371|2.643351|2.643351|n/a|23.005206|
|Qwen|1|8|uring_loop|2677.855298|2.765961|2.765961|n/a|22.327444|
|Qwen|64|8|uring_loop_coalesced|4613.723184|2.346320|110.872069|1.722631|506.808631|
|Qwen|64|8|userspace|4810.983074|2.290191|106.333568|1.651482|441.134950|
|Qwen|64|8|uring_loop|4688.844650|2.392450|107.875784|1.674339|552.933219|

### All signed paired effects

|Model|gen|c|Control|Metric|Mean delta|Nominal t95|Five block deltas|
|---|---:|---:|---|---|---:|---|---|
|Smol|1|1|uring_loop_coalesced|ttft_ms|-0.037118|[-0.105049, 0.030814]|-0.046568, -0.074224, -0.045920, 0.057258, -0.076134|
|Smol|1|1|uring_loop_coalesced|completion_ms|-0.037118|[-0.105049, 0.030814]|-0.046568, -0.074224, -0.045920, 0.057258, -0.076134|
|Smol|1|1|uring_loop_coalesced|tokens_per_s|26.344249|[-26.081027, 78.769524]|32.929310, 63.595058, 26.439569, -44.277016, 53.034323|
|Smol|1|1|uring_loop_coalesced|CPU us/request|2.328081|[-3.230578, 7.886741]|2.823000, -1.326812, -0.303656, 9.853469, 0.594406|
|Smol|1|1|userspace|ttft_ms|-0.000930|[-0.067323, 0.065462]|-0.028911, -0.017173, 0.006399, 0.086998, -0.051964|
|Smol|1|1|userspace|completion_ms|-0.000930|[-0.067323, 0.065462]|-0.028911, -0.017173, 0.006399, 0.086998, -0.051964|
|Smol|1|1|userspace|tokens_per_s|-2.352242|[-55.865878, 51.161393]|18.124262, 13.227570, -10.470175, -72.498237, 39.855369|
|Smol|1|1|userspace|CPU us/request|4.659119|[-6.469387, 15.787625]|-10.163594, 3.126281, 8.400281, 12.653156, 9.279469|
|Smol|64|1|uring_loop_coalesced|ttft_ms|-0.063491|[-0.175195, 0.048212]|-0.130597, -0.054677, -0.018471, 0.056453, -0.170165|
|Smol|64|1|uring_loop_coalesced|completion_ms|-1.682410|[-4.597793, 1.232973]|-4.172876, -0.961487, -1.322768, 1.687718, -3.642636|
|Smol|64|1|uring_loop_coalesced|tokens_per_s|47.013879|[-32.910547, 126.938304]|114.956213, 27.829687, 38.638837, -46.333801, 99.978458|
|Smol|64|1|uring_loop_coalesced|CPU us/request|25.473325|[-130.047040, 180.993690]|-19.025281, 9.436438, -90.434625, 239.221375, -11.831281|
|Smol|64|1|uring_loop_coalesced|tpot_ms|-0.025697|[-0.070291, 0.018897]|-0.064163, -0.014394, -0.020703, 0.025893, -0.055119|
|Smol|64|1|userspace|ttft_ms|-0.034441|[-0.149279, 0.080397]|-0.175172, -0.021546, -0.010210, 0.081743, -0.047023|
|Smol|64|1|userspace|completion_ms|0.736351|[-0.787563, 2.260266]|-0.166252, 0.592000, 0.005402, 2.865250, 0.385356|
|Smol|64|1|userspace|tokens_per_s|-21.032741|[-63.876013, 21.810532]|4.956639, -17.803987, -0.203605, -80.626692, -11.486058|
|Smol|64|1|userspace|CPU us/request|280.308581|[156.995056, 403.622106]|288.848469, 301.656625, 133.857719, 411.673563, 265.506531|
|Smol|64|1|userspace|tpot_ms|0.012235|[-0.010540, 0.035009]|0.000142, 0.009739, 0.000248, 0.044183, 0.006863|
|Smol|1|8|uring_loop_coalesced|ttft_ms|0.041449|[-0.184346, 0.267244]|-0.080750, -0.110173, 0.019123, 0.347643, 0.031403|
|Smol|1|8|uring_loop_coalesced|completion_ms|0.041449|[-0.184346, 0.267244]|-0.080750, -0.110173, 0.019123, 0.347643, 0.031403|
|Smol|1|8|uring_loop_coalesced|tokens_per_s|64.246795|[-456.186480, 584.680070]|285.993483, 557.483849, -202.762766, -505.160654, 185.680065|
|Smol|1|8|uring_loop_coalesced|CPU us/request|2.504181|[-1.167141, 6.175504]|3.764875, -0.347687, 3.269062, 6.404531, -0.569875|
|Smol|1|8|userspace|ttft_ms|0.024604|[-0.117246, 0.166454]|0.107890, -0.026146, -0.017111, -0.113829, 0.172215|
|Smol|1|8|userspace|completion_ms|0.024604|[-0.117246, 0.166454]|0.107890, -0.026146, -0.017111, -0.113829, 0.172215|
|Smol|1|8|userspace|tokens_per_s|-152.909855|[-463.913197, 158.093487]|-272.852164, 18.435825, -181.099481, 156.526384, -485.559839|
|Smol|1|8|userspace|CPU us/request|0.766806|[-2.696693, 4.230305]|2.010094, 4.545594, 1.222500, -2.181125, -1.763031|
|Smol|64|8|uring_loop_coalesced|ttft_ms|-0.226308|[-0.434604, -0.018012]|-0.313031, -0.124903, -0.355568, 0.020046, -0.358085|
|Smol|64|8|uring_loop_coalesced|completion_ms|-7.406544|[-12.301569, -2.511519]|-11.676578, -5.590402, -4.328322, -3.783907, -11.653513|
|Smol|64|8|uring_loop_coalesced|tokens_per_s|391.062716|[102.619263, 679.506168]|633.096882, 246.098746, 229.210818, 191.105722, 655.801410|
|Smol|64|8|uring_loop_coalesced|CPU us/request|-1.254256|[-18.547258, 16.038746]|3.549438, -12.335812, -8.816906, 21.109875, -9.777875|
|Smol|64|8|uring_loop_coalesced|tpot_ms|-0.113972|[-0.189706, -0.038238]|-0.180374, -0.086754, -0.063060, -0.060380, -0.179292|
|Smol|64|8|userspace|ttft_ms|0.010678|[-0.158838, 0.180194]|0.011151, -0.103134, 0.118658, 0.171355, -0.144640|
|Smol|64|8|userspace|completion_ms|0.336005|[-0.585872, 1.257882]|0.350637, -0.824670, 0.587868, 0.339049, 1.227140|
|Smol|64|8|userspace|tokens_per_s|-52.895805|[-90.472152, -15.319458]|-56.469343, -16.080202, -77.292420, -28.501029, -86.136029|
|Smol|64|8|userspace|CPU us/request|45.240269|[29.876490, 60.604048]|43.131438, 40.662406, 50.655313, 29.189531, 62.562656|
|Smol|64|8|userspace|tpot_ms|0.005164|[-0.009574, 0.019902]|0.005389, -0.011453, 0.007448, 0.002662, 0.021774|
|Qwen|1|1|uring_loop_coalesced|ttft_ms|-0.111272|[-0.183836, -0.038709]|-0.080821, -0.193319, -0.083173, -0.149207, -0.049842|
|Qwen|1|1|uring_loop_coalesced|completion_ms|-0.111272|[-0.183836, -0.038709]|-0.080821, -0.193319, -0.083173, -0.149207, -0.049842|
|Qwen|1|1|uring_loop_coalesced|tokens_per_s|53.192655|[10.543163, 95.842148]|28.259858, 98.431953, 38.508172, 80.544913, 20.218380|
|Qwen|1|1|uring_loop_coalesced|CPU us/request|2.883119|[-2.304991, 8.071228]|4.721750, -2.865875, 6.163312, 6.548187, -0.151781|
|Qwen|1|1|userspace|ttft_ms|-0.015325|[-0.071654, 0.041004]|0.014879, -0.020291, -0.090321, 0.024267, -0.005161|
|Qwen|1|1|userspace|completion_ms|-0.015325|[-0.071654, 0.041004]|0.014879, -0.020291, -0.090321, 0.024267, -0.005161|
|Qwen|1|1|userspace|tokens_per_s|4.346907|[-27.563503, 36.257317]|-20.576563, 12.932425, 43.914328, -14.738635, 0.202982|
|Qwen|1|1|userspace|CPU us/request|7.685594|[4.183470, 11.187717]|10.833156, 8.896531, 9.260719, 4.293000, 5.144562|
|Qwen|64|1|uring_loop_coalesced|ttft_ms|-0.057198|[-0.173696, 0.059299]|-0.046045, -0.152446, -0.014101, -0.144675, 0.071275|
|Qwen|64|1|uring_loop_coalesced|completion_ms|-1.805373|[-4.127231, 0.516484]|-1.536318, -3.557412, -1.313538, -3.558335, 0.938736|
|Qwen|64|1|uring_loop_coalesced|tokens_per_s|18.181287|[-4.944601, 41.307175]|15.789995, 35.508486, 13.450618, 35.519114, -9.361779|
|Qwen|64|1|uring_loop_coalesced|CPU us/request|119.171769|[-17.933713, 256.277251]|247.713375, 41.694125, 228.352687, 11.795313, 66.303344|
|Qwen|64|1|uring_loop_coalesced|tpot_ms|-0.027749|[-0.062768, 0.007270]|-0.023655, -0.054047, -0.020626, -0.054185, 0.013769|
|Qwen|64|1|userspace|ttft_ms|0.030207|[0.000927, 0.059487]|0.033987, 0.033185, 0.019947, -0.000366, 0.064282|
|Qwen|64|1|userspace|completion_ms|0.659118|[-0.600523, 1.918759]|0.172118, 0.211841, 0.216077, 0.222023, 2.473532|
|Qwen|64|1|userspace|tokens_per_s|-6.749499|[-19.527528, 6.028531]|-1.793649, -2.192119, -2.279482, -2.327396, -25.154847|
|Qwen|64|1|userspace|CPU us/request|542.766062|[449.176287, 636.355838]|527.007937, 466.805094, 628.638469, 477.440969, 613.937844|
|Qwen|64|1|userspace|tpot_ms|0.009983|[-0.009642, 0.029607]|0.002193, 0.002836, 0.003113, 0.003530, 0.038242|
|Qwen|1|8|uring_loop_coalesced|ttft_ms|0.174813|[0.015763, 0.333864]|0.063238, 0.091558, 0.090923, 0.327824, 0.300522|
|Qwen|1|8|uring_loop_coalesced|completion_ms|0.174813|[0.015763, 0.333864]|0.063238, 0.091558, 0.090923, 0.327824, 0.300522|
|Qwen|1|8|uring_loop_coalesced|tokens_per_s|-95.082872|[-394.839304, 204.673561]|165.841642, 12.317226, 48.939146, -323.717722, -378.794651|
|Qwen|1|8|uring_loop_coalesced|CPU us/request|3.149000|[0.030839, 6.267161]|0.692781, 0.145938, 4.700188, 4.846281, 5.359813|
|Qwen|1|8|userspace|ttft_ms|0.122611|[-0.022360, 0.267581]|0.165511, 0.093522, -0.040622, 0.113559, 0.281082|
|Qwen|1|8|userspace|completion_ms|0.122611|[-0.022360, 0.267581]|0.165511, 0.093522, -0.040622, 0.113559, 0.281082|
|Qwen|1|8|userspace|tokens_per_s|-146.719072|[-285.002636, -8.435509]|-115.968464, -192.895507, -44.234455, -63.279707, -317.217229|
|Qwen|1|8|userspace|CPU us/request|-0.677763|[-4.398996, 3.043471]|2.435937, -2.276969, -4.631969, -1.048969, 2.133156|
|Qwen|64|8|uring_loop_coalesced|ttft_ms|0.046130|[-0.040410, 0.132670]|-0.053261, 0.018950, 0.044211, 0.093719, 0.127031|
|Qwen|64|8|uring_loop_coalesced|completion_ms|-2.996285|[-7.562881, 1.570311]|-3.192802, -7.365159, -4.005828, -3.243627, 2.825992|
|Qwen|64|8|uring_loop_coalesced|tokens_per_s|75.121467|[-144.333957, 294.576890]|104.210971, 244.863030, 156.007717, 92.791351, -222.265736|
|Qwen|64|8|uring_loop_coalesced|CPU us/request|46.124588|[14.166118, 78.083057]|57.455250, 26.986125, 75.069344, 12.167906, 58.944313|
|Qwen|64|8|uring_loop_coalesced|tpot_ms|-0.048292|[-0.119983, 0.023399]|-0.049834, -0.117208, -0.064286, -0.052974, 0.042841|
|Qwen|64|8|userspace|ttft_ms|0.102259|[-0.161864, 0.366382]|0.014902, 0.008624, 0.060414, -0.049016, 0.476371|
|Qwen|64|8|userspace|completion_ms|1.542216|[-3.521460, 6.605892]|1.618481, -3.387453, 0.332727, 1.228879, 7.918446|
|Qwen|64|8|userspace|tokens_per_s|-122.138423|[-370.862461, 126.585614]|-113.090907, 88.783680, -48.919923, -84.892925, -452.572043|
|Qwen|64|8|userspace|CPU us/request|111.798269|[77.037076, 146.559461]|96.969125, 96.955656, 132.406594, 82.945531, 149.714438|
|Qwen|64|8|userspace|tpot_ms|0.022856|[-0.054002, 0.099714]|0.025454, -0.053906, 0.004322, 0.020284, 0.118128|

### Audited ordinary-round effects

|Model|Context|Control|Mean round delta|Nominal t95|Five block deltas|
|---|---|---|---:|---|---|
|Smol|gen1/c8 short|uring_loop_coalesced|2.400000|[1.719913, 3.080087]|[2, 2, 3, 3, 2]|
|Smol|gen1/c8 short|userspace|0.000000|[-0.877989, 0.877989]|[0, 0, 0, -1, 1]|
|Qwen|gen1/c8 short|uring_loop_coalesced|2.400000|[1.719913, 3.080087]|[2, 2, 2, 3, 3]|
|Qwen|gen1/c8 short|userspace|0.200000|[-0.355289, 0.755289]|[0, 0, 0, 0, 1]|
|Smol|gen64/c8 transfer|uring_loop_coalesced|7.000000|[4.223555, 9.776445]|[10, 8, 7, 4, 6]|
|Smol|gen64/c8 transfer|userspace|5.600000|[2.483448, 8.716552]|[8, 7, 7, 2, 4]|
|Qwen|gen64/c8 transfer|uring_loop_coalesced|7.800000|[5.958315, 9.641685]|[10, 6, 7, 8, 8]|
|Qwen|gen64/c8 transfer|userspace|6.400000|[3.283448, 9.516552]|[10, 3, 6, 7, 6]|

## Evidence paths and release

All paths are relative to `/tmp/bpfusion-current-io-placement-6xw2vxa6` unless explicitly stated:

- `plan.md`, `plan-review.md`, `run.py`, `setup.py`, `matched_serving.py`, `short_serving.py`, `transfer_serving.py`, `qualification.py`, `lifecycle.py`, `run_qualification.py`, `run_lifecycle.py`.
- `full.commands.json`, `full.exit.json`, all `full_short_*`/`full_transfer_*` raw JSONL/driver/executor stdout/exit files; `full.analysis.json`, `full.analysis.stdout`, `full.analysis.exit.json`; `analysis.py`.
- `long_counter_analysis.py`, `long_counter.analysis.stdout`, `long_counter.analysis.exit.json`.
- `qualification_vllm_{smol,qwen}.jsonl`, corresponding `.network.txt`, `.gpu.jsonl`, `.references.jsonl`, stdout/exit and `qualification.analysis.*`.
- `lifecycle_vllm_{smol,qwen}/` raw request/reply JSON, native stdout/stderr/strace and `lifecycle.analysis.*`.
- `frozen_references.json`, `{smol,qwen}_frozen.json`, `source_snapshot/`, `source_frozen.json`, `packages.json`, `environment.json`, `build.stdout`, `build.stderr`, `build_status.json`, `preserved_before.json`, `post_run_source.json`.
- `host_preflight.json`, `host_before.json`, `host_during.json`, `host_mid.json`, delayed `host_after.json`.
- Actual current `/workspaces/repository/executor/{vllm_graph.py,vllm_graph.cu,io_uring_tcp.h,userspace_tcp.h}`, `/workspaces/repository/bpf/{fusion.bpf.c,uring_loop.bpf.c,include/bpfusion_queue.h}`, `/workspaces/repository/bench/resident_dispatch.py`, `/workspaces/repository/Makefile` and retained `/workspaces/repository/docs/evaluation.md` AMK boundary.

Review is complete. All CPU read processes returned terminal status and file contexts closed. No GPU process or retained subprocess/handle was created by the reviewer. The report returns the mixed result to the owning agent; original state and all raw adverse/failure evidence remain preserved.
