# Plan review: Qwen192 streaming-tail diagnosis and repair

Review observed 2026-10-16 UTC in the original bpfusion-dev Workspace.
Reviewed source parent: main f56d0ee. This is the single fresh plan review
required by the research-experiment-design skill. No production source,
experiment plan, package, service, GPU process or Git history was changed.

## Verdict

**Admit the staged diagnostic. There is no blocking scientific defect in the
stated two-pair timestamp experiment.** The confirmatory repair comparison is
specified as a subsequent stage and is **not yet admitted for collection**:
its actual intervention does not exist yet. The same reviewer should make the
planned focused follow-up on the diagnosed mechanism, concrete frozen diff and
the actual before/after/native bindings before those five blocks start.
This is not a request to delay the diagnostic or to run a broader matrix.

The implemented entrypoints and instrumentation are still being prepared.
This review admits the design, not unseen code or a claim that preflight has
passed. Actual source/commands must be frozen and the stated real preflight
must show the relevant associations and coverage before the full diagnostic.
Failures in that path are executable preflight findings, not grounds to weaken
the completed-output oracle.

## Admission and research value

The retained user question is the complete Linux TCP/eBPF/shared-queue/resident
reused-model/asynchronous-reply service and its throughput/latency objective.
The repository has no formal paper RQ, idea-story, or thesis contract; this plan
does not invent one. The plan is supporting mechanism evidence for that
existing objective.

Finding0065 supplies a real adverse result: the kernel-minus-native mean-block
ITL P99 difference at Qwen192/s is 6.359661 ms, nominal paired t95
[2.113625,10.605697]. The logical histories prove scheduling/correctness but
contain no timestamps that assign the delay to computation, progress polling,
submission, completion or receiving. The existing0057 incomplete profiler
coverage cannot supply that missing attribution. A repeated unchanged timing
matrix or another aggregate CPU counter would not resolve it.

The new information is token/byte-associated stage timing and the opportunity
for a targeted intervention. A successful diagnosis plus a matched repair
would strengthen the practical service argument. A GPU-production explanation,
client boundary, unresolved alignment, or unhelpful repair would retain or
narrow the adverse finding. Both outcomes change the next engineering/paper
decision; this is not a tautological engagement test or another weak positive
control. Prior raw-data stratification is correctly reused first and labeled
post-hoc. The experiment reasonably outranks unrelated backend breadth and
aggregate resource accounting at this point in the user's priority.

A negative outcome bounds this implementation/workload/metric; it does not
alone refute all GPU-owned I/O or the entire research objective. Setup, default8
ordinary-source qualification, cancellation and publication are engineering
dependencies, not independent scientific contributions.

## Baseline, workload and metrics

The efficient native C++ epoll TCP path with the same qualified mixed GPU
constructor is the credible competing mechanism for causal transport
attribution. It can win and thereby falsify a transport benefit. Its prior
published results do not settle this new stage-timing question, so a matched
run is warranted. There is one main baseline; before-fix loop is the
component control for the later intervention.

The user-requested official vLLM server is a legitimate external whole-service
reference, but adding it to this token-associated diagnosis would change the
question and interfaces. Its separate later placement is appropriate; its
absence here does not invalidate this comparison.

Qwen revision, FP16, vLLM0.31.0,16 slots, the four existing prompts, gen64,
normalized gamma arrivals,192/s, checked warmups and unchanged timeouts match
the adverse finite regime. Two alternating paired blocks are sufficient for
mechanism diagnosis, not a fresh five-block superiority estimate. The later
five paired blocks,96/192 rate controls and same improved computation are
adequate for the declared local repair test. No extra models, rates, baseline
families or independent broad experiment are necessary for admission.

The metric convention is already defined in the inherited0065 plan and the
canonical related-work map. I also opened the official
[vLLM benchmark latency definitions](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)
on this review date. TTFT, per-request TPOT, adjacent arrival ITL and their
percentiles must retain the actual client definitions and quantile algorithm
used by0065. The delivered-window TPS definition is local and descriptive,
not silently interchangeable with a different server's throughput window.
The plan retains client lag, scheduled-origin tails, coalesced/zero gaps,
errors and timeouts. Final-versus-interior stratification must retain those
original full-cell numbers alongside the post-hoc subsets.

