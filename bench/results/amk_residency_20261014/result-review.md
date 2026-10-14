# Fresh independent result review: AMK residency counterfactual

Observation: 2026-10-14 UTC. Reviewer used the research-experiment-design RESULT REVIEW workflow in the original bpfusion-dev Workspace. This report changes only the caller-owned TEMP result-review.md; no production source, plan, reference pool, paper or runtime policy was changed and no new experiment was executed. Read-only native image disassembly/resource inspection and independent Python recomputation were used.

## Separate judgments

- Run status: **valid** for the completed, predeclared finite-output-set ordinary native-plus-park versus native counterfactual and its delivery comparisons. All30 executors and60 measured cells completed. The planned authenticated per-bank/position/cell timeline is unsupported and closed; it is not a completed timeline result.
- Tested hypothesis: **inconclusive as the full conjunctive hypothesis** that additional resident work suppresses cooperative-model overlap and thereby reproduces c8 loss. Its ordinary throughput sufficiency component is supported for this specific added control: native-plus-park loses about49% throughput without handling network traffic. The mediator, SM occupancy and equivalence to io_network's cause are not established.
- Research value: **supporting**. The previously absent non-network intervention changes the driver/backend implementation decision; ordinary model bootstrap, graph catalogue packaging and exit receipts alone are dependencies.
- Paper impact: **mechanism or workload boundary**, adding evidence toward the retained performance/reuse question. This is not a direct thesis challenge and does not answer the whole RQ.
- Next paper decision: retain the ordinary counterfactual as evidence that this concrete additional resident kernel/control collectively is sufficient to degrade c8 delivery; prioritize investigation of the driver/backend scheduling boundary. Do not publish suppression-of-model-overlap, SM-occupancy causality, or a transport-specific explanation. Close this unchanged matrix. A future source-backed intervention should supply a distinct causal discriminator and its own admission, rather than repeating the same matrix or tuning model arithmetic. Keep the previously faster vLLM backend and prior0048 result unchanged.

Retained question: can the CPU request path be removed while retaining efficient reusable real-model GPU execution? No formal RQ is invented, split or renamed. The current hypothesis concerns this constructor, not universal CPU-free model serving.

## Evidence and run completion

Reviewed plan.md, all of plan-review.md including the same-review follow-up, execution-notes.md, both failed preflight receipts and repairs, full.command.json/run.py, full.exit.json, full driver stdout/stderr, all full.jsonl events, all30 stdout files, all15 trace.json.gz files and graph_catalogue.json files, analysis.py and full.analysis.json, frozen references and previous0045/0048 evidence, adapter.py, residency_serving.py, qwen_graph_park.cu and Makefile.park, actual AMK builder/bootstrap/dispatcher, native userspace_tcp.h/io_uring_tcp.h, upstream persistent loader and pinned source, package/build records, and full.host_before/mid/after.json. interpretation.json was not used as an oracle.

Data home: /tmp/bpfusion-amk-residency-tkdf_2wx. Archive: /workspaces/repository/bench/results/amk_residency_20261014. Serving source frozen before collection: eb92fffe67daf588f711979e60cfe851b5a3e353. Full command began emitting at09:51:04 UTC and terminal raw success is09:57:47; wrapper exit0 receipt is09:57:48.322325 UTC. Archive publication after collection does not change the frozen serving-source revision.

Independent record checks find30 each of start, ready, executor, verified and successful executor_terminal;60 measured cells;720 complete request records consisting of480 measured requests/30720 measured tokens and240 excluded checked gen1 warmups. There is one terminal exit0. Each executor has24 requests/1032 output tokens. There are no full-run failed/excluded executors or favorable substitutions. Preflight1/2 failed graph dependency introspection, not output correctness; preflight3 completed six paths. The official dependency-query repairs and unsupported-identity follow-up preceded full collection. No metric, oracle or workload was relaxed after observing the full result.

Actual command is the recorded temporary runtime Python executing residency_serving.py --loop-comparison --untraced --reference-path frozen_references.json --model the pinned cached Smol snapshot --output full.jsonl, cwd /workspaces/repository, with exact bindings in full.command.json/environment.json. Despite the inherited --untraced option name, it disables project BF_TRACE/current-history replay; ordinary/profiled paths are explicitly selected by BF_DIAGNOSTIC_PROFILE and the standard profiler still runs on all15 profiled children.

