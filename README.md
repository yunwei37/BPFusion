# BPFusion

A Linux-native accelerator serving path: an eBPF ingress hook feeds an
mmap'able kernel control page, a **resident GPU executor** drains it, and a
socket path puts completions back on the wire. The target is a request path with
no per-request control-plane work in userspace: eBPF handles requests directly,
and userspace only bootstraps/loads/inits/controls.

This repository is the measured, iterative path toward that target. It is **not**
there yet; each [finding](docs/findings) states exactly what is proven and what
is not.

## Project status

Execution paths are built today at different maturity. Keep them
separate when reading any result:

| path | request model | GPU execution | reply | maturity |
|---|---|---|---|---|
| **Synthetic MLP** — [`executor/executor.cu`](executor/executor.cu) | UDP `:39400` -> tc/clsact ingress -> page | **one resident CUDA kernel**, launched once, spins on the page; no per-request/per-batch host launch or control call | userspace responder `sendto()` per reply | reference/intermediate: proves the resident-kernel + page mechanism (not yet a no-userspace-worker path) |
| **Real LLM** — [`executor/llm_executor.py`](executor/llm_executor.py) | UDP `:39402` or TCP `:39403` -> tc ingress -> token ring | **host Python + HF `transformers`** on Qwen (prefill + batch-1 decode); prefill/decode run on the GPU, but host code drives every step | UDP: client polls `produced`; TCP: `send()` on the accepted socket | host-driven baseline, labelled as such; this is where TTFT/TPOT evidence comes from |
| **Resident Qwen reference** — [`executor/qwen.cu`](executor/qwen.cu) | TCP token IDs -> tc ingress -> page | **one resident CUDA kernel** executes real prefill/decode/KV/argmax | kernel TCP TX | correctness reference: 12 requests/96 tokens agree with eager HF; one CTA, sequential token protocol, kernel accept/drain |

In the synthetic MLP path the no-userspace-worker property covers only GPU
compute; even there a userspace responder thread still `sendto()`s every
reply and the TCP/HTTP reply is not yet a kernel TX. The **real Qwen TCP path is
a host worker**: the Python executor accepts connections, runs HF decode, and
sends tokens — it is the current baseline, not the final closed loop.

An experimental kernel TCP TX path now passes exact-token correctness controls:
`module/bfusion_tx.c` watches the same map as ingress and sends on a referenced
TCP socket. HF still drives inference and accepts connections; this is another
intermediate, not the no-userspace-worker goal. See [finding 0012](docs/findings/0012-kernel-tcp-tx.md).

The resident Qwen reference now proves token-ID TCP -> resident real model
-> kernel TCP replies on sequential loopback requests ([0013](docs/findings/0013-resident-qwen.md)).
The full goal still needs `sockmap` framing, HTTP/text input, GPU-side
tokenize/detokenize, continuous batching and real-NIC measurement. See
[docs/architecture.md](docs/architecture.md) and the finding index below.

## Repository layout

```
bpf/fusion.bpf.c               ingress program (L2/L3/L4 parse, slot publish, doorbell)
bpf/include/bpfusion_queue.h   canonical kernel<->GPU page layout (single source of truth)
executor/executor.cu           resident synthetic-MLP CUDA kernel + responder + latency sampling
executor/llm_executor.py       resident Qwen executor on the token ring (host HF driver; --tcp)
executor/cuda_timer.h          %globaltimer <-> CLOCK_MONOTONIC calibration
tools/bpfusion_load.c          attach/detach/stats; owns and pins the BPF maps
tools/client.c                 verify/own/burst/paced MLP client
tools/llm_*.py, tools/perfcount.c, tools/insn_token.py   LLM + CPU-cost benches
bench/run_*.sh                 reproducible benchmark drivers (logs land in bench/results/)
docs/                          architecture.md + findings/NNNN-*.md
```

## Build

