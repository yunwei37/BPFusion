# Prefill packing: fresh terminal result review — 2026-10-12 UTC

Reviewer: /root/coalesced_network_result_review. This review inspected actual source, setup receipts, raw client/trace/reference records and terminal state in the original yunwei356/bpfusion-dev Workspace. Only this report was written; no serving source, configuration, model, workload, Git state or infrastructure was changed.

## Verdict and paper decision

- Run status: **valid and complete** for the declared traced component experiment.
- Tested hypothesis: **mixed**. The primary gen1/eight-client TTFT hypothesis is locally supported for Qwen kernel transport; Qwen native, Smol kernel and Smol native are inconclusive.
- Research value: **supporting** engineering evidence, including a causal scheduling/metadata intervention. Correctness, semantic checks and untraced validation are setup dependencies, not separate scientific contributions.
- Paper impact: **mechanism/workload boundary and additional serving-adapter evidence**, not a direct thesis challenge. The retained full goal remains active; no formal RQ or thesis was invented.
- Next decision: close this matrix, retain all estimates and the grouped default, and do not promote a universal short-output packing gain. The limited Qwen kernel primary gain and concurrent long-output gains can be reported at their measured scope. The next decisive uncertainty is whether completed-slot retirement/release limits available short-output prefills; its causal role was not tested here.

No invalidating scientific/source-semantic defect or required wider baseline was identified. This review does not authorize source repair, production promotion or another experiment.

## Evidence and completion

Read the [plan](prefill_packing_plan_20261012.md), [independent plan review](prefill_packing_plan_review_20261012.md), current dispatcher/bootstrap, Makefile, driver/analyzer, installed upstream attention path and its pinned cache-writer implementation.

Durable full evidence: [Qwen raw](prefill_packing_20261012/qwen_performance.jsonl), [Smol raw](prefill_packing_20261012/smol_performance.jsonl), [Qwen analysis](prefill_packing_20261012/qwen_performance_analysis.stdout.txt), [Smol analysis](prefill_packing_20261012/smol_performance_analysis.stdout.txt). Per-process `*_p{0..4}_{condition}.gpu.jsonl`, matching `.references.jsonl` and stdout are retained beside these files. Exact selected executors/commands are in raw start records and [environment/build metadata](prefill_packing_20261012/environment.json), [build stdout](prefill_packing_20261012/build.stdout.txt).

Independent reconstruction through Python stdin verified:

- 160 unique complete cells, 10240 measured requests, 332800 exact measured output tokens and 40 normal executors; 320 excluded gen1 warmups add 320 tokens, giving 10560 total requests/333120 tokens.
- Each model has five blocks/four conditions/four cells: 80 cells, 5120 measured requests/166400 tokens plus160 warmups.
- Every measured cell has index0..63 exactly once and sixteen requests per each of four prompts; all timings, TTFT/completion/TPOT and first-send/last-arrival TPS recompute correctly.
- All client markers map uniquely to admissions and independently advanced own-history reference sequences. Compute-event tokens reconstructed by request ID exactly match complete received client tokens and references. Each request has one prefill, valid decode history and its full declared output length.
- Every executor has one resident launch, zero graph errors/trace overflow, max_active8, admitted264/retired264 and trace-model-step counters equal actual compute-event count. Sum of event batch sizes is8328 per executor.
- Kernel records end at head264/reserved0/eight FREE slots, busy0 and successful detach. All old executor PIDs are absent. Native executors each record accepted19/published264/completed264/rejected0.
- Native analyzer reruns exactly match both archived 79-record analyses. Independently recomputed every metric and every paired interval, including transport controls, completion and TPOT.
- All64 performance files/model in the permanent archive byte-match the original temporary files; no source-version stitching or selected row deletion occurred.

Qwen collection:21:57:15–22:10:47UTC, metadata main b2950e5. Smol:22:10:52–22:21:46UTC, metadata main5f18e0f. Source snapshots of driver/client/native/bootstrap match the same inspected implementation; b9031cd published that implementation during collection, and5f18e0f only extended analysis/prose. Serving behavior, oracle, timeout and workload did not change between the two model runs. The exact source snapshots distinguish the candidate from baseline commit names.

Condition order was identical for both models:
block0 GK,PK,GU,PU; block1 PU,GU,PK,GK; block2 GU,PU,GK,PK; block3 PK,GK,PU,GU; block4 GK,PK,GU,PU. GK/PK are grouped/packed kernel; GU/PU are grouped/packed native timed-network. Cell order remains the declared gen1/c1,gen64/c1,gen1/c8,gen64/c8. There is no request-level pseudo-replication.

