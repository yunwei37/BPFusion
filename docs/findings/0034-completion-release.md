# Release the completed FIFO prefix before new GPU work

The experimental BF_PREFIX_RELEASE variant publishes every already-complete
consecutive FIFO request before selecting new prefill/decode work. The original
serial policy publishes one DONE, waits for local TX slot reclamation and may
launch new work before releasing other already-complete requests. Local
reclamation follows accepted/copied sendmsg/tcp_sendmsg output, not remote TCP ACK.

Both controls use the qualified packed vLLM prefill policy and identical
checkpoint/precision/catalogue/head/KV/transport. No model arithmetic,BPF,module,
wire ABI, batching wait or persistent runtime setting changes. The completed comparison below precedes default adoption; grouped/serial
behavior remains an explicit component control. Per-slot
reservation,phase ownership,system fences,final-token protection and FIFO/per-peer
ordering remain intact. Completed graph outputs are consumed before release;
GPU release does not clear TX's reservation or reread a released shared slot.

[Admitted plan](../../bench/results/completion_release_plan_20261012.md) and
[fresh ownership/control review](../../bench/results/completion_release_plan_review_20261012.md)
precede execution. Common release-ID events and counters join publication rounds
to actual client conditions. Traced capacity derives from one admission,at most64
compute and one release event per request. Independent host replay uses its own
generated history and checks final-compute/FIFO/one-time release and physical-slot
reuse. Previous packing archives still reconstruct byte-identically.

## Completed real qualification

The [real TCP preflight](../../bench/results/completion_release_20261012/preflight.jsonl)
completes16 requests/520 exact client tokens in eight-client gen1 andgen64
conditions. Gen1 releases one request,then a seven-request prefix;gen64 releases
all eight together. This proves actual engagement,not speed. All tokens match
independently advanced upstream replay; native stop and terminal are0.

Both cached architectures and all four serial/prefix × kernel/native variants
finish the full strict622-request protocol with22224 independently checked tokens,
259 intentional invalid-ID rejections and5000 empty connections each.
Total4976 requests/177792 tokens,2072 intended rejections and40000 empty connects.
All actualB1..8 occur in each executor. Fragmentation,prompt/block edges,
persistent wrap/reuse,mixed1/64 outputs,pipeline/half-close,binary EOF/HTTP400,
subsequent valid generation and helper-thread shutdown pass. All eight waits
and both complete analyses exit0,zero graph errors/overflow.

Common instrumentation records serial max-prefix1 and candidate max-prefix8.
Qwen release rounds are622/159 for serial/prefix kernel and622/128 native;
Smol622/143 kernel and622/138 native. All admitted IDs release once in FIFO
after their complete actual compute,including zero-compute intentional rejections.
Four kernel terminal maps retain reserved0/eight FREE slots. Their after-ready
all-thread traces have no accept/recv/send calls; native controls have the intended
accept4/recvfrom/sendmsg calls. Deliberate binary invalid EOF abandonment remains
a rejection case,not a lost valid reply.

- [Qwen strict raw](../../bench/results/completion_release_20261012/qwen_correctness.jsonl)
  and [full reconstruction](../../bench/results/completion_release_20261012/qwen_correctness_analysis.stdout.txt).
- [Smol strict raw](../../bench/results/completion_release_20261012/smol_correctness.jsonl)
  and [full reconstruction](../../bench/results/completion_release_20261012/smol_correctness_analysis.stdout.txt).
- [Actual build command](../../bench/results/completion_release_20261012/build_command.json),
  [build stdout](../../bench/results/completion_release_20261012/build.stdout.txt)
  and [pipeline commands/exact serving sources](../../bench/results/completion_release_20261012/pipeline_commands.json).

This validates metadata/control fidelity to unchanged upstream graphs,not an
independently implemented arithmetic or task-quality oracle. Fixed-shape padding
semantics remain qualified by finding0033; different FP16 batch/arrival shapes
can produce different output sequences. Frozen ordinary unpadded diagnostics
are retained,without served-token teacher forcing or tolerance adjustment.

