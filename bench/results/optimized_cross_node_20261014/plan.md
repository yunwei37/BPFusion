# Optimized module-free cross-node serving

## Research question and admission
Retain finding0029's question verbatim: Does removing the steady userspace
request worker improve client latency or throughput over efficient native
networking on a real cross-node path, with identical upstream GPU computation?
There is no formal paper thesis. Planned role supporting.

Findings0035/0042/0044/0045 measure optimized local delivery; finding0029
measures an older HF backend with module TX across nodes. None measures the
current packed/prefix upstream-vLLM backend and module-free eBPF loop on a
physical cross-node path. Prior data cannot be subtracted to assign networking
overhead or predict a matched cross-node win.
Largest credible story is actual optimized Linux network service with resident
GPU computation and no steady userspace request worker, with an honest boundary
against the efficient same-compute TCP alternative.
This repairs a real acceptance gap, not another tiny loop/timer variation.
A positive native primary interval supports that metric in this finite topology;
negative or inconclusive intervals bound the implementation and close unchanged
timing. Results do not prove equivalence, general superiority, total CPU or
absence of environment interference. The full retained objective stays open.

Best alternative is detailed current-backend stage profiling. Older finding0030
already localizes the old HF model span; new profiling would help attribution
but perturb timing and require clock/trace qualification. Cross-node service
delivery is the stronger immediate actual-serving acceptance gap after0045.
Additional small loop variants and unchanged local repeats are rejected.

## Hypothesis and competing outcomes
The current optimized module-free eBPF loop can preserve qualified output and
lifecycle over real cross-node Linux TCP and improve client TTFT or throughput
against efficient native TCP using the identical optimized backend.
Local results make a large speedup unlikely; real-network arrival/batching and
completion delivery can differ. No expected favorable verdict.
Losing to or matching native preserves the portability/implementation result
but does not establish a performance contribution. A contradictory result
bounds this mechanism/workload; it is not a direct broad-thesis challenge.

## Real assets, fairness and prior protocol
Original yunwei356/bpfusion-dev, /workspaces/repository/main, RTX5090,
Linux7.3-rc3. Frozen production source bd39e59e4e5f27b5ac72313795d5ea77d3ef4d82.
No production-source/model math/timer/network-policy change.
Same FP16 vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17, temporary common
libbpf1.6.3, pinned Qwen2.5-0.5B and SmolLM2-135M revisions from0045.
Candidate vllm_graph_uring_loop; sole main baseline
vllm_graph_user_network_wait. Native timed epoll is the strongest runnable
same-compute competing answer. Neither citation nor older local/old-HF runs
can supply this matched changed-backend/topology comparison.
Drop old module, SQPOLL and former-CQ component rows: none discriminates
this serving question. Both timers remain60000ns, both ordinary/untraced.
Same model catalogues, weights/KV/precision, packing/prefix policy and wire;
actual concurrent arrival/batch trajectories need not be identical.

Reuse the source-native resident_dispatch.py request/connect functions
verbatim in a necessary standard-library client adapter, as in0029.
Use the same four literal token prompts as0045. Client Job holds no model,
credentials or project PVC; it runs requests only. Application setup/builds/
analysis/server execution happen in the original Workspace. The client is on
a different eligible non-Spark node; the cross-node predicate is a genuine
experimental dependency, not hostname pinning. Discover actual Pod/node/IP/
imageID/route. Existing CNI/overlay/physical carrier remain unchanged.
A disposable benchmark Job and temporary runtime are authorized test-local
steps under spark-manage AGENTS.md8. No retained service or infrastructure delta.

Official metric precedent:
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py
https://docs.vllm.ai/en/v0.31.0/design/metrics/
TTFT, completion, TPOT and output TPS use client-local monotonic start/arrival
durations; no cross-machine clock subtraction. Connection setup precedes
timing. Binary token body in Content-Length HTTP POST, not text/JSON service.

