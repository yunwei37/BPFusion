# Reused AMK computation in the resident TCP dispatcher

The optional AMK adapter now runs the pinned upstream SmolLM2-135M FP16
persistent kernel under the existing GPU request dispatcher. Model arithmetic
and upstream VM sources are unchanged. Both efficient userspace TCP and the
module-free eBPF/io_uring loop pass finite real-network checks with the same
backend. This is implementation and correctness progress; the admitted
performance matrix remains incomplete.

## Boundary and actual checks

[The plan and review](../../bench/results/megakernel_reuse_20261014/plan.md)
retain the same-backend transport control and current optimized vLLM comparison.
Upstream is RightNow-AI/AutoMegaKernel revision
884534c4d2dbed4381576f81a79ae97feca53c34 (MIT). The earlier native qualification
and its failed C++17 build are retained in the same archive.

The new Python file loads/captures only at bootstrap. The CUDA builder imports
the original public launch-argument header and loads the unmodified native
persistent-kernel cubin. GPU graph nodes patch the input token, execute
request-time prefill/decode and convert the selected token to the existing
dispatcher output type. Each token uses upstream K=1 so the existing
system-scope publication and TCP completion ownership remain in charge.
Eight private KV/graph banks reuse executor/qwen_graph.cu without edits.

The upstream named RTX5090 target describes an82-SM laptop. This adapter
discovers the actual card's170 SMs for scheduling; other cost-model metadata
is retained and supports no roofline claim. Both AMK transports use the same
FP16 weights, cpasync0 and graph construction. The host C++ adapter removes
the upstream conflicting standard flag, allowing installed Torch's default;
CUDA flags and model arithmetic remain unchanged.

The [device-argument probe](../../bench/results/megakernel_reuse_20261014/device_graph/)
passes eight complete outputs/260 tokens against pre-observation HF references.
It preloads prefixes on the CPU, so it alone does not prove request-time GPU
prefill. The first direct-launch wrapper reports CUDA801 and is retained;
the error's exact originating operation was not independently established.
The successful variant launches through a parent device graph.

Real serving checks use the unchanged source-native resident_dispatch
connect/request client and frozen0045 complete-output pools. Each transport
passes12 c1 requests/264 tokens, then24 requests/528 tokens in three
eight-client waves (gen1,gen64,gen1). Across both transports this is72 checked
requests/1584 tokens. All replies match a complete frozen sequence. Each
executor has one host root launch and zero model/graph errors. The c8 checks
reach max_active8; loop counters reach max_requests8, accepted=closed24,
head=completed24 and independently empty SQ/CQ. All eight long replies
report64 sends/63 sends before the final token, followed by correct short
requests. This proves the tested streaming/reuse boundary, not arbitrary
model support or complete protocol qualification.

## Reproduction and remaining work

With the pinned upstream source outside this repository on PYTHONPATH and
its native-build dependencies available, use the recorded build command:

    make amk-graph-uring-loop amk-graph-user-network-wait AMK_PYTHON=/usr/bin/python3

The source-native bootstrap entry points are build/amk_graph_uring_loop and
build/amk_graph_user_network_wait, each taking MODEL [SECONDS].
The kernel loop uses the existing stream-uring-attach lifecycle; the native
control requires no TX module or attached maps. Exact environment overrides,
drivers, raw replies, executor logs and terminal receipts are archived under
[megakernel_reuse_20261014](../../bench/results/megakernel_reuse_20261014/).
Temporary dependency/build directories remain owned while this experiment
continues; they are not installed as a persistent service.

The current AMK checks use Torch2.14.1+cu130/Transformers5.19.0. The qualified
vLLM0.31 runtime uses Torch2.13.0+cu129/Transformers5.17. A common runtime or an
explicitly justified comparison is needed before the full three-path timing
matrix. Current setup timings are not a performance result. Strict fragmented,
rejection, pipeline, reset/idle/stop coverage and full repeated measurements
remain open. The first strict-test launcher failure (missing executable bit)
is retained; executable script mode has been corrected without changing its
protocol checks or independent eager-HF oracle.

## New strict eager-HF diagnostic failure

The source-native tests/resident_qwen.py protocol checks and independently
generated eager-HF FP16 oracle are unchanged in the archived temporary adapter.
Only launcher names, loop attachment and owned log paths are adapted. The
first attempt cannot exec the new script; its executable mode is corrected
and the failed receipt remains. The second native attempt exits1 at the third
fragmented binary request after5000 empty connections. Case2 (Write a short
greeting, gen64) diverges from this fresh eager-HF output at zero-based token16.
The observed AMK output remains a member of the unchanged pre-observation
complete-output pool, but that does not satisfy this stronger exact oracle.
The server stops cleanly with3 completed requests/192 tokens, one root launch,
zero graph errors and all eight AMK error vectors zero. These lifecycle
counters do not negate numerical failure. The stock test's finally block
also asserts its full expected workload count and produces a secondary
assertion; the earlier token mismatch is preserved. The loop strict case
was not launched after native failure. This is incomplete/failed strict
qualification, not a passed broad protocol test. The completed [current-runtime native control](../../bench/results/megakernel_reuse_20261014/native170_comparison.json)
uses the same170-SM target, FP16 and cpasync0. Official AMK per-step and
persistent executions both produce exactly the same64-token sequence as
the server, including the same token16 mismatch against this eager-HF
reference. The mismatch can therefore be reproduced without the network or
new graph adapter for this input. This narrows the failure to upstream
computation/runtime behavior for this case; it does not establish the exact
floating-point cause, all-input equivalence or strict correctness. No oracle
is expanded and no performance result is inferred.

The final actual host observation retains the same11 earlier profiler NVRM
refcnt warnings and observes no new selected Xid/OOM/storage/BUG, no remaining
compute app and unchanged boot. No own experiment process or BPF pin remains.
The original default HF library inode/size, Coder sessions and unrelated WIP
are preserved. Owned temporary dependencies remain for the ongoing experiment.
