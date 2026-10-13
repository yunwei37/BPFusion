# Multi-connection stock io_uring serving

An optional normal build target now runs the unchanged HF model graphs with
GPU-owned asynchronous ACCEPT/RECV/SEND/CLOSE and eBPF completion reclamation,
without bfusion_tx. The network controller no longer stops after12 requests
or assumes fixture timestamps. It matches actual socket peers and admission
sequences and associates completion events with the real service ring.

Both checkpoints complete eight-connection mixed and all-long output waves,
connection churn, vocabulary rejection, RST and generation-time SIGTERM tests.
Fresh repository build artifacts also pass both model lifecycle tests.
This establishes bounded functional evidence, not latency/throughput/CPU
improvement, arbitrary backend support or overload-safe serving.

## Reusable implementation and production entrypoints

executor/io_uring_tcp.h contains transport control, independent of model
layers/weights/arithmetic. It discovers connection capacity from the loaded
sockhash map (4096 in this environment), maintains active/free connection
lists and per-peer reply FIFO, and holds private transmit buffers until
completion. Ring geometry derives from that capacity and the existing model
slots. The model page/slot layout and device model dispatcher remain
byte-identical; the Python adapter adds library-name recognition only.

Bootstrap metadata and tag constants have one definition in the existing
queue header. A small eBPF map records creator namespace metadata and the
bound kernel ring. io_uring_create uses bpf_get_ns_current_pid_tgid to resolve
the creator's actual PID namespace. Completion callbacks require that ring
and full final SEND or explicit abandoned-request NOP completion. No fixed
sequence ceiling or client timestamp is used for reclamation.

Intermediate output waits only for available model tokens; the last token
waits for DONE and final SEND completion releases the reservation. Socket
receive/cancel identifiers include a connection generation to prevent reuse
from retargeting old cancellation. EOF/failed send does not release a live
model buffer prematurely. On stop, ingress ceases admitting, model stream
quiescence precedes the quiesced flag, and the GPU cancels pending I/O,
reclaims abandoned requests and closes accepted FDs. Host calls occur at
bootstrap and stop, not per request or token.

The optional mode is selected with:

    make probes tools qwen-graph-uring
    ./build/bpfusion_load stream-uring-attach
    ./build/qwen_graph_uring PINNED_LOCAL_MODEL_PATH 180

The binary supports the same Qwen/Smol model paths as the existing HF adapter.
The duration is the existing CLI's bounded-test argument. NET_READY prints
the owning native PID; SIGTERM performs cleanup. After that server stops,
stream-detach removes its stream and io_uring hooks/maps; the owning runner
also removes its remaining ctl/stats/doorbell pins. The supplied replay/test
drivers carry this complete cleanup. Existing default/user-network binaries
remain unchanged choices; default stream-attach creates no io_uring map/hooks.
No new daemon, service, schedule, package, sysctl, affinity or driver change
is made. Linux TCP/SQPOLL and BPF still use CPU.

## Source and actual setup progression

Baseline is main0112b898f48c39c350d54b8a0ea29020b081dcce, original
yunwei356/bpfusion-dev, Linux7.3rc3, RTX5090/NVIDIA610.57.04, CUDA13.0.88 and
base Torch2.14.1+cu130/Transformers5.19.0. Cached model snapshots remain Qwen
7ae557604adf67be50417f59c2c2f167def9a775 and Smol
93efa2f097d58c2a74874c7e644dbc9b0cee75a2.

First Qwen preflight fails before READY: plain PID helper comparison sees
host TGID3563486 versus namespace PID202153 in the subsequent minimal
diagnosis. The printed allocation error is stale errno, not established OOM.
CPU-only ring setup reproduces bound0, then the PID-namespace helper repair
produces bound1. Initial sources/raw failure and both diagnoses are retained.
No Workspace namespace/permission/credential mutation or replacement occurs.

A negative control creates two rings in the same diagnostic process and marks
one private test slot DONE. Foreign-ring abandonment completion leaves it
untouched; the bound ring reclaims it. Both CQEs complete0. This tests the
correlation predicate, not access control or a general security boundary.

The repaired real Qwen preflight passes24 empty connections, one live reused
connection,three requests/66 exact tokens and147 equal terminal SQ/CQ positions.

## Complete functional coverage

Eight clients issue three barrier-separated waves, ensuring at most eight
outstanding requests. Input fragments, mixed binary/HTTP on reused connections,
prompt/context edges and changing KV ownership remain checked. This is not an
open-loop overload or unrestricted pipelining experiment.

