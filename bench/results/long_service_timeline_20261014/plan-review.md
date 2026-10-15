# Fresh plan review: long-output GPU service-time discriminator

Observation: 2026-10-14T23:31:18.258181+00:00. One fresh PLAN REVIEW only under research-experiment-design. No build, model/bootstrap launch, GPU workload, cleanup, recipe edit, source edit or Git publication was performed. The only written artifact is this review.

## Verdict

**PASS for the stated supporting, source-neutral diagnostic. No blocking scientific or executability defect found.** This verdict admits real preflight on the existing path; it does not claim that preflight, full collection, coverage or the retained project goal has already passed.

There is no formal paper RQ/thesis contract. The concrete retained user question is sufficiently clear for this bounded supporting experiment: improve delivered latency/TPS for ordinary Linux TCP/eBPF, reused model computation and no steady userspace request worker. The review does not invent or modify an RQ.

## Reviewed evidence

Read plan.md, case.py, analysis.py, adapter.py, setup.py, run.py, source_frozen.json, adapter_semantic_comparison.json and execution-notes.md completely. Also inspected host_entry.json, models.json bindings/reference structure, current evaluation.md's opening and recent relevant sections, current background-related-work.md, findings0043/0047/0055/0056, Makefile's actual target flags, and executor/vllm_graph.cu's graph construction, launch, trace, termination and synchronization paths.

Live repository is main at 458145f495789f83ff662ec6d45b216c83ff7ae8. All twelve source_snapshot paths match their current repository counterparts byte-for-byte. The temporary adapter comparison records the observation-stripped bootstrap equality; the inspected adapter retains the ordinary model/KV/capture/replay implementation. These checks establish the reviewed state, not protection against later source drift.

## Admission and strongest alternative

Admission holds as supporting evidence, potentially decisive for choosing the next implementation investigation. The remaining efficient-native gap is a real rejection argument for a broad performance claim. Finding0047 supplies only short-output single-client model timings. Findings0055/0056 supply ordinary client timing and aggregate rounds but not current gen64/c8 kernel durations or actual matched batch trajectories;0043's copy intervention remains inconclusive. Reanalysis cannot reconstruct activities never collected.

The proposed measurement can change the next action: longer matched-stratum model intervals suggest inspecting reused execution/resource scheduling; comparable intervals with altered batch/round/gap histories suggest progression/admission; mixed, uncertain or strongly perturbed observations close this diagnosis without picking an exclusive cause. A full generic backend/text adapter is a strong alternative for OSS acceptance and remains part of the larger objective, but would not distinguish this measured performance uncertainty. Another unchanged speed matrix, speculative SENDMSG-copy change or model-arithmetic optimization has lower value for this specific next decision. This is not a headline serving result or independent dependency/checker contribution.

## Hypothesis and discrimination

The plan tests an explicit descriptive discriminator rather than presupposing GPU occupancy, PCIe traffic or arithmetic as the cause. Whole-workload kernel union/span, rounds, actual batch trajectories and query/batch strata can distinguish observed service-time association from additional rounds or inter-round availability gaps. Different batching, KV/context histories and scheduling remain constructor-level differences. Even a same query/batch stratum does not isolate context length, request identity or a hardware mediator.

The script's signed paired effects and five independent process-block means are coherent with the plan. Per-stratum tables retain individual blocks; they should inform interpretation alongside aggregate duration effects. A crossing-zero interval is not evidence of equal service time, zero profiling overhead or equivalence. A lack of resolution is an admissible inconclusive outcome, not a reason to extend the unchanged matrix. A contradiction bounds these two constructors/workloads rather than refuting a nonexistent universal thesis.

## Baseline, computation and correctness fairness

Efficient native timed-epoll TCP is the single credible main competitor. It uses the same vLLM graph computation, pinned model snapshots, FP16, input prompts, output budgets, prefix release and padding policies. Its success/loss changes the bounded interpretation; unrelated published hardware numbers cannot replace this matched numerical comparison. Unprofiled/profiled are instrumentation ablations, not additional main baselines. No further baseline is necessary for admission.

The actual Makefile gives both selected trace targets BF_TRACE, BF_PAD_PREFILL and BF_PREFIX_RELEASE; their transport-specific flags select the intended loop/native paths. Both conditions per path resolve to the same privately built shared library, and the adapter only adds observation. Models use Qwen snapshot7ae557604adf67be50417f59c2c2f167def9a775 and Smol snapshot93efa2f097d58c2a74874c7e644dbc9b0cee75a2. The real fixed prompt lengths are2/5/8, so the catalogue's query0/2/5/8 and batch1..8 covers all possible selected graph descriptors.

