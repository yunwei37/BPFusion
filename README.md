# BPFusion

Linux-native accelerator serving: an eBPF ingress hook feeds an mmap'able
kernel control page, a GPU executor (currently driven from a userspace daemon)
drains it, and a replying socket path puts the completions back on the wire.
There is no per-request control-plane work in userspace and no per-connection
server socket — the pinned page *is* the queue.

**Current scope:** the executor launches **one resident kernel** that spins on
the mmap'ed BPF page for the whole run — it reads `slots[]` and writes `done[]`
in place through a `cudaHostRegister(..., cudaHostRegisterMapped)` device alias.
There is **no per-request and no per-batch host control call**; the host only
drains the ingress doorbell and samples completions for histograms. The
remaining control plane is the ingress doorbell itself (a future
`bpf_send_signal`/kernel-side notify). Findings state exactly what is proven.

## What is built and measured today

End-to-end path, proven on loopback (`lo`):

```
client sendto  ->  tc/clsact ingress BPF  ->  pinned mmap page  ->
resident CUDA executor  ->  responder sendto  ->  client
```

- `bpf/fusion.bpf.c` — the ingress program: parses L2/L3/L4, takes a slot only
  when both the request slot and its completion slot are FREE, copies the
  payload, stamps the kernel timestamp, publishes, and rings the doorbell.
  Excess under overload is counted (`drops`, split into `ctl busy`/`done busy`).
- `executor/executor.cu` — the daemon: launches one resident kernel on the
  registered BPF page (no staging copies, no per-batch launch) plus a responder
  thread. It opens the pinned maps with `bpf_obj_get` and does **not** load the
  object.
- `tools/bpfusion_load.c` — `attach`/`detach`/`stats`. Owns the object lifetime
  and pins `/sys/fs/bpf/bpfusion_{ctl,stats,db}`. Run `attach` before the daemon.
- `tools/client.c` — `verify` (GPU vs CPU reference), `own` (latency), `burst`
  (pipelined throughput), `paced` (offered rate / drops).

Measured results, with the honest costs, are in:

- `docs/findings/0001-ingress-wake.md` — the kernel→userspace wakeup cost
- `docs/findings/0002-end-to-end-mlp.md` — packet→GPU→packet (superseded by 0003)
- `docs/findings/0003-direct-page-and-wakeup.md` — direct-page execution, the
  lost-wakeup bugs, 41 µs idle RTT, throughput vs batch depth (superseded by 0004)
- `docs/findings/0004-resident-kernel.md` — **current**: launch-once resident
  GPU kernel, ~28 k req/s, occupancy vs work, the `__ldcg`/L1-coherence pitfall

## Build

Requires clang/LLVM, libbpf + libelf + zlib, `tc` (iproute2), and CUDA `nvcc`.

```
make            # eBPF objects + userspace tools + GPU executor, into build/
```

## Run

```
./build/bpfusion_load attach lo          # pin maps, attach tc to lo ingress
./build/executor 30 4 8 6 7 0            # 30 s, work=4, batch=8, gpu_cpu=6, resp_cpu=7, idle=0
./build/client verify 0 0 39400 4
./build/client own 2000 0 39400 4
./build/client burst 500 8 39400 4
./build/bpfusion_load stats
./build/bpfusion_load detach lo
```

Benchmarks:

```
./bench/run_e2e.sh 30 4 8 6 7 0
./bench/run_batch_sweep.sh 4 "1 4 8 16 32 64"
./bench/run_saturation.sh "4 16 64" 32
```

Logs land in `bench/results/`.
