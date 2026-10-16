# 0076: current controller timing bounds the remaining speed gap

2026-10-16 UTC. [Complete result/raw matrix](../../bench/results/controller_stage_time_20261016/result.md),
[plan](../../bench/results/controller_stage_time_20261016/plan.md),
[independent review](../../bench/results/controller_stage_time_20261016/result-review.md).

The five-block, four-condition Qwen192/s diagnostic completes230400 successful
requests/14745600 measured tokens. Instrumented loop active GPU dispatch is
1.276us/launch higher than instrumented same-executor native
[1.154,1.398], nominal paired95%. Outside-dispatch is2.628us higher
[1.133,4.124], but includes model/head/scheduling and unbracketed work.

Ordinary loop delivers11620.739 versus native11645.377tokens/s:
difference-24.638[-30.620,-18.657]. Mean cell completionP99 is3430.177 versus
3299.484ms, difference+130.692[102.014,159.370]ms. Receive-gapP99 difference
+0.336[-0.399,1.070]ms is inconclusive. Owned group CPU0.638/0.801ms perattempt
is lower for loop, not evidence of speed or exclusive total-resource savings.

Instrumentation itself reduces TPS by44.787 loop/34.735 native; this material
perturbation prevents ordinary root-cause allocation from the timed primary.
The independent GPU network CTA overlaps dispatch/model. Its connection/reply
residence cannot be added to request latency or historical6.36ms; that old
condition still does not reproduce. Shared-resource/mapped-memory/trajectory
effects remain competing explanations.

All10 instrumented cells pass finite dual replay (7372880tokens including80
warmups), clock/count/coverage checks. All1051 pool disagreements remain;
untraced exact fidelity is not claimed. Archived CPU replay is byte-identical,
fresh review finds no blocker for the narrow diagnostic, and actual client
Job/Pod cleanup plus original-session/source preservation is recorded.

Keep selected0074. The next useful discriminator changes concrete network
control placement with identical GPU computation and ordinary matched controls.
[Kernel-owned network engineering](../../bench/results/controller_stage_time_20261016/kernel_owned_build_checks/engineering.md)
now compiles and passes matching8/16 verifier-only loads, with no GPU I/O CTA
and identical1464-instruction dispatch at each capacity. It has not attached,
served TCP, passed model/lifetime checks or shown speedup, and is unselected.
No model-kernel rewrite, new default, arbitrary-plugin or novelty claim follows.
