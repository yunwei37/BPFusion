# Experiment Plan: Drain completed replies before fresh model admission

## Research Question
Retain the user objective: complete Linux TCP/HTTP/eBPF/shared queue/resident real-model/async kernel TCP TX without a steady userspace request worker, and improve latency/TPS with reused computation. The repository has no formal paper RQ; do not invent or rename one. Existing docs/evaluation.md and findings0051/0052 retain this question. Test whether final-response CQ progression, rather than SQ consumption alone, materially explains the remaining vLLM short-output native gap.

## Paper-Value Admission
Planned role: supporting. Finding0052 closes the unchanged SQ-only matrix: vLLM Smol/Qwen gen1/c8 TTFT falls6.99/8.60 to5.09/6.88ms but native remains1.97/2.51. Stronger portable AMK transfer fails; its source was restored, so no AMK rerun/arithmetic campaign.

The largest credible story is a reused-compute GPU serving policy that repairs client-feedback/model-admission coupling without a new worker or fixed batching delay. Native delivery still wins decisively; this is the load-bearing remaining performance boundary. Current source holds the last token unless r.seq==next_final and advances next_final only after final SEND/abort CQ, while coalesced parent progression stops during model children. SQ consumption alone does not ensure those completions are drained. Finding0052's ordinary single-process short observations show old/current/native rounds26/9/8 Smol and26/21/8 Qwen, but trace changes current rounds to19/14. These observations identify an unresolved scheduling relation; they do not prove full-matrix mediation.

This is a new completion-frontier intervention, not a repeated unchanged matrix. A positive result selects a narrow policy with lower client TTFT and authenticated ordinary short-process model-round counts; a negative/mixed result retains a response-completion/fairness or workload boundary and rejects promotion as appropriate. Reduced rounds without latency improvement would reject the performance prediction; latency improvement without reduced rounds would leave that mechanism unsupported. No result proves pure PCIe cost, arbitrary models or formal causal mediation.

The best competing next experiment is removing global final-send serialization. That has broader slot-wrap/FIFO/ownership implications (the existing comment records why it was introduced) and is a larger correctness change. Progressing the existing ordered completed replies before admitting fresh model work preserves that ownership mechanism and directly discriminates whether this coupling is sufficient. It outranks another literature sweep, unchanged network rerun, generic API packaging or model arithmetic optimization for this measured boundary.

## Expected And Alternative Outcomes
Expected: at retired==seen, draining previously completed replies before fresh model admission reduces excess ordinary gen1/c8 model rounds and client TTFT relative to current SQ-only coalescing. Native may still win; all transfer costs remain visible.
Alternative: kernel/CQ timing or parent resource constraints dominate; waiting for all completed reply CQ adds serial delay/backpressure costs without meaningful improvement. Long-output TPS or c1 latency can worsen.
Contradiction: primary TTFT does not improve versus current, or improves while model-round counts do not decrease; distinguish those judgments. Do not manufacture a throughput/noninferiority threshold.

## Published Precedent And Real Assets
Reuse source-native io_uring/BPF transport, matched_serving.py, official optimized vLLM graphs/head, client metric formulas and source-native protocol/lifecycle/replay. Official client metric terminology: https://docs.vllm.ai/en/stable/benchmarking/cli/ . Linux submission/completion are separate states; upstream https://github.com/torvalds/linux/blob/master/io_uring/io_uring.c is context, not installed-version identity proof.

Original yunwei356/bpfusion-dev/main, lab RTX5090/170SMs, qualified Linux7.3rc3 and driver610.57.04. Common temporary Torch2.13+cu129/Transformers5.17/vLLM0.31/libbpf1.6.3; Smol135M93efa2f0 and Qwen0.5B7ae55760 FP16 with unchanged BF_PAD_PREFILL/BF_PREFIX_RELEASE, KV/greedy-head choices and frozen0045 whole-output pools. AMK/current/default source and base runtime remain untouched.

