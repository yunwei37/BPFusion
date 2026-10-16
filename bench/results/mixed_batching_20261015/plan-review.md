# Plan review: packed mixed prefill/decode

## Round 1 — fresh independent review

Verdict: **ADMIT the proposed supporting experiment for preparation and real preflight.**
There is no identified scientific defect that requires rejecting or redesigning
this comparison. This is not a statement that the candidate exists, runs, is
numerically qualified, or is supported by the host's FlashAttention2 backend.
Full collection remains downstream of the plan's own fixed real preflight and
independent numerical/transport qualification.

Reviewed the current plan and saved-data analysis in this directory; live main
`cf6bfeecc8cbe002350846b8772a23f7f631c01f`; production
`executor/vllm_graph.py`, `executor/vllm_graph.cu`; current
`docs/evaluation.md`; and the executed0064 plan/load/analyze workflow.
No formal idea-story/paper RQ contract exists at the expected repository path.
The plan explicitly preserves the user's serving/performance question and does
not claim to create or answer a new paper RQ.

Only this review and source snapshots under the owned TEMP were written.
No application source was edited and no serving/GPU experiment was executed.
The prior schedule analysis was independently rerun against the archived0064
traces; its JSON reproduced **byte for byte**, with40 traces and the stated
per-model/transport16-bank summary counts. The recomputation output was then
removed. Those counts do not contain timing information.

## Scientific admission and hypothesis

Admission holds as **supporting constructor/execution-adapter evidence**.
The current production dispatcher really does select prefill rows whenever
there is a pending prefill, withholding otherwise runnable decode rows
(`vllm_graph.cu:128-165`). The saved histories establish repeated opportunity
for mixed work, while correctly leaving the size of its latency consequence
unknown. Packing changes actual query geometry, padding and batching; an
observed gain cannot be assigned exclusively to removing interruptions.
The plan already treats this as one combined scheduling/packing intervention,
rather than making that unsupported exclusive-cause claim.

Existing0064 capacity evidence does not answer this intervention, and rerunning
0064 unchanged would not answer it either. The proposal can change whether the
constructor is selected and which improved native comparison remains necessary.
Positive, adverse and inconclusive results therefore lead to different,
meaningful next decisions. CPU attribution and another backend port remain
reasonable alternatives but do not settle this directly observed scheduling
opportunity. I do not require either before this comparison.

This cannot establish mixed batching novelty, arbitrary-model support,
untraced ordinary fidelity, general eBPF superiority, or a central paper thesis.
A valid negative result bounds this packed construction and workload; it does
not refute the broader no-steady-userspace-worker objective.

## Baseline and workload fairness

The four-condition matrix is appropriate. Mixed native FIFO is the strongest
same-compute competing transport, while the two original conditions are
component controls. No additional main baseline is required for this narrowly
stated question. A matched local run is necessary: published vLLM timings on
different models, hardware and transport do not provide this paired contrast.

Both transports must receive the identical candidate constructor, precision,
capture policy and capacity. “Same computation” here means the same constructor
within a transport comparison; the original-versus-mixed ablation intentionally
changes graph shapes and round histories. The plan explicitly acknowledges that
distinction. The claimed generic driver benefit must not be inferred from a
constructor improvement that also benefits native.

Two retained real checkpoints, four retained prompts, rates96/192, gen64 and
five paired blocks are sufficient for a finite supporting selection decision.
They do not represent a broad production workload or a capacity curve.
The balanced four-condition order and rotated rate order reduce the avoidable
order bias in earlier simple reversals. Block-level uncertainty is appropriate;
256 requests are not256 independent process replicates. Five blocks give
fragile nominal intervals and limited P99 order statistics, both disclosed.
No broader model/rate sweep is an admission condition.

## Upstream API and FlashAttention2 compatibility

I inspected the actual version-tagged primary sources, including these saved
copies in this directory:

