# Independent result review: upstream batch-invariant matched serving

Reviewed in the original yunwei356/bpfusion-dev Workspace on main. This is the fresh result review required by research-experiment-design. No serving, GPU experiment, oracle repair, production edit, or delegation was performed by this reviewer. All numerical checks below were independently reconstructed from raw JSONL and compared with the saved analysis output, rather than accepting terminal success as scientific validation.

## Separate judgments

- Run status: valid for the completed finite same-mode serving comparison; final restoration was inspected and independently rechecked below.
- Tested hypothesis: supported for finite exact official-output fidelity and compatibility of the tested FP16 backend path. The primary throughput superiority question is inconclusive for both models.
- Research value: supporting. Official reference/setup/width checks alone are dependencies with zero standalone contribution.
- Paper impact: mechanism or workload boundary; this adds qualified same-mode serving evidence without a formal RQ or direct thesis claim.
- Next paper decision: retain an optional qualified execution path and its matched numbers, with no default promotion or transport speedup claim. Prioritize a genuinely discriminating serving/total-CPU experiment over another local publication tweak. This review does not authorize a new experiment or scientific redesign.

## Evidence and completion

Examined plan.md, the full initial plan-review.md, execution-notes.md, setup/reference/run adapters, actual serving.py/analysis.py/vllm_graph.py and their diffs; all ten production source snapshots; official raw generation and frozen assets; every preflight, qualification and full request/cell/executor record; saved analysis/status/command outputs; build/runtime records; qualification graph/reference/network traces; host snapshots. Source-native trajectory replay code independently reconstructs and advances graph/KV/history and asserts each traced GPU result before writing replay references.

Commands were the five literal stages python3 run.py setup, reference, preflight, qualification, full. The reference stage completed before preflight; one actual Qwen preflight succeeded. Both two-transport/model protocol qualifications succeeded before full. Full terminal is 2026-10-15T05:22:02.721225+00:00, with both driver and analysis exits zero. No excluded full cells, failing-output retries, post-observation reference edits, changed timeouts or weaker oracle were found.

The pre-observation list/tuple adapter defect was repaired without altering token IDs; the later pre-observation traced-analysis official equality check preserves the same criterion. Initial saved diffs were stale for these repairs; the root was asked to regenerate exact diffs as a provenance correction, not a runtime rerun.

## Independent official control and oracle

Each model has ten distinct tokenized inputs: four fixed ordinary prompts plus lengths1/15/16/17/32/64. Serial official LLM.generate(max_tokens=64, temperature=0, ignore_eos=True, detokenize=False) ran before BPFusion observation. Every later official gen1/64 forward/reverse request at full widths1..8 matches its single serial64 prefix; no variant union is permitted. The asset is an independent same-mode control, not an eager-HF/task-quality oracle or speed baseline.

- qwen: 394 official request outputs, 13120 tokens, ten unique serial64 references; all 32 order/width/gen combinations represented. Last official record 2026-10-15T04:44:17.068033+00:00.

- smol: 394 official request outputs, 13120 tokens, ten unique serial64 references; all 32 order/width/gen combinations represented. Last official record 2026-10-15T04:45:46.855921+00:00.

The combined asset was frozen at 2026-10-15T04:45:52.039194+00:00, before first serving at04:46:24Z. All served accepted responses and empty rejections in preflight/qualification/full were checked anew against this asset. This qualifies only the observed finite prompts, output lengths, models, dtype, device and mode.

## Independent serving reconstruction

|Stage/model|Executors|Requests incl warmup/reject|Tokens|Measured cells|Measured requests|Measured tokens|
|---|---:|---:|---:|---:|---:|---:|
|preflight_qwen|2|80|2096|8|64|2080|
|qualification_qwen|2|1244|44448|0|0|0|
|qualification_smol|2|1244|44448|0|0|0|
|full_qwen|10|1360|41680|40|1280|41600|
|full_smol|10|1360|41680|40|1280|41600|

Full totals:20 executors,80 cells,2560 measured requests/83200 measured tokens, plus160 checked gen1 warmups. Qualification totals:4 executors,2488 requests/88896 delivered tokens, including1036 empty rejections. Preflight adds80 requests/2096 tokens, including16 warmups. Request counts are not pooled for uncertainty: five paired process blocks/model remain the inferential units.

## Qualification and mechanism engagement

