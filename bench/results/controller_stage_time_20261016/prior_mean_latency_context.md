# Existing-data latency context, not a new experiment

CPU reanalysis of the complete independently reviewed0075 cell metrics, before
new stage-time results. The selected before0074 source versus same-executor
native: mean connect-completion difference+49.743512[36.594103,62.892920]ms;
mean connect-TTFT+49.286070[35.903062,62.669077]ms; mean first-to-last received
token span+0.457442[0.112926,0.801959]ms. Each is a five-block nominal paired
t interval. All15 cells satisfy completion_mean=TTFT_mean+63*TPOT_mean to
floating tolerance. Thus mean differences add; marginal P99s do not.

The extra mean client latency is predominantly before the first received token,
not within its observed64-token receive span. This does not allocate that time
to kernel admission, TCP, GPU scheduling or model prefill. Both paths face
12288offered tokens/s versus about11623/11644 delivered over complete drain;
queue accumulation is compatible with the seconds-long TTFT and amplification
of small capacity differences. That is a load inference, not stage attribution.
Client scheduling-lag mean difference is inconclusive. No clock-domain joins,
new GPU measurement, arbitrary model-math optimization or historical6.36ms
P99 partition follows.

prior_mean_latency_context.py reproduces all signed blocks/intervals from the
archived analysis.stdout whose raw reader and independent review are in0075.
This does not replace the admitted stage diagnostic or its primary; independent
network interference and outside-dispatch intervals remain unresolved.