## Comparison
Actual intervention only in existing vLLM BF_IO_COALESCED hook after io_progress:
 if(c->retired==c->seen &&
    (io_state->next_final!=c->retired ||
     io_load(io_state->ring.head)!=io_load(io_state->ring.tail)))continue;

Model Control and IoState count the same zero-based admitted FIFO sequences; Control.retired publishes DONE, next_final advances at final send/abort CQ. Test/inspect the invariant, do not infer released TX ownership from model retirement. Use equality/inequality for these existing unsigned counters, not an unproved ordered rollover comparison.

Existing unfinished admitted computation remains eligible because retired!=seen. Only fresh model admission when all admitted work is complete waits. Stop is revisited every iteration. This waits for already-completed response CQ plus existing SQ-consumption, not peer TCP ACK or every pending accept/recv. A stalled/backpressured final send can delay fresh admission until stop; finite tests do not prove arbitrary fairness/bounded tail latency. No fixed batching delay/minimum, timer, page/protocol ABI, target, runtime knob, extra GPU CTA, userspace worker or model arithmetic change.

One strongest main competitor: efficient native timed epoll TCP with identical per-model resident computation. Native wins/matches reject superiority. Fresh matched numbers are necessary for the changed scheduling condition; citations cannot estimate its effect.
One component control: captured current f232b475 coalesced SQ-only source/binaries reconstructed as *_uring_loop_coalesced_original under captured identical flags/SASS. This is not SOTA. Candidate uses existing coalesced entrypoint. No fourth old worker path and no AMK timing rows. Those closed comparisons are cited.
Identical code/precision/packing/KV does not imply identical realized batches. Native/full/default source remains unchanged. Freeze source/main/environment/commands before collection and retain all adverse results.

## Workloads And Metrics
Two vLLM models; same four literal prompts, gen1/64 and c1/c8,32 requests/cell. Five paired process blocks use five of six path permutations and odd model/cell reversal; residual order/drift remains uncontrolled. Fixed finite persistent localhost token-ID HTTP waves, not standard text-serving/capacity/SLO/total-CPU/general-model evaluation.

Primary: gen1/c8 client TTFT candidate-minus-current and candidate-minus-native, using paired t95df4 with blocks as uncertainty units. All signed block values remain.
Secondary mechanism: measured model rounds in the SAME ordinary gen1/c8 processes, total device_graph_launches minus exactly8 sequential checked c1/gen1 warmups. Every valid gen1 request computes once and bootstrap graph capture does not increment this Control; verify semantic count and complete replies. This authenticates an aggregate for each primary process, not its batch membership/GPU time or isolated mediation.
Efficiency/transfer: gen64/c8 TPS, gen1/c1 TTFT, gen64/c1, completion/TPOT and known-worker CPU brackets. Process clocks include attributed syscall time; unaccounted kernel/BPF/softirq/client work and energy remain excluded.

To obtain ordinary per-primary counts without BF_TRACE, split the existing four-cell collection into two source-native literal adapters: short_serving.py matrix=((1,8),), transfer_serving.py matrix=((1,1),(64,1),(64,8)). Each has8 sequential warmups/process. No new experiment-control interface or instrumentation; only declared source-native workload subsets. Run contexts short then transfer in even blocks, reverse in odd; models reverse in odd. The same gen1/c8 primary data supplies latency and round counts, so no separate redundant timing/trace observation is added.

Correctness: unchanged pre-observation finite whole-sequence pools for ordinary outputs, source-native candidate traced protocol with independent packed/KV/history replay of reused graphs (not a fresh eager-HF arithmetic oracle), buffer/FIFO/peer generation/slot/SQ/CQ shutdown checks. Existing stronger AMK eager-HF failure remains failed. Do not widen the pool/formula/oracle after seeing candidate output.

