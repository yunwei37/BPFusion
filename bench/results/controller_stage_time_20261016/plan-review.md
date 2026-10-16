# Independent controller-stage plan review

Reviewed 2026-10-16 UTC against main29417807dc27e9b5f0b99e4a47a6fff68e38e8e9.
Fresh reviewer; initial review, no follow-up used. Only this report is written.
No GPU work, build, experiment, source edit or Git mutation was performed.

## Verdict

**Revise before execution: one scientific/mechanism-engagement blocker.**
The source-neutral timing approach has useful supporting value, and its
retained same-compute objective is appropriate. Its present description,
however, measures an inline I/O stage that is not part of the ordinary
selected mixed constructor. This is a concrete invalid-result risk, not a
request for another baseline, model, tuning sweep or ideal profiler.

## Blocking source fact

Makefile244-248 builds vllm_mixed_uring_loop with BF_URING_NETWORK and
BF_URING_BPF_LOOP, BF_PAD_PREFILL and BF_PREFIX_RELEASE. It does not define
BF_IO_COALESCED or BF_CHAINED_DISPATCH. The real archived
active_wait_source_build16.stdout confirms the expanded nvcc command, including
-dc and the absence of both flags. The same current source and build path
underlie0074 and0075; environment.json contains no CPPFLAGS/MAKEFLAGS override.
A source-tree search finds no definition that changes this fact.

Thus executor/vllm_mixed.cu105-113, including io_progress(io_state), is
preprocessed out. executor/io_uring_tcp.h566-572 instead launches a separate
io_network<<<1,1,0,net->stream>>> with a nonblocking stream; its single active
thread repeatedly calls io_progress at383-385. The graph dispatcher launches
model work using fire-and-forget plus a tail-launch continuation at173-183.
This differs from the plan's stated inline, model-critical-path mechanism.

The current fixed primary includes an inline I/O bracket that cannot engage
on the ordinary constructor. Adding BF_IO_COALESCED to make it engage would
change the constructor, defeating the ordinary-versus-instrumented comparison.
Do not solve this by enabling that flag or silently changing the hypothesis.

A valid repair can keep the same broad localization purpose while stating the
actual two independent GPU control contexts. Time dispatch publication/packing/
launch and its outside-dispatch interval, and separately observe actual
io_network/io_progress, including its existing sleep. Explicitly state that
I/O CTA durations overlap model/dispatcher work and cannot be added to
dispatch time or allocated as exclusive request latency. Choose/freeze the
resulting primary and interpretation before collection; no existing result
is being reinterpreted. An inline-constructor comparison instead would need
an explicit different hypothesis and controls.

## Admission and independent evidence

The remaining roughly20tokens/s native advantage at192/s is real matched
evidence in0074/0075, while blind peer caching did not establish a benefit.
Existing per-process graph-round counts cannot supply stage durations:
native can execute more rounds and remain faster.0057 precedes current packed
mixed execution, and its integrated CUPTI decomposition remains invalid on
two cells; its complete Qwen subset does not settle this current constructor.
0066 gives token-associated publication/submission/client timing rather than
current GPU dispatch/network-CTA residence. Source-native brackets therefore
can add previously absent observations and distinguish a plausible next
intervention from another speculative cache. They are supporting localization,
not a direct ordinary-serving speedup or proof that the historical6.36ms is
recovered. The no-material-difference/large-perturbation outcomes must retain
their narrow scope instead of concluding that GPU I/O has no cost.

A current matched CUPTI timeline is a credible alternative; this proposal can
outrank it for narrower stage residence because it avoids missing child-activity
grouping. Neither success nor failure should trigger an unchanged rerun,
larger N or automatic sleep deletion. Stage timing association cannot establish
avoidability or occupancy/PCIe/model-kernel causation.

## Baselines and fairness

The efficient C++ native epoll path with identical mixed model execution is
the credible main competitor. The ordinary/instrumented cells are observation
ablation controls, not additional competitors. Existing official vLLM0069 is
properly retained as a whole-service reference; rerunning it cannot identify
an internal stage on this constructor. One model and one offered load suffice
for this local question; additional models, loads or external implementations
are not admission requirements.

Five paired blocks, identical frozen schedules within block, explicit orders,
one process at a time and no profiler during serving are suitable for the
planned nominal paired interval. Residual order/shared-host interference must
remain a limitation. Instrumentation and BF_TRACE cost differ by actual work
and trajectory; applying them to both paths does not establish equal overhead.
The four conditions correctly allow reporting this combined perturbation.
Large or sign-changing perturbation prevents translating a traced association
into ordinary-serving explanation, even if the diagnostic itself is readable.

## Clock, counter and implementation checks

The official PTX globaltimer documentation describes a64-bit nanosecond
register and explicitly target-specific/tool-oriented semantics:
https://docs.nvidia.com/cuda/parallel-thread-execution/#special-registers-globaltimer-globaltimer-lo-globaltimer-hi
The planned single GPU clock domain is appropriate on the recorded RTX5090;
no host-clock subtraction, synthetic1000ns sleep charge, summed marginal
P99 decomposition or exact execution-instruction cost follows.

