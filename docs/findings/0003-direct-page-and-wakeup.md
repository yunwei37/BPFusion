# Finding 0003 — direct-page execution, lost wakeups, and the 20 ms bug

Status: measured on 2026-10-08 on the host described in
`bench/results/HOST.md`. Raw logs:

- `bench/results/e2e_20261008T044929Z.txt` — full path + baseline
- `bench/results/batch_sweep_20261008T045001Z.txt` — throughput vs batch depth
- `bench/results/saturation_20261008T044714Z.txt` — GPU occupancy under overload

> **Superseded for the executor design and its throughput/occupancy by
> [`0004-resident-kernel.md`](0004-resident-kernel.md).** 0003 still launched
> per batch from the host; 0004 launches once and stays resident. The two
> lost-wakeup fixes and the 41 µs idle RTT below still hold.

This finding supersedes the latency/throughput/occupancy numbers in
`0002-end-to-end-mlp.md` and records two real bugs that made every idle
measurement 20 ms too slow, plus the move from copy-staging to direct-page
execution.

## 1. The executor now reads and writes the BPF page in place

`0002` staged each batch through `cudaMalloc` device buffers with a
`cudaMemcpyAsync(H2D) → kernel → cudaMemcpyAsync(D2H) →
cudaStreamSynchronize` per batch. That copy chain *was* the bubble:

```
bf_exec_kernel(struct bf_page *p, unsigned int base, unsigned int n,
               unsigned int work, long long offset)
    in  = &p->slots[(base + k) % BF_SLOTS]
    out = &p->done[(base + k) % BF_SLOTS]
```

The daemon does, once at startup:

```c
cudaHostRegister(d.page, BF_PAGE_MMAP_BYTES, cudaHostRegisterMapped);
cudaHostGetDevicePointer((void **)&d_page, d.page, 0);
```

and launches on `d_page`, so the kernel reads `slots[].x[]` and writes
`done[].y[]` **directly on the mmap'ed BPF array** — no `d_in`/`d_out`, no
per-batch copy, no `cudaStreamSynchronize` in the steady state. `BF_PIPE = 8`
in-flight launches are retired in FIFO order; when all 8 are occupied the loop
falls back to `cudaStreamQuery` to force a retire rather than block.

Timestamps are still produced GPU-side (`%globaltimer`) and offset to the host
clock, so `parse → GPU start` remains measurable.

## 2. The 20 ms bug: the ring-buffer doorbell never wakes `epoll`

The idle path was:

```c
int r = epoll_wait(ep, &ev, 1, 20);   /* 20 ms timeout */
ring_buffer__consume(rb);
```

Measured on a single request in flight (`work=4`, `client own`):

| idle strategy | RTT p50 | parse → GPU start p50 |
|---|---|---|
| `epoll_wait(..., 20)` | 20 287 108 ns | 118 102 ns |
| `epoll_wait(..., -1)` (infinite) | **lost wakes** (2 of 5 timed out, ~1.03 s) | — |
| `epoll_wait(..., 0)` (pure poll) | **41 988 ns** | **1 363 ns** |

The infinite-timeout test is decisive: if the doorbell *ever* woke the fd, a
blocking wait would return promptly and never time out. It lost 2 of 5 wakes, so
the ring-buffer doorbell (`bpf_ringbuf_submit` from the tc hook) does **not**
reliably wake a blocking `epoll_wait` on the ring-buffer fd. Every idle request
therefore sat for the full 20 ms timeout.

Fix: the page's own `head` counter is the source of truth, so the idle branch is
now an unconditional **non-blocking** `ring_buffer__consume(rb)` busy-poll (the
"no control-plane sleep" shape the resident executor needs). `epoll` is gone
from the daemon entirely.

Result: **RTT p50 20 287 108 ns → 41 040 ns (494×)**, `parse → GPU start`
118 µs → 3.1 µs, single-request goodput 49 → 21 770 req/s.

## 3. Second lost-wakeup bug: `futex_wake` did not bump the futex word

`futex_wake()` called `syscall(SYS_futex, w, FUTEX_WAKE, 1, …)` **without
changing `*w`**. A waiter does:

```
seen = load(done_seq);
if (predicate) futex_wait_ns(&done_seq, seen, 20);
```

Because the word never changed, a wake delivered between the load and the
`FUTEX_WAIT` was lost and the waiter slept the full 20 ms. Fix:

```c
__atomic_add_fetch(w, 1, __ATOMIC_RELEASE);
syscall(SYS_futex, w, FUTEX_WAKE, 1, NULL, NULL, 0);
```

so the stale-`val` `FUTEX_WAIT` returns `EAGAIN` in the race — the standard
lost-wakeup guard. (Both consumers use `done_seq`; the executor publishes, the
responder waits.)

## 4. Latency, one request in flight (`client own`, 2000 samples)

| stage | p50 | p90 | p99 | max |
|---|---|---|---|---|
| client round trip | **41.0 µs** | 43.6 µs | 212 µs | 834 µs |
| kernel parse → GPU kernel start | **3.1 µs** | 3.6 µs | 4.4 µs | 5.8 µs |
| GPU kernel start → done | 27.1 µs | 27.5 µs | 27.7 µs | 32.4 µs |