## Source, semantic independence and setup

The native intervention chooses max prompt length among currently pending full-attention prefills and selects all of them without adding a wait. Leading dummy IDs/positions are0, padding flags true and KV slots-1. Real positions/KV slots/sequence lengths remain original; decode resumes at real prompt length rather than padded width. Grouped production remains the default compile path; BF_PAD_PREFILL selects the candidate. Module/BPF/wire ownership, decoding and model arithmetic are unchanged.

The installed FA2 path takes actual sequence lengths and query boundaries. Bottom-right causal alignment means real shifted query j=(Q−n)+t retains key bound j+n−Q=t. The pinned CUDA cache writer skips negative slot mappings before cache-address calculation. These contracts were checked in installed source and primary sources: [FlashAttention causal alignment](https://github.com/Dao-AILab/flash-attention#how-to-use-flashattention), [vLLM db9527a46 cache writer](https://raw.githubusercontent.com/vllm-project/vllm/db9527a46/csrc/libtorch_stable/cache_kernels.cu). The adapter rejects unsupported non-full-attention/uniform-cache conditions rather than assuming this applies to arbitrary model types.

Python replay reconstructs metadata from original prompts, recorded query width and its own generated history. It never teacher-forces served GPU tokens: outputs are compared only after upstream replay generates them, and replay's own outputs advance history. Real client bytes, rather than a scheduler count alone, must match.

The [semantic discriminator](prefill_packing_20261012/semantic.py) independently removes leading shifts using compact real variable query boundaries and trailing ignored slots while retaining the same total Q×B graph shape. [Qwen](prefill_packing_20261012/qwen_semantic.jsonl) and [Smol](prefill_packing_20261012/smol_semantic.jsonl) each complete ten real-model groups. All631488 real hidden FP16 elements are finite, bit-identical, max_abs_diff0 and pass Torch dtype-default assert_close; sampled tokens also match. Source inspection confirms that failed assertions/nonzero serve status propagate. This is measured same-shape semantic evidence, not arbitrary dynamic-shape or task-quality equivalence. Hidden vectors themselves are not exported; this review verified the actual comparison code and terminal group receipts without launching another GPU replay.

The initial ctypes function-wrapper TypeError is preserved [separately](prefill_packing_20261012/qwen_semantic.initial_ctypes.jsonl). It occurred during import before model serving; the retry uses a CDLL subclass and does not change tolerances or the comparison.

The [real preflight](prefill_packing_20261012/preflight.jsonl) independently links eight mixed requests/512 tokens and actually joins differing prompt lengths. Frozen unpadded B1 agreement was only5/8 full sequences and7/8 first tokens; this was retained, not used to fit acceptance.

[Qwen](prefill_packing_20261012/qwen_correctness.jsonl) and [Smol](prefill_packing_20261012/smol_correctness.jsonl) strict candidate qualification each cover two transports×622 requests/22224 tokens, including259 rejections per transport, actual batches1..8, prompt edges1/15/16/17/32/64, mixed lengths, fragmentation, wrap/reuse, pipeline/half-close,5000 empty connections and helper-thread shutdown. Independent trace reconstruction verified every client→admission→compute→reference link. Actual mixed prefill events: Qwen kernel51/native72; Smol kernel50/native73. Kernel active-network traces exclude a userspace request/reply worker; native traces engage accept/receive/send control.

[Default untraced setup](prefill_packing_20261012/untraced.jsonl) completes four paths×40 requests/1300 tokens, exactly matching independently frozen unpadded B1 references, with normal exits/max_active1. It validates the tested grouped single-client default condition; it does not qualify untraced arbitrary dynamic-batch packed serving.

## Primary effects and uncertainty

Primary effect is grouped-minus-packed mean client TTFT for gen1/c8, paired within model/transport/block. Positive favors packing. Nominal two-sided t95 uses df4 and2.776445105; the four local intervals have no family-wide adjustment, and crossing zero is not equivalence.

| Model | Transport | Gain ms | Nominal t95 ms |
|---|---|---:|---|
| Qwen2.5-0.5B | kernel | 0.158786809 | [0.017961560, 0.299612058] |
| Qwen2.5-0.5B | userspace | 2.583309587 | [-4.679427582, 9.846046757] |
| SmolLM2-135M | kernel | 0.410142516 | [-0.200853279, 1.021138310] |
| SmolLM2-135M | userspace | -0.012981197 | [-0.109618254, 0.083655861] |

Five block differences0–4:

- Qwen2.5-0.5B/kernel: 0.299835578, 0.038204484, 0.094633469, 0.257923469, 0.103337047 ms.
- Qwen2.5-0.5B/userspace: -0.154087469, 0.658909047, -0.003443500, 13.015437781, -0.600267922 ms.
- SmolLM2-135M/kernel: 0.790911063, 0.756351000, -0.160647297, -0.095572781, 0.759670594 ms.
- SmolLM2-135M/userspace: 0.033955594, -0.010999000, 0.048101188, -0.146215531, 0.010251766 ms.

Only the Qwen/kernel primary interval excludes zero. Its grouped8.860676ms becomes packed8.701889ms, a local mean difference about1.8%; this is not a large general batching win. The other three primary comparisons remain inconclusive, including Smol native's negative point estimate.

Qwen native block3 retains grouped-minus-packed13.015438ms: grouped gen1/c8 cell ends22:08:07UTC and has332.549tokens/s, versus packed cell ending22:07:29UTC with896.877tokens/s. Correctness/counters pass. Its cause is unknown; do not remove/recollect it or label it proof of packing robustness. Sequential pairing and a shared host permit time-varying interference; no per-cell GPU/CPU attribution establishes a cause.

## All workload means and long-output tradeoffs

Each row below uses all five process blocks. TPS is the mean of aggregate cell TPS, not pooled-request inverse latency. These means retain single-client controls and negative/mixed data.

| Model | gen/clients | Transport | Grouped TTFT ms | Packed TTFT ms | Grouped TPS | Packed TPS |
|---|---|---|---:|---:|---:|---:|
| Qwen2.5-0.5B | 1/1 | kernel | 1.425937 | 1.424515 | 693.809 | 695.706 |
| Qwen2.5-0.5B | 1/1 | userspace | 1.401847 | 1.452222 | 707.648 | 686.472 |
| Qwen2.5-0.5B | 64/1 | kernel | 1.347752 | 1.338481 | 818.564 | 818.517 |
| Qwen2.5-0.5B | 64/1 | userspace | 1.343504 | 1.387715 | 813.806 | 813.219 |
| Qwen2.5-0.5B | 1/8 | kernel | 8.860676 | 8.701889 | 890.471 | 905.637 |
| Qwen2.5-0.5B | 1/8 | userspace | 11.515655 | 8.932346 | 777.397 | 888.283 |
| Qwen2.5-0.5B | 64/8 | kernel | 2.894712 | 2.155560 | 4632.037 | 4708.372 |
| Qwen2.5-0.5B | 64/8 | userspace | 2.946139 | 2.192735 | 4585.083 | 4668.389 |
| SmolLM2-135M | 1/1 | kernel | 1.191788 | 1.182695 | 831.412 | 836.100 |
| SmolLM2-135M | 1/1 | userspace | 1.204892 | 1.198712 | 819.352 | 825.226 |
| SmolLM2-135M | 64/1 | kernel | 1.174749 | 1.105684 | 1345.156 | 1390.599 |
| SmolLM2-135M | 64/1 | userspace | 1.132211 | 1.136320 | 1390.640 | 1390.038 |
| SmolLM2-135M | 1/8 | kernel | 7.458966 | 7.048823 | 1061.046 | 1118.231 |
| SmolLM2-135M | 1/8 | userspace | 6.967508 | 6.980489 | 1134.974 | 1133.398 |
| SmolLM2-135M | 64/8 | kernel | 2.494936 | 1.774843 | 5176.952 | 5525.449 |
| SmolLM2-135M | 64/8 | userspace | 2.372806 | 1.722330 | 5441.490 | 5543.895 |

Secondary gen64/c8 paired gains use grouped−packed for latency/completion/TPOT and packed−grouped for TPS. Units are ms except TPS(tokens/s).

| Model | Transport | Metric | Gain | Nominal t95 |
|---|---|---|---:|---|
| Qwen2.5-0.5B | kernel | ttft | 0.739151 | [0.726192, 0.752111] |
| Qwen2.5-0.5B | kernel | completion | 1.830379 | [1.481675, 2.179083] |
| Qwen2.5-0.5B | kernel | tpot | 0.017321 | [0.011637, 0.023005] |
| Qwen2.5-0.5B | kernel | tps | 76.335470 | [57.415596, 95.255343] |
| Qwen2.5-0.5B | userspace | ttft | 0.753404 | [0.543669, 0.963138] |
| Qwen2.5-0.5B | userspace | completion | 2.000558 | [-4.031369, 8.032484] |
| Qwen2.5-0.5B | userspace | tpot | 0.019796 | [-0.074208, 0.113800] |
| Qwen2.5-0.5B | userspace | tps | 83.305738 | [-160.986156, 327.597631] |
| SmolLM2-135M | kernel | ttft | 0.720093 | [0.628824, 0.811363] |
| SmolLM2-135M | kernel | completion | 6.401885 | [1.254586, 11.549183] |
| SmolLM2-135M | kernel | tpot | 0.090187 | [0.009872, 0.170502] |
| SmolLM2-135M | kernel | tps | 348.496560 | [76.788685, 620.204435] |
| SmolLM2-135M | userspace | ttft | 0.650476 | [0.537315, 0.763638] |
| SmolLM2-135M | userspace | completion | 1.730107 | [1.333211, 2.127003] |
| SmolLM2-135M | userspace | tpot | 0.017137 | [0.009454, 0.024820] |
| SmolLM2-135M | userspace | tps | 102.405490 | [79.623925, 125.187055] |

Both kernel models show positive local gen64/c8 intervals for all four metrics. Native gen64/c8 TTFT gains are supported in both models; native Smol also supports completion/TPOT/TPS gains, while native Qwen's latter three intervals cross zero. The common long-output TTFT benefit belongs to serving adaptation across transports and cannot be credited uniquely to eBPF. Single-client rows do not engage mixed packing; their differences are descriptive controls, not evidence of a mixed-prefill gain. Complete secondary intervals and P50/P99 are in the linked analyses; finite320-request pooled tails do not support a strong general P99 claim.

## Mechanism engagement and padding work

Per-pair arrays below are actual prefill calls for64 measured requests, not client concurrency. Mixed denotes prefill calls joining different real prompt lengths; dummyQ is extra query positions. Each measured cell has320 real prompt positions.

| Model | gen/c | Transport | Grouped calls0–4 | Packed calls0–4 | Packed mixed0–4 | Packed dummyQ0–4 |
|---|---|---|---|---|---|---|
| Qwen2.5-0.5B | 1/8 | kernel | 58,58,58,58,59 | 56,58,57,56,58 | 3,2,3,3,1 | 27,24,24,27,15 |
| Qwen2.5-0.5B | 1/8 | userspace | 57,58,58,55,58 | 58,58,58,58,58 | 1,1,1,2,2 | 21,21,21,12,18 |
| Qwen2.5-0.5B | 64/8 | kernel | 36,38,36,35,36 | 22,26,25,23,22 | 7,10,9,8,7 | 153,105,138,147,141 |
| Qwen2.5-0.5B | 64/8 | userspace | 38,34,34,37,35 | 20,21,25,22,25 | 9,11,10,10,9 | 156,147,144,132,138 |
| SmolLM2-135M | 1/8 | kernel | 58,58,58,57,58 | 58,58,58,58,58 | 2,1,2,1,2 | 18,24,24,18,15 |
| SmolLM2-135M | 1/8 | userspace | 58,58,58,57,58 | 58,58,57,58,58 | 2,2,2,1,1 | 24,24,21,18,18 |
| SmolLM2-135M | 64/8 | kernel | 38,38,40,39,37 | 26,25,23,26,27 | 7,9,8,9,10 | 132,135,150,123,132 |
| SmolLM2-135M | 64/8 | userspace | 39,40,40,36,36 | 24,26,26,26,23 | 12,12,15,14,11 | 129,129,120,111,138 |

All grouped and all single-client cells have zero dummyQ/mixed-prefill work. Packed gen1/c8 still needs56–58 calls in Qwen kernel and57–58 in the other candidate conditions: little consolidation. Packed gen64/c8 reduces call counts substantially but adds105–156 dummy query positions per320 real prompt positions. Those positions incur actual upstream computation and are not output tokens. No FLOP/CPU/energy reduction is inferred from graph counts.

The unchanged dispatcher retires at most one completed phase2 slot before selecting/launching the next compute group. That can plausibly limit pending-prefill availability under one-token closed-loop requests. Static sequencing and these counts motivate a separate completion-release discriminator; they do not establish that this ordering caused the remaining latency.

## Output differences and limits

Every served token matches its independently advanced same-shape upstream replay. Agreement with the separate frozen unpadded B1 sequence is different and is retained below, including warmups:

| Model | Condition | Full sequences equal/1320 | First tokens equal/1320 |
|---|---|---:|---:|
| Qwen2.5-0.5B | grouped-kernel | 1198 | 1278 |
| Qwen2.5-0.5B | packed-kernel | 1176 | 1256 |
| Qwen2.5-0.5B | grouped-userspace | 1200 | 1280 |
| Qwen2.5-0.5B | packed-userspace | 1180 | 1260 |
| SmolLM2-135M | grouped-kernel | 1208 | 1320 |
| SmolLM2-135M | packed-kernel | 1182 | 1320 |
| SmolLM2-135M | grouped-userspace | 1218 | 1320 |
| SmolLM2-135M | packed-userspace | 1194 | 1320 |


Direct condition-to-condition agreement was also independently reconstructed by model/block/cell/request index and matches all24 archived comparison records in [output_agreement.json](prefill_packing_20261012/output_agreement.json). Every single-client comparison agrees320/320 for full sequences and first tokens. Concurrent comparisons are:

| Model | gen/c | Comparison | Full sequences equal/320 | First tokens equal/320 |
|---|---|---|---:|---:|
| Qwen |1/8|GK→PK|312|312|
| Qwen |1/8|GU→PU|317|317|
| Qwen |1/8|PK→PU|317|317|
| Qwen |64/8|GK→PK|284|284|
| Qwen |64/8|GU→PU|283|283|
| Qwen |64/8|PK→PU|305|305|
| Smol |1/8|GK→PK|320|320|
| Smol |1/8|GU→PU|320|320|
| Smol |1/8|PK→PU|320|320|
| Smol |64/8|GK→PK|280|320|
| Smol |64/8|GU→PU|286|320|
| Smol |64/8|PK→PU|294|320|

Both grouped and packed have dynamic FP16 trajectory differences from B1. Same-shape semantic equality and real own-history replay establish the tested transformation, not identical text across batch shapes or task-quality equivalence. The comparison fixes generated length, checkpoint, upstream math/catalogue/cache and per-transport polling while changing scheduling, actual batch shapes and padding work. It is not external-vLLM serving superiority.

Scope remains loopback/token-ID HTTP, four short prompts in performance, two small full-attention FP16 checkpoints,128-token/eight-slot upstream-owned KV budget, one RTX5090 and identical BF_TRACE instrumentation. No total CPU/energy, real-NIC, full text processing, arbitrary-model or SOTA conclusion follows. Traced gains need not transfer unchanged to untraced dynamic serving; the broader retained goal is incomplete.

## Host state, deviations and proportionality

The durable [owner restoration](prefill_packing_20261012/owner_restoration.json), [Workspace state](prefill_packing_20261012/workspace_after_matrix.txt) and [bounded kernel journal](prefill_packing_20261012/host_journal.json) were also read. The original PodUID3e8994f8-77ba-4a73-a3a5-35ed69a0a8a2 is Running/Ready on lab with0 restarts; original Coder session processes and unrelated tools/setup_env.sh remain. The owner receipt records original base Torch2.14.1+cu130/Transformers5.19.0 and the reason for retaining the owned temporary runtime. The archived successful full journal read covers21:25:00–22:24:10UTC and has no listed fault matches.

At independent22:23:45UTC inspection the same boot04dc0087-5ccc-4c46-9997-b9a92f0e5167 remains; GPU compute-app list is empty. TX module and pins are absent, and host tc/bpftool queries in the original container network namespace show no loopback ingress/egress/XDP/net attachments. Explicit UTC kernel journal since21:55UTC through inspection has no matched OOM/kill/Xid/BUG/Oops/panic entries. This bounded search does not prove an interference-free host or explain Qwen's outlier. No prior-day SGLang-preservation claim is imported into this run.

Temporary runtime is vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0, with CUDA13.0.88 compiler and linked cu129 runtime as recorded. Base packages remain distinct; the owner retains this temporary runtime for the immediately following experiment, so it is not falsely reported as removed or deployed. Initial diagnostic import failure and all output differences remain available. No performance oracle, timeout, acceptance tolerance or model math was adjusted after observing results.

Relative to b2950e5, five changed source/build/analysis files total44 net lines: native dispatcher+12, Python replay+2, Makefile+1, driver+20 and analyzer+9. Serving production adaptation is small; most repository growth is receipts/prose. Four candidate compile variants extend existing native rules, with no persistent service, new scheduler, control schema or per-project orchestration layer. Completion/TPOT analyzer additions expose already-planned tradeoffs and do not alter serving behavior. This is proportional to the admitted experiment.

The evidence supports a small condition-specific Qwen kernel short-output gain and clearer concurrent long-output packing benefits. It also exposes limited short-output consolidation and unresolved dynamic-shape/default/host-cost acceptance. Keep the mixed result, preserve grouped production behavior, and investigate the next causal uncertainty without repeating the unchanged matrix or weakening the hypothesis.
