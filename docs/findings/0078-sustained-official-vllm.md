# 0078: Official vLLM wins sustained delivery; transport speed advantage unproven

2026-10-17 UTC. [Full result](../../bench/results/official_sustained_20261016/result.md),
[reviewed plan/raw/replay/figure](../../bench/results/official_sustained_20261016/).
15 ordinary cells/five paired blocks,172800 successes,11059200 tokens,0 failures.
Same Qwen2.5-0.5B FP16/RTX5090,192 requests/s for60s plus full drain.

| Mean of five cell metrics | BPF network candidate | Native same executor | Official optimized vLLM |
|---|---:|---:|---:|
| Delivered tokens/s | 11645.24 | 11645.24 | 12244.67 |
| Completion P99, ms | 3304.05 | 3313.97 | 610.73 |
| TTFT P99, ms | 3217.46 | 3229.03 | 362.92 |
| Client token receive-gap P99, ms | 3.59 | 4.65 | 18.74 |
| Owned group CPU, ms/attempt | 0.835 | 0.812 | 8.545 |

Fixed primary native-minus-official TPS is -599.430 [-623.509,-575.351],
about4.90% lower delivery. CompletionP99 is higher by2703.245
[2315.942,3090.547]ms. Nominal paired t95(df4); not maximum throughput
or a hardware/protocol-independent serving ranking. Official default CUDA
graphs/compilation/scheduler/cache/capacity are engaged, not forced eager or
artificially restricted. Whole-service APIs and capacity differ from resident16.

BPF-minus-native TPS -0.003 [-6.500,6.493], completionP99 -9.929
[-64.178,44.319]ms and receive-gapP99 -1.062 [-2.197,0.073]ms cross0;
neither superiority nor equivalence follows. Lower resident group CPU and
TPOT/receive gaps coexist with worse external delivery tails/throughput.
Official client residual lagP99 reaches41.99ms in one block; receive chunks
coalesce tokens. Client gaps are not GPU execution time or official ITL.

All1745 frozen-reference disagreement flags remain; full ordinary exact
trajectory parity is unproven. Raw official payloads reconstruct every token/
prompt/finish/arrival. Earlier invalid client prefixes and GC diagnostic
controls are retained separately, never mixed into the final matrix.
Independent raw-gzip replay matches analysis byte-for-byte. Shared host
softirq/device and missing PID-namespace worker visibility do not establish
exclusive total CPU/energy saving. Historical6.36ms remains unallocated.

This is supporting whole-service evidence and a workload/design boundary.
It does not establish intrinsic eBPF speedup or general faster-server novelty.
Kernel-owned network remains an unselected experimental candidate; default0074
is unchanged. See full result/review for costs, residual confounds and cleanup.
