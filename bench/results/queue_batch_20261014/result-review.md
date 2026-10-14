# Independent result review: batched queue publication

Completed 2026-10-14 in the original yunwei356/bpfusion-dev Workspace.
One fresh RESULT reviewer under research-experiment-design. Read-only examination
of source, plan, artifacts and compiled instruction listings; no builds,
experiments, publication or further agents. This report is the sole review home.

## Judgments

- **Run status: valid for the declared finite encoded-token serving comparison.**
  The full planned matrix completed without missing/replaced/excluded cells or
  altered references. This is not a general model-fidelity or HTTP text-service
  acceptance statement.
- **Tested hypothesis: inconclusive as a transferable latency-plus-efficiency
  claim; supported locally for AMK against the prior coalesced component control.**
  AMK primary concurrency-eight short-output latency and long-output TPS improve.
  Neither vLLM workload establishes primary latency improvement; their positive
  latency-change means have zero-crossing intervals. Qwen long-output TPS improves;
  Smol's improvement remains uncertain. The large vLLM native latency gaps remain.
- **Research value: supporting.** This is a new actual queue-publication policy,
  with a matched competitor and preserved component control, not dependency-only
  setup or a repetition of the unchanged0050 matrix.
- **Paper impact: mechanism/workload boundary and additional retained-RQ evidence,
  not a direct central-thesis challenge or a universal eBPF transport win.**
- **Next paper decision:** retain the qualified batching policy as a modest
  coalesced-driver improvement with backend-specific limits. Do not present it
  as fixing0050's vLLM short-output concurrency problem or promote coalesced mode
  to a universal default. Close this unchanged matrix. Any further experiment
  should distinguish admission/batching/driver scheduling rather than repeat
  these cells or optimize model arithmetic without new causal value.

## Audit and completion

Read the entire plan.md and plan-review.md, the production header diff,
both captured CUDA dispatchers and Makefile, actual bootstrap/library selection,
native epoll server, matched_serving.py, analysis.py, qualification.py, lifecycle.py,
wrappers/build/reconstruction recipes and receipts, packages/environment,
full source/command freeze and all15 ordinary full JSONLs/all45 separate stdout
logs. Independently inspected protocol traces, reference replay source,
three lifecycle raw reply records and all four host observations.

Full collection spans metadata12:18:38UTC through terminal12:40:59UTC.
full.exit.json is zero at12:40:59.823102UTC; all15 driver receipts and45
executor results are zero. The independent raw audit found:
**45 executors,180 cells,5760 measured requests,187200 measured output tokens,
360 checked excluded one-token warmups.**

For every request, recomputed TTFT/completion/TPOT from start and arrival
timestamps, checked ordered arrival cardinality and complete output membership
against unchanged pre-observation pools. Independently recomputed every cell's
TPS from its actual first send and last arrival, all process/kernel-TX CPU deltas
and sample brackets, and all108 reported paired effects from five raw block
differences. All signed block values, means and nominal t95df4 endpoints agree
with full.analysis.json within floating arithmetic tolerance. The report retains
all outcomes there rather than copying a second full table. Mean cells and
effects in full.analysis.json are supported by raw arrivals, not accepted merely
because the analyzer exited zero.

Checked five path permutations and odd-block cell reversal for every executor.
full.command.json expanded commands equal full.exit.json executed commands, and
the command record embedded in full.source.json matches the frozen command home.
No full failure events or undocumented exclusions were found. A review-only
initial broad qualification glob also matched a GPU trace lacking metadata;
correcting the read-only selection to the three declared driver files completed
the audit. No experiment artifact or oracle was modified by that selection.

## Main baseline and control engagement

Native is the single strongest runnable competing mechanism for this matched
question, not a synthetic lower bound. Actual native builds use BF_USER_NETWORK
and BF_USER_NETWORK_WAIT, excluding the changed io_uring header, with the same
backend dispatch computation/FP16/model revisions/packing/prefix policy per
workload. Read userspace_tcp.h: nonblocking epoll_pwait2 with nominal60000ns
completion wait, accept4/recv and sendmsg, same shared page and streamed token
delivery. Native stdout records the intended wait path and published/completed
136 requests per executor. All native processes normally complete, no oracle
failure or avoidable interface failure was found. Efficient userspace defeats
several candidate metrics; it is not being counted as a candidate win.

The original coalesced path is a component control, not a second main baseline.
All four original_* snapshots are byte-identical to Git07ba7e0.
Makefile.original/rebuild_original.py reconstruct the actual former source
with the same native flags/linkage. Read-only cuobjdump inspection independently
confirms rebuilt control instruction listings equal the saved pre-rebuild
libraries for all three AMK and all three vLLM functions.
The candidate header snapshot is byte-identical to frozen Git2a2d21d.

