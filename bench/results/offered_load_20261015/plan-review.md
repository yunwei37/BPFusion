# Offered-load plan review

## Round 1 — 2026-10-15 UTC

Reviewer: fresh `/root/offered_load_plan_review`. Read-only inspection of the
current plan, current main `9cfcf98a5dbda283c3e06474c74ca3aab59b65a6`,
finding0060, relevant evaluation history, all proposed native changes and
the archived kernel candidate. No GPU process or workload was launched.

**Verdict: scientifically admit; execution pending one metric-definition
repair and review of the actual load/analysis/qualification adapters.**
This is not a rejection of the offered-load comparison, and it does not require
another baseline or additional model work.

### Admission and decision value

This is supporting evidence with a meaningful new discriminator. Finding0060
measured fixed bursts/quiet gaps and a native competitor that still polls while
idle. It cannot answer independent-arrival P99 against request-aware native
waiting by reanalysis. A positive valid same-compute difference supports a
finite model/load/constructor regime; a native win, mixed models, failed requests
or crossing-zero interval prevents a general service-win claim and keeps the
existing production selection. This is more directly actionable for the user's
latency/TPS objective than another timer/fence micro-variation or an unqualified
model-specific arithmetic port. It does not settle total service cost,
ordinary untraced fidelity, all models, production HTTP compatibility or novelty.

One main baseline is sufficient. Request-aware native epoll represents the
credible competing answer that socket readiness plus active completion polling
already delivers the relevant service behavior without kernel/GPU I/O ownership.
Its matched numerical result is missing from published/existing evidence.
Repeating fixed-idle native as a full extra row would add little; citation to0060
is appropriate. Different real constructor admission/connection limits remain
part of the comparison, with overload/rejections reported, not a claim of an
isolated syscall effect.

### Blocking scientific clarification: TTFT origin

The plan calls the primary standard vLLM TTFT while proposing reuse of
`resident_dispatch.request()`. That function records its start only after the
caller has completed `connect()` (source lines72–101 and104–107). The cited
vLLM0.31 endpoint function starts its clock before `session.post()`, including
connection/connector delay (official source lines185–189 and215–219).
Consequently a fresh-connection overloaded path can defer work into connect,
then appear to have low post-connect TTFT. Equal delivered counts alone do not
resolve this queue-displacement explanation.

For a service-facing primary, use the already planned connect-begin→first-token
measurement, retaining source-native send-start→first-token as a diagnostic;
alternatively make the narrower post-connect claim explicit and do not describe
that timing as the official vLLM protocol or sufficient evidence of a general
service-latency advantage. Scheduled→first-token and scheduling lateness should
remain visible separately so client release lag cannot disappear into a
redefined origin. Fix the definition and adapter before real observation.

Official primary source:
https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/lib/endpoint_request_func.py

### Protocol differences requiring accurate wording, not extra runs

The cited vLLM0.31 `get_request()` precomputes gamma intervals, cumulatively
sums them, then normalizes cumulative delays to `N/request_rate`
(lines417–462). The draft instead specifies unnormalized gamma intervals.
Both are reasonable finite open-loop protocols, but raw gamma is an explicit
deviation, not exact reproduction of v0.31. Shared per-block schedules and
realized arrival-rate reporting make the planned raw-gamma version interpretable.
Do not silently normalize after seeing outcomes.

Official vLLM percentiles use NumPy's default interpolated percentile
(lines698–704), whereas the draft fixes nearest-rank. A declared nearest-rank
P99 is a legitimate quantile convention; call it such, or align to the cited
official implementation before collection. This convention difference alone
does not invalidate a matched comparison.

https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py

### Workload, uncertainty and failures

Four fixed rates, two existing small checkpoints,64-token outputs and five
paired process blocks test one relation, not80 independent experiments.
A256-request block gives a noisy extreme quantile; the plan correctly allows
inconclusive outcomes and nominal t95df4 intervals. No minimum extra sample
count or benchmark breadth is required for execution. Do not describe the
finite run as steady-state saturation capacity, or crossing-zero as equivalence.

Absolute schedules must be fixed independently of completion, and request
threads must not be silently bounded by an executor pool or semaphore. Preserve
actual launch/connect/send/token times, all exceptions, socket60s timeouts,
partial token arrivals and every scheduled attempt. Failures in a primary cell
censor unconditional successful-service superiority; conditional successful-only
P99 cannot substitute. Wrong accepted token sequences are correctness failures.
Paired paths need the same schedules/cases and an analysis that pairs block
effects rather than treating individual correlated requests as independent.

