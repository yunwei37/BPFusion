# Fair native admission: RESULT REVIEW

Reviewer: `/root/fair_admission_result_review`  
Review: one fresh result review of the complete collection  
Reviewed archive: `bench/results/fair_admission_20261015`  
Observation date: 2026-10-15 UTC

## Verdict and five judgments

- **run status: valid**
- **tested hypothesis: inconclusive**
- **research value: supporting**
- **paper impact: mechanism or workload boundary**
- **next paper decision:** Withdraw a general kernel tail-advantage inference from the older FD-priority comparison. This complete stronger comparison establishes neither kernel TTFT-P99 superiority nor equivalence. Retain the reusable same-compute serving objective, all adverse effects and shared-host limitations. Another unchanged matrix or obsolete weak comparator would add little evidence.

The tested hypothesis is that a high-load kernel-loop TTFT-P99 advantage persists against event-driven native TCP with FIFO admission among complete eligible frames. There is no formal paper RQ or central thesis contract. This result bounds that mechanism/workload and does not refute the whole project objective.

No result-invalidating scientific defect was found within the declared finite, traced, loopback, shared-host scope. This verdict does not certify broad overload cancellation, production SLOs, universal model support or adoption of the private native implementation.

## What I inspected and independently recomputed

I read the plan, fresh plan review, complete native candidate header/diff, setup/build bindings, load/client/backend sources, fixed analysis, protocol analysis, lifecycle and idle evidence, full driver records and all model-history/reference sidecars. I inspected the ordering and requested token-gap supplement, figure source/data and postcollection dependency/host receipts. I read the draft finding0063 and checked its presented numbers.

Through the original Workspace, I ran CPU-only checks. No GPU workload, source change, new experiment, rerun of a serving cell or publication action was performed.

Independent checks covered:

- All 40 cells and all five paired blocks per model; exact attempt and token denominators.
- Every full executor's admissions, compute tokens, physical-bank ownership, ordered releases and final empty ownership.
- A bijection between all client markers and reference histories, exact input/output tokens and requested lengths, including warmups.
- Raw timestamp-derived connect-inclusive TTFT/completion and scheduled-origin P99, linear interpolation and all associated five-block effects/nominal t95 intervals.
- Replay of all five frozen analyses from archived paths, byte-equal to saved stdout: two protocol analyses, real preflight and both full models.
- Both supplement scripts reproduce saved JSON byte-for-byte. Separately reconstructed every cell's 16,128 token gaps and per-request maximum-gap P99 directly from arrival timestamps.
- All 40 figure cells, 24 paired rows and two coverage records exactly match the frozen model analyses. I visually inspected a resized JPEG preview of the canonical PNG; labels, points, mean diamonds and the shaded primary rate are legible. This was visual inspection of a downsampled preview, not original-resolution pixel QA.

The compute/kernel candidate files other than the intentionally changed native header and source-binding Makefile are byte-equal to source parent70988bed7d25f313e85277fa420894f1ff835bcf. Embedded full-run driver/client/backend sources match the inspected sources. Existing package versions are unchanged; plot-only additions begin after full terminal.

## Completion, correctness and exclusions

Both full model drivers and analyses finish exit0. Full terminal is2026-10-15T13:20:13.202909UTC; wrapper terminal follows at13:20:13.211001UTC.

| Quantity | Qwen | Smol | Total |
|---|---:|---:|---:|
| Executors | 10 | 10 | 20 |
| Measured cells | 20 | 20 | 40 |
| Measured attempts | 5120 | 5120 | 10240 |
| Measured successes | 5120 | 5120 | 10240 |
| Measured failures | 0 | 0 | 0 |
| Measured output tokens | 327680 | 327680 | 655360 |
| Checked gen1 warmups | 80 | 80 | 160 |

Each executor has520 admitted/released histories, including eight warmups, and32776 checked tokens. All20 execute actual batches1..8. No measured request or cell is excluded or replaced. The recorded request/error event accounting, complete raw records and terminal states agree.

