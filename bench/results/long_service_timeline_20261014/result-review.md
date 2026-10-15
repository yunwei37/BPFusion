# Fresh result review: long-output GPU service-time discriminator

Observation: 2026-10-15T03:19:04.081661+00:00. Independent CPU-only review; the only written artifact is this report. No serving/model/GPU run, build, cleanup, recipe/source edit or Git action.

## Separate judgments

- **Run status: invalid for the planned integrated GPU decomposition.** Collection is terminal, not a partial prefix: all40 drivers, serving children and fresh unprofiled replay children exit0; full.exit.json is0 at2026-10-15T00:56:35.788067UTC. The fixed full analyzer exits1 at03:13:24.642583UTC. Smol loop/profiled p2 and p4 each lack3 model-kernel activities, violating the plan's exact-coverage condition. All40 client and logical-trajectory checks remain valid within the instrumented finite-workload scope;18 profile cells pass independent complete-coverage/identity/serial checks. Do not label this a repaired full pass.
- **Tested hypothesis: inconclusive.** The experiment does not establish that longer actual per-round model service, rather than altered round histories/availability, explains the ordinary native gap. Qwen has a real profiled-client deficit but mixed model-duration effects and uncertain aggregate differences; the complete five-block Smol duration comparison is unavailable. No exclusive bottleneck follows.
- **Research value: supporting.** It adds previously absent long-output real GPU activities and actual batch/query histories, bounds simple causal stories, and exposes a trace-completeness failure. Completed process/checker counts alone are dependency evidence. This is neither a headline improvement nor decisive implementation-selection evidence.
- **Paper impact: mechanism or workload boundary.** No formal paper RQ/thesis exists here. These data bound the two current reused-vLLM constructors on fixed two-model gen64/c8 HTTP token-ID workloads. They do not directly challenge a universal thesis or settle the retained end-to-end project objective.
- **Next paper decision:** close this diagnostic with its valid-client/invalid-integrated-decomposition distinction. Preserve signed results and failed coverage; make no production/default change and no exclusive model-service/transport allocation. This review does not authorize or require a GPU rerun, new review round, instrumentation layer, bottleneck-specific optimization or idea rewrite. The larger user goal remains active.

## Strongest supported conclusions

All40 measured services deliver the fixed complete output sequences and agree exactly with current admission/history traces and fresh-process reused-graph replay. I independently rebuilt both pre-observation reference pools from their24 recorded historical reference files; both match models.json exactly, and every current cell metadata binding matches that frozen pool. Thus this check is not made circular by accepting current output as its own expectation. The historical pool allows multiple whole sequences, so membership alone would be weak; exact trajectory replay and client/trace identity close that specific ambiguity. This still does not repair the older eager-HF/AMK oracle failure or establish fresh arithmetic/backend fidelity.

Qwen profiled loop-native TPS differences are all negative: -119.450,-58.111,-74.178,-126.689,-143.400tokens/s; mean-104.366, nominal t95[-149.564,-59.167]. This supports a local deficit in the BF_TRACE+profiler condition. Qwen BF_TRACE-unprofiled differences include a positive p3 and have mean-125.667[-366.982,115.647]; that condition does not establish a signed population effect or reproduce an exact ordinary untraced gap. Smol TPS is unresolved in both conditions: unprofiled+1.649[-117.523,120.821], profiled+5.708[-110.903,122.320]. None supports a loop performance improvement.

Qwen's complete five paired profile blocks show union differences+6.441,+40.965,+8.308,+16.571,+10.060ms, mean+16.469[-1.182,34.120]; span-sum+13.227[-4.102,30.556]; epoch+4.647[-5.671,14.965]; inter-round gap-8.580[-25.405,8.244]; within-round gap-3.242[-13.326,6.842]. All planned duration intervals cross zero. Aggregate union is consistently larger descriptively, but is an amount of work across changed round histories, not proof that one matched round executes more slowly. There is no equivalence claim.

The dominant Qwen query0/batch8 stratum has loop-native union differences of-0.001814,-0.000414,+0.001300,+0.002216,-0.000550ms and span differences+0.026020,-0.017828,-0.026512,-0.050885,-0.000751ms. Other shared strata also retain both signs; many prefill/tail strata have only1–5 observations per cell. At p1, loop has295 measured rounds versus native259, including30 query0/batch1 and30 query0/batch7 rounds while native has252 query0/batch8 rounds. This accompanies the largest aggregate union excess+40.965ms although dominant-stratum union is slightly lower in loop. This is evidence of a changed execution trajectory, not isolated arithmetic/resource mediation. Context/KV/history/request identity is not fully matched by query and batch alone.

Smol has more measured rounds in every paired block in both conditions: unprofiled differences+2,+10,+16,+24,+6, mean+11.6[0.861,22.339]; profiled+10,+5,+2,+17,+13, mean+9.4[1.919,16.881]. Yet TPS has mixed signs. Additional rounds alone therefore do not imply a measured throughput loss on these observations. The three complete Smol loop profile cells are descriptive rows, not a substitute three-block experiment; no Smol five-block duration mean/CI is reported.

## Completion, deviations and failed rows

Read the entire current plan, initial PLAN REVIEW and both follow-ups, execution-notes, current/preserved recipes, expanded run commands/statuses, current/frozen source for selected computation/transport, all40 raw clients/model traces/reference files and all20 compressed profiles. Source_frozen.json records main458145f495789f83ff662ec6d45b216c83ff7ae8; the live repository is still that main revision and all12 captured paths are byte-identical to their frozen copies. Original loader/build/setup preservation stats remain equal to preserved_before.json; every raw metadata library size/inode is still equal. Unselected qwen/AMK source snapshots are provenance, not a newly validated backend. No source change occurred in this experiment.

setup.py builds source-native vllm_graph_uring_loop_trace and vllm_graph_user_network_wait_trace privately with nvcc-O3/sm_120 and the recorded common CUDA library; packages are vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0. Both selected libraries have BF_TRACE, BF_PAD_PREFILL and BF_PREFIX_RELEASE. Loop adds BF_URING_NETWORK/BF_URING_BPF_LOOP; native adds BF_USER_NETWORK/BF_USER_NETWORK_WAIT. Both instrumentation states per path use the exact same path library. All raw case adapter/driver/client sources match the current reviewed recipes. Expanded full.commands.json agrees with run.py's deterministic rotated condition order and alternating model order. The actual full wrapper ran23:59:08.607921–00:56:35.800230UTC, roughly57m27s including separate replay bootstraps. A cost estimate is not a deadline.

First preflight is preserved as failed_preflight_1: only2/4 drivers ran, the native/profiled child served16 replies/520tokens and exported its trace, then exited-11 in post-profiler cudaMemcpyAsync/Tensor.copy_. It remains failed, not a native performance outcome. The crash location is observed; the CUDA/profiler/driver cause is not established. The retained core receipt/data should not be silently discarded as successful evidence.

Revision1 changes oracle execution placement. Direct source diff confirms replay.py differs from current production bootstrap only by relocating root and skipping lib.serve; its graph/KV/history/token replay body is identical. Serving adapter removes only the former in-process replay block and emits a marker. All four preflight conditions were rerun in attempt2, and all full cells use the same serving-exit0 then fresh-replay-exit0 requirement. Fresh replay reboots the model state and reconstructs prompts, padding, positions, logical histories and slot/page mapping rather than reusing serving KV memory. It is outside the timed/profiled serving region and launches no second transport service. It tests deterministic reused graphs against actual trajectories, not an independent model implementation. Extra bootstrap can affect later process thermal/cache context; rotation is not proof of neutrality.

Attempt2 finishes4/4 drivers at23:52:53.372789UTC. Its initial CPU analyzer fails because the source-native io_initialize kernel had been omitted from the non-model controller classification. The current narrow fix, diffed against analysis_before_initializer_fix.py.txt, requires exactly one loop/zero native initializer, graph/node0, grid/block[1,1,1], and end before the first model kernel; every model-count/oracle/timing check stays unchanged. Fixed preflight analysis exits0 at23:57:25.558493UTC. This CPU observation correction is scientifically legitimate and is not tolerance for missing records. It neither explains the segfault nor licenses another unknown-kernel exclusion.

The full fixed analyzer stops at the first missing-profile cell, so its previously written timeline files are only a verified prefix, not proof that later cells passed. My independent raw review reaches every cell and finds the additional p4 deficit. Root's later client_analysis.py/full.client.analysis.json is explicitly post-hoc client/logical reconstruction. I independently recomputed the raw rows before consulting that supplement; all40 reported client/round values agree at the displayed precision. The supplement does not repair analysis.py or replace missing duration coverage.

## Coverage limits and durations that cannot be trusted

Smol loop p2 has113944 actual model kernels versus113947 expected; p4 has117217 versus117220. Both graph memcpy counts are exact271/271 and340/340; memset0/0. Both controller sets are as expected, including one source-native initializer and one persistent network kernel. Driver/model trace overflows0 describe their own buffers and do not establish CUPTI completeness. No evidence here establishes why the6 activities are absent. Successful oracle/token execution suggests an observation gap rather than failed delivered computation, but does not reconstruct the missing activity durations.

