# 0018: matched resident versus host-dispatch Qwen control

## Question and admission

The retained engineering goal requires "完成可复现正确性和匹配对照实验".
There is no paper RQ or evaluation contract in this repository. This is a
supporting mechanism experiment for that goal, not a newly invented paper RQ
or a complete serving evaluation. The question is whether removing host
request dispatch changes client-observed latency and executor-process CPU
cost when real model math and kernel networking are held constant.

Earlier HF/vLLM findings use different computation engines. They cannot
separate transport/dispatch from math. Reanalysis cannot supply the missing
matched-engine control. A full optimized-serving comparison is ultimately
more consequential, but this control resolves the immediate confound without
another large dependency installation on the crowded shared image filesystem.
A positive result permits only a local dispatch-policy benefit; a null,
contradictory or mixed result bounds that benefit. Every outcome leaves the
optimized-compute, ordinary-HTTP/AF_XDP/GPUNetIO and real-NIC comparisons open.

Hypothesis: the resident policy lowers mean client-observed TTFT relative to
host dispatch on at least some tested request lengths/concurrency conditions.
A difference interval crossing zero is inconclusive for that cell; a negative
host-minus-resident interval contradicts that expectation in that cell.
Neither result answers the whole project goal or establishes production
competitiveness. CPU work is a secondary mechanism measurement, not a veto
unless it invalidates the claimed scope.

## Matched implementation and fixed oracle

Both binaries compile the same `resident` device kernel, including a uniform
`once` argument. Default `build/qwen` launches it once and sleeps on the host.
`make qwen-control` builds `build/qwen_host_launch` with a compile-time host
control: busy-poll the same queue, launch the same cooperative grid once per
whole request and synchronize it. There is no added sleep, token-level host
launch, copy, host sampling or host network worker. This is a dispatch-policy
ablation, not an ordinary HTTP server or an external serving baseline.

Both use the same loaded Qwen2.5-0.5B-Instruct fp16 weights, scalar fp32 math,
fp16 boundaries, KV cache, mapped page, eBPF HTTP parser and kernel TCP TX.
Grid size is the discovered 170 SMs with 256 threads/CTA. Each binary checks
cooperative launch occupancy. `cuobjdump` inspection found identical device
SASS and resources: 96 registers, 32 stack bytes, 3,108 shared bytes. This is
comparison evidence, not an integrity/download/startup gate.

The fixed eager HF fp16 oracle is reused from `tests/resident_qwen.py`.
Both full regressions must pass 29 valid requests / 232 exact token IDs,
three rejections, eight concurrent clients, pipelining and 5,000 empty
connections. All measured requests must match that oracle too. The 64-token
failure from finding 0016 remains failed; this experiment uses output lengths
one and eight and cannot generalize beyond them. The host control has a
request-dispatch worker; it must not be labelled as the target resident path.

## Plan

- Five paired independent process repetitions, alternating mode order.
- Four balanced existing prompts; gen 1 and 8; closed-loop concurrency 1
  and 8; 64 measured requests/cell (16 per prompt). Concurrency is client
  queueing, not parallel sequence execution or continuous batching.
- Eight warmups/process (four prompts at each output length), excluded.
- Persistent token HTTP connections, one `sendall` per request, no byte sleeps.
  Connection/thread creation, model loading, warmup, GPU-state queries and
  teardown lie outside CPU and latency windows.
- Client `monotonic_ns`: TTFT from just before send to the first complete token;
  per-request TPOT `(last-first)/(gen-1)`, null for gen 1; completion latency
  and output-token throughput. Tokens completed in one receive share an
  arrival timestamp. These are client arrivals, not GPU instruction timings.
- Metric conventions follow [NVIDIA NIM benchmarking definitions](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html).
  The binary-token API requires the native adapter rather than an
  OpenAI-compatible GenAI-Perf client.
- `/proc/PID/stat` utime+stime delta measures aggregate executor-process CPU,
  including its threads; record tick resolution and a separate one-second
  idle window. No idle subtraction or total-host instructions/token claim.
  Kernel TX, softirq and unrelated host work are outside this CPU scope.
