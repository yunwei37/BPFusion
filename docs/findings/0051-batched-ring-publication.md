# Batched ring publication gives partial gains, not vLLM latency recovery

Batched queue publication improves tested AMK latency/throughput and Qwen
long-output throughput relative to the prior coalesced driver. It does not
establish recovery of vLLM's eight-connection short-output latency. Efficient
native TCP remains the competing delivery result; this is a mixed driver result.

## Question and actual intervention

The [plan](../../bench/results/queue_batch_20261014/plan.md) and
[fresh plan review](../../bench/results/queue_batch_20261014/plan-review.md)
retain the CPU-path-removal/reusable-computation question. Finding0050's completed
coalescing matrix exposed an AMK native gap and severe vLLM short-output costs.
This new experiment changes queue publication, not model arithmetic.

Only existing BF_IO_COALESCED builds change. Each progression round snapshots
SQ head/tail, reserves against that conservative snapshot and system-orders
buffer/SQE writes before one release tail publication. The early cancel return
also publishes prepared work. CQ processing snapshots the acquire tail,
consumes that finite batch and release-publishes head after reads. Subsequent
completions wait for the next round; a full-ring reservation can also defer.
FIFO/final-send ownership, timeout, shutdown/model quiescence, shared queue ABI
and model math remain. Noncoalesced builds retain their literal per-entry policy.
No new target, timer, worker or runtime setting is introduced.

