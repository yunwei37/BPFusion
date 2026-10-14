# Independent GPU queue publication: no demonstrated primary gain

Observation: 2026-10-14, original yunwei356/bpfusion-dev Workspace, RTX 5090.
Source base: 212a15775e924ea6b2447b3efa046ca6889022a8.

The experiment completed with valid finite protocol/lifecycle checks, but both
models' predeclared candidate-minus-original long-output throughput intervals
cross zero. Selected source restores the original independent worker publication.
No production code, default, timer, model arithmetic or persistent entity is
added. This result closes this particular intervention, not the retained
Linux TCP/eBPF/reused-compute serving objective.

## Question and intervention

Finding0055 establishes a current standalone/coalesced tradeoff, while0051
tests batching only in coalesced builds. Neither measures the missing combination
of independent resident GPU I/O with batched queue publication. This supporting
experiment tests that combination with identical reused vLLM computation.
No formal paper RQ or thesis rewrite is introduced.

Seven existing BF_IO_COALESCED conditionals in executor/io_uring_tcp.h also
accept BF_URING_BPF_LOOP. They cover round-local ring fields, finite CQ snapshot/
drain, batch head publication and normal/cancel-return SQ publication.
Three residency/start/shutdown conditionals stay unchanged. No new public
mode, kernel target, ABI or model computation is introduced. The candidate
bundles publication, layout, finite-drain and timing changes; it is not isolated
PCIe mediation. Added idle SQ cursor reads were recorded before collection
as a competing cost, not discovered and removed after looking at results.

Original per-entry independent I/O is a component control, freshly compiled
before the edit. Efficient native timed epoll TCP is the main competitor.
Candidate, native and traced candidate are freshly built in private TEMP paths.
All three ordinary dispatchers have 1864 equal normalized SASS instructions;
this does not prove whole-binary or dynamic-work equivalence.

## Fixed execution and results

[Plan](../../bench/results/independent_queue_batch_20261014/plan.md),
[plan review](../../bench/results/independent_queue_batch_20261014/plan-review.md)
and [fresh independent result review](../../bench/results/independent_queue_batch_20261014/result-review.md)
retain the full contract and evidence audit.

All20 drivers /60 executors /120 cells complete3840 measured requests and124800
output tokens, plus480 checked one-token warmups. No serving cell failed,
was excluded, restarted or replaced; oracles, metrics and timeouts were unchanged.
Five paired process blocks,32 measured requests/cell and8 warmups/executor
produce nominal paired t95 intervals with df4. They are not familywise,
equivalence or noninferiority tests.

Primary gen64/c8 client output token/s:

| Model | Original independent | Native TCP | Batched independent | Candidate-original, nominal95% CI | Candidate-native, nominal95% CI |
|---|---:|---:|---:|---|---|
| SmolLM2-135M | 5355.165 | 5620.981 | 5480.396 | +125.231 [-103.273,353.734] | -140.585 [-267.251,-13.919] |
| Qwen2.5-0.5B | 4601.708 | 4742.797 | 4575.193 | -26.515 [-270.340,217.311] | -167.604 [-374.057,38.849] |

Both candidate-original contrasts are inconclusive. Smol loses to native;
Qwen's native contrast is inconclusive despite five negative block differences.
A positive Smol mean cannot substitute for the planned uncertainty criterion.
The two-model result does not support retaining the candidate.

Gen1/c8 TTFT means in milliseconds:

| Model | Original | Native | Candidate |
|---|---:|---:|---:|
| Smol | 2.677916 | 2.422762 | 2.657209 |
| Qwen | 2.823275 | 3.195950 | 2.862127 |

All four candidate-original/native short TTFT intervals cross zero.
Gen1/c1 candidate TTFT is1.165012ms Smol and1.448930ms Qwen; these secondary
cells use this reused-graph recipe and cannot be compared as a controlled
speedup against the earlier Hugging Face table. A roughly3ms first token is
not an inherent TCP floor.

