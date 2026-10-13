# eBPF admission and io_uring with real HF model graphs

A finite integration prototype completes the Linux TCP/HTTP -> unchanged
eBPF/sockmap parser/admission -> mapped queue -> resident real-model graphs ->
GPU-published SEND -> ordinary kernel TCP completion -> eBPF recycling path
without loading bfusion_tx. GPU consumes ACCEPT/RECV/SEND/CLOSE completions and
the existing HF dispatcher controls model execution. Both Qwen2.5-0.5B-Instruct
and SmolLM2-135M complete12 one-token requests with exact independent HF outputs.

This is bounded correctness/integration evidence, not a reusable module-free
server or a performance result. The prototype deliberately has one connection,
12 request sequence tags, gen1, fixture timestamps and a global tracepoint
filter tied to those tags. It remains archived experimental source; production
model/transport/defaults are unchanged.

## Scope, source and implementation

Execution is in the original yunwei356/bpfusion-dev on RTX5090, kernel
7.3.0-070300rc3-generic, NVIDIA610.57.04 and installed CUDA13.0.88. Baseline
main is dc3a776fca1f89bf87978e09fb005eef64d39762. Existing base Torch2.14.1+cu130
and Transformers5.19.0, model cache, source and original Coder sessions remain.
No package/driver/sysctl/affinity/persistent-service change occurs.

The temporary BPF source is the unchanged fusion.bpf.c plus a small completion
program; the queue header/layout is unchanged. The existing loader is adapted
only for this temporary object and one additional io_uring completion link.
Sockhash capacity still discovers somaxconn4096. All owned pins are absent
before attachment and removed after each invocation.

The stock interface is SQPOLL|NO_MMAP|NO_SQARRAY, with an eight-entry SQ and
sixteen-entry CQ to exercise wrap, ordinary accepted FDs and caller-allocated
CUDA-registered host memory. Host virtual addresses go into SQEs. Startup
posts NOP and ACCEPT, performs one explicit wake, and consumes only the NOP.
The GPU obtains the accepted FD and remote tuple, posts/drains receives, maps
the peer to the eBPF slot, publishes sends, consumes EOF and posts CLOSE.
The separately running Python client actually receives the complete replies.

## Safe admission reclamation on this GPU

