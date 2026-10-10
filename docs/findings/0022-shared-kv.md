# 0022: shared KV append in GPU-scheduled Qwen graphs

## Engineering question and plan

The active service objective asks for better throughput/latency with exact real-model output and no steady userspace request worker. There is no paper RQ or thesis in this repository. Finding0020 closes request-dispatch ablation and exposes serial queueing. Finding0021 saves capture memory but does not establish speed. This supporting engineering comparison asks whether eliminating repeated KV prefix concatenation/copy-back reduces real-client TPOT and improves output-token throughput with the same resident GPU scheduling policy. It is not a competing-serving or batching result.

The candidate uses the installed HF Cache/DynamicLayer extension: each captured graph has a known prefix offset, appends new keys/values into shared buffers and returns exactly the original attention prefix length. Eager attention, fp16 arithmetic, weights, device argmax, native dispatcher, kernel TX and wire protocol stay unchanged. It removes the DynamicCache prefix construction and whole-prefix output copy-back. No padding, backend or oracle change is involved. The potential gain is fewer GPU cache operations, rather than fewer CPU request calls. A positive result supports retaining this optimization; a negative or inconclusive result bounds its value and shifts priority to batching. New information is the changed cache implementation; the unchanged request-dispatch experiment is not repeated.

## Assets, correctness and fair comparison

Baseline capture source is pinned to `4b9e71a:executor/qwen_graph.py` (last-position logits). Candidate source and exact command are recorded in its strict raw log. Both compare the same `qwen_graph.so` native resident library from finding0020's checked, temporary TCP_NODELAY build. Both launch the native service once and keep model/decode scheduling on GPU. Matching temporary TCP_NODELAY is a test condition, not a retained production setting. Default serving remains unchanged until validation.

The candidate resident strict gen64/prompt-edge regression has passed 303 valid requests / 19,392 exact tokens / 259 rejections. The same host-control regression also passed 303 requests / 19,392 exact tokens / 259 rejections, with zero graph/admission errors, all-thread trace and clean teardown. GPU-only diagnostics completed; these are engineering qualification, not serving speed results. Keep all completed logs, including failures. Oracle, timeouts, metric definitions and model precision remain fixed.

Use the existing `bench/resident_dispatch.py` via a temporary copy with only tests import path, mode labels (`baseline`/`shared-kv`) and expected native launch marker adapted. Both engines are resident; this is a KV component comparison, not a host-policy comparison. The raw artifact will preserve the exact driver delta and sources. Reuse its official real TCP client/independent HF oracle, connection barriers, per-token client timestamps, complete-output verification and cleanup.

## Integrated run and interpretation

Use the previous matrix: four real prompts, gen1/gen64, clients1/8, five paired process blocks with alternating engine order and rotating matching cell order, 64 requests per cell. Eight warmups per process, bootstrap/capture and connection setup are excluded; idle CPU is separate. Complete measurement is 40 cells / ten normal process shutdowns / 2,560 exact requests / 83,200 exact output tokens. Each process has one resident service launch, 8,580 model graphs and 264 publications, zero graph/admission errors, all final slots FREE, and cleanup.

Primary quantities are client TPOT for gen64 and output-token throughput for gen64, separately at clients1/8. TPOT=(last arrival-first arrival)/63; throughput=output tokens/(last arrival-first send), following finding0020's NVIDIA metric definitions. Positive gain means baseline-minus-candidate TPOT or candidate-minus-baseline throughput. Report five paired block differences and two-sided 95% Student-t intervals (df4, critical2.776445105); shared GPU and only five blocks limit inference. Crossing zero is inconclusive, not equivalence. TTFT, completion latency, gen1 and executor-process CPU are secondary. No global superiority, optimized-serving win, total-host or energy claim. Multiple tokens in one recv share an arrival timestamp. GPU-only profiles exclude transport and GPU-tail scheduling and cannot replace real serving evidence.

Fresh read-only plan review precedes one real preflight (four gen1 requests per engine after eight warmups); then the complete matrix and one fresh read-only result review. This is the strongest immediately runnable qualification for an actual compute change. Batching and an official optimized serving comparison are more consequential next work, but adding them here would obscure the cache-only effect.

With `probe` pointing to the recorded owner temporary optimization directory:

```sh
HF_HOME=/workspaces/.cache/huggingface python3 "$probe/shared_kv_bench.py" --gen 64 --preflight --resident-executor "$probe/kv_baseline/qwen_graph" --host-executor "$probe/shared_kv/qwen_graph" --output bench/results/shared_kv_preflight_20261010.jsonl
HF_HOME=/workspaces/.cache/huggingface python3 "$probe/shared_kv_bench.py" --gen 64 --resident-executor "$probe/kv_baseline/qwen_graph" --host-executor "$probe/shared_kv/qwen_graph" --output bench/results/shared_kv_20261010.jsonl
```

All application execution remains in the original bpfusion-dev Workspace. Temporary adapters/binaries have this task as owner and are removed once inactive and no longer needed. Published results must cite raw timestamps and verified oracle outputs. No new service, scheduler, dependency, production flag or test framework is added.

## Qualification and diagnostic observations

Both strict modes passed their unchanged gen64/prompt-edge regression, including 5,000 empty connections, eight clients, reject-to-valid reuse, ring wrap, pipelining and half-close, network trace, expected launch counts, and clean module/pin teardown. [Resident raw](../../bench/results/qwen_shared_kv_correctness_20261010.txt) includes the exact candidate source; [host-control raw](../../bench/results/qwen_shared_kv_host_correctness_20261010.txt) records its command and complete result.

Sequential GPU-only event/profiler diagnostics capture all190 real graphs, warm10/replay30 at five shapes and do not execute TCP or GPU-tail dispatcher. The exact pinned-source wrapper is in both raw files: [baseline](../../bench/results/qwen_baseline_shared_kv_profile_20261010.txt), [shared KV](../../bench/results/qwen_shared_kv_shared_kv_profile_20261010.txt). These are correlated single-process samples, without randomized blocks or integrated clocks, and cannot establish end-to-end speed or causal energy.

| graph shape | baseline event mean ms | shared KV event mean ms | CUDA device events baseline/shared |
|---|---:|---:|---:|
| prefill5 | 2.602524 | 2.505630 | 1245 / 1197 |
| prefill64 | 3.117278 | 3.026666 | 1317 / 1269 |
| decode position16 | 2.711158 | 2.565685 | 1245 / 1149 |
| decode position64 | 2.738151 | 2.569326 | 1245 / 1149 |
| decode position126 | 2.758016 | 2.597180 | 1245 / 1149 |

Post-capture Torch-owned allocated bytes are 1,218,157,568 / 1,089,993,728 (baseline/shared), a 128,163,840-byte reduction; total GPU/native memory is not covered. Held last-position logits are identical57,735,680 bytes. CUDA device event counts include copies, not just CPU launches. These observations justify a real matched TCP comparison, not a serving improvement claim.

The exact temporary driver and its delta are preserved in [adapter raw](../../bench/results/shared_kv_adapter_20261010.txt). The original TTFT comparison direction is explicitly renamed candidate-minus-baseline; the planned primary TPOT/TPS analysis reports positive-as-improvement paired block differences and intervals.

## Plan review

Fresh read-only plan reviewer completed at 2026-10-10T18:35:00.590464+00:00. It found no scientific/executability blocker: source pinned, identical native resident library, correct prefix/mask/keepers, strict two-mode qualification, component-only delta and reasonable small code growth. It noted the dependency on serial KV ownership and that clients8 is closed-loop throughput rather than open-load capacity. Its identified primary-analysis gap was repaired before collection: temporary driver now outputs paired TPOT/TPS intervals and uses accurate TTFT labels. Reviewer conclusions remain in the retained task; no separately saved review report is claimed.

## Real preflight

The [preflight raw](../../bench/results/shared_kv_preflight_20261010.jsonl) and [stdout](../../bench/results/shared_kv_preflight_20261010.stdout.txt) record four measured exact gen1 requests per engine after eight gen1/gen64 warmups, normal one-launch shutdown, graph_error=0 and clean hook/pin teardown. This establishes executability only. The complete paired matrix then finished on the same frozen temporary driver and sources, as recorded below.

## Complete TCP result

The [full raw](../../bench/results/shared_kv_20261010.jsonl) and [stdout/analysis](../../bench/results/shared_kv_20261010.stdout.txt) completed at pinned capture base4b9e71a with 2,621 records: 40 cells, 2,560 exact requests, 83,200 exact measured tokens, ten independent process starts/normal shutdowns, and no failure. Each process records one resident service launch, 8,580 device model graphs, graph_error=0, 264 publications, zero registration/admission failures and eight final FREE slots. The doc-only qualification commit84c14c0 was published during this run; frozen capture/candidate/driver sources and native libraries did not change.

