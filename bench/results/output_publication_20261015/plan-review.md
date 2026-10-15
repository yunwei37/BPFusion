# Independent plan review: batched model-result publication

Review time: 2026-10-15 UTC. Original yunwei356/bpfusion-dev Workspace,
`/workspaces/repository`, main
`ea82f18b703732288b6a38a235cbc978daf4bc23`.
This is the initial fresh PLAN REVIEW. No GPU execution, source/recipe edits,
cleanup, Git action or other-task delegation was performed.

## Verdict

**PASS. No remaining scientific or executability blocker in the frozen plan
and recipes inspected.** This admits a supporting implementation-selection
experiment, not a headline result, general service acceptance or proof of a
speedup. Setup/preflight still have to establish real execution.

One concrete command defect was found while recipes were being prepared:
direct serving commands without `--loop-comparison` would omit source-native
worker/CPU observations and cell rotation that analysis.py requires.
The final plan example and every serving invocation in run.py now include
that existing flag. This was resolved before serving execution; request,
oracle, timeout and metric semantics were not changed.

## Material examined

I read plan.md, candidate.diff, setup.py, serving.py, analysis.py,
lifecycle.py, analysis_lifecycle.py, run.py, recipe-adaptations.md,
source_frozen.json, preserved_before.json and frozen_references.json;
current dispatcher, TCP consumers, Makefile and source-native serving code;
findings0051,0056,0057; current evaluation and closest-work map.
All currently present Python recipes compile in memory without a syntax error.

The saved original_vllm_graph.cu is byte-identical to HEAD's tracked file.
candidate_vllm_graph.cu and source_snapshot/executor/vllm_graph.cu are
byte-identical to the current dirty candidate. The snapshot therefore describes
the candidate, not the pre-edit source; the separately named original file
correctly supplies the control. Git status contains only the owned publisher
edit and the pre-existing untracked tools/setup_env.sh.

The frozen reference asset is byte-identical to the previously archived0056
asset. Both lifecycle configurations embed precisely the corresponding frozen
model object, without adding current outputs. The finite pools contain17
prompt/generation keys per model, with22 Qwen and19 Smol complete sequences.
These facts establish pre-observation qualification scope, not independent
eager-HF model equality.

## Scientific admission and alternatives

The retained serving-path/TPS/latency question is explicit. There is no formal
paper RQ/thesis/idea-story to rewrite. The candidate tests a distinct plausible
coordination cost in the existing real-model driver: one system fence per
published row versus one per completed model batch.0051 and0056 alter SQ/CQ
ring publication, layout and finite-drain behavior, rather than this publisher.
0057 keeps this publisher unchanged, its full Smol decomposition fails, and
even complete Qwen durations do not identify this intervention's effect.
None can select between the two source implementations by reanalysis.

A positive primary effect can justify considering a small local source change;
a negative or inconclusive effect restores the original and closes this
candidate. Those are different concrete implementation decisions. Success does
not establish first GPU I/O, first CPU-proxy removal, eBPF-exclusive gains or
generic model-server superiority. Failure bounds this mechanism/constructor
and workload rather than challenging an invented necessary thesis prediction.

Offered-load/tail/full-CPU service evaluation would have greater breadth, and
another unmodified backend would enlarge portability evidence. Neither settles
this specific source intervention from existing data. Given the small
production delta and already available actual serving/oracle machinery, this
is an admissible supporting step. Its potential gain is plausibly small;
another unchanged timing run or profiler retry after an unresolved result
would have weak value. A new backend or broad service evaluation is not an
additional admission condition for this finite comparison.

## Ordering, ownership and change scope

Only one CUDA thread executes dispatch: all other threads return immediately.
The original loop writes a row payload, system-fences, then publishes produced.
The candidate writes every selected row's payload, performs one system fence,
then writes every selected row's produced count. All payload stores therefore
remain before the fence, and every availability store remains after it.

