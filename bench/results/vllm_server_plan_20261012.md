# Integrate upstream vLLM graphs into the actual kernel-queue server

Retained goal: Linux TCP/HTTP/eBPF/sockmap -> shared queue -> resident real
inference -> GPU completion -> async kernel TCP, without steady userspace
request work, followed by correct matched performance controls and OSS main
publication. Previous generation qualification still bootstraps every prompt
and reserves its KV on CPU. Repeating it cannot establish the required service.

This integrated implementation and supporting experiment asks whether the
same reusable optimized graph catalogue can serve real new requests entirely
from the GPU/shared queue, and what matched client latency/throughput follows
against efficient native userspace TCP. No paper RQ/thesis is invented.
Correct integration enables the consequential identical-backend comparison;
numerical/control/lifetime failures block accepting that new path and select
a concrete repair. Null/negative speed bounds the serving mechanism rather
than prompting model arithmetic tuning.

## Reused computation and necessary binding

Keep pinned vLLM0.31.0/Torch2.13+cu129/Transformers5.17, existing checkpoints
and FP16, original bpfusion-dev/main, default optimized loader/attention/compiler.
The adapter uses the actual ModelCudaGraphManager capture path, with uniform
query lengths1..64 and batch sizes1..8 derived from the canonical queue.
Separate owned managers retain prefill outputs and explicit descriptors for
all batches1..8, including3/5/6/7 missing from the default catalogue. Query1
provides both one-token prefill and decode. Official compute_logits/gumbel_sample supplies greedy output.

Only bootstrap creates graphs/inputs and reserves KV pages for the existing
eight physical slots through the official block pool. Requests overwrite their
own prompt-prefix KV, ignore stale tail via current lengths, advance positions/
slot maps on GPU, publish tokens, and retain existing FIFO TX/recycle rules.
No model arithmetic, attention or sampling replacement; no new queue ABI,
network protocol, module/BPF program, persistent service, permission or limit.

Add a dedicated backend adapter using the existing map/listener/module lifecycle
and userspace_tcp.h timed epoll control. Both networking modes use identical
graphs, checkpoint/precision, GPU scheduling and state glue. CUDA runtime is
discovered from the selected Python environment; preserve the tested explicit
device-link/shared-runtime build and handle ownership.

GPU scheduling batches pending prefills of equal length, then active decodes;
all current batch counts1..8 are captured rather than assuming powers of two.
This is real tensor batching. Arbitrary arrival times may create different
batch trajectories in two serving paths, even with the same policy/catalogue.
FP16 outputs cannot be assumed identical across different trajectories.

## Independent correctness under actual batch trajectories

Use ordinary bounded diagnostic tracing, not a second controller/interface.
A traced candidate records request admission inputs/unique sequence IDs and
actual graph/batch rows/generated tokens in a GPU buffer. Its capacity comes
from the declared bounded workload; overflow is retained and invalidates the
trace evidence, not a service stop policy. Read/export only after shutdown.

Replay the recorded schedule with the independent host-launch path of the
same upstream graphs. Start from actual client/admission prompts and advance
the replay using its own sampled tokens, never the served GPU output.
Require every actual token to match the independently recomputed trajectory;
compare complete received client bytes with the trace-produced sequences.
All slot reuse/wrap, validation/rejections, fragmentation, pipeline/half-close,
mixed prompt/output lengths and shutdown checks remain required.

A trace adds instrumentation overhead. Performance rows must either use
identically traced modes and disclose that condition, or separately qualify
uninstrumented source with an adequate correctness control; do not silently
transfer traced timing to default serving. Existing eager-HF and official
vLLM references remain separate fidelity diagnostics, not fitted acceptance
oracles. Do not weaken any frozen run to hide mismatches.

## Real execution and comparison

Build through make in the owning Workspace. Temporary dependencies are under
/tmp/bpfusion-vllm-server-93s64rmc; no original Python/runtime mutation.
First real preflight is Qwen, actual TCP/HTTP request, gen64, native kernel
path and independent post-run CPU replay. Then exercise the full service
correctness/lifetime protocol and efficient userspace control, with Smol as
the second already-qualified architecture if its actual API supports capture.

The matched supporting matrix reuses the existing token-ID request protocol:
four existing prompts, gen1/64, client concurrency1/8, five paired process
blocks with alternating mode order,64 measured requests/cell and8 checked
warmups/executor. TTFT,TPOT,completion and output throughput are the existing
client metrics; no total CPU/energy or text/API claim is added.
Report actual batching and token correctness, complete failures/exclusions
and nominal paired t95 intervals. No performance threshold/tuning is introduced.

Archive actual commands/source/config/versions, build and native wait statuses,
raw client replies, GPU traces and independent replay outputs. Fresh plan and
result review; validate main commit/push and public contents. Cleanup only
owned test processes/module/pins/temp apparatus, preserving original session,
Workspace/PVC/cache and unrelated tools/setup_env.sh. Keep full scope open
until worker-free request handling and matched end-to-end evidence actually pass.

The independent Python replay reconstructs every input/position/length/padding/
KV row and slot from original prompts and its own previous output, separately
from the native C++ metadata path. It also independently validates admission
rejections. Native trace request identity is joined to actual client timestamps
and input/reply bytes; candidate trace data is not an acceptance oracle.

## Startup repair after initial real preflight

The first full 512-graph capture completed, but native DeviceLaunch
instantiation returned CUDA out-of-memory before readiness or any client
request. Its original sources/logs remain in the temporary apparatus under
initial_oom names for later archive. This is a startup failure, not a failed
model sample or performance measurement.

Default vLLM cache allocation targets its much larger model context and GPU
memory utilization. The existing queue contract owns eight slots with at
most 64 prompt plus 64 output tokens each. Bootstrap therefore binds
max_model_len to that existing 128-token context and derives explicit
kv_cache_memory_bytes from the loaded upstream FullAttentionSpec page sizes:
one allocator null block plus eight full-context reservations. The original
Worker determine_available_memory method still runs profile_run for
compilation, then its explicit-byte branch skips automatic memory-budget
profiling. The official cache allocator creates/owns all pages. Other KV
types or nonuniform groups are explicitly unsupported by this adapter.
Both transports use the identical allocation. This necessary bootstrap
deviation changes no model math, precision, protocol bound, correctness
oracle or performance interpretation. The monkeypatch is restored after
bootstrap; no infrastructure runtime configuration is retained.

Changing max_model_len also changes captured attention bounds and may change
kernel specialization. Earlier default-context qualification is historical;
the repaired path needs fresh independent replay and transfers no old timing.
An intermediate repair used the wrong installed worker class name and failed
at import before capture/request; its raw sources/logs remain under worker_import
names. The installed upstream class is Worker.