For both deficient profiles, planned measured model epoch, union, kernel-duration sum, round span/union, within/inter-round gaps, all query/batch activity-duration strata and all paired duration effects involving those cells are unavailable under the agreed count-based grouping method. Do not shift group boundaries, add zero-duration events, infer expected durations from the other path, accept a 3-record tolerance, trim a slow block or average only complete cells to pass. Observed activity sums could be labeled incomplete observations, but they cannot stand in for the planned total durations; this report does not present them as such. Logical round and batch/query counts and independent client timestamps remain valid and are retained.

For the18 exact profiles, all model kernels are partitioned with each actual descriptor's exact recursive count, per-round unique graph/node identity, and serial non-overlap; whole-serve graph memory counts also match. Serial source graph dependencies and dispatch progression support ordered correspondence. The catalogue contains counts, not independently mapped identities of every instantiated graph memory node, so graph memcpy/memset is only whole-serve count coverage, and kernel uniqueness alone is not a new arithmetic oracle. The persistent io_network and dispatch kernels are deliberately separate from model union/span, not silently missing model work. A full graph elapsed time would include more than kernel intervals; these values are accurately kernel diagnostics.

## Baseline fairness, perturbation, uncertainty and scope

Efficient native timed epoll is a credible matched competing constructor and engages its intended path: every native log identifies epoll_pwait2 with the existing60000ns timeout, every TCP result has9 accepted connections,40 published/completed and0 rejected, same resident dispatcher/model graph arithmetic, pinned model, dtype, prompt/output budget, padding and prefix release. It is not a failed interface counted as a loop win, a deliberately busy-poll straw baseline, or stock full-vLLM serving. The loop's selected source uses eBPF sockmap HTTP parsing/shared mmap queue, GPU-owned network progression and a kernel io_uring BPF submission/completion loop; source and successful attach/ring/drain/token receipts jointly support mechanism engagement. The custom bfusion_tx module is absent on this selected path; Linux kernel TCP executes io_uring SEND. Userspace bootstraps, clients and a process blocked/re-entering the kernel loop remain; no inference of zero total CPU work follows from absence of a per-request userspace worker.

