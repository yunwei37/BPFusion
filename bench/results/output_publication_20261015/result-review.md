# Independent result review: batched model-result publication

Review conducted on 2026-10-15 UTC in the original yunwei356/bpfusion-dev Workspace, `/workspaces/repository`, main `ea82f18b703732288b6a38a235cbc978daf4bc23`.

## Separate judgments

- **Run status: incomplete.** The full wrapper and Qwen driver exit 1. Eleven Qwen executors actually serve all their requests and exit 0; ten reach the unchanged driver qualification. The eleventh original-loop process has one response outside the pre-observation complete-output pool. Only 44 of 160 planned performance cells are collected, and Smol full performance never starts.
- **Tested hypothesis: inconclusive.** There is no completed five-block candidate-minus-original primary estimate for either model. The failed original control cannot be treated as a proposed-method win, and the two completed Qwen blocks cannot replace the planned matrix.
- **Research value: supporting boundary evidence.** This adds a concrete ordinary-output qualification boundary in a previously available control. The passing protocol/lifecycle/preflight portions are dependencies, with no independent novelty or speedup value. There is no usable primary performance result.
- **Paper impact: mechanism/workload boundary.** The evidence does not challenge a necessary thesis prediction or answer the whole serving question. No formal paper RQ/thesis exists here to rewrite.
- **Next paper decision:** do not promote this publisher or claim a performance improvement. Preserve the full failure and partial observations, restore the saved original under the declared source-selection rule, and close this unchanged comparison. Any future ordinary-performance claim first needs a justified independent fidelity path for the actual executed histories; expanding the pool with the failed output, deleting the row, or rerunning until favorable is not such a path. This review authorizes no new experiment.

This is one fresh RESULT REVIEW. I performed read-only source/raw-data inspection and CPU-only recomputation. I wrote only this ordinary report, did not run GPU work or builds, edit source/recipes/oracles/raw data, clean resources, or perform Git publication. Source selection, final restoration and publication remain the root's work after report release.

## Audited materials and execution

I read plan.md, plan-review.md, execution-notes.md, recipe-adaptations.md, candidate.diff, setup.py, serving.py, analysis.py, run.py, lifecycle.py and analysis_lifecycle.py; current/saved dispatcher and bootstrap, source-native client/analyzer, private build commands/bindings, frozen reference assets/configurations, package/linkage/SASS receipts, all phase statuses and raw protocol/lifecycle/full data. I inspected current evaluation and closest-work conclusions to maintain the declared supporting scope.

The real serving commands in each phase's commands.json use the private runtime, actual pinned model snapshots, existing --loop-comparison, and the original source-native client. Performance adds --untraced and the frozen reference asset. Qualification uses --correctness and traced candidate loop/native. run.py stops on the first nonzero driver; it does not replace the failed cell. All expanded command and wrapper receipts remain available.

| Phase | Observed outcome |
|---|---|
| Setup | exit 0, completed 03:40:01.167533 UTC |
| Qwen preflight | four conditions, 16 cells, 128 measured requests / 4160 tokens plus 32 checked warmups; driver and fixed analysis exit 0 |
| Candidate protocol | both models × loop/native; four executors, each 622 requests / 22224 tokens, including 259 rejected requests and 5000 empty connections; both drivers and fixed analyses exit 0 |
| Candidate lifecycle | four conditions, each 32 actions / 652 initially checked complete-or-prefix tokens; all executor/driver exits 0 and fixed lifecycle analysis exit 0 |
| Full performance | Qwen only: 11 serving executors exit 0, 10 driver-verified; 44 cells / 1408 measured requests / 45760 tokens plus 88 warmups; terminal failure |
| Planned full matrix | two models × five blocks × four conditions × four cells = 40 executors / 160 cells / 5120 measured requests / 166400 tokens plus 320 warmups; not completed |

The full model order was Qwen then Smol. Qwen blocks 0 and 1 contain all four conditions. Block 2 collects candidate-loop, candidate-native, then original-loop; original-native is never launched. Qwen blocks 3–4 and every Smol full block are missing. Thus 29 of the planned 40 serving processes do not run. The fixed complete analyzer independently reproduces exit 1 at its terminal-success assertion, with empty stdout; this is an expected reproduction of failure, not a passing result.

