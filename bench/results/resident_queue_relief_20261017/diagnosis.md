# Prior-data diagnosis: backlog grows before first output

2026-10-17 UTC; reanalysis only of complete0078 frozen ordinary raw requests.
prior_queue_context.jsonl retains all5blocks/3conditions/6arrival buckets.
No new performance run or causal certainty is claimed by this diagnosis.

Native meanTTFT for successive10s original-arrival buckets:
235.1,727.0,1331.7,1878.8,2504.1,3003.4ms.
Its generation span remains85.4--86.5ms across those same buckets.
CompletionP99 rises579.2ms in the firstbucket to3363.5ms in the last.
Official meanTTFT is101.2--158.3ms; bucketcompletionP99442.6--561.4ms
without monotonic accumulation,and sampledrunning24--39exceedsresident16
while sampledwaiting0,prefixhits0. These are observed client/periodic samples,
not GPU-stage timing or continuous absence of queues.

The residentdeliveredrate~182/s is below offered192/s. A small capacity
shortfall can accumulate~3s waiting over60s; the5-fold completiontail gap
does not imply a5-fold model-compute slowdown. Current native andBPF
sharethis behavior,so a transport-onlytweak cannot resolve the shared limit.
A matched32-bank constructor tests the capacity/batching explanation directly.
KVbytesincreasewithbanks,but allocationisbootstrap-only; this intervention
doesnotindependentlyseparatebatchwidth,KV/cachelocality or FIFOownership.

The normal32candidatebuild exits0 on the qualified stack. This establishes
buildability only; real model correctness and matched delivery remain pending.
Selected8/defaultandordinarysourceareunchanged. The next action is actual
same-workloadqualification/repair,not declaring this measurement a finished fix.
