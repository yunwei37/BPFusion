# Short-input first-token latency result review

Independent reviewer: /root/cross_node_result_review, 2026-10-12 UTC.
The reviewer did not plan, implement, or collect this diagnosis. No desired
verdict was supplied. Only this report was written; no production source,
other document, or Git publication action was changed.

## Separate judgments

- Run status: valid and complete for the declared instrumented loopback diagnosis.
- Tested hypothesis: supported narrowly. The existing captured model-kernel
  execution region dominates measured short-input first-token latency under
  these profiling conditions.
- Research value: dependency-only. This selects the next performance
  investigation; it is not a separate paper result or contribution.
- Paper impact: current mechanism/workload boundary.
- Next paper decision: treat the reused computation path, including its many
  kernel operations and intervening gaps, as the leading local bottleneck.
  Prioritize qualifying an existing faster backend and comparing serving
  paths with that same backend. Do not conclude that eBPF creates the
  millisecond floor, or numerically explain historical cross-node latency
  by subtracting this profiled local run.

The retained throughput/latency goal remains open. This diagnosis establishes
neither an unprofiled serving speedup nor completion of the broader system.

## Reviewed evidence and completion

Read the plan and independent plan review, short_input_latency_20261012.jsonl,
both gzip Chrome traces, short_input_latency_stages_20261012.jsonl,
successful analysis and retained initial analysis failure. Inspected the
actual /tmp/bpfusion-short-input-latency-uhkfzipi/{diagnose.py,analyze.py,layout.c},
both temporary profiling adapters, original graph sources, native benchmark,
eager-HF oracle source, canonical queue header, and BPF timestamp assignment.

The observed source is main, 9954855859fdc14b7f38dc2ec21768b4fc054f02,
matching raw metadata. There is one completed process per model, twenty
actual sequential gen1 HTTP requests each, one connection each, indices
0..19 once, case=index mod4, first four requests declared warmups, and
sixteen measured requests per model. All forty request rows are retained.
The raw concludes with terminal exit0 and contains no failure event.
Both executor records exit0, report one host launch, twenty device model
graph launches, zero graph errors, eight banks, and max_active=1. Both
traces exist and their recorded export sizes match the archived artifacts.
No selected retry or undeclared exclusion was found.

Raw metadata archives the actual driver and profiling-adapter sources.
They match the temporary files inspected. The two model adapters are
identical, and their native-library symlinks resolve to the original
build/qwen_graph.so. A diff against production qwen_graph.py consists
of CUPTI setup, graph catalogue queries, clock anchors and profiler/export
around the original serve call. Model loading, captured forward computation,
precision, graph/KV layout and greedy selection remain unchanged.

The diagnosis imports native benchmark connect/request rather than
reimplementing the input/output path. The reused independent eager-HF
reference tokens are those archived for the completed cross-node run,
not this profiler's generated output. All forty returned first tokens
match their reference. All native TTFT/completion times reconstruct as
(first token arrival - client start), with tpot absent for gen1.
Four cases have input lengths5,8,5,2, so measured counts by length are
8,4,4 for lengths5,8,2 respectively, as reported. There is no serving
baseline in this diagnostic; the second model is another workload,
not a comparator establishing superiority.

## Queue identity and chronology

The layout helper uses canonical sizeof/offsetof and reports size17336,
LLM offset12856, slot size560, eight slots, client_ns offset24,
ingress_ns offset32 and state offset0. Independently executing the
existing helper reproduces raw metadata. The BPF stream source assigns
ingress_ns=bpf_ktime_get_ns() before publishing PENDING.

All forty rows satisfy client_ns <= native start <= BPF ingress <= first
arrival. Slot indices rotate as request index mod8. Request starts are
strictly after the previous completed reply. The single-client latest-
client_ns selector therefore identifies the current request here; it is
not a general concurrent-request selector. Queue reads happen after the
native measured reply and do not enter that request's TTFT, but their
inter-request pacing remains part of the instrumented conditions.

Stats report twenty publications, one linked socket, zero parser/sockhash
failures, no reserved slots, and all eight slots FREE for both models.
Attach/detach and normal shutdown are recorded. Successful command() calls
use check_output, so recorded empty GPU lists are successful endpoint reads
rather than silently ignored nonzero command statuses. They do not prove
continuous isolation.

## Clock mapping and the analysis correction

The two anchors per model contain monotonic before/inside/after samples
and one profiler annotation interval each. Let O=trace_ns-monotonic_ns,
B/E be the annotation beginning/end, and b/i/a the monotonic samples.
The observed ordering implies:

O >= max(B-i, E-a), and O <= min(B-b, E-i).

Independent reconstruction gives the same bounds as the analysis:

