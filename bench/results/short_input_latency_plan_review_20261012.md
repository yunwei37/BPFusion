# Short-input latency plan review

Reviewed 2026-10-12 UTC in the original yunwei356/bpfusion-dev Workspace.
Source branch and revision observed: main,
9954855859fdc14b7f38dc2ec21768b4fc054f02.
Reviewer read the current plan, temporary diagnose.py and both generated
qwen_graph adapters, bench/resident_dispatch.py, executor/qwen_graph.cu,
bpf/include/bpfusion_queue.h, bpf/fusion.bpf.c, relevant TCP module fields,
the actual archived two-model case metadata and library symlinks.

## Judgment

Admit this dependency diagnosis. There is no scientific or executability
defect that blocks its proposed real preflight. It can determine where time
is spent in the current instrumented, single-client, short-input resident
path. It cannot numerically explain the historical unprofiled cross-node
mean by subtraction, establish a serving speedup, or complete the retained
performance goal. The plan states those boundaries correctly.

## Admission and hypothesis

Existing client-only finding 0029 cannot separate model execution from
service latency. The older CUPTI capture is a useful competing explanation,
but differs in source and profiling conditions. A fresh current-source trace
adds the causal localization missing from those data. Kernel-span dominance
and service-span dominance lead to different next work, so this is not an
unchanged throughput rerun or a positive control counted as a new paper
result. Its declared role is dependency; it should be folded into the next
same-compute performance investigation, not promoted to a standalone RQ.

## Native workload and correctness

The driver imports the production benchmark through runpy and uses its real
connect() and request(). TCP connection setup precedes request timing. The
native request body includes the prompt IDs and a monotonic timestamp, sends
a real HTTP request, validates status/content length and exact output IDs,
and records the receive timestamp of the first complete output token.
The four archived cases per model have input lengths 5, 8, 5 and 2.
Their expected outputs come from the earlier independent eager-HF oracle,
rather than this trace's executor output. Current source has no production
compute change relative to the completed matrix.

Each process receives four declared warmups and 16 measured requests through
one persistent connection. All 20 are traced. The plan deliberately does not
include an additional serving baseline: this is path localization, not a
superiority comparison. Repeating the model or requesting a broader baseline
would not be a prerequisite for this dependency question.

## Queue identity and ABI

The compiled layout helper uses sizeof/offsetof and BF_LLM_SLOTS from the
canonical queue header; the driver does not reproduce guessed offsets.
The observed size/slot offsets are consistent with that header.
BPF writes the wire client_ns and CLOCK_MONOTONIC ingress_ns before
publishing PENDING. Module recycling leaves those timestamp fields intact.

With exactly one sequential client, choosing the greatest client_ns after
the completed response identifies the latest request. The explicit
client_ns <= start <= ingress <= arrival check rejects accidentally choosing
the preceding request, because its ingress precedes the current start.
This reasoning depends on the promised absence of another request producer;
record concurrent-process observations and do not generalize this selector to
a multi-client diagnosis. Slot number also identifies the private graph bank.

The map lookup occurs after native request timing. It therefore does not
enter that request's TTFT, while its inter-request pacing can still influence
GPU/CPU clocks and must remain an interpretation limitation.

## Instrumentation and clock mapping

Both temporary adapters are identical, use the existing native qwen_graph.so
through explicit symlinks and leave model loading/capture and math unchanged.
CUPTI device-graph and HW tracing are enabled before CUDA context creation,
with actual status assertions. The installed torch profiler supplies the CPU
and CUDA activity timeline. Signal termination reaches the native serve
handler, allowing normal GPU stop, module unload and trace export.

Each anchor has a profiler annotation interval and bracketed monotonic
before/inside/after samples. Mapping must retain an interval of possible
offsets, check that beginning and ending constraints are mutually consistent,
and report resulting boundary uncertainty. A single point offset or
unqualified subtraction between raw clock domains would invalidate the
decomposition; the plan explicitly requires bounds and consistency.
Time-namespace observation supports the same-clock assumption but does not
replace these checks.

The graph catalogue covers every physical bank and the three actual prompt
lengths. Its node-type counts support checking real model-kernel activity
coverage; do not assume the old Qwen count applies to Smol or every prompt.
Exclude the named resident dispatch kernels and initialization activities.
Attribute kernels to the sequential request window only when the clock
bounds support that assignment. Missing, ambiguous or crossing-window
activity is uncertainty, not zero model cost. No source/model optimization is
needed to make the diagnostic answer favorable.

Kernel count, first-to-last span, interval union and gaps answer distinct
questions. Span includes scheduling gaps; union is elapsed active kernel
time, not device utilization or summed serial work. The post-model stage
contains sampling/publication, tail dispatch, kernel polling/TCP and client
receive. It must not be labeled pure network latency.

## Execution, completion and lifecycle

The actual command, current cached HF names, native 300-second serving
lifetime, 60-second socket/shutdown handling, output JSONL and gzip traces are
specified and present. Two processes are sequential. A nonzero child status
or exception preserves a failure event and partial raw prefix. Successful
completion needs both traces, all 40 actual replies including warmups,
normal executor exits, valid clock/activity coverage, counters and cleanup;
a small real preflight proves only the adapter executes.

The finally path closes its map FD, stops only the launched child if live,
detaches its hooks and removes its recorded pins. Before attach, ensure the
original serving owner/module/pins are not active; the review does not
authorize detaching another owner's state. Preserve the existing unrelated
tools/setup_env.sh.

## Optional polish

Record installed torch/CUDA/CUPTI/driver versions and the exact native
library build provenance in the raw receipt as the plan already promises.
Annotate any clock-bound width large enough to make a stage ordering or
dominance claim ambiguous. Neither item calls for additional models,
baselines, infrastructure, arithmetic changes or a new protocol.
