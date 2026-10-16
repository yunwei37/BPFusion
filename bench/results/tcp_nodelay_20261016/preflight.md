# Real preflight and packet/socket observations

2026-10-16 UTC. All4 actual Qwen paths complete128/128 measured requests,
8192 tokens plus32 excluded gen1 warmups; collector and fixed analysis exit0.
This diagnostic is not the performance-primary result; full5-block matrix is
now running with both packet/socket observers disabled.

| Condition | Accepted server NODELAY | CORK | Queued+unacked TCP_INFO samples | Longest sampled unsent hold ms | No-intervening-data ACK-delay P99 ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| Kernel before |0|0|1214|40.484560|40.475619|
| Kernel after |1|0|0|unobserved|0.557174|
| Native before |0|0|1341|38.057984|40.105525|
| Native after |1|0|0|unobserved|0.354144|

The hold is a contiguous sampled interval with positive notsent_bytes and
unacked, while bytes_sent is unchanged; its duration is a lower bound.
Before socket69/client48924, already-queued bytes grow4->36 with one packet
unacknowledged and bytes_sent fixed636 for at least40.484560ms.
Packet kernel timestamps show a4-byte send at1792147178170887649ns,
covering ACK at1792147178212452141ns (41.564492ms later), then36-byte send
12.502us after that ACK. The raw header/TCP_INFO values preserve sequence,
window/cwnd, retransmission and queue context. This distinguishes queued
transport data from solely late GPU production in that episode.
It is consistent with Nagle/delayedACK; full controlled effect and independent
result review are still required before source adoption/stronger claims.
It does not explain the historical unreproduced kernel-specific6.36ms gap.

Own accepted FDs are inspected via pidfd_getfd; no foreign FD/permission changes.
Loopback capture actually has only PACKET_HOST, so no duplicate-direction
removal occurs. All packet drop counters are0; captures have finite begin/end
and user-space diagnostic overhead, not a proof that every boundary packet
was persisted. Kernel realtime packet timestamps and monotonic TCP_INFO
sampling remain different clocks; no exact cross-clock stage allocation.
Only own-port headers/metadata are stored, no foreign packet payload.

Frozen driver/candidate/builds and raw compressed observations are here.
CPU-only replay:
python3 bench/results/tcp_nodelay_20261016/tcp_analysis.py bench/results/tcp_nodelay_20261016/tcp_preflight/preflight.jsonl
python3 bench/results/tcp_nodelay_20261016/tcp_diagnostic_analysis.py bench/results/tcp_nodelay_20261016/tcp_preflight

The first private relocated-source build failed to find io_uring_tcp.h;
nodelay_failed_build1 retains it. Adding the original executor include search
path repairs build8/16; no canonical source changed. Current patch is only
netinet/tcp.h and checked listener TCP_NODELAY before listen.

Read-only host journal10:20..10:40UTC is retained, including AppArmor exporter
denials and CNI lifecycle traffic. No matched EXT4/I/O/OOM/Xid/BUG/Oops/NVMe/AER
fault pattern appears in that finite interval. This is not continuous host
isolation or a comprehensive hardware audit. Own preflight groups/pins are
removed; the separate full matrix owns its current server. Shared temporary
runtime and original Coder/build/WIP state are preserved.
