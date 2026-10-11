# Reusing upstream megakernel backends

BPFusion's research direction is to reuse upstream model computation and
measure the Linux TCP/HTTP + eBPF/kernel-to-GPU serving path. Model-specific
operator tuning is not evidence of an eBPF benefit. A useful comparison keeps
the backend revision, checkpoint, precision, KV layout and batching behavior
the same while changing the request/control path.

This landscape combines source audit with separately linked local correctness
qualifications. Source presence alone is not GPU or serving qualification;
performance claims require matched measurements. Observation: 2026-10-11T00:48:05.450904+00:00. Sources were inspected from the
original bpfusion-dev Workspace; the existing executor and unrelated WIP were
preserved.

## Candidate landscape

| Candidate | Reusable scope | Relevant limitation / current evidence |
|---|---|---|
| [Mirage / MPK](https://github.com/mirage-project/mirage) | Tensor-program compiler, device task scheduler, online request/completion rings; several model builders | Existing CPU ring producer/drainer remains part of upstream serving. Native SM120 compatibility probes pass after fixes, but complete Qwen3-0.6B outputs fail the unchanged HF oracle under parallel and serial submission. Registered model names are not independent correctness evidence. |
| [Plow](https://github.com/infervisor/plow) | HF importer, packet compiler, Lean ordering checks and SM120 interpreter; existing native Qwen harness | Native/Rust/Lean builds pass after compile/link compatibility fixes and existing GF2 selection. Four32-token memchecks pass, but only two sequences match the unchanged HF oracle. Decode-only prompt ingestion; no qualified prefill or resident network adapter. See [qualification](findings/0023-batch-execution-qualification.md#upstream-plow-sm120-build-and-mixed-numerical-qualification). |
| [model-as-a-kernel](https://huggingface.co/kernels/phanerozoic/model-as-a-kernel) | Architecture interpreter; a finite prompt-plus-greedy-generation loop within one launch; single and batched decode interfaces | CUDA capability 12.0 is declared and the card reports an SM120 measurement. Native SM120 build passes with unchanged computation; seven of ten64-token SmolLM2 sequences match HF exactly. Not a qualified strict replacement, online queue or kernel-TX adapter. See source boundaries and qualification below. |
| [Luminal](https://github.com/luminal-ai/luminal), [compiler design](https://blog.luminal.com/p/compiling-models-to-megakernels) | General inference compiler and symbolic megakernel work queue | Public backend coverage and host generation/control dependencies need an interface audit. General compiler expressiveness does not prove every model has a runnable whole-model megakernel. |
| [AutoMegaKernel](https://github.com/RightNow-AI/AutoMegaKernel) | HF Llama-family import and whole-forward synthesis, with RTX 5090 evidence | Current generate.py loops on the CPU, lowers/runs each step, synchronizes and reads argmax. Its reported INT8-versus-BF16 gains change precision; they cannot establish our path benefit. |
| [AlpinDale qwen_megakernel](https://github.com/AlpinDale/qwen_megakernel) | Existing BF16 Qwen3-0.6B kernel targeting RTX 5090 | Body/final norm and LM-head/argmax use separate kernels. Global mutable launch/synchronization state needs a concurrency audit; the bulk no-sync API is not evidence of resident online admission. See pinned source below. |
| [Lucebox megakernel](https://github.com/Luce-Org/lucebox/tree/main/optimizations/megakernel) | Qwen3.5-0.8B hybrid DeltaNet/Attention implementation; separate Blackwell NVFP4 path | Current kernel is model-specific and batch 1. Half-precision and NVFP4 paths are different compute conditions. The standalone Python decoder drives steps and reads each output on the host. |
| [Mini-vLLM](https://github.com/BoundlessWindMoon/minivllm) | Small Qwen3 whole-layer CUDA decode implementation; HTTP and continuous-batching paths also exist | The inspected megakernel wrapper synchronizes and reads output on CPU per step. Qwen3.5 source presence is not qualified megakernel support. README says MIT but the inspected tree has no license file. |
| [MegaQwen](https://github.com/Infatoshi/MegaQwen) | Consumer-GPU Qwen3-0.6B cooperative decode implementation and detailed optimization experiments | Static batch1/short-context scope; separate LM head and CPU generation/argmax. README says MIT but no license file was found. A compute reference, not a general resident serving runtime. |
| [HazyResearch Megakernels](https://github.com/HazyResearch/Megakernels) | ThunderKittens-based Llama whole-forward implementation | Published build choices are H100/B200; a 5090 port is not verified. |
| [Cohere megakernel](https://github.com/cohere-ai/cohere-megakernel), [serving design](https://cohere.com/blog/megakernels) | OpenAI-compatible serving and paged KV around a decode megakernel | Current research release targets North Mini Code on one H100, BF16, batches1-8. Prefill pauses decode. Python controls admission/prefill; a C++ loop updates positions, launches, samples and streams each decode step. |
| [TileRT](https://github.com/tile-ai/TileRT) | Tile runtime and model backends for large multi-GPU serving | Current supported wheels target 8 B200s or 8 MI350-class GPUs, with exact PyTorch ABI requirements; core backend is distributed as a binary. Not a demonstrated single-5090 source adapter. |
| [ARK](https://github.com/microsoft/ark) | GPU-driven computation/communication loop-kernel framework and Llama2 example | A relevant execution-model precedent; current model breadth and 5090 compatibility still need verification. |


| [NVIDIA low-latency LSTM](https://github.com/NVIDIA/dl-lowlat-infer) | Apache-2.0 streaming LSTM persistent kernels, reference and ping-pong measurements | Small/medium always-spinning modes retain CPU publication/output polling; large mode launches per iteration. A useful non-LLM compute candidate, not a qualified network adapter. |
| [Qwen3-TTS adapter](https://github.com/gauravlochab/qwen3-tts-megakernel) | Apache-2.0 example reusing AlpinDale's trunk for speech on RTX5090 | Batch1; host/PyTorch codec head and sampling. Hidden-state cosine is not exact closed-loop agreement. A reuse example, not a ready GPU-only speech server. |
| [Qwen3 RTX5090 reproduction](https://github.com/emmanuelalo52/Qwen3-0.6B-megakernel-RTX-5090) | Dynamic-persistent CUDA/CuTeDSL decode paths and HF comparison scripts | No license found; test accepts partial-prefix matches. Eager-vLLM README gains are not matched serving-path evidence. |
| [MaruthiV megakernel](https://github.com/MaruthiV/megakernel) | Qwen3 BF16 whole-forward implementation targeting A100/H100/T4 | Single-token input interface; validation skips absent callbacks and generation hook takes only the last prompt token. No license or full-prompt correctness established. |
| [UCCL mKernel](https://github.com/uccl-project/mKernel) | MIT distributed compute/communication fusion for GEMM, MoE and attention | Components, not whole-model serving. Hopper default; Blackwell source targets SM103a/B300 and eight GPUs, not qualified SM120/RTX5090 support. |

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
The initial source audit read CUDA, importer, bindings and tests without a model
run. A later native qualification is recorded separately in
[the qualification finding](findings/0023-batch-execution-qualification.md#upstream-model-as-a-kernel-sm120-qualification).

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

### Additional source checks

A supplementary read-only search and source inspection on2026-10-11 expands
the candidate set; none of these source observations is a local model run.

- AlpinDale revision [5030e154d39ecd054df03eb4dd9c8aa8185414d1](https://github.com/AlpinDale/qwen_megakernel/tree/5030e154d39ecd054df03eb4dd9c8aa8185414d1)
  has an MIT license. csrc/kernel.cu keeps barrier/position/token state in
  process-global pointers. csrc/torch_bindings.cpp's generate_nosync()
  invokes the bulk launcher and synchronizes once at the end; this establishes
  a useful API boundary, not autonomous service across arriving requests.
- Lucebox revision [ae039d0acc2f03cd0e8cff33836ad05e4f64d310](https://github.com/Luce-Org/lucebox/tree/ae039d0acc2f03cd0e8cff33836ad05e4f64d310)
  is Apache-2.0. Its megakernel README documents the separate Blackwell
  NVFP4 path; model.py and model_nvfp4.py generate() call step() in a CPU
  loop and read the result with item(). The latter also exposes step_many();
  its existence is not qualification of an autonomous online request loop.
- Mini-vLLM revision [c5bde277518942bbebec0730f5b6684f396d7042](https://github.com/BoundlessWindMoon/minivllm/tree/c5bde277518942bbebec0730f5b6684f396d7042)
  and MegaQwen revision [0bc1fdedb82744481373000c5c7d3c58795c7a3a](https://github.com/Infatoshi/MegaQwen/tree/0bc1fdedb82744481373000c5c7d3c58795c7a3a)
  have public source but no license path in their inspected trees.
- [FlashFormer](https://arxiv.org/abs/2505.22758)'s author repository migrated
  to [cheetah-lang/flashformer](https://github.com/cheetah-lang/flashformer/tree/4768b7684ddf94d4845e5c36e2370a3f3c5bd112).
  Its47-file tree exposes operators, memory/synchronization primitives and
  component tests; a complete whole-model runner and license were not
  established. Do not count this as a runnable backend solely from the paper.
- [AutoMegaKernel's experiments](https://github.com/RightNow-AI/AutoMegaKernel/blob/main/EXPERIMENTS.md)
  describe10/10 supported configurations including three named real
  checkpoints, configuration sizes and a toy. This is not ten independently
  qualified real-model serving backends.

## Selection and comparison implications

MPK is the strongest lead for an existing online queue/runtime interface.
model-as-a-kernel exposes a reusable finite generation interface, but the local
unchanged-compute qualification now has mixed strict-reference results. Luminal remains a compiler candidate
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


[NVIDIA's DOCA GPU packet-processing application](https://docs.nvidia.com/doca/sdk/doca-gpu-packet-processing-application-guide/)
already demonstrates GPU processing and replying to HTTP. CPU DPDK handles
SYN/FIN/RST and installs flow rules; CUDA kernels handle data and responses.
It bypasses OS sockets and kernel networking. Therefore GPU-handled HTTP itself
is not the distinction from this prior artifact.

[Linux device-memory TCP](https://kernel.org/doc/html/latest/networking/devmem.html)
already provides direct NIC/device-memory payload transfer while keeping TCP
header processing in the kernel. Its documented API retains userspace recvmsg,
sendmsg and buffer-return/completion handling. Zero-copy transfer and removing
the steady userspace request/control worker are different properties.

[Wave Persistent Kernel](https://dotwave.ai/technical-notes/wpk-persistent-kernel/)
is a first-party continuous-voice execution precedent: the resident program
advances a static cohort, while the host publishes input and waits for output.
Its benefit includes shared-weight batching, not solely eliminating dispatch.
No reusable public source artifact was established in this search; treat it as
a mechanism/evaluation reference rather than a ready backend.


## Further search and source checks

Expanded observation: 2026-10-11T05:53:47UTC onwards. This round used24 additional
queries across reusable/multi-model persistent runtimes, consumer-GPU kernels,
GPU-initiated serving, eBPF/sockmap, kernel-to-GPU inference and citation
branches from Blink. Search results were leads; judgments below use first-party
source, official proceedings or papers. No new model benchmark or clone was run.

Pinned source observations:

- NVIDIA/dl-lowlat-infer
  [a718567b47e8d80ac38d58ac76df8d98a0eaab3d](https://github.com/NVIDIA/dl-lowlat-infer/tree/a718567b47e8d80ac38d58ac76df8d98a0eaab3d):
  docs/persistent_timing.md distinguishes small/medium always-spinning and large
  launch-per-iteration modes. ModelPersistentBase.cuh lines204-220 publish CPU
  input signals and poll output. ModelAsSingleStepGemv.cu retains precompute,
  synchronization and an optional host preprocessing thread. README exposes
  three sizes, reference/ping-pong measurement and a CUDA120a build example.
  This is a useful short-compute/non-LLM lead without new model arithmetic;
  its persistent final timestep is not an entirely host-free whole pipeline.
- Qwen3-TTS
  [61cb00e0b1e50d058a5f3c67de1e2f99b845ce87](https://github.com/gauravlochab/qwen3-tts-megakernel/tree/61cb00e0b1e50d058a5f3c67de1e2f99b845ce87):
  README describes embedding injection, a changed host RoPE table and PyTorch
  codec-head/sampling. talker/megakernel_talker.py asserts batch1;
  validate_talker_trunk.py checks hidden-state cosine over110 prefill positions,
  not exact closed-loop outputs. Absorb the adapter pattern without treating
  its quality/performance claims as our qualification or importing its separate
  math optimizations.
- RTX5090 reproduction
  [5bb05f54c1339a8d1ccc8968ca2278772f38b120](https://github.com/emmanuelalo52/Qwen3-0.6B-megakernel-RTX-5090/tree/5bb05f54c1339a8d1ccc8968ca2278772f38b120):
  megakernel_dynamic/test_dps.py lines138-139 allow partial-prefix matches unless
  shorter than roughly half the compared sequence. This is weaker than our
  unchanged exact oracle. No license was found in the inspected tree/API.
- MaruthiV
  [f2c8fd5c7e221ffabd017dc85afbf4a133c0e12c](https://github.com/MaruthiV/megakernel/tree/f2c8fd5c7e221ffabd017dc85afbf4a133c0e12c):
  src/megakernel.cu lines86-106 accept one input_token/current_pos.
  host/validate.py lines142-161 skip absent callbacks, and the generation hook
  receives prompt_ids[-1]. A validation command is not complete-prompt proof.
  No license was found in the inspected tree/API.
- mKernel
  [97e916b3a731689e4ea98db60bfe5f8adcaf685a](https://github.com/uccl-project/mKernel/tree/97e916b3a731689e4ea98db60bfe5f8adcaf685a):
  Makefile lines34-48 already contain Blackwell SM103a/B300 despite the README
  roadmap. Do not call all Blackwell support absent or equate that component
  implementation with RTX5090 or a complete model server.

### Compute reuse and closest-work implications

[Blink sections4.2-4.3](https://arxiv.org/html/2604.07609v1#S4.SS2) reuse captured
TensorRT engines plus a persistent device scheduler. A whole-model megakernel
is not required. Its same-engine TensorRT-LLM comparison is a causal precedent.
This supports investigating mature graph-capturable compute alongside
megakernels. It does not establish that any existing framework graph is directly
reusable: [CUDA device-graph requirements](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html#device-graph-requirements)
require a single device, supported node types, host instantiation/upload and
proper executable-graph lifetimes. CPU callbacks, dynamic allocation and
host-only sampling/control need inspection in the actual backend.

- [Lynx, ASPLOS2020](https://doi.org/10.1145/3373376.3378528), verified through
  [the authors' institution](https://cris.technion.ac.il/en/publications/lynx-a-smartnic-driven-accelerator-centric-architecture-for-netwo-2/),
  offloads server data/control to SmartNICs and demonstrates neural inference
  without host CPU involvement. Accelerator network services without host CPU
  are older precedents than Blink.
- [SplitRPC, SIGMETRICS/POMACS2023](https://sigmetrics.hosting.acm.org/opentoc/acm23_vol7_issue2_toc.html)
  optimizes accelerator RPC on commodity NICs while retaining CPU orchestration
  across runtimes. "No expensive SmartNIC" alone is insufficient differentiation:
  conventional Linux TCP and steady userspace-worker removal must be demonstrated
  together. A runnable official artifact was not established here.
- [LAKE, ASPLOS2023](https://utns.cs.utexas.edu/assets/papers/lake_camera_ready.pdf)
  exposes accelerators to kernel applications with
  [public source](https://github.com/utcs-scea/LAKE). Its artifact uses a userspace
  API-remoting daemon. Kernel access to GPU compute alone is not our distinction;
  avoiding the steady request/control upcall is the candidate boundary.
- [Concordia](https://arxiv.org/html/2606.23521v1) is a persistent-queue/checkpoint
  precedent. Its paper bounds main claims to checkpoint/recovery and warns
  against interpreting executor microbenchmarks as faster static-graph decode.
  A reusable official artifact was not established in this search.

Investigation priorities remain backend correctness, actual request/step
control, online admission, KV/output ownership, streaming/reclamation and model
coverage. One compiler name or more Qwen forks do not prove broad support.
A qualified second architecture or short-compute model is more informative
than another tuning campaign on the same checkpoint. Credible optimized
userspace controls, CPU-contention/tail behavior and attributed costs are
proposed experiments, not established performance claims or a replacement of
the user's goal.

## Additional graph-runtime and networking artifact search

Read-only observation: 2026-10-11T06:05-06:10UTC. Queries covered multi-model
persistent inference, device-side task graphs, GPU-initiated RPC, Linux/eBPF
and socket paths, ForgeMegakernel artifacts, DITRON, Mustard, Paella, GPUnet
and GPU-Ether. An awesome list supplied leads; the decisions below use pinned
author source, primary papers and official proceedings. No new backend was
installed or run in this search.

- [DITRON, ICML2026](https://proceedings.mlr.press/v306/zheng26ai.html) has an
  actual public compute artifact in
  [Triton-distributed revision7908e4ea9010bb2238f9f05b28c904fd4b71c60a](https://github.com/ByteDance-Seed/Triton-distributed/tree/7908e4ea9010bb2238f9f05b28c904fd4b71c60a).
  Its MIT-licensed source includes ModelBuilder, DenseModel, paged KV, a Qwen3
  chat server and a decode benchmark. The megakernel guide reports BF16,
  batch1/context512 on8 H800 or8 H20 GPUs, including a CUDA-graph baseline.
  dense.py lines191-200 runs embedding/copy outside the generated kernel;
  model_server.py lines75-88 retains CPU generation and per-token .cpu().item().
  This is a concrete compiler/backend candidate, not an autonomous server or
  measured single-5090/multiple-architecture qualification.
- [Mustard, ICS2025](https://doi.org/10.1145/3721145.3730426) has MIT source at
  [38b0e5955829e12a00acc5974776ccbff6ea8bb9](https://github.com/ParCoreLab/mustard/tree/38b0e5955829e12a00acc5974776ccbff6ea8bb9).
  mustard/mustard.h lines108-129 has a GPU scheduler that dequeues ready
  subgraphs and invokes cudaGraphLaunch(..., cudaStreamGraphFireAndForget).
  Existing runnable workloads are LU and Cholesky; CUDA12.3/NVSHMEM/MPI are
  dependencies. This supplies reusable scheduling code and a compute-preserving
  precedent, not an HF importer or ready LLM network server.
- [Toward GPU-centric Networking on Commodity Hardware, EdgeSys2024](https://dejankosticgithub.github.io/documents/publications/gpucentric-edgesys24.pdf)
  already evaluates GPU-driven inference with RDMA on ordinary Mellanox NICs,
  including TVM-compiled SqueezeNet and superresolution. Public
  [apps revisionb7ee60ea8bb67837d5ae6753cec2449ef34af715](https://github.com/rdma-from-gpu/apps/tree/b7ee60ea8bb67837d5ae6753cec2449ef34af715)
  has TVM loading in executor.cu lines379-409 and self tail-launch in
  lines355-376. It retains initialization/connection management but supports
  sleeping host control during serving. It uses RDMA/peermem/PCIe-P2P, rather
  than ordinary Linux TCP. No LICENSE file appears in this apps tree;
  reuse licensing across its related repositories remains unestablished.
  Both CPU-free inference and no-SmartNIC operation have older precedents.
- [GPUnet, OSDI2014](https://www.usenix.org/conference/osdi14/technical-sessions/presentation/kim)
  already exposes GPU socket APIs and a face-verification service.
  [The authors' implementation account](https://acsl.ece.technion.ac.il/gpunet-networking-abstractions-for-gpu-programs/)
  explicitly retains a CPU NIC-control proxy; TCP also requires CPU transport
  and data movement. GPU socket syntax is therefore not equivalent to removing
  a steady userspace worker.
- [GPU-Ether, INFOCOM2021](https://netsys.ajou.ac.kr/publication/jung2021gpu/jung2021gpu.pdf)
  already implements persistent GPU packet I/O on commodity Intel Ethernet.
  It maps descriptors/doorbells using driver changes and GPU P2P.
  This is a packet-I/O precedent, not evidence of Linux TCP/HTTP compatibility
  or a complete LLM serving backend. An ordinary Ethernet NIC alone cannot
  distinguish BPFusion.
- [Paella's SOSP2023 artifact](https://github.com/eniac/paella/blob/master/sosp23_artifact/README.md)
  supplies public model-serving traces and direct-CUDA/Triton comparisons.
  It represents sophisticated userspace/software GPU scheduling. It is an
  evaluation/baseline lead, not a drop-in modern SM120 compute backend; its
  artifact uses older T4/P100 hardware and requires reproduction work.
- [ForgeMegakernel](https://arxiv.org/html/2609.12379v1) reports fourteen
  generated decode tasks across eight models and integration into SGLang,
  with independent intermediate-state checks. This search still finds no
  author-linked complete public repository. The model-generation campaign
  is a separate compute contribution; adopting its reported gains would not
  measure an eBPF benefit.

Together with Blink, these sources favor retaining two compute-reuse options:
upstream megakernel execution and device-launched captured computation.
Choosing the latter does not inherently require inventing model arithmetic.
Actual graph eligibility, full prompt/decode correctness, sampling, dynamic
shapes and buffer lifetimes still need backend-specific verification.

The proposed research boundary remains Linux TCP/HTTP + eBPF/kernel queue +
resident GPU control + asynchronous kernel TX, with demonstrated streaming and
recycling. Linux/eBPF still consume CPU. Same-model/same-precision/same-batching
userspace controls, total attributed host cost, CPU contention and client tail
latency are necessary evidence; merely eliminating launches or using a normal
NIC is insufficient novelty. More model-specific Qwen forks, new quantization
and repeated numerical tuning are not needed to establish this path claim.