Backend/library commands in each raw start select the intended old coalesced,
native or candidate library. Source-native entry selection preserves the
launcher filename and its corresponding .so. Full ordinary metadata embeds the
actual driver and both network policies. The temporary runtime is consistently
Torch2.13.0+cu129, Transformers5.17.0, vLLM0.31.0, Numpy2.3.5.
Pinned AMK884534c4, actual170SM configuration, cpasync0,8 private banks and
the model computation are unchanged. The AMK CUDA13 versus vLLM CUDA12.9
linkage difference remains a cross-backend limit, not an within-workload
transport confound.

## Primary outcomes and strongest-competitor limits

All changes below are candidate-minus-control; intervals are nominal paired
t95df4, not multiplicity-corrected confidence for a joint universal claim.

**AMK/Smol.** gen1/c8 TTFT is130.139ms versus prior133.302 and native130.444.
Against prior, delta−3.163ms [−5.556,−0.770], all five signs negative.
Against native,−0.305ms [−4.267,3.657]: neither superiority nor equivalence.
gen64/c8 TPS is301.132 versus prior293.111 and native304.004:
+8.021 [6.970,9.072] versus prior, but−2.872 [−3.688,−2.056] versus native.
The latency-plus-efficiency intervention is supported against the component
control; it still does not beat the strongest competitor. AMK's large absolute
latency remains.

**vLLM/Smol.** gen1/c8 TTFT is7.159ms versus prior6.325 and native1.970.
Delta+0.833ms [−0.203,1.870] versus prior does not establish a reliable regression
or improvement; four of five signs are positive. Native delta+5.189ms
[4.773,5.605] is reliably worse. gen64/c8 TPS is5197.852 versus prior5074.837
and native5639.217: +123.015 [−116.175,362.205] versus prior, with one adverse
block;−441.365 [−714.104,−168.626] versus native. No demonstrated primary
latency recovery or retained native efficiency is supported.

**vLLM/Qwen.** gen1/c8 TTFT is8.591ms versus prior8.308 and native2.633.
Delta+0.283ms [−0.237,0.803] versus prior is inconclusive; three positive and
two negative block signs. Native delta+5.958ms [5.535,6.381] is reliably worse.
gen64/c8 TPS is4523.922 versus prior4359.722 and native4703.202:
+164.200 [142.069,186.331] versus prior, all five signs positive;
−179.280 [−360.826,2.266] versus native, all five signs negative despite the
zero-crossing interval. Do not call this native parity/noninferiority.
TPS improves against the component control while primary short-output latency
does not demonstrate improvement.

## Secondary outcomes and costs

Reviewed all secondary gen1/c1/gen64/c1 and all completion/TPOT/known-worker CPU
effects; none may be discarded in favor of favorable primary throughput means.

AMK gen1/c1 TTFT improves versus prior by−0.461ms [−0.489,−0.434], but retains
a native penalty+0.127ms [0.075,0.178]. AMK gen64/c1 TPS improves versus prior
and loses versus native; its long-output completion/TPOT improve versus prior
at both concurrency levels and remain reliably worse than native. At gen64/c8
its TTFT change versus prior crosses zero despite completion/TPS improvement.

Smol's gen1/c1 and gen64/c1 changes versus prior are inconclusive. Its
gen64/c8 TTFT reliably worsens versus prior (+0.094565ms), while completion,
TPS, TPOT and CPU changes versus prior cross zero. Versus native, long-output
completion/TPOT and TPS at both concurrency levels and c8 TTFT remain adverse.
The c1 short-output native differences cross zero.

Qwen's gen64/c1 TTFT/completion/TPOT and TPS improve versus prior; c1 short-output
effects are inconclusive. At gen64/c8 completion/TPOT/CPU and TPS improve versus
prior while TTFT crosses zero. Against native, gen64/c1 and gen64/c8 completion,
TTFT and TPS changes have zero-crossing intervals, but gen64/c8 TPOT is reliably
worse. Its small c1 short-output native differences also cross zero.

Known-worker CPU is an all-thread executor-clock bracket plus the separately
reported kernel-TX component (zero here); it excludes total kernel/network CPU
and cannot support total CPU or energy claims. Long-output AMK CPU decreases
versus prior but remains above native; Qwen c8 CPU decreases versus prior but
remains above native at both long-output concurrency levels. Smol CPU versus
prior is inconclusive and long-output/c8-short native costs are reliably higher.
See all exact signed samples/intervals in full.analysis.json. No noninferiority
margin or invented aggregate winner is justified.

## Correctness, worker-free engagement and scientific scope

