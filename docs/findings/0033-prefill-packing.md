# Pack mixed-length prefills with unchanged upstream graphs

This candidate changes GPU request grouping and input metadata, reusing the
qualified upstream vLLM model/attention/head graphs. The existing grouped
default remains available. No model arithmetic, networking,BPF,module,queue ABI
or new batching wait is introduced. The complete performance matrix is still
running; setup/correctness results below are not performance conclusions.

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
Fresh combined result review,final publication and owner cleanup follow the
complete matrix. The full retained goal remains active.
