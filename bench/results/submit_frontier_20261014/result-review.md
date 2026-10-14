# Submit-frontier independent RESULT REVIEW

Reviewed 2026-10-14 in the original yunwei356/bpfusion-dev Workspace.
Repository main was ceadcc06825e23d99684aa05ee0da02b17126853 with precisely
the qualified six-line candidate in executor/qwen_graph.cu and
executor/vllm_graph.cu plus unrelated untracked tools/setup_env.sh.
This review did not edit source, plan or paper, run new serving experiments,
change an oracle, restart a serving command, publish Git or clean artifacts.

## Distinct judgments

- run status: valid, completed for the declared finite matrix and qualifications.
- tested hypothesis: supported for reduced vLLM gen1/c8 client latency versus
  the pre-intervention coalesced control, and selected ordinary observations
  show fewer model rounds. Causal mediation in the ordinary full matrix remains
  inconclusive. A portable no-regression interpretation is contradicted by
  the AMK short-output regression; general superiority over native TCP is
  contradicted by the retained native latency losses.
- research value: supporting. The scheduling intervention adds nonredundant
  evidence about a material latency boundary. Protocol/build/lifecycle checks
  remain dependencies, not separate research contributions.
- paper impact: mechanism or workload boundary. There is no formal paper
  RQ/thesis contract in this repository; the retained user serving/performance
  objective is not replaced with an invented RQ or a direct thesis challenge.
- next paper decision: report a partial vLLM latency repair and an AMK transfer
  cost, retain the native competitor and every adverse/inconclusive row, and
  do not promote this uniform two-dispatcher policy as a universal default or
  claim the complete performance objective is achieved. Any further experiment
  needs a distinct high-value discriminator for the remaining native gap;
  this unchanged matrix is closed.

## Completion and independent methods

I read plan.md, plan-review.md, candidate.diff, source_freeze.json,
the source_snapshot, the literal pre-edit sources, Makefile.original,
rebuild_original.py, build logs and receipts, run.py, full command declarations,
matched_serving.py, analysis.py, actual full/qualification/probe/lifecycle records,
the corrected and initial observation analyzer and their receipts,
docs/evaluation.md, and findings0048/0051. Source inspection included
io_uring_tcp.h, both dispatcher loops, userspace_tcp.h, uring_loop.bpf.c,
the reused Python builders and the client CPU/arrival measurement path.

The full wrapper's actual PID373491 is absent, its terminal receipt records
exit0 at 2026-10-14T14:02:52.390110+00:00, and every fifteen model/block
driver receipt is exit0. The source-native analyzer receipt is exit0 at
14:04:46.662266+00:00. There are exactly45 executors,180 cells,
5760 measured requests/187200 measured tokens, and360 separately checked
excluded warmups. No failed or replaced serving cell is hidden.

The fifteen expanded full.commands.json entries equal
full_declared_commands.json byte-content as parsed. The source/command
declaration was written at13:29:31 UTC, before the full wrapper at13:41:58
and its first raw driver. All recorded full driver sources match the
source-native adapter; their embedded current CUDA sources match the frozen
snapshot and their embedded original source matches the pre-edit control.
Every listed frozen production source still matches the current repository
bytes at review time.

I independently grouped the raw requests by model/backend/process block,
path, generation and concurrency. For every request I verified output length,
ordered arrival timestamps, unchanged frozen whole-output pool membership,
and recomputed TTFT, completion and TPOT from start_ns/arrival_ns.
For every cell I reconstructed first send and final arrival, output-token
throughput, the32 unique measurement indices and CPU measurement brackets.
CPU deltas were recomputed from before/after process-clock and TX-clock
snapshots. The resulting180 cell summaries independently reproduce all
36 published means and all108 signed paired effects exactly, including
the five individual block deltas and nominal paired t95(df4) intervals.
I also reran the source-native CPU-only raw analysis for all15 full drivers
and all three protocol files; all pass. These are reanalyses of preserved
data, not new serving experiments.

The uncertainty unit is the five paired process blocks, not5760 independent
request samples. The interval formula uses2.776445105 * sample_sd(delta)/sqrt(5).
Five of six path permutations and odd block model/cell reversal were respected.
Residual ordering, thermal/frequency drift and other time-varying conditions
remain possible. Intervals are nominal and not multiplicity-adjusted; crossing
zero does not prove equivalence or noninferiority.

## Source intervention and baseline fairness

