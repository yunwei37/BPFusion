# Native timed network control and TX task CPU

## Question and scope

Does removing a native TCP request/reply worker reduce CPU charged to the
executor process plus kernel TX task against a CPU-efficient timed epoll
worker, and what client latency/throughput accompanies that difference?

This supporting component comparison retains identical FP16 HF computation,
eight graph/KV banks and resident GPU dispatch. The three conditions are
eBPF/kernel TCP, native busy epoll and native epoll_pwait2 with a60us timeout.
Socket readiness can wake the latter earlier; its effective wait is not
equivalent to kernel usleep_range(60,120), nor claimed optimal.

[Plan](../../bench/results/timed_network_plan_20261011.md) and
[fresh plan review](../../bench/results/timed_network_plan_review_20261011.md)
precede execution. There is no formal paper RQ or external SOTA baseline.
The new condition and TX accounting are absent from finding0026; old raw
outputs cannot recover them.

Run status: strict qualification and real preflight complete; full comparison
pending. No performance hypothesis is answered by those dependencies.

## Implementation and qualification

Build the new optional control with:
```bash
make qwen-graph qwen-graph-user-network qwen-graph-user-network-wait
make -C module KDIR=/usr/src/linux-headers-7.3.0-070300rc3-generic CC=gcc-15
```

Only the wait library enables BF_USER_NETWORK_WAIT. Existing model math,
GPU dispatcher, parser, partial sends, ordering, rejection and recycling
remain identical. All three dispatcher SASS instruction arrays contain
768 rows and compare equal. Python source compilation and native/module
builds pass. Kernel gcc/pahole version warnings and missing-vmlinux BTF skip
are recorded as build context, not correctness evidence.

The new read-only /sys/module/bfusion_tx/parameters/tx_cpu_ns calls
task_cputime_adjusted for the TX task. An explicit task reference and mutex
preserve getter/shutdown lifetime. The benchmark uses POSIX process CPU
clocks for all executor threads and retains before/after values plus monotonic
read brackets. The sum excludes RX/softirq/BPF and TCP work outside the TX
context, client CPU and GPU computation. It is not total service CPU.

[Strict regression stdout](../../bench/results/timed_network_qualification_20261011.stdout.txt)
records four exit0 commands: SmolLM2-135M and Qwen2.5-0.5B, each under kernel
and wait executors. Totals:1340 valid requests,81728 exact greedy tokens and
1036 rejections. Each condition preserves the unchanged eager-HF oracle,
prompt edges, eight concurrent clients, repeated wrap/reuse, mixed lengths,
HTTP pipelining/half-close, invalid-token recovery, one resident launch,
zero graph errors and cleanup. Tracing distinguishes no steady userspace
network worker in the kernel mode from native userspace network operations
in the controls. These are correctness/lifecycle qualifications, not latency
or throughput conclusions.

[Preflight stdout](../../bench/results/timed_network_preflight_20261011.stdout.txt),
[Smol raw](../../bench/results/timed_network_smol_preflight_20261011.jsonl) and
[Qwen raw](../../bench/results/timed_network_qwen_preflight_20261011.jsonl)
retain six normal executors and24 exact measured one-token replies, with
eight warmup requests/executor separate. Each process reports launch1,
264 model-graph steps, graph_error0 and eight banks. Both native wait markers
engage; kernel TX accounting grows and raw CPU component deltas reconstruct.
Native analysis exits0 for both files. Do not interpret these single-block
four-request cells as performance results.

Qualification/preflight ran on the six reviewed source changes atop bb059df;
a7d097e only added the backend source audit, during preflight. Source will
be committed before full collection; its metadata records the frozen revision.

## Environment boundary

[Read-only environment receipt](../../bench/results/timed_network_environment_20261011.txt)
records the unchanged host boot and an external co-tenant transition.
SGLang PID2762187/18368MiB exists at10:27:34UTC. The separate
gpu-smt-candidate-5090-20261007 Job terminates at10:34:41UTC with exit1;
its log reports ENOSPC while appending generation-events.jsonl, after157/186
tasks. Subsequent host reads find no SGLang process. BPFusion's own32GiB
Longhorn volume has16GiB available; host overlay has346GiB available.
These reads do not identify the cause of the other project's storage growth.

BPFusion did not stop/restart that Job/SGLang or change its PVC/lifecycle.
The event occurs during strict qualification, before all preflight measured
cells and full collection. Old shared-SGLang performance results are not a
matched comparison for this host condition. No induced isolation or
constant co-tenant/activity claim is made; full-run event exposure must be
reported from current observations.

## Full comparison and pending interpretation

Run the two full commands in the plan. Required coverage is120 cells,
7680 exact measured requests,249600 measured tokens and30 normal executors.
Primary paired CPU microseconds/request use gen64/clients8 for each model and
each control. TTFT gen1/client1 and TPS gen64/client8 accompany these estimates.
Raw request timings, tokens, CPU components, idle windows and GPU observations
remain authoritative. Five-pair nominal t95(df4) intervals are descriptive;
there is no family-wide significance or equivalence claim.

Independent result review and full measurements remain pending. Positive,
negative, tradeoff and inconclusive outcomes will be retained in this finding
and docs/evaluation.md. Text processing, continuous batching, physical-NIC
evaluation and strong external serving comparisons remain open under the
full user objective.
