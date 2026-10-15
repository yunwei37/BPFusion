# Adaptive kernel-loop wait: CPU saving with a delivery tradeoff

Observed 2026-10-15 UTC on original Workspace main base
`d87b8e0bc1584123f2c0296ae13ab2dac999a2d6`.
[Plan](../../bench/results/adaptive_wait_20261015/plan.md),
[plan review](../../bench/results/adaptive_wait_20261015/plan-review.md),
[raw archive](../../bench/results/adaptive_wait_20261015/) and
[fresh result review](../../bench/results/adaptive_wait_20261015/result-review.md)
retain the complete comparison.

The repaired finite traced run is valid. Reducing idle timer completions lowers
executor-process CPU in both models, but Smol's achieved burst throughput falls.
The full lower-CPU-without-adverse-delivery hypothesis is therefore mixed/
contradicted as a conjunction. Select original source; the candidate remains
experimental evidence, with zero retained production-code growth.

## Question and intervention

Within the retained Linux TCP/eBPF/GPU-serving objective, does request-aware
waiting reduce coordination cost without hurting delivery? This is supporting
mechanism evidence, not a new model kernel or a formal RQ rewrite. Prior
publication/bookkeeping runs did not measure this idle-wait intervention.
Reusing their raw data cannot supply the missing intervention.

Original before-submit BPF-loop behavior produces a multishot timeout CQE every
60000 ns even while idle. The candidate updates the same timer to the remaining
service deadline while no model work is queued, restoring the existing interval
for active requests. GPU completion acknowledgement and SQ publication ordering
guard the wait transition; kernel monotonic time supplies the remaining interval.
The existing after-submit macro keeps its original behavior because review found
an ordering counterexample there. No new flag, controller or steady userspace
request worker is added. Shared report storage grows32 to48 bytes, outside the
canonical shared request page ABI. Model/dispatcher arithmetic is unchanged.

Three compared conditions reuse identical default optimized FP16 vLLM computation:
adaptive loop, original fixed loop (component ablation), and efficient native
TCP (main competitor). Native itself uses fixed60000 ns epoll timeouts while
idle. Its CPU contrast cannot establish an advantage over adaptive/event-driven
native TCP or prove that these savings require eBPF.

## Completed workload and results

Two cached checkpoints: Qwen2.5-0.5B-Instruct revision
`7ae557604adf67be50417f59c2c2f167def9a775`, SmolLM2-135M revision
`93efa2f097d58c2a74874c7e644dbc9b0cee75a2`.
Each process has8 checked one-token warmups and two cells: gen1/c1, gen64/c8.
Each cell has four waves of8 requests and1 s quiet gaps after the first three.
Five paired blocks/model rotate path/cell order. Full collection completes30
executors,60 cells,1920 measured requests,62400 tokens plus240 warmups;
both drivers/fixed analyses and final wrapper exit0 at06:55:14.755647 UTC.
No full serving failure, exclusion, replacement, retry or oracle/timeout/metric
change. BF_TRACE logical histories and independent graph/KV replay check outputs;
there is no profiler or upstream batch-invariant mode.

Primary gen64/c8 executor-process CPU, milliseconds/request:

| Model | Adaptive | Fixed | Native | Adaptive minus fixed, nominal paired t95 |
|---|---:|---:|---:|---|
| Qwen | 1.021333 | 3.030955 | 2.878811 | -2.009622 [-2.485738,-1.533506] |
| Smol | 0.888569 | 2.980229 | 2.733718 | -2.091660 [-2.467929,-1.715392] |

Mean-ratio reductions are66.30%/70.18%, all five paired effects negative.
POSIX process clocks cover all executor threads and the cell's quiet gaps.
They exclude some kernel RX/softirq/io-wq CPU and are neither total service CPU
nor energy measurements or exclusive BPF attribution.

Gen64/c8 achieved wall token/s:

| Model | Adaptive | Fixed | Native | Adaptive minus fixed, nominal paired t95 |
|---|---:|---:|---:|---|
| Qwen | 603.031064 | 599.922171 | 604.134199 | +3.108893 [-0.104133,+6.321919] |
| Smol | 614.487674 | 616.493501 | 616.618516 | -2.005826 [-3.049775,-0.961878] |