| Model | Begin-anchor interval, ns | End-anchor interval, ns | Intersection, ns |
|---|---|---|---|
| Smol | [711602000405209,711602000466229] | [711602000418219,711602000453426] | [711602000418219,711602000453426] |
| Qwen | [711602000420893,711602000466057] | [711602000418422,711602000453738] | [711602000420893,711602000453738] |

Intersections are nonempty. The analyzer uses their midpoint without
fitting an offset to request results. Half-widths are17.6035us and16.4225us.

The retained initial assertion demanded that even the earliest possible
mapped GPU beginning follow ingress. That would certify ordering for every
offset allowed by conservative calibration. Failure of that stronger
condition does not establish a causal violation or invalidate the trace:
the small ingress-to-GPU stage is unresolved inside the calibration width.

The corrected analyzer tests whether the independently calibrated interval
permits ingress-before-GPU and GPU-end-before-reply, while preserving signed
midpoint estimates and their common uncertainty. That correction is
appropriate for compatibility, not proof that the tiny stage is known
positive. It changes analysis validation; raw requests, trace, oracle,
timeout and workload were not changed. The initial failure remains visible.

I additionally checked a stronger condition than the corrected analyzer's
individual compatibility assertions: one common offset can satisfy all
twenty requests' causal boundaries simultaneously. Intersecting the anchor
interval with every [trace GPU end-client arrival, trace GPU begin-ingress]
constraint gives nonempty feasible intervals:
Smol [711602000418219,711602000437816]ns and
Qwen [711602000420893,711602000436872]ns.
These are review checks, not fitted offsets used to replace the reported
midpoint or narrow its displayed bounds.

Qwen indices7 and11 have midpoint ingress-to-GPU estimates -0.0105us and
-0.4435us. They are within the ±16.4225us anchor half-width and must remain
signed, unresolved estimates. Do not clip them to zero or report physical
negative queue latency. Smol's measured mean ingress-to-GPU4.565125us and
Qwen's2.688438us are also smaller than their calibration uncertainty.

These bounds calibrate CPU CLOCK_MONOTONIC to the profiler CPU axis.
The installed profiler supplies CUDA activities on its common timeline;
independent CUPTI GPU-to-common-axis synchronization error is not measured
by these two CPU brackets. Endpoint consistency also does not establish
absence of all clock drift between anchors. Accordingly, the small stages
should not be claimed as precise microsecond network/dispatch measurements.
The first-to-last GPU model span is offset-independent, and its dominance
does not depend on choosing a favorable clock offset.

## Activity coverage and attribution

CUPTI device-graph/HW setup statuses are zero in both logs. Source graph
catalogues cover all eight physical banks and the three prompt lengths.

Smol has1460 kernel nodes for length2 and1490 for lengths5/8; the trace
contains29650 non-dispatch model-kernel records over twenty requests.
Qwen has808 kernel nodes plus one memset node for each relevant graph;
the trace contains16160 model-kernel records plus all twenty corresponding
graph memset records. No expected kernel activity is missing.

Independent reconstruction groups every kernel into the twenty sequential
request executions using catalogue counts, chronological ordering, graph
identity and unique graph-node IDs. Each group has the full expected count,
one graph identity and the expected number of distinct kernel-node IDs.
No unused model records remain. Across the entire anchor offset interval,
each group's beginning is after the previous client reply and its end is
before the next client start. Thus adjacent requests cannot explain the
same recorded model group. Initialization copies/memsets and the twenty-one
resident dispatch kernel records per trace are excluded as planned.

Kernel-only interval union excludes Qwen's one internal memset per request,
whose mean duration is0.3904us. All of those memsets lie inside the recorded
model-kernel span. This tiny omission does not alter span dominance, but
kernel union is not a complete union of every GPU activity. Persistent
dispatcher activity is also excluded, so union is not device utilization.

Independently reproduced every per-request stage, summed kernel duration,
interval union, span and all aggregated means in successful analysis.
Integer-nanosecond reconstruction from serialized decimal timestamps agrees
with interval unions within0.00003ms; tiny sum/union discrepancies in stored
values arise from float timestamp arithmetic, not meaningful overlap claims.

Mean cumulative gaps within the first-to-last model-kernel region are
0.761876ms for Smol and0.414842ms for Qwen. Maximum individual gap in the
measured records is0.863892us for Smol and1.567993us for Qwen.
These are many small inter-kernel intervals, not a demonstrated millisecond
pause by the eBPF path. The trace does not isolate whether each gap arises
from graph scheduling, dependencies, instrumentation, or another cause.

## Recomputed measured results

The following are sixteen-request means after the four declared warmups.
Queue/post-model estimates use the independently anchored midpoint;
their stage uncertainty is shared and does not shrink by averaging.

