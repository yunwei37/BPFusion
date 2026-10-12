Observation: 2026-10-12T20:39:31.312939+00:00

# Integrated optimized vLLM server plan review

Verdict: admitted for implementation, real TCP preflight and the declared
integrated correctness/performance comparison. No blocking scientific or
executability defect found in the proposed path. Runtime success and
correctness are unproven; this review did not build or run a GPU experiment.

## Evidence inspected

Read vllm_server_plan_20261012.md, the canonical bpfusion_queue.h,
qwen_graph.cu, userspace_tcp.h and corresponding Makefile targets in the
original Workspace. Read both previous optimized-body reuse and autonomous
generation plans/results/reviews; independently inspected their full raw
completion records. Observed main a2ecf9c4ddcd183d2ccea794e3c5ce73d7c4eae1.

The four retained upstream source files in the new owned apparatus match
its installed vLLM package bytes: cudagraph_utils.py, model_runner.py,
block_table.py and block_pool.py. Installed package metadata identifies
vLLM0.31.0, Torch2.13.0+cu129 and Transformers5.17.0. Also inspected installed
InputBatch/InputBuffers, DefaultModelState, FlashAttention metadata and
gumbel_sample source. These are the real optimized compute APIs, not a
project-authored model approximation.

Prior raw establishes nineteen complete decode groups,74 lanes and4736
checked tokens after a CPU-prefill seed, with4662 newly GPU-generated IDs,
one native parent launch/group,63 child launches/group and terminal0.
Its qualified catalogue covers only batch1/2/4/8 and query1. Neither that
result nor the earlier mirror proves new-request prefill, online batching,
queue admission, TCP response delivery or request reuse.

## Admission and claim scope

The integrated proposal fills those missing parts instead of repeating a
standalone backend probe. Positive correctness evidence enables a meaningful
matched end-to-end comparison; state, numerical or lifetime failures identify
an actual missing integration component. A null or negative performance
effect bounds the serving mechanism and does not motivate weakening the
oracle or restarting a model-arithmetic campaign.

The existing timed native epoll network path is a component control: it
changes network admission/TX while retaining the same GPU compute and
scheduling policy. It is appropriate for attributing that path difference.
It is not the official vLLM HTTP server, and cannot support whole-service
superiority over vLLM, SGLang or another optimized serving stack.
No extra external baseline is required to admit this particular comparison.

Research role is supporting implementation/mechanism evidence, with no
invented paper RQ or thesis. The full retained worker-free kernel-network
goal remains open until actual new requests and all lifetime boundaries pass.

## Source-supported execution design

ModelCudaGraphManager accepts decode_query_len, constructs FULL descriptors
with uniform_token_count, and captures through its original model/attention
path. InputBatch.make_dummy distributes an exact uniform token count when
num_tokens equals batch times query length. Capture metadata references
persistent input IDs, int64 positions, int32 query_start_loc/seq_lens, block
tables and int64 slot mappings. DefaultModelState captures worst-case
max_seq_len while allowing those GPU tensors to change at replay.

Installed FA2 advertises UNIFORM_BATCH. Its query1 special handling is not a
general mixed-prefill graph. Separate uniform-query managers are therefore
a source-supported way to capture full prompts without inventing attention
arithmetic. Actual device-launch eligibility and numerical behavior of these
new graphs still require the real run; query1 qualification cannot certify
queries2..64. Retaining separate manager outputs prevents treating a
shared output view as an independent owner.

Default capture sizes do not inherently include every count1..8. The
implementation must discover the actual descriptors and populate missing
3/5/6/7 shapes through the same upstream capture API, including query1.
The plan already requires all counts; it must not accidentally round a
three-request batch into an unrecorded four-request computation.

BlockPool.get_new_blocks removes real free blocks and increments ownership
references; free_blocks releases them. Its null block is explicitly reserved.
Bootstrapping exclusive slot-owned block lists and retaining those references
through shutdown avoids per-request CPU allocation and avoids guessed IDs.
Reserve capacity from the canonical maximum consumed context, not merely
from prompt length: P prompt tokens and G outputs consume positions0 through
P+G-2, hence at most127 positions for P=G=64. Discover actual block sizes,
cache groups, expansion factors, table strides and allocated IDs. Keep
allocator/hash ownership consistent until native graphs stop, then release
those exact owners before engine/cache teardown.

Overwriting the full new prompt prefix, using its true sequence length and
advancing decode from the independently sampled previous token can safely
ignore stale tail KV. The proof must cover actual row permutations, page
crossings, slot reuse and last-token/final-DONE ordering. Query boundaries,
is_padding and last-prefill logits indices are also mutable or shape-specific
inputs; updating only input_ids/positions/seq_lens would be insufficient.

Official compute_logits and temperature0 gumbel_sample preserve the declared
greedy compute seam without implementing model math. Body-to-head dependency
and the parent tail join must complete before publication or reuse. Shared
input/output/scratch owners require serialization across model batches;
independent per-slot KV does not make concurrently overwritten manager
buffers safe.

## Independent correctness and lifecycle evidence

Recorded schedule replay is appropriate because dynamic batch trajectories
can legitimately change FP16 greedy outputs. It is predeclared, rather than
selected after a failed frozen run. To make the replay independent, the host
path must reconstruct positions, query boundaries, sequence lengths, KV
row/slot mapping, padding and logits selection from actual admission prompts,
request identities and its own prior sampled tokens. Reusing the served
tokens or the candidate's prepared metadata/state-update routine would make
this check circular. The shared upstream model graphs may be reused.

The recorded schedule determines which original requests participate in
which graph shape; it must not redefine their prompts, token counters,
positions or completion lengths. Validate each event's unique request ID
through wrap/reuse, every active row, full received byte sequence and every
produced token. Record trace overflow or missing rows explicitly: they
invalidate trajectory evidence, not permission to call a request correct.

