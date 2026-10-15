# Complete fair native admission comparison

All20 executors/40cells terminate successfully at2026-10-15T13:20:13.202909UTC.
Both models/paths complete10,240 measured requests,zero failures and655,360
checked measured output tokens,plus160 gen1 warmups.
The new per-model96/s connect-inclusive TTFT-P99 primary remains inconclusive:
kernel-minus-native+26.113ms [-121.273,173.499] Qwen and
+14.573ms [-26.449,55.596] Smol,nominal paired t95df4.
This does not relabel finding0062's original64/s primary or prove equivalence.
See [finding0063](../../../docs/findings/0063-fair-native-admission.md).

## Experiment and executable sources

[plan.md](plan.md) and [plan-review.md](plan-review.md) preserve the single
reviewed comparison. candidate/ is a source snapshot,not a checkout;
native_fifo.diff replaces native FD-priority publication with eligible-frame FIFO.
The kernel loop,FP16 upstream vLLM graphs,weights,KV layout,eight banks,packed
prefill and FIFO prefix release are unchanged from production70988bed.
The native candidate remains unselected in ordinary application source.

Rates64/96,256 gen64 attempts/cell,five paired blocks/model,alternating path order
and rotating rate order use identical normalized gamma(shape1) arrival schedules.
The actual client creates uncapped independent Python request threads.
Native retains one active response/connection and uncapped buffering; kernel
has finite4096 admission FIFO. Performance traffic has one request/connection.
Both queues engage and clear; the policies align fairness class,not exact
ingress order or every protocol condition.

In the original bpfusion-dev Workspace,the recorded recipe is
/usr/bin/python3 -u run.py,which sequences setup.py,qualification.py,preflight.py,
full.py. Rebind recorded owned temporary source/build/output paths to a new
owned test directory before an intentional rerun; do not launch against another
live experiment. setup.py uses pinned dependencies,normal Makefile rules with
candidate source inputs first,and one private BUILD path. Build logs show actual
bindings. No model/host tuning or module/ABI change is introduced.

## Evidence and replay

full_completion.json gives exact coverage/queue peaks; full_qwen.jsonl and
full_smol.jsonl retain every request,arrival schedule,process/log/counter and
terminal. Adjacent GPU histories and independent upstream references preserve
wire/history fidelity. BF_TRACE numerical-history overflow is zero; bounded
reply diagnostic overflow is a separate expected counter.

Recompute full_qwen/smol and preflight_qwen with
/usr/bin/python3 analyze.py FILE.jsonl.
Recompute protocol_qwen/smol with
/usr/bin/python3 protocol_analysis.py FILE.jsonl.
cpu_replay_full.json confirms all five copied fixed stdout files match bytewise.
Run /usr/bin/python3 admission_order.py . for client-stamp admission diagnostics.
Its inherited output scope says post-review; in this follow-up the plan already
names this diagnostic,and it runs after collection before the fresh result review.
It is not exact ingress ordering,queue residence or a new primary metric.

The user-requested generation-stall supplement is
/usr/bin/python3 tail_summary.py . .
It uses saved client recv timestamps. Same-recv token IDs share timestamps;
gaps include client scheduling/network buffering,not pure GPU decode time.
The output distinguishes token-weighted gap quantiles from request-weighted
maximum-gap quantiles,with all failure denominators.
It is exploratory,not a mid-run change to primary metrics.

plot_results.py uses complete fixed analyses,shows every block and mean block
P99/P50 statistics,and exports PNG/PDF/data.json. Matplotlib is installed only
after full terminal with no changed existing measurement dependency
(plot_dependency.json). figure_qa.json records a90dpi identical-source visual
preview; canonical PNG is170dpi. Five pairs and256 requests/cell do not support
a stable population tail,P99.9,production SLO or equivalence claim.

## Qualification and host boundaries

Qualification completes all5 commands: two actual idle/shutdown cases,four
640-outcome protocol executors totaling2560 outcomes/93,504 replayed tokens,
including1036 intended rejections,and both retained32-action native lifecycle
cases. These include partial/canceled observations and do not newly qualify
large queued-backlog cancellation. Real preflight attempt1 completes128 measured
requests/8192 tokens plus16 warmups; both queues peak16 and drain.

Host receipts name their exact phases. Smol short ownership sample is inside
pair2/kernel64 measurement. Qwen short sample is0.682474s after sampled cells.
The after receipt is58.553113s after full terminal,with no GPU app then,same boot
and the same56 selected historical fault lines. Ambient CPU activity belongs
partly to another Workspace; no foreign workload or host setting is changed.
Sparse observations cannot certify continuous GPU isolation or all-fault absence.

The original Workspace sessions,unowned tools/setup_env.sh,eight recorded
setup/build artifacts,base packages and cached weights are preserved.
restoration_before_cleanup.json records exact checks.
[result-review.md](result-review.md) finds valid supporting evidence and an
inconclusive hypothesis; it independently recomputes metrics,whole histories
and both supplements. [final_restoration.json](final_restoration.json) records
owned runtime/build removal after no active user remained and seven byte-equal
CPU replays without the original temporary directory. Production sources remain
unchanged. No new GPU experiment or favorable rerun is implied by this result.
