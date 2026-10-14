# Independent plan review: batched queue publication

Reviewed 2026-10-14 in the original yunwei356/bpfusion-dev Workspace.
Round 1; one reviewer; no experiments executed, source/plan edits, publication,
or additional agents. Report home: this file.

## Judgment

**ADMIT as a supporting real-serving driver experiment.** No scientific or
executable defect in the proposed design requires closing this proposal.
Admission is prospective: at inspection, production source still implements
the unbatched policy, the temporary runtime is not yet present, and there are
no candidate/preflight results. This review does not certify an unimplemented
policy, a build, correctness, or a performance result. The ordinary preparation,
source freeze and real qualification already required by the plan remain.

## What was independently inspected

Read plan.md, current executor/io_uring_tcp.h, the captured CUDA dispatchers
and Makefile, run.py/setup.py, Makefile.original/rebuild_original.py,
matched_serving.py, analysis.py, qualification.py/run_qualification.py and
lifecycle.py/run_lifecycle.py. Read finding0030 and the current evaluation
history through completed0050. Git is main and the only dirty item observed
was unrelated tools/setup_env.sh. All four original_* source snapshots compare
byte-for-byte with Git 07ba7e042fe4c0488fafbc0c515eccf3234327d1.

Checked current primary sources:
[liburing header](https://github.com/axboe/liburing/blob/master/src/include/liburing.h)
and [vLLM benchmark terminology](https://docs.vllm.ai/en/stable/benchmarking/cli/).
The liburing CQ iterator uses a local finite tail snapshot and CQ advance
release-publishes consumed entries after reads. That is a credible design
precedent, not evidence that GPU system-memory cursor access caused0050.

## Admission and research value

The retained question is CPU-worker-free admission/completion with reusable
efficient GPU model computation. 0050 already answers its unchanged coalescing
matrix: AMK throughput recovery has a remaining native gap, and vLLM throughput
and short-output concurrency latency regress. The new intervention changes an
identified production synchronization/access policy without model arithmetic,
rather than rerunning a settled matrix or adding a nominal model.

The uncertainty is consequential: batching may improve useful serving delivery,
may merely shift work/latency, or may fail to help despite reducing source-level
cursor publications. Positive evidence would select a portable driver policy;
mixed or negative evidence would bound it and change the next diagnosis. These
outcomes do not have the same paper decision. Prior results cannot reconstruct
a policy that was never executed. This is supporting evidence toward the
retained question, not a new RQ, standalone dependency result, universal eBPF
win, or necessary central-thesis prediction. A negative result bounds this
constructor/workload/policy; it does not refute the whole CPU-path-removal idea.

## Baselines and fairness

Efficient source-native epoll TCP with the identical backend computation is the
single main competing mechanism. It represents the credible position that
efficient userspace delivery remains preferable. A fresh matched run is needed
because absolute numbers and relative differences from0050 cannot settle a new
policy under a new process/host interval.

Pre-edit07ba7e0 coalesced code is a component control. It isolates the collective
queue-publication intervention within the same coalesced constructor. The old
independent GPU network worker remains cited0050 evidence; adding it as a fourth
path would be redundant for this hypothesis. No further baseline or broader
workload is required for admission.

The three backend/model combinations test a concrete transfer claim while
holding their own math fixed. Cross-backend results must remain separate:
AMK/vLLM kernels, batching, memory and CUDA linkage differ. AMK's known stronger
eager-HF equality failure and ordinary unobserved batch/KV histories are
explicitly retained. Whole-output-set membership is finite qualification,
not an all-input semantic oracle. The plan does not hide those limits or use
candidate outputs to generate its accepted pool.

## Queue ordering and liveness obligations

The proposed single-GPU-issuer batching is coherent if implemented as stated.
A stale acquire SQ-head snapshot is conservative: it can refuse a reservation
that later becomes available, but must never grant more than the ring capacity.
Every successful reservation advances one local unsigned tail and contributes
one pending operation. Local cursor variables must be shared across every
io_submit call in that round, not copied by value per reservation.

Before publishing SQ tail, all SQEs and referenced SEND/ACCEPT buffers must
be ordered to the host/kernel by the existing system-scope semantics. Publishing
once at round end changes submission/availability ordering collectively; it is
not an instruction-count-only ablation. CPU publication patterns are not a
substitute for preserving CUDA/host system ordering.

Acquire-snapshot CQ tail before reading that finite batch, copy/process each
entry, and release-publish the consumed head after the reads. This also allows
the kernel to reuse consumed CQ storage safely. Entries arriving after the
snapshot belong to a later round; concurrent production is not an error.

The actual source has a critical early return while stopping&&!cancel_done
(previous line160). A queued ASYNC_CANCEL must be SQ-flushed before that return,
or the target completion can never arrive. The normal return and any terminal
branch must also preserve publication; final SQ/CQ telemetry/finished must
describe actually published/drained cursors. Pending cancellation CQEs,
multishot timer finalization and GPU-to-shutdown-worker ownership remain
unchanged. These are existing validity obligations already specified by the
plan, not requests for a new test framework or gate.

Because only BF_IO_COALESCED code changes, noncoalesced compile-time paths must
keep their previous behavior. Static inspection of the actual patch before
freezing, existing protocol/lifecycle runs, independent SQ/CQ emptiness and
normal exits can support the declared finite scope. They cannot prove all
wrap schedules or arbitrary service behavior. No narrower artificial
microbenchmark is needed to admit the real experiment.

## Metrics, executable matrix and interpretation

run.py creates three model/backend drivers per process block; each uses the
three planned modes. The five-block full matrix and four gen/concurrency cells
produce45 executors/180 cells/5760 measured requests187200 tokens plus360
checked excluded warmups. The adapter preserves five path permutations and
odd-block model/cell reversal. Residual order imbalance and shared-host drift
are honestly acknowledged; blocks are the replication units, not individual
requests treated as independent trials.

The analyzer reconstructs arrivals, completion, TPS, TPOT, pool checks,
terminal queue counters and worker CPU brackets. It computes candidate-minus-
old-coalesced and candidate-minus-native effects over five process blocks with
nominal paired t95df4 intervals. TTFT and TPOT definitions agree with the cited
official vLLM terminology; TPS uses the explicitly defined cell collection
interval. Known-worker process clocks are neither total CPU nor energy.

Interpret latency/TPS separately per workload. A reliable latency gain versus
the component control is an intervention result; remaining loss versus native
prevents claiming the strongest competitor has been beaten. A reliable TPS
loss makes the combined latency-plus-long-output-efficiency hypothesis mixed
or contradicted for that workload. Zero-crossing intervals establish neither
equivalence nor retained noninferiority. Do not turn nine nominal primary
contrasts into a familywise-confidence or universal-backend claim. All secondary
signed outcomes should remain available as planned.

The full expanded command/environment freeze, baseline reconstruction and
candidate qualification are still preparation tasks, not missing alternative
experiment design. Source-native commands and paths are concrete. The selected
protocol/lifecycle work is integrated dependency qualification with preserved
oracles and failure limits; it is not a separate scientific contribution.
Discrete before/during/after host observations improve the missing0050 bracket,
but do not establish continuous resource isolation or harmlessness of existing
NVRM warnings.

## Decision returned

Proceed with the specified implementation, frozen original control, actual
qualification and full matrix. No widening of baselines/models, new control
interface, custom score, arbitrary acceptance threshold, arithmetic campaign,
or unchanged re-review is requested. Preserve unexpected/negative rows and
separate collective policy performance from unmeasured cursor/PCIe mediation.


## Round 1 concrete patch inspection addendum

Before returning this review, read the newly prepared implement.py (not executed
by this reviewer). It applies only a conditional change to the captured
07ba7e0 header. Static inspection finds the proposed policy materially matches
the plan:

- Coalesced IoRing adds round-local SQ head/tail/published cursors.
  io_progress copies persistent ring pointers, then acquire-snapshots SQ head
  and tail once. io_submit takes this local ring by reference, preserving all
  reservations in the same round; the unsigned capacity check is unchanged.
- Each accepted SQE increments pending once; io_publish does the existing
  system fence and release-store before updating its local published cursor.
  It is called on the stopping/cancel early return and before the normal
  terminal check/return. No asynchronous issuer is added.
- Coalesced CQ drain acquire-snapshots the tail once, advances a local head
  through that finite set, and release-publishes the consumed head after the
  drain, including MORE/error continue branches. Noncoalesced CQ drain and
  io_submit retain the literal former branches.
- Candidate SQ availability may be deferred because the snapshot precedes CQ
  processing; this is the conservative behavior declared in the plan. A
  finite snapshot can postpone newly produced CQEs. These scheduling effects
  are part of the collective intervention and need actual qualification.

No concrete source-policy defect was found. This is a static prospective
inspection, not a compiler/runtime ordering proof. The patch does not itself
relax numerical references, model arithmetic, protocol checks, timer, queue ABI
or native baseline. The admission judgment remains ADMIT.
