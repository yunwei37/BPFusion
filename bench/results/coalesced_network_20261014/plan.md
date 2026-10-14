# Coalesced GPU networking with unchanged reusable model computation

## Retained question and admission
Retain finding0030's question and user objective: can the CPU request path be
removed while retaining efficient reusable real-model GPU execution?
Finding0049 established a concrete non-network residency control sufficient
to reproduce AMK c8 loss, but did not establish overlap mediation or the exact
cause of actual I/O loss. It cannot establish whether a real driver that removes
independent steady GPU network residency recovers performance safely.
This supporting implementation experiment changes a model-independent driver
decision and outranks another unchanged timing/occupancy/profile sweep or model
arithmetic optimization. No formal RQ or central thesis is rewritten.

Hypothesis: advancing existing asynchronous network work from the existing
GPU model dispatcher between model-graph rounds can remove the tested AMK c8
loss while preserving correct worker-free TCP service and efficient current
vLLM delivery. Positive recovery without vLLM regression supports a common
driver path; AMK recovery with vLLM regression bounds the constructor and blocks
a universal default; no recovery directs investigation away from this proposed
intervention. Failures/unsupported collection remain failures/inconclusive.
The concrete network-state/launch implementation changes collectively; this
is not a pure one-variable SM-occupancy intervention or proof of0049's mediator.

## Implementation and independent evidence
Use original bpfusion-dev/main RTX5090/170SMs and same pinned checkpoints/runtime
as0048/0049. Keep AMK884534c4 upstream VM/math, cpasync0, private banks and K=1;
keep optimized upstream vLLM0.31 computation, packing/prefix release/KV policy.
Existing kernel eBPF parser/io_uring producer, protocol/page ABI and timeout
values are unchanged. Preserve old eager-HF discrepancy and fixed0045 output
pools; do not expand references or promote finite set membership to all-input
parity or current trajectory correctness.

Proposed shared io_uring header factors existing network progress into a
single-thread device step with durable GPU connection/request state. The
coalesced path calls this from the model dispatcher around result publication,
admission and model-graph launch. No independent steady io_network is launched.
At bootstrap initialize durable state; after model root stream quiesces at
shutdown, reuse that same state in the existing network drain worker so native
model-quiesced/deferred-task/cancellation lifecycle remains available.
Same source-native interface/model bootstraps remain; no CPU request worker,
new service/scheduler/permission/driver/clock/cache policy is introduced.
Source-native optional benchmark targets select the intervention. Record every
necessary implementation deviation and its collective scope.

Preserve source-native original-loop baselines from the actual pre-edit main
sources/builds in the same Workspace. They are credible current-practice
component controls, not frozen broken implementations. Efficient native epoll
TCP with the same model backend is the single strongest competing mechanism.
Candidate is real coalesced eBPF/io_uring. Native compilation excludes network
code; verify unchanged model/dispatch computation where feasible. Original
loop and candidate share the same eBPF source, model and protocol policy;
network state allocation/launch/parent work can differ and must be stated.

## Workloads, metrics and cost
Three real backend/model workloads: AMK Smol135M, optimized vLLM Smol135M and
optimized vLLM Qwen0.5B. Three paths each (native, original loop, coalesced).
Five paired process blocks/path/model, four cells gen1/64 atc1/c8,
32 measured requests/cell and8 excluded checked gen1 warmups/executor.
Total45 executors/180 cells/5760 measured requests/187200 output tokens plus
360 checked excluded warmups. This remains finite persistent-connection
localhost serving, not capacity, tail/SLO, arbitrary text or total CPU/energy.
Counterbalance five path permutations; alternate cell order and model order.
Do not claim randomization or isolation.

Primary effect: AMK Smol gen64/c8 candidate-minus-original-loop output TPS and
candidate-minus-efficient-native TPS/latency at the same cells. Current vLLM
delivery comparisons are independent backend-transfer/regression evidence,
not a definitionally weak competitor. Retain all paired per-block effects and
nominal t95 df4; no arbitrary percentage/noninferiority cutoff, zero-overhead/
equivalence assertion or cherry-picked successful path. Mixed tradeoffs remain
mixed. Ordinary client metrics determine effects; correctness, mechanism and
fairness are validity conditions rather than performance-defined oracles.

TTFT=first token arrival-request send; completion=last token arrival-send;
TPOT=(completion-TTFT)/(gen-1); output TPS=measured tokens/(last token
arrival-first send), using source-native resident_dispatch/matched serving
client. Latency terminology: official vLLM benchmark documentation
https://docs.vllm.ai/en/stable/benchmarking/cli/
The finite cell window is the existing local sampling convention.

## Qualification, mechanism and real preflight
Source-native strict/protocol/lifecycle controls are necessary integrated
qualification, not independent paper results. Candidate must exercise real
TCP fragmentation, binary/HTTP invalid and valid requests, c1..8, wrap/mixed/
pipeline/halfclose, RST/reuse, idle and inflight stop with independent fixed
output pools and existing queue/ownership/graph checks. Preserve stronger old
eager-HF failure explicitly; do not change its oracle to pass.
Use source-native vllm_serving/resident_qwen paths and earlier qualified
adaptations, changing launcher/control names only as needed.

Validate no steady userspace accept/recv/send worker using existing strace
protocol procedure and io_uring kernel-loop engagement/queue draining.
Use standard CUPTI/Torch observation only as a bounded mechanism check that
coalesced executors have no independent network kernel during model execution,
and retain actual API/launch/geometry/activity receipts. Do not claim graph
node identity, bank/position or model-overlap mediation from0049's unsupported
mapping; observation counts alone do not establish model trajectory.
The smallest actual end-to-end preflight includes allthree paths/backends and
ordinary client metrics. At most three real preflight attempts under the skill;
failed/partial data retained, no toy fallback or relaxed reference.

## Execution, review, restoration
Fresh plan review then real preflight/qualification; freeze validated main
source and exact source-native make/run/client/analysis commands before full
collection. Complete all45 actual executors to terminal status, preserve raw
outputs/timestamps/counters/CPU brackets (known-worker only), failures and
necessary deviations. One fresh independent result review audits the completed
matrix against this plan and recomputes metrics/oracles/baseline engagement.
One plan/report home; no project promotion/control schema.

Bracket actual host journal/GPU/memory/boot, retain NVRM warnings and faults
without harmlessness or isolation claims. Preserve original Workspace/PVC/
Coder/base/default HF library/WIP and other owners; remove only owned TEMP/
named test builds after review. Commit/push validated own work directly main
and verify public artifacts. Keep full goal active unless all original generic
serving/performance requirements are actually proved.

## Materialized metrics, order and command
Primary driver recovery is AMKSmol gen64/c8 TPS candidate-minus-original.
The efficient native comparison reports the remaining gap in TPS and
gen64/c8 completion/TTFT. Primary latency is gen1/c1 TTFT for each workload;
vLLMSmol/Qwen candidate-minus-original and candidate-minus-native gen1/c1
TTFT and gen64/c8 TPS are labeled backend-transfer comparisons. All other
cells/metrics are secondary. Report each paired contrast and interval without
equivalence or a single manufactured overall winner; partial recovery remains
partial, unresolved regression is not proven non-regression.
The actual driver now uses five of six permutations, residual order/drift
uncontrolled; cell and model order reverse on odd blocks. Exact ordinary full
command is runtime/bin/python run.py full, with each15 source-native driver
invocations/actual environments archived before full. Original binary names
are *_uring_loop_original with saved actual pre-edit source and build receipt.
