# Integrated upstream-vLLM kernel-queue serving: independent result review

Reviewed after both complete runs reached terminal status on2026-10-12.
The review read original Workspace main, production adapters, canonical queue,
timed userspace transport, driver/analyzer, installed upstream graph/KV sources,
plan/review/startup repair, real preflight, full correctness traces, all archived
performance client/trace/reference/stdout/status files, journal/publication
receipts and cross-mode output agreement. Raw metrics were independently
reconstructed rather than accepting the orchestrator's readings. No model/
GPU workload, source/plan edit, process signal, Git publication, infrastructure
entity or extra agent was started. Only this requested review was written.

## Separate judgments

- run status: valid and complete for the predeclared instrumented two-model
  online serving/trajectory contract and matched transport component experiment.
- tested hypothesis: GPU/shared-queue autonomous optimized serving is supported;
  client latency/throughput superiority over the efficient same-backend
  userspace control is inconclusive. Every measured paired interval crosses0.
- research value: supporting engineering/mechanism evidence; the integration
  closes actual online prefill/batching/state/lifetime gaps. Failed startup
  and preflight are setup evidence, not separate scientific contributions.
- paper impact: additional engineering evidence and a mechanism/workload
  boundary. There is no paper RQ/thesis to answer or rewrite.
- next decision: retain this reusable optimized backend and its worker-free
  Linux request path. Do not claim a latency/throughput win or equivalence.
  Prioritize a new causal discriminator relevant to the full goal, rather than
  unchanged paired reruns or model-specific arithmetic tuning. Publication,
  final cleanup and any broader product/network acceptance remain root-owned.

No blocking scientific/execution defect was found for this stated scope.
This review does not declare the entire retained goal achieved.

## Authoritative paths and completeness

Plan: [vllm_server_plan_20261012.md](vllm_server_plan_20261012.md).
Review: [vllm_server_plan_review_20261012.md](vllm_server_plan_review_20261012.md).
Artifacts live in [vllm_server_20261012](vllm_server_20261012), including
qwen/smol_correctness.jsonl, qwen/smol_performance.jsonl, per-executor
.gpu.jsonl and .gpu.jsonl.references.jsonl, stdout, status and analyzer output.

Both original performance drivers and archived analyzer reruns have retained
exit0 receipts. Qwen terminal is21:14:52UTC; Smol terminal is21:20:17UTC.
I independently inspected both raw terminal records and all twenty executor
wait0 records. No complete-run verdict was issued from a live prefix.

For each model, independent reconstruction confirms40 unique
(pair,mode,gen,concurrency) cells,2560 measured requests,83200 measured tokens,
80 excluded/checked gen1 warmups and ten complete executors. Each executor
serves264 total requests/8328 tokens. Across models:80 cells,5120 measured
requests/166400 tokens; warmups add160 requests/tokens, not performance rows.
Every cell contains index0..63 once, with the four actual prompt arrays repeated
16 times each according to index%4. No failed, missing or excluded full-run cell
exists. Both mode orders alternate kernel/userspace in pairs0/2/4 and
userspace/kernel in1/3. Cell order is the same fixed matrix in every process,
as this actual plan/driver specifies; it is not a rotated cell-order experiment.

Every client timestamp metric was independently reconstructed. Arrival arrays
are sorted, begin after request start and contain exactly gen1/64 tokens.
TTFT=(firstarrival-start), completion=(lastarrival-start), and TPOT excludes
the first token. Cell rate is actual measured tokens over firstsend/lastarrival.
Stored values and first_ns/last_ns agree exactly with those calculations.

## Correctness and real Linux mechanism

The four full correctness executors (two models x two transports) each complete
622 requests:363 valid,259 explicit rejections and22224 generated tokens.
Independent CPU-side data reconstruction joined client_ns to admission input/
generation length, unique monotonic request IDs, every compute event and its
replay reference. All622 IDs occur once, every valid request prefills once,
each decode has a nonempty own history shorter than its requested output,
every compute has unique active IDs/batch length, and every generated token
equals both the saved independently replayed sequence and received client
sequence. Invalid requests have no compute output. No trace overflow occurs.

