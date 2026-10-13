# Experiment plan: optimized stock TCP transport and measured worker cost

## Retained question and admission

No formal paper RQ/thesis exists. Preserve the full retained Linux TCP/HTTP →
eBPF/shared queue → resident real-model computation → asynchronous kernel TCP
TX objective. Reuse the local question from the completed ordinary experiment:
"what client latency/throughput does the ordinary packed/prefix adapter deliver
against the efficient native network alternative after BF_TRACE is removed?"
The cross-node question/finding0029 stays separate and unchanged.

Specific hypothesis: replacing the module's polling TX path with GPU-owned
stock io_uring improves ordinary gen1/c1 TTFT or gen64/c8 throughput against
the efficient native alternative with identical optimized computation.
Known-worker CPU is a secondary mechanism/tradeoff measurement, not total CPU
and not an additional independent experiment.

Role supporting. The largest credible story is a portable ordinary-Linux TCP
path without a bespoke TX module or userspace request proxy, with measured
client value/cost on reused optimized inference. Strongest reject argument:
moving work into SQPOLL simply relocates a CPU worker and its cost while GPU
execution or final-response ordering prevents a delivery advantage. Prior
finding0035 has no stock transport or measured worker CPU;0041 only qualifies
correctness. Reanalysis/citations cannot recover absent matched cells.

Positive effects support the scoped path claim. Negative/mixed/null-inclusive
results retain portability/correctness but reject a speedup claim for those
conditions and direct further work toward the measured bottleneck. This does
not directly refute the broad user goal. The best alternative is cross-node
optimized delivery or total-service CPU attribution; first comparing the new
transport locally removes physical-path noise and directly tests the changed
mechanism. Do not repeat an unchanged old matrix or tune model arithmetic.

Expected answer: stock completion may reduce polling latency, but throughput
may remain GPU-bound and default SQPOLL may consume more CPU. A slower stock
path contradicts the latency expectation; zero-containing intervals leave it
inconclusive. No equivalence, total CPU, SOTA, arbitrary models or novelty claim.

## Assets and comparison

Use original yunwei356/bpfusion-dev /workspaces/repository main, RTX5090,
kernel7.3rc3 and current pinned runtime vLLM0.31.0/Torch2.13.0+cu129/
Transformers5.17.0, two unchanged checkpoint revisions. Reuse existing
bench/vllm_serving.py and client/analysis, no custom toy workload.

Candidate: ordinary vllm_graph_uring, stock SQPOLL/NO_MMAP, eBPF framing and
completion recycling. Main matched mechanism alternative: ordinary
vllm_graph_user_network_wait, existing60000ns timed epoll/nonblocking TCP.
It represents the competing efficient userspace request/reply answer, not an
official external framework/SOTA server. Citation cannot settle this newly
integrated same-compute path. If native matches/wins, do not claim a transport
speedup merely because stock has no userspace socket syscalls.

Component control: ordinary vllm_graph with existing bfusion_tx polling. It
separates a stock-path effect from the already tested module transport; it is
not another main baseline. All three have identical upstream model/head/
sampling, FP16, KV budget, packed prefill and FIFO-prefix model release,
same inputs, wire protocol, client and TCP defaults. Timing can change actual
batch shapes/FP16 trajectories. Default server mechanisms are retained,
including stock SQPOLL idle and native wait; their CPU/latency tradeoff is
part of the mechanism, not artificially matched by adding tuning.

## Fixed correctness and preflight

Before any new performance output, freeze complete reference sets from the
public finding0035 frozen asset plus0041's independently replayed strict
references. No served performance output enters those sets. Archive source
paths/model/precision/UTC. Every valid reply must exactly equal one entire
qualified sequence for its exact prompt/gen, without tokenwise mixtures,
tolerance, teacher forcing or expansion after observation. This finite-set
check is weaker than current-batch-history replay; report that limitation.
A novel output fails promotion, even if later diagnosed as legitimate FP16
batch variation; retain raw and do not change this run's oracle.

Finding0041 already completes the new transport's traced strict protocol and
HF shared-header regression. No model/backend source change follows.
Before full timing: build all three ordinary targets; run Qwen real preflight
(8 requests/cell,8 excluded warmups,all four cells/all transports), then run
the full existing622-request untraced strict protocol on both architectures
and all three transports. That adds finite-set ordinary lifecycle evidence,
not a scientific result. Preserve all failed setup/preflight/strict outputs.
The original mixed pacing, fragmentation, wrap, half-close and invalid cases
remain unchanged. Full timing begins only after these actual paths pass.

## Metrics, workload and repetitions