The oracle is not circular: after online execution, the backend reconstructs prompts, positions, padding, physical KV mappings and histories, replays upstream body/head graphs, compares every produced token, and advances replay histories with replayed outputs. It independently checks ownership/release. Client responses then match those references. This is trajectory-matched numerical fidelity for the two checkpoints and trace condition, not batch-independent sequence equivalence or a general quality benchmark.

The bounded128-entry reply diagnostic can overflow by392 at520 histories; this is distinct from the actual model-history trace, whose overflow is zero. Complete numerical histories are present.

Qualification has four640-outcome protocol executors,2560 outcomes including1036 intended rejections and93504 replayed tokens. These are not2560 successful inference responses. Both retained native32-action lifecycle records pass their fixed complete/prefix checks, published32/completed31/rejected10, with no remaining pins or graph error. They deliberately include a partial stopped response, and do not prove cancellation of a large new FIFO backlog. Both idle cases pass. The sole real preflight has128 measured successes,8192 tokens and16 warmups; both queues reach16 and drain.

## Comparator fairness and mechanism engagement

The native implementation removes the previous FD-order publication scan. Complete eligible frames enter one deque entry per Peer; only its head obtains the next physical slot. Queued shared ownership preserves the old Peer across FD reuse; disconnected old entries are skipped. Receive handling, event-driven idle/deadline wait,60us active progression, nonblocking streaming and eventfd stop are retained. Both paths execute the same resident model constructor, weights, FP16 graphs and eight banks.

The comparator is engaged, not merely labeled:

| Model | Kernel executor-wide queued peaks, pairs0..4 | Native peaks |
|---|---|---|
| Qwen | 29,11,17,36,23 | 28,12,29,17,21 |
| Smol | 17,6,15,6,7 | 17,6,7,6,7 |

All final native deques are empty; kernel reservations, slots and SQ/CQ drain. At96/s, maximum later-client-stamp bypass is Qwen kernel1/1/1/1/1 versus native1/0/1/1/0; Smol kernel1/1/1/2/0 versus native1/0/1/1/2. Across all40cells it is0..2. The substantial native starvation pattern of the earlier FD-priority result is absent in this diagnostic.

Client stamps precede sends and are not ingress timestamps. These data do not measure exact queue residence or prove identical arrival order. Native eligibility retains one active response per connection, while kernel pipelining differs; native buffering is uncapped and kernel admission capacity is4096. Measured traffic uses one request per connection, never approaches that capacity and has no deliberate queued-backlog stop. This is a fair stronger competitor for the declared workload, not identical protocol policy at arbitrary overload.

## Fixed primary and adverse results

This follow-up predeclares96/s per-model connect-begin-to-first-token P99 as primary, with64/s secondary. It does not relabel finding0062's original64/s primary. All table values are means of five block statistics, not pooled percentiles. Effects are kernel minus native; intervals are nominal paired t95df4.

| Model/rate | TTFT P99 kernel/native, ms | Difference, ms | Nominal interval, ms |
|---|---:|---:|---:|
| Qwen96 primary | 246.358 /220.245 | +26.113 | [-121.273,173.499] |
| Smol96 primary | 80.777 /66.204 | +14.573 | [-26.449,55.596] |
| Qwen64 secondary | 49.229 /47.612 | +1.617 | [-5.165,8.399] |
| Smol64 secondary | 24.144 /24.415 | -0.272 | [-8.483,7.939] |

Both primary intervals cross zero. No failed-request censoring applies because every measured attempt succeeds. This is inconclusive, not equivalence and not proof that kernel is slower.

At96/s, block-mean TTFT P50 is121.388/94.274ms Qwen and14.190/12.377ms Smol. Completion P99 is330.976/300.859ms and165.198/135.322ms. Completion-P99 and scheduled-origin P99 effects also cross zero.