### Native source inspection

The changed private native source adds an eventfd solely for shutdown and
selects60000ns while `head!=completed || buffered_ready`, otherwise remaining
service deadline. Inspection finds no concrete lost-progress or lost-stop defect:

- `head-completed` covers a model or unsent response; blocked complete buffered
  requests keep polling even when no request is currently admitted.
- Partial socket input waits on EPOLLIN, which is the correct idle behavior.
- The eventfd counter persists when a helper signal arrives before epoll sleep;
  EAGAIN on a saturated counter also leaves the descriptor readable.
- The stop flag is checked after wake; stopped-before-fd-initialization is
  checked by the subsequent loop condition.
- Reply progress, slot publication, model arithmetic and native output framing
  remain the existing source-native implementation.

This is a code review, not proof of liveness. The planned zero-request deadline,
helper-stop and existing real-model protocol/lifecycle checks are necessary
dependency qualification for this changed baseline, not standalone paper wins.
No artificial new stop bound or runtime tuning is requested.

### Kernel source inspection and frozen versions

All three private kernel candidate files are byte-identical to0060's archived
`production-candidate` snapshots at this inspection. That candidate contains the
actual wait-owner TID shutdown repair, before-submit CQ acknowledgement and
adaptive timer, while the existing after-submit macro keeps fixed behavior.
There is no newly invented kernel alteration to justify another timer study.
The private build must still point to its own BPF object/header rather than
accidentally loading main's old object. Preserve actual compiled source/commands.

### Executability still awaiting actual artifacts

At inspection TEMP contained the plan and private snapshots, but no
`setup.py`, `qualification.py`, `load.py` or `analyze.py`.
The root explicitly reports these adapters are being prepared. Their absence
does not make the scientific proposal weak, but execution cannot be approved
from intended behavior alone. Review their actual code for:

1. the fixed metric origin/quantile convention and independent absolute schedule;
2. no admission backpressure, complete failure/partial-output rows and unique IDs;
3. finite service budget sufficient for all four cells and unchanged socket
   timeouts, plus natural process exit;
4. exact trace/client matching and independent graph/KV/history replay for every
   accepted request, without learning an oracle from serving outputs;
5. paired per-process P99 calculation and correct censored-failure interpretation;
6. actual variant build bindings and natural native/helper/idle qualification.

These are the existing planned properties, not a new experiment-control
interface or additional research matrix. Optional style, wider workloads,
more baselines and total CPU instrumentation do not block this experiment.

## Round 2 — explicit follow-up 1, 2026-10-15 UTC

The primary definition is now connect-begin→first-token, with post-connect
and scheduled timing retained separately. Normalized cumulative gamma schedules
and linear percentiles align to the cited pinned protocol. The first-round
scientific timing concern is resolved before observation.

**Verdict: execution blocked by one source-binding defect in the current private
Makefile. The scientific proposal remains admitted.**

### Invalidating defect: main BPF source would be compiled

`kernel/Makefile` line38 still has
`$(BUILD)/%.bpf.o: bpf/%.bpf.c bpf/include/bpfusion_queue.h`.
`setup.py` invokes make with cwd `/workspaces/repository` and asks for
`TEMP/kernel-build/uring_loop.bpf.o`. Consequently its recipe compiles
main's fixed-wait `bpf/uring_loop.bpf.c`, not the archived adaptive candidate.
The private BPF include path and the private GPU helper's corrected object
pathname do not repair the wrong compilation-unit prerequisite. This could
silently test a different hybrid, including wrong adaptive wait coordination.

Bind the actual kernel-loop object target to
`TEMP/kernel/bpf/uring_loop.bpf.c` and its private queue header while keeping
the official compile recipe. Confirm actual source expansion before setup.
The C++ variant first prerequisite already points to private vllm_graph.cu;
quoted local includes then select the variant io_uring/userspace helper.
The private kernel helper opens the corresponding private kernel-build object.
The shared unchanged main attach tool remains an appropriate source-native
loader because the canonical request-page ABI is unchanged.

### Executable scheduler and raw accounting

Actual `load.py` lines196–256 satisfy independent arrivals:

-8 checked warmups precede each executor's cells.
- NumPy gamma draws are cumulatively normalized to N/rate, same pair seed
  and prompt sequence in each path. Rate order rotates by pair; path order
  alternates through the two permutations.
