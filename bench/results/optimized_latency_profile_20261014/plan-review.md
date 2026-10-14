# Fresh plan review: current optimized-backend short-input localization

Review round 1, independent read-only review on 2026-10-14.
Reviewed plan: bench/results/optimized_latency_profile_20261014/plan.md.
Verdict: **ADMIT**. No scientific defect requiring a new proposal or a broader
baseline/workload matrix is identified. This is admission of the proposed
experiment protocol, not evidence that profiling is executable or complete.
Real preflight must establish the expressly planned coverage and correctness;
missing device activities cannot become a latency result.

## Evidence examined

Read the complete proposed plan and current production
executor/vllm_graph.py, relevant executor/vllm_graph.cu graph construction,
the optional Makefile target, findings0030/0044/0045/0046 and the relevant
current docs/evaluation.md history. Read the prior0030 analyzer and retained
adapter metadata as evidence of the prior technique, not current-backend
qualification. docs/idea-story.md is absent; the proposal expressly retains the
short-input question rather than inventing a formal paper RQ.

Official references checked directly:
- https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html
- https://docs.pytorch.org/docs/stable/profiler.html

At this review's inspection, the new temporary root contains owner, model and
frozen-reference files; the adapter, driver and replay analyzer are still being
assembled. This is normal experiment setup and not a completed apparatus
claim. The plan requires exact commands and those artifacts to be archived
before serving. I have not inspected or executed a nonexistent new adapter,
and have not run dependency setup, builds, CUDA initialization or serving.

## Hypothesis and admission

The proposed question is not answered by the existing evidence. Finding0030
profiles an older HF computation path. Findings0044/0045 measure current
optimized end-to-end local delivery, while0046 measures its real cross-node
delivery. BF_TRACE admission/compute/release records do not contain GPU model
kernel timestamps; no reanalysis of those logs can reconstruct the absent
current model span. A current device timeline is therefore independent
supporting evidence rather than another renamed network comparison.

The declared hypothesis is that captured optimized model execution occupies the
major part of gen1/c1 TTFT; the alternative is a large remaining coordination/
publication/delivery interval or profiler perturbation. Positive, contradictory,
mixed and unqualified results change the next intervention: prioritize a reused
backend integration only when model spans provide that justification; investigate
the remaining path when they do not; withhold transfer to ordinary serving when
coverage or perturbation prevents it. This bounds the tested mechanism and
workload, not the entire research thesis.

The largest credible claim is localization of this current short-request
execution budget. It cannot establish external serving superiority, a causal
network saving, device memory/FLOP limitation, general model portability or
completion of the full objective. The plan states those limits. Repeating the
already closed tiny CQ ordering or network matrices lacks this missing causal
discriminator. The proposed finite diagnosis is a reasonable immediate use of
resources; no additional baseline or model/operator sweep is required.

## Comparisons, workload and correctness

Ordinary and profiled processes must load the same actual ordinary
vllm_graph_uring_loop library. The ordinary condition is an instrumentation
ablation, not a serving competitor. Adding native TCP or SQPOLL here would not
identify the candidate's missing model spans and is unnecessary for the claim.

Two models, four fixed literal prompts, gen1/c1 and a persistent loopback
connection match the intended short-input question. Five paired process blocks,
alternating condition order, are legitimate independent repetition units; the
sixteen measured requests inside each process are repeated observations rather
than eighty manufactured independent replicates. The declared twenty executors,
four excluded checked warmups plus sixteen measured requests per executor,
give400 total and320 measured gen1 replies across the full experiment. Expected
totals and all failures must remain visible.

The unchanged pre-observation complete-output sequence set is a valid independent
finite-set check for these requests. No post-observation expansion or tokenwise
union is acceptable. It does not replay each current ordinary batch/KV trajectory
or certify task quality. Max-active1 and the narrow workload make chronological
device grouping practicable; they do not broaden correctness claims.

TTFT is source-native client duration with an official vLLM serving-metric
reference. CUPTI start/end spans, duration sums and interval unions are direct
descriptive measurements. Their fraction of client duration and gap descriptions
are correctly kept as internal localization, not novel benchmark scores.

## Actual instrumentation and graph coverage

The official CUPTI activity API confirms:
1. Device-launched graph collection is disabled by default and its enabling API
   must run before CUDA initialization.
2. Node-granularity device graph activities require Hardware Event System
   collection.
3. cuptiActivityEnableHWTrace is called after CUDA driver initialization and
   before context creation; HES is available on Blackwell and later.
These requirements match the proposed RTX5090 technique. Torch import alone,
an environment flag or a successful profiler context is not evidence of actual
device-node activity. Actual library identity and setup return values/context
state must be retained; node coverage is the decisive practical check.

