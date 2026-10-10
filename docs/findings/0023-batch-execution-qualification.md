# 0023: batch execution qualification

## Why qualify computation before implementing batching

Finding0022 removes repeated KV prefix work but leaves serial requests and large eight-client queueing. The next service work is concurrent/batched execution without a steady host request worker, with independent KV ownership and the same exact eager-fp16 oracle. These are engineering qualification probes, not standalone research or serving-speed results.

## Ordinary HF batch-shape candidate

The [complete raw](../../bench/results/qwen_batch_shape_qualification_20261010.txt) includes the exact temporary script, source commit97a5f74, installed versions, independent batch1 eager-HF oracle sequences, command and all actual outputs. It uses the original exported weights through load_model, eager attention, fp16, last-position logits and ordinary HF DynamicCache. It does not run TCP, the native dispatcher or a resident service. Its host-driven calls are a diagnostic, not the final worker-free path.

The full matrix uses batch2/4/8, each of the ten gen64 correctness/prompt-edge cases replicated across lanes, plus a same-prefix-length mixed batch of the real France/greeting prompts. Every lane owns its own KV state in the HF batch. All33 groups completed and produced9,856 tokens;26 groups pass and7 fail exact oracle agreement. Exit0 means the diagnostic matrix completed, **not** that the candidate passed. No group was omitted after a mismatch.

| batch | failing group | first divergent zero-based output | expected / actual |
|---|---|---:|---:|
| 2 | greeting (case2), mixed5 greeting lanes | 62 | 323 /11 |
| 4 | arithmetic (case1) | 20 | 5145 /64547 |
| 4 | one-token prompt edge (case4) | 31 | 36277 /7010 |
| 8 | greeting (case2), mixed5 greeting lanes | 62 | 323 /11 |
| 8 | one-token prompt edge (case4) | 31 | 36277 /7010 |

The tested batch-shape change diverges under the fixed strict oracle. This does not establish that ordinary HF batching is generally wrong or isolate which arithmetic/dispatch difference causes divergence. The oracle and precision standard are unchanged; no tensor-batched production change is retained, and no latency/throughput figure is reported from this probe.

## Independent batch1 graph-bank qualification

The alternative keeps each request's qualified batch1 calculation shapes and private input/KV/output tensors while sharing read-only model weights. A GPU dispatcher launches each bank's selected model graph with CUDA FireAndForget, then tail-launches itself to sample outputs and feed the next decode step. CUDA's [device graph execution environments](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html) include child work: the parent tail waits for the whole environment, including the fire-and-forget children. This is a GPU-controlled fork/join route, not evidence that model kernels actually overlap.

The [temporary native build raw](../../bench/results/qwen_graph_bank_build_20261010.txt) preserves the exact addon, Makefile command and output at source2062f44. The addon was appended only for its temporary build; production native source was restored unchanged. Each raw below contains the exact wrapper and independent batch1 oracle outputs. Captured graphs and all tensor keepers remain alive through native graph-exec destruction. The first [bank2 attempt](../../bench/results/qwen_graph_bank2_qualification_20261010.txt) completed its first128 model graphs with zero GPU error, then failed while printing because json was absent from exec globals. That failed attempt is retained and is not a completed qualification. The repair adds only json to those globals; capture, scheduler, oracle and evaluation are unchanged.

| private banks | groups passing / completed | exact output tokens | model graphs per job | host launches per job |
|---:|---:|---:|---:|---:|
| [2](../../bench/results/qwen_graph_bank2_qualified_20261010.txt) | 12 /12 | 1,536 | 128 | 1 |
| [4](../../bench/results/qwen_graph_bank4_qualified_20261010.txt) | 12 /12 | 3,072 | 256 | 1 |
| [8](../../bench/results/qwen_graph_bank8_qualified_20261010.txt) | 12 /12 | 6,144 | 512 | 1 |

Each bank-count matrix includes all ten gen64 correctness/prompt-edge cases replicated across banks, a mixed France/greeting group, and a mixed-prompt-length group. All36 groups complete with exact agreement on10,752 tokens; all36 native markers report error=0 and one host launch per whole job, with no per-decode host model calls. These are engineering qualifications, not serving benchmarks: there is no TCP/shared BPF queue/module execution, latency measurement or demonstrated kernel overlap. The production service remains serial.

## Next execution route

Integrate private graph banks into the real GPU-owned request queue. Admission and reclamation follow the existing head-indexed ring; out-of-order computation must preserve slot ownership and per-connection response order. Real TCP lifecycle correctness, actual overlap and serving benefit remain unproven. Do not label this completed continuous batching.
