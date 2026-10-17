# Independent result review: sustained official reference

Reviewed 2026-10-17 UTC under research-experiment-design RESULT REVIEW. This is
one fresh review of the completed ordinary retry2 matrix, not a new plan
review or permission to rerun it. Only this report was written. No serving
run, model/build/source change, Git action, persistent setting or new workload
was performed by the reviewer.

## Judgments

- Run status: **valid**, for delivered service under the recorded client,
  workload and finite correctness checks.
- Tested hypothesis: **contradicted**. The resident native design does not
  keep up with official optimized vLLM on the fixed delivered-throughput
  primary in this sustained workload.
- Research value: **supporting**. This adds the missing sustained official
  whole-service reference; setup, client diagnosis and archival repairs have
  dependency value rather than independent scientific contribution.
- Paper impact: **mechanism or workload boundary**, with additional evidence
  toward the retained serving objective. No formal paper RQ/thesis exists;
  this is not a direct thesis challenge or an invented new RQ.
- Next paper decision: retain official vLLM as the stronger delivered-service
  reference here, retain the same-executor native causal control, and remove
  any general faster-server/eBPF superiority interpretation. K remains
  unselected. The historical 6.36-ms attribution/repair and exclusive total
  resource saving are still unresolved.

No scientific defect requires a rerun for that bounded conclusion. This
does not certify ideal client injection, protocol-independent GPU latency,
maximum capacity, arbitrary-model correctness or completion of every earlier
user goal.

## Material examined and independent checks

I read the retained objective, hypothesis, admission rationale and fixed
primary in [plan.md](plan.md), the single plan-review history, the actual
client/server/analysis/driver/resource sources, model/environment snapshots,
all ordinary server receipts/logs and the complete acquisition analysis.
I also read the prior-prefix and client-GC diagnostic explanations, transfer
recovery record, final acquisition/result, resource ledger, cleanup receipt,
finding0078 and its README/evaluation/architecture navigation.

A separate read-only streamed calculation inspected all15 original merged
gzip clients, all172800 measured request rows and all11059200 output token
IDs. It independently checked exact original indices, prompt selection,
generation count, scheduled timestamps, frozen arrival offsets, success
population, final-close duration and token totals. It recomputed delivered
tokens/s, connect TTFT/completion P99, scheduled completion P99, mean/P99 TPOT,
receive-gap P99/zero fraction and scheduling-lag P99 from raw stamps; these
match acquisition values to floating-point precision.

All five official cells' **3436757** retained SSE data payload frames were
independently decoded. Reconstructed prompt, final length finish reason,
token IDs and token arrival stamps exactly match their request rows. This
checks the archived payload representation, not literal whole-wire framing
or an independent mathematical model oracle.

All60 worker metadata/source snapshots match the frozen ordinary client;
each records uvloop0.23.0 and readiness before its shared future epoch.
The ordinary source has no GC callback instrumentation. The acquisition
analyzer additionally joins every original worker request against its merged
row, checks modulo-worker assignment, common schedules, child terminals,
CPU components and last-close endpoint. The archived-gzip replay is exit0,
byte-identical to acquisition analysis and has empty stderr.

I independently recalculated **all69** paired signed means and nominal
t95 intervals from the15 cell metrics, and separately recalculated the
owned-group, cgroup, GPU-energy and host-softirq deltas from raw resource
samples. Process-group PID membership stays identical across every sample
in each cell, not merely at bracket endpoints. Official has three observed
TGIDs in each cell and all are included in owned-group accounting. GPU
compute-app sets contain the corresponding service process. These checks
do not make shared host/device counters exclusive.

The client/server/analysis/resource-observer/model/config/offset files are
Git-identical between frozen input8d565c7fbdfb8ce87835cd86676d5ad294db2c51
and artifact/transfer checkpoint430988307b5062a7eef46f054bc79a7a474ceea1.
Every same-condition captured model/network/BPF source and command is
constant across all five cells despite differing receipt HEADs. K versus N
captured model source differs only in the network-header include. Therefore
later archive/transfer commits do not imply different measured computation.
The post-run generic graph qualification is separate from this matrix.

## Completion, deviations and preserved adverse data

