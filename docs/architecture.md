# BPFusion architecture

Three paths share the page: a synthetic resident-MLP reference, a host-driven
HF LLM baseline, and a real Qwen CUDA reference with kernel-owned TCP/HTTP
requests and replies. Their compute and control paths differ; compare the
scope table in README before interpreting performance.

## Data path

```
  client sendto (UDP :39400)
        |
        v
  tc/clsact ingress  (bpf/fusion.bpf.c)
        |  parse L2/L3/L4, match magic port
        |  take slot only if slots[i].state == FREE && done[i].state == FREE
        |  copy payload, stamp ingress_ns (bpf_ktime_get_ns), publish
        v
  pinned BPF page  (BF_PAGE_MMAP_BYTES, pinned at /sys/fs/bpf/bpfusion_ctl)
        |  resident reads slots[] / writes done[] in place
        |  producer owns slots[].state; responder owns done[].state
        v
  resident CUDA kernel  (executor/executor.cu, launched ONCE per run)
        |  spins: head > done_seq, slots[idx] == PENDING, done[idx] == FREE
        |  compute, fence, done[idx] = DONE, slots[idx] = FREE
        |  done_seq++ / served++
        v
  responder thread (userspace)
        |  waits on done_seq (futex), reads done[], recycles done[idx] = FREE
        |  sendto() the reply to the client
        v
  client recvfrom
```

The same page carries a second, independent token ring for the LLM path:

```
  client sendto (UDP :39402)
        |
        v
  llm_ingress (bpf/fusion.bpf.c)  ->  page.llm[idx].tok_in[], state=PENDING
        |
        v
  resident LLM executor (executor/llm_executor.py, Qwen2.5-0.5B, fp16)
        |  prefill + decode; writes tok_out[k], bumps produced after each token
        v
  client polls the slot; TTFT/TPOT from successive `produced` bumps
```


The LLM ring serves two transports. UDP (:39402) replies by having the client
poll `produced` in the page (above). TCP (:39403) parses the same request from a
stream segment at the tc hook, records `pad=1` + the peer in the slot, and the
executor streams each token id as a LE `u32` back on the accepted socket
(`0009`):

```
  client connect/send (TCP :39403)
        |
        v
  tc ingress TCP branch -> llm_fill(pad=1, peer=saddr:sport) -> slot PENDING
        |
        v
  resident LLM executor  ->  send(token) on the accepted socket (TCP_NODELAY)
        |
        v
  client recv (len = gen*4 bytes)
```
See `docs/findings/0009-tcp-path.md`.

An optional `--tcp --no-send` control replaces Python token sends with the
`bfusion_tx` module (finding 0012). The loader passes a real BPF map FD to
module initialization; `bpf_map_get` validates and holds the map. The module
uses the canonical page struct and the loading process network namespace.
It holds a TCP lookup reference across sends, sends outside RCU under the
socket lock without dereferencing `sk_socket`, and counts stream bytes exactly.
The executor publishes `DONE` after its final page access. TX releases the slot
only after `DONE` and complete send or terminal disconnect; `PENDING` is never
reclaimed on a timer. Kernel TX currently polls with `usleep_range(60, 120)`.
This control is not a GPU completion interrupt. The resident path below uses the sockmap/HTTP frontend.

The MLP path has **no per-request/per-batch GPU launch or control call**: the
kernel is launched once and stays resident; the host only drains the ingress
doorbell and samples the completion ring for the histograms. It is **not** a
fully no-userspace-worker path: a userspace responder thread still `sendto()`s
every reply, and the TCP/HTTP reply is not yet a kernel TX. The **LLM path is
even further** from the target — `executor/llm_executor.py` is a host-side worker
that accepts connections, runs HF prefill/decode per request and sends tokens.

The optional `executor/qwen.cu` reference now puts real Qwen prefill/decode,
KV cache and argmax inside one resident CUDA kernel (finding 0013), now
a cooperative grid with one CTA per discovered SM (finding 0016). It reads
the same token ring and publishes output directly for kernel TX. The host
only initializes and shuts down. Kernel accept and receive draining manage
connection lifetime. The default resident test now uses sockops/sockhash
stream framing and supports queued concurrent token-ID requests (finding 0014);
Content-Length HTTP POST framing now wraps the same token-ID body (finding 0015).
Stream requests carry a validation-pending flag until the GPU checks their
IDs against the loaded vocabulary. Rejections release their slot without
ending the resident grid: HTTP 400/empty body or binary connection EOF
(finding 0017). TX waits for validation before emitting a success header.
The kernel emits HTTP headers and streamed token bytes, retaining response order
on a connection even across ring wrap. Message offsets are read from the current
kernel strparser layout with CO-RE: helper byte offsets are skb-relative, whereas
several frames can share one skb. GPU text processing and continuous batching
remain open. Exact-token agreement is verified for the recorded eight-token
cases. Linear layers now use 16-row WMMA tiles with K partitioned across
eight warps per CTA; RoPE frequencies are initialized once at bootstrap.
Prompt vectors are evaluated together within each layer, with per-token
normalization and causal token/head attention. Decode and request execution
remain batch 1. Earlier scalar single-CTA/grid controls diverged
at the second prompt's output 21; the current Tensor Core reference matches
the first two 64-token prompts and diverges at the third prompt's output 63
(finding 0016). General long-output correctness remains unproven.

