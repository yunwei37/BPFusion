# Independent kernel-network placement result review

Reviewed 2026-10-16 UTC under research-experiment-design RESULT REVIEW by a
fresh reviewer distinct from the plan reviewer. Only this report is written.
No source/build changes, BPF attachment, GPU/model/benchmark run, Git mutation or
runtime mutation was performed.

## Judgments

- Run status: **valid** for the completed, source-frozen ordinary acquisition
  and its declared finite correctness scope, including verified owned-client
  cleanup and preserved original sessions/source.
- Tested hypothesis: **supported** for K-minus-L delivered tokens/s on this
  Qwen/RTX5090/16-slot/192-request-per-second workload.
- Research value: **supporting**. This is an actual ordinary network-placement
  intervention, rather than another setup pass or instrumented timing proxy.
- Paper impact: **additional RQ evidence and a mechanism/workload boundary**.
  It neither establishes general eBPF superiority nor challenges a formal
  thesis; this repository has no formal paper RQ/thesis contract.
- Next paper decision: retain the positive local placement result together
  with its CPU cost and unresolved native contrasts. Source integration is an
  owner decision after ordinary acceptance. Do not claim equivalence with
  native, total CPU savings, arbitrary-backend portability or repair/allocation
  of the historical unreproduced 6.36 ms.

No invalidating scientific comparison defect was found. A wider speed or
resource claim would exceed the admitted comparison.

## Completion, commands and frozen inputs

I read plan.md and all plan-review discussions, source/, ordinary build
receipts and compiled controls, qualification and preflight artifacts,
kernel_network_server.py, the matrix/client/resource/analysis/plot scripts,
acquisition.md, client runtime context and archive replay receipts. I also
read docs/evaluation.md and completed 0076 result/review as the preceding
mechanism context.

All five by three planned cells exist. Independent terminal-receipt ordering
is exactly K,L,N; L,N,K; N,K,L; K,N,L; L,K,N. All 15 server and client exits
are zero, with no forced server termination, recorded error or remaining
BPF pins. All eight gen1 warmups per process succeed and match their fixed
references, and are excluded from measured request metrics.

The full acquisition has 172800 attempts, 172800 successes, 11059200 measured
tokens, zero failed/partial/protocol outcomes and 120 excluded warmup tokens.
Every retained schedule has the exact 11520 predeclared offsets, ends at
60000000000 ns, and uses seed 20261015+block. Client source and frozen model/
prompt configuration match the archive in all 15 cells. Within each block
all conditions use the same offsets. The fixed 60-second per-I/O timeout,
all-attempt recording, complete drain and fixed primary are unchanged.

All condition-specific server source snapshots are stable across the run.
Shared network/BPF/model controls are identical across conditions. K receipt
sources equal the archived candidate files; L and N use the same selected
active_wait_sourcebuild16 directory, while K uses kernel_owned_build16.
Artifact-only main 904e1e1 changes only experiment artifacts relative to
8ad0af0. The recorded HEAD transition does not substitute for binary identity,
change measured sources or indicate production adoption.

The source-level mixed CUDA difference is only the transport-header include.
I independently normalized the archived emitted instruction streams, retaining
predicates, opcodes and operands. At both 8 and 16 slots, ordinary K/L/N
dispatch streams match exactly (1464 instructions); traced K/native dispatch
streams also match (1656). K has no io_network function; L does. This engages
the placement intervention with unchanged emitted GPU controller computation,
but it remains a bundle including CPU-owned state/token copying and changed
network progression. It does not isolate one fence, softirq, queue or timer.

The recovered SSH timeout was recorded during post-serving data recovery;
all original cell data and successful terminals remain. acquisition.md
retains the subsequent live API observation: all 11 nodes Ready and Lease
ages below their observed 40-second durations. No failed cell was replaced
and no runtime/source/metric repair followed that transfer gap.

## Independent arithmetic and figures

