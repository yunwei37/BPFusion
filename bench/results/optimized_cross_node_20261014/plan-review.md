# Optimized module-free cross-node serving: fresh plan review

## Verdict

**ADMIT.** No scientific or executability defect requiring a plan revision was
identified in the current plan and available client/analysis artifacts.
Proceed through the declared real cross-node preflight, then the complete
matrix if that preflight qualifies the actual candidate and native paths.
This is a supporting serving comparison, not a performance result or proof of
the full project objective.

Reviewed on 2026-10-14. Current production main observed as
bd39e59e4e5f27b5ac72313795d5ea77d3ef4d82. Source review was read-only;
no model execution, setup, source/plan editing or infrastructure mutation was
performed. The only written artifact is this report.

## Question, admission and independent evidence

The retained question asks whether removal of the steady userspace request
worker improves client latency or throughput over efficient native networking
on a real cross-node path with identical upstream GPU computation. The proposed
two-model, two-path comparison directly addresses that relation.

Finding0029 already supplies an inconclusive real cross-node comparison, but
its captured HF backend and module TX differ from the current optimized
packed/prefix vLLM computation and module-free loop. Finding0030 localizes
the older profiled HF short-input span and cannot attribute latency in the
newer unprofiled backend. Finding0035 provides optimized ordinary local
delivery; findings0044 and0045 provide module-free loop local comparisons,
CPU scope and negative/inconclusive performance boundaries. None can be
reanalyzed into the proposed changed-backend cross-node measurement.
Subtracting their means would not produce a matched network-overhead estimate.

Successful cross-node delivery would close a concrete acceptance gap.
Native winning or intervals crossing zero still changes the serving boundary:
the current module-free implementation would remain qualified but lack the
claimed finite-workload latency/throughput advantage. This is decision-relevant
supporting evidence, not a redundant repeat of unchanged local timing or a
dependency-only readiness check.

The plan weighs current-backend stage profiling as the strongest alternative.
That would provide attribution, but cross-node delivery is a stronger immediate
end-state acceptance question after the local mechanism interventions.
Admission does not imply that another inconclusive matrix warrants indefinite
repetition. Preserve the stated closure of unchanged timing.

## Baseline and comparison fairness

Efficient native TCP with timed epoll is the sole main baseline and a credible
competing answer: retain userspace networking while sharing the same optimized
resident GPU model computation. A matched run is necessary because the client
topology, backend, arrival pattern and completion path differ from the
available historical evidence. A native win directly bounds the performance
claim. Additional module/SQPOLL/old-CQ rows would be component controls and are
not needed for this question; dropping them is appropriate.

The current Makefile applies BF_PAD_PREFILL and BF_PREFIX_RELEASE to both
vllm_graph_uring_loop and vllm_graph_user_network_wait, with the intended
transport flags. Both ordinary paths are untraced during timing. Existing
source keeps the loop multishot timer and native completion-poll interval at
60000 ns. Equal nominal periods do not make their wake policies identical;
the experiment measures the implementation alternatives, not exclusive
causation by eBPF, syscall removal or a single polling factor.

The native alternative must engage actual epoll/socket processing, and the loop
must retain no SQPOLL and the qualified steady single ENTER with no steady
userspace socket processing. These engagement checks are explicitly assigned
to the real preflight. Prior strict/lifecycle qualification may be reused
because production source and computation remain unchanged. It does not
replace the actual cross-node preflight.

Model weights, revisions, FP16/KV, prompts, computation, wire and budgets are
matched. Different real arrival/batch/cache trajectories are permitted and
honestly disclosed. This is not a full vLLM server or external SOTA comparison:
it is a binary-token Content-Length HTTP adapter sharing upstream computation.
Do not describe the result as text/JSON service, arbitrary-model portability,
ordinary vLLM serving superiority or full CPU-path elimination.

## Numerical fidelity and finite scope

I independently verified that the new frozen_references.json is byte-identical
to the0045 asset. Its two model assets retain17 prompt/gen keys each, with
22 complete Qwen sequences and19 complete Smol sequences. models.json uses the
same exact model records, and each of the four literal prompts has both gen1
and gen64 references.

The client checks membership of each whole reply in the frozen set for its
exact prompt/gen. The analyzer independently repeats that check for measured
requests and warmups. No post-observation expansion, tokenwise union,
prefix-only long-reply acceptance or forced serving-history oracle occurs in
the available adapters.

This proves only finite previously qualified output-set agreement. As the plan
states, current ordinary batching/KV history remains unobserved; returning
another previously valid sequence could pass. It does not establish exact
current-batch replay, deterministic equivalence between transports, universal
numerical correctness, task quality or general input support. That limit
does not invalidate the declared serving comparison when retained in reporting.

## Metrics, repetitions and interpretation

The cited official vLLM0.31 metric documentation and benchmark source are
accessible:
- https://docs.vllm.ai/en/v0.31.0/design/metrics/
- https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py

