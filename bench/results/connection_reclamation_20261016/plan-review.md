# Fresh plan review: connection reclamation under sustained remote load

2026-10-16 UTC. Independent review under research-experiment-design.
Read the current plan, README/evaluation and previous completed sustained result
review; inspect the actual shared-page/admission/queue/transport code, diagnostic
source diffs and successful build receipts. No GPU, load, source edit, Job
mutation or Git action is performed. This reviewer writes only this file.
There is no formal paper RQ file: retain the question stated in the plan,
whether removing the steady userspace network worker improves remote delivery
or resources with the same resident real-model executor.

## Verdict

**Admit the diagnostic and the declared conditional repair comparison.**
There is no scientific or executable defect requiring this investigation to
stop. The proposed local-reference algorithm is a contract for an implementation,
not reviewed proof that an implementation is safe or that the cause is known.
The full matrix remains conditional on the planned errno/census evidence,
mechanism engagement and actual engineering qualification. If the diagnostic
supports another cause and changes the intervention materially, revise this
same plan transparently and use the available follow-up review; do not describe
an unrelated repair as confirmation of this hypothesis.

## Scientific value and fair comparison

The prior full experiment already establishes adverse sustained behavior:
3926/57600 kernel192 zero-token timeouts, native192 none, and one insertion-
failure counter matching its cell's835 failures. The global close guard, finite
4096 socket capacity and observed peak make lifetime retention a credible
hypothesis, while errno and actual retained socket states are missing. Neither
reanalyzing successful-response tails nor repeating the untouched rate sweep
supplies this causal discriminator. Repairing this confound before claiming
transport performance is a consequential supporting experiment.

Positive and negative decisions differ: removing the failure class can qualify
a repaired path for a fair comparison; a contrary errno, persistent failures
or failure of the control to engage leaves the explanation or sustained path
unqualified. Neither outcome proves an intrinsic eBPF speed benefit or allocates
the historical unreproduced6.36ms gap.

Efficient native epoll with identical resident compute is the single credible
main competing answer. The global-guard row with common reference bookkeeping
is correctly a component ablation, not a second main baseline. It isolates the
choice of close predicate within the new ABI/accounting implementation.
It does not reproduce the untouched2c0cf7b implementation and cannot by itself
measure bookkeeping overhead versus that source; the plan labels this honestly.
The existing official vLLM reference is sufficient for the separate whole-service
context and need not be rerun here.

One192/s point, matched schedules, fixed model/budget, five process blocks and
three ordered conditions test the same relation without unnecessary extra
workloads. Keeping the prior96 evidence rather than adding another sweep is
reasonable. The declared order is not perfectly balanced over five blocks;
retain it, since changing order after results would be worse. Shared-host
exposure and process order remain limitations.

## Diagnostic validity and alternative causes

The archived diagnostic diff reads the actual helper return and CAS-stores its
first positive errno magnitude into admission_pad only on failure. Current
source searches find no other reader/writer of that reserved field except its
declaration. This leaves the ABI, admission and selected GPU/loop objects
unchanged; both actual diagnostic builds exit0. It adds some failure-path work
and is diagnostic evidence, not a clean performance row.

A first errno is not an errno distribution and is not enough alone to prove
capacity exhaustion. In particular EEXIST, ENOMEM and subsequent different
failures remain possible. Preserve insertion counters, first errno, connection
peak, queued/head state and socket census together. The existing snapshot
captures owned socket inode links and own-port TCP rows, which can distinguish
owned CLOSE_WAIT/other retained sockets from unowned TIME_WAIT rows; do not
equate all rows or all process FDs to sockhash occupancy. Its proc/map reads are
finite, sequential snapshots, not an atomic inventory. Failure-to-read stack
or syscall evidence is missing evidence, not zero work.

An E2BIG result with retained owned EOF sockets, a full capacity boundary and
the control/candidate intervention would materially strengthen the proposed
cause. The old counter equality alone does not establish this. Parser/redirect,
slot publication, source-port reuse and scheduling alternatives remain live
until the actual discriminator narrows them.

## Ownership, ordering and collision safety

The existing queue producer increments llm_queued before push and rolls back a
failed push. Its sole loop consumer reserves/advances head, pops, publishes the
slot and then decrements. The current GPU refuses close while it has an active
reply, a receive reference, unseen admissions or global pending. Replacing only
the last global predicate with conservative peer references is a coherent
candidate; preserving merely aggregate counter equality is insufficient.

The stated implementation must preserve all of these properties:

- Every queued producer establishes the same peer bucket before exposing the
  queue element; failed publication removes exactly that reference.
- Consumer publication/head ownership happens before its release decrement.
  GPU obtains the bucket value with system acquisition, then rereads head/seen.
  Reading head first can miss a pop/publication before observing bucket0.
