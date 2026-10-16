# BPFusion

GPU-driven serving over ordinary Linux TCP, with eBPF admission and reused GPU
model computation.

~~~text
TCP/HTTP -> eBPF framing/admission -> shared queue
         -> GPU model execution -> completion -> Linux TCP reply
~~~

Userspace loads weights, captures graphs and initializes the service. On the
kernel-owned paths it does not accept each request, launch each model step or
send each reply after startup. Linux networking, kernel workers and GPU I/O
control still consume resources:this is not a CPU-free server.

**Status: working research prototype on a qualified Linux/GPU stack.**
Two real checkpoints run through HF and upstream vLLM graph adapters.
A recent-kernel io_uring/eBPF path needs no custom TCP kernel module.
General eBPF latency/throughput superiority over efficient native TCP is
**not established**.

## Start here

[Getting started](docs/getting-started.md) covers dependencies, model download,
build, start, client, native comparison and cleanup. It uses the explicit
module-free vLLM target; the legacy module transport remains separate.
[Fresh-environment validation](bench/results/onboarding_20261016/) passes both
models/transports with real HTTP/TCP requests.

Tested stack:Linux 7.3-rc3, x86-64, RTX 5090(sm_120), CUDA toolkit 13.0, libbpf 1.6.3,
Python 3.12 and the [pinned Python environment](requirements.txt).
The BPF loop needs its recent io_uring BPF/BTF/UAPI interfaces.
Another GPU or simply a recent Linux version does not establish compatibility.
See the [host record](bench/results/HOST.md).

With the documented dependencies and environment active:

~~~sh
make build/fusion.bpf.o build/bpfusion_load \
  vllm-mixed-uring-loop vllm-mixed-user-network-wait
./build/bpfusion_load stream-uring-attach
./build/vllm_mixed_uring_loop Qwen/Qwen2.5-0.5B-Instruct 120
~~~

Wait for the ready line. In another terminal with the same Python environment:

~~~sh
python3 tools/llm_tcp_client.py --http --gen 32 --rounds 1
~~~

The client tokenizes text and decodes returned IDs. The server's HTTP body
contains binary token IDs, not JSON or an OpenAI API. The guide also covers
pinned model revisions, Smol and cleanup. The external-vLLM HTTP baseline
client is a different protocol.

## Supported scope

| Surface | Qualified scope |
|---|---|
| Models | Qwen2.5-0.5B-Instruct and SmolLM2-135M; Qwen/Llama architectures |
| Compute | Reused HF graphs or upstream vLLM graphs/head/sampling |
| Network | Binary TCP and Content-Length HTTP POST; streamed token-ID replies |
| GPU | Prefill, decode, model/KV progress and output publication |
| Linux | Framing, admission, asynchronous TCP and reclamation |
| Module-free path | Explicit HF/vLLM io_uring BPF-loop targets on the tested stack |
| Main competitor | Efficient native epoll TCP with the same resident GPU compute |
| Validation | Finite exact outputs/replay, fragmentation, concurrency, reuse, reject, half-close/reset/stop |

Default capacity is 8; input and output counts are each 1..64 tokens.
Explicit16-bank vLLM qualification uses a matching shared-page ABI and separate
builds. See [architecture](docs/architecture.md) and
[capacity evidence](docs/findings/0064-batch-capacity.md).

An experimental [opaque CUDA Graph adapter](docs/graph-backends.md) also runs
unchanged cuBLAS/cuFFT computation through both transports. It accepts fixed
input/output buffers and is separate from LLM generation; arbitrary-CUDA
plugin stability and compatibility are not established.

## Results and research meaning

The controlled question compares serving paths while keeping upstream model
computation matched. Native also retains GPU-controlled generation; it is not
forced into a Python per-token loop.

- [Optimized latency](docs/findings/0047-optimized-short-input-latency.md):
  most short-input time remains in the reused model region.
