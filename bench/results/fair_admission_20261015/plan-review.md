# Fair native admission: PLAN REVIEW

**Verdict: ADMIT. No blocking scientific or executability defect found.**

Reviewer: `/root/fair_admission_plan_review`  
Review round: fresh review, round 1  
Reviewed directory: `/tmp/bpfusion-fair-admission-yijz8oui`  
Source parent: `70988bed7d25f313e85277fa420894f1ff835bcf`

This verdict admits the stated comparison to setup, qualification and real preflight. It does not certify an unbuilt implementation or establish a numerical result.

## Scope and method

I read `plan.md`, the exact native diff and complete candidate header, Makefile and current setup bindings, load/client/analysis scripts, qualification, lifecycle, idle, preflight, full and admission-order drivers. I inspected the actual backend’s library selection and upstream graph/history replay, and the prior comparison and integration records.

Inspection occurred through the original BPFusion Workspace. I changed no file and ran no build, GPU workload or publication action. Python sources parse successfully. The private build directory does not yet exist.

The root reported three binding cleanups during this same review. I inspected the current versions: candidate include precedence in setup, lifecycle loader paths, and the copied helper’s otherwise-unused standalone CLI loader paths. These do not change the experiment’s policy, measurement or oracle.

## Admission and research value

The experiment addresses a concrete unresolved explanation: the earlier native competitor admitted eligible requests through FD-order scanning, and saved traces show substantial later-client-stamp bypass at the condition producing the strongest apparent kernel tail advantage.

Reanalysis establishes that concern but cannot measure the counterfactual native FIFO service. A matched new execution therefore adds independent, decision-relevant evidence. This is **supporting work**, with **mechanism/workload-boundary impact**, consistent with the absence of a formal paper RQ or thesis contract.

The outcomes change interpretation:

- A valid advantage supports a bounded service-tail advantage against the stronger FIFO competitor.
- A valid adverse or inconclusive result removes support for a general tail advantage and strengthens the coordination/admission explanation.
- An unengaged or incorrectly implemented FIFO comparator yields an invalid or inconclusive comparison, never a kernel win.

Repeating the obsolete FD-priority native baseline would add little decision value. Another timer or arithmetic experiment would leave the known fairness objection unresolved. The proposed comparison is the strongest justified next measurement.

## Baseline and policy fairness

There is one credible main baseline: event-driven native TCP with eligible-frame FIFO admission and identical resident model computation. No redundant weak baseline is added.

The source implements the declared policy:

- Complete eligible frames enter a deque once per `Peer`.
- Only the deque head obtains the next physical model slot.
- The former FD-order publication scan is removed.
- Existing active-response streaming, framing/rejection, wait behavior and shutdown wakeup remain.
- Pending entries retain their `Peer` object and immutable frame metadata; subsequent receives append input without shifting the queued frame.

The comparison is appropriately bounded. Native eligibility follows readiness observation and its existing one-active-response-per-connection rule; the kernel can admit pipelined frames differently. Native buffering remains uncapped by an artificial new limit, while the kernel has finite admission capacity. These are disclosed system differences. The measured one-request-per-connection workload avoids presenting pipeline-policy differences as an aligned protocol comparison.

Client stamps are correctly described as diagnostics, not exact ingress times. Large bypass or absent waiting-pressure engagement must constrain fairness attribution. A policy label and an executor-wide peak alone cannot prove the amount or duration of queue waiting; the plan already requires interpretation of actual engagement.

## Build and execution bindings

The model constructor, io_uring adapter, BPF programs, admission/page headers and loader snapshots are byte-equal to the current root counterparts. The native diff exactly matches the intended header change.

The current Makefile/setup path:

- Builds into the owned private `BUILD` directory.
- Compiles the candidate model source with the candidate native header.
- Places candidate page/admission include paths before root fallback includes.
- Retains root `vmlinux` and existing upstream bootstrap code.
- Selects the private `.so` through the invoked private executable name.
- Embeds the private BPF object directory through `BF_BUILD_DIR`.

Both compared variants retain packed prefill, prefix release and equivalent trace instrumentation. There is no page ABI or module change requiring another unchanged module-compatibility experiment.

The measured request helper is identical to the archived preceding comparison’s helper. Its instrumentation differences from the older generic `bench/resident_dispatch.py` are inherited partial-error observations, not a newly changed timing definition. Connection and CPU helpers match the authoritative generic helpers.