- A reserved but not yet fully published slot still blocks unsafe close through
  head/seen. A slot must not be skipped just because publication is incomplete.
- Hash/address/port representation is identical on producer and GPU. Collision
  references may postpone reclaim but never cancel one another or underflow.
  Pending cancellation/stop cannot release a reference that a producer or
  consumer still owns; counter reset is safe only after producer/consumer
  quiescence, including rollback paths.
- Bucket0 is a snapshot, not a lock against a future producer. EOF/dead plus
  completed receive/cancellation and active-reply checks must establish that
  this same socket cannot subsequently publish an unaccounted frame. In
  particular do not assume a send-error/dead flag alone proves that. Explain
  this against the actual TCP/parser/receive ordering in the implementation,
  and exercise reset, pipelined input and half-close cases already in scope.
- Peer identity reuse must not attach an older request to a later accepted
  socket. Retained references and still-live reply ownership must outlive every
  slot/request access. Qualifying same-peer reuse and deliberate hash collision
  must use real requests, not only an abstract counter fixture.

These are the planned ownership contract, not requests for another baseline
or infrastructure. The default8 two-model protocol/dual-replay and ordinary
queued-reset/mid-output-stop cases are appropriate implementation checks.
Rebuild all ABI-dependent8/16 objects and requalify the existing generic
cuBLAS/cuFFT lifecycle surface if its shared transport/header changes, as the
plan already requires. No adoption claim follows from this plan review.

## Metrics, execution and interpretation

Failed attempts/attempts is a standard direct reliability outcome rather than
a project-defined score. The cited existing official benchmark reference
supports the surrounding throughput/latency vocabulary. Five paired block
failure-fraction differences with nominal t95df4 are an honest small-sample
summary if raw counts and individual blocks remain visible; they are not an
exact binomial interval or a production failure-rate guarantee. Zero observed
local/native failures cannot establish equivalence.

All-attempt throughput must include terminal drain. Success-only completion,
TTFT and receive-gap P99 must remain labeled conditional; a failed request is
not a60-second successful response. Same-read zero gaps remain client
observations, not official stream-output ITL. Freeze oracle membership and
original per-operation timeout, with disagreement/error rows retained.
Finite-reference disagreements can limit numerical/comparative claims even
when the reliability observation is valid.

CPU group/cgroup/host and device energy are nested or shared observations:
do not add them or attribute whole-host background directly to serving.
Counter bookkeeping must be common between kernel ablation and candidate.
If native does not execute that bookkeeping, describe it as a competing
implementation cost, not matched mechanism overhead. Preserve observer/control
brackets, startup exclusion and unequal useful-work denominators. Performing
heavy archival only after terminal server stop fixes the prior collection
exposure without changing the measured service intervention.

The existing real remote adapters and retained Job give an executable path.
Before collection record the actual adapted command, build selection and
single-rate condition matrix in ordinary artifacts; no new experiment-control
interface is needed. The plan's4608-attempt preflight crosses cumulative
capacity, but cumulative connections alone do not prove simultaneous retention.
Its explicit full60s diagnostic fallback is therefore sensible. Keep all
preflight outputs and count the fallback within the same at-most-three real
preflight attempts. Expected global failures are valid measured outcomes;
unexpected runner/configuration failures require repair, not favorable
replacement of a negative valid cell.

All15 full cells must finish before a full-result claim, followed by fresh
independent result review. If global does not engage, the reliability
contrast is inconclusive for the lifetime hypothesis even if candidate looks
faster. If local removes failures but native remains faster, report the
reliability repair and adverse/no demonstrated eBPF speed advantage.
No additional baselines, tuning, model-kernel work, Job or service is needed
to execute this plan.

## Initial-review clarification: EOF-only local guard

Before any GPU run, the owner narrows the proposed intervention: use peer-local
pending only for c.eof set by a real receive CQE res0; dead-without-EOF and
canceled receives retain the original global guard, and stopping retains its
existing override. This is a safety-preserving narrowing within the declared
hypothesis, not an extra comparison or a revised expected answer. Record it in
the plan and actual source receipts.