I independently replayed the unchanged preflight and both protocol analyses: exit 0, empty stderr and byte-identical stdout to the retained analysis outputs. The lifecycle analyzer similarly reproduces exit 0 and identical stdout. These CPU checks do not rerun model inference.

## Intervention and matched controls

The saved original_vllm_graph.cu is byte-identical to HEAD. The saved candidate and source_snapshot dispatcher are byte-identical to the current dirty dispatcher at review. The sole production diff is 7 added lines and 1 removed line in dispatch's token publisher: the original fences each output row before its produced store; the candidate writes all batch payloads, fences once, then publishes all produced values. The same single CUDA thread performs both passes. DONE/release fences, model graph/math, KV mapping, admission, padding, FIFO-prefix ownership, stop handling, network ABI, timer and default route are unchanged.

This is a bundled implementation intervention: it reduces source-level repeated fences but also adds a publication pass and delays the first row's visibility until all batch payload/local request updates are done. Source fence counts or compiled SASS cannot identify physical fence latency, causal PCIe cost or a performance gain. The original and candidate SASS receipts contain distinct compiled dispatch code, not a physical mediation measurement.

The private Makefile.original changes only the vllm_graph.cu prerequisite to the saved original. Both private build directories use the same source-native rules, -O3, C++17, sm_120 and corresponding transport/trace flags. Original/candidate entry symlinks both target the unchanged executor/vllm_graph.py; its sys.argv entry path selects the sibling private .so, so labels do bind distinct libraries. All eight linkage receipts exit 0 and resolve the same private libcudart; loop libraries resolve the same private libbpf. No missing-library fallback is apparent.

The four labels mean:

- `uring_loop_original`: original publisher and existing eBPF/io_uring loop.
- `uring_loop`: candidate publisher and the same loop.
- `userspace_original`: original publisher and efficient timed-epoll native TCP.
- `userspace_candidate`: candidate publisher and the same native TCP.

Original-loop is the component control. Timed-epoll native TCP is the main competing orchestration mechanism. Native candidate/original are the matching publisher-policy comparison, not independent external baselines. The native path engages real accept/receive/send operations, rather than a mock or inert control. Its original-loop opponent's fixed-oracle failure prevents superiority claims from that failure.

Performance uses no BF_TRACE or GPU profiler. Qualification deliberately uses BF_TRACE and actual graph/KV/history replay. All actual phase metadata retain byte-equal driver/current candidate/saved original/bootstrap/client source; the full metadata also reports the expected untraced flags, models, request budget and five repetitions. The recipes do not modify token assertions, timeouts, request parser, arrival formulas or correctness criteria after observation.

The pre-observation preparation repair described in plan-review.md adds existing --loop-comparison to obtain native worker/CPU brackets and cell rotation; it precedes serving execution. The later full failure has not been repaired by changing an oracle, timeout, output pool, source, or metric. The absent midpoint host observation is a real deviation discussed below.

## Correctness and mechanism engagement

The common reference asset is byte-identical to the archived 0056 frozen_references.json. Each lifecycle configuration embeds exactly its corresponding frozen model object. Qwen has 17 prompt/generation keys and 22 known complete sequences; Smol has 17 keys and 19 sequences. No current output was appended.

The protocol traces/references independently support the stated finite qualification: request markers, prompts, generation lengths, exact token streams, ownership by physical slot, ordered releases and total emitted tokens agree under the fixed analyzer. Both models exercise actual GPU batches 1–8. The unchanged bootstrap actually replays body/head graphs from each trace's prompt, batch/query, KV slot and autoregressive history and asserts each numeric output; the references are therefore more than an echo of received bytes. They reuse the same graph/model implementation, however, and do not establish eager-HF equality, task quality, arbitrary inputs, or all untraced histories.