## Comparison and current boundary

Build with make vllm-graph-release and the pinned VLLM_PYTHON/runtime
from the plan. Use bench/vllm_serving.py --release-comparison --correctness
--model MODEL --output /tmp/fresh-correctness.jsonl for strict qualification.
The full command omits --correctness; bench/vllm_serving_analysis.py RAW
reconstructs all received bytes/trajectory/cells and paired metrics.

## Complete matched performance result

Both full drivers and analyses finish0: Qwen23:02:11UTC and Smol23:13:33UTC
on2026-10-12. All160 cells/40 executors complete10240 measured requests and
332800 measured tokens plus320 independently checked gen1 warmups. No missing,
failed,excluded or retried full-run cell. Every received sequence matches its
own independently advanced upstream replay; all request IDs join admission,
actual compute,final-token completion,FIFO release and safe physical-slot reuse.
Both policies/transports use identical BF_TRACE instrumentation.

| Model / transport | Serial gen1/c8 TTFT ms | Prefix TTFT ms | Paired reduction ms | Nominal paired t95, df4 |
|---|---:|---:|---:|---:|
| Qwen / kernel |8.821412|2.595630|6.225782|[6.106539,6.345024]|
| Qwen / native |8.892217|2.520429|6.371787|[6.025879,6.717696]|
| Smol / kernel |7.050603|1.891055|5.159548|[5.107920,5.211176]|
| Smol / native |6.939086|2.013869|4.925218|[4.701560,5.148875]|

All four predeclared primary intervals are positive, with positive differences
in every process block. Actual primary release-ID joins establish multi-release;
serial64 release rounds become roughly15..17 prefix rounds and primary prefill
rounds56..58 become15..17. Source and traces support removing the unnecessary
global reclamation wait and permitting timely admission/batching. This is the
net scheduler-policy effect,not a measurement of pure TX wait or GPU kernel cost.
The common benefit in both transports cannot be attributed to eBPF.

Single-client policy-change TTFT/TPS/completion/TPOT intervals all contain0.
Long-output/eight-client policy-change TTFT intervals all contain0. Qwen's
long-output TPS/completion/TPOT intervals contain0 in both transports. Smol kernel
long-output TPS improves63.503572tokens/s[37.600568,89.406575],completion falls
1.040834ms[0.598909,1.482758] and TPOT falls0.017640ms[0.011267,0.024013].
Smol native long-output point estimates worsen,with intervals containing0.
These are nominal exploratory bounds,not equivalence or a universal win.

Prefix kernel-versus-native transport results remain mixed. Qwen gen64/c8
kernel TTFT is0.095339ms slower,nominal interval[0.016997,0.173682] favoring native;
Smol gen1/c1 kernel is0.058183ms faster,[0.014773,0.101593]. Other reported
prefix TTFT intervals and all long-output throughput intervals contain0.
There is no general eBPF latency/throughput superiority claim.

