# First actual preflight: protocol passed, client timing needs repair

2026-10-16 UTC. All3 conditions/384requests/24576tokens succeed,24 checked
excluded gen1 warmups; auth missing/invalid401, actual official optimized
config engaged, all terminal/drain/pin checks and byte-exact CPU replay pass.
K/N/O frozen-pool flags1/1/3 retained. This is dependency evidence, not a full
server comparison or primary effect.

The initial single asyncio loop has CPU fraction0.950/0.948/0.876,
scheduling-lagP99 6.276/10.977/49.134ms. Last due0.619764s, last actual task
start0.623872/0.624964/0.638350s. Official JSON/SSE parsing and binary framing
differ; these observations expose a client-timing risk, not a proven GPU/server
bottleneck. No initial official slowdown is claimed as a server defeat.

Before full collection, one common client event-loop repair will use installed-
runtime uvloop0.23.0 for all conditions, keeping requests/parser/offsets/oracle/
timeout/metric unchanged. It is an existing upstream library, not a new
scheduler/control framework/concurrency cap. Official vLLM throughput benchmark
imports uvloop; its serve benchmark uses asyncio.run, so do not claim the
latter already uses uvloop. Fresh same-plan follow-up and actual second
three-condition preflight precede full eligibility. Initial client/driver/
context are preserved in initial_client/ and metadata embeds actual source.

Official parent exits0 and no children/GPU apps/pins remain; its own logs
force-kill EngineCore during shutdown and warn about one leaked semaphore.
Do not advertise fully graceful teardown. Client Job is held only for this
immediate repair/preflight/full benchmark, then exactUID cleanup is required.
