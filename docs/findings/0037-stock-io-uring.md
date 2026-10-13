# Stock io_uring TCP from an NVIDIA GPU

This is a completed component feasibility diagnosis, not an inference or
performance experiment. On the original RTX5090 Workspace, a GPU can publish
ordinary Linux io_uring SEND/RECV operations into caller-allocated mapped host
memory and consume their completions. An already pending TCP receive can wake
the sleeping SQPOLL thread when a request arrives; eight cold request/reply
cycles complete without a steady userspace network worker or explicit wakeup.
The production eBPF/model/module path and defaults are unchanged.

## Actual environment and scope

Source baseline is main8b27522169bccdeedee0b43a42f01a8ddaaf1910. Execution
uses the original yunwei356/bpfusion-dev, Linux7.3.0-070300rc3-generic,
NVIDIA610.57.04, RTX5090 and installed CUDA13.0.88. No package, sysctl,
affinity, driver or persistent service change is made. Base Torch2.14.1 and
Transformers5.19.0 remain unchanged; neither participates in this probe.

Each native process bootstraps one loopback TCP listener/accepted socket,
registers ordinary anonymous host memory with cudaHostRegisterMapped, and
creates an eight-entry SQ/sixteen-entry CQ with SQPOLL|NO_MMAP|NO_SQARRAY.
The small queue size is a wrapping diagnostic, not a proposed serving limit.
The installed ABI uses sq_off.user_addr for SQEs and cq_off.user_addr for
shared rings, consistent with [liburing setup](https://github.com/axboe/liburing/blob/master/src/setup.c).
There is no importing of kernel-owned mmap buffers, GPUDirect networking,
liburing installation or userspace TCP implementation. The GPU supplies host
virtual addresses to SQEs, uses system-scope acquire/release and fences for
publication, checks each completion and retains each send buffer until completion.
Partial positive sends are handled, although observed sends all return128.
The host runs CUDA synchronization while the device owns the queue.

Default sq_thread_idle is left0. The inspected [upstream kernel source](https://github.com/torvalds/linux/blob/master/io_uring/sqpoll.c)
converts an unset timeout to HZ; do not assume0 means infinite polling.
The running kernel's concrete observation is NEED_WAKEUP after the declared
two-second idle interval, not an exact measurement of its sleep threshold.

## Actual progression, including failures

Initial hot/idle/wake cases run01:12:35–01:12:44UTC2026-10-13. The nominal hot
case is not hot: its initial queue already reports NEED_WAKEUP, no CQE completes
and the client receives zero bytes. The idle case behaves likewise. One explicit
host wakeup delivers all4096 bytes. These initial sources, traces, statuses and
the false hot expected_outcome are retained in initial/. The original wake
case prints stale errno2 with successful return0; errno is meaningful only on
failure and the reporting is corrected in subsequent source.

The corrected hot/idle/wake set runs01:13:24–01:13:31UTC. Startup submits one
NOP, performs one host SQ_WAKEUP and consumes the NOP completion before READY.
This establishes an observed active queue, rather than hiding a runtime waker.

| Condition after startup | GPU SEND completions | Exact client bytes | Runtime explicit host wakes |
|---|---:|---:|---:|
| Hot queue |32|4096|0|
| GPU submission after two seconds idle |0|0|0|
| Same idle submission plus one explicit host wake |32|4096|1|

The idle failure retains its unconsumed SQ entry until ring teardown. Process
exit0/DIAGNOSIS_COMPLETE are wrapper completion, not successful delivery.
The case statistics, actual client hex bytes and replay checks define outcome.

The first network-wake case runs01:14:34–01:14:37UTC. Startup also arms a
one-byte RECV. After observing NEED_WAKEUP, the GPU waits for its CQE. The
client sends byte77 after2.2seconds; the receive completes, the GPU verifies
the byte and sends32 frames. Client gets exact4096bytes; no runtime explicit
host wake occurs. This tests a receive-completion wake, not GPU ability to
invoke io_uring_enter itself.

The extended probe initially fails NVCC because 0xcafe+cycle is lexed as an
invalid preprocessing number. Adding whitespace fixes syntax only; initial
source/build errors remain in receive_cycles/initial_build/. The completed
run is01:16:06–01:16:24UTC. No failed delivery is discarded or silently retried.

## Repeated cold requests and EOF

The extended native process keeps the same connection for eight cycles. Each
client request follows2.2seconds of idle and supplies byte77..84. On each cycle
the GPU observes NEED_WAKEUP, consumes and verifies the receive completion,
then generates32 different128-byte frames whose values depend on the request
byte and frame index. After cycle1 the GPU itself posts each following RECV;
there is no host request loop or keepalive/NOP loop. The GPU posts a final RECV
and consumes zero-byte EOF after the client half-closes.

Actual results:
- Eight received requests and eight observed sleeping-queue flags.
-256 SEND submissions and256 consumed SEND CQEs,32768 exact client bytes.
- GPU arms seven subsequent request RECVs plus the final EOF RECV.
- SQ head=tail=CQ head=tail=266: bootstrap NOP, eight request receives,
 256 sends and EOF receive; dropped=overflow=0.
- Zero runtime explicit host wakes; the only io_uring_enter is the bootstrap
 wake before READY. All-thread native strace records one bootstrap accept and
 zero recvfrom/recvmsg/sendto/sendmsg calls across the entire process.
- Normal native exit, successful ring/socket closure and CUDA unregistration/
 unmapping. Client sees clean EOF with no extra response bytes.

The traces cover the native process and its userspace threads, not kernel
threads or the separately executing Python client. Linux TCP, async polling
and SQPOLL still use CPU. All-thread syscall absence is not zero host CPU.

## Replay, restoration and next integration

[Raw sources/results/traces](../../bench/results/gpu_uring_tcp_20261013/)
include all source generations, initial failures, actual compiler commands,
client byte records and [root self-review](../../bench/results/gpu_uring_tcp_20261013/review.json).
This is explicitly self-review, not independent experiment-plan/result review.
Replay without a GPU from the repository root:

    python3 bench/results/gpu_uring_tcp_20261013/review.py

For a fresh hardware run, copy the selected archived probe.cu/driver.py into an
OS temporary directory inside the original Workspace, compile with the actual
recorded NVCC command using the new temporary path, then run that driver.py.
It writes real results beside its source, so do not run it inside the checkout.
The installed CUDA toolchain and strace suffice; no vLLM environment is needed.
The intentional idle durations, tracing and synthetic data do not provide
serving latency/throughput measurements.

After exact-byte archiving and replay, the owned temporary directory/binaries
are removed. [Restoration](../../bench/results/gpu_uring_tcp_20261013/restoration.json)
records same boot/base runtime, no own GPU process/module and preserved original
Coder processes/WIP.

This establishes an NVIDIA/stock-kernel TCP component that can be explored to
reduce custom TX-module dependency. It does not replace the current module,
which also accepts sockets, drains receives and owns response/slot lifecycle.
The next integration must connect asynchronous accept/FD ownership and receive
completion to existing eBPF admission, GPU model completion, HTTP/binary framing,
disconnect handling and queue reuse. The pending-receive wake must still work
with the actual sockmap/verdict path and inference scheduling; those conditions
are untested here. Multiple connections, receive buffering/backpressure,
connection churn and a matched real-model comparison remain open. Do not claim
a complete module-free server, backend generality, novelty or performance gain.
