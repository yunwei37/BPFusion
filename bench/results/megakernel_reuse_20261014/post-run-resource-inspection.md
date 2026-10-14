# Post-run source inspection: unresolved concurrency mechanism

The full transport comparison is held fixed and complete. After collection,
read-only cuobjdump --dump-resource-usage on the existing common AMK native
module reports persistent model REG106/STACK256/staticSHARED34448; the
network library reports dispatch REG38/staticSHARED0 and the separate
io_network kernel REG40/STACK768/staticSHARED0. Upstream loader defaults
threads_per_block256 and adjusts dynamic shared memory to actual program
needs. These static compiler facts do not establish simultaneous execution
or the cause of the measured c8 difference. The source dispatcher returns
after fire-and-forget model launches and tail-resumes after child graphs;
the separate io_network kernel remains active. Native c8 throughput rises
relative to c1 while loop c8 does not. A future matched model-kernel timeline/
co-residency control could discriminate scheduling interference from network
progress or other explanations without editing model arithmetic. No such
causal experiment has yet been admitted or run, and none is claimed here.
