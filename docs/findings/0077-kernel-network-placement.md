# 0077: Kernel-owned network placement, small local gain with higher CPU

2026-10-16. [Complete result](../../bench/results/kernel_network_placement_20261016/result.md),
[plan/review/raw/source](../../bench/results/kernel_network_placement_20261016/).
15 ordinary cells,172800 successes,11059200 tokens,0 failures.

Moving network CQ/SQ/connection/reply progression from the GPU I/O CTA into the
existing BPF loop keeps actual GPU dispatch instructions identical. Compared
with selected0074, delivered TPS improves25.344 [15.902,34.786],~0.22%;
completionP99 improves124.193 [69.977,178.409]ms. Owned group CPU increases
0.189713 [0.160377,0.219050]ms/attempt,~28.5%. All are nominal5-pair t95.

Candidate versus efficient same-executor native: TPS -2.736 [-15.548,10.076],
completionP99 +20.998 [-41.894,83.890]ms, owned CPU +0.032985
[-0.040210,0.106180]ms/attempt. Crossing0 proves neither superiority nor
equivalence. Mean TPOT is adversely higher by0.003901905
[0.001569381,0.006234429]ms (~0.29%); receive-gapP99 is inconclusive.

The complete ordinary comparison retains996 pool disagreement flags and
bounded network reply-record truncation. Separate finite two-model exact
dual replay/default8 lifecycle qualification passes; it does not certify the
untraced16-bank trajectory or arbitrary model/backend. CPU views are nested;
shared softirq/host/device costs are not exclusive service attribution.

This supports a bundled local placement intervention, not SM/PCIe-only
causality, old6.36ms repair or general faster-server positioning. Mean benefit
mostly appears before the first client token; backlog amplification is an
inference. Original client/PIDs/WIP are cleaned/preserved as applicable.
The candidate remains an unselected archived source, selected0074 unchanged.
See the complete result for all adverse rows, controls, review and reproduction.
