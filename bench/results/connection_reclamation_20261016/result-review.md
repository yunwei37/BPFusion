# Fresh result review: connection reclamation

2026-10-16 UTC. One independent RESULT REVIEW under research-experiment-design.
Reviewed the retained serving-performance question: does removing the steady
userspace network worker improve real remote delivery or resources with matched
resident GPU execution? There is no formal paper thesis/RQ contract in this
repository. This report neither invents one nor changes that question.

## Separate judgments

- **Run status: valid**, for the completed, correctly sourced five-block
  comparison and its bounded delivery/resource claims. All 15 processes and
  172800 measured attempts are terminal. Earlier build-invalid attempts remain
  invalid and are not pooled into this result. Client Job cleanup and canonical
  adoption are separate owner actions, not missing measured cells.
- **Tested hypothesis: supported** for the declared causal repair: replacing the
  unrelated-global-backlog close dependence with conservative peer references
  removes the observed EOF-retention/capacity failure class at this operating
  point. The larger transport-performance expectation is adverse against the
  main native baseline: local has lower delivered throughput, higher completion
  P99 and higher measured group CPU. Device-energy difference is inconclusive.
- **Research value: supporting.** It repairs and bounds a real implementation
  confound using a meaningful causal discriminator; it is not an independent
  headline throughput contribution. Build receipts, qualification and archive
  replays are dependencies of this result, not additional research results.
- **Paper impact: mechanism or workload boundary**, with additional evidence
  toward the retained RQ. This is not a direct thesis challenge, universal
  numerical validation, or evidence for general eBPF superiority.
- **Next paper decision:** retain the bounded reclamation repair and the adverse
  matched-native results together. Close this completed matrix; no additional
  baseline or unchanged favorable rerun is required. Source adoption remains
  subject to the owner's normal source integration/acceptance. Broader mechanism
  redesign is optional only if it supplies a better causal discriminator than
  the next competing use of research effort.

## Review scope and completion

Read plan.md and all three discussions in plan-review.md, preflight.md,
qualification.md, errno-result.md, build-deviation.md, collection-notes.md,
archive-replay.md, result.md, candidate-description.md; the evaluation and
closest-work context; acquisition/analysis/plot adapters; corrected build
commands; candidate and actual frozen private source; ordinary/trace/lifecycle
qualification data; all full client/resource archives and terminal/source/
command receipts. No GPU, load, build, source, Job or Git mutation was performed.
This reviewer writes only result-review.md.

An independent stdlib calculation from raw requests reconstructed every scalar
numeric cell metric in reclaim_analysis.py, including every P50/P95/P99 and
mean for connect/send/scheduled TTFT/completion, TPOT, all/positive gaps and
scheduling lag; all resource numerators and all 16 paired effects. It found no
numeric discrepancy at 1e-10 absolute / 1e-12 relative tolerance. Separate CPU
execution of the archived primary analyzer and both default8 protocol analyzers
exited0, empty stderr, and reproduced acquisition stdout byte-for-byte. Protocol
replay uses its base .jsonl path and reader gzip fallback; passing the physical
.gz name directly is not that analyzer's prefix interface.

The matrix has exactly 11520 distinct indices per cell, 60 seconds of normalized
gamma offsets, identical offset arrays and seed within each three-condition
block, identical four prompts/config/model revision and gen64, and unique
request stamps within each client process. All scheduled stamps equal epoch plus
original offsets; all responses have ordered arrival stamps. All client exits,
observer terminals, server exits and kernel attach/detach/stat commands are0.
All 15 server terminal receipts have empty owned pins. The actual process order
is exactly the plan's global/local/native; native/local/global;
local/global/native; native/global/local; global/native/local. There are120
excluded checked gen1 warmups, 172800 attempts, 168643 full successes,
4157 failures, 10793152 delivered tokens, zero partial failed tokens, zero
protocol/shape/vocabulary errors and zero recorded close errors.

| Block | Global failures / 11520 | Local failures | Native failures | Global finite-set disagreements | Local | Native |
|---|---:|---:|---:|---:|---:|---:|
|0|961|0|0|59|76|0|
|1|853|0|0|65|0|62|
|2|780|0|0|109|129|0|
|3|861|0|0|70|336|281|
|4|702|0|0|70|97|1|