All conditions retain BF_TRACE. The unprofiled arm is logically traced and cannot quantify BF_TRACE overhead or be substituted numerically for ordinary untraced0055/0056. Profiling arms successfully enable device-graph collection before CUDA initialization, then driver initialization/HES before context, and profile serving after graph capture; raw setup statuses all0. Current official [CUPTI Activity API](https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html) and [PyTorch profiler](https://docs.pytorch.org/docs/stable/profiler.html) are the implementation precedent; a successful API return does not guarantee complete collection or neutrality.

Profiler-minus-unprofiled TPS point estimates are Qwen loop-46.360[-155.920,63.199], native-67.662[-281.489,146.165]; Smol loop-19.497[-166.189,127.195], native-23.556[-122.893,75.781]. These intervals are not equivalence bounds. Large signed block variation and changed batch histories prohibit exact transfer to ordinary serving or a pure profiler-overhead subtraction. Do not silently drop Qwen p3's unprofiled loop win+137.959, p1 native-unprofiled TTFT5.366ms, p3 native-profiled TTFT4.330ms, Smol p3 loop wins+158.742/+128.476TPS, Smol p4 profiled loss-135.918TPS or either incomplete-profile cell. All remain in the tables. There is no demonstrated outlier cause authorizing exclusion.

Nominal t95 uses five paired process blocks and t(df4)=2.7764451051977987; no pooled-request pseudo-replication, familywise claim, equivalence margin or causal mediation model is introduced. End-to-end TPS is2048 divided by the client first-request-to-last-token window; TTFT/TPOT/completion come from raw client monotonic timestamps with all tokens in one recv sharing an arrival time. Concepts follow [official vLLM benchmark metrics](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics), but the finite binary token-ID HTTP adapter is not an official full-text API or SLO/capacity benchmark. Device durations use a single GPU trace domain; no absolute CPU/GPU subtraction is valid or used.

Host evidence is sparse. host_entry23:29:46UTC contains33 selected0x56 warnings; host_before23:58:22UTC contains36. host_preflight is during the first preflight, not during full. host_after03:13:10.644863UTC is **2h16m34.857s after fullterminal00:56:35.788067**, not an immediate endpoint or continuous observation. It shows the same boot04dc0087-5ccc-4c46-9997-b9a92f0e5167, empty compute-app query, retained400W power limit versus575W default, and56 selected warnings, including20 new during the full window. It does not establish continuous exclusivity, power/clock constancy, no interference, clean driver history or warning causation. No full-run midpoint observation is present. This missing planned host context is a reporting limitation; it is not imputed from the late idle snapshot.

Public reporting can retain finite correct execution, signed traced client performance, actual trajectories and18 validated kernel profiles with explicit missing cells. It cannot claim a new performance improvement, ordinary-serving percentage decomposition, pure transport/copy cost, GPU occupancy/PCIe/bandwidth/FLOP causation, total CPU/energy removal, universal Linux/hardware/backend portability, arbitrary text serving or completed project acceptance. No new formal paper RQ, mandatory baseline, approval gate or rerun is inferred.

## Recompute and audit trail

The original reproducible path is `python3 TEMP/run.py full` for collection and `python3 TEMP/analysis.py TEMP full` for the fixed analysis; do not rerun collection as part of reproducing this CPU review. For retained data the latter must still fail at exact coverage. `python3 TEMP/client_analysis.py TEMP full` reconstructs only client/logical outcomes and remains explicitly supplemental. Recipes, raw expanded commands, model pools, source_snapshot, source_frozen, package/linkage/build receipts and preserved recipe versions are needed alongside all raw40 client/model/replay outputs and20 profiles. Preserve failed preflight/raw/core provenance, failed initialization analysis and failed full analysis. This report independently recomputed all rows without changing raw data or the fixed recipes; displayed durations and effects use ms/TPS to six decimals. Every all40 client row, all20 coverage row, all logical trajectory, every valid profile cell/stratum and signed comparison follows below. No figure or headline paper number is accepted beyond that stated scope.

## Independently recomputed client outcomes

All 40 cells pass independent raw count/index/timestamp arithmetic; fixed pre-observation pool membership; serving/replay exit; trace admission, physical slot, history and release conservation; exact client/current-trace/fresh-replay tokens; overflow/error/drain and native/loop transport checks. Model and recipe bindings match current source. Activity completeness is separately audited. 1280 measured gen64 requests/81920 tokens plus320 checked gen1 warmups.

| Cell | TPS | TTFT ms | TPOT ms | completion ms | measured rounds | batch histogram |
|---|---:|---:|---:|---:|---:|---|
| full_qwen_p0_loop_profiled | 4533.553083 | 2.410000 | 1.736250 | 111.793765 | 269 | {1: 12, 3: 1, 4: 1, 5: 2, 7: 5, 8: 248} |
| full_qwen_p0_loop_unprofiled | 4521.074159 | 2.453075 | 1.732756 | 111.616715 | 269 | {1: 12, 2: 1, 5: 1, 6: 3, 7: 5, 8: 247} |
| full_qwen_p0_native_profiled | 4653.003449 | 2.371503 | 1.703825 | 109.712458 | 263 | {1: 6, 4: 2, 6: 2, 7: 2, 8: 251} |
| full_qwen_p0_native_unprofiled | 4908.594563 | 2.053541 | 1.604378 | 103.129384 | 263 | {1: 3, 2: 2, 3: 4, 6: 1, 7: 1, 8: 252} |
| full_qwen_p1_loop_profiled | 4496.894878 | 2.478667 | 1.715869 | 110.578400 | 295 | {1: 37, 2: 1, 3: 2, 4: 1, 6: 1, 7: 31, 8: 222} |
| full_qwen_p1_loop_unprofiled | 4452.528993 | 2.485700 | 1.765577 | 113.717039 | 274 | {1: 17, 2: 1, 4: 1, 6: 3, 7: 9, 8: 243} |
| full_qwen_p1_native_profiled | 4555.005661 | 2.241520 | 1.743382 | 112.074580 | 259 | {1: 1, 3: 2, 4: 1, 5: 1, 8: 254} |
| full_qwen_p1_native_unprofiled | 4634.151617 | 5.366396 | 1.664762 | 110.246397 | 271 | {1: 13, 2: 2, 4: 1, 6: 2, 7: 9, 8: 244} |
| full_qwen_p2_loop_profiled | 4477.124725 | 3.004866 | 1.736680 | 112.415686 | 268 | {1: 11, 2: 1, 4: 1, 6: 1, 7: 7, 8: 247} |
| full_qwen_p2_loop_unprofiled | 4499.674927 | 2.394541 | 1.727278 | 111.213054 | 271 | {1: 10, 2: 3, 3: 3, 4: 2, 5: 1, 6: 1, 7: 4, 8: 247} |
| full_qwen_p2_native_profiled | 4551.303206 | 2.228232 | 1.743068 | 112.041489 | 261 | {1: 4, 4: 2, 7: 4, 8: 251} |
| full_qwen_p2_native_unprofiled | 4533.371023 | 2.440572 | 1.749440 | 112.655279 | 260 | {1: 3, 3: 1, 5: 1, 6: 1, 7: 1, 8: 253} |
| full_qwen_p3_loop_profiled | 4570.981105 | 2.557210 | 1.719102 | 110.860611 | 281 | {1: 21, 2: 4, 3: 1, 5: 1, 6: 3, 7: 15, 8: 236} |
| full_qwen_p3_loop_unprofiled | 4660.140451 | 2.597917 | 1.689356 | 109.027347 | 266 | {1: 9, 2: 1, 5: 1, 6: 2, 7: 4, 8: 249} |
| full_qwen_p3_native_profiled | 4697.670335 | 4.330486 | 1.651744 | 108.390385 | 267 | {1: 10, 3: 1, 4: 1, 7: 9, 8: 246} |
| full_qwen_p3_native_unprofiled | 4522.181201 | 2.117911 | 1.759022 | 112.936328 | 260 | {1: 2, 2: 1, 3: 1, 5: 2, 7: 1, 8: 253} |
| full_qwen_p4_loop_profiled | 4440.268761 | 2.508525 | 1.757989 | 113.261829 | 267 | {1: 9, 2: 2, 4: 1, 5: 1, 6: 1, 7: 4, 8: 249} |
| full_qwen_p4_loop_unprofiled | 4617.206275 | 2.494778 | 1.712039 | 110.353260 | 278 | {1: 22, 5: 1, 6: 1, 7: 17, 8: 237} |
| full_qwen_p4_native_profiled | 4583.668286 | 2.391278 | 1.732374 | 111.530842 | 258 | {1: 2, 7: 2, 8: 254} |
| full_qwen_p4_native_unprofiled | 4780.663709 | 2.234003 | 1.588093 | 102.283834 | 291 | {1: 33, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 29, 8: 224} |
| full_smol_p0_loop_profiled | 5306.024950 | 2.109761 | 1.482454 | 95.504363 | 268 | {1: 6, 2: 3, 3: 3, 4: 4, 6: 1, 7: 3, 8: 248} |
| full_smol_p0_loop_unprofiled | 5248.908858 | 2.163367 | 1.501598 | 96.764009 | 266 | {1: 4, 3: 2, 4: 10, 7: 2, 8: 248} |
| full_smol_p0_native_profiled | 5295.930014 | 1.736064 | 1.503835 | 96.477644 | 258 | {2: 2, 4: 1, 8: 255} |
| full_smol_p0_native_unprofiled | 5254.190259 | 1.856824 | 1.512195 | 97.125090 | 264 | {1: 4, 2: 3, 3: 2, 4: 1, 5: 1, 7: 1, 8: 252} |
| full_smol_p1_loop_profiled | 5272.082512 | 2.026547 | 1.501743 | 96.636336 | 263 | {1: 5, 2: 2, 4: 1, 5: 1, 7: 2, 8: 252} |
| full_smol_p1_loop_unprofiled | 5173.782099 | 2.197184 | 1.520980 | 98.018916 | 269 | {1: 8, 2: 3, 3: 2, 4: 4, 7: 4, 8: 248} |
| full_smol_p1_native_profiled | 5255.488436 | 1.594925 | 1.516653 | 97.144063 | 258 | {2: 2, 4: 1, 8: 255} |
| full_smol_p1_native_unprofiled | 5213.341995 | 1.692421 | 1.527889 | 97.949442 | 259 | {1: 1, 2: 1, 3: 1, 5: 1, 6: 1, 7: 1, 8: 253} |
| full_smol_p2_loop_profiled | 5231.658516 | 2.649657 | 1.505802 | 97.515205 | 263 | {1: 5, 2: 1, 3: 2, 5: 1, 7: 2, 8: 252} |
| full_smol_p2_loop_unprofiled | 5194.197185 | 4.329343 | 1.449822 | 95.668154 | 276 | {1: 17, 2: 2, 3: 1, 4: 2, 5: 1, 7: 13, 8: 240} |
| full_smol_p2_native_profiled | 5222.364467 | 1.914241 | 1.520834 | 97.726796 | 261 | {1: 1, 3: 4, 4: 1, 5: 3, 8: 252} |
| full_smol_p2_native_unprofiled | 5294.391225 | 1.718884 | 1.504778 | 96.519893 | 260 | {2: 2, 3: 1, 4: 2, 5: 1, 6: 2, 8: 252} |
| full_smol_p3_loop_profiled | 5291.914169 | 2.337041 | 1.485139 | 95.900809 | 275 | {1: 17, 2: 2, 4: 1, 5: 1, 6: 2, 7: 10, 8: 242} |
| full_smol_p3_loop_unprofiled | 5462.056918 | 2.106567 | 1.412921 | 91.120565 | 284 | {1: 26, 2: 1, 3: 2, 4: 1, 6: 1, 7: 20, 8: 233} |
| full_smol_p3_native_profiled | 5163.438472 | 1.632975 | 1.539134 | 98.598426 | 258 | {3: 2, 5: 2, 8: 254} |
| full_smol_p3_native_unprofiled | 5303.315133 | 2.988732 | 1.480847 | 96.282099 | 260 | {1: 3, 3: 1, 4: 1, 7: 2, 8: 253} |
| full_smol_p4_loop_profiled | 5144.675846 | 2.203222 | 1.531699 | 98.700245 | 272 | {1: 7, 2: 8, 3: 1, 4: 2, 5: 2, 6: 5, 7: 2, 8: 245} |
| full_smol_p4_loop_unprofiled | 5264.897400 | 1.996629 | 1.501760 | 96.607498 | 268 | {1: 9, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1, 7: 3, 8: 249} |
| full_smol_p4_native_profiled | 5280.593788 | 2.451755 | 1.497351 | 96.784855 | 259 | {1: 1, 2: 1, 4: 2, 6: 1, 7: 1, 8: 253} |
| full_smol_p4_native_unprofiled | 5270.356919 | 1.658870 | 1.512242 | 96.930140 | 262 | {1: 1, 2: 2, 3: 4, 5: 2, 6: 1, 7: 1, 8: 251} |

## All signed client paired effects

p0..p4 signed differences. Nominal two-sided t95, df4, independent paired process blocks. Requests are not independent replicates; crossing zero is not equivalence. Missing-profile-activity cells stay in all client effects.

| model | condition/path | contrast | metric | p0..p4 | mean | nominal t95 |
|---|---|---|---|---|---:|---|
| qwen | unprofiled | loop-native | tps | -387.520404, -181.622624, -33.696096, 137.959250, -163.457434 | -125.667462 | [-366.981754, 115.646831] |
| qwen | unprofiled | loop-native | ttft_ms | 0.399534, -2.880696, -0.046031, 0.480006, 0.260776 | -0.357282 | [-2.126415, 1.411850] |
| qwen | unprofiled | loop-native | tpot_ms | 0.128378, 0.100815, -0.022162, -0.069666, 0.123947 | 0.052262 | [-0.061699, 0.166224] |
| qwen | unprofiled | loop-native | completion_ms | 8.487331, 3.470642, -1.442225, -3.908981, 8.069426 | 2.935239 | [-3.963481, 9.833959] |
| qwen | unprofiled | loop-native | rounds | 6.000000, 3.000000, 11.000000, 6.000000, -13.000000 | 2.600000 | [-8.800342, 14.000342] |
| qwen | profiled | loop-native | tps | -119.450366, -58.110784, -74.178482, -126.689230, -143.399525 | -104.365677 | [-149.564260, -59.167095] |
| qwen | profiled | loop-native | ttft_ms | 0.038497, 0.237148, 0.776634, -1.773276, 0.117247 | -0.120750 | [-1.322382, 1.080882] |
| qwen | profiled | loop-native | tpot_ms | 0.032426, -0.027513, -0.006388, 0.067357, 0.025615 | 0.018299 | [-0.027187, 0.063786] |
| qwen | profiled | loop-native | completion_ms | 2.081308, -1.496180, 0.374197, 2.470226, 1.730987 | 1.032108 | [-0.977943, 3.042158] |
| qwen | profiled | loop-native | rounds | 6.000000, 36.000000, 7.000000, 14.000000, 9.000000 | 14.400000 | [-1.073545, 29.873545] |
| qwen | loop | profiled-unprofiled | tps | 12.478924, 44.365885, -22.550202, -89.159346, -176.937514 | -46.360451 | [-155.919944, 63.199042] |
| qwen | loop | profiled-unprofiled | ttft_ms | -0.043075, -0.007033, 0.610326, -0.040708, 0.013746 | 0.106651 | [-0.244202, 0.457504] |
| qwen | loop | profiled-unprofiled | tpot_ms | 0.003494, -0.049708, 0.009402, 0.029746, 0.045950 | 0.007777 | [-0.037272, 0.052826] |
| qwen | loop | profiled-unprofiled | completion_ms | 0.177050, -3.138639, 1.202633, 1.833265, 2.908569 | 0.596576 | [-2.273378, 3.466529] |
| qwen | loop | profiled-unprofiled | rounds | 0.000000, 21.000000, -3.000000, 15.000000, -11.000000 | 4.400000 | [-12.016282, 20.816282] |
| qwen | native | profiled-unprofiled | tps | -255.591114, -79.145956, 17.932184, 175.489135, -196.995424 | -67.662235 | [-281.489255, 146.164785] |
| qwen | native | profiled-unprofiled | ttft_ms | 0.317962, -3.124876, -0.212340, 2.212575, 0.157275 | -0.129881 | [-2.513982, 2.254221] |
| qwen | native | profiled-unprofiled | tpot_ms | 0.099446, 0.078620, -0.006372, -0.107278, 0.144281 | 0.041739 | [-0.082001, 0.165480] |
| qwen | native | profiled-unprofiled | completion_ms | 6.583073, 1.828183, -0.613790, -4.545943, 9.247008 | 2.499706 | [-4.357212, 9.356625] |
| qwen | native | profiled-unprofiled | rounds | 0.000000, -12.000000, 1.000000, 7.000000, -33.000000 | -7.400000 | [-27.122534, 12.322534] |
| smol | unprofiled | loop-native | tps | -5.281401, -39.559896, -100.194040, 158.741784, -5.459519 | 1.649386 | [-117.522680, 120.821451] |
| smol | unprofiled | loop-native | ttft_ms | 0.306542, 0.504763, 2.610459, -0.882164, 0.337759 | 0.575472 | [-0.995087, 2.146030] |
| smol | unprofiled | loop-native | tpot_ms | -0.010597, -0.006909, -0.054956, -0.067926, -0.010483 | -0.030174 | [-0.066116, 0.005768] |
| smol | unprofiled | loop-native | completion_ms | -0.361081, 0.069474, -0.851738, -5.161534, -0.322643 | -1.325504 | [-4.018898, 1.367890] |
| smol | unprofiled | loop-native | rounds | 2.000000, 10.000000, 16.000000, 24.000000, 6.000000 | 11.600000 | [0.861221, 22.338779] |
| smol | profiled | loop-native | tps | 10.094936, 16.594076, 9.294049, 128.475697, -135.917942 | 5.708163 | [-110.903236, 122.319562] |
| smol | profiled | loop-native | ttft_ms | 0.373697, 0.431621, 0.735416, 0.704066, -0.248533 | 0.399253 | [-0.092437, 0.890944] |
| smol | profiled | loop-native | tpot_ms | -0.021381, -0.014910, -0.015032, -0.053995, 0.034348 | -0.014194 | [-0.053426, 0.025038] |
| smol | profiled | loop-native | completion_ms | -0.973280, -0.507727, -0.211591, -2.697617, 1.915390 | -0.494965 | [-2.551291, 1.561361] |
| smol | profiled | loop-native | rounds | 10.000000, 5.000000, 2.000000, 17.000000, 13.000000 | 9.400000 | [1.919039, 16.880961] |
| smol | loop | profiled-unprofiled | tps | 57.116092, 98.300413, 37.461331, -170.142749, -120.221554 | -19.497293 | [-166.189300, 127.194714] |
| smol | loop | profiled-unprofiled | ttft_ms | -0.053606, -0.170638, -1.679686, 0.230473, 0.206593 | -0.293373 | [-1.278678, 0.691932] |
| smol | loop | profiled-unprofiled | tpot_ms | -0.019143, -0.019237, 0.055980, 0.072219, 0.029939 | 0.023951 | [-0.028412, 0.076315] |
| smol | loop | profiled-unprofiled | completion_ms | -1.259646, -1.382580, 1.847051, 4.780244, 2.092748 | 1.215563 | [-1.995536, 4.426663] |
| smol | loop | profiled-unprofiled | rounds | 2.000000, -6.000000, -13.000000, -9.000000, 4.000000 | -4.400000 | [-13.379557, 4.579557] |
| smol | native | profiled-unprofiled | tps | 41.739755, 42.146441, -72.026758, -139.876662, 10.236869 | -23.556071 | [-122.893488, 75.781346] |
| smol | native | profiled-unprofiled | ttft_ms | -0.120760, -0.097495, 0.195357, -1.355757, 0.792884 | -0.117154 | [-1.090964, 0.856656] |
| smol | native | profiled-unprofiled | tpot_ms | -0.008360, -0.011236, 0.016056, 0.058287, -0.014892 | 0.007971 | [-0.030074, 0.046016] |
| smol | native | profiled-unprofiled | completion_ms | -0.647446, -0.805379, 1.206904, 2.316328, -0.145285 | 0.385024 | [-1.277334, 2.047383] |
| smol | native | profiled-unprofiled | rounds | -6.000000, -1.000000, 1.000000, -2.000000, -3.000000 | -2.200000 | [-5.413968, 1.013968] |

## All20 raw profile coverage audits

Actual/expected model kernel and graph memcpy/memset counts cover warmups and measured serving. Recursive catalogue lookup uses every actual compute query/batch. All initializer count/geometry/identity/pre-model checks pass. Per-round unique graph/node and serial/non-overlap checks are only meaningful after complete counts; deficient cells are not grouped or imputed. Memory coverage is whole-serve counts only.

| cell | all rounds | model kernels actual/expected | memcpy actual/expected | memset actual/expected | controllers | complete / group identity+serial |
|---|---:|---|---|---|---|---|
| full_qwen_p0_loop_profiled | 277 | 93307/93307 | 349/349 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 278} | True / True |
| full_qwen_p0_native_profiled | 271 | 91681/91681 | 295/295 | 0/0 | {'dispatch': 272} | True / True |
| full_qwen_p1_loop_profiled | 303 | 99657/99657 | 1023/1023 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 304} | True / True |
| full_qwen_p1_native_profiled | 267 | 90621/90621 | 267/267 | 0/0 | {'dispatch': 268} | True / True |
| full_qwen_p2_loop_profiled | 276 | 92916/92916 | 396/396 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 277} | True / True |
| full_qwen_p2_native_profiled | 269 | 91139/91139 | 293/293 | 0/0 | {'dispatch': 270} | True / True |
| full_qwen_p3_loop_profiled | 289 | 96367/96367 | 625/625 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 290} | True / True |
| full_qwen_p3_native_profiled | 275 | 92621/92621 | 443/443 | 0/0 | {'dispatch': 276} | True / True |
| full_qwen_p4_loop_profiled | 275 | 92789/92789 | 323/323 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 276} | True / True |
| full_qwen_p4_native_profiled | 266 | 90326/90326 | 266/266 | 0/0 | {'dispatch': 267} | True / True |
| full_smol_p0_loop_profiled | 276 | 115692/115692 | 336/336 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 277} | True / True |
| full_smol_p0_native_profiled | 266 | 112262/112262 | 266/266 | 0/0 | {'dispatch': 267} | True / True |
| full_smol_p1_loop_profiled | 271 | 113917/113917 | 271/271 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 272} | True / True |
| full_smol_p1_native_profiled | 266 | 112262/112262 | 266/266 | 0/0 | {'dispatch': 267} | True / True |
| full_smol_p2_loop_profiled | 271 | 113944/113947 | 271/271 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 272} | False / None |
| full_smol_p2_native_profiled | 269 | 113363/113363 | 269/269 | 0/0 | {'dispatch': 270} | True / True |
| full_smol_p3_loop_profiled | 283 | 117781/117781 | 553/553 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 284} | True / True |
| full_smol_p3_native_profiled | 266 | 112262/112262 | 266/266 | 0/0 | {'dispatch': 267} | True / True |
| full_smol_p4_loop_profiled | 280 | 117217/117220 | 340/340 | 0/0 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 281} | False / None |
| full_smol_p4_native_profiled | 267 | 112599/112599 | 267/267 | 0/0 | {'dispatch': 268} | True / True |

