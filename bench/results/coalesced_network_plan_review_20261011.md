# PLAN REVIEW: coalesced native network comparison

Reviewer: /root/coalesced_network_plan_review. Read-only independent review,
returned2026-10-11 around08:02UTC. Source HEAD6688caf879ca2cdc53de5336df10aca6eca6b540.

Verdict: admit the declared supporting engineering comparison. No scientific or
executability blocker identified. Full collection remains conditional on four
strict regressions, passive diagnostics, committed source freeze and two real
preflights; the review does not treat these dependencies as already complete.

Reviewed the actual plan, bench/resident_dispatch.py, tests/resident_qwen.py,
both transport diffs, bench/tcp_stream_trace.py, docs/evaluation.md,
findings0018/0025 and native build/loader interfaces. Graph computation and
benchmark measurement sources had no diff. Qualification wrapper79516 was live;
Qwen kernel case2 exited0 and final Qwen user case3 was running during review.

## Admission and hypothesis

The new question asks whether kernel request/reply improves latency or throughput
after both paths coalesce the HTTP header and first tokens. Finding0025 cannot
answer that condition because both previous transports retained the plateau.
Changing the sending mechanism adds evidence beyond an unchanged repeat.

Positive, contradictory and inconclusive outcomes lead to distinct engineering
decisions. The absence of a formal paper RQ is acknowledged rather than repaired
by inventing one. Admission applies to the retained engineering objective and
supporting evidence, not a paper headline, SOTA, novelty or causal coalescing gain.

## Fairness and mechanism

The native control is a component ablation, not an external main baseline. It
uses identical resident GPU computation and captured FP16 HF graphs, without
a deliberately slow Python token loop. This is consistent with Blink's
same-engine orchestration comparison:
https://arxiv.org/html/2604.07609v1

Both source changes wait for available token bytes before sending valid headers,
submit remaining header/body in one vectored send, and account for partial
returns separately. Rejection, final-token withholding until DONE, and slot
release ordering remain intact. No server NODELAY/QUICKACK, math or measurement
change. Polling and page backing differ, preventing syscall-only attribution.
The measured closed-loop workload has one outstanding request/connection, so
different pipeline admission policies do not invalidate this matrix.

Strict regressions adequately qualify the measured small responses. They do not
establish exhaustive partial-send/backpressure or overload robustness; broader
claims must remain absent. Passive metadata/observer scheduling permits mechanism
diagnostics, not GPU-ready timing or causal speedup claims.

## Execution and correctness

Exact commands match native parsing. --user-network-executor selects the intended
control. Native execution provides5 paired blocks, alternating transport order,
rotated matrix order,4 workload cells,64 measured requests/cell and8 excluded
warmups/process. Totals80 cells/5120 measured requests/166400 measured tokens/
20 executor exits are consistent.

Native checks cover exact tokens, resident/graph launch counts, graph errors,
user publication/completion and cleanup. Independent result reconstruction is
still required for kernel counters, all metrics, coverage and final state.
The eager HF oracle is separate from the serving executor and unchanged.
sendto->sendmsg updates positive syscall instrumentation, not numerical checking.

## Measurements and interpretation

Client TTFT/TPS address the question. TPOT=(completion-first arrival)/(tokens-1)
matches the official vLLM implementation:
https://docs.vllm.ai/en/latest/api/vllm/benchmarks/serve/
TPS uses first measured request start through last measured token arrival;
preserving this window makes the comparison reproducible.

Five paired estimates with nominal t95(df4) intervals suffice for the limited
descriptive inference. The plan avoids family-wide significance, equivalence
from crossing-zero intervals and strong P99 claims. Shared GPU interference,
sequential blocks, token co-arrival and CPU attribution limitations are disclosed.
This supports only the new kernel-versus-user condition. Historical finding0025
numbers cannot identify a causal coalescing effect.

## Optional suggestions, not blockers

1. Archive four diagnostic commands and native --analyze commands.
2. Reconcile docs/evaluation.md's prior matched-before/after next decision with
   this distinct optimized comparison; keep causal optimization measurement open.
