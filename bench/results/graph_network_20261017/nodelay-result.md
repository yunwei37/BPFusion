# Shared small-reply TCP policy repair

One matched before/after kernel/native pair,matmul/repeat1/1000requests/s6s,
unchanged atomic/timerfd client,seed20262017,default8,same remote Job/GPU.
All24000measured responses and128excluded warmups pass. Client monitorP99
is below the original1ms gate in all four controls. Full raw/worker/resources
and every latency quantile are in nodelay_before/,nodelay_after/ and
nodelay_controls.json. This is a dependency/fault-repair diagnostic,not the
prespecified transport-benefit confirmation.

Kernel scheduled-responseP99 falls22.006->2.566ms,P99.9 34.615->4.408ms;
responses>10ms fall130->0,>20ms64->0,>30ms45->0. The before controller sends
7229times for6032warm+measured responses,consistent with split output.
The graph caller omitted TCP_NODELAY,while the ordinary LLM caller already
sets it. Withholding the final word until FIFO retirement can split256bytes
as252+4; the same listener policy is now applied to both graph transports.
This supports a Nagle-related tail mechanism,but does not allocate every
individual packet/softirq/GPU stage or the historical LLM6.36ms difference.

Native is ADVERSE in this single control:P992.864->10.955ms,P99.9 4.918->
22.072ms,responses>10ms0->67. Kernel groupCPU .038194->.036254ms/attempt;
native .038637->.039577ms/attempt. Shared host values and all source/raw remain.
No statistical/native-wide improvement or eBPF advantage is claimed from one
pair. The consistent small-reply policy is adopted with this limit; final
independent matched confirmation decides whether any useful transport benefit
exists. Do not cherry-pick the favorable kernel control as the main result.

Ordinary Make builds all three graph libraries. Kernel/native with repetitions
1/16/256 plus legacy GPU-I/O-loop at repeat1 pass14cells/2548finite checks,
including exact numerical outputs,reject/reuse/wrap/reset/queued-stop and
normal cleanup. All four before/after kernel/native compiled GPU dispatchers
are instruction-identical (376SASS lines); nodelay_gpu_control.json and dumps
retain that control. There is no CUDA math or graph-dispatch optimization.

The preexisting resource observer takes~3.2ms median/up to8ms per100ms sample,
which is material relative to~1ms requests. The final CPU/P99 experiment keeps
CPU/IRQ/thread sampling but moves NVML queries to boundaries. This is an
instrumentation choice before the final matrix,not a proven explanation for
all adverse native outliers. Mid-window GPU fields are unavailable; ownership
and energy are not falsely attributed. Earlier diagnostic cells stay separate.
