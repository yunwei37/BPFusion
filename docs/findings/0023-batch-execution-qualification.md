# 0023: batch execution qualification

## Why qualify computation before implementing batching

Finding0022 removes repeated KV prefix work but leaves serial requests and large eight-client queueing. The next service work is concurrent/batched execution without a steady host request worker, with independent KV ownership and the same exact eager-fp16 oracle. These are engineering qualification probes, not standalone research or serving-speed results.

## Ordinary HF batch-shape candidate

The [complete raw](../../bench/results/qwen_batch_shape_qualification_20261010.txt) includes the exact temporary script, source commit97a5f74, installed versions, independent batch1 eager-HF oracle sequences, command and all actual outputs. It uses the original exported weights through load_model, eager attention, fp16, last-position logits and ordinary HF DynamicCache. It does not run TCP, the native dispatcher or a resident service. Its host-driven calls are a diagnostic, not the final worker-free path.

The full matrix uses batch2/4/8, each of the ten gen64 correctness/prompt-edge cases replicated across lanes, plus a same-prefix-length mixed batch of the real France/greeting prompts. Every lane owns its own KV state in the HF batch. All33 groups completed and produced9,856 tokens;26 groups pass and7 fail exact oracle agreement. Exit0 means the diagnostic matrix completed, **not** that the candidate passed. No group was omitted after a mismatch.

| batch | failing group | first divergent zero-based output | expected / actual |
|---|---|---:|---:|
| 2 | greeting (case2), mixed5 greeting lanes | 62 | 323 /11 |
| 4 | arithmetic (case1) | 20 | 5145 /64547 |
| 4 | one-token prompt edge (case4) | 31 | 36277 /7010 |
| 8 | greeting (case2), mixed5 greeting lanes | 62 | 323 /11 |
| 8 | one-token prompt edge (case4) | 31 | 36277 /7010 |

The tested batch-shape change diverges under the fixed strict oracle. This does not establish that ordinary HF batching is generally wrong or isolate which arithmetic/dispatch difference causes divergence. The oracle and precision standard are unchanged; no tensor-batched production change is retained, and no latency/throughput figure is reported from this probe.

## Independent batch1 graph-bank qualification

The alternative keeps each request's qualified batch1 calculation shapes and private input/KV/output tensors while sharing read-only model weights. A GPU dispatcher launches each bank's selected model graph with CUDA FireAndForget, then tail-launches itself to sample outputs and feed the next decode step. CUDA's [device graph execution environments](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html) include child work: the parent tail waits for the whole environment, including the fire-and-forget children. This is a GPU-controlled fork/join route, not evidence that model kernels actually overlap.

The [temporary native build raw](../../bench/results/qwen_graph_bank_build_20261010.txt) preserves the exact addon, Makefile command and output at source2062f44. The addon was appended only for its temporary build; production native source was restored unchanged. Each raw below contains the exact wrapper and independent batch1 oracle outputs. Captured graphs and all tensor keepers remain alive through native graph-exec destruction. The first [bank2 attempt](../../bench/results/qwen_graph_bank2_qualification_20261010.txt) completed its first128 model graphs with zero GPU error, then failed while printing because json was absent from exec globals. That failed attempt is retained and is not a completed qualification. The repair adds only json to those globals; capture, scheduler, oracle and evaluation are unchanged.

| private banks | groups passing / completed | exact output tokens | model graphs per job | host launches per job |
|---:|---:|---:|---:|---:|
| [2](../../bench/results/qwen_graph_bank2_qualified_20261010.txt) | 12 /12 | 1,536 | 128 | 1 |
| [4](../../bench/results/qwen_graph_bank4_qualified_20261010.txt) | 12 /12 | 3,072 | 256 | 1 |
| [8](../../bench/results/qwen_graph_bank8_qualified_20261010.txt) | 12 /12 | 6,144 | 512 | 1 |

Each bank-count matrix includes all ten gen64 correctness/prompt-edge cases replicated across banks, a mixed France/greeting group, and a mixed-prompt-length group. All36 groups complete with exact agreement on10,752 tokens; all36 native markers report error=0 and one host launch per whole job, with no per-decode host model calls. These are engineering qualifications, not serving benchmarks: there is no TCP/shared BPF queue/module execution, latency measurement or demonstrated kernel overlap. At this GPU-only stage the production service remained serial.

