# CPU-efficient native request control and measured TX task CPU

## Question and admission

There is no formal paper RQ or thesis contract. The retained user objective is
complete Linux TCP/HTTP + eBPF/shared queue -> resident real-model computation ->
asynchronous kernel TCP TX without a steady userspace request worker, with
improved throughput/latency, reused computation and honest matched evidence.

Specific question: does removing the native request/reply worker reduce the
measured executor-process plus TX-task CPU work relative to a native
CPU-efficient timed epoll control, and what client latency/throughput accompanies
that difference? This does not identify total service CPU: RX/softirq, BPF and
some TCP work remain outside those two counters.

Planned role: supporting component experiment. The strongest reject argument is
that an apparent CPU saving comes only from comparing a sleeping kernel worker
against an avoidably busy userspace worker. Finding0026 cannot answer this:
its native control busy-polls, process CPU omits kernel TX, and global CPU mixes
clients/unrelated work. Reanalysis cannot recover the omitted TX task counter or
the absent efficient user condition. Keep that closed, inconclusive matrix.

A positive worker-CPU result adds a bounded efficiency advantage; a contrary
result directs optimization toward kernel accept/drain/completion work. If the
timed user control lowers CPU at a latency cost, report that tradeoff instead
of a Pareto/equivalence claim. Crossing-zero intervals remain inconclusive.
These results bound mechanisms/workloads rather than refute the full user goal.

This is more useful now than another model-specific arithmetic campaign or
a new incompatible compute backend: the same upstream HF computation already
runs, and fair CPU orchestration is load-bearing to the user's CPU-path claim.
Physical-network/external-framework/text/batching work remains necessary for
the full goal, independently of this result.

## Conditions and reused assets

Reuse the native bench/resident_dispatch.py path and strict
tests/resident_qwen.py oracle. All three modes run the identical FP16 HF
forward/argmax graphs, eight private input/KV/output banks, the same resident
device dispatcher, default server TCP and common client TCP_NODELAY.

- resident: existing eBPF stream parser/verdict plus asynchronous kernel TX;
  TX still uses usleep_range(60,120), with no behavior tuning.
- user-network-wait: native epoll_pwait2 timeout {0,60000}; socket readiness
  can wake it earlier and GPU completion is checked after each wait.
  This is one CPU-efficient alternative, not a claim of optimal adaptive
  polling or identical effective wake intervals.
- user-network: existing busy epoll control, retained as a latency/CPU tradeoff
  control needed to evaluate the new wait mode on the same current host.

There is no external SOTA main baseline. These are same-compute component
controls. No Python token loop is imposed on either native control. NanoFlow's
async CPU orchestration motivates testing an efficient CPU alternative, but
this small timed epoll loop is not called a NanoFlow reproduction:
https://github.com/efeslab/Nanoflow.
Blink's same-engine orchestration comparison supplies the matched-compute
precedent: https://arxiv.org/html/2604.07609v1.
Native timed wait API: https://man7.org/linux/man-pages/man2/epoll_wait.2.html.

Model compute and sampling are unchanged. Build the wait library with
BF_USER_NETWORK_WAIT; the loader's entry-name list selects that library.
No new service, host package, Workspace, runtime sysctl, timer/helper process
or persistent service setting is required. The candidate is test-local.

## Workloads, correctness and metrics

Models: HuggingFaceTB/SmolLM2-135M and Qwen/Qwen2.5-0.5B-Instruct.
Per model: output lengths1/64 x closed-loop clients1/8, five paired process
blocks, 64 measured requests/cell, four real prompt cases; eight warmups/process.
Native rotate/reverse three-mode order and rotate matrix order are declared
before collection. Totals:120 cells,7680 exact measured requests,249600 measured
tokens and30 normal executors. No sample exclusion or selectively retried pair.

Before preflight, strict regressions for both models with kernel and wait
executors must preserve independent eager-HF token agreement, all prompt
edges, concurrency, mixed lengths, pipelining/partial requests/rejections,
half-close, reclamation and helper-thread SIGTERM cleanup. Existing busy
control has no arithmetic/protocol change except a startup mode receipt;
preflight and current matched collection verify its engagement.
GPU dispatcher SASS must agree across busy/wait/kernel libraries.

Primary: paired control-minus-resident executor-process+TX-task CPU seconds
per measured request, gen64/clients8, separately for each model and user
control. POSIX clock_getcpuclockid/clock_gettime_ns reads all executor threads;
the module read-only tx_cpu_ns attribute calls exported task_cputime_adjusted
under a mutex with an explicit retained task reference through shutdown.
Native before/after values, monotonic read brackets and individual component
deltas are retained. No writable CPU-accounting setting or new page ABI.
Kernel RX/softirq/BPF/TCP outside TX, clients and GPU execution are excluded.
The sum must never be presented as total service/host CPU or instructions/token.
Legacy /proc/PID/stat and global CPU remain descriptive context.

