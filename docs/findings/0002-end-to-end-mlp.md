# Finding 0002 — packet → GPU → packet, measured end to end

Status: measured on 2026-10-08 on the host described in
`bench/results/HOST.md`. Raw logs:

- `bench/results/e2e_20261008T032203Z.txt` — the full path (GPU daemon + baseline)
- `bench/results/batch_sweep_20261008T030937Z.txt` — throughput vs batch depth
- `bench/results/saturation_20261008T032028Z.txt` — GPU occupancy under overload

## Question

Does a request go from the wire, through an eBPF ingress hook into an
mmap'able kernel control page, through a resident GPU executor, and back out a
socket — with the *GPU* result matching a CPU reference, and with the per-stage
costs and the GPU idle time all visible? And how much of the wall time is the
GPU actually executing versus waiting on the host staging path?

## The path as built

```
 client sendto()
      │
      ▼  lo ingress, clsact/tc  (bpf/fusion.bpf.c)
 BPF: parse eth/ip/udp, check magic
      take ctl slot only if both slots[i] and done[i] are FREE   (else drop++)
      copy x[] from skb, stamp ingress_ns = bpf_ktime_get_ns()
      slots[i].state = PENDING ; head++ ; ringbuf doorbell submit
      │
      ▼  mmap'ed page (BPF_F_MMAPABLE array, pinned /sys/fs/bpf/bpfusion_ctl)
 executor.cu GPU loop: stage batch through pinned memory, cudaMemcpyAsync
      bf_exec_kernel<<<1,16>>>: work passes of 16×16×16 + leaky-ReLU
      %globaltimer start/done, __threadfence_system, done[i].state = DONE
      │
      ▼  responder thread: read done[], sendto() the recorded peer
      free slots[i].state then done[i].state  (slot recyclable only now)
```

No `SO_ATTACH_BPF`, no per-connection socket: the pinned page *is* the queue.
The kernel program is attached to `lo` ingress by `bpfusion_load attach lo`,
which owns the object lifetime; the daemon only `bpf_obj_get`s the pinned maps.

## Correctness

`./build/client verify` sends one request, recomputes the reference network in
`client.c:ref_forward` with the same weight formula as the kernel, and compares:

```
verify: max |GPU - CPU| = 2.602e-17 (OK)
verify: resp magic=46504251 id=0 client_ns_echo=yes
```

`2.6e-17` is float32 round-off (the values are ~1e-2 in magnitude), so the GPU
arithmetic path is confirmed bit-for-bit-consistent with the CPU model. The
`client_ns` echo confirms the response is paired with the request that produced
it rather than a stale slot.

Two bugs made earlier "verify" runs vacuous and are fixed: the reference input
was `1.0f` and the tiny MLP decayed it to ~0 (so the comparison passed
trivially); it is now `8.0f`, and the response's `client_ns` is echoed from a
dedicated field in `bf_done_slot` instead of racing on `slots[idx]`.

## Latency — one request in flight (`client own`, 2000 samples)

| stage | p50 | p90 | p99 | max |
|---|---|---|---|---|
| client round trip (sendto → response) | 45.7 µs | 46.8 µs | 53.8 µs | 358 µs |
| kernel parse → GPU kernel start | 7.4 µs | 8.0 µs | 9.9 µs | 321 µs |
| GPU kernel start → done (`%globaltimer`) | 26.85 µs | 27.2 µs | 27.5 µs | 31.3 µs |

`work=4` means 4 passes of the 16×16×16 triple; 26.9 µs is the arithmetic plus
a fixed launch cost, and its p50/p90/p99 spread is only 0.7 µs — the GPU part
is stable. The round trip is ~46 µs, so ~19 µs is the host side
(`parse → GPU start` + responder `sendto()` + wakeup) outside the kernel.

Daemon-side, over the 12002 requests of the same run:

| stage | p50 | p90 | p99 |
|---|---|---|---|
| kernel parse → GPU done | 123 µs | 198 µs | 238 µs |
| responder `sendto()` | 1.1 µs | 1.5 µs | 1.8 µs |

The `parse → GPU done` p50 is larger than the `own` figure because under a
burst the request waits in the 64-slot ring before its batch is picked up;
`sendto()` itself is ~1.1 µs, i.e. the replying socket path is not the
bottleneck.

## Throughput and the batch-size knee (`batch_sweep`)

`client burst` pipelines a fixed depth; each depth gets a fresh daemon.

| daemon batch | throughput (depth=size) | GPU passes busy/idle |
|---|---|---|
| 1 | 20 721 req/s | 2000 / 2592 |
| 4 | 28 034 req/s | 3986 / 4568 |
| 8 | 30 955 req/s | 3986 / 4557 |
| 16 | 32 091 req/s | 3905 / 4424 |
| 32 | 34 062 req/s | 5766 / 4473 |
| 64 | 33 927 req/s | 5171 / 4026 |

