# 0079: Ordinary kernel-network targets reuse LLM and opaque graph backends

2026-10-17 UTC. [Implementation/validation record](../../bench/results/kernel_network_integration_20261017/result.md),
[build/source/raw/replay](../../bench/results/kernel_network_integration_20261017/).

The measured0077 transport is available as executor/kernel_tcp.h,
bpf/kernel_tcp.bpf.c and shared CPU-state header. Explicit normal Make targets
vllm-mixed-kernel-network[-trace] and graph-server-kernel-network select it.
The same BPF loop owns TCP/CQ/SQ/connections/replies for mixed LLM generation
and caller-owned graphs. Model/graph computation is reused; no GPU networking
CTA is present. Existing selected0074 target semantics/default8 stay.

Normal8/16 builds pass. Compiled model dispatch matches native/selected/private
candidate at1464ordinary/1656traced instructions; graph dispatch matches at376.
Default8 Qwen/Smol each pass640 outcomes/23376 replayed tokens,including259
intended rejects,and144-action ordinary reset/backlog-stop qualification.
Archive CPU replay matches analysis byte-for-byte. Four default8 cuBLAS/cuFFT
kernel/native cells pass182 checks each,with independent analytic numerical
oracles and connection/cancellation coverage. Unobserved canceled requests
and bounded diagnostic reply-record truncation remain explicit.

See [getting started](../getting-started.md#experimental-kernel-owned-networking)
and [graph caller guide](../graph-backends.md#experimental-bpf-owned-networking).
The graph boundary remains experimental fixed buffers/ABI1/at most64words,
with separate autoregressive scheduling. Arbitrary CUDA/model plugin support
and broader hardware/kernel compatibility are unproven.

This is an engineering reuse/reproducibility milestone,not a new scientific
speed result or selected faster default.0077/0078 performance limits and
historical6.36ms/total-resource attribution gaps remain. No model-specific
GPU kernel optimization or persistent runtime service is added.
