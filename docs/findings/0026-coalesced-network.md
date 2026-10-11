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

The first qualification and traces below apply to the original coalescing
candidate, before the later admission repair.

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

## Full failure and atomic admission repair

The first full run on frozen00d8ae3 exited1 at08:34:27UTC during Smol
pair2/resident/gen64/client8. Its [raw prefix](../../bench/results/coalesced_network_smol_20261011.jsonl)
and [stdout](../../bench/results/coalesced_network_20261011.stdout.txt) retain
17 complete cells,1144 exact measured replies,four executor records and a timeout.
Qwen did not start. That prefix cannot support the five-pair performance estimate.

The failure recorded one busy refusal at head72/stateWRITING/head_changed0.
The former producer reserved state before advancing head; bounded retries could
exhaust in that window. This supports the investigated admission explanation,
without establishing exhaustive failure causality. The repair atomically advances
head and reserves its physical slot in the existing aligned64-bit head/pad
region. Its high32 bitmap protects a producer even before WRITING/PENDING.
Kernel TX releases its bit after old accesses and FREE, using an explicit
release RMW that preserves concurrent head advances and other reservations.
Native control and the historical bridge use the same ownership representation.
Page size/offsets, capacity and retry count remain unchanged; no lossless-overload
or unlimited-contention claim follows.

[Repair qualification](../../bench/results/coalescing_admission_repair_20261011.stdout.txt)
retains builds, exact source,1536 unchanged dispatcher SASS rows and terminal
results. Four graph regressions pass; the two affected kernel cases reran after
the explicit-release module build. Both user cases retain unchanged binaries.
The final measured-path qualification covers1340 valid requests,81728 exact
tokens,1036 rejections and20000 empty connections, with the original oracle and
timeouts. Kernel final reservation bits are zero and all slots FREE.

The historical bridge now waits through head-before-PENDING publication rather
than skipping a request. Its real Qwen TCP check passes24 successive replies per
mode, three lengths and slot reuse. A separate actual-main diagnostic holds FREE
then WRITING before PENDING, obtains8 exact Qwen tokens, and verifies native
libatomic recycling preserves head and another reservation. These are compatibility
dependencies, not resident-GPU performance results or exhaustive race proofs.
The first bridge check delivered48 exact replies but exited1 in cleanup because
rmmod was absent. Only its cleanup was repaired to native x86 delete_module;
oracle/input/timeout are unchanged, and the complete rerun exits0. Module,
hooks and all test pins were separately verified cleaned.

## Preflight and full comparison

[Two historical native real preflights](../../bench/results/coalesced_network_preflight_20261011.stdout.txt)
qualify their original candidate only. Their raw outputs retain the actual oracle, metrics,
model/runtime versions and executor counters:
[Smol](../../bench/results/coalesced_network_smol_preflight_20261011.jsonl),
[Qwen](../../bench/results/coalesced_network_qwen_preflight_20261011.jsonl).
Each model has eight exact measured one-token requests and two normal
executors; each executor also checks eight warmups and 264 model graph steps.

[Fresh repaired-source preflights](../../bench/results/coalesced_network_preflight_retry1_20261011.stdout.txt)
exit0 for [Smol](../../bench/results/coalesced_network_smol_preflight_retry1_20261011.jsonl)
and [Qwen](../../bench/results/coalesced_network_qwen_preflight_retry1_20261011.jsonl):
16 exact measured one-token replies/four normal executors, with264 graphs,
launch1/error0 per executor, kernel busy0/reserved0/eightFREE and cleanup.
These establish executability only. Qualified source is being published
before full collection; the entire matrix reruns
from the beginning, using fresh retry1 outputs without stitching the failed
prefix. Planned matrix: both models, gen1/gen64,
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