Current bootstrap captures separate model-body and sampling/head graphs.
Native serve adds these as ordered child graph nodes into a combined graph,
then instantiates and uploads that graph for device launch. A top-level count
of two child nodes is not the model kernel count. The proposed recursive
catalogue must enumerate leaf types for the actual query/batch1 graphs and
include both body and head. Expected memset and any other real leaf activities
must be handled explicitly; no missing record may be relabeled an inferred
model kernel.

Because native construction clones child graphs, captured raw node handles need
not equal CUPTI graph/node IDs after instantiation. Coverage should use the
actual exported identifiers and correct complete grouping, not assume handle
equality or reuse0030's single-graph identity assertion unchanged. Count and
unique-ID checks are necessary but alone do not excuse wrong request boundaries:
every profiled request must have its complete body/head group, expected query
cardinality, consistent graph identities and no leftover unexplained model
activities. Exclude dispatcher/io_network activities from model spans, while
preserving them in raw traces. Ordinary/nonprofiled data cannot be assigned
synthetic GPU spans.

The plan already requires the complete expected activity coverage and all-request
grouping in real preflight before full collection. A profiler incapable of
providing that data is an executability failure to report, not a reason to
weaken the oracle or substitute an older backend timeline.

## Clocks, overhead and interpretation

The model first-to-last interval is offset-independent. The comparison with
client TTFT uses durations, not presumed absolute GPU-to-MONOTONIC subtraction.
CPU annotations can constrain causal compatibility but do not prove common
clock accuracy, fixed bias or microsecond ingress/tail stages. A plausible
intersection does not supply a new clock-calibration guarantee.

Model span includes genuine gaps between model kernels; span dominance alone
does not mean arithmetic execution dominates. Kernel-duration sum/union and
span-minus-union distinguish occupied intervals from intervening time, without
identifying the cause of those gaps or overall GPU utilization. Sampling/head
belongs in the model group. A TTFT-minus-span residual must stay a composite
unresolved description rather than pure TCP time.

Report the ordinary-minus-profiled paired mean TTFT and nominal t95 df4 exactly
as an instrumentation effect. A crossing-zero interval is not zero overhead or
equivalence, and a negative value is not an optimization win. There is no
arbitrary equivalence margin. With just five blocks, large variation and broad
intervals are meaningful limits; retain all individual block and prompt groups.

The plan does not define a scored binary dominance threshold. Interpretation
should therefore present the observed per-process/prompt fractions and occupied
intervals directly, and call mixed or uncertain localization mixed/inconclusive
rather than inventing a post-hoc numerical cutoff. Broad rankings must not be
transferred from profiled to ordinary serving when material perturbation or a
known host fault undermines that transfer.

## Execution, host state and completion

The real source-native optional build target exists and the real graph bootstrap/
native serve path is identified. Necessary temporary instrumentation and analysis
are an allowed adapter to official profiling, not a toy substitute inference
runner. Record exact dependency, build, adapter/client and analyzer commands and
their actual sources before serving as promised; do not describe the present
partially assembled apparatus as a qualified executable.

One Qwen ordinary/profiled real preflight is sufficient for admission's
executability test when all planned output, native-exit, graph/activity and ring
checks pass. It remains setup evidence. The full run requires both models and all
five process blocks; a partial prefix or only successful profiled executions
cannot be the completed experiment. Preserve first failure, retries/deviations
and affected-comparison reruns within the existing protocol.

The known0046 host OOM and I/O faults materially limit historical performance.
Current retained-volume state and discrete resource/journal checks are pertinent,
but do not certify continuous isolation or other workloads. Per-executor
observations must retain actual fault scope and clock brackets. A new known
failure blocks a clean ordinary-serving attribution; successful own replies do
not erase it. The plan appropriately calls for owning-path diagnosis without
stopping unrelated workloads or discarding rows.

No persistent entity, host tuning, new network boundary, model arithmetic or
production source mutation is required. Cleanup must preserve the original
Workspace/PVC/boot, default HF library, Coder processes, global caches and unrelated
tools/setup_env.sh, removing only owned temporary and named build artifacts after
their needed evidence is archived.

## Review disposition

- Planned role: supporting localization; setup/preflight dependency-only.
- Admission: valid nonduplicate discriminator of the current short-input budget.
- Baselines: sufficient; same-library instrumentation ablation is correctly named.
- Executability: plausible actual path; not yet proved, to be tested by the declared
  real preflight and full activity coverage.
- Paper impact: current mechanism/workload boundary and next-intervention choice.
- Blocking plan defects: none.
- Further coverage, more baselines, gen64/c8, remote stage subtraction and
  stylistic polish: unnecessary for this admitted narrow diagnosis.

Proceed through the declared real preflight, full collection and fresh independent
result review. Completion and any proposed numbers remain unproven until those
artifacts actually exist and cover the stated checks. Keep the full project goal
active regardless of this diagnostic result.
