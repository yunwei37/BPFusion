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

Full measurement and fresh result review are pending. No performance conclusion
is established by this plan, preflight or correctness regressions.
