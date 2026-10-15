# Fair native admission comparison — running

Checkpoint 2026-10-15T12:37:18.523819+00:00.

The plan and fresh independent round1 review admit a comparison of the unchanged
kernel FIFO loop with a stronger eligible-frame FIFO native competitor. All
model computation remains shared and unchanged. Main application behavior is
not changed by this archive; candidate/ is a source snapshot, not a checkout.

Setup/build exits0, all installed package versions match the preceding measured
environment (package_comparison.json is empty). Native idle deadline and
helper-thread shutdown dependencies both pass. The live original run is now
performing Qwen protocol qualification. Qualification as a whole, real preflight,
the full matrix and result review remain unfinished. No new performance result
is reported here and no partial prefix should be interpreted as the experiment.

## Question and sources

Does the previously observed high-load kernel P99 advantage survive removal of
the native FD-priority admission weakness? See plan.md and plan-review.md.
native_fifo.diff is the exact intended policy change; candidate/ contains actual
frozen inputs and Makefile bindings. The single main competitor uses identical
FP16 vLLM graphs, weights, KV setup, eight model banks and dispatcher.

New fixed primary: per-model connect-inclusive first-token P99 at96 requests/s;
64/s is secondary. Five paired blocks/model,256 attempts/cell,gen64:
20 executors,40 cells,10240 measured attempts,655360 requested output tokens
plus160 checked warmups. This new follow-up does not relabel finding0062's
original64/s primary. Failed primary requests censor superiority. Keep median,
completion,throughput,CPU,scheduling lag and all adverse outcomes.

FIFO is among complete eligible native frames in observed readiness order.
Native retains one in-flight response per connection; kernel pipeline behavior
differs. Performance traffic has one request per connection. This aligns the
fairness class for that workload, not every protocol or exact ingress order.
Client-stamp bypass diagnostics are not queue-residence timestamps. Native has
no artificial new buffering cap; the finite kernel queue can still overflow.

## Execution

All execution stays in the original bpfusion-dev Workspace. The single current
temporary directory is /tmp/bpfusion-fair-admission-yijz8oui; all.process.json
identifies its existing wrapper, which sequences setup -> qualification ->
preflight -> full. Do not launch another copy alongside it. Source scripts and
recorded temporary paths can be rebound to a new owned rerun directory after
the original reaches terminal. Use /usr/bin/python3 -u run.py with the pinned
dependencies and recorded cached model revisions. Root vmlinux and Python
bootstrap are reused; candidate include paths take precedence in actual builds.

The original Workspace sessions, unowned tools/setup_env.sh, eight recorded
setup/build artifacts, base packages and cached weights are preserved.
Runtime/build files and downloaded dependency trees are not archived.

## Evidence scope and next decision

Current idle receipts include upstream teardown and are not stop-latency SLOs.
Host snapshots and CPU/cgroup receipts describe their observation phases,
not continuous isolation. Workspace CPU has no hard quota; host load is shared.
No other Workspace or host setting was changed.

After complete qualification and real preflight, the original wrapper runs the
full fixed matrix. Full raw outputs, independent model-history/wire replay,
all analyses, queue engagement and a fresh result review are required before
interpretation or adoption. Preserve all failures and deviations. The full
retained project objective remains active.