Setup uses the retained package recipe and checks installed versions against the preceding environment. Actual installation and compilation remain qualification dependencies.

## Metrics, schedules and interpretation

The fixed primary is clear: **per-model kernel-minus-native connect-inclusive TTFT P99 at 96 requests/s**, with five paired nominal t intervals. This is explicitly a new follow-up primary motivated by the old secondary observation; it does not rewrite the preceding 64/s primary.

The workload uses normalized cumulative gamma arrivals, absolute schedules and linear percentiles consistent with the cited [vLLM 0.31 benchmark source](https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py). Its token-ID HTTP endpoint, fresh connections and connect-inclusive primary are disclosed adaptations, so results must retain that wording rather than claim an official endpoint benchmark.

Path order alternates and rate order rotates. Each paired path receives the same normalized schedule. Independent request threads avoid a completion-driven concurrency cap.

Secondary reporting retains median and other tails, completion, scheduled-origin latency, TPOT, delivered throughput, failures, scheduling lag and partial process CPU. Failed primary requests censor superiority. Crossing zero means inconclusive, not equivalent. Adverse results and outliers remain visible.

The plan correctly limits 256-request P99 estimates and five shared-host blocks: they do not establish precise rare-event probabilities, steady-state capacity, exclusive-host latency or total CPU/energy efficiency.

## Numerical oracle and ownership

The traced backend does not accept candidate output as its numerical oracle. After serving, it reconstructs input, positions, padding, block mappings and histories, then independently replays upstream body/head graphs. Subsequent histories use replayed outputs. It also checks physical ownership and ordered release.

The client driver joins references by request marker and checks exact complete bytes or observed error prefixes. The saved-data analyzer checks timing, coverage, counters and references; its CPU replay is correctly distinguished from new GPU numerical execution.

Native lifecycle checks use pre-observation frozen complete-output sets and observed prefixes. They are weaker than a complete trajectory replay and are honestly scoped accordingly.

## FD reuse, queued reset and stop

The FIFO implementation retains `shared_ptr<Peer>` identity across queued and active work. Disconnect sets the old object’s FD to `-1`; a recycled numerical FD belongs to another `Peer`. Queued disconnected objects are skipped, preventing their frame from being served through the new connection.

The page’s `llm_reserved` field aliases the admission word’s high bits. The reservation test and publication therefore protect physical wrap; this is not a missing reservation update.

Retiring a reply releases its model slot and then makes the next buffered frame eligible. Half-close preserves buffered work. Stop closes owned peers and reports remaining deque size.

The plan does **not** claim newly tested cancellation of a large native queued backlog. Full measurement drains before stop, while existing native lifecycle tests cover their retained reset/stop cases. This limitation does not invalidate the requested performance comparison or require a broader lifecycle experiment.

## Runnable matrix and completion

The scripts express the planned stages and accounting:

| Stage | Coverage |
|---|---|
| Qualification | Two native idle cases; both models and paths for protocol qualification; native lifecycle per model |
| Real preflight | Qwen, both paths, 64/256 requests/s, 128 measured attempts plus 16 warmups |
| Full | Two models, five paired blocks, two paths, two rates: 20 executors, 40 cells, 10,240 attempts |
| Full requested output | 655,360 measured tokens plus 160 checked gen1 warmups |

Wrapper and driver terminal records, independent replay, ownership/counter checks, final native deque checks and complete model analyses define completion. The admission-order script can process all full cells separately. No partial prefix qualifies as the experiment result.

Setup/build failure or preflight failure must retain its evidence and follow the plan’s bounded repair rules. Actual FIFO engagement, effective wait behavior and absence of avoidable comparator failure remain execution/result-review questions.

## Required disposition

**Proceed with the reviewed setup → qualification → real preflight → full comparison. No plan revision is required by this review.**

Retain the declared primary, oracle, timeouts, workload and adverse reporting. Any systematic repair affecting a comparison requires the stated deviation record and affected rerun. Final interpretation needs the fresh result review after complete collection. Publication or adoption must not turn qualification success into a performance claim.

Historical memory was used only to orient preservation and the retained objective; current source and evidence inspection supports this verdict.

<oai-mem-citation>
<citation_entries>
MEMORY.md:48-55|note=[retained BPFusion objective and original Workspace preservation context]
</citation_entries>
<rollout_ids>
01a11853-1771-7462-876c-29de77fd8c21
01a1237b-bc13-7d90-a3d1-22ef8fc29d7e
</rollout_ids>
</oai-mem-citation>