## Real TCP private-bank integration

The default resident graph executor now discovers bank count from the existing BF_LLM_SLOTS authority and captures a private input/KV/output graph bank per physical request slot. Model weights remain shared and each model computation is still batch1 eager fp16. The GPU admits published requests in ring order, advances active requests through FireAndForget graphs, and samples only after the parent tail joins all child work. Requests can complete computation out of order. DONE publication follows admission order and waits until kernel TX has released the previous DONE before publishing the next one; FREE or already reused WRITING/PENDING proves that release. This preserves the existing producer's head-indexed reservation without a page ABI, producer or module change. The module continues withholding the final token while the GPU owns PENDING. Private banks remain alive through native graph-exec destruction.

The [resident real TCP strict raw](../../bench/results/qwen_queue_banks_resident_mixed_correctness_20261010.txt) passes335 valid requests /20,432 exact tokens /259 rejects,5,000 empty connections, eight clients, invalid-to-valid reuse, persistent ring wrap, a new32-request mixed gen1/gen64 reuse check, ordered pipeline and half-close. It reports one host launch,20,432 device model graphs,error=0,banks=8,max_active=8,zero admission/registration drops and all slots FREE at shutdown. The all-thread network trace contains no accept/receive/send calls after ready. This qualifies actual queue/TCP ownership and computation, not kernel overlap or serving speed.

The initial [startup-only run](../../bench/results/qwen_queue_banks_resident_correctness_20261010.txt) exceeded the inherited sixty-second readiness wait while capturing eight banks. No requests were published and no module loaded; it is retained as a failed setup attempt. Readiness now follows ready or process exit; the independent oracle and request/shutdown timeouts are unchanged. More capture work and memory are real costs, excluded from steady-state timings and reported separately where measured.

The serial host-launch correctness control captures one bank and returns after one whole request. Its first [mixed strict run](../../bench/results/qwen_queue_banks_host_mixed_correctness_20261010.txt) failed: each parent-tail iteration admitted another queued request while the current one was unfinished, so two physical slots shared bank0 (max_active=2,graph_error=1) and clients timed out. The sole correction requires seen==retired before admission when once=true. This does not change the resident once=false path. The [corrected host raw](../../bench/results/qwen_queue_banks_host_mixed_corrected_20261010.txt) passes the same335 requests /20,432 exact tokens /259 rejects and all lifecycle/trace checks, with594 host launches,20,432 model graphs,error=0,banks=1,max_active=1,zero admission/registration drops and eight FREE slots. The failed raw remains a failure. Resident qualification predates this once-only guard; the reviewed false branch has unchanged behavior.

This implementation permits concurrent request progression with separate batch1 calculations. At this correctness milestone, tensor batching, measured simultaneous kernel overlap, serving benefit, text processing and physical-NIC coverage remained separate open requirements. The completed component comparison below now measures serving benefit in its specified shared-GPU setting.



## Real TCP concurrency comparison plan

There is no paper RQ/thesis in this repository. This is a supporting engineering comparison for the user's throughput/latency objective: does admitting and progressing independent batch1 graph banks reduce eight-client gen64 queueing/TTFT and increase total output-token throughput against the current serial resident service? Finding0022 already establishes serial queueing; GPU-only qualification cannot answer the real-client question. The strongest next comparison changes that serving mechanism. Repeating dispatch or KV-only ablations would not answer it.

Baseline is the serial resident service at2062f44 (same code as10ad405, whose change is records only), including the accepted shared-KV append and last-position logits. Candidate is the qualified real TCP bank executor: private inputs/KV/outputs for the existing eight ring slots, GPU FireAndForget children followed by parent tail sampling, FIFO DONE publication with previous kernel reclamation acknowledged before the next DONE. Producer, page ABI, kernel module, weights, eager fp16 math, strict independent batch1 oracle and request transport remain unchanged. Both engines use one host service launch. The serial engine is a current-practice/component comparator, not an external SOTA baseline. The serial host-launch control is correctness coverage, not part of this concurrency comparison.

