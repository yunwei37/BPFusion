# Sleepable eBPF io_uring coordination

This optional transport keeps the reused model computation and GPU-owned
TCP submission/completion handling, while replacing SQPOLL with an upstream
sleepable io_uring BPF loop. Userspace initializes the ring and enters the
kernel loop once during steady serving. The candidate does not use bfusion_tx.
The completed comparison reduces known-worker CPU against SQPOLL,without
a reliable latency gain over efficient native TCP; Qwen long-output throughput
is lower than native and Smol throughput is inconclusive. The existing module
remains the default; broader kernel/model support and general serving
superiority remain unestablished.

## Implementation and dependencies

The GPU remains the sole steady SQ producer and CQ consumer. A separate
32-byte control prefix in the existing mapped report region supplies ring
offsets and shutdown state; the request page ABI is unchanged. The sleepable
struct_ops program submits published SQEs through bpf_io_uring_submit_sqes
and asks the kernel to wait for the next CQ position. A standard multishot
io_uring timeout nominally fires every60000ns, matching the existing native
timed-epoll value. This is periodic completion polling, not GPU interrupt
notification or proof of that actual wake spacing.

The ring uses SINGLE_ISSUER and DEFER_TASKRUN, rather than SQPOLL. On signal
or the existing service deadline, the creator returns from the kernel loop,
stops model execution, then reenters to drain network cancellation and close.
Explicit TIMEOUT_REMOVE retires the multishot timer. Its MORE CQEs do not
decrement pending operations; only the terminal CQE does. SQ and CQ are
separately empty at shutdown, since multishot produces more CQEs than SQEs.