| Model | Native TTFT, ms | Send→BPF ingress, ms | Ingress→first model kernel, ms | Model-kernel span, ms | Last model kernel→client, ms | Kernel interval union, ms | Span/TTFT |
|---|---:|---:|---:|---:|---:|---:|---:|
| Smol | 3.142528 | 0.012829 | 0.004565 | 3.000588 | 0.124545 | 2.238712 | 95.4833% |
| Qwen | 2.411959 | 0.016351 | 0.002688 | 2.211501 | 0.181419 | 1.796659 | 91.6890% |

Every row's four stages sum to its native TTFT. Span/TTFT ranges across the
sixteen requests are91.66–97.98% for Smol and86.53–95.40% for Qwen.
The result is not generated by assigning residual client latency to compute:
span and union come directly from independently covered GPU activity.

Across lengths2/5/8, Smol model spans are3.041962/2.994598/2.971194ms
and Qwen spans2.188481/2.216517/2.224490ms. Thus very short prompts still
invoke the full existing forward path and hundreds or thousands of kernel
operations. The data support dominance of that captured computation region.
They do not identify a pure arithmetic, memory-bandwidth or FLOP bottleneck.

The last-kernel-to-client stage includes tail dispatch, output publication,
kernel polling/TCP and client reception. The graph includes sampling
kernels, so it should not be casually described as excluding all sampling.
It is not a pure network or pure TX measurement and cannot rank the cost of
each component without more attribution.

## Scope, limitations and next decision

The raw records observed torch2.14.1, transformers5.19.0, kernel
7.3.0-070300rc3-generic, actual cached model references, zero time-namespace
offsets, and actual profiler/CUDA/CUPTI versions in the trace metadata.
Two processes, four prompts and sixteen measured sequential requests per
model provide localization, not population confidence intervals or a
general latency distribution.

Profiler overhead, device-graph tracing, bootstrap state, inter-request
map lookup/pacing, clocks and shared-device conditions can change the
measured durations. No matched unprofiled trace counterfactual exists.
The diagnosis does not numerically attribute the older approximately3ms
cross-node result, nor demonstrate a same-backend eBPF speedup. It also
does not address concurrent throughput, online batching, total CPU/energy,
broader models, long contexts or a full text serving API.

Review-time successful nvidia-smi finds no compute applications; own TX
module and three map pins are absent. Root owns the full lifecycle
restoration/publication audit. Unrelated tools/setup_env.sh is preserved.
The ordinary analyzer currently lives in OS-temp; root should retain its
actual source with the result for durable recomputation before temporary
apparatus cleanup, rather than preserving an unverifiable command alone.

The useful next action is to select a qualified reusable faster compute
backend or another justified same-compute discriminator. Preserve the
project's contribution in the request/control path, and do not turn this
diagnosis into an open-ended single-model arithmetic optimization campaign.
This dependency evidence changes where to investigate next; it is not a
new independent paper result or permission for persistent runtime changes.


## Restoration and driver-warning addendum

Reviewed the subsequently archived
short_input_latency_restoration_20261012.json and durable
short_input_latency_analysis_20261012.py. The restoration receipt records
successful journal observation for18:10:00–18:25:30UTC, both actual TX
lifecycles (18:12:40 and18:13:39UTC), and for each1,640bytes,
twenty completions, zero abandoned/retries, and one accepted/closed socket.
It records all three own process IDs absent, own module/pins absent,
successful empty GPU compute-app query, removal of the owned temporary
directory, preservation of tools/setup_env.sh, and the original Workspace
Pod UID Running/Ready with zero restarts at18:28UTC.

The actual analyzer is now durably retained as
bench/results/short_input_latency_analysis_20261012.py; the receipt records
a byte-identical copy before temporary-directory removal. This resolves
the preceding reproducibility recommendation. Driver and profiling-adapter
sources remain archived in raw metadata.

The same journal also records two NVRM GPU0
refcntRequestReference_IMPL warnings: "Failed to enter state 1
(current state: 0, status: 0x00000056)" at18:11:36 and18:12:48UTC.
Their relationship to capture, clocks, profiling or measured latency is
unknown. The completed token replies and covered GPU records do not prove
the warnings harmless. Do not call the window fault-free, assign them to
the measured bottleneck without evidence, or promote the observed spans
to a canonical latency floor for a healthy unprofiled GPU.

The verdict does not change: the observed diagnostic is complete and
valid for narrow localization under its recorded instrumented environment;
model-region dominance remains directly supported by its trace. The
warnings strengthen the existing limit on generalizing absolute timings
or attributing their cause. Research value remains dependency-only, with
no speedup or cross-node performance claim.
