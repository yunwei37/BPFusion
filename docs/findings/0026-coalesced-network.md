# 0026: HTTP header/first-token coalescing with matched GPU computation

## Question and implementation

This supporting engineering comparison asks whether the kernel request/reply
path improves client latency or throughput over native userspace epoll after
both transports coalesce the HTTP header and first available output tokens.
The full Linux TCP/eBPF -> resident real-model GPU -> asynchronous kernel TX
goal remains active. This is a component ablation, not an external SOTA or
novelty result.

The [reviewed plan](../../bench/results/coalesced_network_plan_20261011.md)
holds FP16 HF computation, eight graph/KV banks, device dispatcher, oracle and
default server TCP fixed. [Independent plan review](../../bench/results/coalesced_network_plan_review_20261011.md)
admits the complete comparison. Both paths use the same GPU dispatcher
instructions and encodings: native cuobjdump comparison records 1536 matching
instruction/encoding rows (768 instructions plus continuation rows).

Kernel TX now supplies a kvec containing the remaining header and available
body to tcp_sendmsg_locked. The userspace control supplies the corresponding
iovec to nonblocking sendmsg. Partial sends update header and body byte offsets
separately, including a partial u32; socket ownership and DONE/FREE FIFO
reclamation remain unchanged. A valid header waits for the first available
token; bodyless rejection headers still complete immediately. No model
arithmetic, precision, server NODELAY/QUICKACK or polling parameter changes.

## Qualification and diagnostic evidence

[Native builds and four strict regressions](../../bench/results/coalescing_qualification_20261011.stdout.txt)
complete for SmolLM2-135M and Qwen2.5-0.5B in both transports:
1340 valid requests, 81728 exact generated tokens, 1036 rejections and
20000 empty connections. Each case passes concurrent clients, immediate
reject/valid reuse, ring wrap, mixed decode lengths, pipeline/half-close and
helper-thread shutdown. Device counters show one resident launch,
20432 model graphs, graph_error=0, banks=8 and max_active=8 per regression.
Userspace traces include accept4/recvfrom/sendmsg; kernel traces have no steady
userspace request/reply syscalls. The numerical oracle is unchanged; only the
positive userspace syscall assertion follows the send-to-sendmsg implementation.

Module builds use the native make path and the running kernel's headers with
CC=gcc-15. Missing headers/compiler/pahole dependencies were supplied only in
the owning Workspace from the existing host files; host configuration and the
default CUDA compiler remain unchanged. Actual loading and the two kernel
regressions establish more than compilation. Compiler patch-version and
pahole/BTF warnings remain visible in the build receipt.

The [passive diagnostic log](../../bench/results/coalescing_traces_20261011.stdout.txt)
retains the first failed attempt and the successful retry commands/source.
The [failed raw attempt](../../bench/results/coalescing_trace_smol_kernel_20261011.jsonl)
ended during graph capture because the diagnostic imposed a 60-second startup
assertion. After that process and its hooks/module/pins were terminal and
cleaned, only that diagnostic startup deadline was removed to match the native
benchmark's readiness/child-exit wait. Request timeout, service lifetime,
shutdown wait and oracle were unchanged. No failed output was overwritten.

Successful native diagnostics, four real prompts and eight output tokens each:

| model | kernel metadata/replies | userspace metadata/replies |
|---|---|---|
| SmolLM2-135M | [raw](../../bench/results/coalescing_trace_smol_kernel_retry1_20261011.jsonl) | [raw](../../bench/results/coalescing_trace_smol_user_retry1_20261011.jsonl) |
| Qwen2.5-0.5B | [raw](../../bench/results/coalescing_trace_qwen_kernel_retry1_20261011.jsonl) | [raw](../../bench/results/coalescing_trace_qwen_user_retry1_20261011.jsonl) |

All four diagnostics exit zero: 16 exact replies and 128 tokens, zero graph
errors, with cleanup checked. All 16 observed response-header packets contain
79 header bytes and the first four token bytes. Client TTFT in these tiny
diagnostics ranges from 2.28 to 7.36 ms; this is not a performance estimate or
a matched before/after optimization effect.

The second through fourth requests in each trace still show an ACK about
40.397-42.255 ms after the header/first-token packet, followed by the remaining
28 response bytes about 0.013-0.036 ms later. This supports an ACK/Nagle
buffering explanation for remaining short-response delivery gaps. Passive
receive timestamps include observer scheduling; they do not measure GPU-ready
time or establish every full-run request's cause. Coalescing the first token
does not establish that all streaming latency is removed.

## Preflight and full comparison

[Two native real preflights](../../bench/results/coalesced_network_preflight_20261011.stdout.txt)
qualify execution only. Their raw outputs retain the actual oracle, metrics,
model/runtime versions and executor counters:
[Smol](../../bench/results/coalesced_network_smol_preflight_20261011.jsonl),
[Qwen](../../bench/results/coalesced_network_qwen_preflight_20261011.jsonl).
Each model has eight exact measured one-token requests and two normal
executors; each executor also checks eight warmups and 264 model graph steps.

The complete comparison is not yet collected. The source will be committed
before the native five-pair run. Planned matrix: both models, gen1/gen64,
one/eight clients, 64 requests per cell; 80 cells, 5120 exact measured
requests, 166400 generated tokens and 20 normal exits. The unchanged native
benchmark alternates mode order and rotates cell order. Primary effects are
user-minus-kernel mean TTFT for gen1/client1 and kernel-minus-user aggregate
TPS for gen64/client8, with five-pair nominal Student t95 intervals. A fresh
result review must reconstruct the complete matrix before a performance claim.

Finding0025 remains historical context, not a matched old/new coalescing
measurement. Anonymous versus kernel page backing and polling differ; process
CPU excludes kernel TX/softirq, and global CPU includes unrelated work. The
SGLang service is preserved on the shared RTX5090. Loopback, token-ID HTTP,
short prompts and two small models limit inference. Attributed host cost,
physical networking, text processing, continuous batching and strong external
serving comparisons remain open.