The declared five-block orders are retained: K,N,O; N,O,K; O,K,N; O,N,K;
N,K,O. Each cell has11520 scheduled attempts at192/s over60s plus full drain,
a fresh server and eight excluded checked gen1 warmups. All172800 measured
requests succeed with11059200 tokens; failures, timeouts, invalid outcomes,
partial outputs and close errors are zero. All120 warmups pass the frozen
gen1 reference checks. Every server/client terminal is zero; official
children drain without forced cleanup, native/K counters balance, detach
succeeds and no owned pins remain in terminal receipts.

Three actual preflights, the two-worker sustained prefix and four-worker
retry1 prefix remain separate. The earlier prefixes have material official
client lag and are not mixed with retry2 or counted as server losses.
The ordinary full matrix was restarted after common worker/client repairs,
rather than replacing favorable cells within a mixed matrix.

The raw-payload repair preserves requested inputs, parsing/validation,
timeouts, schedule, durable request logging and fixed primary. It removes
retained nested decoded SSE trees with default GC enabled and unchanged
thresholds. The instrumented diagnostic supports a client retention/GC
problem: worst-delay interval coverage and the raw-payload control are
appropriately labeled client dependency evidence, not eBPF/model speedups.
The control's finite, ordered nature does not prove unlimited client
headroom, and ordinary residual stalls remain in the final result.

The post-window8 SSH acknowledgment-loss recovery changed only after-stop
raw copying. The archived record verifies the original byte range and
fixed-offset replay; original serving cells were recovered and the matrix
continued at9. No measured request/client/oracle/metric/backend was changed,
and no already-completed serving cell was remeasured. This deviation does not
invalidate the frozen ordinary comparison.

## Independent baseline audit

**O: official optimized vLLM.** The installed source-native tokens-only server
uses the same pinned Qwen revision, FP16 and RTX5090. Each log shows only
model/tokens-only/dtype/host/port as non-default command arguments, normal
32768 context, FLASH_ATTN, compilation, full/piecewise CUDA graphs, chunked
prefill and prefix caching. Its logged KV allocation is2374096 tokens.
It is not forced eager, artificially capped to resident16, stripped of its
scheduler or limited to a weak proxy implementation. Missing/invalid auth401
controls and successful real requests are recorded in every cell. The
capture-only multiprocessing override is removed for O. Its intended
optimized serving mechanism actually engages.

O owns a different scheduler, KV/capacity, API, serialization and streaming
path. Four repeated very short prompts and the offered load bound
generalization; sampled prefix-hit logs are0%, which is not universal cache
behavior. This is a valid whole-service reference, not a transport ablation.

**N: efficient native epoll.** This uses the existing epoll/timed-wait path
with the same resident16-slot GPU computation as K. It is a credible causal
alternative rather than an intentionally busy-spin/weak reference. Its
ordinary successful work/counter/lifecycle evidence is present. Shared
resident scheduling and capacity limitations affect K and N together.

**K: kernel-owned network candidate.** The intended BPF/io_uring network path
engages, its network queues and final counters balance, and model
admitted=retired=11528 including warmups. GPU dispatch errors and GPU
trace_overflows are zero. The separate bounded network reply recorder has
trace_count11528/trace_overflow11400 per cell; that loss is disclosed and
must not be relabeled a trace-loss-free acquisition. This ordinary delivered
comparison does not require those128 record slots to be a full per-stage
latency trace, but cannot use them as one.

## Primary, uncertainty and negative results

Mean delivered tokens/s are K11645.240383, N11645.243595, O12244.673615.
The fixed N-minus-O primary is
**-599.430021 [-623.509431,-575.350611] tokens/s**, approximately4.90% lower.
Every block has the same adverse sign. This contradicts keeping up on the
predeclared fixed-load delivered-service metric. It does not estimate O's
maximum throughput above the offered rate.

Mean per-cell completion P99 is K3304.045033, N3313.974502,
O610.729840ms; N-minus-O is+2703.244661
[2315.942202,3090.547121]ms. Scheduled-origin completion tails preserve the
large adverse resident difference. TTFT is also adverse. The tail gap is
consistent with resident backlog accumulating below offered12288 tokens/s,
but no unique causal share is isolated between capacity, scheduling,
protocol and client behavior.

