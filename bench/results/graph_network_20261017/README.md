# Small-graph network / CPU experiment

This experiment follows the completed LLM capacity comparison in
[0080](../../../docs/findings/0080-resident-queue-relief.md).
The [pre-acquisition plan](plan.md) and [owner-only design review](plan-review.md)
fix its scope, metrics, screen/confirmation selection and positive/negative exit.
No other agent participates.

The reusable client is bench/graph_network_client.py; analysis is
bench/graph_network_analysis.py. The example captures unchanged upstream cuBLAS/
cuFFT, with optional repeated work. See the
[graph guide](../../../docs/graph-backends.md) for normal build, serve, client
and cleanup commands. Client runtime is Python3.12.12/uvloop0.23.0. Binary
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
