# Execution notes

2026-10-15T05:53:58.100216+00:00

Before any setup or GPU observation, preserve the after-submit variant on its existing fixed timer to avoid the reviewer ordering counterexample. Existing macro guards all new GPU adaptive state, updates and acknowledgements there. The default before-submit candidate remains the admitted intervention. Correct the plan client timeout from an erroneous15s description to actual source-native60s; only the independent empty deadline case has a fixed15s post-ready observation bound.

2026-10-15T06:12:11.649548+00:00

Private setup/build exits0. First real preflight completes idle2s service with zero requests and normal cleanup; observed ready-to-Python-process-exit7.034972425s includes native stop plus upstream replay/teardown and is not a seven-second native deadline. All three Qwen paths complete72requests2088tokens each (64measured/2080tokens plus8warmups),216requests6264tokens total; exact independent graph/history replay and CPU analysis exit0. No preflight rerun, oracle/timeout change or output failure. Qualification launched through the same run.py; its lifecycle source remains byte-identical0058, with its existing15s sockets/30s communicate unchanged and explicitly separate from main serving60s clients.

2026-10-15T06:15:50.968793+00:00

Qualification attempt1 fails helper-thread stop liveness: all622 replies complete at06:12:35UTC, but main io_uring_enter remains asleep after helper SIGTERM. Preserve status/fdinfo/tasks and raw logs. Stop only qualification wrapper and send main-thread SIGTERM to its known executor for cleanup. Any subsequent driver PASS is manually assisted and is invalid as a natural lifecycle pass; no full performance matrix launches from it. Investigate and fix source wakeup, then rerun affected checks under distinct output names.

2026-10-15T06:17:12.697115+00:00

Repair helper-thread shutdown by recording the actual io_uring wait-owner TID and forwarding SIGTERM to that TID only when shutdown arrives on another thread. The existing after-submit variant remains excluded from all adaptive additions. Main serving computation/active timer/metrics/oracle/timeouts unchanged. Preserve first source in io_uring_tcp.before_signal_fix.h and run_attempt1.py. Repaired qualification has distinct paths; lifecycle adapter changes only its output directory name. No performance full cells were observed before the repair.

2026-10-15T06:18:44.778322+00:00

Add standard strace -ttt timestamps to repaired protocol runs so helper-to-owner signal forwarding and subsequent native cleanup can be independently timed. This is syscall evidence only; full performance cells do not use strace. Prior serving adapter preserved as serving_attempt1.py. No timeout or correctness assertion changes.

2026-10-15T06:30:26.854151+00:00

Baseline scope audit before full: current native userspace_tcp.h uses epoll_pwait2 with a fixed60000ns timeout even while idle, matching its established constructor. Its exact header is preserved. Native comparisons therefore concern this current timed-epoll implementation, not an unmeasured adaptive/event-driven native implementation, and cannot establish that idle CPU savings uniquely require eBPF. The predeclared primary remains adaptive minus original fixed-loop process CPU; latency/throughput tradeoffs and strongest currently runnable native delivery remain visible. No baseline behavior or matrix changed.

2026-10-15T06:32:11.358812+00:00

Repaired qualification terminal0: Qwen and Smol each622protocol requests22224tokens with exact independent history replay, all batches1..8 and natural helper-stop forwarding; each32-action lifecycle passes unchanged frozen complete/prefix checks, all13connections closed and independently emptySQ/CQ, error/pending/reserved/drop/overflow0. First manually assisted attempt remains failed stop-liveness evidence. Full30executor/60cell matrix launched06:30:47.875567UTC under PID515684/start47721987. Early host06:31:29.517814UTC maps hostGPU2600132 to original containerPID515761, sameboot and56selected historical warnings; sample is bootstrap, not continuous isolation proof. No full conclusion, default selection or commit yet. Continue observing same handle; after terminal do independent result review, affected constructor regressions if retaining, honest archive/restoration/docs/main publication. Do not restart or delete live runtime.

2026-10-15T06:57:35.112769+00:00

Full terminal at06:55:14.755647UTC: both model drivers and fixed analyses exit0;30executors60cells1920measured requests62400tokens plus240warmups. No full serving failure/exclusion/replacement/retry or oracle/metric/timeout change. Source-byte checks preserve actual driver/model/client versions. Source-native HF/coalesced/after compatibility adapters prepared only; no additional compile or GPU run overlaps full, and no compatibility pass is claimed. Fresh independent result review started after full terminal; retain all signed adverse rows and partialCPU scope. Selection remains pending.

2026-10-15T07:05:41.765676+00:00

Restore only three owned candidate production paths byte-for-byte from frozen HEAD, after checking current bytes match production-candidate. Archive true production-original and production-patch separately from existing private path-rewrite snapshots/diff. Retain valid related-work update. Candidate is not selected: supported process CPU reduction has mixed delivery, including adverse Smol achieved burst TPS. Prepared HF/coalesced/after adapters are not executed or claimed qualified.