- Record GPU clocks/temperature/power before and after each cell. The effect
  includes polling, synchronization, kernel re-entry and GPU power behavior;
  do not call all observed difference CUDA launch overhead.
- Primary effect per gen/concurrency is mean TTFT's paired host-minus-resident
  difference across five process blocks, with Student-t two-sided 95% interval
  (df=4; [NIST critical-value table](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm)). It assumes approximately independent, normally distributed paired
  block means; five blocks offer limited power. Pooled p50/p99 over 320
  requests/cell/mode are descriptive and do not establish robust tail bounds.
- Preflight uses both real paths, fixed oracle, gen1/c1, four measured requests.
  Full completion requires every planned request/cell, both modes' launch-count
  evidence and clean teardown. Preserve failed outputs and deviations.

```sh
make probes tools qwen qwen-control
make -C module CC=gcc-15
HF_HOME=/workspaces/.cache/huggingface python3 tests/resident_qwen.py
HF_HOME=/workspaces/.cache/huggingface python3 tests/resident_qwen.py --executor ./build/qwen_host_launch
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --preflight --output bench/results/resident_dispatch_preflight_20261010.jsonl
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --output bench/results/resident_dispatch_20261010.jsonl
python3 bench/resident_dispatch.py --analyze --output bench/results/resident_dispatch_20261010.jsonl
```

The raw JSONL is ordinary per-request measurement output, with versions,
oracle inputs/outputs, cell CPU/time windows, GPU state and executor logs.
An assertion failure terminates the run without changing the oracle or
calling a partial prefix complete. The final table belongs here.

## Plan review

A fresh read-only reviewer inspected model, queue, tests, build and kernel TX
source before execution. Verdict: pass, no blocking scientific/executable
finding. It required shared device resources, strict output checks, mode-aware
launch-count evidence, client timing/coalescing definitions, CPU-scope limits
and separation of client concurrency from GPU batching. Those requirements
are included above. The reviewer explicitly scoped the effect to the combined
dispatch policy, not isolated launch cost or superiority over vLLM.

## Run and result review

Both strict regressions passed: [resident](../../bench/results/qwen_resident_dispatch_correctness_20261010.txt)
and [host launch](../../bench/results/qwen_host_launch_correctness_20261010.txt).
Each serves 29 valid requests / 232 exact token IDs and three rejection cases.
Recorded CUDA launch counts are one and 32, respectively. All executor threads
have no steady accept/receive/send calls; the host-launch control still has
a dispatch loop. [Device inspection](../../bench/results/qwen_dispatch_device_resources_20261010.txt)
confirms identical device instructions and resources.

The [real preflight](../../bench/results/resident_dispatch_preflight_20261010.jsonl)
completed both paths with four exact one-token requests per mode; its
[stdout](../../bench/results/resident_dispatch_preflight_20261010.txt) is retained.
Several persistent-stream requests have approximately 40 ms client latency
in both modes. This is an observation requiring interpretation, not an
isolated GPU-dispatch latency or a reason to change the fixed oracle.

The [first full attempt](../../bench/results/resident_dispatch_failed_20261010.jsonl)
failed with a client timeout during pair 1 / host-launch / gen1 / concurrency8;
[stdout and traceback](../../bench/results/resident_dispatch_failed_20261010.txt)
are retained. It is incomplete, not a performance result. The original runner
only wrote whole completed cells and did not capture the failing queue state,
so the cause is unknown. The runner now preserves completed requests from a
failed cell and records failure-time statistics before cleanup.

A [diagnostic repeat](../../bench/results/resident_dispatch_diagnostic_20261010.jsonl)
with temporary BPF print instrumentation on rejected reservations completed
all five pairs, 40 cells and 2,560 exact requests. No rejection trace was found;
the timeout was not reproduced. Its [stdout](../../bench/results/resident_dispatch_diagnostic_20261010.txt)
is retained as diagnostic evidence. The temporary BPF instrumentation was
removed before the final repeat; the ingress source is unchanged from the
published control commit. This does not establish that the timeout is repaired.

## Final measured result