- Main scheduler sleeps only to an absolute due time and creates an ordinary
  new thread per attempt. No completion-driven admission, semaphore or thread
  pool exists in measured scheduling. All threads are joined only after all
  due-time releases. The retained pool belongs only to the established
  closed-loop protocol qualification, not full measurement.
- Every attempt records its planned release, thread start, connect begin/end,
  source-native send start and token timestamps; actual lateness remains visible.
- OSError subclasses including timeout, reset and short-reply ConnectionError
  are request failures. The necessary private client adapter preserves markers,
  partial token sequences and arrivals on exceptions. Assertions/malformed
  accepted replies remain correctness-invalid instead of becoming fast failures.
- Each cell keeps all256 attempts and success/failure counts. Tokens/s uses
  successfully completed responses and the complete finite cell/drain duration.
  Partial tokens on failed requests remain raw diagnostics, not falsely
  counted as successfully completed generation.
- Child closure variables are unchanged until all child threads join, so the
  next rate cell does not overwrite active requests' gen/rate definitions.

The300s existing service budget is ample for the intended finite successful
schedule (about79s of arrivals plus drain), but pathological repeated failures
can still exhaust it. Such exits remain invalid/incomplete or censored as
appropriate; do not silently extend deadlines or selectively replay cells.
This is not a demand for a new time cap.

### Oracle and failure accounting

Trace budget is the full planned admitted-request upper bound plus warmups,
not a small sampled prefix. Successful client markers are matched uniquely to
independent upstream graph/KV/history replay references, including exact
prompt/gen/bad flag and full tokens. Failed request markers can match an
admitted reference, requiring an exact partial prefix; failed connects with no
admitted reference must have no tokens. Unmatched references invalidate the
driver. CPU analyzer independently checks marker uniqueness, complete attempt
indices, counters, empty request slots and transport queues.

The source-native upstream replay reconstructs model inputs/physical KV history
and executes reused graphs, rather than using returned serving tokens as its
oracle. It remains a traced reused-graph correctness qualification and does not
become an independent eager-HF or ordinary untraced fidelity claim.

### Analysis and qualification

`analyze.py` reconstructs connect-inclusive, post-connect and scheduled timing
from timestamps; its interpolation formula matches NumPy's linear convention.
It checks identical per-block relative schedules and paired process ordering.
Five block P99 differences use nominal t95df4; a failed request in either
condition marks that rate's primary/latency comparison censored rather than
an unconditional superiority result. All-failed cells yield null conditional
quantiles instead of zero latency. The report must honor that flag even when
a conditional interval looks favorable.

Actual qualification includes both model/path protocol suites, all four frozen
whole/prefix lifecycle cases, and native zero-request deadline/helper-stop
diagnostics. Existing socket and lifecycle bounds remain unchanged. This is
appropriate dependency work for the altered baseline/candidate; no extra
baseline, model or compatibility matrix is required for the unretained source.
Real preflight remains necessary after the source binding is fixed.

### Nonblocking provenance note

`load.py` metadata's `client_source` and `native_source` currently read main's
files, whereas actual client instrumentation/native helper live in private
snapshots. The actual private sources and build commands exist independently,
so this does not invalidate the numerical comparison, but these fields should
be accurately labeled as original source or record actual source before
collection. Do not imply the unmodified embedded source is the compiled private
native implementation.

No GPU/setup/run was executed by this reviewer. No application or plan file
was changed. One final explicit follow-up remains under the skill's same-plan
review limit; do not introduce another reviewer to reset it.

### Round 2 resolution during the same review

Before this review closed, root repaired the reported binding defect without
building or observing outcomes. Reviewer reread the actual files:

- Kernel BPF pattern prerequisite and after-submit prerequisite now name private
  kernel BPF source and private queue header.
- Both C++ variant prerequisites now name all private CU/helper/header inputs.
- A reviewer `make -n` for the actual private loop object exits0 and expands to
  clang compiling `TEMP/kernel/bpf/uring_loop.bpf.c` into
  `TEMP/kernel-build/uring_loop.bpf.o`. This is a dry run, not a build or GPU test.
- Every actual top-level Python adapter parses successfully by AST inspection.

**Final round2 verdict: admit execution through the planned real preflight and
full comparison. No unresolved invalidating scientific/executability defect
was found.** The earlier round2 blocked verdict records the intermediate
source state and is superseded by this same-round verification.

Native liveness and kernel engagement remain unproved until real qualification;
review approval is not a passing preflight or a performance result. The
nonblocking metadata-label correction remains useful. No third review round is
required merely to restate this unchanged plan, and no new experiment or
infrastructure is requested.