Pre-observation whole-sequence membership is supplemented by current admission/request matching, physical-slot ownership, release/history conservation and replay of the reused graph after profiling ends. Client replies, traced tokens and replay must agree. This is a strong finite execution/fidelity check for this comparison, not fresh eager-HF arithmetic parity or arbitrary backend qualification. The old AMK eager-HF failure remains failed and does not become accepted through this vLLM diagnostic.

## GPU grouping, coverage and time definitions

Count-based ordered kernel grouping is justified for the reviewed source. A combined graph contains a model body child followed by a dependent sampling/head child (executor/vllm_graph.cu228–240). The dispatcher launches one selected model graph, then schedules its own tail launch; on that subsequent dispatch it records the completed round before selecting the next one (57–75,165–180). CUDA tail-launch ordering waits for the preceding launch environment's outstanding work, giving serial model-round order. Thus the chronological model-kernel groups correspond to ordered compute records when complete coverage and the non-overlap check hold. See [CUDA device graph execution](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html).

analysis.py60–75 excludes the known dispatch/io_network kernels, requires total model-kernel count to equal the sum of recursive graph counts, partitions by each actual query/batch count, requires unique graph/node identities within each group and rejects overlapping consecutive model rounds. Catalogue construction recursively counts child graph node types. Bootstrap/capture and replay kernels fall outside the profiling region; persistent dispatch/network activities remain outside model spans. The real preflight is appropriately responsible for proving that the actual CUPTI/PyTorch export supports these assumptions. Missing/ambiguous coverage cannot be imputed or counted as a successful decomposition.

One reporting limitation is nonblocking: memcpy/memset counts are checked across the whole profiled serve (analysis.py63–66), whereas kernel counts and graph/node uniqueness are checked per round. The current adapter records node-type counts rather than a descriptor-to-instantiated-node identity catalogue. Consequently the automatic analysis alone does not establish the plan wording's strongest literal claim of independently verified memcpy/memset correspondence for every round. Describe the actual checks accurately in the result report; preserve raw events for the already-required independent result review. This does not invalidate the proposed kernel-only union/span diagnostic: memcpy/memset durations are not added to its model-kernel union and the serial source supplies round order. No additional instrumentation or production code is required by this review.

All reported GPU durations subtract timestamps within the GPU trace; they do not need an absolute CPU/GPU clock offset. Model span includes kernel gaps and head work, kernel union excludes the gaps, and inter-round gaps include dispatcher/network/request-availability effects. These measures do not independently isolate full graph elapsed time, transport time, bandwidth, FLOPs or overlap/resource causation. Leading/trailing delivery work is outside the model epoch, so this epoch is not an exact decomposition of the client token window.

## Profiler perturbation

The setup sequence matches the documented API ordering: enable device graph collection before CUDA initialization, initialize the driver, then enable HES before context creation. Status assertions are real, not assumed. [CUPTI Activity API](https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html) specifies these requirements and hardware node-granularity collection for device graphs. Profiling surrounds serve after model/bootstrap capture and ends before replay.

The two profiling conditions per path test perturbation in client timing and actual round histories. Equal BF_TRACE across all four conditions is fair but does not establish neutrality relative to ordinary untraced serving. Prior findings are therefore contextual evidence, not numerical ordinary-substage allocations. Path-specific profiling effects, changed batch trajectories or large perturbation can make transfer inconclusive even with a complete trace. No exact ordinary percentage or exclusive cause is justified merely because a nominal profiling interval crosses zero.

## Executability, repetition and honest completion

The checked setup creates a private runtime/libbpf/build and compiles the existing native targets. Expanded commands, all statuses, raw replies, source/library metadata, traces, catalogues and history replay are retained. Preflight has four Qwen executors,8 measured gen64 requests each plus8 checked warmups. Full collection has40 executors,1280 measured requests/81920 measured tokens plus320 checked warmups, five paired blocks across both models/paths/profiling states. Eight preopened closed-loop client lanes avoid counting connection/bootstrap inside the measured interval. Rotation of condition order and reversal of model order reduce systematic order exposure without promising isolation or randomization.

The driver verifies child exit0, admissions/retirements, graph errors, loop/native transport counters and separate SQ/CQ drainage. The fixed analyzer requires successful case terminals, exact request indices and token counts, trace overflow0, reply/history/replay agreement and all expected cells. Failures remain visible; a failed control cannot become a loop win. The fixed300-second serve duration begins after bootstrap and is not a new task investigation deadline. Sparse host observations, old NVRM warnings and the retained400W setting bound scope; they do not prove continuous exclusivity, clean fault history or energy/total CPU savings.

