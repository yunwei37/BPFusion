# Batched result publication in the existing vLLM dispatcher

Current serving source/main ea82f18b703732288b6a38a235cbc978daf4bc23.
Retained user question: remove steady userspace request handling while reusing
real GPU model computation, and improve delivered latency/throughput with
matched controls. No formal paper RQ/thesis/idea-story exists; do not invent one.

## Admission and scope

Supporting experiment. The largest credible result is a portable-to-the-tested-
backends reduction in shared-output publication overhead without changing model
arithmetic; it is not new eBPF/GPU I/O novelty. The strongest reject argument is
that removing a CPU worker merely moves coordination cost onto the GPU.
Current code executes one __threadfence_system per output row in each model
batch before publishing produced. A single thread writes all rows. A single
system fence after all payload writes and before any produced write can enforce
the same payload-before-availability order. DONE/recycle fencing stays unchanged.
CUDA memory-fence semantics:
https://docs.nvidia.com/cuda/archive/13.0.3/cuda-c-programming-guide/index.html#memory-fence-functions

Expected candidate improvement is uncertain and likely bounded: model kernels
dominate much of the observed time. Additional loop bookkeeping or deferred
publication may offset fewer fences, especially c1/short output. Contradiction
is a nonpositive or adverse client effect despite valid ordering. Do not infer
physical PCIe/fence latency from source counts.

Prior0051/0056 batch io_uring SQ/CQ publications; they do not alter output-row
system fences.0057 cannot substitute: it keeps the original publisher and its
integrated Smol timing fails.0036 changes graph launch topology, a different
intervention. Reuse their pinned runtime, clients, frozen reference pools and
strict protocol/lifecycle checks rather than duplicate instrumentation.
Best alternatives are offered-load/full CPU evaluation or another backend;
those expand service evidence but do not decide this concrete redundant-
synchronization candidate. Repairing0057 alone still cannot choose a publisher.
This is a small implementation selection experiment, not a headline contribution.

The change may touch only vllm_graph.cu's existing batched token publisher;
it must not touch model math, Python/bootstrap/replay oracle, BPF/network/ABI,
DONE/recycle ownership, timer, residency, public flags or runtime defaults.
No persistent mode/flag/target/helper is added. Private original/candidate builds
use existing Make rules. Both transport constructors receive the same candidate.
If no supported primary gain, restore saved original file byte-for-byte before
publication; archive candidate as evidence, add zero production-code growth.
This is restoration of an uncommitted candidate, never reverting a commit.

## Conditions and baselines

Four matched conditions: original-loop, candidate-loop, original-native,
candidate-native. Efficient timed-epoll/native TCP is the sole main competitor;
original-loop is the component control. Native candidate provides a matched
publication-policy transport comparison and bounds generic applicability.
Same pinned Qwen2.5-0.5B-Instruct/SmolLM2-135M FP16 weights/runtime/KV/graph,
padding/prefix-release, prompt/output budgets, preopened TCP, no BF_TRACE or
profiler in performance. Original source is saved before edit; private build
flags differ solely by this publisher source. No clock/power/CPU tuning.

Primary: candidate-minus-original gen64/c8 output TPS on loop, independently
for each model. Positive nominal paired t95df4 interval supports a local gain;
zero-crossing is inconclusive; negative is adverse. Both models need their own
reported decision. Candidate-native difference is a matched competitor result,
not a condition for claiming a component-local gain. Latency/other cells are
signed secondary boundaries, not a search for an alternative winning primary.
Correctness failure invalidates the candidate even if throughput improves.
Only supported model-specific finite gain could justify retaining the shared
change after considering adverse secondary behavior; no universal promotion.

## Real workloads and frozen correctness

Reuse source-native bench/vllm_serving.py client/protocol/analyzer and its
existing untraced pre-observation whole-sequence contract. Temporary adapter
changes paths/condition labels/ordering and exact process coverage only, not
request parsing, token checks, timing formulas, timeouts, metric or oracle.
Use already-frozen0056 reference pools; never add current outputs to them.

Preflight: actual Qwen, all4 conditions, all4 gen1/64 byc1/8 cells,8 requests
per cell plus8 checked sequentialgen1warmups per process; 128measured requests/
4160tokens+32warmups. At most3 actual preflight attempts; keep failures.

