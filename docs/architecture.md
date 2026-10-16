# BPFusion architecture

The qualified service paths use bootstrap-captured upstream model graphs
and resident GPU dispatchers,with HF references and an optimized vLLM adapter. Earlier synthetic MLP, host-driven HF and
handwritten Qwen paths remain separate references. Their maturity and compute
differ; see the README scope table before comparing results.

## Service and compute boundary

The service path owns Linux connections, request framing/admission, the shared
queue, completion observation, response ordering and recycling. The GPU backend
owns model computation and the input/output buffers that its execution consumes
and publishes. Current Qwen and Llama graph reuse demonstrates two architectures
through one capture interface, not arbitrary backend compatibility.

The intended reusable boundary keeps those service mechanisms independent of
model arithmetic. The existing queue carries token-ID requests and the
dispatcher performs LLM generation, so protocol and execution adapters are still
needed for a different output type or execution contract. No new runtime/plugin
framework has been implemented or claimed.

The matched comparison runs the same GPU computation with two network
paths. The native userspace alternative also retains GPU-controlled generation;
it is not forced into a Python per-token loop. Linux/eBPF and kernel TX remain
host CPU work.

## Current real-model data path

~~~text
TCP/HTTP -> sockmap framing/admission -> kernel pending queue
         -> shared model slots -> resident GPU -> reused HF/vLLM graphs
         -> produced tokens -> GPU-owned io_uring SEND -> Linux TCP
         -> completion/recycling -> reusable connections and slots
~~~

The optional BPF loop submits GPU-published SQEs and waits for completion/timer
progress. Linux still performs socket I/O and reservation atomics.
GPU execution advances model/KV inputs and publishes outputs.
Userspace initializes and waits for termination;no steady userspace request
worker owns admission,model-step launches or replies on this path.
The native alternative retains reused computation and uses timed epoll and
nonblocking send for networking.

## Linux kernel dependency

Observation: 2026-10-12. The tested host runs Linux7.3-rc3. Its installed
`include/linux/bpf_ksock.h` and compiled/BTF symbol names include
`bpf_ksock_create/connect/send/acquire/release`; saying BPF cannot send data
at all would be incorrect.

