# Sleepable eBPF/io_uring loop with unchanged GPU computation

## Question and admission

Retain finding0035's local ordinary-serving question:what client latency/
throughput does the ordinary packed/prefix adapter deliver against the
efficient native network alternative after BF_TRACE is removed? No formal
paper RQ, external SOTA or arbitrary-model claim is introduced.

Role supporting. Findings0042/0043 establish roughly one CPU core of known-
worker cost in stock SQPOLL, versus roughly0.03–0.04 native cores, without a
reliable stock delivery advantage. Finding0043 cannot identify that cost's
exclusive cause and cannot supply the absent sleepy-loop intervention.
A current-kernel upstream BPF loop may replace SQPOLL while preserving GPU-
owned TCP requests and model computation. This is a new causal discriminator,
not another copy retry, dependency-only paper result or model arithmetic
campaign. It outranks extra model/scale points or another unchanged matrix.
Optimized cross-node serving remains a valuable later comparison but cannot
answer this measured local coordination cost.

Hypothesis:replacing stock SQPOLL coordination with the upstream sleepable
eBPF/io_uring loop reduces known-worker CPU for long eight-client output; the
same comparison tests resulting client TTFT/TPS against efficient native TCP.
These are the tradeoffs of one intervention, not independent experiments.
A CPU improvement alone does not establish delivery superiority or equivalence.
A contradictory CPU result rejects this replacement's intended efficiency
benefit. Delivery loss bounds the path even if CPU improves. Inconclusive
delivery stays inconclusive; do not keep repeating until favorable.

Largest credible story:an upstream, model-agnostic kernel I/O driver can
coordinate resident GPU inference without a steady userspace request worker
or a continuously active SQPOLL core. This two-architecture experiment cannot
establish general model support, full JSON/text serving, total CPU/energy or
GPU-interrupt completion. Shared-control lifecycle and strict correctness are
integration dependencies, never independent novelty/results.

## Implementation and causal scope

Original Workspace/main, current kernel7.3rc3, RTX5090. No host kernel/package/
driver or persistent infrastructure change. Reuse vLLM0.31.0, Torch2.13+cu129,
Transformers5.17, FP16, exact checkpoints, packed prefill and FIFO-prefix
release, head/greedy selection and KV budget. Model arithmetic kernels stay
unchanged. Host serve/signal/lifecycle entry points may route into the new
kernel loop. Compare ordinary model-dispatch SASS; do not call changed arrival/
batching histories identical computation trajectories.

Use upstream io_uring_bpf_ops.loop_step and bpf_io_uring_submit_sqes/
bpf_io_uring_get_region. Current live BTF contains all required types/kfuncs.
Upstream requires DEFER_TASKRUN and rejects SQPOLL/IOPOLL. Use SINGLE_ISSUER,
NO_MMAP/NO_SQARRAY as required for the same GPU-owned SQ/CQ memory.
The ring creator enters io_uring once for steady service, remaining in the
kernel callback/wait loop. No CPU accept/recv/send, per-request syscall proxy,
periodic userspace helper or new daemon is introduced.

A standard kernel multishot TIMEOUT supplies60us CQ wakeups, matching the
existing native60000ns completion wait. This is a declared initial mechanism,
not a measured tuning optimum. No idle/deadline/SQPOLL adjustment, transport
policy change or parameter search. Without a kernel wakeup, GPU SQ publication
alone cannot resume a sleeping loop. Do not disguise such a deadlock with
client barriers, a busy userspace helper or changed model pacing.

Bootstrap the timeout before the GPU SQ producer starts, then attach the BPF
loop to the same ring. A registered io_uring memory region exposes a small
transport control prefix in the existing mapped report:actual ring offsets,
model-quiesced/finished/stop state and the existing finite serve deadline.
Discover offsets from io_uring_setup; no replicated kernel layout constants.
The callback submits published SQEs and waits for the next CQ index. Repeated
timeout CQEs with MORE do not retire the one pending timeout; final cancellation
does. Timer CQEs never become model requests or output tokens.

