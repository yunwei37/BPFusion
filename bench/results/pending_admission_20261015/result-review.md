# Pending-admission experiment: independent result review

Reviewer: `/root/pending_admission_result_review`  
Archive: `/workspaces/repository/bench/results/pending_admission_20261015`  
Reviewed main revision: `8044ab317f1212db31f77443afae58c2f33634d3`

```text
run status: valid
tested hypothesis: inconclusive for the predeclared performance superiority;
                   supported for finite-workload admission correctness
research value: supporting
paper impact: mechanism or workload boundary
next paper decision: retain the admission-repair evidence and mixed matched
                     performance results; do not claim general superiority,
                     equivalence, complete backpressure, or completed delivery
```

The completed experiment provides credible evidence that the candidate eliminates observed admission losses on this finite workload while preserving the real-model serving path. Neither model establishes the predeclared first-token P99 advantage at 64 requests/s. Qwen has a substantial secondary tail advantage at 96 requests/s, accompanied by worse median latency and higher executor process CPU. Delivered-throughput differences remain inconclusive.

There is no formal paper RQ or thesis contract to challenge. These results bound an implementation and workload, and do not resolve the entire retained user objective.

## Review method and independence

I read the plan, all three plan-review discussions, implementation notes, setup/build commands and failure receipts, actual candidate/native/original snapshots and diffs, qualification and lifecycle sources/results, raw performance data and sidecars, and host observations.

All inspection and recomputation occurred in the original Workspace. I ran no GPU workload and modified no experiment source, oracle, raw data, metric, or paper.

I independently:

- Replayed all seven archived CPU analyses; every invocation exited zero and reproduced its saved stdout byte for byte.
- Recomputed request timing, linear percentiles, cell throughput, process CPU deltas, paired differences, and nominal paired t95 intervals directly from raw records.
- Checked every full-run saved token against its reference and reconstructed GPU admission, compute history, physical ownership, and FIFO release.
- Regenerated all 64 full/preflight arrival schedules using the retained runtime’s NumPy 2.3.5 and recorded seeds; every schedule matched exactly.
- Rechecked lifecycle complete/prefix classifications and observed bytes against the unchanged frozen reference sets.
- Obtained CPU-only Clang record layouts for all three page headers.
- Compared archived source snapshots with the still-present private runtime sources.

This CPU inspection verifies the saved numerical evidence and the implementation of the original GPU replay. It is not a second independent GPU numerical execution.

## Completion and deviations

The run is complete, rather than a favorable prefix:

| Stage | Completion |
|---|---|
| Qualification | 10/10 commands, exit 0, terminal `10:24:36.373252 UTC` |
| Real preflight | Attempt 1, exit 0, terminal `10:27:15.998038 UTC` |
| Full comparison | Both model drivers and analyses exit 0 |
| Full wrapper | Exit 0, terminal `11:21:07.991049 UTC` |

The full run began at `10:31:56.293859 UTC`. Each model has ten executors and thirty cells. The combined measurement contains **15,360 attempts, 15,360 complete successes, zero failures, and 983,040 delivered output tokens**, plus 160 checked gen1 warmups. Each model/path/rate contains 1,280 measured attempts. All twenty recorded executor PIDs are now absent from `/proc`, consistent with their successful terminal records.

The initial failures remain available and were not hidden as exclusions:

1. An initial snapshot edit stopped on a whitespace mismatch before the BPF edit/build.
2. Initial kernel/native builds succeeded, but the module build failed because `/lib/modules/<running-kernel>/build` was absent. The private rebuild used the existing `/usr/src/linux-headers-7.3.0-070300rc3-generic` through the supported `KDIR` override. It succeeded without a host configuration change.
3. The initial synthetic module fixture attempted to receive the final token while retaining `PENDING`; the existing module deliberately withholds that token until `DONE`. The timeout was therefore a fixture sequence defect. Cleanup also encountered missing `rmmod`.
4. The repaired fixture checks the exact pre-DONE `n−1` prefix, retains the PENDING assertion, then publishes DONE and checks the full exact response and recycle. The original five-second timeout, token oracle, 24 complete replies, two resets, and 26 cycles remain. Direct `delete_module` cleanup replaces the unavailable command. Initial failure and explicit cleanup receipts are retained.

