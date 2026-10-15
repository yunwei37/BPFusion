# Batched token publication: incomplete performance comparison

Observed2026-10-15UTC in original yunwei356/bpfusion-dev Workspace/main,
baseea82f18b703732288b6a38a235cbc978daf4bc23.
[Plan](../../bench/results/output_publication_20261015/plan.md),
[plan review](../../bench/results/output_publication_20261015/plan-review.md),
[fresh result review](../../bench/results/output_publication_20261015/result-review.md)
and [archive/replay](../../bench/results/output_publication_20261015/)
retain the actual experiment and source selection.

## Intervention and question

The existing vLLM dispatcher system-fences each selected row before publishing
its produced count. The candidate writes all batch payloads, fences once, then
publishes every produced count. One CUDA thread performs both passes; DONE/
recycle fences, graph/model arithmetic, weights, KV, admission, padding/prefix
release, transport, timer and residency remain unchanged. The source delta is
7 added lines/1 removed line. It adds a pass and defers first-row visibility,
so fewer source fences do not establish lower delivered cost.

This supporting selection experiment asks whether reducing repeated result
publication fences improves gen64/c8 loop output TPS while preserving correctness.
Prior0051/0056 change SQ/CQ publication, a distinct intervention. Original-loop
is the component control; efficient timed-epoll native TCP is the main competing
mechanism. Original/candidate native conditions bound generic publisher effects.
Both paths use the same reused vLLM computation; any shared publisher benefit
would not be an eBPF-exclusive gain. No formal paper RQ is invented.

## Completion and failed qualification

Qwen real preflight completes four conditions/all four cells:128 measured
requests4160tokens plus32 excluded checked warmups. Both models' candidate
loop/native protocol checks each complete622requests22224tokens,259rejections,
5000empty connections and exact independently advanced graph/KV/history replay.
All batches1..8 occur. All four candidate lifecycle suites pass32actions/
652checked complete-or-prefix tokens each. Independent review also authenticates
10additional post-stop tokens across suites, all valid frozen prefixes.
Native intentionally completes31/32 transport requests after active stop;
loop drains32completions/3aborts, empty independent SQ/CQ and free model slots.
These passing portions are qualification dependencies, not performance evidence.

The full plan is40executors160cells5120measured requests166400tokens plus320warmups.
Actual collection stops after11Qwen executors, all serving exits0 but only10
driver-verified. It collects44cells1408measured requests45760tokens plus88warmups.
Qwen block2 original-loop returns one complete64-token response outside the
unchanged pre-observation whole-output pool, so full driver/wrapper exit1.
The remaining29processes, including all20Smol processes, are never launched.
No complete five-block primary estimate exists for either model.

Independent all-row inspection finds exactly one outside-pool response among
1496request rows. It is gen64/c8, measured index2, prompt IDs
[7985,264,2805,42113,13], marker468830097634060. The best of three frozen
sequences shares62tokens; the final two differ. All64tokens arrive,
graph_error=0,admitted=retired136 and transport queues drain.
This is neither a short response nor a TCP timeout. It occurs on the original
publisher and cannot be attributed to the candidate. Unrepresented legitimate
batch-dependent output and an actual wrong trajectory remain unresolved:
ordinary serving records no current batch/history replay. Do not label this
a proved floating-point cause, expand the pool, discard the row or rerun until
a favorable sequence appears.

## Available observations and limits

Run status is **incomplete**; tested performance hypothesis **inconclusive**.
The fresh review classifies value as supporting boundary evidence and impact
as a mechanism/workload boundary. It independently checks all44 collected
cells and40 signed descriptive contrasts; none substitutes for the planned
five-block result. Smol performance remains unavailable.

The two fully driver-qualified Qwen loop candidate-original gen64/c8 TPS
differences are+311.463 and-32.032token/s. Block2 arithmetic difference-130.027
uses the unqualified original control. These are partial observations, not a
pooled mean/CI or selection criterion. The corresponding TTFT differences
are adverse+0.099645,+0.090579,+0.192618ms, with the third comparison unqualified.
All native comparisons and the10.120238ms candidate-native short-output
TTFT maximum remain in the review tables. No favorable secondary result or
failed baseline is substituted for the fixed primary.

Performance uses no BF_TRACE/profiler. Traced qualification replays identical
upstream graphs and verifies metadata/history fidelity; it is not fresh eager-HF
parity, task quality or proof of every untraced trajectory. All-thread syscall
traces verify no steady loop userspace network handling and one serving
io_uring_enter; Linux kernel/timer/RX work remains. Partial known-worker CPU
cannot establish total service CPU/energy. The existing128-response network
diagnostic truncation is retained separately from model-trace/SQ/CQ overflow.

Pinned private packages equal0057 exactly: vLLM0.31,Torch2.13cu129,
Transformers5.17,NumPy2.3.5. This is not proof of all codegen/cache equivalence.
Sparse host observations retain boot04dc0087 and the existing400W power limit,
with56selected historical NVRM warnings before and after. The intended active
snapshot actually occurs04:11:54.668266UTC,48.730698seconds after full wrapper
terminal04:11:05.937568. No active full-run midpoint or continuous-isolation
evidence exists; warning harmlessness and mismatch causation are unproved.

## Source selection and reproducibility

No supported primary gain exists. Restore the saved original dispatcher
byte-for-byte; retain the candidate source/diff in the archive. No production
code growth, target, flag, model math, default or infrastructure change remains.
Default-module compatibility was conditional on selecting the shared publisher;
it is not run for this unselected candidate. Original shared builds and sessions
are preserved.

The fixed analyzer reproduces failure on the nonzero full terminal; its explicit
post-terminal replay remains failed. Preflight/protocol/lifecycle analysis
replays pass. [Archive guide](../../bench/results/output_publication_20261015/README.md)
and [restoration receipt](../../bench/results/output_publication_20261015/final_restoration.json)
record exact commands, byte equality, cleanup and post-cleanup CPU replay.
Close this unchanged publisher comparison. Before another ordinary performance
claim, establish a justified fidelity path for the actual execution rather than
enlarging a finite output pool after failure. Broader serving/performance work
remains active; this failed experiment does not establish a speedup.
