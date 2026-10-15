# Plan review, round 1

Observed 2026-10-15T13:48:50 UTC in the original bpfusion-dev Workspace.
Reviewer: /root/batch_capacity_plan_review, fresh for this plan.
Verdict: **ADMIT for the declared traced capacity experiment.**
No blocking scientific or source-level executability defect was found. This is
permission to proceed under the retained experiment protocol, not evidence of a
speedup, successful build, correctness qualification, or production adoption.

## Evidence and review scope

I read plan.md, the actual candidate8/candidate16 source trees, setup.py and
Makefile bindings, load.py and load.diff, analyze.py and analyze.diff,
protocol_analysis.py and its diff, lifecycle.py and its diff, qualification.py,
preflight.py, full.py, run.py, prior_batch_analysis.py/json, and the ordinary
executor/vllm_graph.py used by the symlinked launchers. I also read current
docs/evaluation.md, finding0063, finding0058, and the current related-work map.
No idea-story or user-instruction document exists, and the retained user
objective is not silently replaced with a formal paper RQ.

Live repository HEAD is fa84cd2289cc904fe446ae066e5ac26334cf2cb2 on main;
git status contains only the unowned tools/setup_env.sh. The candidates and
experiment are private, unbuilt and unexecuted at review time. I performed no
GPU execution, build, source edit, oracle edit, or repository mutation.
All nine reviewed Python entrypoints parse. Re-executing only the saved-data
prior_batch_analysis.py against the complete0063 archive exits0 and exactly
reproduces all40 cell rows/eight aggregate rows in prior_batch_analysis.json.

## Scientific admission and decision value

The eight-bank limit is a concrete, shared constructor limit. Prior saved Qwen
96/s histories really show mean block decode batch7.58655 kernel/7.64931 native
and8759/10630 versus8838/10544 decode rounds at width8. These are event counts,
not time occupancy, saturation capacity, or proof of the dominant bottleneck.
The plan states that distinction correctly.

A fresh capacity intervention supplies information those histories cannot.
Positive, adverse, mixed and inconclusive outcomes lead to different capacity
selection decisions, while the native conditions separate a generic batching
benefit from an eBPF-specific transport advantage. The strongest alternative,
further clock/profiler decomposition after incomplete0057 evidence, might explain
costs but cannot directly establish that this easily identified limit is useful
to change. This bounded intervention is a reasonable next use of the experiment,
not an unchanged retry. Its research role is supporting and its impact is a
constructor/workload boundary; it does not establish a new generic GPU-I/O
primitive or resolve the full retained objective.

There is one main competing mechanism, fair eligible-frame-FIFO native16.
Kernel8 is the existing-capacity control, native8 is the matching capacity
ablation, and the same-width transport contrasts prevent a shared compute
improvement from being claimed as syscall-removal gain. There is no scientific
need to add more external baselines to this specific intervention.

## Source, bitmap, page and build safety

A recursive actual-source comparison finds only BF_LLM_SLOTS8->16 in the
canonical header, plus candidate-specific Makefile path substitutions.
Both native headers exactly equal0063's qualified FIFO candidate.
The candidate8 dispatcher, I/O header, fusion BPF source, loop source, admission
header and loader exactly equal current ordinary source. Thus this does not
sneak in arithmetic, dispatcher, timer, precision, or FIFO changes between widths.

The32-bit reservation bitmap supports sixteen physical bits. Reservation uses
head modulo BF_LLM_SLOTS, 1u shifted by an index0..15, and the combined64-bit
head/bitmap word. Native release and BPF release address bits32..47, within
the64-bit word. Request/reply/control arrays, selection arrays, graph tables,
I/O transmit storage and iteration bounds are capacity-derived. I found no
hardcoded modulo8/index mask in the reviewed changed paths that would silently
alias the second half of the banks.

The larger bf_page is an ABI change. Both map value and mapped allocation sizes
derive from the common struct/mmap macros; setup binds the selected private
header before the root header for CUDA, BPF and loader compilation. The loader's
BF_BUILD_DIR uses the same distinct build8/build16, and launchers choose their
adjacent .so. The Python adapter discovers max_requests() from that library and
derives graph dimensions, allocated KV blocks, physical bank pages and replay
ownership from it. The16-wide case increases graphs, KV, metadata, trace-record
size and resource use; it is not identical executed kernel sequences. The plan
properly says this. No candidate page may be used with an old module; these runs
assert that module absent and use only stock loop/native paths.

