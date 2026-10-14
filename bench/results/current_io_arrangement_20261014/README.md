# Current GPU I/O arrangement comparison, 2026-10-14

Source-neutral completed comparison on BPFusion main
048c204ed78e006f1e31cfa8a7fb4699b7429d06. All model computation is reused.
Read plan.md, plan-review.md, result-review.md and
../../../docs/findings/0055-current-gpu-io-arrangements.md for scope and decisions.

The full run has20 drivers,60 executors,120 cells,3840 measured requests,
124800 measured tokens and480 one-token warmups. Raw JSONL contains original
metadata, clients, commands and exits. Ordinary performance is untraced;
qualification retains traced reused-graph history/KV and actual syscall records.
lifecycle_vllm_smol/ and lifecycle_vllm_qwen/ preserve actual wire bytes and
shutdown/recycle evidence. These are finite token-ID checks, not arbitrary
fresh eager-HF parity or a full text/API benchmark.

From the repository root, standard-library CPU replay:

```sh
python3 bench/results/current_io_arrangement_20261014/analysis.py bench/results/current_io_arrangement_20261014 full
python3 bench/results/current_io_arrangement_20261014/long_counter_analysis.py bench/results/current_io_arrangement_20261014
python3 bench/results/current_io_arrangement_20261014/analysis_lifecycle.py bench/results/current_io_arrangement_20261014
python3 -c 'import sys,pathlib,json;sys.path.insert(0,sys.argv[1]);import analysis;print(json.dumps([analysis.analyze(pathlib.Path(sys.argv[1])/n) for n in ["qualification_vllm_smol.jsonl","qualification_vllm_qwen.jsonl"]],indent=2))' bench/results/current_io_arrangement_20261014
```

analysis.py regenerates full.analysis.json; compare stdout with full.analysis.stdout.
The protocol analysis prints verified records before its JSON list. Lifecycle
analysis emits a current UTC; compare substantive fields rather than that time.
final_restoration.json records actual post-cleanup archive replay outcomes.

setup.py and run.py retain the actual private BUILD/runtime recipe and expanded
full.commands.json. For a new explicitly requested GPU reproduction, copy the
recipes/references to a fresh OS-temp directory; do not run setup.py in this
archive or overwrite existing logs. Restore source from source_snapshot at the
recorded base, retain the source-native /workspaces/repository location, use the
cached exact model revisions in frozen_references.json, and use the recorded
common packages/compiler/Linux7.3rc3/RTX5090 prerequisites. setup.py derives its
private BUILD/runtime from its own directory and writes environment.json;
run.py then derives the three current entrypoints and fixed matrix there.
The existing root build/bpfusion_load and build/uring_loop.bpf.o are necessary
source-native shared tools; their frozen metadata is in preserved_before.json.
The recorded commands contain original temporary paths as provenance, not a
currently retained runtime. Candidate/control/native were all freshly built via
existing Makefile targets; original root trace artifacts were not overwritten.

source_snapshot/ freezes12 source files; source_frozen.json and post_run_source.json
record base/path equality. original_*.cu/h retain additional source captures.
No production source/default/configuration changes are selected. Binary builds,
weights, package environments, libbpf download/source/install and caches are
excluded. Text recipes, complete raw results, dependency/build receipts and
host snapshots are retained. The after host snapshot is delayed to20:36:52UTC
after the19:14:43UTC run terminal; sparse observations are not proof of continuous
exclusivity. Cleanup removes only this experiment's original temporary tree,
preserving original Workspace/session/WIP/shared builds/base packages.