- `review_upstream_cudagraph_utils.py`
- `review_upstream_input_batch.py`
- `review_upstream_flash_attn.py`
- `review_upstream_model_state.py`

The planned API exists in **v0.31.0**. In
[cudagraph_utils.py](https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/v1/worker/gpu/cudagraph_utils.py),
`BatchExecutionDescriptor` has optional uniform and maximum-query fields
(lines63-77); mixed FULL descriptors use request count
`min(num_tokens,max_num_reqs)` (mixed descriptor construction); and
`prepare_inputs_to_capture` sets an absent FULL maximum-query bound to total
input tokens (lines767-785). The latter is the material distinction from a
decode-only capture.

[InputBatch](https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/v1/worker/gpu/input_batch.py)
provides GPU query offsets and request/sequence metadata. Its dummy creation
requires nonempty capture requests, distributes tokens over them, and pads
remaining request offsets/sequence lengths. That makes the proposed capture
geometry plausible. It is not proof that every zero-query runtime row works
in the actual host kernels or that sampled output gathering is correct.

The
[FlashAttention builder](https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/v1/attention/backends/flash_attn.py)
still advertises FA2 as UNIFORM_BATCH, with a specific warning that graphs
captured at maximum query length1 do not handle mixed prefill/decode
(lines602-633). The plan accurately identifies that limitation and does not
silently change the advertised capability. A descriptor captured with a
larger query bound addresses the named special-case concern but is **not an
upstream guarantee** of this custom fullgraph replay on this GPU.

The
[default model state](https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/v1/worker/gpu/model_states/default.py)
exposes `prepare_attn` with independently supplied InputBatch metadata and
`for_capture=False`; it derives CPU query offsets, maximum query length and
sequence bounds rather than needing the candidate's phase counters
(lines169-231). Thus the proposed fresh-metadata reference is source-native
and implementable in principle.

These are genuine preflight uncertainties, not a demonstrated impossibility.
A failed capture or exact reference mismatch would leave the candidate
unqualified; it would not be a negative performance result. The plan says this
already, so no speculative backend modification is required for admission.
Do not convert the source warning into a claim of established compatibility.

## Correctness independence

The proposed two checks serve different purposes and are both necessary to
the stated validity:

1. Existing exact wire/history/ownership replay checks the complete serving
   path and independently reconstructs input/query/position state.
2. Fresh source-native attention metadata and model forward checks the new
   captured mixed geometry, avoiding sole reliance on replaying the same
   captured graph and gathering code that might share a capture error.

The plan requires clean histories/KV reconstruction, no candidate-observed KV
as expected state, and exact sampled-token agreement. That avoids the rejected
near-greedy threshold and accepted-output-pool expansion. Its result can support
finite traced exact execution only. A reference that merely copies the
candidate's trace query lengths, output indices or KV bytes would not implement
the declared independent check; this is an implementation audit point, not a
request for another oracle or framework.

Actual mixed execution must appear in the saved serving histories: rounds
containing both new prefill and continuing decode. Configured mixed support
alone is not mechanism engagement. Likewise retain padding rows, packed offsets,
real positions, maximum queried contexts, releases and overflow/error outcomes
needed to audit the reconstructed reference. These are ordinary raw artifacts
of the already specified check.

## Metrics, execution and interpretation

The primary per-request TPOT formula matches the
[official vLLM benchmark definition](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics).
Mean TPOT is a reasonable direct measure of the declared ongoing-generation
hypothesis. It must not be relabeled ITL P99: averaging a request's decoding
interval can hide individual stalls. TTFT/completion P95/P99 and client
scheduling lag remain essential reported secondary costs, as planned.
Connect-inclusive and scheduled-origin values must retain their explicit
origins rather than borrowing send-origin TTFT terminology without qualification.
Delivered-window TPS is a finite offered-load metric, not saturation throughput.
Process CPU remains partial service accounting.