SIGTERM directed at a helper thread must stop this path too:the existing
signal handler updates the mapped loop-stop flag; the next kernel wake ends
steady loop entry. Existing model shutdown then marks quiescence and enters
a bounded kernel cleanup loop until the GPU network controller has drained
cancels, replies and closes. Cleanup may actively drain; it is outside steady
request service. GPU release-publishes finished after final counters. Standard
timeout cancellation and all SQ/CQ/buffer lifetimes must balance.

Build the optional loop BPF object separately; ordinary probes/default module
must not acquire this dependency. Use already installed running-kernel UAPI
headers for the new memory-region API, discovered from /usr/src or the mounted
kernel build path. Do not add guessed compatibility shims or change system
headers. A source-adapter failure is recorded and repaired without relaxing
wire/oracle/pacing. No formal completion claim follows from BTF presence.

Primary upstream sources:
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c
- https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.c
- https://github.com/torvalds/linux/blob/v7.3-rc3/include/uapi/linux/io_uring.h

## Fair comparisons and fixed fidelity

Candidate:ordinary vllm_graph_uring_loop and its traced counterpart, sharing
the repaired/incremental stock TCP logic and GPU network controller.
Main alternative:efficient native timed-epoll TCP, representing the strongest
runnable same-compute alternative. A fresh matched measurement is necessary;
old means cannot isolate a changed backend or phase.
Component control:current incremental SQPOLL stock. It tests the intended
coordination replacement, not historical0042 or a second main baseline.
Drop the module row:prior matched results already cover it and it cannot
identify this intervention.

All paths share checkpoint revisions, FP16, wire/client/prompts, graph/KV
policy, normal TCP options and existing counters. BPF loop adds timeout/CQ and
kernel callback work, with different submission/scheduling behavior. This
is a complete coordination-path effect, not exclusively polling overhead.

Freeze byte-identical0043/0042 complete references before new serving:
Qwen17 keys/22 whole sequences; Smol17/19. Every complete valid ordinary reply
must match one full qualified sequence for exact prompt/gen. No tolerance,
tokenwise union, post-observation expansion, teacher forcing or retries that
discard novel sequences. Current ordinary batch/KV trajectory is unobserved;
traced qualification independently replays its actual histories. Do not claim
task quality, universal numerical correctness or identical concurrent outputs.

## Preflight and full qualification

Fresh plan review precedes any new model serving. At most three real preflight
attempts. Rebuild optional ordinary/traced loop and SQPOLL plus native.
Smallest real preflight:Qwen,all three paths,the existing four cells with8
measured requests/cell plus8 excluded gen1 warmups/executor.
Three executors/12 cells/120 total requests/3144 total checked tokens including
24 warmups. Inspect actual exits,counters,oracle and syscall receipts, not just
wrapper status.

Both models then run all3 paths through existing622-request traced and ordinary
strict protocol:12 executors/7464 requests/266688 valid tokens,3108 intended
rejects and60000 empty connections. Preserve fragmentation, prompt/block
edges, concurrency1..8, reuse/wrap, mixed pacing, pipeline/half-close,
HTTP400/binary EOF, following valid requests and helper-thread SIGTERM.
No omitted failures, new client barriers or relaxed counters.

The shared HF path also builds the loop and runs the already archived two-model
eight-idle-cycle plus original lifecycle workload from0043 hf_self_redirect/
driver.py:32 requests/652 checked complete/prefix tokens per model,13 closes
and3 expected aborts. Adapt only the selected binary and kernel-loop syscall
expectation. Keep oracle,wire,pacing,cases and stop target unchanged.

After-ready all-thread traces must show no server userspace socket calls.
Loop serving contains one blocking io_uring_enter kernel-loop entry rather
than stock's zero steady entries; no per-request reentry proxy is allowed.
Native must engage accept/recv/send. Verify loop has no SQPOLL task and stock
has the actual SQPOLL task. All timed requests/counters/references and normal
terminal ownership remain required. Dependency success is not a paper result.

## Full workload, metrics and interpretation

Reuse four tokenized prompts and matrix (gen1,c1),(gen64,c1),(gen1,c8),(gen64,c8).
64 measured requests/cell,8 excluded checked gen1 warmups/executor.
Six paired process blocks/model,each permutation of (uring_loop,userspace,uring)
once,cell rotation as in0042. Qwen thenSmol; no model overlap.
Complete scope36 executors/144 cells/9216 measured requests/299520 measured
tokens plus288 excluded checked warmups. Ordinary binaries have no BF_TRACE;
first128 stock network records and aggregate counters remain real measured costs.

