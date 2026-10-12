# Official optimized serving comparison

On this finite Qwen2.5-0.5B token-ID workload, the current BPFusion frontend
has lower first-token latency, while official optimized vLLM has substantially
higher eight-client long-output throughput. This completed comparison bounds
the current implementation and selects the next compute-reuse work. Different
computation, output sequences and wire interfaces prevent attributing the
differences to eBPF or claiming identical-output superiority.

## Conditions and completion

Frozen production source is 442ab452b38680fb4bd6aa58ff21b7ab68be4d31.
The benchmark/preflight publication 85c77fa during collection changes no
executor, BPF, module, test or native request computation. The actual driver
and production sources are embedded in full raw metadata.

Original bpfusion-dev Workspace, lab RTX 5090, persistent loopback connections,
four fixed prompts of 2/5/8 tokens, gen1/64 and concurrency 1/8.
Each of five alternating process pairs rotates the four cell conditions and
measures 64 requests/cell after eight declared warmups/process.
Complete raw has 2706 rows, 40 cells, 2560 measured requests, 83200 output tokens
and 80 warmups. No full-run failure, selected exclusion or retry occurs.
Ten launching parents return wait exit 0; complete replay analysis exits 0.
The detached collection wrapper's own wait status was not retained.

The strongest external competitor is official vLLM 0.31.0 with its default
optimized scheduler/kernels/caches/graphs, token-only HTTP and FP16 weights.
Its temporary environment uses Torch 2.13.0+cu129/Transformers 5.17.0; BPFusion
retains Torch 2.14.1+cu130/Transformers 5.19.0. Actual safetensors/export comparison
covers 290 parameters / 494032768 FP16 elements, bit-identical for the frozen
checkpoint 7ae557604adf67be50417f59c2c2f167def9a775.

BPFusion reuses eight independent HF graph/KV banks and binary-token HTTP
responses. vLLM uses its compiled model/attention/batching and JSON/SSE token-ID
responses. These are different complete implementations, not a same-backend
control-path ablation. Token IDs are counted, not text chunks or SSE frames.
Explicit greedy/max-token/no-EOS settings are verified through the installed
token-only API; no tokenizer/chat-template work is added.

Official command:
`TEMP/venv/bin/vllm serve MODEL --tokens-only --dtype half --host 127.0.0.1 --port 39404`.
An ephemeral environment-only API key protects requests. The recorded missing/
invalid-key checks return 401; no key values enter artifacts.
No utilization override or eager fallback is used.

## Client results

Means are arithmetic means of five process-block means. Gain is BPFusion-minus-
vLLM for throughput, and vLLM-minus-BPFusion for latency. Intervals are separate
nominal paired two-sided t95 with df4, without multiplicity adjustment.

| gen64 primary metric | Clients | BPFusion | vLLM | Gain | Nominal t95 gain |
|---|---:|---:|---:|---:|---|
| Output tokens/s | 1 | 566.153 | 536.485 | +29.667 | [12.636,46.699] |
| TTFT, ms | 1 | 2.184801 | 8.953710 | +6.768909 | [5.644424,7.893394] |
| TPOT, ms | 1 | 1.759397 | 1.749842 | -0.009555 | [-0.054305,0.035195] |
| Output tokens/s | 8 | 1407.718 | 4713.694 | -3305.976 | [-3920.097,-2691.855] |
| TTFT, ms | 8 | 10.067280 | 14.845462 | +4.778182 | [0.461273,9.095091] |
| TPOT, ms | 8 | 5.592549 | 1.501113 | -4.091435 | [-4.315847,-3.867023] |

Secondary gen1/client1 TTFT is 2.263094 versus 7.028931ms,
gain 4.765836[2.811999,6.719674]ms. Gen1/client8 TTFT is 14.957079 versus
16.814639 ms, gain 1.857560[-1.494740,5.209861]ms; that interval contains zero.

All five long-output/eight-client pairs favor vLLM throughput and TPOT.
The fifth vLLM block is slower than the first four and is retained.
This is a mixed performance boundary: lower observed first-token time does not
imply higher sustained throughput. It motivates investigating reused optimized
batching/compute; the comparison does not isolate batching as the sole cause.

## Output agreement and baseline engagement

All 1280 BPFusion measured sequences equal the independent frozen eager HF
reference. vLLM matches 838/1280 full sequences:320/320 at gen1/c1,80/320 at
gen64/c1,277/320 at gen1/c8 and161/320 at gen64/c8. Every returned vocabulary
ID, requested length, prompt identity and stream completion is retained.
Different optimized floating-point computation can change greedy trajectories;
reference disagreement alone is not a task-quality verdict. No oracle,
precision or suffix was changed to manufacture agreement.

These output differences rule out an identical-output superiority claim.
The recorded fixed-length client observations remain useful for choosing the
next implementation, with this limitation visible.

