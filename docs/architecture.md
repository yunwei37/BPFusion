# BPFusion architecture

One picture of what runs today, and where each piece is measured.

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
  pinned BPF page  (BF_PAGE_MMAP_BYTES, /sys/fs/bpf/bpfusion_page)
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

See `docs/findings/0005-resident-llm.md`.

There is **no host/GPU control call on the steady-state path**: the kernel is
launched once and stays resident; the host only drains the ingress doorbell and
samples the completion ring for the histograms.

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

## What is not here yet

- TCP path (`sockops`/`sockmap` + kernel TX) — today the reply is a userspace
  `sendto`, not an asynchronous kernel TX completion.
- **GPU-side tokenization and sampling** — the LLM executor is host Python
  driving HF `transformers`; prefill/decode run on the GPU but tokenize/detokenize
  and the token stream into the page are host work.
- A batched/served LLM (continuous batching, KV-cache sharing) — today batch 1.
- Real-NIC measurement (the `tc` hook is on `lo`).
- An asynchronous kernel→waiting-userspace wake to replace the doorbell poll
  (`bpf_send_signal` or a module); see `docs/findings/0001-ingress-wake.md`.
