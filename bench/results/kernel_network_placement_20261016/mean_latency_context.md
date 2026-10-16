# Existing-data mean latency context

Post-hoc descriptive reuse of the frozen full analysis; no new acquisition or
changed primary. Client connect-origin mean completion equals mean TTFT plus
63 times mean TPOT. This is an identity of matched success means, not an
allocation of marginal P99 or internal GPU/Linux stages. All attempts succeed.

- before: mean TTFT 1670.222432246 ms + first-to-last receive span 84.841470707 ms = mean completion 1755.063902953 ms.
- candidate: mean TTFT 1606.191869124 ms + first-to-last receive span 84.699876355 ms = mean completion 1690.891745479 ms.
- native: mean TTFT 1603.683530993 ms + first-to-last receive span 84.454056319 ms = mean completion 1688.137587312 ms.

Candidate-minus-before mean completion improves64.172157 ms, comprising
64.030563 ms before the first client token and0.141594 ms of first-to-last
receive span. This points to queueing/first-token time as the main observed
location of the mean benefit; it does not identify its internal cause. Offered
192*64=12288 tokens/s exceeds delivered~11640; backlog amplification from a
small capacity change is a plausible inference, not a measured stage allocation.

Relative to native, candidate mean TPOT is adversely higher by0.003901905 ms
[0.001569381,0.006234429] nominal paired t95, about0.29%/0.246 ms per63 gaps.
This retained secondary result limits any claim that all latency metrics improve.

Client CPU consumes approximately one core in each condition, despite no quota
or recorded cgroup throttling. Scheduling delays and per-cell CPU remain in raw
results; delivered TPS is not an exclusive GPU/server capacity ceiling.
