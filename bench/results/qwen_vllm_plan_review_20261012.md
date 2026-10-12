# Independent plan/code review: official token-only vLLM comparison

Reviewed on 2026-10-12 in the retained bpfusion-dev Workspace. Read-only review
except this requested report. No GPU/model/server task, production edit, Git
publication, process signal or additional agent was performed.

## Verdict

Scientific admission: accept as supporting engineering evidence.
Initial execution verdict: the owned-orphan cleanup defect below required
repair before launching. The focused follow-up at the end verifies that repair
and closes the blocker. Final verdict: accept for real preflight and the
declared full matrix. Do not count setup or preflight as a competitive result.

The source inspected was at main cc2409992601c4b840f3883cb350a61777805195.
Plan and adapter are currently untracked ordinary benchmark artifacts.
The current production resident request helper differs from the historical
20261010 helper; this review read its current implementation, not an old copy.
No paper RQ/thesis is invented. docs/evaluation.md:3-7 explicitly identifies
the retained engineering objective without a formal paper contract.

## Admission, competitor and interpretation

qwen_vllm_plan_20261012.md:11-30 states a decision-relevant question: client
throughput/latency against a credible optimized official server. Component
comparisons preserving the HF graph computation cannot answer this. A loss
changes the next engineering priority toward computation/batching/scheduling;
a gain is bounded to this finite workload/interface/hardware condition.
Mixed or inconclusive results remain such. The single official vLLM competitor
is sufficient for this experiment; no extra external server is a condition.

The plan's introductory statement that earlier host controls are serial is
historically overbroad: finding0024 qualified an eight-bank concurrent host
control. Correcting that wording would improve accuracy, but it does not
invalidate admission: the missing official optimized external comparison
remains materially different from any component dispatch control.

The method uses current build/qwen_graph, not the old fc58 temporary compute
adapter. Current method has eight private batch1 graph/KV banks and fork/join;
vLLM may tensor-batch, schedule asynchronously, cache prefixes, and use its
native optimized attention/graph paths. These differences belong in a strongest
whole-system comparison. Equalizing them by disabling optimizations would make
the competitor weaker. This is not an isolated experiment on eBPF, CPU
dispatch, a particular GPU kernel or scheduler.

Token inputs, checkpoint, fp16 dtype, greedy decoding, fixed output lengths,
client concurrency and prompt schedule match. Binary HTTP versus JSON/SSE,
different contexts/cache footprints, separate Torch/Transformers distributions,
server authentication work, and client framing/serialization paths remain
explicit interface/runtime differences. They prevent isolated kernel/control
causality. They do not by themselves invalidate a scoped client-observed
comparison. Four short repeated prompts and closed-loop loads cannot establish
production diversity, open-load capacity, robust tails or total-service quality.

## Installed official source and defaults

Inspected the existing temporary environment's distribution METADATA:
vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0,
flashinfer-python0.7.0.post1. These match the saved versions record.
qwen_vllm_dependency_install_20261010.txt:755-758 records successful install and
EXIT0; /proc/49482 is absent at review time. The existing venv executable is
present. This confirms reusable dependency state, not GPU compatibility or
server acceptance.

Source root:
 /tmp/bpfusion-vllm-uapngodu/venv/lib/python3.12/site-packages/vllm

Relevant actual defaults/source:
- config/cache.py:103 has gpu_memory_utilization default0.92; :142 enables
  prefix caching by default.
- config/scheduler.py:135 enables chunked prefill; :209 allows automatic async
  scheduling selection; :214 has stream_interval1.
- engine/arg_utils.py:2460-2461 skips tokenizer initialization for tokens-only.
- The adapter command does not set eager mode, kernel/backend selection,
  max_num_seqs, max_model_len, graph mode, prefix-cache disable, or scheduler
  disable. Thus it does not deliberately suppress default optimizations.
- These are configuration/source facts, not proof of the actually selected
  SM120 kernel, graph mode or scheduler. Real startup logs and terminal result
  review must verify intended optimization engagement. Compatibility/startup
  failure cannot be counted as BPFusion winning.

The proposed utilization0.35 fallback is acceptable only after the actual
default allocation failure and a live memory observation, as written. Preserve
that failed attempt and disclose the resulting cache/allocation difference.
Do not apply it preemptively, sweep it for a preferred result, or retain it as
a production service setting.

## Token-only protocol, decoding and arrival timestamps

The installed source matches the adapter:
- entrypoints/scale_out/token_in_token_out/protocol.py:145-219 defines token_ids,
  sampling_params, return_token_ids and stream.
- serving.py:241-257 respects explicitly supplied max_tokens, forces no
  detokenization in tokens-only mode, and uses RequestOutputKind.DELTA for
  streaming. The current protocol does not require a newer output_mode field.
- serving.py:455-513 returns prompt IDs once when requested and returns delta
  choice.token_ids. :527 and :567 emit LF-delimited SSE and the DONE frame.