| Model / mode | gen / clients | TTFT ms | Completion ms | TPOT ms | token/s |
|---|---:|---:|---:|---:|---:|
|qwen / serial-kernel|1 / 1|1.464290|1.464290|—|676.623|
|qwen / prefix-kernel|1 / 1|1.426892|1.426892|—|694.780|
|qwen / serial-userspace|1 / 1|1.465237|1.465237|—|675.812|
|qwen / prefix-userspace|1 / 1|1.442436|1.442436|—|686.079|
|qwen / serial-kernel|64 / 1|1.374687|78.181241|1.219152|818.172|
|qwen / prefix-kernel|64 / 1|1.406323|79.101341|1.233254|808.818|
|qwen / serial-userspace|64 / 1|1.384899|78.648977|1.226414|813.427|
|qwen / prefix-userspace|64 / 1|1.370860|78.184272|1.219261|818.148|
|qwen / serial-kernel|1 / 8|8.821412|8.821412|—|893.394|
|qwen / prefix-kernel|1 / 8|2.595630|2.595630|—|2938.469|
|qwen / serial-userspace|1 / 8|8.892217|8.892217|—|891.316|
|qwen / prefix-userspace|1 / 8|2.520429|2.520429|—|3052.374|
|qwen / serial-kernel|64 / 8|2.210103|108.738193|1.690922|4704.211|
|qwen / prefix-kernel|64 / 8|2.256484|110.396506|1.716508|4637.193|
|qwen / serial-userspace|64 / 8|2.295831|109.794396|1.706326|4662.224|
|qwen / prefix-userspace|64 / 8|2.161145|108.098412|1.681544|4731.391|
|smol / serial-kernel|1 / 1|1.189327|1.189327|—|831.063|
|smol / prefix-kernel|1 / 1|1.179105|1.179105|—|837.947|
|smol / serial-userspace|1 / 1|1.224917|1.224917|—|807.306|
|smol / prefix-userspace|1 / 1|1.237288|1.237288|—|795.751|
|smol / serial-kernel|64 / 1|1.111007|45.960007|0.711889|1391.343|
|smol / prefix-kernel|64 / 1|1.119492|45.953465|0.711650|1391.563|
|smol / serial-userspace|64 / 1|1.131769|45.944484|0.711313|1391.875|
|smol / prefix-userspace|64 / 1|1.187033|47.084263|0.728527|1359.243|
|smol / serial-kernel|1 / 8|7.050603|7.050603|—|1115.012|
|smol / prefix-kernel|1 / 8|1.891055|1.891055|—|3984.046|
|smol / serial-userspace|1 / 8|6.939086|6.939086|—|1141.154|
|smol / prefix-userspace|1 / 8|2.013869|2.013869|—|3772.481|
|smol / serial-kernel|64 / 8|1.684107|92.402984|1.439982|5535.611|
|smol / prefix-kernel|64 / 8|1.754604|91.362150|1.422342|5599.114|
|smol / serial-userspace|64 / 8|1.751136|92.206930|1.435806|5545.326|
|smol / prefix-userspace|64 / 8|1.835053|94.808871|1.475775|5403.139|