The eventual prepared implementation must preserve the measured source
boundaries. Use ordered/volatile timer reads with compiler memory barriers as
needed and inspect generated PTX/SASS around the bracketed sections. Do not
add synchronization that changes the serving memory protocol merely to make a
time bracket look exact. A graph-launch API bracket measures launch-call
residence, not completion of launched child kernels. Previous launch-call end
to next dispatch entry includes child execution, scheduling, previous CTA
return and any unbracketed code; call it outside-dispatch interval rather than
pure model time. Any counter bookkeeping after a timestamp belongs to the
unbracketed part.

Keep launching, nonlaunching/idle and terminal iterations separate; do not
silently amortize all busy idle loops onto tokens or drop them. Preserve
early-return/error/continue paths in count identities. Whole-process counters
include startup, warmups and idle/shutdown as planned, whereas client metric
denominators exclude warmups. Report the actual count scope and never subtract
an assumed fixed internal warmup budget. Histogram/launch/client joins and
nonnegative timing checks are worthwhile dependency acceptance, not new
scientific findings. New private network-CTA counters should remain device
local rather than add per-iteration writes to the mapped host stats, which
would itself change the data path.

## Metrics, execution and correctness

The official vLLM metric source supports client TTFT, TPOT and streamed-output
ITL terminology:
https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics
Keep this project's actual token receive-gap formula and measurement endpoints
explicit, since coalesced output observations are not device generation times.
The stage-time primary is an explicitly custom diagnostic, not a standard
end-to-end metric or a headline score. The plan properly keeps all-attempt
failure/scheduling lag and full terminal drain.

The frozen4-condition128-request preflight and5x4 full matrix are executable
in principle using existing runtime/client/schedules. Exact scripts are still
being prepared, so this is not a claim to have audited unavailable code.
Before the real preflight, freeze the actual build/serve/replay/analysis scripts
and capture ordinary compiler flags, immutable source/library bindings and
BPF equality as stated. This is ordinary reproduction support, not a new
experiment-control interface. No separate setup experiment is needed.

Native and loop BF_TRACE trajectories must pass unchanged source-native
graph/KV/history replay plus complete client/admission/compute/release joins.
That is finite current-trajectory validation, not independent eager-HF parity.
No graph error or overflow, failed prefixes retained, unchanged timeout/oracle,
all terminal states and actual client cleanup are appropriate. No source
selection follows from this diagnosis. Original PID1/10909, foreign
tools/setup_env.sh and the owning Workspace remain outside reviewer changes.

## Next action

Correct the one constructor/engagement defect in the same plan and prepared
instrumentation, then request the first of the permitted two follow-ups on this
same report. No other scientific blocker is identified at this stage.


## Follow-up1: revision1 and prepared implementation

Reviewed 2026-10-16 UTC before any build or measurement. This is the first
follow-up of the same fresh review; the initial rejection remains above.
Read revision1 plan, boundaries.md, source_entry.json, private before/
instrumented .cu/.h and their diffs, private Makefile, build/server/PowerShell
driver/analysis, source-native executor/mixed_replay.py, client and acquisition
assets. Python AST parsing only was performed; no script serving/build/test,
GPU invocation, compilation or Git mutation was run.

**Verdict: admit revision1; the constructor blocker is resolved. No remaining
scientific or executability blocker was found.** This authorizes neither an
ordinary speed claim nor source adoption: it is a supporting observational
diagnostic whose actual runtime acceptance remains the planned real preflight.

### Mechanism and source scope

The same plan explicitly records the initial mistaken inline premise and
preserves its unexecuted plan/source in unexecuted_revision0. Revision1 measures
the actual separate io_network CTA and dispatch. The primary is now dispatch
publication+packing+launch residence per launching iteration; it excludes
network-CTA residence and cannot rule out concurrent network interference
when its interval crosses zero or has a negative sign. A stage association
selects further investigation, not an automatic sleep removal.

Archived before .cu/.h are byte-identical to canonical source. The private
Makefile diff redirects the mixed .cu prerequisite and private .h dependency;
the ordinary flags, -dc, device-link and CUDA-runtime linkage remain. The
explicit executor include path supplies unchanged userspace_tcp.h; the quoted
include from the private source resolves its private io_uring_tcp.h. Neither
BF_IO_COALESCED nor BF_CHAINED_DISPATCH is enabled. A compile-time error guards
against accidentally enabling the former. uring_start and io_network execution
remain independent; no scheduling, sleep duration, mapped protocol, BPF or model
arithmetic intervention appears in either instrumentation diff.

Private Control and IoState additions remain device-local. Network counters
are copied only after the existing network-stream synchronization. Existing
shared page/IoStats interface and per-iteration mapped protocol are not
expanded. Extended private structs/codegen/register use are real measurement
perturbations, properly bounded by the four conditions rather than dismissed.

### Time and count audit

