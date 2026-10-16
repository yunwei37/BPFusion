# Independent sustained official-vLLM plan review

Reviewed 2026-10-16 UTC under research-experiment-design PLAN REVIEW. This is
the initial review and its same-pass timeout clarification, not a result
review. Only this file is written. No model/GPU run, build, BPF attachment,
Job creation, source edit, Git mutation or runtime-setting change was made.

## Decision

Admit the proposed integrated comparison to real preflight. No scientific or
executability defect currently blocks that preflight. Full acquisition
requires its declared actual three-condition preflight to succeed; this
review does not certify an unexecuted API/client/server path.

The comparison is supporting whole-service evidence toward the retained
serving objective. There is no formal paper RQ/thesis contract in the
repository, and this review does not invent one. It is neither a new eBPF
mechanism result nor a repair/allocation of the historical 6.36-ms gap.

## Evidence and scientific value

I read plan.md, official_remote_server.py, official_remote_client.py,
official_remote_analysis.py, run_official_remote_matrix.ps1, client_job.json,
models.json, environment.json and resource_observer.py. I also read the
completed 0077 placement result and independent result review, its finding,
and 0069 official_api.py, official_reference.py and result.md.

0077 establishes a small local K-minus-old-loop throughput gain and completion
tail improvement with higher CPU, while K/native speed remains unresolved.
It does not compare this current long remote workload with official serving.
0069 runs only 256 requests per cell, uses loopback/threaded clients and
includes an older transport state. Its offered interval is approximately
1.33 seconds rather than this 60-second workload. Reanalysis cannot turn
that short acquisition into a matched sustained comparison. The proposed run
therefore adds a missing, user-requested external performance level.

The admission rationale is decision-relevant: native beating official
supports only this fixed-load whole-service positioning; losing redirects
attention toward common scheduling/compute/API behavior; mixed or
inconclusive results constrain the claim and retain adverse tails and costs.
Another small transport sweep or generic-interface fixture would not answer
that strongest-competitor question. This is a reasonable next use of the
experiment budget, without claiming that completing its setup is itself
scientific progress.

## Baselines and fairness

Official O is a credible strongest external whole-service competitor.
The actual command uses official vLLM serve with the real pinned Qwen
checkpoint, tokens-only API, FP16 and private bind/port. It removes the
resident capture-only VLLM_ENABLE_V1_MULTIPROCESSING setting. It does not cap
official sequences, token budget, memory or context, force eager execution,
disable prefix caching or replace the normal scheduler. Actual startup logs
must establish that compilation/graphs/cache engage. The repeated four
prompts can favor the normal prefix cache; the plan discloses this rather
than disabling an ordinary official feature.

N is the efficient epoll/timed-wait native path with the same resident GPU
executor; K is the previously qualified, still-unselected kernel-owned
network candidate. Their same-executor contrast isolates their bundled
transport mechanisms more closely. The older GPU-I/O placement is already a
completed ablation in 0077 and is appropriately omitted here. No extra weak
baseline or broader workload is needed for admission.

Official scheduling, KV allocation, capacity, streaming JSON/SSE, bytes and
API semantics differ from the resident fixed-16 implementation. A whole-
service win must not become an eBPF attribution. O may simply sustain the
offered rate with different batch/cache behavior. None of the three
conditions establishes capacity above the offered rate.

## Fixed workload, metrics and correctness

The model snapshot path is revision
7ae557604adf67be50417f59c2c2f167def9a775, shared by all conditions.
Five paired blocks use the same four frozen token-ID prompts, deterministic
sampling request, 64 requested tokens and exact existing gamma-arrival
offsets at 192 requests/second for 60 seconds plus drain. The actual
driver order agrees with the plan: K,N,O; N,O,K; O,K,N; O,N,K; N,K,O.
There are 15 cells, 11520 measured attempts per cell and eight sequential,
excluded, checked gen1 warmups per fresh server.

The fixed primary is N-minus-O successfully delivered output tokens/second.
The analyzer uses all scheduled attempts and complete-drain duration, retains
partial tokens separately and applies the declared paired t95 coefficient
2.776445105 across five block effects. Failure fractions and conditional
success tails remain explicit. A zero-crossing interval is inconclusive;
a positive throughput interval does not override an invalid baseline or
establish better tails, equality or general SOTA.

The plan cites official vLLM benchmark definitions for conventional metrics.
Connect-origin TTFT/completion, scheduled-origin tails, TPOT, client lag/CPU,
zeros and positive receive-gap views are available in actual analysis.
The client receives timestamps per socket chunk; coalesced token IDs share
timestamps. These gaps cannot be advertised as GPU token execution times,
official per-stream-output ITL or an additive kernel-stage P99 decomposition.
Official request-start includes aiohttp setup; the analyzer does not invent
official send-done timestamps.

The async official adapter preserves the qualified 0069 request fields and
checks HTTP status, event-stream framing, DONE, requested prompt IDs,
vocabulary range, finish_reason=length and exact returned token count.
Its parser keeps incremental token/arrival arrays on an error. Native
binary parsing and its source-native stop/network counters are retained.
The fixed frozen-pool membership remains a flag, not an exclusion or an
expanded oracle. This is finite protocol/count/range checking plus earlier
exact traced support; it does not certify exact untraced trajectories,
eager-HF parity or arbitrary-model correctness.

The initial prose overstated identical per-write timeout behavior. In this
same review pass the owner clarified the actual contract: binary connect,
drain and read are 60 seconds; aiohttp connect/socket-read are 60 seconds,
with default small-body write handling and no separate write deadline.
There is no overall deadline censoring or retry. This clarification matches
the implementation without adding a false timeout-equivalence claim.

