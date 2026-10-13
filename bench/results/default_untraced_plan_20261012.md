# Experiment plan: ordinary untraced optimized serving

## Retained question and admission

No formal paper RQ/thesis exists; preserve the retained full Linux TCP/HTTP →
eBPF/shared queue → resident real-model GPU inference → kernel TCP TX objective.
Question: what client latency/throughput does the ordinary packed/prefix adapter
deliver against the efficient native network alternative after BF_TRACE is
removed? Does the current matched untraced transport comparison favor the
kernel path in gen1/c1 TTFT or gen64/c8 throughput?

Role: supporting serving comparison with integrated adoption qualification,
not a new headline/novelty result. The current source is main bd6a0a0.
Finding0034's completed four-policy matrix qualifies traced integration and
publishes the new default, but its timing cannot establish untraced performance.
Its untraced checks are only c1. No existing raw can be reanalyzed into absent
untraced dynamic client arrivals. Success permits a bounded ordinary-default
performance statement; negative/mixed results bound the transport benefit and
close this unchanged ordinary comparison. Neither proves equivalence, SOTA,
total service CPU, arbitrary models or task quality.

Strongest next alternative is full-service CPU attribution/physical delivery
or an optimized host-driven scheduler comparison. Those could be consequential,
but cannot supply the absent ordinary-default measurement. An unchanged traced
matrix is redundant. This run first closes that implementation/measurement gap;
do not claim build/check/archive count as scientific progress.

## Assets and fairness

Reuse current unchanged native/backend source, existing official vLLM0.31.0
FULL model/head/greedy sampler catalogue, Torch2.13.0+cu129 and Transformers5.17.0,
both cached pinned model revisions, original RTX5090/kernel7.3rc3 Workspace.
Same eight-slot KV budget, FP16, packed prefill, prefix release and default TCP.
Compare ordinary vllm_graph vs vllm_graph_user_network_wait, both without BF_TRACE.
The native60000ns epoll control is the strongest existing matched networking
alternative; it is a mechanism control, not an external SOTA server baseline.
Bodies/head/sampling/math and request budget are identical; actual scheduling
can change tensor shapes and FP16 greedy trajectories.

Temporary runtime: /tmp/bpfusion-untraced-oli4icwu/venv. Initial ordinary venv attempt fails because
the base image lacks ensurepip, before serving. Reuse the previously validated
official python3 -m venv --without-pip plus python3 -m pip --python ENV/bin/python
installation, preserving the original base runtime. Archive both setup records.
No infrastructure/runtime setting, model math, BPF/module or wire delta.

## Fixed numerical and lifecycle check

Before any new serving output, freeze /tmp/bpfusion-untraced-oli4icwu/frozen_references.json from all
existing finding0034 strict/performance independent reference files at bd6a0a0.
Qwen has17 prompt/gen keys and22 distinct complete sequences; Smol17 keys/19.
Each earlier reference independently advances its own upstream history without
served-token teacher forcing and passed complete client/trace reconstruction.
Current native/backend code equals the qualified sources. The frozen asset
records all contributing source paths, precision/model identity and the narrow
reference scope. Archive it before running.

Every valid untraced response must match one complete frozen sequence for its
exact prompt and generation length; invalid replies use the unchanged EOF/400
protocol. Do not add variants after observing this experiment, use tokenwise
mixtures, adjust tolerance or force the oracle from served histories.
A novel sequence fails this fixed qualification; preserve the raw and stop
performance promotion. A new legitimate FP16 trajectory is not automatically
a model or transport fault. Membership establishes qualified complete-output-set
fidelity, not replay of the current unobserved batching trajectory or universal
numerical equivalence. This explicit limit remains even if every request passes.

Before full timing run, real preflight exercises both ordinary transports and
both gen1/64 and clients1/8 for Qwen (8 measured requests per cell,8 warmups).
Then full strict622-request protocol on both architectures/transports checks
fragmentation,block/prompt edges,invalid IDs,wrap/reuse,mixed1/64,pipeline/
half-close,binary rejection/subsequent valid generation and helper-thread stop,
with all-thread after-ready network traces and terminal page/aggregate counters.
Total strict2488 requests/88896 tokens/1036 intentional rejects/20000 empty connects.
No per-step GPU trace is generated. max_active/counters are executor aggregates;
do not invent per-cell batching/release trajectories.

