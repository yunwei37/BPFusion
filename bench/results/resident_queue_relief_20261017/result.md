# Shared capacity repair: completed five-block16/32/official comparison

2026-10-17 UTC. Owner-only implementation, experiment, recomputation and audit.
The user prohibits other agents, including reviews; no independent-person
review is claimed. Frozen [plan](plan.md), [diagnosis](diagnosis.md),
[32-bank qualification](qualification.md) and [single diagnostic](diagnostic.md)
precede this full acquisition. No partial prefix is substituted.

The capacity repair removes the sustained pre-output queue growth in this
short-prompt workload. Prespecified Resident32-minus-Resident16 completionP99:
**-3119.915ms, nominal pairedt95[-3227.115,-3012.715]**.
Means3337.271->217.356ms (~93.49% lower); delivered throughput11639.616->
12265.069tokens/s (+625.453[613.268,637.639],~5.37%).
This is a shared constructor/batching/KV-capacity repair, not an eBPF benefit
or a new model-kernel optimization.

## Exact scope and complete outcomes

Qwen2.5-0.5B-Instruct FP16 revision7ae557604adf67be50417f59c2c2f167def9a775,
RTX5090/lab, remote g10 client. Same four2/5/8-token prompt IDs, generation64,
temperature0/ignoreEOS, original offsets/seeds20261015+block,192requests/s for
60s+full drain. Each of15 fresh processes receives11520 measured requests.
All172800 requests/11059200output tokens complete with0 observed failures;
120 checked gen1 warmups are excluded. Five counterbalanced blocks are in the
plan. No parser,model,oracle,timeout,metric or arrival switch during acquisition.

Resident16 and32 share ordinary native epoll and upstream model computation;
matching bank counts change capture/layout/KV/effective admission capacity
together. The current comparison DOES NOT contain a32-bank BPF path.
Official0.31.0 uses normal optimized defaults/CUDAgraphs/cache/scheduler,
tokens-only HTTP and actual auth controls; no forced-eager or reduced capacity.
The qualified stack/commands/source/client/offsets/builds and every server/
merged/worker/resource/warmup receipt remain in this directory.

| Metric (mean of five process cells) | Resident16 | Resident32 | Official vLLM |
|---|---:|---:|---:|
| Delivered output tokens/s | 11639.615972 | 12265.069167 | 12249.355231 |
| Completion P99 ms, connect origin | 3337.271462 | 217.356456 | 405.869178 |
| Completion P99 ms, scheduled origin | 3337.258010 | 219.693607 | 407.840973 |
| TTFT P99 ms, connect origin | 3248.606249 | 124.619143 | 220.045015 |
| Mean TTFT ms | 1631.568360 | 38.641424 | 102.606228 |
| Mean TPOT ms | 1.361841 | 1.395148 | 2.392531 |
| Client receive-gap P99 ms | 4.265771 | 5.760249 | 14.890055 |
| Client dispatch-lag P99 ms | 2.016655 | 1.890186 | 3.704376 |
| Owned group CPU ms/attempt | 0.750658 | 0.523302 | 8.326998 |
| Workspace cgroup CPU ms/attempt (nested/shared) | 1.154378 | 0.911157 | 8.680403 |
| Host active CPU ms/attempt (shared) | 58.453125 | 55.355035 | 68.097743 |
| Client CPU ms/attempt | 10.127315 | 9.584540 | 12.922624 |
| Device-wide energy J/attempt | 1.715748 | 1.683272 | 1.347554 |

Resident32-minus-official deliveredTPS+15.714[11.272,20.155],only~0.128%.
Both are near the offered ceiling12288tokens/s; the difference includes final
drain and DOES NOT rank maximum capacity. CompletionP99 difference is
-188.513[-234.410,-142.615]ms. It closes the motivating5x tail/5% throughput
gap locally, not universally. Official's current405.869ms is contemporaneous;
0078's~611ms remains dated evidence and is not silently reused or rewritten.
The preregistered primary remains32-minus16, not a switched official metric.

## Mechanism and adverse evidence

