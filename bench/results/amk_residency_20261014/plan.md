# AMK driver residency and model-overlap discriminator

## Retained question and admission
Keep the user's performance/reuse objective and finding0030's latency question:
can the CPU request path be removed while retaining efficient reusable real-model
GPU execution? No formal RQ is invented or changed. This is supporting evidence
for a driver/backend resource boundary, not another model optimization campaign.

Finding0048's complete matched run loses at gen64/c8: loop158.094 versus
same-AMK native303.377 tokens/s, while c1 is164.204 versus165.099. Those finite
results and failed eager-HF exact diagnostic remain unchanged. They do not
identify whether additional resident GPU work, actual I/O processing, model
overlap or TCP progress explains c8 loss. Reanalysis cannot reconstruct absent
kernel timelines or the residency counterfactual. Static REG/shared-memory
data does not settle co-residency. This experiment outranks an unqualified
new backend port or an unchanged timer/CQ repeat because it can select a
model-independent driver repair.

Hypothesis: the implemented additional resident GPU work can suppress
cooperative AMK model overlap and is sufficient to reproduce the c8 loss
without handling network traffic. Positive counterfactual plus matched
model-overlap evidence directs work toward GPU residency/scheduling. An
unaffected residency control narrows attention to actual network work/progress,
and a profiled slowdown without changed overlap suggests per-kernel execution
rather than overlap. Mixed or instrumentation-sensitive outcomes bound the
constructor without proving a cause. No result changes the central claim or
requires model arithmetic edits.

## Sources and real-system reuse
Use original bpfusion-dev/main, actualRTX5090/170SMs, cachedSmol135M FP16
revision93efa2f097d58c2a74874c7e644dbc9b0cee75a2, AMK884534c4 and the same
Torch2.13+cu129/Transformers5.17/vLLM0.31 temporary package set as0048.
Reuse unmodified AMK VM/math, amk_graph.py/builder, qwen_graph.cu,
userspace_tcp.h, io_uring_tcp.h and source-native resident_dispatch client.

NVIDIA cooperative launch requires co-resident grids; platform/API permission
does not establish simultaneous execution:
https://docs.nvidia.com/cuda/cuda-programming-guide/05-appendices/device-callable-apis.html
Use standard concurrent-kernel activity tracing, not serialized kernel tracing:
https://docs.nvidia.com/cupti/12.9.1/main/main.html
Retain activity graph/node IDs and cooperative launch/geometry metadata:
https://docs.nvidia.com/cupti/api/structCUpti__ActivityKernel8.html
https://docs.nvidia.com/cupti/api/group__CUPTI__ACTIVITY__API.html
Device-graph/HES setup reuses0047's successful standard profiler adapter;
ordinary/profiled matched delivery controls test transfer. Prior NVRM warnings
and their unproved purpose/harmlessness remain visible.

## Conditions and scientific roles
One credible alternative mechanism/control is efficient native TCP with the
same resident AMK graphs. Candidate is current AMK eBPF/io_uring loop, whose
separate io_network GPU kernel is actually launched<<<1,1>>> on a nonblocking
default-priority stream. Model cubin/program/graph/private-bank policy stays
identical between conditions.

The residency ablation adds one low-activity, non-network GPU CTA to native
TCP on a nonblocking default-priority stream, one block/one thread as the
actual I/O launch. It polls the existing mapped stop field with system acquire,
sleeping1000ns between polls, and exits on the existing stop before CUDA
quiescence/page free. This is an explicit test-local null/resource control,
not a baseline, real TCP handler, fake model, traffic generator, or purported
bit-identical resource footprint: registers/local traffic differ from
io_network and must be reported. A positive effect establishes sufficiency
of this specific resident control collectively, not SM occupancy alone.

Keep this small CUDA control outside production source in owned TEMP, with a
source-native make target and unchanged original dispatcher/model/transport
code apart from its launch/teardown hook. No new runtime service/helper,
permission, scheduler, exclusive GPU slot, driver/cache/clock change or
raw AMK arithmetic patch.