| Model / candidate path | Model rounds | Prefill / decode | Real prompt tokens | Padded query tokens | Release rounds / max prefix |
|---|---:|---:|---:|---:|---:|
| Qwen loop | 7104 | 206 / 6898 | 5374 | 3427 | 130 / 8 |
| Qwen native | 8003 | 168 / 7835 | 5374 | 3179 | 188 / 8 |
| Smol loop | 6979 | 210 / 6769 | 5374 | 3784 | 156 / 8 |
| Smol native | 8029 | 172 / 7857 | 5374 | 3332 | 193 / 8 |

All four protocol executors report graph_error=0, one resident launch and zero model trace overflows. Loop rings finish head/completed=622, accepted/closed=5086, empty independent SQ/CQ, zero pending/error/reserved/dropped/overflow and free eight physical slots. Loop trace_count=622 with trace_overflow=494 is the existing bounded 128-response network diagnostic, not model trace loss; it is retained, not mislabeled as zero. The one protocol abort is retained. Native reports 622 published/completed and 259 rejects.

I independently read the all-thread syscall traces after readiness. Loop qualification has zero accept/recv/send syscall matches for either model, and one io_uring_enter before the stop signal. Native has actual accept4/recvfrom/sendmsg calls: Qwen 5144/9035/4835, Smol 5141/8485/4966. All eleven full worker snapshots contain 133 tasks and no iou-sqp task. These support removal of the steady userspace request worker on the tested loop, not elimination of Linux CPU execution or total service CPU.

Lifecycle raw wire payloads were independently unpacked rather than trusting pass/exact fields. Every valid payload is a frozen allowed complete sequence or prefix; invalid replies carry no token body. Both loop conditions conserve accepted/closed=13, head/completed=32, aborted=3, empty rings, zero pending/error/reserved/dropped/overflow, and no remaining pins. Both native conditions preserve the declared accepted=13, published=32, completed=31, rejected=10 interrupted-stop boundary. Neither is silently converted into 32 fully delivered native requests.

The 652-token lifecycle count excludes bytes read after the explicit first-token stop. I independently checked those extra bytes too:

| Model / path | Initial stop prefix | Extra tokens after stop | Total captured stop prefix | Frozen prefix check |
|---|---:|---:|---:|---|
| Qwen loop | 1 | 1 | 2 | pass |
| Qwen native | 1 | 1 | 2 | pass |
| Smol loop | 1 | 0 | 1 | pass |
| Smol native | 1 | 8 | 9 | pass |

These additional 10 captured tokens remain separate from the suite's declared 4×652 checked-token count. They do not prove the remaining generation was delivered or all native model slots retired before interruption.

## Full-run failure and fidelity limit

Independently checking all 1496 full request rows finds precisely one outside-pool row, matching the retained read-only failed_full_diagnostic.json:

- Qwen, block 2, original-loop, gen64/c8, measured index 2, client marker 468830097634060.
- Prompt token IDs `[7985, 264, 2805, 42113, 13]`.
- All 64 token IDs arrive; the serving process exits 0 with graph_error=0 and admitted=retired=136.
- The prompt/gen key has three known complete sequences. The best matching frozen sequence shares the first 62 token IDs; the complete 64-token response is absent from the fixed pool.

Thus this is a fixed whole-output qualification failure, not a transport timeout or short response. It occurs on the original publisher, so it is not evidence that the candidate introduced a numerical bug; neither does that fact make the row valid or establish the candidate is correct for unseen trajectories. It could indicate an unrepresented legitimate trajectory or an actual wrong trajectory/output. Without the current ordinary batch/history replay, the data do not distinguish those explanations. Attributing it to floating-point sensitivity, cache drift, driver warnings or ordering corruption would exceed evidence.

All recorded request arrival arrays, lengths, TTFT/completion/TPOT formulas and all 44 cell TPS windows, request indices and worker CPU brackets independently recompute. The failed executor's raw ring also drains all 136 requests with empty SQ/CQ and zero error/reserved/dropped/overflow; cleanup stats/detach exit 0. Those transport/logical receipts do not override the failed token contract. The other 1495 rows belong to frozen sequences, including all 88 warmups; current ordinary histories remain unobserved for every performance process.

There are 40 cells in ten driver-verified processes, plus four cells in the failed original-loop process. Exactly one of those four cells contains the outside-pool row. Every cell is retained below; none is dropped or replaced. Full status remains failed/incomplete. Smol performance is NA, not borrowed from qualification or older experiments.

