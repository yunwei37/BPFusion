# Full trace capture failure and bounded repair
First full diagnostic fails honestly in its first loop cell: GPU serving,
shutdown and both exact replays complete264 replies/16392 tokens, but ftrace
overwrites events on five CPUs (CPU13:238013; CPU12:78068; CPU6:339811; CPU3:26010; CPU0:41538) with the existing1410KiB per-CPU buffer.
The complete failed prefix and all per-CPU counters remain. No missing record
is imputed or treated as zero cost. No completed two-pair result is claimed.

Increase only this owned tracefs instance's per-CPU buffer to32768KiB, based on
the observed overflow (roughly23x default, temporary768MiB across24 CPUs).
The streaming reader remains; the larger buffer covers reader starvation.
Remove the instance on finish, so the allocation is not retained.
No global tracer/other instance/service/affinity/host setting changes.

A cleanup bug called finish twice after the coverage assertion, masking the
first error and skipping attached-map cleanup. Preserve both tracebacks.
The original exporter process is confirmed exited, GPU process list empty,
the owned loader detaches, all owned BPF pins are removed. Repair the driver
so finish clears its object before asserting, and cleanup tracing errors do
not skip executor/pin cleanup. Failed coverage remains a run failure.
Rerun the entire unchanged two-pair diagnostic with the buffer/source change
frozen separately. This is an instrument repair, not a transport optimization.
