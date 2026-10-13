# Fresh result review: optimized stock TCP transport matrix

Reviewer: `/root/vllm_uring_result_review`. Read-only review of the original `yunwei356/bpfusion-dev` Workspace, `/workspaces/repository`, main, on 2026-10-13 UTC. No source edits, serving runs, configuration changes, or cleanup were performed.

## Judgments

- **Run status: valid**, within the declared local workload, implementation, timing, and finite-reference scope. Temporary runtime cleanup remains a separate closure action.
- **Tested hypothesis: inconclusive overall.** Neither model demonstrates a reliable stock-path TTFT improvement. Qwen’s long-output throughput result contradicts improvement in that cell; Smol’s throughput result is inconclusive.
- **Research value: supporting.** This adds the previously absent matched stock-transport and known-worker CPU evidence. Qualification, provenance, and packaging are dependencies rather than independent contributions.
- **Paper impact: mechanism/workload boundary and additional RQ evidence.** It does not directly challenge a necessary paper thesis or answer the separate cross-node question.
- **Next paper decision:** retain the module-free stock path as a qualified implementation option, publish its measured CPU cost and negative/inconclusive performance results, and withhold claims that removing the steady userspace request worker improves latency, throughput, or CPU consumption under these tested conditions. Do not repeat the unchanged matrix to seek a favorable outcome.

## Selected question and evidence inspected

The retained question is:

> what client latency/throughput does the ordinary packed/prefix adapter deliver against the efficient native network alternative after BF_TRACE is removed?

This experiment compares the complete stock io_uring implementation against the efficient native timed-epoll implementation. The module path is a component control. It does not compare against an official vLLM serving stack or establish SOTA performance.

I inspected `plan.md`, both rounds in `plan-review.md`, literal build/qualification/performance commands and pipeline files, status records, the frozen reference asset and its source assets, both performance JSONL files, both correctness JSONL files, the 36 performance stdout logs, six strict syscall traces, the driver/client/backend/native/header/Makefile/module source, the analyzer, and the before/after Workspace/host receipts.

In addition to rerunning the existing analyzer, I independently reconstructed coverage, schedules, output membership, client-arrival metrics, CPU counter differences, paired effects, and relevant terminal counters using Python standard-library code. Both analyzer reruns exited zero and reproduced their archived stdout exactly.

## Completion and provenance

The full timing matrix ran to terminal success:

| Coverage | Verified total |
|---|---:|
| Models | 2 |
| Process blocks/model | 6 |
| Transports/block | 3 |
| Executors | 36 |
| Measured cells | 144 |
| Measured requests | 9,216 |
| Measured output tokens | 299,520 |
| Excluded, checked warmup requests/tokens | 288 / 288 |

Each executor served 264 requests: eight gen1 warmups and four cells of 64 measured requests. All measured indices are exactly `0..63`, without duplicates or omissions. Every cell uses the four tokenized prompts in the prescribed `index % 4` order.

Actual transport order matches all six permutations exactly:

1. uring, userspace, kernel
2. uring, kernel, userspace
3. userspace, uring, kernel
4. userspace, kernel, uring
5. kernel, uring, userspace
6. kernel, userspace, uring

The actual four-cell rotation matches the plan and is identical across transports within each block. Qwen runs precede Smol. Full performance windows are Qwen **04:26:49–04:35:42 UTC** and Smol **04:35:47–04:43:54 UTC**.

All performance metadata records frozen source commit:

`e7092937534c1dea8cb163fcb817d09ad2b33597`

Embedded driver, client, backend, and native source exactly match that commit. Current shared I/O header, userspace header, module source, Makefile, and analyzer also match the frozen commit. There is no detected in-run source change, oracle expansion, excluded process block, failed timing prefix, or metric-changing deviation.

The recorded build, Qwen preflight, both complete ordinary correctness stages, both full performance stages, and their analyses all report exit zero. These receipts agree with the raw data; terminal status alone was not used as proof.

## Correctness and oracle independence

`frozen_references.json` records `frozen_at=2026-10-13T04:16:47.805543+00:00`, before preflight and timing. It contains:

- Qwen: 17 prompt/gen keys, 22 complete sequences.
- Smol: 17 prompt/gen keys, 19 complete sequences.

I reconstructed the exact union of the earlier default-untraced asset and the archived io_uring qualification replay references. It equals the frozen sets for both models. The references embedded in both new performance files equal the archived frozen model assets.

Every valid warmup and measured reply equals one **entire** qualified sequence for its exact prompt/gen key. Tokenwise combinations, tolerance, and post-observation additions are absent. Client markers are unique across all 4,752 delivered requests per model.

The historical replay code independently advances upstream graph computation using its own generated token history and checks computed tokens against the trace. It does not teacher-force served tokens into its autoregressive history.

