# Socket readiness before kernel accept and receive

## Question and current status

Does the eBPF/kernel path use less bounded worker CPU than an efficient
native userspace control after avoiding unnecessary accept/recv attempts,
with identical upstream model computation? What client latency/throughput
accompanies it?

[Reviewed plan](../../bench/results/readiness_network_plan_20261011.md) and
[fresh plan review](../../bench/results/readiness_network_plan_review_20261011.md)
admit a supporting component comparison,not an external SOTA claim.
Finding0027's valid negative result remains unchanged and closed.

The candidate module builds; both affected-kernel strict runs and all six
three-mode preflight executors pass. Full comparison and independent result
review remain pending; no performance gain has been established.

## Mechanism and evidence

The [dependency perf diagnostic](0027-timed-network-control.md#follow-up-cpu-localization-dependency-evidence)
localizes accept/recv paths in a real Qwen eight-client strict stage.
It does not reproduce the primary performance window or predict an improvement.

The module now calls the existing TCP socket poll callback before accepting
or draining. Listener EPOLLIN reflects the accept queue; receive checks include
data,EOF,shutdown and error readiness. TCP's sockmap callback includes ingress
messages,so ordinary skb-queue emptiness is not used.

The complete behavior diff is8 inserted/1 removed lines,one include and two
guards. Readiness never frees queue state or socket ownership.
Existing accept/recv,error handling,peer_pending,partial TX,final GPU release,
FIFO reclamation and60-120us sweep remain. Arrival after a false readiness
snapshot can wait until the next sweep; the comparison must retain any latency
cost. Model math,precision,KV/GPU graphs,batching,page ABI and CPU counters
are unchanged.

[Build log](../../bench/results/readiness_network_build_20261011.stdout.txt)
records the owning Kbuild command and exit0. Existing compiler/pahole mismatch
warnings and unavailable-vmlinux BTF skip are context,not correctness failures.
No new runtime flag,helper,service,permission or device setting is added.

## Strict qualification

[Canonical qualification stdout](../../bench/results/readiness_network_qualification_20261011.stdout.txt)
records two exit0 commands,SmolLM2-135M and Qwen2.5-0.5B,each with gen64 and
prefill edges. Together670 valid requests,40864 exact eager-HF greedy tokens,
518 rejected requests. Each passes5000 empty connections,eight-client
concurrency,256 rejection/valid cycles,mixed lengths,ring wrap,pipelined
HTTP/half-close,invalid IDs,helper SIGTERM and cleanup. Each executor has
one host launch,20432 model-graph steps,zeroerrors,eightbanks,maxactive8.
After-ready tracing confirms no steady userspace accept/receive/send worker.

The native userspace source is unchanged; reuse its strict qualification from
finding0027. Current three-mode preflight and full collection still check its
engagement and exact outputs. These strict checks are dependency evidence,
not performance results.

## Real preflight and source freeze

[Native preflight stdout](../../bench/results/readiness_network_preflight_20261011.stdout.txt),
[Smol raw](../../bench/results/readiness_network_smol_preflight_20261011.jsonl),
[Qwen raw](../../bench/results/readiness_network_qwen_preflight_20261011.jsonl) and
[native analysis](../../bench/results/readiness_network_preflight_analysis_20261011.stdout.txt)
retain six normal executors and24 exact measured one-token replies.
Eight warmup requests/executor are separate. All six report one host launch,
264 model-graph steps,zeroerrors and eight banks. Both analyses exit0;
all12 idle/cell raw CPU component deltas and sequential read brackets reconstruct.
The module is absent for both userspace controls. Own processes,module and
pins are absent after normal completion.

The kernel preflight unloads each report2000 bytes,12 completions,zero
abandoned/retries and two accepted/closed sockets. Strict runs each report
593 completed/one abandoned,matching the intentionally disconnected binary
rejection case; all5058 accepted sockets close normally. Do not treat that
strict-case counter as a failed performance request.

Qualification/preflight run the reviewed module candidate atop d16fac01;
their metadata names that base revision. No model/dispatcher/benchmark/oracle
source changes occur. Candidate source and reviewed plan are committed before
full collection,whose raw metadata records its frozen revision.

A fresh22:28UTC host observation finds the same boot/GPU UUID and no GPU
compute processes. Host memory use differs from the22:11 receipt. Retained
journal reads through qualification/preflight show normal module lifecycles
and no matching OOM/Xid/Oops/BUG/CallTrace/I/O/EXT4 fault lines.
An idle endpoint observation does not establish continuous isolation,
equal host load or a causal old/new comparison.

## Planned comparison and boundaries

Use unchanged bench/resident_dispatch.py with kernel,busy native epoll,
and timed native epoll_pwait2 controls. Models SmolLM2-135M/Qwen2.5-0.5B,
gen1/64,clients1/8,five native rotating paired blocks,64 requests/cell.
Totals120 cells,7680 exact measured requests,249600 tokens,30 normal executors.

Primary efficient-control-minus-kernel executor-process + TX-task CPU
us/request at gen64/client8,separate per model; report nominal five-pair t95.
Standard gen1/client1 TTFT and gen64/client8 throughput accompany it.
Exclude RX/softirq/BPF/networking charged outside TX,client/GPU CPU from this
bounded measure. Neither total service CPU nor a historical before/after
causal effect is identified.

Current [environment receipts](../../bench/results/readiness_network_environment_20261011.txt)
retain actual observations. An idle GPU observation does not prove continuous
isolation. Record co-tenant changes/unknowns and all failures/negative outcomes;
never remove inconvenient pairs.

Strict/preflight/correctness/accounting availability have dependency value only.
Publish full measurements and a fresh result review before judging the
hypothesis. Physical-NIC,strong official serving,total attributed CPU,full text
and online batching remain open under the unchanged full research goal.
