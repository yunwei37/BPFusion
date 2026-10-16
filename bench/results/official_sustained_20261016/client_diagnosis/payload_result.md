# Client raw-payload control: sustained fault repair supported

Same actual official checkpoint/GPU/defaults,60s192/s/11520requests/gen64,
4 common workers, same parsed protocol checks/timeouts/offsets. Both
instrumented constructors complete11520successes/737280 output tokens plus
8 excluded warmups. Default GC enabled, thresholds[700,10,10] unchanged.

|Instrumented client diagnostic|Decoded object retention|Raw data payload retention|
|---|---:|---:|
|Client scheduling lag P99 ms|211.219452|3.256700|
|Client maximum scheduling lag ms|505.003549|75.438691|
|Generation2 collections per worker|8|2|
|Largest generation2 pause across workers ms|472.669996|48.791266|
|Maximum per-request serialization ms|39.094614|2.884195|
|Maximum file-write ms|11.434461|2.845223|

Original same-worker worst1% delay windows have89.37% GC interval coverage.
Removing retained decoded JSON trees while preserving raw data drastically
reduces long GC and client-start delay in this finite control. Arrival lag is
not zero and residual GC/host/library costs remain. One ordered instrumented
control is not a5-pair ordinary server performance estimate or a universal
client-capacity proof. No GPU model/kernel optimization or historical6.36ms
allocation follows.

[payload_archive_validation.md](payload_archive_validation.md) independently
reconstructs every raw SSE JSON data payload's prompt/finish/token/arrival
fields against all client outcomes. Literal whole-wire framing is not claimed.
All frozen-pool disagreements remain, with no oracle expansion or exclusions.
Request logging stays immediate/durable; no GC tuning or hidden worker cap.

This closes the diagnostic dependency and justifies the minimal representation
repair. Ordinary full K/N/O must restart atblock0 with no GC/log timing
instrumentation, fixed original primary/offsets/oracle and all15cells.
Earlier3 preflights, both incomplete full prefixes and both instrumented
controls remain separate and committed. Root cause here belongs to the custom
official benchmark client, not to official GPU execution or the eBPF path.