The only source mutation is two comments and two identical two-line predicates,
one per BF_IO_COALESCED dispatcher, after io_progress:
retired==seen && mapped SQ head!=mapped SQ tail causes continue.
There is no added worker, model math, precision, packing/KV policy, page ABI,
timer, fixed batching threshold, runtime service or permission change.
The io_load reads are system-acquire; existing I/O publication system-orders
prepared data and release-publishes SQ tail. Model-idle admitted work is
distinguished from sockets/pending I/O/model-pending queue entries.
The predicate waits on SQ consumption rather than CQ or TCP completion.
Stop is revisited on each continue. It leaves already-admitted unfinished
computation eligible and preserves the shutdown ownership handoff.

The actual BPF issuer consumes published SQEs then treats CQ progress
separately. Equality can coexist with outstanding asynchronous I/O.
There is no predicate activation counter or authenticated per-cell GPU-time
measurement; this experiment tests the policy and its collective ordering
effects, not a pure access-latency, PCIe, occupancy or identified mediation
claim. Stalled submission can delay new model admission until stop; arbitrary
fairness/backpressure/liveness bounds remain unproved.

The old coalesced condition is a component control, not external SOTA.
I verified original_io_uring_tcp.h, original_qwen_graph.cu,
original_vllm_graph.cu and original_Makefile directly against git show ceadcc0.
The saved actual pre-edit libraries and separately rebuilt snapshot controls
have equal normalized SASS on independent cuobjdump inspection:
AMK3 functions/3656 instruction lines, vLLM3/4872.
The control is not silently the candidate.

The one main competitor is efficient native epoll TCP with
BF_USER_NETWORK_WAIT and epoll_pwait2 timeout_ns=60000; its actual executor
logs contain the intended wait marker, successful computation/completion
counters and no interface failure. It retains the same per-workload resident
model math and vLLM BF_PAD_PREFILL/BF_PREFIX_RELEASE flags.
The AMK and vLLM source recipes use the same170-SM RTX5090, model snapshots,
common temporary runtime and per-workload builder/bank/precision choices.
vLLM old/candidate/native all retain its CUDA-runtime linking recipe;
AMK uses its own recipe. Cross-backend differences are not a fusion effect.
The source-only six-line change changes realized admission/batching history;
identical model code does not imply identical batches.

No avoidable native interface/compute-budget failure was found.
Native wins remain substantive evidence against overall superiority.
The older independent network-worker comparison is cited rather than
redundantly added as another main baseline.

## Primary means and paired effects

Units: TTFT ms for gen1/c8; output token/s for gen64/c8.
Path order in this table is old coalesced, efficient native TCP, candidate.

| Workload | gen1/c8 TTFT old / native / candidate | gen64/c8 TPS old / native / candidate |
|---|---:|---:|
| AMK Smol135M |130.568611 /129.459725 /131.920117 |300.956502 /303.712664 /301.532471 |
| vLLM Smol135M |6.992107 /1.968652 /5.091485 |5286.312735 /5540.676521 /5340.193444 |
| vLLM Qwen0.5B |8.601220 /2.511788 /6.875646 |4525.631656 /4816.390813 /4564.005932 |

All signed effects are candidate minus comparison; negative TTFT is better,
positive throughput is better.

| Workload / metric | versus old mean [t95] | versus native mean [t95] |
|---|---:|---:|
| AMK gen1/c8 TTFT |+1.351507 [+.387822,+2.315192] |+2.460392 [+1.023886,+3.896898] |
| Smol gen1/c8 TTFT |-1.900622 [-3.042158,-.759086] |+3.122832 [+2.059875,+4.185789] |
| Qwen gen1/c8 TTFT |-1.725574 [-3.130448,-.320700] |+4.363857 [+3.024918,+5.702797] |
| AMK gen64/c8 TPS |+.575969 [-.605341,+1.757279] |-2.180192 [-3.235810,-1.124575] |
| Smol gen64/c8 TPS |+53.880709 [-131.165198,+238.926615] |-200.483077 [-508.337580,+107.371427] |
| Qwen gen64/c8 TPS |+38.374277 [-87.502549,+164.251102] |-252.384880 [-374.090134,-130.679627] |

The measured vLLM short-output TTFT means decrease27.18%/20.06% versus old
(cohort point estimates), with all five signed old-control block deltas negative.
These local latency improvements are supported, while candidate remains about
2.59x/2.74x native TTFT and every native block delta is positive.
Do not turn the relative improvement into native parity.

Retained signed primary blocks:
- Smol TTFT vs old: -.949477,-3.115572,-1.686986,-1.185171,-2.565904.
- Qwen TTFT vs old: -2.918205,-2.684118,-.290606,-1.849073,-.885868.
- Smol TTFT vs native: +3.881232,+2.331976,+2.927403,+4.149648,+2.323903.
- Qwen TTFT vs native: +3.060864,+3.501099,+5.696636,+4.573066,+4.987623.
- AMK TTFT vs old: +1.388875,+2.097628,+1.731910,+.052152,+1.486969.
- AMK TPS vs old: +.479190,-.467919,-.223582,+1.543106,+1.549049.
- Smol TPS vs old: -1.845531,+315.235450,+8.547882,+9.273866,-61.808123.
- Qwen TPS vs old: +14.992268,+218.317959,-12.530342,-16.710162,-12.198339.
- Smol TPS vs native: -402.557344,+17.231050,+111.222607,-305.335450,-422.976245.
- Qwen TPS vs native: -270.204520,-81.098881,-311.397370,-279.236174,-319.987455.