Use the existing bench/resident_dispatch.py protocol through its previous shared-KV temporary adapter, renamed serial/banks. Both temporary native libraries enable the same checked listener TCP_NODELAY call used in finding0022; production default transport is unchanged. Record exact sources, native build command and adapter delta. The bank startup exceeded the old sixty-second capture wait before requests; readiness now follows ready or process exit, with capture excluded from measurement and original request/shutdown timeouts retained. Record that deviation before collection.

Matrix: four real prompts, gen1/gen64, clients1/8, five paired process blocks with alternating engine order and rotating matching cell order,64 requests per cell (16 per prompt), eight excluded warmups per process, one-second idle samples separate from active cells. Full collection is40 cells,2,560 requests,83,200 measured output tokens and ten independent process starts/shutdowns. Preflight reuses the driver's gen1/client1/four-request cell for each engine; it establishes executability only. Connection/thread/barrier creation, model loading and capture precede timing/CPU windows. Record bootstrap duration separately for its larger bank-capture cost.

[NVIDIA metrics](https://docs.nvidia.com/nim/benchmarking/llm/metrics) define primary gen64/clients8 total output TPS over first-send/last-arrival, and request TTFT from send to first complete token. Report five paired block differences and nominal two-sided t95 intervals (df4): banks-minus-serial for TPS, serial-minus-banks for latency. Co-primary effects are assessed separately; a positive one with an inconclusive other is mixed support, while a clear tradeoff is reported as such. TPOT=(last-first)/63 and completion latency, single-client effects, gen1, executor-process CPU and idle CPU remain reported diagnostics/tradeoffs, not silent vetoes. Multiple tokens completed in one recv share its arrival timestamp; no weighted score or familywise correction.

Positive eight-client effects support retaining this serving path; negative/inconclusive effects bound its benefit and direct the next implementation toward measured compute/queueing overhead. All requests must match the independent oracle, counts must match, both service launch counts must be one, graph/admission errors must be zero, final slots must be FREE and test hooks/module/pins must clean up. The native max_active marker can prove multiple graph requests in flight, not simultaneous kernel overlap. Retain every paired block and any failed run. No compiler/precision/oracle changes or post-hoc sample removal.

Shared GPU: another project's SGLang workload was observed in finding0022. Preserve it. Record GPU clocks/temperature/power/utilization before/after each cell and current host process residency before/after the run through existing diagnosis paths. These are coarse observations, not an activity trace or isolation proof. Alternating pairs limit but do not eliminate temporal confounding; inference is local to this shared-GPU run, with no fixed isolated speedup, energy, open-load capacity, physical-NIC or optimized-serving claim.

Command after qualification/build/plan review: HF_HOME=/workspaces/.cache/huggingface python3 /tmp/<owned-queue-bank-directory>/queue_banks_bench.py --gen 64 --output bench/results/queue_banks_20261010.jsonl --resident-executor /tmp/<owned-queue-bank-directory>/serial/qwen_graph --host-executor /tmp/<owned-queue-bank-directory>/banks/qwen_graph. Add --preflight with its own output path for setup. The exact instantiated command, paths and script are retained in raw artifacts. Final table reports both primary effects with all paired blocks plus the TPOT/single-client tradeoffs. Plan and result reviews are read-only chat verdicts recorded here; no separate saved report is claimed.

Fresh read-only plan review admitted this comparison on the corrected source and exact temporary build/adapter. It verified the new decision value, matched serial comparator, metric signs/counts, private-bank lifetimes, FIFO reclamation and small production growth. The failed host run and applied once-mode guard were explicitly reviewed; finish its qualification and real preflight before full collection. The inherited primary_metric output label was renamed metric before collection; interpretation follows the declared TPS/TTFT co-primary plan, with TPOT diagnostic. Completion latency must be aggregated from stored request timestamps in the final results. No separate saved review report is claimed.

Real preflight completed on source41e5fc4: [raw](../../bench/results/queue_banks_preflight_ready_20261010.jsonl) /[stdout](../../bench/results/queue_banks_preflight_ready_20261010.stdout.txt),15 records/eight exact measured gen1 requests, two normal process shutdowns, each12 publications/264 model graphs/one host launch/error0/zero drops/eight FREE slots and cleanup. The [first preflight](../../bench/results/queue_banks_preflight_20261010.jsonl) /[stdout](../../bench/results/queue_banks_preflight_20261010.stdout.txt) failed at Popen because frozen Python source copies lacked executable mode, before any request/service launch. Restore executable mode on those owned temporary copies only; source bytes, oracle and timing unchanged. Both attempts remain retained. Preflight is executability evidence, not a serving result.


## Complete TCP concurrency result

The [full raw](../../bench/results/queue_banks_20261010.jsonl) and
[stdout](../../bench/results/queue_banks_20261010.stdout.txt) finish normally
with EXIT0 at source41e5fc4: 2,621 records, 40 cells, 2,560 requests,
83,200 exact measured output tokens, and ten independent executor starts and
normal exits. Every executor records one host service launch, 8,580 device
model graphs, graph_error=0, 264 publications, zero admission/registration
failures, and eight final FREE slots. All five candidate processes report
banks=8,max_active=8. All five pairs are retained; no failed full-run cell or
post-hoc exclusion occurred.

The [supplementary analysis](../../bench/results/queue_banks_analysis_20261010.txt)
includes its exact script and recomputes oracle agreement, every timestamp
metric, the first-send/last-arrival TPS denominator, prompt balance, process
order, counters and the intervals below. Its first checker mistakenly equated
the stored barrier/future CPU window with the TPS window and failed. Reading
the inherited cell() shows these are intentionally different; the corrected
checker verifies containment and independently recomputes TPS from request
timestamps. Both checker attempts remain visible. Measurement, original
metrics, oracle, timeout, source and all samples are unchanged.

Means are arithmetic means of five paired block values; TPS is the mean of
five cell rates, not a pooled rate. A positive gain means banks-minus-serial
TPS, or serial-minus-banks latency. Intervals are nominal two-sided t95, df4,
conditional on this shared-GPU collection; they have no familywise adjustment
and do not establish an isolated causal magnitude.

| gen64 / eight clients | serial mean | private-bank mean | paired gain | nominal t95 gain |
|---|---:|---:|---:|---|
| **Primary: total output tokens/s** | 230.344378 | 595.069687 | +364.725310 | [+361.080986, +368.369634] |
| **Primary: TTFT ms** | 1829.276558 | 23.656817 | +1805.619741 | [+1789.658322, +1821.581160] |
| Completion ms | 2102.076239 | 857.127669 | +1244.948570 | [+1226.924977, +1262.972163] |
| TPOT ms | 4.330154 | 13.229696 | -8.899542 | [-8.977403, -8.821682] |

Both primary effects are positive in every pair, with nominal intervals above
zero. Mean throughput is 2.58339 times the serial comparator; mean completion
latency falls by about59.2%. However, per-request TPOT increases by about3.06
times. Independent request progression removes waiting behind whole serial
requests and improves aggregate throughput/completion at this concurrency,
while each active request emits subsequent tokens more slowly. This is a
measured tradeoff, not an across-the-board latency improvement. max_active=8
still does not demonstrate simultaneous model-kernel overlap.

| paired block | TPS gain tokens/s | TTFT reduction ms | completion reduction ms | TPOT reduction ms |
|---:|---:|---:|---:|---:|
| 0 | +367.147928 | +1808.813123 | +1251.860902 | -8.840511 |
| 1 | +367.368739 | +1822.292134 | +1264.922017 | -8.847145 |
| 2 | +360.840590 | +1811.665708 | +1245.955405 | -8.979529 |
| 3 | +365.839352 | +1792.134424 | +1232.746949 | -8.879166 |
| 4 | +362.429940 | +1793.193316 | +1229.257578 | -8.951361 |

## Diagnostics and implementation costs

Single-client gen64 effects are inconclusive; none of these intervals excludes
zero. The new scheduling mechanism does not establish faster individual model
computation.

| gen64 / one client | serial mean | private-bank mean | nominal t95 gain |
|---|---:|---:|---|
| Output tokens/s | 229.598173 | 229.462857 | [-2.295026, +2.024394] |
| TTFT ms | 5.441970 | 5.438350 | [-0.248967, +0.256208] |
| TPOT ms | 4.337837 | 4.340241 | [-0.042568, +0.037761] |
| Completion ms | 278.725727 | 278.873535 | [-2.782383, +2.486768] |

| gen1 / clients | metric | serial mean | private-bank mean | nominal t95 gain |
|---|---|---:|---:|---|
| 1 | Output tokens/s | 187.022402 | 184.215714 | [-8.629934, +3.016558] |
| 1 | TTFT/completion ms | 5.330338 | 5.410282 | [-0.244871, +0.084983] |
| 8 | Output tokens/s | 198.996008 | 214.925069 | [+13.245113, +18.613007] |
| 8 | TTFT/completion ms | 37.989774 | 36.986667 | [+0.591449, +1.414763] |

One-token/eight-client means improve modestly, while single-client effects
remain inconclusive. Gen1 has no TPOT. Per-request p99 figures in stdout are
pooled descriptive statistics, not independent block-level tail estimates;
for example gen1/eight-client TTFT p99 rises from41.036071 to45.770807ms despite
the mean reduction. No general tail-latency guarantee follows.

Five bootstrap durations average10.312394s serial versus54.058607s private
banks, with ranges[10.250398,10.401339] and[54.015439,54.108346]s. Loading,
capture, native graph instantiation and readiness are included in this startup
measurement and excluded from steady-state cells. Capturing and instantiating
private graphs is a substantial startup cost.

Across the20 active cells per engine, executor-process CPU totals are0.13s
serial and0.08s private banks, at100Hz/0.01s accounting resolution. Each
engine's five one-second idle samples total0.01s CPU. These coarse values
support sleeping-host behavior; they do not establish zero CPU work, a precise
CPU saving, total host/kernel cost or energy efficiency.

## Shared environment, cleanup and interpretation

[Host residency snapshots](../../bench/results/queue_banks_environment_20261010.txt)
record a separate SGLang scheduler with18,402MiB GPU memory before, during and
after this run. The active-run snapshot also attributes python processes with
13,038MiB and652MiB to this BPFusion container; total GPU memory is32,127MiB.
This is a coarse residency observation, not a measured peak, an isolated
allocation delta, or a before/after serial-versus-bank memory comparison. The
larger graph footprint is a practical concern on this32GiB device. No other
owner was stopped or modified. Per-cell clocks/temperature/power/utilization
are retained in raw; their endpoints do not establish within-window co-tenant
activity, energy use, or causal isolation.

Post-run diagnosis at2026-10-10T19:46:16UTC finds only the same SGLang GPU
process; this task's executor/benchmark GPU processes have exited. The boot ID
is unchanged. The kernel module and bpfusion pins are absent, and every driver
cleanup call returned successfully; final eight FREE slots were observed before
detaching. Cleanup is recorded in the supplementary analysis and environment
raw. The retained original Workspace, PVC and unrelated setup_env.sh are
preserved.

The five paired blocks support retaining concurrent request progression for
this closed-loop workload and this shared RTX5090 collection. The result is a
supporting engineering comparison against the previous serial resident path,
not an optimized external-serving win. Default-transport correctness is
separately qualified above; the performance table uses the documented common
temporary TCP_NODELAY setting. Fixed isolated speedup, physical-NIC behavior,
open-load capacity, total-host cost, energy, text serving and competitive
serving remain unproven. Historical findings have their own environments and
must not be compared as a longitudinal speed curve.


## Independent result review

A fresh read-only result reviewer independently recomputed oracle agreement,
all request metrics, cell TPS, balanced prompts, rotating cell/process order,
all five-pair t95 intervals, preflight/failures, runtime counters and cleanup.
It checked frozen sources against their reported commits, the common temporary
transport delta, private-bank ownership and parent-tail lifetime semantics,
and the shared-GPU interpretation. Its verdict is valid and supporting for
this recorded component/workload comparison, with no publication blocker.
Both primary improvements and the TPOT/startup/memory costs remain explicit;
no separately saved reviewer report is claimed.

The implementation commit has net30 production lines and net13 test lines
(17 test additions /4 deletions). This result milestone adds only necessary
raw evidence and paragraph-level documentation; no production helper, mode
flag, dependency, framework, queue ABI or kernel module change. The next
engineering decision is to target model/Graph execution costs that still
limit single-request TPOT and make concurrent requests emit more slowly,
while retaining the unchanged strict oracle. Repeating the closed KV or
dispatch comparisons would not resolve that uncertainty.
