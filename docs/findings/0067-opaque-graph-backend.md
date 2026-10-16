# A non-LLM captured-graph transport boundary

The normal source now accepts caller-owned, device-launchable CUDA graphs and
opaque input/output buffers through [ABI1](../../executor/graph_backend.h).
The existing TCP/eBPF/io_uring and efficient native epoll paths share the
same generic GPU dispatcher. No model dimensions, vocabulary, tokenizer,
KV cache or autoregressive loop enters this adapter.

The actual [normal Make builds and four lifecycle runs](../../bench/results/graph_backend_20261016/)
use default8, ordinary non-BF_TRACE libraries, Linux7.3rc3/RTX5090 and the
existing pinned Torch2.13.0+cu129 environment. The example captures unchanged
upstream cuBLAS matrix multiplication and cuFFT, without handwritten math
kernels. All four operation/transport cases pass182 checks each:128 concurrent
requests, connection reuse/idle, HTTP400 and binaryEOF/recovery, half-close,
40 pipelined requests, RST recovery and queued SIGTERM. In each case180
complete output checks cover11520 words, plus2 intended rejections.
Canceled requests are separate observed numeric prefixes, not complete replies.
All four stop prefixes end on full words; all kernel ring cursors drain,
accepted equals closed, and error/pending/reserved/drop/overflow are zero.
The legacy128-entry reply sample truncates71/86 records; no zero-truncation
claim is made.

Matrix inputs and the fixed8x8 weight contain small integers, so the independent
CPU integer sum is exactly representable in FP32; every output compares
numerically exactly. FFT controls use analytically exact zero, index0 impulse,
constant and alternating32-point inputs. Signed zero is numerically equal.
This is finite control fidelity, not a general FFT numerical error bound or
proof for arbitrary user graphs.

The initial missing fcntl.h build and harness cleanup failure are preserved;
the include/owned-pin cleanup repair and full four-case rerun are explicit.
These engineering checks qualify this small boundary, not a paper speedup.
No timing comparison was selected from them.

The interface is one-shot and fixed-shape, at most64 input/output words, with
one graph/buffer pair per slot. Device-launchable graph restrictions still
apply. LLM generation remains a separate scheduler; wire/internal names are
historical LLM names. No universal CUDA plugin stability or compatibility
claim follows. See the [runnable example and ownership contract](../graph-backends.md).
