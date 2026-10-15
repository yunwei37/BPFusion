# Long-output GPU service-time diagnostic: incomplete decomposition

Observed2026-10-14/15 in the original yunwei356/bpfusion-dev Workspace on main
458145f495789f83ff662ec6d45b216c83ff7ae8. No serving source or default changes.
[Plan](../../bench/results/long_service_timeline_20261014/plan.md),
[plan review and both follow-ups](../../bench/results/long_service_timeline_20261014/plan-review.md),
[fresh result review](../../bench/results/long_service_timeline_20261014/result-review.md)
and [raw archive/replay](../../bench/results/long_service_timeline_20261014/)
retain the complete decision and failures.

## Question and outcome

Prior current-constructor and publication comparisons0055/0056 left a native
long-output gap without identifying actual model service time. This supporting
diagnostic asks whether GPU model kernels take longer, or execution trajectories
and intervals between rounds differ, while retaining identical reused vLLM
model arithmetic. No new formal paper RQ is invented.

Collection is complete:40 serving drivers and40 separately recorded fresh
unprofiled graph/KV/history replays exit0. Two models, five paired process
blocks, loop/native and profiled/unprofiled conditions deliver1280 measured
gen64/c8 requests81920 output tokens, plus320 checked gen1 warmups.

The planned integrated GPU decomposition is **invalid**: the fixed full
analyzer exits1 on missing activity records. Independent review finds18 of20
profiles complete; two Smol loop profiles each miss3 model kernels. All40
client/logical-trajectory checks remain valid within this instrumented finite
workload. Bottleneck interpretation remains **inconclusive**. Research value
is supporting; impact is a mechanism/workload boundary. A completed collection
and a passing client supplement do not constitute a repaired full-analysis pass.

## Matched serving and client results

Private source-native vllm_graph_uring_loop_trace and
vllm_graph_user_network_wait_trace reuse the same FP16 checkpoint, graph
computation, padding, prefix release, input/output budgets and dispatcher.
The loop uses eBPF sockmap/shared queue, resident GPU network progression and
upstream sleepable io_uring BPF coordination; the efficient native alternative
uses timed epoll_pwait2 and nonblocking TCP. Both use the existing60000ns timer.
This selected loop sends through Linux TCP without bfusion_tx; kernel/timer CPU
work remains. No per-request userspace worker does not mean zero host CPU.

All conditions retain BF_TRACE; “unprofiled” disables CUPTI activity profiling,
not logical tracing. These numbers cannot replace ordinary untraced0055/0056.
TPS means and loop-minus-native nominal paired t95df4 intervals:

| Model | Condition | Loop token/s | Native token/s | Signed difference [t95] |
|---|---|---:|---:|---|
| Qwen2.5-0.5B | BF_TRACE, unprofiled |4550.125|4675.792|-125.667 [-366.982,115.647]|
| SmolLM2-135M | BF_TRACE, unprofiled |5268.768|5267.119|+1.649 [-117.523,120.821]|
| Qwen2.5-0.5B | BF_TRACE, profiled |4503.765|4608.130|-104.366 [-149.564,-59.167]|
| SmolLM2-135M | BF_TRACE, profiled |5249.271|5243.563|+5.708 [-110.903,122.320]|

Only the profiled Qwen deficit has a signed interval here. All primary
unprofiled intervals cross zero; none establishes improvement or equivalence.
Client TTFT/completion contrasts also cross zero. Every signed block, TPOT,
latency outlier and profiler contrast is retained in result-review.md.
Profiler-minus-unprofiled intervals crossing zero do not prove zero overhead.

Smol measured rounds increase in every pair: unprofiled loop272.6/native261.0,
difference+11.6[0.861,22.339]; profiled268.2/258.8,+9.4[1.919,16.881].
Yet TPS effects have mixed signs. Round count alone does not establish the
throughput mechanism.

## What the GPU traces can establish

Smol loop/profiled p2 records113944 model activities versus113947 expected;
p4 records117217 versus117220. Their graph memcpy counts match271/271 and
340/340, but that does not recover missing kernel durations. Cause is unknown.
No tolerance, imputation, shifted grouping, block exclusion or replacement run
is introduced. Both cells' planned activity durations remain NA, and no
three-complete-block mean substitutes for the planned five-block estimate.

