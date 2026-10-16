# Remove ACK-dependent small-send stalls

2026-10-16 UTC. The [full experiment](../../bench/results/tcp_nodelay_20261016/result.md),
[raw/replay](../../bench/results/tcp_nodelay_20261016/tcp_full/) and
[fresh review](../../bench/results/tcp_nodelay_20261016/result-review.md)
test one server TCP_NODELAY intervention, with GPU computation unchanged.

The persistent16 stall is caused materially by server Nagle/receiver delayed-ACK
interaction in these conditions. Actual accepted sockets are NODELAY0 before,
NODELAY1 after, CORK0 throughout. During before stalls, TCP already holds unsent
bytes while an earlier packet is unacknowledged and bytes_sent is constant.
One sampled kernel hold lasts at least40.484560ms; a pure ACK arrives41.564492ms
after a4-byte send, and queued36-byte data follows12.502us later. No retransmit
or zero-window explanation appears in the checked episode. The single option
removes sampled queue holds; full timing excludes diagnostic observers.

Five blocks/four conditions/two regimes complete10240 successful attempts,
655360 tokens plus160 excluded warmups, no favorable exclusions.

| Persistent16 | Before token-gap P99 ms | After ms | Before token/s | After token/s |
| --- | ---: | ---: | ---: | ---: |
| Kernel |40.459794|2.287216|8841.740|11260.440|
| Native |40.466041|2.713494|8780.373|11358.343|

Numbers are means of five process statistics. Gap P99 retains zeros for
coalesced tokens, distinct from official stream-output ITL.
After-minus-before primary effects are-38.172577[-38.550854,-37.794300]ms
kernel and-37.752547[-38.667032,-36.838063] native, nominal paired t95df4.
Throughput improves2418.700[2059.492,2777.908] and
2577.970[2008.595,3147.345]token/s respectively.

Owned process CPU increases0.131716[0.097310,0.166122]ms/attempt kernel and
0.117034[0.097963,0.136105] native. Sending each small result promptly has a
measured CPU tradeoff; complete resource cost remains unmeasured here.

This helps both transports and is not an eBPF speedup. After-fix transport
speed intervals still cross zero and kernel CPU is higher than native.
Offered192 benefits are inconclusive; native-before block3 scheduling-lagP99
133.515557ms remains in the data. Do not attribute its whole latency shift to
the socket option or replace that block.

All outputs have64 valid token IDs/protocol completion. Finite-reference
disagreements remain visible without expanding the oracle; performance
trajectories are untraced and universal numerical fidelity is not claimed.
All full-run groups drain/exit0, but legacy kernel admission diagnostics still
truncate392 records per520 outcomes. Complete client histories remain intact.

Run valid, scoped hypothesis supported, research value supporting, paper impact
mechanism/workload boundary. This does not allocate the old unreproduced
kernel-specific6.36ms difference. Canonical source adoption waits for the
separate default8 protocol and mid-output cancellation acceptance.
