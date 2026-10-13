# Stock io_uring with the optimized vLLM adapter

The optional stock TCP transport now runs the existing packed-prefill/FIFO-prefix
vLLM adapter for both qualified checkpoints, without bfusion_tx or a steady
userspace request/wake worker. This is integration and correctness evidence,
not a latency, throughput, CPU-saving or novelty result. Normal serving
defaults remain unchanged.

## Changes and retained failure

Makefile adds vllm-graph-uring, ordinary and traced libraries. The native adapter
reuses executor/io_uring_tcp.h for initialization and shutdown; the complete
device dispatcher is byte-identical to public main 0af41e4 and the Python
backend is unchanged. Upstream graphs, FP16, model/head/greedy selection,
shared-weight batching, KV ownership, packed prefill and prefix release remain
the qualified implementation.

The shared network header now treats receive EOF as write-side half-close,
allowing queued replies to finish before closing. It also submits final
responses and abort reclamation in admission order. Intermediate tokens can
still stream on multiple connections. Physical-slot iteration alone could
expose a later completed response while the next wrap target remained reserved.
The FIFO rule can introduce head-of-line waiting; this qualification does not
establish optimal scheduling or overload behavior.

The first Qwen strict run times out in the unchanged mixed-length workload,
after607 delivered/admitted/retired requests. Their independent replay has
21519 tokens, but the complete622-request protocol did not pass. The raw
failure, source versions, traceback and trace are retained. No BPF map snapshot
was saved before that failure's detach, so the missing requests must not be
reported as a measured drop count or a proven exclusive failure cause.
After the final-response ordering repair, the complete original protocol is
rerun for both models, without added client barriers, changed pacing, relaxed
oracle or excluded cases. The driver additionally records exchange attempts
and pre-detach map state for diagnosis.

## Complete qualification

Each repaired model run completes622 requests,22224 valid tokens,259 intended
invalid-ID rejections and5000 empty connections. Together:1244 requests,
44448 exact valid tokens,518 rejections and10000 empty connections.
Fragmented binary/HTTP, prompt/block edges, concurrency1..8, repeated wrap/reuse,
mixed1/64 outputs, six pipelined requests half-closed before reading, HTTP400
with subsequent valid output, binary rejection/EOF and helper-thread SIGTERM
all pass. Independent upstream histories reconstruct actual admitted batches,
cache ownership and complete greedy outputs, without feeding served tokens
back into the reference. All actual batch sizes1..8 occur.

The existing analyzer recomputes both client/reference matches, compute tokens
and FIFO model release ownership. Qwen executes6738 model graphs with155
release rounds; Smol6972 graphs with146 rounds. Both reach max_prefix8 and
zero graph/trace errors. These are whole-executor diagnostic counts, not timed
cell observations or performance results.

Both stock-ring logs have5086 accepted/closed connections,622 completed/recycled
slots, zero pending/error/reserved/SQ-drop/CQ-overflow and equal final SQ/CQ
positions. All eight BPF slots are FREE, reserved mask0 and BPF drops0.
One binary invalid request per run is an intentional abort/EOF. The128-record
network diagnostic buffer reports494 omitted records while serving all622;
that is diagnostic truncation, not an execution/request limit.

All-thread native syscall traces contain no serving accept/receive/send or
io_uring_enter calls from ready until SIGTERM. Startup/shutdown calls are
outside that window. Linux TCP, eBPF, SQPOLL and other kernel work still use CPU.

The shared header is also rebuilt through make qwen-graph-uring and the
previous public HF lifecycle driver is run unchanged for both checkpoints.
Each passes8 requests,130 complete tokens plus2 checked first-token prefixes,
HTTP400/reuse, invalid binary EOF, reset after a token and in-flight SIGTERM.
Each closes5 connections and reclaims3 intentional aborts with no pending/
reserved/error. Abandoned output prefixes remain separate from complete tokens.

## Evidence and reproduction

[Raw archive](../../bench/results/vllm_uring_qualification_20261013/) retains
initial/repaired outputs, independent references, GPU and all-thread syscall
traces, exact build/install commands,201 resolved packages, before/failure/final
source snapshots, production diff and HF regression commands/results.
[Qwen reconstruction](../../bench/results/vllm_uring_qualification_20261013/qwen_analysis.stdout)
and [Smol reconstruction](../../bench/results/vllm_uring_qualification_20261013/smol_analysis.stdout)
are root self-review, not a fresh independent experiment review.

Use the documented temporary pinned vLLM0.31.0/Torch2.13.0+cu129/
Transformers5.17.0 environment; keep the Workspace base runtime intact:

    make probes tools vllm-graph-uring VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --uring --correctness --model PINNED_MODEL_PATH --output /tmp/MODEL_correctness.jsonl
    python3 bench/vllm_serving_analysis.py /tmp/MODEL_correctness.jsonl

Set PATH to that environment and VLLM_ENABLE_V1_MULTIPROCESSING=0 only for the
test process, as in the archived commands. Run each qualified pinned checkpoint.
The harness owns attachment, startup, output validation and detach.

The post-run receipt has no own GPU application, bfusion_tx or BPF pins, with
the original boot and Coder processes1/10909 retained. The temporary pinned
runtime/build outputs remain available for the directly following matched
performance experiment; their final removal is not claimed here. Original
tools/setup_env.sh remains untouched.

Next: measure stock io_uring against the efficient native alternative with
identical optimized computation, using the existing module transport as a
component control. Attribute known worker CPU honestly; neither this passing
regression nor absence of userspace socket calls demonstrates a speedup or
removal of CPU networking costs. General CUDA backends, full text/API serving,
overload/backpressure, partial-send stress, device errors and long operation
remain unqualified.
