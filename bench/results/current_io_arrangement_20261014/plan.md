# Experiment Plan: current reused-graph GPU I/O arrangements

## Research Question

The retained user question is the full Linux TCP/HTTP + eBPF/sockmap -> kernel/GPU shared queue -> resident real-model GPU -> asynchronous kernel TCP reply path, without a steady userspace request worker, improving latency/TPS while reusing existing model computation. There is no formal paper RQ/idea-story contract in this repository; do not invent one.

Specific uncertainty: on current main's reused vLLM graphs, does the already-existing standalone GPU I/O constructor deliver better gen64/c8 throughput than the current coalesced constructor, and what remains against efficient native userspace TCP? This compares whole existing constructors, not exclusive overlap or one-CTA occupancy mediation.

## Paper-Value Admission

Planned role: supporting. Largest credible story: select the effective current serving arrangement without changing upstream model math, exposing a backend/workload boundary of a generic eBPF/GPU driver. A positive current-path result can recover delivery using existing code/entrypoints rather than adding another speculative optimization.

Load-bearing uncertainty/reviewer rejection: recent coalesced vLLM still loses long-output throughput to native despite fewer model rounds; the bookkeeping-placement test0054 adds no demonstrated primary gain. Why optimize a losing arrangement if an existing stronger one is available? The strongest available alternative is already in the repository and must be compared fairly.

Reuse before collection: finding0050's matched original-loop vLLM TPS was5592.135/4758.151 versus native5630.454/4806.615 and coalesced5070.858/4373.108. Its AMK arrangement result goes the other way; cite it rather than rerun unqualified AMK. Existing source/metadata proves current vLLM model CUDA differs from that original dispatcher only by the BF_IO_COALESCED block. Current noncoalesced I/O, however, uses the later durable IoState refactor rather than the old thread-local implementation; it received finite legacy compatibility, not this current matched performance/complete candidate qualification. Later coalesced publication/admission changes are also not the old0050 constructor. Old numbers settle neither current source selection nor current short/long tradeoffs, and must not be numerically substituted across run contexts.

Independent evidence: a source-neutral current-main comparison of the stronger existing alternative versus selected coalesced and native, with the same frozen model arithmetic/runtime and ordinary counter authentication. Not a new novelty claim from rerunning old data, not a dependency-only version bump: success selects an existing faster constructor, while failure says the old original-loop performance does not transfer to the current implementation and redirects optimization. Both change the engineering/research decision.

Positive: favor the existing standalone entrypoint for this finite vLLM scope, reporting native limits and secondary tradeoffs. Contradictory/mixed/inconclusive: keep coalesced selection where appropriate and preserve the current standalone boundary; no universal shared arrangement/model acceptance or source promotion by mean alone.

Best alternative: new timer/CQ or shared-memory optimization. This constructor comparison is stronger because old matched evidence supplies a credible better implementation and0054 fails to support one small placement optimization; neither new tuning nor model arithmetic changes can be justified before checking the stronger existing path.

## Expected And Alternative Outcomes

Expected: standalone GPU I/O recovers at least some gen64/c8 throughput relative to coalesced, possibly approaching native. It progresses independently of the model dispatcher on a nonblocking CUDA stream, whereas coalesced advances I/O between rounds and returns while model children execute.

Competing explanations: current GPU-state refactor/per-entry publication may erase original-loop gains; a resident network CTA may interfere with reused graph kernels; coalesced publication and idle final-response/SQ admission can improve round shape and short latency. These are bundled constructor differences. A win is not isolated overlap, PCIe cost, GPU time or resource-occupancy proof.

Contradiction: candidate-minus-coalesced primary TPS interval below0, or inconclusive effects with no justified source selection. Native wins bound the serving advantage. A valid local result bounds this arrangement, not a direct thesis challenge.

## Published Precedent And Real Assets

Reuse current source-native Makefile/executor/vllm_graph.py and unmodified vLLM FP16 graph computation; original source /workspaces/repository, yunwei356/bpfusion-dev/main base048c204ed78e006f1e31cfa8a7fb4699b7429d06. Exact cached Smol revision93efa2f097d58c2a74874c7e644dbc9b0cee75a2 and Qwen7ae557604adf67be50417f59c2c2f167def9a775.