## Executability and lifetime

The PowerShell driver launches the archived lifecycle wrapper in the existing
Workspace, waits for real native-ready output or official health/auth checks,
runs the real remote client warmups, starts/stops the observer around actual
client execution, signals the owned server group, then archives data after
serving stops. Its real preflight supplies the existing 128-offset prefix
file rather than using a substitute client/protocol. The unused client
--preflight option slices 32 offsets, but this driver does not pass that
option; the analyzer correctly expects 128.

The official wrapper records parent exit, gives remaining owned process-group
children a grace interval and records any forced EngineCore cleanup.
The analysis requires the parent to exit zero, no wrapper error/forced parent,
no remaining children/pins, checked warmups, real auth checks and successful
client process exit. Forced children are recorded rather than silently
converting the known 0069 shutdown behavior into graceful shutdown.
Native graph/network counters and BPF detach results remain checked.

The disposable remote client manifest has no CPU/memory limits or node pin.
Its anti-affinity excludes the actual server Workspace placement, which
supports a remote-client comparison. The original Workspace/PIDs and foreign
setup_env.sh remain outside this benchmark's ownership. Actual UID-specific
Job deletion and Pod absence, plus absence of owned server GPU processes and
pins, are completion requirements rather than facts established by this
review. No additional persistent entity is needed.

## Uncertainties and optional suggestions

The most consequential preflight uncertainty is client work. Prior 0077's
binary event loop already used approximately 0.94--0.98 core. Official SSE
decoding and retained JSON frame serialization add work and may distort
delivery or arrival scheduling. Inspect the actual three-condition preflight
CPU, scheduling lag, achieved schedule and outcomes. If that exposes an
avoidable official-client bottleneck, repair the adapter before freezing
full acquisition or restrict the resulting claim appropriately; do not
count it as a server win. This is an acknowledged comparison-validity issue,
not a demand for another competitor or a larger experiment.

The archived frames preserve decoded JSON objects and timestamps, not every
literal SSE byte/comment/malformed pending fragment. Calling them decoded
SSE frames would be more exact; retaining a small malformed fragment on
failure could help diagnosis. This is not presently an execution blocker.

CPU group/cgroup/host views are nested and the busy lab host includes other
work. Process-group churn can make group CPU unavailable, and host softirq/
device energy are not exclusive service costs. Keep missing values and
resource scope visible. No total CPU or energy conclusion follows merely
from smaller process CPU.

Subject to the declared real preflight, the command, raw path, complete-matrix
analysis, fixed primary, failure retention, uncertainty calculation and
cleanup plan are sufficient for the narrow supporting comparison. No
outstanding blocker remains at this initial plan-review stage.

## Follow-up 1: actual preflight and proposed common event-loop repair

The first real preflight is complete for all three actual conditions:
384 successful attempts, 24576 measured output tokens, no failures, checked
warmups/authentication and zero parent/drain terminals. Its frozen-pool flags
K1/N1/O3 are retained. These are executable preflight facts, not the sustained
experiment result. Full collection has not started.

I read its actual analysis.stdout. K/N/O client CPU is respectively
5.842985/5.795271/5.813577 ms per attempt. Client scheduling-lag P99 is
6.275930/10.976557/49.134080 ms, and durations are
0.787484/0.782381/0.849613 seconds. O's approximately 0.876 average CPU-core
fraction versus K/N approximately 0.950/0.948 is partly a different drain
denominator. Similar CPU per attempt does not establish greater SSE CPU
demand; a short event-loop lag spike does not establish sustained client
saturation or allocate its cause. It does, however, make the previously
identified adapter/scheduling uncertainty real enough to address before
the longer run.

One common upstream uvloop event loop for K/N/O is a scientifically valid,
targeted executable repair before full acquisition. It does not change the
server hypothesis, primary, oracle, timeout, request schedule, protocol or
baseline capacity. Run the second real preflight for all three paths and
retain the original source/raw/preflight as the first attempt. Do not combine
old and new client-loop cells into the fixed full matrix. If used, freeze
the resulting one common client and actual dependency version before every
full cell. No concurrency cap, official-only acceleration or broad parameter
sweep is implied or needed.

The installed upstream source must be described accurately:
vllm/benchmarks/serve.py:2022 calls asyncio.run(main_async(args));
vllm/benchmarks/throughput.py imports uvloop and calls uvloop.run around its
async throughput path; vllm/entrypoints/cli/serve.py:154 uses uvloop.run for
the serving process. Therefore common-client uvloop is a proposed use of an
existing upstream runtime, not a claim that the official serving-benchmark
client itself defaults to uvloop. The official SERVER already uses it.

This repair is preferable to knowingly carrying an avoidable client-risk
into a purported service-level ranking. It is not a mandatory method for
obtaining a pass: retaining the present client could still support a narrowly
labeled client-delivery measurement, provided its lag/CPU and inability to
measure exclusive server capacity are explicit and no bottlenecked baseline
is called a server loss. Such a narrow measurement is less responsive to the
user's request for credible official-server performance positioning.

The second preflight must establish actual successful API/client lifecycle
and record comparable lag/CPU/schedule facts. Improvement is not proof of
unlimited client headroom at 60 seconds; full-run client context and
scheduling distributions remain necessary. This is follow-up 1 in the same
plan review, not a new experiment or permission for an indefinite repair/
benchmark sweep. No new scientific blocker to this common repair is found.