|Model|Transport|Compute rounds|Prefill|Decode|Release rounds|max release|
|---|---|---:|---:|---:|---:|---:|
|qwen|uring_loop|5690|146|5544|276|8|
|qwen|userspace|6504|146|6358|187|8|
|smol|uring_loop|5566|146|5420|279|8|
|smol|userspace|6484|146|6338|186|8|

All four histories independently reconstruct admission identity, physical-slot ownership, compute outputs, ordered prefix release and complete622-request replay. Actual GPU batch sizes1..8 occur in each; all accepted output IDs also match the separate official references. The final model trace overflow is zero. Loop network reply diagnostics are intentionally bounded128 entries: qualification trace_count622/trace_overflow494; ordinary full136/8. These counters do not mean model-token trace loss.

All-thread strace begins before readiness. After readiness each loop has zero accept/recv/send-family calls and exactly one io_uring_enter before termination signal. Native engages actual accept4,recvfrom,sendmsg. This is mechanism evidence from traced qualification, not direct syscall observation of every ordinary cell. Worker tasks show no loop SQPOLL thread. Runtime graph counters show one resident launch, two graph launches per model step, graph_error0 and model_trace_overflows0. Ordinary every executor admits/retires136; ring head/completed136, accepted/closed19, zero error/pending/reserved/dropped/overflow, empty SQ/CQ; every physical BPF request slot is FREE with reserved bitmap0. Native every ordinary executor publishes/completes136 with zero rejection. One loop protocol abort per qualification accompanies empty/half-close behavior and does not lose a checked request. No new lifecycle claim follows.

Native syscall counts from raw trace (post-ready) are retained, without interpreting strace cost as speed:
- qwen/uring_loop: {}, io_uring_enter before termination=1.
- qwen/userspace: {"accept4": 5139, "recvfrom": 8998, "sendmsg": 11559}, io_uring_enter before termination=0.
- smol/uring_loop: {}, io_uring_enter before termination=1.
- smol/userspace: {"accept4": 5133, "recvfrom": 8994, "sendmsg": 7518}, io_uring_enter before termination=0.

## Independently recomputed full metrics

Client throughput is delivered tokens divided by first measured request send-start to last token arrival, computed per cell and averaged over five processes. TTFT/completion/TPOT are reconstructed from client timestamps; socket chunks may coalesce token arrival times. Connections/thread creation/bootstrap/reference work occur outside timing. This is a local closed-loop finite workload, not official CLI execution, offered-load SLO, remote-network RTT, tokenization, or production tail measurement.

The following table includes every full workload cell family; loop/native are process-mean throughput and pooled-request mean latencies (equal32 requests per block).

|Model|gen/c|TPS loop/native|TTFT ms loop/native|Completion ms loop/native|TPOT ms loop/native|Known-worker CPU s/request loop/native|
|---|---|---|---|---|---|---|
|qwen|1/1|151.098603559/147.620796141|6.589406875/6.741029338|6.589406875/6.741029338|NA/NA|0.000206395/0.000183857|
|qwen|64/1|152.901298064/153.055872892|6.655110625/6.673553200|418.520997025/418.105183688|6.537553752/6.530660801|0.012962980/0.011010407|
|qwen|1/8|611.813807713/630.229065323|12.282638762/11.832950094|12.282638762/11.832950094|NA/NA|0.000073416/0.000064753|
|qwen|64/8|1204.242506214/1213.613253668|11.538442631/7.991935469|424.758021406/421.785191956|6.559040933/6.568146928|0.001741650/0.001512152|
|smol|1/1|273.487746567/276.729612383|3.645108794/3.597059662|3.645108794/3.597059662|NA/NA|0.000108911/0.000109580|
|smol|64/1|300.065034080/296.719911911|3.446369431/3.590427988|213.240618669/215.707778475|3.330067448/3.366942071|0.006376227/0.005097199|
|smol|1/8|1158.750387375/1141.242277007|6.489834194/6.328027375|6.489834194/6.328027375|NA/NA|0.000036468/0.000041570|
|smol|64/8|2304.156651082/2303.450626129|6.046930531/4.975821263|221.949086950/222.067384275|3.427018356/3.445897826|0.000889136/0.001028866|