The primary confirmatory effect, after-minus-before loop block ITL P99 at192/s,
uses process blocks rather than treating individual token gaps as independent
replicates. Nominal paired t95 df4 is a limited finite estimate, clearly
labeled. Native comparison and other tails/throughput qualify any narrower
improvement. No equivalence or production SLO conclusion follows from
crossing-zero intervals or these short runs.

## Timeline validity and causal limits

The plan correctly rejects adding marginal stage P99s to explain the6.36 ms
difference. A quantile difference is not a delay on one representative token.
The useful report is a common set of token/byte intervals for the client tail
events, with stage distributions and representative causal histories, followed
by the separate before/after metric test.

The proposed instrumentation addresses the required boundaries:

- GPU logical production, progress observation and SQE/CQE stamps use the same
  GPU clock and stable request/marker/byte associations.
- Host monotonic send/scan stamps and kernel trace mono timestamps use the host
  domain. Synchronized before/after calibration kernels bracket the cross-clock
  alignment instead of assuming GPU globaltimer equals CLOCK_MONOTONIC.
- SQ publication, actual kernel submission, kernel send completion and later
  GPU completion consumption are separate observations.
- Partial writes and sends covering several tokens are reconstructed by bytes;
  no one-SQE-per-token assumption is made.
- The client receive event is the delivery observation. A send CQE proves
  neither NIC transmission nor client scheduling.
- io-wq, softirq and scheduler events are attribution only where the ring,
  operation and thread lineage establish association. Mere temporal overlap
  or global CPU exposure must remain labeled unresolved.

These choices can distinguish a producer gap from delayed progress/submission
or late consumption without requiring a complete CUPTI kernel census.
Calibration uncertainty, drift, impossible orderings and missing joins must
remain visible. If a boundary is narrower than its alignment bracket, report
a bound or unresolved residual rather than a precise positive/negative stage
duration. A missing field or tracepoint may limit one decomposition without
invalidating same-domain intervals that remain complete.

For actual preflight, inspect complete expected-event counts and stable
operation identity across ring-slot/user_data reuse, completed byte coverage,
GPU trace capacity/overflow indicators, tracefs CPU overrun/drop counters,
and monotonic causal joins. This is execution of the plan's existing coverage
requirements, not an additional performance gate. sched/softirq buffers can
be busy on a shared host; their missing coverage cannot be treated as zero
latency. A private instance avoids interfering with global tracing or another
owner. The bounded adjustment after an observed overflow is an instrumentation
repair, with failed capture retained.

Different GPU/native instrumentation event rates can impose different
overheads. The plan appropriately restricts these traces to mechanism
diagnosis and reserves performance claims for equally BF_TRACE paths without
timeline/ftrace. A stage that looks large under instrumentation becomes a
causal explanation only when associated timing and the targeted intervention
support it. A changed client lag or GPU schedule can remain an alternative
explanation even if transport code changes.

## Correctness, execution and interpretation

Both diagnostic paths retain exact independently reconstructed history and
source-native fresh-attention-metadata replay for every completed trajectory.
The plan does not substitute serving output, loosen token tolerance, expand an
accepted-output pool after observing failure, or weaken full retirement.
Trace/ring/graph errors or unexpected partial outcomes remain failures.
Default8 ordinary cancellation later uses incomplete-prefix semantics without
pretending canceled work is a complete valid response.

The concrete temporary directory, pinned requirements, existing Make recipes,
archive location, diagnostic and independent-analysis entrypoints, real
32-arrival preflight, two full diagnostic pairs and later fixed five-block
comparison make the workflow executable. The exact commands/scripts and
source snapshots are to be frozen before GPU execution as stated. A runtime
failure should be repaired within that admitted path and recorded; it does not
justify dropping a difficult cell or changing an oracle. The full run ends
only after fixed cells, correctness checks, analysis and fresh result review
reach terminal status. No partial prefix is a completed result.