Every failure is a read TimeoutError with zero received bytes and tokens;
there are no excluded failing blocks. Global final sockhash failures equal the
five client failure counts exactly, first errno is7/E2BIG in each, and local
reports zero insertion failures/errno. All queues drain, llm_reserved is0,
admitted equals retired, graph_error and trace_overflows are0. Finite first
errno is not an errno distribution. The earlier census's2947 owned CLOSE_WAIT
with queued173 and the4096 connection capacity provide mechanism evidence;
neither its sequential snapshot nor the final post-drain snapshot is an atomic
full-map measurement.

## Numbers, uncertainty and figure

The entire proposed result.md delivery/cost table and quoted primary and
secondary effects recompute correctly. Five-process means are means of cell
statistics, not pooled percentiles. Primary local-minus-global failed-attempt
fraction is -0.072170139 [-0.082609721,-0.061730557], or -7.217 percentage points.
All 16 audited paired estimates follow; units are those in metric names.

| Contrast | Metric | Signed mean | Nominal t95 lower | Upper |
|---|---|---:|---:|---:|
| local minus global | failure_fraction | -0.072170139 | -0.082609721 | -0.061730557 |
| local minus global | connect_completion_ms_p99 | -2372.687037098 | -3273.355463585 | -1472.018610611 |
| local minus global | server_host_active_cpu_s_per_attempt | -0.022166319 | -0.024586924 | -0.019745715 |
| local minus global | owned_group_cpu_ms_per_attempt | -3.050975169 | -3.351076012 | -2.750874325 |
| local minus global | workspace_cgroup_cpu_ms_per_attempt | -3.156359462 | -3.451507389 | -2.861211535 |
| local minus global | device_energy_J_per_attempt | -0.251015069 | -0.275956194 | -0.226073945 |
| local minus global | output_tokens_per_s | 3829.968487521 | 3550.624237938 | 4109.312737103 |
| local minus global | client_token_gap_ms_p99 | -4.599979024 | -4.666284528 | -4.533673520 |
| local minus native | failure_fraction | 0.000000000 | 0.000000000 | 0.000000000 |
| local minus native | connect_completion_ms_p99 | 96.432967350 | 44.854261323 | 148.011673377 |
| local minus native | server_host_active_cpu_s_per_attempt | 0.000791146 | 0.000195394 | 0.001386897 |
| local minus native | owned_group_cpu_ms_per_attempt | 0.963469867 | 0.863478266 | 1.063461468 |
| local minus native | workspace_cgroup_cpu_ms_per_attempt | 0.958398576 | 0.867612982 | 1.049184171 |
| local minus native | device_energy_J_per_attempt | 0.006299080 | -0.003749479 | 0.016347639 |
| local minus native | output_tokens_per_s | -19.697640000 | -28.805820811 | -10.589459190 |
| local minus native | client_token_gap_ms_p99 | 0.165252640 | 0.075087164 | 0.255418116 |

The t multiplier is2.776445105, sample SD of five paired block differences,
divided by sqrt(5), df4. These are predeclared nominal small-sample intervals,
not simultaneous/multiplicity-adjusted intervals, production failure-rate
bounds or proof of independent stationary processes. All secondary signs remain
visible. Zero local/native differences give [0,0] only because this finite
block statistic is identically zero; it does not establish equivalence or bound
rare failures. The native mean is11642.740923 token/s versus local11623.043283;
completion P99 is3313.845881 versus3410.278848ms; group CPU is0.732279571 versus
1.695749438ms/attempt. These support no native superiority reversal.

Success-only global completion tails omit7.217% of attempts; consequently global
all-attempt P95/P99 completion cannot be reported as a finite successful latency
from these observations. Failures are terminal timeout outcomes, not completed
60s responses. Throughput divides delivered tokens by the interval from offered
schedule epoch through full terminal drain: global86.369-91.156s,
local/native63.279-63.472s. That is achieved all-attempt delivered throughput
under this workload and timeout path, not saturated GPU compute throughput.

Visually inspected completion_ecdf.png and reviewed the common PNG/PDF plotting
code. Pooled and faint per-block curves divide successful completions by all
attempts; the global curve ends at92.782986%, local/native at100%. The dashed
horizontal extension does not turn failures into successes. Axes, legend and
counts are consistent. This is a subdistribution of observed completions;
there is no inferred failure-completion time or missing-mass redistribution.
The figure accurately shows global's mixed early mass and worse upper delivery
mass; it does not imply stochastic dominance at every percentile.

