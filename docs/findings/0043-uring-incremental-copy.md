# Incremental stock TCP output copying

The optional GPU-owned stock transport skips output tokens whose bytes have
already been sent. The next SEND still begins at the actual completed byte
offset; a partly sent token is recopied in full so its unsent suffix stays
correct. Header creation, SEND size/flags, queue reclamation, FIFO final
submission and model arithmetic remain unchanged. The module remains the
default transport. The completed comparison establishes no reliable performance benefit.

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
general reliability. At that stage no timing had started; the completed ordinary comparison is reported below.
The completed comparison retains the initial failure and limits its conclusion
to ordinary gen64/c8 workloads. No delivery failure occurs in timing; a failed
control would not count as a candidate win or be silently replaced.

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
plus 24 excluded gen1 warmups. This qualified source was then frozen for the completed ordinary comparison below.
These are dependency checks, not copy-performance results.

The relevant upstream receive-accounting implementation is
[Linux tcp_bpf.c](https://github.com/torvalds/linux/blob/v7.3-rc3/net/ipv4/tcp_bpf.c)
and [skmsg.c](https://github.com/torvalds/linux/blob/v7.3-rc3/net/core/skmsg.c).
No GPU publication, SQPOLL wakeup or host-kernel fix is claimed from these observations.

## Completed ordinary comparison

Frozen main 0330145710dc66de66dbb0864f4133ee345b86d8 completes the entire
planned comparison on 2026-10-13:36 executors/36 cells,9216 measured gen64
requests/589824 measured output tokens, plus288 checked gen1 warmups excluded
from timing. Both models complete all six permutations and18 executors, with
exit/analysis0 and no failed, excluded, replaced or retried timing cells.
All actual outputs match the unchanged pre-observation whole-sequence sets.
This is finite-set fidelity, not replay of the unobserved current ordinary
batch/KV history or a task-quality evaluation.

| Model | Incremental stock TPS | Full-copy ablation TPS | Efficient native TPS |
|---|---:|---:|---:|
| Qwen2.5-0.5B | 4534.005144 | 4489.431207 | 4507.866830 |
| SmolLM2-135M | 5221.026420 | 5273.257856 | 5116.563478 |

| Model | Candidate-minus-control TPS | Mean | Nominal paired t95,df5 |
|---|---|---:|---|
| Qwen | full copy | +44.573938 | [-28.962858,118.110733] |
| Qwen | native | +26.138314 | [-46.980792,99.257420] |
| Smol | full copy | -52.231436 | [-185.829930,81.367058] |
| Smol | native | +104.462942 | [-198.996499,407.922382] |

All four predeclared primary intervals include zero:neither a reliable copy
benefit nor an advantage over native is established. This is not equivalence
or a familywide superiority result. Retain every block, including Qwen full
copy pair0 and Smol incremental pair1; no unverified cause or exclusion is
assigned to their larger differences. Different arrival/batching histories
remain possible despite unchanged model arithmetic and dispatcher SASS.

| Model | Incremental / full-copy / native CPU ms/request | Incremental / native TTFT ms |
|---|---|---|
| Qwen | 14.224701 / 14.372412 / 0.536699 | 2.075738 / 2.159118 |
| Smol | 12.367607 / 12.232235 / 0.412901 | 1.686342 / 1.782708 |

These TTFT values are secondary gen64/c8 measurements, not the older
gen1/c1 or cross-node conditions. Known-worker CPU is the all-thread process
clock during the cell bracket; observed SQPOLL belongs to that thread group
and is counted once. Incremental stock uses about27/30 times the respective
native means and about one CPU-second per second. RX/softirq/BPF/TCP elsewhere,
clients and energy are excluded; this is not total service CPU or exclusive
per-thread attribution. The nominal CPU differences favor native for both
models. Copy/full-copy CPU differences remain inconclusive.

[Qwen raw](../../bench/results/uring_incremental_copy_20261013/qwen_performance.jsonl),
[Qwen reconstruction](../../bench/results/uring_incremental_copy_20261013/qwen_performance_analysis.stdout),
[Smol raw](../../bench/results/uring_incremental_copy_20261013/smol_performance.jsonl)
and [Smol reconstruction](../../bench/results/uring_incremental_copy_20261013/smol_performance_analysis.stdout)
retain arrivals, complete outputs, counters, clocks, tasks, exact commands
and all six paired effects. The [fresh result review](../../bench/results/uring_incremental_copy_20261013/result-review.md)
independently audits completion, arithmetic, fidelity, repair fairness and
qualification. This is a supporting local mechanism boundary, not an official
vLLM server comparison, arbitrary-model result or eBPF-only speedup.

The actual timing-window [kernel receipt](../../bench/results/uring_incremental_copy_20261013/performance_kernel_journal.json)
reads1354 lines with no listed fault-pattern matches. The separately dated
[late closure endpoint](../../bench/results/uring_incremental_copy_20261013/late_closure_endpoint.json)
confirms the original boot/base and no own process/module/pins/GPU application;
it is not immediate-post-run or continuous isolation evidence.

[Final restoration](../../bench/results/uring_incremental_copy_20261013/final_restoration.json)
removes the owned temporary runtime/apparatus and30 build entries after result
review. Seven entries are launcher symlinks; only the named links are unlinked,
and their original source target is preserved. Original boot/base, cached
models and unrelated tools/setup_env.sh remain. No own model process/module/
pins/GPU application remains. This is late closure, not continuous isolation.

Close this completed copy comparison with its inconclusive performance result.
Do not repeat unchanged cells or infer that copy work has zero cost. Keep the
module default and optional stock path. Prioritize the measured polling/
wakeup CPU cost and optimized cross-node delivery while continuing to reuse
upstream computation; do not start a model-specific arithmetic campaign.

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
