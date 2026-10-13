# Experiment plan: incremental stock-TCP output copying

## Retained question and admission

No formal paper RQ exists. Retain finding0035's local question:
"what client latency/throughput does the ordinary packed/prefix adapter deliver
against the efficient native network alternative after BF_TRACE is removed?"
The cross-node question and full retained project objective remain unchanged.

Hypothesis: avoiding rereads/rewrites of fully sent output prefixes improves
gen64/c8 delivery throughput of the complete stock transport. Source inspection
shows the former SEND loop starts at token0 after each positive completion,
although its next send starts at r.sent. Candidate starts at floor of unsent
body-byte offset, preserving a partly sent token and the header.

Role supporting, with correctness/build setup dependency-only. Largest
credible story: reusable optimized inference over ordinary Linux TCP can avoid
a real transport-copy cost without a userspace proxy or model-specific tuning.
This could improve the qualified stock option and narrow its native throughput
deficit. It does not remove SQPOLL CPU cost or prove general/SOTA superiority.

Finding0042 cannot identify the cause of stock's lower Qwen throughput:
GPU control resources, mapped-memory traffic, ordering and batching differ.
No old raw can supply this absent copy-only A/B. Current source supplies a
specific discriminator rather than another unchanged transport matrix.
A positive old/new effect supports practical importance of this copy loop;
a negative/null effect rejects or bounds it and redirects investigation.
Candidate/native determines whether the complete path actually gains against
the strongest same-compute alternative. No favorable subset replaces either.

Best alternative: SQPOLL CPU/wakeup redesign or cross-node optimized delivery.
Those are broader and important, but cannot distinguish this directly observed
redundancy. This small causal intervention outranks model arithmetic work,
unchanged repetitions or extra weak baselines. If inconclusive, close it and
prioritize another measured cost rather than repeat it until favorable.

## Method and fair comparisons

Candidate: existing optional vllm_graph_uring with incremental first-token copy.
The remaining logic, header, SEND lengths/addresses/flags, CQ handling, FIFO
final submission, peer/buffer ownership, polling defaults and counters remain
unchanged. Normal module serving remains the project default.

Main alternative: existing efficient vllm_graph_user_network_wait. It tests
the competing practical answer of a native timed-epoll request/reply worker
with the same optimized computation, not an official vLLM server/SOTA stack.
Matched measurement is necessary for the new candidate on these requests.

Component ablation: vllm_graph_uring_full_copy, compiled from the same source
with BF_IO_FULL_COPY setting first=0. This restores the former loop alone.
It has the same GPU network-control block, maps/queues, SQPOLL defaults, first128
IoRecord diagnostics and other counters as the candidate. Do not remove those
costs or call BF_TRACE-off free of all instrumentation. Drop the module row
here: finding0042 already supplies that control and it cannot isolate copy work.

All paths reuse vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0, pinned
Qwen2.5-0.5B-Instruct and SmolLM2-135M, FP16, packed prefill, prefix release,
head/greedy selection, KV budget, client/wire/TCP policies. Model arithmetic/
dispatcher source is unchanged. Arrival timing can change batches/FP16
trajectories; identical algorithms do not imply identical concurrent outputs.

## Byte and numerical correctness

For completed send offset r.sent, copy begins at0 while still inside the
header, otherwise floor((r.sent-header)/4). A partly transmitted token is
copied again; fully transmitted tokens are skipped. r.busy still prevents
buffer mutation before CQ completion. This is a source-level byte argument,
not proof that real socket partial-send stress has been exercised.

Use the same public finding0042 frozen complete references, copied unchanged
before any new serving output: Qwen17 prompt/gen keys/22 whole sequences,
Smol17/19. Do not expand after observation, use tokenwise mixtures/tolerance,
or teacher-force served output. Every valid ordinary response must match one
whole qualified sequence for its exact input/gen. A novel sequence fails this
fixed check; retain/diagnose separately without changing the run's oracle.
This is finite-set fidelity, weaker than current unobserved trajectory replay.

Before full timing: compile ordinary/traced candidate and full-copy control
plus native; run real Qwen three-path preflight (8 gen64/c8 requests/path and
8 excluded gen1 warmups/path). Then both architectures/all3 paths run the
existing complete622-request traced strict protocol, including all prompt/
block/concurrency/rejection/wrap/mixed/pipeline-half-close cases, independent
upstream batch/cache-history replay and all-thread network/wake checks.
Also rebuild shared-header qwen_graph_uring and run the unchanged public
two-model HF lifecycle driver for reset/in-flight stop regression.
These are integration dependencies, not extra scientific results.

