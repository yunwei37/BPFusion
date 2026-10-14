# Model-idle admission follows the SQ submission frontier

## Retained question and admission
Retain the complete Linux TCP/HTTP/eBPF/shared-queue/resident real-model/async-TX
objective and improve latency/TPS with reused computation. Finding0030 keeps
model arithmetic outside the contribution. Finding0051 closes the prior queue-
publication matrix: AMK and Qwen have local throughput gains, but vLLM gen1/c8
TTFT remains7.16/8.59ms versus native1.97/2.63.

Reanalysis of its existing ordinary counters gives vLLMSmol2380.4 model graph
launches/102 release rounds versus native2357.2/84; Qwen2380.6/102 versus
native2356.2/84.2. These executor totals mix four cells and do not attribute the
difference to gen1/c8. Current qualification traces mainly exercise long-output
concurrency; they cannot supply the missing ordinary short-output trajectory.
The source is more specific: io_progress submits asynchronous work; each final
reply waits for next_final/CQ before the next ordered final reply. The parent
can immediately admit a fresh model request, suspending further network
progress while that child executes. This may couple client feedback and batching
to extra model rounds. It is not an established cause.

Proposed actual intervention: when all previously admitted model work has
published completion (retired==seen), keep advancing I/O while the kernel has
not consumed the published SQ tail. Then admit new model work. This tests a new
submission-frontier scheduling policy, not an unchanged rerun, a model sweep or
a toy queue. Positive would select a small portable driver ordering improvement;
mixed/negative would retain the boundary and select a distinct diagnosis.
It can materially repair the strongest current latency reject argument.
Role supporting, with real serving/client primary metrics.

## Concrete scope and hypothesis
Add only the following existing BF_IO_COALESCED dispatcher condition after
io_progress in qwen_graph.cu and vllm_graph.cu:
 if(c->retired==c->seen &&
    io_load(io_state->ring.head)!=io_load(io_state->ring.tail))continue;

No new flag, target, worker, fixed batching delay/minimum, timer, page ABI,
model arithmetic or runtime infrastructure. The existing stop check is revisited
on every loop. Already admitted unfinished computation remains eligible because
retired!=seen. This waits for SQ consumption, not TCP/CQ completion or all
pending operations. A stalled kernel issuer can delay fresh admission; this is
a real tradeoff to retain. Do not claim arbitrary backpressure/fairness proof.
Kernel/BPF loop source checks SQ head/tail and submits published SQEs, then
waits on CQ independently; inspect actual source/qualification, not speculative
queue semantics. https://github.com/torvalds/linux/blob/master/io_uring/io_uring.c
is upstream context, not a version-identity proof for installed kernel7.3rc3.

Hypothesis: this policy reduces tested vLLM short-output extra model rounds
and client latency without new userspace work, while preserving existing
computation and selected ownership/lifecycle correctness. Publication-to-
consumption availability ordering and driver work change collectively.
No pure PCIe latency, occupancy or authenticated GPU-time mediation claim.

## Controls, workloads and primary metrics
Candidate versus captured current ceadcc0 coalesced driver (component control)
and efficient native epoll TCP (single strongest main competing mechanism).
Old controls use actual saved pre-edit source/binaries named
*_uring_loop_coalesced_original and source-native snapshot reconstruction.
Native excludes the changed network path and retains identical model computation.
Existing independent-worker evidence from0050 is cited; no fourth timing path.

Original Workspace/main and RTX5090/170SMs; common temporary Torch2.13+cu129/
Transformers5.17/vLLM0.31. AMK884534c4 Smol93efa2f0 FP16/cpasync0/K1/eight private
banks; current vLLMSmol/Qwen7ae55760 computation/packing/KV/prefix policies.
Same four prompts/frozen0045 pools. AMK stronger exact-HF failure stays failed.
Cross-backend constructor/CUDA linkage differs; no pure fusion comparison.

