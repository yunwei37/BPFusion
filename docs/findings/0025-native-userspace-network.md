# 0025: native userspace network control with reused HF graphs

## Question and admission

The user retains the goal of a complete Linux TCP/HTTP + eBPF/shared queue
to resident real-model GPU inference and asynchronous kernel TX, and asks:
“性能能不能想办法改进一下. 尤其是 tp / lantency, 理论上应该可以做到很快”.
There is no paper RQ or thesis contract in this repository. The supporting
engineering question here is whether removing the userspace network worker
improves client latency or output throughput when computation and GPU control
are the same.

Finding0024 changes host/GPU request dispatch but uses eBPF and kernel TX in
both conditions. It cannot answer this network question. Reanalysis cannot
recover the absent userspace condition. The new control closes that gap with
a native nonblocking epoll reactor and the same resident GPU dispatcher,
rather than a Python HF per-token control or a different model kernel.

Planned role: supporting component ablation. There is no external main serving
baseline or SOTA claim. A positive effect would support the tested kernel
request/reply path; negative or mixed effects would bound its advantage and
direct optimization toward transport/completion overhead. Null intervals
would remain inconclusive, not equivalence. These outcomes change where
performance work goes without changing the full user goal.

The stronger eventual comparison is an optimized external serving engine
with compatible computation and a real NIC. Current alternative megakernels
lack strict qualification. The new exact-compute network control is the
strongest presently runnable discriminator. A first-token write-coalescing
optimization is also promising: historical packet traces support ACK/Nagle
buffering, and current default-TCP TTFT is often near40ms. This collection
keeps the current default protocol and sending behavior fixed to establish
the missing network comparison. It does not claim that these sending
patterns are optimal or that a buffering plateau is model compute time.

## Matched implementation and qualification

Both variants use executor/qwen_graph.py, identical FP16 weights and captured
HF forward/argmax graphs, eight private input/KV/output banks, and the exact
same dispatch device kernel. Both launch the resident service once; decode,
sampling, admission consumption and FIFO DONE publication stay on the GPU.

The kernel variant maps the eBPF page and uses the existing stream parser and
asynchronous kernel TX. The new BF_USER_NETWORK compile variant registers an
anonymous page of the identical ABI and runs a native epoll receive/publish/
send loop. It has no per-token model execution or CUDA launch on the host.
It deliberately busy-polls completion to avoid imposing a coarse sleep on
the latency control; its executor CPU cost must be reported. This is not a
claim that every optimized userspace server consumes a full core.

The reactor buffers split/coalesced requests, uses one active request per
connection, and queues further requests on that stream. This differs from
kernel pipeline admission, but the measured closed-loop workload has exactly
one outstanding request per connection in both conditions. Responses use the
same binary token-ID HTTP body and default server TCP settings; no NODELAY
or QUICKACK is set on either server. The client NODELAY setting is common.
Partial sends retain byte offsets, the last token waits for DONE, and FREE
is published only after complete response or disconnect plus GPU release.

The independent eager-FP16 oracle and existing full TCP/HTTP regression
qualify both models. The user control must pass335 valid requests/20432 exact
tokens,259 rejections,5000 empty connections, eight-client concurrency,
immediate reuse, mixed lengths, ring wrap, pipeline/half-close and helper-thread
shutdown. Its trace must contain host accept/receive/send and no kernel TX
module may be present. Native counts must show594 published/completed,
259 rejected,1 service launch,20432 model graphs,graph_error0,banks8,max_active8.
The kernel conditions have the committed final four-case qualification in
finding0023. No oracle, timeout or correctness relaxation is permitted.

## Workload, metrics and interpretation

Use Qwen/Qwen2.5-0.5B-Instruct and HuggingFaceTB/SmolLM2-135M (Llama), each
with its own eager-FP16 oracle for the four existing real text prompts.
Use the existing bench/resident_dispatch.py measurement path. Its model
and user-network executor arguments are adapters; historical defaults and
analysis remain available.

For each model, compare gen1/gen64 and closed-loop clients1/8,64 requests/cell,
five paired process blocks with alternating mode order and identical rotated
cell order within each pair. Each process has eight excluded warmups, four
prompts balanced16 times/cell and freshly captured banks. This is independent
batch1 graph concurrency, not shared-weight tensor batching.