These changes repair a compatibility dependency before model qualification/preflight; they do not weaken the real-model oracle or replace measured cells. All affected qualification ran again from the start.

The later root `tests/kernel_tx.py` synchronization has the same assertions and cleanup as the passing private-bound fixture. Its normal loader/module bindings were restored; the root default invocation was not separately run during this experiment. That limitation is correctly recorded.

The kernel build retains userspace-header warnings. The repaired module build retains compiler-package/pahole differences and unavailable-vmlinux BTF generation. Successful module load and live compatibility tests provide the relevant execution evidence; the warnings should remain reproducibility information.

## Source binding, identical computation, and page compatibility

The archived candidate, native, original, and diff files are byte-equal to their retained private counterparts.

The actual build logs bind BPF, loader, and CUDA compilation to the private sources. Both measured variants compile with:

- `-O3`, C++17, `sm_120`;
- `BF_TRACE`;
- packed prefill and FIFO prefix release;
- eight model banks and the same page header.

The expected network-specific macros differ. The measured native CUDA source differs from the candidate only in its userspace shutdown interrupt. The model computation is unchanged. Native model/network source also matches the earlier offered-load native source; its copied build paths and page header were updated.

The launchers are symlinks to `/workspaces/repository/executor/vllm_graph.py`, which remains byte-equal to the archived Python backend and the backend embedded in both full raw metadata records. The Python entrypoint resolves the adjacent private `.so`, so it does not accidentally select the ordinary root build.

The runtime pins vLLM 0.31.0, Torch 2.13.0+cu129, Transformers 5.17.0, and NumPy 2.3.5. Both paths use the same retained Qwen and Smol checkpoint revisions, FP16 graphs, KV setup, prompts, and output lengths.

CPU Clang layout inspection confirms:

| Field | Original | Candidate/native |
|---|---:|---:|
| `llm_admission` offset | 12,848 | 12,848 |
| `llm[]` offset | 12,856 | 12,856 |
| Model slot size | 560 | 560 |
| Page size | 17,336 | 17,344 |
| `llm_queued` offset | absent | 17,336 |

The eight tail bytes do not move existing fields. The page still rounds to 20,480 mapped bytes. The module checks exact `value_size == sizeof(*page)`, making its private rebuild necessary. Its implementation remains byte-equal to the root module; the fixture demonstrates rejection of an incompatible genuine map and successful use of the enlarged page.

The eight preserved root setup/build file stat records still match live state. This is preservation evidence, not certification of eventual cleanup.

## Queue, ownership, wakeup, EOF, and stop

The intended mechanism engaged.

The loader discovers `somaxconn=4096`, applies that capacity to the pending queue, and pins it. The kernel loop reuses the exact `ctl` and `pending` map FDs. Only loop bootstrap sets the existing owner word to enable queued admission; the non-loop compatibility path remains direct admission.

Producers increment the pending count before queue publication, roll it back on push failure, and do not use overwrite semantics. The single loop consumer performs peek → CPU atomic model-slot reservation → pop → publish → decrement. Final-send/abort completion retains the existing CPU reservation-release owner. The GPU does not perform host CAS.

The admission acknowledgment extends the existing CQ/timer handshake: newly admitted work prevents a kernel sleep until GPU I/O progress has observed it and can publish the needed timer/SQ updates. GPU system-scope acquire/release operations and system fences remain present.

EOF/dead connection recycling now also waits for the global queued count to clear during normal operation. This conservatively retains unrelated dead connections while any backlog exists; it is not per-peer queue cancellation. The qualified half-close and backlog reset cases exercise the resulting path.