Actual correctness batches cover1..8, including non-power-of-two3/5/6/7.
Queries cover decode0 and prefill1/2/5/8/15/16/17/32/64. There are512 distinct
captured body/head shapes (64 lengths x eight batch counts) and520 descriptor
entries including eight query1 aliases for decode. Capture/warmup is not
independent numerical coverage for every possible prompt at all512 shapes;
only the real executed trajectory/workload coverage is claimed.

The protocol includes30 byte-fragmented requests across binary/HTTP and
prompt-edge lengths, explicit client concurrency1..8,256 invalid-then-valid
pairs on eight persistent clients,32 mixed gen1/gen64 requests with immediate
reuse, six ordered pipelined half-close responses, pipelined first/last-ID
rejections, binary invalid EOF and subsequent valid requests. Each executor
also accepts/drains5000 empty connections. Helper-thread-targeted SIGTERM
exercises actual shutdown. Client bodies/status/lengths and subsequent reuse
are checked, not merely server-side outputs.

I independently searched the preserved all-thread network traces after the
ready marker: kernel mode has no accept/recv/send family syscalls; userspace
mode actually has accept4,recvfrom and sendmsg. Kernel production host logic
after launching the parent graph only waits for stop/shutdown. GPU dispatch
handles new prompt admission, input/position/length/block metadata, prefill/
decode batches, official sampled tokens, completion and FIFO reclamation.
This is actual new-request serving, not CPU-prefilled finite GPU generation.
The same listener/module/eBPF ingress and kernel TCP TX lifecycle delivers
the validated client replies without a steady userspace network worker.

All native correctness exits report launches1,graph_error0,max_active8,
admitted622,retired622,trace_overflows0 and completed independent replay.
Kernel stats have zero admission/registration failures, llm_reserved0 and
eight final FREE slots. The host journal distinguishes the deliberate binary
invalid EOF: each correctness kernel lifecycle has621 completed and1 abandoned,
matching363 valid plus258 HTTP rejection responses and one binary EOF.
It is not zero-abandoned correctness, nor an unexplained failed valid reply.

For all ten performance kernel lifecycles, stats show264 publications,
zero admission/registration drops, reserved0/FREE8. Saved host journal has264
completed,0 abandoned,0 retries,54160 bytes and19 accepted/closed per lifecycle.
Successful bounded journal read has no listed fault matches. These receipts
support actual kernel delivery/recycle and cleanup in the recorded window;
they are not proof of arbitrary future availability or continuous isolation.

## Independence of trajectory replay

The native candidate and Python host-launch replay update metadata separately.
Replay starts with actual admitted/client prompts, reconstructs positions,
sequence lengths, query boundaries, padding, block table rows and slot maps
from its own per-request history, runs upstream body/head graphs on the host,
then appends its own sampled actual outputs. It compares against trace tokens
but never uses served trace tokens as the next model input. Thus candidate
metadata/state mistakes are not automatically copied into the reference.

The recorded batch membership/query schedule is a predeclared condition used
to compare the same FP16 computation trajectory, not an output-derived
replacement oracle. Independent audit additionally checks admission identity,
one prefill before decode, generation limits, all IDs and complete client
sequences, so an arbitrary trace cannot simply invent acceptance.

This is an independent metadata/state/trajectory execution reference using
the same upstream math, not an independent model-math or quality oracle.
Known eager-HF/official-server numerical disagreements remain separate
fidelity diagnostics. Passing replay cannot establish general eager-HF token
identity, equal task quality, all checkpoint shapes or mathematical equivalence.

## Reused optimized computation, repairs and source scope

The adapter uses official vLLM0.31.0, Torch2.13.0+cu129 and Transformers5.17.0
through ModelCudaGraphManager, the upstream model forward/FlashAttention2,
official compute_logits and temperature0 gumbel_sample. I inspected installed
manager capture/hidden-state ownership, block pool get_new_blocks/free_blocks
and reserved null block sources. Actual model logs confirm FA2, the real
bootstrap catalogue and full reference replay for both architectures.