Each cell contains exactly indices0..7, two copies of each of the four same literal prompts, gen64 and c1/c8. Prompt lengths are5,8,5,2. All paths use the source-native binary-token HTTP connect/request implementation, pre-opened persistent connections and identical client TCP_NODELAY; connection/thread creation and text tokenization are outside reported request windows. The c8 cell is one eight-client wave and c1 is eight sequential requests. Path order uses the first five deterministic permutations, cell order alternates by block and instrumentation order reverses by block. This is ordered counterbalancing, **not randomization** or a continuous-isolation guarantee.

## Real-model/output and lifecycle qualification

Actual cached HuggingFaceTB/SmolLM2-135M snapshot is93efa2f097d58c2a74874c7e644dbc9b0cee75a2,30 layers, h576, vocabulary49152. All conditions load the same checkpoint as FP16 and use pinned RightNow-AI/AutoMegaKernel884534c4d2dbed4381576f81a79ae97feca53c34. Read-only byte comparison against upstream.tar.gz finds no changes in103 upstream .py/.cu/.cuh/.h/.cpp source files. Graph builder fixes K=1 for safe per-token publication; this is not the upstream whole-request K-token single-launch implementation. Eight private KV/input/output banks and190 graphs per bank use the discovered actual170-SM target, cpasync0, model grid170/block256 and4096-byte requested dynamic shared memory. Reuse is real graph/bank reuse for these finite requests, not generic serving qualification.

Every one of720 outputs has exactly the requested number of tokens and arrival timestamps; arrivals are nondecreasing and after request start, tokens are in vocabulary, and each whole sequence belongs to the unchanged independent pre-observation pool. frozen_references.json is byte-identical to0045's artifact. No tokenwise mixing or pool expansion occurred. Each condition has one distinct complete sequence for each of the four prompt/gen1 and four prompt/gen64 keys in this run. This finite result does not establish all-input parity, exact eager-HF semantics, current bank/KV trajectory replay or task quality.

The old stronger exact diagnostic remains **failed**: megakernel_reuse_20261014/strict2_native.exit.json records exit1 at08:12:00.457550 UTC. After5000 empty connections, case2, Write a short greeting,gen64, third fragmented binary request differs at zero-based token16 (AMK2683 versus eager-HF504). The later finally-block expected-workload assertion is secondary. Its server cleanly completes3 requests/192 tokens, launches1,graph_error0, all eight AMK update errors0; those counters do not negate numerical failure. native170_comparison.json shows both official per-step and persistent AMK produce the same server sequence and same token16 mismatch. This narrows that historical case to upstream computation/runtime behavior without identifying its floating-point cause. This run does not repair it or rerun the old strict loop case.

All30 current children exit0 with one root launch,1032 device graph launches, eight banks,max_active8,graph_error0 and eight zero argument-update errors. max_active counts dispatcher admissions/launches, not simultaneous cooperative kernel execution. All20 native/native-plus-park children report accepted10,published24,completed24,rejected0. All10 loop children report accepted=closed10,received=head=completed24,sends1032,bytes6032,max_requests=max_connections8; pending,error,reserved,dropped,overflow,aborted,trace_overflow all0 and trace_count24. SQhead=SQtail and CQhead=CQtail independently; unequal SQ versus CQ counts are expected with multishot timeout completions, not an emptiness failure. All10 attach,stats,cleanup_stats,detach commands exit0. Both stats snapshots have head24, reserved0 and all eight slots FREE. Normal loop cleanup releases ring/connections/buffers; park stop reads the existing mapped stop field with system acquire, exits before cudaDeviceSynchronize returns, stream destroy occurs before page unregister/unmap. No normal stop was replaced by timeout/kill acceptance.

The full run does not rerun fragmentation, invalid-token rejection, half-close, reset or stop-during-generation coverage for the new park control. Prior common-runtime0048 protocol/lifecycle qualification remains historical supporting evidence for the unchanged native and loop code, with its finite-set scope. Current source and task snapshots support the intended loop mechanism, but this full timing run is not a new all-thread syscall trace proving complete CPU-path removal. Kernel TCP/eBPF/softirq CPU work remains real CPU work.

## Baseline fairness and control engagement

The single main baseline is efficient native TCP with the same AMK resident model graphs, epoll_pwait2 nominal60000ns completion waits, normal TCP buffering, identical model/checkpoint/banks/compute and fixed workload. Its native mechanism engages: real userspace accept/recv/send, all requests completed, c8 actually reachesmax_active8, no model or transport failure. It is a credible competing answer to this within-AMK driver question, not a failed proxy or artificial busy-wait baseline. A second general serving baseline is unnecessary for this counterfactual; prior0048's vLLM comparison is retained rather than being silently replaced.