The latest mainline release on this date is7.3-rc7. The
[exact upstream header](https://github.com/torvalds/linux/blob/v7.3-rc7/include/linux/bpf_ksock.h)
and [implementation](https://github.com/torvalds/linux/blob/v7.3-rc7/net/core/bpf_ksock.c)
were also read through the official GitHub contents API. Creation rejects socket
types other than SOCK_DGRAM and protocols other than UDP/zero.
Create/connect/send require a user-task context; workqueue/kernel-thread
contexts return EOPNOTSUPP. Send is registered for sleepable syscall/LSM
contexts. These interfaces do not supply this prototype's asynchronous TCP
server response and connection lifecycle.

The default transport consequently uses `module/bfusion_tx.c` for kernel accept/receive
draining, completion polling, ordered TCP sends and socket/slot lifetime.
That is a current implementation and upstream-API boundary, not an old-kernel
bug or proof that a module-free design is impossible. Future upstream APIs
should be evaluated against TCP support, completion context and connection
ownership before replacing this adapter. No host kernel was changed during
the matched comparison.

Later qualification on2026-10-14 adds a
[module-free optional transport](findings/0044-uring-bpf-loop.md) on the same
tested host. GPU-owned io_uring handles TCP operations; an upstream sleepable
BPF loop submits published SQEs and waits for completion/timer CQ progress.
It reuses both HF and vLLM computation adapters without a steady userspace
request worker. Current BPF/io_uring interfaces,BTF/UAPI and libbpf remain
dependencies. The default module stays available; qualified CPU savings
against SQPOLL do not establish delivery superiority over efficient native.

## Historical UDP and host-driven controls

```
  client sendto (UDP :39400)
        |
        v
  tc/clsact ingress  (bpf/fusion.bpf.c)
        |  parse L2/L3/L4, match magic port
        |  take slot only if slots[i].state == FREE && done[i].state == FREE
        |  copy payload, stamp ingress_ns (bpf_ktime_get_ns), publish
        v
  pinned BPF page  (BF_PAGE_MMAP_BYTES, pinned at /sys/fs/bpf/bpfusion_ctl)
        |  resident reads slots[] / writes done[] in place
        |  producer owns slots[].state; responder owns done[].state
        v
  resident CUDA kernel  (executor/executor.cu, launched ONCE per run)
        |  spins: head > done_seq, slots[idx] == PENDING, done[idx] == FREE
        |  compute, fence, done[idx] = DONE, slots[idx] = FREE
        |  done_seq++ / served++
        v
  responder thread (userspace)
        |  waits on done_seq (futex), reads done[], recycles done[idx] = FREE
        |  sendto() the reply to the client
        v
  client recvfrom
```

The same page carries a second, independent token ring for the LLM path:

```
  client sendto (UDP :39402)
        |
        v
  llm_ingress (bpf/fusion.bpf.c)  ->  page.llm[idx].tok_in[], state=PENDING
        |
        v
  resident LLM executor (executor/llm_executor.py, Qwen2.5-0.5B, fp16)
        |  prefill + decode; writes tok_out[k], bumps produced after each token
        v
  client polls the slot; TTFT/TPOT from successive `produced` bumps
```


The LLM ring serves two transports. UDP (:39402) replies by having the client
poll `produced` in the page (above). TCP (:39403) parses the same request from a
stream segment at the tc hook, records `pad=1` + the peer in the slot, and the
executor streams each token id as a LE `u32` back on the accepted socket
(`0009`):

```
  client connect/send (TCP :39403)
        |
        v
  tc ingress TCP branch -> llm_fill(pad=1, peer=saddr:sport) -> slot PENDING
        |
        v
  resident LLM executor  ->  send(token) on the accepted socket (TCP_NODELAY)
        |
        v
  client recv (len = gen*4 bytes)
```
See `docs/findings/0009-tcp-path.md`.

An optional `--tcp --no-send` control replaces Python token sends with the
`bfusion_tx` module (finding 0012). The loader passes a real BPF map FD to
module initialization; `bpf_map_get` validates and holds the map. The module
uses the canonical page struct and the loading process network namespace.
It holds a TCP lookup reference across sends, sends outside RCU under the
socket lock without dereferencing `sk_socket`, and counts stream bytes exactly.
The executor publishes `DONE` after its final page access. TX releases the slot
only after `DONE` and complete send or terminal disconnect; `PENDING` is never
reclaimed on a timer. Kernel TX currently polls with `usleep_range(60, 120)`.
This control is not a GPU completion interrupt. The resident path below uses the sockmap/HTTP frontend.

The MLP path has **no per-request/per-batch GPU launch or control call**: the
kernel is launched once and stays resident; the host only drains the ingress
doorbell and samples the completion ring for the histograms. It is **not** a
fully no-userspace-worker path: a userspace responder thread still `sendto()`s
every reply, and the TCP/HTTP reply is not yet a kernel TX. The **LLM path is
even further** from the target — `executor/llm_executor.py` is a host-side worker
that accepts connections, runs HF prefill/decode per request and sends tokens.

The optional `executor/qwen.cu` reference now puts real Qwen prefill/decode,
KV cache and argmax inside one resident CUDA kernel (finding 0013), now
a cooperative grid with one CTA per discovered SM (finding 0016). It reads
the same token ring and publishes output directly for kernel TX. The host
only initializes and shuts down. Kernel accept and receive draining manage
connection lifetime. The default resident test now uses sockops/sockhash
stream framing and supports queued concurrent token-ID requests (finding 0014);
Content-Length HTTP POST framing now wraps the same token-ID body (finding 0015).
Stream requests carry a validation-pending flag until the GPU checks their
IDs against the loaded vocabulary. Rejections release their slot without
ending the resident grid: HTTP 400/empty body or binary connection EOF
(finding 0017). TX waits for validation before emitting a success header.
The kernel emits HTTP headers and streamed token bytes, retaining response order
on a connection even across ring wrap. Message offsets are read from the current
kernel strparser layout with CO-RE: helper byte offsets are skb-relative, whereas
several frames can share one skb. GPU text processing and continuous batching
remain open. Exact-token agreement is verified for the recorded eight-token
cases. Linear layers now use 16-row WMMA tiles with K partitioned across
eight warps per CTA; RoPE frequencies are initialized once at bootstrap.
Prompt vectors are evaluated together within each layer, with per-token
normalization and causal token/head attention. Decode and request execution
remain batch 1. Earlier scalar single-CTA/grid controls diverged
at the second prompt's output 21; the current Tensor Core reference matches
the first two 64-token prompts and diverges at the third prompt's output 63
(finding 0016). General long-output correctness remains unproven.

```
  client TCP / HTTP POST (:39403, binary token body)
    -> Linux TCP sequencing/reassembly
    -> sockops + sockhash stream parser/verdict (eBPF framing and admission)
    -> shared mmap BPF page, FREE -> WRITING -> PENDING
    -> one resident Qwen CUDA kernel (prefill/KV/decode/argmax)
    -> token publication + DONE (system-visible page stores)
    -> kernel module completion poll + ordered tcp_sendmsg_locked
    -> client HTTP header + token stream
```
The launcher loads weights, maps/registers the page, creates the listener,
launches CUDA and loads the module once. It then sleeps until shutdown.
There is no host accept/read/send, sampling or per-request launch loop in this
resident path. Kernel polling still has CPU cost; removing a userspace worker
is not proof of lower total host CPU work.

The compile-time `qwen-control` target provides a host-dispatch ablation of this
same path (finding 0018). The device kernel takes a uniform `once` argument:
false for the default launch-once loop, true to return after one whole request.
The control host polls the same queue and launches/synchronizes per request;
model math, grid resources, eBPF framing and kernel TX stay the same. It has a
host request-dispatch worker, so only the default binary meets the no-steady-
userspace-worker property. This control does not change the default path.

The `qwen-graph` variant captures actual HF eager-fp16 GPU operations during
bootstrap. Its native dispatcher graph reads/validates the same queue, fills
captured inputs on-device, schedules prefill/decode and publishes each completed
argmax to the page. The host launches that service graph once and sleeps.
The original serial path is recorded in findings0019/0020. Finding0023 now
allocates private input/KV/output graph banks from the existing ring-slot count.
Active requests launch independent batch1 model graphs with FireAndForget;
the parent tail joins all child work before sampling outputs and scheduling the
next step. Admission can continue while earlier requests are active. Model
weights remain shared, and graph/tensor owners survive through GPU shutdown
and native graph-exec destruction. Multiple graphs in flight alone do not
establish kernel overlap. A later process-local activity diagnostic in
finding0023 matches complete model-kernel counts and observes distinct-graph
interval overlap with eight clients,none with one. That instrumentation
does not measure SM instruction simultaneity or uninstrumented serving speed.
Finding0023 records a complete matched TCP
comparison: improved eight-client throughput, TTFT and completion against the
serial resident path, with slower per-request TPOT and larger startup/memory
costs. Its shared-GPU and temporary common TCP_NODELAY scope does not establish
an isolated or optimized-serving win.

Queue head/state/stop polling uses system-scope acquire loads; the native
backedge reloads shared publication words instead of reusing a cached condition.
The existing kernel connection/TX path and producer/page ABI are unchanged.
Computation may finish out of order, but DONE publication follows admission
order and waits for the previous DONE to be reclaimed. FREE or already reused
WRITING/PENDING proves that old ownership was released. This preserves the
head-indexed producer ring, including immediate client reuse across wrap;
the module withholds the last token while a request remains GPU-owned PENDING.
The [live kernel-TX regression](../tests/kernel_tx.py) reads the available prefix,
publishes DONE and then checks the final token and exact complete response.
Its cleanup uses the existing delete_module syscall and releases its owned tc
attachment/maps, so it does not require a separate rmmod executable.

At bootstrap, the existing HF RoPE pointwise helper and the RMSNorm
post-reduction expression are compiled with the default backend/mode and
emulate_precision_casts=True to preserve fp16 boundaries. RMSNorm retains
the original eager float32 conversion and pow/mean reduction; projections and
eager attention remain unchanged. Finding 0021 qualifies both default-native
modes and records complete matched component TCP comparisons with improved
TPOT/throughput at one and eight clients. The compiler is outside steady-state
request handling; warm-cache startup and the shared-GPU/common temporary
transport scope are reported.

Captured graphs append into their request's private shared KV buffers and expose
only the exact attention prefix, avoiding repeated prefix concatenation/copy-back
(finding0022). Both64-token/prompt-edge/mixed-length controls pass; the custom
WMMA reference retains its separately recorded accuracy boundary.
The `qwen-graph-control` variant now captures the same eight banks and uses
the same admission/compute dispatcher with once=true. After publishing one
FIFO DONE it returns so the host can synchronize and resume. An unfinished bank
moves from awaiting child sampling to awaiting its next launch before that
return; re-entry cannot sample the previous output twice. Both modes retain
GPU-controlled decode, HF computation and kernel TX. The host control has a
steady dispatch worker. Finding0024 qualifies both concurrent modes;
finding0020 remains the historical matched serial-dispatch measurement.

Upstream model computation candidates are recorded in the
[backend audit](upstream-backends.md). Finding0023 retains the failed MPK
whole-model qualification and mixed Plow results; neither changes the current
HF graph executor or supplies a resident network integration.

The optional qwen-graph-user-network target reuses the same capture and GPU
dispatcher with a CUDA-registered anonymous page of the existing ABI. A native
epoll loop accepts and buffers token-ID TCP/HTTP requests, publishes PENDING
and streams produced tokens after validation. It withholds the last token
until DONE and returns FREE only after response completion or disconnect
plus GPU release. One request per connection is active; later pipeline
requests stay buffered. There is no eBPF ingress or kernel TX in this control.
Its busy completion polling and userspace network calls are explicit
comparison costs, not default production behavior. See finding0025 for the
qualified scope and completed matched measurements.

The optional qwen-graph-user-network-wait build adds epoll_pwait2 with a
60000ns timeout to that same native loop. Readiness wakes it early; GPU
completion is checked after each wait. It changes host polling, with no
model/dispatcher change. Finding0027 records its strict qualification and
complete three-mode comparison: the timed native control uses less measured
executor-plus-TX CPU at gen64/eight clients in both models; client latency
and throughput remain inconclusive. This does not identify total service CPU
or a transport-only causal effect.

The module checks each owned socket's existing TCP poll callback before
accepting or draining input. Listener readiness reflects the accept queue;
peer readiness includes sockmap ingress data,EOF/shutdown and errors.
It preserves kernel accept/recv and queue/socket reclamation on readiness,
as well as the existing60-120us sweep. An arrival after a false readiness
snapshot can wait for the next sweep. Finding0028 records strict qualification
and the complete matched comparison with fresh result review; both primary
efficient-control CPU intervals and planned client-performance intervals cross
zero. CPU or latency gains are not established.

The module exposes a read-only tx_cpu_ns sysfs parameter for the TX task's
adjusted user+system CPU time. A retained task reference and mutex cover its
getter/shutdown lifetime. Native measurement adds this delta to the executor
process CPU clock and retains sequential-read brackets. CPU charged outside
these contexts, including RX/softirq/BPF/TCP, is excluded; this sum must not
be called total service CPU. Connection handling and the page ABI are unchanged.

The graph listener defaults to loopback and reuses BF_BIND for a concrete
IPv4 interface. With a listener FD,kernel TX derives its local lookup address
from inet_rcv_saddr; reply_addr is only the legacy no-listener fallback.
Concrete IPv4 binding avoids ambiguous wildcard lookup.
[Cross-node qualification](findings/0029-cross-node-network.md) retains actual
client/server tuples and the existing overlay/physical carrier boundary.

## Upstream optimized graph adapter

The optional vllm_graph backend captures upstream vLLM model/attention/compiler
graphs and official output-head/greedy-sampler computation. It reserves the
existing eight128-token slot regions once through the official KV block pool;
new requests require no host prefill or per-request allocation. GPU code
reconstructs metadata,packs mixed-length prefills,tensor-batches active
decodes and publishes the already-complete FIFO prefix before selecting new
work. Per-slot ownership and ordered DONE/TCP recycle rules remain.
The supported scope is one full-attention KV group on the two qualified
checkpoints, not arbitrary backend support. Finding0032 records strict traced
service fidelity and the completed matched traced comparison.

The ordinary adapter compiles BF_PAD_PREFILL and BF_PREFIX_RELEASE.
Leading dummy Q entries pack mixed lengths into unchanged uniform-query
upstream graphs. Real positions/lengths/KV remain unchanged; dummy slots-1
are skipped by upstream cache writes. Prefix publication drains consecutive
phase2 requests after all child outputs are consumed and a system fence.
It does not wait between publications for local TX reclamation; TX still owns
reservation release after its last slot access. DONE departure is local send
acceptance/recycle,not remote TCP ACK. Logical release IDs come from local
records,without rereading a published/reclaimed shared slot.
Findings0033/0034 record completed semantic/service/policy comparisons and
actual ordinary untraced single-client qualification. Named padded(serial) and
grouped(serial) executables preserve explicit compute-policy controls. Broader
untraced dynamic-batch timing and arbitrary-backend support remain open.

## Ownership rules (the correctness core)

| object | writer | reader | recycle |
|---|---|---|---|
| `slots[i].state` | producer (BPF) | GPU + responder | GPU sets `FREE` after reading `x[]` |
| `done[i].state` | GPU | responder | responder sets `FREE` after copying `y[]` |
| `head` | producer (BPF) | GPU + host | monotonic |
| `done_seq` | GPU | host (responder + sampler) | monotonic |
| `stop_ns` | host, once | GPU | |

The GPU takes slot `i = done_seq % BF_SLOTS` only when both
`slots[i].state == PENDING` (producer published) and `done[i].state == FREE`
(responder finished a previous round) — otherwise it would overwrite a
completion the responder is still reading.

## Memory ordering

- Device→host-visible reads of the page use `__ldcg` (gpu-scope load,
  **bypassing the SM L1**, which is not coherent with host memory). `volatile`
  alone reads stale values forever.
- Device publications use `__stcg` after `__threadfence_system()`.
- Host reads/writes of page words use `__atomic_load_n`/`__atomic_store_n`
  (acquire/release).

## Components

| file | role |
|---|---|
| `bpf/fusion.bpf.c` | ingress parse + slot publish + doorbell; drops split ctl/done |
| `bpf/include/bpfusion_queue.h` | the canonical page layout (single source of truth) |
| `executor/executor.cu` | resident kernel + responder thread + latency sampling |
| `executor/cuda_timer.h` | `%globaltimer` ↔ `CLOCK_MONOTONIC` calibration |
| `tools/client.c` | `verify`/`own`/`burst`/`paced` client (MLP path) |
| `executor/llm_executor.py` | host-driven HF Qwen baseline on the token ring |
| `executor/qwen.cu` | real resident Qwen inference, bootstrap and shutdown only on the host |
| `executor/qwen_graph.py` / `.cu` | bootstrap-only HF graph capture and native GPU request/model dispatch |
| `executor/vllm_graph.py` / `.cu` | upstream optimized capture/head and GPU prefill/tensor-batched decode |
| `executor/io_uring_tcp.h` | optional GPU-owned stock TCP accept/receive/send/close, with eBPF admission and final-CQ reclamation |
| `module/bfusion_tx.c` | kernel connection ownership, completion polling and ordered TCP/HTTP TX |
| `tools/llm_bench.py` | LLM TTFT/TPOT vs a direct in-process baseline |
| `tools/llm_load.py` | LLM concurrency sweep (goodput / TTFT / TPOT) |
| `tools/perfcount.c` | per-PID instruction/cycle counting (perf_event_open) |
| `tools/insn_token.py` | CPU instructions per generated token under load |
| `tools/llm_tcp_client.py` | TCP LLM client (request in, tokens on the socket) |

## What is not here yet

- General HTTP and text input/output — the resident reference implements
  Content-Length POST with binary token bodies (`0015`), including split writes,
  pipelining, half-close and concurrent correctness controls.
  The separate Python baseline still uses tc packet ingress (`0012`). Finite offered-load admission and drops are measured in findings0061..0065;
  physical packet-loss/retransmission and general overload behavior remain unqualified.
- GPU-side tokenization/detokenization and configurable sampling. The graph
  path already performs greedy token selection on-device, but still consumes
  pretokenized input. Full text conversion and stochastic sampling remain
  unqualified.
- General serving and shared-prefix KV caching. The HF graph path advances
  private batch1 banks; the optional vLLM adapter now qualifies tensor-batched
  prefill/decode for two full-attention checkpoints. Its matched traced timing
  is complete and inconclusive; arbitrary models and shared-prefix reuse
  remain unqualified.
- Direct-NIC and loss/retransmission/overload evaluation. Finding0029 now measures
  actual cross-node TCP over flannel/Tailscale and Ethernet; it is not bare-NIC
  TCP or GPUDirect.
- GPU-triggered completion notification. The legacy custom TCP worker uses
  a polling sweep;the optional BPF-loop path coordinates CQ/timer progress.
  Neither establishes a true GPU interrupt path or universal idle/active CPU benefit.

The optional stock SEND loop preserves its buffer until CQ completion, then
starts the next send at the completed byte offset and recopies only tokens
containing unsent bytes. BF_IO_FULL_COPY restores the former copy loop for
the matched ablation; it does not change the queue/model/transport policy.
[Finding0043](findings/0043-uring-incremental-copy.md) retains an unexplained
half-close failure and the limits of subsequent passing diagnostics.

Stock receive completions EAGAIN/EINTR clear the outstanding receive reference
and rearm it; they do not mean peer EOF. Zero marks read EOF, and other errors
mark connection death. The captured transient-read failure and common repair
are retained in finding0043.

After request publication, the stream verdict redirects ingress to the same
sockhash socket. On the qualified kernel this avoids the repeated-idle receive
stall observed with plain SK_PASS and divergent TCP/psock cursors. The flow key
reuses the existing passive-established sockhash insertion; no new network
route, kernel module or userspace request worker is added. This affects the
shared BPF ingress; both model default module compatibility workloads pass
alongside stock protocol qualification. Finding0043 retains the failures and candidate
evidence without claiming a general kernel fix.

## Optional upstream io_uring BPF loop

The optional qwen-graph-uring-loop and vllm-graph-uring-loop targets use the
same shared TCP transport and model computation with SINGLE_ISSUER/
DEFER_TASKRUN instead of SQPOLL. The creator enters a sleepable struct_ops
loop; BPF submits GPU-published SQEs and waits on CQ progress. A standard
60000ns multishot timeout supplies periodic wakeups. No steady userspace
request worker or custom TX module is used, but kernel/timer CPU work remains.

A separate report-region control prefix carries actual ring offsets and
stop/quiesce/finished state. Signal/deadline leaves steady serving, model
execution stops, and reentry drains cancellation, timer removal and closes
before report/queue memory is freed. Multishot SQ/CQ totals differ; each queue
must be empty independently. The request page ABI is unchanged. The
[finding](findings/0044-uring-bpf-loop.md) records current upstream dependencies,
failed setup/exit attempts and the completed measured CPU/delivery tradeoffs. This
does not replace the existing module default or qualify interrupt notification.

## Optional AMK computation adapter

executor/amk_graph.py loads the pinned upstream model/VM only at bootstrap;
executor/amk_graph.cu builds device-updatable prefill/decode graph nodes around
the unmodified AMK persistent cubin. Eight private banks feed the existing
qwen_graph.cu dispatcher and either existing TCP transport. Model arithmetic,
per-token publication, final-CQ ownership and queue ABI stay in their existing
components. The current finite checks qualify SmolLM2-135M FP16 at c1/c8;
the selected protocol and idle/reset/stop checks pass frozen whole-output
pools in a common runtime. Stronger eager-HF exact equality and arbitrary models remain unqualified.
The complete selected comparison is negative for AMK against both its native
TCP control and current vLLM; broader performance acceptance remains open.
See [finding0048](findings/0048-reused-amk-dispatch.md) for actual commands,
raw results, dependency compatibility and the ongoing experiment boundary.

## Optional coalesced GPU network progression

The amk-graph-uring-coalesced and vllm-graph-uring-coalesced targets store
network queue/connection/request state durably on the GPU and advance it once
inside existing model dispatchers between rounds. The standalone network
kernel runs after model quiescence only to drain shutdown. Shared queue ABI,
BPF/protocol and model arithmetic stay unchanged; parent/state/launch work
changes collectively. Current ordinary loop builds share the state refactor
and pass bounded legacy compatibility. The original captured loop remains the
performance component control. [Finding0050](findings/0050-coalesced-gpu-network.md)
reports AMK partial recovery, remaining native gap/latency cost and vLLM
throughput regressions. Defaults remain unchanged.

## Queue publication in coalesced builds

Current BF_IO_COALESCED rounds acquire a finite CQ tail snapshot, consume that
batch and release-publish its head after reads. SQ reservations use a
conservative round-local head/tail snapshot; buffer/SQE writes are system
ordered before one release tail publication, including the early cancel-return
path. Ring-full work can defer to the next round. Timer, FIFO/final ownership,
model quiescence, queue ABI and model arithmetic remain unchanged. Other builds
retain existing per-entry publication. The
[completed experiment](findings/0051-batched-ring-publication.md) qualifies the
selected protocol/lifecycle and records partial AMK/Qwen throughput gains,
remaining native gaps and unresolved vLLM c8 short-output latency. Finding0050's
numbers describe the earlier coalescing implementation. No dynamic system-access
or model-overlap cause is established.

## Idle model admission in coalesced vLLM builds

After io_progress, the vLLM dispatcher checks whether all admitted model work
has retired and the mapped SQ head still differs from its published tail.
It then keeps progressing I/O before fresh model admission. Existing unfinished
admitted computation remains eligible. SQ consumption is separate from CQ/TCP
completion and buffer ownership; stop is revisited each iteration. A stalled
issuer can defer fresh admission, and arbitrary fairness/backpressure bounds
are unproved. No timer, ABI, worker or model math change is added.

[Finding0052](findings/0052-model-admission-after-sq-consumption.md) measures
vLLM local short-output latency recovery with remaining native losses. Its
two-hook candidate regresses AMK; selected main restores the AMK prior policy
and retains only the vLLM hook. Frozen collected sources and that post-result
selection are separately recorded. Noncoalesced/default targets keep their
existing policy; trace sensitivity prevents full-matrix batching mediation.

## Completed-response drain in coalesced vLLM admission

[Finding0053](findings/0053-final-response-drain-before-admission.md) extends
only the existing vLLM experimental coalesced admission hook. After
io_progress, when Control.retired equals Control.seen, fresh admission waits
until IoState.next_final equals that retired model prefix and SQ head equals
tail. next_final counts consumed final SEND/abort completions; this is not a
TCP-ACK or all-network-idle condition. Already unfinished model work retains
the preceding admission behavior.

This postpones fresh model launches while the completed response prefix
progresses. Stop remains checked before the gate and uses the existing
model-quiescence/shutdown worker sequence. No I/O/BPF/ABI, timer, worker or
model arithmetic change is introduced. The global final-send frontier and
per-peer reply chain remain ordered; an earlier backpressured final send may
stall fresh admission on other peers. The finite comparison supports local
latency recovery and fewer aggregate model rounds, not arbitrary-peer
fairness, causal mediation or generic portability.

## Bookkeeping-placement experiment boundary

[Finding0054](findings/0054-gpu-local-io-bookkeeping.md) records a completed
candidate that kept loop-control flags host/BPF-shared while placing regular
I/O accounting in device memory and copying only the finished report suffix.
Both models' predeclared long-output TPS contrasts against host bookkeeping
are inconclusive, so selected main retains the existing mapped host report.
The experimental split-control allocation is preserved in the archive,
not introduced into current serving. Shared page/control ABI, model math,
timer cadence, workers and current defaults remain as before this experiment.
Its finite shutdown/protocol success does not establish arbitrary-backend
or AMK acceptance, physical PCIe mediation or universal performance benefit.

## Current standalone and coalesced I/O tradeoff

[Finding0055](findings/0055-current-gpu-io-arrangements.md) qualifies and compares
the existing current standalone GPU I/O constructor against current coalesced
and efficient native TCP, using identical reused vLLM model computation.
Standalone runs independent resident network progression on a nonblocking CUDA
stream; coalesced advances I/O inside the model dispatcher and has batched
publication/completed-response admission. Current shared durable state and
per-constructor policy differences form a bundle, not a pure overlap ablation.

Smol long-output throughput recovery over coalesced is supported, while native
still wins; Qwen recovery is inconclusive and concurrent-short-output latency
worsens. More standalone model rounds accompany the Smol recovery, so aggregate
round count alone does not explain the constructor difference. Existing targets
and defaults are unchanged, with zero production-code growth. Finite protocol/
lifecycle qualification does not establish arbitrary backend acceptance.

## Independent-worker publication experiment

[Finding0056](findings/0056-independent-gpu-queue-publication.md) extends seven
existing coalesced publication conditions to independent BPF-loop builds while
leaving residency/start/shutdown conditions unchanged. It qualifies the finite
protocol/lifecycle but demonstrates no primary throughput gain for either model.
Selected source restores original per-entry independent publication. Captured
candidate sources remain reproducible; no default, timer, ABI or compute change
is retained. The tested bundle does not isolate dynamic PCIe or GPU-time costs.

## Long-output observation boundary

[Finding0057](findings/0057-long-output-service-timeline.md) observes current
independent BPF-loop and efficient native TCP with identical reused vLLM math.
Private logical tracing/profiling adds no serving/default change. All40
client/replay cells pass finite checks; two Smol activity profiles fail exact
coverage, leaving the planned integrated decomposition invalid. Complete Qwen
duration/trajectory comparisons do not identify an exclusive bottleneck.

## Batched token publication experiment boundary

[Finding0058](findings/0058-batched-token-publication.md) tests one system fence
for a completed batch's token payloads before publishing produced counts.
DONE/recycle ownership and model math stay unchanged. The full comparison stops
on an original-control finite-output-pool failure; candidate promotion is
unsupported. Selected main restores the original per-row publisher, with no
retained production/default change.

## Upstream batch-invariant compute boundary

[Finding0059](findings/0059-batch-invariant-serving.md) qualifies the existing
GPU-owned graph interface in upstream batch-invariant FP16 mode against official
LLM.generate outputs and exact history replay for the two tested checkpoints.
The optional test environment changes upstream compute behavior equally for loop
and native TCP; transport/dispatcher sources are unchanged. Ordinary outputs pass
the finite frozen single-sequence checks, but throughput superiority is
unestablished and concurrent long-output TTFT worsens. No production mode/default,
new adapter framework, arbitrary-backend or default-mode fidelity claim follows.

## Adaptive idle-wait experiment boundary

[Finding0060](findings/0060-adaptive-kernel-wait.md) tests request-aware updates
to the existing before-submit multishot timer, with unchanged reused model math.
Process CPU falls, but Smol achieved fixed-burst TPS worsens. Removing idle
heartbeat wakeups also exposes a helper-stop wakeup bug; the archived candidate
forwards shutdown to the recorded wait-owner TID and passes repaired finite
protocol/lifecycle checks. The after-submit variant remains unchanged.
Select original behavior: no timer/report/helper/default change is retained.
Prepared compatibility adapters are unexecuted, not backend qualification.

## Offered-load admission boundary

[Finding0061](findings/0061-offered-load-admission.md) completes a finite
same-compute offered-load collection against event-driven native TCP.
The current stream verdict validates a frame and calls llm_reserve; a
reserved next physical slot causes SK_DROP and increments page drops/llm busy.
There is no pending request backlog between framing and the eight model slots.
Balanced SQ/CQ cursors and zero ring dropped/overflow counters do not account
for this separate model-admission failure boundary.

All709 observed kernel timeouts have no token and no independently replayed
model admission, with matching per-executor admission-drop counters. Native
buffers instead. Successful-request P99 can consequently appear low while
the full service fails requests. The all-attempt analysis retains unknown
upper tails rather than treating timeouts as completed60s responses.

At finding0061 publication, independent review confirms the negative service
result; owned temporary state is removed and copied-data analyses replay
identically. Original source/defaults remain selected at that step. The subsequent private waiting-queue
candidate has now completed the separately scoped finding0062 below; its
qualification does not select production behavior or establish arbitrary
load/backend support. Admission/lifetime behavior belongs to the driver;
model arithmetic remains reused and unchanged.

## Finite pending-admission candidate

[Finding0062](findings/0062-pending-admission-tails.md) qualifies a private FIFO
between frame validation and physical model-slot publication. The existing
kernel loop is its single consumer; model arithmetic and GPU reservation
ownership are unchanged. Capacity is discovered from somaxconn; a full queue
still drops, so finite buffering is not complete transport backpressure.
The shared page adds eight tail bytes, preserving existing offsets but requiring
a same-header module rebuild. Global backlog conservatively delays normal EOF
recycling; stop cancels unadmitted work instead of claiming completed responses.

Both paths/models complete all 15,360 measured requests. The primary 64/s
P99 effects remain inconclusive. Qwen/96 has better P99 but worse median and
process CPU; no general performance or total-CPU saving follows. Source,
qualification, raw data and independent review are archived together.
Subsequent [ordinary-source integration](../bench/results/pending_admission_integration_20261015/)
selects the finite queue and repaired wait/stop behavior for the BPF loop,
with the event-driven native competitor synchronized too. The normal Makefile
passes its absolute BUILD directory to loader/loop object bindings; private
source paths are absent. The page-size change requires a module rebuild.
Four newly compiled loop/native protocol executors pass2560 outcomes/93504
replayed model tokens. Other shared-adapter builds are compile coverage only.
This adoption repairs observed admission loss; it does not establish general
performance superiority or complete TCP backpressure.


## Native FIFO admission and explicit build capacity

The ordinary native TCP alternative now uses the eligible-complete-frame FIFO
from findings0063/0064. A connection queues one eligible frame once; its next
frame becomes eligible after its preceding response retires. Shared Peer
ownership survives reply completion and disconnect, and stale disconnected
entries are discarded. This preserves per-connection response ordering while
removing FD-ordered cross-connection admission. It does not establish transport
superiority; the fair comparison does not reproduce the earlier tail advantage.

The canonical header still defaults BF_LLM_SLOTS to8. A CPPFLAGS override is
propagated consistently by the normal Makefile to queue consumers, with its
absolute BUILD binding retained even for command-line CPPFLAGS. Each capacity
needs a separate build directory and matching BPF/loader/GPU objects.
At16, the header preprocesses identically to finding0064's qualified snapshot.
The existing module rejects mismatched page sizes; module16 and HF/AMK16
are outside the qualified scope.

The [integration record](../bench/results/batch_capacity_integration_20261015/)
contains actual normal-Make builds and six traced protocol executors across
both checkpoints:6416 outcomes including2578 intended rejects,235552 replayed
tokens,actual batch1..8 or1..16 and normal ownership/queue drain.
Four ordinary native lifecycle cases pass:HF/vLLM with both checkpoints at8,
32 actions and652 checked tokens each,including two partial observations.
Frozen references are unchanged; no untraced performance or universal fidelity
generalization follows.
Default8 and model arithmetic remain unchanged.


## Mixed prefill/decode candidate

[Finding0065](findings/0065-mixed-prefill-decode.md) packs real prefill inputs
and active decode tokens into one upstream graph call. It changes request
offsets/metadata and scheduling,not arithmetic or network ownership.
Full/protocol trajectories pass graph replay and independently reconstructed
attention metadata at16 banks. Both transports gain in mean TPOT;general
eBPF speed superiority is unproven and adverse Qwen ITL P99 remains.
The original candidate and its measurement remain frozen in the archive.
[Ordinary-source integration](findings/0068-mixed-source-integration.md) selects
explicit vllm-mixed-uring-loop and vllm-mixed-user-network-wait targets after
normal default8 protocol and partial-stop acceptance. Legacy homogeneous
controls retain their original source/meaning. The close-scan candidate is
separate and remains unselected.

## Opaque one-shot graph adapter

[graph_server.cu](../executor/graph_server.cu) reuses both transport headers with
caller-owned captured graphs and opaque32-bit input/output words. Per-slot
graphs execute as GPU fire-and-forget children; a tail launch observes outputs
after child completion, then publishes and retires the FIFO prefix. Input and
output buffers remain device-owned and are retained by the caller for the whole
serve lifetime. There is no model/vocabulary/KV metadata in this adapter.

[ABI1 and example](graph-backends.md) are qualified for cuBLAS/cuFFT on the tested
stack with default8. This fixed-shape one-shot interface is experimental;
autoregressive model scheduling remains separate and the existing wire shape
is limited to64 words. [Finding0067](findings/0067-opaque-graph-backend.md)
retains finite numerical/lifecycle checks and failed setup/cleanup attempts.

[Finding0066](findings/0066-tail-path-diagnosis.md) closes the tail diagnostic
and conservative close-scan candidate. Its confirmation is inconclusive, so
the production transport header remains unchanged.
