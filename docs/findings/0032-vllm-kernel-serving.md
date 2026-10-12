# Upstream optimized graphs in the actual kernel-queue server

The optional vLLM adapter now serves real TCP/HTTP requests through the existing
kernel/eBPF queue. GPU code performs new-request prefill, dynamically tensor-batched
decode, official greedy sampling and output publication; kernel TCP handles
responses and queue recycling. Userspace owns bootstrap and shutdown only.
No model arithmetic, eBPF program, module or queue ABI is replaced.

This integration uses vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0 and the
recorded mixed CUDA12 runtime/CUDA13.0 compiler build on the original RTX5090.
The graph manager captures uniform prompt queries1..64 and tensor batches1..8.
The model's actual compute_logits and upstream gumbel_sample form the output
head. Pending equal-length prefills run together; active decodes run together.
Different arrival trajectories may produce different optimized FP16 sequences.

## Ownership and necessary bootstrap repair

The original canonical protocol allows eight slots,64 prompt tokens and64
output tokens. The adapter reserves eight128-token KV regions once through
the official BlockPool. It derives cache bytes from the loaded upstream
FullAttentionSpec page sizes plus the allocator's null block, and binds
max_model_len to128. Qwen requires65 blocks/12779520 bytes. The original
Worker explicit-budget branch runs profile_run for compilation but skips
automatic memory-budget profiling. The temporary bootstrap method replacement
is restored immediately afterward.

This replaces the default much larger cache allocation only because the first
512-graph capture exhausted memory during DeviceLaunch instantiation, before
readiness or requests. Preserve that [failed raw](../../bench/results/vllm_server_20261012/preflight.initial_oom.jsonl)
and [startup log](../../bench/results/vllm_server_20261012/preflight_server.stdout.initial_oom.txt).
An intermediate wrong worker class import also failed before requests and is
retained. Changing context bounds may change attention specialization, so no
earlier default-context correctness or performance qualification transfers.

Graph/tensor owners, output buffers and reserved KV blocks remain alive through
GPU synchronization, graph-exec destruction and independent replay. Slot reuse
overwrites prompt KV and uses current sequence lengths; stale tails are outside
attention bounds. The existing ordered DONE/TCP recycle invariant is retained.
Scope is one full-attention KV group with no context parallelism or auxiliary
hidden outputs, fixed-length greedy token-ID generation. It does not establish
arbitrary model, text API, sampling or CUDA-runtime portability.

## Real correctness qualification

The [successful real preflight](../../bench/results/vllm_server_20261012/preflight.jsonl)
returns64 client tokens, all matching independent host replay. Native startup
and shutdown report one host launch,64 device model launches and zero errors.

For both Qwen2.5-0.5B-Instruct and SmolLM2-135M, both kernel and native timed-epoll
paths complete the strict real service protocol. Each of four executors
completes622 requests:363 valid replies with22224 independently checked tokens
and259 intended invalid-token rejections. Total2488 requests/88896 tokens,
1036 rejections and20000 empty connections; no failed or excluded request.
All tensor batch counts1..8 occur in every executor. Prompt lengths include
1/15/16/17/32/64 and the original four prompts. Fragmentation, persistent
eight-client slot reuse/wrap, mixed output lengths, pipelining, half-close,
binary EOF/HTTP400, subsequent valid requests and helper-thread shutdown pass.

The GPU diagnostic trace is exported only after serving stops. Independent
Python replay reconstructs inputs, positions, lengths, padding, block rows and
slots from original prompts and its own previous sampled tokens. Served tokens
do not advance the reference. Complete client inputs/timestamps/lengths/bytes
join to that replay. This is control/metadata fidelity to the reused upstream
graphs, not an independently implemented model-math or task-quality oracle.
Earlier eager-HF output differences remain historical and explicit.

After-ready traces of all executor threads show no accept/receive/send calls
in the kernel path. Timed userspace controls engage accept4/recvfrom/sendmsg
and have kernel TX absent. All four native exits are0 with graph_error0,
max_active8,admitted/retired622 and no trace overflow. The first Qwen diagnostic
allocated capacity for2048 requests, above its622-request workload; Smol derives
capacity directly from622. Neither is a service stop policy or compared timing.

- [Reviewed integrated plan](../../bench/results/vllm_server_plan_20261012.md)
  and [plan review](../../bench/results/vllm_server_plan_review_20261012.md).
- [Qwen raw](../../bench/results/vllm_server_20261012/qwen_correctness.jsonl)
  and [reconstruction](../../bench/results/vllm_server_20261012/qwen_correctness_analysis.stdout.txt).
- [Smol raw](../../bench/results/vllm_server_20261012/smol_correctness.jsonl)
  and [reconstruction](../../bench/results/vllm_server_20261012/smol_correctness_analysis.stdout.txt).
- [Environment and exact version commands](../../bench/results/vllm_server_20261012/environment.json).

## Build and reproduce

Use a separate temporary Python environment; retain the existing base runtime.
The measured installation uses the official pinned wheels:

```sh
python3 -m venv /tmp/bpfusion-vllm-env
/tmp/bpfusion-vllm-env/bin/python -m pip install 'vllm==0.31.0' 'torch==2.13.0+cu129' 'transformers==5.17.0' --extra-index-url https://download.pytorch.org/whl/cu129
export PATH=/tmp/bpfusion-vllm-env/bin:$PATH
export VLLM_ENABLE_V1_MULTIPROCESSING=0
make VLLM_PYTHON=/tmp/bpfusion-vllm-env/bin/python vllm-graph vllm-graph-user-network-wait vllm-graph-trace
# Build the existing probes/tools/module against the actual running kernel.
python3 bench/vllm_serving.py --model Qwen/Qwen2.5-0.5B-Instruct --correctness --output /tmp/qwen-correctness.jsonl
python3 bench/vllm_serving_analysis.py /tmp/qwen-correctness.jsonl
```

Replace the model with HuggingFaceTB/SmolLM2-135M for the second qualified
architecture. Use fresh output filenames; do not overwrite archived evidence.
The diagnostic drivers own their attach/module/pin lifecycle. The untraced
vllm_graph and vllm_graph_user_network_wait variants build, but untraced service
correctness/timing is not yet established by these traced runs.

## Matched performance status

The integrated matrix is in progress: five alternating process pairs/model,
four gen1/64 × clients1/8 cells with64 measured requests and8 excluded checked
warmups/executor. Both paths use identical optimized computation, allocation,
GPU batching policy and BF_TRACE instrumentation. This is a matched component
comparison against efficient native networking, not official-vLLM-server or
external-SOTA superiority. No performance conclusion follows from this
correctness prefix. The full goal remains active until the matrix, fresh
result review, honest publication and restoration are verified.
