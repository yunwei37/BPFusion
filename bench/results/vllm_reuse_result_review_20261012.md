# Independent terminal result review: official vLLM FULL graph reuse

Observation: 2026-10-12T20:01:26.200421+00:00. Reviewer is independent of this candidate's plan review and implementation. Reviewed the existing original Workspace only; no GPU execution, build, source/plan edit or Git action was performed.

## Verdict and next decision

- Run status: **valid / complete for the declared FULL-body mirror qualification**, with recorded setup deviations.
- Tested hypothesis: **supported for sequential device launch of the four tested final FULL decode graphs and preservation of their active FP16 hidden-state outputs**.
- Research value: **dependency-only**. This is not an independent paper-performance or novelty result.
- Paper impact: **optimized-backend integration boundary**; no formal RQ or direct thesis conclusion.
- Next decision: this seam qualifies continued GPU-owned input/attention-metadata, sampling/generation and admission/lifecycle integration, followed by a genuinely same-backend serving comparison. Do not claim that CPU scheduling/sampling or TCP serving has already moved to GPU/kernel.
- Invalidating defects: none found for this narrow qualification. Broader backend, concurrency, ABI and state guarantees remain untested.

Finding0030 localized the existing short-input model span; finding0031 established a consequential optimized-serving throughput boundary. Neither is reused as a performance result for this new probe.

## Reviewed artifacts and completion

Read the [current plan](vllm_reuse_plan_20261012.md), [plan review](vllm_reuse_plan_review_20261012.md), [actual qualifier](vllm_reuse_qualify_20261012.py), [bridge](vllm_reuse_bridge_20261012.cu), all archived vllm_reuse raw/source/build/status artifacts, and actual retained apparatus under /tmp/bpfusion-vllm-reuse-j3k3go83. All five attempts' JSONL, stdout and status archives are byte-identical to their temporary originals. Final qualifier/bridge archives and metadata source texts equal the actual final files.

The successful [preflight](vllm_reuse_preflight_20261012.jsonl) has74 rows, one group/lane,64 official CPU-loop tokens per phase and63 actual device calls. The [full raw](vllm_reuse_full_20261012.jsonl) has1253 rows:
metadata1, owners1, reference19, references_frozen1, runtime_maps1, catalog4, instantiate4, device_call1197, instrumented19, complete1, destroy4, terminal1. No full failure row occurs. Internal terminal and external [full status](vllm_reuse_full-status_20261012.json) both record exit0. Preflight internal/external statuses also agree at0.

Independent CPU reconstruction confirms all19 declared groups: batch1/2/4/8 with four homogeneous prompt groups each, plus cycling mixed groups for2/4/8. They cover74 lanes and4736 output tokens **per phase**,9472 returned token IDs across reference and instrumented phases. Each returned sequence contains64 vocabulary-valid IDs. All19 instrumented groups and74 complete sequences exactly equal the independently frozen source-native references.

The4736-token count is an output of official CPU-controlled scheduling and sampling. It is not a count of autonomously GPU-generated tokens. Direct evidence covers1197 FULL-body replay calls,4662 active decode lane-vectors and4177152 active FP16 elements. Every group has63 FULL hooks; its initial generation token/prefill path lies outside this direct seam.

## Actual shape and mechanism coverage

Runtime descriptors, rather than requested batch labels alone, establish coverage:

| Actual FULL descriptor num_tokens/num_reqs | Groups | Direct calls | Elements/call | Captured kernel nodes | Captured memcpy nodes |
|---|---:|---:|---:|---:|---:|
| 1/1 | 4 | 252 | 896 | 265 | 25 |
| 2/2 | 5 | 315 | 1792 | 337 | 1 |
| 4/4 | 5 | 315 | 3584 | 337 | 1 |
| 8/8 | 5 | 315 | 7168 | 337 | 1 |

All descriptors are FULL, uniform_token_count1, num_active_loras0, num_ubatches1. Every call's recorded shape matches its group's logical lane count; there is no additional padded shape inferred qualified. Four distinct raw graph handles are catalogued. Every catalog code is0 and all other32-entry node counters are0, including no nested graph nodes. Counts describe graph definitions, not an independent CUPTI count of executed activities.