3. Publish paired primary effects alongside pooled summaries.

No extra baseline/model/runner/configuration layer or repeated unchanged
experiment is required. No follow-up review or required repair.

## PLAN REVIEW follow-up1: atomic admission repair

Returned2026-10-11 around08:50UTC by the same independent reviewer.
The hypothesis and matched comparison remain admissible, with two required
executability repairs before collection: the legacy CPU bridge advances seen
when a newly reserved request is not yet PENDING, and both amended preflight
commands still reuse occupied JSONL paths opened with mode x. Graph consumers
already wait for PENDING, so the bridge defect does not invalidate graph-only
qualification; those runs cannot establish historical bridge compatibility.

The admission CAS updates low32 head and high32 physical-slot ownership together.
A paused producer cannot be overwritten on wrap. Recycle occurs only after old
slot accesses and FREE, and clears only its bit, preserving head and other
reservations. Capacity and bounded contention remain; no lossless-overload claim.
Admission offset12848 and ring offset12856 and page size are unchanged. Native
user control remains a single producer with its historical publication order.

Actual x86 ordering is sufficient: matching kernel arch_atomic64_and uses locked
andq with compiler memory clobber, and built module stores FREE before that
locked clear. Generic atomic64_andnot is relaxed; atomic64_fetch_andnot_release
would express ownership release portably. This recommendation does not invalidate
the inspected x86 run; if applied, requalify that module before full collection.
The bridge mask/libatomic are present but need an actual native call and delayed
publication qualification.

Reviewer independently extracted1536 identical dispatcher SASS instruction/
encoding rows across both frozen00d8ae3 libraries and both repaired libraries.
No diff to tests/resident_qwen.py, bench/resident_dispatch.py, qwen_graph.py or
qwen_graph.cu: numerical oracle, model arithmetic, GPU dispatcher, timeouts,
matrix and estimator remain unchanged. Failure receipt independently retains
TimeoutError and one admission refusal at head72/WRITING/head_changed0. This
supports the investigated window without proving exhaustive failure causality.
Do not stitch the failed prefix into the repaired matrix or interpret this as
causal coalescing speedup. Fix required items, retain failures, qualify and run
fresh preflights, then collect the unchanged complete matrix.

## PLAN REVIEW follow-up2: final disposition

Returned2026-10-11 around08:59UTC by the same reviewer. Admit amended experiment:
no remaining scientific/executability blocker. Bridge waits through FREE/
WRITING, retains exactly-once seen advancement after finish/recycle at line226.
The intermediate missing-increment alert was factually incorrect and withdrawn.
Fresh retry1 preflight paths were verified absent. Explicit
atomic64_fetch_andnot_release expresses ownership release portably.

Existing qwen_kernel_tx.py checks actual bridge TCP in user/kernel modes,
24 successive exact replies each, three lengths and slot reuse. Temporary
actual-main real-Qwen diagnostic checks delayed head-before-PENDING publication,
eight exact tokens and native Page.recycle preserving head/another reservation.
This is a focused compatibility dependency, not exhaustive race proof or a
resident-GPU performance result. At review time earlier cases0-3 and rebuilt
Smol kernel rerun were terminal0; wrapper86759/Qwen and bridge tests remained
live/pending. Fresh preflight/full results were still uncollected.

Oracle, benchmark, GPU code, matrix/timeouts/effects remain unchanged. Previous
1536 identical SASS rows still apply to unchanged graph binaries. Recollect the
complete80-cell matrix on frozen repaired source; keep failed prefix separate
and avoid causal coalescing claims. Six production files coherently define,
reserve, release and observe ownership without changing layout. Removing a
producer/releaser update reopens ownership errors. Loader's one existing-path
reservation diagnostic is useful; no material reduction warrants reopening the
repair. No production test framework/persistent helper/map/service/control
interface was added. Complete current qualification and fresh preflights, then
publish/freeze source before unchanged full retry.