The [uninstrumented raw run](../../bench/results/resident_dispatch_20261010.jsonl)
on source `28bcf9ead4c6e3f7de2ea29da1c749ae1cdc661e` completed all five pairs,
ten processes and 40 cells: 2,560 measured requests and 11,520 exact output
token IDs, plus excluded warmups. Each cell contains 64 unique indexes and
16 requests for each prompt. Each resident process launched once; each
host-dispatch process launched 264 times (eight warmups plus 256 requests).
All ten processes shut down normally, published 264 requests each, and had
zero registration failures or admission drops. [Stdout](../../bench/results/resident_dispatch_20261010.txt)
records the per-cell measurements and native analysis.

| Output / clients | Resident mean TTFT, ms | Host-dispatch mean TTFT, ms | Host minus resident, ms | Paired 95% t interval, ms |
|---|---:|---:|---:|---:|
| 1 / 1 | 40.6103 | 40.6058 | -0.0045 | [-0.1222, 0.1132] |
| 8 / 1 | 40.5369 | 40.5626 | 0.0258 | [-0.0979, 0.1494] |
| 1 / 8 | 80.7184 | 80.5873 | -0.1311 | [-0.6564, 0.3942] |
| 8 / 8 | 214.4801 | 214.4443 | -0.0358 | [-0.8908, 0.8193] |

Every interval crosses zero. The result establishes neither a detected TTFT
advantage nor equivalence. These are four separate local comparisons; no
family-wide superiority is claimed. Five adjacent blocks on one shared GPU
provide limited statistical power and depend on the stated t assumptions.
Pooled p99 remains descriptive.

Across the twenty measured cells per mode, executor-process CPU time was
0.04 s over 38.660 s of windows for resident versus 38.73 s over 38.680 s
for host dispatch. The idle windows show approximately one CPU-second/second
for the busy host control versus no reported resident ticks. At the recorded
100 Hz resolution, near-zero readings are quantized: they are not exact zero
or a useful denominator for a savings ratio. The data show removal of this
specific busy host-dispatch process cost, not total host CPU, instructions,
energy or an optimized-server comparison. Kernel TX, softirq and client work
are excluded. GPU endpoint samples also differ: resident remains busy even
when polling; host dispatch can idle/downclock. This is part of the policy
effect and is not an integrated energy measurement.

For gen8, 315/320 single-client replies and 280/320 eight-client replies in
**each mode** deliver all tokens at the same recorded receive time. The resulting
near-zero client TPOT cannot describe model decode time. This coalescing and
the persistent-connection 40 ms plateau are the main competing transport
explanation, not a reason to relabel the TTFT null result as a launch benefit.

## Transport discriminator (separate diagnosis)

`HF_HOME=/workspaces/.cache/huggingface python3 bench/tcp_stream_trace.py`
reuses the same requests/oracle and passively records packet metadata for the
owned loopback port using AF_PACKET. It captures no arbitrary payloads.
[The default trace](../../bench/results/resident_tcp_packet_trace_20261010.txt)
shows a streaming first response (TTFT 10.209 ms; client TPOT 2.616 ms), then
three replies with TTFT 41.629, 40.950 and 40.764 ms and coalesced token bodies.
Their headers precede delayed ACKs; the full token body follows the ACK.
The [Linux Nagle test](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/net/ipv4/tcp_output.c)
and [40 ms minimum delayed-ACK constant](https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/include/net/tcp.h)
are consistent with this mechanism. Passive receive timestamps include
observer scheduling; this is not a direct GPU-ready timestamp.

A bounded test-local candidate set TCP_NODELAY on the bootstrap listener so
accepted sockets inherited it. It was compiled with native `make` into an OS
temporary directory, and the tracked Qwen source and default binaries were
restored/preserved before tracing. [Candidate trace](../../bench/results/resident_tcp_nodelay_diagnostic_20261010.txt):
all four replies match the same eight-token oracle, TTFT 10.241, 16.320,
10.389 and 4.615 ms, with streamed client TPOT 2.516..2.680 ms. This strengthens
the ACK/Nagle buffering diagnosis. Four requests are a discriminator, not a
new serving benchmark, a confidence interval or evidence of resident-policy
superiority. No TCP_NODELAY default or persistent infrastructure setting was
retained; the candidate build was removed after shutdown.

