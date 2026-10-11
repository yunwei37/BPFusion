# Reusing upstream megakernel backends

BPFusion's research direction is to reuse upstream model computation and
measure the Linux TCP/HTTP + eBPF/kernel-to-GPU serving path. Model-specific
operator tuning is not evidence of an eBPF benefit. A useful comparison keeps
the backend revision, checkpoint, precision, KV layout and batching behavior
the same while changing the request/control path.

This is a source audit and candidate comparison, not a GPU qualification or
performance result. Observation: 2026-10-11T00:48:05.450904+00:00. Sources were inspected from the
original bpfusion-dev Workspace; the existing executor and unrelated WIP were
preserved.

## Candidate landscape

| Candidate | Reusable scope | Relevant limitation / current evidence |
|---|---|---|
| [Mirage / MPK](https://github.com/mirage-project/mirage) | Tensor-program compiler, device task scheduler, online request/completion rings; several model builders | Existing CPU ring producer/drainer remains part of upstream serving. RTX 5090 qualification is outstanding. Registered model names are not independent correctness evidence. |
| [model-as-a-kernel](https://huggingface.co/kernels/phanerozoic/model-as-a-kernel) | Architecture interpreter; a finite prompt-plus-greedy-generation loop within one launch; single and batched decode interfaces | CUDA capability 12.0 is declared and the card reports an SM120 measurement. No BPFusion queue, online admission, kernel TX or request recycling is implemented. See source boundaries below. |
| [Luminal](https://github.com/luminal-ai/luminal), [compiler design](https://blog.luminal.com/p/compiling-models-to-megakernels) | General inference compiler and symbolic megakernel work queue | Public backend coverage and host generation/control dependencies need an interface audit. General compiler expressiveness does not prove every model has a runnable whole-model megakernel. |
| [AutoMegaKernel](https://github.com/RightNow-AI/AutoMegaKernel) | HF Llama-family import and whole-forward synthesis, with RTX 5090 evidence | Current generate.py loops on the CPU, lowers/runs each step, synchronizes and reads argmax. Its reported INT8-versus-BF16 gains change precision; they cannot establish our path benefit. |
| [AlpinDale qwen_megakernel](https://github.com/AlpinDale/qwen_megakernel) | Existing BF16 Qwen3-0.6B kernel targeting RTX 5090 | Narrow model/hardware coverage. Useful for assessing a small adapter; not automatic multi-model support. |
| [Lucebox megakernel](https://github.com/Luce-Org/lucebox/tree/main/optimizations/megakernel) | Qwen3.5-0.8B hybrid DeltaNet/Attention implementation; separate Blackwell NVFP4 path | Current kernel is model-specific and batch 1. Half-precision and NVFP4 paths are different compute conditions. The standalone Python decoder drives steps and reads each output on the host. |
| [HazyResearch Megakernels](https://github.com/HazyResearch/Megakernels) | ThunderKittens-based Llama whole-forward implementation | Published build choices are H100/B200; a 5090 port is not verified. |
| [Cohere megakernel](https://github.com/cohere-ai/cohere-megakernel), [serving design](https://cohere.com/blog/megakernels) | Complete serving features around a decode megakernel, including paged KV and continuous batching | Current research release targets North Mini Code on one H100. Python controls admission/prefill; a C++ loop updates positions, launches, samples and streams each decode step. |
| [TileRT](https://github.com/tile-ai/TileRT) | Tile runtime and model backends for large multi-GPU serving | Current supported wheels target 8 B200s or 8 MI350-class GPUs, with exact PyTorch ABI requirements; core backend is distributed as a binary. Not a demonstrated single-5090 source adapter. |
| [ARK](https://github.com/microsoft/ark) | GPU-driven computation/communication loop-kernel framework and Llama2 example | A relevant execution-model precedent; current model breadth and 5090 compatibility still need verification. |

[Event Tensor](https://arxiv.org/abs/2604.13327),
[Ada-MK](https://arxiv.org/abs/2605.11581), and
[ForgeMegakernel](https://arxiv.org/abs/2609.12379) are additional relevant
compiler/synthesis papers. This audit did not establish a complete, directly
usable public artifact for these candidates.
[FlashInfer MegaMoE](https://flashinfer.ai/2026/09/22/mega-moe.html) is a
MoE-layer compute/communication implementation rather than a complete
resident model-serving backend.

## Pinned source findings

### model-as-a-kernel

Audited Hub v1 revision:
[5858c6ddbe04c6b749e81daeb47bcd1857c1e618](https://huggingface.co/kernels/phanerozoic/model-as-a-kernel/tree/5858c6ddbe04c6b749e81daeb47bcd1857c1e618).
The CUDA source, Python model importer, bindings and existing tests were read
without modifying them or running a model.

- The Python generate() implementation at lines 929-961 calls mak_run_seq()
  once for prompt consumption plus generation. Its alternative uses the same
  program with individual launches. The CUDA mega_kernel() at lines 1483-1556
  has a finite position loop and returns when that generation completes.
  This removes inter-token host launches for that call; it does not implement
  a service resident across requests.
- The interpreter consumes an int64 [n_phases, 16] program containing device
  pointers and dimensions. MegaModel owns the weights and buffers. Those
  lifetimes must remain valid through inference and final output ownership.
- from_pretrained() at lines 591-592 rejects attention projection biases.
  BPFusion's current Qwen2.5 loader explicitly loads those biases. A direct
  swap of the existing checkpoint into this importer is therefore unsupported;
  changing the model requires its own independent reference.
- build.toml declares CUDA capabilities through 12.0. Grid sizing queries
  occupancy; the CUDA implementation uses a software global barrier between
  phases. BPFusion's existing eight independent graph banks must not simply
  be assumed safe or equivalent for this full-grid kernel. Concurrent launch
  residency and the alternative tensor-batched path need qualification.
- generate_batch() performs per-sequence prefill, reads first tokens on the
  host and then launches a batched decode. Its existence is not proof of
  GPU-only online batching or request admission.
- Output tokens are written into device buffers. The existing Python API
  transfers the result back to the host. It does not publish BPFusion's
  system-scope produced/DONE fields or implement TCP streaming/reclamation.
- In tests/test_mak.py, test_additional_model_coverage() for Qwen3/TinyLlama
  permits at least 85% argmax agreement across 48 fixed-history positions
  (lines 250-292), alongside logit/KV tolerance checks. Mode equivalence is
  checked separately. These tests do not establish token-exact HF greedy
  generation for those models. test_generate_closed_loop_and_speed() compares
  the backend's own launch modes; its eager speed threshold is not an eBPF
  comparison.

The current card is narrower than parts of the source: the importer includes
additional architecture/RoPE handling. Source presence alone is not measured
support, so that extra breadth is not promoted to a BPFusion coverage claim.

### Mirage / MPK

Audited upstream revision:
[f9eb70c254acefc9f3667b2a973d0dcf25471fce](https://github.com/mirage-project/mirage/tree/f9eb70c254acefc9f3667b2a973d0dcf25471fce).

- python/mirage/mpk/online_pinned_runtime.py exposes request/completion rings,
  ready flags, slot token inboxes and row ownership/release acknowledgement.
  Its submit(), completion-drain thread and output handling remain CPU work.
  These existing interfaces make it a promising transport/ownership adapter
  candidate, not an already CPU-free network service.
- python/mirage/utils.py's shared-memory capacity helper has branches through
  compute capability 100 and rejects other values. CMakeLists.txt line 28 lists
  native architectures 75/80/86/89/90. This identifies compatibility questions,
  not proof that every 5090 execution path fails: the call path and generated
  tasks must be checked before deciding how to build or adapt it.
- The Qwen3 builder registers several names, including a Qwen3.5 alias.
  A registry entry alone does not establish correctness for a different
  hybrid architecture.
- A native build and bounded SM120 Qwen3-0.6B qualification now exist.
  The temporary compatibility patch repairs attention metadata, shared-memory
  capacity and LM-head synchronization. Independent LM-head probes pass,
  but the complete model fails all12 reference prefixes under both parallel
  and serial submission, from the first output token. MPK is not a qualified
  model backend or kernel-queue integration. The [qualification finding](findings/0023-batch-execution-qualification.md#upstream-mpk-sm120-compatibility-and-terminal-numerical-rejection)
  links the exact patch, commands and complete positive/negative raw receipts.

## Selection and comparison implications

MPK is the strongest lead for an existing online queue/runtime interface.
model-as-a-kernel is a concrete source-level lead for reusing a finite whole
generation with minimal compute changes. Luminal remains a compiler candidate
whose current public runtime needs deeper inspection. The native 5090 Qwen
implementation is a useful narrower implementation reference.

These are investigation priorities, not a final backend selection. Qualify
checkpoint semantics and the actual launch/control interface before comparing
speed. Reuse upstream arithmetic and credit its compute performance. Necessary
adapters concern request publication, GPU control, streaming output and
lifetime/reclamation; model-specific arithmetic improvements are a separate
claim.

For the causal path comparison, keep model/backend, precision, KV and
batching equal. A credible userspace alternative can submit an entire GPU
generation per request; forcing it to execute a slow Python token loop would
confound the effect. Existing serial host-control results do not isolate the
current concurrent graph path. Measure client TTFT/TPOT/completion and host
cost with explicit attribution and report shared-GPU conditions.

## Closest serving claim

[Blink](https://arxiv.org/abs/2604.07609) already removes the steady host CPU
from serving by combining a SmartNIC/RDMA request path with GPU-resident
scheduling, batching and KV management. "First CPU-free LLM serving" is not a
defensible BPFusion novelty claim from the current evidence.

BPFusion's candidate distinction is ordinary Linux TCP/HTTP plus
eBPF/sockmap and a kernel/GPU shared queue, with the existing Linux networking
and asynchronous kernel TX semantics. Kernel networking, eBPF and kernel TX
still use CPU. Removing the userspace request worker is not removing all host
CPU work; total cost and useful latency/throughput gains remain to be measured.