The [CUDA13.0.3 memory-fence documentation](https://docs.nvidia.com/cuda/archive/13.0.3/cuda-c-programming-guide/index.html#memory-fence-functions)
specifies system-scope ordering for writes by the calling thread. That supports
this same-thread batching inference. It does not by itself establish consumer
visibility or make this a generally atomic publication API. Here the existing
cache-global stores, system-acquire GPU consumer loads and host acquire loads
remain unchanged. No new writer is introduced.

Selected indices and batch remain intact until the second loop finishes.
The candidate increments each request's k exactly once, then publishes that
updated count; only afterward can DONE/release and new admission run.
DONE's own system fence, FIFO-prefix ownership, shutdown/quiescence and final
transport/recycle conditions are unmodified. Transport cannot recycle a slot
merely from the newly published count: final availability is still gated by
DONE and ordered final ownership. Rejection processing is unchanged.

There is a real bundled timing effect: earlier rows become visible after all
batch payload/local-request updates, rather than individually during that
loop. The extra publication pass can cost work, and c1 cannot amortize fences.
Those are properly included in the intervention and secondary latency tests;
source fence counts cannot identify physical PCIe cost or exclusive mediation.
Real protocol/lifecycle qualification remains necessary despite this static
ordering argument.

The candidate is a small shared-dispatcher change, not model arithmetic.
No additional public flag, persistent helper, target, queue ABI, timer, driver,
clock/power setting or infrastructure entity appears. Temporary private builds
and runtime fit the authorized benchmark scope. Restoring the saved dirty
original if unselected is source selection, not undoing a Git commit. A
positive source decision still requires the declared module-compatibility
qualification because the shared publisher also reaches that existing path.

## Fair comparison and fixed metrics

Original-loop is the direct component control. Efficient timed-epoll native TCP
is the credible main competing orchestration mechanism; its matching or win
prevents claiming transport superiority. Original-native and candidate-native
provide the corresponding source-policy controls and separate generic publisher
effects from loop-specific effects. These are not four independent external
baselines. Another hardware-specific network stack is unnecessary for this
same-compute local question.

setup.py saves a Makefile with only the source prerequisite redirected to the
saved original. It builds the same four existing target names in separate
original/candidate private directories, with the same NVCC/options/runtime,
before exposing either to the serving driver. All conditions share FP16
checkpoints, native graph/bootstrap/KV/padding/prefix behavior, input/output
budgets, preopened TCP and the existing timer. Ordinary performance has no
BF_TRACE or GPU profiler; traced protocol is a separate qualification dependency.

The fixed primary is loop candidate-minus-original gen64/c8 client output TPS,
reported independently for both models with paired process-block uncertainty.
It cannot be replaced with a favorable secondary latency result. Native policy
and transport contrasts, TTFT/TPOT/completion, percentiles and partial worker
CPU remain signed boundaries. The analyzer reports latency/CPU differences
with its inherited favoring sign; prose must explicitly convert those signs
if presenting raw candidate-minus-original latency.

The [official vLLM metric documentation](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)
supports client TTFT and per-request TPOT terminology. Actual timing formulas
and the finite TPS window are preserved in the source-native client/analyzer;
this does not make the custom token-ID HTTP frontend an official vLLM
capacity/SLO benchmark. Pooled p99 from these small finite cells is descriptive,
not a production tail guarantee.

Five paired process blocks, not requests, are the replicate unit. The four
condition orders rotate; the fifth repeats the initial order and residual
drift/order confounding remains. Model ordering is sequential Qwen then Smol,
so cross-model results should not be pooled as exchangeable repetitions.
Nominal t95df4 intervals are appropriate to the declared narrow analysis but
provide neither familywise protection, equivalence nor noninferiority proof.
All signed blocks/outliers must remain.

## Executability, full coverage and fixed correctness

The executable phase commands are
`python3 TEMP/setup.py`, then `python3 TEMP/run.py preflight`,
`qualification`, `lifecycle`, and `full`, using the private runtime/environment.
run.py writes actual driver commands and terminal exits. Each serving command
uses the existing --loop-comparison path. Root/source imports remain in the
original Workspace; entry symlinks resolve their private sibling libraries.
Existing shared BPF loader/object are reused, not overwritten.

Preflight is actual Qwen across all four paths and all four gen1/64 byc1/8
cells:128 measured requests4160 output tokens, plus32 checked warmups.
The full matrix is40 executors160 cells5120 measured requests166400 tokens
plus320 excluded checked gen1 warmups. The unchanged source-native analyzer
requires complete named process/cell coverage, exact request indices,
terminal success, frozen whole-output membership, arrival/metric formulas,
ownership/queue conservation and native counter agreement.

Candidate traced protocol selects loop/native for both models, with the full
622-request22224-token contract per executor,259 rejects and5000 empty
connections. It preserves actual graph/KV/history replay, all-thread strace
and model/slot/queue checks. BF_TRACE qualification does not invoke the CUPTI
profiler that was present in0057's failed post-profile replay; that distinction
does not promise that no new real failure can occur.

Lifecycle covers both candidate transports and both models with the existing
32-action652-checked-token complete-or-prefix workload and raw wire/post-stop
bytes. Native's interrupted31-of32 completion accounting is explicitly retained;
loop requires32 transport completions/3 aborts, independent empty SQ/CQ and
free physical model slots/recycle counters. The separate analysis_lifecycle.py
is runnable against TEMP and checks those conserved outcomes. Fresh result
review must independently inspect raw post-stop bytes and syscall mechanism
rather than treating a stored pass boolean as sufficient evidence.

Frozen ordinary pools are weaker than independent eager-HF equality and leave
unobserved ordinary batch histories and arbitrary inputs unqualified. Existing
AMK exact-HF failures are not repaired. These limits are stated rather than
hidden or used to inflate generic backend acceptance.

Setup, raw driver exits, fixed analysis, sparse host observations, result review,
source selection, owned-resource restoration and archived CPU replay are
necessary completion artifacts. Host observations cannot prove continuous
exclusive use or harmless driver warnings. Any failed preflight/qualification,
baseline mechanism failure or fixed-analysis failure remains failed evidence;
it cannot count as a candidate win or be repaired by expanding output pools,
weakening oracle/timeout criteria or replacing adverse cells.

## Remaining nonblocking limits and result decision

There are no results to assess yet. Source-level fence removal predicts
ordering, not a performance win. Model work may dominate, scheduling histories
may differ, partial worker CPU is not total kernel/softirq/energy cost, and two
models on this RTX5090 do not establish a generic server contract.

Proceed to the declared real preflight and complete integrated run if executable.
If ordinary primary intervals cross zero, close this intervention and restore
the exact original; do not promote similar means to parity. If a model has a
supported gain, retain that model-specific conclusion alongside adverse latency,
native and qualification boundaries before considering any shared-source
selection. The broader serving/performance objective remains active regardless
of this supporting experiment's outcome.
