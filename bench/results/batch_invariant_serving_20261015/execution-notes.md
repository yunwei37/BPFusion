# Execution notes
Plan review completed before setup launch502540 at2026-10-15T04:35:48.543023UTC.
The list/tuple adapter comparison was repaired before any GPU observation.
After review and before reference/preflight, analysis.py also recomputes the
same single official-reference equality for traced qualification as well as
ordinary results. This duplicates the fixed driver assertion, changes no
expected token or pass criterion, and addresses the review's nonblocking
reproducibility suggestion. No observed output informed this change.
The initial host query04:33:41UTC was inspected in tool output; the separately
retained host_entry.json is04:34:45UTC. Both precede all GPU execution and show
no compute application, same boot and400W setting. Sparse endpoints are not
continuous isolation.
Stages are separate literal commands:
python3 run.py setup
python3 run.py reference
python3 run.py preflight
python3 run.py qualification
python3 run.py full
Only run each stage when its prior required stage succeeds.

Actual Qwen ordinary preflight took111.96s for two executors, dominated by
bootstrap and upstream warmup outside measured cells. A20-executor full matrix
therefore costs roughly20minutes plus qualification on this host; this is an
estimate, not a new timeout/deadline. Qwen complete traced qualification passed
both transports and independent analysis; Smol loop passed, native still live
at2026-10-15T04:57:21UTC. No performance inference follows these dependencies.

Full wrapper terminal2026-10-15T05:22:02.721225UTC, exit0; both model drivers
and fixed analyses exit0. Root observed terminal05:22:26UTC.
Post-run review noticed serving.py.diff and analysis.py.diff had been written
before the pre-observation repairs and were stale. They are regenerated
from the exact actual executed .py files against saved current-main sources;
no runtime source, expected token, analysis criterion or raw output changes.
Host after is05:23:18.874653UTC,76.153428s after wrapper terminal, no compute
app and same56selected historical warnings. Active receipts are matrix-active
sparse observations, not continuous perf-window isolation.
