# Client diagnosis: retained decoded SSE graphs drive GC stalls

One actual instrumented stock-official60s/192/s run,11520 successes/737280
tokens,8 excluded warmups. No server performance ranking or old6.36ms claim.
Source/versions/full raw worker records and offline interval analysis retained.

Default Python GC thresholds[700,10,10], GC enabled. Each4 workers records
8 generation2 collections, maximum438.716/416.664/472.670/394.577ms.
Maximum request serialization12.974/18.663/39.095/26.958ms;
file-write11.434/9.376/3.572/4.114ms. Instrumented client lagP99
211.219452ms, similar to ordinary four-worker208.800613ms; not equivalence.

Same-worker scheduled-to-task-start interval coverage, largest116 actual
delays (ceil1%of11520, post-hoc diagnostic selection):
total36074.662302ms, GC32239.406977ms (89.3686%), logging outsideGC858.232747ms
(2.379%), residual2977.022578ms (8.253%). These are exclusive interval
intersections on actual request windows, not sums of marginal P99s or a
Linux/GPU latency allocation. Individual examples and all four worker counts
are in original_stalls.stdout. All output/pool flags remain; flags400 total.

Source retains all64 decoded nested SSE JSON trees per successful request
until the entire cell drains. The observed long GC pauses overlap most worst
client arrival delays. This supports a client object-retention cause and
refutes assuming a saturated CPU core or slower model from arrival lag alone.

Necessary repair: retain each original SSE data payload as lossless UTF-8
surrogateescape text and receive timestamp, decode transiently for unchanged
prompt/count/vocabulary/finish/token checks, then release decoded object tree.
No trace content removal, model/kernel change, GC disable/threshold change,
timeout/oracle weakening, reference-pool expansion or extra worker increase.
Keep immediate per-request durable logging; it is not the dominant measured
pause, so do not introduce an unnecessary deferred writer.

One same-workload instrumented payload-recording control will test removal of
long GC/arrival stalls with defaults unchanged. This is a client-fault repair
control within the existing diagnostic, not a fourth preflight or a server
performance result. Thereafter the complete ordinary K/N/O matrix must restart
fromblock0 with source frozen and no profiler. Old prefixes remain separate.