I independently recomputed all 69 paired rows from their five cell summaries:
effects, signed means and nominal paired t95 intervals (df4,
coefficient 2.776445105) agree. Independently reading every request of block4
K/L/N reproduces delivered TPS, completion/TTFT P99, receive-gap P99 and
scheduling-lag P99; all 11520 request indices and complete 64-token outputs
are present for each sampled condition. The acquisition analyzer checks the
complete matrix, not a favorable prefix. Its already completed full archive
CPU replay has exit0, byte-identical stdout and empty stderr; I did not rerun
that entire heavy analyzer.

| Contrast | Delivered tokens/s, mean [nominal 95%] | Completion P99, ms, mean [nominal 95%] |
|---|---:|---:|
| K minus L, fixed primary TPS | +25.343567 [15.901519,34.785614] | -124.193195 [-178.409430,-69.976960] |
| K minus N | -2.735807 [-15.548018,10.076404] | +20.997933 [-41.893880,83.889746] |
| L minus N | -28.079374 [-43.281968,-12.876779] | +145.191128 [77.364158,213.018098] |

Mean cell TPS is L11615.073581, K11640.417148 and N11643.152955.
The supported primary is approximately 0.218% over L. K/native
zero-crossing intervals do not establish equality, noninferiority or a native
win. Secondary intervals are nominal descriptive comparisons, without a
family-wide multiplicity claim.

K-minus-L owned-group CPU increases by 0.189713 ms/attempt
[0.160377,0.219050], approximately 28.5% over L. K-minus-N owned CPU is
+0.032985 [-0.040210,0.106180], unresolved. K-minus-N mean TPOT is adverse:
+0.003901905 ms [0.001569381,0.006234429]. This supported secondary cost must
remain alongside the favorable primary and completion comparison.

Receive-gap P99 contrasts remain inconclusive: K-minus-L -0.124218
[-0.649177,0.400742] ms; K-minus-N -0.180676 [-0.977015,0.615662] ms.
These are client receive timestamps with coalesced zero gaps, not a direct
per-model-token GPU execution clock. Marginal P99s cannot be added or
subtracted into a stage allocation.

The four-panel PNG was visually inspected against plotting source and cell
values: all five paired points/lines and the horizontal means agree for TPS,
completion P99, owned CPU and receive-gap P99. Horizontal bars are means,
not confidence intervals; the report must say this. The actual PDF is a
complete single-page vector document with matching dimensions/text and is
produced from the same figure. No PDF raster renderer was available in the
review environment, so PDF structure/text was checked rather than claiming
a separate raster visual inspection.

## Correctness, adverse evidence and oracle limits

The first default8 qualification completes both models. Independent joins
between each 640-request client log, GPU trace and reference replay reproduce
all 23376 observed token IDs/model. Fresh upstream attention metadata checks
5591 Qwen and 6128 Smol compute rounds. Each model retains 259 expected
rejections and actual batches1..8. Captured-graph/KV/history plus fresh
metadata replay is meaningful finite trajectory checking; shared upstream
arithmetic does not establish eager-HF or general-model parity.

The two ordinary lifecycle fixtures each retain 144 input frames, 78 accepted/
closed connections, 88 admitted/completed requests, 58 aborts and 56 queued
frames cleaned at stop. Qwen733 and Smol813 observable prefix tokens are
checked; canceled unobserved tokens are not certified. Rings balance and
pending/reserved/error/drop/overflow are zero. Independent strace inspection
finds no accept/recv/send call after recorded NET_READY: the 53 such startup
calls/model precede it. The real ordinary BPF path serves and drains without
a steady userspace request worker; it still executes CPU work in the kernel.

Distinguish GPU/model trace loss from the bounded transport reply-record
buffer. GPU trace_overflows is zero in the exact qualification. Network
RESULT trace_count640/trace_overflow512 is the expected 128-record truncation,
explicitly required by the unchanged protocol analyzer. Full ordinary K/L
transport trace_count11528/trace_overflow11400 is likewise retained. This is
not SQ/CQ overflow, but it prevents a complete per-reply transport-trace claim.
The initially broad qualification prose was clarified during this same review
pass to distinguish these counters. The corrected qualification.md preserves
all raw results and correctness predicates; this documentation issue is closed.

