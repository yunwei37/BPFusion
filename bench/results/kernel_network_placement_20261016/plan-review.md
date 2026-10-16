# Independent kernel-network placement plan review

2026-10-16 UTC. Fresh PLAN REVIEW under research-experiment-design. Read-only
for plan, sources and execution artifacts; only this report is written. No
build, BPF attachment, TCP service, GPU/model run or Git action was performed.

## First review: diagnostic verdict

The scientific comparison is admitted for the stated supporting intervention.
One concrete command-status correction is needed before using the documented
qualification command as successful terminal evidence: the outer
kernel_network_acceptance.py currently writes its exit JSON but always returns
process status0. Add raise SystemExit(0 if ok else 1) after that record. This
propagates the already-computed result; it changes no request, oracle, timeout,
counter assertion or analysis. Qualification failure must remain failure,
with the recorded original outcome retained.

No other blocking scientific or executability defect was found. This review
does not assume candidate speed, correctness or source adoption. Final ordinary
build/control snapshots and actual real preflight remain the planned execution
dependencies, rather than proof already supplied by verifier-only loading.

## Admission and evidence value

The retained objective and absence of a formal paper RQ are stated honestly.
I read docs/evaluation.md, docs/background-related-work.md, complete0076 result
and its independent result review, plus the kernel-owned engineering/build
checks. 0076 establishes a small instrumented association with material
perturbation, not a latency allocation. Its separate GPU-network CTA overlaps
model/dispatch. The current plan correctly does not add those durations or
claim to partition the old unreproduced6.36ms.

The proposed intervention has distinct decision value: replace GPU CQ/SQ,
connection and reply progression with CPU/kernel-owned registered state in the
existing BPF loop, while retaining the GPU computation/controller. No prior
valid dataset measures this constructor. A positive fixed primary supports
local avoidability; adverse/inconclusive evidence closes its performance case
and keeps0074. An application failure requires repair or an honestly incomplete
experiment, not dropping the case. That is a meaningful supporting test; merely
compiling or loading the object would remain dependency-only evidence.

A source audit confirms mixed CUDA differs from canonical source only in the
transport header include. The intervention nevertheless includes host-owned
buffers/token copies and removal of the GPU I/O CTA. It cannot isolate a single
fence, sleep, PCIe transfer or softirq mechanism. The plan preserves this scope.
Upstream Linux io_uring BPF and prior GPU I/O mechanisms are cited as prior work;
no first-system or universal kernel-networking novelty follows.

## Baseline and budget fairness

N is the credible efficient C++ epoll/timed-wait competing mechanism using the
same resident upstream-vLLM model computation. It must run successfully, not
lose through an avoidable interface failure. L is the selected0074 component
ablation, not an additional external baseline. The K/L/N matrix distinguishes
improvement over the current network placement from defeating the competing
userspace mechanism. Both contrasts are necessary and fairly matched in
checkpoint, precision, slot16, four prompts, output64, arrival schedule and
client handling.

The official vLLM0069 reference has a distinct whole-service role and real
frontend/KV/scheduler differences. Its existing evidence should remain cited;
no new official run or additional baseline is needed to admit this causal
mechanism comparison. Different batching/KV trajectories may still arise and
are an outcome of the scheduling/transport comparison, not equal-work
per-model-kernel timing.

## Primary, uncertainty and claim boundaries

The fixed primary K-minus-L client-delivered tokens/s is aligned with the
placement hypothesis. Five paired process blocks, predeclared orders and
nominal paired t95 df4 supply a clear uncertainty rule: interval above0 local
support, below0 contradiction, zero-crossing inconclusive. It is neither
equivalence nor an automatic general eBPF superiority claim. K-minus-N and
L-minus-N, all-attempt failures, conditional-success tails, scheduling lag,
CPU and energy remain disclosed. A K-minus-L win with native still better
would support only the local placement improvement.