All five vLLM logs engage FlashAttention2, VLLM_COMPILE and FULL_AND_PIECEWISE
CUDA graphs. Chunked prefill and prefix caching remain enabled; printed prefix
hit rate is0%. The actual async-scheduling selection is not established here.
There is no deliberately serial, slow-Python or eager-only competitor.
BPFusion final logs each show one host launch, 8580 device model launches,
graph_error=0, eight banks and max_active=8.

## Costs, shutdown and scope

All 50 active/idle CPU read brackets reconstruct at 100 Hz. For gen64/c8,
owned process-group CPU averages 62.5 us/request for BPFusion and 15531.25 us/request
for vLLM. The sum excludes kernel TCP TX, RX/softirq/BPF, driver, client and
other host work. BPFusion's zero accounting ticks in some cells do not mean
zero work. These values cannot establish total service CPU/energy savings.
The planned descriptive p50/p99 and warm-start/idle metrics are in the
secondary analysis; pooled finite-request percentiles are not a production
tail or population confidence interval.

Preflight attempt1 fails before requests because FlashInfer JIT cannot find
the already-installed ninja executable. Exposing the existing venv/bin only
to the vLLM child repairs its normal launch environment. Attempt2 completes
eight cells/64 measured requests/2080 measured tokens, plus 520 warmup tokens.
The historical plan review's1040-total/780-graph numbers are arithmetic errors:
1040 measured tokens belong to each method, and BPFusion launches1300 model
graphs. Full collection uses the same corrected path and unchanged workload.

Shutdown logs matter: official vLLM force-kills remaining EngineCore children;
BPFusion records Torch SubprocPool unclean-exit warnings. Parent wait codes0
do not prove all child exits were graceful or zero. The adapter's own timeout
SIGKILL path is not observed. Original groups are cleared; no requests are
discarded by these after-collection shutdowns.

The host journal read18:50-19:12UTC records one preflight TX exit8360 bytes /
40 completions and five full TX exits each 55176 bytes /264 completions,
zero abandoned/retries and 19 accepted/closed sockets. No matching fault line
appears in that bounded read; it does not prove continuous interference-free
execution. GPU endpoints/clocks are observations, not exclusivity or isolated
bandwidth evidence. Warm caches, shared-host conditions, short repeated prompts,
closed-loop load, unequal libraries/compute/KV capacity and wire formats bound
the result. No physical-NIC, full text/API, arbitrary-model or SOTA claim follows.

## Reproduction and next decision

Use the [reviewed plan](../../bench/results/qwen_vllm_plan_20261012.md) and
[plan review](../../bench/results/qwen_vllm_plan_review_20261012.md), with
[actual comparator](../../bench/results/qwen_vllm_compare_20261012.py),
[weight equality](../../bench/results/qwen_vllm_weight_match_20261012.json) and
[installed official protocol sources](../../bench/results/qwen_vllm_protocol_sources_20261012.json).

- [Failed default preflight](../../bench/results/qwen_vllm_preflight_default_20261012.jsonl)
  and [successful path-repaired preflight](../../bench/results/qwen_vllm_preflight_path_20261012.jsonl).
- [Complete raw](../../bench/results/qwen_vllm_20261012.jsonl),
  [collection stdout](../../bench/results/qwen_vllm_20261012.stdout.txt)
  and [primary replay output](../../bench/results/qwen_vllm_analysis_20261012.txt).
- [Secondary replay](../../bench/results/qwen_vllm_secondary_20261012.py)
  and [output](../../bench/results/qwen_vllm_secondary_20261012.txt).
- [Fresh result review](../../bench/results/qwen_vllm_result_review_20261012.md),
  [shutdown evidence](../../bench/results/qwen_vllm_shutdown_20261012.json)
  and [restoration](../../bench/results/qwen_vllm_restoration_20261012.json).

Full command:
`HF_HOME=/workspaces/.cache/huggingface python3 TEMP/compare_current.py --output bench/results/qwen_vllm_20261012.jsonl`.
Replay primary metrics using the archived comparator's `--analyze --output`
arguments; replay descriptive secondary metrics with its linked script.
The comparator retains the original TEMP path for reconstruction. Recreate
the pinned temporary environment as documented, select a new output filename
and never overwrite archived evidence.

Run status: valid and complete. Hypothesis: mixed within this workload and
comparison scope. Research value: supporting engineering evidence.
Paper impact: current implementation/workload boundary; no paper RQ is invented.
Close this matrix without unchanged repeats. Qualify reuse of an optimized
compute/batching interface, then compare kernel/eBPF and efficient userspace
control using that identical backend. Neither this external comparison nor
the earlier inconclusive same-compute matrix proves an eBPF speedup.
The temporary environment/source apparatus is removed after archiving and
review; own processes/module/pins are absent and successful nvidia-smi is
empty. Original Workspace/PVC/cache and unrelated tools/setup_env.sh remain.
The full retained performance and serving objective remains open.