Client token-gap measurements reuse one read timestamp for every token decoded
from that read. Mean zero-gap fractions are global63.613883%, local23.895365%,
native21.541639%. They measure client receive grouping; the zeroes are neither
zero GPU token-generation time nor official output ITL. Both positive-only and
all observed gap summaries remain archived. Client scheduling-lag P99 ranges
5.013-12.013ms across cells; scheduled-origin summaries retain that exposure.
No cross-host timestamp subtraction enters delivery latency.

## Build, source and main-baseline fairness

All seven candidate files byte-match the actual TEMP/reclamation_source frozen
files. Full server receipts embed that same executor/header/BPF source. The
corrected48 build-command receipts all exit0 and explicitly cover local8,
local16 and global16, including nvcc -dc candidate source selection and candidate
include precedence. The16 compile defines apply consistently to BPF, loader and
GPU; global differs by BF_IO_GLOBAL_PENDING_GUARD. Actual CPU cuobjdump of the
corrected local/global16 libraries confirms identical model-dispatch SASS and
different io_network SASS. Archived default8 comparison confirms unchanged
native networking. The executor vllm_mixed.cu and native userspace_tcp.h are
byte-identical to pre-adoption2c0cf7b. Git1ae46d6 is artifact provenance, not proof
of canonical-source adoption.

The native condition is the single main competitor and engages its intended
mechanism: ordinary C++ nonblocking sockets, eligible-frame FIFO, epoll_pwait2,
60000ns active completion wait, socket/deadline idle waiting and eventfd stop.
It completes every request with no rejection or avoidable baseline failure.
It uses the same resident model executor, weights/revision, precision, prompts,
slots16, generated token budget and TCP_NODELAY. No evidence of a disadvantaged
compute or information budget was found. Its lack of the candidate's BPF
bookkeeping is a competing implementation's real cost, not a reason to add that
cost artificially. Official vLLM whole-service evidence already has a separate
role in finding0069; this matched component question does not require rerunning
it or adding another baseline.

Global is correctly labeled a component ablation: it shares pending metadata,
ABI and the corrected pending-before-fresh-head order. It is not untouched2c0cf7b
and cannot quantify bookkeeping overhead versus that old implementation.
Removing observed capacity failures relative to this ablation cannot establish
superiority over native; the actual native comparison points the other way.

## Ownership and correctness boundary

Source review finds producer reference increment before pending publication,
rollback on push failure, sole consumer slot/head publication before bucket
release, and GPU system acquire of pending before a fresh head/seen comparison.
Actual RECV CQE res0 sets EOF. Reclaim also requires no receive reference and no
active reply; dead without EOF keeps the global guard. Hash representation is
shared by BPF and GPU and collisions add conservative references, so a collision
can postpone close rather than cancel another peer's ownership. There is no live
counter reset; quiescence and map removal retain the shutdown boundary.

The upstream version cited in the plan was opened during this review:
[Linux tcp_bpf.c v7.3-rc3](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/net/ipv4/tcp_bpf.c).
Its parser receive path locks the socket, processes preaccept receive data and
checks redirected ingress before its EOF/shutdown returns. This supports the
specific EOF argument; it is not a universal safety proof for other kernels,
protocols, or arbitrary reset/error traffic.

Independent CPU reconstruction joins all105 targeted wire replies by unique
client_ns to admission and model-compute events and the captured-model replay;
all6153 tokens match. Fresh-metadata replay has782 matching compute rounds,
terminal exact=true,6153 checked tokens and105 requests. At nonblocking observed
EOF the own/colliding bucket is0 while unrelated global pending is40, following
an earlier bucket40/global88 observation. No intervening request is introduced.
Same-peer port reuse succeeds. Thus the corrected trajectory actually exercises
reclamation under unrelated backlog; the earlier blocking-read observation did
not establish this and remains withdrawn.

The default8 Qwen/Smol protocol archives independently replay to2560 outcomes
and93504 exact tokens, with invalid-frame rejection, mixed batches, pipeline/
half-close and slot/release controls. Four ordinary lifecycle receipts pass
queued-reset, partial-output and stop/drain within their declared cases.
Four generic matmul/FFT transport cases have182 checks each and pass analytic/
numeric controls. These are useful engineering coverage, not universal RST-flood
or backend stability guarantees.

