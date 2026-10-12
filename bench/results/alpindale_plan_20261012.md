# Existing RTX5090 Qwen megakernel qualification

Scope: a dependency for the retained same-compute serving comparison and
performance goal. The current profiled HF model region dominates short-input
TTFT (finding0030); prior MPK/Plow/MAK exact-generation qualification is mixed
or failed. This candidate adds a different existing native compute backend,
not another unchanged transport matrix or new model arithmetic campaign.

Question: can the unmodified AlpinDale CUDA computation for Qwen3-0.6B
produce complete reference-matched prompt-plus-64-token sequences on the
existing RTX5090? If qualified, inspect the smallest request/graph adapter
needed to reuse it identically in kernel and efficient userspace serving.
Positive results enable that comparison; numerical failure closes this
candidate under the strict standard and retains the current backend.
This qualification has zero standalone paper performance/novelty value.

## Frozen inputs and source-native path

Pinned upstream5030e154d39ecd054df03eb4dd9c8aa8185414d1,
MIT license, official qwen_megakernel/build.py JIT build and Decoder.
Source URLs:
https://github.com/AlpinDale/qwen_megakernel/tree/5030e154d39ecd054df03eb4dd9c8aa8185414d1
https://github.com/AlpinDale/qwen_megakernel/blob/5030e154d39ecd054df03eb4dd9c8aa8185414d1/qwen_megakernel/bench.py

Existing cached checkpoint revisionc1899de289a04d12100db370d81485cdf75e47ca,
Qwen/Qwen3-0.6B. BF16 matches the upstream contract; this is a new compute
condition, not a comparison with the earlier Qwen2.5 FP16 timing.

Before execution source inspection finds an importer mismatch: upstream
RoPE tables use theta10000 while the cached model config declares1000000.
Predeclare two importer conditions: unchanged upstream; existing importer
with only that literal replaced by the verified checkpoint theta.
The existing environment lacks accelerate. The loader may replace only
device_map="cuda" with an explicit .to("cuda") after from_pretrained,
preserving the tensors/dtype while avoiding an unnecessary package install.
Record this build/interface compatibility delta separately from theta.
No CUDA, reductions,precision,compiler flags,launch sizes or sampling edits.
The compatibility condition tests checkpoint interpretation, not an excuse
to weaken the oracle. Preserve both conditions and their exact delta.

Four fixed plain prompts: "Hello", "The capital of France is",
"Write a Python function to add two numbers.", and
"Explain why the sky appears blue in one sentence."
Use the cached tokenizer with add_special_tokens=True; archive actual IDs.
Independent HF BF16 eager forward with full prompt and cached autoregressive
decode generates exactly64 greedy tokens, without EOS truncation.
An independent default-attention HF reference is a predeclared diagnostic
to show whether upstream's own default-HF comparison changes the outcome;
it does not replace the eager reference after a failure.

Both step-by-step Decoder.step and upstream generate_nosync are tested.
Prompt prefix always consumes all input tokens except the last before the
64-step call. Decoder.reset precedes every actual generation; each of the
four prompts repeats twice per mode/condition to expose state reuse.
Total32 actual64-token sequences, complete actual/expected IDs retained.
The two modes must agree, repeated calls must agree, and every sequence must
equal the frozen eager oracle. Report default-reference agreement separately.
No partial-prefix/tolerance pass, prompt shortening, EOS exclusion or retry
selection. A mismatch is a valid negative qualification result.

## Execution and acceptance

Download the pinned author source to OS-temp inside the original matching
Workspace; no infrastructure-repo external tree, replacement
Workspace or persistent service. Use installed Torch/Transformers/CUDA and
existing cache. No change to the existing Python environment. If no existing
ninja executable is available, install only the upstream-required ninja
build dependency under the owned OS-temp directory via pip --target;
record its version/command and remove it with the apparatus. CUDA is already
at /usr/local/cuda; expose that existing bin directory only to this child.
Record software/device/source/checkpoint/build flags,
source texts/delta, actual commands, exit states and complete outputs.

Real preflight: official native build and one complete Hello/gen64 call
against the frozen oracle. A numerical mismatch does not justify rerunning
or changing the fixed workload; finish the other planned qualification
cells so their failure boundary is visible. A build/runtime failure may be
repaired only for genuine interface compatibility, preserving CUDA math
and recorded source. Do not patch model arithmetic or add numerical tuning.

Full command: HF_HOME=/workspaces/.cache/huggingface python3
<owned OS-temp directory>/qualify.py. Archive actual qualifier source and
raw stdout/results under bench/results/alpindale_*_20261012.*.
This is ordinary dependency apparatus, not a new experiment control layer.

Performance/latency measured during this qualification, if any, is diagnostic
only. No speed claim, cross-model gain, network comparison or total-CPU claim.
A future matched serving experiment requires independent admission and
the same qualified backend, precision, checkpoint and batching in both paths.
Current singleton synchronization/token pointers, host-launched step loop
and separate body/head kernels are known adapter questions; the no-sync API
does not prove persistent online serving or concurrent safety.

Close only own processes and file handles; retain the original Workspace,
cache, current production source and unrelated tools/setup_env.sh.
Remove owned temporary source/build apparatus after complete archiving and
fresh result review. No module/BPF hooks are needed for this compute dependency.
