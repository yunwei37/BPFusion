# Small-graph network / CPU experiment

This experiment follows the completed LLM capacity comparison in
[0080](../../../docs/findings/0080-resident-queue-relief.md).
The [pre-acquisition plan](plan.md) and [owner-only design review](plan-review.md)
fix its scope, metrics, screen/confirmation selection and positive/negative exit.
No other agent participates.

The [coordinator](../../graph_network_client.py), [native worker](../../graph_network_client.cpp)
and [analysis](../../graph_network_analysis.py) retain fixed-format raw data.
[Format and recovery](native_client_format.md) document every byte/timestamp. The example captures unchanged upstream cuBLAS/
cuFFT, with optional repeated work. See the
[graph guide](../../../docs/graph-backends.md) for normal build, serve, client
and cleanup commands. Client runtime is Linux x86-64/Python3.12.12 plus the static native worker;
uvloop is not needed by the final client. Binary
requests/responses are280/256bytes and every observed output is checked.

Historical acquisition wrappers in this directory record the real original
Workspace/build/client paths. They are not portable installers and must not
be run beside another service sharing these pins/GPU/port. CPU affinity
changes only owned service threads; all original sessions/foreign work remain.

Calibration and finite numerical/lifecycle qualification precede performance.
Screen results cannot establish a benefit; confirmation_selection.json freezes
new seeds/selected cells before the five-pair confirmation. Full raw resources,
workers, failures, tails and code are retained. Whole-host counters are shared,
not exclusive service cost. The [complete report](result.md) closes this bounded search:no selected
confirmation point meets the predeclared useful CPU/P99 advantage criterion.

The final CPU2 FFT sweep's original client-timing interruption is retained in
client_dispatch_initial/,with handling,raw timer diagnosis and a client-only
probe. The entire final configuration is acquired under screen_cpp_recovered
tags with forward-declared new seeds. No failed data is pooled or overwritten;
the original unchanged timing guard still applies. The first54valid cells have a separate owner receipt;full60-cell coverage
and30-cell confirmation now pass owner-code audits. No result is inferred
from the retired timing-failure pair.

## Read and replay the completed result

[Result](result.md),[screen table](screen_table.csv),
[confirmation table](confirmation_table.csv),[paired effects](confirmation_summary.json)
and[resource ledger](resource_ledger.json) separate every scope and tail.
[Canonical replay](analysis_replay.json),[owner audit](confirmation_owner_audit.json)
and[lifecycle counts](lifecycle_audit.json) check original data.
The[control-stream incident](control_connection_interruption/incident.md)
contains32warmups but zero measured requests;no confirmation result is replaced.

From the repository root,with Python and NumPy available:

~~~sh
archive=bench/results/graph_network_20261017
python3 "$archive/confirmation_analysis.py" "$archive"
python3 "$archive/owner_audit.py" "$archive" confirmation
python3 "$archive/replay_analysis.py" "$archive"
python3 "$archive/resource_ledger.py" "$archive"
python3 "$archive/export_tables.py" "$archive"
python3 "$archive/lifecycle_audit.py" "$archive"
# Optional:Matplotlib in an analysis environment;see analysis_environment.json.
python3 "$archive/plot_results.py" "$archive"
~~~

The owner audit requires the frozen3d3878c source commit in Git history.
Original acquisition wrappers contain the recorded Coder paths;use the current
graph runbook for portable build/serve/client/cleanup commands. Replaying
analysis writes its derived outputs;keep original archive copies when comparing.
The executed canonical-replay check itself uses OS-temp symlinks and does not
overwrite original metrics or ECDFs. Full raw request/timer formats are documented.

Final[cleanup receipt](cleanup.json) records actual Job/Pod/key removal and
original Workspace/session preservation.