The plan links official vLLM metric definitions and explicitly retains its
source-native token-ID/client-window differences. Client receive-gap timestamps
and zero gaps are not silently equated with official per-output ITL. Marginal
P99 values are not additive. Host/cgroup/group/device views remain nested or
shared and are not summed into exclusive total-service costs. No secondary
metric is used to rename the primary after observation.

## Executable path, checks and source binding

I inspected source/kernel_tcp_state.h, kernel_tcp.h, kernel_tcp.bpf.c,
vllm_mixed.cu and Makefile; the acceptance, protocol, ordinary lifecycle,
server, matrix, client, replay, resource observer and analysis scripts.
All inspected Python adapters parse. Source/Make receipts retain real
compile commands and build-directory binding. Earlier engineering histories
preserve the missing-object Make defect, verifier rejections and final8/16
verifier-only successes without calling them served correctness.

The protocol and ordinary lifecycle adapters were independently diffed against
their existing active-wait versions. Changes are candidate build/source paths
and artifact names; request/oracle/counter/network assertions remain intact.
Captured-graph/KV/history replay plus fresh upstream attention metadata checks
actual tokens, while sharing upstream arithmetic and finite observed
trajectories. They do not prove eager-HF or general-model fidelity. Default8
Qwen/Smol qualification, partial stop/backlog/reset/reuse and ordinary teardown
are a reasonable finite constructor check; no wider coverage is demanded here.

The private host RESULT interface now matches the unchanged qualification
parser before serving. Its final normal rebuild and compiled comparisons are
explicitly still required. The planned SASS check establishes unchanged emitted
GPU dispatch; the old-loop ablation still legitimately contains io_network.
Final source and actual object/library bindings should be recorded, rather
than treating an artifact-only main HEAD or an old successful Make exit as
the serving-binary identity.

Ordinary performance deliberately has weaker frozen-reference pool flags.
The plan correctly retains flags and separates traced finite qualification
from untraced performance; it does not claim exact full-run output fidelity.
No request/oracle/timeout/metric change during the matrix is allowed. The
outer qualification-status propagation described above is the only requested
execution correction and is safe before real qualification/preflight.

## Matrix completion and cleanup

The prepared PowerShell driver selects exactly candidate/before/native paths,
three preflight identities and fifteen full identities; analyzer assertions
reject a partial prefix. Full offered192/s60s plus drain retains all11520
attempts/cell and failures/partial tokens. Warmup checks, unchanged offsets,
5s idle context, resource bracketing, server exit0/no-pins receipts, deferred
archival and full CPU replay are consistent with the plan. Candidate host
finish additionally checks pending/error/drop/overflow and SQ/CQ balance.

The bounded remote client must use its actual Job/Pod UID, and final cleanup
must confirm absence and preserve the original Workspace/PIDs/foreign WIP.
Server exit alone is not client cleanup or scientific completion. Fresh
RESULT REVIEW is still required after the complete fixed acquisition and
analysis, including adverse outcomes. No extra baseline, broader workload,
increased repetition count, unchanged rerun or persistent helper is needed
for this plan.

One first review is recorded here; at most two substantive follow-ups remain.

## First follow-up: execution correction closed

The TEMP and archived kernel_network_acceptance.py are byte-identical, parse
successfully, and now end with raise SystemExit(0 if ok else 1), immediately
after the unchanged computed-result JSON. The reported command-status defect
is closed without changing the request/oracle/timeout/metric contract.

Final compiled_controls.json records matching capacity8/16 ordinary dispatch
streams for K/L/N (1464 instructions each), matching K/native traced streams
(1656 each), no candidate io_network and the expected old-loop io_network.
Normal final host rebuild receipts retain the RESULT interface change.
These are build/control dependencies; no application or performance success
is inferred from them.

Current verdict: **admitted; no remaining blocking defect found** for the
declared finite qualification, real three-condition preflight and fixed
fifteen-cell ordinary matrix. All interpretation and completion boundaries
in the first review remain. One first review and one substantive follow-up
have been used; an unchanged-plan rereview is unnecessary.
