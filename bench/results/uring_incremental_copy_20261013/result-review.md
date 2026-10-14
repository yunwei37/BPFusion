The completed comparison is **valid for the declared local ordinary-serving and frozen complete-sequence fidelity contract**. It does **not establish an incremental-copy throughput improvement**, a native-transport advantage, or equivalence. All four predeclared throughput intervals include zero. The experiment adds useful supporting evidence about this implementation; its qualification and repair work remains dependency evidence.

| Required judgment | Result |
|---|---|
| Run status | **Valid and complete**, within the declared finite-set contract |
| Tested hypothesis | **Inconclusive** |
| Research value | **Supporting** |
| Paper impact | **Mechanism or workload boundary** |
| Next paper decision | Close this completed copy comparison; do not promote incremental copying into a demonstrated performance gain or infer that it explains historical0042. Prioritize a different measured transport cost if continuing. |

The retained question remains finding0035’s local question: “what client latency/throughput does the ordinary packed/prefix adapter deliver against the efficient native network alternative after BF_TRACE is removed?” There is no formal paper RQ or external SOTA comparison to revise. This result neither completes the full project objective nor challenges a necessary central thesis prediction.

**Independent reconstruction and completion.** I read the approved plan, qualification history, commands, pipeline, source snapshots/diff, serving/client/analysis source, raw timing data, executor receipts, relevant qualification raws and HF lifecycle results. I reran `python3 bench/vllm_serving_analysis.py RAW` for both complete timing files and independently reconstructed throughput and CPU arithmetic directly from request timestamps and clock brackets. Both reanalyses exit zero and reproduce the archived analysis stdout byte-for-byte. Timing driver and analysis stderr files are empty.

Each model contains 18 distinct executor starts, 18 measured cells, 18 normal executor exits, 18 verified records and 18 successful executor-terminal records, followed by terminal exit zero. There are no timing failure records. Each executor has 256 measured gen64 requests and eight checked gen1 warmups:

- Both models together: **36 executors/cells, 9,216 measured requests and 589,824 measured output tokens**.
- Excluded from timing: **288 checked gen1 warmup requests/tokens**.
- No missing, excluded, replaced or retried timing cell was found.

All six permutations occur exactly once per model, in the specified order:

1. incremental, full-copy, native
2. incremental, native, full-copy
3. full-copy, incremental, native
4. full-copy, native, incremental
5. native, incremental, full-copy
6. native, full-copy, incremental

Qwen’s raw interval is 2026-10-13 **08:02:30–08:11:53 UTC**; Smol’s is **08:11:58–08:20:05 UTC**. Each condition has 1,536 measured requests/model. The six paired process blocks—not the pooled individual requests—are the inference units.

**Source freeze and comparison fairness.** Both timing metadata records identify main commit `0330145710dc66de66dbb0864f4133ee345b86d8`. During review, the checkout remains on `main` at that revision. Every file in `source_snapshot.json` equals the current file; embedded timing driver/client/native source also agrees with the inspected source. The archived pinned runtime is vLLM 0.31.0, Torch 2.13.0+cu129 and Transformers 5.17.0.

The incremental and full-copy targets compile the same stock implementation, packed prefill and prefix release. `BF_IO_FULL_COPY` changes the output-loop start to zero; the candidate starts at the floor of the completed unsent body-byte offset. The shared header leaves header construction, send offset/length/flags, receive handling, busy-buffer ownership and final ordering common. The recorded ordinary model-dispatch SASS is byte-identical between the two stock conditions.

The common **EAGAIN/EINTR receive repair** and **same-socket ingress redirect** precede all timing and apply identically to candidate/full-copy. They therefore do not confound this matched copy intervention. They do change the interpretation of the control: full-copy is a **repaired implementation restoring the former copy loop**, not the unmodified historical0042 implementation.

The native condition engages its intended userspace TCP path, completes all assigned requests and exits normally. It is a credible same-compute alternative for the retained local question, not an official external vLLM server or SOTA stack. Its success is not inferred from a wrapper exit. Neither baseline/control experienced an interface failure in the final timed comparison.

**Mechanism engagement and byte boundary.** The candidate preserves a partly transmitted token through floor division and recopies it; fully transmitted tokens are skipped. `r.busy` prevents modifying a buffer while its send remains outstanding. This is a coherent source-level byte argument.

