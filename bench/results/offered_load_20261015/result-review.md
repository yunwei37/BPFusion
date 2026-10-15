# Independent result review: offered-load service comparison

Reviewer: `/root/offered_load_result_review`, fresh result reviewer, distinct from the plan reviewer. Inspected the persistent archive and current source in the original Workspace. No GPU workload, source mutation, result edit or publication action was performed.

- **Run status: valid and complete**, within the declared traced, finite, loopback token-ID HTTP comparison.
- **Tested hypothesis: inconclusive for the numerical unconditional primary because of failed-request censoring; the complete-delivery requirement is contradicted.** Neither model supports the declared no-failed-request P99 advantage.
- **Research value: supporting.**
- **Paper impact: mechanism/workload boundary and additional service evidence**, not a direct thesis challenge.
- **Next decision: retain the original production selection; publish the complete negative evidence.** Prioritize admission waiting/ownership over another timer variation or model-arithmetic optimization. This review does not assess or approve the separate unexecuted pending-admission candidate.

## Completion and executable fidelity

`full.exit.json`, both model terminals, `full.statuses.json` and all 20 executor exits agree: the wrapper terminated successfully at **2026-10-15T09:17:40.729227 UTC**. Original full PID 528787 is absent. All **80 cells, 20,480 measured attempts and 160 gen1 warmups** are present.

Measured outcomes independently counted:

| Model | Attempts | Successful | Failed | Successful measured tokens |
|---|---:|---:|---:|---:|
| Qwen2.5-0.5B | 10,240 | 9,787 | 453 | 626,368 |
| SmolLM2-135M | 10,240 | 9,984 | 256 | 638,976 |
| Total | 20,480 | 19,771 | 709 | 1,265,344 |

These successful counts include both paths. All failures occur on the kernel side. Collection success must remain distinct from successful service delivery.

Setup, qualification and preflight terminal records are complete. Actual compiler logs bind the CUDA variants and adaptive BPF object to their private inputs, with matching model-computation flags. The kernel CUDA file equals the archived original; the native CUDA change only calls its shutdown notifier. Relative to0060, the kernel queue header and BPF loop are identical; the I/O header differs only in the private BPF-object pathname. The source-binding repair and metric/scheduling corrections precede execution.

I found no observed mid-run oracle, timeout, metric or workload relaxation, no favorable-cell replacement, and no missing/unreported executor suffix.

## Independent recomputation

I recomputed the 80 cell rows directly from raw request timestamps, token arrivals, outcomes and CPU snapshots using a separate calculation. All saved timing quantiles/means, successful-request throughput, output-token throughput, process CPU per attempt, duration and scheduling-lag P99 agree within floating-point tolerance.

All **48 paired contrasts** independently reproduce their five effects, means, nominal t95df4 intervals and censoring flags. The two primary rows reproduce:

| Model | Conditional kernel−native P99 | Nominal paired t95 |
|---|---:|---:|
| Qwen | −52.429704 ms | [−101.969195, −2.890212] |
| Smol | −7.851692 ms | [−22.570351, 6.866967] |

Both have failed kernel requests in every primary block. The favorable conditional Qwen interval cannot support unconditional service superiority.

Separately, I reran the frozen analyzers against copied data: two protocol analyses, preflight analysis, two full analyses and two supplemental tail analyses all exited0 and reproduced the saved stdout **byte for byte**.

The draft finding’s eight conditional-P99 table rows, failure counts, primary intervals, low-load comparisons, achieved-window throughput and process CPU figures agree with the raw calculations. No numerical correction is required for those claims.

## Correctness and mechanism engagement

Across all 20 full GPU histories, I independently reconstructed admission IDs, physical-bank ownership, generated token sequences and FIFO releases. Every saved reference matches those events, and every successful client response matches its independently replayed reference. No successful request is omitted or checked against a reference belonging to another marker.

The backend’s replay is substantive: it reconstructs graph inputs, positions, KV slots and histories using its own previous replay outputs, replays upstream body/head graphs, and compares each computed token with the observed event. It does not merely copy serving tokens into an oracle. Every executor records the actual replay completion before exit0. CPU review rechecks the saved evidence; it is not a new GPU numerical execution.

Both sides use the same traced FP16 model computation, banks, graph options and dispatcher. This establishes the stated trajectory-matched correctness scope, **not** arbitrary untraced fidelity or batch-independent equivalence.

All **709 errors** are `TimeoutError`, with no received token or partial output; every failed marker is absent from model references. Per kernel process, error counts exactly match page drops and `llm busy`:

- Qwen: 96, 83, 92, 82, 100.
- Smol: 59, 46, 60, 38, 53.

The actual code at `bpf/fusion.bpf.c:394–395` reserves the next model slot and returns `SK_DROP` when it cannot. This directly supports an admission-loss explanation. Describe it precisely as **the next physical slot remaining reserved**; the source does not require proving that all eight physical slots are simultaneously occupied.

