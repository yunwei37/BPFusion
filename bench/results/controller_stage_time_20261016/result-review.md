# Independent controller-stage result review

Reviewed 2026-10-16 UTC against the approved revision1 plan and completed
controller_stage_full archive. Fresh result reviewer, distinct from the plan
reviewer. Only this report is written; no source changes, builds, GPU execution,
new workload or Git publication were performed.

## Judgments

- Run status: **valid** for the completed acquisition, fixed diagnostic analysis
  and the narrow instrumented-constructor comparison.
- Tested hypothesis: **supported narrowly**: instrumented loop has longer
  observed active dispatch residence per launching iteration than instrumented
  native. Its extension to an ordinary-serving causal explanation is
  **inconclusive** because instrumentation and trajectory changes matter.
- Research value: **supporting**, not a speedup or a dependency-only setup result.
- Paper impact: **additional RQ evidence and a mechanism/workload boundary**.
  There is no formal paper thesis/RQ contract to invalidate.
- Next paper decision: retain the selected ordinary implementation and native
  speed advantage; close this localization experiment without an unchanged
  rerun. Use the measured boundary to choose a distinct ordinary transport/
  progression intervention, with its own matched performance evidence.
  Neither timing-based source adoption nor an assertion that the historical
  6.36 ms is repaired follows.

No blocking defect was found for that scope. A claim of exclusive stage
causation, a latency decomposition, pure model duration, total CPU saving or
ordinary-serving speedup would exceed this experiment's evidence.

## Completion, commands and deviations

All five by four planned cells exist, with exactly the frozen per-block orders.
All 20 server terminal receipts have exit0, no forced termination, no recorded
error and no remaining BPF pins; all 20 client receipts have exit0. Ordinary
cells bind active_wait_sourcebuild16; instrumented cells bind
controller_stage_build16 trace targets. Server sources in every receipt equal
the correct archived ordinary/instrumented source snapshots. All unchanged
native-network/shared-ABI/BPF sources are identical across all receipts.

The realized matrix contains 230400 successful attempts and 14745600 measured
output tokens, with no failed/partial/protocol outcomes. Eight checked gen1
warmups per process are excluded from client metrics; internal counter scopes
include those 160 warmup tokens plus startup/loaded-idle/shutdown. The analyzer
requires all 20 condition identities rather than accepting a completed prefix.
All retained client schedules have exactly 11520 offsets, identical within
each block; model configuration and frozen prompts are also identical within
each block. Client metadata, per-I/O timeout and full drain remain unchanged.

The initial inline-I/O interpretation was rejected and revised before any
execution. The actual constructor has an independent io_network CTA. Initial
clock-order code generation and a warmup-reader filter were repaired before
serving/preflight; their earlier artifacts remain. The recorded rebuild is the
actual serving build. Artifact-only Git publication during gaps changes receipt
HEAD, not source/binary selection; no such HEAD is treated as adoption. There
is no post-result primary/oracle/timeout change or favorable-cell replacement
in the reviewed acquisition.

The source-native acquisition analyzer exits0 with empty stderr. The archived
CPU replay receipt reports byte-identical stdout and empty stderr. This
review independently checked selected raw clients and every fresh-metadata
trace, rather than rerunning the complete heavy archive analyzer again.
Owned-client deletion and original-session preservation are lifecycle closeout
receipts to be supplied by the owner; this report does not infer those from
server exit or scientific validity.

## Independent arithmetic and raw checks

All 100 emitted paired records were independently recomputed from the 20 cell
summaries, including all signed effects, means and nominal paired t95 intervals
using coefficient2.776445105, df4 and five process blocks. Six records correctly
have null effects because ordinary builds do not expose internal durations;
they are not measured zero effects. No pooled-request independence assumption
or multiplicity-adjusted conclusion is claimed.

The fixed primary, LI minus NI active dispatch duration per model-launching
iteration, is:

**+1276.054083 ns [1154.233845, 1397.874321]**, or
**+1.276054 us [1.154234, 1.397874]**.

All five block effects are positive. Average observed active dispatch is
43.875138 us for LI and42.599084 us for NI. The descriptive component means
are publication/retirement22.600927 versus21.597555 us,
packing16.989926 versus16.763892 us and launch API4.284285 versus4.237638 us.
These component means describe the instrumented constructor; they do not
prove the publication logic itself is the avoidable cause.

The outside-dispatch contrast is +2.628272 us [1.132849, 4.123696] per launch.
That interval includes model/head execution, graph scheduling, CTA return and
unbracketed bookkeeping; it is not a measured model-kernel execution contrast.

I independently decoded full raw client/response/reference joins for p0LI and
p4NI: each has11520 unique measured requests, 64 outputs each, eight gen1
warmups and737288 exact tokens including warmups. Direct client timestamps
reproduce P99 completion3611.422612 and3539.315570 ms respectively; their TPS
also reproduces. All ten full fresh-metadata files were separately streamed:
every compute row reports exact tokens, all round counts match actual launches,
and each sums737288 tokens with an exact terminal summary. This is7372880
finite dual-replayed tokens across instrumented cells including80 warmups.
The analyzer additionally checks trace admission/compute/FIFO-release coverage,
unique client_ns joins, both source-native replay summaries, histogram
identities, graph_error0, trace_overflows0 and clock_bad0.

