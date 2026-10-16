# Current mixed service versus official vLLM

2026-10-16 UTC. Same RTX5090, Qwen2.5-0.5B-Instruct revision7ae55760,
FP16 and pinned vLLM0.31 runtime; ordinary mixed source45f0ec2.
The [plan, raw data and replay](../../bench/results/official_reference_20261016/)
and [fresh independent review](../../bench/results/official_reference_20261016/result-review.md)
cover15 executors/30 cells:7680 successful attempts/491520 tokens, plus120
excluded gen1 warmups. All conditions complete without measured failure.

Official vLLM uses its optimized server defaults, including FLASH_ATTN2,
compilation, CUDA graphs and enabled prefix cache. Actual cache-hit rate is
unknown. Its scheduler/capacity/cache and JSON/SSE differ from our binary
resident16 service, making this a whole-service reference. Efficient native
epoll with identical resident computation remains the transport baseline.

| Regime | Path | Output token/s | Client token-gap P99 ms | Zero-gap fraction |
| --- | --- | ---: | ---: | ---: |
| Offered192/s | Kernel |10771.094|3.467749|3.119%|
| Offered192/s | Native |11019.771|3.389845|1.982%|
| Offered192/s | Official |11167.040|10.794975|7.982%|
| Persistent16 | Kernel |8718.357|40.457465|83.408%|
| Persistent16 | Native |8861.996|40.424057|83.419%|
| Persistent16 | Official |8528.025|4.872805|2.672%|

Entries are arithmetic means of five process statistics. The gap metric
retains zero gaps for coalesced tokens; it is not official stream-output ITL.
Native-minus-official primary effects are persistent16 throughput
+333.971[+80.480,+587.461]token/s and offered192 gapP99
-7.405130[-9.880985,-4.929275]ms, nominal paired t95df4.
These narrow effects coexist with much worse persistent streaming gaps.
TPOT at persistent16 is1.81450/1.79067/1.56172ms kernel/native/official.

No same-executor kernel/native speed effect excludes zero. Kernel process-group
CPU is higher by0.442575[0.267646,0.617504]ms/attempt offered192 and
0.118876[0.104885,0.132866] persistent16. Both resident paths use less owned-group
CPU than official here, a shared implementation effect rather than eBPF gain
or complete service resource accounting.

Finite reference-set matches are2521/2560 kernel,2524/2560 native and2527/2560
official. All sequences have valid64-token protocol results; disagreements
remain visible and do not establish identical numerical outputs or task quality.
Shared-host interference, short repeated prompts, finite local traffic and
client scheduling/framing differences limit generalization.

All parent exits are0 with no owned group left, but official logs explicitly
force-kill EngineCore and warn about semaphore cleanup. Kernel legacy admission
diagnostics truncate392 records per520 outcomes, distinct from zero GPU/ring
overflow. Full client histories remain complete.

Next: causally diagnose the repeatable shared40ms stalls before sustained
remote/full-resource runs. Missing server TCP_NODELAY is a candidate
discriminator, not yet a demonstrated cause. The old kernel-specific6.36ms
difference remains unreproduced and unexplained as a quantitative allocation.