These checks establish coherent source bindings, not a successful compiler,
verifier or hardware result. Real preflight must confirm the matching bootstrap,
actual batch widths and free/drained states. Qualification explicitly requires an
observed16-wide compute, rather than trusting the configured constant.

## Workload, metrics and completion

The four-condition rotation and alternate reversal are implemented consistently
in the driver and analyzer. Rate order rotates, schedules are identical relative
to each epoch within a process block, and actual independent threads preserve
scheduling lag and all attempt denominators. Five blocks cannot perfectly balance
four conditions. Transport order is not a full Latin square and is not uniformly
balanced; shared-host temporal drift remains a limitation, especially for small
secondary transport contrasts. This does not invalidate the primary capacity
comparison or justify changing the design after seeing outcomes.

The primary is fixed independently for each model: delivered output token/s at
192/s, kernel16 minus kernel8, five paired blocks and nominal t95df4. The analyzer
computes the stated sign and interval and marks all primary failure censoring.
Its denominator includes the finite scheduled arrival window and trailing work;
it is delivered-window TPS, not steady saturation capacity. Request TPS is
redundant when every request has64 output tokens but harmless as an interpretable
secondary. Crossing-zero intervals are inconclusive, not equivalence. Any failed
primary attempt prevents a complete-delivery superiority claim. All native and
adverse secondary rows must remain visible.

I inspected the cited official
[vLLM v0.31.0 benchmark source](https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py),
which defines throughput and client latency summaries. The plan correctly labels
the token-ID adapter, connect-inclusive timing and custom finite execution rather
than presenting it as the official text/API benchmark. Tail estimates from256
requests/cell are sparse; neither precise P99.9 nor production SLO evidence follows.
Process CPU remains a partial accounting bracket.

The full arithmetic is correct: two models x five blocks x four conditions x
two rates =40 executors/80 cells/20,480 measured attempts/1,310,720 requested
measured tokens, plus320 gen1 warmups. The actual command sequence and terminal
records are executable in principle and retain failed runs. Preflight is real
Qwen through all four conditions, not generated data or a toy model.

## Independent fidelity and lifecycle scope

Traced qualification and full performance use actual transport outputs matched
by client marker to independent upstream graph/head replay. The replay rebuilds
inputs and positions from prompt plus its own prior replayed outputs, derives
invalidity from configuration/vocabulary, preserves physical-bank ownership,
and compares numerical tokens with every candidate compute event. Candidate
tokens do not become the next reference history. Reusing the recorded batch
schedule is trajectory matching, not circular expected-token construction.
Wire responses then equal those complete references; failed partial responses
retain prefix checks and failure denominators.

The16-bank protocol counts are internally correct:1284 outcomes,515 intended
rejects and47,200 checked tokens per executor, four protocol executors total.
The numeric slot sorting and modulo-bank ownership checks are adjusted correctly.
The bounded128-reply diagnostic is distinct from numerical BF_TRACE overflow:
trace_count=head with trace_overflow=max(0,head-128) is appropriate for that
diagnostic and must never excuse loss of model histories.

Ordinary lifecycle exercises a different, untraced evidence contract. Its native
32-action scope remains narrow. Loop arithmetic is144 actions/78 connections:
31 initial actions,48 queued-reset frames, one recovery action, and64 stop
clients. The >16 queued-state checks and head+remaining-queued accounting are
coherent. Observed prefixes use the historical complete-output pool; canceled,
unobserved frames are explicitly not full numerical checks.

**Important nonblocking scope correction:** requiring this ordinary frozen-pool
membership to pass before a separately traced full comparison is not scientifically
necessary for the declared primary. Finding0058 already documents an outside-pool
ordinary response with unresolved coverage/correctness ambiguity. A new16-wide
trajectory can have the same ambiguity; a finite historically8-wide pool cannot
become universal merely because it was frozen.