## Profile durations with invalid cells retained

Measured kernel-only epoch/union/span/kernel-sum/inter-round-gap/within-round-gap, ms. GPU timestamps are differenced only with GPU timestamps. Epoch excludes leading/trailing delivery. Gaps are not pure transport; graph memory durations are not added.

| cell | epoch | union | span-sum | kernel-sum | inter-round gap | within-round gap |
|---|---:|---:|---:|---:|---:|---:|
| full_qwen_p0_loop_profiled | 415.421335 | 311.848512 | 351.144038 | 311.849215 | 64.277297 | 39.295526 |
| full_qwen_p0_native_profiled | 406.151872 | 305.407938 | 336.900673 | 305.408480 | 69.251199 | 31.492735 |
| full_qwen_p1_loop_profiled | 426.104252 | 341.232538 | 382.089559 | 341.233232 | 44.014693 | 40.857021 |
| full_qwen_p1_native_profiled | 420.122473 | 300.267288 | 345.820801 | 300.267880 | 74.301672 | 45.553512 |
| full_qwen_p2_loop_profiled | 420.186473 | 310.509892 | 349.506746 | 310.510326 | 70.679727 | 38.996854 |
| full_qwen_p2_native_profiled | 415.347622 | 302.202243 | 347.971115 | 302.203316 | 67.376507 | 45.768873 |
| full_qwen_p3_loop_profiled | 413.400713 | 325.651980 | 358.163041 | 325.652373 | 55.237673 | 32.511060 |
| full_qwen_p3_native_profiled | 422.648040 | 309.081165 | 355.242676 | 309.081611 | 67.405364 | 46.161511 |
| full_qwen_p4_loop_profiled | 425.601338 | 309.053306 | 355.569146 | 309.053703 | 70.032192 | 46.515840 |
| full_qwen_p4_native_profiled | 413.208909 | 298.992931 | 344.400951 | 298.993996 | 68.807958 | 45.408019 |
| full_smol_p0_loop_profiled | 352.103805 | 230.906567 | 289.031990 | 230.906117 | 63.071815 | 58.125423 |
| full_smol_p0_native_profiled | 352.946578 | 223.426088 | 279.848902 | 223.426052 | 73.097676 | 56.422814 |
| full_smol_p1_loop_profiled | 354.552432 | 227.258455 | 284.372179 | 227.257693 | 70.180252 | 57.113725 |
| full_smol_p1_native_profiled | 357.213538 | 223.212404 | 279.619580 | 223.212258 | 77.593958 | 56.407176 |
| full_smol_p2_loop_profiled | INVALID missing3 model activities | NA | NA | NA | NA | NA |
| full_smol_p2_native_profiled | 359.369824 | 225.858126 | 282.878031 | 225.858073 | 76.491793 | 57.019905 |
| full_smol_p3_loop_profiled | 352.898733 | 236.195016 | 276.315114 | 236.193695 | 76.583619 | 40.120098 |
| full_smol_p3_native_profiled | 353.751109 | 223.138243 | 279.485731 | 223.138037 | 74.265378 | 56.347488 |
| full_smol_p4_loop_profiled | INVALID missing3 model activities | NA | NA | NA | NA | NA |
| full_smol_p4_native_profiled | 347.056206 | 224.012909 | 280.663576 | 224.012753 | 66.392630 | 56.650667 |

