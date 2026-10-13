# Chained device-graph dispatch

## Implementation and current status

The existing dispatcher uses one model fire-and-forget launch plus one parent
tail launch per step. The opt-in candidate attaches the unchanged dispatcher
as a dependent node after upstream body/head and tail-launches the chosen next
combined graph. CUDA explicitly permits tail self-launch. Model/head/sampling,
FP16, KV budget, packed prefill, FIFO-prefix release and both transports stay
matched. Original default remains separate pending performance evidence.

The [plan](../../bench/results/tail_chain_plan_20261012.md) and
[fresh plan review](../../bench/results/tail_chain_plan_review_20261012.md)
admit one supporting causal comparison. Official semantics are documented in
[CUDA device graphs](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cuda-graphs.html#tail-launch).
This is reusable GPU orchestration, not arithmetic fusion or an eBPF-only gain.

## Completed setup and strict qualification

Eight binaries build using the pinned temporary official runtime. Four traced
Qwen preflight executors pass160 requests/4192 independently replayed tokens.
Native successful launch counters show2/model-step in separate mode and1/step
in chained mode; trace step counts independently agree.

Both models/four conditions finish strict checks:4976 requests/177792 valid
tokens,2072 intentional rejects and40000 empty connections. All batch sizes1..8,
fragmentation,edges,wrap/reuse,mixed output lengths,pipelines/half-close,
rejection/subsequent valid response and helper-thread stop pass. Each actual
client sequence matches independently advanced host replay of its actual trace.
After-ready all-thread syscall checks engage native network operations and find
no steady serving accept/recv/send calls in either kernel condition. All native
exits/analysis are0; output release/cache ownership and teardown pass.

Before any untraced observation, the frozen complete-output set at
2026-10-13T00:28:04.805780+00:00 combines earlier finding0034 references and this
run's independently replayed strict/traced-preflight sequences. No untraced
output contributes. Exact whole-sequence membership is a finite-set
qualification, not replay of the current unobserved batch/cache trajectory,
universal numerical correctness, task quality or batch invariance.

The full untraced comparison remains in progress. No timing improvement or
default adoption is established by these dependency checks.

## Environment and reproducibility

During the first separate-Qwen bootstrap/preflight window lab becomes NotReady
and Tailscale/campus SSH time out. Existing Cloudflare SSH remains usable; the
same boot returns Ready automatically. Global OOM kills other Lean/Coder
processes and iSCSI/EXT4 errors occur on other devices. Original BPFusion Pod,
Coder processes and pipeline stay live; no replacement/restart/host mutation
occurs. Preserve this unequal setup exposure; do not claim host isolation.

Completed source/commands/build/strict/reference/fault evidence is in
[the experiment archive](../../bench/results/tail_chain_20261012/).
The exact runtime and pipeline commands are recorded there. Reproduce using
the documented vLLM runtime and existing make targets, then
python3 bench/vllm_serving.py --dispatch-comparison with --correctness for
independent traced replay, or --untraced --reference-path FROZEN for the
pre-observation finite-set contract. Analyze the raw with
python3 bench/vllm_serving_analysis.py RAW.
