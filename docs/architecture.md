# BPFusion architecture

One picture of what runs today, and where each piece is measured. Two paths
share the page: a **synthetic-MLP path with a resident, launch-once CUDA
kernel** (the mechanism this project is about) and a **real-LLM path driven by
a host Python executor** (the honest baseline that produces TTFT/TPOT numbers).
They have different maturity; `README.md` has the scope table.

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
This is not a GPU completion interrupt or a sockmap/HTTP frontend.

The MLP path has **no per-request/per-batch GPU launch or control call**: the
kernel is launched once and stays resident; the host only drains the ingress
doorbell and samples the completion ring for the histograms. It is **not** a
fully no-userspace-worker path: a userspace responder thread still `sendto()`s
every reply, and the TCP/HTTP reply is not yet a kernel TX. The **LLM path is
even further** from the target — `executor/llm_executor.py` is a host-side worker
that accepts connections, runs HF prefill/decode per request and sends tokens.

The optional `executor/qwen.cu` reference now puts real Qwen prefill/decode,
KV cache and argmax inside one resident CUDA kernel (finding 0013). It reads
the same token ring and publishes output directly for kernel TX. The host
only initializes and shuts down. Kernel accept and receive draining manage
connection lifetime. The default resident test now uses sockops/sockhash
stream framing and supports queued concurrent token-ID requests (finding 0014);
HTTP, GPU text processing and continuous batching remain open.

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
| `executor/llm_executor.py` | resident Qwen2.5 executor on the token ring |
| `tools/llm_bench.py` | LLM TTFT/TPOT vs a direct in-process baseline |
| `tools/llm_load.py` | LLM concurrency sweep (goodput / TTFT / TPOT) |
| `tools/perfcount.c` | per-PID instruction/cycle counting (perf_event_open) |
| `tools/insn_token.py` | CPU instructions per generated token under load |
| `tools/llm_tcp_client.py` | TCP LLM client (request in, tokens on the socket) |

## What is not here yet

- HTTP and text input/output — the resident reference has sockops/sockhash
  stream framing (`0014`) with split-write and concurrent correctness controls.
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