Each of three conditions runs ordinary and standard profiled variants. Only
profiling setup/collection differs within an instrumentation pair. Enable
concurrent/HES/device-graph activities before CUDA initialization using the
existing official interface. Do not silently accept serial traces, missing
kernel events or an unsupported CPU fallback.

## Workload and complete matrix
Three paths x ordinary/profiled x five paired process blocks =30 executors.
Each executor:8 excluded checkedgen1 warmups; two cellsgen64/c1 andgen64/c8,
8 actual requests/cell, the same four literal prompts, source-native pre-opened
persistent connections and client timing/CPU brackets. Cell order alternates;
path order uses the first five permutations; ordinary/profile order reverses
by block.480 measured requests/30720 measured tokens plus240 checked warmups.
The smaller count is sufficient for a measured overlap/counterfactual
discriminator, not a representative-tail, capacity or SLO claim.

Use unchanged pre-observation0045 independent complete-output pools. Keep the
stronger eager-HF diagnostic failed; no expansion or current-history claim.
Every output, admission/reclamation, independent SQ/CQ emptiness, CUDA/model
error vector and owned cleanup must pass before interpretation. Data includes
all negative/failed rows with reasons.

Primary counterfactual effect is ordinary gen64/c8 throughput difference
(native+resident control versus native), five PROCESS-block paired differences
with nominal t95df4. Report loop-versus-native as engagement/replication, not
replace0048 with a favorable repeat. Model-overlap diagnostics use actual
amk_megakernel_persist intervals: max concurrent model executions, sum-duration
over occupied union, per-model durations and full model-region span. These
standard activity/timeline quantities are not new composite scores.

## Trace and correctness proof
Capture real graph/node catalogue and cooperative/launch geometry using
official CUDA/CUPTI metadata; map all model kernel records to actual private
bank/prefill/decode nodes. Include warmups in total coverage, exclude them from
measured metrics. Expected model calls derive from real inputs:
prompt_length+gen-1 per request. Model intervals are GPU-clock differences;
do not label TTFT-minus-model-span pure network latency or infer an
independent GPU/CPU bias. Validate per-bank graph/position sequences and
cell boundaries, not mere kernel count. Retain helper/dispatch/network/park
activities separately.

Measure ordinary/profiled throughput and completion differences per path/cell.
If instrumentation changes concurrency or delivery enough to undermine
transfer, ordinary mechanism interpretation is inconclusive. No arbitrary
overhead cutoff or equivalence claim. If standard tracing cannot observe these
cooperative device graphs, preserve the failure and close the timeline claim;
do not synthesize activity or substitute toy-model evidence.

## Actual invocation and completion
Owned TEMP=/tmp/bpfusion-amk-residency-tkdf_2wx.
Archive=bench/results/amk_residency_20261014.
Actual source-native build/server/client/profile adapters and one full command
will be archived before full collection; these are necessary experiment
artifacts, not a project control/promotion interface. Complete all30 executors,
both cells and unrelaxed references; freeze main source before full run,
retain raw replies/traces/commands/actual exits, and get one fresh result review.
A preflight must exercise all three paths and actual profile collection.

## Decision and restoration
This can add a driver/backend concurrency boundary, not arbitrary eBPF/model
superiority or direct thesis challenge. No hidden model-specific performance
tuning or unchanged sweep follows. A source-backed driver change is considered
only after the measured discriminator and its review.

Bracket execution with actual host journal/GPU/memory observations, preserve
historical warnings and any new genuine fault. Restore/remove only owned TEMP
and named test builds after review; preserve default HF library inode/size,
base packages, original Coder/PVC/cache, unrelated tools/setup_env.sh and other
owners. Publish honest finding/evaluation on main; the full objective remains
active.

## Metric definitions
Client TTFT = first token arrival minus request send; completion = final token
arrival minus request send; TPOT = (completion minus TTFT)/(output count-1).
Finite-cell output throughput = total measured output tokens divided by
(last measured token arrival minus first measured request send).
The latency terms follow [official vLLM benchmark terminology](https://docs.vllm.ai/en/stable/benchmarking/cli/);
the finite-cell sampling window is the existing local source-native convention.