## Partial numerical observations and uncertainty

The prespecified primary is loop candidate-minus-original gen64/c8 TPS, separately per model over five paired process blocks. No such five-block sample exists. I do not replace it with a two-block confidence interval, pool individual requests as replicates, average incomplete conditions, or manufacture missing Smol estimates.

The two fully driver-qualified Qwen primary differences are +311.463036 and −32.031830 token/s. The block-2 arithmetic difference is −130.027433 token/s against the unqualified original control and is labeled accordingly. This mixture cannot select the shared change. Candidate-minus-original loop gen64/c8 TTFT differences are +0.099645, +0.090579 and +0.192618 ms, respectively: adverse descriptive latency shifts, with the third comparison unqualified.

Candidate-loop minus candidate-native gen64/c8 TPS differences are −85.897776, −32.615404 and −156.922510 token/s in the three collected blocks. Those partial descriptive losses cannot become a complete repeated transport result or establish general inferiority. Native publisher-policy differences are +57.486673 and +213.852875 token/s in the two complete blocks; the third original-native process is absent. These signed observations cannot substitute for the primary.

The block-1 candidate-native gen1/c1 cell includes a 10.120238 ms TTFT maximum/p99 with mean 2.015874 ms and p50 1.322061 ms. It is retained, not excluded as an outlier. More generally, all 32-request cell p99s below are descriptive nearest-rank maxima, not production tail guarantees.

The source-native client timestamps completed token IDs at recv arrival, including coalesced tokens with the same arrival timestamp. TPS is count×gen divided by last token arrival minus first request send. TTFT, TPOT and completion are client observations, not GPU execution times. Preopened connection setup/bootstrap/capture/warmups are outside the timed cell. Worker CPU below is the existing process CPU bracket plus the measured module worker contribution; module contribution is zero here. It excludes RX/softirq/eBPF and much kernel TCP work, so lower loop process CPU is not total-CPU savings.

No primary superiority, equivalence, noninferiority, familywise significance, SOTA result, physical mediation, energy result or open-loop/SLO capacity result follows. Existing eager-HF/AMK failures and broader backend/model support gaps remain untouched.

## Environment, preservation and remaining closure

All recorded private packages equal the 0057 package list: vLLM 0.31.0, Torch 2.13.0+cu129, Transformers 5.17.0, NumPy 2.3.5, Triton 3.7.1 and FlashInfer 0.7.0.post1. This excludes package-list drift as an observed difference, not every possible runtime/codegen/cache difference. The Qwen and Smol model snapshots remain respectively 7ae557604adf67be50417f59c2c2f167def9a775 and 93efa2f097d58c2a74874c7e644dbc9b0cee75a2, FP16.

All four host observations report the same boot ID 04dc0087-5ccc-4c46-9997-b9a92f0e5167, empty GPU app list, current/requested power limit 400 W versus default 575 W, and the same 56 selected historical NVRM 0x56 warnings, latest 00:53:50 UTC. The pre-existing power limit was not introduced by this candidate. No new selected warning is observed over these endpoints; existing warnings are not declared harmless.

| Receipt | UTC |
|---|---|
| host_entry | 03:36:40.756522 |
| host_preflight | 03:40:33.777399 |
| host_before | 04:02:35.296555 |
| full wrapper terminal | 04:11:05.937568 |
| host_after | 04:11:54.668266 |

The last observation is 48.730698 seconds after full terminal. It is correctly named host_after; there is no active full-run midpoint GPU/host snapshot. Sparse idle endpoints cannot prove continuous exclusive GPU use, absence of interference, or driver health throughout. Root's notes disclose late observation rather than recasting it as an active-run measurement. The wrapper process is absent at this review, consistent with its terminal receipt.

At review all eight preserved original path metadata objects match entry (including tools/setup_env.sh and original shared build/BPF outputs), and all twelve captured current sources match source_snapshot. Git remains main at the declared base, dirty only in the candidate dispatcher, with the pre-existing untracked tools/setup_env.sh retained. No new production target, mode, helper, service, model arithmetic, infrastructure config or persistent runtime change appears.