Secondary standard client metrics: TTFT, TPOT, completion and output tokens/s.
TTFT/TPOT follow https://docs.vllm.ai/en/latest/api/vllm/benchmarks/serve/.
Report gen1/client1 TTFT and gen64/client8 TPS with the primary CPU estimates,
without arbitrary latency thresholds, equivalence tests or posthoc CPU/latency
scores. Preserve raw per-request arrivals, exact tokens and GPU observations.
Five-pair nominal two-sided t95(df4) intervals; no family-wide significance.
One-second idle observations retain the same high-resolution counters.

POSIX CPU clock API reference:
https://man7.org/linux/man-pages/man3/clock_getcpuclockid.3.html.
CPU readings bracket the request window, with sequential counter reads; record
these brackets and do not claim nanosecond window alignment.

## Execution and completion

Original yunwei356/bpfusion-dev Workspace, /workspaces/repository, main.
Preserve unrelated tools/setup_env.sh and original shared SGLang service.
Record host boot, original service PID/residency, memory and current fault
journal before/after and cell GPU observations. Pairing does not prove freedom
from shared-host interference. Keep any unequal event exposure explicit.

Build:
```bash
make qwen-graph qwen-graph-user-network qwen-graph-user-network-wait
make -C module KDIR=/usr/src/linux-headers-7.3.0-070300rc3-generic CC=gcc-15
```

Qualification (each checkpoint, both executors):
```bash
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 tests/resident_qwen.py --gen 64 --prefill-edges --executor ./build/qwen_graph --model MODEL
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 tests/resident_qwen.py --gen 64 --prefill-edges --executor ./build/qwen_graph_user_network_wait --model MODEL
```

Real preflight (both checkpoint names in place of MODEL; fresh MODEL_TAG paths):
```bash
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --preflight --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --user-network-wait-executor ./build/qwen_graph_user_network_wait --model MODEL --output bench/results/timed_network_MODEL_TAG_preflight_20261011.jsonl
```

After qualification/preflight, commit/push source and reviewed plan; freeze that
revision before full collection:
```bash
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --user-network-wait-executor ./build/qwen_graph_user_network_wait --model HuggingFaceTB/SmolLM2-135M --output bench/results/timed_network_smol_20261011.jsonl
HF_HOME=/workspaces/.cache/huggingface /usr/bin/python3 bench/resident_dispatch.py --gen 64 --resident-executor ./build/qwen_graph --user-network-executor ./build/qwen_graph_user_network --user-network-wait-executor ./build/qwen_graph_user_network_wait --model Qwen/Qwen2.5-0.5B-Instruct --output bench/results/timed_network_qwen_20261011.jsonl
```

Native raw logs, command/exit receipts, exact source revision and native analysis
are authoritative. Complete all120 cells/7680 exact requests/249600 tokens/
30 normal exits, launch1/graph_error0/eight banks and normal queue/counters.
Independent result review reconstructs raw CPU deltas, timings, sample coverage,
paired estimates, comparison engagement, event exposure and cleanup.
No restart on an observation timeout; inspect the same actual live handle.

Publish results in the existing findings sequence and docs/evaluation.md with
the question, scope, plan/reviews/raw evidence, uncertainty and next decision.
Keep failures and negative outcomes. Bootstrap/regressions/preflight/accounting
availability have dependency value only. The full goal remains active.


## Observed environment deviation before full collection

Read-only observation at10:40UTC identifies the previously shared SGLang
process as absent. Its separate GPU-SMT candidate Job terminates at10:34:41UTC
with ENOSPC in result logging; BPFusion did not stop/restart it or mutate its
PVC. All measured preflight cells and the planned full collection occur
after this event. Current before/after boot, residency, storage and fault
receipts replace assumptions of unchanged SGLang residency. Do not compare
old shared-SGLang performance directly or claim induced isolation.
The question, compute, oracle, matrix, metrics and native commands are unchanged.
Record further events and unequal exposure; do not exclude inconvenient samples.

A fresh pre-full observation at10:51:29UTC finds a new SGLang scheduler,
PID4026103 with18398MiB GPU residency; the original PID2762187 remains absent.
The owning session may have resumed independently; cause/lifecycle is not
established here. Full collection therefore starts with this observed shared
GPU condition, whereas preflight followed the earlier disappearance. Keep
per-cell and after-run observations; do not claim a permanently absent
co-tenant or compare preflight timings against full collection as matched.