Preflight measured a queue peak of 16, with final queue/reservations zero. Full-run executor-wide peaks were:

- Qwen: **29, 31, 33, 16, 21**.
- Smol: **13, 7, 7, 5, 16**.

These are whole-executor peaks, not per-rate measurements. The explicit lifecycle receipts establish queued work beyond the eight physical model slots: 16 queued before backlog RST and 56 queued before stop for each model.

This is **finite FIFO admission buffering**. A full pending map still causes a drop; transport redirect/receive behavior does not constitute complete TCP backpressure. The test did not approach the 4,096-entry queue limit or establish arbitrary-overload reliability. Passing finite tests also does not prove every weak-ordering interleaving.

## Correctness and baseline engagement

The real-model qualification comprises six traced executors:

- Loop/native: 640 requests and 23,376 checked model tokens per executor.
- Non-loop compatibility: 622 requests and 22,224 checked tokens per executor.
- Combined: **3,804 protocol outcomes and 137,952 checked model tokens**.

These counts include deliberate invalid-request rejection cases; they are not all successful inference responses. Qualification covers byte fragmentation, concurrency 1–8, wrap/reuse, mixed gen1/gen64, invalid vocabulary, pipelining, half-close, binary/HTTP handling, and helper-thread shutdown. The main loop/native half-close pipeline has 24 requests; compatibility retains six.

Actual post-ready strace evidence shows zero userspace `accept4`, `recvfrom`, or `sendmsg` calls in the loop protocol executors. Native exhibits all three. The loop enters the kernel loop through `io_uring_enter`; task evidence excludes an SQPOLL thread in that mode. This supports the claimed absence of a steady userspace request worker on the qualified path, while acknowledging bootstrap, kernel execution, GPU I/O orchestration, and teardown.

Native is an engaged, credible same-compute competitor. It uses event-driven epoll readiness, deadline sleep when idle, eventfd shutdown wakeup, and its existing active completion wait. The idle deadline and helper-thread signal traces demonstrate those mechanisms rather than an inadvertently spinning or uninterruptibly sleeping baseline. No native request fails in the full comparison.

The comparison still includes different network admission/scheduling policies. Native traverses buffered peers and the candidate uses a FIFO pending queue. The Qwen tail result cannot isolate syscall removal from scheduling, buffering, GPU batch trajectories, timer behavior, and shared CPU contention.

### Numerical replay substance

The backend replay is substantive rather than reference-file membership alone:

- It reconstructs request prompts, validity, physical bank ownership, and generated history.
- It rebuilds padded prefill/decode inputs, positions, sequence lengths, block tables, slot mappings, and padding.
- It executes retained upstream body/head graphs and compares each sampled output against the traced token.
- History advances using the independently replayed output after equality.
- It checks FIFO releases and physical reuse through completion.

Every full executor reports 776 replayed requests and 49,160 checked tokens. Across twenty executors this is **15,520 request histories and 983,200 tokens**, including warmups. All full saved admissions, compute tokens, references, and client bytes agree; every model history has its requested length. Observed batches span 1–8; full prefill queries are 2/5/8, with query zero representing decode.

The replay shares the upstream model graphs and intentionally follows the observed batching trajectory. It validates native dispatch/KV/history/wire fidelity for that trajectory; it is not an independent model implementation, a task-quality evaluation, or numerical validation across other models/architectures.

### Lifecycle classifications

Independent byte/reference checks reproduce:

| Model/path | Complete valid responses checked | Explicit partial rows | Invalid outcomes | Unobserved canceled rows | Checked tokens |
|---|---:|---:|---:|---:|---:|
| Qwen loop | 21 | 66 | 10 | 23 | 852 |
| Smol loop | 21 | 66 | 10 | 23 | 1,044 |
| Qwen native | 20 | 2 | 10 | 0 | 652 |
| Smol native | 20 | 2 | 10 | 0 | 652 |

