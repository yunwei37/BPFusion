# Fresh result review: close-scan confirmation

Observed 2026-10-16 UTC, after full terminal09:37:53.651672UTC. This is the
single fresh result review of the completed five-block close-guard run under
research-experiment-design, not another plan review. I reviewed the approved
plan/focused follow-up, frozen execution sources, original temporary raw
outputs, source-native replay records, archived copies and result report.
Only this report was written; no experiment, GPU run, source repair, package,
service or Git publication action was performed.

## Separate judgments

- **Run status: valid.** The complete planned finite comparison ran, with
 15 executors,30 cells, all7680 measured attempts and all120 excluded warmups.
 There is no observed correctness, coverage, execution or baseline-fairness
 defect that invalidates this local comparison.
- **Tested hypothesis: inconclusive.** The conservative close-scan cache has
 not established a reduction in192/s client ITL P99. The primary nominal
 paired interval crosses zero. This is neither confirmation of a useful
 effect nor proof of no effect/equivalence.
- **Research value: supporting.** The intervention adds a real causal
 discriminator beyond a timestamp correlation. Default8 protocol/lifecycle
 acceptance and packaging are dependencies, not additional scientific results.
- **Paper impact: mechanism or workload boundary.** The candidate is not a
 demonstrated explanation/repair for the historical6.36ms difference. This
 does not directly refute the entire GPU-owned I/O objective or answer the
 whole throughput/latency question.
- **Next paper decision:** publish the complete inconclusive result and keep
 the production close scan unchanged. Do not claim that this candidate
 repaired6.36ms, removed the historical kernel disadvantage, or established
 eBPF speed/CPU superiority. Continue the separately requested resource,
 remote-tail, official-vLLM-reference and reusable-backend work with the
 diagnosed host/client exposure visible. A new causal experiment needs a
 distinct decision-relevant discriminator; this result does not authorize
 repeating unchanged runs until favorable.

## Completion, source binding and comparison fairness

The admitted design retained Qwen2.5-0.5B-Instruct revision7ae55760,FP16,
16 slots,gen64,four prompts,256 normalized-gamma attempts per rate,96/192,
five process blocks and8 checked excluded gen1 warmups per executor. Actual
start orders and rate orders match the declared orders exactly. Seeds are
20261015..20261019 by block. I checked the raw schedules: each block/rate has
the same integer relative arrival offsets across all three conditions.
Timeouts are unchanged: the inherited client uses60-second sockets. Scheduled
time, thread start, connect start/end, all token arrival times and finish time
remain in raw rows; delayed launches are not silently moved to new due times.

The comparison is before kernel loop, candidate kernel loop and efficient
native C++ epoll with the same mixed GPU constructor. I checked recorded
commands, actual launcher symlink targets, private Make rules/compiler logs,
source-local header inclusion and exact source contents. Both loop conditions
use the same numerical Cu and Python bytes; candidate changes only the
published +5/-1 close predicate. Native uses the same numerical constructor
and unchanged userspace_tcp.h. The tested Cu includes each transport header
conditionally; the candidate header beside fixed_sources/vllm_graph.cu is
the one compiled. All three executed trace libraries have BF_TRACE; there is
no BF_TIMELINE/ftrace condition in this confirmation. Before/fixed binaries
and the native comparator bind to their recorded private build directories.

The full metadata's driver/client/mixed Cu/Py/replay/header strings agree with
the frozen files. confirmation_sources contains the same actual client,
analyzer, model/replay and headers frozen before preflight. Root homogeneous
backend source is also recorded in metadata for context; it is not mistakenly
used as the tested mixed constructor. The actual mixed variant and build
commands establish that binding.

