# Diagnose repeated small-graph tail stalls before final screening

Written before changing any server TCP option. Client timerfd and atomic
epoch publication now pass the unchanged1ms monitor gate on the kernel
1000/s6s control. Actual6000responses are numerically correct; completionP99
22.006ms/P99.9 34.615ms while client waitP99 .676ms/monitor .725ms.
An earlier timerfd kernel control hasP99.9 41.485ms. Preserve all controls.

The graph caller leaves TCP_NODELAY disabled,unlike the already repaired
ordinary LLM caller. The shared transport withholds the final word until FIFO
retirement; graph output can therefore be sent as252bytes plus4bytes.
A Nagle/delayed-ACK interaction is a concrete candidate,not a GPU-math cause.
Check actual send counts and then test the same previously qualified TCP
policy on BOTH transports; do not make native artificially slow.

Finish the current atomic-client kernel/native1000/s6s pair as the before
control. Build an ordinary separate8-bank constructor with only listener
TCP_NODELAY enabled (accepted sockets inherit it),same CUDA graphs/dispatch.
Run both after controls with exactly the same operation/work/load/seed/client
and resource/tail definitions. Compare full tails/slow-response counts,not
only a best latency. Retain any CPU increase,failures or inconclusive result.
Qualification covers all repeated-library combinations and cancellation.

This is a fault-repair diagnostic inside the bounded network experiment,
not an extra paper result or transport-advantage confirmation. Adopt only with
material supported benefit and no correctness/lifecycle regression. Final
screening starts anew under a distinct source label on both paths; no mixture
of pre/post-option cells. Predeclared CPU/P99 confirmation criteria stay fixed.
