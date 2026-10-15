# No reliable high-load tail advantage against fair native admission

The complete matched follow-up establishes no reliable kernel TTFT-P99 advantage
against an eligible-frame FIFO native server. All10,240 measured requests complete
and655,360 output tokens pass trajectory-matched upstream replay. Both new96/s
primary intervals cross zero. Removing the known FD-priority weakness is a
meaningful stronger comparison, not evidence of an intrinsic eBPF speedup or
equivalence. The native candidate remains archived and unselected.

The retained question is whether a reusable eBPF/kernel serving path around the
same GPU computation improves complete-service latency/throughput while removing
a steady userspace request worker. There is no formal paper RQ/thesis contract.
[Plan](../../bench/results/fair_admission_20261015/plan.md),
[plan review](../../bench/results/fair_admission_20261015/plan-review.md) and the
[complete archive](../../bench/results/fair_admission_20261015/) preserve scope.
Role: supporting. Impact: mechanism/workload boundary.

## Why this comparison matters

Finding0062's secondary Qwen96/s result was280/1418ms kernel/native TTFT P99,
but the native FD-order scan allowed substantial overtaking of waiting requests.
The corresponding client-stamp maximum bypass was149/175/165/72/159 versus
kernel1/2/2/1/1. Those stamps precede sends; they are not exact ingress times.

This follow-up changes only private native admission to FIFO among complete
eligible frames. It preserves the event-driven wait, nonblocking replies, one
active response per connection and existing independent upstream computation.
The kernel FIFO loop is unchanged from70988bed. Both paths share FP16 vLLM graphs,
weights, KV setup, packed prefill, FIFO prefix release and eight model banks.
No model arithmetic, placement, transport flag, timer or host policy is tuned.