No gen64/c8 candidate-versus-old TPS interval excludes zero; no throughput
improvement is established by this run. AMK and Qwen native losses do exclude
zero. Smol native throughput has mixed block signs and a crossing-zero interval,
which is inconclusive, not parity.

All other cells/metrics are retained in full.analysis.json and its raw sources.
Notable adverse secondary evidence: AMK gen1/c1 candidate-minus-native TTFT
+.131663 [.085347,.177980] ms; AMK gen64/c1 completion
+3.452749 [3.199555,3.705942] ms; AMK gen64/c8 completion
+12.096247 [6.234619,17.957874] ms and TPOT+.168098
[.079371,.256826] ms. Qwen gen64/c8 completion versus native
+5.768220 [2.911698,8.624743] ms and TPOT+.090759
[.048762,.132755] ms. All vLLM gen1/c1 TTFT effects cross zero;
there is no supported c1 TTFT gain or equivalence claim.

Known-worker CPU per gen64/c8 request, old/native/candidate seconds:
AMK .004847111/.004095878/.004803799;
Smol .000465583/.000387157/.000437890;
Qwen .000519660/.000446528/.000505703.
Candidate-minus-native CPU intervals are positive for these cells and many
others. These process/TX clocks exclude total host/kernel-BPF/softirq/client
CPU and energy; they cannot support total CPU savings. Executor process CPU
includes attributed syscall time; do not describe it as excluding all kernel CPU.

## Correctness, protocol and ownership

Frozen_references.json, smol_frozen.json and qwen_frozen.json are byte-identical
to the prior queue_batch archive, not broadened after observations.
Every ordinary measured and warmup output passes finite whole-sequence set
membership at fixed inputs. This is not current-batch exact equality,
representative text/task quality or all-input numerical fidelity.

Three candidate protocol runs each complete622 requests/22224 tokens,
including259 selected rejects and5000 empty connection churn.
The source-native checks and independently reanalyzed raw records cover
fragmentation, invalid HTTP/binary cases, halfclose/pipeline/wrap and empty
queues/slot reservations. AMK reports22224 model steps and all eight
private graph errors0. Traced vLLM qualifications have actual batch sizes1..8:
Smol7001 compute rounds/147 release rounds; Qwen7102/134.
Release/KV ownership and exact request association pass.

I inspected the reused trace replay implementation: it reconstructs packed
input IDs, padding, positions, sequence lengths, physical block/slot mapping
and per-request history, replays the reused vLLM body/head graphs, and compares
independently recomputed sampled output to recorded tokens. It is independent
history reconstruction/replay, not a fresh eager-HF oracle or an independent
implementation of model arithmetic. Use precise wording.

The stronger old AMK eager-HF test remains failed at the third greeting gen64
case, zero-based token16; findings0048/0051 retain that evidence and upstream
170-SM reproduction. Matching a finite previously observed pool does not
repair this failure. This review does not certify generic exact AMK correctness.

Three candidate lifecycle files independently contain32 actions,652 checked
complete-or-prefix tokens, all recorded exact checks true, native exit0,
three aborted requests, graph/model errors0, accepted==closed,
completed==head==32, empty SQ/CQ, pending/reserved/error/dropped/overflow0,
empty remaining pins and free BPF slots. RST/SIGTERM prefixes are explicitly
partial;652 is not a claim that every submitted long reply completed.
These finite cases do not prove every possible fault race or backpressure bound.

Protocol strace after the actual resident-ready marker and before SIGTERM
shows no accept/recv/send request syscall and one blocking io_uring_enter
loop start for each candidate workload. Source and log show coalesced GPU
network progression during service and a shutdown-only network worker.
Bootstrap network/library setup syscalls and final prints are outside that
steady request-work claim. The selected path has no custom TX module.
This supports the selected no-steady-userspace-request-worker mechanism,
not absence of all userspace/bootstrap activity.

## Integrated short-output observation and instrumentation

Four declared probe driver files yield twelve executors,384 measured gen1/c8
requests/tokens plus96 excluded sequential warmups. I independently checked
40 unique client markers per executor, eight warmups,32 measured requests,
model admission/retirement/graph errors, raw TTFT means and graph counters.
Subtracting exactly eight sequential c1/gen1 warmup rounds gives the selected
ordinary process's measured model rounds.