However, the new ordinary runs do **not** observe or independently replay their own actual batch/cache histories. Membership in a historical complete-output set is weaker evidence. A server returning a previously qualified sequence could satisfy this check. This experiment therefore supports fixed-workload delivery with that disclosed fidelity check; it does not establish current-trajectory equivalence, general output correctness, arbitrary-model support, or model quality.

The six ordinary strict executor runs independently cover 622 replies, 259 rejections, and 22,224 valid output tokens each. Raw kinds include fragmentation, every client concurrency from one through eight, wrap/reject reuse, continuously paced mixed outputs, six pipelined half-close replies, pipelined rejection/reuse, binary rejection/EOF, and a valid binary request afterward. No strict-oracle failure is present.

## Mechanism engagement and baseline fairness

The intended mechanisms engaged:

- Stock logs report `NET_READY`, ring binding, capacity 4096, SQ8192/CQ16384. Every stock process has a live `iou-sqp-*` entry in its recorded `/proc/PID/task` snapshot.
- Both stock strict traces contain zero userspace accept/receive/send calls after ready, and zero `io_uring_enter` calls between ready and SIGTERM. Each contains two total enter calls, consistent with bootstrap and shutdown.
- Module strict traces contain zero userspace accept/receive/send calls after ready.
- Native strict traces contain substantial `accept4`, `recvfrom`, and `sendmsg` activity. Logs report `epoll_pwait2 timeout_ns=60000`; the baseline did not silently fall back to a broken or inactive path.

All transports use the same pinned checkpoint, FP16 computation, graph captures, packed prefill, FIFO-prefix model release, KV layout/budget, prompt allocation, client, output count, and wire protocol. Each records the same 520 captured graph configurations. All performance executors reach `max_active=8`, admit/retire 264 requests, have zero graph errors, and retain the same two-device-launch dispatch policy.

The native baseline is a credible efficient alternative mechanism for this question. Its successful full strict and timing coverage provides no evidence of an avoidable interface failure. Its existing 60 µs wait and stock SQPOLL defaults represent different measured cost/latency choices; they were not retuned during collection.

Identical model arithmetic does not mean identical total GPU resources. Stock adds a resident GPU network-control block, queue scanning, and different submission/completion/final-send ordering. Results are comparisons of these complete implementations, not an isolated causal estimate for eliminating syscalls or replacing module polling.

**Additional reporting limitation:** disabling `BF_TRACE` removes model admission/compute/release tracing. Stock still unconditionally records its first 128 `IoRecord` entries and maintains diagnostic counters. These are part of the measured implementation. Calling these runs “ordinary BF_TRACE-off” is accurate; calling them free of all tracing/instrumentation is inaccurate.

## Queue and terminal state

All 36 model executors finish with admitted=retired=264 and graph_error=trace_overflows=0.

For every stock performance executor:

- head=completed=received=264;
- accepted=closed=19;
- sends=8328;
- aborted=pending=error=reserved=SQ-dropped=CQ-overflow=0;
- SQ head/tail and CQ head/tail are equal;
- diagnostic trace_count=264 and trace_overflow=136.

The diagnostic overflow means entries beyond the 128-record diagnostic buffer are not retained; it does not indicate missing served requests.

Both stock and module page snapshots have `llm_head=264`, `llm_reserved=0`, all eight slots FREE, and zero recorded admission drops. Stock BPF snapshots show 264 stream publishes and 264 recycles. Native publishes/completes 264 with zero rejections in timing runs. Raw stdout and the embedded executor stdout agree.

These checks establish the measured run’s delivery and terminal ownership state. They do not establish all future socket lifecycles or arbitrary continuous loads.

## Independently reconstructed primary results

TTFT is client send-start to arrival of the first complete token. Throughput is delivered tokens divided by the interval from earliest measured request start to latest final-token arrival in each cell. Connections and initialization are outside those intervals.

Primary differences favor stock when positive:

- TTFT: native minus stock, milliseconds.
- Throughput: stock minus native, tokens/s.

| Model | gen1/c1 mean TTFT, stock / native | TTFT difference, nominal paired t95 | gen64/c8 throughput, stock / native | Throughput difference, nominal paired t95 |
|---|---:|---:|---:|---:|
| Qwen2.5-0.5B | 1.406185 / 1.365673 ms | −0.040512 [−0.109705, +0.028680] ms | 4547.288 / 4702.741 token/s | −155.453 [−289.450, −21.457] token/s |
| SmolLM2-135M | 1.085011 / 1.166208 ms | +0.081197 [−0.025390, +0.187784] ms | 5374.508 / 5444.231 token/s | −69.723 [−344.364, +204.919] token/s |

Qwen stock throughput is lower in all six paired blocks. Its nominal interval excludes zero. Both TTFT intervals and Smol’s throughput interval include zero. No primary provides a reliable stock advantage.