Full-run finite frozen-set disagreements remain373 global,638 local,344 native,
1355/168643 total. The unchanged finite-set check is not an exact full-run model
oracle. Targeted collision dual replay despite9 such disagreements establishes
that particular trajectory, not every full-run output or the original trace-less
failure. No output-pool expansion or new circular method-output oracle was found.
The observations support protocol-valid delivery and bounded lifetime repair;
claims of full-run exact numerical parity, external-server equivalence or model
quality would be unsupported.

## Resource audit and collection deviations

All30 resource gzip files, including15 idle brackets, decompress byte-for-byte
to the original acquisition resources. Active sample brackets are65.869-94.111s.
Process-group membership/starttimes remain stable for all full cells. Group CPU
uses process CPU clocks once per process leader; io-wq threads' recorded TGIDs
match the actual server and their CPU is already inside group CPU. It must not
be added again. The finite thread ledger is lower-bound tick/scheduler evidence:
workers born/dying between one-second detail censuses can be missed. Recorded
zero worker deltas do not prove zero work or allocation.

Nested group, Workspace cgroup and host counters are never summed. Host active
CPU uses user/nice/system/irq/softirq without counting guest again; whole-device
energy is a difference of monotone energy counters. Observer CPU is visible
(4.316-5.825s per active bracket) and is separate from service-group CPU but
inside shared host/Workspace exposure. Counter reads are sequential, so endpoints
have sampling skew; these are control/observer brackets, not exact per-request
instruction attribution. Resource costs divide full numerators, including failed
work and drain, by all attempts; successful-output denominators in details do
not remove failed-work cost. No double counting was found.

Startup/model capture/shutdown are outside the declared steady-serving bracket.
Idle loaded device mean power101.991-106.379W is whole-device observation, not
an isolated queue cost or a no-model baseline. NVML compute-app samples contain
one app set in each cell; that does not eliminate unobserved device work or
shared-host activity. Utilization100% is not SM saturation. Static GPU usage
is48 registers/168 stack bytes for both network variants and40 dispatch
registers; this is not dynamic cycle/energy attribution. The actual16 ctl map
receipt reports38208-byte value and45056-byte memlock; 40960-byte mmap rounding
is consistent, and the appended pending buckets add16384 bytes.

The missed nvcc -dc rewrite is an actual invalid build, not an unfavorable
candidate result. Invalid old-guard qualification/preflight data stay separate;
corrected affected builds, qualification and comparisons were repeated before
full acquisition. Third preflight retains expected global499 failures versus
local0 and real mechanism engagement. The changed collision oracle path is
recorded and tested in full; the initial failed trace-less trial and invalid
old-guard trace remain, with no retrospective favorable explanation.

Both stdout resets occurred after measured client exit0 and observer terminal;
the same original cells were recovered, and none was measured again. The
resumed order matches the plan. Gaps after pair1/local and pair2/local server
stop are246.559s and414.739s versus roughly5-9s elsewhere. Shared-host and
thermal/time exposure remain competing explanations for small secondary effects;
no process or block is excluded and no absence-of-interference proof follows.
The primary difference's repeated capacity counter engagement is stronger than
a small timing-only claim.

**Report wording correction found and resolved during this review:** result.md's original unqualified statement
that heavy compression occurs after server stop is too broad. All three
acquisition scripts gzip/transfer measured client data after observer terminal
but before the finally block stops the server; warmup transfer precedes idle.
Resource/durable archive compression is after server stop and before the next
cell. Distinguish these operations. Measured resource intervals exclude client
transfer, but the resident server can keep running during transfer and longer
gaps can affect later conditions. This is a prose correction, not evidence of
an affected measured cell or a reason for a replacement run.

No new scientific run, baseline, model change or extra review round is required
by this review. The owner corrected result.md and collection-notes.md before
review close; the correction is visible in the current files. Supplemental
host-observation.md records a finite lab journal query for12:53-13:49 UTC with
no matched storage/OOM/Xid/kernel/NVMe/AER failure patterns. This reviewer read
that receipt, not its953306-byte OS TEMP journal; it neither rules out faults
nor explains the exec resets. Preserve the negative native comparison and finite-oracle,
shared-host, timeout and scope qualifications when integrating the result.
