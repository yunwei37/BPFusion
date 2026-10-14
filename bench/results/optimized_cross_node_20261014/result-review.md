# Optimized module-free cross-node serving: independent result review

Reviewed 2026-10-14 against production source bd39e59e4e5f27b5ac72313795d5ea77d3ef4d82 and frozen execution checkpoint 81baa94c84a5567950e87f3310788c000c6e9d6a. This was a fresh read-only result review. No source, plan, paper, infrastructure or serving execution was changed; the only written artifact is this report.

## Separate judgments

- Run status: **valid completed serving and finite shared-host observational comparison**, with a material host-fault qualification. The raw protocol, numerical scope, matrix and actual child terminals pass. This does **not** validate a clean, stable-host causal performance comparison.
- Tested hypothesis: **inconclusive** for the four predeclared latency/throughput improvements. Every primary nominal interval crosses zero. Finite cross-node delivery with the qualified output set is supported. A secondary Smol single-lane long-output performance regression is observed.
- Research value: **supporting**. This adds current optimized, module-free cross-node service evidence absent from prior local/older-backend runs. Setup, report counts and resource readiness are dependencies rather than separate contributions.
- Paper impact: **additional RQ evidence and a mechanism/workload/environment boundary**, not a direct thesis challenge. There is no formal paper thesis being tested.
- Next paper decision: close the unchanged comparison honestly. Keep the serving acceptance result, publish all observed numbers, failures and environmental faults, and make no speedup/equivalence/clean-host claim. Diagnose and recover the real host/storage fault through its owning path before further serving experiments. Once recovered, choose new evidence that resolves an actual causal uncertainty or strengthens full-objective acceptance; this review does not authorize an unchanged rerun, tuning sweep, extra baseline or scientific redesign.

The new authoritative kernel journal changes the interpretation substantially: there was a global OOM and EXT4/I/O failure burst on lab at 05:28:38 UTC inside the run. This is known instability, beyond merely lacking continuous isolation. Arithmetic confidence intervals account for the five observed blocks; they do not remove this confounding condition or guarantee stationary sampling.

## What was independently checked

I read plan.md, plan-review.md, production/backend/network sources, source_frozen.json, the exact client and analysis code, build/runtime and topology records, preflight qualification and traces, both full JSONL files, all per-executor client/server start/terminal/command/output records, observation and bootstrap failures, endpoint and actual host journal receipts.

The production diff from bd39e59 to 81baa94 is empty for executor/, bpf/, Makefile and bench/resident_dispatch.py. This run therefore compares the unchanged admitted implementation, not a source repair fitted to its observations. Current main remained the frozen checkpoint during review.

Each model has exactly 10 normal executors, 40 cells, 2,560 measured requests and 83,200 measured output tokens, plus 80 checked one-token warmups. The complete matrix is 20 executors, 80 cells, 5,120 measured requests and 166,400 output tokens, plus 160 excluded warmups. Both model raw files have their full terminal event, no failure/excluded row, and actual server and client subprocess exit 0. Aggregate request/cell/client rows are exactly equal to archived per-executor client stdout; server receipts are exactly equal to archived actual server terminals. A client-written success event alone was not treated as an owning process exit.

Each model uses five paired process blocks with the exact alternating order: loop/native, native/loop, loop/native, native/loop, loop/native. Both paths use the same cell rotation within each block: the four admitted gen/concurrency cells rotate by pair modulo four. Every measured cell has indices 0..63 exactly once and 16 requests per literal prompt. Every executor has eight checked gen1 warmups outside measured cells. No negative block, high-latency sample or post-disconnect row was removed.

## Numerical fidelity and metric reconstruction

The frozen reference file is byte-identical to the0045 asset. Qwen has17 prompt/gen keys with22 complete sequences; Smol has17 keys with19 sequences. I independently checked every warmup and measured reply against the exact complete frozen sequence set for its literal prompt and generation length, and checked that logged input IDs equal the selected prompt. No reference expansion, tokenwise union or post-hoc expected output exists.

This is finite whole-output-set agreement, not exact replay of current ordinary batching/KV history, which is unobserved. Previously qualified alternate trajectories can pass this oracle. There is no universal numerical correctness, task-quality, arbitrary-input or deterministic transport-equivalence proof.

The client request() and connect() functions are byte-verbatim source-native functions from bench/resident_dispatch.py. Socket creation and lane/barrier setup precede timing. Each request records send-start and complete-token receipt arrivals on the client's own monotonic clock. I independently recomputed TTFT, completion latency and TPOT from those timestamps; arrival count, monotonicity and generation lengths all pass. No server/GPU/client clock subtraction occurs. Multiple tokens can share a recv timestamp, so TPOT describes client delivery/coalescing rather than an individual GPU-token clock.

