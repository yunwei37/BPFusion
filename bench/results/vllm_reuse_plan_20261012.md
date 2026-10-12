# Reusing official vLLM full graphs for GPU-controlled execution

The retained objective is Linux TCP/HTTP/eBPF shared-queue inference with no
steady userspace request worker and better throughput/latency. Finding0031
completes the strongest current external comparison: vLLM is much faster at
eight-client long generation, while current BPFusion has lower first-token
time. Current private batch1 graphs are not shared-weight tensor batching.
Repeated rejected HF batching/math probes cannot resolve this backend seam.

This is a dependency within that integration, not a standalone paper result.
No paper RQ/thesis exists and none is invented. The strongest runnable next
discriminator is whether the actual optimized vLLM graphs can be instantiated
and launched by CUDA device code with preserved real-model computation.

## Scope and decision

Official vLLM0.31.0 source revisiondb9527a46873454610df6dbedf79a36d6bf1a7f6.
Reuse its actual model loader, compiler, FlashAttention, paged KV and FULL graph
manager; no model arithmetic, dtype, kernel tuning or attention replacement.
Use cached Qwen2.5-0.5B revision7ae557604adf67be50417f59c2c2f167def9a775,
FP16, exact token-ID cases from finding0031. Preserve productiona40fd5b.

Native graph eligibility is a load-bearing interface question, not a new
network benchmark. A pass enables GPU-owned metadata/generation integration;
unsupported nodes/launch failures select a concrete interface repair or another
backend route. A numerical discrepancy prevents accepting this bridge.
No unchanged serving matrix or single-model math campaign follows.

The current vLLM library normally owns its scheduling on CPU. This probe
does not yet remove that CPU loop or implement TCP admission. It checks the
actual GPU-launch seam before building those adapters; those missing parts
remain explicit requirements of the full objective.

## Source-native control and correctness

For a new backend, compare control correctness against its independent official
host path with the same checkpoint, precision, batch shape, inputs and graph.
First freeze all official64-token greedy sequences before installing the native
probe hook. Then repeat the same complete matrix with GPU-launch probes.
Require identical full output sequences and retain any mismatches; do not use
the probe's own output as the oracle.

This answers same-backend/control correctness, distinct from replacing the old
FP16 eager-HF backend under its previous exact oracle. Retain those old failures.
Report agreement with the unchanged eager-HF sequences separately; their known
difference from optimized vLLM is not hidden or relabeled as model quality.
There is no accuracy-tolerance threshold, EOS truncation or oracle change during
execution. Sampling explicitly greedy,64 tokens,ignore_eos,token-ID input.

Batch1/2/4/8: four homogeneous prompt groups each, plus one cycling mixed group
for batch2/4/8. Nineteen groups,74 lanes,4736 source-native CPU-loop-generated tokens per phase.
The direct device evidence is FULL-body hidden states, not autonomous GPU
generation; this probe does not yet move sampling or scheduling to GPU.
All inputs are the existing four prompts, with full lengths2/5/8.
Repeat complete reference matrix once with the native hook (two phases total).
Each instrumented FULL decode call first executes its official host graph and
clones hidden states, then the native bridge launches the same captured graph
from a GPU kernel. Before device replay, fill the dedicated persistent output
buffer with NaNs and synchronize; source store_capture_output allocates it
separately from model inputs/KV. Require the real device replay to overwrite
all output elements with the finite, bit-identical host result. This prevents
a no-op replay from passing on leftover host output. Compare the actual hidden states and restore the saved host
output before upstream sampling, so the returned oracle is not replaced by
the method's own output. Full frozen-sequence agreement additionally detects
state contamination across future steps. Document graph cache writes at fixed
slot/position and any non-idempotent state. Qwen attention state is tested;
no general recurrent-model claim follows.

Record every runtime descriptor,raw handle,node types,host/model outputs,
device-graph instantiation/upload/launch status and actual FULL hook count.
Prefill/PIECEWISE calls are recorded as untested by this seam, not assumed to
be GPU-eligible. Graph/model/KV/output owners live until native handles are
destroyed; no overlapping host/device launch of one executable.

## Necessary interface apparatus

Use the official in-process LLM path with test-local
VLLM_ENABLE_V1_MULTIPROCESSING=0, since CUDA addresses/graphs cannot be borrowed
across the default engine process context. It changes bootstrap/control location,
not model arithmetic. Keep other default optimized settings. This is not a
production runtime or comparison against a deliberately weakened CPU server.

Preserve raw graph definitions by constructing existing torch.cuda.CUDAGraph
with keep_graph=True before upstream capture. The public replay path still
instantiates/replays them normally. Confirm the installed PyTorch API.
This preserves ownership for a separate device-launch instantiation and is not
a model math change. Record any necessary capture/ABI compatibility deviation.

A minimal native CUDA adapter follows NVIDIA's Device Graph Launch API:
instantiate original graph with DeviceLaunch,upload, launch a one-thread parent
graph that calls cudaGraphLaunch(child,FireAndForget), synchronize parent
environment and retain device status. No model kernels are authored.
Use the runtime loaded by the vLLM Torch process; archive actual compiler/
runtime linkage and status rather than assuming CUDA13 and CUDA12 handles mix.

Primary sources:
https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html#device-graph-requirements
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/v1/worker/gpu/cudagraph_utils.py
https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/envs.py

## Execution and limits

Original bpfusion-dev Workspace/lab RTX5090 only. OS-temp owner apparatus
/tmp/bpfusion-vllm-reuse-j3k3go83, existing cached weights and installed fleet
driver/toolkit. Recreate the already measured package condition under only its
owned temp venv: vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0. Preserve
original Python environment, primary checkout, other owners and tools/setup_env.sh.
No network server, module/BPF attachment, service, Job, scheduler or gateway
entity is needed for this computation qualification.

Preflight: batch1 one full prompt64-token reference plus instrumented phase
with the real official model graph, actual native device launch and metrics/raw.
It proves only executability. Full run follows the complete19-group matrix.
Build/interface defects can be repaired with fixed source-native computation;
do not turn failure into success by altering model math,oracle,workload or
skipping unsupported activities. Preserve all failed/partial rows and deviations.

Actual command will be recorded with the completed qualifier under OS-temp.
Archive sources,versions,actual native commands,complete inputs/outputs,
all status/counters and ordinary stdout/JSONL under bench/results/vllm_reuse_*.
No latency/TPS/totalCPU/energy/worker-free-network claim comes from this probe.
Fresh plan and terminal result review. Close only own process/group/handles;
remove owned temp environment after archiving/review and verify original
Workspace/GPU/module/pins. Performance integration and same-backend serving
comparison remain open after a successful eligibility qualification.

## Setup deviations before native replay

Three recorded attempts reached, respectively, missing device-link registration,
keep_graph initialization reset by the inherited initializer, and unsupported
default-stream capture when constructing the native parent. None completed
a GPU model replay or is counted as a pass. The last attempt successfully
catalogued and instantiated/uploaded the real FULL graph:265 kernel and25
memcpy nodes. Replace only parent stream capture with explicit
cudaGraphCreate/cudaGraphAddKernelNode, as the current production dispatcher
already does. Original model graphs,reference,inputs and checks are unchanged.
Continue this necessary interface repair under the operator's explicit
no-added-stop-condition and continue-implementation direction; record the
additional attempt rather than concealing it under a fresh experiment name.
