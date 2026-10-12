# Official vLLM graph reuse plan review

Reviewed 2026-10-12 UTC in original yunwei356/bpfusion-dev Workspace.
Observed main a40fd5b8650e7ce053b8739f6cb9936334cb4143. Reviewed
vllm_reuse_plan_20261012.md, finding0031, and the downloaded pinned source
under /tmp/bpfusion-vllm-reuse-j3k3go83/source: GPU graph manager/model runner,
graph wrapper, input structures, in-process executor/engine and PyTorch
CUDAGraph implementation. The named cached checkpoint directory exists with
config and model.safetensors. No GPU model run, build, install mutation,
production edit or publication was performed by this reviewer.

## Verdict and decision value

Admit preparation and the declared actual-model preflight. No scientific
defect blocks this integration-dependency probe. Native executable apparatus
does not yet exist in the inspected temp directory, so actual ABI/build/launch
executability is unproven and is correctly the preflight's job.

Finding0031 establishes a consequential implementation boundary: an optimized
official backend substantially exceeds current private batch1 graph throughput
at eight clients. Determining whether its real model graphs support device
launch selects the next integration route. An actual launch incompatibility,
numerical discrepancy, or successful qualified bridge changes that route.
Another unchanged serving matrix or another rejected eager-HF batching probe
would not answer this interface uncertainty.

The role is dependency. Success is not a new paper result, an eBPF speedup, a
general-model guarantee, or proof of worker-free TCP serving. The plan preserves
those missing requirements instead of redefining the retained objective around
the convenient computation-only probe.

## Source-native seam and control fairness

The pinned CudaGraphManager captures final FULL graphs into graphs[desc].
Its run_fullgraph first syncs outstanding offloader work and then invokes the
ordinary graph replay. ModelCudaGraphManager returns persistent hidden-state
buffers populated inside the captured graph. GPUModelRunner stages inputs and
attention/cache metadata before that call and performs sampling afterwards.
This is a real graph interface, rather than an authored replacement model.

The installed-source PyTorch keep_graph option retains raw_cuda_graph and
defers ordinary executable instantiation to explicit instantiate or first
replay. Thus the proposed test-local constructor change can preserve the raw
definition without changing the ordinary public replay computation.
VLLM_ENABLE_V1_MULTIPROCESSING=0 is an explicit, necessary same-process ownership
condition. Source inspection confirms the in-process worker/engine route.
Neither modification establishes that production worker control has been
removed; the plan says this clearly.

The same checkpoint, FP16, official compiled model/attention, actual captured
graph, inputs and batch shape are shared by host and device control. The
reference matrix is generated independently before installing the probe hook.
Its outputs cannot be replaced by device outputs during qualification.
Old eager-HF oracle failures remain separate, preventing backend-specific
control agreement from being mislabeled old-backend numerical qualification
or task quality.

## Correctness and engagement

Nineteen groups / 74 lanes / 4736 output tokens per phase reconstruct from
the declared batch1/2/4/8 homogeneous groups plus three mixed groups.
Greedy 64-token generation with ignore_eos and exact token-ID prompts prevents
a favorable truncation or a changed input protocol. All failures and complete
outputs must remain archived.

Each official host FULL replay followed by an actual native device replay is
a useful same-state control. Save and finish the host result before device
launch; compare actual device-written hidden states exactly, including their
shape/dtype, without a newly introduced tolerance. Restore the saved result
only after that comparison, before upstream sampling.

Frozen full-sequence agreement has a distinct role: it can reveal later
state contamination or changes in the official path. Because host outputs
are restored before sampling, sequence agreement alone cannot prove successful
device execution. A valid successful seam qualification therefore needs actual
nonzero FULL hooks/device launches, successful statuses and hidden-state
comparisons for every batch shape claimed qualified. Record the actual padded
descriptor and logical lane count; do not infer graph coverage from requested
batch size alone. Zero-FULL or uninstrumented groups are untested, not passes.
This is engagement of the declared mechanism, not an added baseline or wider
workload requirement.

Qwen's KV slot/position writes are expected to target the same positions during
the duplicate replay, but must not be assumed universally idempotent.
Document actual cache/metadata mutations and any non-idempotent state;
preserved host output does not restore KV or other state. Full-sequence
agreement is useful evidence for the tested finite Qwen trajectories, not
proof for recurrent/SSM/MoE or arbitrary other backends.