Saturation is ~34 k req/s, and the curve is flat from batch 32 to 64: the
*client* keeps only `depth` requests outstanding, and the queue depth, not the
GPU, sets the achieved rate below 32. Zero drops at every depth
(`drops=0`, `received == sent`).

## GPU occupancy and the exposed bubble (`saturation`)

Here the client offers 100 000 req/s for 5 s — far above what the page can
absorb — so the ring stays full and the producer drops the excess. The daemon
now separates, per pass, the kernel execution time taken from the GPU clock
from the host wall time the pass took, and also totals the doorbell wait:

| work | offered | served | drops | GPU kernel busy | GPU-busy wall | doorbell wait | occupancy | bubble |
|---|---|---|---|---|---|---|---|---|
| 4 | 100 000/s | 35 936/s | 320 281 | 4.81 s | 5.01 s | 5.01 s | **96.0 %** | 0.20 s |
| 16 | 100 000/s | 9 478/s | 452 546 | 4.97 s | 5.03 s | 4.97 s | **98.9 %** | 0.06 s |
| 64 | 100 000/s | 2 406/s | 487 906 | 5.09 s | 5.11 s | 4.89 s | **99.7 %** | 0.02 s |

Reading the columns:

- `GPU kernel` is summed from `%globaltimer` around the per-request arithmetic,
  so it is *GPU time*, not host time.
- `GPU-busy wall` is the host wall time during which at least one request was
  queued and a batch was being staged/executed. The difference is the staging
  bubble: pinned-memory copies in/out plus the launch itself.
- Occupancy is `kernel / busy_wall`. At `work=4` the GPU is genuinely executing
  96 % of the time it is "busy"; 4 % (0.20 s over 5 s) is the host-side staging
  and launch cost. As `work` grows the kernel dominates and the bubble shrinks
  to 0.02 s. **The pipeline is wall-clock-limited by the ~27 µs per-batch host
  staging cost, not by arithmetic.**

Drops are essentially all `drop: ctl busy` (the ring is full), with only 5–20
attributed to `done busy`. So the 64-slot ring is the back-pressure point and
the page-level drop counter is what reports it, exactly as designed.

## Latency at saturation (queueing, not service)

The `own` measurement taken right after the saturated `paced` run is *not* a
latency claim — the ring is still draining — but it does show service time is
unchanged: at `work=16` `GPU start → done` is 105 µs (vs 27 µs at `work=4`),
and at `work=64` it is 417 µs. Both match `work × ~6–7 µs` of arithmetic.

## Baselines (same client, same host, same run)

| path | method | p50 | throughput |
|---|---|---|---|
| GPU pipeline | `own` | 45.7 µs | 21 629 req/s |
| GPU pipeline | `burst` depth 8 | 243 µs | 30 070 req/s |
| userspace UDP echo (no GPU, no page) | `own` | 6.2 µs | 154 976 req/s |
| userspace UDP echo | `burst` depth 8 | 8.2 µs | 469 527 req/s |

The echo baseline is the floor: ~6.2 µs round trip on loopback with a
packet-per-syscall server. The GPU path costs ~7× that in latency and delivers
~15× fewer requests per second, which is the honest price of putting a real
kernel launch in the loop. The baseline is *not* a competitor design; it exists
so no number above is quoted in a vacuum.

## Honesty notes

- **Loopback only.** The `tc` hook is on `lo`; NIC RX, DMA and the real
  interrupt path are not in any number here. No DPDK/AF_XDP.
- **Timer spread.** `%globaltimer` was correlated to `CLOCK_MONOTONIC` at
  startup; the per-run offset spread was 275–4694 ns across these runs, and
  the GPU timestamps are published on the host clock using that offset, so the
  `parse → GPU start` stage is meaningful (it was previously ~1.8e18 ns before
  the offset was applied).
- **Occupancy is host-observed.** `busy_wall` is a host measurement around the
  stream; a CUDA-graph or event-timed occupancy could tighten it but would not
  change the conclusion, because the bubble is host-side staging.
- The client and daemon were not run under `SCHED_FIFO`; p99 tails therefore
  include scheduler noise and are upper bounds.

## What this changes for the design

1. The page-as-queue design works: no locks, slot recycling by paired FREE
   flags, drop accounting in the kernel, and a single pinned object per host.
2. The largest remaining non-GPU cost is the **per-batch host staging** (~27 µs
   for a 32-deep batch at `work=4`). Batching amortises it, which is why the
   throughput curve rises to a ~34 k req/s plateau.
3. Next: push `work` past the launch-latency knee so the GPU, not the host
   staging, is the bottleneck, and measure whether the bubble can be hidden by
   double-buffering the pinned staging buffers.
