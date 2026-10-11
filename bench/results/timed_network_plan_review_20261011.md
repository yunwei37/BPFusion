# PLAN REVIEW — native timed epoll and TX task CPU

Fresh independent review by timed_network_plan_review on2026-10-11.
Current source: bb059dfd90ceec8007982967ae98e055879250cd plus six scoped
uncommitted source changes. Read-only review; no GPU experiments executed.

Verdict: admit to qualification and real preflight. No blocking scientific or
execution defect found. Required substantive repairs: none.

## Scientific value and scope

This is an honest supporting component experiment. No formal paper RQ exists,
and the plan preserves the full user objective without inventing one.
It resolves whether the bounded executor-plus-TX CPU advantage survives an
efficient native request/reply worker. Finding0026 cannot answer through
reanalysis because it lacks both the timed condition and TX task accounting.
Positive, negative, tradeoff and crossing-zero outcomes change interpretation.
Qualification/counter availability remain dependencies, not research results.

## Attribution and metric reconstruction

clock_getcpuclockid/clock_gettime_ns measure the executor process including its
threads. The module exposes adjusted CPU time for the specific TX task.
Raw rows retain before/after components and monotonic read brackets. Current
analysis divides paired nanosecond differences by requests_per_cell*1000,
correctly yielding microseconds per measured request. The installed header
export task_cputime_adjusted was independently confirmed; its path agrees with
[Linux scheduler accounting](https://raw.githubusercontent.com/torvalds/linux/master/kernel/sched/cputime.c).

The sum supports CPU charged to these execution contexts during the window.
It cannot support total service CPU, all networking work, instructions, energy
or a syscall-only explanation. Sequential reads and client-close boundaries
prevent exact nanosecond alignment and complete connection-lifecycle accounting.
The plan already bounds those claims appropriately.

TTFT, TPOT, completion and throughput reconstruct from raw timestamps/tokens.
TPOT follows the conventional completion-minus-first-token calculation in
[vLLM benchmarks](https://docs.vllm.ai/en/latest/api/vllm/benchmarks/serve/).
Co-received tokens share arrival timestamps intentionally; client delivery
metrics remain distinct from GPU generation intervals.

## Fairness and mechanism

All conditions share model loading, captured computation, eight graph banks
and resident device dispatch. The wait build adds native timed epoll only;
model math is unchanged. Socket readiness can wake the timed worker before
the nominal60us timeout; it checks GPU completion after each wait.
This is credible but neither proven optimal nor equivalent to kernel
usleep_range(60,120). The busy condition supplies the latency/CPU tradeoff.

Parser placement, page backing, transport and wakes remain bundled. Matching
arithmetic does not isolate one cause. No external SOTA or NanoFlow
reproduction claim follows.

## Counts, order and execution

Totals:120 cells,7680 measured requests,249600 measured tokens,30 executors.
Eight warmups/process are separate.
Three-mode order: R,U,W; R,W,U; W,R,U; W,U,R; U,W,R.
Matrix rotation is deterministic/reconstructible. Five blocks do not balance
all six permutations; this is not a validity blocker for the stated comparison.
Nominal paired t95(df4) intervals have no family-wide significance claim.

Commands, fresh paths, strict independent oracle, counters and exit receipts
are executable. Native analysis validates coverage, token agreement, request
indices and executor receipts. Result review must independently reconstruct
CPU deltas, timings, engagement, queue completion, events and cleanup.

## Module/task lifetime and current evidence

TX retains an explicit task reference after successful creation. Shutdown stops
the task, reads final accounting and releases that reference under the same
mutex used by the getter. No new task-lifetime defect found. Executor teardown
unloads the module before unregistering/unmapping the page.
Root reports successful builds and identical dispatcher SASS; reviewer did not
execute these checks. Strict regressions and real preflights remain outstanding.
This review establishes plan validity, not a completed experiment.

Historical memory supplied ownership/acceptance context only; current source
and plan supplied the scientific review evidence.
