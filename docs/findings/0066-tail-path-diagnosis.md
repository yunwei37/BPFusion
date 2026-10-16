# Qwen tail-path diagnosis and unsuccessful close-scan repair

A token-associated timeline locates GPU I/O iteration, submission-thread
runnable waiting and client delivery/observation delay. SEND operations in
the diagnostic are not queued to io-wq; kernel submit-to-CQ P99 is about0.11ms.
Softirq events are exposure, not an exclusive allocation of service CPU.
Marginal stage P99s cannot be added to divide the historical6.36ms difference.
The [diagnostic](../../bench/results/tail_path_20261016/diagnostic-result.md)
and [independent review](../../bench/results/tail_path_20261016/diagnostic-result-review.md)
retain clock uncertainty, negative residuals, full byte joins, failed trace
buffer capture and its complete rerun.

A conservative per-scan memoization avoids repeated host-mapped close checks
after the global admission condition first fails. It passes two models'
default8 protocol and ordinary cancellation checks, but its complete matched
five-block confirmation does not establish a performance benefit.
Qwen192 after-before ITLP99 is-0.167588[-1.533927,+1.198750]ms.
Before/candidate/native block-mean P99 is4.608/4.441/4.718ms; the unchanged
before path already lacks the old14.723/8.363 gap. Do not attribute the
cross-run reduction to the candidate. **The close-scan source is not adopted.**

All15 executors/30 cells,7680 requests and491520 measured tokens complete with
exact dual replay and no failures. Candidate-native process CPU is adverse,
+0.258141[+0.177460,+0.338822]ms/request at192, excluding full kernel/GPU cost.
See the [complete result](../../bench/results/tail_path_20261016/confirmation-result.md),
[fresh review](../../bench/results/tail_path_20261016/confirmation-result-review.md),
and [raw/replay](../../bench/results/tail_path_20261016/confirmation/).
This is supporting mechanism/workload boundary evidence, not an eBPF latency
or throughput win. Complete resource, remote and current official-reference
measurements remain separate work.