Independent inspection of the exact
[Linux7.3-rc3 receive implementation](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_bpf.c#L207)
supports this boundary: the parser receive path locks the socket, processes
pre-accept receive data, drains ingress messages and recognizes FIN/shutdown
before returning EOF. A nonzero-size, non-PEEK receive EOF is materially stronger
than an arbitrary send error or canceled operation. The actual code uses4096
byte receive buffers and no MSG_PEEK. Together with no outstanding receive,
pending acquisition followed by fresh head/seen, and no reply owner, this is a
reasonable conservative candidate for the declared real-request qualification.

This judgment is source-scoped and still requires actual implementation checks;
it does not prove arbitrary future kernel compatibility. A broken-pipe/reset
connection that never produces receive EOF may retain the old conservative
dependency. The candidate therefore cannot claim to fix sustained RST floods or
every dead-socket retention case. That limitation does not block the targeted
graceful-completion capacity experiment.

## Follow-up 1: actual private candidate and engaged diagnostic

2026-10-16 UTC. Read the current amended plan, candidate-description.md and
actual TEMP/reclamation_source files, comparing each flat source file with its
canonical repository path. Read both diagnostic snapshots directly and
reconstruct owned socket states by joining proc TCP inode fields to the captured
owned FD socket links. No GPU, build, source mutation, Job change or Git action
is performed by this reviewer.

**Verdict: no concrete invalidity blocks compilation and real preflight of this
candidate.** This is implementation/plan review, not qualification or adoption.
The original full comparison and correctness requirements still apply.

### Diagnostic engagement

The first snapshot records3385 successful insertions, zero failed insertions,
llm_queued173 and3112 model-head admissions. Of its captured process-owned
TCP rows,2947 are CLOSE_WAIT,187 ESTABLISHED and one LISTEN. These observations
show substantial owned peer-closed retention while unrelated admission backlog
exists; individual completion is not proved for every retained socket.

The later snapshot records4248 linked,368 failed, first errno7(E2BIG),
llm_queued0 and head4248, with368 owned ESTABLISHED and one LISTEN row.
This is actual insertion capacity error evidence, not assumed errno. Because
the later snapshot is already after queue drain and most retained sockets have
closed, it is not a simultaneous census of a full sockhash. The first errno
does not classify every failure. Preserve the eventual terminal/client counts
and match them to the separate counters rather than silently calling every
E2BIG observation a per-request causal trace.

Together with the prior4096 peak and source predicate, these snapshots engage
the planned retention/capacity mechanism sufficiently to test the intervention.
EEXIST/ENOMEM are not the observed first failure here, but their complete
absence is not established.

### Actual reference accounting and close predicate

The shared-page header appends4096u32 counters without shifting existing fields.
Its single unsigned hash function is used by BPF producer, BPF consumer and
GPU predicate; the actual producer and sockaddr peer address/port use the
same network-order representation. The constant is a power of two and the
masked index is in bounds. Collisions share a nonnegative conservative count;
they do not subtract one peer's queued request on another peer's completion.

On the actual queued branch the producer increments the peer bucket, then the
global count, before the queue helper. Failed push decrements global then peer
exactly once. The sole consumer reserves head/slot, pops the queue request,
publishes the slot and then decrements global followed by that request's peer
bucket. Thus a successful own-bucket transition to0 follows slot publication.
Existing nonqueued direct admission does not consume a queue bucket and does
not decrement one; it remains covered by head/seen and receive-EOF ordering.

The actual GPU predicate first requires dead-or-EOF, no outstanding receive,
no reply owner and no close in progress. Only actual c.eof takes the peer-local
branch. Otherwise it loads the original global count. System acquire io_load
reads pending before the fresh llm_head load. If the consumer releases the
last pending reference after publishing a request, fresh head/seen prevents
closing before attaching that request. The candidate does not replace the
receive-EOF test with a canceled-receive or arbitrary send-error condition.

Under the scoped receive-EOF terminal-producer premise already reviewed, another
peer incrementing or draining the same hash bucket can only defer this socket
or provide another publication barrier; it cannot create a missing reference
for an actual queued request of this EOF socket. Overflow is not a realistic
case within the finite4096-entry queue and declared attempt counts, although
the unsigned counter is not an unbounded mathematical reference count.
The planned real collision, pipeline, same-peer-reuse and reset/stop cases
remain required engineering checks of this reasoning.

Stopping keeps its original pending override and fresh head constraint.
There is no new live counter reset or selective queue cancellation. Unconsumed
queue entries can retain counters until shutdown; map removal after the
existing transport/model/BPF lifecycle is the cleanup boundary. Verify actual
detach/shutdown completion, rather than assuming counters must be0 at a
deliberate stop with queued abandoned work.

### Fairness and remaining execution checks

The BF_IO_GLOBAL_PENDING_GUARD ablation uses the identical counters/page and
fresh pending-before-head ordering, changing only the selection of local versus
global pending. It is a clean close-predicate ablation with common accounting,
not an untouched-source before row. The separate diagnostic still uses the
original selected GPU object and unchanged-size page.

vllm_mixed.cu and bpfusion_admission.h are byte-identical to canonical source in
this candidate. No model computation edit is hidden in the diff. The actual
BPF change also retains the same first-errno instrumentation in the common
candidate/control implementation; its failure-path overhead is common but can
naturally execute more often on a failing condition.

All components that interpret/map/register the expanded shared page must use
the same rebuilt header and actual page/map size. This is a necessary ABI check
already in the plan; successful compilation alone will not establish load,
mmap registration, or runtime bounds. Preserve the normal8/16 receipts and
affected generic backend lifecycle results before adoption.

The actual candidate is deliberately narrower than a universal dead-connection
repair: RST/send-error sockets without receive EOF retain the global dependency,
and sustained hash collisions can also postpone reclaim. Those boundaries
do not invalidate the graceful completed-connection192/s comparison, but they
must remain explicit if the candidate fixes that measured failure class.

## Follow-up 2: collision qualification oracle revision

2026-10-16 UTC. Final allowed plan-review follow-up. Inspected the actual
TEMP/reclaim_collision.py, failed collision_reclaim_vllm_qwen_8_loop/qwen.results.json,
current plan, executor/vllm_mixed.py and the complete source-native
executor/mixed_replay.py. This review runs no GPU/load/build and changes only
this appended review.

**Verdict: admit the recorded traced qualification-path correction before any
candidate remote acquisition.** This is not permission to relabel the failed
trial as a pass or to change the scientific full-run oracle after observing
results. No candidate remote preflight/full cell has yet run, and the
scientific remote oracle, timeout, outcomes and paired matrix remain frozen.

### What failed and what remains unknown

The actual ordinary collision trial reaches bucket626 pending40, head9 and
global queued88, and its early-EOF check does not fail. It then stops on a
gen64 reply outside the finite pre-observation reference set. The saved result
has pass=false,97 requested rows,41 rows with checked reply transcripts and
the failing reply bytes in the retained exception text. Error handling closes
clients and stops the server; remaining work is partly canceled.

That run therefore establishes initial collision engagement, not completion
of the intended105-request collision/drain/same-peer-reuse workload. Exit0 from
the server and no remaining pins are cleanup receipts, not qualification.
There is no captured serving compute trace in that trial, so it cannot
distinguish a schedule-dependent numerical variant from incorrect transport,
slot association or memory contents. The observed failure must remain visible.

### Why the proposed discriminator is valid

The revised qualification uses the existing BF_TRACE implementation and
bootstrap --trace-output/--trace-requests path. The bootstrap runs
mixed_replay.audit after serving, with two exact checks: replay of captured
graphs, then reconstruction of fresh upstream attention metadata. Both
zero the model KV caches before reconstructing each trace history.

The replay derives packed inputs, positions, sequence lengths, physical pages
and metadata from admitted requests and previously verified history, then
compares independently executed model outputs token-for-token against each
serving compute event. Following traced history is not circular when every
step's output is independently verified; a wrong earlier token fails at that
step. Fresh-metadata reconstruction additionally checks the captured metadata
path. Both remain same-model/backend finite engineering oracles, not a
universal model quality or external official-server equivalence proof.

The replay alone verifies the model trace, not bytes delivered over TCP.
Accordingly, the proposed exact join from unique client_ns to admission and
compute history is necessary: request prompt/gen/identity must match, every
returned token must equal the traced per-request output, and all105 requested
responses must be accounted for without duplicated or missing stamps.
For the unchanged cases, the expected complete returned token count is6153
(1 early token,96 gen64 responses and8 gen1 reuse responses).
Trace overflow, incomplete release, unexpected token count, either replay
failure, or a client/trace mismatch leaves qualification failed.

The revised client must retain raw received bytes/tokens before classifying
finite-reference membership, including membership=false. It must not throw
away a disagreeing reply before the independent comparison, expand the frozen
pool, select a favorable replay, or compare only the first candidate sequence.
If exact dual replay and client correlation pass, report schedule-specific
independent replay agreement alongside the still-false finite membership flags.
Calling the disagreement specifically an FP16 numerical effect would require
additional numerical evidence; passing replay more narrowly excludes the
tested transport/model-trace mismatch and establishes the observed schedule's
upstream computation result.

### Scope of the correction

Record this as a changed qualification evaluation path and rerun the affected
collision/reuse workload in full, keeping its original trace-less failure and
all diagnostic/cleanup files. It is a genuine missing-oracle repair, not an
unchanged repeat until favorable output. The basic source, workload,
collision/EOF/reuse conditions and frozen membership set remain unchanged.

Keep tracing/replay outside the ordinary remote performance matrix. Tracing
can change scheduling, so its timing does not replace ordinary latency or
resource results. The already completed ordinary lifecycle and protocol
qualifications supply distinct evidence; they do not erase this failed trial.
The new traced bootstrap must terminate both replay modes before success:
a serving-ready line, server return or a first replay summary is insufficient.
Its existing outer communication timeout must not cause an unfinished replay
to be reported as passed; any actual timeout remains a recorded execution
failure.

This is the third and final plan-review discussion (initial plus two
follow-ups), not a reset of review count. If a blocking oracle or correctness
defect remains after this correction, return the failed qualification and
history to the owner rather than adding another reviewer round or weakening
the hypothesis. No additional baseline, infrastructure or model optimization
is required for this discriminator.
