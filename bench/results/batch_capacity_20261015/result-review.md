# Independent result review — same-compute batch capacity

Reviewer: `/root/batch_capacity_result_review`, different from the plan reviewer.
This is the single RESULT REVIEW of the completed run; no desired verdict was
supplied. Review date:2026-10-15, after full terminal and proposed finding0064.

## Required judgments

- **Run status: valid** for the admitted finite BF_TRACE shared-host comparison.
- **Tested hypothesis: supported**, separately for both models: sixteen banks
  improve kernel delivered TPS at192/s over eight, with exact trajectory-matched
  numerical/wire fidelity and zero measured failures.
- **Research value: supporting.** This is new evidence for a shared constructor
  capacity boundary, not a new eBPF performance mechanism.
- **Paper impact: mechanism or workload boundary.** No formal RQ/thesis was
  introduced; the retained full serving/performance objective remains open.
- **Next paper decision:** close this unchanged matrix; retain native16 as the
  strong competitor and retain its counterevidence. Do not claim intrinsic eBPF
  superiority, select ordinary defaults or transfer traced timings to ordinary
  serving. Actual ordinary adoption or a new causal discriminator is a separate
  decision. This review authorizes no new experiment or persistent setting.

No blocker invalidates this traced run. Restoration/publication remain the
owner's subsequent work at review time, not presumed complete.

## Independent audit and exact recomputation

I read plan.md and the complete three-part plan-review.md; load.py, analyze.py,
protocol_analysis.py, full.py, setup/build/env/package/model records and diffs;
the actual frozen candidate differences, relevant admission/dispatcher/I/O/native
source; embedded backend/client/native sources in both full metadata records;
full raw requests/GPU histories/references, protocol raw streams and network
traces, ordinary lifecycle raw records and frozen-pool implementation; host
phase receipts; plot source/data; proposed finding0064, README and evaluation
addition. Figure pixels were not inspected here; root performs visual QA.

With A=/workspaces/repository/bench/results/batch_capacity_20261015, I freshly ran:

```text
/usr/bin/python3 A/analyze.py A/preflight_qwen.jsonl
/usr/bin/python3 A/protocol_analysis.py A/protocol_qwen.jsonl
/usr/bin/python3 A/protocol_analysis.py A/protocol_smol.jsonl
/usr/bin/python3 A/analyze.py A/full_qwen.jsonl
/usr/bin/python3 A/analyze.py A/full_smol.jsonl
```

All five exit0 with empty stderr and reproduce their saved analysis stdout
**byte for byte**. This was fresh execution, not reliance on root's replay.
No GPU experiment or numerical replay was started by this reviewer.

A separate in-memory Python audit, without importing analyze.py, independently
recomputed all80 raw cells' membership/denominators/TPS; request-, connect- and
scheduled-origin TTFT/completion P50/P95/P99 and means; CPU deltas/brackets;
all96 paired effect vectors/means/t95df4 intervals; and all16 figure aggregate
block vectors/means/attempt/failure counts. Everything agrees. The independent
percentile sorts values and interpolates at(n-1)*q. Independently auditing every
full admission/compute/release stream also reconstructs exact reference tokens,
physical ownership and FIFO release:40executors,20,800 requests incl320warmups,
1,311,040 tokens. Wire matching is checked by unique marker.