K-minus-N throughput is-0.003212 [-6.499599,6.493175] tokens/s and
completionP99 is-9.929469 [-64.178327,44.319389]ms. These intervals cross zero:
neither superiority nor equivalence follows. K's favorable mean TPOT
difference-0.003639 [-0.006788,-0.000489]ms is secondary, small and cannot
replace the fixed primary. The69 nominal intervals are not simultaneous
multiplicity-adjusted guarantees. Five seeded process blocks, fixed orders,
this machine and this short-prompt workload limit generalization.

Lower resident owned-group CPU/TPOT/client gaps coexist with worse official
throughput/TTFT/completion results. The adverse shared-energy observation
is retained. The report does not suppress inconvenient metrics or promote
a secondary win into an overall faster-server result.

## Client fairness, correctness and cost limits

Ordinary O scheduling-lag P99 is4.475/3.359/41.992/16.995/3.841ms;
N is3.685/1.385/1.360/1.514/3.229ms; K is around1.35--1.48ms.
There is residual protocol/client asymmetry and occasional much larger
maximum stalls. The repaired injector is not ideal. Official nevertheless
wins the recorded delivery/completion comparison rather than having its
client defect counted as a proposed-method win. The appropriate conclusion
is conditional recorded-client service performance; server-only capacity
and fine inter-token attribution remain unidentifiable.

Receive chunks stamp multiple tokens together. Zero-gap fractions differ
substantially, and O's higher receive-gap P99/mean TPOT cannot establish
slower GPU kernels or be called official per-stream-output ITL.
Official connect-origin includes aiohttp setup; binary send/connect origins
remain distinct. Binary connect/drain/read each has60s bounds, official
connect/socket-read has60s with default small-body write handling and no
separate write bound. Neither uses an overall deadline or retries.
All these differences are explicit and no timeout occurs.

Frozen-pool disagreement counts are K222/N462/O1061, total1745; all remain.
Protocol/count/range/prompt/finish/DONE validation and earlier finite exact
controls provide bounded correctness evidence. They do not establish exact
ordinary trajectories for every16-slot request or arbitrary model. The
finite reference set was not enlarged after observation or used to drop
optimized-path disagreement. No circular output-defined accuracy claim is
made.

Mean group CPU is K0.834701/N0.812080/O8.544668ms per attempt. That large
resident/official difference includes whole-design/API/scheduler behavior;
it is not an eBPF-only saving. Group user/system tick rows and shared
softirq rows match raw observations. Primary thread subsets omit official
child TGID threads, although group CPU includes those TGIDs. No visible
io-wq/kernel worker in the Workspace PID namespace is missing coverage,
not zero cost. Stable-thread runnable wait is not request latency, and GPU
controller work counts are not critical-path time.

Owned group, cgroup, thread, host and device views overlap and must not be
summed. Foreign CPU work remains active; observer/control and post-drain
merge affect the broad resource brackets. No exclusive total service CPU,
softirq or energy reduction is proved. The original historical+6.36-ms
inter-token P99 difference is still unreproduced/unallocated/unrepaired;
this experiment cannot close that user requirement by substituting a
different latency metric.

## Figures, reporting and closure

I independently viewed the generated PNG: all four panels, five paired
points, labels, means and gray pair connections are legible and match the
fixed data. Mean bars are not confidence intervals. Table P99 entries are
means of five cell quantiles, not a pooled request P99. The PDF is the same
savefig figure output and was not separately rasterized in this review.
The proposed result/finding/navigation numbers and resource subset table
agree with the independently checked metrics and preserve the limits above.

The final cleanup receipt records original PID1/10909 start times,
empty GPU apps/pins, byte-unchanged selected sources, preserved foreign
setup_env.sh, removed ephemeral key, exact owned Job/Pod UIDs and fresh fleet
health. I independently queried the owning client Job and Pod with
ignore-not-found after cleanup: both queries exit0 with no object output.
Publication is the owner's next closure action; this reviewer performs no
Git mutation.

Keep the external negative result and honest same-executor null result.
Do not claim eBPF novelty, general speed superiority, native equivalence,
complete total-resource accounting or a fix of historical6.36ms. The finite
generic-backend implementation goal can proceed as engineering work; it is
not a replacement scientific win. A future performance experiment needs a
new causal discriminator and decision value, not another unchanged sweep
or a demand to optimize model math merely to obtain a favorable ranking.