The production patch adds38/removes2 lines in one shared header. Internal ring
layout, finite-drain/availability timing and compiled dispatcher work change
collectively; this is not an isolated PCIe-access-cost experiment.
Static AMK dispatcher instructions fall2328→2216 and vLLM3536→3432;
network drain1432→1384. Initialization retains56 instructions but differs with
internal layout offsets. Static counts do not measure dynamic system accesses
or establish mediation. The
[official liburing CQ iterator/publication](https://github.com/axboe/liburing/blob/master/src/include/liburing.h)
and [SQ flush](https://github.com/axboe/liburing/blob/master/src/queue.c)
provide the design precedent; GPU system-scope publication remains.

## Controls and completed collection

Original bpfusion-dev Workspace/main, RTX5090/170SMs and the same temporary
Torch2.13+cu129/Transformers5.17/vLLM0.31 runtime are used. Pinned AMK884534c4
computation, Smol93efa2f0 FP16/cpasync0/K1/eight private banks and current vLLM
Smol/Qwen7ae55760 computation/packing/KV/prefix policy remain unchanged.
AMK CUDA13 and vLLM CUDA12.9 linkage differ across backends; no pure fusion claim.

Candidate source is2a2d21d5a8da35dc37d4d6bb842bb1f014d5576c. The component control
is actual pre-edit07ba7e0 coalescing, loaded as *_uring_loop_coalesced_original.
It is not0050's older independent network-worker control. Its captured sources
reconstruct saved normalized GPU SASS: AMK3 functions/3816 instructions and
vLLM3/5024. Efficient native epoll TCP with the same per-workload computation
is the single strongest main competing mechanism. Prior independent-worker
evidence is cited, without adding a fourth unchanged path.

All45 ordinary executors complete at12:40:59.823102UTC:180 cells,5760 measured
requests/187200 output tokens plus360 checked excluded gen1 warmups. Every
actual child exits0; no full cell is excluded, substituted or restarted.
Five paired process blocks cover gen1/64 atc1/c8,32 requests/cell, four literal
prompts over preopened persistent localhost connections. Five of six path
permutations and odd-block model/cell reversal retain residual order/drift
confounding. Replication units are five process blocks, not individual requests.
This is not representative arbitrary-text, capacity, tail/SLO or total CPU/energy.

## Ordinary serving results

Means of five blocks; latency is measured at the client.

| Backend/model | Path | gen1/c1 TTFT ms | gen1/c8 TTFT ms | gen64/c8 token/s |
|---|---|---:|---:|---:|
| AMK Smol135M | Before batching |18.824859|133.302093|293.111235|
| AMK Smol135M | Native TCP |18.236809|130.444295|304.004198|
| AMK Smol135M | Batched |18.363459|130.139273|301.132448|
| vLLM Smol135M | Before batching |1.213314|6.325096|5074.836727|
| vLLM Smol135M | Native TCP |1.197806|1.969981|5639.216779|
| vLLM Smol135M | Batched |1.186492|7.158562|5197.851818|
| vLLM Qwen0.5B | Before batching |1.476726|8.308400|4359.721639|
| vLLM Qwen0.5B | Native TCP |1.390926|2.633415|4703.201704|
| vLLM Qwen0.5B | Batched |1.419200|8.591165|4523.921622|

Primary candidate-minus-control effects, nominal pairedt95df4 intervals:

| Workload | gen1/c8 TTFT vs before, ms | gen1/c8 TTFT vs native, ms |
|---|---:|---:|
| AMK Smol135M |−3.162821 [−5.555847,−0.769794]|−0.305022 [−4.266797,3.656753]|
| vLLM Smol135M |+0.833465 [−0.203219,1.870149]|+5.188581 [4.772662,5.604500]|
| vLLM Qwen0.5B |+0.282765 [−0.237319,0.802848]|+5.957750 [5.534988,6.380512]|

| Workload | gen64/c8 TPS vs before | gen64/c8 TPS vs native |
|---|---:|---:|
| AMK Smol135M |+8.021213 [6.970035,9.072392]|−2.871750 [−3.687511,−2.055989]|
| vLLM Smol135M |+123.015092 [−116.174996,362.205179]|−441.364961 [−714.104308,−168.625614]|
| vLLM Qwen0.5B |+164.199983 [142.069462,186.330505]|−179.280082 [−360.826004,2.265840]|

AMK's long-output recovery is about2.7% relative to before batching, with a
remaining0.94% native throughput gap; every signed throughput contrast agrees.
Qwen improves about3.8% relative to before. These ratios use displayed means.
Smol's mean improvement is not established: its block2 difference is−220.278
token/s, versus positive other blocks; the row remains included. Neither a
crossing-zero throughput interval nor similar means establish native parity.

The primary short-output latency hypothesis is supported narrowly for AMK
versus the prior coalesced control, but not for either vLLM workload. Both
vLLM native gaps remain strongly positive. Positive versus-before means with
intervals crossing0 do not prove either harm or non-regression/equivalence.

Secondary AMK gen1/c1 TTFT improves−0.461401 ms versus before
[−0.488677,−0.434124], but remains+0.126650 versus native
[0.075359,0.177941]. All vLLM gen1/c1 intervals cross0; no general latency
win follows. The [full analysis](../../bench/results/queue_batch_20261014/full.analysis.json)
retains all36 means/108 paired effects, signed blocks, completion/TPOT and
known-worker CPU. No historical before/after serving speedup is substituted
for these matched controls.

TTFT=first arrival−request send; completion=last arrival−send;
TPS=tokens/(last arrival−first send);TPOT=(completion−TTFT)/(gen−1).
The finite cell window follows the source-native client. CPU brackets cover
known process/worker components, not total kernel/softirq work or energy.

## Correctness, mechanism and environmental scope

All6120 complete outputs/187560 tokens including warmups match unchanged finite
whole-output pools. Model/graph errors, ownership and independently empty SQ/CQ
checks pass. The stronger old AMK eager-HF exact failure remains failed;
pool membership and unobserved ordinary batch trajectories do not prove all-input
parity. Current vLLM's selected traced protocol independently replays batch/KV
history, rather than replacing that oracle with the output pool.

Nine real preflight paths pass36 cells/288 requests9360 tokens plus72 warmups.
Candidate protocol completes622 requests22224 tokens/259 rejects plus5000
empty connections per workload, covering fragmentation, invalid inputs,
wrap, pipeline and halfclose. Three32-action lifecycle checks cover idle,
RST/reuse, inflight stop and pending accept/recv, with652 checked complete/prefix
tokens each. strace shows no steady userspace accept/recv/send request worker.
These are qualification dependencies, not independent performance contributions.

Host observations before, during at12:20, mid-run at12:30 and after at12:41UTC
retain boot04dc0087 and33 prior NVRM status0x56 warnings, with no new selected
fault. Endpoint GPU application lists are empty; in-run lists are retained.
These discrete records are not continuous isolation, a clean-journal claim,
warning harmlessness or a complete environmental-cause exclusion.
No CUPTI model-overlap, per-bank identity or dynamic cursor-count claim is made.

## Review, reproducibility and next decision

The [fresh independent result review](../../bench/results/queue_batch_20261014/result-review.md)
audits raw outputs/arrivals, all paired effects, controls, code growth and scope,
qualification and host observations. The
[complete archive](../../bench/results/queue_batch_20261014/) retains source-native
adapters, exact environment/packages and expanded commands, source snapshots,
receipts, failures and raw records; runtime/vendor/ELFs/weights are excluded.

Rebuild prior controls using Makefile.original/rebuild_original.py and the
captured source home; build current candidates with the existing coalesced
Make targets. setup.py describes the pinned temporary runtime. Full command
is /usr/bin/python3 run.py full, with TEMP/runtime/bin/python model drivers;
offline replay is python3 analysis.py ARCHIVE full. Historical absolute paths
identify the original run; adapt them to a fresh temporary directory for replay.

Retain batching as a limited improvement within the existing experimental
coalesced mode. Keep defaults and efficient native/current optimized vLLM
delivery evidence. The unchanged matrix is closed: queue-publication batching
does not solve the vLLM short-output cost. A next driver diagnosis should
distinguish network progression/admission availability and actual model batches,
rather than claim PCIe or model arithmetic as the cause. Full retained serving/
performance objective remains active; this component result is not completion.

[Restoration](../../bench/results/queue_batch_20261014/final_restoration.json)
records owned TEMP/build cleanup, preservation of default/base/Coder/PVC/
unrelated WIP and byte-identical archive replay. An accidentally archived
operational publication helper is removed forward; scientific build/run/replay
sources remain. No new persistent service, schedule or runtime setting is kept.
