# Batched publication in independent GPU I/O, 2026-10-14

Read plan.md and the complete independent plan/result reviews for the fixed
experiment and its evidence limits. Source base:
212a15775e924ea6b2447b3efa046ca6889022a8, original yunwei356/bpfusion-dev Workspace.

The candidate extends seven existing BF_IO_COALESCED publication conditionals to
BF_URING_BPF_LOOP in executor/io_uring_tcp.h. The three residency/start/shutdown
conditionals remain literal. Original independent per-entry I/O is a component
control; efficient native timed epoll TCP is the single main competitor.
Model computation/padding/prefix release, timer60000ns and protocol are unchanged.
The source/algorithm/layout/timing bundle is not isolated PCIe mediation.

Original control is freshly compiled in TEMP/control-build before the candidate
edit. Candidate/native/trace are compiled in TEMP/build. Raw labels
uring_loop_original/userspace/uring_loop bind those actual paths. Private entry
names all use the existing vllm_graph.py sibling-library mechanism. There is no
new public mode or saved-ELF substitution. The actual Make commands and library
linkage are retained; compile-time libbpf headers are existing system1.3 while
runtime loop libraries select private1.6.3.

Full collection contains20 drivers60 executors120 cells3840 measured requests,
124800 measured output tokens plus480 checked gen1 warmups. Raw JSONL preserves
actual commands, sources, replies, arrivals, CPU brackets and terminal status.
The primary is gen64/c8 TPS, with five paired process blocks and nominal t95df4.
All signed secondary rows and adverse blocks remain in full.analysis.json.
Ordinary performance is untraced finite frozen whole-output membership, not
fresh eager-HF parity or an observed current batch trajectory.

qualification_*.jsonl plus actual network/GPU/reference transcripts contain
fixed622-request22224-token259-reject5000-empty-connection checks per model.
Traced replay uses the same reused model graph, so it is not an external math
oracle. The earlier AMK eager-HF failure stays failed. Fixed128-record I/O
diagnostic truncation is distinct from full model event overflow.
Lifecycle directories retain actual request_hex/reply_hex/post_stop_extra_hex,
32 actions652complete-or-prefix tokens per model, physical slot/bitmap/recycle/
queue evidence and syscall traces. Intentional admitted32/retired31 is retained.

From the repository root, standard-library CPU replay:

```sh
python3 bench/results/independent_queue_batch_20261014/analysis.py bench/results/independent_queue_batch_20261014 full
python3 bench/results/independent_queue_batch_20261014/long_counter_analysis.py bench/results/independent_queue_batch_20261014
python3 bench/results/independent_queue_batch_20261014/analysis_lifecycle.py bench/results/independent_queue_batch_20261014
python3 -c 'import sys,pathlib,json;sys.path.insert(0,sys.argv[1]);import analysis;print(json.dumps([analysis.analyze(pathlib.Path(sys.argv[1])/n) for n in ["qualification_vllm_smol.jsonl","qualification_vllm_qwen.jsonl"]],indent=2))' bench/results/independent_queue_batch_20261014
```

The full analyzer regenerates full.analysis.json. Compare stdout with the retained
full.analysis.stdout; lifecycle output has a new UTC and should be compared
without that observation timestamp. final_restoration.json records actual
post-cleanup CPU replay outcomes and preservation.

For an explicitly requested new GPU reproduction, use the recorded base source
and existing Make targets in the matching Workspace. Copy recipes/references
into a fresh OS-temp directory; do not run setup.py in this archive or overwrite
old raw outputs. setup.py derives its private runtime/build directories from
its own file location, first builds the original control, asserts original
source equality, applies the captured candidate.diff and freezes candidate
sources before building candidate/native/trace. This order matters. Current
selected source may differ from the collected candidate; reproduce the original
header from original_io_uring_tcp.h and the recorded base before the controlled
build/edit sequence. Model checkpoints/revisions are in frozen_references.json.

Exact current candidate sources, original header/CUDA sources, Makefile/client,
packages, commands, build/linkage/SASS receipts and observation context remain.
Normalized ordinary dispatch SASS1864instructions matches all three paths;
this is not whole-binary or dynamic-work equivalence. Sparse host snapshots and
the existing400W GPU limit bound interpretation; they do not prove continuous
exclusivity or a clean journal.

Runtime environments, private ELF/build artifacts, libbpf download/source/install,
CUDA caches and weights are excluded. Text recipes/source/raw data/reviews remain.
Cleanup removes only this experiment's TEMP/control-build/build/runtime tree;
root shared/unowned builds, original tools/setup_env.sh, base packages and Coder
sessions are preserved. No retained service/configuration/credential entity is
introduced by this experiment.