All18 complete profiles pass exact recursive model-kernel totals, per-round
graph/node uniqueness and serial non-overlap, plus whole-serve graph memcpy/
memset counts. Memory-node identity is not independently mapped per round.
The initializer/controller records are kept outside model-kernel intervals.

Qwen has five complete pairs. Loop-minus-native kernel union is
+16.469ms[-1.182,34.120], model epoch+4.647ms[-5.671,14.965],
span sum+13.227ms[-4.102,30.556], inter-round gap-8.580ms[-25.405,8.244]
and within-round gap-3.242ms[-13.326,6.842]. All intervals cross zero.
Changed actual round histories confound aggregate work with per-round speed.
The dominant decode query0/batch8 stratum has both signs across blocks;
matching query/batch does not match context, KV/history or request membership.
GPU durations stay in one clock domain; no absolute CPU/GPU subtraction,
ordinary-serving fraction, exclusive transport allocation or occupancy/PCIe
cause is established.

## Failures, correctness and host limits

The first preflight is failed/incomplete: loop/unprofiled passes; native/profiled
delivers16 replies520tokens and exports its trace, then segfaults in the
post-profiler in-process replay at cudaMemcpyAsync/Tensor.copy_. The cause is
unestablished. Its logs, sources and traces remain in failed_preflight_1.
The authenticated5.862GB owned core is excluded from Git; its receipt and text
backtrace remain. No general CUDA/driver repair is claimed.

Revision1 moves the unchanged production replay body to a fresh model bootstrap
after serving for every condition. Byte-comparison receipts and old recipes
remain. This is exact reused-graph trajectory replay, not independent eager-HF
parity. All four second-preflight conditions pass serving and replay. Its first
CPU analysis exposes a previously unclassified one-thread io_initialize kernel;
source and trace show synchronization before model start. The narrow classifier
fix requires exactly1loop/0native initializer, graph/node0, one-thread geometry
and pre-model placement. It retains strict model counts and the failed analyzer
receipt. Fixed preflight passes; full analysis still fails honestly.

Independent review reconstructs both frozen output pools from24 historical
reference files per model and verifies all40 current bindings and exact
client/admission/slot/history/release/replay tokens. This finite binary token-ID
HTTP scope does not qualify arbitrary text/models/backpressure or repair the
earlier eager-HF/AMK fidelity failure.

Full collection ends2026-10-15T00:56:35.788067UTC. Root observes completion late;
host_after03:13:10.644863 is2h16m34.857s after terminal, and no full midpoint
exists. Selected NVRM0x56 warnings rise36 before→56 after, including20 during
full. Sparse same-boot/idle snapshots prove neither continuous exclusivity,
clean driver history, harmless warnings nor crash/missing-record causation.
Linux7.3rc3, driver610.57.04, CUDA13.0.88,170-SM RTX5090 and the existing400W
power limit are recorded. Common private runtime is vLLM0.31.0,
Torch2.13cu129/Transformers5.17; base packages are preserved.

## Selection and reproducibility

Keep current serving sources and defaults byte-identical. Close this unchanged
diagnostic without a bottleneck-specific optimization or unchanged GPU rerun.
This result supplies valid traced-client evidence and18 complete profiles,
with an explicit unavailable Smol decomposition. It establishes no new speedup,
generic-backend acceptance, total CPU/energy removal or completed project goal.

[Archive guide](../../bench/results/long_service_timeline_20261014/README.md)
provides CPU replay commands. Fixed preflight must pass; fixed full analysis
must reproduce its coverage failure. The explicitly post-hoc client supplement
and coverage diagnostic reproduce separately. [Restoration receipt](../../bench/results/long_service_timeline_20261014/final_restoration.json)
records archive byte checks, owned TEMP/build/core cleanup, preserved original
paths/base/Coder/source and actual post-cleanup replay outcomes. The broader
serving/performance goal remains active; another experiment needs a distinct
discriminator or stronger service evidence.