```
  client TCP / HTTP POST (:39403, binary token body)
    -> Linux TCP sequencing/reassembly
    -> sockops + sockhash stream parser/verdict (eBPF framing and admission)
    -> shared mmap BPF page, FREE -> WRITING -> PENDING
    -> one resident Qwen CUDA kernel (prefill/KV/decode/argmax)
    -> token publication + DONE (system-visible page stores)
    -> kernel module completion poll + ordered tcp_sendmsg_locked
    -> client HTTP header + token stream
```
The launcher loads weights, maps/registers the page, creates the listener,
launches CUDA and loads the module once. It then sleeps until shutdown.
There is no host accept/read/send, sampling or per-request launch loop in this
resident path. Kernel polling still has CPU cost; removing a userspace worker
is not proof of lower total host CPU work.

The compile-time `qwen-control` target provides a host-dispatch ablation of this
same path (finding 0018). The device kernel takes a uniform `once` argument:
false for the default launch-once loop, true to return after one whole request.
The control host polls the same queue and launches/synchronizes per request;
model math, grid resources, eBPF framing and kernel TX stay the same. It has a
host request-dispatch worker, so only the default binary meets the no-steady-
userspace-worker property. This control does not change the default path.

The `qwen-graph` variant (finding 0019) captures actual HF eager-fp16 GPU
operations during bootstrap and runs them through device graph tail launches.
A native dispatcher graph reads/validates the same queue, fills captured
inputs on-device, schedules prefill/decode and publishes each completed
argmax to the page. The host launches that service graph once and sleeps.
Tail ordering ensures model graph completion before publication/reuse.
Queue head/state/stop polling uses system-scope acquire loads; the native
backedge reloads shared publication words instead of reusing a cached condition.
Graph/kernel owners and buffers remain alive until the GPU finishes shutdown.
It reuses the existing kernel connection/TX path and still handles one request
at a time.
Captured graphs append new keys/values directly into shared GPU KV buffers
and expose only the exact attention prefix, avoiding repeated prefix
concatenation/copy-back (finding0022). This ownership relies on serial model
graph completion; future batching needs separate KV state for live requests. Its recorded 64-token oracle and prompt-edge controls pass; the
custom WMMA reference retains its separately recorded accuracy boundary.
Its `qwen-graph-control` variant uses the same uniform dispatcher kernel,
returning after a whole request so the host can launch/synchronize again.
Both modes retain GPU-tail decode, captured model computation and kernel TX;
the control measures request dispatch and has a steady host request worker.

## Ownership rules (the correctness core)

| object | writer | reader | recycle |
|---|---|---|---|
| `slots[i].state` | producer (BPF) | GPU + responder | GPU sets `FREE` after reading `x[]` |
| `done[i].state` | GPU | responder | responder sets `FREE` after copying `y[]` |
| `head` | producer (BPF) | GPU + host | monotonic |
| `done_seq` | GPU | host (responder + sampler) | monotonic |
| `stop_ns` | host, once | GPU | |

The GPU takes slot `i = done_seq % BF_SLOTS` only when both
`slots[i].state == PENDING` (producer published) and `done[i].state == FREE`
(responder finished a previous round) — otherwise it would overwrite a
completion the responder is still reading.

## Memory ordering

- Device→host-visible reads of the page use `__ldcg` (gpu-scope load,
  **bypassing the SM L1**, which is not coherent with host memory). `volatile`
  alone reads stale values forever.
- Device publications use `__stcg` after `__threadfence_system()`.
- Host reads/writes of page words use `__atomic_load_n`/`__atomic_store_n`
  (acquire/release).

## Components

| file | role |
|---|---|
| `bpf/fusion.bpf.c` | ingress parse + slot publish + doorbell; drops split ctl/done |
| `bpf/include/bpfusion_queue.h` | the canonical page layout (single source of truth) |
| `executor/executor.cu` | resident kernel + responder thread + latency sampling |
| `executor/cuda_timer.h` | `%globaltimer` ↔ `CLOCK_MONOTONIC` calibration |
| `tools/client.c` | `verify`/`own`/`burst`/`paced` client (MLP path) |
| `executor/llm_executor.py` | host-driven HF Qwen baseline on the token ring |
| `executor/qwen.cu` | real resident Qwen inference, bootstrap and shutdown only on the host |
| `executor/qwen_graph.py` / `.cu` | bootstrap-only HF graph capture and native GPU request/model dispatch |
| `module/bfusion_tx.c` | kernel connection ownership, completion polling and ordered TCP/HTTP TX |
| `tools/llm_bench.py` | LLM TTFT/TPOT vs a direct in-process baseline |
| `tools/llm_load.py` | LLM concurrency sweep (goodput / TTFT / TPOT) |
| `tools/perfcount.c` | per-PID instruction/cycle counting (perf_event_open) |
| `tools/insn_token.py` | CPU instructions per generated token under load |
| `tools/llm_tcp_client.py` | TCP LLM client (request in, tokens on the socket) |

## What is not here yet

- General HTTP and text input/output — the resident reference implements
  Content-Length POST with binary token bodies (`0015`), including split writes,
  pipelining, half-close and concurrent correctness controls.
  The separate Python baseline still uses tc packet ingress (`0012`). Physical
  packet loss/retransmission and overload response behavior remain unmeasured.
- **GPU-side tokenization and sampling** — the LLM executor is host Python
  driving HF `transformers` in the Python baseline; the optional CUDA Qwen
  reference performs prefill/decode/KV/argmax and token publication on-device
  but still consumes pretokenized input.
- A batched/served LLM (continuous batching, KV-cache sharing) — today batch 1.
- Real-NIC measurement (the `tc` hook is on `lo`).
- An asynchronous kernel→waiting-userspace wake to replace the doorbell poll
  (`bpf_send_signal` or a module); see `docs/findings/0001-ingress-wake.md`.
