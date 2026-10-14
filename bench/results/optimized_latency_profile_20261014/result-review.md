# Independent result review: current optimized short-input localization

Review date: 2026-10-14 UTC. Fresh RESULT REVIEW, one completed run.
Reviewed frozen full source: 9b3cf6a2f0014c70010b801cb4a9d082e078a267.
Original Workspace: yunwei356/bpfusion-dev, /workspaces/repository.

## Disposition

- Run status: **valid**, for the complete finite, shared-host, profiled/ordinary observation described below.
- Tested hypothesis: **supported within the observed profiled condition; inconclusive for transfer to ordinary serving**.
- Research value: **supporting** current-backend localization. Dependency installation, preflight and archive replay have no separate research contribution.
- Paper impact: **mechanism/workload boundary and additional latency evidence**, not a direct thesis challenge.
- Next paper decision: close this finite diagnosis, keep computation reuse separate from transport claims, and choose a genuinely new discriminator or general serving/backend work. Do not rerun unchanged timer/CQ/copy variants or begin a model-specific arithmetic tuning campaign on the authority of this result.
- Blocking scientific defects in the retained bounded report: **none**. Ordinary-stage allocation, arithmetic cause and clean-host causality remain unproved, rather than silently promoted into positive findings.

The profiled model-kernel region occupies most of its corresponding short-request client interval. This establishes an observed ranking for the instrumented executions; it does not establish exactly the same ranking or fraction for an ordinary process. Both models retain millisecond-scale model spans even for the two-token prompt. Neither kernel count nor short input alone guarantees a shorter span.

## Evidence and independent checks

Read the approved plan and fresh plan review, adapter.py, case.py, analysis.py, unmodified backend_source.py, setup/build/dependency records, preflight report and raw preflight results, execution notes, all 20 raw full_*.jsonl files, all ten standard trace.json.gz files, all 40 actual host before/after brackets, the proposed finding0047 and README/evaluation changes. Also inspected production executor/vllm_graph.py, executor/vllm_graph.cu graph construction, executor/io_uring_tcp.h timer setup and source-native bench/resident_dispatch.py request timing.

I ran no model serving, CUDA setup, build or Git publication action. Independent in-memory Python analysis read every raw request and every profile trace. It recalculated TTFT from arrival_ns minus start_ns; checked frozen complete outputs, actual model/driver exit records, native counters, ordered request indices and warmup flags; reconstructed model groups, interval unions and paired process statistics without consuming the existing timeline outputs. I then replayed the final archive analyzer directly against this archive. Exit was 0, stderr empty, and stdout was byte-identical to original full_analysis.stdout.

The relocated analyzer changes prefer each case's adjacent archived trace and skip only its own .timeline.jsonl outputs. Inspection shows no change to metric arithmetic, output checks or graph grouping. The first failed archive replay remains retained and is not an excluded measurement. frozen_references.json equals the earlier0045 frozen reference bytes exactly.

## Completion and workload

The actual matrix contains Qwen and Smol, five process pairs per model, ordinary/profiled order alternating by pair. Each process runs one persistent loopback HTTP connection, c1/gen1, four checked excluded warmups followed by sixteen measured requests. There are 20 executors, 400 complete requests and tokens, 320 measured and 80 checked warmups. No case or sample is omitted.

All 20 model children and actual driver wrappers exit 0. Logs report one host graph launch per executor, 20 device graph launches, admitted=retired=20, graph_error=0, max_active=1 and trace_overflows=0. Every ring has accepted=closed=1, received=sends=completed=head=20, SQ head=tail, CQ head=tail and zero aborted/pending/error/reserved/dropped/overflow/trace_overflow. Detach status is 0. These establish successful finite completion and drain, not system-wide isolation.

The first ordinary Qwen case remains followed by a longer observer interval before the next process. execution-notes.md records a Windows wrapper-construction NameError before any affected next model starts. No affected cell is launched twice, and no workload/oracle/metric change follows. The process means remain the repetition units; the sixteen observations inside each process are not sixteen independent process replications.

## Mechanism, grouping and fidelity

Both conditions use the same ordinary vllm_graph_uring_loop.so path, recorded size197248 and inode265295, and identical adapter/client/driver source in all 20 raw metadata records. Production native/model code is unchanged. Adapter diff from backend_source.py consists of repository location, actual graph catalogue and the optional profiling/CUPTI wrapper. Its ordinary and profiled native serve arguments remain identical. CUPTI enables precede bootstrap in the profiled process, while exported profiling surrounds native serve after model loading/capture. Therefore the ablation includes the total instrumentation condition, not merely trace export after serving.

