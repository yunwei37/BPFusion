# Post-hoc ordinary long-output diagnosis

Recorded2026-10-14 after finding0053 was collected, reviewed and published.
This reuses its unchanged raw data. It is descriptive exploratory evidence,
not a predeclared primary result or a replacement for the independent review.

## Authentication and subtraction

Each ordinary transfer executor has eight sequential gen1 warmups plus
32 gen1/c1,32 gen64/c1 and32 gen64/c8 measured requests. The captured driver
and bench/resident_dispatch.py complete each serial request before starting
the next; raw start/last-arrival timestamps confirm nonoverlap. The model
dispatcher increments device_graph_launches only for successful nonempty
model rounds, and emits one token per selected request per round. A valid
single active gen1/gen64 request therefore contributes exactly1/64 rounds.
All104 requests complete with admitted=retired=104 and graph_error=0.

The serial contribution is8+32+32*64=2088 rounds. Subtracting it from the
same ordinary process's final model counter isolates aggregate gen64/c8
rounds, without extra GPU tracing. This does not recover per-round shapes,
batch membership, GPU time or exclusive causal mediation.

Run from the repository root:

    python3 bench/results/final_drain_20261014/posthoc_long_rounds.py bench/results/final_drain_20261014

posthoc_long_rounds.json retains every raw derived row and signed contrast.
The original metrics/oracles/timeouts/analysis/results are unchanged.
All ten captured client_source strings also match current
bench/resident_dispatch.py; the client source is retained inside each raw
metadata record even though the selected source_snapshot directory did not
copy that bench file. An initial read-only locator used tools/ instead of
bench/ and failed before analysis; the corrected authoritative path was used.
No serving run or data was changed because of that locator error.

## Existing-data result

| Model | SQ-only rounds | Native rounds | Selected drain rounds | Native TPS | Drain TPS |
|---|---:|---:|---:|---:|---:|
| Smol135M | 266.8 | 261.8 | 260.6 | 5618.537296 | 5343.548010 |
| Qwen0.5B | 266.0 | 260.8 | 259.4 | 4749.956402 | 4616.848576 |

Drain-minus-native model-round vectors are[-2,-1,-2,0,-1] Smol and
[0,-1,-2,-2,-2] Qwen. Nominal paired t95(df4) differences are
-1.2[-2.238851,-0.161149] and-1.4[-2.510578,-0.289422].
The drain path never uses more aggregate long-output model rounds than native
in these blocks. Additional model rounds therefore do not explain its
remaining mean TPS deficit; per-round shape/padding, model/I/O progression,
client boundaries and delivery costs remain competing explanations.
Finding0053's Smol/native throughput loss remains established; Qwen/native
throughput difference remains inconclusive.

All ordinary coalesced transfer rings end with pending/error/dropped/overflow0,
SQ head=tail and CQ head=tail. The bootstrap NOP and every ordinary single-shot
operation produce one CQE; only the one indefinite multishot timeout produces
extra CQEs. Thus CQtail-SQtail identifies its extra completion count in these
fresh nonoverflowed rings. The extra-CQ fractions range88.05–88.45% Smol old,
88.08–88.48% Smol drain,92.09–92.23% Qwen old and91.99–92.20% Qwen drain.
These totals cover the whole three-cell transfer process and warmups, not
gen64/c8 alone; they do not measure how much GPU time those CQEs consume.
The existing60us heartbeat remains necessary to wake the CQ-waiting BPF loop
when the GPU publishes fresh SQ work. Changing its cadence could trade
submission latency against completion traffic; these counts do not establish
a winning timer setting.

## Source-backed next discriminator

Receive SQEs already use asynchronous RECV with zero message flags.
The code does not set MSG_DONTWAIT or reissue empty receives as a deliberate
polling loop. Upstream liburing's POLL_FIRST skips an initial receive attempt
before internal readiness polling; that would not remove the observed
multishot timeout traffic. Reject the speculative empty-read tuning path.

IoStats currently shares CPU-mapped storage with bf_uring_loop_control.
Regular accounting, pending/error bookkeeping and reply records are updated
and consumed by the single GPU I/O progression owner; source inspection finds
CPU reads of those fields only after the network stream synchronizes.
The BPF/host steady loop needs only its shared control prefix, including
deadline/stop/quiescence/finished fields.

The next proposed intervention is to keep regular bookkeeping in GPU device
memory while leaving that exact control region shared, and copy only the
noncontrol suffix to the existing host report after stream synchronization.
This preserves final report semantics and avoids overwriting live control
flags. It tests ordinary bookkeeping placement with unchanged model math,
network operations, heartbeat, FIFO/recycle policy and worker structure.
It does not eliminate mandatory ring/page communication or timeout CQEs,
and no performance/correctness result for this proposal exists yet.

Primary references for the rejected receive option and retained heartbeat:
[upstream recv documentation](https://github.com/axboe/liburing/blob/master/man/io_uring_prep_recv.3),
[upstream timeout documentation](https://github.com/axboe/liburing/blob/master/man/io_uring_prep_timeout.3).
