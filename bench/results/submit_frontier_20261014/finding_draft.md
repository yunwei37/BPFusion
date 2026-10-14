# Idle model admission after SQ consumption improves vLLM short-output latency locally

This completed scheduling experiment keeps reused model arithmetic and tests a new admission order. It improves vLLM gen1/c8 latency versus the prior coalesced driver, retains substantial native TCP gaps and worsens AMK short-output latency. Long-output throughput gains and non-regression are not established. This is a limited driver result.

## Intervention and controls

Both experimental BF_IO_COALESCED dispatchers were changed after io_progress: if retired==seen and mapped SQ head differs from tail, continue network progression before admitting fresh model work. It waits for published SQ consumption, not CQ/socket completion. Equality is sufficient for no unfinished admitted model computation, but it does not release TX ownership. Stop is revisited every iteration; a stalled issuer can delay fresh admission. This does not prove arbitrary fairness/backpressure bounds. No model math, protocol/page ABI, timer, target, runtime knob or steady userspace worker is added.

The completed run tests the six-line candidate in both qwen_graph.cu and vllm_graph.cu. Exact source_snapshot and candidate.diff retain those bytes at main ceadcc0. The prior coalesced component control is captured from that pre-edit main source, rebuilt under distinct library names with equal normalized SASS (AMK3 functions3656 instructions, vLLM3 functions4872). Efficient native epoll is the strongest competing delivery mechanism with the same per-workload reused model code, KV/packing/precision. Actual realized batches can differ; this is not identical kernel-sequence or pure arithmetic/PCIe mediation.

## Completed ordinary paired comparison

Original bpfusion-dev/main, RTX5090/170SMs, temporary Torch2.13+cu129/Transformers5.17/vLLM0.31. Pinned AMK884534c4 Smol FP16/cpasync0 and the existing optimized vLLM Smol/Qwen computations remain. Cross-backend linkage/construction differs; no cross-backend pure fusion claim.

Five paired process blocks use three paths and four gen1/64,c1/c8 cells with32 requests/cell and8 excluded sequential checked warmups/executor. The full run completes45 executors/180 cells/5760 measured requests187200 tokens plus360 warmups (6120 complete replies187560 tokens), all actual exits0, with no restarted/excluded/replaced cells. Source, environment and all15 expanded commands were frozen before collection; actual and declared commands match. Five of six path permutations and odd model/cell reversal leave residual order/drift confounding. Nominal pairedt95df4 intervals use five process blocks, not individual requests. This is a finite localhost token-ID HTTP workload, not capacity/SLO/text-serving/general-model/total-CPU evaluation.

| Workload | Path | gen1/c8 TTFT ms | gen64/c8 token/s |
|---|---|---:|---:|
| AMK Smol135M | uring_loop_coalesced_original | 130.568611 | 300.956502 |
| AMK Smol135M | userspace | 129.459725 | 303.712664 |
| AMK Smol135M | uring_loop_coalesced | 131.920117 | 301.532471 |
| vLLM Smol135M | uring_loop_coalesced_original | 6.992107 | 5286.312735 |
| vLLM Smol135M | userspace | 1.968652 | 5540.676521 |
| vLLM Smol135M | uring_loop_coalesced | 5.091485 | 5340.193444 |
| vLLM Qwen0.5B | uring_loop_coalesced_original | 8.601220 | 4525.631656 |
| vLLM Qwen0.5B | userspace | 2.511788 | 4816.390813 |
| vLLM Qwen0.5B | uring_loop_coalesced | 6.875646 | 4564.005932 |

| Workload | Candidate minus control | gen1/c8 TTFT difference, ms | Nominal paired t95 |
|---|---|---:|---|
| AMK Smol135M | uring_loop_coalesced_original | 1.351507 | [0.387822, 2.315192] |
| AMK Smol135M | userspace | 2.460392 | [1.023886, 3.896898] |
| vLLM Smol135M | uring_loop_coalesced_original | -1.900622 | [-3.042158, -0.759086] |
| vLLM Smol135M | userspace | 3.122832 | [2.059875, 4.185789] |
| vLLM Qwen0.5B | uring_loop_coalesced_original | -1.725574 | [-3.130448, -0.320700] |
| vLLM Qwen0.5B | userspace | 4.363857 | [3.024918, 5.702797] |