## Signed duration effects

Every p0..p4 loop-native difference is retained. Qwen has five valid pairs and the planned nominal df4 interval; Smol p2,p4 stay NA, with no partial-pool mean/CI replacing the planned five-block estimate.

| model | metric | p0..p4 differences | planned five-block mean/t95 |
|---|---|---|---|
| qwen | model_epoch_ms | 9.269463, 5.981779, 4.838851, -9.247327, 12.392429 | 4.647039 [-5.671286, 14.965364] |
| qwen | model_union_ms | 6.440574, 40.965250, 8.307649, 16.570815, 10.060374 | 16.468932 [-1.181967, 34.119832] |
| qwen | model_round_span_sum_ms | 14.243365, 36.268758, 1.535631, 2.920364, 11.168195 | 13.227263 [-4.101727, 30.556252] |
| qwen | model_kernel_sum_ms | 6.440735, 40.965352, 8.307010, 16.570762, 10.059707 | 16.468713 [-1.182413, 34.119840] |
| qwen | inter_round_gap_ms | -4.973901, -30.286979, 3.303220, -12.167691, 1.224234 | -8.580223 [-25.404683, 8.244236] |
| qwen | within_round_gap_ms | 7.802791, -4.696491, -6.772019, -13.650451, 1.107821 | -3.241670 [-13.325571, 6.842231] |
| smol | model_epoch_ms | -0.842773, -2.661106, NA, -0.852376, NA | unavailable: p2,p4 deficient |
| smol | model_union_ms | 7.480479, 4.046051, NA, 13.056773, NA | unavailable: p2,p4 deficient |
| smol | model_round_span_sum_ms | 9.183088, 4.752600, NA, -3.170617, NA | unavailable: p2,p4 deficient |
| smol | model_kernel_sum_ms | 7.480065, 4.045435, NA, 13.055658, NA | unavailable: p2,p4 deficient |
| smol | inter_round_gap_ms | -10.025861, -7.413706, NA, 2.318241, NA | unavailable: p2,p4 deficient |
| smol | within_round_gap_ms | 1.702608, 0.706548, NA, -16.227390, NA | unavailable: p2,p4 deficient |

## All measured query/batch trajectories

BF_TRACE compute counts remain available for all40 cells, including deficient profiles.

| cell | (query,batch): rounds |
|---|---|
| full_qwen_p0_loop_profiled | {(0, 1): 3, (0, 3): 1, (0, 5): 1, (0, 7): 3, (0, 8): 248, (2, 1): 4, (5, 1): 5, (8, 4): 1, (8, 5): 1, (8, 7): 2} |
| full_qwen_p0_loop_unprofiled | {(0, 1): 4, (0, 2): 1, (0, 6): 1, (0, 7): 4, (0, 8): 247, (2, 1): 1, (5, 1): 4, (8, 1): 3, (8, 5): 1, (8, 6): 2, (8, 7): 1} |
| full_qwen_p0_native_profiled | {(0, 1): 1, (0, 7): 1, (0, 8): 251, (2, 1): 2, (5, 1): 3, (5, 4): 1, (8, 4): 1, (8, 6): 2, (8, 7): 1} |
| full_qwen_p0_native_unprofiled | {(0, 1): 1, (0, 7): 1, (0, 8): 251, (2, 1): 1, (5, 1): 1, (5, 2): 1, (5, 3): 1, (8, 2): 1, (8, 3): 3, (8, 6): 1, (8, 8): 1} |
| full_qwen_p1_loop_profiled | {(0, 1): 30, (0, 7): 30, (0, 8): 222, (2, 1): 2, (5, 1): 4, (5, 2): 1, (8, 1): 1, (8, 3): 2, (8, 4): 1, (8, 6): 1, (8, 7): 1} |
| full_qwen_p1_loop_unprofiled | {(0, 1): 9, (0, 7): 9, (0, 8): 243, (2, 1): 2, (5, 1): 6, (8, 2): 1, (8, 4): 1, (8, 6): 3} |
| full_qwen_p1_native_profiled | {(0, 8): 252, (5, 3): 1, (8, 1): 1, (8, 3): 1, (8, 4): 1, (8, 5): 1, (8, 8): 2} |
| full_qwen_p1_native_unprofiled | {(0, 1): 8, (0, 7): 8, (0, 8): 244, (5, 1): 5, (5, 2): 1, (8, 2): 1, (8, 4): 1, (8, 6): 2, (8, 7): 1} |
| full_qwen_p2_loop_profiled | {(0, 1): 5, (0, 7): 5, (0, 8): 247, (2, 1): 1, (5, 1): 1, (5, 4): 1, (8, 1): 4, (8, 2): 1, (8, 6): 1, (8, 7): 2} |
| full_qwen_p2_loop_unprofiled | {(0, 1): 4, (0, 3): 1, (0, 5): 1, (0, 7): 4, (0, 8): 247, (2, 1): 1, (2, 2): 1, (5, 1): 3, (5, 2): 1, (5, 3): 1, (5, 4): 1, (8, 1): 2, (8, 2): 1, (8, 3): 1, (8, 4): 1, (8, 6): 1} |
| full_qwen_p2_native_profiled | {(0, 1): 1, (0, 7): 1, (0, 8): 251, (5, 1): 3, (5, 4): 1, (8, 4): 1, (8, 7): 3} |
| full_qwen_p2_native_unprofiled | {(0, 8): 252, (2, 1): 1, (5, 1): 1, (5, 3): 1, (8, 1): 1, (8, 5): 1, (8, 6): 1, (8, 7): 1, (8, 8): 1} |
| full_qwen_p3_loop_profiled | {(0, 1): 14, (0, 2): 2, (0, 6): 2, (0, 7): 14, (0, 8): 236, (5, 1): 5, (5, 2): 1, (8, 1): 2, (8, 2): 1, (8, 3): 1, (8, 5): 1, (8, 6): 1, (8, 7): 1} |
| full_qwen_p3_loop_unprofiled | {(0, 1): 2, (0, 2): 1, (0, 6): 1, (0, 7): 2, (0, 8): 249, (2, 1): 2, (5, 6): 1, (8, 1): 5, (8, 5): 1, (8, 7): 2} |
| full_qwen_p3_native_profiled | {(0, 1): 7, (0, 7): 7, (0, 8): 245, (5, 1): 2, (8, 1): 1, (8, 3): 1, (8, 4): 1, (8, 7): 2, (8, 8): 1} |
| full_qwen_p3_native_unprofiled | {(0, 8): 252, (2, 2): 1, (5, 1): 2, (8, 3): 1, (8, 5): 2, (8, 7): 1, (8, 8): 1} |
| full_qwen_p4_loop_profiled | {(0, 1): 2, (0, 2): 1, (0, 6): 1, (0, 7): 2, (0, 8): 249, (2, 1): 1, (5, 1): 4, (5, 2): 1, (8, 1): 2, (8, 4): 1, (8, 5): 1, (8, 7): 2} |
| full_qwen_p4_loop_unprofiled | {(0, 1): 15, (0, 7): 15, (0, 8): 237, (5, 1): 7, (8, 5): 1, (8, 6): 1, (8, 7): 2} |
| full_qwen_p4_native_profiled | {(0, 8): 252, (5, 1): 1, (8, 1): 1, (8, 7): 2, (8, 8): 2} |
| full_qwen_p4_native_unprofiled | {(0, 1): 28, (0, 7): 28, (0, 8): 224, (2, 1): 2, (5, 1): 3, (5, 2): 1, (8, 3): 1, (8, 4): 1, (8, 5): 1, (8, 6): 1, (8, 7): 1} |
| full_smol_p0_loop_profiled | {(0, 1): 2, (0, 2): 1, (0, 4): 2, (0, 6): 1, (0, 7): 2, (0, 8): 248, (2, 1): 1, (5, 1): 1, (5, 2): 1, (5, 3): 2, (8, 1): 2, (8, 2): 1, (8, 3): 1, (8, 4): 2, (8, 7): 1} |
| full_smol_p0_loop_unprofiled | {(0, 4): 8, (0, 8): 248, (2, 1): 3, (5, 3): 1, (8, 1): 1, (8, 3): 1, (8, 4): 2, (8, 7): 2} |
| full_smol_p0_native_profiled | {(0, 8): 252, (5, 2): 1, (8, 2): 1, (8, 4): 1, (8, 8): 3} |
| full_smol_p0_native_unprofiled | {(0, 8): 252, (2, 1): 1, (5, 1): 2, (5, 2): 1, (5, 3): 1, (8, 1): 1, (8, 2): 2, (8, 3): 1, (8, 4): 1, (8, 5): 1, (8, 7): 1} |
| full_smol_p1_loop_profiled | {(0, 8): 252, (2, 1): 1, (5, 1): 4, (5, 2): 1, (8, 2): 1, (8, 4): 1, (8, 5): 1, (8, 7): 2} |
| full_smol_p1_loop_unprofiled | {(0, 1): 2, (0, 4): 4, (0, 7): 2, (0, 8): 248, (2, 1): 2, (5, 1): 4, (5, 2): 2, (5, 3): 1, (8, 2): 1, (8, 3): 1, (8, 7): 2} |
| full_smol_p1_native_profiled | {(0, 8): 252, (5, 2): 1, (8, 2): 1, (8, 4): 1, (8, 8): 3} |
| full_smol_p1_native_unprofiled | {(0, 8): 252, (5, 1): 1, (8, 2): 1, (8, 3): 1, (8, 5): 1, (8, 6): 1, (8, 7): 1, (8, 8): 1} |
| full_smol_p2_loop_profiled | {(0, 8): 252, (5, 1): 5, (8, 2): 1, (8, 3): 2, (8, 5): 1, (8, 7): 2} |
| full_smol_p2_loop_unprofiled | {(0, 1): 11, (0, 3): 1, (0, 5): 1, (0, 7): 11, (0, 8): 240, (5, 1): 1, (5, 2): 1, (5, 4): 2, (8, 1): 5, (8, 2): 1, (8, 7): 2} |
| full_smol_p2_native_profiled | {(0, 3): 1, (0, 5): 1, (0, 8): 251, (5, 1): 1, (5, 3): 2, (8, 3): 1, (8, 4): 1, (8, 5): 2, (8, 8): 1} |
| full_smol_p2_native_unprofiled | {(0, 8): 252, (5, 2): 1, (5, 3): 1, (8, 2): 1, (8, 4): 2, (8, 5): 1, (8, 6): 2} |
| full_smol_p3_loop_profiled | {(0, 1): 9, (0, 2): 1, (0, 6): 1, (0, 7): 9, (0, 8): 242, (5, 1): 6, (5, 2): 1, (8, 1): 2, (8, 4): 1, (8, 5): 1, (8, 6): 1, (8, 7): 1} |
| full_smol_p3_loop_unprofiled | {(0, 1): 19, (0, 7): 19, (0, 8): 233, (2, 1): 1, (5, 1): 5, (5, 3): 2, (8, 1): 1, (8, 2): 1, (8, 4): 1, (8, 6): 1, (8, 7): 1} |
| full_smol_p3_native_profiled | {(0, 8): 252, (8, 3): 2, (8, 5): 2, (8, 8): 2} |
| full_smol_p3_native_unprofiled | {(0, 1): 1, (0, 7): 1, (0, 8): 251, (5, 1): 2, (5, 3): 1, (8, 4): 1, (8, 7): 1, (8, 8): 2} |
| full_smol_p4_loop_profiled | {(0, 1): 2, (0, 2): 4, (0, 4): 2, (0, 6): 4, (0, 7): 2, (0, 8): 245, (2, 1): 1, (5, 1): 4, (8, 2): 4, (8, 3): 1, (8, 5): 2, (8, 6): 1} |
| full_smol_p4_loop_unprofiled | {(0, 1): 2, (0, 4): 2, (0, 7): 2, (0, 8): 249, (2, 1): 5, (5, 2): 1, (5, 3): 1, (8, 1): 2, (8, 2): 1, (8, 5): 1, (8, 6): 1, (8, 7): 1} |
| full_smol_p4_native_profiled | {(0, 8): 252, (5, 1): 1, (8, 2): 1, (8, 4): 2, (8, 6): 1, (8, 7): 1, (8, 8): 1} |
| full_smol_p4_native_unprofiled | {(0, 2): 1, (0, 6): 1, (0, 8): 251, (2, 1): 1, (5, 3): 2, (8, 2): 1, (8, 3): 2, (8, 5): 2, (8, 7): 1} |

