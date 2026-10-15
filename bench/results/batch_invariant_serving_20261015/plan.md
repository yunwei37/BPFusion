# Experiment plan: ordinary matched serving with upstream batch invariance

## Research question
No formal paper RQ/thesis/idea-story currently exists. Retain the user question:
Linux TCP/HTTP + eBPF/sockmap -> shared queue -> resident reused real-model GPU
-> asynchronous kernel TCP TX without a steady userspace request worker,
improving throughput/latency with matched computation.
Specific uncertainty: can the official batch-invariant FP16 execution mode
support independently checked ordinary untraced serving, and what delivered
throughput/latency does loop achieve against efficient native TCP in that mode?

## Paper-value admission
Role supporting. The largest credible story is a reusable service boundary with
ordinary exact upstream-output qualification and a fair compute-matched delivery
comparison. This is not a new determinism or model-kernel contribution.
The load-bearing reject argument is that finite output pools do not establish
correctness of new untraced batch trajectories; 0058 demonstrates that boundary.
Existing protocol traces replay histories but perturb the measured path.
No existing results establish official-reference equality or performance for
this upstream mode with GPU-owned graph execution. Reanalysis cannot recover
unrecorded ordinary histories or unrun mode.
Official reference generation/setup is dependency work, zero standalone research
value, folded into this serving comparison. The best alternative is offered-load
tail latency/total CPU measurement; checking its outputs is also required, so
this comparison addresses the nearer validity uncertainty. Another publisher
micro-optimization has lower value after 0058 and its mixed partial effects.
Positive: qualify this optional backend mode and report the matched comparison.
Contradictory: close its execution/fidelity boundary, preserve any failed case;
do not claim general-purpose deterministic serving or a transport win.
Mixed/inconclusive: retain every signed effect and narrow the backend/workload
claim. Do not expand frozen references or retry an output failure until passing.
0058 remains closed/incomplete; no cause for its mismatch is assumed.

## Expected and alternative outcomes
Tentatively expect same-mode native and loop to match independently generated
official outputs. Opposing explanation: upstream mode does not cover this FP16,
padding/prefix-release, device-launch graph path, or changes capture legality.
The correctness outcome is open. No directional throughput superiority is
assumed given prior native gaps. A failure of either path invalidates its
performance comparison. This tests a backend/workload boundary, not a necessary
paper thesis prediction.

## Published precedent and real assets
Official mode: https://docs.vllm.ai/en/stable/features/batch_invariance/
Official primary metric convention:
https://docs.vllm.ai/en/stable/cli/bench/serve/
Use vLLM 0.31.0 (cached official wheel source commit db9527a46), Torch2.13.0+cu129,
Transformers5.17.0, NumPy2.3.5, libbpf1.6.3, current NVCC13.0.88.
Source inspection: FP16 does not select the BF16 tuned breakable-graph default;
this is not proof our device-launched graphs work.
All source/runtime/build/test in original yunwei356/bpfusion-dev Workspace,
main base 3cb7685f368195a1d398ca9639a143df99e64a28. Original setup WIP remains.
Reuse official LLM.generate and SamplingParams, existing model checkpoint cache,
executor/vllm_graph.py/.cu, shared transport, bench/vllm_serving.py client driver
and existing analysis. No production source/default changes. Private builds
and runtime in this experiment's OS TEMP. No model tuning/new server.

## Comparison and fairness
Proposed: existing vllm_graph_uring_loop, upstream VLLM_BATCH_INVARIANT=1.
Single main baseline: existing vllm_graph_user_network_wait, same mode/FP16
checkpoint, graph construction, padded prefill/prefix-release, timer, budgets.
It represents efficient native Linux TCP without a Python per-token loop.
Its matching/winning bounds the proposed transport story. Published figures
cannot settle this matched mode/hardware/interface comparison.
Official CPU-scheduled LLM.generate is an independent correctness control,
not a speed baseline. No default-mode performance cell: its current ordinary
fidelity gap is unresolved. Earlier default figures are context, not a
new paired estimate of mode overhead. No tracing/profiling in performance.