The tested host is Linux7.3.0-070300rc3-generic/RTX5090. This requires the
running kernel's io_uring BPF struct_ops/kfuncs, BTF and current UAPI headers,
plus libbpf with struct_ops initial-value support. The experiment uses
upstream libbpf1.6.3 under its temporary runtime for every condition; system
libbpf1.3 is preserved. This is not a claim that every new Linux release
supports this interface or that the kernel module can be removed on older
hosts. See upstream [BPF operations](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c),
[kernel loop](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c),
[timeout ownership](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/timeout.c)
and [libbpf initial values](https://github.com/libbpf/libbpf/blob/v1.6.3/src/libbpf.c).

## Current evidence and planned comparison

The [plan](../../bench/results/uring_bpf_loop_20261014/plan.md) and
[fresh plan review](../../bench/results/uring_bpf_loop_20261014/plan-review.md)
admit one supporting intervention after finding0043 identified high measured
stock worker CPU with no reliable throughput gain. Efficient native TCP is
the main alternative; current incremental SQPOLL is a component control.
DEFER_TASKRUN, timer, task-work execution and loop coordination change
together, so any result cannot isolate eBPF, a syscall or polling as its
exclusive cause.

The [qualification history](../../bench/results/uring_bpf_loop_20261014/qualification.md)
retains two failed preflights: missing struct_ops shadow data under old
libbpf, and an uncanceled timer after all40 replies succeeded. Third and final
preflight passes all3 paths/12 cells,120 requests/3144 checked tokens including
24 excluded warmups, with analysis0 and normal shutdown. All12 vLLM protocol
executors then pass7464 requests/266688 valid tokens,3108 expected rejects
and60000 empty connections. Traced checks replay actual upstream batch/KV
history; ordinary checks retain the fixed complete-output-set scope. All
network traces engage intended mechanisms; compiled model dispatcher SASS
is byte-identical between loop and stock. Prior0043 analyses replay unchanged.

Initial HF qualification fails before requests because its launcher-name
mapping selects the default library. The owned executor exits normally on
SIGTERM; add the omitted launcher name and rerun the unchanged HF workload.
Both corrected HF workloads pass32 requests/652 independently checked
complete/prefix tokens per model,13 closed connections and3 expected aborts.
Actual traces show one steady loop entry with no userspace socket calls,then
one cleanup entry after SIGTERM. Full planned qualification is complete.
The failed original wrapper record remains archived alongside the successful
affected retry. Performance collection and fresh result review are complete below; final restoration is recorded below.
These checks are dependency evidence, not a performance result.

The admitted ordinary comparison is two models, all six permutations of
loop/native/stock,gen1/64 at one/eight clients and64 measured requests/cell.
Three predeclared primary effects per model are native-minus-loop gen1/c1
TTFT,loop-minus-native gen64/c8 throughput and stock-minus-loop gen64/c8
known-worker CPU per request. Report all six nominal paired t95 intervals
separately. Process CPU includes all process threads, but excludes Linux
network work elsewhere, clients and energy. Fixed pre-observation complete
output sets remain weaker than replay of current unobserved ordinary batch
history. No official-vLLM-server or arbitrary-model claim follows.

With qualified current headers, libbpf runtime and pinned vLLM environment:

    make vllm-graph-uring-loop vllm-graph-uring vllm-graph-user-network-wait VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --loop-comparison --correctness --model MODEL --output RAW
    ENV/bin/python bench/vllm_serving.py --loop-comparison --untraced --reference-path FROZEN --model MODEL --output RAW
    python3 bench/vllm_serving_analysis.py RAW

The shared HF graph transport builds with make qwen-graph-uring-loop.
Exact dependency and runtime bindings are in the linked experiment archive.

## Completed ordinary comparison

Frozen main ddc444c393a38be2ffbabf372d22e139e4aa4bc3 completes the full matrix
on2026-10-14:36 executors/144 cells,9216 measured requests/299520 measured
output tokens and288 excluded checked warmups. Each model completes all six
transport permutations,18 normal executors and72 cells. Both source-native
analyses pass. There are no failed,excluded,replaced or retried timing cells.
Every complete reply matches the unchanged pre-observation output set; this
does not replay the unobserved current ordinary batch/KV history or establish
task quality.

| Model | Loop / native / SQPOLL gen1,c1 TTFT ms | Loop / native / SQPOLL gen64,c8 tokens/s |
|---|---|---|
| Qwen2.5-0.5B | 1.378481 / 1.368795 / 1.337637 | 4605.364822 / 4681.213707 / 4536.448200 |
| SmolLM2-135M | 1.104221 / 1.136882 / 1.111258 | 5471.373930 / 5450.017739 / 5348.630357 |

All six predeclared primary effects favor loop when positive. CPU is converted
from seconds/request to milliseconds/request; intervals are nominal paired
t95,df5 over the six process blocks.

| Model | Primary effect | Mean | Nominal paired t95 |
|---|---|---:|---|
| Qwen | native-minus-loop TTFT1,c1 ms | -0.009686 | [-0.071448,0.052076] |
| Smol | native-minus-loop TTFT1,c1 ms | +0.032660 | [-0.042745,0.108066] |
| Qwen | loop-minus-native TPS64,c8 | -75.848884 | [-119.599452,-32.098316] |
| Smol | loop-minus-native TPS64,c8 | +21.356192 | [-108.669300,151.381683] |
| Qwen | SQPOLL-minus-loop CPU64,c8 ms/request | +13.649411 | [13.218863,14.079960] |
| Smol | SQPOLL-minus-loop CPU64,c8 ms/request | +11.580469 | [11.071859,12.089079] |

The intended reduction in known-worker CPU against SQPOLL is supported for both
models. Neither native latency contrast establishes a reliable improvement.
Qwen long-output throughput loses to native by75.85tokens/s,about1.62% of the
native mean; every paired Qwen throughput difference is negative. Smol
throughput is inconclusive. Crossing-zero intervals do not establish
equivalence, and the CPU result cannot be counted as a latency or throughput
win. Retain all blocks,including the larger positive Smol throughput estimates
in blocks2/3; no unverified cause or exclusion is assigned.

| Model | Loop CPU ms/request | SQPOLL CPU ms/request | Native CPU ms/request |
|---|---:|---:|---:|
| Qwen | 0.572526 | 14.221937 | 0.491585 |
| Smol | 0.482410 | 12.062879 | 0.426647 |

The loop mean is about96% below SQPOLL in this gen64/c8 comparison.
Native known-worker CPU remains lower than loop for both checkpoints,including
the nominal secondary paired contrasts. The all-thread process clock counts
the creator's kernel loop and actual SQPOLL once; RX/softirq/BPF/TCP elsewhere,
clients and energy remain excluded. These are not total service CPU or
exclusive timer/polling/BPF cost estimates. Changed timer/task-work/dispatch
coordination and ordinary arrival/batching histories prevent a sole-cause
explanation of the Qwen throughput loss.

[Qwen raw](../../bench/results/uring_bpf_loop_20261014/qwen_performance.jsonl),
[Qwen reconstruction](../../bench/results/uring_bpf_loop_20261014/qwen_performance_analysis.stdout),
[Smol raw](../../bench/results/uring_bpf_loop_20261014/smol_performance.jsonl) and
[Smol reconstruction](../../bench/results/uring_bpf_loop_20261014/smol_performance_analysis.stdout)
retain all outputs,arrivals,clocks,worker identities,commands and counters.
The selected timing-window
[kernel journal receipt](../../bench/results/uring_bpf_loop_20261014/performance_kernel_journal.json)
returns exit0 with '-- No entries --'; it is not proof of continuous isolation
or absence of unlogged faults/interference. The separately observed
[performance endpoint](../../bench/results/uring_bpf_loop_20261014/performance_end.json)
finds the original boot/base and no own module,pins or GPU application.
Owned temporary runtime/build outputs are removed after result review,as
recorded in the final restoration below.

This complete intervention demonstrates a lower-cost stock coordination
alternative within the qualified workload,without a reliable delivery
advantage over efficient native TCP. It is supporting mechanism/workload
evidence,not external SOTA,arbitrary-model support or an eBPF-only cause.
Keep the module default and the loop optional; do not repeat unchanged timing
or start model-specific arithmetic tuning. The [fresh independent result review](../../bench/results/uring_bpf_loop_20261014/result-review.md)
admits valid/complete supporting evidence and reconstructs all six primary
intervals directly from raw data. Both performance and all four strict
analyses replay byte-identically. Secondary native comparisons also favor
native for both models' gen64/c1 throughput and gen1/c8 TTFT/throughput;
retain these negative effects rather than describing delivery as uniformly
unchanged. No new physical-network,task-quality or broad-backend result
follows. [Final restoration](../../bench/results/uring_bpf_loop_20261014/final_restoration.json)
removes the owned temporary runtime and31 named build entries after review.
Launcher links are unlinked without deleting their source targets. Original
boot/base,Coder processes,model/global caches,default HF library and unrelated
tools/setup_env.sh are retained; no own process,module,pins or GPU application
remains. This separately observed endpoint is not continuous isolation.
Close this completed comparison with its supported scoped CPU benefit and
mixed native delivery results. Optimized cross-node deployment and broader
backend/service acceptance remain under the full retained project goal.
