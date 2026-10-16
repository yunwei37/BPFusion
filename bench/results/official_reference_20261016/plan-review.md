# Independent plan review: current official serving reference

2026-10-16 UTC. Fresh reviewer, round1. Read the proposed plan, evaluation
status, closest-work/baseline map, findings0031/0065/0066 and the preserved
official token-only client. No formal paper RQ or idea-story exists; review
uses the retained complete-service performance question without inventing one.
No GPU work, application edits or Git publication performed.

## Verdict

**Revise one narrow primary-metric definition before preflight; otherwise
admit this supporting whole-service comparison.** The baseline, finite
workload, matrix and causal-scope choices are sound. No additional model,
competitor, load regime, host isolation or experiment is required.

The remaining defect is not a demand to improve a number: the plan's declared
primary is not the official metric it currently cites. It can be repaired in
the same plan before any timing data, retaining the existing workload and
historical primary if desired.

## Required correction: token-observation gaps versus official ITL

The plan says metrics follow official vLLM, but also assigns the receive
timestamp to every token in a coalesced output and includes the resulting
zero gaps. The current [official latency definitions](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics),
opened2026-10-16, explicitly define ITL between streamed outputs. When a
streamed output includes multiple tokens, the official definition does not
insert zero samples for those tokens. The same page warns that metric names
are not standardized and comparisons require measurement points/formulas.

This matters scientifically for the primary native-minus-official tail:
different streaming/coalescing policies change both the number and weighting
of samples. It is not enough to label both numbers ITLP99 and imply official
benchmark equivalence.

One sufficient minimal repair is to retain the predeclared historical
per-token client-observation primary, explicitly call it **client-observed
per-token gap P99**, write its formula and denominator, and state that it is
an adaptation rather than official stream-output ITL. Report the zero-gap
fraction and tokens-per-observed-output/receive exposure from retained raw
arrivals/frames so a low percentile cannot hide its coalescing basis. Do not
change the primary after seeing comparative results. A separately labeled
official-style stream-output gap is useful when recoverable, but is not a
new baseline or mandatory extra run.

Clarify that official TTFT/TPOT definitions still supply the appropriate
measurement precedent. Ordinary client completion after final streamed token
and protocol drain should remain distinguishable; the full-cell throughput
denominator already includes drain. No need to change the timeout, output
oracle or all-attempt denominator.

## Admission and decision value

Admit the motivation. Finding0031 used the older HF execution path, different
runtime libraries and a different finite concurrency matrix. Its numerical
ranking cannot settle this now-qualified upstream-vLLM mixed backend.
Findings0065/0066 answer same-compute scheduling/transport questions, not
current whole-service competitiveness. The new official comparison adds
independent evidence rather than an unchanged repeat.

The strongest runnable external reference is the official optimized server.
Keeping the same-executor native C++ epoll condition separately preserves
the eBPF attribution boundary. A resident win or loss against official
changes performance positioning; native matching/beating kernel still
prevents an eBPF superiority claim. Mixed or crossing-zero outcomes are
meaningful, not pressure to tune or replace unfavorable blocks.
Role remains supporting; contradictory data bounds this implementation and
workload rather than proving a universal thesis false.

## Baseline and output fairness

Official default optimized scheduling, CUDA graphs, compilation and capacity
must remain engaged; removing the capture-only multiprocessing override is
appropriate. Do not impose resident16 capacity on official serving, disable
its caching or use eager mode merely to align internals. Same checkpoint
revision, FP16, common pinned packages, same GPU and prompts/output length
are the relevant external controls. The JSON/SSE versus binary HTTP difference
makes this a whole-service comparison, not an eBPF component ablation.

The finite pre-observation reference pool is appropriate for reporting
agreement when fixed before execution. Exact greedy agreement can vary with
optimized execution; record every mismatch, prompt identity, requested and
observed length, vocabulary validity, finish state and protocol failure.
Do not convert disagreement into a task-quality claim, silently expand the
pool or require arbitrary-model numerical equivalence for this comparison.
The ordinary-source integration qualification supplies the resident
implementation correctness dependency; this benchmark is not a replacement
for it.

