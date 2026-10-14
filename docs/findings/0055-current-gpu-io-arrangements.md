# Current GPU I/O arrangements with identical reused model computation

The current standalone resident GPU I/O path recovers SmolLM2-135M long-output
throughput relative to the current coalesced path, but remains below efficient
native userspace TCP. Qwen2.5-0.5B throughput recovery is inconclusive and its
concurrent short-output latency worsens relative to coalesced. This source-neutral
experiment supports a workload-specific choice between existing constructors,
not a universal advantage from removing userspace request handling.

## Question and fixed comparison

The retained objective is the Linux TCP/HTTP + eBPF/sockmap -> shared queue ->
resident real-model GPU -> asynchronous kernel TCP reply path, improving latency
and throughput while reusing model computation and eliminating a steady userspace
request worker. This is supporting evidence for that question, not new model
arithmetic, a new formal paper RQ or a complete general-purpose serving system.

Recent coalesced refinements recover short-output latency, but long-output
throughput still trails native TCP. Finding0054's device-local bookkeeping
intervention is inconclusive and was not selected. Before adding another
optimization, this experiment compares the stronger existing standalone path.

Finding0050's older standalone results cannot replace this comparison: current
standalone uses the later durable GPU IoState refactor, while current coalesced
also has subsequent queue-publication and final-response/SQ admission changes.
Older AMK arrangement results point in the other direction; they are cited as a
backend boundary and not rerun here. The earlier stronger eager-HF AMK exact-output
failure remains failed.

All three paths use current main at
048c204ed78e006f1e31cfa8a7fb4699b7429d06, identical reused vLLM FP16 model graphs,
precision, four prompts, prefix-release/padding policy and common runtime:
vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0, libbpf1.6.3 and NVCC13.0.88.
Checkpoint revisions are Smol93efa2f097d58c2a74874c7e644dbc9b0cee75a2 and
Qwen7ae557604adf67be50417f59c2c2f167def9a775, on the original RTX5090 Workspace
and Linux7.3.0-070300rc3-generic.

- Candidate: existing vllm_graph_uring_loop, independent resident GPU I/O on a
  nonblocking CUDA stream, mapped host bookkeeping and per-entry publication.
- Component control: existing vllm_graph_uring_loop_coalesced, I/O progression
  inside the model dispatcher, batched publication and completed-response/SQ gate.
- Main competitor: existing vllm_graph_user_network_wait, efficient native epoll
  TCP with the same model computation and response semantics.

These are whole constructor bundles. Their differences include progress
placement, state access, queue publication and admission; neither dynamic overlap
nor one-CTA interference is independently measured. Private BUILD compiles all
three current targets afresh, preserving original root artifacts. Production
source and defaults do not change.

## Completed run and primary results

Five paired blocks reverse context/model/cell order on odd blocks and rotate five
of six path permutations. Short-only gen1/c8 and transfer gen1/c1, gen64/c1,
gen64/c8 use32 measured requests per cell and8 sequential one-token warmups per
executor. All20 drivers /60 executors /120 cells finish:3840 measured requests,
124800 measured output tokens plus480 warmups,4320 complete replies and125280
total output tokens. The full run exits0 at2026-10-14T19:14:43.986672+00:00.
No serving failure, exclusion, replacement, restart or oracle/metric/timeout
change is used to obtain the result.

Predeclared primary is gen64/c8 client output token/s:

| Model | Coalesced control | Native userspace | Standalone GPU I/O |
|---|---:|---:|---:|
| SmolLM2-135M | 5175.049 | 5619.008 | 5566.112 |
| Qwen2.5-0.5B | 4613.723 | 4810.983 | 4688.845 |

| Model | Standalone minus control, token/s (nominal paired t95) | Standalone minus native, token/s (nominal paired t95) |
|---|---:|---:|
| SmolLM2-135M | +391.063 [102.619,679.506] | -52.896 [-90.472,-15.319] |
| Qwen2.5-0.5B | +75.121 [-144.334,294.577] | -122.138 [-370.862,126.586] |

Smol gains7.557% over coalesced and loses0.941% against native by ratios of means;
all five signed block effects agree in each contrast. Qwen gains1.628% by mean,
but the control contrast crosses zero and includes one adverse block. Its
native contrast also crosses zero. Neither crossing establishes equivalence,
noninferiority or superiority. Nominal paired t95 uses five process blocks,
df4 and2.776445105; these are not familywise intervals or pooled-request tests.

## Secondary boundaries and ordinary counters

Gen1/c8 TTFT means, in ms:

| Model | Coalesced control | Native userspace | Standalone GPU I/O |
|---|---:|---:|---:|
| SmolLM2-135M | 2.179160 | 2.196005 | 2.220609 |
| Qwen2.5-0.5B | 2.591148 | 2.643351 | 2.765961 |

