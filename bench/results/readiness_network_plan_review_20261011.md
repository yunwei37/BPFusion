# Fresh plan review: socket readiness and measured worker CPU

Reviewer /root/readiness_network_plan_review,2026-10-11.
Read-only review of main d16fac01c43b3974b88dcb1c18953d62058a7442,
the eight-insertion/one-deletion candidate module diff, plan,finding0027,
perf diagnostic,native benchmark,strict suite and Linux7.3-rc3 source.
No edits,builds or inference.

## Verdict: admit; no blocking defect found

Scientifically valid and executable as a supporting component experiment.
Proceed with affected-kernel qualification,three-mode preflight,frozen-source
full comparison and fresh result review. No additional baseline/workload/
profiling run is required for this claim.

Finding0027 establishes that the previous kernel loses the bounded worker-CPU
comparison to timed native epoll; it cannot answer the candidate by reanalysis.
The diagnostic identifies substantial accept/recv activity but avoids
transferring sample fractions to benchmark CPU windows.

The candidate tests bypassing empty accept/receive attempts while preserving
the sweep and computation. Positive,negative,inconclusive outcomes lead to
different decisions. This fits the requested CPU-path focus; adopting another
model stack would introduce unrelated computation changes.

A positive result supports a bounded CPU advantage for this candidate/workload,
not a causal historical old/new effect,total-service CPU,general serving
superiority or completion of the full retained goal.

## Source safety

The readiness calls are reasonable for these owned TCP sockets.

tcp_poll passes the file argument only to sock_poll_wait,which reaches
poll_wait. A NULL poll table invokes no callback; the reviewed path therefore
does not dereference the NULL file or register a waiter.
https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp.c#L532
https://github.com/torvalds/linux/blob/v7.3-rc3/include/linux/poll.h#L42

Listener poll checks the actual accept queue. kernel_accept allocates before
acceptance; the guard avoids an empty-queue allocation path.
https://github.com/torvalds/linux/blob/v7.3-rc3/include/net/inet_connection_sock.h#L305
https://github.com/torvalds/linux/blob/v7.3-rc3/net/socket.c#L3705

TCP readability includes sk_is_readable; the BPF protocol callback checks
sockmap ingress messages,avoiding ordinary-skb-only checks. EOF,shutdown and
error readiness are represented by the candidate mask.
https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp.c#L518
https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_bpf.c#L643
https://github.com/torvalds/linux/blob/v7.3-rc3/net/core/skmsg.c#L508

Listener file reference and accepted socket ownership survive the calls.
Teardown stops the thread before socket release. No peer_pending,partial TX,
executor-release or final FREE changes. Arrival after a false readiness
snapshot waits for the next existing sweep; this may affect latency and must
remain visible. No event-driven wakeup or lost-wakeup dependency is introduced.

## Comparison and execution

Timed native is the meaningful efficient same-compute control; busy epoll is
a tradeoff control. Unequal wait policies are disclosed,not equated.

Native source supports the matrix,rotations,independent eager-HF oracle,
raw CPU brackets and paired statistics. Totals reconstruct:
120 cells,7680 requests,249600 tokens,30 normal exits.
Qualification's fragmented input,empty connections,ring reuse,pipelining,
half-close and recovery directly exercise readiness changes.
Reuse unchanged userspace strict qualification; current preflight/full still
engage all three conditions.

## Interpretation cautions and code growth

Use the primary interval sign,not merely a positive mean,to claim support.
Report models separately; retain crossing-zero/negative client metrics and
shared-host exposure. CPU improvement alone establishes no latency/TPS gain.
Five paired blocks provide nominal supporting uncertainty,not equivalence/
broad robustness.

The source diff is local:8 insertions/1 deletion,one include and two guards.
No new helper,state,mode,permission layer or test boilerplate. Existing ownership
and protocol behavior are preserved apart from avoiding unnecessary calls;
possible readiness timing differences are part of the declared measurement.

No scientific or execution defect requires plan revision before qualification.
