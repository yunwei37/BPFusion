# Submit-frontier PLAN REVIEW

Reviewed 2026-10-14 in the original yunwei356/bpfusion-dev Workspace.
Live repository main was ceadcc06825e23d99684aa05ee0da02b17126853;
git status showed only unrelated untracked tools/setup_env.sh.
This review is read-only for implementation and plan. No experiment was run.

## Verdict

ADMIT the proposed supporting experiment. No scientific or prospective
implementation defect found that blocks source implementation and real preflight.
This verdict does not certify an unbuilt candidate, establish the cause of the
vLLM latency loss, or approve a universal default.

The ordinary matched comparison is specified and its source-native driver,
wrapper, analysis and old-source reconstruction recipe are present. The
integrated one-cell observation adapter and old-control trace recipes are still
prospective. Materialize and inspect those exact executable commands before
executing their observation; retain the promised source/command/environment
freeze before full collection. This is the stated execution sequence, not a
request for another review or a new control interface.

## Independent evidence read

- plan.md and implement.py in this experiment directory.
- Current executor/qwen_graph.cu, executor/vllm_graph.cu,
  executor/io_uring_tcp.h, bpf/uring_loop.bpf.c, Makefile and
  executor/vllm_graph.py.
- docs/evaluation.md, docs/findings/0030-short-input-latency.md and the complete
  docs/findings/0051-batched-ring-publication.md finding.
- Source-native matched_serving.py, run.py, Makefile.original and
  rebuild_original.py in this experiment directory.
- Official upstream Linux io_uring submission source and vLLM benchmark metric
  definitions, linked below.

docs/idea-story.md and docs/background-related-work.md do not exist. The owning
evaluation document explicitly says there is no formal paper RQ/thesis
contract. The retained user serving/performance objective is the question here;
the reviewer did not invent a new paper RQ or require paper artifacts.

## Admission and expected decision value

Finding0051 already closes the unchanged queue-publication comparison. Its
vLLM c8/gen1 means remain 7.158562/8.591165 ms versus native
1.969981/2.633415 ms. Existing four-cell aggregate graph counts cannot identify
the short-output batching history, and those historical counters must not be
presented as per-cell mechanism proof.

The new predicate alters whether a model-idle parent starts new computation
before the kernel consumes already-published I/O. That is an actual scheduling
intervention not covered by0051, not a repeated unchanged benchmark or model
arithmetic optimization. It can repair a material measured latency boundary
while remaining within reused model computation. A contradictory or mixed
outcome would constrain that policy rather than demand another queue tweak or
claim a direct general thesis failure.

The selected role, supporting, is appropriate. Positive primary latency
effects may justify this driver policy within measured workloads. Failure
leaves the previous latency rejection intact; a native loss remains a loss
even with component-control gains. If count/batch observations change while
ordinary latency does not, the mechanism engagement is useful but the
performance prediction is unsupported. If latency improves without the
predicted count/batch change, report performance and mechanism judgments
separately. No outcome here establishes general OSS novelty or the full goal.

The best immediately competing use of the next run would be a read-only
batching diagnosis. This plan incorporates that source-native diagnosis and a
small direct intervention in one experiment, making it a reasonable stronger
next step. It does not require adding a fourth old network-worker timing path.

## Semantics of the prospective two predicates

In both dispatchers, seen counts model-admitted FIFO requests. retired advances
only when the corresponding request reaches completed/rejected phase2 and DONE
is published, then its local request phase is cleared. The proposed hook is
after prior child results are collected and after retirement/publication.

Thus retired == seen is sufficient for no unfinished *admitted model*
computation in these paths. It is not necessary: a finished phase2 request may
still await the existing FIFO release/reclaim rules, leaving retired != seen.
Nor does equality imply no model-pending BPF request, free slot ownership,
completed socket response, or an empty network active list. The plan correctly
limits the predicate to idle fresh admission. Existing unfinished admitted work
remains schedulable because the predicate is false when retired != seen.

