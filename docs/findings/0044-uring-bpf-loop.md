# Sleepable eBPF io_uring coordination

This optional transport keeps the reused model computation and GPU-owned
TCP submission/completion handling, while replacing SQPOLL with an upstream
sleepable io_uring BPF loop. Userspace initializes the ring and enters the
kernel loop once during steady serving. The candidate does not use bfusion_tx.
The existing module remains the default; broader kernel support and any
CPU, latency or throughput benefit remain unestablished.

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
affected retry. Performance collection and fresh result review remain pending.
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
