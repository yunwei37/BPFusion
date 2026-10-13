# Optimized stock TCP: matched delivery and worker CPU

The completed local comparison does not establish stock io_uring superiority
over the efficient native transport. Qwen's eight-client long-output throughput
is lower in the nominal paired estimate; both TTFT primaries and Smol's
throughput remain inconclusive. Stock also uses substantially more measured
known-worker CPU. Removing the userspace request proxy does not remove the
kernel polling cost.

[Plan](../../bench/results/vllm_uring_performance_20261013/plan.md) and
[two-round fresh plan review](../../bench/results/vllm_uring_performance_20261013/plan-review.md)
retain finding0035's local ordinary-serving question, leaving finding0029's
cross-node question unchanged. The stock integration is a changed mechanism,
not another unchanged module/native run. Role supporting; no formal paper RQ,
external SOTA, general-backend or syscall-only causal claim follows.

## Same backend, three mechanisms

Frozen main e7092937534c1dea8cb163fcb817d09ad2b33597 uses unchanged upstream
vLLM0.31.0 graphs/head/greedy selection, FP16, checkpoint revisions, KV budget,
packed prefill and FIFO-prefix model release. Original RTX5090/kernel7.3rc3
Workspace and temporary Torch2.13.0+cu129/Transformers5.17.0 runtime are reused.

Stock GPU-owned SQPOLL/NO_MMAP TCP is the candidate. Efficient native timed
epoll/nonblocking TCP is the main matched mechanism alternative, not an
official external-framework server. Existing bfusion_tx is a component control.
All use the same token-ID HTTP, inputs/client and default transport policies.
Stock additionally runs a GPU network-control block and has different queue/
submission/completion behavior; matching arithmetic does not match available
GPU resources or isolate polling as an exclusive cause.

The pre-performance whole-sequence reference sets freeze from independently
qualified histories before observing these outputs: Qwen17 keys/22 complete
sequences,Smol17/19. Every actual reply matches one whole sequence for its exact
prompt/gen. No tokenwise union, tolerance, teacher forcing, exclusions or
post-observation expansion. This finite-set qualification is weaker than
replay of the current unobserved ordinary batch/KV trajectory. Source compute
is unchanged, but actual arrival/batch/FP16 trajectories can differ.

## Complete run and controls

Real Qwen preflight completes three transports/12 cells/120 requests/3144
tokens including24 warmups. Six ordinary strict executors complete3732 requests,
133344 valid tokens,1554 intentional rejects and30000 empty connections.
Fragmentation, prompt/block edges, concurrency1..8, wrap/reuse, unchanged mixed
pacing, pipeline/half-close, binary/HTTP rejection and helper-thread SIGTERM pass.
All native network/wake syscall checks, terminal ownership and stock counters
pass. Earlier finding0041's failed strict attempt remains separate.

Full timing completes36 executors,144 cells,9216 measured requests and299520
measured tokens, plus288 checked gen1 warmups excluded from timing. Both models
finish all18 executors/72 cells and analysis0, without failed/excluded/retried
timing cells. All six transport permutations occur once/model; cell rotation
matches the plan in each block. Six process blocks are paired units, not
pooled requests. Ordinary binaries have no BF_TRACE.

[Fresh independent result review](../../bench/results/vllm_uring_performance_20261013/result-review.md)
reconstructs raw coverage, schedules, complete-reference membership, timings,
CPU deltas and paired effects, finding no result-invalidating defect. BF_TRACE
off removes model tracing; stock still writes its first128 IoRecord entries
and aggregate diagnostics. These are measured hot-path implementation costs,
so this is not a comparison free of all instrumentation.

## Primary client results

TTFT is client first complete-token arrival minus send start. Throughput is
all cell output tokens over first send to last arrival. Initialization and
connection setup are outside those timers. Client TCP/coalescing remains
included. See [official vLLM client](https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py).

| Model | Primary | Stock io_uring | Efficient native | Module component control |
|---|---|---:|---:|---:|
| Qwen | gen1/c1 mean TTFT,ms |1.406185|1.365673|1.396491|
| Smol | gen1/c1 mean TTFT,ms |1.085011|1.166208|1.142984|
| Qwen | gen64/c8 output tokens/s |4547.287626|4702.740966|4675.092299|
| Smol | gen64/c8 output tokens/s |5374.508043|5444.230784|5438.512919|

