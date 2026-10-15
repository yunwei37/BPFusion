# Upstream batch-invariant ordinary serving experiment

Original Workspace/main base3cb7685f368195a1d398ca9639a143df99e64a28;
observed2026-10-15UTC. No production source/default change.

Read [plan](plan.md), [plan review](plan-review.md), [fresh result review](result-review.md)
and [finding0059](../../../docs/findings/0059-batch-invariant-serving.md).
The official-reference/setup steps are dependencies, not a determinism
contribution. This is a finite same-mode serving comparison.

## Outcome and scope

Both official controls pass394requests13120tokens/model before serving.
One exact serial official64-token sequence per prompt is frozen; later
official widths1..8/forward-reverse and every accepted serving output must
match it or its prefix. No observed BPFusion variant enters the oracle.

Real Qwen preflight passes both paths. All four protocol/history/network
suites pass622requests22224tokens each, including259 intentional rejections.
Full20executors80cells deliver2560 measured requests83200tokens plus160
checked warmups. All driver/fixed analysis exits0; terminal05:22:02.721225UTC.
Primary loop-minus-native gen64/c8 TPS intervals cross zero for both models.
Concurrent long-output TTFT is adverse for loop. See complete signed review
tables, outliers and CPU limits; no default promotion/speedup follows.

This mode changes upstream computation relative to prior default-mode runs.
It cannot explain0058, establish default-mode ordinary fidelity, quantify
mode overhead or total CPU, or imply arbitrary-model/text API support.

## Raw artifacts

- reference.py, qwen/smol.official.jsonl, qwen/smol.frozen.json and
  frozen_references.json: independent official generation, width/order checks
  and exact single-sequence expected tokens, frozen before serving.
- serving.py/analysis.py: private adaptations of source-native benchmark;
  vllm_graph.py adds only private root and effective-mode assertion/logging.
  *.diff and source/ retain exact executed changes and ten original sources.
- setup.py/run.py, *.commands.json, *.statuses.json, *.exit.json,
  *.pid.json, environment.json, packages.json and install/build/linkage
  records retain the actual workflow, versions, commands and terminal evidence.
- preflight_*, qualification_* and full_* JSONL/stdout/stderr retain all
  requests, cells, errors/counters, syscall traces, GPU logical histories and
  independent graph/KV/history replay outputs. The ordinary full has no
  BF_TRACE/profiler; trace_overflow counters distinguish bounded network reply
  diagnostics from model logical tracing.
- Six host_*.json receipts retain entry, official-active, full-active and after
  observations. GPU PID namespace/cgroup identity maps to the original
  Workspace. Two full samples are bootstrap observations; sparse endpoints
  do not prove continuous isolation. Selected56historical warning arrays and
  boot/400W setting are unchanged. After is76.153428s after wrapper terminal.
- preservation_after_run.json and final_restoration.json retain original
  setup/build metadata, base packages/Coder starttimes, unchanged sources,
  absence of owned processes/module/pins, dependency removal and CPU replay.
  execution-notes.md records pre-observation fixes and post-run stale-diff
  correction. The three read-only extracted upstream inspection files are
  omitted; wheel_provenance.json identifies the official pinned wheel/source.
  No runtime, binary, vendor build tree, model weights or symlinks are included.

## CPU recomputation

From this archive directory, Python3.12 standard library suffices:

```sh
python3 analysis.py preflight_qwen.jsonl
python3 analysis.py qualification_qwen.jsonl
python3 analysis.py qualification_smol.jsonl
python3 analysis.py full_qwen.jsonl
python3 analysis.py full_smol.jsonl
```

Each returns0 and reproduces its saved *.analysis.stdout/.stderr exactly.
The root and fresh reviewer independently reran all five after cleanup;
archive-copy replay is also recorded. This is recomputation, not another
GPU run or statistical replication.

## Recorded GPU execution

Inside the owned OS TEMP in the original Workspace, the literal sequence was:

```sh
python3 run.py setup
python3 run.py reference
python3 run.py preflight
python3 run.py qualification
python3 run.py full
```

The recorded scripts preserve original absolute paths, source-base and
preservation checks; they are evidence of that Workspace execution, not a
relocatable fresh-clone installer. GPU reruns require the matching source
snapshots, pinned runtime and checkpoint revisions, Linux/BPF/CUDA environment
and corrected experiment-local paths. Existing README/make serving entrypoints
remain authoritative. Do not treat old PID/path receipts as live authority
or run historical cleanup against current unrelated state.

Runtime pins are vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0/NumPy2.3.5,
libbpf1.6.3 and NVCC13.0.88. Only the official test-local
VLLM_BATCH_INVARIANT=1 was requested beyond the existing in-process bootstrap.
Upstream chose subsidiary mode settings; no local model/driver/clock/timer
tuning was added. Full packages/config/source/compile commands remain above.
Shared global compilation caches are preserved and limit cross-run equivalence.

All owned runtime/build/libbpf resources were removed; original eight paths,
base Torch2.14.1/Transformers5.19.0/NumPy2.5.3, Coder PID1/10909 and unowned
tools/setup_env.sh remain preserved. The comparison is closed; the broader
serving/performance objective is still active.

The owned OS TEMP source/raw directory was removed after a byte-equal archive
copy. All five CPU analyses were rerun from the archive with the TEMP absent
and still reproduced identical exit/stdout/stderr; final_restoration.json
records this final archive-cleanup observation separately.