| Workload | Candidate minus control | gen64/c8 throughput difference, token/s | Nominal paired t95 |
|---|---|---:|---|
| AMK Smol135M | uring_loop_coalesced_original | 0.575969 | [-0.605341, 1.757279] |
| AMK Smol135M | userspace | -2.180192 | [-3.235810, -1.124575] |
| vLLM Smol135M | uring_loop_coalesced_original | 53.880709 | [-131.165198, 238.926615] |
| vLLM Smol135M | userspace | -200.483077 | [-508.337580, 107.371427] |
| vLLM Qwen0.5B | uring_loop_coalesced_original | 38.374277 | [-87.502549, 164.251102] |
| vLLM Qwen0.5B | userspace | -252.384880 | [-374.090134, -130.679627] |

vLLM short-output latency improves about27.2% Smol and20.1% Qwen versus the fresh matched prior-control means; every signed latency contrast versus prior is negative. Both native latency gaps remain positive in every block. AMK worsens in every block versus prior and native, so that transfer is rejected. All three long-output candidate-vs-prior throughput intervals contain0; this establishes neither gains nor equivalence/non-regression. Qwen and AMK retain negative native throughput intervals; Smol native throughput is inconclusive, with positive and negative blocks retained.

All gen1/c1 candidate-vs-prior TTFT intervals contain0. AMK remains0.131663ms above native [0.085347,0.177980]. vLLM c1 native intervals cross0 and do not prove equivalence. All36 means/108 signed effects, completion, TPOT and known-worker CPU brackets are retained in full.analysis.json. CPU brackets omit kernel/softirq work and energy; no all-CPU removal claim.

## Integrated observation and qualification

The one-cell observation executes two models xthree paths xordinary/BF_TRACE, one process each, with32 gen1/c8 measured requests and8 excluded warmups. All12 executors/480 replies complete; independent selected trace history replay, unchanged finite output pools, unique marker/ID associations, compute/release exactly once and graph-counter agreement pass. Ordinary model rounds subtract exactly8 warmups: Smol prior/native/candidate26/8/9; Qwen26/8/21.

Traced candidate rounds differ materially: Smol19 versus ordinary9, Qwen14 versus ordinary21; old/native traced rounds are26/8 Smol and24/8 Qwen. Client latencies differ too. One process/condition is descriptive sensitivity, not trace neutrality, equivalence or authenticated batching/causal mediation in the ordinary five-block matrix. The source/order intervention and these selected counts are supporting evidence only. probe_observation.md and probe.analysis.json retain actual per-round IDs/batches.

The initial observation analyzer glob mistakenly included per-executor trace/reference files and failed before reading results. Initial source/stdout/stderr/exit1 and analysis_repair.md remain. Literal selection of the four declared driver files succeeds without changing metrics, oracle or serving raw records and without repeating an executor. qualification_probe_completion.md distinguishes the failed original analysis chain from the corrected standalone analysis.

Nine real preflight paths pass36 cells/288 measured requests9360 tokens plus72 warmups. Three protocol runs each complete622 requests22224 tokens/259 rejects plus5000 empty connections, covering fragmentation/invalid/wrap/pipeline/halfclose. Three32-action lifecycle workloads pass idle/RST/reuse/inflight-stop/pending-accept/recv and independent ownership/SQ/CQ/model checks. strace qualifies no steady userspace request worker/custom TX module in selected paths. These finite qualifications are dependencies, not independent performance contributions. All ordinary complete outputs match unchanged finite whole-output pools; the stronger old AMK eager-HF discrepancy remains failed and all-input parity is not proved.

Host records before13:41:55UTC, during13:43:31, mid13:50:42 and after14:04:46 retain boot04dc0087 and33 old NVRM status0x56 warnings, with no new selected fault. The mid snapshot records one Python GPU application, endpoint applications are empty. These discrete observations do not prove continuous isolation, clean journal, harmlessness or exclude every environmental cause.

## Review and selection

The fresh independent result review is pending. The prospective selection is vLLM-only experimental retention and AMK restoration to its tested prior control, preserving the measured AMK rejection. Final source/selection/restoration must be recorded after review; this draft is not a publication or completion claim. Defaults and ordinary noncoalesced policy remain unchanged. Full retained serving/performance goal remains active.

