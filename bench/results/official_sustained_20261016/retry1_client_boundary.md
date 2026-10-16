# Four-worker sustained prefix: root cause still open

Frozen source b90a7b1. First K/N/O block completes; official11520/11520
requests succeed, but its client scheduling lag linearP99 208.800613ms,
maximum474.880003ms despite workerCPU fractions0.583041/0.583301/
0.581399/0.582196. More workers reduced averageCPU but did not remove the
arrival distortion; this refutes treating one-core saturation as its established
root cause. No server ranking/paired primary is computed from this3-of15 prefix.

All3 server groups already exit0, original sessions alone remain/noGPUapps/pins.
The driver itself then exits1 on a post-serving WebSocket data-recovery reset
(write connection reset/unexpectedEOF while reading original stdout). No
request is failed by this transfer error; durable prefixes/originals remain.
Existing control-plane reads and Pod exec succeed. Contemporaneous client
Pod CPU quota/throttling remains absent, cgroup CPU/IO pressure low; host load
1.25/2.20/2.18 and hostCPU pressure~7%, not an established CPU starvation cause.
Raw recovery is resumed with1MiB bounded chunks through the existing function,
below sizes already successfully streamed whole. This is an archival reliability
repair; it affects no measured request or backend setting.

four_worker_client/ preserves actual source. Before another ordinary full run,
diagnose the client source's retained decoded SSE object graphs, Python cyclic
GC and synchronous per-request JSON/file emission. An instrumented client-only
full-load diagnostic may log GC pause and serialize/write spans; it is fault
diagnosis after a real sustained defect, not a fourth preflight or a server
performance result. Preserve every raw artifact and any failing outcomes.
Do not raise worker count again or change the scientific primary to hide lag.

All61 original retry1 files are now archived; all34560 outcomes and worker joins independently match. See retry1_client_context.md. No data-recovery work remains before client diagnosis.