All actual valid bytes, input/length, membership checks, HTTP status, errors,
admitted=retired/published=completed, kernel reserved0/eight FREE and clean
module/pin/process teardown are necessary validity evidence. The strict source
and driver changes are ordinary existing benchmark adaptations, not new
control interfaces or a new service.

## Workload and effect

Reuse the existing four real prompts, output1/64 and closed-loop clients1/8.
Five alternating process pairs per model,64 requests per cell plus8 excluded
gen1 warmups per executor. Full scope:20 executors/80 cells/5120 measured
requests/166400 tokens plus160 checked warmup tokens. Two cached architectures;
same native clients,request wire and algorithms. Capture/init/connections outside
client timing; retain every process/block/sample/outlier.

Primary user-minus-kernel gen1/c1 mean TTFT and kernel-minus-user gen64/c8 TPS,
separately per model. Five process blocks are independent paired units;
nominal two-sided t95 df4. Interval wholly positive supports that bounded gain,
wholly negative contradicts it,including0 is inconclusive; report mixed cells
without a universal/equivalence claim. All other TTFT/completion/TPOT/TPS and
finite sample p50/p99 remain descriptive/secondary; they veto only correctness
or fairness. No CPU/energy quantity is invented.
Definitions: [vLLM metrics](https://docs.vllm.ai/en/v0.31.0/design/metrics/) and
[official client benchmark](https://github.com/vllm-project/vllm/blob/main/docs/benchmarking/cli.md).
Client token arrivals include send/TCP/polling/coalescing. They are not GPU-ready
timers. Do not subtract earlier traced means to claim a causal tracing speedup.

## Executable workflow

Minimal existing-driver additions: --untraced --reference-path FROZEN and
--preflight; native/backend production source unchanged. The untraced analysis
checks all request bytes against the frozen complete set and actual logs/counters,
then reuses existing metric/pair formulas. Preserve old traced archive analyses.
Build make VLLM_PYTHON=/tmp/bpfusion-untraced-oli4icwu/venv/bin/python vllm-graph vllm-graph-user-network-wait.
Use current pinned model paths from the frozen asset.

With PATH=/tmp/bpfusion-untraced-oli4icwu/venv/bin:$PATH, VLLM_ENABLE_V1_MULTIPROCESSING=0 and existing
HF_HOME=/workspaces/.cache/huggingface:

    python3 bench/vllm_serving.py --untraced --reference-path /tmp/bpfusion-untraced-oli4icwu/frozen_references.json --preflight --model QWEN_PINNED_PATH --output /tmp/bpfusion-untraced-oli4icwu/preflight.jsonl
    python3 bench/vllm_serving.py --untraced --reference-path /tmp/bpfusion-untraced-oli4icwu/frozen_references.json --correctness --model MODEL_PINNED_PATH --output /tmp/bpfusion-untraced-oli4icwu/MODEL_correctness.jsonl
    python3 bench/vllm_serving.py --untraced --reference-path /tmp/bpfusion-untraced-oli4icwu/frozen_references.json --model MODEL_PINNED_PATH --output /tmp/bpfusion-untraced-oli4icwu/MODEL_performance.jsonl
    python3 bench/vllm_serving_analysis.py RAW

Run both model strict/performance stages to terminal only after preflight passes
and fixed checks work. Wait same handles; retain any failed/incomplete prefix.
Actual scripts/commands/source snapshots and statuses are recorded before
serving. Durable archive bench/results/default_untraced_20261012/. No arbitrary
wall budget or replacement of live processes. The existing bounded seconds
argument remains a benchmark parameter,not a new persistent policy.

Fresh plan review precedes serving; fresh combined result review independently
checks all completed raw/metrics/source/frozen-output checks and limitations.
Retain bounded host journal,co-tenant/endpoint evidence and uneven exposure,
not clean-host assertions. After review/archive,remove only owned runtime/build/
process/module/pins and verify original Workspace/base/session/caches/WIP.
Publish own validated main paths and honest finding/evaluation/README status.

## Real preflight implementation repair

The first kernel preflight executor stops normally and all40 requests/1048
tokens pass fixed membership and terminal counters/page checks. The driver
then fails before the native condition on a retained traced-only log variable:
batches was undefined in the untraced branch. Raw/status/source remain under
preflight. Set the log field explicitly to None (batch trajectories unobserved)
and rerun the whole preflight as preflight_retry1. No model/transport/checker/
reference/cell/timing change. This is a runner repair before any full timing.
