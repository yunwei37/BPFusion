Reviewed UTC: 2026-10-14T18:28:52.284349+00:00

# Independent plan review: current GPU I/O arrangements

Verdict: **ADMIT**, as a finite supporting constructor-selection experiment. No blocking scientific or executability defect was found in the inspected plan and prepared recipes. This admits the proposed preflight, not a performance conclusion, correctness pass, source promotion, or additional experiment.

Reviewer: fresh independent `/root/current_io_placement_plan_review`. Review round: initial. No desired verdict was supplied. Review scope was source/CPU inspection in the original `yunwei356/bpfusion-dev` Workspace. No GPU execution, package install, build, service change, cleanup, publication, or interruption was performed.

## 1. Hypothesis, retained question and paper value

The retained question concerns delivered latency/TPS for the Linux TCP/HTTP/eBPF/shared-queue/resident real-model GPU/asynchronous reply path without a steady userspace request worker, while reusing upstream math. The repository has no formal paper RQ or idea-story contract to quote. The plan accurately preserves that fact; this review does not invent a thesis. Its narrower hypothesis is that current standalone GPU I/O recovers gen64/c8 output TPS against current coalesced serving, with efficient native TCP establishing the remaining competing-mechanism boundary.

This is a whole-constructor comparison. Standalone residency, durable state access, per-entry publication, model-idle admission and coalesced progression differ together. A positive result identifies a useful existing route; it does not identify exclusive overlap, SM occupancy, PCIe access or GPU-time mediation. The plan consistently limits interpretation to this scope.

The admission rationale survives an independent reuse check. Finding0050 already establishes that the old original-loop vLLM implementation was faster than then-coalesced serving. CPU recomputation from all five raw gen64/c8 client blocks confirms original/native/coalesced TPS of 5592.135316/5630.454317/5070.857739 for Smol and 4758.150868/4806.615252/4373.107613 for Qwen. Repeating that old comparison would be redundant. However, archived original sources and raw metadata agree with `82d31c8`; current header inspection confirms an actual later transformation from kernel-local request/state variables to allocated durable `IoState`, initialization and an `io_progress` call. Current standalone was covered only by finite legacy compatibility, not this matched current performance and complete candidate qualification. Current coalesced also includes subsequent batched publication and final-response/SQ admission policy. Old0050 numbers cannot settle that current constructor tradeoff.

Findings0053/0054 and current `docs/evaluation.md` provide the other necessary prior evidence: substantial short-output recovery already occurred, remaining long-output native gaps are not explained by additional ordinary model rounds, and device bookkeeping placement did not establish primary TPS gains. Comparing the credible existing standalone alternative before another timer/model tuning intervention has higher immediate decision value. The role remains **supporting**, not headline or a new research contribution from version changes. Qualification/setup are dependencies folded into this comparison.

Outcomes change the local decision: a reliable standalone gain supports selecting the existing route for the tested model/cell, subject to short-output and native limits; an adverse result says the historical advantage does not transfer and closes this unchanged route comparison; mixed results require model/workload-specific decisions; crossing-zero uncertainty justifies no promotion by mean alone. A negative result bounds the tested constructor and cannot directly reject the broader retained objective. This limited decision value is sufficient for admission but would not justify presenting another general coalescing novelty claim.

## 2. Baselines and numerical fairness

Efficient native `vllm_graph_user_network_wait` is the single main baseline: a credible alternative answer using ordinary userspace TCP with the same reused model graphs. Source confirms timed `epoll_pwait2` at the existing nominal 60000ns wait, nonblocking socket handling and streamed output. It is not a deliberately busy or definitionally weak baseline. A fresh matched comparison is needed for current source/common runtime; there is no published or old numerical result that resolves the current constructors under the proposed process contexts.

Current coalesced is correctly labeled a **component control**, rather than another external competitor. It supplies the route-selection contrast. There is no unnecessary AMK rerun or additional weak baseline. The opposite AMK finding is a cited boundary, with its stricter eager-HF discrepancy retained rather than repaired by this run.

All paths use the same current `vllm_graph.py` and `vllm_graph.cu` model computation, FP16 model/KV policy, captured graph set, padded prefill, prefix release, four prompts, cached exact Smol/Qwen snapshot paths, output budgets, warmups, client parser, runtime and compiler. The old-to-current CUDA source diff contains only the conditional coalesced progression/admission block. That supports the same-math premise; it does not promise identical compiled instructions or identical serving GPU work. Native/standalone/coalesced flags differ intentionally. No condition-specific tuning is prepared.

