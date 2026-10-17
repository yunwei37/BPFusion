# Completed same-executor16/32 diagnostic

One matched process pair,192/s60s+fulldrain with unchanged0078repaired client,
Qwenrevision/FP16/gen64/4prompts andseed20261015. This is an actual normal
constructor change (16->32banks),not an eBPF transport change or model-math
optimization. Both cases use nativeepoll and the same upstream graph adapter.

| Metric | N16before | N32repair |
|---|---:|---:|
| Attempts/successes |11520/11520|11520/11520|
| Failures/timeouts |0|0|
| Delivered outputtokens/s |11649.608|12266.103|
| CompletionP99,ms |3328.880|357.484|
| TTFTP99,ms |3244.200|225.900|
| MeanTTFT,ms |1786.157|53.406|
| MeanTPOT,ms |1.354614|1.427012|
| ClientreceivegapP99,ms |3.272828|9.804483|
| Clientarrival-lagP99,ms |1.552435|2.608308|
| OwnedgroupCPU,ms/attempt |0.751162|0.588059|
| Peakinflight |621|94|
| Frozen-pooldisagreementflags |1|123|

Tail reduction is~89.26%,throughput~+5.29% in this single control; no five-pair
uncertainty or current official superiority is claimed. MeanTPOT and clientreceivegapP99 worsen and
all123N32poolflags remain; finite exact protocol/replay is not universal
ordinary trajectory parity. Request/parser/oracle/timeout/metrics are unchanged.
All raw merged/four-worker/warmup/server/resource files and exit0analysis are
in queue_relief_diagnostic/. Archived-gzip replay is byte-identical and stderr0.

This supports the shared capacity/batching hypothesis for the historical
3.3s backlog in this workload,not exclusive KV-vs-batch causality or eBPF gain.
Earlier16raw arrived faster than it could complete; at32delivered rate covers
the fixed offered workload and avoids the same accumulateddrain. Full5blocks
N16/N32/official and implementation adoption remain; do not stop at this table.
