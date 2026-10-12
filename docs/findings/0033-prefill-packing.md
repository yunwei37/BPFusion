# Pack mixed-length prefills with unchanged upstream graphs

This candidate changes GPU request grouping and input metadata, reusing the
qualified upstream vLLM model/attention/head graphs. The existing grouped
default remains available. No model arithmetic, networking,BPF,module,queue ABI
or new batching wait is introduced. The complete performance matrix is now closed, with a mixed primary outcome
and qualified long-output effects. Setup/correctness alone is not a speed result.

## Mechanism and admission

Current grouped serving selects the oldest pending prompt length and runs only
matching lengths together. Finding0032 observes gen1/eight-client mean TTFT
8.946ms Qwen and7.155ms Smol, versus1.474/1.201ms with one client. A packed
candidate selects all pending prefills at their maximum query width Q.
Each actual prompt of length n has Q-n leading dummy queries. Real token IDs,
positions0..n-1,sequence length n and page slots retain their original semantics;
dummy entries use input0,position0,is_padding=true,slot=-1.

[FlashAttention2's documented causal alignment](https://github.com/Dao-AILab/flash-attention#how-to-use-flashattention)
aligns Q against K at the bottom right. A real tail query index Q-n+t has
causal key bound (Q-n+t)+n-Q=t, the ordinary unpadded prefix bound.
The pinned upstream CUDA reshape_and_cache_flash writer returns on negative
slot mappings before address calculation. Actual installed FA2 metadata reads
dynamic query_start_loc andseq_lens. This supports the proposed binding but
does not replace real model/output validation or establish arbitrary backend
coverage. Sources remain pinned to vLLM0.31.0 commitdb9527a46.

The baseline is grouped serving with the identical model/catalogue/head/cache/
transport. Both kernel and native timed-epoll controls use each packing policy.
A common benefit belongs to GPU serving adaptation, not eBPF alone.
See the [integrated plan](../../bench/results/prefill_packing_plan_20261012.md)
and [independent review](../../bench/results/prefill_packing_plan_review_20261012.md).
The160-cell comparison tests one mechanism and retains all tradeoffs.

## Real dependency qualification

The [real eight-client/gen64 preflight](../../bench/results/prefill_packing_20261012/preflight.jsonl)
completes512 exact client tokens against independently advanced padded host
replay. Actual mixed prefill events query5/batch2 andquery8/batch6 engage the
packing intervention; native exits0 with65 model launches,max_active8 and
zero errors/trace overflow. Against the frozen unpadded batch1 diagnostic,
5/8 full sequences and7/8 first tokens match. Those differences remain visible
rather than becoming a fitted oracle or task-quality verdict.

Full strict packed service qualification completes both models/transports.
Each of four executors has622 requests/22224 independently checked tokens/
259 intentional rejections plus5000 empty connections. All batch counts1..8
occur. Fragmentation,prompt/block edges,persistent reuse/wrap,mixed output lengths,
pipeline/half-close,binary EOF/HTTP400,subsequent valid generation,helper-thread
shutdown and after-ready network syscall checks pass. CPU replay reconstructs
leading pads,positions,real lengths,negative/real slots and its own generated
history independently; it never advances from served GPU tokens.

A separate semantic diagnostic compares leading padding with compact real
variable-length query metadata and trailing ignored slots under the exact
same total Q×B tensor shape. It tests actual cached models,ordinary upstream
graphs and all real final hidden rows,not a synthetic attention fixture.
Across ten groups/model (all batch counts1..8 and mixed1..64 prompts),
all631488 active FP16 elements are finite and bit-identical. Max absolute
difference is0 and all corresponding official greedy samples agree.
Torch default assert_close also passes without tolerance changes. This
distinguishes a correct padding transformation from replay of shared bad
leading-padding semantics. It does not establish identical FP16 results
across different total batch/token shapes or universal model support.
One initial ctypes function-wrapper import failure occurs before model loading;
the class-preserving subclass repair and original failed evidence are retained.

Default untraced kernel and native timed-network paths also pass real
single-client qualification: four normal executors,160 requests/5200 exact
tokens,all original prompts and1/15/16/17/32/64 prompt edges,gen1/64 repeated
on persistent sockets. Expectations are frozen upstream batch1 sequences
from finding0032, before this candidate. Every executor reports one host
launch,1300 device model launches,max_active1,admitted/retired40 and zero errors.
This proves those default single-client conditions only; arbitrary untraced
dynamic-batch correctness/timing does not follow.

- [Qwen strict raw](../../bench/results/prefill_packing_20261012/qwen_correctness.jsonl)
  and [reconstruction](../../bench/results/prefill_packing_20261012/qwen_correctness_analysis.stdout.txt).
- [Smol strict raw](../../bench/results/prefill_packing_20261012/smol_correctness.jsonl)
  and [reconstruction](../../bench/results/prefill_packing_20261012/smol_correctness_analysis.stdout.txt).
- [Qwen semantic raw](../../bench/results/prefill_packing_20261012/qwen_semantic.jsonl)
  and [Smol semantic raw](../../bench/results/prefill_packing_20261012/smol_semantic.jsonl).
- [Untraced real requests](../../bench/results/prefill_packing_20261012/untraced.jsonl)
  and [native wait status](../../bench/results/prefill_packing_20261012/untraced_status.json).

## Reproduction and performance boundary

The candidate compiles with make vllm-graph-padded in the existing pinned
temporary Python environment. Use existing same-runtime VLLM_PYTHON discovery;
the target builds padded traced/untraced kernel/native-timed variants.
Strict candidate command:
`python3 bench/vllm_serving.py --packing-comparison --correctness --model MODEL --output /tmp/new-packed-correctness.jsonl`.
Full comparison omits --correctness. The original command without the packing
flag retains its grouped transport comparison. Use fresh output files.
`python3 bench/vllm_serving_analysis.py RAW` replays complete client/trace/reference
coverage and paired metrics with standard Python.

The full matrix has four conditions,gen1/64,clients1/8,64 measured requests/cell,
five process blocks/model,two models:160cells/10240 requests/332800 measured
tokens and320 excluded checked warmups. Both policies/transports are identically
BF_TRACE-instrumented. The primary effect is grouped-minus-packed gen1/c8 TTFT
within each transport. Throughput/TPOT/completion,single-client effects,prefill
call reduction and padded work describe tradeoffs. Actual optimized FP16 batch
trajectories and outputs can differ; every sequence must independently replay.
No physical-network,CPU/energy,untraced speed or external-SOTA/eBPF gain is claimed.
The complete matrix, fresh combined review and ownership restoration are
recorded below. The full retained goal remains active.

## Completed matched comparison

Both models finish all160 cells and40 normal executor waits. The measured
matrix has10240 requests/332800 tokens;320 checked gen1 warmups are excluded.
Both full independent replay analyses exit0. Including warmups,10560 real
requests and333120 client tokens are verified. No performance row fails,
is excluded or is retried. Actual process order, every per-request timestamp,
graph trajectory and reference remain archived.

The primary effect is grouped-minus-packed gen1/c8 mean TTFT. Each row below
uses five paired process blocks, not320 independent request repetitions.
Intervals are separate nominal Student-t95 df4, without familywise inference.

| Model | Transport | Grouped TTFT, ms | Packed TTFT, ms | Gain, ms | Nominal paired t95 |
|---|---|---:|---:|---:|---|
| Qwen2.5-0.5B | Kernel |8.860676|8.701889|0.158787|[0.017962,0.299612]|
| Qwen2.5-0.5B | Native timed epoll |11.515655|8.932346|2.583310|[-4.679428,9.846047]|
| SmolLM2-135M | Kernel |7.458966|7.048823|0.410143|[-0.200853,1.021138]|
| SmolLM2-135M | Native timed epoll |6.967508|6.980489|-0.012981|[-0.109618,0.083656]|

Only Qwen kernel's primary interval is positive. The other three are
inconclusive, including Smol kernel's two negative paired differences.
Qwen native pair3's13.015438ms apparent gain and grouped p99 of131.373818ms
remain in the estimate; cause is unknown. Do not delete this sample or call
a large mean driven by it a reliable improvement. No universal short-output
packing win, equivalence or resolution of the concurrent queueing cost follows.

The gen64/c8 secondary condition has positive TTFT intervals in every
model/transport. Full metric tradeoffs are retained, including the Qwen native
completion/TPOT/TPS intervals that cross0.

| Model | Transport | Grouped / packed TTFT, ms | TTFT gain t95, ms | Grouped / packed tokens/s | TPS gain t95 |
|---|---|---|---|---|---|
| Qwen | Kernel |2.894712 /2.155560|[0.726192,0.752111]|4632.037 /4708.372|[57.416,95.255]|
| Qwen | Native timed epoll |2.946139 /2.192735|[0.543669,0.963138]|4585.083 /4668.389|[-160.986,327.598]|
| Smol | Kernel |2.494936 /1.774843|[0.628824,0.811363]|5176.952 /5525.449|[76.789,620.204]|
| Smol | Native timed epoll |2.372806 /1.722330|[0.537315,0.763638]|5441.490 /5543.895|[79.624,125.187]|

Kernel completion gains are1.830379ms Qwen and6.401885ms Smol, with positive
intervals[1.481675,2.179083] and[1.254586,11.549183]. Kernel TPOT gains are
0.017321ms and0.090187ms, intervals[0.011637,0.023005] and[0.009872,0.170502].
Smol native completion andTPOT intervals are positive; Qwen native's cross0.
Every c1 packing interval for TTFT/TPS/TPOT/completion crosses0; this does
not establish equivalence. All packed-kernel versus packed-native TTFT/TPS
intervals also cross0, so transport superiority remains unproven.

For the primary Qwen kernel cell, grouped prefill counts across blocks are
58/58/58/58/59 versus packed56/58/57/56/58 for64 requests. Native counts show
no consistent reduction. Real mixed packing engages, but most short-output
prefills remain single-request. Additional dummy-query arithmetic and different
actual shapes/arrival trajectories are part of the treatment; graph count
alone is not a latency result. The full fresh review retains every cell's
prefill/mixed-batch/padding counts.

All single-client matched output sequences agree320/320 per model/condition.
At c8, grouped-versus-packed gen64 agreement is284/320 Qwen kernel,
283/320 Qwen native,280/320 Smol kernel and286/320 Smol native. Packed
cross-transport gen64 agreement is305/320 Qwen and294/320 Smol.
Every actual sequence separately matches its independently advanced upstream
replay. These FP16 shape trajectories preclude an identical-output or task-quality
claim; semantic setup proves the leading-pad binding at fixed total shape,
not numerical invariance across shapes. Frozen ordinary batch1 diagnostics
and all gen1 agreement counts remain in output_agreement.json.

- [Qwen full raw](../../bench/results/prefill_packing_20261012/qwen_performance.jsonl),
  [wait status](../../bench/results/prefill_packing_20261012/qwen_performance_status.json)
  and [complete analysis](../../bench/results/prefill_packing_20261012/qwen_performance_analysis.stdout.txt).
- [Smol full raw](../../bench/results/prefill_packing_20261012/smol_performance.jsonl),
  [wait status](../../bench/results/prefill_packing_20261012/smol_performance_status.json)
  and [complete analysis](../../bench/results/prefill_packing_20261012/smol_performance_analysis.stdout.txt).
- [All output agreements/frozen diagnostics](../../bench/results/prefill_packing_20261012/output_agreement.json),
  [actual environment](../../bench/results/prefill_packing_20261012/environment.json)
  and [fresh combined result review](../../bench/results/prefill_packing_result_review_20261012.md).

The [owner restoration receipt](../../bench/results/prefill_packing_20261012/owner_restoration.json)
records absent benchmark/GPU processes,module and pins; original base
Torch2.14.1+cu130/Transformers5.19.0, Coder session and unrelated work remain.
The [Workspace read](../../bench/results/prefill_packing_20261012/workspace_after_matrix.txt)
confirms original UID Running/Ready with zero restarts. The successful bounded
[kernel journal](../../bench/results/prefill_packing_20261012/host_journal.json)
21:25:00–22:24:10UTC has no listed fault matches; neither read proves continuous
device isolation. The owned temporary dependency runtime/build artifacts remain
only for the immediately following approved completion-release experiment,
rather than a retained deployment; remove them when no owner uses them.

Close this complete packing comparison with its mixed primary outcome and
qualified long-output effects. Keep grouped production behavior until the
next complete candidate qualification supports adoption. Use packed serving
as the already-qualified stronger long-output component control for the
[next release-policy experiment](../../bench/results/completion_release_plan_20261012.md),
with [fresh independent plan review](../../bench/results/completion_release_plan_review_20261012.md).
The current global reclaim wait observes local TX slot release, not a remote
TCP ACK. Testing release of an already-complete FIFO prefix is a distinct
causal intervention; neither this matrix nor its source inspection proves
that future mechanism. The full goal remains active.