Four existing tokenized text prompts, outputs1/64, closed-loop clients1/8.
Capture, initialization and connection setup are outside client timing.
Primary effects per model: native-minus-stock gen1/c1 mean TTFT, and
stock-minus-native gen64/c8 output tokens/s. Standard client definitions:
[vLLM metrics](https://docs.vllm.ai/en/v0.31.0/design/metrics/).
The versioned [official serving client](https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py) supplies the client-arrival precedent.
Completion and TPOT plus other cells/quantiles are descriptive/secondary.
TTFT includes actual TCP/client arrival, not GPU-ready time.

Secondary: measured known-worker CPU seconds/request in gen64/c8 and other
descriptive cells. Reuse resident_dispatch.py's POSIX all-thread process CPU
clock plus module tx_cpu_ns when present, brackets sampled before/after each
cell. Archive components and read brackets. Connections are established
before the initial CPU read; lane connection close and any work until the
final read can fall inside the bracket. Label CPU as known-worker CPU during
the cell bracket divided by requests, not pure inference/request CPU. Stock SQPOLL/io-workers are
created in the server thread group upstream:
[io_uring/sqpoll.c](https://github.com/torvalds/linux/blob/master/io_uring/sqpoll.c),
[kernel/fork.c](https://github.com/torvalds/linux/blob/master/kernel/fork.c).
Verify actual live /proc/PID/task comm entries for stock. Count them once via
the process clock, never add their per-thread readings again. Module TX is
outside that group and its existing counter is added separately. This omits
RX/softirq/BPF and TCP work elsewhere and cannot establish total CPU/energy
or a syscall-only causal saving. APIs:
[POSIX CPU clock](https://man7.org/linux/man-pages/man3/clock_getcpuclockid.3.html).

Six process blocks/model, all six permutations of (uring,userspace,kernel)
exactly once in itertools.permutations input-tuple order:
(uring,userspace,kernel),(uring,kernel,userspace),(userspace,uring,kernel),
(userspace,kernel,uring),(kernel,uring,userspace),(kernel,userspace,uring).
Rotate the four cell orders by block index through the existing matrix. Per executor64 requests/
cell plus8 excluded checked gen1 warmups. Two models sequential Qwen thenSmol.
Full totals36 executors,144 cells,9216 measured requests,299520 measured tokens
and288 excluded warmup tokens. Startup cost is excluded; expected tens of
minutes. Preserve every block/sample/outlier and relevant shared-host events.

The six paired process blocks are the units, nominal two-sided t95(df5,
critical2.570581835636305), not pooled requests. Report all four primary
intervals, with no familywide significance claim. Entirely positive supports
that scoped effect; entirely negative contradicts it; crossing0 is inconclusive.
CPU tradeoffs do not veto a correctly measured latency effect unless the
claim itself is CPU/Pareto improvement. Component comparisons and secondary
intervals are explicitly labeled; no posthoc composite score/cutoff.

## Execution and completion

Minimal existing-driver adaptation: --transport-comparison selects the three
ordinary paths and six orders, records per-cell CPU snapshots/task identities,
and reuses --untraced --reference-path. Analysis adds stock stats verification,
CPU delta reconstruction, two labeled comparisons and df5 for six blocks.
No new service/control schema/persistent setting or model math change.

Temporary environment is /tmp/bpfusion-vllm-uring-q26fqorc/runtime.
PATH uses its bin and VLLM_ENABLE_V1_MULTIPROCESSING=0 only for test children.

    make vllm-graph vllm-graph-user-network-wait vllm-graph-uring VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --transport-comparison --untraced --reference-path FROZEN --preflight --model QWEN_PINNED --output /tmp/RUN/preflight.jsonl
    ENV/bin/python bench/vllm_serving.py --transport-comparison --untraced --reference-path FROZEN --correctness --model MODEL_PINNED --output /tmp/RUN/MODEL_correctness.jsonl
    ENV/bin/python bench/vllm_serving.py --transport-comparison --untraced --reference-path FROZEN --model MODEL_PINNED --output /tmp/RUN/MODEL_performance.jsonl
    python3 bench/vllm_serving_analysis.py RAW

Run both strict/full model stages sequentially after fresh plan review and
real preflight. Freeze validated source main before full timing. Raw archive:
bench/results/vllm_uring_performance_20261013/. One plan, plan-review.md and fresh
result-review.md, all commands/status/logs/reference checks and raw cells.
Do not replace live processes on observation timeout; inspect same handles.
Retain failure prefixes and systematic repair deviations. Complete every
planned cell/executor before interpretation; no partial-run result.

Record original boot/Workspace/session/GPU endpoints, bounded host fault
journal and task identities. Shared-host placement remains a limitation;
endpoint reads do not prove continuous isolation. Following fresh result
review, archive results and remove only this test's runtime/owned build outputs,
verify no own process/module/pins and original base/Coder/WIP retained.
Publish honest finding/evaluation and main commit/push. Target table: both
models' primary latency/throughput effects with paired intervals and known
CPU components/tradeoff beside the module component control.

## Concrete bindings before preflight

Runtime ENV is /tmp/bpfusion-vllm-uring-q26fqorc/runtime; FROZEN is
/tmp/bpfusion-vllm-uring-q26fqorc/transport_frozen_references.json, archived
here as frozen_references.json before performance observations. Qwen has17 keys/22 complete
sequences; Smol has17 keys/19. Pinned paths and exact literal invocations are
recorded in qualification_pipeline.py before execution; the performance
pipeline will use the same bindings and flags after validated main source
is committed. No oracle expansion occurs.

The stock transport also adds a resident GPU network-control block. Its GPU
resource and queue-scanning cost belong to this complete mechanism comparison;
identical model arithmetic does not imply identical available GPU resources.
No syscall-only or exclusively polling-caused attribution follows. Actual
process/mode and rotated-cell order are reconstructed by the analyzer.
