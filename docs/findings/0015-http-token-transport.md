# 0015: kernel HTTP token transport to resident Qwen

Observed 2026-10-10 UTC on the RTX 5090 / CUDA 13 / Linux 7.3-rc3 Workspace.
The loopback path now accepts HTTP Content-Length POST requests in the
sockmap BPF stream frontend, publishes their binary token bodies to the
shared page, executes actual Qwen inference inside one resident CUDA kernel,
and returns HTTP headers plus token bytes through the kernel TCP module.
Kernel accept/drain owns connections; userspace only initializes and stops.

## API and implementation

On TCP port 39403, send a normal HTTP POST with one Content-Length header
and a binary body. The URI is not routed; tests use /generate. Body layout,
little endian: magic u32=0x514c4d51, n_prompt u32, n_gen u32, reserved u32,
client_monotonic_ns u64, followed by n_prompt u32 token IDs. Prompt and
output each use the existing 1..64 token ring bounds. A successful reply is
HTTP/1.1 200 OK, Content-Type application/octet-stream, Content-Length
n_gen*4, then exactly n_gen little-endian u32 generated IDs. The original
unwrapped binary TCP protocol is still accepted on the same listener.

BPF scans available stream bytes for the header terminator and a
case-insensitive Content-Length; it requires exactly one length matching
the token body. There is no separate configured header-length cap. The
byte state transition is an independently verified global BPF function,
which avoids verifier state explosion without shortening accepted headers.
This is a minimal transport, not a general HTTP server: no JSON/text,
chunked transfer, TLS, routing, OpenAI compatibility or HTTP error contract.
Malformed requests and overload do not currently produce explicit status
responses. The client tokenizes; the GPU does not yet tokenize/detokenize.

The module accounts for partially sent HTTP header and token bytes
independently. It waits for earlier requests on the same peer before sending
a later response, including ring wrap or TCP backpressure. Slots remain
executor-owned until DONE; disconnect does not reclaim PENDING memory.

## Faults caught by persistent-connection control

The initial split-write/concurrent control passed 20 requests/160 tokens:
[initial HTTP log](../../bench/results/resident_qwen_http_20261010.txt).
A six-request pipeline exposed response-header interleaving:
[before ordering repair](../../bench/results/resident_qwen_http_pipeline_before_20261010.txt).
After fixing TX order, the pipeline still returned the first prompt's tokens
for a later request:
[ordering-only repair](../../bench/results/resident_qwen_http_pipeline_20261010.txt).

Linux strparser can clone one skb for several framed messages while retaining
the original data base. The generic bpf_skb_load_bytes helper addresses that
base; each message's offset must also be applied. The frontend now uses
bpf_cast_to_kern_ctx plus CO-RE to read sk_skb_cb.strp.strp.offset and includes
it in every framing/payload read. Sources:
[Linux strparser](https://github.com/torvalds/linux/blob/v7.3-rc3/net/strparser/strparser.c),
[message layout](https://github.com/torvalds/linux/blob/v7.3-rc3/include/net/strparser.h),
[byte helper](https://github.com/torvalds/linux/blob/v7.3-rc3/net/core/filter.c).
This depends on modern kernel kfunc/BTF support, tested on this kernel; no
portable-kernel compatibility claim is made.

## Reproduce and verified scope

```sh
make probes tools qwen
make -C module CC=gcc-15
# export the real model weights outside Git as in finding 0013
python3 tests/resident_qwen.py
PYTHONPATH=executor python3 tests/kernel_tx.py
```

The final [real-model log](../../bench/results/resident_qwen_http_pipeline_fixed_20261010.txt)
contains 26 requests / 208 generated IDs, all matching the independent eager
HF fp16 oracle: 12 binary and 14 HTTP requests, four prompts, byte-separated
writes, eight concurrent clients, and six pipelined HTTP requests on one
half-closed connection across the ring boundary. Kernel counters report
26 stream publications, 5,021 socket registrations, zero registration
failures/drops, 1,126 parser calls and zero parser errors. The existing
[TX ownership/reset regression](../../bench/results/kernel_tx_http_regression_20261010.txt)
also passes 24 exact synthetic replies, two resets and 26 recycle cycles.
Strace follows every executor thread and finds no accept/receive/send
syscalls after ready. The test unloads its module, detaches the stream hook,
removes its pins and stops its process. Host boot ID remained unchanged.

This establishes a real HTTP token-body -> resident model -> asynchronous
kernel TCP TX closed loop without a steady userspace request worker. Kernel
TX still polls, the GPU is a slow one-CTA reference, and concurrency is queued,
not continuously batched. No total-CPU reduction, tail-latency improvement,
physical-NIC result, packet-loss behavior or broad model-quality claim follows.