The candidate still exists uncommitted during review. Because no admissible supported primary gain exists, the plan's source-selection condition for retention is unmet. Root must perform and verify original restoration, owned TEMP cleanup, final base/Coder/build checks, complete evidence archive and CPU replay, then honest documentation/main publication. I have not claimed these post-review actions already happened. The original module-compatibility qualification was conditional on selecting the shared publisher and is not established by this unselected candidate's loop/native checks.

The full user objective remains active. Closing this failed supporting comparison is not completion of a generic reused-kernel server or proof that eBPF improves delivered latency/throughput.

## Appendix A: every collected full cell

These are independent raw-row recomputations, not output from a repaired full analyzer. L0/L1 mean original/candidate loop; N0/N1 mean original/candidate native. V means the process passed the unchanged driver; U means the original-loop process failed qualification, including its three otherwise in-pool cells. Outside is the number of this cell's outside-pool request rows. Each cell has 32 measured requests. All latency columns are ms, CPU is known-worker ms/request. Values are rounded here only; raw rows retain full precision.


| Block | Path | gen/c | V/U | Outside | TPS | TTFT mean/p50/p99 | Completion mean/p50/p99 | TPOT mean | CPU ms/request |
|---:|---|---|---|---:|---:|---|---|---:|---:|
| 0 | L0 | 1/1 | V | 0 | 735.812094 | 1.354147 / 1.352610 / 1.414011 | 1.354147 / 1.352610 / 1.414011 | NA | 0.034101 |
| 0 | L0 | 64/1 | V | 0 | 778.565777 | 1.422128 / 1.351329 / 3.321552 | 82.174586 / 81.976419 / 84.672231 | 1.281785 | 1.592086 |
| 0 | L0 | 1/8 | V | 0 | 2457.504751 | 2.921630 / 2.961228 / 4.035340 | 2.921630 / 2.961228 / 4.035340 | NA | 0.026536 |
| 0 | L0 | 64/8 | V | 0 | 4510.380352 | 2.460266 / 2.687374 / 3.708321 | 112.674449 / 120.008887 / 122.989675 | 1.749431 | 0.462873 |
| 0 | N0 | 1/1 | V | 0 | 707.026243 | 1.399918 / 1.376619 / 1.805179 | 1.399918 / 1.376619 / 1.805179 | NA | 0.052966 |
| 0 | N0 | 64/1 | V | 0 | 819.653588 | 1.315689 / 1.287031 / 1.691963 | 78.035969 / 78.009988 / 78.597107 | 1.217782 | 2.529726 |
| 0 | N0 | 1/8 | V | 0 | 2984.974664 | 2.505364 / 2.518936 / 2.991513 | 2.505364 / 2.518936 / 2.991513 | NA | 0.024270 |
| 0 | N0 | 64/8 | V | 0 | 4850.254491 | 2.145955 / 1.834640 / 8.450841 | 105.446482 / 111.779152 / 117.149804 | 1.639691 | 0.526845 |
| 0 | L1 | 1/1 | V | 0 | 706.797557 | 1.393922 / 1.394137 / 1.433913 | 1.393922 / 1.394137 / 1.433913 | NA | 0.075068 |
| 0 | L1 | 64/1 | V | 0 | 804.249602 | 1.448653 / 1.290029 / 2.894195 | 79.536457 / 79.297344 / 82.358896 | 1.239489 | 2.102894 |
| 0 | L1 | 1/8 | V | 0 | 2903.682405 | 2.584382 / 2.616626 / 3.320208 | 2.584382 / 2.616626 / 3.320208 | NA | 0.024397 |
| 0 | L1 | 64/8 | V | 0 | 4821.843388 | 2.559911 / 2.602232 / 3.653640 | 105.596957 / 112.991801 / 115.959484 | 1.635509 | 0.295329 |
| 0 | N1 | 1/1 | V | 0 | 717.618315 | 1.385527 / 1.378077 / 1.894424 | 1.385527 / 1.378077 / 1.894424 | NA | 0.046824 |
| 0 | N1 | 64/1 | V | 0 | 817.926983 | 1.490823 / 1.283031 / 4.148982 | 78.207049 / 77.966965 / 80.813116 | 1.217718 | 2.124289 |
| 0 | N1 | 1/8 | V | 0 | 2840.181899 | 2.554543 / 2.508264 / 4.052317 | 2.554543 / 2.508264 / 4.052317 | NA | 0.022899 |
| 0 | N1 | 64/8 | V | 0 | 4907.741164 | 1.929878 / 1.772891 / 3.465733 | 104.172832 / 111.070032 / 113.547031 | 1.622904 | 0.361730 |
| 1 | N0 | 64/1 | V | 0 | 794.321609 | 1.442924 / 1.379799 / 2.358547 | 80.539727 / 80.201429 / 83.634324 | 1.255505 | 2.008498 |
| 1 | N0 | 1/8 | V | 0 | 2097.417162 | 2.640369 / 2.806607 / 4.264905 | 2.640369 / 2.806607 / 4.264905 | NA | 0.033874 |
| 1 | N0 | 64/8 | V | 0 | 4527.322616 | 2.032362 / 1.676914 / 2.986657 | 112.901533 / 118.124728 / 123.203010 | 1.759828 | 0.507279 |
| 1 | N0 | 1/1 | V | 0 | 659.429252 | 1.497853 / 1.391463 / 4.130348 | 1.497853 / 1.391463 / 4.130348 | NA | 0.052971 |
| 1 | L1 | 64/1 | V | 0 | 806.988453 | 1.446037 / 1.291815 / 2.993041 | 79.260405 / 79.069818 / 80.945751 | 1.235149 | 2.063441 |
| 1 | L1 | 1/8 | V | 0 | 2280.560057 | 2.651403 / 2.519387 / 4.367191 | 2.651403 / 2.519387 / 4.367191 | NA | 0.027450 |
| 1 | L1 | 64/8 | V | 0 | 4708.560087 | 2.418893 / 2.511508 / 4.480892 | 107.702177 / 112.988334 / 118.875149 | 1.671163 | 0.476972 |
| 1 | L1 | 1/1 | V | 0 | 506.830644 | 1.966452 / 1.993812 / 4.363309 | 1.966452 / 1.993812 / 4.363309 | NA | 0.066836 |
| 1 | N1 | 64/1 | V | 0 | 817.566619 | 1.585299 / 1.289928 / 3.777568 | 78.245717 / 77.958641 / 81.857328 | 1.216832 | 2.150991 |
| 1 | N1 | 1/8 | V | 0 | 2627.051604 | 2.514854 / 2.497660 / 3.977325 | 2.514854 / 2.497660 / 3.977325 | NA | 0.031166 |
| 1 | N1 | 64/8 | V | 0 | 4741.175491 | 1.920801 / 1.493028 / 3.442148 | 107.438872 / 113.232230 / 120.851147 | 1.674890 | 0.345772 |
| 1 | N1 | 1/1 | V | 0 | 494.114471 | 2.015874 / 1.322061 / 10.120238 | 2.015874 / 1.322061 / 10.120238 | NA | 0.037801 |
| 1 | L0 | 64/1 | V | 0 | 805.116901 | 1.406418 / 1.302261 / 3.135508 | 79.445112 / 79.186702 / 81.776292 | 1.238709 | 2.271384 |
| 1 | L0 | 1/8 | V | 0 | 2471.123188 | 2.698564 / 2.600632 / 4.895453 | 2.698564 / 2.600632 / 4.895453 | NA | 0.029004 |
| 1 | L0 | 64/8 | V | 0 | 4740.591917 | 2.328313 / 2.150247 / 4.963188 | 107.069344 / 112.904797 / 119.998403 | 1.662556 | 0.481372 |
| 1 | L0 | 1/1 | V | 0 | 542.907802 | 1.824282 / 1.980173 / 2.084360 | 1.824282 / 1.980173 / 2.084360 | NA | 0.063855 |
| 2 | L1 | 1/8 | V | 0 | 2454.557323 | 2.719432 / 2.802783 / 3.993762 | 2.719432 / 2.802783 / 3.993762 | NA | 0.028189 |
| 2 | L1 | 64/8 | V | 0 | 4452.108854 | 2.460002 / 2.391040 / 4.612600 | 112.350361 / 117.180810 / 126.671999 | 1.744291 | 0.385950 |
| 2 | L1 | 1/1 | V | 0 | 723.228238 | 1.370391 / 1.362820 / 1.423499 | 1.370391 / 1.362820 / 1.423499 | NA | 0.051229 |
| 2 | L1 | 64/1 | V | 0 | 805.120118 | 1.457462 / 1.297915 / 3.340751 | 79.455236 / 79.259066 / 82.225370 | 1.238060 | 1.816795 |
| 2 | N1 | 1/8 | V | 0 | 2137.324430 | 3.038983 / 2.845649 / 6.401842 | 3.038983 / 2.845649 / 6.401842 | NA | 0.031349 |
| 2 | N1 | 64/8 | V | 0 | 4609.031364 | 2.517449 / 2.523553 / 5.525101 | 110.616487 / 116.113699 / 119.250622 | 1.715858 | 0.474509 |
| 2 | N1 | 1/1 | V | 0 | 553.359927 | 1.786191 / 1.633821 / 4.135605 | 1.786191 / 1.633821 / 4.135605 | NA | 0.058636 |
| 2 | N1 | 64/1 | V | 0 | 817.893551 | 1.557185 / 1.282945 / 3.192686 | 78.217566 / 77.968805 / 79.850906 | 1.216831 | 1.952315 |
| 2 | L0 | 1/8 | U | 0 | 2293.592119 | 2.730682 / 2.802198 / 3.955756 | 2.730682 / 2.802198 / 3.955756 | NA | 0.028665 |
| 2 | L0 | 64/8 | U | 1 | 4582.136288 | 2.267384 / 2.369854 / 3.863171 | 108.369393 / 113.773428 / 122.817483 | 1.684159 | 0.526158 |
| 2 | L0 | 1/1 | U | 0 | 721.948016 | 1.374410 / 1.298365 / 3.454579 | 1.374410 / 1.298365 / 3.454579 | NA | 0.049312 |
| 2 | L0 | 64/1 | U | 0 | 804.090382 | 1.344489 / 1.287661 / 2.802948 | 79.552663 / 79.446594 / 82.046538 | 1.241400 | 2.158555 |