Per-model predeclared primary effects:
1. native-minus-loop gen1/c1 mean TTFT (positive favors loop);
2. loop-minus-native gen64/c8 output tokens/s;
3. stock-minus-loop gen64/c8 known-worker CPU seconds/request.

Six total intervals. Six process blocks—not pooled requests—are paired units.
Nominal two-sided t95 df5,critical2.570581835636305/sqrt6. Report every primary,
negative estimate and outlier; no familywide superiority/equivalence or
post-selection claim. Positive interval supports that scoped metric, negative
contradicts it,crossing0 is inconclusive. Interpret CPU/delivery separately;
no composite score,noninferiority cutoff or CPU-win-as-latency-win rule.
Other cells,completion,TPOT and remaining CPU contrasts are secondary.

Use existing client timing and all-thread POSIX process clock read brackets,
actual /proc/PID/task worker identity and no double count. The blocking
creator task's kernel CPU remains in its process clock. RX/softirq/BPF/TCP
elsewhere,client and energy are excluded. No exclusive CPU attribution or
total-service claim. Standard TTFT/TPOT/TPS follow official versioned vLLM:
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py
https://docs.vllm.ai/en/v0.31.0/design/metrics/

## Executable path and evidence

Use existing source-native bench/vllm_serving.py with a loop-comparison mode,
and existing bench/vllm_serving_analysis.py extended to these paths and the
fixed primary contrasts. No experiment-control schemas or new gating interfaces.
Literal runtime/model/output bindings are written before serving.

    make probes tools vllm-graph-uring-loop vllm-graph-uring vllm-graph-user-network-wait vllm-graph-trace VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --loop-comparison --untraced --reference-path FROZEN --preflight --model QWEN --output TEMP/preflight.jsonl
    ENV/bin/python bench/vllm_serving.py --loop-comparison --correctness --model MODEL --output TEMP/MODEL_traced_correctness.jsonl
    ENV/bin/python bench/vllm_serving.py --loop-comparison --untraced --reference-path FROZEN --correctness --model MODEL --output TEMP/MODEL_correctness.jsonl
    ENV/bin/python bench/vllm_serving.py --loop-comparison --untraced --reference-path FROZEN --model MODEL --output TEMP/MODEL_performance.jsonl
    python3 bench/vllm_serving_analysis.py RAW

Qualify source,commit/push main and freeze one revision before timing. Preserve
all initial failures and raw arrivals/output/counters/clocks/commands/source/
build/package data. Reanalysis of0042/0043 must remain unchanged.
No timing cell replacement or failed baseline counted as a win. Resume the
same confirmed live process after observation timeout.

Fresh result review reconstructs coverage,all permutations,primaries,CPU/
numerical scope and fair mechanism engagement. Archive one plan,all plan-review
rounds in plan-review.md,raw/results and one result-review.md in this directory.
After review remove only owned runtime/build output,verify original boot/base/
Workspace/Coder/WIP and no own process/module/pins/GPU app,and publish honest
main results. Endpoint/journal observations do not prove continuous isolation.
Keep the full project goal active until its actual requirements are proven.

Concrete TEMP: /tmp/bpfusion-uring-loop-frmz3lrm; ENV=TEMP/runtime; FROZEN=TEMP/frozen_references.json.

CPU-clock definition: https://man7.org/linux/man-pages/man3/clock_gettime.3.html
(CLOCK_PROCESS_CPUTIME_ID covers all threads, including their kernel CPU.)

## Temporary dependency correction before serving

Real preflight attempt1 fails before any request:system libbpf1.3 exposes no
struct_ops shadow initial value. Use official temporary libbpf1.6.3 in all
three conditions; base/system libraries remain unchanged. Its upstream
bpf_map__initial_value supports the required initialization API. This corrects
startup rather than changes the hypothesis/oracle/client/matrix. Record build
and runtime paths before retry2 and keep the original failure.
Source: https://github.com/libbpf/libbpf/blob/v1.6.3/src/libbpf.c