The intervals use six paired process blocks, sample standard deviation, `t(0.975,5)=2.570581835636305`, and division by `sqrt(6)`. Requests are not treated as independent replicates. Four primary intervals are reported without a familywise-significance claim. Zero-containing intervals establish neither equality nor equivalence.

The retained component-control comparisons also provide no clear stock benefit:

| Model | Module TTFT gen1/c1 | Module throughput gen64/c8 | Module-minus-stock TTFT t95 | Stock-minus-module throughput t95 |
|---|---:|---:|---:|---:|
| Qwen | 1.396491 ms | 4675.092 token/s | −0.009694 [−0.110984, +0.091597] ms | −127.805 [−297.915, +42.306] token/s |
| Smol | 1.142984 ms | 5438.513 token/s | +0.057973 [−0.023783, +0.139728] ms | −64.005 [−407.785, +279.775] token/s |

These remain component comparisons, not an extra headline baseline.

## CPU reconstruction and interpretation

I recomputed every cell’s process-clock difference and module-TX difference directly from the raw before/after readings. All are nonnegative and agree with stored sums. Sampling brackets contain the earliest request start and latest arrival. Connections exist before the initial sample; client close and work before the final sample can fall inside the bracket.

The POSIX process clock includes all executor threads. Stock task snapshots place SQPOLL inside that group, so it is counted once. Module TX is a separate kernel task, measured by its adjusted user+system counter and added separately.

Mean known-worker CPU during gen64/c8 brackets, divided by 64 requests:

| Model / transport | Executor process CPU | Module TX CPU | Known-worker sum |
|---|---:|---:|---:|
| Qwen stock | 14.212284 ms/request | 0 | 14.212284 ms/request |
| Qwen native | 0.442915 | 0 | 0.442915 |
| Qwen module | 0.101057 | 0.228078 | 0.329135 |
| Smol stock | 12.040271 | 0 | 12.040271 |
| Smol native | 0.394414 | 0 | 0.394414 |
| Smol module | 0.088545 | 0.210233 | 0.298778 |

Stock’s **added** known-worker CPU relative to native is:

- Qwen: **13.769369 ms/request**, nominal paired t95 **[13.402130, 14.136608]**.
- Smol: **11.645856 ms/request**, nominal paired t95 **[11.185172, 12.106541]**.

Stock’s process-clock CPU divided by sampled wall time is approximately **1.007–1.009 CPU-seconds/second** in every gen64/c8 block. This is consistent with roughly one active CPU core, including other executor threads. The data do not attribute every CPU tick specifically to SQPOLL.

This scope omits the client, RX/softirq/BPF execution, and TCP work outside the measured thread groups. It is not total service CPU, energy, or pure per-request inference CPU. Nevertheless, the measured known-worker cost clearly rises; absence of userspace network syscalls is not evidence of eliminating CPU work.

## Anomalies, exclusions, and competing explanations

No measured sample, executor, or process block is excluded.

Smol block 1 reverses the TTFT direction and has an approximately −549 token/s stock/native throughput difference. Blocks 2 and 3 contain lower native throughput, while block 4 contains lower module throughput. These remain in the statistics. Qwen stock/native throughput differences range from approximately −336 to −51 token/s, all negative.

Balanced transport orders reduce simple position confounding, but six sequential blocks on a shared host cannot eliminate temporal, scheduling, GPU-clock, batching, or contention effects. Cell rotation is prespecified, not post hoc. No recorded continuous utilization trace identifies the cause of individual shifts.

The host journal reports no matches for its specified fault patterns over the declared UTC window. The original boot ID, Workspace UID/Ready state, zero restarts, base packages, and original Coder PIDs are retained. The after-run receipt and my live process read find no serving process; the receipt also reports no module, BPF pins, or GPU application. These are endpoint/fault checks, not proof of continuous isolation or absence of all interference.

Possible explanations for stock’s throughput loss include GPU network-control resource cost, mapped-memory scanning, final-response ordering, and actual batch scheduling. This experiment does not distinguish them. The approximately one-core CPU cost is a measured tradeoff, not proof that CPU contention causes the GPU throughput change.

## Allowed conclusion and next decision

The experiment validly adds local evidence for the complete stock implementation on two pinned small models and four fixed workload cells. It demonstrates delivery with the disclosed finite-set check and an engaged module-free path without a steady userspace socket worker. It does **not** demonstrate a reliable latency/throughput advantage, and it records substantially greater known-worker CPU consumption.

The next decision should follow that evidence: preserve and document the stock implementation’s portability option, report all four primary intervals and the CPU tradeoff, and avoid a speedup or CPU-elimination claim. Further optimization is worthwhile only through a new discriminator that tests a specific suspected cost, or through the separately retained cross-node question. The current result does not justify another unchanged run, additional weak baselines, or model-specific arithmetic work as a way to obtain a favorable transport result.

No result-invalidating defect was found in the reviewed matrix. Final owned-runtime/build cleanup and publication should be recorded separately before claiming the experiment’s operational closure.
