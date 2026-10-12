Observation: 2026-10-12T18:35:46.671953+00:00

# AlpinDale qualification plan review

Verdict: admitted as a backend dependency. No blocking scientific or
executability defect in the proposed qualification. This is not admission
of a standalone paper experiment or a serving-performance comparison.

## Evidence examined

Read the current alpindale_plan_20261012.md, finding0030 and upstream-backends.md
in the original Workspace. Independently fetched the pinned upstream source
at5030e154d39ecd054df03eb4dd9c8aa8185414d1: build.py, model.py,
bench.py, __init__.py, torch_bindings.cpp and the native launch functions.
Read the cached checkpoint config atc1899de289a04d12100db370d81485cdf75e47ca.
No build, model execution, GPU experiment or production edit was performed.

The upstream importer really hardcodes RoPE theta10000.0; the cached config
specifies1000000. Its other directly checked dimensions match the importer:
28 layers, hidden1024, intermediate3072,16 query heads,8 KV heads, head_dim128,
vocabulary151936, BF16 and tied embeddings. The plan's two importer conditions
therefore distinguish an unchanged author implementation from a predeclared
checkpoint-interpretation repair without changing CUDA arithmetic or selecting
a condition after seeing results.

## Admission and decision value

Finding0030 localizes most instrumented short-input TTFT to the current
model execution span. It does not prove pure launch overhead or a bandwidth
bottleneck. Qualifying an existing RTX5090-native complete-model implementation
is a concrete reuse decision that can enable a faster same-compute serving
comparison; another unchanged transport matrix cannot resolve this dependency.

This is different source/backend evidence from the recorded MPK, Plow and
model-as-a-kernel qualifications. Success permits interface investigation;
strict failure closes this candidate and retains the qualified backend.
Both outcomes change the next implementation choice. The qualification has
zero independent novelty or serving-performance value, exactly as declared.
No paper RQ exists here, and this review does not invent one.

## Correctness and executable path

The pinned build uses the official Torch extension path with sm_120a and its
default tuning/fast-math flags. The Workspace environment has no LDG_*,
CC/CXX or TORCH_CUDA_ARCH_LIST overrides in the inspected process.
Successful compilation remains a real-preflight outcome, not a source claim.

Decoder.step ingests one token, advances its position and reads the next ID.
Consuming every prompt ID except the last, then feeding the last prompt ID
through64 autoregressive steps, implements the stated full-prompt test.
Decoder.reset clears position and KV before another sequence. The native
generate_nosync binding accepts the same weights/cache/scratch tensors and a
start position, returns a64-ID device tensor and synchronizes at the end.
It can be called directly to retain all tokens without Decoder.generate's
EOS truncation/text decoding. Upstream bench.py checks only eight tokens of
Hello and merely prints them; it cannot substitute for the planned full oracle.

The four prompts, two importer conditions, two execution modes and two repeats
give32 complete64-token candidate sequences. Independent HF BF16 eager
prompt-plus-cached-decode output is an appropriate frozen strict oracle.
Default-attention HF output is a separately reported diagnostic, not a
replacement pass condition. Mode/repeat agreement cannot by itself certify
correctness because both candidate paths share the same native computation.

Native generate_nosync still submits kernels from a host loop. Process-global
barrier/token/position pointers also remain. Consequently qualification does
not establish device-launch eligibility, concurrent request safety, resident
online admission or absence of a userspace worker. The plan explicitly
preserves these adapter uncertainties and defers serving claims.

## Implementation and interpretation requirements

These clarify execution of the admitted plan; they do not require broader
workloads, another baseline or another experiment:

- Load both candidate weights/tokenizer and both independent HF references
  from the recorded local snapshot, or explicitly pass its frozen revision.
  HF_HOME alone identifies a cache location, not an immutable checkpoint.
- Archive the actual qualifier and runnable command before interpreting
  results. The current command's owned-directory placeholder is ordinary
  setup still to be completed; no concrete qualifier has been reviewed.
- Ensure each importer condition actually invokes its own declared table
  construction despite Python module caching. Record the literal delta and
  effective theta. Use sequential calls because upstream global state is
  unqualified for concurrent use.
- Retain all32 complete candidate sequences, both reference sequences,
  repeat/mode comparisons and mismatch locations. A mismatch may close
  acceptance while the remaining declared cells expose its boundary; do not
  replace the eager oracle or omit EOS/token suffixes.
- Interface/build repairs may preserve the upstream CUDA computation and
  recorded default flags. Successful repaired builds alone are dependency
  evidence, not a numerical pass.
- Any observed timing is diagnostic for this new Qwen3 BF16 condition.
  It cannot establish improvement over earlier Qwen2.5 FP16 or attribute a
  speedup to eBPF, kernel networking, CPU removal or resident serving.

## Return

Plan admitted; research role dependency-only; paper impact none by itself.
Perform the actual build and complete real qualification, then obtain a fresh
terminal result review. A pass enables assessment of the smallest shared
backend adapter. A failure closes the strict replacement candidate without
numerical tuning or expansion into a model-arithmetic campaign.

Primary source:
https://github.com/AlpinDale/qwen_megakernel/tree/5030e154d39ecd054df03eb4dd9c8aa8185414d1

## Same-event prerequisite update

The parent supplied and this reviewer read the revised pre-execution plan.
The existing environment lacks accelerate and a ninja executable. The
predeclared loader-only replacement of device_map="cuda" by .to("cuda")
preserves the BF16 state tensors and source-native weight importer for both
theta conditions; it does not change the numerical acceptance standard.
Using upstream-required ninja1.13.2 only beneath the owned OS-temp deps
directory, and exposing the existing CUDA bin only to the child, avoids
replacing the measured Python environment. Record these interface/setup
changes independently of the RoPE literal delta.

Independently compared downloaded model.py, build.py, kernel.cu and
torch_bindings.cpp against the pinned upstream bytes; all remain identical
at this observation. No qualifier, native build or generation has been
reviewed or executed here. This is normal preflight setup still to be
completed. Admission remains unchanged, with no additional blocking defect.