## Workload, cache and timing scope

Five complete three-condition process blocks, two integrated gen64 regimes
and fixed workload/order/seeds are sufficient for this bounded question.
The offered192 regime links the adverse-tail discussion; closed16 provides
a useful finite throughput reference without claiming maximum throughput.
Retain all requests and drain; error/timeout rows cannot disappear from
throughput or be reclassified as successful sixty-second latencies.

Eight checked gen1 warmups define a reproducible initial state. They do not
by themselves establish full gen64 steady-state or a cold-cache result.
Resident graph construction and official initialization can warm different
things; retain actual compilation/capture logs and state this limitation.
The official documentation also warns about repeated-prompt prefix-cache
reuse. Record whatever actual cache configuration/hit statistics the official
logs expose and the regime order; no cache disabling or new cache experiment
is required. If the short prompts do not hit prefix caching, establish that
from observations rather than assuming it.

Client serialization/parsing and coalescing remain in observed end-to-end
times and may be performance explanations. Scheduled-origin latency and
client scheduling lag are essential with a heavily shared CPU host; the
plan retains them. Connection reuse differs by declared regime, consistently
across methods, and should remain visible in the actual driver.

## Executability, uncertainty and reporting

The actual acquisition script is an implementation dependency still to be
frozen, not existing measured evidence. Before real preflight, retain the
final normal-source commit, compiler/runtime/library identities, commands,
source/driver and API reader. Preflight must traverse all three actual
methods and both metric paths, followed by the declared full matrix.
An executable defect can be repaired under the stated bounded preflight
rule without requesting another scientific experiment.

The arithmetic checks are coherent:15 full processes,30cells,7680attempts
and120excluded warmups. Nominal paired t95df4 on five block contrasts is a
bounded uncertainty summary, not population-P99 confidence, equivalence or
a multiplicity-adjusted joint claim. Report each block and every failure;
the two primaries can disagree and must not be collapsed into a single win.

Shared-host CPU observations and bounded journals cannot isolate interference.
No foreign workload should be stopped. Owned-process CPU is explicitly
partial and does not settle total resource cost; leave the separate full
resource and sustained remote questions open. Limited loopback/token-only
prompts and finite samples prevent production/SLO or general model claims.

The cleanup scope is executable and appropriate: bounded private listeners,
owned process groups and pins, recorded forced child cleanup if needed,
preserved original Workspace/Coder processes/builds/unrelated WIP. Ordinary
source integration finishes before collecting the official matrix; no own
GPU overlap is allowed. Publication on main is separately user-authorized.

## Follow-up boundary

This is round1 of one fresh plan review. A same-file follow-up can verify the
single metric correction; no unchanged re-review or additional reviewer is
needed. No desired performance verdict is supplied.

## Focused follow-up1: metric definition corrected

2026-10-16 UTC, before collection. Reread the corrected Standard metrics
section and the prepared acquisition/API readers in the existing temporary
directory. The plan now explicitly fixes the primary to client-observed
per-token gap P99, supplies gap[j]=(a[j+1]-a[j])/1e6, retains zero gaps and
requires coalescing exposure plus a separately reported positive receive-gap
distribution. It explicitly disclaims official stream-output ITL equivalence.
The protocol reader retains actual token arrival stamps and frame records,
so these quantities are recoverable without another collection condition.

**Verdict: admit real preflight and the declared complete matrix.** The
round1 scientific defect is resolved. The isolated later ITLP99 shorthand
in the contrast sentence is governed by the section's explicit primary
definition; use the unambiguous client_token_gap_ms_p99 name in analysis and
published tables as planned. This does not change a metric after observing
data, and no GPU collection has occurred.

The prepared acquisition driver does not yet implement its promised analysis
entrypoint; finishing and freezing that CPU analysis before actual preflight
is the already declared implementation dependency, not a new scientific
review gate. The real preflight must demonstrate that raw arrival/length/
failure rows pass through the final metric code. No additional workload,
baseline, run or follow-up review is requested. All other round1 scope and
interpretation limitations continue to apply.