Primary TPS and latency terminology has an official defining source in the plan ([vLLM benchmark metrics](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)); the finite token-ID closed-loop adapter is not an official full text/API benchmark. Duration decomposition is an internal diagnostic, not a new score. The proposed commands and completion requirements are adequate for preflight/full collection with the stated20–40-minute estimate treated only as cost guidance.

## Latest entry observation

The added host_entry.json is an entry snapshot, not a run result: boot04dc0087-5ccc-4c46-9997-b9a92f0e5167, MemAvailable88929096kB, empty compute-application observation, and retained older selected NVRM warnings. The GPU snapshot timestamp is2026-10-14 16:29:44 and identifies the Blackwell RTX5090/driver610.57.04. This supplies real entry context without resolving continuous interference or declaring those warnings harmless. No build/model/GPU condition had started at review.

## Result boundary

Report every signed block, profiler contrast, actual batch stratum and failed/deviated row. A complete valid result may be supporting and inconclusive. It cannot establish generic Linux/kernel/backend portability, SLO capacity, full-text service, total CPU/energy elimination, exact untraced serving decomposition or universal superiority. Preserve the original Workspace/session/WIP and full project objective. Optional report wording improvements are not execution blockers.

Blocking defects: **none**.


# Follow-up1: explicit preflight repair revision1

Observation: 2026-10-14T23:46:18.773895+00:00. This is the first follow-up to the same fresh plan review, not a new protocol/reviewer. Read revised plan.md, adapter.py, case.py, analysis.py and replay.py completely; compare the three preserved pre-repair recipes and current executor/vllm_graph.py, including their complete replay bodies. Inspect first-attempt statuses/raw events, the failed child's serving/export/backtrace tail, execution-notes.md and host_after_preflight_failure.json. Only this review is appended; no build, CUDA/model workload, cleanup, production edit or Git action is performed.

## Verdict

**PASS revision1 for another real preflight on the revised common path; blocking scientific/executability defects: none.** The revised path has not yet passed preflight or full execution. The first attempt is failed/incomplete and is never promoted by this verdict.

## Actual failure and preserved scope

First-attempt statuses contain loop/unprofiled driver exit0 followed by native/profiled driver exit1; only two of four conditions launched. Native/profiled delivered16 replies/520tokens, records accepted/published/completed16, admitted/retired16, graph_error0 and trace_overflows0, then exported the profile and exited-11. The backtrace includes cuMemcpyDtoDAsync_v2, cudaMemcpyAsync and Tensor.copy_ after TRACE_EXPORTED. This places the observed crash in the old post-profiler replay copy path, without establishing the CUDA/profiler/driver root cause. The completed serving prefix is not a successful experiment, a native loss or a native win.

The after-failure observation at2026-10-14T23:42:09.731582+00:00 retains boot04dc0087-5ccc-4c46-9997-b9a92f0e5167 and empty GPU application output. Selected NVRM lines increase from33 to34, with another same-type0x56 line at23:39:51. This is a recorded warning, not proof of causation, harmlessness, recovery or continuous isolation. The raw failed cell, exported trace, original recipe versions and failed statuses remain necessary provenance.

## Oracle fidelity and comparison fairness

The removed serving-adapter block is the existing trace replay, replaced only by a marker. Serving/profile setup/catalogue/model computation/stop/export logic is otherwise identical to adapter_pre_repair.py.txt. replay.py differs from current production executor/vllm_graph.py only in resolving the private copy's repository root and replacing lib.serve with status0. Its replay body is byte-identical to both current source and the pre-repair serving adapter. Model dtype/checkpoint, queue-derived KV reservation, graph descriptors/capture, padding/positions/slot mappings, deterministic sampling, token/history assertions, release ownership and reference output remain intact.

The fresh process reconstructs the complete recorded request/batch/history trajectory and executes the same body/head graphs on independently bootstrapped KV allocations. Physical page IDs or addresses need not equal the serving process: request-id modulo slot ownership, logical positions and trace history define the tested mapping, and the replay remaps these to its own corresponding pages. Every valid prefill recomputes the recorded prompt before its dependent decode sequence, so carrying the prior serving process's KV allocation is not required by this oracle. This arrangement tests replay correctness from reconstructed state rather than sharing potentially affected post-profiler runtime state; it does not broaden the arithmetic-oracle claim.

