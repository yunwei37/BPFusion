# Bounded small-graph network / CPU comparison

2026-10-17 UTC / 2026-10-16Los Angeles. Sole-thread implementation,acquisition,
writing and independent-code recomputation;no new agents or independent-person
review. The user closes LLM speed competition after0080 and specifies a
bounded same-executor cuBLAS/cuFFT CPU/P99 experiment with a negative exit.

**Result: no predeclared useful advantage is established.** Retain the
module-free reusable-graph transport as an OSS research prototype and close
this performance search. No CPU-saving/small-kernel-low-latency paper claim
is supported by these data.

K is BPF-owned connection/CQ/SQ/reply progression;N is efficient C++ timed
epoll. They use the same8-slot graph dispatcher and unchanged upstream
cuBLAS 8x8 FP32/cuFFT 32 complex64 work. Remote g10 clients send280-byte requests
and receive256-byte replies over128 persistent connections. Work repetitions
1/16/256,offered-rate saturation and owned-service affinity1/2 logical CPUs
are swept before deterministic confirmation selection.

The full60-cell screen covers2,520,000 measured requests. Three selected points
receive five counterbalanced20 s process pairs each,with new seeds and
600,000 measured requests. All main requests complete with zero observed
failures;all confirmation timing/resource/mask gates pass.

| Confirmation at1,000 requests/s,repeat 1 | Group CPU K/N,t95 | Scheduled P99 K/N,t95 |
|---|---:|---:|
| FFT,unrestricted | 1.011 [0.995, 1.027] | 1.254 [0.514, 3.058] |
| GEMM,unrestricted | 1.019 [0.967, 1.074] | 1.160 [0.497, 2.706] |
| GEMM,one logical CPU | 1.129 [0.956, 1.334] | 2.589 [1.196, 5.607] |

These are nominal paired log-ratio t95 intervals with five process pairs,
not millions of independent statistical replicates or a multiplicity guarantee.
The fixed criterion requires CPU upper95<.90/P99 upper<=1.05,or P99 upper<.90/
CPU upper<=1.05,with throughput lower95>=.98 and zero failures. None passes.
Unrestricted intervals crossing1 do not establish equivalence. The one-CPU
P99 is adverse under the matched observation conditions. Delivered rates near
the1,000/s offered ceiling do not rank maximum capacity.

Removing userspace work shifts cost into system execution. At FFT,the coarse
TGID user/system split is about2.8/35.2us for K and11.3/26.2us for N;
high-resolution group totals are37.959/37.560us. Whole-host CPU intervals
cross 1 and include foreign work/observer. No net CPU saving is established.
The sampled observer itself costs1.99..34.01 us/attempt across main cells and
may perturb tails;these results are instrumented,not production SLOs.
Affinity is not exclusive CPU allocation or a strict CPU-saturation proof.

All 20 path sweeps first meet the saturation rule at16,000 offered/s after4,000/s.
Longer work narrows the throughput gap without a confirmed CPU advantage.
No confirmed beneficial crossover is found in this grid;this does not rule
out untested implementations or hardware. Full P50/P90/P95/P99/P99.9/max,
failure-aware tails,client waiting and separate nested CPU scopes are retained.

[Complete report,figures and method](../../bench/results/graph_network_20261017/result.md)
link the preregistered plan,source/selection,seeds,CSV tables,raw binaries and
resource ledger. Independent-code NumPy audit and original-analyzer replay
check all 92 native measured cells (including the separately retained old
client-interruption pair);canonical metrics and ECDF gzip bytes match.
Actual GPU launch/retirement and kernel reply-byte counts reconcile.

Two interruptions remain explicit:the old CPU2 FFT client-timing pair is
preserved and excluded from the main screen under the predeclared gate;
the later control-stream timeout occurs before main measurement and preserves
32 warmups/zero measured requests. No measured confirmation sample is replaced.
Actual final cleanup is recorded in the linked archive.

The usable integration boundary remains [0079](0079-kernel-network-source-integration.md)
and the [graph runbook](../graph-backends.md). The completed LLM capacity result
[0080](0080-resident-queue-relief.md) is shared scheduling/capacity relief,not
an eBPF speedup. Fixed shapes,64 words,recent qualified Linux/GPU interfaces
and finite numerical/lifecycle checks do not establish a stable arbitrary-CUDA
plugin,broader compatibility or a new universal worker-removal mechanism.