For each model/stock condition, the archived first-128-per-executor diagnostics contain 720 measured gen64 reply records. Every such record has **64 sends, 63 early sends and 336 delivered bytes**. Thus the measured workload exercises repeated prefix delivery; this is not an inactive-copy ablation. All stock terminal counters show completed264, aborted0, pending0, error0, reserved0, dropped0 and ring overflow0, with balanced SQ/CQ heads and tails.

The stock diagnostic `trace_overflow=136` is the expected overflow of the fixed first128 `IoRecord` capacity after264 requests. It is separate from model `trace_overflows=0` and ring `overflow=0`. It limits per-request diagnostic coverage; it does not indicate a lost measured response.

There is no direct measurement of copied bytes, memory traffic or per-copy execution time. The send records do not establish actual short-send stress or permit a measured “32.5× fewer copies” claim. The complete end-to-end intervention is tested; its internal hardware cost is not isolated.

**Primary numbers.** Throughput reconstructs as **16,384 output tokens divided by the interval from the first measured send to the last complete-token arrival** for each cell. The displayed condition means are arithmetic means of six cell rates, not one pooled rate. The intervals are nominal two-sided paired t95 with df5 and the predeclared critical value.

| Model | Incremental token/s | Full-copy token/s | Native token/s |
|---|---:|---:|---:|
| Qwen | 4,534.005144 | 4,489.431207 | 4,507.866830 |
| Smol | 5,221.026420 | 5,273.257856 | 5,116.563478 |

| Model | Candidate-minus-comparator primary | Mean token/s | Nominal paired t95 |
|---|---|---:|---|
| Qwen | Incremental − full-copy | +44.573938 | [−28.962858, +118.110733] |
| Qwen | Incremental − native | +26.138314 | [−46.980792, +99.257420] |
| Smol | Incremental − full-copy | −52.231436 | [−185.829930, +81.367058] |
| Smol | Incremental − native | +104.462942 | [−198.996499, +407.922382] |

All four intervals cross zero. The Qwen positive mean and Smol negative mean against full-copy are both inconclusive under the fixed interpretation rule. The experiment does not establish a benefit, harm, negligible effect, equivalence or familywide superiority.

The six differences, retained in order and without dropping outliers, are:

| Model/comparator | Paired candidate-minus-comparator token/s |
|---|---|
| Qwen/full-copy | 184.523134, 2.543606, −0.787425, 38.006954, 17.092465, 26.064892 |
| Qwen/native | −89.019874, 12.509204, 126.500483, 37.036136, 50.405559, 19.398377 |
| Smol/full-copy | 21.136606, −296.132888, 20.041722, −6.962176, 35.441663, −86.913543 |
| Smol/native | 310.331300, −398.765840, −72.853802, 296.720384, 329.859199, 161.486408 |

Qwen’s first full-copy cell is substantially slower than its subsequent cells; Smol exhibits substantially larger process-block variability. These observations remain in the estimate. The evidence does not identify their cause. Balanced order helps with position effects but is not randomized isolation or proof of independence/stationarity.

**Secondary delivery and CPU.** TTFT is first complete-token client arrival minus send start; completion is last arrival minus start; TPOT is first-to-last arrival divided by63. Recomputed values agree with raw records. TCP/client coalescing is included.

| Model/condition | TTFT ms | Completion ms | TPOT ms | Known-worker CPU ms/request |
|---|---:|---:|---:|---:|
| Qwen/incremental | 2.075738 | 112.816888 | 1.757796 | 14.224701 |
| Qwen/full-copy | 2.148417 | 113.969680 | 1.774941 | 14.372412 |
| Qwen/native | 2.159118 | 113.547133 | 1.768064 | 0.536699 |
| Smol/incremental | 1.686342 | 98.020647 | 1.529116 | 12.367607 |
| Smol/full-copy | 1.637846 | 96.787382 | 1.510310 | 12.232235 |
| Smol/native | 1.782708 | 100.133219 | 1.561119 | 0.412901 |

All inspected paired TTFT, completion and TPOT intervals also include zero. They provide no independent delivery win that changes the primary verdict.

The CPU calculation uses the executor’s POSIX process CPU clock. Raw `/proc/<pid>/task` records contain exactly one `iou-sqp-*` task for every stock executor and none for native. The all-thread clock therefore covers the observed executor thread group; adding SQPOLL again would double count. Every CPU snapshot bracket encloses the measured arrival window, and the recorded deltas agree with subtraction of the raw clocks. No module TX clock is added in this matrix.