## Graph eligibility, ownership and ABI

The official manager has a throwaway profiling capture phase before final
KV allocation. Its own comments explicitly warn that those profiling graphs
embed obsolete pointers and cannot be reused. The hook must operate on the
actual final serving manager and its live descriptor graph, with the final
model/KV/input/output owners retained until native handles are destroyed.

The plan records prefill/PIECEWISE as untested, rather than bypassing unsupported
activities and declaring a complete worker-free backend. Retain all runtime
descriptor and node-type receipts, including nested graph nodes when present.
An unsupported node is the interface result; replacing attention, model math,
or activity coverage to produce success would invalidate this probe.

NVIDIA's device graph API requires explicit device-launch instantiation and
upload. It also prohibits overlapping host/device launches of the same
executable. The plan follows those requirements and keeps device status.
Host replay, hidden-state clones, uploads and device replay need explicit
completion ordering on their actual streams, not presumed legacy-default
stream ordering. Synchronizing the launching parent stream/environment must
complete its fire-and-forget child before hidden states are read/restored
or the next native launch starts.

The official Torch process uses CUDA12.9, while fleet tooling includes another
CUDA version. Actual loaded runtime, compiler, link targets, context and
status must be retained. Using the already loaded runtime is sensible but
does not itself prove handle/function registration compatibility; a failed
instantiation/build is an honest preflight result. No driver/package change,
new server or new context-sharing service is required.

Primary device-launch constraints were checked against the official
[CUDA Graphs documentation](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html#device-graph-requirements).

## Execution and lifecycle

The plan names its owned temp environment, pinned package condition, cached
checkpoint, complete workload, raw paths and real preflight. Once the minimal
qualifier exists, archive its runnable command and source before collecting
results; no generic control schema or broader orchestration layer is needed.
Installed-source/kernel compatibility remains a genuine test, not something
the plan review can certify from prose.

The offline in-process route needs no BPF/module/network attachment or another
Workspace/Job/service. Parent retains ownership of the existing installation
process. Handle destruction must precede model/cache owners and environment
removal; all failed partial rows and deviations remain evidence. Preserve the
original environment/cache, production main and unrelated tools/setup_env.sh.
Successful cleanup and the promised fresh terminal result review remain part
of completion.

No additional competitor, more models, task-quality benchmark, tuning campaign
or latency measurement is a prerequisite for this narrow interface question.
After success, GPU-owned input/metadata updates, generation/sampling, admission
and lifecycle plus same-backend kernel/eBPF versus efficient userspace serving
are still open work.

## Focused follow-up: output poisoning and claim boundary

Reviewed the updated same plan before GPU execution. The update explicitly
identifies 4736 tokens/phase as outputs of the official CPU-controlled
generation loop; direct device evidence is FULL-body hidden-state replay.
This removes an ambiguity without expanding the experiment or changing its
oracle.

The declared NaN poisoning addresses a real potential false positive: after
the host replay, a no-op native replay could otherwise leave an already
correct output buffer. The pinned store_capture_output implementation
allocates persistent hidden_states using torch.empty_like and copies the
model forward result into it. For this Qwen, single-last-rank seam, poisoning
that dedicated output after cloning/synchronizing the host result does not
alter the input IDs, attention metadata or KV intended to be replayed.
After native completion, every compared element must be finite and exactly
match the saved host result; no poisoned element may remain. Restoring the
saved host result occurs only after this check and native completion.

This is aligned necessary instrumentation, not model arithmetic tuning.
There is no new scientific or executability blocker. The existing ordering,
actual nonzero device engagement, descriptor coverage, live-owner and
state-contamination checks remain necessary. Verify that the poisoned
range is exactly the persistent output range read by the instrumented FULL
call, and retain its pointer/shape/dtype and overwrite/comparison counts.
The source allocation supports separation; the actual receipt should not
infer general alias safety for other model families.

Terminology clarification: finite elementwise exact comparison, such as
torch.equal, is not in itself a storage-bit comparison for signed zero.
Describe the implemented check accurately; claim bit-identical only if the
corresponding dtype-bit representations were actually compared. This does
not call for tolerance, a different oracle or another workload.