For every traced executor I associated client markers with actual admission IDs,
separated warmup IDs0..7 and measured IDs8..39, verified each request computes
and releases exactly once, no mixed warmup/measurement round, batch lengths
and token/ID lengths agree, warmups occupy eight singleton rounds, all32
measured IDs are covered, trace overflows0 and graph counters agree.
Reference marker/token associations match actual client outputs.
These selected trace histories are valid observations.

| Model | Condition | measured rounds old / native / candidate | TTFT old / native / candidate ms |
|---|---|---:|---:|
| Smol |ordinary |26 /8 /9 |7.401656 /2.047399 /3.097042 |
| Smol |trace |26 /8 /19 |7.472170 /2.010669 /5.751040 |
| Qwen |ordinary |26 /8 /21 |8.922232 /2.665664 /7.561046 |
| Qwen |trace |24 /8 /14 |8.335259 /2.565763 /5.359445 |

The ordinary observations support fewer extra model rounds in those exact
processes. Trace changes candidate Smol9->19 and Qwen21->14 measured rounds.
One process per condition and this substantial sensitivity prohibit tracing
an authenticated batch trajectory through the ordinary five-block full matrix,
asserting trace neutrality, or claiming causal latency mediation.
Native8 rounds does not imply one batch of eight per wave: actual traced native
round membership includes split batches. Use real recorded batches rather than
inventing full batches from aggregate counts.

The initial observation analyzer accidentally globbed driver and trace/reference
JSONLs and stopped at its file-count assertion, exit1.
probe_analysis_initial.py and original stdout/stderr/exit are retained.
The correction changes only that selection to the literal four declared driver
files; formulas, association and oracle checks are unchanged, corrected exit0.
qualification_probe_completion.md records resumed analysis, not a fabricated
successful original chain. No serving executor was repeated. This is an analysis
execution repair on identical raw data and does not invalidate comparisons.

## Host conditions and remaining limitations

Actual host observations bracket the full collection:
before13:41:55.149334, during13:43:31.273889,
mid13:50:42.654141, after14:04:46.500934 UTC.
All name lab, boot04dc0087-5ccc-4c46-9997-b9a92f0e5167,
RTX5090/driver610.57.04 and exactly the same33 selected prior NVRM warnings,
latest10:50:43 status0x56. No newly selected fault line appears.
The first during GPU-app snapshot is empty; mid contains one Python GPU app;
before/after are empty. Sparse samples do not prove continuous isolation,
a fully clean journal, harmless prior warnings, fixed clocks or zero background
load. These remain environmental limitations, not grounds to invent an exclusion.

The fixed four prompts, token-ID binary HTTP body, finite persistent localhost
waves, gen1/64, c1/c8, two model families and two constructors do not establish
arbitrary model/plugin support, ordinary text-server throughput, remote/network
latency, capacity/SLO performance or universal hardware/kernel compatibility.
The kernel SQ consumption context is version-sensitive; source-native installed
path and this qualification are the empirical boundary. Upstream documentation
is context, not installed-kernel identity proof.

## Return and artifact release

This independent result review is complete. All serving/full/protocol/lifecycle/
probe process handles inspected are terminal and their owned wrapper PIDs absent.
I release experiment TEMP and owned build artifacts for the root's planned
scientific archival/replay and ownership-aware cleanup. Preserve the raw failed
analyzer, corrected analyzer, source/commands/receipts, all negative rows and this
review in the archive before deleting TEMP; do not delete original Coder/PVC,
default qwen_graph.so, base packages, unrelated setup_env.sh, model caches or
unowned vllm_graph_uring_loop_trace artifacts. This release is not a claim that
cleanup, commit/push, public bytes or the complete user goal already passed.

No new review of unchanged artifacts, repeated timing matrix, new paper RQ,
additional runtime entity or model arithmetic optimization is required by this
report. Report the supported local repair and unresolved native/AMK boundaries
honestly, then route further work according to its next distinct experiment value.

## Draft wording audit

After completing raw/source audits I also read finding_draft.md. Its numerical
tables, counts, signed interval interpretations, rounded27.2%/20.1% latency
estimates and sensitivity/correctness limitations agree with this audit.
Its final selection/review section is explicitly prospective. Post-result
vLLM-only retention and restoration of the AMK hook to the actually tested
prior-control source are consistent with these results; preserve the frozen
two-hook candidate and state the later selection separately. The selected
hybrid source must not be represented as the originally collected candidate.
Refine its broad CPU phrase to omit separately unaccounted kernel/BPF/softirq/
client work and energy, since process clocks include attributed syscall time.
No new experiment or changed oracle is required merely to make that honest
implementation selection.
