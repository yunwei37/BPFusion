# PLAN REVIEW — incremental stock-TCP output copying

**Verdict：admit。当前计划没有会使实验结果失效的科学或执行缺陷，可以进入真实 preflight。** 本次只做只读审查；没有编辑源码、计划或启动 serving。资格验证及完整性能运行尚未完成，不能据此声称候选正确或更快。

## 1. 问题、假设与研究价值

计划准确保留 finding0035 的本机问题，并明确不改写 finding0029 的跨节点问题或完整项目目标。选定的假设是：跳过已发送输出前缀的重复复制，能否改善 stock transport 的 gen64/c8 吞吐。候选与 full-copy 控制构成直接干预，native 条件再回答优化后的完整路径是否具有实际竞争力。

这是**supporting** 实验，不是 headline、novelty 证明或总目标完成证明。0042 已经显示 stock 的 CPU 成本高、Qwen 吞吐较低，但没有 copy-only 条件，旧数据无法通过重分析回答这次问题。因此并非重复同一个 transport matrix。

Admission 理由成立，但价值应保持有限：

- 正结果：说明这段重复工作在当前实现与负载中具有可测成本，可以改善 stock 路径。
- 负结果：说明减少这些复制仍不足以提高当前负载的吞吐，或候选产生了负面的执行影响。
- 混合结果：形成模型或负载边界，不支持通用优势。
- 跨零：未识别可靠效应，关闭这一矩阵，不以重复运行寻找正结果。

SQPOLL CPU/wakeup 和跨节点优化的总体项目价值更高；不过本次干预具体、局部，能分辨 0042 未辨明的一个原因。它可以作为一次有终点的 supporting 实验先做。完成后，应回到这些更重要的未解决问题，而不能连续扩大 copy 微优化矩阵。

## 2. 对照是否公平

当前 diff 支持计划中的隔离：

- `executor/io_uring_tcp.h:185–194` 只改变复制循环起点。
- full-copy 控制通过 `BF_IO_FULL_COPY` 将起点恢复为零，复现此前的循环。
- Makefile 给两种 stock 条件匹配 `BF_URING_NETWORK`、`BF_PAD_PREFILL`、`BF_PREFIX_RELEASE`；只有控制多一个复制标志。
- 没有改变模型数学、backend Python、模型 dispatcher、队列、SQPOLL 参数、SEND 地址和长度、完成回收、FIFO 或诊断计数。
- `bench/vllm_serving.py` 对两个 stock 名称使用相同 attach、task 检查、终态和计数器检查。
- native 使用现有 `vllm_graph_user_network_wait`，代表同计算条件下可信的高效 CPU 编排替代方案。将其称作机制对照，而非官方 vLLM server 或 SOTA，正确。
- 删除 module 行合理：它不能隔离这次复制变化，0042 已有该组件条件。

源码层面的 copy-only 干预不等于硬件层面只有映射内存流量变化。编译后的指令数、寄存器使用或控制线程执行行为也可能改变。结果可以归因于**这段代码干预的整体效果**，不能进一步独占归因于显存带宽、单次 load latency 或某个具体硬件瓶颈。

## 3. 字节语义与缓冲区生命周期

当前起点计算在源码层面正确：

```cpp
first = r.sent > r.header ? (r.sent - r.header) / 4 : 0;
```

- 尚未发送完整 HTTP header：仍从 token0 开始复制，header 本身由 `header_ready` 保留。
- 正好发送完 header：起点为零。
- 已完整发送若干 token：跳过这些 token。
- 在 token 中间发生短 SEND：向下取整，重新复制该完整 token，下一次 SEND 从 `r.sent` 开始，已发送字节不会再次上网。
- binary 路径 header 为零，同样成立。
- `r.busy` 在 CQ completion 前阻止再次修改 TX buffer；这次 diff 没有削弱该生命周期约束。
- HTTP400、EOF、RST、停止和最终提交的原有分支保持不变。