The table includes **all five paired blocks**, including the two much slower pairs. TPS means are the means of five cell rates, not pooled-window aggregate rates. A positive paired gain means baseline-minus-shared TPOT or shared-minus-baseline TPS. Intervals are nominal two-sided t95 (df4), conditional on this changing shared-GPU run; no familywise correction or stable isolated causal effect is claimed.

| gen64 / clients | primary metric | baseline mean | shared KV mean | paired gain | nominal t95 gain |
|---|---|---:|---:|---:|---|
| 64 / 1 | TPOT ms | 3.241723 | 3.079612 | +0.162111 | [-0.007227, +0.331449] |
| 64 / 1 | output tokens/s | 345.636143 | 359.578495 | +13.942352 | [+2.752351, +25.132354] |
| 64 / 8 | TPOT ms | 3.266693 | 3.039565 | +0.227128 | [+0.115352, +0.338903] |
| 64 / 8 | output tokens/s | 342.111621 | 368.069383 | +25.957763 | [+10.359470, +41.556056] |

Eight-client TPOT/TPS and single-client TPS support a benefit in this recorded paired comparison. Single-client TPOT is inconclusive: its interval crosses zero despite positive point estimates in every block. These are mixed, narrowly supporting results, not an overall architecture/optimized-serving win. Eight clients still queue behind serial requests. Their gen64 mean TTFT is 1378.944184 /1283.763196 ms, so the large queueing problem remains. Completion means are 208.180912 /197.782190 ms (clients1) and1584.745830 /1475.255804 ms (clients8).

## Shared environment and limits

Endpoint raw shows pairs0-2 at approximately2880-2910MHz SM,50-56C; pairs3-4 at2812-2835MHz,58-64C. Memory clock stays13801MHz. Gen64 throughput in **both** engines falls from around430-460 to214-229 tokens/s in the latter two pairs. Nothing was excluded or replaced by earlier findings' faster figures. The small SM-clock change alone does not establish the cause of a near2x slowdown.

[Post-run read-only diagnosis](../../bench/results/shared_kv_environment_20261010.txt) finds another Pod's SGLang scheduler with18,400MiB resident GPU memory. Host process start was18:38:31UTC, during collection; its cgroup matches the separate GPU-SMT candidate workload. The container-local compute-app query returned empty output, which does not prove an unoccupied host GPU. No other owner's process or service was interrupted. This establishes observed sharing and temporal change, not within-window activity or a causal explanation: no activity trace or integrated power/clock measurement was collected.

Alternating pairing and common slowdown allow a valid local observational comparison, but block stationarity/independence and co-tenant overlap are uncertain. Therefore nominal intervals must not become fixed isolated4%/8% causal speedup claims. No strong inference about default TCP buffering, open-load capacity, total-host cost, energy or an optimized external server follows. GPU-only profiles remain separate diagnostics.

## Independent result review and implementation

A fresh read-only result reviewer independently recomputed every request's oracle agreement, timestamps/TTFT/TPOT/completion, cell TPS, pairing/order, all primary t95 intervals, preflight, runtime counters and cleanup. It verified the exact pinned/candidate source, identical resident native library and its checked temporary TCP_NODELAY call, inherited cache mask/sequence semantics and lifetime, plus profile means/allocation/event counts and the shared-environment limitation.

Judgments: run **valid** within the recorded shared-GPU environment; hypothesis **narrowly supported with mixed results**; independent stable-GPU causal magnitude **inconclusive**; research value **supporting**; paper impact **mechanism/workload boundary**. It recommends retaining the small correct cache optimization and moving to batching rather than rerunning unchanged comparisons for prettier numbers. Net production growth is13 lines in the capture script, with no new framework, runtime helper, dependency, mode flag or test boilerplate. The existing serial ownership is essential; simultaneously live batched requests will require separate KV state.

The retained implementation is byte-for-byte the qualified temporary candidate. Production native transport and dispatcher are unchanged. Complete gen64/prompt-edge regressions against default native libraries passed: [resident](../../bench/results/qwen_shared_kv_default_resident_correctness_20261010.txt) and [host-control](../../bench/results/qwen_shared_kv_default_host_correctness_20261010.txt), each303 valid requests /19,392 exact tokens /259 rejects, 5,000 empty connections, eight clients, invalid-to-valid reuse, pipeline/ring wrap/half-close, expected launch counts, graph_error=0, all-thread network trace and clean teardown. These confirm production correctness; the serving performance table uses the explicitly documented common temporary TCP_NODELAY condition.
