# Adaptive wait plan review

Fresh reviewer, round 1, 2026-10-15 UTC. Reviewed original Workspace main worktree and /tmp/bpfusion-adaptive-wait-nwu1nulh/plan.md, three actual source diffs and snapshots, existing bench/vllm_serving.py and resident_dispatch.py, Makefile target selection, findings0055-0059, and official Linux v7.3-rc3 io_uring/loop.c and timeout.c. This reviewer edits only this report.

## Current status

Scientific admission passes for a supporting, finite bursty process-CPU comparison. The default before-submit handshake has no identified source-level blocker on the actual x86 host, subject to real preflight and declared protocol/lifecycle checks. Executable review remains pending until private Makefile/runtime/serving adapters exist and are inspected. This is not permission to run or a production-selection verdict.

## Admission and comparison

The existing evidence cannot estimate CPU savings from eliminating fixed60us idle timeout wakeups: earlier runs lack the intervention and fixed quiet gaps. The tested uncertainty includes the cost of CQ acknowledgements while active, so an adaptive timeout is not automatically a delivered improvement merely because it suppresses idle ticks. Positive and negative outcomes change whether this source-local mechanism should be retained; neither establishes generic eBPF superiority. The stronger alternative of total-system CPU/offered-load/SLO measurement remains important, but current host totals cannot exclusively attribute unrelated load. The mechanism comparison is reasonable supporting work, and should not be presented as the completed whole-service CPU or latency goal.

The fixed-timer original is correctly a component ablation, and efficient native TCP is the one credible main competing mechanism. Identical optimized default FP16 graph computation in all three conditions is appropriate. Native matching or winning must remain visible. No extra weak baseline or wider workload is needed to admit this finite hypothesis.

Process CPU seconds/request uses the existing POSIX process clock and includes executor threads and syscall work charged there, while excluding parts of RX/softirq/io-wq/other kernel work. The plan correctly avoids calling this total CPU or energy. TTFT/completion/TPOT are standard client delivery metrics; achieved tokens/s includes the fixed gaps and is not saturated throughput. Five paired process blocks and a signed t95 interval are defensible for this scope; a crossing-zero interval is inconclusive, not equivalence. The four-wave, two-cell, two-model matrix is coherent, and counts recompute to30executors,60cells,1920measured requests,62400tokens plus240warmups.

## Fidelity

Using BF_TRACE in every compared condition and reconstructing expected tokens via independent upstream graph/KV/history replay is a legitimate comparison with clearly restricted scope. It does not repair0058's untraced frozen-pool failure, and cannot support ordinary untraced fidelity. The existing serving driver matches all client markers/prompts/gen/rejection flags and exact output tokens to references, requires zero model trace overflow, verifies loop network syscall absence, final ring draining, free physical slots, and executor terminal success. The independent replay implementation must remain unchanged in the adapter except path redirection.

## Source semantics and identified issue

The default branch snapshots CQ tail before submitting SQEs. While timer_may_idle is true, an unacknowledged CQ tail yields no sleep, allowing GPU processing and subsequent SQ publication to precede cq_seen. GPU SQ publication precedes io_acknowledge via the system fence and release store, including coalesced io_publish. If an idle transition races an earlier false flag snapshot, the update CQE occurs after the pre-submit CQ snapshot and wakes/re-enters the loop. This is a plausible lost-wakeup closure on the actual x86/CUDA system; it needs the declared real tests and is not a cross-architecture memory-model proof.

The same argument does not hold for BF_IO_CQ_AFTER_SUBMIT as currently patched. Concrete interleaving:
1. BPF reads timer_may_idle=0.
2. GPU decides idle, publishes timer_may_idle=1 and the long-timeout update SQE.
3. BPF samples SQ tail and submits that update, possibly an accept/recv as well.
4. Its after-submit CQ-tail snapshot includes the update and network completion.
5. Because the cached may_idle is0, it requests observed+1 and can sleep.
6. GPU consumes those completions, publishes the next recv/send/active-timer update SQE and acknowledges, but SQ publication is not itself a kernel wakeup. The next timer CQ may be delayed until the service deadline.

With the fixed60us timer this constructor's old lost-wakeup window was bounded by the next tick; changing that tick to a long idle interval changes its consequence. This is a production-selection blocker for a shared patch affecting the after variant, not an automatic reason to reject the default-before matrix. Resolve it in source or explicitly preserve the original after behavior and limit claims. A few passing regressions alone cannot refute this ordering counterexample.