Reuse0053/0054 ordinary split-context client, frozen whole-output pools, protocol/history/KV and lifecycle suites. Official [vLLM benchmark metrics](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics) define client TTFT/TPOT terminology. We use the retained finite output-token throughput window, not an official OpenAI benchmark/SOTA comparison.

Necessary glue is only TEMP harness mode selection and private executable paths. No production source edits, new public flags/modes/interfaces or persistent configuration. Existing Makefile BUILD override creates candidate/control/native libraries and symlinks in this TEMP; it avoids overwriting four unowned root loop_trace artifacts. Root build/bpfusion_load and build/uring_loop.bpf.o are existing shared qualified tools/objects and will be read-only/frozen/preserved. Adapter entry-derived .so lookup supports private symlinks; its resolved source/root and model calculation remain unchanged.

## Comparison

Candidate: current vllm_graph_uring_loop, independent resident GPU network worker, host-mapped regular bookkeeping, per-entry ring publication, standard model dispatcher.

Main baseline: efficient vllm_graph_user_network_wait native epoll TCP, identical reused model math/padding/prefix release. It represents the strongest runnable competing CPU request/reply mechanism; it needs a fresh matched run because current source/context cannot be numerically settled by old matrices. If it wins, no native-superiority claim. A crossing0 interval does not prove equivalence/NI.

Component control: current vllm_graph_uring_loop_coalesced with finding0053 final-response/SQ gate and batched ring publication, same mapped bookkeeping. It is not an external competitor. The existing BF_IO_COALESCED conditional changes the whole arrangement, not only overlap; label that scope honestly.

Same current source, common private runtime vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0/libbpf1.6.3, compiler sm_120, FP16 weights/KV, four frozen prompts, warmups/output budgets and no condition-specific tuning. All three targets are freshly built via their existing Makefile definitions under private BUILD. No historical saved ELF is substituted; intended compile flags differ and instruction equality is not claimed.

## Workloads And Metrics

Two already-output-qualified models, local token-ID HTTP/binary scope; no arbitrary text, other model, AMK or kernel-portability transfer. Primary: gen64/c8 client output token/s, candidate minus coalesced and native, separately by model.

Secondary: gen1/c8 TTFT; gen1/c1 and gen64/c1 TTFT/completion/TPS/TPOT; partial known-worker CPU; same-process short and long model rounds. Retain all signed means/contrasts and nominal paired t95(df4,2.776445105), not familywise/equivalence scores or pooled-request inference.

Five paired process blocks, short-only((1,8),) and transfer((1,1),(64,1),(64,8)),32 measured requests/cell,8 sequential gen1 warmups/executor. Five of six path permutations; odd blocks reverse context/model/cell order. Source and serialized client timestamps authenticate rounds minus8 for short and minus2088 for transfer gen64/c8. Whole-transfer CQ-SQ excess is descriptive multishot traffic, not per-cell cost or exclusive mediation.

Correctness: fixed frozen complete-output pools, client reply status/length/tokens/arrival, graph errors/accounting, actual physical slots FREE/bitmap/recycle and ring pending/error/drop/overflow. Ordinary trajectories are unobserved; pool membership is finite, not fresh eager-HF arithmetic parity. Candidate-only622-request22224-token259-rejection5000-empty-connection suite for both models includes actual trace/history/KV replay. Existing coalesced/current math qualification from0054 is reused rather than rerun unnecessarily.

Two candidate32-action lifecycle suites check652 complete-or-prefix tokens each, reset/stop/half-close/reject/reconnect,13 connections32 completions3aborts, separately empty SQ/CQ, eight FREE slots/bitmap0/recycle32 and intentional admitted32/retired31. Independently inspect actual raw bytes/accounting/syscalls, not only pass booleans. The old coalesced-only stdout-marker assertion is inapplicable to standalone; source/build flags plus successful standard-path execution establish arrangement, without pretending that exclusive dynamic overlap was profiled. No correctness criterion/oracle/timeout is weakened.