## Appendix B: every available signed within-block contrast

All values are literal candidate minus baseline. Positive TPS favors the named candidate; positive latency or CPU is adverse. Loop policy=L1−L0; native policy=N1−N0; candidate transport=L1−N1; original transport=L0−N0. V means both processes passed the driver, not that the integrated full experiment is valid. U identifies contrasts involving the failed original-loop process. Missing pairs/conditions stay absent; there is no confidence interval or pooled primary estimate. TTFT/completion/TPOT are ms; CPU is ms/request. Executor CPU equals known-worker CPU here; measured module-worker CPU and all its contrasts equal zero.

| Block | Contrast | gen/c | V/U | TPS difference | TTFT difference | Completion difference | TPOT difference | CPU difference |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 0 | loop policy | 1/1 | V | -29.014537 | 0.039775 | 0.039775 | NA | 0.040966 |
| 0 | loop policy | 64/1 | V | 25.683825 | 0.026526 | -2.638129 | -0.042296 | 0.510807 |
| 0 | loop policy | 1/8 | V | 446.177654 | -0.337247 | -0.337247 | NA | -0.002139 |
| 0 | loop policy | 64/8 | V | 311.463036 | 0.099645 | -7.077492 | -0.113923 | -0.167544 |
| 0 | native policy | 1/1 | V | 10.592071 | -0.014391 | -0.014391 | NA | -0.006142 |
| 0 | native policy | 64/1 | V | -1.726605 | 0.175135 | 0.171081 | -0.000064 | -0.405437 |
| 0 | native policy | 1/8 | V | -144.792764 | 0.049180 | 0.049180 | NA | -0.001371 |
| 0 | native policy | 64/8 | V | 57.486673 | -0.216077 | -1.273650 | -0.016787 | -0.165115 |
| 0 | candidate transport | 1/1 | V | -10.820757 | 0.008395 | 0.008395 | NA | 0.028243 |
| 0 | candidate transport | 64/1 | V | -13.677380 | -0.042170 | 1.329408 | 0.021771 | -0.021395 |
| 0 | candidate transport | 1/8 | V | 63.500505 | 0.029839 | 0.029839 | NA | 0.001498 |
| 0 | candidate transport | 64/8 | V | -85.897776 | 0.630033 | 1.424125 | 0.012605 | -0.066401 |
| 0 | original transport | 1/1 | V | 28.785851 | -0.045771 | -0.045771 | NA | -0.018865 |
| 0 | original transport | 64/1 | V | -41.087810 | 0.106439 | 4.138617 | 0.064003 | -0.937640 |
| 0 | original transport | 1/8 | V | -527.469913 | 0.416266 | 0.416266 | NA | 0.002266 |
| 0 | original transport | 64/8 | V | -339.874139 | 0.314310 | 7.227967 | 0.109741 | -0.063972 |
| 1 | loop policy | 1/1 | V | -36.077158 | 0.142171 | 0.142171 | NA | 0.002981 |
| 1 | loop policy | 64/1 | V | 1.871552 | 0.039620 | -0.184707 | -0.003561 | -0.207944 |
| 1 | loop policy | 1/8 | V | -190.563131 | -0.047161 | -0.047161 | NA | -0.001554 |
| 1 | loop policy | 64/8 | V | -32.031830 | 0.090579 | 0.632833 | 0.008607 | -0.004400 |
| 1 | native policy | 1/1 | V | -165.314781 | 0.518021 | 0.518021 | NA | -0.015171 |
| 1 | native policy | 64/1 | V | 23.245010 | 0.142376 | -2.294009 | -0.038673 | 0.142493 |
| 1 | native policy | 1/8 | V | 529.634442 | -0.125515 | -0.125515 | NA | -0.002708 |
| 1 | native policy | 64/8 | V | 213.852875 | -0.111561 | -5.462661 | -0.084938 | -0.161507 |
| 1 | candidate transport | 1/1 | V | 12.716172 | -0.049422 | -0.049422 | NA | 0.029035 |
| 1 | candidate transport | 64/1 | V | -10.578166 | -0.139262 | 1.014687 | 0.018317 | -0.087550 |
| 1 | candidate transport | 1/8 | V | -346.491547 | 0.136549 | 0.136549 | NA | -0.003716 |
| 1 | candidate transport | 64/8 | V | -32.615404 | 0.498092 | 0.263304 | -0.003727 | 0.131200 |
| 1 | original transport | 1/1 | V | -116.521450 | 0.326429 | 0.326429 | NA | 0.010883 |
| 1 | original transport | 64/1 | V | 10.795292 | -0.036506 | -1.094615 | -0.016795 | 0.262886 |
| 1 | original transport | 1/8 | V | 373.706026 | 0.058195 | 0.058195 | NA | -0.004870 |
| 1 | original transport | 64/8 | V | 213.269301 | 0.295952 | -5.832190 | -0.097272 | -0.025907 |
| 2 | loop policy | 1/1 | U | 1.280222 | -0.004019 | -0.004019 | NA | 0.001917 |
| 2 | loop policy | 64/1 | U | 1.029736 | 0.112973 | -0.097427 | -0.003340 | -0.341760 |
| 2 | loop policy | 1/8 | U | 160.965204 | -0.011249 | -0.011249 | NA | -0.000476 |
| 2 | loop policy | 64/8 | U | -130.027433 | 0.192618 | 3.980968 | 0.060133 | -0.140208 |
| 2 | candidate transport | 1/1 | V | 169.868311 | -0.415800 | -0.415800 | NA | -0.007407 |
| 2 | candidate transport | 64/1 | V | -12.773433 | -0.099724 | 1.237669 | 0.021228 | -0.135520 |
| 2 | candidate transport | 1/8 | V | 317.232892 | -0.319551 | -0.319551 | NA | -0.003160 |
| 2 | candidate transport | 64/8 | V | -156.922510 | -0.057447 | 1.733874 | 0.028434 | -0.088559 |

Review released 2026-10-15T04:19:53.660109+00:00.