Preflight retains all 13 pool flags (L12/K1/N0); full ordinary acquisition
retains all 996 (L184/K169/N643). None is excluded, relabeled as an exact
match, or used to expand the frozen reference pool. Full untraced performance
therefore establishes successful framing/count/range/counter behavior with
explicit weak reference flags, not exact full-run model fidelity. The unequal
flags do not by themselves prove semantic failure or K semantic superiority.
Separate traced qualification cannot certify every untraced full-run output.

## Baseline and resource interpretation

N engages its intended efficient epoll/timed-wait mechanism, completes every
request and uses the same resident upstream-vLLM checkpoint, precision and
GPU computation. There is no avoidable baseline transport failure counted
as a K win. L is the placement/component ablation. Official vLLM0069 remains
a separately dated whole-service external reference with different HTTP/
token/KV/scheduler behavior, not evidence that this new K constructor beats
the official server. No additional baseline is needed to interpret this
specific placement test.

The offered 12288 output tokens/s exceeds all observed delivered rates.
Backlog amplification is plausible, but this finite client-delivered
comparison does not measure exclusive server saturation capacity or allocate
internal queue/prefill/softirq latency. Client CPU is roughly 5.32--5.36
ms/attempt; mean cell scheduling-lag P99 is L8.988/K9.442/N8.968 ms. Actual
client cpu.max is max, with no recorded quota throttling; this does not
exclude client event-loop/CPU limitations. Retain scheduling and client CPU
alongside service metrics.

Sampled resource raw data independently reproduce the block4 group values;
groups are stable, candidate/old-loop snapshots include visible io-wq threads,
and only the serving GPU process is listed in those sampled cells. Whole-host
CPU/IRQ/softirq, Workspace cgroup and device energy remain shared, nested or
bracketed views. Observer/control work and unrelated busy lab workload prevent
adding them into an exclusive total-service cost. No total CPU/energy saving
is established.

## Lifecycle closure and next decision

Within this same ongoing review pass, I read the completed result.md,
mean_latency_context.md, corrected qualification.md, finding0077 and the
updated README/evaluation/architecture text. Their numeric tables, relative
effects and supported/inconclusive/adverse interpretations agree with the
recomputed results. The mean identity completion=TTFT+63*TPOT holds independently
for all 15 cells. K-minus-L mean completion improves64.172157 ms, of which
64.030563 ms is connect-origin TTFT and0.141594 ms is first-to-last receive
span. This is a descriptive location in client time, not an internal stage
decomposition. All stated secondary costs and native uncertainty remain.

Actual client CPU ranges0.941509--0.984318 core over each recorded client window,
which reproduces the report's0.94--0.98 range and reinforces its capacity caveat.
The reported future sustained official-vLLM reference is a proposed next
comparison, not a result established here.

I matched cleanup.json Job UID c4ff0ae9-89b3-4ee9-8f21-955cc88d912c and Pod UID
e9f16759-38f8-40bf-acdc-2b2e61690c09 to client_started.json. Independent read-only
live ignore-not-found queries for the actual Job and Pod both exit0 with empty
stdout. Live Workspace checks independently confirm no BPFusion pins or GPU
applications, no production diff in executor/bpf/Makefile, preserved foreign
tools/setup_env.sh and original PID1/10909 start ticks8626595/8662925.
Owned-client cleanup is complete, not merely requested. Candidate remains
unselected and accepted0074 production source is unchanged.

No outstanding scientific or lifecycle blocker was found for closing this
fixed experiment. These are final checks within the same result review,
not another review round, a repeated experiment or authority for source adoption.

The admitted local prediction is supported with a real CPU tradeoff.
Close this fixed comparison without an unchanged rerun, increased N or renamed
primary. Any ordinary-source choice must preserve that tradeoff and the
unresolved native comparisons. It can support separating network progression
from reused computation; the protocol, queue ABI and generation scheduling
remain LLM-specific, not a stable arbitrary CUDA-kernel plugin. Historical
6.36-ms allocation, long reset-pressure reliability, generic backend acceptance
and exclusive total resources remain open boundaries.