The pinned models are Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775
and SmolLM2-135M revision93efa2f097d58c2a74874c7e644dbc9b0cee75a2.
The same checkpoint/dtype/graph/state/scheduling code is used by both
transports. No model/attention/argmax math is rewritten in this adapter.
It is a CUDA-graph catalogue of optimized upstream computation, not proof
that an entire model is a single CUDA megakernel.

Startup evidence is complete and retained: initial 512-shape capture reaches
native DeviceLaunch instantiation then exits1 with CUDA out-of-memory before
readiness/client work. The intermediate wrong GPUWorker import exits1 before
capture. The repaired real TCP/gen64 preflight exits0 and independently
replays its actual request. These failures are not performance wins or
discarded numerical observations.

The necessary repair binds existing queue context to128 tokens and derives
explicit cache bytes from actual upstream FullAttentionSpec page sizes:
65 allocator blocks (one null plus64 slot-owned), with16-token blocks.
Observed cache budgets are12779520 bytes Qwen and23961600 bytes Smol.
Official get_new_blocks owns the64 slot blocks through serving/replay and
free_blocks releases them after graph completion. Current metadata lengths
prevent stale tail KV from being consumed across reuse.

Worker.determine_available_memory's original explicit-byte path still runs
profile_run but skips the default available-memory sizing branch. This is
a disclosed explicit cache-budget bootstrap deviation, not unchanged default
memory profiling. max_model_len128 may affect attention specialization,
timing and FP16 output; historical default-context numbers are not transferred.
Fresh repaired service/replay evidence is used here for both transports.

The production addition is233 native plus167 Python lines; benchmark/analysis
are210 plus103 lines. Its scope is descriptor/input/KV/lifetime binding, GPU
request scheduling, real-protocol validation, bounded tracing and independent
replay. No model arithmetic, replacement attention/sampling implementation,
new infrastructure entity or experiment-control framework was added. The
code volume is commensurate with the demonstrated online binding; startup
cost and private upstream API coupling remain material maintenance limits.

The current adapter accepts its checked FullAttentionSpec/single-group/cache
and parallelism assumptions; two architectures are demonstrated. It does not
claim arbitrary vLLM model, hybrid/sliding/MoE/cache-layout support. Captured
shape ownership, device-launch compatibility and private upstream API coupling
are real engineering maintenance/coverage boundaries.

## Comparison fairness and output scope

This is a component comparison with efficient native userspace TCP,
not the official vLLM HTTP server or a strongest whole-serving competitor.
Userspace actually selects BF_USER_NETWORK_WAIT with epoll_pwait2 nominal
60000ns completion polling; its source/log/network activity engage that
intended control rather than substituting a busy-spin or broken path.
Kernel TX uses its existing polling behavior. Equal nominal lower waits
are not measured identical wake timing; their implementation difference
belongs to this component experiment.

Both transports use identical BF_TRACE, catalogue, same GPU batching policy,
checkpoint/fp16, reserved context/cache and client binary HTTP protocol.
Shared input/output buffers are serialized behind the parent tail join;
tensor batching comes from upstream batch shapes, not concurrent clobbering
of private manager state. Actual performance batches are1/2/3/4/8; all1..8
are exercised in correctness. Each performance executor has4536 decode graph
events and variable229-233 prefill graph events,4765-4769 total combined
body/head graph launches; each event's batch-weighted tokens sum to8328.
Actual dynamic arrival/batch trajectories are reported, not assumed identical.

Both archived performance sources equal current production/native/driver/client
bytes. Qwen metadata was emitted at earlier maina2ecf9c4, before integration
publication; Smol metadata identifiesacee1d3. This is source provenance,
not permission to pretend Qwen began at the later commit. Correctness Python
source differs only by removed unused heads/selected locals; native/client
source is identical. The raw snapshots permit inspection of that harmless
publication-time edit. No computation behavior or run oracle changed.

