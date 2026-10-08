# Finding 0001 — ingress → userspace wakeup on this kernel

Status: measured on 2026-10-08, `bench/results/ingress_20261008T003403Z.txt`.

## Question

To drive a resident GPU executor from an eBPF request path, the kernel has to be
able to *wake a userspace thread* when a request is parsed. What does the only
programmable mechanism available today — a pollable BPF map — actually cost on
this host, and how does it compare with a kernel module's direct
`wake_up()`? Is the gap small enough that the "no control plane in the steady
state, but userspace runs the GPU" design is still worth building?

## Setup

- Socket filter (`SO_ATTACH_BPF`) on a loopback UDP socket records
  `(payload_timestamp, bpf_ktime_get_ns())` per packet into a
  `BPF_MAP_TYPE_RINGBUF` (`bpf/wake_probe.bpf.c`).
- The sender stamps `CLOCK_MONOTONIC` **inside the payload**, so pairing of
  send/record/wake is exact under loss, reordering or unread datagrams. The
  filter reads the payload at offset 8 (`bpf_skb_load_bytes`), which on this
  kernel is where the UDP header ends; offset 0 is the UDP header, not the
  payload. Recorded `load_ret=0` confirms the read.
- Two consumers: `epoll_wait()` on the ring-buffer map fd (the ordinary way to
  sleep on a pollable map) and a busy-wait `ring_buffer__consume()` spinner.
- Baseline: blocking `recvfrom()` on the same socket, timestamped on return.
- 20 000 packets per run, 50 µs spacing between sends, 3 repetitions.

## Results

| chain | p50 | p90 | p99 | max |
|---|---|---|---|---|
| sendto → BPF socket filter | 1.6–1.7 µs | 1.9 µs | 3.8–7.4 µs | 20–38 µs |
| BPF record → userspace, **busy-wait** | 110–124 ns | 132–168 ns | 204–229 ns | up to 170 µs |
| BPF record → userspace, **epoll_wait** | 2.4–2.5 µs | 5.2–5.4 µs | 135–149 µs | 422–877 µs |
| sendto → blocking `recvfrom()` (baseline) | 3.4–3.5 µs | 6.2–7.7 µs | 142–148 µs | 262 µs–1.6 ms |

Interpretation:

1. The BPF-record → userspace hop with a spinning consumer is ~150 ns p50
   (mean 140–220 ns). Once the consumer is running, the pollable map is a
   shared-memory handoff, not a syscall: `ring_buffer__consume()` reads the
   same pages the kernel wrote. This is the floor for a *userspace* executor
   woken by a pollable map.
2. `epoll_wait()` adds ~11–18× at p50 (2.4 µs vs 150 ns) because every record
   that arrives while the consumer is sleeping must wake a task. At 20 k
   packets / 50 µs spacing, one wakeup per packet is priced in; this is the
   realistic cost of the "sleep until a request lands" policy.
3. A full `sendto → recvfrom()` on loopback is ~3.4 µs p50 — the same order as
   the epoll path, so the ring buffer does not make the datapath cheaper, only
   more programmable (the filter can classify, and — see below — decide where
   the payload is dispatched).
4. The p99/max values of the *blocking* variants (135–150 µs) are
   placement/scheduling outliers, not queueing: the p99 of the spin variant is
   229 ns in the same window, and the busy-wait sender chain keeps a stable p50
   throughout (sender and consumer were not CPU-pinned during these runs).

## Why the busy-wait variant is a *measurement*, not a production path

A spinning consumer used 100 % of a core, and during the first attempt the main
thread's `nanosleep()` starved the spinner outright (100 µs–2 s wakeups). The
numbers are only trustworthy *after* the sampling loop was forced onto
`now_ns()` deadlines with the spinner owning the ring buffer.

## Consequence for the BPFusion design

A kernel module calling `wake_up()` on a wait-queue would cut the 2.4 µs p50 of
the epoll path to roughly a task-scheduler wakeup, but it needs a module load
and gives up the verifier-enforced programmability that is the point of the
project. The measured cost of staying programmable is ~2.4 µs per wakeup, and
only the *first* packet after an idle period pays it — a resident executor that
drains a batch per wake pays it once per batch, not once per request.

**Decision taken:** keep the pollable-map wakeup as the kernel↔userspace
handoff, make the userspace GPU executor resident, and (finding 0002) do not
poll per record at all — sleep on a futex that the executor itself bumps, and
never spin during steady state. The kernel-module `wake_up()` remains the
documented escape hatch if the measured GPU path turns out to be latency-bound
on this hop.

## Open items

- No CPU pinning/`SCHED_FIFO` used; the p99 outliers are therefore an upper
  bound on the "unmanaged host" case and will be re-measured with pinning
  before any headline claim.
- Loopback only: this measures the whole stack above the NIC, so the NIC RX
  contribution is *not* included. A real-NIC measurement is still owed.