Every reported paired effect was checked. The table below uses the literal signed difference loop minus native for all metrics, so positive latency/CPU is worse for loop. Saved analysis uses favoring-loop sign (native minus loop) for latency/CPU; the values below invert that sign explicitly. Intervals are nominal paired Student-t95 df4, critical2.776445105; no multiplicity correction, causal isolation, equivalence or broad population inference is implied.

|Model|gen/c|Metric|Five loop-native block differences|Mean|Nominal t95|
|---|---|---|---|---:|---|
|qwen|1/1|tokens_per_s|2.720361018, 2.921998922, 1.998315606, 10.580898796, -0.832537250|3.477807418|[-1.793949125, 8.749563962]|
|qwen|1/1|ttft_ms|-0.121754219, -0.102871250, -0.086569906, -0.456099438, 0.009182500|-0.151622463|[-0.372052876, 0.068807951]|
|qwen|1/1|completion_ms|-0.121754219, -0.102871250, -0.086569906, -0.456099438, 0.009182500|-0.151622463|[-0.372052876, 0.068807951]|
|qwen|1/1|known_worker_cpu_s_per_request|0.000078301, -0.000037317, -0.000008291, -0.000008227, 0.000088224|0.000022538|[-0.000047985, 0.000093061]|
|qwen|64/1|tokens_per_s|-0.302168730, -0.149534422, -0.329144853, 0.405068036, -0.397094171|-0.154574828|[-0.558974244, 0.249824588]|
|qwen|64/1|ttft_ms|-0.079356563, 0.023689938, -0.049358750, -0.065197813, 0.078010313|-0.018442575|[-0.101575397, 0.064690247]|
|qwen|64/1|completion_ms|0.833533187, 0.409784875, 0.884886563, -1.123276187, 1.074138250|0.415813338|[-0.694199582, 1.525826257]|
|qwen|64/1|tpot_ms|0.014490313, 0.006128491, 0.014829291, -0.016794895, 0.015811555|0.006892951|[-0.010244096, 0.024029998]|
|qwen|64/1|known_worker_cpu_s_per_request|-0.000143685, 0.000192224, 0.003783758, 0.003052246, 0.002878322|0.001952573|[-0.000278336, 0.004183482]|
|qwen|1/8|tokens_per_s|4.027093730, -3.725120355, -87.435690722, -0.349096732, -4.593473972|-18.415257610|[-66.507531961, 29.677016741]|
|qwen|1/8|ttft_ms|0.450590937, 0.493039156, 0.785216344, -0.300917563, 0.820514469|0.449688669|[-0.110912791, 1.010290128]|
|qwen|1/8|completion_ms|0.450590937, 0.493039156, 0.785216344, -0.300917563, 0.820514469|0.449688669|[-0.110912791, 1.010290128]|
|qwen|1/8|known_worker_cpu_s_per_request|-0.000000771, 0.000012311, 0.000033591, 0.000013650, -0.000015468|0.000008663|[-0.000013986, 0.000031312]|
|qwen|64/8|tokens_per_s|-7.207104353, -18.490179608, -1.523163407, -3.544917718, -16.088372183|-9.370747454|[-18.755311468, 0.013816560]|
|qwen|64/8|ttft_ms|2.274742313, 4.099826531, 3.953785625, 3.612672875, 3.791508469|3.546507163|[2.635378841, 4.457635484]|
|qwen|64/8|completion_ms|1.466016906, 6.364879437, 0.467807188, 1.132683094, 5.432760625|2.972829450|[-0.398524035, 6.344182935]|
|qwen|64/8|tpot_ms|-0.012836911, 0.035953221, -0.055332991, -0.039364917, 0.026051622|-0.009105995|[-0.058511306, 0.040299315]|
|qwen|64/8|known_worker_cpu_s_per_request|-0.000124233, 0.000568806, 0.000240254, 0.000120671, 0.000341991|0.000229498|[-0.000090016, 0.000549012]|
|smol|1/1|tokens_per_s|15.083224482, 5.451191234, 32.092735315, -52.742706963, -16.093773149|-3.241865816|[-43.836004740, 37.352273107]|
|smol|1/1|ttft_ms|-0.153841312, -0.064585937, -0.428251438, 0.760466281, 0.126458063|0.048049131|[-0.505151825, 0.601250087]|
|smol|1/1|completion_ms|-0.153841312, -0.064585937, -0.428251438, 0.760466281, 0.126458063|0.048049131|[-0.505151825, 0.601250087]|
|smol|1/1|known_worker_cpu_s_per_request|-0.000077645, -0.000004452, -0.000014674, 0.000039944, 0.000053481|-0.000000669|[-0.000064940, 0.000063602]|
|smol|64/1|tokens_per_s|0.129477536, 0.025406006, 8.487969636, -1.168338385, 9.251096051|3.345122169|[-2.957518895, 9.647763233]|
|smol|64/1|ttft_ms|-0.112148625, -0.114436156, -0.303144094, 0.045979781, -0.236543687|-0.144058556|[-0.310497129, 0.022380016]|
|smol|64/1|completion_ms|-0.107704656, -0.029705187, -6.199418875, 0.808759406, -6.807729719|-2.467159806|[-7.071798600, 2.137478987]|
|smol|64/1|tpot_ms|0.000070539, 0.001344936, -0.093591663, 0.012107613, -0.104304540|-0.036874623|[-0.107629197, 0.033879951]|
|smol|64/1|known_worker_cpu_s_per_request|0.001322429, 0.001376294, 0.000762228, 0.002468170, 0.000466021|0.001279028|[0.000326610, 0.002231447]|
|smol|1/8|tokens_per_s|-16.734430309, 104.364858940, 17.102449458, -9.970068311, -7.222257938|17.508110368|[-44.833600756, 79.849821492]|
|smol|1/8|ttft_ms|0.193597562, 0.100875375, 0.287668219, -0.138753344, 0.365646281|0.161806819|[-0.080597130, 0.404210768]|
|smol|1/8|completion_ms|0.193597562, 0.100875375, 0.287668219, -0.138753344, 0.365646281|0.161806819|[-0.080597130, 0.404210768]|
|smol|1/8|known_worker_cpu_s_per_request|0.000000132, 0.000004721, -0.000023363, 0.000001906, -0.000008910|-0.000005103|[-0.000019273, 0.000009068]|
|smol|64/8|tokens_per_s|-31.009342225, -12.620360649, 80.661117705, -29.823216412, -3.678073655|0.706024953|[-56.624470021, 58.036519927]|
|smol|64/8|ttft_ms|0.948987563, 1.253082250, 0.000677750, 2.080950562, 1.071848219|1.071109269|[0.147418175, 1.994800363]|
|smol|64/8|completion_ms|2.679530688, 1.188077719, -7.988080594, 3.263223031, 0.265762531|-0.118297325|[-5.776053747, 5.539459097]|
|smol|64/8|tpot_ms|0.027468938, -0.001031818, -0.126805688, 0.018766230, -0.012795011|-0.018879470|[-0.096344282, 0.058585343]|
|smol|64/8|known_worker_cpu_s_per_request|0.000323485, -0.000216276, -0.000022730, -0.000430544, -0.000352586|-0.000139730|[-0.000514291, 0.000234831]|