Prior ten-second arrival buckets show16-bank TTFT growing while generation
duration remains~86ms. Official actual running counts exceed16. The ordinary32
constructor and two-model exact finite replay/lifecycle controls directly test
that capacity explanation. Full arrival-bucket plot/data distinguish queue
growth from a slow individual generation. Full first/last10s meanTTFT grows240.738->3022.133ms for16,
while32 stays31.975->39.727ms;16generation span stays85.846->85.357ms.
OfficialTTFT stays88.992->102.572ms. full_queue_context.json retains values.
Wider capture/KV/batching are coupled;
this does not isolate KV management,chunked prefill or a specific GPU stage.
Normal Make's existing BF_LLM_SLOTS=32 profile is documented as preferred for
this sustained mixed workload; legacy global default8 remains for its actual
hardcoded layouts. No handwritten attention/matrix arithmetic is introduced.

MeanTPOT worsens16->32 by **0.033308[0.014804,0.051811]ms** (~2.45%).
Receive-gap P99 point estimate worsens4.266->5.760ms; paired+1.494ms interval
[-2.196,5.185] crosses0. TPOT P99 is also inconclusive. These are retained,
not hidden by the much larger queue-tail improvement.
Finite reference-pool disagreement flags remain952/633/739 for16/32/official
(total2324). All protocol counts/ranges and official prompt/finish/raw-SSE
reconstruction pass, but this finite trajectory pool does not prove universal
numerical parity. It is not expanded after seeing flags.

Client lagP99 maxima16/32/official are3.934/3.465/5.084ms. Scheduled-origin
tails are retained. JSON/SSE/token coalescing and client timing are delivered
service measurements, not GPU/kernel ITL. The historical6.36ms kernel/native
receive-gap difference is still unreproduced/unallocated; this capacity repair
does not claim to fix it.

Group CPU falls0.751->0.523ms/attempt (difference-0.227356
[-0.264118,-0.190595]). Shared host difference32-minus16 is-3.098ms/attempt
[-6.253,+0.057],inconclusive. Group/cgroup/host/thread views overlap and are
never summed. Foreign CPU work,shared IRQ/softirq and incomplete kernel-worker
visibility prohibit exclusive whole-service CPU/energy attribution.
Against official,device-wide energy is adverse:+0.335718[0.322754,0.348683]
J/attempt (~24.9%); keep this alongside lower resident group CPU. The resource
ledger exposes owned thread user/system/io-wq and shared host context.

## Reproduction, auditing and lifecycle

[Full raw and all69 paired effects](queue_relief_full/analysis.stdout) are the
machine-readable source of every table value. The normal acquisition driver,
source copies,offsets,model/environment and build qualification are retained.
Run the archived queue_relief_analysis.py against queue_relief_full, then
owner_audit.py, resource_context.py and queue_relief_plot.py as in the closure
script. Gzip logs contain the original request/worker data; no row exclusion.

Archive replay is byte-identical with empty stderr; owner_audit.py independently
recomputes172800attempts,all69effects/t95 intervals and every official raw-SSE
payload using separate calculation code. All15sample groups are stable and
all sampled GPU applications are owned. source_freeze_audit.json verifies all15
actual server/BPF/network source snapshots againstf7ac3d0,with no changes in
executor/,bpf/,Makefile or the example during acquisition. Closure receipts,
resource_context.stdout and owner-audit.md retain details. The generated PNG
was visually inspected for all four panels,labels,points and original-arrival
queue slope; PDF comes from the same Matplotlib figure. This is owner-only
checking,not an independent-person review.
The bounded client Job is deliberately retained for the user's next requested
small-graph experiment; final Job deletion is not claimed here. All15 serving
processes and their GPU contexts/pins terminate before this milestone.
Original Workspace/PVC/session processes and foreign tools/setup_env.sh remain.

## Decision

Run valid; shared queue-relief hypothesis supported locally; research value
supporting mechanism/repair evidence. This is not transport novelty or a general
LLM victory. The user closes LLM speed competition after this commit. Next is
one bounded cuBLAS/cuFFT small-request network/CPU experiment, same-executor
epoll controls, work/rate/service-core crossovers, remote clients, complete tails
and fixed positive/negative exit criteria. Do not run the superseded LLM K32/N32
matrix or continue model-specific tuning to rescue a transport claim.