I independently reconstructed each cell's throughput from its earliest measured send-start and latest output arrival and verified indices, prompts, first/last bounds and output counts. I reran analysis.py without serving: both outputs replay byte-identically after only normalizing the input path. I also separately reconstructed process-block TTFT/TPS differences directly from raw arrival timestamps, confirming every archived paired difference and interval to numerical precision. Five paired process blocks, not thousands of individual requests, are the statistical units. The intervals use nominal two-sided t95 df4 critical2.7764451051977987; there is no familywide, equivalence or zero-effect inference.

## Matched computation, real topology and mechanisms

Client receipts place the disposable Python client Pod on g10 at10.42.6.216 and the original GPU Workspace on lab at10.42.1.238. The source-native clients target that actual Workspace Pod address. The route uses the existing flannel.1 overlay. This is real different-node Kubernetes TCP, not loopback, a demonstrated direct ConnectX path, NIC bypass or a GPUDirect claim. Actual client imageID and Pod identities are retained. The placement predicate excludes the original Workspace node without fixed hostname pinning.

Both paths use the same pinned model revisions, FP16 upstream vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0 backend, captured query1..64/batch1..8 graphs, model/KV precision, literal prompts, packed prefill and complete-prefix release source policies. Both ordinary timing binaries are untraced; the preflight is deliberately straced and is not used as full-run performance.

The loop and native nominal completion periods are both60000ns. Native genuinely accepts/receives/sends requests and its source and actual logs engage epoll_pwait2 with that timeout. The selected preflight strace does not include epoll_pwait2, so it supplies no direct wait-syscall-count proof. Native is a credible efficient same-compute alternative, not a deliberately busy userspace baseline or failed interface counted as a candidate win.

The preflight loop has one steady io_uring_enter between ready and SIGTERM, followed by a separate cleanup ENTER. Bootstrap setup calls precede that interval. No steady userspace request socket operation appears in the qualified trace. Worker-task snapshots contain no SQPOLL task, and source flags select SINGLE_ISSUER/DEFER_TASKRUN rather than SQPOLL. Full timing runs reuse that unchanged qualified mechanism; they are not independently syscall-traced. Userspace CUDA/bootstrap/control threads still exist, and the GPU io_network controller remains part of the candidate. Do not call this elimination of all CPU/GPU transport overhead.

All10 full loop terminals independently pass accepted=closed=19; received=completed=head=264; admitted=retired=264; no aborted, pending, transport error, reserved, dropped or transport overflow. SQ head=tail and CQ head=tail drain independently, with no requirement for SQ indices to equal CQ indices. Native published=completed=264 and rejected=0. Model graph_error and model trace_overflows are0 throughout.

There is a real diagnostic limit: every full loop executor has trace_count=264 and trace_overflow=136 because its IoStats reply record array holds128 entries. Those are truncated reply diagnostic records, **not** dropped serving replies or CQ overflow. All264 requests are present in client raw output and completion counters. Do not report all overflow counters zero or claim a complete per-reply server diagnostic trace. Current batch/KV histories remain unobserved.

Matched upstream model computation and identical dispatcher source/policy do not mean all machine code is byte-identical. Direct cuobjdump of the current ordinary libraries shows common dispatch SASS bodies of428846 versus425116 characters for loop/native, with compiler-generated instruction/register/layout differences. Their dispatch source has no transport conditional inside the algorithm. This does not reveal a source arithmetic unfairness, but it prevents a byte-identical compiled-dispatch claim. The candidate additionally executes io_network, real batch/launch trajectories differ, and equal nominal wait periods do not make wake policies identical. This comparison cannot attribute effects exclusively to eBPF, syscall removal or one polling factor.

## Full observed numbers

Means below are loop / native. TTFT, completion and TPOT are milliseconds; output TPS is tokens/s. TPS means average the five cell values rather than pooling all intervals. Pooled quantiles remain descriptive.

