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

## Next execution route

Investigate concurrently executing independent **batch1** captured model graphs, with separate input/KV/output owners per request and GPU-controlled scheduling. This retains the already-qualified calculation shapes while allowing request work to overlap. It is an execution-architecture proposal; correctness, memory/lifetime, actual overlap, FIFO TCP response/admission behavior and real serving benefit remain unproven. Do not label it completed continuous batching.
