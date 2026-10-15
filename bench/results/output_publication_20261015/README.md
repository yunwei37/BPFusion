# Batched token publication experiment, 2026-10-15

Original yunwei356/bpfusion-dev Workspace/main base
ea82f18b703732288b6a38a235cbc978daf4bc23. Read plan.md,
plan-review.md, result-review.md and execution-notes.md before using results.

This is a failed/incomplete performance collection, not a completed comparison.
The publisher candidate writes all selected token payloads, uses one system
fence, then publishes every produced count. DONE/recycle fences, graph/model
arithmetic, BPF/network, residency, timer and protocol are unchanged.
original_vllm_graph.cu is the saved pre-edit source; candidate_vllm_graph.cu and
source_snapshot/executor/vllm_graph.cu are the collected dirty candidate.
Source selection/restoration is recorded separately, never inferred from the
candidate snapshot.

Four intended ordinary conditions are original/candidate x loop/native, with
same reused vLLM math, checkpoints/runtime, FP16/KV, padding/prefix policies
and finite token-ID HTTP workload. No BF_TRACE/profiler in performance.
Efficient native timed epoll is the main competing orchestration mechanism;
original-loop is the component control. Both native policies prevent an
eBPF-exclusive interpretation of generic publisher effects.

Qwen preflight completes all4 conditions/all4 cells,128 measured requests/
4160tokens plus32 checked warmups. Four candidate traced protocol conditions
(two models x loop/native) each complete622requests22224tokens and259rejections,
with exact independently advanced reused-graph/KV/history replay and all-thread
network syscall checks. Four lifecycle conditions each complete32actions/
652checked complete-or-prefix tokens; native intentionally stops31/32, loop
drains32transport completions/3aborts. All retained fixed analyses exit0.

Planned full:40executors160cells5120measured requests166400tokens+320warmups.
Actual full:11Qwen serving processes exit0;10 driver-verified; pair2 original-
loop serves all136 requests but fails fixed pre-observation whole-output pool
membership. Collection stops;29planned processes, including all20Smol, are
not launched. Actual1496raw requests45848tokens include1408measured requests/
45760tokens and88warmups. Exactly one raw response is outside the frozen pool,
a gen64/c8 greeting request, with62tokens matching the closest known prefix.
No actual batch trajectory was recorded in ordinary serving. Neither valid
optimized arithmetic variation nor data corruption is established by this
untraced observation. Never extend the pool with this output, delete the row,
rerun favorable cells, or synthesize a five-block effect. The full comparison
does not select a performance improvement.

full_qwen.analysis.* is an explicit post-terminal reproduction of the unchanged
fixed analyzer; it exits1 on the failed terminal, as it must. It is not an
original successful full-analysis result. failed_full_diagnostic.json is a
read-only count/pool scan, not a relaxed acceptance path; the actual package
list matches0057 exactly.

Standard-library CPU replays from repository root:

    python3 bench/results/output_publication_20261015/analysis.py bench/results/output_publication_20261015/preflight_qwen.jsonl
    python3 bench/results/output_publication_20261015/analysis.py bench/results/output_publication_20261015/qualification_qwen.jsonl
    python3 bench/results/output_publication_20261015/analysis.py bench/results/output_publication_20261015/qualification_smol.jsonl
    python3 bench/results/output_publication_20261015/analysis_lifecycle.py bench/results/output_publication_20261015
    python3 bench/results/output_publication_20261015/analysis.py bench/results/output_publication_20261015/full_qwen.jsonl

First four must exit0 with retained outputs; last MUST exit1. Historical
absolute paths in raw metadata identify original execution, while analyzed
adjacent .gpu.jsonl/.references files resolve from the archive path.
final_restoration.json records actual post-cleanup archive replay equality,
including normalized traceback path relocation for expected failure.

For an explicitly requested fresh GPU reproduction only, copy the ordinary
recipes, original/candidate sources, model reference/configuration files and
plan into new OS TEMP in the matching Workspace. Follow recorded setup/build/
serving/run commands, source/base and dependency versions. Do not run setup
inside the archive or overwrite original evidence. This failed experiment does
not authorize an unchanged rerun or a weaker output oracle.

Private runtime, original-build/candidate-build, libbpf vendor/install/download,
CUDA extension caches, compiled ELF files, launcher symlinks and __pycache__
are excluded. Original shared builds, model/global caches, Coder sessions and
unrelated tools/setup_env.sh are preserved. Only owned TEMP is removed after
independent review release and byte equality.

host_after.json at04:11:54.668266UTC is48.731seconds AFTER full terminal
04:11:05.937568, although it was initially intended as a during-run snapshot.
No full active-GPU or midpoint observation was captured before failure.
The before/after selected warning counts remain56 and boot unchanged. Sparse
snapshots do not establish continuous exclusivity, harmless old warnings or
the numerical mismatch's cause. Existing400W power setting is unmodified.