- api_router.py:46-73 exposes /inference/v1/generate via StreamingResponse with
  text/event-stream. stdlib http.client handles HTTP chunk transfer framing.
- sampling_params.py:225,244 defaults n1 and repetition_penalty1.0. The cached
  Qwen generation_config contains repetition_penalty1.1, but this token-only
  serving implementation only applies generation-config max_tokens defaulting
  when the request omits it; the explicit token-only request retains the
  SamplingParams defaults. Therefore the inspected request is ordinary greedy
  argmax without the checkpoint's text-generation repetition penalty.

qwen_vllm_compare_20261012.py:29-66 timestamps read1 completion before JSON
parsing, then assigns that timestamp to complete SSE frames and their tokens.
It does not count metadata frames or DONE as output tokens, handles multiple
frames/read and fragmented frames, validates prompt echo, vocabulary IDs,
requested length and finish_reason length. Multiple tokens/read share the
arrival timestamp. Current resident_dispatch.py:72-97 similarly timestamps
complete binary tokens at recv return. TTFT starts at the corresponding send
operation; body construction is outside timing. These are client arrival
metrics including their actual different HTTP implementations, not GPU-ready
timestamps or a text-tokenization benchmark.

The [NVIDIA standard definitions](https://docs.nvidia.com/nim/benchmarking/llm/metrics)
match TTFT, completion latency, TPOT excluding the first token, and aggregate
TPS over first-send/last-token-arrival. The adapter's analysis recomputes these
from stored timestamps. Five process-pair differences, df4 and critical
value2.776445105 implement the declared nominal two-sided t95 convention.
Gen1 has no TPOT interval. Separate metric/cell effects require the plan's
explicit no-familywise-superiority interpretation.

## Oracle and model identity

The fixed reference comes from existing qwen_paired_kv_20261010.jsonl metadata,
four prompts with64 outputs each. Current tests/resident_qwen.py:22-39 uses
independent eager fp16 model.forward plus greedy argmax and cache progression;
it is not generated by the candidate serving path. Adapter lines157-158
freeze the existing reference, not a fresh changing oracle.

BPFusion native_request asserts exact reference tokens. vLLM preserves actual
tokens, per-request exact equality and first mismatch and requires valid IDs
and requested lengths. This is an honest separation of numerical agreement
and fixed-length serving performance. Disagreement must preclude an
identical-output superiority claim and cannot be hidden by replacing the
oracle, excluding prompts, changing precision or only reporting matching rows.
It is not evidence of output-quality equivalence or inferiority.

Plan lines24-26 also require exported fp16 parameter-content equality with the
pinned cached safetensors before measurement. The adapter does not implement
that comparison itself. The orchestrator must supply the promised CPU-side
verification receipt and freeze current source/native identities before
collection; a matching model name alone is insufficient. This is a declared
preflight prerequisite, not a request for a new checksum gate.

## Matrix, completion and metrics

Full matrix is gen1/64 x concurrency1/8,64 requests/cell,
four prompts16 times each, five pairs and two methods:
40 cells,2560 measured requests,83200 measured tokens, ten engine exits.
Each engine receives eight excluded warmups and256 measured requests:
264 publications and8580 generated tokens/model steps. Preflight has the same
four cells at8 requests per cell with one pair:64 measured requests and1040
measured tokens. Each preflight engine receives40 total requests and780
generated tokens/model steps including warmups.

Adapter lines159-174 implement that matrix, alternate mode order for full
runs, and rotate identical cell order within each pair. Ready barriers in
lines76-95 put connections/thread creation before timed active windows.
Lines108-148 check per-cell indexes/prompt counts/reference records and
recompute TPS/latencies, then emit paired gains with the correct signs:
BPFusion-minus-vLLM TPS and vLLM-minus-BPFusion latency.

Counts alone do not prove unique coverage. The analysis does not explicitly
assert all40 (pair,mode,gen,concurrency) keys exactly once. Fresh result review
must independently verify that unique complete matrix, all actual output
counts, first mismatches, all repetitions, executor exits, model/bank counters,
zero registration/admission drops, final FREE slots, and module/hook/pin
cleanup. Code captures native stats but currently asserts only one service
launch and graph_error0. This is an independent-result-audit responsibility
already promised by the plan; it does not require another experiment.

Pooled p50/p99 are listed as secondary in the plan but not emitted by the
current adapter analysis. They can be recomputed from the retained rows in the
supplementary analysis. Their absence does not block raw collection, and five
blocks do not justify a robust tail claim.

## CPU accounting and shared-state limits

group_cpu uses /proc/PID/stat pgrp and utime+stime, covering same-PGID API/engine
processes and their threads. It excludes kernel TX/softirq and clients.
Active cells require before/after PID keys equal; that prevents treating a
changing process tree as a valid CPU delta. Idle records do not assert this,
so result review must also inspect idle key equality. Workers moved into a
different process group would be omitted; prove actual same-PGID residency
rather than claiming arbitrary descendant-tree accounting from the helper.

These counters have100Hz quantization and are not idle-subtracted. Even a
near-zero BPFusion process-group value does not imply zero system CPU cost,
because its kernel TX worker is excluded. The latest production helper has a
separate read-only TX counter, but adding it is not required to admit this
declared executor/group metric; do not call the present comparison total-host
CPU or energy. Coarse GPU endpoint snapshots cannot prove continuous
isolation. Shared-GPU interference and warm compile/cache state constrain
inference; retain all blocks without post-hoc selection.

## Authentication, logs and concrete cleanup defect

Authentication is source-native and private: adapter lines175-180 create a
fresh ephemeral key and place it only in the child environment; command,
metadata, frames and ordinary exceptions do not serialize the key.
middleware/register.py:32-36 consumes VLLM_API_KEY.
middleware/authenticate.py:11,47-61 guards /inference and returns401;
health is deliberately unguarded, allowing readiness probes.
The missing/invalid-key probes therefore precede validation and should return401.
api_utils.py:270-286 redacts sensitive CLI args; envs.py:2328-2330 excludes
VLLM_API_KEY from persisted compile-cache factors. This is not evidence that an
uninspected custom logger is safe; inspect actual logs before publishing them.

Concrete blocker, adapter stop() lines97-105 and finally lines228-229:
stop sends group SIGTERM only when p.poll() is None. If the API parent has
already exited while an engine child remains in its owned PGID, finally calls
stop because group_cpu is nonempty, but stop sends no signal, waits up to60s,
then raises. That leaves an owned GPU worker alive rather than fulfilling the
plan's cleanup boundary. Likewise, if the API parent exits normally on TERM
but a child remains beyond the group wait, the timeout only asserts instead
of completing owned-group cleanup.

Smallest repair: send SIGTERM when either the owned parent or its original
owned group is still live, tolerate ProcessLookupError for an already-empty
group, and on the group-wait timeout terminate only that original owned PGID
with an explicitly recorded forced-cleanup failure. Never broad pkill,
another service signal, reboot or credential mutation. Preserve the original
failure/result; this repair must not turn a forced cleanup into a successful
normal-shutdown record. No new helper/service/permission layer is needed.

Default process duration300s starts at serving ready in the native method;
current small fixed matrix is plausibly within it, but if a real cell reaches
that terminal state it remains a retained failure, not a reason to silently
change request timeout or count a prefix. Startup waits for readiness or actual
terminal state, so observation timeout alone is not terminal.

## Decision and next evidence

Repair only the owned-orphan cleanup defect, retain this reviewed plan and
reference, verify/freeze the declared current model/source identities, then
run the real token preflight. Runtime-selected optimized mechanisms, actual
hardware compatibility, auth responses, resource residency and cleanup still
need real receipts. If preflight succeeds, run all five paired blocks to
terminal status and submit the complete raw/logs to a fresh result reviewer.

Run status: not run; dependency setup only.
Hypothesis: untested.
Research value: admitted supporting external-serving comparison.
Paper impact: prospective additional engineering evidence; no thesis verdict.
No progress or competitiveness claim follows from this review alone.


## Focused follow-up: cleanup repair and weight receipt

The orchestrator applied the narrow repair before GPU preflight. Re-read
archived qwen_vllm_compare_20261012.py:97-112 and the existing temporary
compare_current.py. Their complete text is identical at this inspection.

stop now sends SIGTERM if the API parent OR original owned PGID remains,
tolerates an already-empty group, waits for the parent, then waits for children.
If children remain beyond the group wait it signals only that original PGID
with SIGKILL and raises an explicitly named forced-cleanup failure. The
original finally path retains that failure and rechecks owned-group lifetime.
This fixes the identified orphan-with-no-signal path without weakening normal
shutdown acceptance or targeting another service. Actual preflight/full-run
termination receipts remain necessary; no synthetic lifecycle test or GPU
task was performed by this reviewer.

Plan lines126-132 now records the defect, repair and normal full-run group
shutdown requirement. This is the same plan's focused repair, not a new
experiment or broader baseline requirement.

Read qwen_vllm_weight_match_20261012.json: at18:48:30UTC it records the pinned
checkpoint, binary/config header,290 parameter rows and494032768 elements,
with all_fp16_parameter_bits_equal true. A lightweight independent read of
those rows confirms290 unique names, their total element count and every
fp16_bits_equal true. The comparison covers the actual exported parameters;
the tied LM head is represented by the shared embedding weights.
The receipt lists production_head442ab452b38680fb4bd6aa58ff21b7ab68be4d31.
This resolves the promised weight-identity prerequisite at the receipt level,
without adding an integrity/checksum gate. Production/source/native identity
freeze for the collected run remains ordinary provenance.

Final reviewed execution verdict: accept for the declared real preflight and
complete matrix. The concrete cleanup blocker above is closed by this focused
source review. No GPU compatibility, actual optimized-kernel engagement,
auth response, normal terminal cleanup or performance result is inferred from
dependency setup, the weight receipt or this review.