这是源码论证，不能写成已真实覆盖所有短 SEND 的运行证明。标准异步 SEND 允许短发送；官方 liburing 文档也说明，未要求完整长度时，短发送不被视为错误，并提醒同一 socket 的多个 in-flight SEND 需要处理顺序。[liburing SEND 文档](https://github.com/axboe/liburing/blob/master/man/io_uring_prep_send.3)

既有完整 strict 与 HF lifecycle 回归是合理资格依赖。没有必要为了本次性能假设额外制造一个广泛网络压力矩阵。结果报告应继续明确短 SEND 特定边界是否实际观察到。

## 4. 数值正确性和固定参考集

我核对了冻结文件：它与公开 0042 的 `frozen_references.json` **字节一致**；Qwen 为17个 prompt/gen key、22个完整序列，Smol 为17个 key、19个完整序列，gen 集合为1和64。

计划没有从新输出构建 oracle：

- traced strict 使用独立 upstream batch/cache-history 回放。
- ordinary strict、preflight、性能使用预先冻结的完整序列集合。
- driver 与 analyzer 都检查整个序列对精确 prompt/gen 的集合成员关系。
- 没有逐 token 拼接、误差容忍或事后扩大参考集。

固定集合的限制已写明，而且实质存在：它不证明当前 ordinary 请求的真实 batch/KV 轨迹正确，也不保证各条件生成相同序列。历史合格序列之间的差异可能随到达和批处理变化。计划允许的结论应保持为**相同计算算法与有限完整序列资格下的性能比较**，不能写成相同执行轨迹或逐请求相同输出的因果比较。

如果出现新序列，应保留并诊断本次失败，不把它直接当成数值错误，也不能通过添加新序列让当前运行通过。现有计划正确保留了这条边界。

## 5. 工作负载、统计和指标

范围与源码一致：

- 2模型 × 6 process blocks × 3路径 = 36 executors。
- 每 executor 256个 gen64/c8 测量请求：9216请求、589824 token。
- 每 executor 8个 gen1 warmup：288个排除计时的 token。
- preflight 为3路径 × 8测量请求：24请求、1536测量 token，另24 warmup token。
- 12个 traced/ordinary strict executors：7464请求、266688有效 token、3108拒绝、60000空连接。

gen1 不作为独立 timing cell 是合理的：它不能直接作用于“跳过已发送前缀”的假设。TTFT、TPOT、completion 和 CPU 作为同一 gen64/c8 单元的次要指标已经足够，不需要为了完整性增加负载。

6种排列各一次，三个条件在每种位置各出现两次。配对单位为 process block，`df=5`、临界值2.570581835636305、标准差除以 √6，分析器实现正确。不能把256请求或32 waves 当成额外独立重复。

四个主效应分别报告：

1. Qwen candidate/native 吞吐差；
2. Qwen candidate/full-copy 吞吐差；
3. Smol candidate/native 吞吐差；
4. Smol candidate/full-copy 吞吐差。

没有家族范围的 superiority 或 equivalence 结论。负估计、异常样本、跨零区间必须保留，secondary 不替换 primary。

指标定义有合适的官方来源。versioned vLLM client 定义 output throughput 为输出 token 数除以运行时长，TPOT 为 `(latency − TTFT)/(output_tokens − 1)`，并将 completion 作为客户端发送到完整响应的时间。本项目使用 first-send 到 last-arrival 的 cell 窗口，是清楚声明的本地测量边界。[vLLM v0.31.0 client](https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/benchmarks/serve.py)

已检查 driver 与 analyzer：它们从原始 arrival/start 重算对应指标，且吞吐差的符号为 candidate-minus-baseline，延迟与 CPU 差的符号反向。结果表必须说明后一类正数表示候选更低，避免把这些符号混为一谈。

## 6. CPU 与其他归因限制

`worker_cpu_snapshot` 使用 POSIX executor 全线程 CPU clock；stock 的实际 SQPOLL task 存在检查仍然保留。无 module 的本次矩阵中 TX counter 应为零，因此没有 SQPOLL 双计数。

采样包围 first-send 和 last-arrival，包含期间的一些连接关闭或收尾成本，排除其他线程组的 RX、softirq、BPF/TCP 与客户端。计划没有总 CPU、能耗或 CPU-saving primary，正确。

共享主机的有限端点和 fault 检查不证明连续隔离。若出现实质不均衡故障或外部 GPU workload，需要记录受影响区间并判断比较有效性，不能将 baseline 故障当成候选优势。

## 7. 可执行性与进入完整运行的条件

literal qualification pipeline 已绑定原 Workspace、临时 runtime、两个固定 checkpoint、child PATH 和 `VLLM_ENABLE_V1_MULTIPROCESSING=0`。Makefile 和 binary 命名、attach 选择、三条件 preflight、traced/ordinary strict、分析命令相互一致。没有发现当前 driver/analyzer diff 的执行阻断问题。

两个尚未绑定完整的后续事项不阻止当前 preflight，但完成资格链和 full-run 前必须补足真实记录：

- 当前 `qualification_commands.json` 没有计划要求的 `qwen-graph-uring` rebuild 和两模型 HF lifecycle 命令。应在执行该资格步骤前记录实际命令及输出，不能只用文字声明已覆盖。
- performance pipeline 尚未归档。计划已明确它在资格通过、main 源码冻结后生成；应使用同一 literal runtime/models/reference，运行全部36 executors，不修改 oracle、pacing、预算或 source。

源码尚未经过本次 GPU 验证。因此本 review 允许进入真实执行，并不预先接受 correctness、机制参与或结果。若修复影响复制机制或对照公平性，应记录变更、重跑受影响资格及比较；不能用 qualification 失败偷偷缩减用例。

## 返回判断

- **Plan status：admitted，允许真实 preflight。**
- **Planned research value：supporting。**
- **Paper impact：局部 transport 机制与负载边界；可能增加 retained local question 的证据。**
- **Primary claim boundary：copy-only 源码干预的吞吐效果，以及候选相对同计算 native 的性能。**
- **不支持的结论：跨节点优势、总 CPU 节省、模型优化贡献、SOTA、通用正确性或完整项目完成。**
- **运行后决策：无论正、负或不确定，关闭这次预声明矩阵；通过独立 result review 后再选择 SQPOLL、跨节点或其他有新因果区分能力的工作。**

## Follow-up 1 — unexplained initial full-copy half-close failure

This is the first follow-up to the original plan review. It reviews the new
failure-validity concern, not a new experiment or an approval authority.
Production source and serving were not changed or started by this reviewer.

### Evidence inspected and current status

I read qualification.md, the amended plan, the initial failing raw/client/model
records, both diagnostic receipts, current source diff, and the subsequently
terminal temporary half-close stress records.

The initial Smol full-copy strict run is a real failed qualification attempt.
The client receives EOF before completing the first pipeline HTTP header.
It has no successful pipeline_halfclose request row. The eventual terminal
records show616 admissions/completions, six aborts, graph_error0, no recorded
BPF drop, all slots FREE and balanced SQ/CQ. These records are after the
driver's error cleanup, which terminates the server. They do not establish
whether abort/close preceded the client error or resulted from cleanup.
Independent model replay of616 requests is not successful TCP delivery of
the six missing replies. The initial protocol remains failed/incomplete.

The GPU close-instrumented and kernel-printk diagnoses each subsequently
complete the three Smol strict paths, but neither reproduces or explains
the initial failure. Their instrumentation can perturb timing. Restoring
production code and the ordinary BPF object is necessary; those passes
cannot serve as proof of a fix.

At this review's observation, the temporary noninstrumented Smol stress
driver has reached terminal exit0 for full-copy followed by candidate.
Each reports1000 requests,46416 independently replayed tokens,259 intentional
rejections and64 six-request half-close pipelines. Terminal ring head and
completed are1000; pending/error/reserved/dropped/overflow are zero. Each
reports one abort, consistent with the driver's intentional binary rejection;
do not conflate this with the initial six missing pipeline replies.
This increases direct evidence for the unchanged half-close path. It does
not reveal the initial cause or establish a failure probability. The stress
driver is a diagnostic, not a replacement for the original622-request strict
protocol, native condition, ordinary qualification or HF lifecycle.

The current production header is byte-identical to the retained failure
version. Its only diff against main is the already-reviewed loop-start
candidate/full-copy branch. No production lifecycle repair is established.

### Does an unexplained qualification failure invalidate later timing?

Not automatically. Separate two questions:

1. Does this implementation reliably implement the complete TCP lifecycle?
2. What throughput does the unchanged implementation deliver in the declared
   ordinary gen64/c8 workload when all its requests complete and validate?

The first has contradictory evidence and remains unresolved. The second
can still obtain valid, narrowly scoped measurements. The planned performance
client uses established connections with one request at a time per lane and
reads the complete reply before sending the next request. It does not
pipeline six requests and half-close the write side before reading replies.
The failing lifecycle exposure is therefore not an intended timing cell.
This distinction is established by the actual client paths, not by excluding
an inconvenient failed timing sample.

Passing the original noninstrumented traced and ordinary strict protocols
and the unchanged HF lifecycle qualification would complete those specified
execution steps. It would show subsequent successful qualifications, not
erase the initial failed attempt or show the fault repaired. A root cause is
not logically necessary to interpret every successfully delivered ordinary
measurement; conversely, later passes cannot justify a comprehensive
correctness/reliability claim.

As of this review, performance remains unexecuted/incomplete and the original
ordinary/native/HF requirements still need their actual terminal receipts.
This follow-up does not treat their future success as already observed.

### Conditions for a scientifically interpretable single timing matrix

The existing acceptance and oracle remain unchanged. A later single complete
matrix can be interpreted only if its own evidence establishes the following:

- The original noninstrumented qualification and HF steps actually finish;
  diagnostic passes do not replace them.
- All36 planned executors/cells run with the frozen candidate/control/native
  source and literal bindings. All9216 measured requests and warmups pass
  their fixed complete-output checks; ownership/counter/termination checks
  pass, with no missing or failed timing row.
- All conditions engage their intended mechanisms, including the full-copy
  ablation and native control. The source freeze includes restored ordinary
  BPF/GPU logic; there is no instrumented-control versus ordinary-candidate
  comparison.
- Retain the initial failed qualification, every diagnosis and any later
  failure beside the timing results. Do not assemble six successful blocks
  from repeated attempts, replace unfavorable blocks, or count delivery
  failure/abort as a throughput loss that establishes candidate superiority.
- If delivery/lifecycle failure recurs in a timing executor, that declared
  complete matrix is incomplete, and the affected comparison is invalid or
  incomplete. Completed earlier rows remain raw evidence, not a full-matrix
  win. Any systematic repair changes the source and requires recorded
  rerunning of affected comparisons, rather than unchanged success-seeking
  retries.

These are validity consequences of the original protocol, not additional
workloads, thresholds or acceptance relaxation. Unknown failure risk should
not be converted into an invented statistical penalty or a reliability rate.

### Justified interpretation and remaining limit

If all original qualifications and the one complete frozen timing matrix
finish under those checks, report its run status as valid completed
measurements for the declared ordinary workload, with the unresolved
qualification failure explicitly attached as an implementation limitation.

Then candidate/full-copy effects may support, contradict or leave
inconclusive the copy-loop intervention's scoped throughput hypothesis.
Candidate/native effects remain separately scoped to the same ordinary
workload. Four nominal paired df5 intervals are still the declared analysis.
No conclusion follows about pipelined half-close performance or reliability,
general end-to-end correctness, elimination of lifecycle races, or a robust
production serving advantage.

The defensible wording is:
"On a complete later ordinary gen64/c8 comparison, all requests pass the
declared fidelity and terminal checks; an earlier full-copy traced strict
half-close attempt failed and remains unexplained despite subsequent
successful diagnostics/qualifications."

The indefensible wording is:
"The failure was fixed", "all qualification attempts passed", "no lifecycle
issue exists", or "the candidate wins because the control failed".

A positive throughput interval does not erase that implementation concern.
The full retained project goal's correctness/completeness requirement remains
unproven until the unresolved lifecycle issue is addressed with stronger
evidence. Thus timing need not remain forever incomplete solely because the
first failure lacks a cause, but the broader lifecycle claim must remain open.
If diagnosis continues to consume effort without new discriminating evidence,
record the boundary and compare further investigation with the already
identified higher-value SQPOLL/cross-node work; do not turn a finite supporting
experiment into indefinite retries.

### Follow-up judgment

- Original copy-only scientific admission remains appropriate.
- Current full timing status: not executed/incomplete.
- Known lifecycle evidence: one real failed control qualification; later
  noninstrumented stress success does not explain or repair it.
- A complete no-retry timing matrix can yield valid ordinary-workload evidence
  after the unchanged required qualifications actually pass.
- Broader correctness/reliability and full-goal completion remain unproven.
- No production change, oracle/pacing change, extra baseline or altered timing
  acceptance is requested by this review.

## Follow-up 2 — captured transient RECV failure and common lifecycle repair

This is the second and final follow-up under the existing reviewer protocol.
It assesses the amended plan and implementation evidence. It is diagnostic,
not authority to execute, and introduces no extra baseline or acceptance
relaxation. Only this review is appended; production source/plan and serving
are not edited or started by this reviewer.

### Captured evidence and what it establishes

I inspected hf_idle_stress/qwen.results.json, qwen.native.stdout, the temporary
CQ diagnostic source, the current production header diff, qualification.md,
the amended plan and qualification_repaired.py.

The HF idle reproduction records early HTTP EOF on its first valid Qwen
request. Its wrapper exit is0, but the actual result is pass=false with
RuntimeError('early header EOF'); it is a failed reproduction, not a passing
qualification. Before releasing CQ slot sequence2, the device records the
same RECV tag144115192370823168 and res=-11 through both ordinary and
system-acquire loads. The diagnostic source records those fields before
publishing CQ head, which avoids interpreting a reused CQ slot as the
exceptional observation.

The old production branch treats every negative RECV result as c.dead=1.
The recorded receive EAGAIN therefore directly explains why that branch
marks this connection dead and permits closing rather than rearming.
accepted/closed1, received/sends0, eventual head/completed1 and aborted1,
with graph_error0, are consistent with the captured failure and cleanup.
This establishes a concrete fatal handling defect for the captured
transient result. It does not establish why the underlying operation
returned EAGAIN, or prove a universal absence of all coherence issues.

The original six-request half-close failure did not capture its CQ errno.
It remains inappropriate to retroactively assign this cause to that event.
The new evidence narrows the earlier unresolved investigation by identifying
a real shared-header defect, not by proving every earlier EOF had one cause.

### Repair mechanics and execution consequences

The current common change is:

    else if(e.res!=-EAGAIN && e.res!=-EINTR)c.dead=1;

RECV completion still resets c.receiving to0. For those two transient
results, the normal existing receive-rearm condition can submit another
RECV for a live, non-EOF connection. Actual res0 still sets eof. Other
negative results still set dead. Existing stopping, cancellation and
pending-buffer ownership rules remain, including the no-rearm check
during stopping. No new CPU request worker, timer, polling setting,
wire-format change or client barrier is introduced.

The current production diff contains this common branch and the reviewed
copy-loop branch, without the temporary CQ/shutdown diagnostic members or
prints. The correction is material to lifecycle behavior: previously failing
requests may now survive and be admitted, which can also alter arrivals,
batch trajectories and counters. Old qualification is consequently not
qualification of the corrected implementation.

EAGAIN is observed in the diagnostic. EINTR handling is a reasonable
implementation counterpart, but no captured EINTR exercise was shown here;
the report must not claim that branch was empirically exercised.

### Meaning of the full-copy control after the repair

The control now means:
"full-prefix copying on the same corrected RECV implementation as candidate."

It no longer means:
"the complete original0042 implementation with identical lifecycle semantics."

That change is scientifically appropriate. An unrepaired condition with a
known avoidable transport fault would be a poor mechanism baseline; retaining
the fault merely to resemble historical source is not required. Applying the
same repair to both stock conditions preserves the within-matrix copy-only
contrast. The selected local question, hypothesis, gen64/c8 workload, four
primary contrasts and six-block analysis do not change.

A valid new candidate/full-copy difference estimates the effect of the copy
intervention on the corrected common transport. A valid candidate/native
difference compares the corrected incremental complete path against native.
Neither difference separately estimates the RECV repair's performance cost
or benefit. Subtracting0042's old means to claim a copy-only speedup would
mix the common repair, source/history and execution environments and is
unsupported. No additional broken-receive baseline is requested.

The earlier narrative that all remaining CQ/receive logic is unchanged
should be read as a within-new-matrix statement. The added explicit common
repair paragraph supplies the essential provenance correction; final
finding/result wording should say both stock variants share this repair.

### Requalification, freezing and validity

qualification_repaired.py actually schedules rebuilding, the original
three-path Qwen preflight, both model triples of traced strict, both triples
of ordinary strict, shared-header HF rebuilding and the two-model HF
lifecycle. It uses the pinned vLLM child environment for vLLM and base
environment for HF. The HF wrapper's status is explicitly checked for two
entries, exit0 and pass=true; wrapper exit alone is not accepted.
The existing references, driver pacing, matrix and analysis remain fixed.

At this observation the repaired status records build exit0 only. Remaining
preflight/strict/HF success and performance completion are not yet evidenced
by that status. Earlier passing source versions cannot fill those entries.

The designated reruns cover the changed shared path and are the correct
response to a material common repair before timing. After they actually
pass, freeze the corrected common source and full-copy/candidate build
meaning before the one complete timing matrix. If any repaired qualification
fails, preserve the failure and diagnose the actual defect; do not silently
proceed using old passes or change the oracle/pacing to manufacture a pass.

A later successful repetition of the captured idle reproduction would
strengthen evidence for the repair, but is not a new primary experiment or
a prerequisite for every narrow performance interpretation. Its current
diagnostic failure is already retained. The original designated strict and
HF requirements remain required and unchanged.

If the complete corrected timing matrix passes all planned delivery,
fidelity, mechanism and terminal checks, it can support the same narrowly
scoped performance conclusions described in Follow-up1. No failed timing
condition can become a candidate win. No successful blocks may be selected
from repeated attempts to construct the declared matrix. The finite-set
ordinary oracle and shared-host uncertainty remain exactly as before.

### Final follow-up judgment

No new scientific/executability blocker is introduced by applying the
captured-defect repair identically to the two stock conditions. The amended
experiment remains a supporting copy-intervention comparison, conditional
on actual repaired-source qualification and complete frozen timing.

The current state is source repaired/build completed; full qualification
and timing are incomplete at this review's observation. The captured
EAGAIN fatal-handling defect has an explicit code correction, not yet a
complete empirical repair claim. The original unobserved-errno pipeline
failure remains a separate historical uncertainty; subsequent broad
qualification can bound observed behavior without proving universal
reliability or retrospectively supplying that errno.

The final result must preserve the original failures, specify the common
repair, label full-copy as a corrected-source ablation, and avoid historical
copy-only gain or comprehensive reliability claims. No additional baseline,
workload expansion, source change or acceptance relaxation is requested.

This closes the permitted three plan-review rounds: original review plus
two follow-ups. A future blocking scientific defect must be returned to
the parent under the existing protocol, rather than creating another
review name or another unchanged plan-review round.