After traced qualification, run the same complete ordinary strict protocol
on both architectures/all3 paths against the fixed complete sets before
performance. No added client barriers, changed pacing, relaxed checks or
excluded cases. Record all failures and source versions. Current code/header
must remain fixed through the full comparison.

## Workload and primary effects

Reuse the four real tokenized prompts and closed-loop8 clients, gen64.
No gen1 timing repetition: first-token copying has no fully sent prefix, and
finding0042 already supplies its local comparison. gen64/c8 TTFT, completion
and TPOT are collected as secondary delivery metrics within this same cell.

256 measured requests/executor,8 excluded checked gen1 warmups. Longer cells
than0042 reduce setup/close amortization and provide32 request waves; they
do not manufacture additional independent repetitions. Six process blocks/
model, all6 permutations of (uring,uring_full_copy,userspace) once in
itertools.permutations input-tuple order. Qwen thenSmol sequentially.

Full scope36 executors/36 measured cells/9216 measured requests/589824 tokens,
plus288 excluded warmup tokens. Preflight3 executors/3cells/24 measured gen64
requests1536tokens plus24 warmup tokens. Twelve complete traced+ordinary strict
executors add7464requests/266688 valid tokens/3108 intended rejects/60000 empty
connections. Prior qualified compute is reused; expected tens of minutes.

