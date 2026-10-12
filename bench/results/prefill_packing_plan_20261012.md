# Mixed-length GPU prefill packing with unchanged upstream computation

Retain the full user goal: Linux TCP/HTTP/eBPF queue -> GPU-owned real inference
-> asynchronous kernel TCP, upstream compute reuse, matched correctness/
latency/throughput and honest main publication. Existing main b2950e5 is the
qualified grouped-prefill baseline. No formal paper RQ/thesis is invented.

## Admission and causal question

Finding0032 closes the same-backend transport comparison as inconclusive.
It also exposes gen1/eight-client TTFT8.946ms Qwen and7.155ms Smol, versus
single-client1.474/1.201ms. The native scheduler admits available prompts but
groups prefills only when lengths match. Actual full-run prefill counts
230-233 per264-request executor show little prefill consolidation.

Hypothesis: packing all currently pending full-attention prefills into one
uniform-query graph, with left dummy Q positions and unchanged real KV/position
semantics, reduces short-output concurrent latency without rewriting model math.
This is serving scheduling/buffer adaptation, not an eBPF or new GPU-kernel claim.
Positive: primary grouped-minus-packed gen1/c8 TTFT paired interval above0
supports this adapter optimization. Negative/inconclusive: retain bounds and
the grouped implementation; do not tune model arithmetic or rerun unchanged
conditions. Throughput/TPOT tradeoffs must be visible; no universal claim follows.

Role: supporting engineering/causal mechanism comparison. It adds an actual
packing intervention beyond0032's unchanged transport paths. The strongest
runnable alternative is current grouped serving with the identical captured
catalogue/model/head/KV/transport. A new unchanged cross-node matrix, another
default compute probe or model-specific kernel campaign would not isolate this
known scheduler uncertainty. Existing official-vLLM comparisons remain cited;
this component experiment is not external serving superiority.

## Upstream contract and candidate

FlashAttention2 documents bottom-right causal alignment for Q length greater
than K length: leading fully masked query rows output0, real tail queries see
their ordinary causal prefixes.
Source: https://github.com/Dao-AILab/flash-attention#how-to-use-flashattention
and the pinned installed vLLM FA2/cache implementation. Inspect actual installed
negative slot mapping behavior before execution; the device cache writer must
skip dummy -1 slots. These are source contracts, not evidence that the entire
model adapter is already correct.

Choose query=max actual prompt length among pending prefills and select all
pending prompts, without a new wait, policy parameter or admission delay.
Each row retains uniform Q width=query. Leading query-prompt dummy entries
use input0,position0,is_padding=true,slot=-1. Real entries use original prompt
IDs and original positions0..n-1,real sequence length n,slot pages for those
real positions. Query starts remain uniform; final row token remains the actual
last prompt token, so the existing official head indices are unchanged.
Decode, state ownership, FIFO DONE/recycle, wire ABI,module/BPF and graph math
are unchanged. Both checkpoints/transports use the same policy.

Keep grouped production behavior while candidate qualification runs. Use an
ordinary temporary compile variant for packed prefill, not a retained service/
scheduler/control layer. After valid positive complete evidence, apply only
the qualified packing behavior and keep the old grouped path as the named
component control if needed for reproduction. Reject unsupported cache/attention
types rather than silently broadening model support.

## Correctness and real preflight

The padded reference is independently reconstructed Python metadata plus
host replay of upstream graphs. For every traced prefill use original prompt,
own generated history,actual recorded uniform query width,explicit leading
dummy slots/positions/padding and real lengths. Never feed served GPU tokens
as the next reference input. Require complete actual received client bytes
to match independently advanced replay, with zero trace overflow/errors.

Additionally inspect semantic attention/KV contracts and retain ordinary
unpadded upstream fidelity diagnostics. Do not relabel an arbitrary packed
sequence as mathematically equivalent if padding changes the model; source
contract alone or agreement with an identically buggy state transformation
does not establish general model fidelity. Real cases must include mixed
2/5/8 and1/15/16/17/32/64 prompts,invalid tokens,reuse and differing output lengths.
Known FP16 batch-shape output differences remain explicit, not automatic
task-quality failure or fitted oracle acceptance.

