# Normal-build capacity and native-FIFO integration

2026-10-15 UTC. Engineering implementation/regression evidence, with no new
performance matrix or performance hypothesis.

## Changes and scope

The ordinary native TCP path now selects the eligible-complete-frame FIFO
already qualified in findings0063/0064. Its source is byte-identical to the
reviewed capacity8 snapshot; peer lifetime, disconnection and response ordering
remain covered. This removes FD-priority admission from the native competitor,
without claiming an eBPF performance advantage.

The canonical queue header defaults to eight banks and permits the existing
CPPFLAGS to supply the tested sixteen-bank layout. The normal Makefile propagates
CPPFLAGS consistently and retains its required absolute BF_BUILD_DIR when the
caller supplies CPPFLAGS on the command line. Default8 preprocesses identically
to the old header; explicit16 to the qualified private header. Model arithmetic
is unchanged. Each ABI needs a separate BUILD directory and matching BPF,
loader and GPU objects. No sixteen-bank runtime default is selected.
Legacy module16 and HF/AMK16 remain outside qualification. The module's existing
exact-page-size check rejects mismatched layouts; module source is unchanged.

## Actual builds and dependency repair

build_status.json records normal root-Make builds at8 and16: BPF,loader,
traced/ordinary vLLM BPF-loop/native libraries and launchers. Default8 HF native
also builds successfully (build_hf8.status.json). Original root build outputs
are preserved; no private source/include-precedence patch is needed.

The initial setup exits1 after successful builds because cuda-python and
cuda-bindings select newer transitive versions. setup.initial_exit.json and
packages_initial.json retain that failure. restore_packages.py then restores
12.9.7/12.9.9 in this test-only runtime; dependency_repair.json, pin_repair logs
and setup.exit.json record the actual repair. package_comparison.json is empty:
all installed versions match0064 before any GPU serving. The first setup
attempt is not represented as successful. Base packages are preserved.

## Actual runtime qualification

The single wrapper runs2026-10-15T16:21:54.764720UTC through
17:01:58.070030UTC; validation.exit.json is0. It uses the normal newly built
libraries, not the original root build. Cold bootstrap includes upstream JIT,
model loading and graph capture; no startup/request timing is promoted to a
new performance result.

Six traced vLLM protocol executors pass6416 outcomes,including2578 intended
rejections,with235552 independently replayed tokens. Default8 native and16
BPF-loop/native run both checkpoints. Actual batches cover1..8/1..16.
Wire bytes,independent upstream graph/head/KV/history replay,fragmentation,
reuse,pipelines,half-close,invalid inputs,stop and final ownership/queue drain
pass. These are not6416 successful inference replies.
protocol_summary.json preserves individual executor counts. The default8
kernel path's code/header are unchanged and its full protocol is not repeated.

Four ordinary default8 native lifecycle cases pass:HF/vLLM with Qwen and Smol.
Each has32 actions,13 accepted connections,32 published/31 completed requests,
10 intentional rejections and652 checked output tokens. Two observed prefixes
per case cover RST/SIGTERM; cancellation/remaining bytes are not promoted to
full-response correctness. All FIFO queues drain and graph_error is0.
lifecycle_summary.json and per-case results preserve those scopes.
vLLM uses the unchanged historical frozen complete-output pools; HF uses the
existing independently frozen HF oracle, with singleton exact sequences.
No pool is enlarged and no numerical tolerance is introduced. This finite
lifecycle check does not resolve general ordinary batch-history fidelity.

## Performance boundary and reproduction

The performance result remains [finding0064](../../../docs/findings/0064-batch-capacity.md):
tested traced capacity improves delivery and high-load queueing tails; native16
also improves and wins the Qwen192/s comparison. Smol same-width intervals cross
zero. TPOT adverse results and client-lag outliers remain. This integration adds
no ordinary timing, total-CPU, P99.9, arbitrary-model or general transport claim.

entry.json, source_before/source_after, integration.diff, source_binding.json,
compile_binding.json and self_review.json record source/ABI bindings. The four
archived protocol analyses require only stdlib Python and adjacent raw sidecars:

    python3 protocol_analysis.py protocol_qwen_8.jsonl
    python3 protocol_analysis.py protocol_smol_8.jsonl
    python3 protocol_analysis.py protocol_qwen_16.jsonl
    python3 protocol_analysis.py protocol_smol_16.jsonl

For a GPU reproduction,recreate packages.json and libbpf1.6.3,rebind the recorded
temporary path in setup/environment/validation drivers to an owned temporary
directory,and build the same normal-Make targets. setup.py is the actual initial
script; apply its recorded two-package repair before validation. Use the private
runtime for vLLM,and the recorded unchanged base environment for HF. Existing
model snapshots/oracles remain separate; never replace them with observed
answers from the candidate under test.

The short host snapshots bound their exact observation times and do not prove
continuous GPU isolation. final_restoration.json records actual owned-directory
removal and preserved original files/processes/packages. final_replay.json
records copied-data CPU analysis after cleanup. Upstream default JIT caches and
model weights are not deleted.
