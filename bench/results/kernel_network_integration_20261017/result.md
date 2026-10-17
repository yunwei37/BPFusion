# Ordinary kernel-network source and finite backend qualification

2026-10-17 UTC, entry main9d81013. Engineering implementation/qualification,
not an additional paper-performance experiment. [Scope](scope.md),
[actual builds](kernel_network_sourcebuild.statuses.json),
[compiled controls](kernel_network_source_compiled_controls.json),
[qualification summary](qualification_summary.json), [cleanup](cleanup.json).

## Source and public commands

The0077 kernel-owned transport now has normal source homes:
executor/kernel_tcp.h, bpf/kernel_tcp.bpf.c and bpf/include/kernel_tcp_state.h.
Those files differ from the already measured/qualified0077 snapshot only at
their maturity comment. BF_KERNEL_TCP selects the shared header in
executor/vllm_mixed.cu and executor/graph_server.cu. Math,model metadata,
GPU dispatcher and public graph ABI are unchanged.

Normal Make exposes vllm-mixed-kernel-network,
vllm-mixed-kernel-network-trace and graph-server-kernel-network. Existing
selected0074 loop/native/default8 targets retain their meaning. The new
BPF object is excluded from generic default probes like the existing loop.
No private source path, persistent service/helper, model rewrite, extra
runtime configuration or transport selection policy is introduced.

With the documented dependencies/environment active:

    make build/fusion.bpf.o build/bpfusion_load vllm-mixed-kernel-network
    ./build/bpfusion_load stream-uring-attach
    ./build/vllm_mixed_kernel_network MODEL 120

Use the existing token client/stop/cleanup in getting-started.md. For a
caller-owned graph:

    make graph-server-kernel-network
    ./build/bpfusion_load stream-uring-attach
    python3 examples/torch_graph_server.py build/graph_server_kernel_network.so matmul --seconds 120

Stop/clean one server before the next; replace matmul with fft as documented
in graph-backends.md. Native uses the existing corresponding user-network-wait
target with the same computation. Actual acceptance commands below retain
original Workspace/TEMP/model-cache paths; they are acquisition records,
not a portable installer or a claim of other-stack compatibility.

## Actual validation

Ordinary normal-Make default8 and explicit16 builds pass for candidate,
selectedloop,native and trace executors with matching BPF/loader objects.
At8,all three graph adapters also build. Expected recent-UAPI user-header
compiler warnings are retained; no build/verifier fallback is used.
Compiled CUDA instruction/control encodings:
ordinary mixed dispatch1464 instructions and traced1656 match candidate/
native/selected controls and original private candidate at8/16.
The kernel candidate contains no GPU io_network CTA, selected oldloop does.
Opaque graph dispatch376 instructions matches native/private at8.

Both real checkpoints pass the unchanged default8 protocol fixture:
640 request outcomes and23376 checked model tokens each,including259
intended invalid-input rejections; actual batches1..8. Existing independent
same-graph output replay and independently rebuilt attention metadata pass.
Both archived protocol analyses reproduce acquisition stdout byte-for-byte
with empty stderr (archive_replay.json). Examples:

    python3 protocol_analysis.py qwen_kernel_network_source_protocol8.jsonl
    python3 protocol_analysis.py smol_kernel_network_source_protocol8.jsonl

The new ordinary untraced candidate passes mid-generation reset/backlog-stop
for both checkpoints:144 recorded input actions/model,78 accepted=closed,
modelerror0, networkerror/pending/reserved/drop/overflow0,balanced SQ/CQ.
88 admitted/completed requests plus56 queued unadmitted requests remain at
stop and are canceled by teardown; this is not144 completed replies.
Every observed stop prefix is checked against the frozen complete-output
pool, including empty/partial reply cancellation. Unobserved canceled
generations are not counted as validated complete output.
The normal source tests use the same frozen pool; it is not enlarged.

Four actual ordinary opaque-graph cells pass:matmul/native,matmul/kernel,
FFT/native,FFT/kernel at8,182 checks each (180 numeric replies plus2 expected
rejects). Computation is unchanged upstream cuBLAS8x8 FP32/cuFFT32 complex64.
The original analytic CPU oracle checks exact finite chosen cases, including
signed-zero allowance. Binary/HTTP/concurrent requests,reuse,idle restart,
wrong shape rejection/reuse,half-close,pipeline40/ring wrap,RST32outstanding/
fresh request and stop32queued are included. Stop checks complete observed
numeric words and retains trailing partial-word bytes; empty cancellation
is allowed. No unobserved completion is claimed. Raw input/reply bytes and
stop observations are in kernel_network_source_graph_acceptance/.
Private graph preparation/build and its first4 checks are retained separately
in kernel_network_graph_acceptance/; neither dataset is a speed result.

Bounded reply-record truncation is explicit: protocol network trace_count640/
trace_overflow512 per model, separate from GPU trace_overflows0.
Ordinary mid-cancel head88 has no reply-record truncation. Canonical graph
kernel cells head212/222 have reply-record truncation84/94.
This truncates diagnostic records,not client replies; do not claim every
network reply record was retained. Full numeric/client/protocol raw outcomes
and all lifecycle counters remain.

## Review, limits and decision

Owner self-review follows the immature-repository OSS path: scoped diff,
normal target/selected-path semantics, source-versus-measured snapshot
comparison,compiled GPU controls,actual protocol/numeric/lifecycle cases,
archive replay,links,foreign-WIP and final cleanup. No unrelated source is
changed. Qwen/Smol imply two finite model checkpoints,not arbitrary-model
fidelity. cuBLAS/cuFFT imply two fixed-shape callers,not arbitrary CUDA-library
device-launch support. The graph interface remains experimental ABI1,
fixed buffers and1..64words; LLM generation retains a separate scheduler.
No new registry/plugin framework,text/JSON API,TLS,long-context,multiGPU or
Linux/GPU compatibility promise is made.

The scientific bounds remain0077/0078: this candidate has a small local
placement gain at higher ownedCPU, and does not establish native/official
speed superiority or fix historical6.36ms. It is now available as an explicit
experimental reproducible source target; it remains unselected as default.
No new throughput/latency experiment,primary or favorable performance
conclusion is inferred from these engineering checks.

All final owned GPU processes/pins are absent; original PID1/10909starttimes
and foreign setup_env.sh remain, shared default sources byte-match main9d81013.
Temporary remote client was already actually removed by0078. README,
architecture,evaluation,getting-started and graph-backends expose the finite
source/command boundary; builds and raw evidence accompany this milestone.