Qwen standalone-minus-control is+0.174813ms [0.015763,0.333864], all five
blocks adverse. Smol's control contrast and both native contrasts cross zero.
The complete24 means and72 signed metric contrasts preserve gen1/c1,
gen64/c1, TTFT/completion/TPS/TPOT and known-worker CPU rows, including adverse
native boundaries. These secondary results do not replace primary throughput.
Known-worker CPU is partial process/worker accounting, not total CPU or energy.
At gen64/c8 standalone-minus-native CPU is+45.240us/request [29.876,60.604]
for Smol and+111.798us/request [77.037,146.559] for Qwen. Removing the steady
userspace request worker does not eliminate this measured process cost or
kernel/network CPU.

Ordinary untraced short contexts authenticate model rounds after subtracting8
warmups: coalesced/native/standalone means are5.8/8.2/8.2 for Smol and5.8/8.0/8.2
for Qwen. Standalone adds2.4 rounds versus coalesced for each model.

Transfer contexts authenticate2088 warmup/serial rounds before deriving
gen64/c8 rounds. Coalesced/native/standalone means are259.4/260.8/266.4 for Smol
and259.2/260.6/267.0 for Qwen. Standalone adds7.0/7.8 versus coalesced and5.6/6.4
versus native, with positive nominal intervals. Smol is faster than coalesced
despite more aggregate rounds, so fewer rounds alone do not explain this
constructor's throughput. Additional rounds against native are a possible
contributor, not exclusive causal mediation. Batch membership, per-round GPU
time and exact network/model overlap remain unobserved. Whole-transfer CQ-SQ
excess is descriptive multishot timer traffic, not per-cell GPU cost.

## Correctness and observation limits

Real preflight finishes4 drivers /12 executors /24 cells,192 measured requests
and6240 measured output tokens plus96 warmups. Two standalone protocol suites
each complete622 requests /22224 tokens,259 expected rejections and5000 empty
connections, with actual traced graph history/KV replay. Two32-action lifecycle
suites each check652 complete-or-prefix tokens,13 closed connections,
32 completed transport requests and3 aborts. All eight physical slots are FREE,
bitmap0, recycle32, pending/error/drop/overflow0 and SQ/CQ separately empty.
Intentional stop retains admitted32/retired31; this is not complete model output
for the interrupted request. The report preserves actual bytes and syscall
transcripts, not only summary pass booleans.

Protocol terminal trace_overflow=494 is the fixed128-entry I/O reply-diagnostic
truncation, separate from the full GPU event trace's zero overflow and complete
622-request client/history checks. It is retained in raw data rather than
reported as a zero-overflow diagnostic. Ordinary/lifecycle contexts are within
that diagnostic capacity.

Ordinary performance is untraced finite frozen whole-output membership, with
unobserved trajectories. Traced protocol history/KV replay uses the reused graph
and is not a fresh eager-HF arithmetic oracle. These checks do not establish
arbitrary prompts/models/text, AMK acceptance, fairness, backpressure bounds or
full OpenAI-compatible server quality. The syscall evidence supports the selected
path's lack of a steady userspace request worker; kernel/timer work remains.

Sparse host observations share boot04dc0087-5ccc-4c46-9997-b9a92f0e5167 and retain
33 older selected NVRM warnings, latest10:50:43UTC, without new selected lines.
The after snapshot is delayed until20:36:52UTC, rather than an immediate full-run
boundary; it finds no GPU applications. This does not prove continuous GPU
exclusivity, an entirely clean journal or harmlessness of older warnings.
Post-run12-source byte comparisons and eight preserved-path checks pass. The
existing common GPU power limit is400W versus575W device default; no run changes
it. One machine, sparse observations and five blocks bound generalization.

## Decision and replay

The [independent result review](../../bench/results/current_io_arrangement_20261014/result-review.md)
judges the run valid, the overall recovery hypothesis inconclusive with a
supported Smol boundary, research value supporting and impact a mechanism/
workload boundary. It independently recomputes all numerical rows and decodes
actual protocol/lifecycle bytes.

Prefer the existing standalone target for this measured Smol long-output scope.
Retain the coalesced Qwen concurrent-short-output boundary; do not promote an
all-model policy or change defaults. This experiment adds no production code,
allocation, flag, runtime configuration or entity. No further unchanged matrix
or speculative single-model arithmetic campaign is justified by this result.

The [archive and CPU replay](../../bench/results/current_io_arrangement_20261014/)
contains the fixed plan, complete independent reviews, frozen source/commands,
raw outputs, analyses and restoration evidence. All signed secondary results
remain in [full.analysis.json](../../bench/results/current_io_arrangement_20261014/full.analysis.json).
The [ordinary long-counter output](../../bench/results/current_io_arrangement_20261014/long_counter.analysis.stdout)
and [restoration record](../../bench/results/current_io_arrangement_20261014/final_restoration.json)
describe counter scope and cleanup. The full serving/performance objective remains
active: superiority over the strongest native competitor, generic backend
acceptance and a causal explanation of remaining cost are still open.