| Model | Gain favoring stock over native | Mean | Nominal paired t95,df5 |
|---|---|---:|---|
| Qwen | TTFT reduction,ms |-0.040512|[-0.109705,0.028680]|
| Smol | TTFT reduction,ms |+0.081197|[-0.025390,0.187784]|
| Qwen | Throughput increase,tokens/s |-155.453340|[-289.449821,-21.456859]|
| Smol | Throughput increase,tokens/s |-69.722741|[-344.364089,204.918607]|

Report all four primaries. Qwen throughput contradicts the expected gain in
this scoped nominal comparison; the other three intervals contain zero.
Neither equivalence nor a familywide superiority test follows. Module effects,
other cells, TPOT, completion/quantiles and every block difference remain
secondary in complete raw analysis. Do not use nominal secondary effects
to replace the primary conclusion.

## Measured CPU cost and numerical boundary

CPU is the secondary known-worker quantity during the cell bracket divided by
requests: POSIX all-thread process CPU plus the separate module TX counter.
Actual /proc/PID/task observations show stock SQPOLL inside the server thread
group; count it once through process CPU. Connections are established before
the initial read, while close and other work until the final read can be inside.
RX/softirq/BPF/TCP elsewhere, clients and energy are excluded.

| gen64/c8 | Stock CPU ms/request | Native CPU ms/request | Module process / TX / sum,ms/request |
|---|---:|---:|---|
| Qwen |14.212284|0.442915|0.101057 /0.228078 /0.329135|
| Smol |12.040271|0.394414|0.088545 /0.210233 /0.298778|

Native-minus-stock CPU seconds/request is-0.013769369
[-0.014136608,-0.013402130] for Qwen and-0.011645856
[-0.012106541,-0.011185172] for Smol. Both are higher stock cost within this
counter scope, about32/31 times the native mean. Stock executor CPU is about
one CPU-second per second of its cell bracket, consistent with a continuously
active kernel poller. This is not total service CPU or exclusive per-thread
attribution, and no whole-machine energy or universal efficiency claim follows.

Matched-index complete outputs agree384/384 for gen1/c1 in both models.
For gen64/c8, stock/native whole-sequence agreement is350/384 Qwen and339/384
Smol. All replies nevertheless pass the fixed whole-sequence reference check.
Do not claim identical concurrent output/batch trajectories or task quality.

## Evidence, restoration and next decision

[Qwen complete raw](../../bench/results/vllm_uring_performance_20261013/qwen_transport_performance.jsonl),
[Qwen reconstruction](../../bench/results/vllm_uring_performance_20261013/qwen_transport_performance_analysis.stdout),
[Smol complete raw](../../bench/results/vllm_uring_performance_20261013/smol_transport_performance.jsonl)
and [Smol reconstruction](../../bench/results/vllm_uring_performance_20261013/smol_transport_performance_analysis.stdout)
retain all arrivals, counters, CPU components/read brackets, commands/source
revision, task identities, logs and differences. Frozen references, literal
pipelines and qualification records share that archive. Package/install/build
details remain linked from finding0041's archive for the same retained runtime.

The bounded kernel journal04:26:40→04:45:38UTC reads1400 lines with no listed
fault-pattern matches. That is not continuous isolation or absence of all
interference. Post-run has the original boot/base runtime/Coder processes,
Workspace UID Ready/zero restarts, no own model process/module/pins/GPU app.
[Final restoration](../../bench/results/vllm_uring_performance_20261013/final_restoration.json)
removes the owned temporary runtime and26 build outputs after review. No own
serving process/module/pins/GPU application remains; original base, boot,
Coder processes and tools/setup_env.sh are preserved.

Close this completed matrix with its negative/inconclusive performance result.
Keep the module default and optional stock path; porting successful TCP I/O
does not by itself deliver latency/CPU benefit. A read-only source audit finds
the stock SEND loop recopies all produced tokens on each incremental send,
including already sent prefixes. Removing that repeated work is a concrete
next transport optimization candidate, but its contribution to the measured
throughput loss is not established. Do not rerun unchanged conditions to seek
a favorable estimate, tune model arithmetic, or attribute backend speed to eBPF.
