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
