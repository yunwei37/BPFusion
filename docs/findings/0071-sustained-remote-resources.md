# 0071: sustained remote load exposes kernel connection failure

[Complete result](../../bench/results/sustained_remote_resources_20261016/result.md),
[raw/replay/figures](../../bench/results/sustained_remote_resources_20261016/full/)
and [independent review](../../bench/results/sustained_remote_resources_20261016/result-review.md)
cover20 cells/five paired blocks/172800 attempts. At192/s kernel times out
3926/57600, native succeeds57600/57600. Successful tokens/s7622.919 versus11637.947;
conditional completionP99 5901.403 versus3330.029ms, censoring failures.
Group CPU adverse +3.885098[3.792477,3.977719]ms/attempt. Host/device adverse
totals do not establish exclusive service attribution. Actual io-wq is inside
group CPU; sampled creator system CPU dominates.96/s latency/host inconclusive.

A sockhash insertion-failure snapshot exactly matches835 timeouts; another
cell reaches4096 connections. Global-queue close dependency is a lifetime/
capacity hypothesis, not proven errno/causality. Diagnose/repair and matched
retest take priority. No allocation of old unreproduced6.36ms difference.
Reference disagreements, observer/shared-host cost, timeout/drain and96/s
checkpoint exposure retained. All10 servers exit0; temporary client retained
for immediate bounded repair/retest. Sustained192 kernel reliability unqualified.
