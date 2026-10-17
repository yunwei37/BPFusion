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
not exclusive service cost. The final report will state supported boundaries
and close this bounded search if the predeclared benefit is absent.

The final CPU2 FFT sweep's original client-timing interruption is retained in
client_dispatch_initial/,with handling,raw timer diagnosis and a client-only
probe. The entire final configuration is acquired under screen_cpp_recovered
tags with forward-declared new seeds. No failed data is pooled or overwritten;
the original unchanged timing guard still applies. The first54valid cells have
a separate owner recomputation receipt;terminal coverage remains pending.
