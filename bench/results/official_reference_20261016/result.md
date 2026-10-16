# Current official serving reference: complete finite result

All15 ordinary executors/30 cells finish at2026-10-16T10:22:29UTC:
7680/7680 successful measured attempts,491520 returned tokens, plus120excluded
gen1 warmups. No measured failure or favorable exclusion. Source-selected
mixed Cu/Py45f0ec2 is unchanged; collection metadata commitf04d8bc changes
only records. Same RTX5090/Qwen checkpoint7ae55760/FP16/pinned runtime.

## Complete observations

The latency column is **client-observed per-token gap P99**, with zeros for
coalesced tokens, not official streamed-output ITL. Each table entry is the
mean of five process-block statistics; no pooled primary confidence interval.

| Regime | Path | Successful output token/s | Client token-gap P99 ms | Zero-gap fraction | TTFT P99 ms | Completion P99 ms | Owned groupCPU ms/attempt |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Offered192 | Kernel loop | 10771.094 | 3.467749 | 0.031188 | 148.994697 | 234.638234 | 0.895807 |
| Offered192 | Efficient native | 11019.771 | 3.389845 | 0.019816 | 108.377877 | 193.724222 | 0.453231 |
| Offered192 | Official vLLM | 11167.040 | 10.794975 | 0.079824 | 126.672046 | 385.352696 | 8.936414 |
| Closed16 | Kernel loop | 8718.357 | 40.457465 | 0.834077 | 4.379739 | 122.306365 | 0.393422 |
| Closed16 | Efficient native | 8861.996 | 40.424057 | 0.834189 | 3.763546 | 121.057327 | 0.274547 |
| Closed16 | Official vLLM | 8528.025 | 4.872805 | 0.026724 | 29.080656 | 175.365452 | 10.130406 |

Primary native-minus-official comparisons, nominal paired t95df4:
- Closed16 output token/s:+333.970520[+80.480328,+587.460713].
- Offered192 client token-gapP99:-7.405130[-9.880985,-4.929275]ms.

These are narrow finite whole-service observations. Closed16 also exposes
much worse own-path token-gapP99 despite lower first-token/completion P99.
A40ms persistent-connection stall and extensive coalescing demand packet-level
diagnosis; current evidence alone does not establish Nagle/delayedACK as cause.
Do not present only favorable first-token/throughput numbers or equate this
client metric to the official benchmark ITL definition.

## eBPF attribution and adverse CPU

Kernel-minus-native offered192 token throughput is
-248.677387[-627.923917,+130.569142]token/s; client gapP99 is
+0.077903[-0.656335,+0.812141]ms. Atclosed16 throughput is
-143.638068[-375.183613,+87.907477] and gapP99 is
+0.033408[-0.039531,+0.106347]ms. All intervals cross zero, establishing
neither superiority nor equivalence. No eBPF speedup is demonstrated.

Kernel-minus-native owned groupCPU is adverse:
+0.442575[+0.267646,+0.617504]ms/attempt atoffered192 and
+0.118876[+0.104885,+0.132866] atclosed16. Both own serving paths use much
less process-group CPU than the full official server in these conditions,
but that shared benefit belongs to the resident implementation/scheduler
comparison, not a demonstrated extra eBPF gain. GroupCPU includes owned threads
and is not complete host/kernel/IRQ/GPU cost.

## Correctness, baseline engagement and limits

Every returned sequence has the requested64 valid vocabulary IDs and successful
HTTP/stream completion; actual prompts/frames/bytes/errors are retained. Exact
membership in the unchanged pre-observation finite output set is2521/2560
kernel,2524/2560native,2527/2560official. Disagreement rows are retained and
not declared universally correct, invalidated away, or used to expand the
oracle. These ordinary untraced trajectories lack current hidden-batch replay.
No identical-output, task-quality or universal numerical-fidelity superiority
claim follows from the fixed output-budget timing comparison.

Official default optimized behavior engages FLASH_ATTN version2,torch.compile
and CUDA graph capture, with no eager or capacity/utilization/context reduction.
The capture-only in-process setting is removed for official serving.
Default cache/capacity/context/scheduler and JSON/SSE differ from resident16
binary HTTP. They are intentional whole-service implementation differences,
not an isolated eBPF ablation. Prefix/warm-cache observations and full actual
configurations remain in each server log. No text/tokenizer work is added.

All parent waits return0 and no owned group remains after collection.
Official server logs force-kill remaining EngineCore children and semaphore
cleanup warnings; parent0 does not mean all children exit gracefully.
The harness does not invoke its forced-kill path. Kernel model/ring ownership
and SQ/CQ drain checks pass;128-entry reply diagnostics truncate392 records
per520-outcome kernel executor, separate from zero model trace overflow.
After the run GPU apps and own pins are empty.

The source/API reader and all request/counter/source data are in
[full/](full/). Large data is losslessly gzip compressed. Archive CPU replay:
python3 bench/results/official_reference_20261016/official_analysis.py bench/results/official_reference_20261016/full/full.jsonl
Its stdout is byte-identical to acquisition analysis. Client lag,scheduled
origins,positive receive gaps,all percentiles,partial outcomes and processCPU
are retained in full.analysis.stdout. Shared-host5-block drift,short prompts,
local traffic,finite load and unequal implementation/API scope remain limits.

The [independent result review](result-review.md) finds a valid complete run,
narrow support for the two external primary effects, and supporting research
value. It independently reproduces630 cell fields and36 paired contrasts. The next useful work is to diagnose the
repeatable persistent-connection40ms stalls before sustained remote/resource
collection; no model math rewrite or favorable timer sweep is warranted.
