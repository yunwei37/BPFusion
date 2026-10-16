# Fresh plan review: persistent TCP delivery stalls

2026-10-16 UTC. One fresh PLAN REVIEW under research-experiment-design.
Read the complete proposed plan, the completed official-reference result and
independent result review, current evaluation and closest-work map, and the
selected mixed listener and both transport send paths. No formal paper/RQ or
idea-story file exists; the retained serving-performance question is explicit.
No GPU run, source/plan modification or Git publication is performed here.

## Decision

**Admit. No scientific or executability blocker.** The proposed single-option
before/after comparison and a separate instrumented diagnostic can test a
concrete, previously unmeasured cause of the severe shared streaming stall.
Its value is supporting mechanism/workload evidence, not an additional eBPF
contribution. The current forty-millisecond pattern alone establishes no cause.

## Admission and decision value

The prior official-reference run is complete, with both resident paths showing
approximately40.4ms token-gap P99 and83.4% coalesced-token zero gaps in closed16.
Offered192 uses fresh connections and has much smaller gaps. Source inspection
confirms that the selected listener and accepted-socket paths omit TCP_NODELAY;
native sendmsg uses MSG_DONTWAIT|MSG_NOSIGNAL, with no MSG_MORE in that path.
This is a concrete intervention opportunity, not causal evidence.

Existing client histories cannot reveal whether data had entered TCP before a
stall. The proposed ACK/queue observations add a discriminator that reanalysis
cannot supply. A positive result can justify a shared streaming transport fix;
a null or contradictory result rejects that choice for the claimed workload
and directs attention to production, scheduling or observation delays.
It cannot retroactively explain the old unreproduced kernel-specific6.36ms
difference. Diagnosing this repeatable defect before longer remote/resource
collection is a reasonable higher-value use of the next run.

## Fairness, controls and metrics

The strongest causal competitor remains efficient native TCP with identical
resident GPU computation, model revision, precision, input/output budget and
capacity. The original binary for each transport is its own intervention
control; no additional external baseline is necessary. The official result
remains a dated whole-service reference, not a row silently repaired after the
fact. Changing only listener NODELAY before listen avoids a late-option
transition being mistaken for steady option behavior.

Ordinary builds, equal clients, fixed schedules, request deadlines, finite
numerical reference policy and all failures are retained. The client per-token
receive-gap is explicitly distinguished from official vLLM stream-output ITL.
Zero fractions and positive-gap distributions are necessary companions here;
they prevent burst/coalescing behavior from disappearing behind one percentile.
TTFT/completion/TPOT, throughput and adverse outcomes constrain interpretation
without substituting a favorable secondary metric for the primary.

Five paired block contrasts per transport with a declared nominal t95df4
interval are executable and appropriately bounded. They estimate variation of
these process-level P99 statistics, not population-quantile confidence,
equivalence or a joint multiplicity-adjusted claim. The fifth Williams order
repeats the first, so this is not exact four-condition counterbalancing across
all five blocks; the frozen order is transparent and this is not a blocker.

## Mechanism evidence and executable telemetry

The diagnostic correctly requires evidence that data was buffered before the
packet gap, not merely an ACK arriving immediately before the next send.
Actual own accepted-socket TCP_INFO with notsent/unacked state, or a correctly
joined completed-send trace, can establish that discriminator without changing
the GPU computation. Queue-state sampling and packet timestamps must share a
documented time basis, with actual sampling gaps and losses retained.
The plan already treats unavailable attribution as unknown.

Execution should use the kernel-returned TCP_INFO length and version-correct
field layout, retain socket identity/connection tuple and verify accepted
NODELAY values. A listener-only getsockopt does not independently establish the
option on the observed child. An own-FD access denial is not permission to
alter host security; the permitted alternate completed-send observation or an
honest missing-attribution result is sufficient.

To interpret a positive mechanism observation, distinguish pure delayed ACKs
from ACKs piggybacked on a later request and retain sequence/ACK progression,
window information and retransmission evidence. The headers-only capture can
support this. On loopback, outgoing/incoming duplicate observations and offload
representation must be handled explicitly; do not count duplicate sightings as
independent transmissions. These are interpretation details within the
declared diagnostic, not a demand for another experiment or broader tracing.

The matched-kernel source makes the proposed instrumentation technically
plausible: Linux7.3-rc3 tcp_info exposes tcpi_notsent_bytes and related send/
retransmission counters. The TCP output implementation tests outstanding small
data when Nagle applies. This supports the choice of discriminator, not a
prediction that it will necessarily be observed:
[matching TCP output source](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/net/ipv4/tcp_output.c),
[matching TCP_INFO ABI](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/include/uapi/linux/tcp.h).
The [tcp manual](https://man7.org/linux/man-pages/man7/tcp.7.html) documents
NODELAY, CORK precedence and TCP_INFO. No assertion that current stalls are
caused by Nagle follows from these sources.

## Execution, completion and result scope

The integrated count is coherent:20 executors,40 cells,10240 measured attempts,
655360 requested tokens, plus160 excluded checked gen1 warmups. The real
preflight uses the actual Qwen model and both transports; packet/syscall
observers remain outside full performance acquisition. Source/build snapshots,
the retained official client/analyzer, raw outcomes and normal default8
protocol/cancellation regression provide a sufficient ordinary replay path.
The declared Python entrypoint and four-condition analysis are necessary
experiment adapters; their implementation can be completed and frozen during
preflight without introducing a separate control framework.

If the mechanism observer cannot establish queued-before-stall data, the full
before/after result can still establish a bounded NODELAY performance effect,
but the specific Nagle/delayed-ACK hypothesis remains inconclusive. A favorable
P99 effect does not establish that all remaining delays are network holds.
No unchanged blocks should be replaced because they are noisy or contrary.

Shared CPU/GPU exposure, small finite workload and the two nominal primary
contrasts remain limitations. No isolated-host, total-resource, remote-SLO,
model-quality or eBPF superiority claim is available from this matrix.
Normal lifecycle qualification is an adoption dependency, not extra scientific
value. Proceed with the real diagnostic preflight, retaining failures and
missing attribution exactly as proposed.
