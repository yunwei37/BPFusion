# Kernel-owned network placement: complete ordinary comparison

2026-10-16 UTC. [Frozen plan](plan.md), [plan review](plan-review.md),
[actual default8 qualification](qualification.md), [remote preflight](preflight.md).
This is supporting intervention evidence, not a general faster-server result.

## Completion and controls

All15 planned ordinary cells/five paired blocks complete:172800 successes,
11059200 measured output tokens, zero failed/partial/timeout/protocol outcomes;
120 checked gen1 warmups excluded. No replaced/dropped cells. Each server exits0,
all counters/drain checks pass, no remaining pins. [Cleanup](cleanup.json)
records actual client Job/Pod absence, empty GPU app/pin lists and preserved
original Workspace sessions/WIP; no production source/default is adopted.

Candidate K moves CQ/SQ, connection/reply state and token copies from the
independent GPU io_network CTA to the existing kernel BPF loop. Before L is
selected0074. Native N is efficient C++ epoll with the same resident upstream
vLLM model execution. Actual ordinary dispatch1464 instructions match exactly
at8/16; traced dispatch1656 also matches. K has no GPU I/O CTA. This is a
bundled placement intervention, not exclusive SM/PCIe/softirq attribution.
Checkpoint/runtime/FP16,16 slots,4 prompts,gen64,gamma192/s for60s+full drain,
60s per-I/O timeout and all fixed assets remain as planned. No instrumentation
or source/timer/oracle change during collection.

## Results

Arithmetic mean of5 process-cell values; P99 entries are means of per-cell
P99s, not pooled population P99. Units shown explicitly.

| Metric | Before L | Candidate K | Native N |
|---|---:|---:|---:|
| Delivered output tokens/s |11615.074|11640.417|11643.153|
| Connect-origin completion P99 ms |3457.714|3333.521|3312.523|
| Client receive-gap P99 ms |4.6795|4.5553|4.7360|
| Mean TTFT ms |1670.222|1606.192|1603.684|
| Mean completion ms |1755.064|1690.892|1688.138|
| Mean TPOT ms |1.346690|1.344442|1.340541|
| Owned group CPU ms/attempt |0.665960|0.855673|0.822688|
| Workspace CPU ms/attempt |1.066266|1.258509|1.224557|
| Remote client CPU ms/attempt |5.358213|5.362478|5.324851|
| Mean client scheduling lag ms |2.488419|2.520122|2.539484|
| Device energy J/attempt |1.711816|1.708989|1.710150|

Nominal paired95%t intervals across5 blocks, df4; all69 planned rows and
individual effects are retained in kernel_network_full/analysis.stdout.

| Contrast/metric | Signed effect [95% interval] |
|---|---:|
| K-L TPS, fixed primary |+25.343567 [15.901519,34.785614]|
| K-L completion P99 ms |-124.193195 [-178.409430,-69.976960]|
| K-L receive-gap P99 ms |-0.124218 [-0.649177,0.400742]|
| K-L owned CPU ms/attempt |+0.189713 [0.160377,0.219050]|
| K-L mean TTFT ms |-64.030563 [-78.696211,-49.364915]|
| K-N TPS |-2.735807 [-15.548018,10.076404]|
| K-N completion P99 ms |+20.997933 [-41.893880,83.889746]|
| K-N receive-gap P99 ms |-0.180676 [-0.977015,0.615662]|
| K-N owned CPU ms/attempt |+0.032985 [-0.040210,0.106180]|
| K-N mean TPOT ms |+0.003901905 [0.001569381,0.006234429]|
| L-N TPS |-28.079374 [-43.281968,-12.876779]|
| L-N completion P99 ms |+145.191128 [77.364158,213.018098]|

Primary supports a small local gain: K-L +0.2182% delivered TPS and -3.59%
completionP99, with +28.49% owned CPU. Versus native, TPS/completion/gap/CPU
intervals cross0: neither superiority nor equivalence is established.
Mean TPOT is adversely higher than native by~0.29%; retain this secondary
result. Energy intervals cross0; no energy benefit established.
[Figure](kernel_network_full/kernel_network_comparison.png)
([PDF](kernel_network_full/kernel_network_comparison.pdf)) shows5 paired
values and arithmetic means; bars are means, not uncertainty intervals.

[Mean context](mean_latency_context.md) reuses only frozen summaries:
64.172157ms mean completion improvement over L is mostly64.030563ms TTFT,
with0.141594ms shorter first-to-last receive span. This locates the observed
mean change before the first token; it does not identify an internal stage.
192*64 offered12288 tokens/s exceeds delivered~11640: queue/backlog
amplification of a small capacity difference is a plausible inference.
Marginal stage P99s are never added.

## Correctness and cost limits

996 frozen-pool disagreements remain: L184,K169,N643 of57600 successes each.
The full ordinary run checks framing/length/vocabulary/frozen-pool flags, not
exact current-trajectory fidelity. Separate default8 Qwen/Smol dual replay
qualification checks captured graph/KV and fresh upstream attention metadata
against actual complete client tokens; this finite evidence is not eager-HF,
general-model or exact untraced16-bank proof.

GPU trace overflow0 differs from the bounded network reply-record buffer.
Qualification K retains128/640 network records (512 overflow); full K
likewise truncates network records. These original counters remain and prevent
complete per-reply transport tracing; they do not remove client outcomes.
See corrected qualification.md. Performance has no GPU trace instrumentation.

Owned TGID group includes its io-wq; Workspace cgroup is broader and includes
observer/control work. Shared host user/system/softirq costs include foreign
lab work and cannot be exclusively allocated or added to nested group totals.
GPU energy/queue occupancy are not total attributed service cost. Remote client
uses0.94--0.98 core across cells, with no quota/recorded throttling; measured
scheduling delays and delivered TPS are not an exclusive server-capacity ceiling.

Source input main8ad0af0; artifact-only904e1e1 publication in a verified stopped-
server data-recovery gap changes later HEAD receipts but not measured code.
One SSH timeout occurs during post-serving raw transfer, then recovery succeeds
without rerunning any cell; live follow-up all11 nodes Ready/fresh leases.
[Acquisition record](acquisition.md) retains both facts.

## Reproduction, review and decision

Frozen scripts/source/Makefile/build logs/SASS controls/client assets/config
are in this archive. Execute run_kernel_network_matrix.ps1 with actual owned
client Pod/Workspace IP as documented in plan.md; analysis is
kernel_network_analysis.py DIRECTORY. Lossless gzip originals decompress only
to OS TEMP. [Archive replay](full_archive_replay.json) reports byte-identical
full analysis stdout, empty stderr and exit0. [Fresh result review](result-review.md)
independently audits raw outcomes/69 paired rows/compiled controls/figure.

Run status: valid.
Tested hypothesis: supported for local K-L delivered throughput.
Research value: supporting.
Paper impact: additional serving-objective evidence and mechanism/workload boundary.
Next decision: retain K as an unselected experimental source snapshot.
Its local speed/CPU tradeoff does not justify replacing selected0074 silently;
no native advantage or universal latency improvement is established.

Historical Qwen192 +6.36ms receive-gap P99 is still not reproduced, causally
allocated or quantitatively repaired. This intervention improves another
ordinary completion-tail result, not that historical number. Existing0076
timing perturbation also forbids using instrumented durations to allocate it.
Next useful performance comparison is official optimized vLLM under the same
current sustained remote workload; old0069 is a short256-request reference
and must not be numerically ranked against this60s saturation run.
General backend qualification and total attributed CPU remain separate limits.