## All valid activity strata

Each cell/query/batch mean span and kernel union, ms. No pooling or claim of context/history matching. All activity-stratum durations for Smol loop/profiled p2,p4 are unavailable.

| cell | query | batch | rounds | span ms | union ms |
|---|---:|---:|---:|---:|---:|
| full_qwen_p0_loop_profiled | 0 | 1 | 3 | 1.204677 | 1.133469 |
| full_qwen_p0_loop_profiled | 0 | 3 | 1 | 1.325318 | 1.149991 |
| full_qwen_p0_loop_profiled | 0 | 5 | 1 | 1.329477 | 1.152643 |
| full_qwen_p0_loop_profiled | 0 | 7 | 3 | 1.298054 | 1.158494 |
| full_qwen_p0_loop_profiled | 0 | 8 | 248 | 1.308553 | 1.160122 |
| full_qwen_p0_loop_profiled | 2 | 1 | 4 | 1.285526 | 1.167725 |
| full_qwen_p0_loop_profiled | 5 | 1 | 5 | 1.228569 | 1.124588 |
| full_qwen_p0_loop_profiled | 8 | 4 | 1 | 1.307974 | 1.155271 |
| full_qwen_p0_loop_profiled | 8 | 5 | 1 | 1.236901 | 1.182537 |
| full_qwen_p0_loop_profiled | 8 | 7 | 2 | 1.315046 | 1.164018 |
| full_qwen_p0_native_profiled | 0 | 1 | 1 | 1.200646 | 1.128235 |
| full_qwen_p0_native_profiled | 0 | 7 | 1 | 1.226695 | 1.162380 |
| full_qwen_p0_native_profiled | 0 | 8 | 251 | 1.282533 | 1.161936 |
| full_qwen_p0_native_profiled | 2 | 1 | 2 | 1.259735 | 1.163948 |
| full_qwen_p0_native_profiled | 5 | 1 | 3 | 1.232625 | 1.122666 |
| full_qwen_p0_native_profiled | 5 | 4 | 1 | 1.270503 | 1.119593 |
| full_qwen_p0_native_profiled | 8 | 4 | 1 | 1.307335 | 1.154666 |
| full_qwen_p0_native_profiled | 8 | 6 | 2 | 1.268711 | 1.165334 |
| full_qwen_p0_native_profiled | 8 | 7 | 1 | 1.225062 | 1.170558 |
| full_qwen_p1_loop_profiled | 0 | 1 | 30 | 1.211575 | 1.142962 |
| full_qwen_p1_loop_profiled | 0 | 7 | 30 | 1.227859 | 1.160213 |
| full_qwen_p1_loop_profiled | 0 | 8 | 222 | 1.318314 | 1.159090 |
| full_qwen_p1_loop_profiled | 2 | 1 | 2 | 1.263651 | 1.168357 |
| full_qwen_p1_loop_profiled | 5 | 1 | 4 | 1.240475 | 1.123060 |
| full_qwen_p1_loop_profiled | 5 | 2 | 1 | 1.182851 | 1.131876 |
| full_qwen_p1_loop_profiled | 8 | 1 | 1 | 1.177731 | 1.127332 |
| full_qwen_p1_loop_profiled | 8 | 3 | 2 | 1.229187 | 1.126436 |
| full_qwen_p1_loop_profiled | 8 | 4 | 1 | 1.305667 | 1.153735 |
| full_qwen_p1_loop_profiled | 8 | 6 | 1 | 1.313506 | 1.161789 |
| full_qwen_p1_loop_profiled | 8 | 7 | 1 | 1.313411 | 1.162830 |
| full_qwen_p1_native_profiled | 0 | 8 | 252 | 1.336142 | 1.159504 |
| full_qwen_p1_native_profiled | 5 | 3 | 1 | 1.265092 | 1.124516 |
| full_qwen_p1_native_profiled | 8 | 1 | 1 | 1.268291 | 1.128219 |
| full_qwen_p1_native_profiled | 8 | 3 | 1 | 1.271620 | 1.120926 |
| full_qwen_p1_native_profiled | 8 | 4 | 1 | 1.303875 | 1.151436 |
| full_qwen_p1_native_profiled | 8 | 5 | 1 | 1.333635 | 1.180956 |
| full_qwen_p1_native_profiled | 8 | 8 | 2 | 1.335219 | 1.183085 |
| full_qwen_p2_loop_profiled | 0 | 1 | 5 | 1.211945 | 1.141834 |
| full_qwen_p2_loop_profiled | 0 | 7 | 5 | 1.289002 | 1.156811 |
| full_qwen_p2_loop_profiled | 0 | 8 | 247 | 1.308661 | 1.159809 |
| full_qwen_p2_loop_profiled | 2 | 1 | 1 | 1.211395 | 1.161093 |
| full_qwen_p2_loop_profiled | 5 | 1 | 1 | 1.266307 | 1.126722 |
| full_qwen_p2_loop_profiled | 5 | 4 | 1 | 1.173507 | 1.118909 |
| full_qwen_p2_loop_profiled | 8 | 1 | 4 | 1.245683 | 1.128175 |
| full_qwen_p2_loop_profiled | 8 | 2 | 1 | 1.183011 | 1.132745 |
| full_qwen_p2_loop_profiled | 8 | 6 | 1 | 1.313603 | 1.162402 |
| full_qwen_p2_loop_profiled | 8 | 7 | 2 | 1.316067 | 1.164690 |
| full_qwen_p2_native_profiled | 0 | 1 | 1 | 1.199107 | 1.127111 |
| full_qwen_p2_native_profiled | 0 | 7 | 1 | 1.334179 | 1.157250 |
| full_qwen_p2_native_profiled | 0 | 8 | 251 | 1.335173 | 1.158509 |
| full_qwen_p2_native_profiled | 5 | 1 | 3 | 1.260696 | 1.120302 |
| full_qwen_p2_native_profiled | 5 | 4 | 1 | 1.270915 | 1.118915 |
| full_qwen_p2_native_profiled | 8 | 4 | 1 | 1.303971 | 1.152074 |
| full_qwen_p2_native_profiled | 8 | 7 | 3 | 1.317443 | 1.166708 |
| full_qwen_p3_loop_profiled | 0 | 1 | 14 | 1.213033 | 1.143885 |
| full_qwen_p3_loop_profiled | 0 | 2 | 2 | 1.264147 | 1.200019 |
| full_qwen_p3_loop_profiled | 0 | 6 | 2 | 1.223634 | 1.160116 |
| full_qwen_p3_loop_profiled | 0 | 7 | 14 | 1.232162 | 1.160243 |
| full_qwen_p3_loop_profiled | 0 | 8 | 236 | 1.284125 | 1.160627 |
| full_qwen_p3_loop_profiled | 5 | 1 | 5 | 1.192008 | 1.123585 |
| full_qwen_p3_loop_profiled | 5 | 2 | 1 | 1.174658 | 1.124040 |
| full_qwen_p3_loop_profiled | 8 | 1 | 2 | 1.265971 | 1.125654 |
| full_qwen_p3_loop_profiled | 8 | 2 | 1 | 1.185219 | 1.134749 |
| full_qwen_p3_loop_profiled | 8 | 3 | 1 | 1.180770 | 1.126337 |
| full_qwen_p3_loop_profiled | 8 | 5 | 1 | 1.233539 | 1.178277 |
| full_qwen_p3_loop_profiled | 8 | 6 | 1 | 1.315971 | 1.164674 |
| full_qwen_p3_loop_profiled | 8 | 7 | 1 | 1.319106 | 1.168646 |
| full_qwen_p3_native_profiled | 0 | 1 | 7 | 1.213259 | 1.145474 |
| full_qwen_p3_native_profiled | 0 | 7 | 7 | 1.333328 | 1.156125 |
| full_qwen_p3_native_profiled | 0 | 8 | 245 | 1.335010 | 1.158411 |
| full_qwen_p3_native_profiled | 5 | 1 | 2 | 1.259939 | 1.120354 |
| full_qwen_p3_native_profiled | 8 | 1 | 1 | 1.265443 | 1.125571 |
| full_qwen_p3_native_profiled | 8 | 3 | 1 | 1.271267 | 1.119553 |
| full_qwen_p3_native_profiled | 8 | 4 | 1 | 1.307587 | 1.154688 |
| full_qwen_p3_native_profiled | 8 | 7 | 2 | 1.318931 | 1.167219 |
| full_qwen_p3_native_profiled | 8 | 8 | 1 | 1.336962 | 1.184244 |
| full_qwen_p4_loop_profiled | 0 | 1 | 2 | 1.206354 | 1.135765 |
| full_qwen_p4_loop_profiled | 0 | 2 | 1 | 1.372066 | 1.195492 |
| full_qwen_p4_loop_profiled | 0 | 6 | 1 | 1.331555 | 1.155036 |
| full_qwen_p4_loop_profiled | 0 | 7 | 2 | 1.334786 | 1.156910 |
| full_qwen_p4_loop_profiled | 0 | 8 | 249 | 1.334837 | 1.158366 |
| full_qwen_p4_loop_profiled | 2 | 1 | 1 | 1.305666 | 1.166885 |
| full_qwen_p4_loop_profiled | 5 | 1 | 4 | 1.264779 | 1.124057 |
| full_qwen_p4_loop_profiled | 5 | 2 | 1 | 1.261026 | 1.121859 |
| full_qwen_p4_loop_profiled | 8 | 1 | 2 | 1.265219 | 1.126003 |
| full_qwen_p4_loop_profiled | 8 | 4 | 1 | 1.302306 | 1.150885 |
| full_qwen_p4_loop_profiled | 8 | 5 | 1 | 1.324674 | 1.174302 |
| full_qwen_p4_loop_profiled | 8 | 7 | 2 | 1.312818 | 1.161118 |
| full_qwen_p4_native_profiled | 0 | 8 | 252 | 1.335588 | 1.158916 |
| full_qwen_p4_native_profiled | 5 | 1 | 1 | 1.257698 | 1.117924 |
| full_qwen_p4_native_profiled | 8 | 1 | 1 | 1.266850 | 1.126284 |
| full_qwen_p4_native_profiled | 8 | 7 | 2 | 1.319395 | 1.168255 |
| full_qwen_p4_native_profiled | 8 | 8 | 2 | 1.334770 | 1.182698 |
| full_smol_p0_loop_profiled | 0 | 1 | 2 | 0.780546 | 0.614527 |
| full_smol_p0_loop_profiled | 0 | 2 | 1 | 1.240932 | 1.036487 |
| full_smol_p0_loop_profiled | 0 | 4 | 2 | 1.093507 | 0.874745 |
| full_smol_p0_loop_profiled | 0 | 6 | 1 | 1.100227 | 0.879849 |
| full_smol_p0_loop_profiled | 0 | 7 | 2 | 1.084627 | 0.864552 |
| full_smol_p0_loop_profiled | 0 | 8 | 248 | 1.083284 | 0.863815 |
| full_smol_p0_loop_profiled | 2 | 1 | 1 | 1.156547 | 0.997699 |
| full_smol_p0_loop_profiled | 5 | 1 | 1 | 1.011683 | 0.838341 |
| full_smol_p0_loop_profiled | 5 | 2 | 1 | 0.992643 | 0.819305 |
| full_smol_p0_loop_profiled | 5 | 3 | 2 | 0.991539 | 0.818283 |
| full_smol_p0_loop_profiled | 8 | 1 | 2 | 0.992739 | 0.820080 |
| full_smol_p0_loop_profiled | 8 | 2 | 1 | 0.994403 | 0.821191 |
| full_smol_p0_loop_profiled | 8 | 3 | 1 | 0.990755 | 0.817771 |
| full_smol_p0_loop_profiled | 8 | 4 | 2 | 1.000707 | 0.827911 |
| full_smol_p0_loop_profiled | 8 | 7 | 1 | 1.003011 | 0.829557 |
| full_smol_p0_native_profiled | 0 | 8 | 252 | 1.086537 | 0.866760 |
| full_smol_p0_native_profiled | 5 | 2 | 1 | 0.994436 | 0.820860 |
| full_smol_p0_native_profiled | 8 | 2 | 1 | 0.996804 | 0.823081 |
| full_smol_p0_native_profiled | 8 | 4 | 1 | 1.001700 | 0.829248 |
| full_smol_p0_native_profiled | 8 | 8 | 3 | 1.016217 | 0.843093 |
| full_smol_p1_loop_profiled | 0 | 8 | 252 | 1.084041 | 0.864905 |
| full_smol_p1_loop_profiled | 2 | 1 | 1 | 1.164034 | 1.006109 |
| full_smol_p1_loop_profiled | 5 | 1 | 4 | 1.012690 | 0.838994 |
| full_smol_p1_loop_profiled | 5 | 2 | 1 | 0.994243 | 0.820439 |
| full_smol_p1_loop_profiled | 8 | 2 | 1 | 0.994467 | 0.820381 |
| full_smol_p1_loop_profiled | 8 | 4 | 1 | 0.996227 | 0.822508 |
| full_smol_p1_loop_profiled | 8 | 5 | 1 | 0.992195 | 0.820160 |
| full_smol_p1_loop_profiled | 8 | 7 | 2 | 1.000995 | 0.828396 |
| full_smol_p1_native_profiled | 0 | 8 | 252 | 1.085653 | 0.865948 |
| full_smol_p1_native_profiled | 5 | 2 | 1 | 0.991299 | 0.817598 |
| full_smol_p1_native_profiled | 8 | 2 | 1 | 0.997603 | 0.824355 |
| full_smol_p1_native_profiled | 8 | 4 | 1 | 1.001763 | 0.828683 |
| full_smol_p1_native_profiled | 8 | 8 | 3 | 1.014744 | 0.840988 |
| full_smol_p2_native_profiled | 0 | 3 | 1 | 1.105122 | 0.885824 |
| full_smol_p2_native_profiled | 0 | 5 | 1 | 1.096610 | 0.876897 |
| full_smol_p2_native_profiled | 0 | 8 | 251 | 1.086314 | 0.866423 |
| full_smol_p2_native_profiled | 5 | 1 | 1 | 1.010498 | 0.836735 |
| full_smol_p2_native_profiled | 5 | 3 | 2 | 0.996834 | 0.822862 |
| full_smol_p2_native_profiled | 8 | 3 | 1 | 0.998498 | 0.825965 |
| full_smol_p2_native_profiled | 8 | 4 | 1 | 1.001859 | 0.828186 |
| full_smol_p2_native_profiled | 8 | 5 | 2 | 0.995666 | 0.821427 |
| full_smol_p2_native_profiled | 8 | 8 | 1 | 1.015682 | 0.843811 |
| full_smol_p3_loop_profiled | 0 | 1 | 9 | 0.704851 | 0.619476 |
| full_smol_p3_loop_profiled | 0 | 2 | 1 | 1.246946 | 1.042602 |
| full_smol_p3_loop_profiled | 0 | 6 | 1 | 1.101218 | 0.881317 |
| full_smol_p3_loop_profiled | 0 | 7 | 9 | 0.945563 | 0.866141 |
| full_smol_p3_loop_profiled | 0 | 8 | 242 | 1.019887 | 0.868088 |
| full_smol_p3_loop_profiled | 5 | 1 | 6 | 0.940823 | 0.841359 |
| full_smol_p3_loop_profiled | 5 | 2 | 1 | 0.991106 | 0.816972 |
| full_smol_p3_loop_profiled | 8 | 1 | 2 | 0.941378 | 0.823733 |
| full_smol_p3_loop_profiled | 8 | 4 | 1 | 0.890177 | 0.827849 |
| full_smol_p3_loop_profiled | 8 | 5 | 1 | 0.991713 | 0.818560 |
| full_smol_p3_loop_profiled | 8 | 6 | 1 | 0.895906 | 0.833761 |
| full_smol_p3_loop_profiled | 8 | 7 | 1 | 1.004066 | 0.830540 |
| full_smol_p3_native_profiled | 0 | 8 | 252 | 1.085214 | 0.865742 |
| full_smol_p3_native_profiled | 8 | 3 | 2 | 0.997314 | 0.824530 |
| full_smol_p3_native_profiled | 8 | 5 | 2 | 0.993314 | 0.819725 |
| full_smol_p3_native_profiled | 8 | 8 | 2 | 1.015250 | 0.841379 |
| full_smol_p4_native_profiled | 0 | 8 | 252 | 1.085805 | 0.865815 |
| full_smol_p4_native_profiled | 5 | 1 | 1 | 1.009634 | 0.836621 |
| full_smol_p4_native_profiled | 8 | 2 | 1 | 0.997954 | 0.824576 |
| full_smol_p4_native_profiled | 8 | 4 | 2 | 1.003650 | 0.830093 |
| full_smol_p4_native_profiled | 8 | 6 | 1 | 1.004802 | 0.831812 |
| full_smol_p4_native_profiled | 8 | 7 | 1 | 1.006466 | 0.832932 |
| full_smol_p4_native_profiled | 8 | 8 | 1 | 1.014562 | 0.841319 |