The final ModelCudaGraphManager contains35 serving graphs; only these four are instantiated by the bridge. The hook takes manager.graphs[desc] from the live runner after complete official engine initialization and a complete reference matrix. It does not borrow a throwaway memory-profiling graph. Official logs confirm final FULL/PIECEWISE capture and compiled FlashAttention model operation. Prefill/PIECEWISE, larger graph sizes, LoRA, pipeline/multi-GPU and other models are not qualified by this seam. No unsupported node was removed or model activity substituted to produce the four successes.

Each native child is instantiated with DeviceLaunch, uploaded and synchronized. A one-thread host-launched parent graph calls device cudaGraphLaunch(child,FireAndForget). Every call has host code0, run stage5, entered1, device_status0. The status buffer is reset to -1 before each launch, so its entry/success receipt cannot be stale.

## Independent control, poison and storage-bit check

References are generated by the official source-native LLM path **before** the instrumented hook is installed. All19 reference records precede references_frozen, and no reference is generated after it. Checkpoint7ae557604adf67be50417f59c2c2f167def9a775, FP16, exact four prompt ID arrays, greedy temperature0, max_tokens64, ignore_eos and detokenize=False are fixed. The new same-backend contract was declared in the plan; it is not a replacement oracle selected after this probe failed.

Each instrumented call first runs the official host graph, clones its actual hidden-state output and performs device-wide synchronization. It requires that saved host result be finite, fills the actual returned persistent output view with NaNs, synchronizes again and verifies every element is poisoned. Only then does the native replay run.

After native completion the qualifier requires all active elements finite and compares output.view(torch.int16) against host.view(torch.int16). This is a FP16 storage-bit comparison, including signed-zero differences, rather than merely numeric torch.equal. It also records numeric equality and max_abs0. All1197 calls have poisoned/finite/bits_equal/numeric_equal true. Host output is restored and synchronized **after** the comparison and **before** official sampling.

The pinned store_capture_output allocates persistent hidden_states with torch.empty_like, copies model output into it, and run_fullgraph returns its active prefix. All four catalogs report the same persistent output base address, distinct from input_ids; source inspection establishes the output allocation separate from input/KV owners. The poisoned range is exactly the returned active prefix, not untested inactive tail storage. Finite host completion, synchronized poisoning and native overwrite exclude a no-op replay passing on the old host output.

Full hidden-state bytes are not archived. This review independently validates the comparison implementation and all per-call receipts/elements/statuses; it cannot recompute their bit comparison offline from stored tensor bytes. Complete output token arrays are archived and independently recomputed. This evidence limit is not a detected execution or numerical defect.

The unchanged eager-HF reference is kept separate. It matches36/74 complete source-native sequences in each phase:1/4 at batch1,5/10 at batch2,10/20 at batch4,20/40 at batch8. All source-native versus instrumented outputs match74/74. This is not old-backend eager-HF numerical qualification or a task-quality conclusion.

## State, ordering and owner lifetime

Official ModelCudaGraphManager.run_fullgraph first synchronizes offloader work before host replay. Explicit global synchronization finishes host output/clone, poisoning, native completion and restoration. The bridge synchronizes its parent stream before reading device status. CUDA's execution-environment semantics include generated fire-and-forget child work before completion of the host stream launch; host and device executables do not overlap here. [NVIDIA CUDA Graphs](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html#device-graph-requirements).

Duplicate Qwen attention replay writes K/V to the same source-native slot_mapping positions with unchanged input IDs, positions, block tables and attention metadata. Those fixed-position scatter writes are not a demonstrated general recurrent-state transition. Host-output restoration does not restore KV. Matching later complete trajectories is evidence against observed contamination in these finite tested Qwen cases, not proof of all KV/state bytes being unchanged or idempotence for SSM/MoE/other models. The probe does not archive all intermediate cache bytes or independently implement GPU metadata updates.

LLM, runner, manager, model/cache/input/output buffers and graph references remain live while native child handles exist. The bridge holds graph owners, restores the original manager method, and destroys all four handles after the final comparisons, each with code0. Destruction releases parent executable, parent graph, child executable and status buffer, while original graph owners remain alive. The default-stream null handle skips bf_destroy's conditional stream sync, but all successful calls and final restore already synchronized; no outstanding launch is observed at destruction. This is not a general failure-recovery or concurrent-handle guarantee.