The replay oracle is not merely the measured server saying that its own
outputs pass: unchanged mixed_replay.py resets KV tensors, reconstructs
trajectory/ownership, executes the captured graph and then invokes upstream
model execution with freshly prepared CUDAGraphMode.NONE attention metadata.
It checks actual token IDs. Both passes still share upstream model arithmetic
and the observed trajectory; they do not establish eager-HF parity or general
model fidelity. Ordinary cells have only the weaker frozen-pool membership
check. All1051 pool disagreements remain: L197, LI202, N200 and NI452. None is
a hidden exclusion or a certificate of exact untraced fidelity.

## Main baseline and instrumentation audit

Native C++ epoll is a credible competing transport, with the same resident
mixed GPU execution, checkpoint, FP16 arithmetic, slot16 setting, four prompts,
output64 and paired offered192/s schedule. It successfully engages its intended
path with no interface failure. Ordinary/instrumented rows are ablation
controls, not extra main baselines. Existing official vLLM whole-service
reference remains separate; it cannot isolate this internal stage comparison.
Native and loop can produce different batching/KV trajectories; the actual
input histograms retain those differences, so this is not equal-work
per-model-kernel timing.

The ordinary comparison remains adverse for loop:

| L minus N | Mean paired effect | Nominal paired95% interval |
|---|---:|---:|
| Delivered output tokens/s | -24.638372 | [-30.619771, -18.656973] |
| CompletionP99, ms | +130.692434 | [102.014413, 159.370456] |
| Client receive-gapP99, ms | +0.335522 | [-0.399276, +1.070321] |
| Owned group CPU, ms/attempt | -0.162614 | [-0.189810, -0.135418] |

Thus ordinary CPU is lower while TPS/completion tail remain worse; receive-gap
P99 is inconclusive. The earlier14.72-versus8.36 ms condition is not reproduced
or allocated by these results.

Instrumentation has measurable adverse delivery effects on both transports:

| Contrast | TPS effect [paired95%] | CompletionP99 ms effect [paired95%] |
|---|---:|---:|
| LI minus L | -44.787025 [-62.578379, -26.995671] | +238.099616 [142.665793, 333.533439] |
| NI minus N | -34.735153 [-43.955463, -25.514842] | +184.175755 [131.644056, 236.707453] |

The point difference between those TPS perturbations is10.051873 tokens/s,
material relative to the ordinary24.638372 gap; this descriptive subtraction
has no separately claimed confidence interval. Equal timing source is not
proof of equal overhead. These perturbations prevent translating the primary
into the ordinary critical-path allocation or an expected avoidable speedup.
They do not invalidate the predeclared instrumented association itself.

Timers use volatile GPU globaltimer reads with memory clobbers and reject
backward observations without clipping. Archived build controls show8 dispatch
reads in each instrumented library and10 in loop io_network, with original
NANOSLEEP retained and end reads ordered. BPF instructions/relocations match
selected ordinary controls. Private counter/layout/code-generation changes are
real perturbations, not shared-page ABI or scheduling-policy changes.

## Concurrent network stages and causal limits

The loop's owned-request network iterations show connection receive/reclamation/
accept residence125.065--165.953 us per iteration and reply preparation/
submission63.969--76.039 us; measured sleep is approximately0.529--0.530 us.
These are whole-process, conditional per-iteration observations, including
polling/memory stalls and concurrent work. The no-owned-request bucket is not
proof of inactivity, and source timer values are not exact sleep durations.

The independent network CTA overlaps model/dispatcher execution. None of its
six durations can be added to dispatcher time, assigned as an exclusive
request latency fraction or converted into a portion of a marginal token-gap
P99. Large connection/reply residence identifies a plausible progression/
placement investigation; it neither establishes avoidability nor justifies
deleting sleep. Shared GPU resource contention, mapped accesses, graph shape/
KV history and scheduling remain competing explanations.

The four-panel PNG was visually inspected against its plotting source and
underlying cell data. Its means/paired points and units are consistent; the
network panel correctly says independent/concurrent. Horizontal bars represent
means, not uncertainty intervals. The result text must state that explicitly,
because the figure itself does not draw95% intervals.

## Research consequence

This is new, valid supporting localization beyond earlier round counts and
older incomplete profiling. It establishes a reproducible instrumented
constructor association while bounding its translation to ordinary serving.
It does not answer the whole user objective or claim a universal eBPF win.
The next useful discriminator would change a concrete transport/progression
mechanism while preserving the GPU model/controller, then compare ordinary
matched latency/TPS and correctness against current loop and native. A
kernel-owned-network implementation is a possible engineering candidate,
not an adopted source or tested performance result in this matrix.
No broader workload, extra baseline, increased N, unchanged rerun or automatic
timer/cache sweep is required by this review.