Output throughput at96/s is5600.243/5668.162token/s Qwen, difference-67.919[-348.642,212.804], and5991.070/5995.084 Smol, difference-4.013[-9.476,1.450]. Finite offered-load delivery does not establish maximum steady-state capacity or throughput superiority.

Executor CPU at96/s is0.998/0.630ms per attempt Qwen and0.711/0.548 Smol. Qwen's difference is+0.368205[0.210310,0.526100]; Smol's is+0.162885[-0.077821,0.403591]. At64/s both model CPU effects are also adverse in the block means. Partial process CPU excludes client/RX/softirq and some io-wq work and energy. Prior idle CPU savings must not be presented as active-workload CPU savings in this result.

## Requested token-gap tails

The saved-data supplement answers the user's additional tail question without changing the primary. At96/s:

| Model | Mean block client-gap P99 kernel/native, ms | Mean block P99 of request-maximum gap, ms |
|---|---:|---:|
| Qwen | 7.133 /5.192 | 27.110 /57.052 |
| Smol | 5.670 /5.702 | 53.870 /12.760 |

All40cells contribute16,128 adjacent-token gaps each,645,120 total. Per-cell pooled gap quantiles weight transitions equally; per-request maximum-gap quantiles weight requests equally. These summaries answer different questions, and neither establishes stable stall superiority here. No paired uncertainty was prespecified for these exploratory summaries.

All newly observed IDs from one recv share a timestamp, so coalescing produces zero gaps. These are client-observed gaps including scheduling/network buffering, not isolated GPU decode intervals. Do not call them GPU token latency.

## Scheduling, host scope, figure and claim limits

The client starts independent request threads at absolute schedules rather than imposing a completion-based concurrency cap. Both paths receive identical normalized per-pair arrival offsets; mode order alternates and rate order rotates. Nevertheless actual scheduling is imperfect. Maximum cell scheduling-lag P99 is197.821ms for Qwen pair2/native96 and179.102ms for Smol pair2/kernel96. These unfavorable cells remain in every result. Scheduled-origin metrics are retained and do not create superiority.

The host is shared. A CPU sample identifies other Workspace activity and actual own cgroup has no hard CPU quota, with cpu.weight1. The sample occurs during native preflight bootstrap, not measured serving. No foreign workload was controlled or stopped. The Smol short GPU snapshot lies inside pair2/kernel64, the Qwen short snapshot occurs0.682474s after its sampled cells, and the after snapshot is58.553113s after full terminal. Boot ID and56 selected historical fault lines are unchanged, and no GPU application is reported at that after snapshot. These sparse observations cannot establish continuous GPU exclusivity, absence of every possible fault or causal responsibility for an outlier.

The figure includes all block P99/P50 points and their mean diamonds, uses log axes and labels96/s as primary. Its accompanying data preserve coverage and paired uncertainty. The figure alone does not display confidence intervals; interpretation must retain the primary interval table. Plot dependencies were added after measurement, with no existing measurement-package changes.

256 attempts per cell provide only a few P99 order statistics. Five sequential paired blocks and nominal t intervals on a shared host do not support P99.9, precise rare-event probabilities, production SLO guarantees, remote-network generalization, syscall-only causality, total CPU savings or universal model/backend claims.

## Finding and disposition

Draft0063's tables, effect intervals, adverse CPU/throughput discussion and exploratory gap summaries agree with the inspected data. Its body correctly avoids an old/new causal ablation claim. I recommended changing its title from “Fair native admission removes the apparent high-load tail advantage” to “No reliable high-load tail advantage against fair native admission” so the title has the same scope.

The earlier FD-priority result remains valid historical evidence of that implementation, but it does not establish a general kernel tail advantage. The new result makes fairness a substantial competing explanation without estimating a simultaneous old/new causal effect.

Return this valid supporting result to the orchestrator. Native FIFO remains private/unselected at review time; the verdict neither requires nor authorizes production adoption, a broader backlog-cancellation claim, model arithmetic tuning or a repeated unchanged experiment. Owned cleanup, main publication and final documentation status are still the root agent's remaining delivery work.
