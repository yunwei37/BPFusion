# BPFusion

BPFusion is a research prototype for eBPF-driven GPU serving over Linux TCP.
It studies whether a server can remove its steady userspace request worker
while reusing the same GPU model computation.

```
client TCP/HTTP -> eBPF framing/admission -> kernel/GPU shared queue
                -> resident GPU model execution -> kernel TCP reply
```

Userspace loads weights, captures model graphs and initializes the service.
After startup, the GPU controls inference and the kernel owns connection
handling, response transmission and recycling. Linux networking and the kernel
worker still consume CPU; this is not removal of all host CPU work.

## Project status

The current qualified path reuses Hugging Face FP16 model graphs for
Qwen2.5-0.5B-Instruct and SmolLM2-135M (Llama architecture). A persistent
device dispatcher advances up to eight private graph/KV banks and publishes
tokens without a steady userspace request worker.

The HTTP frontend accepts Content-Length POST requests with binary token-ID
bodies and returns token IDs. It is not yet a text/JSON or OpenAI-compatible
service. Arbitrary model/backend support, shared-weight tensor batching and
full-service CPU attribution remain open.

| Path | Compute/control | Network/reply | Role |
|---|---|---|---|
| `qwen_graph` | Reused HF graphs, GPU-controlled generation | eBPF admission, kernel accept/drain and TCP TX | Current worker-free prototype |
| `qwen_graph_user_network_wait` | Identical resident GPU computation | Efficient native userspace timed epoll and nonblocking send | Matched alternative mechanism |
| `qwen_graph_control` | Same graph banks, host resumes after requests | Same eBPF/kernel transport | Dispatch ablation |
| `qwen.cu`, Python HF and synthetic MLP paths | Earlier implementations with different maturity | See their individual findings | Historical references and controls |

Strict regressions cover output agreement, fragmented messages, concurrent
requests, connection reuse, pipelining, half-close, invalid inputs and queue
recycling. The [completed cross-node comparison](docs/findings/0029-cross-node-network.md)
uses a Raspberry Pi client and lab RTX 5090 server over the existing
flannel/Tailscale/Ethernet path. Its primary latency and throughput intervals
contain zero for both models; reliable superiority remains unproven.
[Evaluation status](docs/evaluation.md) links the plans, raw data and reviews.
The [short-input diagnosis](docs/findings/0030-short-input-latency.md) finds
that the existing captured model region occupies about 95%/92% of profiled
local TTFT for Smol/Qwen; even 2-token inputs traverse 1460/808 GPU kernels.
This guides backend reuse, without establishing an eBPF speedup.
The [official optimized-serving comparison](docs/findings/0031-optimized-serving.md)
finds lower single-request first-token time but much lower eight-client
long-output throughput, with different compute, outputs and wire interfaces.

## Service and compute boundary

The intended open-source boundary is a reusable serving path around existing
GPU backends: receive and admit requests, publish inputs, observe completion,
stream responses and reclaim resources. Backend adapters provide model
execution, input/output interpretation and their buffer lifetimes. Reusing a
megakernel or device-launchable captured graph are both valid compute routes.