Candidate strict qualification: both models, candidate-loop/native, original
source-native full622-request real protocol with exact graph/KV/history replay,
all-thread syscall checks and queue/slot shutdown checks. No profiler, so
in-process replay's earlier CUPTI-associated crash context is absent, but
record any real failure rather than weaken the check.
Frozen ordinary performance is weaker finite-set membership; it does not
establish eager-HF equality, current unobserved histories or task quality.
Earlier AMK eager-HF failure remains failed.

Use existing lifecycle suite for candidate loop/native for both models:
idle/reuse, reset after token, rejection, stop during generation/receive/accept,
complete-or-prefix semantics and actual raw post-stop bytes. Preserve original
native interrupted31/32 and ordered ownership criteria, no invented full-
retirement requirement. Check original default module compatibility only if a
shared publisher is selected; no module default is changed by this plan.

Full: two models x5 paired process blocks x4 conditions x4 cells;
32measured requests/cell plus8 checkedgen1warmups/process.
40executors/160cells,5120measured requests166400tokens+320warmups.
Use rotated condition order by block and rotate cell order as existing driver.
All admitted cells finish; no exclusion/favorable replacement. Bootstrap,
capture/connect/warmups outside client timer. No extra profiler/timeline layer.

TPS=output tokens/(last token arrival-first request send); TTFT,TPOT/completion,
p50/p99 and process/known-worker CPU are source-native diagnostics.
Metrics follow official terminology:
https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics
These are finite closed-loop token-ID HTTP cells, not offered-load/SLO/text
capacity or total service CPU/energy. Five paired process blocks are replicates;
requests are not independent process samples. Nominal t95df4, no familywise or
equivalence claim. Keep all signed rows/outliers.

## Execution, completion and interpretation

Create only owned OS TEMP inside original Workspace. setup.py creates the
common pinned temporary vLLM0.31/Torch2.13cu129/Transformers5.17 runtime/private
libbpf1.6.3 and builds frozen original before candidate using source-native
make. No base packages/shared original builds touched. Main source remains
dirty only in the candidate publisher until selection.

Runnable paths: python3 TEMP/setup.py; TEMP/runtime/bin/python
TEMP/serving.py --model MODEL --loop-comparison --preflight --untraced --reference-path
TEMP/frozen_references.json --output TEMP/preflight_MODEL.jsonl;
same without --preflight for full; --correctness without --untraced for
candidate protocol. Source-native analysis plus a small paired-summary adapter
reconstructs all client metrics. Expanded actual commands are retained.
Lifecycle source-native adapter and actual commands must be frozen before its
run and full performance. No project-authored control schema or gate API.

Keep entry/before/actual-midpoint/after host observations of boot,GPU apps,
current power, selected warning/fault journal. They are sparse observations,
never continuous isolation or proof warnings harmless. Check live process
handles during long runs and record real terminal exits; no observation-
timeout restart. Wrapper run logs remain in TEMP.
Expected cost roughly1–2GPUhours including repeated graph bootstrap; estimate
is not a deadline or new stop rule.

Complete means setup/preflight, candidate correctness/lifecycle, entire full
matrix, unchanged fixed analysis, one fresh independent result review, source
selection, owned TEMP cleanup, preserved source/build/base/Coder checks and
archive replay. Every failed/inconclusive row remains. Real defect repairs
are recorded and affected comparisons rerun under a revised plan, never relaxed.
Result review independently checks completion/fairness/all metrics/oracle and
code growth/scope, with separate validity/hypothesis/value/impact decisions.

Positive: consider retaining this small shared publisher for the measured
scope; any backend-general or eBPF-exclusive speedup remains unproved.
Negative/inconclusive: restore original, close unchanged candidate, prioritize
stronger service evidence or a distinct causal mechanism. No timer/copy sweep
or unchanged0057 rerun follows automatically. Full user objective stays active.

Actual orchestration: python3 TEMP/run.py preflight|qualification|lifecycle|full.
All serving commands include existing --loop-comparison, enabling unchanged
worker tasks/CPU brackets and cell-order collection; explicit publication
labels replace its old three-mode list. Per-driver fixed analysis runs after
collection. Lifecycle analysis: python3 TEMP/analysis_lifecycle.py TEMP.