Independent same-pair/index/input cross-mode sequence agreement is:

| model | gen1/client1 | gen64/client1 | gen1/client8 | gen64/client8 |
|---|---:|---:|---:|---:|
|Qwen|320/320|320/320|312/320|278/320|
|Smol|320/320|320/320|320/320|290/320|

Qwen concurrent mismatches first occur at output0; Smol gen64/client8 first
mismatches occur at16. All remain in raw and each path matches its own
independently replayed trajectory. Same graphs/math/policy does not imply
same actual batch trajectory or same FP16 greedy sequence. Therefore no
identical-output superiority, general fidelity/quality equivalence or
perfect isolation of network cost is claimed. The valid timing scope is
the requested fixed-length service under the actual disclosed trajectories.

## Independent metric reconstruction

The following tables include every planned cell and mean/paired effect, with
320 measured requests per latency row and five aggregate cell TPS measurements.
TTFT/TPOT/completion are client arrival metrics. Positive gain favors kernel:
userspace-minus-kernel latency, kernel-minus-userspace throughput. Nominal
two-sided t95 uses five paired process-block means, sample standard deviation,
df4 and critical2.776445105. Individual requests are not independent trials.
P50/P99 are descriptive nearest-rank pooled320-request quantiles, matching the
actual analyzer definition. No robust-tail confidence or familywise claim
is made. Gen1 has no TPOT.

### Qwen2.5-0.5B-Instruct

| gen / clients | mode | TTFT ms | TPOT ms | completion ms | output tok/s | TTFT p50 / p99 ms |
|---|---|---:|---:|---:|---:|---:|
| 1 / 1 | kernel | 1.473674 | -- | 1.473674 | 670.055 | 1.461850 / 2.182450 |
| 1 / 1 | userspace | 1.432418 | -- | 1.432418 | 688.325 | 1.445880 / 1.569956 |
| 64 / 1 | kernel | 1.370063 | 1.226498 | 78.639424 | 813.545 | 1.363413 / 1.626678 |
| 64 / 1 | userspace | 1.331727 | 1.220235 | 78.206515 | 817.954 | 1.278892 / 1.616779 |
| 1 / 8 | kernel | 8.946219 | -- | 8.946219 | 884.466 | 9.701748 / 10.823910 |
| 1 / 8 | userspace | 8.800102 | -- | 8.800102 | 902.142 | 9.667602 / 9.961821 |
| 64 / 8 | kernel | 3.038542 | 1.726828 | 111.828683 | 4576.218 | 2.796077 / 5.459309 |
| 64 / 8 | userspace | 2.965979 | 1.706445 | 110.472027 | 4630.119 | 2.871178 / 5.042291 |

| gen / clients | gain metric | mean | nominal paired t95 |
|---|---|---:|---:|
| 1 / 1 | ttft_ms | -0.041256 | [-0.093513, 0.011001] |
| 1 / 1 | latency_ms | -0.041256 | [-0.093513, 0.011001] |
| 1 / 1 | output_tokens_per_s | -18.269966 | [-48.793163, 12.253232] |
| 64 / 1 | ttft_ms | -0.038336 | [-0.101286, 0.024614] |
| 64 / 1 | tpot_ms | -0.006263 | [-0.025325, 0.012799] |
| 64 / 1 | latency_ms | -0.432909 | [-1.693807, 0.827989] |
| 64 / 1 | output_tokens_per_s | -4.409695 | [-17.265125, 8.445736] |
| 1 / 8 | ttft_ms | -0.146117 | [-0.503230, 0.210997] |
| 1 / 8 | latency_ms | -0.146117 | [-0.503230, 0.210997] |
| 1 / 8 | output_tokens_per_s | -17.675637 | [-51.123026, 15.771751] |
| 64 / 8 | ttft_ms | -0.072563 | [-0.220128, 0.075003] |
| 64 / 8 | tpot_ms | -0.020382 | [-0.080631, 0.039867] |
| 64 / 8 | latency_ms | -1.356656 | [-5.266316, 2.553004] |
| 64 / 8 | output_tokens_per_s | -53.901104 | [-208.235786, 100.433577] |