Each displayed condition has320 measured requests over five process blocks.
The analysis preserves all five differences and nominal intervals. TTFT is
first complete client-token receipt minus request send start; completion is
last-token receipt; TPOT is first-to-last receipt divided by gen-1; throughput
uses the complete cell interval. These include network/client coalescing and
are not GPU-ready/decode-kernel timings. Definitions follow the official
[vLLM metrics](https://docs.vllm.ai/en/v0.31.0/design/metrics/).

Cross-run output agreement is a diagnostic,not the service correctness oracle.
All serial/prefix single-client sequences agree320/320. Qwen gen1/c8 agreement
is264/320 kernel and248/320 native;gen64/c8 is287/320 and284/320. Smol gen1/c8
is320/320 both,gen64/c8 is290/320 kernel and288/320 native. Changed arrival/
batch trajectories can change FP16 greedy outputs. Every actual trajectory
still matches its own independent upstream replay. This is not an identical-
output performance comparison or task-quality measurement.

The bounded host journal records global OOM23:06:50UTC killing another
Lean49PreparedB process and contemporaneous connection ping timeouts. It overlaps
Smol pair1 serial-kernel bootstrap(start23:06:10,ready23:07:07),rather than
its measured-ready cells. Preserve the pair; memory-pressure exposure before/
after the event is unknown and not matched across policies. No clean-host,
continuous isolation or transport-only causal claim follows. The final owner
receipt finds no own executor/GPU application/module/pins,unchanged original
boot/base runtime,and the original Workspace Running/Ready with0 restarts.

- [Qwen full raw](../../bench/results/completion_release_20261012/qwen_performance.jsonl)
  and [all reconstructed metrics](../../bench/results/completion_release_20261012/qwen_performance_analysis.stdout.txt).
- [Smol full raw](../../bench/results/completion_release_20261012/smol_performance.jsonl)
  and [all reconstructed metrics](../../bench/results/completion_release_20261012/smol_performance_analysis.stdout.txt).
- [Qwen output agreement](../../bench/results/completion_release_20261012/qwen_output_agreement.json)
  and [Smol output agreement](../../bench/results/completion_release_20261012/smol_output_agreement.json).
- [Bounded host journal](../../bench/results/completion_release_20261012/performance_host_journal.json),
  [owner receipt](../../bench/results/completion_release_20261012/performance_owner_receipt.json)
  and [Workspace receipt](../../bench/results/completion_release_20261012/performance_workspace_receipt.txt).
- [Fresh combined result review](../../bench/results/completion_release_result_review_20261012.md).

Run complete; scoped primary prediction supported; role supporting. This closes
the unchanged release-policy matrix. The fresh review supports adoption; the ordinary untraced checks below
complete its bounded qualification. Full-service CPU/energy,
physical-network timing,arbitrary backends,full-text/API and external-SOTA
acceptance remain open under the retained goal. Original Workspace/PVC/session/model cache and unrelated tools/setup_env.sh
remain; final cleanup is recorded separately below.


## Ordinary default adoption

After the independent completed-run review, ordinary vllm_graph, its native
control and their traced counterparts now compile the exact qualified
BF_PAD_PREFILL+BF_PREFIX_RELEASE flags. Native/backend C++/Python sources and
analyzer remain byte-identical to the qualified candidate. Only Makefile
selection and the driver's explicit binary mapping change. No model arithmetic,
module/BPF/wire protocol or persistent infrastructure setting changes.

The12-variant catalogue retains distinct controls instead of accumulating
combinations: ordinary4 are packed/prefix, vllm_graph_padded4 are packed/serial,
vllm_graph_grouped4 are grouped/serial. The release driver selects padded versus
ordinary; the packing driver selects grouped versus padded, preserving both
causal comparisons. Ordinary transport comparison selects ordinary. The old
padded_prefix names in archived raw describe the pre-adoption6754 revision;
current names are disclosed here and in the new source/build record.

All12 binaries are freshly rebuilt. Actual compile definitions are retained in
[build stdout](../../bench/results/completion_release_20261012/default_build.stdout.txt)
and [command/current source snapshots](../../bench/results/completion_release_20261012/default_adoption_sources.json).
Four real ordinary untraced executors then pass two architectures × two
transports,40 persistent single-client requests each, gen1/64 and prompt/block
length edges1/15/16/17/32/64. Total160 requests/5200 client tokens match the frozen
independently generated upstream batch1 sequences. All four native waits exit0,
one host launch each,1300 model steps,max_active1,40 admitted=retired,zero graph
errors/trace overflow. This qualifies the actual default executable/lifecycle
path; it does not establish untraced dynamic-batch correctness/timing or transfer
the traced performance numbers to untraced serving.

[Actual check source](../../bench/results/completion_release_20261012/untraced.py),
[raw replies and embedded frozen references/sources](../../bench/results/completion_release_20261012/untraced.jsonl),
[driver stdout](../../bench/results/completion_release_20261012/untraced_driver.stdout.txt)
and [terminal status](../../bench/results/completion_release_20261012/untraced_status.json)
retain the distinction. To rebuild current comparison controls, use
make vllm-graph-release vllm-graph-grouped with the documented runtime.

[Final restoration](../../bench/results/completion_release_20261012/final_restoration.json)
after all adoption checks verifies no own process/module/pins/GPU application,
same original boot/base runtime and removal of the two owned temporary roots
and owned adapter build outputs. Archived evidence and source remain; rebuild
against the documented pinned runtime before another run. Original Coder owners,
Workspace/PVC/model caches and unrelated tools/setup_env.sh are preserved.
