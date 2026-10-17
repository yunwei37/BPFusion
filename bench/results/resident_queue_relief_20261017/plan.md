# Relieve the shared resident admission/queue bottleneck

2026-10-17 UTC, entry mainfcc184c. User explicitly requires self implementation/
experiments without OMP or another agent. Therefore plan/result checking is by
the owner; no independent agent review is claimed. This supersedes skill review
delegation for this task. Retained serving objective is faster delivered
throughput/latency with reused model computation, followed by fair eBPF effect.
No formal paper RQ/idea-story exists.

0078 establishes~11645 resident versus12245 official outputtokens/s and
completionP99~3314 versus611ms at192/s. Both resident transports agree.
Prior raw ten-second arrival buckets and actual default-official running/waiting
logs show a testable alternative:16 active resident banks limit sustainable
capacity just below offered rate,accumulating work before first output.
Official running requests exceed16,waiting sampled0,prefix hits0,short prompts.
Generation spans are shorter on resident. These facts motivate a capacity/
batching repair but do not isolate a GPU stage or prove KV/chunked-prefill causes.
Existing0064 covers8vs16 traced/short cells,not this ordinary60s external gap
or32; no repeated unchanged capacity matrix is proposed.

Hypothesis: an actual normal32-bank resident native constructor,with matching
shared-page/BPF/loader/GPU layouts and unchanged upstream math,suffices to remove
the sustained queue growth and approach official whole-service delivery here.
Contradictory outcome: stable same-client gap/queue remains or correctness fails;
then investigate common scheduler/capture/KV work instead of claiming a fix.
This is an implementation repair with supporting causal evidence,not eBPF novelty.

Begin with normal32build,finite real model/protocol/replay and actual same-load
native16/native32 diagnostic controls. Build32 is within the existing32-bit
reservation representation; do not exceed it or silently widen ABI. A matching
separate BUILD is required; default8 is unchanged until evidence/qualification.
Do not alter parser/arrival offsets/model/oracle/timeout/latency definitions.
Reuse original0078 repaired four-worker uvloop client,gen64,four prompt IDs,
192/s60s+fulldrain,seeds20261015+block and official default-optimized source.
Keep all attempts,failures,pool flags,client lag,CPU and raw payloads.
No hand-optimized attention/matrix kernels,forced-eager official,or artificial
external scheduler limits.

If the repair works,complete the matched N16/N32/O five-process-block comparison
and then compare K32/N32 for transport effect. Existing official result is context,
not a replacement contemporaneous final baseline. Exact full order/primary and
commands are recorded before full acquisition after real path qualification.
No partial prefix is a completed result; no runtime change during a matrix.
Results and all source/raw/deviations commit/push as milestones. Do not stop at
a measurement-only report while a directly evidenced repair is available.

Same original bpfusion-dev Workspace/main/PVC/PIDs and foreignsetup_env remain.
Temporary serving/client steps use the requested benchmark lifecycle; no new
persistent service/scheduler/Workspace/configuration. Cleanup exactowned
Job/PodUIDs,pins,GPUgroups; preserve all existing work. Source implementation,
builds/tests and experimental choices are owner-executed only.


## Executable diagnostic and final comparison contract

The32real-model protocol passes2764outcomes/107136tokens with exact same-graph
and rebuilt-metadata replay. Subsequent CPUanalysis's hardcoded8padding is
repaired from existingbanks metadata without altering measured checks/outputs;
initial error and original8byte-equalcontrol remain in analyzer_repair.md.

Diagnostic: one native16/native32 process pair,unchanged0078client192/s60s,
stagequeue_relief_diagnostic. This completed causal repair check is not a
substitute for five-block uncertainty or the contemporaneous official result.
Fixed final matrix (if executable repair is supported) is5blocksN16/N32/O:
before,native,official; native,official,before; official,before,native;
official,native,before; native,before,official. Both native labels use the
same clientmode=native,with actual matchingbuild16/32 respectively.
Official uses defaults/actual auth and sameoriginalmodel/seed/client.

Fixed primary final effect: N32-minus-N16 connect-origin completionP99,
nominal pairedt95df4. Negative interval supports a local tail improvement;
crossing0 is inconclusive. Preserve N32-O throughput/completion/TTFT and
scheduled-origin/TPOT/receivegap/failures/clientlag/resources; do not substitute
another metric after seeing results. Report exact ratios/distances to official
rather than inventing a posthoc universal definition of "close". Nomaximum-
capacity claim at fixed192/s. No independent agent audit is claimed.


## Diagnostic outcome and continuation

Both diagnostic cellscomplete11520successes0failures; completionP99 falls
3328.880->357.484ms,TPS11649.608->12266.103,meanTTFT1786.157->53.406ms.
MeanTPOTworsens1.354614->1.427012ms and referenceflags1/123 remain.
Archive CPUreplay byte-identical. This is one mechanism/repaircontrol,no
full five-pair or contemporaneous official result. It supports continuing
the predeclared fullmatrix after32-model/lifecyclequalification completes.

User clarified: "Codex 自己的子代理也不允许用，只能由你这个线程本身干活。
实现、实验、文档、论文，以及独立复核和审计，都在本线程里完成，不再派生任何
subagent，也不用 OMP 或其他 agent。" Existing prior reviews are retained;
live inventory shows all old subagentscompleted,no running child. This run's
checks are owner recomputation/self-audit,not an independent-person review.

## User continuation decision during full acquisition

2026-10-17 UTC: complete and commit this unchanged five-block16/32/official
comparison first. Afterwards LLM speed competition is closed as the main line.
The earlier planned K32/N32 LLM continuation above is superseded, not executed.
Proceed instead to one bounded cuBLAS/cuFFT small-request network/CPU experiment
with same-executor epoll controls, work/load/core crossovers, remote client,
complete tails, predeclared confirmation/exit criteria and owner-only execution.
No frozen comparison input, order, primary or exclusion changes.
Daily OSS upkeep and substantive-progress reflection are recorded in
docs/progress.md and committed/pushed with completed milestones.