Incremental/native known-worker CPU ratios are **26.504× for Qwen** and **29.953× for Smol**. Relative to the delivery window, both stock variants consume approximately **1.008 known-worker CPU cores**; native consumes approximately **0.038 Qwen / 0.033 Smol cores**. The native-minus-incremental CPU saving estimates are negative with intervals wholly below zero: Qwen −13.688002 ms/request [−13.801573, −13.574431]; Smol −11.954706 [−12.318178, −11.591234].

Copy-ablation CPU intervals cross zero. The optimization has not demonstrated a CPU saving. These clocks include bracket work and connection closing, and exclude CPU elsewhere in RX/softirq/BPF/TCP. They are neither total service CPU nor energy measurements, and do not prove polling is the exclusive cause of any delivery difference.

**Numerical fidelity and history.** The archived frozen reference asset is byte-identical to0042’s asset, with pre-performance frozen timestamp **2026-10-13 04:16:47 UTC**. Qwen has17 exact prompt/gen keys and22 complete sequences; Smol has17/19. Independent checking confirms every warmup and measured reply belongs to one whole frozen sequence for its exact input/gen. There is no tokenwise mixing, tolerance or post-observation expansion.

This reference is independent of the new candidate output and is not circular. Its boundary is nevertheless narrower than current trajectory replay: ordinary actual batching, KV/cache history and per-request ownership trajectories remain unobserved.

Matching request indices have identical prompts and generation lengths across conditions, but whole output sequences do not always agree:

| Model | Incremental/full-copy agreement | Incremental/native agreement |
|---|---:|---:|
| Qwen | 1,348 / 1,536 | 1,354 / 1,536 |
| Smol | 1,338 / 1,536 | 1,347 / 1,536 |

Aggregate executor histories also differ. For example, Qwen device-graph launches range2142–2211 for incremental,2142–2165 for full-copy and2093–2108 for native; Smol ranges2123–2364,2180–2456 and2100–2110 respectively. These executor-wide counts include warmups and do not reconstruct individual timed batches. Unchanged algorithms and matched token budgets therefore do not mean identical numerical/compute trajectories. No task-quality or universal numerical-correctness claim follows.

**Qualification, failures and exclusions.** I reanalyzed all four final redirect qualification raws: both models’ traced and ordinary three-path strict workloads. All exit zero, covering12 executors,7,464 requests and266,688 checked tokens; traced qualification reconstructs actual batches1–8. Final production-source module/native qualification and three-path Qwen preflight also reanalyze successfully.

The HF self-redirect results independently contain actual exit0, passTrue,32 response rows and652 checked tokens/model, with all exact checks passing. Their three intended aborted lifecycle cases are distinct from performance failures.

Initial failures remain material records: the first Smol full-copy half-close failure, HF timeout/EOF failures, captured genuine RECV EAGAIN, subsequent idle stall and failed `IOSQE_ASYNC` attempt are archived. Passing instrumented diagnoses do not erase those failures or establish the initial half-close failure’s cause. The final timed comparison uses the common repaired path, and none of those failed setup/diagnosis rows is counted as a candidate performance win or quietly removed timing sample.

The bounded timing-window journal search **08:02–08:21 UTC** exits0, examines1,354 lines and reports no matches for its explicitly listed fault patterns. It does not prove continuous host/GPU isolation or absence of interference. `late_closure_endpoint.json` is explicitly dated **2026-10-14 01:39:58 UTC**: same boot/base, preserved setup file, no model process/module/pins/GPU applications. It is a late endpoint, not an immediate post-timing receipt. My live read also finds no recorded timing PID, module, BPFusion pin or compute application remaining. Owned temporary-runtime cleanup remains the root agent’s subsequent action.

**Decision supported by the evidence.** Close this matrix with an inconclusive copy-performance verdict. It adds a fair, previously absent intervention against the repaired former loop; it does not demonstrate that redundant prefix copying is the practical throughput bottleneck. Do not subtract historical0042 numbers to attribute a gain to copying or either common repair.

A concrete next research decision is to move attention to a different measured transport cost. The persistent approximately-one-core stock worker cost makes polling/wakeup or complete delivery coordination a better-supported investigation direction than unchanged copy retries. Any next experiment should introduce a new causal discriminator chosen by the owning implementation agent. Wider baselines, repeated unchanged cells or a desired favorable outcome are not required by this review. The full project goal remains active.

<oai-mem-citation>
<citation_entries>
MEMORY.md:36-44|note=[located prior copy experiment context and replaced stale status with live raw evidence]
</citation_entries>
<rollout_ids>
01a1237b-bc13-7d90-a3d1-22ef8fc29d7e
</rollout_ids>
</oai-mem-citation>