The loop’s 120 actions are not 120 complete numerical responses. Before stop, head=64 and queued=56; final physical reservations clear and 78/78 connections close. The 56 unadmitted requests remain explicit shutdown cancellations until owned map destruction. The 23 unobserved reset responses cannot be numerically certified. Stop observations include empty and partial wire prefixes checked against frozen complete outputs.

Native retains 32 actions, 31 internal completions, and two deliberately partial checks. Internal completion counters must not substitute for complete client-observed responses. I also checked the retained native post-stop extra bytes against the frozen allowed prefix.

### Two different overflow counters

Every full loop executor reports `trace_count=776` and diagnostic reply `trace_overflow=648`: its fixed 128-entry reply-detail array is full. Source inspection confirms that meaning.

The actual GPU numerical-history trace separately reports **zero overflows**, has complete records, and supports every saved request/reference. SQ/CQ drop and overflow counters are also zero. Calling the diagnostic reply overflow a lost GPU correctness trace would be incorrect; calling the reply diagnostic array complete would also be incorrect.

## Recomputed matched results

The following are arithmetic means of the **five per-block statistics**, not pooled request percentiles. Every row has 0/1,280 failed attempts. TTFT starts at connection begin; completion ends at the last token. CPU is executor process CPU per attempted request.

| Model | Rate/s | Path | TTFT P95 ms | TTFT P99 ms | Completion P95 ms | Completion P99 ms | Requests/s | Tokens/s | CPU ms/attempt |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen | 4 | Kernel | 8.162 | 13.440 | 88.340 | 95.421 | 3.995 | 255.658 | 3.452 |
| Qwen | 4 | Native | 5.170 | 8.253 | 84.582 | 87.558 | 3.995 | 255.675 | 3.195 |
| Qwen | 64 | Kernel | 35.929 | 51.446 | 121.749 | 138.477 | 62.632 | 4,008.457 | 0.934 |
| Qwen | 64 | Native | 31.029 | 65.621 | 114.541 | 150.994 | 62.699 | 4,012.723 | 0.693 |
| Qwen | 96 | Kernel | 254.557 | 280.139 | 337.189 | 362.191 | 86.669 | 5,546.843 | 1.032 |
| Qwen | 96 | Native | 680.460 | 1,418.437 | 765.908 | 1,503.890 | 87.679 | 5,611.480 | 0.590 |
| Smol | 4 | Kernel | 9.063 | 14.067 | 72.874 | 77.708 | 3.997 | 255.789 | 2.808 |
| Smol | 4 | Native | 4.782 | 8.481 | 70.195 | 73.627 | 3.997 | 255.795 | 2.637 |
| Smol | 64 | Kernel | 34.132 | 47.667 | 103.404 | 128.913 | 62.990 | 4,031.369 | 0.817 |
| Smol | 64 | Native | 10.076 | 22.275 | 75.900 | 86.961 | 63.052 | 4,035.325 | 0.599 |
| Smol | 96 | Kernel | 52.541 | 65.889 | 120.183 | 132.182 | 93.584 | 5,989.351 | 0.772 |
| Smol | 96 | Native | 67.297 | 145.327 | 135.702 | 212.338 | 93.209 | 5,965.383 | 0.565 |

All primary and secondary directions below are **kernel minus native**.

### Predeclared primary: 64 requests/s connect-inclusive TTFT P99

| Model | Five paired effects, ms | Mean, ms | Nominal paired t95, df4 |
|---|---|---:|---|
| Qwen | −68.996647, +12.211456, −9.202988, +4.310305, −9.199895 | −14.175554 | [−53.893458, +25.542351] |
| Smol | −2.887203, +18.447024, +5.836504, +2.070687, +103.491470 | +25.391696 | [−29.697391, +80.480783] |

There is no failed-request censoring in either primary comparison. Both intervals cross zero. The planned superiority claim is **inconclusive**, and neither interval establishes equivalence.

