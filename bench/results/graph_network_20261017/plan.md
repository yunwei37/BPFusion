# Bounded small-graph network / CPU experiment

Plan written 2026-10-17 UTC (2026-10-16 America/Los_Angeles), before any
measurement of this experiment. Sole-thread execution and self-audit; no other
agent or independent-person review. The user closes the LLM speed competition
after the frozen five-block16/32/official comparison. That comparison is sealed
and committed first. This experiment asks a different question:

When existing library GPU work is small and requests frequent, does moving
TCP/framing/admission/reply lifetime into eBPF improve CPU cost or delivered
tail latency compared with efficient userspace epoll using the SAME GPU graph?

## Controls and workload

Reuse ordinary kernel_network_sourcebuild8, graph_server_kernel_network.so
versus graph_server_user_network_wait.so, default8 slots and exactly the same
graph dispatcher/buffers. No model math optimization, fake delay, empty kernel
or userspace Python-per-request server. Existing torch.mm/cuBLAS8x8FP32 and
torch.fft.fft/cuFFT32complex64 both use64 input/output32-bit words. Repeating
the SAME library operation1/16/256 times within a captured graph changes work
duration while leaving inputs/outputs, arithmetic oracle and transport fixed.
Writes to the same output preserve capture dependencies. Report measured graph
calibration separately from whole-request latency; no isolated-kernel latency
claim from host graph replay.

The binary TCP protocol has280-byte requests and256-byte responses. Persistent
connections are the primary high-request-rate workload; this bounds connection
setup noise and tests per-request path work. Both transports receive the same
request payloads and arrival offsets. The remote client is the existing bounded
g10 Job, server the original bpfusion-dev Workspace on lab/RTX5090. This is
inter-node cluster networking, not a datacenter-wide deployment claim.
Upstream kernels, graph layout, TCP options and service affinity remain matched.
The optional userspace io_uring comparator is added only if results expose a
specific epoll bottleneck; graph_server_uring_loop is NOT that comparator.

## Bounded acquisition and selection

1. Qualify all six operation/repetition combinations with independent numeric
   outputs and both transports, graph calibration, reuse/wrap/reset/shutdown.
   Existing repeated-one arithmetic oracle is unchanged; inspect normal stop
   and io_uring errors/counters. Record all failures and repairs.
2. Screening: both operations, repetitions1/16/256, unrestricted service CPU,
   geometric offered rates1000,4000,16000,64000 requests/s,6s/cell plus drain.
   Stop a path's escalation after clear saturation; still run its matched peer
   at the same rates. If neither saturates, extend once to256000/s. Saturation
   means delivered rate<90% offered OR>1% failed OR growing scheduled-response
   backlog (last-quarter mean exceeds first-quarter mean by100ms and is more
   than twice it). A client ceiling is a client limit, never server saturation.
3. CPU pressure: both operations at repetition1, service affinity1 and2 CPUs,
   same geometric rates and saturation rule. Restrict only the process started
   by this benchmark and its inherited threads; never foreign processes,
   global CPUs, Workspace quotas or production services. Discover allowed CPUs
   and use the same first one/two allowed CPUs for paired paths; report sharing.
   Apply inherited affinity before startup and verify/apply it to all current
   owned-service threads after warmup. Check actual sampled thread affinity;
   escaped/new threads invalidate a claimed finite-core cell until repaired.
4. Confirm with NEW fixed seeds and five counterbalanced process pairs,
   20s/cell plus drain, at three deterministic cells chosen from screening:
   (a) fastest-work operation/rate with the largest provisional CPU benefit;
   (b) fastest-work operation/rate with largest provisional P99 benefit;
   (c) CPU1 operation/rate with largest provisional CPU benefit.
   Eligible cells: no failures and attained>=98% offered on BOTH paths,
   P99 client timer-dispatch lag<=max(1ms,10% scheduled-response P99), and no
   unstable resource/correctness evidence. Deduplicate identical selections;
   if no eligible cell, confirm the lowest-rate repetition1 cell for each
   operation plus CPU1 lowest-rate matmul. This prevents cherry-picked
   screen-only claims. Record selection before confirmation. Use independent
   confirmation; no retuning, exclusions or extra searches after its results.
   Categories without an eligible repetition1 cell are left unselected; if no
   selection remains use the three stated fallback cells. Ties sort by operation
   name then rate. Confirmation seeds=420261017+selection_index*100+pair; even
   (pair+selection_index) runs kernel then native, odd runs native then kernel.
   Screening itself supplies work-duration/load/core crossovers, with honest
   unbracketed boundaries where no crossover occurs.