Executor CPU equals known-worker CPU here; module-TX task counter and its paired effects are identically zero. Those duplicate CPU series and all analysis means/percentiles/intervals were also checked, but repeated identical columns add no information. They omit RX/softirq/BPF/kernel TCP/io_uring work, client and other host costs. Zero module-TX accounting is not zero CPU.

Observed TTFT pooled p50/p99 and maxima, with all outliers retained:

|Model|gen/c|Mode|p50 ms|p99 ms|Maximum ms/block/index|
|---|---|---|---:|---:|---|
|qwen|1/1|uring_loop|6.547418000|7.670764000|8.879607000/p2/i27|
|qwen|1/1|userspace|6.601800000|10.777748000|11.393779000/p0/i29|
|qwen|64/1|uring_loop|6.552091000|9.065587000|9.269236000/p3/i9|
|qwen|64/1|userspace|6.566898000|9.154403000|12.036247000/p3/i16|
|qwen|1/8|uring_loop|12.431328000|16.355893000|19.220931000/p2/i25|
|qwen|1/8|userspace|12.309393000|14.384517000|14.447839000/p2/i22|
|qwen|64/8|uring_loop|12.345490000|15.131816000|15.139982000/p4/i6|
|qwen|64/8|userspace|6.272800000|13.361137000|13.807876000/p1/i4|
|smol|1/1|uring_loop|3.449866000|8.800590000|9.695635000/p3/i17|
|smol|1/1|userspace|3.469908000|6.751833000|9.200099000/p2/i26|
|smol|64/1|uring_loop|3.365382000|5.791306000|5.974905000/p4/i0|
|smol|64/1|userspace|3.412504000|6.296586000|8.838103000/p1/i29|
|smol|1/8|uring_loop|6.605359000|9.911046000|9.921777000/p4/i4|
|smol|1/8|userspace|6.524962000|8.997320000|9.778175000/p4/i30|
|smol|64/8|uring_loop|6.496854000|8.906858000|11.123469000/p4/i6|
|smol|64/8|userspace|3.884886000|13.457318000|13.470058000/p2/i28|