Paired effects, in original pair0..4 order:

- 1/1 ttft_ms: [-0.053526, 0.006183, -0.083957, -0.075122, 0.000143].
- 1/1 latency_ms: [-0.053526, 0.006183, -0.083957, -0.075122, 0.000143].
- 1/1 output_tokens_per_s: [-22.723460, 10.423036, -43.080275, -39.874742, 3.905613].
- 64/1 ttft_ms: [-0.124989, -0.029177, -0.000502, -0.003166, -0.033847].
- 64/1 tpot_ms: [-0.033709, 0.001512, 0.000465, 0.000157, 0.000259].
- 64/1 latency_ms: [-2.248641, 0.066089, 0.028805, 0.006735, -0.017533].
- 64/1 output_tokens_per_s: [-22.921681, 0.692795, 0.284779, 0.065561, -0.169928].
- 1/8 ttft_ms: [-0.659729, 0.006769, -0.026686, -0.038290, -0.012647].
- 1/8 latency_ms: [-0.659729, 0.006769, -0.026686, -0.038290, -0.012647].
- 1/8 output_tokens_per_s: [-65.802779, -4.245223, -4.660536, -7.697855, -5.971794].
- 64/8 ttft_ms: [-0.237142, -0.077494, -0.117796, -0.011465, 0.081083].
- 64/8 tpot_ms: [-0.107080, -0.001822, 0.003884, 0.003228, -0.000122].
- 64/8 latency_ms: [-6.983207, -0.192288, 0.126910, 0.191901, 0.073405].
- 64/8 output_tokens_per_s: [-275.985358, -8.168634, 6.985604, 6.329039, 1.333827].

### SmolLM2-135M

| gen / clients | mode | TTFT ms | TPOT ms | completion ms | output tok/s | TTFT p50 / p99 ms |
|---|---|---:|---:|---:|---:|---:|
| 1 / 1 | kernel | 1.201405 | -- | 1.201405 | 821.367 | 1.188263 / 1.788058 |
| 1 / 1 | userspace | 1.222876 | -- | 1.222876 | 806.753 | 1.219575 / 1.470203 |
| 64 / 1 | kernel | 1.147084 | 0.720139 | 46.515819 | 1375.545 | 1.134250 / 1.607638 |
| 64 / 1 | userspace | 1.160655 | 0.720035 | 46.522839 | 1375.363 | 1.148612 / 1.456302 |
| 1 / 8 | kernel | 7.155260 | -- | 7.155260 | 1103.601 | 7.684312 / 8.687419 |
| 1 / 8 | userspace | 7.124197 | -- | 7.124197 | 1115.548 | 7.677381 / 8.667548 |
| 64 / 8 | kernel | 2.357515 | 1.479236 | 95.549386 | 5358.410 | 2.214422 / 4.063838 |
| 64 / 8 | userspace | 2.374469 | 1.477588 | 95.462511 | 5363.427 | 2.256875 / 4.304030 |

| gen / clients | gain metric | mean | nominal paired t95 |
|---|---|---:|---:|
| 1 / 1 | ttft_ms | 0.021471 | [-0.044829, 0.087771] |
| 1 / 1 | latency_ms | 0.021471 | [-0.044829, 0.087771] |
| 1 / 1 | output_tokens_per_s | 14.613823 | [-33.925534, 63.153179] |
| 64 / 1 | ttft_ms | 0.013571 | [-0.080954, 0.108096] |
| 64 / 1 | tpot_ms | -0.000104 | [-0.035550, 0.035342] |
| 64 / 1 | latency_ms | 0.007020 | [-2.318881, 2.332921] |
| 64 / 1 | output_tokens_per_s | 0.182046 | [-66.261641, 66.625732] |
| 1 / 8 | ttft_ms | -0.031062 | [-0.785074, 0.722949] |
| 1 / 8 | latency_ms | -0.031062 | [-0.785074, 0.722949] |
| 1 / 8 | output_tokens_per_s | -11.946418 | [-122.390755, 98.497919] |
| 64 / 8 | ttft_ms | 0.016954 | [-0.259524, 0.293432] |
| 64 / 8 | tpot_ms | -0.001648 | [-0.112180, 0.108884] |
| 64 / 8 | latency_ms | -0.086875 | [-7.314584, 7.140834] |
| 64 / 8 | output_tokens_per_s | -5.016982 | [-391.065270, 381.031306] |