- [Capacity](docs/findings/0064-batch-capacity.md):more slots improve high-load
  delivery on both paths.
- [Mixed scheduling](docs/findings/0065-mixed-prefill-decode.md):the complete
  reviewed experiment improves mean generation time on both paths.
  General transport superiority is unproven; Qwen has an adverse tail-token
  result. [Ordinary integration](docs/findings/0068-mixed-source-integration.md)
  selects explicit mixed Make targets after default8 and cancellation validation;
  old homogeneous controls retain their semantics.
- [Tail-path diagnosis](docs/findings/0066-tail-path-diagnosis.md):the complete
  close-scan retest is inconclusive; the candidate is not adopted. The old tail
  gap does not reproduce even before modification, and process CPU is adverse
  versus native in this retest.
- [Official vLLM reference](docs/findings/0069-current-official-vllm.md):
  the finite whole-service comparison has mixed results. Persistent connections
  expose approximately40ms token-gap P99 in both own paths; no eBPF speedup or
  total-resource saving is established.
- [Opaque graph backend](docs/findings/0067-opaque-graph-backend.md):cuBLAS/cuFFT
  ordinary default8 numerical/lifecycle checks pass on both transports.
- [Fair native admission](docs/findings/0063-fair-native-admission.md):
  removing a native scheduling disadvantage weakens earlier apparent wins.
- [Kernel-loop coordination](docs/findings/0044-uring-bpf-loop.md):less known
  CPU work than SQPOLL does not imply less total CPU than efficient native TCP.

[Evaluation](docs/evaluation.md) links complete plans, failures, raw data, analyses
and reviews. [All findings](docs/findings/) retain the historical detail.
Process CPU, throughput, first-token latency, completion time and tail token gaps
answer different questions; an improvement in one does not imply all improve.

The useful target is a reusable Linux TCP service around existing GPU backends:
programmable admission, shared ownership, GPU-controlled execution and complete
connection/reply lifetimes without a steady userspace request worker.
Generic GPU networking, GPU-initiated I/O and megakernel compute have prior work;
none alone is claimed as new. Current evidence establishes a working
integration and shared scheduler improvements, not a general faster server.
See [related work](docs/background-related-work.md) and
[backend audit](docs/upstream-backends.md).

## Remaining work

- Broaden reliability and workload coverage beyond the finite default8
  mixed-scheduling protocol and partial-output cancellation checks.
- Measure complete service CPU, including kernel I/O, softirq and GPU polling/
  resource cost; process CPU alone is insufficient.
- Establish sustained remote offered-load/tail behavior with errors and client
  lag visible. Current finite runs do not prove production SLOs or isolation.
- Broaden the experimental fixed-shape graph boundary beyond the qualified
  cuBLAS/cuFFT cases before claiming arbitrary-model/kernel support.
- Extend kernel/hardware compatibility and longer-running reliability with real
  runs. Text/JSON APIs, TLS, long context and multi-GPU serving are not qualified.

These gaps do not justify repeating closed micro-optimizations or rewriting
model-specific attention/matrix kernels.

## Repository map

| Path | Purpose |
|---|---|
| bpf/ | Framing, admission, sockmap and io_uring BPF coordination |
| bpf/include/bpfusion_queue.h | Shared kernel/GPU ABI |
| executor/ | Reused compute adapters, resident dispatch and shared transport |
| tools/llm_tcp_client.py | Text-to-token TCP/HTTP demo |
| tools/bpfusion_load.c | Attach, stats and detach |
| module/ | Legacy TCP transport |
| tests/, bench/ | Correctness and controlled benchmarks |
| docs/findings/, bench/results/ | Findings and reproducible evidence |

Synthetic MLP, host-driven Python, handwritten Qwen and experimental variants
remain controls with their own evidence. Older bench/run_* scripts manage
hooks/pins and may terminate matching executors; read their lifecycle before
running alongside another service. The current walkthrough uses explicit
process and cleanup steps.

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
