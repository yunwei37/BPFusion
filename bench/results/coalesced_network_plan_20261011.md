# Matched network comparison after HTTP header/first-token coalescing

## Objective and admission

The repository has no formal paper RQ or thesis contract. This is a supporting
engineering experiment under the retained user objective: improve throughput
and latency of ordinary Linux TCP/HTTP + eBPF/sockmap -> shared queue ->
resident real-model inference -> asynchronous kernel TX, while reusing model
compute and comparing against credible optimized userspace request control.

Question: with identical resident GPU computation and default server TCP,
does removing the native userspace request/reply worker improve client latency
or throughput once BOTH transports submit the HTTP header and first available
tokens in one vectored send?

The largest credible outcome is additional evidence for the complete serving
path with existing computation, on two architecture families. It cannot prove
SOTA, real-NIC performance, total CPU savings or novelty.

Finding0025 supplies 80 valid cells but retains a roughly40ms plateau in both
transports. Finding0018's separate packet traces motivate header/body ACK/Nagle
buffering. Candidate coalescing changes an observed transport mechanism while
holding computation fixed, so this is not an unchanged repeat. Correctness and
passive traces are dependencies, not additional scientific contributions.

Positive primary intervals support only the measured latency/throughput
conditions. Negative intervals contradict superiority for those conditions.
Crossing-zero intervals are inconclusive, not equivalence. A mixed result is
reported by metric/model. None alone refutes the user's larger engineering
objective. If coalescing removes the plateau but the optimized native control
matches or wins, the next decision is to report that boundary and investigate
attributed host cost, contention/tails or physical networking, not tune model
math or add weaker baselines.

This outranks more model-specific kernel forks: the complete path and strict
compute are already available; the untested load-bearing issue is fair control
comparison after the common transport problem is repaired.

## Conditions

Reuse bench/resident_dispatch.py unchanged. Strongest runnable fair comparison
is resident kernel request/reply versus native user-network epoll request/reply,
both using the SAME FP16 HF graph executor, 8 private graph/KV banks and device
dispatcher. The optimized control submits whole resident GPU requests and does
not incur a deliberately slow Python token loop. This is a component ablation,
not an external SOTA baseline; TensorRT/SGLang comparisons remain separate.

Models: HuggingFaceTB/SmolLM2-135M and Qwen/Qwen2.5-0.5B-Instruct.
Matrix per model: output lengths1/64 crossed with closed-loop clients1/8.
Five paired process blocks, alternating mode order and rotating matrix order.
64 measured requests per cell, balanced four real prompt cases; eight warmups
per process precede measurement. Planned totals:80 cells,5120 requests,
166400 exact measured tokens,20 normal executor exits.

Both transports coalesce valid HTTP header/first tokens; kernel uses kvec and
tcp_sendmsg_locked, userspace uses iovec/sendmsg. Rejection/partial-send,
DONE/FREE/FIFO semantics remain unchanged. Server TCP defaults; existing common
client TCP_NODELAY remains. No QUICKACK, server NODELAY, sleep tuning, precision,
sampling or model arithmetic change. Anonymous versus kernel page backing and
polling still differ, so this cannot attribute an effect to syscalls alone.

Build/strict qualification receipts must precede collection:
tests/resident_qwen.py --gen 64 --prefill-edges, each transport x each model.
Expected per regression:335 exact valid replies/20432 tokens,259 rejections,
5000 empty connections, eight-client concurrency/ring reuse/mixed lengths/
pipelining/half-close/helper-thread signal termination, graph_error0,1 resident
launch; user accept/receive/send traced, kernel none after ready.
Numerical oracle, native timeout and correctness path are fixed.

Existing bench/tcp_stream_trace.py supplies passive loopback metadata and
independent eager HF token agreement for four real prompts/8 output tokens.
Run sequentially for each candidate transport/model after qualification.
Inspect whether a response header packet contains token bytes and whether any
long ACK-delayed gaps remain. Packet-arrival observer scheduling is a limitation.
These traces are mechanism diagnostics, not performance results and not a
matched old/new speedup comparison. Preserve failures and original exits.

## Metrics and interpretation

Primary latency: mean client TTFT for gen1/clients1; effect user minus kernel.
Primary throughput: aggregate output tokens/s for gen64/clients8; kernel minus
user. Five paired estimates and nominal two-sided Student t95(df4) intervals,
computed by native analyze(); four model/metric intervals are descriptive
without a family-wide significance claim. P50/P99 TTFT, TPOT, completion,
other matrix cells and per-pair values are secondary context.

TTFT/TPOT definitions follow vLLM's official serving benchmark metrics:
https://docs.vllm.ai/en/latest/api/vllm/benchmarks/serve/
Same-compute comparison precedent: Blink section6.1 compares the same TensorRT
engines to isolate orchestration (https://arxiv.org/html/2604.07609v1).
Native measurement retains monotonic request/token arrivals; tokens in one recv
share an arrival timestamp. Independently reconstruct all cell TPS and
latency/TPOT summaries, token agreement, order and paired intervals.

Executor process CPU excludes kernel TX/softirq. Global /proc/stat includes
clients and unrelated host work, so CPU numbers are descriptive and cannot
establish service-attributed savings. Preserve GPU clocks/power/temp per cell.
The existing SGLang service stays running on shared RTX5090. Record original
service process, GPU residency and host health before/during/after; pairing does
not prove the GPU was interference-free. All published claims remain
loopback/token-ID HTTP, short prompts, two small checkpoints and that hardware.

No causal old-versus-new coalescing speedup is claimed. Comparing this run's
numbers to finding0025 is historical context only. A quantitative optimization
effect would require a separately matched before/after experiment; it is not
silently inferred from these independent runs.

## Execution, evidence and completion

Run only in original yunwei356/bpfusion-dev Workspace /workspaces/repository,
on main. Preserve existing service and unrelated tools/setup_env.sh. Commit/
push qualified source and this plan before full collection; freeze commit,
commands, sources, configs and native raw outputs. No concurrent experiment,
new Workspace, external clone, model deployment, custom control interface or
runner replacement.

Exact preflight commands, sequentially:
```bash
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --preflight --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model HuggingFaceTB/SmolLM2-135M --output bench/results/coalesced_network_smol_preflight_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --preflight --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model Qwen/Qwen2.5-0.5B-Instruct --output bench/results/coalesced_network_qwen_preflight_20261011.jsonl
```

Exact full commands, sequentially:
```bash
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model HuggingFaceTB/SmolLM2-135M --output bench/results/coalesced_network_smol_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model Qwen/Qwen2.5-0.5B-Instruct --output bench/results/coalesced_network_qwen_20261011.jsonl
```

Archive exact native stdout/exit, source snapshot and host observations.
Do not restart on observation timeout; inspect the same live process.

Completion requires all80 cells/5120 requests/166400 exact measured tokens,
20 normal exits, native publication/completion/graph counters and cleanup.
Preserve negative, failed and inconclusive rows. A failed correctness/fairness
condition invalidates the affected comparison; do not count it as a win.
Fresh result reviewer independently audits complete raw evidence and estimates.
Update docs/evaluation.md and the existing finding sequence with honest
qualified implementation/diagnostic/matched-result boundaries.