I opened the official [vLLM v0.31.0 serving benchmark source](https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py)
and [CLI documentation](https://docs.vllm.ai/en/stable/cli/bench/serve/)
for metric provenance. This is a custom token-ID HTTP adapter/finite protocol,
not the official API benchmark.

## Completion, deviations, binding and mechanism

full.exit.json, rather than preparation-only all.exit.json, ends at
2026-10-15T15:22:39.023596UTC:exit0,2/2. Both full.statuses entries have driver
and analysis exits0. Each model has20starts/executors/successful executor
terminals,40cells and10,400requests, no request_error/request_invalid/failure.
Total:40executors,80cells,20,480 measured successes,zero failures/exclusions,
1,310,720 measured tokens plus320gen1warmups. No favorable replacement occurred.
/proc/611266 is absent at review.

Pre-execution followups corrected Williams ordering and separated ordinary
finite-pool lifecycle qualification from traced numerical validity, including
stop-on-unexpected-nonzero lifecycle subprocess exit. The final driver and
analyses implement this reviewed plan. No outcome-driven oracle, precision,
timeout, metric, workload or replacement change appears during full collection.
Plot dependencies were installed after terminal at15:24:29.140814UTC;
archived version lists agree with changed_existing={}.

Recursive byte comparison identifies exactly two differing candidate files:
BF_LLM_SLOTS8->16 in bpfusion_queue.h and Makefile path substitutions. Makefiles
are equal after normalizing candidate8/candidate16 names. Native eligible-frame
FIFO and arithmetic source are shared. The32-bit reservation bitmap covers0..15;
private header precedence binds BPF,loader,CUDA to each matching build. Adapter
max_requests() discovers the library width and sizes graphs/KV banks. Launchers
select adjacent matching libraries; embedded driver/client equal archived files,
and embedded backend equals current backend. Both builds exit0.

Runtime pins vLLM0.31.0,Torch2.13.0+cu129,Transformers5.17.0,NumPy2.3.5,
libbpf1.6.3; package differences against previous qualified runtime are empty.
Cached Qwen revision7ae557604adf67be50417f59c2c2f167def9a775 and Smol
93efa2f097d58c2a74874c7e644dbc9b0cee75a2 use FP16 in both paths.
All width16 conditions actually execute widths1..16; controls execute1..8.

Aggregate decode-round engagement below combines both rates and five blocks.
These are logical event counts, not time occupancy or a unique bottleneck.

| Model/path | Decode rounds | Mean width | Rounds at max | Executor queued peaks |
|---|---:|---:|---:|---|
| Qwen kernel8 |21158|7.62265|17803|130,133,132,134,145|
| Qwen native8 |20897|7.71785|18497|136,128,128,128,134|
| Qwen kernel16 |14946|10.79085|3893|47,45,49,54,32|
| Qwen native16 |14834|10.87232|4426|51,21,29,39,33|
| Smol kernel8 |22850|7.05821|14851|99,94,96,116,102|
| Smol native8 |23030|7.00304|14664|113,96,96,112,96|
| Smol kernel16 |18193|8.86495|2853|22,14,13,60,10|
| Smol native16 |17152|9.40299|3117|17,7,16,11,17|

Qwen KV changes65blocks/12,779,520bytes to129/25,362,432; Smol changes
65/23,961,600 to129/47,554,560. Graph dimensions/counts, resource allocations,
shared-page ABI and realized grouping differ. This is matched arithmetic,
precision and requests, not identical kernel sequences or isolated syscall
removal. The private16 ABI is not qualified against legacy/module paths.

Native16 is a credible strong mechanism competitor: same width/model/optimized
graphs/banks/packing/prefix release and complete eligible-frame FIFO admission.
It has real nonzero queued peaks and empty pending deque at stop; descriptor
priority does not unfairly govern its admission. Existing60us nominal active
completion wait matches the kernel lower-bound policy; idle waits for socket/
deadline and shutdown uses eventfd. It is not an intentionally busy baseline.
All attempts complete and it wins an important comparison below. No baseline
failure is counted as a kernel victory. This is a matched native alternative,
not unrestricted external production-serving SOTA. Native/kernel buffering,
readiness ordering, finite4096kernel queue and one-active-native-response per
connection differ. One request/connection avoids pipelining workload asymmetry.
Width8 conditions are capacity controls/ablations, not extra main baselines.

## Independent oracle, resource accounting and ordinary scope

Backend replay independently rebuilds padding/input/position/sequence length,
slot mappings, block tables and physical ownership from prompts plus its own
previous replay outputs. It executes upstream body/head graphs, compares each
token, then appends the replayed token to reference history. Invalidity comes
from bounds/vocabulary. Candidate output never becomes reference next-input
history. Sharing the observed batch schedule is deliberate trajectory matching,
not circular expected-output construction. The oracle shares intended upstream
arithmetic and weights: it qualifies dispatch/history execution fidelity, not
independent architecture, model task quality or universal trajectory equivalence.
Every full reference exactly matches reconstructed traces and actual client
HTTP bytes by unique marker, with64 arrival timestamps per measured request.
No admitted response is unchecked and no numerical trace overflow is excused.

All40executors have admitted=retired=520, graph_error=trace_overflows=0.
Independent stream audit confirms no physical-bank reuse before release and
strict next-prefix release. Kernel head/completed agree, accepted=closed,
pending/error/reserved/dropped/overflow=0, SQ/CQ drain and final banks/admission
are free. Native publishes/completes520,rejects0 and queued_at_stop0. This is
real terminal accounting rather than a successful trigger or running process.

Two copied protocol analyses independently reproduce5136outcomes,2060intended
rejects,188800checked tokens and1..16widths. I separately searched saved serving
strace sections: both kernel cases have zero accept/recv/send-family calls and
one io_uring_enter; native has thousands of accept4/recvfrom/sendmsg. Source
agrees with retained kernel-loop entry/device-owned model dispatch. This
qualifies absence of a steady userspace request worker for these paths, not
absence of CPU/kernel work or a transport speed claim.

All four ordinary lifecycle raw records pass their unchanged frozen complete/
prefix-membership contract. Each loop has144actions/78accepted-and-closed
connections,16active,32queued at reset and48queued at stop. Head96+48cancellations
accounts for144. There are97exact observed rows and47unobserved canceled rows
per loop; checked tokens1484Qwen/1020Smol, including66partial rows each. Native
has32rows/13connections,32published/31completed/10rejects,652checked tokens,
2partial rows each. All record model_errors[0] and no pins. These are not144or32
complete numerical responses. The finite historical pool is not universal,
native queued-stop scope is narrow, and ordinary passes neither qualify all
possible16-bank ordinary trajectories nor establish ordinary performance.

## Results and metric interpretation

TPS denominator is end_ns-begin_ns: before scheduled arrivals through all client
thread joins. It includes offered window, drain, Python scheduling and completion
overhead. It is finite delivered-window TPS, not steady saturation capacity or
production-SLO goodput. All attempts succeed, so success-conditioned tails hide
no failed request here. Failure denominators nevertheless remain in every row.
Request throughput is TPS/64 for this successful gen64 matrix.

Primary kernel16-minus8 at192/s, five paired blocks, nominal t95df4:

| Model | Kernel8 TPS | Kernel16 TPS | Difference [t95] | Ratio-of-means increase |
|---|---:|---:|---:|---:|
| Qwen |5653.495|9672.702|+4019.207 [3554.685,4483.729]|71.0924%|
| Smol |7190.349|10524.759|+3334.411 [2143.702,4525.120]|46.3734%|

Every primary block effect is positive for both models. Native capacity also
gains: Qwen+4413.412[4057.039,4769.784] and Smol+4218.648[3453.942,4983.354]TPS.
This is useful shared capacity relief, not isolated eBPF benefit.

The complete mean table below is checked against raw cells. Latencies are means
of block P99s, not pooled P99s.

| Model | Rate | Path | TPS | Connect TTFT P99 ms | Connect completion P99 ms | Scheduled TTFT P99 ms |
|---|---:|---|---:|---:|---:|---:|
| qwen | 96 | uring_loop_8 | 5595.255 | 243.150 | 324.512 | 244.631 |
| qwen | 96 | userspace_8 | 5632.848 | 218.014 | 303.734 | 219.894 |
| qwen | 96 | uring_loop_16 | 5949.757 | 23.104 | 117.912 | 24.403 |
| qwen | 96 | userspace_16 | 5943.252 | 18.481 | 112.788 | 22.639 |
| qwen | 192 | uring_loop_8 | 5653.495 | 1486.048 | 1564.246 | 1488.352 |
| qwen | 192 | userspace_8 | 5946.441 | 1361.071 | 1441.535 | 1361.904 |
| qwen | 192 | uring_loop_16 | 9672.702 | 297.181 | 383.272 | 298.948 |
| qwen | 192 | userspace_16 | 10359.853 | 200.338 | 288.349 | 204.527 |
| smol | 96 | uring_loop_8 | 5974.236 | 73.026 | 142.738 | 74.528 |
| smol | 96 | userspace_8 | 5986.781 | 62.394 | 130.425 | 64.619 |
| smol | 96 | uring_loop_16 | 5986.804 | 20.031 | 93.458 | 22.943 |
| smol | 96 | userspace_16 | 5988.667 | 13.020 | 89.576 | 16.496 |
| smol | 192 | uring_loop_8 | 7190.349 | 890.705 | 953.925 | 892.569 |
| smol | 192 | userspace_8 | 7229.893 | 878.424 | 944.028 | 879.587 |
| smol | 192 | uring_loop_16 | 10524.759 | 155.250 | 271.669 | 204.306 |
| smol | 192 | userspace_16 | 11448.541 | 62.696 | 139.318 | 66.684 |

High-load kernel-capacity TTFT P99 effects are Qwen-1188.867
[-1341.720,-1036.015]ms and Smol-735.456[-798.975,-671.936]ms; completion
-1180.973[-1345.151,-1016.795] and-682.256[-823.368,-541.144]ms.
At96/s Qwen capacity TPS+354.503[105.300,603.705],TTFT P99-220.046
[-373.904,-66.188]ms and completion-206.600[-368.249,-44.951]ms are favorable.
Smol96/s TPS+12.568[-14.210,39.346],TTFT P99-52.994[-111.435,5.446] and
completion-49.279[-107.252,8.694]ms are inconclusive. Native Smol96/s capacity
also crosses zero. Lower means alone do not establish low-load benefits.

The strongest same-width comparison, kernel16-minus-native16 at192/s, is
adverse for Qwen: TPS-687.151[-1145.186,-229.115],TTFT P99+96.843
[17.381,176.306]ms,completion P99+94.923[6.911,182.935]ms,scheduled TTFT
P99+94.420[14.222,174.619]ms. Smol TPS-923.782[-2453.508,605.945],TTFT
P99+92.554[-123.651,308.758],completion+132.350[-92.290,356.990],scheduled
TTFT+137.621[-96.148,371.391]ms are inconclusive. Both96/s width16 transport
TPS/TTFT/completion intervals cross zero, as do width8 transport contrasts at
both rates/models. No same-width transport superiority or equivalence follows.

An adverse secondary behavior must remain explicit when discussing latency:
mean block mean TPOT increases8->16. Qwen kernel1.34646->1.47646ms at96/s,
1.34619->1.51465 at192/s; Smol1.11003->1.14014 and1.04694->1.33270.
Native TPOT means rise too. Queue relief is not uniform improvement in token
gaps. These are descriptive means, not predeclared paired TPOT significance
claims. Client recv coalescing prevents interpreting TPOT as isolated GPU time.

## Ordering, uncertainty, host exposure and leakage

The first four Williams blocks put every condition in every position once;
fifth repeats block0. Pairwise precedence counts2or3, rotating rates and exact
matched normalized gamma(shape1) schedules reduce avoidable order bias, but five
blocks cannot eliminate temporal correlation. Paired t95 uses2.776445105*SD/sqrt5,
nominal independent-block assumptions, no multiplicity correction. There are
two model primaries and many secondary comparisons. Crossing zero is inconclusive,
not equivalence.256requests/cell provide sparse P99 order statistics, not precise
population tails/P99.9/production SLOs. Four short prompts/gen64 do not qualify
arbitrary contexts/models/tasks.

All scheduling lag remains included. Smol kernel16 pair1/192 has lag P99
288.425ms and pair3/192222.994ms. Pair1 connect TTFT P99=72.934ms versus
scheduled-origin312.474ms. Mean Smol192kernel16 connect versus scheduled TTFT
P99=155.250 versus204.306ms. Qwen kernel16 has49.039/49.955ms lag in two
192/sblocks; native16 reaches45.984ms in one. Effective arrivals and grouping
can differ despite equal intended schedules. These delays bound causal transport
attribution and tails without changing the admitted finite-window hypothesis
into a scheduler-free comparison. No outlier was dropped after observation.

Process CPU brackets all executor threads slightly outside epoch/end and
excludes client work and separate RX/softirq/BPF/io-wq/all TCP accounting.
Module TX CPU=0 because that path is absent. At192/s kernel16/native16 is
0.846591/0.452892ms per attempt Qwen,0.564381/0.396877Smol. Signed differences
+0.393699[0.352155,0.435243] and+0.167504[0.082233,0.252776]ms/attempt are
adverse. Capacity reduces high-load kernel process CPU versus8; eliminating
steady userspace request processing does not imply total CPU/energy efficiency.

Supplemental post-collection calculation of raw global /proc/stat user,nice,
system,irq,softirq deltas (numeric indices0,1,2,5,6), divided by verified
SC_CLK_TCK=100 and each epoch-to-thread-join duration, gives about24.03..24.44
busy-core equivalents. Counter samples bracket that duration slightly outside
it. They include client/unrelated-host/kernel work and are not attributed
service CPU. I do not convert this to utilization percent or saturation: the
host logical-CPU denominator/container allowed CPUs are not established by this
metric. This reinforces shared-host exposure, not a proven bottleneck.

Qwen short ownership sample is4.167s after its measured cell,replay/teardown;
Smol short sample is inside one pair0/kernel8/192cell. Post-full sample is
92.802857s after terminal,same boot,56unchanged selected historical fault lines,
no reported GPU app. These sparse receipts do not prove continuous isolation,
no interference or absence of all faults. No foreign workload was paused.

Oracle GPU replay is after serving, outside measurement. Both methods share
model trajectory information only for post-hoc checking, with no future/reference
output or candidate-dependent expected-history supplied to serving. Repeated
short prompts and warmed graphs are matched intended conditions, not cold-start
evidence. Common BF_TRACE overhead may interact with width/batch/scheduling;
its positive effect cannot be transferred to ordinary untraced timing.

## Proposed numbers/figure and return to owner

All proposed primary/native/tail/CPU/lag numbers and percentages in finding0064
and the current evaluation addition match raw results and independent
recomputation. Their scientific claims fit this scope. Complete data has80cells,
96paired effects,2coverage rows and16plotted aggregates, all independently checked.
Plot source shows192/s TPS and96/s TTFT P99 for both models, all block points
plus means, log tail axis and caption identifying means of block statistics.
No adverse block is omitted or nonexistent confidence interval drawn. The full
data/report must remain linked because the plotted subset omits192/s transport
tails/CPU/lag. PNG/PDF values are admitted; pixels remain root's visual QA.

Minor editorial cleanup remains: README intro still calls full.process.json
current and says full.exit.json will record completion, despite its appended
terminal section. Evaluation text also mixes historical running checkpoints
with current completion. Preserve dated provenance but make current status
unambiguous when recording this review and actual restoration. This is not a
validity blocker. TPOT's adverse direction should remain explicit when presenting
broad latency benefits; all full metric rows must remain accessible.

At review git symbolic-ref --short HEAD is main. All eight preserved entry.json
inode/size/mtime/symlink records still match live state, including unowned
tools/setup_env.sh and original builds. This reviewer modified only this report;
no experimental source/plan/data/docs, competing GPU process, checkout/worktree/
Workspace/infrastructure change or owned cleanup. Root retains restoration and
publication ownership.

Return this valid supporting result. It explains a useful previous8-bank
constructor boundary and prevents attributing shared capacity gains to eBPF.
It neither directly challenges a formal thesis nor completes the full user goal.
Retain native16 as the strong comparison, close this unchanged experiment, and
route any ordinary adoption or new causal discriminator through its own decision.
No additional run is required or authorized by this result review.
