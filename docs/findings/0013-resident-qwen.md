# 0013: real Qwen in one resident CUDA kernel

Observed 2026-10-10 UTC: RTX 5090, CUDA 13, Linux 7.3-rc3. Raw output:
[resident_qwen_20261010.txt](../../bench/results/resident_qwen_20261010.txt).

## Implemented path

`executor/qwen.cu` executes the actual Qwen2.5-0.5B-Instruct model with
fp16 weights and fp32 dot accumulation. One CUDA CTA, launched once, consumes
the mmap BPF token ring directly. Embedding, RMSNorm, Q/K/V projections, RoPE,
causal grouped-query attention, KV cache, residuals, SwiGLU and vocabulary
argmax all execute on-device. Prompt tokens are processed sequentially for
prefill; decode reuses the on-device KV cache. The GPU writes each token and
produced count, then releases DONE after its final page write. The kernel TX
module sends those tokens through Linux TCP.

This is a scalar/warp reference, not tensor-core optimized. Model dimensions,
normalization epsilon and RoPE theta are discovered from the HF config during
export. The export supports tied-embedding Qwen2 with default RoPE and full
attention. The existing 64-token request and output bounds imply at most 128
KV positions. Model weights remain outside Git; they are not test fixtures.

Implementation references: [Qwen model config](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct/blob/main/config.json)
and [HF Qwen2 math](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen2/modeling_qwen2.py).
The correctness oracle uses installed Transformers 5.19.0 eager attention and
fp16 greedy inference. It is loaded, produces expectations, and is released
before the resident executor starts.

## Reproduce

```sh
make probes tools qwen
make -C module CC=gcc-15
python3 tools/export_qwen.py /workspaces/.cache/bpfusion/qwen25-05b-fp16.bin
python3 tests/resident_qwen.py
```

Export writes 988,065,568 bytes: a 32-byte dimensions/epsilon/theta header and
contiguous fp16 tensors in the order stated in `tools/export_qwen.py`. CUDA
loads these once before launch. The test owns its executor, tc hook and module
and cleans them up. It requires the same root/GPU/matching-header environment
as finding 0012.

## Result and limits

Four real prompts, eight generated tokens each, repeated three times: all
12 TCP requests and all 96 generated IDs exactly match the independent eager
HF oracle. The eight-slot ring is reused. The host executable only initializes
weights, maps the page, creates a listener, launches CUDA, sleeps, and sets a
shutdown flag. It has no accept/read/send or per-request CUDA launch loop.
Kernel TX log reports 384 bytes and 12 completions. The module and test
processes exit and GPU allocation returns to 15 MiB; boot ID is unchanged.

Eight-token completion takes approximately 1.1–1.7 seconds in this reference.
No throughput improvement is claimed. No logits error bound or broad accuracy
result follows from agreement on these prompts. HTTP, text tokenization,
detokenization, sockmap stream framing, concurrent producers/batching and
physical-NIC measurements remain unimplemented. The listener is not drained
in this first increment, so pending connections consume its accept backlog;
kernel acceptance and receive-buffer cleanup are the next lifecycle repair.
The TX module still polls the completion page rather than using a GPU
completion interrupt. This is real resident-model inference with kernel TCP
replies on a pretokenized sequential loopback path, not the full service goal.

## Follow-up: kernel-owned connection lifecycle

The launcher now passes its map and listener FDs to module initialization.
The module pins the listener file with sockfd_lookup, accepts connections
with kernel_accept, and drains already-ingested request bytes with
nonblocking kernel_recvmsg. Accepted sockets stay kernel-owned until EOF
after their slot finishes or a terminal receive error. Shutdown releases
all accepted sockets and the listener reference. The launcher unloads its
module after the resident kernel has stopped. No userspace accept loop was
added. This replaces the undrained-backlog limitation of the initial run.

Reproduction uses the same test command and additionally requires `strace`.
The updated test first opens/closes 5,000 empty connections (beyond Linux's
SOMAXCONN listen backlog), then repeats the 12 exact Qwen requests. Raw logs:
[accept/trace control](../../bench/results/resident_qwen_accept_trace_20261010.txt),
[executor syscalls after ready](../../bench/results/resident_qwen_network_20261010.txt).
All 96 tokens still match HF eager. Module counters show accepted=5012,
closed=5012, completed=12 and 384 output bytes. Strace follows all executor
threads and finds no accept/receive/send syscalls after ready. The earlier
[accept-only run](../../bench/results/resident_qwen_accept_20261010.txt) also
matched 96 tokens and closed all 12 connections. Split/retransmitted stream
input, HTTP/text processing and the other limitations above remain open.