Paired effects, in original pair0..4 order:

- 1/1 ttft_ms: [-0.039790, 0.008448, 0.027082, 0.106269, 0.005347].
- 1/1 latency_ms: [-0.039790, 0.008448, 0.027082, 0.106269, 0.005347].
- 1/1 output_tokens_per_s: [-34.666265, 5.529301, 19.541343, 74.117256, 8.547479].
- 64/1 ttft_ms: [0.023404, -0.098906, 0.112522, 0.033247, -0.002412].
- 64/1 tpot_ms: [0.000038, -0.039798, 0.040920, -0.000646, -0.001034].
- 64/1 latency_ms: [0.025812, -2.606157, 2.690467, -0.007458, -0.067566].
- 64/1 output_tokens_per_s: [0.764588, -74.359382, 76.939576, -0.307249, -2.127307].
- 1/8 ttft_ms: [0.018999, -0.878343, 0.829613, 0.014299, -0.139880].
- 1/8 latency_ms: [0.018999, -0.878343, 0.829613, 0.014299, -0.139880].
- 1/8 output_tokens_per_s: [-5.102941, -135.543879, 114.305922, -3.666377, -29.724816].
- 64/8 ttft_ms: [0.077793, -0.225972, 0.365638, -0.057674, -0.075014].
- 64/8 tpot_ms: [0.003422, -0.125054, 0.125782, 0.002835, -0.015225].
- 64/8 latency_ms: [0.293402, -8.104384, 8.289873, 0.120907, -1.034174].
- 64/8 output_tokens_per_s: [20.544083, -434.331540, 440.715487, 6.721805, -58.734743].

## Interpretation, exclusions and remaining limits

Every TTFT, throughput, TPOT and completion interval in both models crosses0.
Thus no local performance superiority is established, and no equivalence is
proved. This does not erase the independent online serving/correctness/
worker-removal result. Kernel mean gen64/eight-client results are Qwen4576.218
tok/s,TTFT3.038542ms,TPOT1.726828ms; Smol5358.410 tok/s,TTFT2.357515ms,
TPOT1.479236ms. Smol1.201405/1.222876ms are gen1/client1 TTFT values,
not its primary concurrent gen64 TTFT.

Qwen pair0 has larger unfavorable deltas in several cells and Smol pairs1/2
move in opposite directions; no pair was removed. Fixed cell order, adjacent
paired processes, warm compile caches, four repeated short prompts and only
five process blocks limit inference. These runs do not include total process/
kernel CPU accounting, energy, text/tokenization/OpenAI JSON, long-context
capacity, larger models, arbitrary cache types, production load/tails or
physical-NIC measurements. No CPU or energy saving number follows from the
absence of host network syscalls. Equal tracing overhead is disclosed;
timing is not silently transferred to an untraced production claim.

The mainline implementation/qualification publication receipt has HTTP200
and byte matches for the actual integration files atacee1d3; complete new
performance/review documentation is still the root's publication responsibility.
Root also owns final original-Pod/process/module/pin checks and temporary
apparatus cleanup. Workspace/PVC/session and untracked tools/setup_env.sh
remain preserved. This review requires no new service, controller, schedule,
configuration gate or model-math optimization.

The next useful discriminator should change the actual uncertainty: broader
request-path conditions or meaningful optimized-backend integration/ownership
coverage under the retained goal. An unchanged inconclusive rerun is not a
new scientific contribution, and optional broader work is not permission to
rewrite this experiment's contract or discard its negative/inconclusive rows.