The client records request send-start and first/last complete-token receive
arrival on one monotonic clock. TTFT, completion and TPOT are then direct
durations with no cross-machine subtraction. Tokens in the same recv share an
arrival time, so TPOT/quantiles describe delivery and coalescing, not individual
GPU token timestamps. Throughput is completed output tokens divided by the
observed client interval from earliest measured send-start to latest token
arrival. These are standard metric classes, but this finite closed-loop
persistent-connection protocol is not numerically interchangeable with the
official vLLM streaming/text benchmark workload.

The adapter request() and connect() functions were independently verified
byte-verbatim against current bench/resident_dispatch.py. Connection setup and
thread creation precede measured request timing. At concurrency8, a ready/start
barrier releases all lanes, each traversing its predetermined request indices.
Four cases are balanced and count64 is divisible by8 and4.

Five paired process blocks, alternating transport order and rotating cells,
are reasonable for this bounded comparison. The analyzer computes paired
process-block mean differences, standard deviation and nominal t95 df4 with
critical2.7764451051977987. Its directions match the plan: native-minus-loop
TTFT and loop-minus-native TPS. It reconstructs arrivals, output TPS,
request-index/case coverage, warmup count and normal executor/client terminals.
The predeclared four primaries are gen1/c1 TTFT and gen64/c8 TPS, for each model.
Other cells, completion/TPOT and nearest-rank quantiles are secondary or
descriptive; all negatives/outliers remain reportable.

Four nominal intervals are not familywide confirmation, proof of equality or
an equivalence test. Crossing zero is inconclusive, not zero effect. A favorable
secondary cannot override unfavorable/inconclusive primaries. Correctness or
mechanism/fairness failure can invalidate a comparison and must not be counted
as a method win.

The planned counts reconstruct: preflight64 measured requests/2080 output
tokens plus16 one-token warmups totals80 requests/2096 tokens. Full20 executors
and80 cells yield5120 measured requests/166400 tokens plus160 excluded checked
warmups. Separate local CPU values must not be relabeled cross-node server
CPU. This plan correctly omits per-cell remote process CPU and total
CPU/energy claims.

## Execution and resource preservation

Available client.py, analysis.py, models.json, owner.json and frozen references
exist both in the owned temporary directory and experiment archive.
The client is an ordinary necessary standard-library adapter; the analysis
is an adaptation of the existing0029 direct reconstruction. No retained runner,
new control schema or scheduler is introduced. Runtime/build/Job creation and
discovered address/placement remain execution/preflight tasks.

Manual orchestration through the existing owning kubectl API is executable
with the declared source-native commands and literal client stdin, provided
each actual binding, invoked stdin, stdout/stderr and real process/client exit
is retained as the plan already requires. A command receipt or client-written
terminal event alone is not the owning API exit; save both. Neither an SSH
observation failure nor a management timeout establishes benchmark termination.

The source supports concrete IPv4 BF_BIND for the listener. request.client_ns
is preserved as a correlation field; client timings do not subtract it from
server/GPU clocks. The source's module-free loop branch enters uring_wait and
drains via uring_quiesce/uring_drain/uring_finish; native engages user_network.
Normal model completion reports admitted/retired and graph errors. Loop RESULT
reports completion/head, pending/error/reserved/dropped/overflow, connections
and ring indices; SQ head/tail and CQ head/tail must balance independently,
not be forced equal across SQ/CQ. The plan already correctly specifies this.

A client Job with no model, credentials or project PVC on a different eligible
non-Spark node is a real cross-node dependency. Excluding the server's actual
Workspace node through discovered workspace identity is justified for that
predicate; hostname pinning or a new persistent topology is not needed.
Actual Pod/node/IP/imageID/route receipts must establish the client placement
and topology before counting cross-node delivery. No continuous-isolation claim
follows from endpoint GPU/boot/Pod checks. Existing unrelated workloads remain
outside scope.

Setup/builds/analysis/server execution stay in the original project Workspace.
Owned Job/runtime/build cleanup must preserve default library, model caches,
base environment, original Coder/session/WIP and source. These are appropriate
restoration obligations; setup and cleanup are dependencies, not independent
scientific results.

## Final disposition

Proceed with the declared real preflight and complete the admitted integrated
matrix on the unchanged comparison if it passes. No additional baseline,
workload, tracing campaign, source tuning or plan round is required by this
review. Record discovered runtime/topology and genuine execution deviations;
rerun affected comparisons only when a deviation invalidates them. After all
rows reach authoritative terminal state, use the skill's fresh result review
to judge correctness, engagement, raw reconstruction and all four primary
intervals without a desired verdict.

Admission is limited to this supporting finite-topology serving question.
The full Linux TCP/HTTP, resident inference, general server architecture and
performance objective remains open beyond this experiment.
