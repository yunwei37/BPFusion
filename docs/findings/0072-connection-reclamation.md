# 0072: repair EOF reclamation under sustained remote load

2026-10-16. Same lab RTX5090, QwenFP16, reused mixed executor,16 slots,
g10 client,192 offered requests/s,60s/cell,five paired blocks,three paths.
[Plan](../../bench/results/connection_reclamation_20261016/plan.md),
[review](../../bench/results/connection_reclamation_20261016/plan-review.md),
[raw result](../../bench/results/connection_reclamation_20261016/result.md)
and [independent result review](../../bench/results/connection_reclamation_20261016/result-review.md).

The global queue guard retains EOF connections while unrelated work waits.
An errno/census diagnostic finds E2BIG and2947 owned CLOSE_WAIT connections;
a corrected collision trajectory proves safe local EOF while unrelated queued40.
The repair uses conservative peer pending buckets with matched publication and
acquire order; hash collisions defer reclamation. Non-EOF dead/reset behavior
retains its global guard. Model arithmetic is unchanged.

All15 full cells complete:172800 attempts,168643 successes,4157 zero-token
global timeouts,10793152 successful tokens. Global/local/native each57600
attempts. Local and native have zero observed failures. Primary local-minus-
global failure fraction -0.072170[-0.082610,-0.061731], nominal paired t95df4.
Global is an ablation with the same new bookkeeping/ABI, not untouched old main.

| Five-block mean | Global guard | Local guard | Native epoll |
|---|---:|---:|---:|
| Failed attempts |4157|0|0|
| Delivered tokens/s |7793.075|11623.043|11642.741|
| CompletionP99 ms |5782.966*|3410.279|3313.846|
| Client token-gapP99 ms |8.456*|3.856|3.691|
| Group CPU ms/attempt |4.746725|1.695749|0.732280|

*Global tails condition on success and censor7.217% missing completions;
timeouts are not completed60-second samples. Throughput/resources retain all
attempts and terminal drain. Local-minus-native TPS -19.698[-28.806,-10.589],
completionP99 +96.433[44.854,148.012]ms, client-gapP99
+0.165253[0.075087,0.255418]ms, groupCPU
+0.963470[0.863478,1.063461]ms/attempt remain adverse.
Whole-host/device costs are shared observational totals, not exclusive attribution;
io-wq CPU is already included in the owned TGID group.
1355 finite frozen-reference disagreements remain; no universal fidelity claim.

This supports bounded lifetime/capacity repair. It does not allocate the old
unreproduced6.36ms gap or establish eBPF performance/CPU superiority.
The missed nvcc -dc selection, invalid earlier qualification/preflight, numerical
finite-pool failures and two postmeasurement API transfer resets are preserved.
All affected checks were repeated with the actual corrected source.
Primary and both protocol archive CPU replays are byte-identical.

Default8 qualification passes both models, dual-replayed93504 tokens and
352 ordinary lifecycle outcomes; cuBLAS/cuFFT cases also pass. Canonical-source
integration is recorded separately after normal build and cancellation checks.