## Signed common-stratum comparisons

Per paired block, common actual query/batch only; loop-native ms from the independently recomputed six-decimal tables above. Different contexts/history/request sets can remain. Noncommon strata remain in the preceding per-cell tables. Both Smol deficient profile blocks retain no stratum comparisons.

| model | block | query | batch | loop/native rounds | span difference ms | union difference ms |
|---|---:|---:|---:|---|---:|---:|
| qwen | 0 | 0 | 1 | 3/1 | 0.004031 | 0.005234 |
| qwen | 0 | 0 | 7 | 3/1 | 0.071359 | -0.003886 |
| qwen | 0 | 0 | 8 | 248/251 | 0.026020 | -0.001814 |
| qwen | 0 | 2 | 1 | 4/2 | 0.025791 | 0.003777 |
| qwen | 0 | 5 | 1 | 5/3 | -0.004056 | 0.001922 |
| qwen | 0 | 8 | 4 | 1/1 | 0.000639 | 0.000605 |
| qwen | 0 | 8 | 7 | 2/1 | 0.089984 | -0.006540 |
| qwen | 1 | 0 | 8 | 222/252 | -0.017828 | -0.000414 |
| qwen | 1 | 8 | 1 | 1/1 | -0.090560 | -0.000887 |
| qwen | 1 | 8 | 3 | 2/1 | -0.042433 | 0.005510 |
| qwen | 1 | 8 | 4 | 1/1 | 0.001792 | 0.002299 |
| qwen | 2 | 0 | 1 | 5/1 | 0.012838 | 0.014723 |
| qwen | 2 | 0 | 7 | 5/1 | -0.045177 | -0.000439 |
| qwen | 2 | 0 | 8 | 247/251 | -0.026512 | 0.001300 |
| qwen | 2 | 5 | 1 | 1/3 | 0.005611 | 0.006420 |
| qwen | 2 | 5 | 4 | 1/1 | -0.097408 | -0.000006 |
| qwen | 2 | 8 | 7 | 2/3 | -0.001376 | -0.002018 |
| qwen | 3 | 0 | 1 | 14/7 | -0.000226 | -0.001589 |
| qwen | 3 | 0 | 7 | 14/7 | -0.101166 | 0.004118 |
| qwen | 3 | 0 | 8 | 236/245 | -0.050885 | 0.002216 |
| qwen | 3 | 5 | 1 | 5/2 | -0.067931 | 0.003231 |
| qwen | 3 | 8 | 1 | 2/1 | 0.000528 | 0.000083 |
| qwen | 3 | 8 | 3 | 1/1 | -0.090497 | 0.006784 |
| qwen | 3 | 8 | 7 | 1/2 | 0.000175 | 0.001427 |
| qwen | 4 | 0 | 8 | 249/252 | -0.000751 | -0.000550 |
| qwen | 4 | 5 | 1 | 4/1 | 0.007081 | 0.006133 |
| qwen | 4 | 8 | 1 | 2/1 | -0.001631 | -0.000281 |
| qwen | 4 | 8 | 7 | 2/2 | -0.006577 | -0.007137 |
| smol | 0 | 0 | 8 | 248/252 | -0.003253 | -0.002945 |
| smol | 0 | 5 | 2 | 1/1 | -0.001793 | -0.001555 |
| smol | 0 | 8 | 2 | 1/1 | -0.002401 | -0.001890 |
| smol | 0 | 8 | 4 | 2/1 | -0.000993 | -0.001337 |
| smol | 1 | 0 | 8 | 252/252 | -0.001612 | -0.001043 |
| smol | 1 | 5 | 2 | 1/1 | 0.002944 | 0.002841 |
| smol | 1 | 8 | 2 | 1/1 | -0.003136 | -0.003974 |
| smol | 1 | 8 | 4 | 1/1 | -0.005536 | -0.006175 |
| smol | 2 | NA | NA | deficient profile | NA | NA |
| smol | 3 | 0 | 8 | 242/252 | -0.065327 | 0.002346 |
| smol | 3 | 8 | 5 | 1/2 | -0.001601 | -0.001165 |
| smol | 4 | NA | NA | deficient profile | NA | NA |