This includes quiet gaps and fresh wave connections; it is not saturated
capacity and must not be compared numerically with earlier continuous-load TPS.
Smol's five paired effects are all adverse (mean-ratio loss0.325%).
Both adaptive-minus-native throughput intervals cross zero; that establishes
neither superiority nor equivalence/noninferiority.

Gen64/c8 TTFT adaptive/fixed/native is2.595955/2.714130/2.623918 ms Qwen and
2.349833/2.580223/2.188037 ms Smol. Gen1/c1 is
1.538648/1.630396/1.505792 ms and1.441838/1.392865/1.316085 ms respectively.
All corresponding adaptive latency contrasts cross zero. TTFT starts after
connect; connection setup is outside this timing definition.

Qwen secondary completion improves versus fixed by3.431752 ms
(t95 [-5.901725,-0.961778]) and TPOT by0.052596 ms
([-0.088581,-0.016612]); native contrasts remain inconclusive.
Smol completion/TPOT contrasts cross zero. All12 metric rows,78 signed contrasts,
block effects and outliers remain in the fixed outputs and independent appendix.
No secondary benefit replaces the primary or erases the adverse delivery row.
Five-block t95df4 intervals are nominal, without multiple-testing correction.

## Failure, repair and qualification

Real preflight passes all three Qwen paths and a zero-request2 s service.
Its ready-to-Python-exit7.035 s includes upstream teardown, not native deadline
latency. Preflight used the pre-shutdown-repair candidate and establishes setup
only for that version.

The first qualification delivers all622 Qwen requests, then exposes a shutdown
failure: helper-thread SIGTERM sets the stop flag while the loop owner remains
asleep. At06:15:50.968793 UTC the unresolved stop is captured in
`qualification.helper_stop_failure.json`; only its wrapper/executor is manually
stopped/woken for cleanup. Its subsequent raw driver PASS is manually assisted
and invalid as natural-stop evidence. No full cells ran on that version.

The candidate records the actual io_uring wait-owner TID and forwards shutdown
SIGTERM there when received by another thread, avoiding self-recursion.
Both affected model protocol/lifecycle suites are rerun under separate repaired
paths before full collection. Each protocol checks622 requests/22224 tokens,
259 intended rejections,5000 empty connections, batches1..8 and independent
history replay. All-thread traces show no steady network syscalls and one
io_uring entry. Natural owner wake/cleanup is observed in both repaired traces;
those strace timings are not production SLO estimates.

Each unchanged32-action lifecycle passes frozen complete/prefix controls,
652 checked tokens/prefix tokens,13 closed connections and empty SQ/CQ, with
no pending/reserved/error/drop/overflow. This finite traced qualification does
not explain or close finding0058's ordinary default-mode reference-pool failure.
Prepared HF/coalesced/after compatibility adapters were never built/run and
supply no compatibility claim; they are unnecessary for selecting an unretained
shared-helper patch.

## Host, source selection and reproducibility

Pinned private setup uses vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0,
NumPy2.3.5, libbpf1.6.3 and NVCC13.0.88 on RTX5090/Linux7.3-rc3.
Actual Makefile invocations, sources, commands, package and environment records
remain in the archive. Private BPF object path rewrites are distinct from the
true production-original/candidate/patch snapshots.

Four sparse host receipts show the same boot, existing400W limit and exactly
equal56 selected historical warning lines. Both during-full GPU-owner samples
are bootstrap/pre-ready, not serving coverage. After is07:04:12.724552 UTC,
537.968905 s after terminal, with no GPU application. This is not continuous
isolation or evidence that historical warnings are harmless. Whole-host counters
mix client/kernel/other activity and remain descriptive.

[Restoration](../../bench/results/adaptive_wait_20261015/final_restoration.json)
records original source selection, preserved eight setup/build paths, base
packages/Coder starttimes, absent module/pins, private dependency/build cleanup
and five byte-identical CPU replays. No serving/default change is retained.
The valid related-work refresh is independent of the rejected candidate.

Close this unchanged matrix. Stronger complete-service offered-load/tail and
total-cost evidence against a credible event-driven native competitor has more
decision value than another unmotivated timer/publication micro-optimization.
Reusable backend breadth still needs actual unchanged-engine hardware/API and
fidelity qualification; model-specific arithmetic work is not justified by
these results. The larger serving/latency/TPS objective remains open.