| Model | gen/c | TTFT | Completion | TPOT | Output TPS |
|---|---|---:|---:|---:|---:|
| qwen | 1/1 | 3.422434 / 3.418743 | 3.422434 / 3.418743 | — / — | 286.135531 / 286.473022 |
| qwen | 64/1 | 3.255658 / 3.359546 | 81.189987 / 81.359418 | 1.237053 / 1.238093 | 787.304398 / 785.684316 |
| qwen | 1/8 | 4.003628 / 3.920503 | 4.003628 / 3.920503 | — / — | 1869.294094 / 1891.991671 |
| qwen | 64/8 | 4.431863 / 4.025878 | 118.820177 / 118.412540 | 1.815688 / 1.815661 | 4288.188620 / 4316.247740 |
| smol | 1/1 | 3.146517 / 3.169289 | 3.146517 / 3.169289 | — / — | 310.192337 / 308.046799 |
| smol | 64/1 | 3.050300 / 3.104016 | 49.546347 / 48.753358 | 0.738032 / 0.724593 | 1289.280843 / 1310.208173 |
| smol | 1/8 | 3.529004 / 3.596948 | 3.529004 / 3.596948 | — / — | 2124.569675 / 2030.650714 |
| smol | 64/8 | 3.516338 / 3.591750 | 100.425795 / 99.666248 | 1.538245 / 1.524992 | 5020.916572 / 5016.229532 |

## Primary and secondary effects

All four predeclared primary intervals cross zero. The Qwen point estimates favor native; the Smol primary point estimates favor loop. Neither pattern supplies reliable superiority, equivalence, zero-effect or a composite win.

| Model | gen/c | Metric and positive direction | Paired mean | Nominal t95 interval |
|---|---|---|---:|---|
| qwen | 1/1 | native−loop TTFT **primary** | -0.003691 | [-0.126505, +0.119122] |
| qwen | 1/1 | loop−native TPS secondary | -0.337491 | [-10.910882, +10.235899] |
| qwen | 64/1 | native−loop TTFT secondary | +0.103888 | [-0.037154, +0.244930] |
| qwen | 64/1 | loop−native TPS secondary | +1.620082 | [-0.929407, +4.169571] |
| qwen | 1/8 | native−loop TTFT secondary | -0.083125 | [-0.220114, +0.053863] |
| qwen | 1/8 | loop−native TPS secondary | -22.697577 | [-67.126510, +21.731356] |
| qwen | 64/8 | native−loop TTFT secondary | -0.405985 | [-1.286114, +0.474144] |
| qwen | 64/8 | loop−native TPS **primary** | -28.059120 | [-76.190291, +20.072051] |
| smol | 1/1 | native−loop TTFT **primary** | +0.022772 | [-0.033461, +0.079005] |
| smol | 1/1 | loop−native TPS secondary | +2.145538 | [-3.527976, +7.819052] |
| smol | 64/1 | native−loop TTFT secondary | +0.053717 | [-0.117043, +0.224476] |
| smol | 64/1 | loop−native TPS secondary | -20.927330 | [-24.437698, -17.416961] |
| smol | 1/8 | native−loop TTFT secondary | +0.067944 | [-0.293208, +0.429095] |
| smol | 1/8 | loop−native TPS secondary | +93.918961 | [-112.589447, +300.427369] |
| smol | 64/8 | native−loop TTFT secondary | +0.075412 | [-0.372269, +0.523093] |
| smol | 64/8 | loop−native TPS **primary** | +4.687041 | [-43.215784, +52.589865] |

The important secondary loss is Smol gen64/c1 output TPS: loop−native =−20.927330 token/s, nominal interval[−24.437698,−17.416961], negative in all five blocks. Separate timestamp reconstruction also gives native−loop completion =−0.792989ms, interval[−0.922043,−0.663935], and TPOT =−0.013440ms/token, interval[−0.016445,−0.010434]. These are concordant observed delivery regressions, not predeclared primary confirmations and not clean causal effects given the known host instability.

Qwen gen1/c1 TTFT/TPS, gen1/c8 TTFT/TPS and gen64/c8 TTFT/TPS/completion/TPOT have unfavorable loop point estimates; their intervals cross zero. Smol gen64/c8 completion and TPOT also have unfavorable loop means despite its slightly favorable primary TPS mean. Report these rather than selecting only favorable secondary cells.

Tails and outliers remain present: Qwen loop gen64/c8 TTFT p99 is14.900516ms versus native10.299882; completion p99 is134.882691 versus129.250755. Smol loop gen64/c1 completion p99 is56.786113 versus50.747700, TPOT p99 .768669 versus .754399. These descriptive quantiles have no declared paired tail interval. The Qwen primary TTFT paired differences are[−.019775,−.086560,+.167720,−.039784,−.040057]ms; its TPS differences are[−91.627463,−12.162597,−28.455808,+12.728286,−20.778018]. Smol primary TTFT differences are[−.024904,−.028707,+.054889,+.057403,+.055180]ms; TPS differences are[+40.074553,+35.078741,+13.895641,−11.816304,−53.797428]. Mixed directions are retained.