## Independent preflight provenance crosscheck

This final CPU-only crosscheck retains first-attempt failure separately and authenticates attempt2 coverage without rerunning its analyzer or writing a replacement receipt.

| attempt/cell | request rows/tokens | serving exit | reference rows | model kernels actual/expected | memcpy actual/expected | controller records |
|---|---|---:|---:|---|---|---|
| failed1/preflight_qwen_p0_loop_unprofiled | 16/520 | 0 | 16 | not profiled | not profiled | not profiled |
| failed1/preflight_qwen_p0_native_profiled | 16/520 | -11 | 0 | 24343/24343 | 73/73 | {'dispatch': 74} |
| attempt2/preflight_qwen_p0_loop_profiled | 16/520 | 0 | 16 | 24614/24614 | 74/74 | {'io_initialize': 1, 'io_network': 1, 'dispatch': 75} |
| attempt2/preflight_qwen_p0_loop_unprofiled | 16/520 | 0 | 16 | not profiled | not profiled | not profiled |
| attempt2/preflight_qwen_p0_native_profiled | 16/520 | 0 | 16 | 24885/24885 | 75/75 | {'dispatch': 76} |
| attempt2/preflight_qwen_p0_native_unprofiled | 16/520 | 0 | 16 | not profiled | not profiled | not profiled |
