# Adaptive kernel-loop wait experiment

Observed2026-10-15 UTC on main base d87b8e0bc1584123f2c0296ae13ab2dac999a2d6.
Read [plan](plan.md), [plan review](plan-review.md),
[result review](result-review.md) and
[finding0060](../../../docs/findings/0060-adaptive-kernel-wait.md).

The repaired finite traced matrix completes30 executors/60 cells/1920 measured
requests/62400 tokens plus240 warmups. Primary executor CPU/request decreases
in both models. Smol achieved fixed-burst wall TPS worsens versus fixed;
original production behavior is selected. No default/code change is retained.

## Recompute on CPU

Python3 standard library, from this directory:

```sh
python3 analysis.py preflight_qwen.jsonl
python3 analysis.py qualification_repaired_qwen.jsonl
python3 analysis.py qualification_repaired_smol.jsonl
python3 analysis.py full_qwen.jsonl
python3 analysis.py full_smol.jsonl
```

The first five exit0 and reproduce saved analysis stdout/stderr byte-for-byte.
The independent reviewer recomputes all12 metric rows and78 signed contrasts;
see reviewer-recomputation.md for full tables and descriptive cold-wave subset.
The latter script records its original TEMP base; inspect its source before
relocating that optional independent recomputation. The fixed analysis is
archive-relative. Replaying arithmetic is not another GPU replication.

## Recorded GPU execution

Inside the original owned OS TEMP, actual sequence:

```sh
python3 run.py setup
python3 run.py preflight
python3 run.py qualification
python3 rebuild_signal.py
python3 run.py qualification_repaired
python3 run.py full
```

Qualification attempt1 failed natural helper-stop liveness and was manually
cleaned; its raw PASS is not a valid lifecycle pass. The repaired protocol and
lifecycle runs precede full, with no oracle/timeout/metric relaxation.
The scripts preserve literal paths, source-base checks and ownership context;
they document historical execution rather than a relocatable installer.
A GPU rerun requires source snapshots, recorded dependencies/environment,
matching hardware/kernel and normal benchmark-local ownership coordination.

## Contents and limits

- plan/reviews/execution-notes, expanded commands/statuses/exits and raw JSONL,
  stdout/stderr, strace, logical histories and independent reference outputs
  preserve all failures, repaired and full observations.
- production-original/, production-candidate/ and production-patch/ retain the
  true three-file source intervention. original/ and candidate/ preserve private
  builds, including BPF path rewrites; the earlier io_uring_tcp.h.diff contains
  adapter path noise and is not the true production patch.
- source/ preserves source-native benchmark/client/model adapters; setup/build/
  package/environment records identify exact executed dependencies. No model
  weights, wheel/runtime trees, binaries or global caches are included.
- compatibility.py, serving_after.py, serving_coalesced.py, compat_* and
  candidate/Makefile.compat are prepared-only, unexecuted dependency adapters.
  Do not treat them as passes or part of the full comparison.
- host_*.json are sparse observations. Both during-full samples are pre-ready
  bootstrap. The after receipt is537.969 s late; all selected warning arrays
  match, but continuous serving exclusivity and fault harmlessness are unproven.
- final_restoration.json/source-selection.json retain preservation and cleanup.
  Shared original build files, unowned tools/setup_env.sh, base packages, Coder
  processes, weights and global caches are preserved.

BF_TRACE default optimized computation is checked against independent exact
graph/KV/history replay. This does not qualify ordinary untraced trajectories
or repair finding0058. Native uses fixed60us idle epoll waiting; there is no
adaptive-native CPU superiority claim. Process CPU is partial accounting,
wall TPS includes quiet gaps, and nominal five-block intervals crossing zero
do not imply equivalence or no delivery penalty.

The raw serving.py.diff retains a blank diff-context line with trailing space;
its byte-preserved archival form is excluded from the whitespace check. Authored
documentation and all remaining staged files pass that check.