The native baseline engages its intended efficient path: socket/deadline idle
waiting,eventfd shutdown, eligible-frame FIFO, no rejected requests, correct
published/completed counts and the same mixed scheduler/replays. The loop
paths show attached existing eBPF transport, no SQPOLL substitute, balanced
ring counters, all slots released and accepted connections closed. There is
no intentional compute/information advantage, weakened native path or failed
baseline interface being counted as a proposed-method win. Actual batch
trajectories differ dynamically; source equality does not imply identical
per-request schedules. Official vLLM is correctly absent from this transport
attribution comparison and remains a separate requested whole-service
reference.

All15 executor terminal states and the overall terminal are successful.
All30 cells retain256 indexed attempts, with no request_error, request_invalid
or failure rows. Thus there are no observed timeouts/failed requests to censor
in this completed run; their absence is checked, not achieved by filtering.
Measured output is491520 tokens; including120 gen1 warmups gives491640 tokens.
Every process completes520 requests/32776 tokens. All five blocks, including
the unfavorable candidate effects, are retained.

## Independent recomputation and correctness

I reran the original confirm/analyze.py on the original full.jsonl: exit0,
empty stderr, byte-identical full.analysis.stdout. I then independently
grouped raw request rows by process/rate, recomputed linear-interpolated
ITL P99 directly from adjacent client arrival timestamps, TPOT, connect/
scheduled-origin TTFT and completion P99, delivered-window output token/s,
client scheduling lag and executor process CPU. All30 cells agree with the
saved analysis within1e-10 absolute floating-point arithmetic. Independently
recomputed paired effects and t95df4 agree as reported below. Process blocks,
not individual correlated tokens, are the units for the primary interval.

I audited the source-native replay implementation. It reconstructs each
request's prompt/history and physical-slot ownership, resets cache contents,
replays the actual batch trajectory, and then independently rebuilds upstream
attention metadata from that history for eager forward/sampling verification.
Outputs are compared exactly rather than used as their own expected values.
The trace supplies the actual schedule, not an oracle of its numerical answer.
The fresh attention-metadata path does not simply replay the captured graph
or accept its trace tokens without model computation.

All15 processes have successful captured-history and fresh-metadata summaries.
I independently reconstructed ownership/admission/compute/release histories,
checked no physical-slot reuse before release, sequential FIFO releases and
all per-request output tokens against references. Fresh-metadata records,
actual request markers/client responses and terminal counters agree. Totals
are50021 compute rounds,6639 actual mixed rounds and491640 checked tokens.
Logical traces have zero overflow, graph errors and complete requests/releases.

The legacy io_uring128-record admission sample does truncate for520 requests.
This is expected and explicitly checked by the runner; it is not a complete
admission trace and must not be described as having zero sample overflow.
The complete logical trace/client/source-native replay and ring counters
supply the coverage used here. This confirmation has no timestamp stage
decomposition; the prior diagnostic's signed associations/clock limits
cannot be promoted into exclusive additive contributions to these tails.

I also reran both candidate default8 protocol analyzers: exit0 and byte-equal
saved outputs. Each Qwen/Smol executor has640 outcomes,259 intended rejections,
23376 exact output tokens and actual batches1..8. Ordinary non-BF_TRACE
candidate lifecycle results each contain144 outcomes and successful cleanup,
including mid-output/backlog cancellation. Their pre-observation reference
pool precedes execution; complete outputs/prefixes are checked with that finite
pool. Empty/unobserved canceled responses remain incomplete and supply no
numerical evidence; exact-prefix checks do not make them complete requests.
The finite ordinary output-set check is an engineering acceptance scope,
not universal numerical correctness or current batch-trajectory replay.

## Primary effect and adverse evidence

These are means of the five process-block P99 values in milliseconds, not a
pooled request/token P99:

| Rate | Before kernel | Candidate kernel | Native |
| --- | ---: | ---: | ---: |
| 96/s | 3.754489 | 3.790730 | 3.629037 |
| 192/s | 4.608287 | 4.440699 | 4.718439 |