The source constructs a combined graph with body before head; the six terminal model kernels include indexing, logits GEMV and sampling/reduction/scatter. These belong in the model region. The persistent dispatch and io_network activities remain in the raw traces but are excluded from the model-kernel region.

Recursive actual graph catalogues give:

| Model | Query2 | Query5 | Query8 | Graph memory leaves/request |
|---|---:|---:|---:|---|
| Qwen | 265 body + 6 head = 271 | 271 | 271 | one memcpy, zero memset |
| Smol | 301 body + 6 head = 307 | 331 body + 6 head = 337 | 337 | one memcpy, zero memset |

Independent grouping strengthens the existing analyzer's cardinality/unique-node checks. For every one of the 200 profiled requests, its complete group has one instantiated graph ID, all expected unique node IDs, a stable exact node/name pattern for repeated instances of that query, no temporal overlap with the next request's model group, and exactly one memcpy with the same graph ID inside the first-to-last kernel span. Each query selects a stable graph ID within the process. No leftover model kernels or graph memory activities remain. Qwen traces contain 5420 model kernels/case; Smol6590/case. Across ten traces this is60050 model kernels and200 matching graph memcpy activities. Graph copy durations are submicrosecond in these records; they are covered rather than replaced by inferred kernel activities.

Counts use actual CUDA graph leaves, not captured raw-handle equality with CUPTI cloned graph IDs. Grouping is supported by c1 sequential source-native requests, graph-specific repeated patterns and the complete coverage; it is not based solely on sorting an arbitrary kernel list into requested cardinalities.

Each reply matches one complete pre-observation frozen sequence. The frozen corpus supplies a finite independent output control and is not learned from these timing outputs. This is not unrestricted correctness: current ordinary batch/KV trajectories are not independently replayed here, and gen1/c1/four prompts do not prove general text/model or task-quality fidelity. No BF_TRACE or online userspace model request worker is added.

## Recomputed measurements

Five equally weighted process means per condition, milliseconds. GPU measurements are only from profiled processes.

| Model | Ordinary TTFT | Profiled TTFT | Profiled model span | Kernel-duration sum | Kernel union | Span minus union |
|---|---:|---:|---:|---:|---:|---:|
| Qwen | 1.469674075 | 1.462109050 | 1.274583542 | 1.134865575 | 1.134866290 | 0.139717252 |
| Smol | 1.188708963 | 1.244535075 | 1.043884789 | 0.874083975 | 0.874084546 | 0.169800243 |

Independent span calculation differs from the supplied analyzer only at floating timestamp-rounding scale, below0.00000002ms; rounded proposed numbers agree. Interval sum and union differ at exported floating precision. Do not read that difference as physically meaningful overlap.

The ratio of overall profiled mean model span to overall profiled mean TTFT is approximately87.17% Qwen and83.88% Smol. These are ratios of mean durations, not ordinary fractions, whole-GPU utilization or pure arithmetic occupancy. Occupied model-kernel intervals are approximately77.62% and70.23% of the corresponding profiled TTFT. The remaining inter-kernel gaps and outside-span interval are unresolved. The kernel union counts execution intervals, not instructions, bandwidth or FLOPs, and cannot discriminate compute from memory waiting inside a kernel.

Ordinary-minus-profiled effects, nominal paired t95 with df4:

| Model | Paired differences ms | Mean ms | Nominal interval ms |
|---|---|---:|---|
| Qwen | -0.006609813, +0.043399125, +0.008510063, -0.007040687, -0.000433563 | +0.007565025 | [-0.018504051, +0.033634101] |
| Smol | -0.060902938, -0.003487625, -0.009680688, -0.051339187, -0.153720125 | -0.055826113 | [-0.130578673, +0.018926448] |

Both intervals cross zero. That means this five-block observation is inconclusive about the mean perturbation under this interval construction; it does not demonstrate zero overhead, equivalence or an optimization. In Smol, all five signs favor ordinary serving, the mean delay is55.8us, and pair4's153.7us delay remains in the analysis. A positive Qwen ordinary-minus-profiled mean is likewise not a method speedup. There is no prespecified equivalence margin and no exclusion/outlier removal.

## Prompt observations and competing explanations

The independent descriptive query groups match prompt_summary.json:

| Model | Query tokens | Measured profile requests | TTFT ms | Model span ms | Kernel union ms |
|---|---:|---:|---:|---:|---:|
| Qwen | 2 | 20 | 1.484991 | 1.306583 | 1.167289 |
| Qwen | 5 | 40 | 1.457438 | 1.262448 | 1.122448 |
| Qwen | 8 | 20 | 1.448570 | 1.266856 | 1.127281 |
| Smol | 2 | 20 | 1.350838 | 1.158677 | 1.000221 |
| Smol | 5 | 40 | 1.204390 | 1.010916 | 0.837302 |
| Smol | 8 | 20 | 1.218523 | 0.995030 | 0.821513 |

There are two literal query5 prompts but one query2 and one query8 prompt, repeated in a fixed sequence. Prompt contents, selected graph shape and request position are confounded; these data do not isolate the causal effect of input length. Smolquery2 has fewer kernels yet a longer span and occupied union. Thus counting kernels alone is not an adequate explanation. The observed behavior is compatible with graph-shape/operator-algorithm differences and other execution effects, but neither their source nor a particular bandwidth/FLOP limit is established.

Every profiled request has span below its client duration. Qwen's measured per-request span/TTFT range is about0.788–0.937; Smol's is about0.583–0.946. In particular, the Smolquery8 long client interval remains included. A mean ratio alone would hide variation in the composite outside-span path.

CPU annotation brackets and causal inequalities have a nonempty compatibility intersection in each profiled process. The analyzer labels that scope correctly. A compatibility solution does not independently establish GPU/CPU clock bias or calibrated ingress/tail timestamps; independent GPU intervals and CPU client durations are enough for the bounded duration comparison. TTFT-minus-span is not pure TCP time. Cross-node0046's3ms-scale results cannot be subtracted from this new loopback run to construct a measured network stage.

This result does not compare efficient native transport against the eBPF loop. Ordinary is an instrumentation ablation, not a main baseline. Existing matched transport work answers that separate comparison; this experiment provides no new transport superiority/equivalence, total CPU or SLO claim.

## Host state and deviations

All40 full-run health records come from actual host SSH reads, with successful journal, GPU and compute-application queries. They cover06:28:30.725 through06:42:48.884UTC and preserve the same boot ID. Their compute-application listings are empty at the brackets, GPU Recovery Action is None, and available memory remains at least112034280kB. Those discrete observations do not prove continuous isolation, default GPU policy, unchanged clocks throughout requests, zero background load or filesystem integrity.

The selected journal retains11 distinct NVRM refcnt state1/status0x56 warnings: one preflight warning and one around each full profiled bootstrap. The temporal association must remain visible. The official status-name mapping reported by preflight is not evidence of the failed reference's purpose, profiler causality, harmlessness or timing independence. There is no selected new Xid/OOM/storage/BUG and no recovery action at these endpoints. The journal must not be called clean.

The earlier05:28 OOM/storage incident is outside this full matrix, so it does not justify treating these rows as interrupted by that fault. Its existence and the current shared-host uncertainty still prohibit a stronger stable-host causal performance claim. Successful own completions cannot certify other projects' recovery or erase the warnings.

The observation wrapper NameError and first archive replay failure are apparatus/reproduction deviations, not failed model executions or timing-cell reruns. The final archive-path correction is narrow and independently replayed. No oracle, workload, excluded prefix, timer, model or numerical metric is changed during the full matrix.

## Proposed reporting and next decision

Audited the proposed finding0047, README paragraph and evaluation section. All rounded tables, totals, prompt observations and nominal intervals match the raw recomputation. The first finding wording was corrected after review from a potentially ordinary-stage/model-execution assertion to an explicit profiled model-kernel-span observation; ordinary-stage allocation remains unproved. Keep that qualification near the opening and preserve the supported-profiled/inconclusive-ordinary split.

This is credible supporting evidence that the current captured upstream computation region remains a large observed short-input budget. It supports considering reusable optimized/fused backend interfaces rather than ungrounded per-model arithmetic work. It does not prove that any specific megakernel integration will help, that gaps are launch overhead, or that eBPF removes enough CPU work to improve latency.

Close this diagnosis after review and owned restoration. The full objective remains open: general text/protocol/backend support, matched long-output/SLO and full CPU evidence, and reliable same-computation serving advantage. No additional unchanged profiling or transport rerun is needed to turn this bounded result into a more favorable one. A new experiment should add a genuine causal discriminator or satisfy a concrete acceptance gap.

Cleanup/publication are the root's remaining actions, not reviewed completion claims. Preserve TEMP until this report is received, then archive required evidence and remove only owned artifacts while retaining the original Workspace/PVC/default library/Coder and unrelated work.
