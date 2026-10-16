# Server NODELAY: complete matched result

All20 executors/40 cells finish2026-10-16T10:53:54UTC, collector/analysis0.
10240/10240 attempts succeed,655360 measured tokens plus160 excluded warmups.
Ordinary source-selected computation, same16 slots/model/GPU/runtime/client;
only server listener TCP_NODELAY differs. Full acquisition has no packet or
TCP_INFO observer. Five blocks use the admitted order and no replacement.

## All condition means

Entries are means of five process statistics. Token gap retains coalesced zeros;
it is not official stream-output ITL. All tails and CPU fields remain in raw analysis.

| Regime | Condition | Output token/s | Token-gap P99 ms | Zero fraction | TTFT P99 ms | Completion P99 ms | Owned CPU ms/attempt |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
|closed16|kernel_before|8841.739650|40.459794|0.833929|3.826305|120.843583|0.387381|
|closed16|kernel_after|11260.439910|2.287216|0.003336|3.380644|93.225301|0.519097|
|closed16|native_before|8780.373010|40.466041|0.834400|3.754885|122.158931|0.274653|
|closed16|native_after|11358.342806|2.713494|0.013294|4.069138|91.535581|0.391687|
|offered192|kernel_before|10995.734168|3.392872|0.019010|111.711727|197.003934|0.923578|
|offered192|kernel_after|10869.148301|2.960842|0.018626|123.005627|209.729927|0.911016|
|offered192|native_before|10776.796737|2.982559|0.024330|141.365278|227.839441|0.459563|
|offered192|native_after|11014.609900|3.036499|0.018552|108.675635|193.708502|0.451263|

## Predeclared primary effects

- kernel_after_vs_before: -38.172577ms [-38.550854,-37.794300], candidate minus before, nominal paired t95df4.
- native_after_vs_before: -37.752547ms [-38.667032,-36.838063], candidate minus before, nominal paired t95df4.

Closed16 output throughput effects are+2418.700[2059.492,2777.908]token/s
kernel and+2577.970[2008.595,3147.345] native. CompletionP99 improves
27.618[23.771,31.465]ms and30.623[26.683,34.564] respectively.
Process-group CPU increases0.131716[0.097310,0.166122]ms/attempt kernel
and0.117034[0.097963,0.136105] native. More immediate small transmissions
therefore have a real observed CPU tradeoff; total resources are not measured here.

After-fix kernel/native speed intervals still cross zero in both regimes.
After-fix kernel owned CPU remains higher: closed16+0.127410[0.101754,0.153066]
and offered192+0.459753[0.262323,0.657184]ms/attempt. This repair helps both
transports; it is not an eBPF-specific novelty or speedup. Offered192 effects
remain in the complete analysis, including adverse/inconclusive rows.

## Direct mechanism evidence and limits

The [actual socket/packet preflight](preflight.md) shows before NODELAY0/CORK0
and after NODELAY1/CORK0 for accepted sockets. Before has positive queued unsent
bytes with an earlier packet unacknowledged, constant bytes_sent, positive receive
window and no retransmission in the concrete episode. ACK arrival releases
queued small data. The single NODELAY intervention removes sampled unsent
holds and the observer-free full run removes the persistent40ms delivery tail.
This supports Nagle/delayedACK as a material cause for the tested shared stall.
It does not say every remaining tail is TCP or precisely allocate the old
unreproduced kernel-specific6.36ms difference; that older question remains bounded
by finding0066. No host/GPU timer/affinity/sysctl or model arithmetic is changed.

Diagnostic polling/capture overhead and finite boundary coverage remain explicit.
Kernel packet realtime and socket-sample monotonic clocks are not added as
exact phase totals. Hardware/shared-host exposures are not continuous isolation.

## Numerical and lifecycle boundaries

- kernel_before: finite-set matches 2545/2560.
- kernel_after: finite-set matches 2524/2560.
- native_before: finite-set matches 2516/2560.
- native_after: finite-set matches 2552/2560.

All measured sequences have64 vocabulary-valid IDs and valid protocol completion.
The unchanged finite reference set is not expanded after output. Disagreements
remain visible; current ordinary hidden trajectories are not independently replayed
in this performance matrix, and no identical-output or task-quality claim follows.

Default8 protocol/replay and ordinary cancellation qualification is running
separately before canonical source adoption. The candidate remains private until
that acceptance and the fresh result review finish. Existing homogeneous controls
retain their original behavior. Generic graph source is outside this measured
LLM performance contrast.

Raw/source/commands are in [tcp_full/](tcp_full/), [preflight](tcp_preflight/)
and the candidate diff/build files. CPU-only replay:
python3 bench/results/tcp_nodelay_20261016/tcp_analysis.py bench/results/tcp_nodelay_20261016/tcp_full/full.jsonl
The archived gzip is lossless and replay stdout is byte-identical.
The [fresh independent result review](result-review.md) finds the full run valid,
the scoped hypothesis supported, and supporting mechanism/workload evidence.
It independently recomputes both primaries and critical secondary tradeoffs.
Offered192 native-before block3 has client scheduling-lagP99 133.515557ms;
retain it and do not attribute its after-before TTFT shift cleanly to NODELAY.
All20 full-run parents exit0 with no forced cleanup, ten detach receipts exit0.
Kernel legacy128-entry admission diagnostics truncate392/520 in each full
kernel executor; full client outcomes remain complete. Source adoption still
waits for separate ordinary-default8 acceptance.