Both successful external process statuses are0. No explicit LLM.shutdown receipt is recorded; process exit supplies engine/context lifetime termination after explicit native destruction. Current owned qualifier processes are absent, GPU compute-apps are empty, RTX5090 reports15MiB, and no bfusion module/bpfusion pins exist. Endpoint observations do not establish continuous isolation. Temporary environment/source/build apparatus intentionally remains for this review and needs owner removal after complete archiving; teardown of the apparatus is not yet claimed complete.

## Setup failures and authorized additional repair

All three failed setup attempts remain raw and external exit1, with **zero device_call rows**:

1. [initial](vllm_reuse_preflight_initial_20261012.jsonl): bridge load fails on unresolved device-link registration symbol after the official64-token reference.
2. [keep_initial](vllm_reuse_preflight_keep_initial_20261012.jsonl): inherited CUDAGraph initializer resets keep_graph; raw graph access fails before catalog/device replay. Adding the explicit super initializer(True) fixes ownership construction.
3. [default_stream](vllm_reuse_preflight_default_stream_20261012.jsonl): actual batch1 FULL graph is catalogued and child instantiated/uploaded, but parent default-stream capture fails at stage5/code900. No model device replay completes. Explicit parent cudaGraphCreate/cudaGraphAddKernelNode repairs only that wrapper.

The successful fourth preflight replaces parent stream capture by explicit graph construction. It preserves model graph, source-native reference, inputs, workload and equality checks. Earlier build-level failures also remain: nvcc rejects the runtime-library path in the initial command; missing device linking yields unresolved registration; --cudart=none conflicts with -dlink. The final three-stage build has each exit0 and bridge LOAD_OK.

This exceeds the skill's default three-preflight-attempt limit. It is explicitly recorded in the same current plan and continued under the operator's no-added-stop-condition/continue-implementation direction, which takes precedence over skill guidance. It is not concealed as another experiment or treated as a numerical retry. No criterion or oracle was weakened.

## Source and ABI boundary

Seven retained vLLM source files independently match both installed package bytes and pinned official revisiondb9527a46873454610df6dbedf79a36d6bf1a7f6; retained torch CUDA graph source matches the installed Torch file. No model/kernel source is authored or changed. Actual owners are official LLMEngine, UniProcExecutor, GPUModelRunner, ModelCudaGraphManager and Qwen2ForCausalLM.

The declared test-local changes are in-process VLLM_ENABLE_V1_MULTIPROCESSING=0 and preserving raw definitions via keep_graph=True. They apply equally to official reference and instrumented phases and do not establish removal of official CPU scheduling. Package installation is restricted to the owned temporary venv, with [setup/install](vllm_reuse_setup-command_20261012.txt), [versions](vllm_reuse_versions_20261012.txt) and clean [pip check](vllm_reuse_pip-check_20261012.txt).

Actual build uses NVCC13.0.88/sm120 and separate relocatable device compilation/linking. The final bridge has NEEDED libcudart.so.12 and its owned CUDA-runtime12 RUNPATH; ctypes loads it with RTLD_LOCAL|RTLD_DEEPBIND. The process maps also contain toolkit libcudart13.0.96 and torchvision's bundled libcudart12, in addition to the Torch/vLLM venv runtime12.9. Therefore this is an **empirically successful mixed-toolkit/runtime artifact**, not proof of interchangeable CUDA12/13 ABIs or portability across other builds, drivers and contexts. Archive [actual build command](vllm_reuse_build-command_20261012.json), [build output](vllm_reuse_build_20261012.stdout.txt), dry run, versions and all statuses for reconstruction.

Full collection metadata records productiona40fd5b8650e7ce053b8739f6cb9936334cb4143. This reviewer changes only this report; original Workspace/cache/production and unrelated WIP are preserved.

## Remaining full-goal requirements

This succeeds at a real optimized-model FULL-body launch seam. It does not generate the next input, update scheduler-owned metadata/block allocation, execute sampling autonomously, move prefill/PIECEWISE to device launch, admit Linux TCP requests, publish GPU completion to the BPF shared queue, reclaim request memory or asynchronously transmit replies from kernel. It measures no latency/TPS/totalCPU/energy and establishes no serving superiority.

Continue integration only with these missing components explicit. A future comparison must use the identical qualified backend/checkpoint/precision/batching in both kernel/eBPF and efficient userspace paths. No unchanged serving matrix or unbounded model-arithmetic campaign is justified by this dependency result.