Official timeout.c confirms TIMEOUT_UPDATE parses addr2 (SQE off), preserves the target multishot operation, produces its own completion, and returns ENOENT/EALREADY when the target is transiently absent/running. The candidate allows one update at a time, so its timespec buffer is not overwritten until that update has completed parsing. The persistent timeout retains one pending count until a final non-MORE CQE; update/removal completions own separate counts. New updates are suppressed after stopping; cancel-all and the existing timeout-remove fallback remain. No source-level counter lifetime defect was identified in those paths.

Remaining relative deadline is computed from BPF's most recently published now_ns, not from the instant the kernel applies the update. Some overshoot from publication/submission delay is possible. The plan tests natural idle expiration rather than claiming an exact deadline bound; report the actual overshoot if material, and do not extend client timeouts to make a hang pass.

## Executability items to inspect

Private source/header resolution must ensure baseline binaries do not include candidate headers accidentally; paired BPF object paths must match each binary. Runtime dependencies and model revision need ordinary recorded provenance. Wave timing/connection lifetime, CPU snapshots across the quiet gaps, exact cell indexing, analysis pairing and complete matrix checks need source inspection once adapters exist.

The plan currently says existing15s client/socket timeout, whereas resident_dispatch.connect sets60s. This is a concrete mismatch to settle before execution: make the private adapter use the declared15s, or correct the plan to the actual fixed timeout before observing results. Keep the check fixed thereafter.

HF/coalesced/after compatibility is conditional on selecting a shared production change, not evidence supplied by the main vLLM matrix. Broad backend claims remain unsupported without affected regression checks.

## Optional suggestions

Report actual active/idle timing and which requests define the predeclared cold subset so gap accounting is auditable. This is clarification, not a demand for more conditions. Preserve absolute candidate-original and candidate-native CPU and delivery effects together; selecting a lower process cost does not establish lower whole-service cost.


## Pre-execution scope correction inspected

Before any setup or observation, the owner revised the same candidate and plan. Inspection of refreshed snapshots/diffs confirms BF_IO_CQ_AFTER_SUBMIT keeps its original fixed timer and wait expression. Added GPU adaptive state, update completion handling, timer updates and CQ acknowledgements are excluded under that existing macro; the BPF side also excludes new shared-field reads/writes. The shared control struct still grows, so matching source/header rebuild remains necessary, but no adaptive-after behavior is selected. This resolves the identified after-submit issue by preserving its old mechanism and limiting adaptive claims to before-submit, without inventing another flag.

The plan now accurately fixes source-native socket timeout at60s before execution, and separately fixes the actual-model empty2s service-deadline test at a15s post-ready observation bound. The earlier timeout mismatch is resolved. Executable adapters are still being prepared, so their review remains pending.


## Executable review completed before setup

Inspected setup.py, run.py, the full serving.py and its diff, full analysis.py and diff, idle_deadline.py, lifecycle.py, models.json, both private Makefiles, private CU/header path resolution and model snapshot existence. Parsed all six Python scripts with ast.parse without executing setup, builds, models or experiment stages. At inspection, runtime and setup.exit.json do not yet exist. Both private model CU files are byte-identical to current unchanged executor/vllm_graph.cu; the actual intervention remains network-only.

Source/build isolation is adequate for the explicit targets used here. Quoted io_uring_tcp.h resolves next to each private CU, and the private queue header is the first include path for both CUDA and BPF builds. The private io_uring header redirects its object pathname to the matching original-build or candidate-build. Native is built from the original CU and queue header. Common model bootstrap is the unchanged source-native symlink path. The Makefile's broad path replacement would not make it a generally correct replacement for all targets (its BPF_SRCS transformation is not useful outside the selected explicit targets), but this does not invalidate the explicitly named serving/BPF targets in setup.py. Do not describe that private Makefile as a new general build system.

setup.py pins the declared vLLM/Torch/Transformers/NumPy runtime, builds the private libbpf, records commands/status/packages and preserves original8build/setup metadata, base package versions and Coder process state. Actual build success and dependency resolution remain real-preflight facts, not proved by source inspection.