| Actual condition / model | Requests | Complete exact tokens | Accepted/closed | Terminal SQ/CQ positions |
|---|---:|---:|---:|---:|
| Mixed Qwen |24|780|32/32|903|
| Mixed Smol |24|780|32/32|903|
| All gen64 Qwen |24|1536|32/32|1659|
| All gen64 Smol |24|1536|32/32|1659|
| Lifecycle Qwen, temporary candidate |8|130 plus2 checked prefix tokens|5/5|162|
| Lifecycle Smol, temporary candidate |8|130 plus2 checked prefix tokens|5/5|161|
| Lifecycle Qwen, repository target |8|130 plus2 checked prefix tokens|5/5|161|
| Lifecycle Smol, repository target |8|130 plus2 checked prefix tokens|5/5|161|

The32 connections include24 empty connects and eight real clients. All mixed/
long replies match the single exact whole-sequence references independently
generated before these runs in finding0039, not an alternative output set.
HF private-bank computation has unchanged per-request shapes and fresh KV
ownership; no dynamic-batch numerical equivalence is inferred.

Both mixed runs reach eight network requests/connections; device launch-batch
max is8 for Qwen and6 for Smol. Both all-long runs reach8 in all three counters.
Every run has graph_error0 and one host model launch. Normal runs have no
abandoned requests and all native drivers/pipelines exit0. Both lifecycle
and fresh production runs cover HTTP400 followed by valid reuse, invalid
binary EOF, RST after a real first token, successful subsequent connection,
and SIGTERM while a model/accept/receive remain pending. Each records three
abandoned requests: invalid binary, RST and interrupted generation. Intentional
HTTP rejection is a completed header response, not successful inference.

A code review catches a possible rejection header sent before DONE, which
would never receive a final reclamation tag. Lifecycle/all-long headers wait
for DONE on rejection; mixed source predates that one-branch correction.
Production uses shared types/constants and additionally refuses to publish
model quiescence after a failed model-stream synchronization. Source versions
and exact snapshots are retained; no mixed-source identity is concealed.

## Fidelity, lifecycle and source verification

Across the repaired preflight and eight complete subsequent runs,5218 full
model tokens and eight first-token prefixes are independently checked.
Partial/abandoned outputs are not counted as complete sequences or successful
requests. Every admitted slot is reclaimed, with head=completed, all eight
FREE slots, reservation/pending/error/drop/overflow0 and equal SQ/CQ head/tail.
Sends accepted by TCP are not a claim of peer acknowledgement; actual client
bytes, EOF and FD completion are the delivery evidence.

All-thread native strace between NET_READY and native SIGTERM has zero
accept/accept4,recvfrom/recvmsg,sendto/sendmsg and io_uring_enter calls.
Each server makes one setup, one bootstrap wake and one shutdown wake.
The latter occurs after SIGTERM and is not a steady request worker.
Traces exclude kernel threads and the separately executing Python clients.

make rebuilds probes/tools, the optional target and default/native controls
successfully. A real default stream-attach creates only the five original
pins; new io_uring maps/hooks are absent. Fresh build/qwen_graph_uring runs
pass both model lifecycle suites. Core model dispatch and model page/slot
layout comparisons pass. Sources/math are isolated from the transport changes;
default BPF ingress gains only the necessary stop-admission guard.

[Root self-review](../../bench/results/uring_concurrent_20261013/review.json)
reconstructs every request/token/prefix, reply-to-timestamp join, BPF counters,
queue endpoint and syscall window. This is self-review, not independent paper
plan/result review. [Raw artifacts](../../bench/results/uring_concurrent_20261013/)
include initial failures, namespace/foreign-ring controls, versions, actual
build commands and public-target tests.

    python3 bench/results/uring_concurrent_20261013/review.py

Fresh hardware reproduction uses the documented production make/load/run
entrypoints in the original Workspace and cached model runtime. The archived
production driver selects those artifacts; use a temporary writable copy and
adjust its reference-data base path before running. Prototype drivers instead
use their explicitly captured temporary source/loader paths. Never run a
record-writing driver inside the checkout. Restoration records owned temporary
sources/binaries/pins removed and original Coder/WIP/base packages/boot retained.

Remaining work: integrate the optimized vLLM adapter, demonstrate matched real
latency/throughput/CPU costs, test unrestricted pacing/overload/backpressure,
deeper pipelining, forced partial sends, device failures and extended operation.
Diagnostic reply records retain the first128 entries while execution continues;
trace-overflow qualification beyond that is open. IPv6/full text/JSON and
arbitrary model support remain unqualified. Keep the default module path while
this optional implementation and its practical value receive further evidence.
