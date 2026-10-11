# Socket readiness checks and measured request-worker CPU

## Question and admission

There is no formal paper RQ. Preserve the full retained Linux TCP/HTTP +
eBPF/shared queue -> resident reused real-model computation -> asynchronous
kernel TX objective, with improved throughput/latency and no steady userspace
request worker.

Question: after using existing Linux socket readiness to avoid unnecessary
accept/recv attempts, does the eBPF/kernel path use less executor-process +
TX-task CPU than an efficient native userspace worker, and what client
latency/throughput accompanies it? Planned role: supporting component evidence.

Finding0027 already contradicts the CPU-saving prediction for the unguarded
kernel path. Its complete raw matrix remains closed. The subsequent unchanged
Qwen strict-stage perf diagnostic localizes327/1116 stacks to recv and233
to accept. Linux kernel_accept allocates a socket before attempting acceptance.
This does not predict a speedup or reproduce the primary cell window, but
identifies a specific avoidable source operation.

Expected result: readiness guards reduce charged kernel work sufficiently to
make control-minus-resident CPU positive at gen64/client8. Competing explanations
are costly timer scheduling, actual TX/inline networking, readiness polling
itself, and shared-host conditions. Negative CPU differences contradict this
implementation prediction; crossing-zero intervals are inconclusive. Client
performance cannot be inferred from CPU reduction. A latency/throughput loss
must be reported, not hidden by a CPU-only headline.

The largest credible story this unlocks is resource-efficient ordinary Linux
serving with reused compute against a credible same-compute CPU alternative.
It does not establish total-service CPU, SOTA serving or a complete paper thesis.
Compared with immediately installing a different SGLang computation stack,
this very small source change and existing runnable paired control better
discriminate the currently identified request-path overhead. Official external
serving and physical-NIC work remain necessary beyond this supporting result.

Prior valid outputs cannot answer this source change by reanalysis. Do not
run another arithmetic campaign or duplicate the unchanged matrix. Keep negative,
failed and inconclusive rows. No baseline count expansion.

## Source and reused assets

Only module/bfusion_tx.c changes behavior:
- Before kernel_accept, use the listener's existing poll callback and EPOLLIN.
- Before receive draining, use each owned socket's poll callback with
  EPOLLIN/EPOLLRDNORM/EPOLLRDHUP/EPOLLHUP/EPOLLERR.
- A readiness false negative due to concurrent arrival is revisited in the
  existing next sweep. Readiness never releases queue memory.
- On readiness, existing kernel_accept/kernel_recvmsg, error handling,
  peer_pending, socket ownership, partial sends and final FREE publication remain.
- Keep60-120us polling, model math/precision/KV, GPU dispatcher, common TCP
  behavior, page ABI and CPU-accounting counters unchanged. No new option,
  scheduler, timer, process or service.

Linux7.3-rc3 TCP poll uses sockmap's sock_is_readable callback as well as TCP
input, EOF/error state. Do not substitute an ordinary skb queue emptiness
test that misses BPF ingress messages.
Source references:
https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp.c
https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_bpf.c
https://github.com/torvalds/linux/blob/v7.3-rc3/net/core/skmsg.c
https://github.com/torvalds/linux/blob/v7.3-rc3/net/socket.c
https://github.com/torvalds/linux/blob/v7.3-rc3/include/linux/poll.h

Scope: the implementation may change readiness checks in the owning TX module;
it preserves model computation, network protocol, socket/queue lifetime and
existing wait policy. Necessary docs record the actual evidence.

## Conditions, workloads and metrics

Reuse bench/resident_dispatch.py and tests/resident_qwen.py unchanged.
Same three conditions as finding0027: kernel/eBPF, busy native epoll and
native epoll_pwait2 timeout60000ns; all run identical FP16 HF computation,
eight private graph/KV banks and the same resident device dispatcher.
These are component controls; no external SOTA baseline is claimed.
Busy mode is a minimal CPU/latency tradeoff control, not the headline competitor.

Models SmolLM2-135M and Qwen2.5-0.5B-Instruct; four prompt cases,
gen1/64 x clients1/8,64 requests/cell,five paired process blocks.
The native predetermined mode/cell rotation is unchanged.
Totals120 cells,7680 measured requests,249600 exact tokens,30 normal executors.
Eight warmups/executor remain outside measurement.

Primary: efficient-control-minus-resident process+TX CPU us/request at
gen64/client8, separately per model. Retain busy-control estimates as context.
Sequential raw before/after CPU values, read brackets and component deltas
remain authoritative; all components must reconstruct. This measure excludes
networking charged outside TX/client/GPU CPU and is not total service CPU.
No causal old-new improvement is inferred from historic matrices.

Secondary planned standard client metrics: control-minus-resident TTFT at
gen1/client1, resident-minus-control TPS atgen64/client8, all raw
TTFT/TPOT/completion. Definitions unchanged:
https://docs.vllm.ai/en/latest/api/vllm/benchmarks/serve/
Five-pair nominal two-sided t95(df4), no family-wide/Pareto/equivalence claim.
Retain all client negatives/crossing-zero intervals. Independent eager-HF
tokens are generated before service startup and never passed as expected
outputs to the GPU.

## Execution and completion

Original yunwei356/bpfusion-dev Workspace /workspaces/repository,main.
Preserve untracked tools/setup_env.sh and other owners/services.
Fresh plan review precedes canonical qualification/preflight.
Build the owning module through the documented Kbuild command:
make -C module KDIR=/usr/src/linux-headers-7.3.0-070300rc3-generic CC=gcc-15

Strict qualification: both checkpoints with --gen64,--prefill-edges and
./build/qwen_graph via tests/resident_qwen.py. The userspace source is unchanged;
reuse its completed strict qualification from finding0027 and verify all three
current modes in native preflight/full collection. The strict suite covers fragmented input,
5000 empty connections,8-client wrap/reuse,rejections,mixed lengths,pipelining,
half-close,invalid IDs,exact outputs,helper SIGTERM,trace and cleanup.
A readiness defect requires repair before performance; never weaken the oracle.

Preflight: both checkpoints, unchanged native --preflight --gen64 with all
three executors. It verifies engagement/counters/raw CPU availability, not speed.
Qualification and preflight are dependencies, not independent paper results.

After both pass, commit/push the candidate source and plan, freeze the
revision, and run the two native full commands:
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --user-network-wait-executor ./build/qwen_graph_user_network_wait --model HuggingFaceTB/SmolLM2-135M --output bench/results/readiness_network_smol_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --user-network-wait-executor ./build/qwen_graph_user_network_wait --model Qwen/Qwen2.5-0.5B-Instruct --output bench/results/readiness_network_qwen_20261011.jsonl

Native command/exit stdout, raw JSONL, native --analyze and current before/
during/after host GPU/boot/fault observations are ordinary authoritative
artifacts. Record shared-device exposure and unknowns. No co-tenant lifecycle
changes or claim of isolation. Keep source/oracle/timeout fixed throughout.
An observation timeout does not imply the live runner stopped.

Complete every cell; all30 executors need normal exits,onehostlaunch,
8580 model-graph steps,zeroerrors,eightbanks,maxactive8 and normal
queue/TX/recycle. Fresh independent result review reconstructs coverage,oracle,
CPU/timing/order,mechanism,uncertainty and environment exposure after both finish.
A valid contradictory result closes this candidate comparison without indefinite
retries; select next work by new causal information and full-goal relevance.
The unchanged full objective remains active.