Extreme observed TTFT values include Qwen loop gen64/c8 pair0 requests48/52 around15.28/15.29ms, Qwen native gen64/c1 pair0 request41 at12.799948ms, and Smol native gen64/c8 pair2 request20 at20.389334ms. Their causes are unproved. No outlier trimming, selective blocks or replacement estimate is justified.

## Deviations, host fault and what the receipts establish

The native preflight wrapper initially omitted source-native post-detach removal of three owned pins and failed before model launch or any native client sample. Its traceback remains archived. Adding those existing pin removals repaired the adapter; the previously complete candidate preflight was preserved. This did not alter timing, output oracle, production source or sampled model behavior. Both actual preflight paths then completed80 total requests/2096 tokens including16 excluded warmups. A Windows command-line length error occurred while transferring already-complete client artifacts; chunked transfer preserved the original logs without a serving rerun.

After12 full executors, Cloudflare SSH failed with a websocket bad handshake. Parent reconnection_observation.md preserves observed READY=True, original server PID296241 live and no server terminal, followed by absent client_started before launching the client through the existing Kubernetes path. The earlier observation RPC stream was not independently archived, and the exact failure instant is unrecorded. Actual start/terminal records retain the same PID296241; the aggregate has exactly one client and executor for that case. There is no evidence of a benchmark replacement, no inference of model death from SSH failure, and no sample exclusion. Controller failure alone is not the authoritative server terminal.

The host kernel_journal.txt/json is a real nonempty2957-line bracket05:11:22–05:40:30 UTC. It contains global OOM, kills of other-workload Lean49PreparedB processes near99GB RSS, and EXT4/I/O errors and aborted journals on transient device names sdt/sdn at05:28:38. Device/workload mapping and the fault cause are not established by this review; do not blame this benchmark, infer which PVC those transient names represent, or dismiss the fault as unrelated to timing merely because other processes were killed.

The burst lies inside the lifetime of Smol native pair1 server PID296241,05:27:34–05:31:00. Parent reconnection observations bound its first client launch after05:29:10, hence after the recorded burst, rather than overlapping measured requests with it. Qwen completed by05:24:22 and Smol pair0 native by05:27:18. Nonetheless the full Smol matrix spans a known resource-state discontinuity, including memory-pressure buildup and subsequent fault/recovery; absence of direct burst overlap does not prove unaffected latency. Client monotonic timestamps are from a different machine and cannot be directly aligned to lab UTC without an actual clock mapping.

Every own actual server/client child still completed normally and finite outputs/counters passed. Those support functioning service under the observed conditions. They do not restore stable-host performance validity. Keeping all rows avoids post-hoc exclusions but does not remove environmental confounding. The root must retain this as a known fault-qualified observational comparison, with the observed negative and inconclusive values, rather than an unqualified clean comparison or a clean causal proof of the Smol regression. The journal has no selected GPU Xid/Oops/panic evidence; that narrower absence is not proof of no GPU/host interference.

full_endpoint.json retains the original boot, frozen source, base Torch2.14.1+cu130/Transformers5.19.0 and no own module/pins/GPU app at its observation time. It is an endpoint only. Existing unrelated Jobs and Workspaces were not stopped. Final owned Job/runtime/build cleanup and publication are still the parent's responsibility and were not certified by this review.

## Claims and limits

The admissible new result is finite real cross-node optimized model service using the module-free kernel loop without a steady userspace request worker in its qualified mechanism, plus a fully retained observational comparison that establishes no primary performance advantage. It is binary-token Content-Length HTTP, not text/JSON tokenization/detokenization or ordinary vLLM serving API.

There is no measured remote per-cell server CPU, total CPU, energy, SLO goodput, open-loop capacity, NIC-to-GPU instruction delay, GPU-ready-to-TX attribution or host-induced-bubble decomposition here. Prior local CPU means cannot be relabeled remote measurements. The same-compute native baseline is not an external SOTA server comparison. This experiment does not prove generic backend portability, all requested full-objective stages, broad performance novelty or clean absence of host interference.

No blocking raw reconstruction, output-set, baseline-engagement or matrix-completion defect was found. The material blocker to a **clean performance interpretation or further serving mutation** is the actual host/storage fault, not missing stylistic polish or extra baselines. Preserve this experiment and its changed evidence, finish honest documentation/restoration, diagnose the fault, and continue the original full objective without declaring it achieved.