### Secondary effects and adverse results

| Model/rate | TTFT P99 difference, ms [t95] | Output tokens/s difference [t95] |
|---|---|---|
| Qwen/4 | +5.187 [−0.204, +10.577] | −0.017 [−0.049, +0.016] |
| Qwen/96 | **−1,138.298 [−1,647.711, −628.885]** | −64.638 [−247.344, +118.069] |
| Smol/4 | **+5.586 [+2.538, +8.634]** | −0.007 [−0.018, +0.005] |
| Smol/96 | −79.438 [−175.748, +16.872] | +23.968 [−56.394, +104.330] |

At Qwen/96, all five paired P99 effects favor the candidate, and scheduled-origin TTFT gives a similar result: −1,138.436 ms [−1,647.705, −629.167]. Completion P99 is −1,141.698 ms [−1,651.797, −631.600].

This secondary tail improvement has a tradeoff: Qwen/96 mean block-median TTFT is **134.386 ms kernel versus 30.120 ms native**, and median completion is 220.757 versus 116.754 ms. The candidate distributes waiting differently; the result is not a uniform latency improvement.

At 4 requests/s, Smol’s tail is worse on the candidate. Completion P99 differences are adverse for both models: Qwen +7.863 ms [+0.887, +14.839], Smol +4.081 ms [+0.817, +7.345].

Executor process CPU is higher in all four 64/96-rate comparisons:

| Model/rate | CPU difference ms/attempt [t95] |
|---|---|
| Qwen/64 | +0.241695 [+0.161519, +0.321871] |
| Qwen/96 | +0.441910 [+0.356092, +0.527729] |
| Smol/64 | +0.218247 [+0.130915, +0.305580] |
| Smol/96 | +0.206631 [+0.047593, +0.365669] |

These are partial process measurements, not total service CPU or energy.

P50, scheduled-origin completion, and TPOT recomputations also match the saved analyses. For example, mean block-median TPOT at 64 requests/s is 1.368/1.343 ms for Qwen kernel/native and 1.077/1.040 ms for Smol. This does not establish a model-compute acceleration.

## Metric validity, scheduling, and uncertainty

The source uses independent request threads released against absolute due times, without a completion-driven cap. Matching path schedules are identical within each pair, path order alternates, and rate order rotates. The retained vLLM implementation confirms gamma arrival generation and NumPy percentile conventions; the adapter’s recorded normalization is reproducible.

Timing checks establish monotonic request ordering and exact timestamp-derived formulas for TTFT, completion, scheduled-origin timing, and TPOT. Multiple tokens received together share an arrival timestamp, as documented.

Throughput includes the full scheduled cell window and final drain, rather than only the successful response interval. With no failures, every attempted output token contributes. The 96-rate throughput below offered load includes drain time and is not a steady-state capacity estimate.

Scheduling lag materially limits interpretation:

- Qwen maximum individual scheduling lag: **22.540 ms**.
- Smol maximum: **245.824 ms**.
- Smol kernel/64 block P99 lag ranges from **4.082 to 218.468 ms**; native ranges from 4.845 to 6.465 ms.
- Smol kernel pair4 is the large adverse primary block. Its scheduled-origin P99 difference is +210.813 ms, versus +103.491 ms from connection begin.

Keeping this outlier and both timing origins is essential. Shared-host/client scheduling is a competing explanation; it does not justify deletion.

The uncertainty calculation uses five paired process blocks and the planned t multiplier 2.776445105. These are nominal intervals with five observations, sequential execution, and no multiplicity correction for secondary exploration. The blocks do not establish independent stationary environments. A 256-request cell has only a few observations determining P99; P99.9 or precise rare-event reliability is unsupported.