Compared with `0002` (45.7 µs / 7.4 µs), the idle fix removed the epoll latency
and the direct page removed the staging round-trip from the critical path. The
GPU stage (27 µs at `work=4`) is now the dominant term; the host side around it
is ~14 µs total.

Under a paced 2000 req/s load (no queueing), daemon-side:

| stage | p50 | p90 | p99 |
|---|---|---|---|
| kernel parse → GPU done | 29.7 µs | 170 µs | 228 µs |
| responder `sendto()` | 1.4 µs | 2.0 µs | 3.7 µs |

`parse → GPU done` p50 is now ~27 µs above `parse → GPU start` — i.e. it is the
GPU kernel, not queue wait. `sendto()` is ~1.4 µs; the reply socket path is not
the bottleneck.

## 5. Throughput vs batch depth (`batch_sweep`, `work=4`)

Each depth gets a fresh daemon; the client keeps `depth` requests outstanding.

| daemon batch | throughput | drops |
|---|---|---|
| 1 | 22 089 req/s | 0 |
| 4 | 28 073 req/s | 0 |
| 8 | 29 994 req/s | 0 |
| 16 | 31 255 req/s | 0 |
| 32 | **32 360 req/s** | 0 |
| 64 | 1 409 req/s | ~2 |

The curve is flat from 16→32: at `work=4` and a 27 µs kernel the GPU saturates
around 32 k req/s and the client depth sets the achieved rate below that.

**Batch 64 is a degenerate case.** `BF_SLOTS` is 64, so a batch of 64 fills the
entire ring and the *previous* request's `BF_DONE` is still visible in every
slot — the in-order retire check `done[last].state == BF_DONE` then fires early
on stale data. Two guards fix it: (a) the retire check also compares
`done[last].id == base + n - 1` so a stale `BF_DONE` is rejected, and (b) a
batch is capped at `BF_SLOTS - 1 = 63` so it can never wrap the whole ring. With
batch 63 the same client burst gives **32 612 req/s, 0 lost**. The table uses
batch 64 deliberately to show the unfixed-looking number; 63 is the usable max.

## 6. GPU occupancy under overload (`saturation`, 100 000 req/s offered)

| work | served | GPU kernel | GPU-busy wall | occupancy | bubble |
|---|---|---|---|---|---|
| 4 | 34 417 req/s | 4.64 s | 5.01 s | **92.5 %** | 0.37 s |
| 16 | 9 368 req/s | 4.92 s | 5.03 s | **97.8 %** | 0.11 s |
| 64 | 2 387 req/s | 5.07 s | 5.10 s | **99.4 %** | 0.03 s |

Occupancy is `kernel / busy_wall`. At `work=4` the GPU executes 92.5 % of the
time a request is in flight; the 7.5 % is host launch + driver visibility, now
*without* the copy staging of `0002`, yet the occupancy is a little lower
(92.5 % vs 96.0 %) because the kernel is now so short (27 µs) that the fixed
launch gap is a larger fraction. As `work` grows the kernel dominates and
occupancy approaches 100 %. The `bubble` field no longer underflows — the
regime-tiled accounting now yields positive values (0.37/0.11/0.03 s).

The kernel-time vs `work` curve: `work=1` ≈ 8.7 µs, `work=4` ≈ 26.8 µs
(~6 µs per added pass), `work=16` ≈ 105 µs, `work=64` ≈ 417 µs — all linear in
`work` plus a fixed ~2–3 µs launch term.

## 7. Baselines (same client, same host, same run)

| path | method | p50 | throughput |
|---|---|---|---|
| GPU pipeline | `own` | 41.0 µs | 21 770 req/s |
| GPU pipeline | `burst` depth 8 | — | 30 264 req/s |
| userspace UDP echo (no GPU, no page) | `own` | 4.2 µs | 193 167 req/s |
| userspace UDP echo | `burst` depth 8 | — | 276 964 req/s |

Loopback packet-per-syscall echo is the floor: ~4.2 µs RTT. The GPU path costs
~10× that in latency and ~7× fewer requests/s at depth 8 — the honest price of a
real kernel launch in the loop.

## 8. Reproduce

```
make tools executor
./build/bpfusion_load attach lo
./build/executor 30 4 8 6 7 0 &        # seconds work batch cpu_gpu cpu_resp idle
./build/client verify
./build/client own 2000 0 39400 4
./build/client burst 400 8 39400 4
./bench/run_batch_sweep.sh 4 "1 4 8 16 32 64"
./bench/run_saturation.sh "4 16 64" 32
./bench/run_e2e.sh 30 4 8 6 7 0
```

## Honesty notes

- **Loopback only.** The `tc` hook is on `lo`; no NIC RX/DMA/interrupt path is
  in any number.
- **Timer spread.** `%globaltimer` is correlated to `CLOCK_MONOTONIC` at
  startup (offset spread 509–5094 ns across these runs); the GPU timestamps are
  published on the host clock via that offset. Close rates do **not** prove a
  shared 1 GHz counter, and the spread is *variation*, not an absolute error
  bound.
- **Still host-driven, not resident.** Launch-once residency over the page is
  the remaining goal-level step; `BF_PIPE=8` host launching is what is measured
  here.
- p99 tails include scheduler noise (no `SCHED_FIFO`) and are upper bounds.