To reproduce that diagnostic candidate without retaining a source change:

```sh
HF_HOME=/workspaces/.cache/huggingface python3 - <<'PY'
from pathlib import Path
import subprocess, tempfile
source=Path('executor/qwen.cu')
original=source.read_text()
with tempfile.TemporaryDirectory(prefix='bpfusion-tcp-nodelay-') as build:
    try:
        candidate=original.replace('#include <netinet/in.h>', '#include <netinet/in.h>\n#include <netinet/tcp.h>')
        candidate=candidate.replace('    setsockopt(listener,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof(yes));',
            '    setsockopt(listener,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof(yes));\n    if (setsockopt(listener,IPPROTO_TCP,TCP_NODELAY,&yes,sizeof(yes))) return 1;')
        source.write_text(candidate)
        subprocess.run(['make', 'BUILD='+build, 'qwen'],check=True)
    finally:
        source.write_text(original)
    subprocess.run(['python3','bench/tcp_stream_trace.py','--executor',build+'/qwen'],check=True)
PY
```

## Fresh result review and remaining work

A different read-only reviewer inspected sources, both strict regressions,
raw data, negatives and diagnostics, and independently recomputed the metrics.
It confirmed matching device SASS/resources, all cell/request indexes, oracle
tokens, ordering and launch counts. No invalidating defect was found for the
local experiment. It required the CPU quantization/scope limits, coalesced
TPOT warning, GPU-power-policy context, unresolved timeout and statistical
assumptions reported above. The native protocol adapter and small shared-kernel
control were judged justified; no experiment-control framework is needed.

- Run status: final uninstrumented run valid/complete; first attempt incomplete.
- Tested hypothesis: inconclusive in every cell.
- Research value: supporting mechanism evidence.
- Paper impact: mechanism/workload boundary; no paper RQ or thesis verdict.
- Next decision: preserve the null latency result and test the transport
  discriminator in the same matched matrix before drawing a better-path claim.

The earlier timeout remains unexplained, not repaired by later successes.
The 64-token numerical failure, GPU text processing, batching, completion
interfaces/measurements, complete CPU accounting, optimized serving baselines
and real-NIC controls remain open. This experiment does not complete BPFusion.

## Matched transport follow-up: plan

The initial four-request TCP_NODELAY discriminator cannot answer whether
transport buffering hid a resident-versus-host-dispatch latency difference.
Reanalysis of the default run cannot recover token arrivals that TCP buffered.
This follow-up therefore repeats the same integrated matrix with TCP_NODELAY
on the bootstrap listener in **both** executors. It is supporting mechanism
evidence for the same retained engineering goal, not a new paper RQ, a serving
baseline or an independent research contribution. A stronger optimized-server
comparison remains necessary; first separating the observed 40 ms plateau
from dispatch makes that future comparison interpretable without installing
another large compute stack on the shared filesystem.

The hypothesis remains that removing host request dispatch reduces mean
client-observed TTFT in at least some tested conditions. A positive interval
for host-minus-resident supports only this transport/dispatch boundary; a
negative interval contradicts that prediction for the cell; crossing zero
remains inconclusive. These outcomes determine whether the earlier transport
masking explanation plausibly changes the local dispatch result, not whether
BPFusion is a competitive service. Comparing this run against the older default
run is descriptive: transport settings are not randomized factorial blocks
and their numerical difference is not a causal transport effect estimate.

- Reuse the fixed independent HF oracle, four prompts, output lengths 1/8,
  client concurrency 1/8, 64 requests/cell, five paired process repetitions,
  alternating mode order and rotating matched cell order, exactly as above.
- Native make builds both candidate binaries from the same temporarily edited
  Qwen source into one OS temporary directory. The only candidate source delta
  adds `netinet/tcp.h` and a checked listener `TCP_NODELAY=1` call. Restore the
  tracked source immediately after building; preserve default binaries. No
  runtime setting or infrastructure configuration is retained after testing.
- Confirm candidate device SASS and resources agree with each other and the
  defaults. Run both full strict regressions with the original oracle and
  rejection/churn/trace checks. Then run the real two-mode preflight.