Client uses multiple ordinary worker processes and persistent connections,
deterministic open-loop offsets, per-connection ordered replies and complete
drain. Record every scheduled attempt including late sends, timeout, short
reply, reset and numerical mismatch. Preserve payload/received bytes and exact
timing before decoding. Queue waiting for a busy client connection is reported
as client backlog and included in scheduled-response latency, never hidden.
A high timer-dispatch lag invalidates a server-capacity interpretation and
triggers client-only repair followed by a NEW labeled acquisition, preserving
failed originals. Fixed timeout30s is a declared finite-drain boundary.

## Metrics and decision fixed before acquisition

Co-primary metrics: owned process-group CPU-ms/attempt and scheduled-arrival
to complete-response P99. Also report send-origin P99, P50/P90/P95/P99/P99.9/
maximum and empirical CDF, timer dispatch lag, connection wait, throughput
(successes divided by offered window plus drain), all attempted/completed/
failed counts. CPU/attempt counts failures; additionally CPU/success prevents
failure-heavy cells looking cheap. Record idle group CPU and whole-host
user/system/IRQ/softirq active CPU with adjacent idle windows. TGID, io-wq,
visible kernel workers, cgroup and host totals are nested, never summed.
Whole-host totals include foreign tenants and observer cost; report raw and
idle-context deltas separately, never call them exclusive service cost.
Observe actual affinity, GPU applications, clock/throttling/context/CPU pressure.

Confirmation statistics: paired log ratios, five process pairs, nominal
Student-t95(df4); disclose small sample/multiple selected cells. A local useful
advantage requires zero observed confirmation failures, delivered throughput
ratio lower95>=0.98, plus either:
* CPU benefit: CPU ratio upper95<0.90 and P99 ratio upper95<=1.05; or
* tail benefit: P99 ratio upper95<0.90 and CPU ratio upper95<=1.05.
No whole-service CPU-saving claim if host active CPU rises significantly;
an inconclusive shared-host interval supports only a process-accounting claim.
Any positive claim states its exact operation/work/rate/core/network range.
No broad eBPF superiority or LLM claim follows.

If confirmed, develop only the supported CPU/small-graph-tail claim with these
limits. If no eligible confirmed advantage, close the research search and tidy
the OSS prototype, publish negative/crossover evidence and supported scope.
No endless new baseline/parameter expansion to rescue a negative result.

## Lifecycle and provenance

Finish and push the current frozen LLM comparison BEFORE this acquisition.
Use original Workspace/main/PVC and existing bounded client Job with exact
UIDs; preserve original session PIDs and unrelated tools/setup_env.sh.
No new service, scheduler, Workspace, permanent helper or runtime policy.
Record commands/source/environment/seeds/raw traces/errors and cleanup. Commit
and push each completed milestone. Keep historical negative evidence.

Pre-acquisition correction:confirmation seeds are420261017+selection_index*100+
pair. The earlier20262017base accidentally overlapped the first screening
seed under the fixed rate-dependent screening rule. No performance cell had
started when this was corrected; calibration/qualification are deterministic.
The forward correction restores the promised distinct confirmation seeds.

## Qualified acquisition dependencies before final screening

77980ae retains the invalid timer prefix and incomplete epoch-publication
prefix; timerfd plus atomic ready publication passes the original timing gate
on a fresh matched12000-request pair. This becomes the TCP before control,
not final screening. nodelay-plan.md/controls record graph caller's omitted
small-reply TCP policy. Listener TCP_NODELAY now matches the repaired LLM caller
on BOTH transports; compiled GPU dispatch is identical in all four libraries.
Kernel control improves22.006->2.566ms P99,130->0responses>10ms. Native control
is adverse2.864->10.955ms; one pair gives no statistical/native improvement
claim. All14ordinary numerical/lifecycle cases pass,including legacy graph
transport at repeat1. Adopt the consistent small-reply policy with that limit;
the final matrix,not this diagnostic,decides any transport benefit.

A one-second same-client core1 check verifies the requested service affinity
before broad acquisition; it is engineering qualification,not a paper result.
Final acquisition uses fresh screen_nodelay_* tags and graph_nodelay_build8
on both paths. No pre-repair cell is mixed into screening. All source,CPU/P99
criteria,selection rules,loads and confirmation seeds remain recorded.

Before final acquisition,the reusable bench/resource_observer.py retains the
same0.1s CPU/group/host/IRQ sampling and1s thread details,but queries GPU/NVML
only at the two window boundaries. Old diagnostic samples take~3.2ms median,
up to~8ms every100ms against~1ms requests; periodic GPU queries are unnecessary
for CPU/latency primaries and are moved out of the request window. This does
not establish a causal explanation for all observed outliers. Interval device
fields are unavailable,not zero/absence. Boundary GPU/clock snapshots and
unattributed resource limits remain. All final cells use the same source;
earlier diagnostic observer data are separate.
