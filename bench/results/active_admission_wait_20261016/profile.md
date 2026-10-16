# Separately profiled candidate mechanism context

After the complete fifteen-cell unprofiled matrix and terminal cdabd3a
publication, the one planned candidate creator-TID perf cell completed.
Same normal active_wait_sourcebuild16, Qwen FP16, block0 192/s60s schedule,
64 outputs and frozen prompts/oracles/timeouts; eight excluded checked gen1
warmups. All11520 attempts complete737280 measured tokens with no invalid,
transport or close outcome. Twenty-six finite-pool disagreements are retained.
All outputs remain in active_wait_profile.

Official private perf6.12.95, cpu-clock:k499Hz, creator TID777745 only,
--no-inherit --no-buildid --no-buildid-cache. Kernel ancestry follows the
kernel unwinder; the fp option does not force kernel frame-pointer unwinding.
Perf starts after warmup, stops after measured client drain by intentional
SIGINT (record exit-2), then observer/server stop, then client transfer and
offline decode/archive. All five decodes exit0, stderr empty; recording stderr
contains only normal capture lines. Server exits0 with queues drained and no
pins. Serving replay is byte-identical with empty stderr.

| Observed classifier | Samples | Period sum seconds | Fraction |
|---|---:|---:|---:|
| socket_network_or_softirq | 2752 | 5.515030016 | 80.303472% |
| loop_coordination_other | 469 | 0.939879752 | 13.685439% |
| scheduler_without_socket_ancestor | 171 | 0.342685368 | 4.989787% |
| bpf_map_without_socket_ancestor | 32 | 0.064128256 | 0.933761% |
| unknown_leaf | 3 | 0.006012024 | 0.087540% |

Total3427 samples, each2004008ns, period sum
6.867735416s. Unknown leaf3;
at least one unknown kernel frame2896
(84.505398%).
All samples remain in the denominator. Inclusive/self distributions overlap,
never sum them. Independent binary record parsing confirms3427 SAMPLE records and zero LOST,
LOST_SAMPLES, THROTTLE or UNTHROTTLE records; counts and periods match the
script independently. See binary_records.json and result-review.md.

The observed coordination/map categories contain501 samples (14.619200%),
versus7146 (70.850684%) in the earlier0073 before profile. Observed total
period sums are6.867735416s versus20.212424688s; network/softirq samples are
2752 versus2693. Named queue-map and clock leaves cease to dominate.
This is consistent with the waiting intervention reducing coordination cost.
These are separate, noncontemporaneous, profiler-exposed cells on a shared
host, with unresolved ancestry and possible unrelated network softirq.
They are not a paired performance estimate, exact branch accounting,
exclusive service CPU attribution, or an additive decomposition of client P99.

Profiled serving CPU is0.668507358ms/attempt, throughput11621.261864tokens/s,
connect completionP993462.194977ms and client receive-gapP993.960040ms.
These remain diagnostic context; the five unprofiled blocks determine the
CPU-effect and delivery claims. Whole-host/cgroup/device and observer data
remain separate nested/shared views. No Git/archive review workload overlaps
the measured bracket; retained unrelated host work remains.