The new fixed primary is per-model connect-begin-to-first-token P99 at96/s;
64/s is secondary. This does not relabel0062's original64/s primary.
Five paired process blocks/model alternate path order and rotate rate order.
Each cell has256 independently scheduled gen64 requests from four short prompts.
Both paths use the same per-pair normalized gamma(shape1) arrival schedule.
Collection is finite and loopback, with actual Python-thread scheduling on a
shared host. Metric definitions reuse the
[official vLLM benchmark](https://docs.vllm.ai/en/stable/cli/bench/serve/);
the token-ID HTTP adapter is not an official text/JSON endpoint benchmark.

## Complete results

Full terminal is2026-10-15T13:20:13.202909UTC. All20 executors/40cells complete:
10,240/10,240 measured requests, zero failures,655,360 checked measured tokens,
plus160 checked gen1 warmups. No serving cell is replaced or excluded, and
oracle, timeout, computation and metrics stay fixed during collection.

Values below are means of five block statistics, not pooled quantiles.
Every pair is kernel/native; times are milliseconds.

| Model | Configured req/s | TTFT P50 | TTFT P95 | TTFT P99 | Completion P99 | Output token/s | Executor CPU ms/attempt |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-0.5B | 64 | 4.382 / 3.346 | 33.779 / 33.855 | 49.229 / 47.612 | 134.541 / 133.794 | 4009.419 / 4011.371 | 1.045 / 0.751 |
| Qwen2.5-0.5B | 96 | 121.388 / 94.274 | 226.247 / 189.941 | 246.358 / 220.245 | 330.976 / 300.859 | 5600.243 / 5668.162 | 0.998 / 0.630 |
| SmolLM2-135M | 64 | 3.445 / 2.669 | 15.086 / 14.466 | 24.144 / 24.415 | 92.049 / 90.641 | 4032.477 / 4032.179 | 0.933 / 0.749 |
| SmolLM2-135M | 96 | 14.190 / 12.377 | 66.680 / 54.482 | 80.777 / 66.204 | 165.198 / 135.322 | 5991.070 / 5995.084 | 0.711 / 0.548 |

Kernel-minus-native primary P99 effects, nominal paired t95df4:

- Qwen: +26.113ms [-121.273,173.499].
- Smol: +14.573ms [-26.449,55.596].

Both are inconclusive; this is neither a reliable advantage nor equivalence.
The64/s secondary P99 contrasts are+1.617ms [-5.165,8.399] Qwen and-0.272ms
[-8.483,7.939] Smol (the exact saved rows are authoritative).
Completion-P99 and scheduled-origin primary-rate contrasts also cross zero.
Qwen96/s throughput difference is-67.919token/s [-348.642,212.804];
Smol is-4.013 [-9.476,1.450]. No throughput superiority is established.

The median is higher on the kernel path in the block means shown. Qwen
executor CPU is also higher:96/s difference+0.368205ms/attempt
[0.210310,0.526100]. This CPU bracket excludes client, RX/softirq and some
io-wq work; it is not whole-service CPU or energy. Earlier idle CPU savings
cannot be transferred into a current active-workload CPU benefit.

[Figure](../../bench/results/fair_admission_20261015/fair_admission_results.png)
shows all block P99/P50 points and means.
[Source data](../../bench/results/fair_admission_20261015/fair_admission_results.data.json)
retain all cell/paired metrics and denominators.

## Queue fairness and generation stalls

Both queues actually engage. Executor-wide peaks are11..36 entries on Qwen
kernel and12..29 native; Smol kernel6..17 and native6..17. Final native deque,
kernel reservations, model slots and SQ/CQ are drained. At96/s maximum
later-client-stamp bypass is Qwen kernel1/1/1/1/1 versus native1/0/1/1/0,
and Smol kernel1/1/1/2/0 versus native1/0/1/1/2.
[Saved ordering analysis](../../bench/results/fair_admission_20261015/admission_order.json)
supports engagement of the stronger fairness class, not exact ingress ordering,
queue residence or syscall-only causality. Kernel pipelining and finite4096
admission limit still differ from native eligibility/buffering policies; measured
traffic has one request per connection and never approaches that queue limit.

The user also requested generation-stall tails during collection. The
[supplement](../../bench/results/fair_admission_20261015/tail_summary.json) is
post-collection analysis of saved arrival timestamps, not a changed primary.
At96/s, mean block client-observed gap P99 is7.133/5.192ms Qwen and5.670/5.702ms
Smol. Mean block P99 of each request's maximum gap is27.110/57.052ms Qwen and
53.870/12.760ms Smol. These different summaries must not be conflated.

Each recv timestamps all newly observed token IDs together; coalesced tokens have
zero gaps. Thus these are client-observed stalls, including client scheduling
and buffering, not isolated GPU decode duration. They do not support a stable
stall advantage. Each256-request cell has few P99 order statistics; no P99.9,
rare-event guarantee, production SLO or steady-state capacity claim follows.

## Correctness, host limits and decision

Qualification completes four640-outcome protocol executors:2560 total outcomes,
including1036 intended rejections, with93,504 replayed tokens. Native retained
32-action lifecycle checks include partial/reset/stop observations; they do not
newly prove cancellation of a large queued backlog. Both idle cases and the
128-request real preflight pass; both preflight queues reach16 and drain.

Full successful wire responses match independently replayed upstream graph/head
histories; actual BF_TRACE history overflow is zero. The bounded128-entry reply
diagnostic can overflow at520 histories/executor and is distinct from lost
numerical history. This is traced trajectory-matched fidelity for two checkpoints,
not universal model/backend support or batch-independent output equivalence.

Actual scheduling lag is material: maximum cell P99 is197.821ms Qwen
(pair2/native96) and179.102ms Smol (pair2/kernel96). These outliers are retained
in connect- and scheduled-origin results. They limit attribution of small server
differences. Shared-host ambient CPU samples show other Workspace activity;
no foreign process or host setting was changed.

The short Smol GPU ownership snapshot lies inside pair2/kernel64 measurement.
The Qwen snapshot is0.682474s after its sampled cells. The after snapshot is
58.553113s after full terminal, shows no GPU app, same boot and the same56
selected historical fault lines. Sparse observations establish neither continuous
GPU exclusivity nor absence of all possible faults.

Five copied fixed CPU analyses reproduce saved stdout byte-for-byte.
Plot dependencies were installed only after collection and changed no existing
measurement package; figure QA used an identical-source90dpi preview.
The fresh independent [result review](../../bench/results/fair_admission_20261015/result-review.md)
finds valid complete supporting evidence with an inconclusive hypothesis.
[Final restoration](../../bench/results/fair_admission_20261015/final_restoration.json)
records removal of the owned temporary runtime/build directory after no live
users remained. Seven copied-data analyses then reproduce bytewise without that
directory. Original sessions,eight build/setup artifacts,base packages and
cached weights are preserved. Production sources remain unchanged; publication
of this record does not select the archived native candidate.

Withdraw any general tail-advantage inference from the old FD-priority comparison.
The present data are consistent with admission fairness being a substantial
competing explanation, but old/new runs on a shared host are not a simultaneous
causal ablation. Preserve all positive/adverse/inconclusive observations.
No further unchanged matrix, weak-baseline rerun or model-specific arithmetic
optimization follows from this result. The reusable serving boundary stays the
project target; whole-service CPU and coordination/queue timing remain unresolved.
The retained full project objective remains active.