Requirements: Linux with BTF/libbpf, `clang`/LLVM (BPF target), `libbpf` +
`libelf` + `zlib` development headers, `tc` (iproute2), Python 3 with `torch` +
`transformers` (LLM path), and CUDA `nvcc` (executor). Root — or `CAP_BPF` +
`CAP_NET_ADMIN` — is required to load BPF programs and attach tc.

```
make            # eBPF objects + userspace tools + GPU executor into build/  (= probes tools executor)
make probes     # eBPF objects only
make tools      # userspace C tools only
make executor   # CUDA executor only
```

The executor is compiled for `SM_ARCH` (default `sm_120`); override for other
GPUs, e.g. `make executor SM_ARCH=sm_90`. This tree is verified on one RTX 5090
(32 GB, `sm_120`) with CUDA 13; the exact host is recorded in
[bench/results/HOST.md](bench/results/HOST.md).

## Run

The bench drivers in `bench/run_*.sh` are the reproducible entry points: each
synchronizes on the executor's ready line, runs the client, prints the
page/BPF counters, and writes a timestamped raw log to `bench/results/`.

Resident synthetic-MLP path (loopback), or `./bench/run_e2e.sh 30 4 8 6 7 0` for
the same run plus the plain-userspace UDP baseline:

```
./build/bpfusion_load attach lo     # pin maps, attach tc to lo ingress (do NOT pre-attach before a bench script)
./build/executor 30 4 8 6 7 0 &     # 30 s; work=4 batch=8 gpu_cpu=6 resp_cpu=7 idle=0(futex)
sleep 1
./build/client verify 0 0 39400 4   # numeric agreement with the CPU reference
./build/client own 2000 0 39400 4   # one-request latency
./build/client burst 500 8 39400 4  # pipelined throughput
./build/bpfusion_load stats         # read counters
wait
./build/bpfusion_load detach lo
```

Real-LLM path: use `./bench/run_llm.sh` (UDP page path) or
`./bench/run_llm_tcp.sh` (TCP reply socket) — both do the attach, wait for the
executor's `model loaded` line (model load takes tens of seconds), run the
baseline comparison, and detach. `llm_executor.py` needs the Python environment
that has `torch` + `transformers`; it attaches to the already-pinned page and
does not load the BPF object.

To drive it by hand instead: `tools/llm_bench.py` does `from llm_executor
import ...`, so the executor directory must be importable (`PYTHONPATH=executor`
from the repo root; the bench drivers already set this). Start the executor,
wait for `model loaded`, run the client, then stop the executor and detach:

```
./build/bpfusion_load attach lo
PYTHONPATH=executor python3 executor/llm_executor.py --seconds 90 & exec=$!   # model load ~tens of seconds
# wait for "executor: model loaded" on stdout, then:
PYTHONPATH=executor python3 tools/llm_bench.py --gen 32 --rounds 8    # --tcp + tools/llm_tcp_client.py for TCP
kill "$exec"; wait "$exec" 2>/dev/null    # stop only this executor
./build/bpfusion_load detach lo
```

## Reproducible benchmarks

Each driver runs an end-to-end scenario and writes a timestamped raw log to
`bench/results/`; the numbers in `docs/findings/` cite those logs.

```
./bench/run_e2e.sh 30 4 8 6 7 0                                  # MLP latency/throughput/drops
./bench/run_batch_sweep.sh 4 "1 4 8 16 32 64"                    # throughput vs batch depth
./bench/run_saturation.sh "4 16 64" 32                           # offered-load / SLO
./bench/run_ingress_latency.sh                                   # RX -> kernel -> userspace wake (PIN=1 to pin CPUs)
./bench/run_veth.sh 12                                           # over a real netdevice (two netns)
./bench/run_llm.sh 90 32 8                                       # LLM TTFT/TPOT (UDP page path)
./bench/run_llm_tcp.sh 70 32 6                                   # LLM over TCP reply socket
./bench/run_llm_model.sh Qwen/Qwen2.5-1.5B-Instruct 100 32 6     # matched model-size comparison
./bench/run_http.sh Qwen/Qwen2.5-0.5B-Instruct 32 8              # external vLLM HTTP baseline
```