- The benchmark's executor-path arguments are only a native binary adapter;
  defaults, model, parser, queue, kernel TX, warmups, timeouts, measurement and
  analysis are unchanged. Raw metadata records both executable paths.
- Use the same client TTFT, TPOT, throughput and executor-process CPU definitions
  and paired 95% t intervals. Quantized CPU, power-policy differences, serial
  client queueing, limited repetitions and local-loopback scope still apply.
- Inspect per-token arrivals and a passive trace to check whether the plateau
  and coalescing persist. Their disappearance does not measure GPU-ready time.
- Preserve all failures and the earlier unexplained timeout. Stop only at the
  normal terminal status; partial output is not a complete matrix. Remove the
  owned candidate build after the completed run and diagnostic shutdown.

After setting `candidate` to the native make output directory, run:

```sh
HF_HOME=/workspaces/.cache/huggingface python3 tests/resident_qwen.py --executor "$candidate/qwen"
HF_HOME=/workspaces/.cache/huggingface python3 tests/resident_qwen.py --executor "$candidate/qwen_host_launch"
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --preflight --resident-executor "$candidate/qwen" --host-executor "$candidate/qwen_host_launch" --output bench/results/resident_dispatch_nodelay_preflight_20261010.jsonl
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --resident-executor "$candidate/qwen" --host-executor "$candidate/qwen_host_launch" --output bench/results/resident_dispatch_nodelay_20261010.jsonl
python3 bench/resident_dispatch.py --analyze --output bench/results/resident_dispatch_nodelay_20261010.jsonl
```

The full run must contain all forty cells, 2,560 exact requests, ten normal
executor shutdowns, and the same per-process launch counts 1/264. Five-pair
intervals are local estimates under the same assumptions; no practical
equivalence, robust-tail or complete-host-cost claim is planned.

### Follow-up plan review and candidate provenance

The read-only plan reviewer passed the follow-up without an invalidating
scientific or executable defect. It independently confirmed that the adapter
leaves the fixed oracle, workload, timeouts, warmups, repetitions, cell order
and analysis unchanged. Required interpretation limits are cell-specific
intervals, no causal transport effect from comparing sequential runs, client
arrival rather than GPU timing, and the previously recorded CPU/power/serial
execution limitations.

The candidate native build was:

```sh
make BUILD=/tmp/bpfusion-dispatch-nodelay-l_mibt7t qwen qwen-control
```

Relative to `1e30e76`, the temporary `executor/qwen.cu` edit added only
`#include <netinet/tcp.h>` and, after listener `SO_REUSEADDR`:

```cpp
if (setsockopt(listener,IPPROTO_TCP,TCP_NODELAY,&yes,sizeof(yes))) { perror("TCP_NODELAY"); return 1; }
```

Source was restored immediately after both native builds, before regressions.
[Four-binary resource inspection](../../bench/results/qwen_nodelay_device_resources_20261010.txt)
confirms device SASS equality for both candidates and both preserved defaults:
96 registers, 32 stack bytes and 3,108 shared bytes. The path is disposable;
the source delta and native build command above reproduce the candidates.

Both candidate strict regressions passed: 29 valid requests / 232 exact tokens
and three rejections in each mode, 5,000 empty connections, eight concurrent
clients, six pipelined replies/ring wrap/half-close, continued correct service
after invalid inputs, and all-thread network tracing with no accept/read/send
after ready. Launch counts are 1 for resident and 32 for host dispatch.
[Resident regression](../../bench/results/qwen_nodelay_resident_correctness_20261010.txt)
and [host regression](../../bench/results/qwen_nodelay_host_launch_correctness_20261010.txt)
retain the complete native output. The [real preflight](../../bench/results/resident_dispatch_nodelay_preflight_20261010.jsonl)
passed both paths with four exact one-token replies per mode; mean TTFT was
10.339 ms resident and 10.294 ms host. These eight requests are setup evidence,
not a performance result. Preflight metadata records base `1e30e76` plus the
uncommitted path adapter and temporary candidate source delta documented above;
the full matrix starts after the adapter/plan checkpoint commit.
