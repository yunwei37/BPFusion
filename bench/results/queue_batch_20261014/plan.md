# Batched queue publication in the coalesced GPU driver

## Retained question and admission
Finding0030 retains the user's question: remove CPU request admission/completion
work while preserving efficient reusable real-model GPU execution. Keep backend
arithmetic out of the contribution. The current CPU-worker-free optional Linux
eBPF/io_uring path remains the actual target, not a synthetic queue microbenchmark.

Finding0050 supplies the completed strongest prior discriminator: coalescing
recovers AMK gen64/c8 TPS158→293 but native304 remains better, AMK latency
increases, vLLM TPS regresses8–9%, and gen1/c8 TTFT rises2.04/2.64→6.75/8.25ms.
An unchanged matrix is closed. The next independent uncertainty is whether
repeated system-scope accesses/publication of host-mapped ring cursors in each
progression round impose a avoidable driver cost. Source io_submit currently
loads SQ head/tail and fences/publishes each SQE; CQ drain reloads tail and
publishes head for each CQE. The official liburing iterator snapshots the
acquire tail, processes a finite local batch and release-publishes head once;
its SQ flush similarly publishes prepared work after memory ordering.
Sources: https://github.com/axboe/liburing/blob/master/src/include/liburing.h
and https://github.com/axboe/liburing/blob/master/src/queue.c
The CPU library is design precedent; GPU system-scope publication is retained,
not replaced with a relaxed CPU-only store.

A collective queue-publication batching intervention can change the driver
decision without touching arithmetic or adding a new network worker. Positive
would support a portable synchronization/driver improvement; mixed/negative
would bound this approach and prioritize a distinct admission/batch scheduling
diagnosis. This is supporting evidence, not a headline eBPF transport win.
It beats an unchanged rerun or model sweep because the production access
pattern is concretely different and no prior matched result tests it.
It does not establish that this is the cause of0050's large latency regression.

## Hypothesis, implementation and validity
Hypothesis: one system-scope cursor snapshot/publication per progression round
reduces coalesced driver latency while retaining finite correct worker-free
service and long-output efficiency. Compare actual serving, not a fake queue.

Only existing BF_IO_COALESCED builds change. Do not introduce another target,
runtime knob, timer, worker, queue ABI or infrastructure. In each round:
snapshot SQ head/tail locally; reserve/prepare SQEs against that snapshot;
system-order buffer/SQE writes and release-publish new tail once, including
early shutdown/cancel returns. Snapshot acquire CQ tail; read/process only
that finite CQ batch and release-publish consumed head after reads. New CQEs
are processed next round. Preserve FIFO/final-send ownership, single issuer,
pending accounting, timeout/cancel and model-quiescence policy. A stale SQ-head
snapshot may defer a full-ring reservation to the next round, never overwrite
an unconsumed SQE. Wrap uses existing unsigned arithmetic. Noncoalesced source
retains existing semantics. Network round/availability ordering changes
collectively; no pure cursor-latency/PCIe/occupancy attribution.

Preserve actual pre-edit07ba7e0 coalesced sources and source-native rebuilt
control libraries named *_uring_loop_coalesced_original. They are component
controls. Efficient native epoll TCP with identical computation per workload
is the single strongest main competing mechanism. The current original
independent-worker evidence in0050 remains cited, not an added fourth path.
Native compilation excludes network code. Verify unchanged native computation
and old-control build recipes/source identity.

## Workloads and metrics
Original Workspace/main, RTX5090/170SMs. Pinned AMK884534c4 unmodified computation,
Smol93efa2f0 FP16/cpasync0/K1/eight private banks; optimized vLLM0.31 Smol and
Qwen7ae55760, same current packing/KV/prefix policy. Common temporary runtime
Torch2.13+cu129/Transformers5.17; retain AMK CUDA13/vLLM CUDA12.9 differences.
Literal four prompts and unchanged frozen0045 complete-output pools.

Three workloads × three paths × five paired process blocks × four cells
(gen1/64 × c1/c8);32 measured requests/cell and8 excluded checked warmups.
45 executors/180 cells/5760 measured requests187200 tokens plus360 warmups.
Five path permutations, odd-block cell/model reversal. Residual order drift
uncontrolled; no randomization, representative-text, capacity, SLO, total CPU
or energy claims.

Primary latency: gen1/c8 candidate-minus-before-coalesced and candidate-minus-
native TTFT independently for each workload. Retain AMK's absolute backend
limits. Primary efficiency guard: gen64/c8 TPS for each workload against both
controls. Report all gen1/c1/gen64/c1 and completion/TPOT/known-worker CPU as
secondary; retain every signed paired block effect and nominal t95df4 interval.
No invented aggregate score, noninferiority cutoff, universal winner or
equivalence when intervals contain0. Use the existing source-native client:
TTFT=first arrival−send; completion=last arrival−send;
TPS=tokens/(last arrival−first send);TPOT=(completion−TTFT)/(gen−1).
Terminology: https://docs.vllm.ai/en/stable/benchmarking/cli/

## Execution and review
One fresh independent plan review before real preflight/full. Prepare source/
commands/runtime in original Workspace. Reuse archived setup.py, source-native
matched_serving.py/analysis.py and qualification/lifecycle adapters; change
TEMP/old-control names only. Actual standard-library wrapper:
 /usr/bin/python3 TEMP/run.py preflight1
then full after qualification/source freeze:
 /usr/bin/python3 TEMP/run.py full
Each inner driver uses TEMP/runtime/bin/python matched_serving.py --backend
BACKEND --block BLOCK --loop-comparison --untraced --reference-path
TEMP/frozen_references.json --model PINNED_SNAPSHOT --output TEMP/FILE.jsonl.
Modes are old coalesced, native, new coalesced. Freeze all15 expanded commands,
source revision, environment and actual native build flags before full.

Use the real9-executor preflight with all36 cells. Preserve failed attempts,
up to three per skill; no oracle/workload relaxation. Candidate selected
source-native full protocol:622 requests/22224 tokens/259 rejects plus5000
empty connections per workload; three existing32-action lifecycle tests with
idle/RST/reuse/inflight stop and independent empty SQ/CQ/counter checks.
vLLM traced protocol independently replays actual batch/KV history, and outputs
also retain unchanged pool checks. AMK stronger eager-HF equality remains
failed. All-input parity and ordinary batch trajectory remain unproved.

Actual code/static build establishes the policy; strace selected protocol
checks worker-free engagement. Do not invent per-bank/timeline mediation or
precise dynamic cursor-access attribution. Mechanism/protocol setup is
dependency work, not separate scientific results.

Record host journal/GPU/memory/boot before, during and after actual full
collection; use same live wrapper handle to completion. Endpoints are not
continuous isolation. Preserve all warnings/faults and all rows. Fresh result
review independently recomputes complete raw evidence, baselines and tradeoffs.
One ordinary plan/review/report home. Archive source/env/commands/raw arrivals,
failures/analysis; omit runtime/vendor/ELFs/weights. Remove only owned TEMP/builds
after terminal processes/reviewer release; preserve default qwen_graph.so,
base packages, Coder/PVC/unrelated tools/setup_env.sh and unowned trace builds.
Commit/push validated own work directly main and verify public bytes.
Keep the full generic serving/performance goal active unless actually achieved.