The `run_*` scripts each `detach`/`attach` and clear stale pinned maps
(`/sys/fs/bpf/bpfusion_*`) themselves, and kill leftover executors first — run
them with privileges (`sudo -E` or `CAP_BPF`+`CAP_NET_ADMIN`) and do not
pre-attach. The MLP run also prints the `client verify` numeric check.

## Architecture and results index

- [docs/architecture.md](docs/architecture.md) — the data path, page ownership
  rules, memory-ordering rules, and the component map.
- [0001-ingress-wake.md](docs/findings/0001-ingress-wake.md) — kernel->userspace
  wakeup cost (spin vs `epoll_wait` vs blocking `recvfrom`), plus the pinning
  control experiment.
- [0002-end-to-end-mlp.md](docs/findings/0002-end-to-end-mlp.md) — first
  packet->GPU->packet path (superseded by 0003).
- [0003-direct-page-and-wakeup.md](docs/findings/0003-direct-page-and-wakeup.md)
  — direct-page execution, the lost-wakeup bugs, 41 µs idle RTT (superseded by 0004).
- [0004-resident-kernel.md](docs/findings/0004-resident-kernel.md) — launch-once
  resident GPU kernel, throughput, occupancy vs work, the `__ldcg`/L1 pitfall.
- [0005-resident-llm.md](docs/findings/0005-resident-llm.md) — real
  Qwen2.5-0.5B on the packet->page->GPU->page path; TTFT/TPOT vs a direct
  in-process baseline.
- [0006-veth-netdevice.md](docs/findings/0006-veth-netdevice.md) — the same path
  over a real netdevice (veth across two netns), not loopback.
- [0007-concurrency-slo.md](docs/findings/0007-concurrency-slo.md) — concurrency
  sweep: token goodput flat, TTFT scales with queue depth (batch-1 executor).
- [0008-instructions-per-token.md](docs/findings/0008-instructions-per-token.md)
  — CPU instructions/token via `perf_event_open`: host Python is the CPU bottleneck.
- [0009-tcp-path.md](docs/findings/0009-tcp-path.md) — request in over TCP,
  tokens streamed back on the accepted socket (+2.6 ms TTFT, TPOT flat).
- [0010-model-size.md](docs/findings/0010-model-size.md) — matched 0.5B / 1.5B /
  Qwen3-1.7B comparison; path overhead is size-independent, decode scales
  sub-linearly.
- [0012-kernel-tcp-tx.md](docs/findings/0012-kernel-tcp-tx.md) — exact Qwen
  tokens returned by kernel TCP TX; lifecycle/reset tests; HF still drives inference.
- [0011-http-baseline.md](docs/findings/0011-http-baseline.md) — external vLLM
  HTTP server baseline on the same model: path overhead is within noise of
  in-process, the gap to vLLM is decode, not transport.

## Contributing

Development happens on `main`: commit validated work directly to `main` and push;
create no other branches.

- Exercise the surface you change (run the affected client/executor/bench) before
  committing; pure documentation changes need only the links/commands checked.
- Record measurements as a [docs/findings/NNNN-*.md](docs/findings) file that
  cites the raw log path it comes from, and state the proven scope and the
  honest limitations — never claim unmet numbers.
- Update this README and [docs/architecture.md](docs/architecture.md) in the same
  commit when components, commands, or proven scope change.
- Do not commit build artifacts (`build/` is ignored) or benchmark logs other
  than the ones a finding cites.

## License

Apache-2.0 — see [LICENSE](LICENSE). The separately loaded kernel module
`module/bfusion_tx.c` is GPL-2.0-only, as marked in its SPDX header; it uses
GPL-exported Linux TCP internals and does not link into the userspace objects.

The optional resident Qwen reference is built with `make qwen`; its export and
correctness commands are in [finding 0013](docs/findings/0013-resident-qwen.md).