The predeclared primary candidate-minus-before192/s ITL P99 effects by block
are +0.165075,-1.131296,+1.607038,-0.761900,-0.716859ms.
Mean **-0.167588ms**, nominal paired t95df4
**[-1.533927,+1.198750]ms**. Both signs are plausible under this finite
estimate; choosing the negative mean alone would overstate the result.

Candidate-minus-native192/s is -0.277740[-3.583043,+3.027563]ms.
Before-minus-native192/s is -0.110152[-3.058267,+2.837963]ms.
Thus the historical kernel14.723/native8.363ms gap is absent even in the
unchanged before condition. That cross-run change is not evidence of a
candidate speedup or of its causal repair. It also does not erase the valid
historical adverse result. Shared-host/client nonstationarity and short finite
windows remain competing explanations; this run does not identify their
exclusive contribution.

At96/s candidate-minus-before is
+0.036240[-0.321872,+0.394353]ms; candidate-minus-native is
+0.161692[-0.538676,+0.862061]ms. These also establish neither superiority
nor equivalence.

At192/s mean delivered-window token/s is10764.320/10955.967/11072.221
before/candidate/native. Candidate-minus-before
+191.647[-395.092,+778.387] and candidate-minus-native
-116.255[-403.394,+170.885] token/s cross zero. These windows include the
arrival schedule and drain; neither is a sustained saturation/maximum
throughput result. Means of connect-origin TTFT P99 are
139.808954/113.555680/95.234675ms and completion P99
225.004769/198.678192/179.315514ms. Their paired intervals remain in the
analysis; selecting the favorable point estimates would be unjustified.

Adverse process-resource evidence is preserved. Candidate-minus-native
executor CPU is +0.258141[+0.177460,+0.338822]ms/attempt at192/s and
+0.135698[+0.098944,+0.172452] at96/s. These conditions do not reproduce
a process-CPU saving. This CPU clock is not full service CPU, GPU queue cost,
softirq or all external kernel-worker accounting. It cannot establish total
resource superiority or infer why this difference arose.

All ordinary TTFT/completion P50/P95/P99, scheduled-origin metrics, TPOT,
ITL, throughput, CPU and lag rows are preserved. At192/s mean block client
lag P99 is5.486507/8.492538/12.398506ms before/candidate/native; at96/s
it is25.843169/29.170006/28.094637ms. Client offered-load fidelity and local
scheduling therefore remain material, even with identical nominal schedules.
No failures are discarded to improve those metrics.

## Interpretation and artifact audit limits

The root confirmation-result.md's proposed primary/effect/table numbers,
throughput, adverse CPU finding and non-adoption decision agree with this
audit. The small conservative source change passed its declared safety
checks, but safety is not evidence of material latency benefit. Five paired
process blocks on one shared machine and short arrival windows support only
the declared local finite comparison. Nominal t intervals rely on their
paired-process assumptions; residual order imbalance and shared-host drift
remain. Crossing zero is not equivalence; no production SLO, all-model or
remote-load claim follows.

The independent audit ran CPU analyses only, not a new model replay/GPU run.
The model replay evidence comes from the actual post-serving exact checks
whose source, complete per-round records, counters and successful exits were
audited. A fresh GPU rerun was unnecessary for the result review and would
be a new run rather than independent analysis of this completed run.

I compared91 original confirmation files to their archived original or
losslessly decompressed sidecar. The only intentionally different same-name
file is archive analyze.py, which adds gzip-aware reads; the executed analyzer
is retained as analyze_original.py. Both archived preflight and full analyzers
run successfully and produce byte-identical original saved stdout. No raw
observations were changed by compression.

Relevant artifacts: plan.md, plan-review.md, candidate-close-guard.diff,
confirmation-result.md, confirmation_sources/, confirmation/full.jsonl.gz,
confirmation/full.analysis.stdout, confirmation/analyze_original.py,
confirmation/analyze.py and candidate_safety/. Original authoritative run:
 /tmp/bpfusion-mixed-integration-n4cog5c6/confirm/.