If failures occur, retain the existing all-attempt accounting and censoring
labels; a successful-request TPOT reduction is conditional evidence, not an
unconditional latency/service win. This follows the plan's reuse of0064 client
definitions and failure reporting. No new synthetic failure penalty is needed.

The named setup/preflight/qualification/full entrypoints do not yet exist in
this TEMP. That is expected for this pre-implementation plan review, so the
proposal is **not execution-ready today**. Adapting the established real workflow
is legitimate preparation; freeze the actual runnable sources, command lines,
metric computation (including the newly selected mean TPOT), condition order and
reference path before GPU preflight, exactly as the plan states.
The real32-arrival four-condition Qwen preflight plus both-model protocol
qualification is proportionate. None is evidence of a completed performance
matrix. Full completion requires all40 executors/80 cells and fixed analyses,
including adverse and failed outcomes.

The paired signed TPOT effect and nominal t95 interval can support or contradict
this per-model claim. Intervals crossing zero are inconclusive, and TTFT/TPS
tradeoffs must remain visible even after a favorable primary. No production
selection follows from preparation, capture success, or a smoke pass.

## Optional suggestions, not blockers

A saved-data ITL/stall-tail supplement would help explain whether a mean-TPOT
change also improves long pauses, particularly given the user's tail-latency
interest. It should follow the official inter-output-gap definition and describe
recv coalescing. It is optional and does not require widening the fixed primary
matrix or inventing a composite latency score.

Keep the version-tagged source links alongside any stable documentation links,
since stable pages can drift. The current plan already pins the implementation
API version.

## Decision

Proceed to implement the necessary adapter and fixed independent reference,
then the declared real preflight and qualification. **No blocking defect is
identified in the current scientific plan.** Unsupported FA2 compatibility,
unfinished runners, or future reference mismatches must not be reported as
passes; they are the concrete questions the planned preparation/preflight must
resolve. No extra baseline, wider workload, new control interface, or additional
review round is required by this review.

## Follow-up 1 — execution-scope clarification before GPU execution

The proposed clarification **does not invalidate the finite completed-request
scheduling comparison** and does not change the Round1 admission verdict.
This is a qualification-scope change from the plan's broad reset/stop wording;
record it explicitly before execution. It is not a newly passed lifecycle suite.

I inspected the now-existing `mixed_replay.py` relevant to this clarification:
each of its two reconstruction passes zeros this bootstrap's runner KV caches,
reconstructs histories, checks exact sampled tokens, and requires complete
ownership/release accounting. Its fresh pass uses source-native
InputBatch/prepare_attn/model execution. This source inspection establishes the
intended implementation, not runtime numerical qualification.

It is scientifically sound to keep strict complete-history replay for every
new protocol/performance run and reuse cf6bfee's unchanged-transport lifecycle
evidence for its actual scope. A helper-thread SIGTERM after admitted work
completes is a normal-stop/resource check; it is not evidence about cancellation
during mixed generation. Old network/stop evidence cannot certify the changed
constructor's partial-state numerical behavior.

Mid-generation RST/SIGTERM and incomplete-prefix numerical fidelity may remain
outside this finite performance experiment. Their absence limits cancellation
and later source-adoption claims; it does not confound a comparison whose
admitted measured requests all complete and exactly replay. Do not introduce a
weaker prefix oracle merely to call these cases qualified.

An unexpected partial request, cancellation, nonzero graph error, missing
release or replay failure in the actual newly collected protocol/performance
runs must remain a failure/incomplete outcome under the declared rules. It
cannot be removed from the matrix or classified as “out of scope” using this
clarification. Retain all-attempt failure/censoring reporting as already planned.

Additional mixed mid-generation lifecycle coverage is therefore **not a blocking
scientific requirement for this completed-request comparison**. It remains a
separate unresolved integration question before any adoption that claims that
behavior. No GPU work was executed and no plan/application source was edited
for this follow-up.
