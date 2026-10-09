# Finding 0004 — launch-once resident GPU kernel (no per-request host control call)

Status: measured on 2026-10-08 on the host described in
`bench/results/HOST.md`. Raw logs:

- `bench/results/e2e_20261008T052618Z.txt` — full path + baseline
- `bench/results/batch_sweep_20261008T052722Z.txt` — throughput vs batch depth
- `bench/results/saturation_20261008T052650Z.txt` — GPU occupancy under overload

Supersedes `0003-direct-page-and-wakeup.md` for the executor design and its
throughput/occupancy numbers; the two lost-wakeup fixes and the 41 µs idle RTT
result still hold.

## What changed

`0003` still *launched per batch from the host* (`BF_PIPE = 8` in-flight
launches, `cudaStreamQuery` force-retire). That host launch loop **is** the
steady-state control-plane work the goal eliminates: one driver call per batch
on the request path. This finding removes it.

The executor now:

```c
__atomic_store_n(&page->stop_ns, deadline, __ATOMIC_RELEASE);
bf_exec_kernel<<<1, 32, 0, stream>>>(d_page, work, offset);   /* launched ONCE */
```

`bf_exec_kernel` spins on the registered page for the whole run and pulls one
request at a time itself:

```
while (!stop) {
    if (seen >= head) continue;              /* __ldcg, L1-bypassing */
    idx = seen % BF_SLOTS;
    if (slots[idx].state != PENDING) continue;    /* producer published */
    if (done[idx].state  != FREE)   continue;     /* responder recycled */
    compute(); write done[idx]; fence; done_seq++
}
```

The host does **no** per-request or per-batch GPU call. Its only steady-state
work is `ring_buffer__consume()` (drain the ingress doorbell) and sampling
`done_seq` for the latency histograms. `stop_ns` is a host `CLOCK_MONOTONIC`
deadline converted through the calibrated `%globaltimer` offset; the kernel
compares its own clock against it.

Two correctness details that cost real debugging time:

- **`__ldcg`/`__stcg`, not `volatile`.** Volatile loads still hit the SM's L1,
  which is *not* coherent with host memory, so the resident kernel spun forever
  on stale zeros — `served=0` with `head` climbing. Loads that observe host
  writes (`head`, `slots[].state`, `done[].state`, `x[]`) use `__ldcg`
  (gpu-scope, L1-bypassing); the kernel's own publications use `__stcg`.
- **`done[idx].state == BF_FREE` is the GPU's write-permission gate.** The GPU
  must not overwrite `done[idx]` while the responder is still reading it; it
  waits for the responder's recycle. The ctl slot is owned by the producer
  (`BF_PENDING`), the done slot by the responder until `BF_FREE`.

Also fixed: the `bpf/%.bpf.o` Makefile rule had no header dependency, so a page
layout change silently left the *BPF object* stale while the userspace tools
rebuilt — the ingress program then wrote at the old offsets and the daemon saw
garbage. The rule now depends on `bpf/include/bpfusion_queue.h`.

## Latency, one request in flight (`client own`, 2000 samples)

| stage | p50 | p90 | p99 | max |
|---|---|---|---|---|
| client round trip | **41.3 µs** | 43.4 µs | 175 µs | 818 µs |
| kernel parse → GPU kernel start | **2.5 µs** | 3.4 µs | 3.8 µs | 5.1 µs |
| GPU kernel start → done | **25.5 µs** | 26.3 µs | 26.6 µs | 26.8 µs |

Latency is unchanged from `0003` (41.0 µs / 3.1 µs): launching once does not
help single-request latency, it removes host CPU from the *sustained* path.
`parse → GPU start` is now 2.5 µs — the resident kernel notices a new `PENDING`
slot within one spin iteration.

Daemon-side under a paced 2000 req/s load:

| stage | p50 | p90 | p99 |
|---|---|---|---|
| kernel parse → GPU done | 27.7 µs | 191 µs | 258 µs |
| responder `sendto()` | 1.9 µs | 2.2 µs | 3.8 µs |

## Throughput vs batch depth (`batch_sweep`, `work=4`)

| daemon batch | throughput | note |
|---|---|---|
| 1 | 21 849 req/s | |
| 4 | 25 835 req/s | |
| 8 | 26 564 req/s | |
| 16 | 27 952 req/s | |
| 32 | **28 250 req/s** | |
| 64 | 1 447 req/s | client-side depth-64 ring wrap |

**`batch` is now ignored by the executor** — with no host launch to amortize,
there is nothing to batch; the resident kernel pulls one slot per spin. The
column still moves slightly (21.8 k → 28.3 k) because it changes the *client's*
outstanding depth, which sets the achieved rate. The resident plateau is
**~28 k req/s** vs ~32 k for the launch-per-batch `0003` design; the ~12 % is
the resident kernel's spin-loop polling cost. That is the honest price of
removing the host from the request path.

Batch 64 is the client's full-ring depth (unrelated to the daemon batch now);
its 1 447 req/s is a client-side measurement artifact, not a GPU one.

## GPU occupancy under overload (`saturation`, 100 000 req/s offered)

| work | served | GPU kernel | GPU-busy wall | occupancy | bubble |
|---|---|---|---|---|---|
| 4 | 29 281 req/s | 3.61 s | 5.01 s | **72.2 %** | 1.39 s |
| 16 | 9 284 req/s | 4.60 s | 5.03 s | **91.4 %** | 0.43 s |
| 64 | 2 477 req/s | 4.99 s | 5.11 s | **97.6 %** | 0.12 s |

Occupancy is `kernel / busy_wall`. At `work=4` it is now **72.2 %** — lower than
`0003`'s 92.5 % — because the ~27 µs kernel is short enough that the gap
between consecutive requests (ingress + doorbell-visible latency) is a large
fraction of it. As `work` grows the kernel dominates and occupancy climbs to
97.6 %. The shortfall is *request-arrival visibility*, not a host launch: the
GPU is idle only because no `PENDING` slot is visible yet.

## Baselines (same client, same host, same run)

| path | method | p50 | throughput |
|---|---|---|---|
| resident GPU pipeline | `own` | 41.3 µs | 22 286 req/s |
| resident GPU pipeline | `burst` depth 8 | — | 26 765 req/s |
| userspace UDP echo (no GPU, no page) | `own` | 7.0 µs | 125 455 req/s |
| userspace UDP echo | `burst` depth 8 | — | 416 983 req/s |

## Reproduce

```
make                      # rebuild the BPF object too (layout changed)
./build/bpfusion_load attach lo
./build/executor 30 4 8 6 7 0 &
./build/client verify
./build/client own 2000 0 39400 4
./bench/run_e2e.sh 30 4 8 6 7 0
./bench/run_batch_sweep.sh 4 "1 4 8 16 32 64"
./bench/run_saturation.sh "4 16 64" 32
```

## Honesty notes

- **Loopback only.** The `tc` hook is on `lo`; no NIC RX/DMA/interrupt path is
  in any number.
- **The resident kernel is tightly coupled to this host's page layout.** It is
  a hand-written cache-coherent spin over a registered host mapping, with
  `__ldcg`/`__stcg`; a UVA/host-memory ordering assumption made explicit.
- **The kernel spins on `stop_ns` even when idle**, consuming one SM's issue
  slots for the whole run. That is invisible in these single-tenant runs but is
  a real GPU-resource cost.
- **Timer spread.** `%globaltimer` correlated to `CLOCK_MONOTONIC` at startup
  (offset spread 888–3811 ns across these runs); close rates do not prove a
  shared 1 GHz counter.
- p99 tails include scheduler noise (no `SCHED_FIFO`) and are upper bounds.
