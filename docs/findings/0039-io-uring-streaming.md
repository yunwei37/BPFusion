# Stock io_uring streaming with real model graphs

The finite io_uring/eBPF prototype now delivers complete1/64-token model
outputs through asynchronous streaming SENDs. Qwen and Smol each complete
12 requests/390 exact independently generated tokens,2036 complete wire
bytes,390 consumed send completions and normal EOF/GPU CLOSE. The actual
client receives each long response in42–64 body chunks. Production defaults
and computation remain unchanged; no performance benefit is established.

## Implementation and invariant

Source baseline main80e69456376165ec2f04bb5b2f2975015d1683a4 and the original
Workspace/kernel/RTX5090/base HF runtime are retained. The native model
dispatcher is byte-identical to production, Python changes only library
lookup, and BPF admission/queue/recycle source equals finding0038.

The temporary network kernel reads model-owned produced/state, sends newly
available prefixes, and holds the final token until DONE. HTTP Content-Length
reflects actual n_gen*4. Intermediate SENDs carry ordinary completion IDs;
only final SENDs carry the reclamation tag. Partial positive sends use the
remaining private bytes and require a full completion before release.
All GPU slot reads/copies precede final tagged publication; afterward the
sender touches only its private output buffer/CQ/record. The unchanged
kernel-side eBPF completion callback owns FREE/reservation release. No GPU/
CPU map read-modify-write, host network loop, host per-token model launch,
periodic wakeup/keepalive or SQPOLL idle tuning is introduced.

Per-request device records distinguish successful intermediate sends selected
from a non-DONE model observation and final tagged sends. They do not timestamp
the subsequent physical SEND completion against model DONE, so do not interpret
the intermediate counter as precise pre-DONE completion timing. Client body
chunks and exact sequences independently establish incremental delivery.
Each tested gen64 request records first_produced1,last_produced64,63 successful
intermediate sends and one final send. Short gen1 requests send only at DONE.

## Frozen references and workload

Initial references for an alternating1/64 output schedule are retained unused
in model/initial_oracle/. Before any candidate observation, the schedule changes
to cover long binary and HTTP responses and prompt64/gen64 together. This is
a coverage change, not selection from candidate failures or favorable timing.

The final independent eager-HF FP16 oracle freezes both checkpoints at
2026-10-13T01:50:59.810351UTC. It starts each prompt with a fresh cache,
greedily selects its own token, advances its own HF KV history and never takes
tokens or cache from the candidate. Every whole sequence is fixed before
serving, with no tolerance, alternative set, reference expansion or forced
served history. Runtime/path/source details are archived.

Prompt lengths are1,2,5,8,16,31,63,64,2,5,8,1; output lengths are
1,64,1,64,64,1,64,64,1,1,1,64. Each run has six long and six short requests,
alternating binary/HTTP, fragmented input, one cold asynchronous accept,
eight cold receives, slot wrap/reuse, client half-close and GPU-owned CLOSE.
The first8 requests are delayed2.2seconds; this and strace are diagnosis
apparatus, not a workload suitable for serving throughput claims.

## Complete actual results

| Model | UTC start/end2026-10-13 | Requests/tokens | SEND/CQ count | Intermediate/final sends | Wire bytes |
|---|---|---:|---:|---:|---:|
| Qwen |01:52:30–01:53:48|12/390|390|378/12|2036|
| Smol |01:53:48–01:55:19|12/390|390|378/12|2036|

Both candidate drivers and the outer pipeline exit0. No failed delivery,
selected exclusion or favorable candidate retry occurs. All24 full outputs/
780 tokens equal their exact pre-observation oracle. Per model, SQ head=tail=
CQ head=tail=406: NOP+ACCEPT+12receives+390sends+EOFreceive+CLOSE. Dropped/
overflow0,head12,reserved0,eight FREE slots. BPF admits/recycles12,links one
socket and reports zero busy/invalid-parser/failed-link counts. The original
HF dispatcher reports one host launch,390 device model launches,eight banks,
max_active1 and graph_error0.

Every gen64 response has multiple actual client body chunks with first arrival
before last. Most have64 chunks; the final Qwen/Smol responses have42/43.
TCP coalescing is retained. This is not a claim that each client chunk is a
GPU step or that delivery timestamps measure pure decode/network latency.

Each native all-thread trace between NET_READY and native SIGTERM has zero
accept/accept4,recvfrom/recvmsg,sendto/sendmsg and io_uring_enter calls.
One setup and one bootstrap wake precede READY. Kernel TCP/SQPOLL and BPF
still use CPU; no total CPU/energy attribution follows.

## Reproduce, restoration and open scope

[Raw sources, oracle, client bytes/chunks and traces](../../bench/results/uring_streaming_20261013/)
and [root replay self-review](../../bench/results/uring_streaming_20261013/review.json)
reconstruct every request/token,wire byte,device counter,slot and native syscall
boundary. This is root self-review, not an independent research result review.

    python3 bench/results/uring_streaming_20261013/review.py

For a fresh hardware run, use the original Workspace. Copy this archive to a
new OS temporary directory, substitute its root for the recorded old temporary
path in loader.c, rebuild using builds.json and model/build.json with the new
paths and original repo includes, run model/oracle.py, then model/pipeline.py.
Drivers write beside source; do not execute them in the checkout. The current
repo supplies unchanged queue/vmlinux dependencies and cached model/runtime.
No vLLM environment or new package is installed.

Restoration records removed owned sources/binaries/pins, no own GPU process/
module, same boot/base packages and preserved original Coder processes/WIP.
Endpoint observations do not establish continuous host isolation.

This extends the previous gen1 qualification to real long-output streaming,
including the existing128-token context boundary. It remains a one-connection,
12-tag prototype. Concurrent connections, generic ring/FD completion ownership,
backpressure, rejection, partial-send/error qualification, abort/stop during
pending I/O and optimized-vLLM integration remain open. Keep the existing
production module/default. Matching latency/throughput/CPU comparisons must
follow those integration boundaries; do not transfer older backend gains.