CPU reconstruction of frozen pools from every recorded original reference file exactly equals the prepared pools: 17 prompt/gen entries with 19 complete sequences for Smol and 22 for Qwen. Candidate outputs cannot expand these pools during measurement. This is finite pre-observation qualification, not an independent eager arithmetic oracle or all-input/model quality claim.

## 3. Workloads, metrics and uncertainty

The primary gen64/c8 delivered output TPS is appropriate to the question. The actual driver computes total measured output tokens divided by last client token arrival minus first request send; fixed analysis independently recomputes that window. These are finite persistent localhost request waves, not offered-load capacity, tail/SLO, arbitrary text or full official vLLM-server throughput.

The plan's official [vLLM benchmark documentation](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics), checked during review, reports output-token throughput and defines client TTFT and per-request TPOT. The prepared arrival formulas match those latency definitions. The custom finite throughput window is explicitly disclosed; the citation does not make this a standard full-server benchmark. Known-worker CPU and aggregate model rounds remain explanatory secondary measurements, not new paper-facing scores or total CPU/energy claims.

Five paired process blocks are the inference unit; the analysis uses signed block differences, sample standard deviation and nominal paired t95 coefficient 2.776445105 with df4. It does not pool 32 client requests as independent repetitions. Four primary model/control contrasts are nominal, not familywise-corrected. The declared small-N, shared-host drift and five-of-six permutation imbalance are real limitations but do not invalidate this finite supporting result. Odd context/model/cell reversals reduce order bias without proving its removal.

The fixed short/transfer matrix and count arithmetic agree: 20 drivers, 60 executors, 120 cells, 3840 measured requests, 124800 output tokens, 480 excluded one-token warmups. Real preflight has 4 drivers, 12 executors, 24 cells, 192 measured requests, 6240 tokens and 96 warmups. Candidate-minus-coalesced and candidate-minus-native TPS remain the primary effects for each model; all secondary signs are retained and cannot replace an inconclusive primary or supply equivalence.

Counter subtraction is source-grounded. Eight sequential one-token warmups imply eight model rounds in short contexts. Transfer includes 8 warmup plus 32 serial gen1 plus 32 serial gen64 rounds, yielding 2088; long-counter analysis checks complete output counts and serial nonoverlapping timestamps before subtraction. Source increments `launches` for each admitted batch computation and reports it as `device_graph_launches`. Round totals do not identify ordinary batch membership, GPU time or exclusive causal mediation. Whole-transfer CQ-SQ excess is appropriately descriptive and not a gen64/c8 per-cell cost.

## 4. Candidate correctness and mechanism engagement

`qualification.py` actually selects standalone `uring_loop` and its private traced entry. The suite retains fragmented HTTP/binary requests, concurrency1..8, wrap/rejection reuse, mixed output lengths, pipeline/half-close, invalid first/last token cases and 5000 empty connections. Required counts are 622 requests, 22224 output tokens and 259 rejections per model. Client status/length/output checks, frozen pool membership, request-marker association, observed batch/history/KV replay and trace-overflow checks are preserved. Replay uses the reused graphs, so it is not fresh eager-HF arithmetic parity.

Protocol strace retains a post-ready ban on accept/recv/send-family calls and the expected one steady `io_uring_enter`; source has no steady userspace request handler for these builds. No SQPOLL worker is expected for BPF-loop targets. This proves the finite intended path when real qualification succeeds, not kernel portability or zero host CPU.

The lifecycle stdout-marker removal is justified. That marker is printed only under `BF_IO_COALESCED`; requiring it for standalone would reject the intended constructor. Source instead launches `io_network` on a nonblocking stream before readiness in the standalone branch, while coalesced supplies `io_state` to the dispatcher and starts the network worker only after model quiescence. The private Make flags select these branches without production mutation. This is adequate source/build plus real-path engagement for the claimed constructor comparison; it is not dynamic overlap profiling.

Lifecycle retains 32 actions and 652 complete-or-prefix tokens per model, HTTP/binary rejection, idle/reconnect/half-close, RST after first token and inflight SIGTERM. Source synchronizes model stream0, publishes shared `model_quiesced`, drains the BPF loop until `finished`, synchronizes the network stream and releases ring/link/state/connections/mappings. Physical FREE slots, bitmap0, recycle32, pending/error/drop/overflow0, separately balanced SQ/CQ, 13 accepted/closed, 32 completions and 3 aborts remain required. Intentional admitted32/retired31 is not a complete model-response claim. Quiescence is source plus successful shutdown evidence, not sampling a freed field.