The current implementation has qualified two LLM architectures, but its token
protocol and GPU generation dispatcher are still LLM-specific. It is not yet
an arbitrary-CUDA-kernel server. Linux kernel integration also remains a real
dependency; see the [architecture and upstream BPF socket boundary](docs/architecture.md#linux-kernel-dependency).

To attribute a latency difference to the serving path, keep the backend
revision, checkpoint, precision, KV layout and concurrency/batching identical
between the kernel/eBPF and efficient userspace paths. Model arithmetic
improvements belong to the backend and do not prove an eBPF benefit.

## Reusing upstream compute

Backend integration reuses upstream optimized computation so a matched
comparison can attribute effects to the Linux/eBPF serving path.
[Backend source audit](docs/upstream-backends.md) compares candidates and
records concrete model, launch, correctness and online-service boundaries.
No alternative megakernel is qualified yet; the measured executor remains in use.
[Official vLLM FULL-graph reuse](docs/findings/0031-optimized-serving.md#optimized-backend-integration-actual-full-graph-reuse)
passes1197 actual GPU launches at batch1/2/4/8 with bit-identical hidden states.
This qualifies the computation interface. The [GPU-owned decode follow-up](docs/findings/0031-optimized-serving.md#optimized-backend-integration-gpu-owned-decode-and-sampling)
then generates4662 tokens with official head/sampling and GPU metadata advancement,
matching74 frozen official sequences after CPU prefill. Prefill/admission and
kernel-queue integration remain unfinished; no optimized-serving speedup is claimed.
The existing HF graph interface now also accepts HF checkpoints/model directories.
[Qwen and Llama qualification](docs/findings/0023-batch-execution-qualification.md#hf-graph-reuse-across-qwen-and-llama-architectures)
passes both resident and host-control dispatch for Qwen2.5-0.5B and
SmolLM2-135M: 1340 valid requests and 81728 exact generated tokens in total.
This extends tested computation reuse without new model arithmetic; it does
not establish arbitrary-model support or a new serving-speed result.
The [MPK qualification](docs/findings/0023-batch-execution-qualification.md#upstream-mpk-sm120-compatibility-and-terminal-numerical-rejection)
records repaired native memory/synchronization faults and failed whole-model
outputs under both parallel and serial submission.
The [Plow qualification](docs/findings/0023-batch-execution-qualification.md#upstream-plow-sm120-build-and-mixed-numerical-qualification)
records successful SM120 builds and zero-error finite memchecks, with two of
four32-token sequences matching HF; it is not a qualified replacement.


## Repository layout

```
bpf/fusion.bpf.c               ingress program (L2/L3/L4 parse, slot publish, doorbell)
bpf/include/bpfusion_queue.h   canonical kernel<->GPU page layout (single source of truth)
executor/executor.cu           resident synthetic-MLP CUDA kernel + responder + latency sampling
executor/llm_executor.py       host HF Qwen baseline on the token ring (--tcp)
executor/qwen.cu               real Qwen reference in one resident CUDA kernel
executor/qwen_graph.py/.cu     HF bootstrap capture + GPU-tail graph dispatch
module/bfusion_tx.c            kernel accept/drain and asynchronous TCP/HTTP TX
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

For the qualified graph/TCP path on the recorded host:

```sh
make qwen-graph qwen-graph-user-network-wait
make -C module KDIR=/usr/src/linux-headers-7.3.0-070300rc3-generic CC=gcc-15
HF_HOME=/workspaces/.cache/huggingface python3 tests/resident_qwen.py --executor ./build/qwen_graph --gen 64 --prefill-edges
```

The module must be built against the running kernel's headers/compiler; the
path and compiler above describe the tested host. Use the same strict command
with `--executor ./build/qwen_graph_user_network_wait` for the native network
alternative, or add `--model HuggingFaceTB/SmolLM2-135M` for the second qualified
architecture. These tests check real model outputs and connection/queue
lifetimes; they do not establish a performance advantage.

The [cross-node plan](bench/results/physical_network_plan_20261011.md) and
[actual invocations](bench/results/physical_network_full_invocations_20261011.txt)
describe the completed matched experiment and temporary client lifecycle.
The older synthetic and Python-driven reference commands follow.


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
- [0013-resident-qwen.md](docs/findings/0013-resident-qwen.md) — real Qwen inference inside one resident kernel and kernel-owned connection lifecycle.
- [0014-sockmap-stream.md](docs/findings/0014-sockmap-stream.md) — TCP stream framing and concurrent queue reservation.
- [0015-http-token-transport.md](docs/findings/0015-http-token-transport.md) — Content-Length POST token API, persistent connection framing and ordered HTTP replies.
- [0016-cooperative-resident-qwen.md](docs/findings/0016-cooperative-resident-qwen.md) — one cooperative resident grid, strict short-output passes and an explicit longer-decode accuracy failure.
- [0019-device-scheduled-qwen.md](docs/findings/0019-device-scheduled-qwen.md) — GPU-driven HF graph execution with passing 64-token TCP/HTTP correctness and no userspace request worker.
- [0020-graph-dispatch.md](docs/findings/0020-graph-dispatch.md) — complete matched graph/64-token dispatch measurement; narrow TTFT evidence, serial queueing and executor-process CPU results.
- [0017-invalid-token-rejection.md](docs/findings/0017-invalid-token-rejection.md) — invalid model token IDs fail their request and leave subsequent inference live.
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

The optional resident Qwen reference is built with `make qwen`; its weight
export is in [finding 0013](docs/findings/0013-resident-qwen.md), and its current
TCP/HTTP correctness command is in [finding 0015](docs/findings/0015-http-token-transport.md).
