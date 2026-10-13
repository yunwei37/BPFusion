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
python3 -m venv --without-pip /tmp/bpfusion-vllm-env
python3 -m pip --python /tmp/bpfusion-vllm-env/bin/python install 'vllm==0.31.0' 'torch==2.13.0+cu129' 'transformers==5.17.0' --extra-index-url https://download.pytorch.org/whl/cu129
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

## Completed matched performance comparison

Both checkpoints complete all five alternating process pairs and four
gen1/64 × clients1/8 cells per mode:80 cells,5120 measured requests and166400
measured tokens. Another160 checked gen1 warmups are excluded from metrics.
All20 executor waits and both complete replay analyses exit0. No failed,
excluded or retried full-run row occurs. Individual graph/batch trajectories
and output references are retained for every process.

| Model | Primary condition | Kernel | Native timed userspace | Difference favoring kernel | Nominal paired t95, df4 |
|---|---|---:|---:|---:|---|
| SmolLM2-135M | gen1/c1 mean TTFT, ms |1.201405|1.222876|+0.021471|[-0.044829,0.087771]|
| Qwen2.5-0.5B | gen1/c1 mean TTFT, ms |1.473674|1.432418|-0.041256|[-0.093513,0.011001]|
| SmolLM2-135M | gen64/c8 output tokens/s |5358.410349|5363.427331|-5.016982|[-391.065270,381.031306]|
| Qwen2.5-0.5B | gen64/c8 output tokens/s |4576.218124|4630.119229|-53.901104|[-208.235786,100.433577]|

Latency difference is user-minus-kernel; throughput is kernel-minus-user.
All primary intervals contain zero: reliable superiority and equivalence
remain unproven. Qwen pair0's -275.985358TPS and the large opposing Smol pair1/2
differences remain in the estimates, without selective exclusion or invented
cause. These are separate nominal intervals, with no familywide superiority
test or isolated-GPU assumption. Secondary conditions and finite-request
nearest-rank p50/p99, TPOT and completion are retained in the replay output.

Both paths reuse identical graph arithmetic, checkpoint/precision, reserved
KV allocation and GPU batching policy. The actual arrival/batch trajectories
differ. All single-client matched sequences agree320/320 per model/condition.
At c8, Qwen cross-mode agreement is312/320 forgen1 and278/320 forgen64;
Smol is320/320 forgen1 and290/320 forgen64. Every actual sequence separately
matches its independently advanced host replay. These optimized FP16 trajectory
differences preclude an identical-output superiority claim. Fixed token-ID
lengths and wire encoding remain matched. Anonymous versus kernel-backed
pages, polling, connection handling and trajectory effects prevent attributing
any difference solely to eBPF instructions or saved syscalls.

The absolute results demonstrate a working optimized worker-free backend
with real tensor batching. They do not establish an eBPF speedup or a causal
speedup over the older HF/cross-node/profiling conditions. This new comparison
is loopback and identically BF_TRACE-instrumented; it measures neither physical
delivery nor uninstrumented production timing. No total CPU/energy, text API,
arbitrary model, shared-prefix cache or external-serving superiority follows.

- [Qwen full raw](../../bench/results/vllm_server_20261012/qwen_performance.jsonl),
  [wait status](../../bench/results/vllm_server_20261012/qwen_performance_status.json)
  and [complete reconstruction](../../bench/results/vllm_server_20261012/qwen_performance_analysis.stdout.txt).
- [Smol full raw](../../bench/results/vllm_server_20261012/smol_performance.jsonl),
  [wait status](../../bench/results/vllm_server_20261012/smol_performance_status.json)
  and [complete reconstruction](../../bench/results/vllm_server_20261012/smol_performance_analysis.stdout.txt).
- [Cross-mode sequence agreement](../../bench/results/vllm_server_20261012/cross_mode_output_agreement.json)
  and [bounded host journal](../../bench/results/vllm_server_20261012/host_journal.json).

Reproduce a complete model matrix with
`python3 bench/vllm_serving.py --model MODEL --output /tmp/new-performance.jsonl`.
Replay either archived raw with
`python3 bench/vllm_serving_analysis.py bench/results/vllm_server_20261012/qwen_performance.jsonl`
(and the analogous Smol filename). Replay requires only standard Python.
Each raw snapshot embeds source/config/actual invocations; integration
publication during collection and removal of unused Python locals change
no computation behavior or measurement definition.

The ten performance kernel TX lifecycles each retain54160 bytes,
264 completed,0 abandoned/retries and19 accepted/closed. Strict correctness
has621 completed plus the one deliberate invalid binary EOF abandonment per
kernel executor; these are not missing valid replies. All terminal kernel
maps have reserved0/eight FREE slots. Successful bounded journal read
20:20:00–21:20:45UTC has no listed fault matches, but does not establish
continuous isolation. No changes to the original base runtime or host settings.
[Final owner restoration](../../bench/results/vllm_server_20261012/restoration.json)
records absent owner processes/module/pins/GPU applications, unchanged original
Torch2.14.1+cu130/Transformers5.19.0, removal of the owned temporary environment
and runtime-linked build artifacts. Existing Workspace/PVC/model caches and
unrelated tools/setup_env.sh remain. The [live Workspace read](../../bench/results/vllm_server_20261012/workspace_final.txt)
confirms the original UID Running/Ready with zero restarts.
[Installed package versions](../../bench/results/vllm_server_20261012/installed_packages.json)
remain as provenance. Two cleanup observation commands used unavailable pip
and an incorrect Python path; neither removed state. Installed distribution
metadata and the actual base interpreter supplied the successful observations.
[Fresh combined result review](../../bench/results/vllm_server_result_review_20261012.md)
independently reconstructs every model/cell/metric and trajectory, admits the
run as valid/complete supporting evidence and finds no blocker within the
declared instrumented scope. It does not declare the whole goal achieved.
Close this matrix with its inconclusive transport-performance outcome; do not
repeat unchanged conditions to obtain a favorable estimate. Keep the optimized
adapter and select a causal discriminator for broader default service/network
and CPU-cost acceptance, with the full retained goal still active.
