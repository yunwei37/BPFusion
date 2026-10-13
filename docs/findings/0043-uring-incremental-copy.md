# Incremental stock TCP output copying

The optional GPU-owned stock transport skips output tokens whose bytes have
already been sent. The next SEND still begins at the actual completed byte
offset; a partly sent token is recopied in full so its unsent suffix stays
correct. Header creation, SEND size/flags, queue reclamation, FIFO final
submission and model arithmetic remain unchanged. The module remains the
default transport. Performance benefit is not yet established.

The separate make target vllm-graph-uring-full-copy builds the matched former
copy loop, using the same repaired source with BF_IO_FULL_COPY. This is a copy ablation,
not the unmodified implementation from finding0042. The existing serving
driver's --copy-comparison selects candidate, full-copy ablation and efficient
native TCP, gen64/c8,256 requests/cell and all six transport order permutations.
The analyzer reports candidate/native and candidate/full-copy paired effects;
this does not compare against an official vLLM server or isolate hardware
bandwidth as the sole cause.

## Evidence and current boundary

[Plan](../../bench/results/uring_incremental_copy_20261013/plan.md) and
[fresh plan review with follow-up](../../bench/results/uring_incremental_copy_20261013/plan-review.md)
admit one supporting copy intervention. Reused independent complete references
are frozen before any new output. Traced checks independently replay upstream
batch/KV history; ordinary checks use the narrower fixed whole-sequence set.

[Qualification history](../../bench/results/uring_incremental_copy_20261013/qualification.md)
retains an initial Smol full-copy strict half-close EOF failure. Subsequent GPU
and kernel diagnostics did not reproduce it, and temporary instrumentation was
removed. An unchanged-production stress workload subsequently passes both
stock paths:1000 requests/46416 independently replayed tokens per condition,
including64 consecutive six-request half-close pipelines. These passes do not
establish the cause or repair of the initial failure. General reliability and
the full retained project goal remain unproven.

A separate HF idle reproduction captured receive CQ sequence2/res=-11
(EAGAIN), equal under ordinary and system GPU loads, followed by premature
connection closure. The old code treated every negative RECV as peer death.
The common header now rearms EAGAIN/EINTR while retaining real EOF and fatal
errors. This source repair is identical in both stock conditions. It explains
the captured failure, not retrospectively the initial six-request pipeline.

After the EAGAIN repair, the three-path preflight, all twelve traced/ordinary
strict executors (7464 requests/266688 valid tokens) and both original HF
lifecycle workloads pass. The ordinary candidate/full-copy compiled model
dispatcher SASS is byte-identical. A subsequent eight-cycle idle regression
nevertheless exposes another receive stall, so these passes do not establish
general reliability. No complete timing matrix or performance conclusion exists.
Any later completed comparison must retain the initial failure and limit its
conclusion to successfully completed ordinary gen64/c8 workloads; a delivery
failure in timing cannot become a candidate win or be silently replaced.

## Idle receive diagnosis

The archived [idle regression](../../bench/results/uring_incremental_copy_20261013/hf_idle_repaired/)
fails on Qwen after the EAGAIN repair. Read-only
[ring/page/TCP observations](../../bench/results/uring_incremental_copy_20261013/hf_idle_tcp/)
show an outstanding receive, empty submission/completion queues, no admission
of the stalled request and no occupied GPU slot. A temporary IOSQE_ASYNC
receive attempt also fails and is removed; it is not a repair.

The [kernel psock snapshot](../../bench/results/uring_incremental_copy_20261013/hf_psock_diagnostic/)
captures the TCP consumed cursor 75 bytes ahead of the psock parser cursor,
one raw receive skb, zero ingress bytes, active parser/verdict programs and
an unpaused parser. This supports a TCP/psock receive-accounting interaction,
but does not establish its complete cause. The diagnostic only reads kernel
state; it changes neither the host kernel nor model computation.

A temporary [same-socket ingress redirect candidate](../../bench/results/uring_incremental_copy_20261013/fusion_self_redirect.bpf.c)
uses the existing sockhash flow key after publication instead of plain SK_PASS.
Both models pass the [eight-cycle idle and protocol workload](../../bench/results/uring_incremental_copy_20261013/hf_self_redirect/):
32 requests and 652 independently checked complete/prefix tokens per model,
13 accepted/closed connections, three expected aborts, zero pending/error/drop
and balanced SQ/CQ counters. All twelve traced/ordinary vLLM protocol executors then pass (7464 requests/
266688 valid tokens), and the temporary wrapper successfully restores the
original object. The same redirect is now in the production BPF source;
both default module compatibility workloads and the final copy preflight pass.
The four module/native strict executors add 2488 requests/88896 valid tokens.
The final three-path preflight checks 24 measured gen64 requests/1536 tokens
plus 24 excluded gen1 warmups. The source is ready to freeze before full timing.
These are dependency checks, not copy-performance results.

The relevant upstream receive-accounting implementation is
[Linux tcp_bpf.c](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_bpf.c)
and [skmsg.c](https://github.com/torvalds/linux/blob/v7.3-rc3/net/core/skmsg.c).
No GPU publication, SQPOLL wakeup or host-kernel fix is claimed from these observations.

From the original repository and qualified pinned runtime, build with:

    make vllm-graph-uring vllm-graph-uring-full-copy vllm-graph-user-network-wait VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --copy-comparison --correctness --model MODEL --output RAW
    ENV/bin/python bench/vllm_serving.py --copy-comparison --untraced --reference-path FROZEN --model MODEL --output RAW
    python3 bench/vllm_serving_analysis.py RAW

Literal model/runtime/output bindings and source-native diagnosis commands are
retained in the linked experiment archive. Partial-SEND correctness is a
source byte-offset argument; the stress does not establish observed short CQ
returns inside a token. No eBPF-only, total CPU,energy,SOTA or arbitrary-model
performance claim follows.
