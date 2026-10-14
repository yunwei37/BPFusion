# CQ progress captured before submission

The optional sleepable loop candidate captures CQ tail before submitting
GPU-published SQEs, then asks the kernel to wait for that saved value plus1.
Previously it captured CQ tail after submission. The before snapshot can
recognize completions produced during submission instead of requiring another
completion. Quiesced cleanup retains current-tail/no-sleep behavior.

Upstream [loop.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c)
skips waiting when the requested CQ index is already reached.
[io_uring.c](https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/io_uring.c)
flushes immediate completion state before io_submit_sqes returns.
This supports a candidate mechanism; it does not establish observed avoidable
sleep counts or the cause of finding0044's delivery losses.

The former loop builds from the same BPF source with BF_IO_CQ_AFTER_SUBMIT
and uses build/uring_loop_after.bpf.o. The optional
vllm-graph-uring-loop-after target selects that object only at bootstrap.
Candidate/control GPU model and network-controller code,request ABI,timer,
TCP and compute policy remain unchanged. No userspace request worker or
custom TX module is introduced. Default module serving remains unchanged.

The [plan](../../bench/results/uring_cq_progress_20261014/plan.md) and
[fresh plan review](../../bench/results/uring_cq_progress_20261014/plan-review.md)
admit one supporting completion-order intervention with efficient native TCP
as main baseline and the former loop as a component control. Four primary
native contrasts are gen1/c8 TTFT and gen64/c8 throughput for both models,
selected before outputs. CPU is a measured secondary tradeoff. Whole-output
references stay byte-identical to finding0044; ordinary batch histories
remain unobserved. No universal correctness,task quality or SOTA claim.

Common temporary pinned dependencies and native/BPF builds complete.
Candidate/control model dispatcher and io_network SASS are byte-identical.
First real preflight passes all3 paths/12 cells,120 requests/3144 checked
tokens including24 excluded warmups,exit/analysis0. All12 strict vLLM
executors pass7464 requests/266688 valid tokens,3108 intended rejects and
60000 empty connections. Both unchanged HF idle/lifecycle workloads pass32
requests/652 complete/prefix tokens per model,13 closed sockets and3 expected
aborts. All checks exit normally; loop traces show one steady kernel entry
with no userspace socket calls. Full qualification is complete and archived in
[qualification history](../../bench/results/uring_cq_progress_20261014/qualification.md).
Matched timing remains pending. No performance or CPU result follows from
these dependency checks.

From the original qualified Workspace and runtime:

    make vllm-graph-uring-loop vllm-graph-uring-loop-after vllm-graph-user-network-wait vllm-graph-trace VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --correctness --model MODEL --output RAW
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --untraced --reference-path FROZEN --model MODEL --output RAW
    /usr/bin/python3 bench/vllm_serving_analysis.py RAW

Exact bindings are in the linked plan/command/package archive. Full retained
project acceptance remains open; unchanged0044 timing stays closed.