The earlier offered-load archive independently contains 453 Qwen and 256 Smol kernel failures—709/10,240 kernel attempts—and zero native failures. Its matrix includes an additional rate, and hosting conditions differ. It is useful prior failure evidence, not a concurrently matched old-versus-new effect estimate. The old failure was encountering the reserved **next physical slot**, which does not imply simultaneous occupancy of all eight slots.

## Host and CPU evidence

This is a heavily occupied shared-host comparison.

The `10:29:41.106648 UTC` pre-full CPU observation spans approximately 1.280 seconds and records about 21 sampled process CPU cores on the 24-core host. The prominent `repl` processes belong to the other cgroup identified in the retained ownership receipt as `gpu-smt-dev`. No such processes were changed.

Global `/proc/stat` deltas during measured cells are approximately 24 work cores. Some short-window estimates slightly exceed 24 because the host-counter sampling brackets differ from the denominator window. These figures describe aggregate host work, including clients and other workloads; they do not attribute that work to BPFusion.

Executor CPU uses process-clock differences with retained sample brackets. Maximum before-sample read spans are about 17.880 ms for Qwen and 7.953 ms for Smol; after-sample spans are below 0.157 ms. These are approximate cell-bracketing measurements, not exact isolation of every service task. Kernel/softirq/io-wq costs outside the executor process and energy remain unmeasured.

The host sample timing is correctly constrained:

- `host_before`: `09:41:28.537957 UTC`, before qualification.
- `host_before_full`: `10:28:31.376116 UTC`, before full; no GPU compute application observed.
- `host_full_observation1`: `10:34:13.199385 UTC`, after Qwen pair0 kernel measured cells ended.
- `host_full_observation2`: `10:41:28.840579 UTC`, after Qwen pair1 kernel measured cells ended.
- The latter two are replay/teardown observations, not serving-isolation evidence.
- Qwen’s 152.948 ms short sample lies entirely inside pair2 kernel/rate4 measurement. GPU host PID 3,824,400 maps to executor namespace PID 565,549.
- Smol’s 130.661 ms short sample lies entirely inside pair1 native/rate4 measurement. Host PID 3,920,928 maps to namespace PID 573,750.
- `host_after`: `11:22:26.758652 UTC`, **78.767603 seconds after full terminal**; no GPU compute application observed.

The sampled boot ID and 56 selected historical fault lines remain unchanged. This supports only those sparse observations and that selected fault filter. It does not establish continuous GPU exclusivity, CPU isolation, absence of every host fault, or service-level power consumption.

## Result interpretation and next decision

The admitted experiment adds **supporting research evidence**, beyond setup or packaging: finite offered-load admissions now complete with exact saved model/wire correctness; the strongest same-compute native competitor completes too; and the matched data exposes both a conditional high-load tail improvement and meaningful costs.

The supported statement is:

> On the tested shared host, both models completed every measured request through the finite pending-admission candidate with saved trajectory-matched numerical correctness. The predeclared 64 requests/s TTFT-P99 comparisons remained inconclusive. Qwen showed a secondary tail improvement at 96 requests/s, alongside worse median latency, higher executor process CPU, and no established throughput advantage.

The following claims are unsupported:

- General latency/throughput or CPU superiority.
- Equivalence at the primary rate.
- Complete TCP backpressure or arbitrary-overload reliability.
- Universal numerical/model/compiler correctness.
- Exclusive-host performance or energy savings.
- Completion of production selection, final cleanup, publication, or the entire user objective.

Return this completed run and its bounded interpretation to the root agent. No repair or repeated result-review loop is necessary to make these measurements valid. Any later implementation selection must preserve the finite-queue boundary and the unfavorable results. This review does **not** certify that later selection, cleanup/restoration, OSS documentation integration, or publication has occurred.

<oai-mem-citation>
<citation_entries>
MEMORY.md:55-56|note=[existing Workspace and kernel TCP evidence boundaries refreshed against current artifacts]
</citation_entries>
<rollout_ids>
01a11853-1771-7462-876c-29de77fd8c21
</rollout_ids>
</oai-mem-citation>