## Interpretation of the measured effects

Qwen gen64/c8 loop/native throughput is1204.242506214/1213.613253668 token/s. All five literal loop-minus-native block differences are negative; mean-9.370747454 token/s with nominal t95[-18.755311468,+0.013816560]. The interval narrowly crosses zero: do not round its upper end away to declare a statistically resolved loss. It establishes no throughput win. Smol is2304.156651082/2303.450626129, mean+0.706024953[-56.624470021,+58.036519927], also inconclusive rather than equivalent.

The adverse secondary effect is clear within this finite matrix: gen64/c8 mean TTFT is worse for loop by3.546507163ms[2.635378841,4.457635484] on Qwen and1.071109269ms[0.147418175,1.994800363] on Smol. These do not replace the fixed primary throughput result. Qwen loop TTFT is11.538442631ms versus7.991935469 native, Smol6.046930531 versus4.975821263. No transport latency benefit should be claimed. Smol gen64/c1 known-worker CPU is also worse for loop by0.001279028s/request[0.000326610,0.002231447]; that remains partial CPU accounting. Other workload metrics and adverse tails remain in the complete tables above.

Absolute mode speeds differ from prior default-mode snapshots, but this matrix has no concurrently matched default-mode cell or fully settled ordinary default fidelity. Neither a numerical mode-overhead effect nor the cause of0058's mismatch follows. The observed same-mode equality is useful new evidence that ordinary output validation can be independent of wrapper batch-history tracing for these finite inputs; it does not demonstrate arbitrary-input invariance, eager-HF equality, task quality or universal model compatibility.

## Baseline, mode, leakage and competing explanations

Native is the actual optimized timed-wait/epoll TCP implementation, not a Python per-token worker or failing proxy. Its traced accept/recv/send engagement, successful client outputs and completion counters were independently examined. It uses the same source, FP16 checkpoint revision, graph construction/body+head dispatch, padded prefill and prefix release, queue capacity, upstream mode, timer and request budgets. Build differences are the intended transport macros; BF_TRACE is present for both qualification builds and absent for both full builds. Four graph builds use NVCC13.0.88 sm_120/O3/C++17, same linked libcudart and libraries. Baseline suffered no avoidable runner failure or unequal output oracle.

All26 serving executors (preflight2,qualification4,full20) explicitly report enabled upstream mode with VLLM_BATCH_INVARIANT=1, CUBLAS_WORKSPACE_CONFIG=:16:8, CUBLASLT_WORKSPACE_SIZE=1, VLLM_USE_BREAKABLE_CUDAGRAPH unset and VLLM_USE_AOT_COMPILE=0; official controls report the same. The pinned upstream source initializes operation overrides, disables reduced precision reduction and uses cuBLASLt preference. FP16 does not select BF16 tuned matmul/breakable-graph policy. Its actual execution on this SM120 device is empirical support limited to the tested configuration, not a general upstream hardware promise.

Pinned runtime packages include vLLM0.31.0 (wheel commitgdb9527a46), Torch2.13.0+cu129, Transformers5.17.0, NumPy2.3.5, Triton3.7.1 and FlashInfer0.7.0.post1. Checkpoint revisions are Qwen7ae557604adf67be50417f59c2c2f167def9a775 and Smol93efa2f097d58c2a74874c7e644dbc9b0cee75a2. Full package vectors, requested env, original source snapshots and exact commands are retained; inherited/shared compilation caches remain a reproducibility limitation, not proof of equivalence to another run.

Official generation is independent of BPFusion outputs: its only source use from the old0058 asset is the local model checkpoint path. It constructs the prompts itself and writes a new single sequence per input before serving. The production driver is never allowed to add an observed serving variant. All accepted outputs and bad/empty responses were independently compared anew in this review. No answer-selection leakage or circular official oracle was found. The source-native trajectory replay is a distinct graph/history control and is not mislabeled as independent official generation.