A resource estimate is qualitative rather than a time limit: setup/build,
upstream graph capture and independent replays dominate repeated process
costs, with finite short serving cells. This omission does not invalidate the
scientific comparison and is not a reason to impose an arbitrary budget.

The private builds, preserved main files/WIP/Coder identities and package
state, explicit pin/process/trace-instance cleanup and no-new-service boundary
are appropriate. Commit/push is separately user-authorized; the reviewer does
not perform it.

## Follow-up scope

Before confirmatory collection, append one focused discussion here addressing
the actual observed delay, uncertainty and competing explanation; the precise
repair and unchanged controls; and frozen commands/correctness/metric bindings.
If no concrete valid repair emerges, report the diagnosis and retained adverse
or unresolved result instead of manufacturing a fix. Broader official-server,
complete CPU and remote-load work can then follow the user's order.


## Focused follow-up 1: concrete close-scan candidate

Observed 2026-10-16 UTC. **Admit the fixed before/after/native confirmation
design, after the already planned candidate safety regressions and real
preflight succeed.** No blocking scientific or source-level correctness
defect was found in the proposed intervention. This is the planned first
focused follow-up by the original plan reviewer, not a new experiment or
reviewer reset. It approves neither a speedup claim nor ordinary-source
adoption in advance. A failed, adverse or inconclusive repair comparison
remains a valid possible outcome.

### Evidence and causal discriminator

I read the appended concrete proposal, exact candidate-close-guard.diff,
diagnostic-result.md, diagnostic-result-review.md, connection_progress.json,
the original network close/progress code, actual private fixed_sources and
the ordinary Make build commands/statuses. The diagnostic result review is
the independent result audit of those completed traces; this plan follow-up
does not impersonate a second independent numerical recomputation.

The diagnostic establishes substantial post-production delay, creator-thread
runnable waiting and client receive/recording delay. It does not assign an
exclusive additive share of the historical6.36 ms, and the candidate does
not repair external host runqueue contention, Python scheduling or an unknown
softirq/GIL component. SEND io-wq involvement is absent for the associated
operations, not for the entire service. Client receipt can precede SEND
completion; completion-to-receive is a signed association, not a universally
serial causal stage. The legacy128-record admission sample is truncated;
complete logical/timeline/ftrace joins are the authoritative evidence.

The removable source-level cost is specific: retained EOF/dead connections
independently reload mapped-host admission head/queued values inside every
close eligibility check, even after the scan already knows that admission
has not drained. Only16 active model slots do not bound that connection list.
The two diagnostic peaks are245 and160; the post-hoc progress medians rise
from0.103/0.132 ms at at-most32 inferred connections to0.654/0.527 ms
above128. These strata support a plausible progress-cost candidate, not its
exclusive causal contribution: accepted-minus-closed is an approximation
subject to CQ-consumption lag, and connection pressure can covary with backlog
and time. No per-bin process-level causal inference follows from the many
correlated iteration samples.

The concrete intervention is therefore a reasonable discriminator. It removes
repeated blocked close checks while retaining all safety predicates and
everything else, then tests the actual end-to-end finite metric against its
own unchanged before condition. The single variable is transport close-scan
work; numerical computation is not tuned. A positive primary after-before
effect would support this implementation repair at the tested workload. It
would not by itself measure how many milliseconds of historical6.36 came from
these loads or establish that this mechanism dominates the runqueue/client
delays. A crossing-zero/adverse effect would show that this correct local
optimization has not established the targeted latency benefit; the data must
remain rather than trigger another arbitrary tuning sweep.

### Candidate safety and source binding

The exact diff adds a local tri-state close_ready initialized to -1 for each
io_progress call. A close-eligible connection initializes it using the same
seen/head and stopping/queued predicate as before.

- A cached false skips later close checks during that scan. It cannot
  authorize a close; it may defer one that becomes eligible concurrently.