The serving adapter uses the three declared modes, two cells, five process blocks, and process-order permutations; correctness uses candidate only. Each measured cell opens fresh connections/threads for each of four waves, sends8requests per wave with the existing barrier, and sleeps1s after each of the first three waves. Gen1/c1 has eight sequential requests; gen64/c8 has one per lane. CPU sampling begins before first-wave connection setup and ends after last-wave clients close, so it includes connection management and all three quiet gaps. This is correctly executor-process CPU per delivered request, not isolated timeout handler cost. Achieved wall TPS runs from the first sent request to final token and includes the three quiet gaps, while excluding initial connection setup. Keep these distinct measurement windows explicit in results.

The analyzer verifies executor success, independent reference marker/token matching, model trace capacity, FIFO slot ownership/release and ring lifetime; recomputes latency/TPOT from client timestamps; requires every index0..31 in each measured cell, four wave records and three at-least1s gaps; verifies all three mode orders and all five block pairings; recomputes CPU deltas and emits candidate-minus-baseline effects with df4 t95 intervals. Thus it does not infer a completed matrix from a partial prefix. The runner checks serving and analysis exits, lifecycle pass booleans and expected command counts before its terminal success. A failing lifecycle driver's nominal process exit0 cannot be mistaken for a pass because run.py separately inspects its result pass field.

The empty-deadline check actually loads the Qwen model/candidate path, requests a2s service duration, waits at most15s after observed readiness, requires no admissions and completely drained successful shutdown, and preserves a hang/failure. Its15s is an observation/cleanup bound, not a claim that the server meets a precise2s deadline. Main serving retains source-native60s sockets, while the independently reused lifecycle retains its existing15s sockets; these distinct checks are fixed before observation.

lifecycle.py is byte-for-byte equal to the archived0058 lifecycle source, including its frozen complete/prefix membership oracle, eight2.2s idle-before-request probes, rejection/reuse, reset after a token, and in-flight signal stop. It does not enlarge the old reference pools. A default-mode frozen-pool mismatch remains a failure and may prevent this candidate's qualification; it must not be reclassified as expected simply because the trace-based main matrix has a stronger reference method. This lifecycle path is an additional finite shutdown/protocol control and does not close0058's unresolved ordinary fidelity gap. The prior source-native independent replay code was inspected directly: it builds request histories from independently recomputed upstream outputs, asserts each against trace tokens, then emits the references used to compare served outputs.

No scientific or executable blocker remains for the revised default-before-submit experiment as written. Verdict: PASS for proceeding to the declared real preflight, then qualification/full only on that path's successful correctness evidence. This is not a runtime correctness pass, a favorable result, authority to retain a production non-default, or broad HF/AMK/coalesced support proof. A selected shared production patch still needs the affected regression promised in the plan.

Nonblocking reporting clarification: the plan promises descriptive whole-host ticks, but serving.py currently records only the existing process clock/known TX counters. Sparse host receipts may provide global ticks separately; otherwise record this field as uncollected rather than inventing a total-host claim. This omission does not invalidate the predeclared primary process-CPU comparison. Likewise the optional cold subset has no adapter analysis yet; either derive the already-predeclared first-by-client-start request per wave from retained timestamps, or omit that optional subset. Neither requires another workload or a looser check.

## Final review judgments

- Admission: supporting, nonredundant evidence toward the retained serving objective.
- Hypothesis/primary metric: coherent finite bursty process-CPU intervention.
- Baseline fairness: strongest runnable native mechanism plus correctly labeled fixed-timer ablation.
- Correctness/oracle: source-native independent traced graph/history replay for the main comparison; unchanged finite frozen-prefix lifecycle controls.
- Source ordering: identified after-submit race resolved by preserving its original fixed-timer behavior; before-submit handshake remains to be tested.
- Execution/completion/uncertainty: adequate explicit commands and fixed matrix; partial failures cannot be promoted.
- Remaining blockers: none for revised preflight execution.
- Optional reporting: actual cold-subset definition if shown, separate CPU/TPS windows, missing descriptive host ticks if not collected, finite and traced scope throughout.

Primary source links used for this review: https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/io_uring/loop.c and https://raw.githubusercontent.com/torvalds/linux/v7.3-rc3/io_uring/timeout.c. Standard metric sources are linked in the plan. No external-source verbatim passages are reproduced here.


### Final nonblocking recording clarification closed

