# Fresh plan review: sustained remote delivery and observable resource ledger

2026-10-16 UTC. Planning review only. Read the current plan, evaluation and
closest-work/baseline map, completed official-reference review, ongoing
TCP_NODELAY plan, and the prepared async client, schedule generator, frozen
offsets, resource observer and static CUDA resource report. No GPU execution,
load acquisition, Job creation, source modification or Git publication.
This reviewer writes only this file.

## Decision

**Admit as a supporting experiment**, with the scope already stated in the
plan: sustained different-node delivery and a complete ledger of *available
observations*. It cannot by itself establish exclusive total service CPU or
energy cost on this shared host/device. The selected TCP_NODELAY source must
first finish its separate matched result and ordinary qualification. This is
a real dependency, not a reason to execute the old known-stalled service now.

The experiment adds evidence absent from the old finite closed-loop remote
result and the short local offered-load matrices. A successful latency
contrast can identify a bounded operating range; adverse or inconclusive
contrasts can rule out the proposed transport advantage there. Host/device
resource observations can expose displaced costs or bound claims, while
unattributed shared work remains an explicit unresolved quantity. This is
decision-relevant supporting evidence, not a new thesis, universal driver
claim or independently decisive total-cost experiment.

## Scientific comparison

The main competing mechanism is efficient timed epoll with the identical
resident mixed GPU executor, model revision, FP16 arithmetic, slot count,
prompts and output budget. This is the right causal competitor for removal of
the userspace network worker. The completed official vLLM result remains a
whole-service external reference; another remote official row is not necessary
to interpret this component contrast. No weak or redundant baseline is
required.

Two offered rates and five paired process blocks are sufficient for the
declared bounded question. Matched frozen offsets, alternating path and rate
order, ordinary non-traced builds, no foreign-work interruption and no
transport-specific NODELAY behavior preserve the intended comparison.
The source selection must be frozen before acquisition; choosing a different
source in one path or changing it mid-matrix would invalidate the pairing.

The plan correctly distinguishes client token receive gaps from official
stream-output ITL, and retains coalesced zero gaps and positive receive gaps.
Its TTFT/TPOT terminology reuses the project's previously declared protocol and
the [official vLLM metric definitions](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)
linked in the closest-work map. Raw timestamps must remain authoritative for
the explicitly adapted observation metric. The plan does not equate a local
token-ID frontend with an official end-user text API.

Nominal paired t95 intervals over five blocks are acceptable descriptive
uncertainty for this finite experiment, with the stated small-sample/shared
host limitations. Crossing zero is neither equivalence nor evidence of no
possible benefit. Correlated shared-host disturbances cannot be removed by
calling the blocks paired.

## Executable client and failure treatment

CPU-only checks confirm all three prepared scripts parse. The ten frozen
offset arrays have the declared counts and monotone offsets ending at
60 seconds. Reuse of these arrays across two paths gives the declared
172800 measured attempts, not a new result.

The asyncio client has no project concurrency cap or per-request OS thread.
It records due/task-start/connect/send/receive/finish/close stamps, raw IDs,
partial bytes, protocol/validation errors and finite-reference-set agreement.
Every attempt remains in the denominator, including delayed scheduling,
transport failure and partial output. Its per-operation 60-second timeouts
are explicit; they are not a 60-second total request deadline. An actively
progressing slow request can therefore drain longer than 60 seconds, which
must remain visible rather than being replaced by a favorable cutoff.

A concrete metric alignment is necessary in the pending analyzer:
**connect-origin completion is**
(last token arrival minus connect_begin_ns); stored latency_ms and ttft_ms
currently use start_ns after connect and are send-origin quantities.
Scheduled-origin tails derive from scheduled_ns. The owner has acknowledged
this and is preparing the explicit derivations before preflight. Substituting
the stored latency_ms for the declared primary would invalidate that primary.

Success-only tails must be labeled conditional on success and presented with
failure counts and observed partial tokens. Failures cannot be assigned a
successful response time, discarded, or treated as evidence for a low P99.
Finite-reference disagreement must remain separate from protocol success and
must qualify numerical parity; no observed-output expansion is allowed.

## Resource accounting and attribution

The proposed /proc/stat active total covers user, system, IRQ and softirq work
on the host, including kernel work invisible to a namespace process census.
It also includes unrelated tenants, observer and control activity. A paired
difference is an observed whole-host contrast, **not an exclusive causal
service CPU saving**, even if its interval excludes zero. Process-group,
owning cgroup and host totals are nested views; summing them would double
count. io-wq task identities/TGIDs must be checked rather than assumed to be
outside the service process. Root kthreads not visible here remain unknown.

The observer records actual sample brackets, CPU ticks, per-process CPU
clocks, identities, cgroup counters and pressure, host counters, its own CPU
and NVML device-wide measurements. Sampling about every100 ms and thread
detail about every1 s is adequate for integrated counter deltas, not a claim
to assign individual tail events or see every short-lived worker. Group-clock
deltas require stable before/after identities; exited or missing processes
cannot silently contribute zero. Ensure the launcher really creates the
server process group whose ID is passed to the observer.

NVML energy/power and GPU process lists are device-wide exposures. Dispatcher/
I/O CTA register and launch counts are static footprints, not dynamic SM time
or saturation proof. These observations are scientifically useful with those
limits. They do not complete unobservable per-service kernel/driver or GPU
attribution. Idle brackets must be shown separately; subtracting noisy host
idle totals cannot create an exclusive service estimate.

Observer CPU and cadence quantify some measurement cost. They do not prove
the observer has zero latency impact. Equal instrumentation on both paths
makes this an instrumented comparison; retain that scope and actual observer
work rather than making an unmeasured zero-overhead assertion. An additional
observer-off matrix is optional and is not an admission requirement.

## Preflight completion and terminal interpretation

At review time the outer executable driver and CPU-only analyzer are still
being prepared, as the plan explicitly says. Their absence is a current
preparation dependency, not scientific rejection. Before actual preflight
they must provide the real command, discovered Pod/node/image/source receipts,
actual idle/active sample brackets, the declared timestamp derivations and
denominators, source/config preservation, and owned cleanup. Do not call syntax
checks or scheduler readiness a real preflight. The two-path real preflight
must exercise endpoint, remote client, counters and analysis end to end.

Completion means all ten servers and twenty cells reach terminal status with
all attempted requests represented, including any failures. Keep faulty or
adverse cells and diagnose actual host/storage faults; do not replace blocks
for favorable results. A genuine systematic acquisition defect can be repaired
with its affected comparison rerun and recorded. Preserve the selected source
and metric/oracle/timeout definitions throughout.

No scientific blocker remains in this plan. The pending NODELAY qualification
and executable end-to-end preflight must actually finish before the full remote
run. This review does not declare any result, source adoption, total-resource
benefit or original-project completion.