## Fidelity and preflight
Freeze byte-identical0045 whole-output reference sets before outputs: Qwen17
prompt/gen keys22 sequences; Smol17/19. Every warmup/measured reply must match
one exact complete frozen sequence for its prompt/gen, never a tokenwise union,
post-observation expansion or forced serving history. Current ordinary batch/
KV trajectories remain unobserved; no universal correctness or task quality.
Reuse0045 source-identical strict/lifecycle evidence rather than rerunning
unchanged local622-request qualification as another result.

Real preflight on Qwen runs both paths, four cells gen1/64 x c1/8, eight
measured requests/cell and eight checked gen1 warmups per executor.
80 requests/2096 tokens total incl16 excluded warmups. Strace each preflight
server after readiness: loop one steady ENTER, no SQPOLL or steady userspace
accept/read/write/send; native actual epoll/socket mechanism engaged.
Retain EOF/cleanup, original source/counters and exact outputs.
No synthetic probe is substituted for actual model/network preflight.
Allow at most three real preflight attempts; retain failures.

## Full matrix and interpretation
Both models; five paired process blocks, alternating candidate/native order
and rotating all four cells.64 measured requests/cell and eight checked gen1
warmups/executor.20 executors,80 cells,5120 measured requests/166400 tokens
plus160 excluded warmups. Qwen then Smol without own overlaps.
Four primary contrasts: native-minus-loop TTFT gen1/c1 and loop-minus-native
TPS gen64/c8, for each model. Positive favors candidate. Five process blocks
are paired units; nominal two-sided t95 df4 critical2.776445105.
Intervals entirely positive/negative/crossing zero respectively support/
contradict/leave inconclusive that scoped metric. Report all four, every
secondary cell/outlier/failure, no familywide/equivalence/composite claim.
TPOT/completion/pooled nearest-rank p50/p99 are secondary/descriptive.
No per-cell server CPU: remote client clocks cannot bracket server process CPU.
Do not import local CPU means as cross-node CPU measurements.

## Execution and delivery
TEMP=/tmp/bpfusion-optimized-cross-node-nk49zfoa.
Archive=bench/results/optimized_cross_node_20261014.
Build source-native targets:
make vllm-graph-uring-loop vllm-graph-user-network-wait VLLM_PYTHON=TEMP/runtime/bin/python
Server environment common PATH=TEMP/runtime/bin, LD_LIBRARY_PATH temporary
libbpf, VLLM_ENABLE_V1_MULTIPROCESSING=0, BF_BIND discovered concrete PodIPv4.
Candidate attach: build/bpfusion_load stream-uring-attach.
Launch ordinary build/vllm_graph_uring_loop MODEL 300 or
build/vllm_graph_user_network_wait MODEL 300; readiness is actual log.
Use existing Kubernetes owning API kubectl exec client -- python3 -u -
with literal source-native request/client code, fixed cases and matrix.
Save exact client stdin/commands/raw stdout/stderr and normal exit per stage;
stop owned server SIGTERM, wait terminal, inspect ring/native counters and
detach owned BPF. Timing begins only after publication/frozen revision.

Preflight/run adapter and independent analysis reuse0029 plus current0045
source-native client/numerical checks. Scripts are ordinary reproducibility
artifacts, not a new control schema or retained scheduler. Archive code before
serving for review; exact discovered bindings/commands are receipts.
Completion requires every planned row and normal server/client exits, qualified
loop SQ/CQ drains independently, no pending/errors/reservations/drops and
admitted=retired. A failed observation channel is not a benchmark terminal;
inspect same handles and preserve reconnection history. No replacement or
exclusion without an explicit retained deviation and affected rerun.
Full run ends with fresh independent result review, honest docs/main commit/
push, then deletion of owned client Job/runtime/build outputs. Preserve default
library, original Workspace/session/WIP/global caches/base/Coder. Keep original
boot/Pod UID, no own module/pins/GPU app at final endpoint; endpoint checks do
not prove continuous isolation. Record entry/free-space/concurrent-work reads.
Existing gpu-smt and other workloads are outside scope and are not stopped.
Estimated elapsed20-40min dominated by startup, with shared-host uncertainty.
Target table reports candidate/native means and all four primary intervals.