## Planned Runs
| Run group | Role | Workload | Paths | Repetitions | Decision consequence |
|---|---|---|---|---:|---|
| Short ordinary | primary plus aggregate mechanism |2 models, gen1/c8,32 req |old SQ-only/native/new drain |5 paired blocks |TTFT difference and SAME-process model rounds |
| Transfer ordinary | efficiency/transfer |2 models, gen1/c1,gen64/c1,gen64/c8,32 req/cell |same3 paths |5 paired blocks |retain latency/TPS/CPU tradeoffs |
| Real preflight | dependency |both literal contexts,8 req/cell |same3 paths |one initial attempt |path/metric/oracle executability |
| Selected protocol/lifecycle | dependency |2 candidate models, existing cases |candidate existing entrypoints |one set |finite ownership/stop correctness |

Full:20 driver calls/60 executors/120 cells/3840 measured requests124800 tokens +480 excluded warmups (4320 complete replies125280 tokens). Short:30 executors960 measured requests/tokens+240 warmups. Transfer:30 executors2880 measured requests123840 tokens+240 warmups. Startup/warm cost differs from0052; do not substitute a historical delta. Cost is one bounded full integrated experiment, roughly tens of minutes on original hardware; all terminal statuses, warmups and host brackets are retained.

## Execution
Authoritative command: /usr/bin/python3 TEMP/run.py full; model drivers TEMP/runtime/bin/python TEMP/short_serving.py or transfer_serving.py with existing --backend vllm --block N --loop-comparison --untraced --reference-path --model --output. All20 exact expanded commands declared before collection.
Necessary adapters/wrapper/reanalysis/control build recipes will be materialized before execution and inspected as part of real preflight. No production edit/real preflight before fresh independent plan review.
Real preflight uses both models/contexts/three paths,8 requests/cell:12 executors24 cells192 measured requests6240 tokens+96 warmups. Preserve failures; maximum three actual preflight attempts under the owning skill without oracle relaxation.
Protocol each candidate622 requests22224 tokens/259 rejects+5000 empty connections. Two existing32-action lifecycle workloads/652 checked complete-or-prefix tokens each cover idle, RST/reuse, inflight stop, pending accept/recv, and independent model/slot/SQ/CQ emptiness. These do not certify worst-case stalled-peer fairness.
Full completion: same actual wrapper handle to terminal with every declared driver/cell completed; no restart on observer timeout. Raw files, stdout/stderr, original and candidate sources, actual binaries' original reconstruction receipts, command/env/package metadata and all negative rows remain. Source/control/performance check uses actual system, no toy trace.
Read actual host before/during/mid/after including warning history; do not infer continuous isolation/harmlessness. Fresh independent result review after full completion recomputes raw effects, counts, baseline engagement, source invariants, qualifications and limits. Then select/publish validated own main code/docs/results and verify public bytes; cleanup only owned artifacts after release/archive/replay.

## Interpretation
Positive: supported local ordinary TTFT improvement vs current, counts independently support fewer rounds in the exact primary processes; native comparison decides superiority. No automatic universal/default promotion.
Negative: retain metric/counter evidence and reject that component prediction; bound completion policy rather than rewrite the retained objective. A useful distinct redesign is optional and must outrank alternatives.
Mixed/inconclusive: retain all metric contrasts; crossing-zero does not prove equivalence/NI. Counters improving alone do not replace client TTFT. Any correctness/comparison-invalid result is repaired only while scientifically useful, without weakening its fixed checks.
Target table: two-model prior/native/candidate primary TTFT/model rounds plus transfer TPS/c1 and signed t95 effects, exact sources and selected scope. Full retained objective remains active until its actual requirements pass.

## Reproducibility Notes
Source/base f232b475; exact source snapshots/candidate.diff and all20 commands precede full collection. Reuse original Workspace/main/PVC/default qwen_graph.so/Coder PIDs1/10909, base2.14.1+cu130/5.19.0/2.5.3, unrelated tools/setup_env.sh and four unowned vllm_graph_uring_loop_trace artifacts. Source/build/tests only matching original Workspace/main; no new branch/checkout, permanent service/schedule/config/model setting or credential boundary. Owned temporary runtime/vendor/builds removed only after terminal/review release and CPU-only archive replay.