The serving child must exit0 before a fresh replay starts; case.py46–64 requires the original serving counters and the fresh replay exit0/reference file. analysis.py adds replay exit0 without removing serving exit0, token pool membership, history/release/slot conservation, replay agreement or profile-coverage checks. A partial reference file produced before a replay crash cannot pass. There is no tolerance change, result-conditioned output pool, chosen trajectory substitution or alternative expected-token oracle.

All four conditions use this additional bootstrap/replay after the measured serving interval. Although profiled cases pass BF_DIAGNOSTIC_PROFILE1 in the environment, replay.py does not interpret that variable, enable CUPTI/HES or enter a profiler; the replay is unprofiled as claimed. The same private library supplies max_tokens/max_requests and model dimensions, but lib.serve is not called in replay, so there is no second listener, native request worker or additional measured transport workload. Loop pins can remain until its driver's ordinary finally cleanup, but replay neither attaches a new BPF path nor starts I/O. Its output cannot contaminate the completed client timing interval.

The deviation changes oracle execution placement and total experiment cost, not the expected scientific answer. Equal application to both paths/profiling states and rerunning the complete four-condition preflight avoids mixing pre-repair and repaired validation regimes. The added bootstrap is outside metrics; its potential thermal/cache/history effects on a later process are part of the shared-device/order limitation, not proof of neutral carryover. The condition rotation and sparse host evidence continue to bound inference.

## Parser, trace and coverage preservation

The profiler remains around only lib.serve after bootstrap capture, and closes/exports before adapter finalization. Fresh replay reads model.gpu.jsonl and writes only its adjacent references file; it does not rewrite raw admissions/computes/releases or trace.json.gz. No observed GPU event is synthesized or trimmed. Kernel grouping/counts, whole-serve memcpy/memset counts, graph/node uniqueness, serial-order/non-overlap checks, selected-round logic and all TPS/span/union/gap formulas are unchanged. The plan now correctly states whole-serve memory-node coverage rather than literal independently verified per-round memcpy/memset identities; this addresses the prior report's scope wording without weakening the implemented test.

All six current/preserved recipe texts parse as Python, and replay.py also parses. This is read-only static executability evidence, not substitute preflight. The replay's private entry name begins vllm_graph and has its adjacent .so symlink, matching the unchanged native library-selection rule. It uses the same pinned runtime/env/model binding and archived trace path. Reference matching still occurs after replay and serving both succeed.

run.py/case.py retain stage preflight keys rather than an attempt suffix, and use mkdir/exclusive raw creation. Thus a direct rerun into the existing active names would intentionally collide. The stated preservation of first-attempt artifacts and use of a fresh active preflight prefix/location must be concretely performed before launching attempt2; the already-planned archival move can satisfy this without changing a recipe, oracle or metric. Preserve the failed original logs and recipe bindings together, and do not pool their prefix with attempt2's four successful-condition requirement. This is ordinary announced rerun preparation, not a reason to reject the repair design or add a new interface.

## Remaining limitations and next valid evidence

Revision1 avoids the observed post-profiler in-process replay location; it does not establish a repaired driver/profiler fault or guarantee that serving finalization/fresh replay will run. A new serving exit failure, replay failure, missing activity or inconsistent oracle remains a failed preflight rather than an excluded nuisance. Real attempt2 must complete all four conditions and their fixed analysis before full collection; full remains40 serving drivers/executors plus40 separately recorded replay children, with both exits required and the increased40–70-minute estimate explicitly just cost guidance.

The original bounded graph replay/Frozen-pool scope, BF_TRACE transfer uncertainty, profiler perturbation, finite workload, constructor bundles and sparse host limitations remain. The repair admits no universal model/backend or arithmetic fidelity claim. Prior PASS reasoning for admission/native baseline/serial kernel grouping remains applicable; no additional numerical baseline, production instrumentation or oracle loosening is requested.

Blocking defects in revision1: **none**.


# Follow-up2: source-native I/O initializer classification

Observation: 2026-10-14T23:58:14.609707+00:00. This is the second and final follow-up under the same review/protocol. Read current analysis.py and its complete pre-fix version, the appended plan clarification, execution-notes.md and all preflight.analysis.before_initializer_fix receipts. Inspect current/frozen io_uring_tcp.h initialization/synchronization and both actual profiled attempt2 traces read-only. Append only this review; do not run fixed analysis, any serving/model/CUDA process, build, cleanup, source edit or publication.

## Verdict