stage_now uses volatile globaltimer assembly with a memory clobber.
stage_delta records any backward observation through a device atomic error
counter and leaves its raw unsigned difference intact; the reader rejects a
nonzero clock_bad. It does not silently clip a negative interval into zero.
Both control contexts share that error reporting and execute serially within
their own one active thread; neither context races on the other's duration
array.

Dispatch records launching, nonlaunching and stop iterations separately.
Every ordinary active continue is in the nonlaunching bucket; the unsupported
coalesced continue is compiled out. Publication and FIFO retirement stay before
the pack timestamp, packing stays before the launch timestamp, and the final
launch timestamp brackets the actual one model graph API plus tail continuation
API and original launch accounting. The first dispatch has no outside anchor;
each later dispatch follows a launched model step. Final normal stop is counted.
The histogram and counts bind launching iterations to actual source counters.

The outside anchor follows stage-record/histogram bookkeeping and precedes its
stored anchor/CTA return. Hence this is explicitly an interval between anchors,
including model/head execution, graph scheduling, CTA return and unbracketed
bookkeeping, not an exhaustive wall-time partition or pure model duration.
The generated PTX/SASS bracket placement and expanded compile arguments still
need actual build evidence as already planned; this source audit does not
pretend to establish future generated code.

Network CQ/claim/send/connections/timer-publish/sleep brackets preserve the
ordinary control-flow order. Both cancellation-wait and terminal false-return
paths record stopping, with the former retaining its actual sleep and the
latter no synthetic sleep. Ownership classification uses existing local
seen/next_final/active-request state. Its no-owned-request bucket can include
producer or first-claim activity and is not an inactivity or client-window
classifier. Main-path counter updates after the last timestamp are outside
some brackets. That loss of exhaustive partition is documented, not hidden.
No total across concurrent network/model/dispatch contexts is permitted.

### Source-native replay and client coverage

Instrumented server entries use the source-native trace Make targets and pass
trace_requests=n+8. The actual bootstrap invokes unchanged mixed_replay.audit
after serving. It reconstructs slot ownership/admission/FIFO release/history,
resets KV values, executes captured graph replay and separately prepares fresh
upstream metadata with CUDAGraphMode.NONE. Both passes check the actual trace
tokens exactly. The second is still the same upstream-model trajectory oracle,
not independent eager-HF parity or a general fidelity result.

The analyzer checks both replay summaries, their exact token/request counts,
the fresh metadata terminal and round count, graph error/overflow, trace
admission/compute/release coverage, launch histogram, and unique client_ns
reference joins for all scheduled client tokens plus warmups. An initial
prepared-reader defect filtered warmups using event=request, while the unchanged
client emits event=warmup. This was reported and corrected before any run; the
current archived and TEMP analyzer filters warmup. No oracle, client behavior,
timeout, plan outcome or measured result was changed to accommodate it.

All seven unchanged client/config/schedule/observer/model/environment/preflight
assets match their existing TEMP originals byte-for-byte. The128-entry0_192
preflight schedule equals the first128 full offsets. The PS driver does not
pass the client's separate32-row --preflight switch; it selects the preserved
128-prefix file. Thus the planned request count is executable, rather than
silently truncated.

The PS four-condition preflight and fixed five-block/full orders match the
revised plan. Ordinary conditions bind active_wait_sourcebuild16, instrumented
conditions bind controller_stage_build16 with trace targets, and the mode/path
mapping uses native only for N/NI. Eight warmups precede a separately observed
five-second loaded-idle bracket; then the192/s schedule and full drain execute.
Server stop precedes client compression/transfer/archive, and the source-native
post-serving replay precedes terminal archival. The analyzer's full set equality
requires20 cells with all5x4 condition identities and computes the fixed
LI-minus-NI paired t primary without selecting favorable blocks. The raw reader
also resolves lossless gzip artifacts.

### Remaining implementation note, not a blocker

The CPU reader currently asserts the full20-cell set but does not independently
assert exactly four preflight conditions. The present PS driver calls it only
after all four preflight iterations, so this is not a validity defect in the
specified execution. A small explicit preflight set assertion would prevent
future manual replay of a partial prefix from being mislabeled complete.
This is a suggestion about ordinary completion checking, not another
experiment, interface or admission gate.

No additional model, load, baseline, profiler, N increase or tuning setting is
requested. Continue the planned actual build and smallest real four-condition
preflight, retaining any failed prefixes and all runtime perturbation/correctness
outcomes. One follow-up remains available only if a material newly observed
plan/execution defect requires it; unchanged artifacts do not need rereview.

Follow-up1 closing observation: before any execution, the owner adopted that
nonblocking completion suggestion. The current analyzer now explicitly
requires the four preflight cells (pair0,L/LI/N/NI,192), in addition to the
unchanged20-cell full assertion. I reread the actual assertion and parsed the
updated Python AST. This aligns with the already-fixed completion rule; it
does not change workload/oracle/metric or require a second follow-up.
Final follow-up1 verdict remains admitted with no blocker.
