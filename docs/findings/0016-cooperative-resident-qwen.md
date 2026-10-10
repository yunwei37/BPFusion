# 0016: cooperative resident Qwen and the longer-decode accuracy boundary

Observed 2026-10-10 UTC in the existing BPFusion Workspace, RTX 5090,
CUDA 13, Linux 7.3-rc3, Qwen2.5-0.5B-Instruct, eager HF fp16 oracle.

## One grid, one launch

The real-model reference now uses one resident cooperative CUDA grid instead
of one CTA. The launcher discovers the device SM count (170 on this GPU),
checks cooperative-launch support and that the kernel can reside with at
least one 256-thread CTA per SM, then launches once. There is no per-request
host launch, copy, sampling, accept or send loop.

Matrix rows and elementwise operations are distributed across the grid;
warp dot-product order and fp16 rounding boundaries remain the same as the
single-CTA reference. Attention heads are assigned to global warps. RMSNorm
and vocabulary argmax retain their original CTA-local reductions in CTA zero.
Grid barriers publish intermediate device buffers. CTA zero publishes queue
head/state, request dimensions and selected token to a shared device control
buffer, so all CTAs take the same branches and reach the same barriers.
Polling the mapped queue independently in each CTA would make barrier
participation nonuniform and could deadlock.

This follows the [CUDA cooperative groups synchronization contract](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/cooperative-groups.html):
all participating threads must reach a barrier, which makes preceding memory
accesses visible within the group. The grid must be launched cooperatively
and fit the device's residency constraints. There is no hand-built inter-CTA
spin barrier or model-specific SM-count override.

## Passing scope

```sh
make probes tools qwen
make -C module CC=gcc-15
python3 tests/resident_qwen.py
```

[The grid log](../../bench/results/resident_qwen_grid_20261010.txt) passes the
existing strict oracle: 26 requests / 208 generated token IDs, four prompts,
12 binary and 14 HTTP requests, eight concurrent clients, six pipelined
requests across ring wrap, byte-separated writes and a half-closed stream.
Kernel counters show 26 completions, 1,938 reply bytes, 5,021 accepted/closed
connections, zero abandonment, TX retries, registration failures and drops.
Strace follows all executor threads and finds no accept/receive/send calls
after ready. Module unload and BPF detach complete at shutdown. The test now removes its
three control/statistics/doorbell map pins as well, including when an oracle
assertion fails; previously only the stream link/map were removed.

After a storage-pressure eviction during baseline preparation, the same PVC and
Workspace were restored and the executor was rebuilt. The
[post-recovery run](../../bench/results/resident_qwen_grid_recovery_20261010.txt)
again passes all 26 requests / 208 tokens against the same PyTorch 2.14.1+cu130
and Transformers 5.19.0 versions. This is a workload recovery receipt, not
a new performance comparison. The
[cleanup regression](../../bench/results/resident_qwen_grid_cleanup_20261010.txt)
also passes the strict oracle and confirms removal of the remaining map pins.

Request wall times in this correctness test include one millisecond sleeps
between transmitted bytes. They are not an inference-only latency measure
or a matched serving comparison. No serving speedup or total-CPU saving is
claimed from this log.

## Failing scope and diagnostic control

The test now accepts `--gen` (within the existing queue's 1..64 output bound)
and `--executor` to exercise another binary with the same strict oracle.

```sh
python3 tests/resident_qwen.py --gen 64
python3 tests/resident_qwen.py --gen 64 --executor /tmp/bpfusion-qwen-single
```

The [64-token grid run](../../bench/results/resident_qwen_grid64_20261010.txt)
passes the first prompt but fails the second, `What is 2 plus 2?`, at output
position 21 (one-based). A control binary compiled from the previous main
commit `5302639a6826ad3311b951925e8112100d607c93` produces the **same 64 CUDA
token IDs**, including that divergence:
[the single-CTA control](../../bench/results/resident_qwen_single64_20261010.txt).
This failure was already present in the model reference; distributing work
across CTAs did not introduce it in this control.

A separate diagnostic teacher-forced the shared prompt plus the first 20 HF
tokens, generated one token, and copied the final logits only after stopping
the kernel. [Its log](../../bench/results/resident_qwen_logits_20261010.txt)
shows the decisive near tie:

| Token ID / text | HF fp16 logit | CUDA reference logit |
|---|---:|---:|
| 5145 / ` Start` | 20.671875 | 20.65625 |
| 64547 / ` Identify` | 20.671875 | 20.671875 |

HF argmax breaks the tie toward the lower ID, 5145; CUDA selects 64547.
The vocabulary-wide maximum absolute logit error was 0.044921875 and mean
absolute error 0.0071140439 at that prefix. Different floating-point reductions
are a plausible explanation, consistent with [PyTorch numerical accuracy guidance](https://docs.pytorch.org/docs/2.14/notes/numerical_accuracy.html),
but this experiment does not locate every numerical difference or establish
broader model quality. No tie bias, relaxed token assertion or replacement
oracle was added to conceal the failure.

Thus the verified exact-token scope remains the recorded eight-token cases.
The 64-token oracle is explicitly **failed**; general long-decode bitwise
agreement with HF is not claimed. This reference still uses scalar fp32
accumulation with fp16 boundaries, not tensor-core GEMM or continuous batching.
GPU text processing, robust malformed-request/error handling, completion-event
measurement, real-NIC controls and a matched serving comparison remain open.