- A cached true still evaluates the original live seen/head and
  stopping/queued predicate for each attempted close, together with the
  unchanged receive/reply/closing checks. It cannot turn a stale positive
  cache result into an early close.
- The flag is local and resets on the next progress invocation. io_network
  continues calling io_progress; stopping/pending/active termination remains
  unchanged. A one-scan deferral is not a permanent disable or new queue
  admission rule.
- Receive rearm and receive cancellation are unchanged. A connection skipped
  by the false guard is already EOF/dead, so it does not become eligible for
  the live-peer rearm else branch. SEND byte order, one outstanding send,
  FIFO response retirement, buffer lifetime and numerical model execution
  are untouched.

The first true check performs an additional host-load predicate before the
live recheck; at low connection pressure it can add overhead. That is a
reason to retain the96/s condition and adverse results, not a correctness
defect or justification to remove the live check.

The private fixed vllm_graph.cu is byte-identical to the private before mixed
constructor; before Cu is byte-identical to the qualified0065 candidate.
The actual fixed io_uring_tcp.h diff matches candidate-close-guard.diff.
Quoted local inclusion resolves the header beside the copied Cu; ordinary
Make8/16 commands compile that actual source. Both completed build statuses
are exit0. The fixed native compilation may carry the same copied Cu but
does not engage the loop network header; its same numerical constructor
remains the efficient comparator.

These observations do not substitute for the already planned real safety
checks. Candidate default8 ordinary mid-output cancellation, traced8 exact
protocol/lifetime regression and32-arrival real preflight precede collection.
The already completed ordinary baseline cancellation controls qualify the
before path, not the changed candidate. Preserve failures and exact full
history/fresh-metadata oracle semantics. No output-pool expansion or canceled
prefix substitution is permitted. No additional idealized safety matrix is
required by this review.

Before the first candidate GPU preflight, freeze the actual Cu/Py, both
network headers, client, replay/analyzer sources, actual binary/launcher
bindings and runnable command in the archive, as the existing plan requires.
The current review certifies the inspected diff and proposed comparison,
not as-yet-unwritten collection entrypoints. That ordinary source/command
binding is execution work, not a new scientific review round.

### Confirmatory comparison and interpretation

The three conditions are before loop, fixed loop and efficient native, with
the same qualified mixed model constructor, same Qwen revision/FP16/runtime,
explicit16 slots and equal BF_TRACE. Timeline/ftrace is absent. None of the
diagnostic instrumented timing rows enters the confirmatory effect estimate.

The five orders
[before,fixed,native], [fixed,native,before], [native,before,fixed],
[native,fixed,before], [fixed,before,native]
cover five distinct permutations, spread every condition across all process
positions, and keep paired block comparisons. Five blocks cannot give equal
counts at each of three positions; the slight residual order imbalance is a
finite design limit, not a blocker or reason to demand a sixth block. Rate
order alternates by block and remains identical for its three conditions.
Seeds, gamma schedules, timeouts, prompts,256 attempts/cell and8 excluded
checked warmups retain0065 definitions; actual offsets should be compared
during analysis rather than inferred from condition names.

Primary192/s after-minus-before block ITL P99 and nominal paired t95 df4
remain fixed. Fixed-minus-native is reported alongside it; the claim is not
changed to whichever contrast wins. Keep all five blocks, all30 cells,
failures/timeouts/client lag, scheduled-origin latency, TTFT/completion
P50/P95/P99, TPOT and delivered-window throughput. Correlated tokens are not
additional independent replicates. Other tails and throughput can qualify a
narrow improvement, while correctness or unfair comparison invalidates the
affected claim. Different actual batch trajectories may occur and should
remain visible; identical computation source does not promise identical
per-request timing or model invocation sequences.

A supported local effect could justify adopting this small transport change
only after ordinary source integration/regressions, with remaining native gap
and adverse metrics reported. An unsupported effect leaves the overall task
incomplete and the historical adverse result visible. It does not mean the
diagnosis failed, nor that unrelated CPU/client delays were repaired. Complete
resource accounting, sustained remote load, current official vLLM reference
and generic backend work remain subsequent authorized tasks.
