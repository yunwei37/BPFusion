# Long-output GPU service-time discriminator, 2026-10-14/15

Original yunwei356/bpfusion-dev Workspace, main source
458145f495789f83ff662ec6d45b216c83ff7ae8. See plan.md, the complete plan-review.md
including both follow-ups, result-review.md and execution-notes.md.

Current independent GPU io_uring BPF-loop and efficient timed epoll native TCP
use the same reused vLLM FP16 model computation. Each path has unprofiled and
profiled conditions using its same actual privately built BF_TRACE library.
Both logical traces and profiler perturbation limit transfer to ordinary
untraced serving. This is a diagnostic, not a new performance knob/default.
Production source snapshots remain unchanged.

Full commands bind two models, five blocks, four conditions:40 serving drivers,
1280 measured gen64/c8 requests81920 output tokens, plus320 excluded checked
gen1 warmups. Each serving child is followed by a separately recorded fresh
unprofiled graph/KV/history replay; both exits must0. Per-case raw JSONL stores
actual commands, sources, client arrivals/tokens, completion and CPU brackets.
Case directories contain standard trace.json.gz, model.gpu.jsonl and its
references, serving/replay logs and CPU-derived per-round timeline.json.
Checkpoint revisions and fixed pre-observation complete-output pools are in
models.json. Replayed graph math is not independent eager-HF parity.

Private source-native Make targets are vllm_graph_uring_loop_trace and
vllm_graph_user_network_wait_trace. setup.py uses private BUILD/runtime/libbpf,
reusing the original root BPF loader/object read-only. Source/native flags,
resolved dependencies and actual linkage remain; system libbpf1.3 compiles,
private1.6.3 supplies loop runtime linkage. The observation adapter is the
current model bootstrap plus prior0047 CUPTI/HES observation and recursive
query/batch catalogue, with no model math edits.

The first real preflight is failed/incomplete, preserved in failed_preflight_1:
loop/unprofiled exits0, native/profiled serves16 requests520tokens and exports
the trace but segfaults during post-profiler in-process replay memcpy, exit-11.
Do not reinterpret its completed prefix as a successful comparison.
Revision1 moves the unchanged original replay body to a fresh bootstrap for all
conditions. replay_semantic_comparison.json and preserved recipe texts record
the change. Cause of the original crash remains unestablished. The owned core
was authenticated by ELF process notes and moved from the checkout to TEMP;
its binary is excluded, while core_receipt.json and the text backtrace remain.

Second preflight reruns all four conditions and completes serving+replay0.
The first CPU analysis over it fails on one extra loop kernel: io_initialize.
Source and raw trace prove this one-thread state initializer is synchronized
before model start. Fixed analysis retains it as non-model activity and requires
exactly1 loop/0native initializer with graph/node0, one-block/one-thread geometry
and pre-model placement. Previous analyzer/error receipts remain. Raw GPU data
is unchanged; no serving cell is replaced for this classification correction.

Coverage requires exact total recursive model-kernel count, per-round node
uniqueness, ordered/nonoverlapping model groups, and whole-serve graph memcpy/
memset counts. Per-round memory-node identity is not independently established.
Model spans/union/gaps use within-GPU-trace durations. CPU anchors do not prove
an absolute clock bias, and the model epoch does not decompose the entire
client window. Controller lifetime durations are not GPU utilization.

Standard-library CPU replay from repository root:

    python3 bench/results/long_service_timeline_20261014/analysis.py bench/results/long_service_timeline_20261014 preflight
    python3 bench/results/long_service_timeline_20261014/analysis.py bench/results/long_service_timeline_20261014 full

The fixed preflight analysis exits0. The fixed full analysis MUST exit1 at
full_smol_p2_loop_profiled:113944 actual versus113947 expected model kernels.
A second deficient cell, full_smol_p4_loop_profiled, has117217/117220. The
complete planned Smol duration comparison is unavailable;18/20 profiles pass
independent coverage/identity/serial checks. Do not relax counts or pool only
complete blocks. All40 client outcomes remain usable within BF_TRACE scope.

Additional standard-library CPU replays:

    python3 bench/results/long_service_timeline_20261014/client_analysis.py bench/results/long_service_timeline_20261014 full
    python3 bench/results/long_service_timeline_20261014/coverage_diagnostic.py bench/results/long_service_timeline_20261014

The post-hoc client supplement retains all40 cells and never replaces the failed
integrated analysis. Coverage diagnostic counts do not by themselves validate
per-round identity; the independent review audits that for all18 complete cells.
The fixed analyzer rewrites derived timeline.json and, only on success,
STAGE.analysis.json. Retained full.analysis.stderr/exit.json remain failure
evidence. final_restoration.json records actual post-cleanup replay equality,
including normalized traceback paths for the expected full-analysis failure,
source/preserved-build/base/Coder checks.

For an explicitly requested new GPU reproduction, copy setup.py, adapter.py,
replay.py, case.py, run.py, analysis.py and models.json into fresh OS TEMP in the
matching Workspace; use the recorded source and existing Make targets. Do not
run setup inside this archive or overwrite original raw results. Historical
absolute TEMP/model paths identify the original execution and need ordinary
relocation. Root shared/unowned build artifacts are not reconstruction outputs.

Private runtime/vendor source/download/install, CUDA extension caches, compiled
ELFs and all .so launcher symlinks, the binary core and __pycache__ are excluded.
Text recipes/sources/raw client/model data, standard compressed GPU traces,
reviews and host/preservation receipts remain. Sparse host snapshots retain
boot, current400W power setting and old/new selected NVRM warnings without
continuous-isolation, clean-journal or harmlessness claims. Cleanup removes
only owned TEMP, not original sessions, weights, caches or shared builds.

Full collection ended2026-10-15T00:56:35.788067UTC. The late host_after snapshot
at03:13:10.644863 is2h16m34.857s later; no full midpoint exists. Selected NVRM
0x56 warnings rose36 before→56 after,20 during full. Neither missing activities
nor the earlier crash is causally attributed to these warnings. The signed
client and Qwen duration effects are inconclusive for an ordinary-serving
bottleneck; profiled Qwen TPS is locally lower than native. No source/default
change is selected and no unchanged GPU rerun follows this diagnostic.
