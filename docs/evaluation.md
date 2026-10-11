# Evaluation status

The repository has no formal paper RQ or thesis contract. The retained user
objective is a complete Linux TCP/HTTP + eBPF/shared queue to resident
real-model inference and asynchronous kernel TX, with reproducible matched
correctness and throughput/latency evidence. Do not substitute model arithmetic
tuning or a component result for that complete goal.

The [native userspace network comparison](findings/0025-native-userspace-network.md)
is the current supporting component experiment. It tests whether the kernel
request/reply implementation improves client latency or output throughput
against a native epoll control with the same resident HF graph computation.
Finding0024's dispatch comparison cannot answer this absent network condition.
The [fresh plan review](../bench/results/userspace_network_plan_review_20261011.md)
admits it. Both user-control model regressions and both real preflights pass.
Independent reconstruction confirms exact outputs, complete process counts
and cleanup. The full paired matrix is next; preflight supplies no performance
conclusion.

Positive effects support the tested transport boundary; negative/mixed effects
redirect optimization toward polling/write grouping and transport buffering.
Intervals crossing zero remain inconclusive. This is not an external SOTA,
physical-NIC, text/JSON, attributed total CPU or full-goal completion result.
Raw paths, commands, metrics, fixed correctness contract and limitations live
in the linked plan. Update this status only from terminal collection and fresh
independent result review.