Existing eager-HF and official-vLLM outputs remain separately reported
fidelity controls. Prior source-native output disagreement with eager HF is
already known and cannot be hidden by calling host replay a universal
model-fidelity oracle. New prefill/batch-shape coverage must establish actual
use of request inputs and optimized model operations rather than stale
capture output. This integrated acceptance remains scoped to the disclosed
same-backend trajectory contract.

The canonical queue reserves physical slots until TX finishes all accesses,
holds the last token until DONE, and reclaims completion in admission order.
Retain those semantics for successful and rejected requests. The full
protocol checks must substantiate fragments, pipeline/half-close, mixed
lengths, wrap, immediate reuse, rejection and shutdown in both network modes.
For the kernel mode, native host work must remain bootstrap/wait/shutdown;
a Python or upstream CPU scheduling loop handling live requests would fail
the declared mechanism even if token bytes matched.

## Fair comparison and execution record

Both network modes must use the same complete catalogue, precision,
checkpoint, batching policy, GPU state glue and instrumentation choice.
Different observed trajectories are a result to report and independently
validate, not an excuse to force identical output from different FP16
computations or remove a losing condition.

Use the timed BF_USER_NETWORK_WAIT control; the busy epoll alternative alone
would not establish efficiency. Its nominal60us polling timeout is the
existing comparison condition, not identical actual wake timing to kernel TX.
Retain default server transport and disclose any test-local flags equally.

For each qualified model the declared matrix contains forty cells,2560
measured requests and83200 measured output tokens, plus80 checked warmups
across ten executors. Five paired process blocks support nominal paired
t95 intervals on per-block effects; individual requests are not independent
experimental repetitions. Preserve all declared cells and failures. Final
metric definitions and effect directions should reuse the established
client analyzer, and no significance or positive speed threshold is needed
for accepting a correct implementation.

Identically traced performance is a disclosed instrumented condition.
Uninstrumented timing needs corresponding correctness evidence; neither
may silently inherit the other's measured effect. No total-CPU, energy,
text API, arbitrary-model or physical-network superiority follows from this
matrix. Record the actual client location/topology before any network claim.
Smol must obtain its own new-graph/service qualification before inclusion;
unsupported capture is a recorded boundary, not silent exclusion.

The concrete adapter/runner/build commands are still implementation work:
none was present during this review. Complete and archive their exact
commands, sources, shape/ownership records and actual raw paths before
interpreting collected data. This is normal execution preparation, not
a reason to demand another standalone dependency experiment.

## Return

Plan admitted; blocking defects none. Proceed to the actual integrated
implementation and Qwen TCP/gen64 preflight, then complete the service
protocol and matched matrix under the fixed trajectory oracle. Obtain one
fresh terminal result review, preserve failures, verify cleanup and main
publication. Do not count this review or prior finite GPU generation as
completion of the full service goal.

Follow-up observation: 2026-10-12T21:01:58.746705+00:00

## Same-event startup OOM repair review

The recorded first preflight completed all64 query managers and512 distinct
model/head shape captures, then failed native DeviceLaunch instantiation
with CUDA out-of-memory before readiness or a client request. Its launching
status is exit1; the initial_oom JSONL retains original backend/native/driver/
client source texts and failure output. This is an executability failure,
not a numerical sample or performance result. The520 dictionary entries
include eight query1 aliases, not520 independently captured body shapes.

Read the appended plan, actual updated executor/vllm_graph.py, preserved
initial_oom records, and installed GPUWorker/FullAttentionSpec/cache-config
sources. The new binding is admitted as a necessary startup repair, with
no additional blocking scientific defect.

The adapter discovers max_tokens/max_requests from the existing native
protocol, binds max_model_len to2*max_tokens, derives actual layer page
sizes from get_kv_cache_spec, and computes one null block plus
banks*ceil(2*max_tokens/block_size). For the observed16-token blocks and
eight64+64-token slots this means65 allocator blocks,64 slot-owned blocks
and one reserved null block. It does not shorten any accepted request:
the maximum consumed position remains126, within the unchanged128-token
context capacity. The official block pool still allocates and owns pages;
no private page allocator or guessed physical-ID path is introduced.
Unsupported cache kinds/nonuniform groups remain an explicit adapter
boundary rather than silently receiving this formula.

The GPUWorker monkeypatch delegates to the original method and is restored
in finally immediately after LLM initialization. Both networking modes use
the same adapter and allocation. Required capacity comes from existing
protocol ownership rather than performance-selected memory tuning.

A documentation precision matters: the installed original method's explicit
kv_cache_memory_bytes branch runs model_runner.profile_run for compilation,
but skips the default automatic memory-budget profiling and CUDA-graph
memory-estimation branch before returning the explicit cache budget.
Calling the original method therefore does not preserve all default memory
profiling. The plan/result should describe this as the official explicit
cache-budget path, not unchanged default memory sizing.

max_model_len also feeds capture-time max_seq_len and may alter attention
launch/workspace specialization or FP16 output/timing. Model weights and
operators are unchanged, but prior default-context numerical qualification
and timing cannot be transferred wholesale. The repaired path needs its
own full preflight/service/replay validation; both transports must use this
same repaired backend in every matched cell. Preserve the failed attempt
and exact delta, and qualify repaired trajectories without changing the
predeclared replay oracle or selecting an older favorable reference.

This review does not establish that the reduced cache actually removes
DeviceLaunch OOM, that all new graphs execute correctly, or that cleanup
has completed. Those require the actual repaired run and terminal result
review. No workload, build, source/plan edit or Git operation was performed
by this reviewer; only this appendix was written.