I recommend separating ordinary adoption qualification from traced experiment
validity before execution. Preserve the exact lifecycle observations and oracle;
do not enlarge its pool, relabel an unqualified response as passing, or promote
the candidate to ordinary defaults on that basis. A mere outside-pool observation
does not by itself invalidate independently replayed traced histories. Conversely,
actual transport/accounting/resource corruption should be diagnosed and cannot
automatically be dismissed as pool ambiguity. The current stricter stop-on-any-
qualification-failure sequence can only make the planned study incomplete; it
does not convert failure into valid negative throughput evidence. This is not a
request for a weaker numerical oracle or more lifecycle experiments.

## Return to implementation owner

Proceed with this supporting traced capacity comparison under the fixed plan,
including actual mechanism engagement, complete failures and fresh independent
result review. The ordinary-lifecycle scope separation above is a recommended
pre-observation plan/runner cleanup, not a requirement to change the numerical
oracle or production source. No additional baseline, model, setting, test suite,
permission gate, infrastructure object or reviewer reset is requested.

A successful private BF_TRACE result can justify further compatibility/adoption
work. It cannot by itself select sixteen ordinary banks, prove an untraced
speedup, establish a general eBPF benefit, or complete the broader serving goal.


## Follow-up 1 — pre-execution order and lifecycle separation

Observed 2026-10-15T13:51:19 UTC. This is the same reviewer and discussion,
not a new review round or reset. Verdict remains **ADMIT**.

The owner repaired the originally incomplete order counterbalance before any
execution. load.py, analyze.py and protocol_analysis.py now use the same
four-condition sequence modes[(j+pair)%4] with j=(0,1,3,2); the two-mode protocol
case retains simple alternation. I independently enumerated the five orders:
[0,1,3,2], [1,2,0,3], [2,3,1,0], [3,0,2,1], [0,1,3,2]. The first four place each
condition in every position once; every pairwise precedence count across five
blocks is either2 or3. This supersedes the round1 description of the former
rotate/reverse imbalance. Five-block precision and shared-host drift remain
limits, but the avoidable systematic transport-order weakness is repaired.

The plan now separates fixed untraced lifecycle outcomes from traced numerical
validity. qualification.py retains four ordinary lifecycle records while requiring
both model protocol driver/analysis pairs to pass; it checks retained serving
resources before advancing. run.py now ends after setup, real preflight and
qualification, with expected3 stages. The owner interprets actual lifecycle
outcomes and diagnoses transport/resource faults before separately invoking
full.py. Thus all.exit.json from this first wrapper is expressly not full-matrix
completion. The full driver, complete raw results, upstream replays, analyses
and fresh result review still must reach terminal independently.

The lifecycle source itself retains its reviewed build16 binding,144-loop-action/
78-connection arithmetic and unchanged frozen membership oracle. A recorded
pool miss stays unqualified ordinary evidence; no weaker oracle, candidate-derived
reference, favorable rerun or ordinary-default adoption is introduced.

One nonblocking execution precaution was sent to the owner before launch:
qualification.py at inspection continues even after a nonzero ordinary lifecycle
subprocess exit. A handled pool assertion normally returns exit0 plus passfalse;
an unexpected nonzero may indicate a cleanup/communicate exception, potentially
leaving an executor after pins disappear. Stop for diagnosis on nonzero lifecycle
driver exit while preserving exit0/passfalse outcomes for interpretation. Pin
absence alone should not be treated as proof that an unexpectedly failed
subprocess left no GPU executor. This does not change the hypothesis, oracle,
workload or candidate source.


## Follow-up 2 — final execution precaution resolved

Observed 2026-10-15T13:52:31 UTC. Same reviewer, same discussion; final verdict
**ADMIT**, no remaining blocking item.

I inspected only the requested correction. qualification.py now contains exactly:

```python
if x['exit'] or (name.startswith('protocol_') and x.get('analysis_exit',0)):break
```

Thus any nonzero ordinary lifecycle subprocess exit stops the sequence for
diagnosis; protocol analysis failures also stop it. Handled exit0/passfalse
ordinary outcomes remain preserved for owner interpretation before the separately
invoked traced full matrix. The plan records this distinction, qualification.diff
exists, and the actual qualification.py parses. This resolves the execution
precaution recorded in follow-up1 without changing the numerical oracle,
hypothesis, candidates, workload or primary interpretation. No broad rereview,
GPU execution, build or source modification was performed by this reviewer.