Full ordinary matrix:3 workloads ×3 paths ×5 paired process blocks ×4 cells
(gen1/64 ×c1/c8),32 requests/cell,8 checked excluded gen1 warmups/executor.
45 executors/180 cells/5760 measured requests187200 tokens plus360 warmups.
Five of six path permutations; odd model/cell reversal, residual order/drift
uncontrolled. Finite persistent localhost waves, not representative text,
capacity/SLO, arbitrary model or total CPU/energy.

Primary vLLMSmol/Qwen gen1/c8 candidate-minus-prior and candidate-minus-native
TTFT; gen64/c8 TPS and AMK gen1/c8/TPS transfer are efficiency/transfer guards.
All gen1/c1/gen64/c1, completion/TPOT and known-worker CPU are secondary.
Retain every signed block and nominal pairedt95df4, no manufactured aggregate,
noninferiority cutoff, universal winner or equivalence from crossing-zero CIs.
Source-native client TTFT=first arrival−send;completion=last arrival−send;
TPS=tokens/(last arrival−first send);TPOT=(completion−TTFT)/(gen−1).
Terminology https://docs.vllm.ai/en/stable/benchmarking/cli/

## Integrated batch observation and qualification
The real preflight retains all9 paths/36 ordinary cells. Preserve failures;
up to three actual preflights per skill, without oracle/workload relaxation.
Selected candidate protocol622 requests22224 tokens/259 rejects/5000 empty
connections per workload and three existing32-action lifecycle tests include
fragmentation/invalid/wrap/pipeline/halfclose, idle/RST/reuse/inflight stop,
pending accept/recv and independent empty SQ/CQ/model/ownership checks.
These are dependency qualification, not independent paper contributions.

Add one source-native short-output observation to this admitted experiment:
two vLLM models ×three paths ×ordinary/BF_TRACE, one process per condition,
one gen1/c8 cell32 requests plus8 excluded c1 gen1 warmups each.12 executors,
384 measured requests/tokens plus96 warmups (480 complete replies).
Reuse matched_serving.py/gen1 client and preexisting BF_TRACE interface,
source-native Make flags; reconstruct old-control trace variants from the
same old source. Do not overwrite preexisting unowned ordinary-loop trace files.

Ordinary one-cell total graph launches minus exactly8 warmup launches gives
measured model-round count directly (each valid gen1 request computes once).
Traced admission client_ns authenticates request IDs; compute request_ids
supply actual per-round membership/batch sizes, including separated warmups.
Validate every token against independent trace history replay and unchanged
pools. Retain traced versus ordinary client latency and aggregate counts as
descriptive instrumentation sensitivity; one observation is not proof of
neutrality/equivalence or causal mediation in the untraced full matrix.
No CUPTI graph-node mapping, GPU clock offsets or new custom control schema.
If trace association fails, retain valid ordinary latency/count evidence and
limit the mechanism claim; do not replace it with a toy/proxy timeline.

## Execution, review and cleanup
One fresh independent plan review before source implementation/real preflight.
Preserve pre-edit sources and actual controls; build using existing Make targets
and necessary snapshot trace recipes in owned TEMP. Exact source-native full
wrapper /usr/bin/python3 TEMP/run.py full, with all model drivers from
TEMP/runtime/bin/python and fixed references/snapshots. Freeze source/main,
environment, native flags and all15 expanded commands before full collection.

Complete same actual wrapper handle; no restart on an observation timeout.
Retain all raw requests/arrivals/outputs, CPU brackets/counters, actual child
terminal statuses and deviations. Record host before/during/mid/after, warnings
and faults without continuous isolation/harmlessness claims. Fresh independent
result review recomputes full raw effects, outputs, baseline engagement,
qualifications, observed model-round counts and instrumentation/scope limits.

Source editing/build/tests only original Workspace/main; preserve original
Coder/PVC/default qwen_graph.so/base packages/unrelated tools/setup_env.sh
and unowned vllm_graph_uring_loop_trace artifacts. Archive only scientific
sources/env/commands/data; omit vendor/runtime/ELFs and operational publication
helpers. Remove owned TEMP/named builds only after processes terminal/reviewer
release; archive replay must remain valid. Commit/push validated own main
work and verify actual public bytes. No new persistent service/schedule/setting.
Full goal stays active unless its actual requirements are proved.