Native-plus-park is a resource/null control, not an external baseline or real TCP handler. Diff against original qwen_graph.cu adds only resident_control, its one-CTA/one-thread nonblocking default-priority stream launch and teardown. The existing stop lifetime and unchanged native transport remain. Normalized native dispatch SASS contains1536 nonempty instruction/encoding lines and is identical across native,park andloop images; model arithmetic/source are unchanged. Park requires -Iexecutor because the source resides in TEMP; CUDA architecture/optimization/compiler flags otherwise match native. This supports the control attribution without assuming identical whole-binary layout or host transport glue across loop/native.

All five park traces observe one resident_control activity at grid[1,1,1]/block[1,1,1]; all five loop traces observe one actual io_network activity at the same geometry; both span the entire observed model-activity session, and native traces contain neither. This establishes launch/presence and duration of the controls, not an SM-residency map. Static cuobjdump reports parkREG8/STACK0/shared0 and io_networkREG40/STACK768/shared0; common dispatchREG38/STACK0/shared0. Runtime profiler reports park16 registers/thread versus io_network40, both shared0. The park static/runtime register discrepancy is retained rather than silently treating the two receipts as identical measurements. The park is not bit-identical to io_network and its system-scope polling/mapped traffic, sleep instructions and launch can matter collectively. A positive intervention demonstrates sufficiency of this control as implemented, not occupancy alone or the exact cause of the real network loop.

Environment is Python3.12.3/GCC13.3.0, Torch2.13.0+cu129,Transformers5.17.0,vLLM0.31.0 present in the common temporary runtime; vLLM is not a measured path here. Actual /usr/local/cuda/bin/nvcc is13.0/V13.0.88. RTX5090/KMD610.57.04 and CUDA UMD13.3 are recorded; trace metadata reports driver13030,runtime12090,CUPTI28 and installed CUPTI package12.9.79. These distinct compiler/runtime/driver versions must not be conflated.

## Metric recomputation and uncertainty

Independent arithmetic from request arrivals reproduces all60 cell throughputs and all120 stored TTFT/completion means in full.analysis.json; all720 per-request TTFT/completion/TPOT fields agree. Every process CPU delta equals after-minus-before and its bracket surrounds the entire client sampling interval. The existing analyzer's primary block differences and t95 agree (its rounded t4=2.776445105 affects only about1e-10).

