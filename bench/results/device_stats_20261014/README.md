# GPU-local I/O bookkeeping experiment, 2026-10-14

Supporting experiment within the retained no-steady-userspace-worker Linux
TCP/eBPF/GPU serving question. [Finding0054](../../../docs/findings/0054-gpu-local-io-bookkeeping.md)
states the completed result and source choice. [Plan](plan.md),
[plan review](plan-review.md) and [fresh independent result review](result-review.md)
retain admission, execution and interpretation.

Full collection completed20 drivers60 executors120 cells3840 measured requests
124800 output tokens plus480 one-token warmups. Both old-control primary
gen64/c8 TPS intervals cross zero. Candidate Smol loses to native; Qwen's
native contrast is inconclusive. Secondary rows and all five paired vectors
are retained. Main keeps host bookkeeping; candidate source/diff are evidence.

## CPU-only replay

From this directory, with ordinary Python3:

```sh
python3 analysis.py . full
python3 -c 'import pathlib,analysis;[analysis.analyze(pathlib.Path(n)) for n in ["qualification_vllm_smol.jsonl","qualification_vllm_qwen.jsonl"]]'
python3 analysis_lifecycle.py .
python3 long_counter_analysis.py .
```

The full analysis rewrites full.analysis.json with identical data. Protocol
replay uses the two explicit driver files, not a broad glob that includes
model references. Lifecycle stdout differs only in fresh UTC; compare its
substantive fields. These replays need no GPU or deleted experimental runtime.

## Collection and source reconstruction

run.py recorded full.commands.json before executing all20 source-native
adapter commands. Short context gen1/c8 and transfer gen1/c1,gen64/c1,gen64/c8,
32 measured requests/cell,8 sequential warmups/executor, five paired blocks.
Odd blocks reverse context/model/cell order; five of six path permutations.
Primary observations are untraced, preserving finite frozen whole-output
membership rather than pretending ordinary batch trajectories were observed.

Source base34eb2b0b7b1d282d47766a4125df2e216c952c09, original Coder Workspace,
Linux7.3rc3/RTX5090, common vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0.
Exact revisions, compiler/package/environment/model/kernel receipts and raw
stdout/strace/graph history/references are here. source_frozen.json,
source_snapshot/, original captured files, candidate.diff and
post_run_source.json distinguish collected candidate from selected main.
Old-control normalized SASS reconstruction matches3 functions4888 lines;
the compiled ELF itself and runtime/weights/libbpf source archive are omitted.

The recipes are literal historical collection/build/setup commands. Their
private TEMP paths and base-commit guards are provenance; do not blindly
execute prepare.py against a newer HEAD or assume the deleted runtime exists.
A new GPU replication must reconstruct that common private runtime, source
and fixed comparison from the recorded revisions/Make targets/expanded
commands in its matching Workspace, adapting only physical artifact paths
and preserving the oracle, computation, budgets and measurement contract.
CPU replay above is directly runnable after cleanup.

Each candidate model qualifies622 requests22224 tokens259 deliberate rejects
5000 empty connections plus reused graph trace/history/KV replay. Each
32-action lifecycle checks652 complete-or-prefix tokens and independently
empty/recycled physical state. This is finite protocol/trajectory evidence,
not fresh eager-HF arithmetic parity, arbitrary model/text reliability or AMK
acceptance. CPU brackets and sparse host snapshots are partial attribution,
not total CPU/energy or continuous isolation. All signed adverse and
inconclusive results remain available.

selected_source.json records keeping the original host-stats constructor.
final_restoration.json records owned cleanup/preservation and post-cleanup
CPU replays. Publication requires exact main commit/push and public-byte
verification; a reviewer verdict or successful trigger is not publication.