Before any execution, the owner added existing resident_dispatch.host_cpu_ticks sampling immediately before the process CPU window and as each cell is emitted. Fresh inspection confirms these raw before/after fields now exist in every cell and the updated serving.py still parses. They remain descriptive global counters, with no exclusive attribution or primary-metric substitution. This closes the earlier missing-host-ticks reporting note; verdict remains PASS for the declared real preflight.


## Final permitted follow-up: source-local helper-stop repair (round 3)

Reviewed after the actual first qualification attempt exposed a shutdown defect and before repaired qualification/full observation. This is the final permitted plan-review follow-up; it does not reset the review limit. Inspected qualification.helper_stop_failure.json, the first qualification raw tail and driver PASS, the before_signal_fix header against current production source, current private candidate header, run_attempt1.py/current run.py, lifecycle.py/lifecycle_repaired.py diff, current plan/execution notes and private rebuild script/status/stdout.

### Observed fault and evidence treatment

The saved receipt identifies executor513782's main thread sleeping in __io_run_loop, the signalled helper513787 in futex_do_wait, empty CQ/SQ with an outstanding operation, and622 completed replies. Helper SIGTERM was emitted06:12:35UTC; the owner observed the unresolved stop at06:15:50.968793UTC and explicitly sent a main-thread signal for cleanup after stopping only the stage wrapper. This supports a failed prompt helper-thread shutdown over that observed interval, not proof of an infinite hang beyond the service deadline. The subsequently successful output/token/ring checks and terminal exit0 are real but manually assisted. They cannot count as natural helper-stop/liveness success. Preserve both the raw PASS and the explicit invalid-liveness note; do not suppress the failure or present this attempt as fully valid qualification.

### Source repair

The repair addresses the source-visible wakeup problem: a helper-thread handler previously release-stored stop_requested without waking the thread actually asleep in io_uring. The new before-submit code records the actual uring_wait caller TID, release-stores stop_requested, and forwards SIGTERM using tgkill only when the handler runs on another TID. A handler on the owner TID does not forward again, avoiding recursion. Recording occurs before entering the wait loop; a signal before registration sets stopped and avoids that wait. TID remains available through drain and is cleared at finish alongside io_signal_control. The target is a specific same-process loop owner, not another service/session, and no steady request worker or persistent helper is added. The existing after-submit constructor excludes all new forwarding/TID behavior under its existing macro.

No new source-level blocker was identified on the current Linux/x86 target. The change needs real helper-stop and in-flight lifecycle qualification; source inspection alone cannot establish signal liveness. It does not change model computation, oracle, primary metric, active timer or client timeout. The original helper stopped flag and signal handler remain the same path. The documented failing first attempt remains an important mechanism boundary showing why suppressing idle CQEs requires an explicit stop wakeup.

### Affected rerun and executable review

run.py now uses qualification_repaired output names while preserving the original run_attempt1.py and failed outputs. Its correctness flag still selects the exact622-request candidate protocol path, and analysis exit is required. lifecycle_repaired.py differs only in the output directory prefix; its frozen complete/prefix oracle and existing timeouts remain byte-identical in meaning. The runner resolves repaired lifecycle result paths by the model suffix and checks the explicit pass boolean, so the lifecycle driver's nominal exit0 cannot silently hide a failure. Both revised Python files parse.

The private rebuild reuses the recorded candidate command/environment. candidate_signal_rebuild_status.json reports exit0 at06:18:08.020211UTC and stdout shows actual CUDA recompilation for both traced and lifecycle libraries. The private candidate header contains the TID repair and matching private BPF object paths. Full performance has not been collected from the earlier candidate, so there is no pre/post repair performance mixing to salvage. Repaired protocol/lifecycle checks for both models are the affected correctness path; earlier three-path preflight is setup evidence for the pre-repair candidate and must retain that version label.

### Final follow-up verdict

PASS for proceeding with the declared repaired qualification path and, only after valid unassisted correctness evidence, the unchanged full performance matrix. No remaining scientific or executable blocker identified in the inspected repair/runner. This verdict does not convert the failed first qualification to a valid run, predict a favorable performance result, or authorize another plan-review loop. Any unresolved blocker after this final review must be returned under the owning skill's review-limit rule rather than adding a new reviewer/round.

Research question, expected/contradictory outcomes, primary process-CPU metric, native competitor, fixed-timer ablation and fixed fidelity checks remain unchanged. This is a necessary source-local correctness repair within the admitted experiment, not a new scientific experiment or a weaker acceptance target.