Ring acceptance/closure, completed/head, SQ/CQ drain and zero ring error/pending/reserved/dropped/overflow checks hold. Their zero values do not negate separate model-admission drops. The bounded128-entry reply diagnostic overflow is correctly distinguished from actual BF_TRACE history overflow, which remains0.

Qualification genuinely exercised both mechanisms: four622-request protocol cases independently replay successfully, including actual batches1–8. Native executes the expected socket calls; the kernel path’s protocol trace verifies its absence of steady userspace accept/receive/send and the expected single BPF-loop entry.

Four lifecycle cases retain32 actions each and independently match the frozen complete/prefix references for **652 observed tokens per case**. Two rows per case are partial. Native records32 published/31 completed under stop-with-active-work; this is not32 fully delivered numerical responses. The draft’s cautious lifecycle wording is appropriate. Idle deadline/helper shutdown records qualify the changed native waiting mechanism without establishing a production stop-latency SLO.

## Baseline fairness and arrival limitations

The native comparator engages its intended mechanism: socket/deadline epoll while idle,60us completion checks while active or holding complete buffered work, and shutdown-only eventfd. It completes all **5,120 measured requests per model**. There is no observed avoidable baseline interface failure being counted as a proposed-method win.

Paths share model computation, prompts, requested output length and per-block normalized schedules. Process order alternates, rate order rotates, and the client schedules each request independently using an uncapped new thread. Timing starts before connection setup; post-connect and scheduled-origin timing remain separately available. No completion-driven semaphore or hidden pool cap was found.

However, these are **actual Python-thread loopback arrivals**, not ideal network arrivals. Scheduling lateness is material and must stay visible:

- Maximum cell scheduling-lag P99: **19.241940 ms** for Qwen.
- Smol pair2/kernel/64req/s: **107.677338 ms** scheduling-lag P99.

This limits attribution of millisecond tail differences exclusively to server mechanisms and prevents treating configured rate as exact achieved arrival timing. The raw and scheduled-origin metrics preserve the limitation. Add the concrete Smol outlier to the interpretation if presenting a detailed timing conclusion. It does **not** invalidate the observed admission failures or justify rerunning unfavorable cells.

The competing constructors also have different admission/buffering behavior. Therefore this is a valid complete-service-constructor comparison, not an isolated measurement of syscall removal or eBPF’s intrinsic latency.

## Tail bounds and figure

I independently recomputed all80 supplemental tail-bound rows from every attempt and checked the16 plotted aggregate rows against their source bounds. I also visually inspected the PNG. The figure correctly shows observed points, right-censored lower-bound triangles and complete failure denominators.

The supplemental analysis uses the fixed linear quantile convention without changing the primary:

- Every Qwen64/96 block has all-attempt P95/P99 lower bounds exceeding60s.
- Every Smol64/96 block has an unbounded P99 upper tail.
- At Smol64, one linear P99 lower bound is approximately27.035s; the other four exceed60s.
- Every Smol96 block has P95/P99 lower bounds exceeding60s.

These are finite-sample identification bounds, **not exact completed latencies, CIs or guarantees about eventual response**. The draft and figure maintain that distinction.

A256-attempt cell’s P99 depends on only the extreme few order statistics. Five paired process blocks and nominal t intervals do not turn it into a stable population P99 estimate. No P99.9, equivalence, steady-state capacity or broad serving-SLO inference is justified.

## CPU, throughput and host attribution

At64req/s, the draft’s achieved token rates and process CPU per attempt reproduce. Kernel throughput windows include60-second timeout drains, so the very low achieved rates measure these finite delivered-window outcomes. They do not show that the GPU’s model-compute capacity is only232/248tokens/s.

Process CPU includes executor threads but omits portions of RX/softirq/io-wq and client costs. Different success fractions also prevent equal-work CPU attribution. Neither this run nor the previous idle-CPU result establishes total-service CPU, energy saving or an exclusive GPU bottleneck.

Sparse host receipts have the same boot ID and exactly the same56 selected historical warning lines. Their phases are correctly stated:

- Qwen08:02:04 lies inside pair0/rate32 measurement and timeout drainage.
- Smol08:58:01.879603 lies inside pair2/rate4 measurement.
- After receipt09:18:57.831632 is77.102405 seconds after full terminal and shows no GPU application.

The active GPU PIDs map to the Workspace executors at the two sampled moments. This does not prove continuous isolation or the absence of unselected/unlogged faults. The draft does not overclaim those properties.

## Final disposition

No discovered scientific or execution defect invalidates this collection. It is a valid, complete, decision-relevant **negative service result**.

Keep the predeclared numerical primary classified as censored/inconclusive; separately state that the observed complete-delivery requirement fails. Do not promote conditional successful-only tails, idle CPU savings or dependency qualification into a latency/TPS victory.

Close this unchanged comparison after preservation, owned cleanup/restoration and honest main publication. Those operational steps were still pending at review time and are not certified complete here. The separate admission-waiting candidate requires its own execution evidence; this review neither inspects nor endorses it.