First actual TCP preflight: mixed short prompts, eight clients,gen64,
kernel packed candidate. It must engage an actual mixed-length prefill compute
event and complete independent replay. Then full622-request strict protocol
for each candidate model/transport,including all actual batch counts1..8,
fragmentation,259rejections,5000empty connects,pipeline/half-close/helper stop.
The existing grouped reference is already fully qualified and uses the same
generic replay after any necessary reference adaptation.

Default untraced startup/real-request validation is folded into setup, not
a standalone paper result. Use independently frozen batch1 upstream sequences
for real single-client repeated gen1/64 requests and prompt edges in both
untraced transports/models. This proves that tested default condition only,
not unobserved arbitrary dynamic-batch equivalence.

## Integrated matched experiment

One matrix, two models, four conditions:
grouped-kernel,packed-kernel,grouped-timed-userspace,packed-timed-userspace.
The userspace rows are a transport/control check: a common packing benefit in
both paths belongs to GPU serving adaptation, not eBPF alone.
All conditions reuse the same pinned vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17,
FP16 checkpoint,128-token/eight-slot upstream-owned KV budget and BF_TRACE.
No total CPU/energy,full text,physical-NIC,arbitrary-model or SOTA claim is added.

Four existing prompts; gen1/64; clients1/8;64 measured requests/cell;
eight checked gen1 warmups/executor; five process blocks/model. Rotate/reverse
the four condition orders across blocks and retain actual ordering. In total:
160cells/10240 measured requests/332800tokens/40 executors plus320warmup tokens.
Primary paired metric is grouped-minus-packed gen1/c8 mean TTFT within each
transport; report df4 nominal t95. Other TTFT/TPOT/completion/output TPS conditions
and actual batching/prefill call counts show tradeoffs and mechanism engagement.
No finite-request pseudo-replication,selected exclusion or arbitrary gain threshold.

Metric definitions/client implementation reuse bench/resident_dispatch.py
and existing vLLM driver/analyzer. First/last client monotonic arrivals define
TTFT/TPOT/completion; cell tokens over first-send/last-arrival define throughput.
A graph-count reduction alone is not a performance result. Report instrumentation,
padding work and distinct actual optimized FP16 trajectories.

Real command and artifact paths will use the existing make/bench workflow in
original bpfusion-dev main, temporary dependencies at
/tmp/bpfusion-padding-b45ull5p and ordinary bench/results/prefill_packing_20261012
raw/stdout/trace/reference/status records. Never overwrite earlier evidence.
Document exact selected executors/compile flags and sources in raw metadata.
Plan and one fresh plan review precede actual candidate serving; one fresh result
review follows the complete matrix. Preserve original session/Workspace/PVC/
base runtime/caches and tools/setup_env.sh; cleanup only owned test artifacts.
The full goal remains active if the stated broader acceptance is incomplete.

## Additional semantic discriminator before performance

The real mixed eight-client preflight passes512 independently replayed tokens,
but only5/8 full sequences and7/8 first tokens agree with the frozen unpadded
batch1 reference. Keep these differences. Before interpreting candidate timing,
compare real hidden states under identical captured total Q×B tensor shapes:
left-padding versus compact real variable-length query_start_loc with ordinary
positions/lengths/KV slots and trailing ignored -1 slots. Both replay unchanged
upstream model graphs, and the compact reference uses no leading pad/shift.
Compare all actual prompt hidden FP16 elements, finiteness, bit equality,
max absolute difference and torch.testing.assert_close's dtype defaults,
fixed before this diagnostic. This is an additional semantic setup check,
not a substituted serving oracle or a performance result. No tolerance tuning,
served-token teacher forcing or model arithmetic rewrite.
