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
Matched timing and fresh independent result review are complete below; owned
temporary resources are removed and restoration is recorded. No performance or CPU result follows from dependency checks.

From the original qualified Workspace and runtime:

    make vllm-graph-uring-loop vllm-graph-uring-loop-after vllm-graph-user-network-wait vllm-graph-trace VLLM_PYTHON=ENV/bin/python
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --correctness --model MODEL --output RAW
    ENV/bin/python bench/vllm_serving.py --loop-progress-comparison --untraced --reference-path FROZEN --model MODEL --output RAW
    /usr/bin/python3 bench/vllm_serving_analysis.py RAW

Exact bindings are in the linked plan/command/package archive. Full retained
project acceptance remains open; unchanged0044 timing stays closed.

## Completed ordinary comparison

Frozen main d45b82f255c2b4afc452ba482b90b092c52e08bc completes36 executors/
144 cells,9216 measured requests/299520 measured output tokens plus288
excluded checked warmups. Each model has18 normal executor exits,72 cells
and both analysis exits0. Every complete reply passes the unchanged
pre-observation output set. This is finite-set fidelity,not replay of current
unobserved ordinary batch/KV history or task-quality evaluation.

| Model | Before / native / former-after TTFT gen1,c8 ms | Before / native / former-after TPS gen64,c8 |
|---|---|---|
| Qwen2.5-0.5B | 2.595156 / 2.521403 / 2.616306 | 4576.208668 / 4693.095908 / 4640.751804 |
| SmolLM2-135M | 1.994043 / 2.044095 / 2.021901 | 5453.524713 / 5374.723866 / 5397.356865 |

All four predeclared primary effects favor candidate when positive,with
nominal paired t95,df5 over six process blocks.

| Model | Primary native contrast | Mean | Nominal paired t95 |
|---|---|---:|---|
| Qwen | native-minus-before TTFT1,c8 ms | -0.073754 | [-0.192306,0.044798] |
| Smol | native-minus-before TTFT1,c8 ms | +0.050052 | [-0.116828,0.216932] |
| Qwen | before-minus-native TPS64,c8 | -116.887239 | [-261.334558,27.560079] |
| Smol | before-minus-native TPS64,c8 | +78.800847 | [-129.197723,286.799418] |

Every primary interval includes zero. No reliable native delivery advantage
is established; this is not equivalence or proof that snapshot ordering has
no cost. Keep all larger block differences,including Qwen throughput blocks1/2
and Smol blocks0/3. No unverified cause or exclusion is assigned.

Retain nominal secondary negatives: Qwen gen1/c8 TPS is lower than native
by167.590019 token/s, t95[74.234413,260.945626]. Qwen gen64/c8 TTFT
is slower than former-loop by0.106719ms, t95[0.031336,0.182103]. Smol
gen64/c1 TTFT improves over native by0.058104ms, t95[0.024078,0.092130],
but its before/after component interval crosses zero. These secondary effects
do not replace the predeclared primaries. The complete review retains every
cell and comparison.

The same-cell former-loop contrasts are component effects,not a second main
baseline or a way to replace inconclusive native primaries.

| Model | Component contrast favoring before | Mean | Nominal paired t95 |
|---|---|---:|---|
| Qwen | after-minus-before TTFT1,c8 ms | +0.021149 | [-0.154022,0.196321] |
| Smol | after-minus-before TTFT1,c8 ms | +0.027858 | [-0.013878,0.069595] |
| Qwen | before-minus-after TPS64,c8 | -64.543136 | [-192.914599,63.828327] |
| Smol | before-minus-after TPS64,c8 | +56.167848 | [-55.068777,167.404473] |

All four component delivery intervals also include zero. The source-backed
possibility remains unproven as an observed avoidable-wait count, cause of old
finding0044 losses or useful performance correction.

| Model | Before / former-after / native CPU64,c8 ms/request |
|---|---|
| Qwen | 0.550996 / 0.557682 / 0.490435 |
| Smol | 0.489155 / 0.500387 / 0.435193 |

Before/after CPU contrasts are inconclusive. Native known-worker CPU remains
lower on both nominal secondary gen64/c8 intervals. These all-thread process
clock brackets include creator kernel work once,but exclude RX/softirq/BPF/
TCP elsewhere,clients and energy. Neither total CPU nor exclusive snapshot/
timer/BPF cost is identified. Different arrival/batch trajectories may mediate
delivery despite identical candidate/control GPU instructions.

The observation SSH connection fails during Smol,local exec48829 exit1.
[Disconnect receipt](../../bench/results/uring_cq_progress_20261014/performance_observation_disconnect.json)
records reconnection and the same original remote pipeline282080/driver286552
still advancing. No executor or timing cell is restarted,replaced or excluded.
Both model children and analysis commands eventually return0,with complete
raw terminal events. The remote wrapper exit is unobserved after SSH failure;
do not report an overall wrapper exit0 or confuse the observation failure
with a proved benchmark-client delivery failure. Its cause and arbitrary
measurement interference are not established.

[Qwen raw](../../bench/results/uring_cq_progress_20261014/qwen_performance.jsonl),
[Qwen reconstruction](../../bench/results/uring_cq_progress_20261014/qwen_performance_analysis.stdout),
[Smol raw](../../bench/results/uring_cq_progress_20261014/smol_performance.jsonl) and
[Smol reconstruction](../../bench/results/uring_cq_progress_20261014/smol_performance_analysis.stdout)
preserve all requests,outputs,arrivals,worker identities,clock brackets,
commands and counters. The [kernel journal](../../bench/results/uring_cq_progress_20261014/performance_kernel_journal.json)
returns0 with '-- No entries --' over the selected actual timing bracket.
It is not positive proof of no faults or continuous isolation. The separately
observed [endpoint](../../bench/results/uring_cq_progress_20261014/performance_end.json)
has the original boot/base and no own module,pins or GPU app.
The [fresh independent result review](../../bench/results/uring_cq_progress_20261014/result-review.md)
judges this completed run valid, its tested hypothesis inconclusive and its
research role supporting. Both timing and four strict analyzers replay with
byte-identical stdout; independent arrival/CPU/interval reconstruction matches.
The [final restoration](../../bench/results/uring_cq_progress_20261014/final_restoration.json)
removes the owned temporary runtime and32 named build entries, preserving the
original boot, base runtime, default HF library, Coder processes and unrelated
tools/setup_env.sh. No own module, pins or GPU app remains at the endpoint.

This completed source intervention establishes no reliable delivery gain.
Keep the module default and describe before/after as qualified experimental
variants,not a proven recommended optimization. Close unchanged timing after
completed review/restoration; do not search timer settings until favorable
or tune model arithmetic. Optimized cross-node deployment remains an unresolved
matched acceptance boundary under the full retained project goal.