**PASS the explicit observation-classification repair; blocking defects: none.** Retain the earlier failed analyzer receipt and rerun the fixed CPU analysis on unchanged attempt2 data. This review does not substitute for that analysis or declare the full matrix complete. No new reviewer/protocol or further plan-review round is called for by this verdict.

## Source and raw evidence

The preserved analyzer failed at2026-10-14T23:54:21.243767+00:00 on loop/profiled model cardinality24615 versus catalogue-derived24614. The revised second-preflight statuses already record all four serving-driver exits0, and both inspected profiled case records contain serving and fresh replay exit0. This is an observation parser error after serving, not a failed model/transport cell to discard or replace.

io_uring_tcp.h98–102 defines io_initialize(IoState*) exclusively to initialize connection/free-list and request state. It neither computes model output nor executes a captured model graph. uring_start480–490 uploads state, launches io_initialize<<<1,1>>>, checks its launch, synchronizes default stream0, launches the persistent io_network kernel and then emits NET_READY. The default-stream model parent starts after this uring_start completes. The inspected current header remains byte-identical to the source_snapshot header; this initialization was present during collection rather than invented after observing results.

Actual loop/profiled trace has24691 total kernel records:24614 model records,75 dispatch records,1 io_network and1 io_initialize. Its74 actual compute records require exactly24614 recursive catalogue kernels and74 graph memcpys; observed graph memcpys are74. The single initializer has name io_initialize(IoState*), graph/node IDs0, grid[1,1,1], block[1,1,1], start1164819318105.935us and duration211.456us. It ends at1164819318317.391us, before first model kernel1164819388518.177us. It cannot be the first captured-model kernel or a measured-round event.

Actual native/profiled trace has24961 total kernels:24885 model records and76 dispatch records, with no initializer or io_network. Its75 compute records require24885 model kernels and75 graph memcpys, all observed exactly. Thus the extra loop record has a concrete source-native identity and timing, while the model count remains exact in both constructors. No missing event is hidden by adding this exclusion.

## Scientific legitimacy and fixed classification

The original analysis excluded known controller kernels from model-only span/union. It omitted one newly relevant source-native controller initialization relative to the earlier short-input profiler precedent. Adding this explicitly identified initialization to that same non-model class corrects the intended model-activity definition; it does not redefine successful model coverage or alter the measured request interval.

The diff is narrow: classify dispatch/io_network/io_initialize separately; require exactly one initializer in a loop profile and zero in native; require graph/node0 and exact one-block/one-thread geometry; require its end no later than the first model-kernel start; retain controller names/timestamps/durations/graph IDs in non_model_kernel_records. The existing exact recursive model-kernel count, per-group identity uniqueness, serial/non-overlap, whole-serve graph memcpy/memset checks and every duration/TPS/oracle formula remain byte-identical outside this inserted classification block.

This is not an arbitrary extra-record allowance, tolerance, generic name-based dropping of unknown kernels, clipped tail, synthesized activity or path-specific native penalty. An unexpected model kernel, duplicate/missing kernel, extra initializer, initializer inside the model epoch, wrong geometry/identity or initializer in native still makes the relevant check fail. The matching prefix corresponds to the one actual function in reviewed source; it does not authorize future unknown activities to be silently reclassified. Both full paths will use this fixed classification before their results are observed.

Raw trace.json.gz records are retained unmodified; controllers also become visible in analysis output. The initializer duration remains part of the trace's serving startup region, while client TPS excludes that startup by the unchanged client-window definition. Report this observation correction and both failed/successful analysis receipts. No serving rerun is scientifically required: the token oracle, source, profiling activity collection, actual requests and all four serving/replay exits were already unchanged, and only CPU event classification was wrong.

## Remaining boundaries and closure

Source-native initializer classification does not establish post-profiler crash causation, ordinary BF_TRACE neutrality, profiler non-perturbation, per-round memory-node identity coverage, continuous isolation or exclusive hardware mediation. Those prior limitations remain. The timestamp check uses a single GPU trace time domain, avoiding any CPU/GPU absolute-clock subtraction. Model/kernel union/span/gaps remain the same intended diagnostics.

The corrected recipe parses as Python. Independent read-only raw counting establishes the initializer explanation and exact kernel/memcpy totals for the inspected profiled preflight traces; it is not the complete fixed preflight analyzer receipt. After this last follow-up, fixed CPU preflight analysis and then the already-planned full matrix/result review are the relevant evidence paths. There is no remaining blocking issue that requires closing the proposal, adding instrumentation or widening the experiment.

Blocking defects after the final follow-up: **none**.