[Full analysis](../../bench/results/independent_queue_batch_20261014/full.analysis.json)
retains all24 means /72 signed metric contrasts and ordinary short counters.
[Long-counter analysis](../../bench/results/independent_queue_batch_20261014/long_counter.analysis.stdout)
authenticates serial/warmup deductions and retains every signed block.
Gen64/c8 round means original/native/candidate are279.8/262.4/263.6 Smol
and284.2/260.6/278.6 Qwen; all four candidate round contrasts cross zero.
Original Smol332, original Qwen319 and candidate Qwen324 rounds are retained
without an assigned cause or exclusion. Aggregate rounds do not identify
batch membership, GPU service time, cursor traffic or exclusive mediation.

Known-worker CPU candidate-original contrasts are inconclusive. Candidate-native
costs rise39.838us/request Smol [0.589,79.088] and64.473us Qwen [41.756,87.190].
This partial process accounting is not total CPU or energy. Removing a steady
userspace request worker does not remove kernel/timer CPU work.

## Correctness, provenance and limitations

Private setup, preflight, protocol, lifecycle, full collection and fixed
analyses all complete0. The preflight includes24 cells192 measured requests
6240 tokens and96 warmups. Per-model traced protocol checks622 requests22224
tokens,259 rejects and5000 empty connections, with real batch1..8 and KV/history
replay. Full model event overflow is zero. Fixed128-entry network diagnostic
truncation remains recorded separately.

Each lifecycle suite retains32 actions,652 complete-or-prefix checked tokens,
13 connections32 transport completions3aborts, all8 physical model slots FREE,
bitmap0/recycle32, pending/error/drop/overflow0 and independently empty SQ/CQ.
Intentional stop admits32 and retires31; this is neither hidden nor a requirement
for all interrupted computation to retire. Raw request/reply/post-stop bytes and
syscall traces are retained and independently decoded.

Ordinary performance uses finite frozen whole-output membership. Traced
qualification replays reused graph computation and is not a fresh eager-HF
math oracle. Earlier AMK eager-HF exact equality remains failed. This does not
qualify arbitrary models/text/backpressure, broad kernel portability or a
generic open-source driver contract.

Linux7.3.0-070300rc3, driver610.57.04, NVCC13.0.88,170-SM RTX5090 and the existing
400W power limit are captured. Private runtime vLLM0.31.0/Torch2.13cu129/
Transformers5.17/NumPy2.3.5 is common; base packages remain unchanged.
System libbpf1.3 supplies compile headers/linker, private1.6.3 supplies actual
loop runtime libraries; linkage receipts retain that distinction.
Sparse entry/preflight/before/during/mid/after host observations share one boot,
retain33 older selected NVRM warnings and show no new selected fault. They do
not prove continuous exclusivity, a clean journal or harmlessness of old warnings.
The after snapshot is2026-10-14T22:02:14UTC, about73 seconds after full completion.

A lifecycle observer wrapper initially lacked a json import and failed before
any child or GPU cell. The import was corrected; no lifecycle cell was retried.
The raw execution note retains this observer failure.

## Source selection and reproducibility

Both primary candidate-original intervals cross zero, so restore the exact
saved original header after independent review. The candidate diff and collected
sources remain in the [archive and replay guide](../../bench/results/independent_queue_batch_20261014/).
[Restoration receipt](../../bench/results/independent_queue_batch_20261014/final_restoration.json)
records source selection, byte equality, owned TEMP cleanup, preserved original
builds/sessions/base packages and post-cleanup archived CPU replays.
No original/unowned build or tools/setup_env.sh is removed.

The unchanged matrix is closed. Further work needs a distinct discriminator
or stronger complete-service evidence rather than another unchanged timing run.
The [literature/novelty map](../background-related-work.md) identifies substantial
overlap for generic GPU I/O/CPU-proxy removal and megakernel computation;
the ordinary Linux TCP/eBPF integration remains a candidate distinction whose
broad evidence and performance advantage are still incomplete.