Transport order alternates within paired blocks; cell order rotates. Qwen always precedes Smol; only five process pairs/model were run. Small closed-loop samples, scheduling/batch-formation differences, caches and host activity can influence the observed latency/throughput. Exact outputs and logical compute configuration are matched, but ordinary batch trajectories are intentionally unobserved. Do not infer identical graph-step schedules from output equality. No profiler runs perturb the full matrix.

## Host observations and limits

Read all six retained host receipts. Entry04:34:45.353019UTC and after05:23:18.874653UTC show no GPU compute application; after is76.153428s after the wrapper terminal. All receipts have boot04dc0087-5ccc-4c46-9997-b9a92f0e5167, existing400W requested/current ceiling (default575W), driver610.57.04, and exactly the same56 selected historical fault lines. I checked the selected-line arrays byte-equivalently, not just their count. The selected journal query returned0. No new selected warning was observed; the filter is not an exhaustive hardware-health proof.

Reference-active04:41:38 maps host PID2029961 to Workspace PID503233. Full-early05:01:33 maps2134248 to505898, Qwen block0 loop, after its ready05:01:26 and before terminal05:01:47. Full-Qwen05:07:33 maps2169660 to507372, Qwen block3 native, before its ready05:08:02. Full-Smol05:15:59 maps2215228 to509306, Smol block2 loop, before ready05:16:16. Every mapped GPU process belongs to original Pod3e8994f8-77ba-4a73-a3a5-35ed69a0a8a2/containera83771de83c8751ca3851fb01f648f254b33bee02efedf85f1d50713ebbf644d. The latter two are bootstrap observations. None of these sparse samples establishes continuous isolation across all performance windows or causation/harmlessness of historical warnings.

## Scope, artifact size and restoration

Production source change is exactly zero. I compared all ten source snapshots byte-for-byte with the current repository and raw metadata's embedded sources. Private executed adapters change serving.py by17 added/11 removed lines, analysis.py by8/4, bootstrap vllm_graph.py by4/1:29 additions,16 deletions, net13 lines across reused code. New setup/reference/stage-runner scripts are33/49/35 lines. These are necessary benchmark location/matrix/oracle/mode-observation adaptations, not a new public backend, protocol, configuration authority, scheduler or retained nondefault setting. Corrected .diff files now reproduce exactly from the executed scripts and saved sources.

At review time156 retained nonbinary files total18767022bytes, dominated by raw request, graph and strace evidence and source snapshots; this is archive growth, not implementation growth or scientific novelty. Reusing private full scripts duplicates existing code but preserves executed reproducibility. No extra public/default toggle, model kernel rewrite, persistent helper or unrelated boilerplate was found. Exclude runtime/binaries/vendor build trees and symlinks from the published archive; retain raw failures/warnings and experiment source. A later archive copy can add its README/report without changing these executed artifacts.

I read final_restoration.json at05:25:02.126313UTC and independently rechecked every removed owned path is absent. Owned processes are absent, runtime/private-build/libbpf source/install/tar are removed, and the eight original WIP/build paths retain identical inode/size/mtime/symlink metadata. Base Torch2.14.1/Transformers5.19.0/NumPy2.5.3 and Coder PID1/10909 starttimes are unchanged. Source bytes all match, the module is absent and BPF pins are empty. Git tracked worktree remains clean on main with only the original unowned tools/setup_env.sh. Shared model/global caches were retained.

After cleanup, I personally reran all five fixed CPU analyses (preflight Qwen, qualification Qwen/Smol, full Qwen/Smol). Each returned0 with stdout and stderr byte-for-byte identical to its saved output. This replay validates archive recomputation only; it is not another GPU experiment or additional independent statistical replication.

## Return decision

The finite official-output qualification gap is materially reduced in this optional upstream mode. The matched complete performance result does not show a throughput advantage and contains a reproducible adverse gen64/c8 TTFT effect within this sample. Keep the unchanged production implementation/defaults and report both facts together. This is supporting evidence toward the user's reusable serving objective, not the completion of that objective. The default ordinary-fidelity question, causal source of0058, total CPU cost, broader workloads/backends and service-level performance advantage remain unresolved. No new experiment, code repair, oracle adjustment or default promotion is authorized by this review.