The live CUDA attribute hostNativeAtomicSupported returns0. A compiled
precursor containing GPU atomicAnd_system on the BPF map is preserved in
before_recycle/, but is never executed. It is not evidence of atomic support.
NVIDIA documents that mapped-memory GPU read/modify/write atomics do not in
general provide atomicity against the host; see the
[CUDA13 mapped-memory contract](https://docs.nvidia.com/cuda/archive/13.0.0/cuda-c-programming-guide/index.html)
and [current host-atomic discussion](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/unified-memory.html).
Do not confuse aligned system-scope loads/stores with shared CPU/GPU RMW.

The executed prototype leaves the shared admission RMW on the CPU/kernel side.
A SEND carries a fixture tag encoding request sequence and remaining bytes.
The completion BPF program requires matching tag, full positive byte result,
DONE state and fixture client timestamp. It then sets FREE and atomically
releases the reservation using the unchanged CPU reservation protocol. A
partial positive result does not release ownership; the GPU can resubmit the
remaining bytes. All observed replies complete in one SEND, so partial/error
behavior remains unqualified.

All GPU slot accesses precede the tagged submission. After publishing it, the
network kernel only accesses its private buffer and CQ until that reply ends.
The callback therefore does not release a slot that this finite GPU sender
will later touch. The receive parser/admission and head/bitmap CAS stay byte-
identical. This preserves wrap protection without unsupported GPU map atomics.
The fixture-specific global tracepoint/tag design is not a production ring/FD
ownership mechanism; generalizing it is required before default adoption.

## Component qualification and retained setup failures

Initial NVCC compilation fails on a mixed-type auto declaration. Splitting the
unsigned-char device pointer declaration fixes syntax only; initial source and
build errors remain in initial_build/. The safe completion version then builds
BPF, temporary loader and CUDA probe successfully. No precursor atomic binary
is executed.

The echo component runs01:29:31–01:29:51UTC2026-10-13. One cold asynchronous
ACCEPT and eight cold RECVs observe NEED_WAKEUP; connection/request arrival
completions wake SQPOLL without runtime host wakeups or keepalive loops.
Twelve fragmented requests alternate binary and HTTP, with prompt sizes
1,2,5,8,16,31,63,64,2,5,8,1. Synthetic last-input-plus-one computation is
explicitly a transport probe, not inference. All12 replies/516wire bytes match,
including full HTTP headers. Reuse passes beyond the eight physical slots.
GPU EOF/CLOSE completes, all SQ/CQ positions are28, all eight slots are FREE
and reservation is0. BPF publishes/recycles12, links one socket and reports
zero busy/invalid-parser/failed-link counts.

## Real models and pre-observation oracle

The independent oracle at01:33:17.937039UTC loads the original unpatched eager
HF model in FP16, executes each full prompt with use_cache=False and selects
the first-token argmax. It freezes both models'12 exact references before
either network-model observation. It does not use candidate outputs, cached
historical alternatives or teacher forcing. Pinned paths and actual model
dtype/runtime are in model/oracle.json; original model snapshots are Qwen
7ae557604adf67be50417f59c2c2f167def9a775 and Smol
93efa2f097d58c2a74874c7e644dbc9b0cee75a2.

Temporary qwen_graph.cu changes only transport initialization/finalization and
includes the network header. Its entire device model dispatcher is byte-
identical to current production. qwen_graph.py changes only library lookup;
weight loading, graph capture, math, FP16, greedy sampling and eight private
banks are unchanged. The independent oracle does not inherit main()'s Qwen
compilation patches. [Source identity and diffs](../../bench/results/uring_sockmap_models_20261013/model/source_identity.json)
record the actual boundary.

The network runs in a separate nonblocking CUDA stream. It waits for the
original model's DONE, copies the real token, posts SEND and leaves reclamation
to eBPF completion. There is no synthetic output or host model step in this
version. The existing host only waits for duration/stop, then tears down.

| Actual run | UTC start/end | Requests/tokens | Exact wire bytes | Native/model result |
|---|---|---:|---:|---|
| Qwen |01:34:00–01:35:19|12/12|516|exit0, one host launch,12 device model launches, graph_error0|
| Smol |01:36:29–01:38:01|12/12|516|exit0, one host launch,12 device model launches, graph_error0|

Every first token equals its exact pre-observation oracle. Both runs preserve
the same prompt sizes, alternating binary/HTTP fragmentation, cold accept/
receives, reuse, EOF and GPU CLOSE contract. BPF admits/recycles12 per model.
All queue positions28, reserved0, eight FREE slots and zero drops/overflow.
The generic native log still says resident Qwen for Smol; actual model config
is Llama30layers/hidden576/vocab49152, with its pinned path in raw metadata.

Qwen delivery finishes correctly, but the original driver's finally pin loop
shadows the model-name variable and saves bpfusion_uring_link.results.json.
The outer pipeline exits1 on the missing qwen.results.json after delivery.
The complete original JSON/stdout/driver/pipeline error remain in
model/reporting_failure/. Copying that same JSON to qwen.results.json and
renaming the cleanup loop variable repair reporting only. Qwen is not rerun.
Smol executes with the corrected driver. Neither references nor native/BPF
source change. Do not call the original outer pipeline exit0 or hide its failure.

## Verification, artifacts and restoration

[Root self-review](../../bench/results/uring_sockmap_models_20261013/review.json)
reconstructs requests, exact oracle tokens, complete client byte strings, BPF
counters, all queue positions and terminal slot state. Per-model all-thread
strace between NET_READY and native SIGTERM records zero accept/accept4,
recvfrom/recvmsg,sendto/sendmsg and io_uring_enter calls. Each process has one
io_uring_setup and one bootstrap io_uring_enter before READY. Traces cover
native userspace threads, not kernel threads or the independent Python client.
Linux TCP/SQPOLL and eBPF still consume CPU. No total CPU or energy claim follows.

All source generations, compiler commands/statuses, raw requests, oracle, actual
stdout/stderr/strace and reporting failures are
[archived](../../bench/results/uring_sockmap_models_20261013/). This is a root
self-review, not an independent paper experiment-plan/result review.

Replay without GPU from the repository root:

    python3 bench/results/uring_sockmap_models_20261013/review.py

For a fresh hardware run, copy the archive into an OS temporary directory
inside the original Workspace, substitute that new root for the recorded old
temporary path in loader.c, and use the actual builds.json/model/build.json
commands with the new source/output paths and unchanged repo include paths.
Run the component driver.py, then model/oracle.py, then model/driver.py qwen
and model/driver.py smol. Drivers write beside their source; do not run them
inside the checkout. The documented public main supplies the unchanged queue
header/vmlinux/tool dependencies. The installed CUDA/HF/clang/libbpf/strace
runtime is sufficient; no new serving environment is installed.

The restoration receipt records removed owned temporary sources/binaries and
pins, no own serving GPU process/module, same boot/base packages and retained
original Coder processes/WIP. Endpoint receipts do not prove continuous host
isolation or absence of unrelated interference.

Keep the current production module/default while generalizing and qualifying
the alternative. Concurrent connections/accept churn, gen64 token streaming,
pipelining, vocabulary rejection, partial sends, disconnect/abort ownership,
generic completion cookies/ring association, stop while I/O is pending and the
optimized vLLM adapter remain open. This finite prototype is a step toward
backend-independent stock-kernel serving, not broad correctness, novelty,
portability or speedup. A matched real-model latency/throughput/CPU comparison
must follow integration qualification; do not transfer earlier backend gains.