The changed hook is within BF_IO_COALESCED after io_progress. That function
system-orders prepared SQE/buffer writes and release-publishes tail before
returning; head and tail reads are volatile PTX system-acquire loads. There is
one GPU producer during steady coalesced service; shutdown switches ownership
only after model synchronization. Comparing mapped ring head and tail therefore
tests a submission-consumption frontier, not local stale unpublished
ring.sq_tail fields.

The source-native BPF issuer reads SQ head/tail, invokes
bpf_io_uring_submit_sqes on the outstanding count, and waits on CQ separately.
The current official upstream implementation publishes shared SQ head after
SQE consumption/submission. This supports the intended interpretation, but
upstream master is not identity proof for installed7.3rc3. Preserve the plan's
version caveat and infer only the mapped SQ state actually tested.

Once head == tail, an asynchronous accept, recv, send, cancellation or timer
can remain outstanding. A send CQE and next_final advancement may still be
needed before later final responses progress. Therefore the policy does not
wait for all response completion and cannot guarantee batching improvement.
It plausibly changes availability ordering; the real observation and ordinary
results must decide whether it helps.

The sequential acquire reads are not an atomic snapshot. Because the same GPU
thread is the only steady producer, tail cannot gain additional unpublished
work between these reads except work this thread itself prepares on the next
iteration; a concurrent kernel head advance can conservatively add an idle
iteration. This is a timing cost, not a new memory/ownership violation.

## Liveness, stop and ownership

Both dispatcher loops revisit stop after a continue: qwen has the while
condition; vLLM polls stop before release/progression on each loop. The new
predicate does not bypass the host's existing model-quiescence / drain handoff.
No new model child is active when equality holds, and no dedicated steady
network CTA is introduced.

A stalled issuer can delay fresh model admission indefinitely until stop.
Continuous publication/consumption of incoming network work can also change
fairness and admission delay. These are actual policy tradeoffs; selected
finite lifecycle checks cannot prove arbitrary backpressure/fairness or bounded
tail latency. The plan explicitly retains the stalled-issuer risk and does not
claim those properties.

The predicate does not change existing next_final, request generation, peer
association, per-connection reply chain, buffer ownership, pending accounting,
slot release or SQ/CQ quiescence logic. The requested protocol/lifecycle cases
remain necessary integrated qualification. Passing them supports their
specific finite behavior only, especially idle, pending accept/recv,
RST/reuse and inflight stop. It does not prove all possible socket fault races.

## Controls, fairness and metrics

The efficient native epoll TCP condition is the one main competing delivery
mechanism. It is a stronger competitor than a deliberately busy userspace
worker and uses the same per-workload resident model computation. A matched
fresh run is needed because the intervention changes scheduling and actual
batch availability; citation alone cannot estimate its numerical effect.

The captured ceadcc0 coalesced source is a component control, not external
SOTA. Its literal snapshot / reconstruction and distinct library names prevent
the candidate being silently used as its own control. Current native builds
exclude BF_IO_COALESCED and must be built with the same source-native
model/KV/packing flags as before. Avoid overwriting the unrelated
vllm_graph_uring_loop_trace artifacts, as specified.

Three reused workloads, three paths, five process blocks and the same four
gen/concurrency cells test one scheduling hypothesis and its transfer costs.
There is no need to add models or weak baselines as an admission condition.
Five of six path permutations and odd order reversal leave residual
order/drift confounding; five paired process blocks, not individual requests,
are the uncertainty units. Nominal paired t95 intervals are reasonable
descriptive evidence with that limitation and no multiplicity-adjusted
generalization.

The primary vLLM gen1/c8 client TTFT effects match the observed defect.
Long-output c8 throughput and AMK transfer keep relevant tradeoffs visible.
Completion, TPOT and known-worker CPU remain secondary, without an invented
aggregate score or NI threshold. The source-native formulas are clear and
compatible with the cited official vLLM client metric definitions. The custom
token-ID wire protocol and fixed wave window are narrower than a vLLM official
text-serving benchmark; do not label this a complete standard serving eval.