The fixed lifecycle analysis still partly trusts driver `exact` flags; the plan explicitly additionally requires independent inspection of stored request/reply bytes, frozen pools, resource/counter stdout and syscall records at result review. That planned independent audit must actually occur. Merely citing `pass=true` or `analysis_lifecycle.py` output alone would not satisfy the plan, but this is not a missing plan requirement and does not block preflight.

## 5. Executability, private paths and preservation

CPU AST parsing succeeds for all ten required prepared scripts. `matched_serving.py` agrees with the short/transfer drivers except their intended matrix split. `run.py` emits all expanded ordinary commands before collection, executes serially, records per-driver exit receipts and stops on real failure. Drivers retain raw source/oracle/client/executor/counter records and terminal status. Fixed full analysis requires all20 files and all expected executors/cells; a partial prefix cannot silently be treated as complete. Resume/deviation handling remains the owning agent's task without resetting live processes based on observer timeouts.

A CPU-only `make -n` expansion with explicit private targets and a placeholder `VLLM_CUDART` value succeeds. No compiler, linker or mkdir is executed. The native flags are `BF_USER_NETWORK`/`BF_USER_NETWORK_WAIT`; coalesced adds `BF_URING_NETWORK`/`BF_URING_BPF_LOOP`/`BF_IO_COALESCED`; standalone omits only `BF_IO_COALESCED`; traced standalone additionally sets `BF_TRACE`. All four retain padded prefill/prefix release. Objects, dlink objects, libraries and symlinks resolve under TEMP/build. The explicit library/entry targets do not depend on root or private BPF rebuild targets. This protects the four unowned root trace artifacts; no accidental root artifact build appears in the expanded graph.

`vllm_graph.py` resolves repository root through the symlink's source but derives the library from absolute `sys.argv[0]`, selecting the private adjacent `.so`. Repository cwd then makes `io_uring_tcp.h`'s actual `build/uring_loop.bpf.o` lookup point to the existing root object. Drivers invoke existing root `build/bpfusion_load`. These two shared tools are read-only in setup and must remain frozen/preserved during collection. Private PATH chooses runtime Python for the source shebang; `VLLM_PYTHON` chooses the same Torch CUDA runtime for linkage; private `LD_LIBRARY_PATH` supplies downloaded libbpf1.6.3. Package resolution, actual dynamic library loading and real host compatibility remain preflight responsibilities, not proven by this dry run.

Live repository HEAD is `048c204ed78e006f1e31cfa8a7fb4699b7429d06` on main; only unrelated `tools/setup_env.sh` is untracked. All eight preserved path inode/size/mtime/symlink records still exactly equal `preserved_before.json` after this review. No TEMP runtime or private build was created by the reviewer. The planned source/build/environment/model freeze before collection, sparse actual host brackets, full terminal collection, independent result review and post-run restoration are sufficient and must remain attached to the eventual result.

## 6. Blocking defects and optional suggestions

**Blocking scientific defects: none. Blocking executability defects found by CPU inspection: none. No necessary repair before the admitted real preflight.** Actual install/build/real-path failures, if encountered, remain execution defects to repair under the unchanged plan, not favorable scientific results.

Optional suggestions, not admission conditions:

- In the final table call this current constructor selection explicitly; keep original0050 evidence beside it as historical context rather than a merged numerical dataset.
- Retain block signs/order alongside nominal intervals, especially if a small mean advantage is sensitive to one block. Do not increase collection just to cross significance.
- Make the final source recommendation describe throughput and short-latency tradeoffs by model/workload; native matching or crossing0 is not equivalence.
- The result reviewer should independently decode lifecycle raw bytes and inspect shutdown/syscalls as already promised, because fixed analyzer booleans alone are insufficient for that part of the agreed audit.

No new baseline, observer, tuning sweep, control interface, permanent runtime, configuration, source change or investigation limit is requested by this review.

## 7. Reviewer completion and handle release

Review completed with source reads, frozen-pool and old0050 raw-client CPU recomputation, AST parsing and a non-executing Make recipe expansion in the original Workspace. All read subprocesses returned terminal status; file contexts closed; no background session, GPU process, open subprocess pipe or retained file handle remains. The only written artifact is this `plan-review.md`. The reviewer releases all handles and returns **ADMIT** to the owning agent.