Every ordinary executor's separate stdout equals its JSONL stdout. All roots
report launches=1 and graph_error=0. AMK token-step counts equal actual generated
tokens,8 bank error values are zero; vLLM admits/retires136 and trace_overflows=0.
Ordinary io_uring head/completed136, accepted=closed, pending/error/reserved/
dropped/overflow zero, independent SQ and CQ empty, page slots free. The
diagnostic trace_overflow8 is the expected136−128 receipt capacity, not lost SQ/CQ
work. Native publishes/completes136 with zero rejects. No ordinary numerical
failure was hidden.

All three candidate protocol runs independently rechecked:
622 requests/22224 output tokens/259 rejects plus5000 empty connections per
workload, normal exit and empty rings/counters. Read the actual network strace:
after readiness no userspace accept/recv/send requests occur; exactly one
io_uring_enter appears before SIGTERM, consistent with blocking kernel progression
rather than a steady request worker. vLLM selected BF_TRACE protocol logs and
reference files pass structural admission/compute/release ownership checks and
actual token matching; actual batches1..8 are retained. Read bootstrap reference
replay: it reconstructs inputs, positions, per-bank KV mappings and batch history,
replays existing graphs and compares recomputed tokens, rather than simply
echoing candidate outputs. Ordinary paths remain untraced and do not establish
those same batch histories.

All three32-action lifecycle records independently rechecked including652
complete/prefix tokens per workload,8 idle intervals, invalid HTTP/binary reuse,
halfclose, RST after first token and inflight SIGTERM.
Each normally exits with13 accepted/closed,32 completed,3 aborted, all model
errors zero, pending/error/reserved/dropped/overflow/diagnostic overflow zero,
independent empty SQ/CQ and no remaining pins. These are finite dependency
qualifications, not a new research contribution or all-interleaving proof.

The frozen complete-output pools are byte-identical to the previous archive
and precede this experiment. They support finite set membership, not arbitrary
input/model parity. The stronger AMK eager-HF diagnostic failure from0048 remains:
the literal greeting/gen64 diverges at zero-based token16, reproduced in the
upstream path. Nothing in this queue experiment repairs or invalidates that
failure. The encoded-token HTTP API does not establish generic text/tokenizer,
arbitrary-length, arbitrary-model or production-serving acceptance.

## Actual policy, code growth and mediation

Production code diff is38 added/2 removed lines in one existing header; no
new Make target, worker, runtime setting, queue ABI or model arithmetic.
BF_IO_COALESCED alone receives local SQ snapshot/reservation cursors and
io_publish with retained system fence/release tail store. CQ processing
acquire-snapshots a finite tail and release-publishes consumed head after reads.
Both the stopping/cancel early return and ordinary terminal path flush queued
SQ work. Noncoalesced branches preserve the literal previous reservation and
CQ-processing policies. No concrete ownership/order/liveness defect was found
in source inspection or finite qualification.

This is collective publication/availability ordering: the snapshot can defer
newly available SQ capacity and newly arriving CQEs to another round. It is
not a pure instruction-count or PCIe-latency ablation. Read-only compiled
instruction inspection reproduces static_driver_instructions.json:
AMK dispatch2328→2216, vLLM dispatch3536→3432, shutdown io_network1432→1384.
io_initialize remains56 instructions but its instructions differ with the
coalesced ring layout. These static receipts establish changed compiled driver
code; they do not measure dynamic publications, PCIe traffic, occupancy or a
mediating latency mechanism. Model kernels outside this driver are not claimed
to have been optimized. The modest shared-driver code is justified by durable
ordering and finite batched publication, rather than new model-specific code.

## Host/order uncertainty and final decision

Host snapshots are12:18:33.155UTC before collection,12:20:21.288UTC during,
12:30:46.126UTC mid,12:41:45.787UTC after. Boot identity is unchanged.
All four selected kernel-journal observations contain the same33 historical
NVRM state0/status0x56 warnings, latest10:50:43UTC; no new selected Xid/OOM/
storage fault is shown. Do not call the journal clean or the warnings harmless.
During/mid GPU-app receipts each show one Python application in host PID
namespace; before/after show none. They are discrete observations, not a
continuous isolation or interference guarantee. Memory, GPU clocks/utilization
and shared-host state remain possible unobserved contributors.

Only five blocks and five of six deterministic path permutations were used.
The odd-block reversals mitigate but do not eliminate order/batching/cache/drift
effects; individual requests are not independent replication units. All
nominal interval and correctness scope caveats are material.

No validity defect requires rerunning this completed unchanged comparison.
The admitted supporting experiment adds credible local evidence: queue batching
helps AMK and Qwen long-output service, but it does not establish the intended
vLLM primary short-output latency recovery or a general native win. Preserve all
negative/uncertain effects in findings and evaluation. The full generic serving
and performance goal remains incomplete.

Reviewer is finished and explicitly releases
/tmp/bpfusion-queue-batch-2su5dvmy for owner-directed archival/cleanup.