TPS = measured output token count / (last measured token arrival minus first measured request send). TTFT = first arrival minus send; completion = last arrival minus send; TPOT = (completion-TTFT)/(64-1). Client recv chunks may assign one timestamp to multiple tokens; TPOT is a client endpoint statistic, not GPU token-computation time. These client terms use [official vLLM benchmark terminology](https://docs.vllm.ai/en/stable/benchmarking/cli/), while the finite cell window is explicitly the local source-native convention.

All means below are means of the five process-block cell means; latency in milliseconds, CPU is executor-process milliseconds per measured output token. CPU excludes client, total host, RX/softirq/BPF and other kernel TCP costs; kernel_tx_cpu_ns is0 because the custom TX module is absent, not because TCP uses zero CPU.

| Condition | c | TPS | TTFT ms | Completion ms | TPOT ms | Executor CPU ms/token |
|---|---:|---:|---:|---:|---:|---:|
| amk_userspace_ordinary | 1 | 165.083649 | 18.249451 | 387.645770 | 5.863434 | 0.113130 |
| amk_userspace_ordinary | 8 | 309.140757 | 76.763140 | 1652.564841 | 25.012725 | 0.062390 |
| amk_park_ordinary | 1 | 164.318631 | 18.348098 | 389.451086 | 5.890524 | 0.110049 |
| amk_park_ordinary | 8 | 157.765344 | 134.764113 | 3238.916568 | 49.272261 | 0.122221 |
| amk_uring_loop_ordinary | 1 | 164.341743 | 18.329069 | 389.397679 | 5.889978 | 0.151264 |
| amk_uring_loop_ordinary | 8 | 157.769889 | 142.947713 | 3237.313627 | 49.116919 | 0.156574 |
| amk_userspace_profiled | 1 | 164.880745 | 18.268625 | 388.120891 | 5.870671 | 0.115152 |
| amk_userspace_profiled | 8 | 309.901609 | 74.508877 | 1648.949000 | 24.991113 | 0.060763 |
| amk_park_profiled | 1 | 164.111622 | 18.391207 | 389.942197 | 5.897635 | 0.108791 |
| amk_park_profiled | 8 | 157.521248 | 135.142072 | 3244.673866 | 49.357648 | 0.122416 |
| amk_uring_loop_profiled | 1 | 164.071865 | 18.372511 | 390.037036 | 5.899437 | 0.152733 |
| amk_uring_loop_profiled | 8 | 157.392214 | 136.891410 | 3245.639079 | 49.345201 | 0.159050 |

The predeclared primary ordinary park-minus-native c8 effect is **-151.375413 tokens/s**, nominal paired t95 df4 **[-152.840219,-149.910607]**. Its five signed differences are[-151.619264,-151.127902,-151.169466,-153.120608,-149.839823]. All five are negative; none excluded. Mean paired percentage loss is48.965910%, nominal interval[48.715518,49.216301]; this secondary ratio interval uses per-block ratios, not endpoints obtained by dividing the primary interval. Native c8 is309.140757,park157.765344; ordinary loop157.769889 reproduces the earlier loss direction. The larger current native mean than0048 is a separate finite run, not an improvement claim replacing0048.

| Ordinary paired contrast | c | Mean TPS difference | Nominal t95 lower | Upper |
|---|---:|---:|---:|---:|
| park-native | 1 | -0.765018 | -0.851178 | -0.678858 |
| loop-native | 1 | -0.741906 | -0.831871 | -0.651941 |
| park-loop | 1 | -0.023112 | -0.086847 | 0.040623 |
| park-native | 8 | -151.375413 | -152.840219 | -149.910607 |
| loop-native | 8 | -151.370868 | -152.779568 | -149.962168 |
| park-loop | 8 | -0.004545 | -0.160320 | 0.151230 |

Only park-native c8 is the predeclared primary. c1 and loop rows are controls/descriptive supporting contrasts; no multiple-primary or equivalence claim follows. The park-loop interval crossing zero does not prove equivalence or common mechanism. Five process blocks, not480 individual requests, are the replication unit. Nominal t intervals assume the paired differences are sufficiently independent/regular; five deterministic blocks cannot diagnose temporal dependence or deliver robust tail uncertainty. There are no SLO,capacity,representative-load,steady-offered-load or power conclusions.

## Instrumentation transfer

All15 profiled children have device_graph_status,driver_status,hardware_trace_status0 before CUDA initialization, then standard torch.profiler CPU+CUDA capture around serve. Ordinary/profiled children share the same adapter and library for each path; extra catalogue/profiling work happens only when enabled. Full completion and output qualification pass in both states.

Independent paired differences below are profiled-minus-ordinary; t95 df4. Profiling has measurable throughput/completion perturbations, especially park andloop, even though the large c8 between-condition pattern is preserved.

| Path | c | TPS difference [t95] | Completion ms difference [t95] | TTFT ms difference [t95] |
|---|---:|---|---|---|
| amk_userspace | 1 | -0.202903 [-0.298917,-0.106889] | 0.475121 [0.250410,0.699831] | 0.019174 [-0.015603,0.053952] |
| amk_userspace | 8 | 0.760852 [-0.951381,2.473085] | -3.615841 [-9.999928,2.768246] | -2.254263 [-14.192319,9.683793] |
| amk_park | 1 | -0.207009 [-0.246874,-0.167144] | 0.491111 [0.395694,0.586527] | 0.043110 [-0.000662,0.086882] |
| amk_park | 8 | -0.244096 [-0.368180,-0.120012] | 5.757298 [0.377387,11.137210] | 0.377959 [-10.182791,10.938709] |
| amk_uring_loop | 1 | -0.269877 [-0.373705,-0.166050] | 0.639357 [0.393732,0.884982] | 0.043441 [-0.010781,0.097664] |
| amk_uring_loop | 8 | -0.377675 [-0.689056,-0.066294] | 8.325451 [1.817001,14.833901] | -6.056303 [-13.236900,1.124293] |

Small overhead relative to the49% ordinary intervention does not authenticate per-bank concurrency or prove profiled-to-ordinary mechanism equivalence. Crossing-zero TTFT/native-c8 intervals do not prove no overhead. Source-native standard capture is appropriate in principle: [NVIDIA CUPTI usage](https://docs.nvidia.com/cupti/12.9.1/main/main.html) distinguishes concurrent activity from serializing collection. This export does not expose an independently authenticated concurrent-collection-kind/drop-status receipt; no exported warning was found, but absent warnings are not a dropped-event guarantee. No serial or synthetic fallback was substituted. Ordinary numerical throughput stands independently of the profile.

## Timeline failure and exact causal limits

Every one of15 source catalogues has1520 graph entries,17648 unique cooperative source model nodes, correct bank/index coverage and ordered source positions. Every trace has1128 name-filtered amk_megakernel_persist activities, all grid[170,1,1]/block[256,1,1]. Expected count from real inputs is40 warmup model calls plus2*(40+8*63)=1088 measured calls, total1128. prepare1128 and selected1032 appear in every trace; dispatch appears586 times except native block1 with585. This variation is retained and not converted into a scientific overlap difference. Totals are16920 model activities,16920 prepare,15480 selected and8789 dispatch; five actual park andfive actual network activities are separate.

Source model attributes mark cooperative and device-updatable nodes. Actual trace graph/node IDs identify instantiated graphs; **0 of1128 activity node IDs matches the17648 catalogue IDs in every profile**. Example first activity graph1529,node6567004995584 cannot be authenticated to source bank/prefill/decode position. Instantiate activities retain cbid/correlation only, without the source/exec graph relation. [NVIDIA kernel activity metadata](https://docs.nvidia.com/cupti/api/structCUpti__ActivityKernel8.html) documents the graph/node identity fields; matching name,geometry,count or numeric ID patterns is not a replacement for the missing relation.

Therefore there is no validated per-bank sequence, private-bank reuse trajectory, measured-cell grouping, launch-type attribution or promised model-overlap result. Missing/duplicated/wrong-position events cannot be ruled out by aggregate count. No ID offset is inferred. analysis.py's unused interval_metrics function would compute peak overlap, sum-duration/union and session span mathematically, but it is not invoked for the report and cannot fix identity. Its ratios are interval diagnostics, not utilization or SM occupancy. The trace's estimated occupancy17%,activeBlocksPerMultiprocessor2,106 model registers and37520 shared-memory field are profiler/static estimates, not measured residency.

For audit transparency only, an independent name-filtered **whole-session** sweep gives maximum overlapping intervals3 in each native trace and2 in each park/loop trace; means of all1128 name-filtered kernel durations are about5.744..5.765ms native,5.762..5.764ms park and5.763..5.772ms loop. These include warmups/both cells and unsupported identities, and are not accepted paper evidence for causal model-overlap suppression or cell-level per-model slowdown. Their existence does not upgrade the full hypothesis verdict. No client TTFT-minus-model interval is labeled pure network time or converted using an unsupported GPU/CPU offset.

The same-review pre-full fallback explicitly retained the unchanged primary ordinary intervention and closed the unsupported timeline claim. This review accepts that separation; it does not retrofit a weaker full hypothesis to call the planned mechanism proved.

## Host warnings, cleanup and remaining scope

Actual host brackets are09:49:22.289403,09:52:28.455846 and09:59:44.568511 UTC. All share boot04dc0087-5ccc-4c46-9997-b9a92f0e5167. Selected journal line counts are16,20,31:15 new NVRM refcntRequestReference_IMPL status0x00000056 warnings during the full run. No selected Xid/reset/OOM/storage lines appear. These are filtered observations, not a clean journal, a harmless-warning finding or evidence that warnings cannot affect scheduling. Compute-app listings are empty at observed brackets; they do not establish continuous isolation. MemAvailable is119698260/118729280/119794504kB, and GPU memory returns to15MiB at the final bracket. No reboot,driver mutation,clock/policy repair or competing session change was part of this review.

The source-frozen data and report should be archived before owned TEMP/build removal. Normal per-child serving resources are quiesced and raw cleanup receipts pass, but experiment-wide TEMP/build restoration intentionally awaits this completed review. This report does not itself certify a later removal or the caller's claimed default-library inode/size; verify those in the final restoration receipt. Preserve original Coder/PVC/cache/base packages, existing default library and unrelated WIP. The caller remains responsible for evidence-backed final cleanup and publication through main.

Accepted paper sentence: adding this specific non-network one-CTA resident control to otherwise identical native AMK serving reduces ordinary gen64/c8 finite-wave throughput from309.141 to157.765tokens/s, with mean paired difference-151.375[-152.840,-149.911] across five process blocks. This establishes a concrete constructor/resource-control sufficiency boundary; the authenticated overlap mediator remains unavailable.

Rejected expansions: occupancy alone explains the loss; actual io_network loses for precisely the same reason; removal of the CPU request path is generally efficient; arbitrary model/KV/eager-HF parity passed; profiling is equivalent to ordinary serving; native-versus-park-loop equality is proved; this is a whole-RQ answer or direct thesis challenge. The original objective remains open.