No arithmetic, precision, backend revision, page ABI or runtime worker change
is proposed. Driver ordering and resulting dynamic batching can change
collectively; matching computation code does not imply identical realized
batch trajectories.

## Observation and oracle audit

The proposed observation uses the actual source-native client, existing
BF_TRACE record path and independent post-serving replay. It is integrated
mechanism evidence, not another standalone benchmark or toy timeline.

For sequential eight c1/gen1 warmups, each request completes before the next
is sent. Current vLLM increments device_graph_launches once for a model compute
round, and each valid gen1 request completes in one round. Consequently
ordinary one-cell total graph launches minus8 identifies that process's
measured round count when the adapter really executes only the declared
32-request gen1/c8 cell and8 warmups. Do not apply this subtraction to the
four-cell full-matrix totals.

Traced admission records contain actual ID and client_ns. Compute records
contain request_ids and batch, allowing warmup IDs to be separated and measured
round membership reconstructed. The existing replay reconstructs packed
inputs, physical KV ownership and batch history, replays the reused graphs and
checks recorded tokens; it is not an oracle inferred from candidate output
pools alone. Verify unique marker associations, every measured request exactly
once for gen1, batch sizes matching request_ids, trace overflows0, all releases
and graph-count agreement. These are natural checks on the existing trace
rather than a new experiment-control schema.

There is one process per traced/ordinary observation condition, so traced
versus ordinary latency/count differences are descriptive instrumentation
sensitivity only. That evidence cannot authenticate per-cell batching in the
untraced five-block full matrix or prove causal mediation / trace neutrality.
If association fails, preserving valid ordinary counts/latency while limiting
mechanism claims is an honest prespecified fallback.

The finite frozen pool checks remain weaker than all-input exact correctness.
The old AMK eager-HF discrepancy must remain failed. Traced vLLM replay
strengthens only selected histories and cannot erase that separate failure.

## Executability and remaining materialization

The supplied full wrapper expands fifteen model/block driver calls; each
driver has three paths/four cells, yielding the stated45 executors,180 cells,
5760 measured requests/187200 tokens and360 excluded warmups. Preflight uses
eight requests/cell for nine paths. Actual child exit, output pool,
graph/model counters and independent queue shutdown are already checked by
the source-native adapter. Source/flags/commands must be frozen after candidate
build and before collection, as specified.

At review time the one-cell observation adapter and original trace make
targets are not yet present. The root explicitly describes them as required
materialization, not completed evidence. Before observation verify its
matrix=((1,8),), requests_per_cell=32, eight sequential warmups,
exact six path/model conditions under both untraced/traced modes, and
preserved old BF_PAD_PREFILL/BF_PREFIX_RELEASE network flags with BF_TRACE
only added for trace variants. No preflight or full result is certified here.

Host before/during/mid/after observations and preserved warnings appropriately
bound environmental uncertainty without promising continuous isolation.
Existing process handles must resume to terminal; a timeout is not a reason
to restart. Archive the selected source-native apparatus and data, exclude
temporary vendor/runtime/ELFs, and preserve default/base/Coder/WIP on cleanup.

## Primary sources checked

- [Linux io_submit_sqes / io_commit_sqring](https://raw.githubusercontent.com/torvalds/linux/master/io_uring/io_uring.c):
  shared SQ head is release-published after consumption/submission; pending
  completion is a separate state. This is upstream context, not installed
  kernel identity.
- [vLLM benchmarking CLI metric definitions](https://docs.vllm.ai/en/stable/benchmarking/cli/):
  TTFT and TPOT client measurement points and output-token throughput
  terminology. The actual project window/formulas remain explicitly stated.

No wider matrix, runtime setting, additional agent, paper rewrite or model
optimization is required by this review.
