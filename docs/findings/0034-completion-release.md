# Release the completed FIFO prefix before new GPU work

The experimental BF_PREFIX_RELEASE variant publishes every already-complete
consecutive FIFO request before selecting new prefill/decode work. The original
serial policy publishes one DONE, waits for local TX slot reclamation and may
launch new work before releasing other already-complete requests. Local
reclamation follows accepted/copied sendmsg/tcp_sendmsg output, not remote TCP ACK.

Both controls use the qualified packed vLLM prefill policy and identical
checkpoint/precision/catalogue/head/KV/transport. No model arithmetic,BPF,module,
wire ABI, batching wait or persistent runtime setting changes. Original grouped/
serial production behavior remains while this candidate qualifies. Per-slot
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

Build with make vllm-graph-release and the pinned temporary VLLM_PYTHON/runtime
from the plan. Use bench/vllm_serving.py --release-comparison --correctness
--model MODEL --output /tmp/fresh-correctness.jsonl for strict qualification.
The full command omits --correctness; bench/vllm_serving_analysis.py RAW
reconstructs all received bytes/trajectory/cells and paired metrics.

The full160-cell/four-condition/two-model matrix is in progress:gen1/64,
clients1/8,64 measured requests/cell,five paired process blocks. Planned totals
10240 measured requests/332800 tokens plus320 checked gen1 warmups. Both policies/
transports are identically BF_TRACE-instrumented. Primary is serial-minus-prefix
gen1/c8 mean TTFT within each transport,nominal paired t95 df4. Keep every
pair/outlier,all single-client and long-output TTFT/TPS/TPOT/completion tradeoffs,
actual release-to-cell joins and batching/padding work.

No performance conclusion,untraced dynamic-batch timing,physical delivery,total
CPU/energy,arbitrary-model,equivalence,SOTA or eBPF-only gain follows from setup.
No default adoption until complete evidence and fresh combined result review
support it,with necessary real untraced default checks. The original runtime/
Workspace/PVC/session/caches and unrelated tools/setup_env.sh remain. The full
retained goal stays active.