[NVIDIA definitions](https://docs.nvidia.com/nim/benchmarking/llm/metrics)
supply client TTFT, TPOT excluding the first token, completion latency and
aggregate output TPS. Primary effects are userspace-minus-kernel TTFT for
gen1/one client, and kernel-minus-userspace TPS for gen64/eight clients.
Report both effects separately for each model; conflicting effects are mixed.
Report every cell and pair, with nominal two-sided paired t95 intervals
(df4; [NIST critical value](https://www.itl.nist.gov/div898/handbook/eda/section3/eda3672.htm)).
Intervals crossing zero are inconclusive. No familywise superiority, robust
P99, total CPU savings, energy, SOTA or real-NIC claim follows.

Connections/thread creation, model capture, warmups, GPU queries and cleanup
remain outside the measured windows. Client timestamps are monotonic; tokens
received in the same recv share their arrival time. Executor process CPU
covers the userspace reactor but excludes kernel TX/softirq in the kernel
condition. Global /proc/stat includes client and unrelated host work and is
only descriptive; it cannot establish service-attributed CPU savings.
Coarse GPU state is recorded, with the other SGLang workload preserved.
Shared-device timing and adjacent pairs limit inference.

## Execution and completion

Build make qwen-graph qwen-graph-user-network in the original Workspace/main.
Keep the same native source, model loader, oracle, request/shutdown timeouts
and default transport for preflight/full collection.

For each model, run the existing real preflight and full matrix:

```sh
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --gen 64 --preflight --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model HuggingFaceTB/SmolLM2-135M --output bench/results/userspace_network_smol_preflight_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --model HuggingFaceTB/SmolLM2-135M --output bench/results/userspace_network_smol_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --gen 64 --preflight --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --output bench/results/userspace_network_qwen_preflight_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --output bench/results/userspace_network_qwen_20261011.jsonl
python3 bench/resident_dispatch.py --analyze --output bench/results/userspace_network_smol_20261011.jsonl
python3 bench/resident_dispatch.py --analyze --output bench/results/userspace_network_qwen_20261011.jsonl
```

Preflight has four exact measured gen1 requests per mode and checked warmups;
it establishes executability only. Complete collection requires80 unique
cells,5120 measured requests,166400 exact measured tokens,20 normal executor
exits, ten complete model/pair blocks, balanced prompt/index coverage and no
excluded failed row. Each full process publishes/completes264 requests and
executes8580 model graphs, with1 service launch,banks8,max_active8,graph_error0.
Kernel stats must show no admission/registration failures and eight FREE
slots; user control native counters and zero rejection plus exact responses
verify its request completion. All owned modules/hooks/pins/processes must
be cleaned up. The raw/source/qualification receipts stay visible.

A fresh plan reviewer checks source fairness and executability before real
preflight. A fresh result reviewer independently reconstructs metrics,
reference tokens, counters, order, completion, failures and scope after full
collection. Reviews diagnose scientific defects, not operator permission.
The target table shows each model/cell/mode and all paired effects; a partial
collection is incomplete. Startup cost is roughly twenty eight-bank captures
plus the serving matrix on the shared device, not an investigation deadline.

## Engineering qualification and plan review

The [native control receipt](../../bench/results/userspace_graph_network_qualification_20261011.txt)
records both model regressions from06:44:26 through06:48:39UTC, each exit0:
335 valid requests,20432 exact tokens,259 rejects and5000 empty connections.
Both complete split writes, eight clients, immediate invalid-to-valid reuse,
mixed lengths, ring wrap, ordered pipeline, half-close and helper-thread
SIGTERM. Native transport counters record5058 accepted,594 published/completed
and259 rejected per process. The GPU reports1 service launch,20432 model graphs,
banks8,max_active8 andgraph_error0.

Independent CPU reconstruction verifies all78 printed64-token reference/actual
arrays, after-ready accept/receive/send activity, target helper-thread signals,
normal exits and cleanup. cuobjdump comparison finds identical dispatcher
SASS instruction/encoding lines between the existing kernel and user variants.
The two graphs are not independent model implementations; their computation
is deliberately reused. This is correctness evidence, not a serving-speed run.

The06:51:46UTC read-only host observation retains boot
04dc0087-5ccc-4c46-9997-b9a92f0e5167 and SGLang PID2762187 at18348MiB;
the journal read has no NVRM Xid since06:40UTC. Other-service residency is not
acceptance. Own qualification processes, module and map pins are absent.
The unrelated tools/setup_env.sh WIP remains untouched.

[Fresh independent plan review](../../bench/results/userspace_network_plan_review_20261011.md)
admits the complete comparison without a required repair. Its scope
clarification is retained: the user loop may send header/body in one busy
iteration, while kernel TX sends one part per poll and sleeps60--120us.
Effects therefore include completion polling and write grouping, not syscall
removal alone. The measured closed-loop workload matches one outstanding
request per connection. Finite small responses do not establish exhaustive
partial-send/backpressure robustness. No performance claim precedes complete
collection and independent result review.

## Real preflight

Both model preflights completed normally, SmolLM2 at06:56:19UTC and Qwen at
06:58:24UTC. Each records17 events, two cells, eight exact measured gen1
tokens and two checked executor exits. Each process also checks eight excluded
warmups and reports12 completed requests,264 model graph launches, one
resident service launch, eight banks and graph_error0. Kernel stats show zero
registration/parser/admission failures and all eight slots FREE; the user
control reports12 published/completed and zero rejections.

Independent reconstruction checks balanced prompt/index coverage, oracle
prefixes, client timestamp ordering, TTFT/completion, aggregate TPS and
descriptive host CPU arithmetic. All owned worker/module/map state is absent
afterward. These preflights establish executability only; they are not the
full paired performance experiment.

Raw [Smol JSONL](../../bench/results/userspace_network_smol_preflight_20261011.jsonl)
and [Qwen JSONL](../../bench/results/userspace_network_qwen_preflight_20261011.jsonl)
have accompanying stdout/source/command/exit receipts. Their metadata names
base HEAD3c320391; the preflight tested the then-uncommitted control patch.
Frozen benchmark source in stdout and the qualification/source receipt,
together with the subsequent control commit, make that distinction explicit.
The full matrix runs on committed source. No correctness or timeout change
was made between qualification and preflight.