Cost: roughly30 minutes ordinary captures/collection plus common setup and integrated qualification; this is an estimate, not a new enforced deadline/budget.

## Planned Runs

| Run group | Role | Workload | System/method | Repetitions | Decision consequence |
|---|---|---|---|---:|---|
| Ordinary short+transfer | candidate/native/component control | two models/four cells | current standalone/current coalesced/native | 5 paired blocks | select effective current arrangement with native/latency boundaries |
| Protocol/lifecycle | integrated qualification | two candidate models | current standalone | one reused suite each | invalidate an incorrect constructor |

Full20 drivers/60 executors/120 cells3840 measured requests124800 output tokens plus480 one-token warmups =4320 complete replies125280 tokens. Preflight4 drivers/12 executors/24 cells192 measured requests6240 tokens plus96 warmups. No AMK rerun, additional weak baseline, math sweep or standalone packaging experiment.

## Execution

All project work remains in original Workspace /workspaces/repository/main. TEMP is /tmp/bpfusion-current-io-placement-6xw2vxa6. Production diff starts0; the unrelated tools/setup_env.sh stays untouched.

After independent plan admission, run python3 TEMP/setup.py. It installs/builds only this private runtime/BUILD using source-native Make definitions; no root trace ELF or common loader/BPF object is rebuilt. Freeze current source/build/env/model and expanded commands before collection. No original-source rebuild/implementation patch is needed.

Real preflight: python3 TEMP/run.py preflight1 then fixed analysis.py TEMP preflight1. Then run_qualification.py and run_lifecycle.py and fixed independent raw analyses. Maintain the skill's real preflight protocol without creating an additional control interface.

Full command: python3 TEMP/run.py full. run.py writes all20 expanded commands before execution and retains driver/stdout/stderr/executor/source/oracle/exit receipts. Continue the same live process handle until authoritative terminal status; observer timeout is not terminal/restart authority. All20 drivers/all60 executors and fixed full/long-counter analyses plus integrated qualification/lifecycle are required; a partial prefix is not the full result. Preserve failures/exclusions/deviations and never alter metric/oracle/timeouts to pass.

Sparse actual host before/during/mid/after observations preserve boot/fault/GPU-app context without continuous-isolation/all-fault-free proof or interrupting others. Fresh independent result review follows completed collection. Only then select honest docs/source policy, archive/replay, clean owned TEMP only, verify original preservation, commit/push main and public bytes.

## Interpretation

Candidate-minus-coalesced primary TPS t95 above0 supports local current-constructor recovery for that model. Candidate-minus-native above0 supports only the tested finite superiority; native wins bound it. Below0/crossing0 results are retained as contradictory/inconclusive without universal conclusions.

Secondary latency/CPU informs a source recommendation but replaces primary only if it invalidates correctness/fairness/exact claim, not as a favorable headline substitute. No pure overlap/occupancy/PCIe/GPU-time causal claim, arbitrary fairness/model quality, total host CPU elimination, energy or official full-server SOTA claim.

Target table: both-model gen64/c8 TPS with signed coalesced/native differences and uncertainty, linked secondary latency/CPU and ordinary counters. Reuse earlier AMK opposite-arrangement evidence as a scope boundary. Success means choose an existing effective route with no new code where justified; failure closes this constructor test and directs a distinct discriminator, not an unchanged rerun.

## Reproducibility Notes

Linux7.3rc3/RTX5090 original Pod/PVC/weights/cache/session remain. Current source and existing common loader/BPF object are captured; private BUILD and adapter path glue are the only recipe deviations. Exact model revisions/precision/pools/common packages/compiler/config/commands/raw outputs and standard-library CPU replay are preserved.

Before manifest captures eight preserved paths: original WIP, qwen_graph.so, four unowned loop_trace artifacts, bpfusion_load and uring_loop.bpf.o. Base Torch/Transformers/NumPy2.14.1+cu130/5.19.0/2.5.3 and Coder1/10909 remain. No retained runtime, service, credential, network, storage, machine, scheduler or branch delta. Plan/recipe materialization is preparation, not scientific performance evidence.