## Workloads and correctness
Two fixed local checkpoints:
Qwen2.5-0.5B-Instruct revision 7ae557604adf67be50417f59c2c2f167def9a775;
SmolLM2-135M revision 93efa2f097d58c2a74874c7e644dbc9b0cee75a2.
Use the existing four tokenized prompts, plus the six existing protocol
length cases 1/15/16/17/32/64 for qualification. Official generation:
temperature=0, ignore_eos=True, max_tokens=64, detokenize=False; no chat template.
First produce serial official outputs independently of BPFusion, then verify
the same outputs with official full batch widths2..8 and reversed input orders.
Any official discrepancy fails qualification; never union output variants.
Freeze one complete64-token reference per prompt before observing serving.
One-token and stopped-prefix checks use exactly its corresponding prefix.
All correctly rejected inputs must have empty output. This is finite exact
token fidelity to official same-mode vLLM, not eager-HF/task quality proof.
Use the existing source-native protocol driver (622 total requests including259 rejections, invalid
messages, wrap, fragmentation, pipeline/half-close, all concurrency1..8)
on both transports/models with BF_TRACE and existing independent history
replay plus the frozen official output equality. This is qualification only.
Untraced preflight/full require exact official output/prefix equality and
existing error/counter/ring-drain assertions. No post-observation pool edits.
The binary protocol is unchanged; text tokenization/API semantics remain out
of scope. Existing lifecycle code unchanged; no independent lifecycle thesis
or added stop requirement is made.

## Metrics/repetitions
Fixed primary: gen64/concurrency8 client output token/s, loop minus native,
five paired process blocks/model. Signed mean difference and nominal paired
t95 interval df4; no pooled-request pseudoreplication. CI crossing zero is
inconclusive, not equivalence. Secondary: TTFT, completion latency, TPOT,
known-worker CPU, gen1/c1, gen1/c8, gen64/c1. CPU remains partial accounting;
no total CPU/energy or offered-load SLO claim.
32 measured requests/cell,8 checked sequential gen1 warmups/executor.
Models execute Qwen then Smol; within each model alternate transport order
and rotate cell order across paired blocks. Between-model order is not
balanced and cannot support a causal comparison of models. Report every block, adverse effect and outlier.
20 full executors,80 cells,2560 measured requests83200tokens plus160 warmups.
Reference/control/protocol work is excluded from performance timing.

## Execution
One command: python3 run.py {setup,reference,preflight,qualification,full}
after entering this OS TEMP. Exact subprocess commands/raw source/env/version
recorded there. Setup uses private pip venv pinned as above and private make
BUILD with unchanged current source. Preserve8 original build artifacts,
unowned tools/setup_env.sh, base packages/Coder processes and shared caches.
Only VLLM_BATCH_INVARIANT=1 added to test env; upstream-selected subsidiary
settings recorded, not manually copied/tuned. No power/clock/driver changes.
Preflight actual Qwen official control and loop/native gen1/64,c1/8 each8
measured requests. Full only after references and both models' actual
qualification pass. At most three preflight attempts per owning skill;
no retry can change fixed oracle/hypothesis to manufacture agreement.
Full completion requires both models/all planned cells, exact outputs,
terminal driver/analysis success, rings/lifetimes restored. A failure is
retained and stops affected comparisons; do not call a prefix a full result.
Source/env snapshots and JSONL/stdout/stderr are raw results. Record host
GPU/process/boot/warning snapshots before/active/after, with timestamps;
sparse observations cannot establish continuous isolation.
Fresh plan review before actual setup/run; fresh result review after terminal.
Cleanup only this owned TEMP's runtime/build/dependencies after preserving
reproducible nonbinary source/raw outputs. Original source unchanged. Archive
under bench/results/batch_invariant_serving_20261015, update evaluation/finding
and README as appropriate, commit+push on main under existing authorization.

## Interpretation
All correctness succeeds: report ordinary same-mode loop/native difference.
Primary intervals above zero support only this measured throughput gain;
below zero bound the mode/transport; crossing zero remains inconclusive.
Latency secondary does not silently replace primary. Any fidelity/capture
failure closes the proposed backend path's evidence without a speed claim.
No universal model support, zero CPU, mode-overhead, task quality, previous
mismatch-cause, or new model-kernel claim follows.
Target table: two models' matched same-mode throughput, latency and signed
uncertainty, or explicit unavailable cells and exact failure if unexecutable.