Primary standard metric: cell output tokens/s, all tokens from firstsend to
lastarrival. Primary candidate-minus-baseline effects per model against both
native and full-copy ablation,4 intervals total. TTFT/TPOT/completion follow
[versioned vLLM client](https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py)
and [vLLM metrics](https://docs.vllm.ai/en/v0.31.0/design/metrics/).
Client delivery includes TCP/coalescing; initialization/connections excluded.

Six paired process blocks are units, nominal two-sided t95 df5 critical
2.570581835636305/sqrt6. Report all4, retain outliers/negative estimates,
no familywide superiority/equivalence or pooled-request pseudoreplication.
Positive interval supports that scoped effect, negative contradicts it,
crossing0 inconclusive. Copy/native conclusions stay separate: improving an
ablation alone does not establish a native advantage.

Secondary known-worker CPU uses existing POSIX all-thread process clock and
raw cell read brackets, with actual SQPOLL task verification and no double
count. No module in this matrix. Connection close/other bracket work included;
RX/softirq/BPF/TCP elsewhere excluded. This is not total CPU/energy. Polling
defaults are fixed and CPU savings are not expected from the copy change.
Standard async SEND completion can be short:
[official liburing](https://github.com/axboe/liburing/blob/master/man/io_uring_prep_send.3).
No new CPU threshold, composite score or tuning.

## Executable workflow and completion

Original yunwei356/bpfusion-dev Workspace/main. Preserve original sessions/WIP,
base packages, caches and host/kernel/driver. Temporary pinned runtime is
TEMP/runtime. Make adds a separate full-copy control target, avoiding extra
ablation builds in normal vllm-graph-uring. Benchmark --copy-comparison uses
the existing runner/oracle/client/analysis, selecting these3 modes and one cell.

    make probes tools vllm-graph-uring vllm-graph-uring-full-copy vllm-graph-user-network-wait vllm-graph-trace VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --copy-comparison --untraced --reference-path FROZEN --preflight --model QWEN_PINNED --output TEMP/preflight.jsonl
    ENV/bin/python bench/vllm_serving.py --copy-comparison --correctness --model MODEL_PINNED --output TEMP/MODEL_traced_correctness.jsonl
    ENV/bin/python bench/vllm_serving.py --copy-comparison --untraced --reference-path FROZEN --correctness --model MODEL_PINNED --output TEMP/MODEL_correctness.jsonl
    ENV/bin/python bench/vllm_serving.py --copy-comparison --untraced --reference-path FROZEN --model MODEL_PINNED --output TEMP/MODEL_performance.jsonl
    python3 bench/vllm_serving_analysis.py RAW

Bind literal paths/pinned models/child PATH and
VLLM_ENABLE_V1_MULTIPROCESSING=0 in archived pipeline before preflight. Review
plan before new serving; real preflight then full qualifications; commit/push
validated source main before full timing, freeze that revision. Existing
analysis must preserve previous0042 outputs byte-identically.

Archive plan/plan-review.md/result-review.md, raw arrivals/bytes/counters/
components, commands/status/source diff/build/package versions and endpoint/
fault observations under bench/results/uring_incremental_copy_20261013/.
Do not restart on observation timeout; inspect the same live handle. Complete
all planned cells/executors before interpretation. Any systematic defect is
recorded and affected comparisons rerun; no invalid baseline failure becomes
a candidate win. Shared-host endpoint/fault checks are not continuous isolation.

Fresh result review independently reconstructs numbers, fidelity, fairness,
orders and terminal ownership. Target table: both models' candidate/full-copy/
native TPS, four paired effects, secondary delivery/CPU tradeoffs.
After archive/review remove only owned runtime/build outputs and verify original
boot/base/Workspace/Coder/WIP and no own process/module/pins/GPU app. Publish
honest main evidence; keep full goal active until its requirements are proven.

## Concrete bindings before serving

TEMP is /tmp/bpfusion-uring-copy-6wpl3780, ENV is its runtime directory, FROZEN is
/tmp/bpfusion-uring-copy-6wpl3780/frozen_references.json.
qualification_pipeline.py and qualification_commands.json record all actual
commands, both pinned model paths and child environment before serving.
The unchanged asset equals the public0042 asset; no new serving output has
been observed. The separate performance pipeline will use the same literal
bindings after source qualification/main publication.

HF lifecycle commands are now bound in qualification_pipeline.py and
qualification_commands.json before execution, using the unchanged0040 driver
and oracle copied inside this owned temporary directory. The parent verifies
both lifecycle exit/pass receipts, not merely the wrapper exit.

## Failure investigation before timing

See [qualification.md](qualification.md). An initial full-copy strict control
failed pipeline half-close delivery. Subsequent diagnostic passes do not erase
that failure or establish its cause. The oracle, client pacing and planned
performance matrix remain unchanged; no timing has started.

HF lifecycle uses the original /usr/bin/python3 with the base PATH, matching
the retained HF CUDA13 environment. vLLM commands alone use the pinned
CUDA12 runtime PATH. This pipeline correction is made before HF execution;
no model or runtime package is changed. Literal continuation commands are
archived in qualification_continuation.py.

The HF reproduction captured genuine RECV -EAGAIN, which the previous shared
header treated as connection death. The common source now rearms EAGAIN/EINTR
for both stock conditions. This recorded lifecycle repair precedes all new
qualification and timing; the full-copy control restores the former copy loop
with the same corrected receive semantics. No timer, polling tuning, CPU
request helper, oracle expansion or client barrier is introduced.

## Common ingress repair before timing

After the EAGAIN-repaired normal qualification passed, the repeated-idle HF
regression still stalled before admission. Read-only kernel observations record
divergent TCP/psock consumed cursors and a queued raw skb. Temporary same-socket
ingress redirect passes both architecture idle workloads and all twelve
traced/ordinary vLLM protocol executors. This standard sockhash helper is now
adopted in the shared BPF source before timing, with the default module path
and final copy preflight still being checked. Both copy conditions use the
identical BPF object and EAGAIN/EINTR repair; only BF_IO_FULL_COPY differs.
The copy hypothesis, six permutations, native alternative, fixed complete
references, client pacing and four primary effects remain unchanged. The
full-copy ablation is this repaired implementation with the former copy loop,
not historical0042. No new expected answer or timing result follows from the
repair. Existing HF candidate commands and final qualification pipeline retain
literal bindings. The temporary candidate wrapper restored the original BPF
object before the production source edit; all initial failures remain archived.

Final production-source qualification completes: both model module/native
strict workloads pass (four executors,2488 requests/88896 valid tokens), as
does the final three-path copy preflight (24 measured gen64 requests/1536
tokens plus24 excluded gen1 warmups). Final commands, raw outputs, analyses
and build receipts are in final_qualification/. Original boot/base/Coder/WIP
remain; endpoint checks find no own BPF pins, loaded module or GPU application.
This completes integration dependencies only. Full copy timing has not started;
all conditions will use one published source revision and unchanged references.
