# Completed-response drain before fresh model admission

This experiment changes one ordering condition in the existing experimental
vLLM coalesced driver. On the tested local token-ID workload it cuts gen1/c8
client TTFT versus the matched SQ-only control by about58.0% Smol and60.0%
Qwen, with fewer model rounds in the same ordinary timing processes.
Candidate superiority over native, equivalence and universal throughput gains are not
established. [Independent result review](../../bench/results/final_drain_20261014/result-review.md)
confirms the finite run and independently recomputes every mean/contrast.

## Question and intervention

The retained user objective is a complete Linux TCP/HTTP + eBPF/sockmap ->
shared queue -> resident real-model GPU -> asynchronous kernel TCP send path,
without a steady userspace request worker, improving latency/TPS while reusing
model kernels. This is a supporting experiment within that serving-path
question, not a new formal paper RQ or a model-arithmetic contribution.

Finding0052 leaves a substantial concurrent short-output native gap. SQ
consumption alone can let fresh inference start while completed responses
still await final-send CQ progress. The new hypothesis is that finishing that
ordered response frontier while the model is idle improves delivered latency
and reduces fragmented model rounds. Separate ordinary short processes
authenticate aggregate rounds without BF_TRACE's known scheduling sensitivity.
No existing measurement answers this new intervention.

After io_progress, the vLLM coalesced dispatcher delays fresh admission only
when all already-admitted model work is retired and either next_final differs
from that retired prefix or published SQ work is unconsumed. It continues
network progress until those conditions clear. This waits for final SEND/abort
CQ processing, not TCP ACK, all accepts/receives, or new requests' inference.
Already unfinished model work retains its existing eligibility. Model math,
AMK, shared I/O/BPF/ABI, timers, knobs, default/noncoalesced targets and worker
structure are unchanged; the production diff adds one net line.

The competing delivery mechanism is efficient userspace epoll TCP with the
same reused vLLM model computation. The f232 SQ-only driver is a component
control, not another external baseline. If native wins, that limits
performance claims even when the component change helps.

## Collection and reconstruction

[Plan](../../bench/results/final_drain_20261014/plan.md) and
[plan review](../../bench/results/final_drain_20261014/plan-review.md)
predeclare five paired blocks, three paths and two models. Each block uses a
short-only process context for gen1/c8 and a transfer context for gen1/c1,
gen64/c1 and gen64/c8. Odd blocks reverse contexts/models/cell order; path
order uses five of six permutations. Each cell has32 measured requests and
each executor has eight sequential gen1 warmups. These contexts differ from
finding0052, so historical numbers are not substituted as controls.

All20 drivers/60 executors/120 cells terminated successfully at
2026-10-14 15:43:07.790518 UTC:3840 measured requests/124800 output tokens,
plus480 one-token warmups =4320 complete responses/125280 tokens.
No failed, excluded, restarted or replaced serving cell occurred.
The four real preflight drivers/12 executors/24 cells completed192 measured
requests/6240 tokens plus96 warmups. Source, oracle, timeout, metrics and
evaluation path did not change during collection.

Collection used original bpfusion-dev/main base
f232b475a4663731636067c0d2a95fc52603cd82 plus the captured candidate diff.
Source was frozen before collection; all20 expanded commands were recorded
before driver execution. Old-source rebuild matches the saved old ELF's
normalized SASS (3 functions/4888 instruction lines). This reconstructs the
control; it does not claim candidate SASS equality. The common runtime uses
vLLM0.31.0, Torch2.13.0+cu129 and Transformers5.17.0; full package/build/model
revision/precision/packed-prefix receipts are archived.

## Primary delivered latency

Means are five process-block cell means; lower TTFT is better.

| Model | Path | gen1/c8 TTFT, ms | gen64/c8 output token/s |
|---|---|---:|---:|
| Smol135M | SQ-only control | 5.211340 | 5272.601679 |
| Smol135M | native epoll | 2.139125 | 5618.537296 |
| Smol135M | completed-response drain | 2.188197 | 5343.548010 |
| Qwen0.5B | SQ-only control | 6.368539 | 4560.647844 |
| Qwen0.5B | native epoll | 2.638576 | 4749.956402 |
| Qwen0.5B | completed-response drain | 2.545532 | 4616.848576 |

Signed candidate-minus-control effects use nominal paired t95 intervals
(df4, coefficient2.776445105), not simultaneous familywise intervals.

| Model | Control | gen1/c8 TTFT difference, ms | Nominal paired t95 |
|---|---|---:|---|
| Smol135M | SQ-only | -3.023143 | [-4.652360,-1.393925] |
| Smol135M | native | +0.049072 | [-0.153749,+0.251894] |
| Qwen0.5B | SQ-only | -3.823006 | [-4.731456,-2.914557] |
| Qwen0.5B | native | -0.093044 | [-0.333415,+0.147328] |

All five old-control latency differences are negative for each model.
Native differences have mixed signs and intervals crossing0. That supports
local recovery versus the component control, not native superiority,
equivalence, noninferiority or zero effect.

## Same-process model-round evidence

Each untraced primary process contains only eight sequential gen1 warmups and
32 gen1/c8 measured requests. Retained source/counters authenticate eight
warmup model rounds; subtracting them gives the measured aggregate.

| Model | SQ-only mean rounds | Native mean rounds | Candidate mean rounds |
|---|---:|---:|---:|
| Smol135M | 16.8 | 8.4 | 5.6 |
| Qwen0.5B | 17.2 | 8.0 | 6.0 |

| Model | Candidate minus | Round difference | Nominal paired t95 |
|---|---|---:|---|
| Smol135M | SQ-only | -11.2 | [-16.569389,-5.830611] |
| Smol135M | native | -2.8 | [-3.838851,-1.761149] |
| Qwen0.5B | SQ-only | -11.2 | [-13.588388,-8.811612] |
| Qwen0.5B | native | -2.0 | [-2.877989,-1.122011] |

All five contrasts against both controls are negative. This supports the
aggregate prediction together with the old-control client latency effect.
It does not authenticate individual batch membership, GPU time or exclusive
causal mediation of the latency change. Fewer rounds than native do not
establish faster delivered responses.

## Transfer and negative evidence

| Model | Candidate minus | gen64/c8 token/s difference | Nominal paired t95 |
|---|---|---:|---|
| Smol135M | SQ-only | +70.946330 | [+35.366252,+106.526409] |
| Smol135M | native | -274.989286 | [-298.534115,-251.444458] |
| Qwen0.5B | SQ-only | +56.200732 | [-43.628973,+156.030438] |
| Qwen0.5B | native | -133.107826 | [-275.972521,+9.756869] |

Smol's old-control throughput difference is positive in all five blocks
(about1.35% mean gain), while its native difference is negative in all five.
Qwen has one negative old-control difference and one positive native
difference: both intervals cross0. No universal throughput gain,
equivalence or non-regression follows.

Gen1/c1 candidate TTFT is1.192125ms Smol and1.453678ms Qwen. Differences
versus old are+0.028103[-0.041868,+0.098073] and
+0.033352[-0.058582,+0.125285]: both inconclusive. Versus native, all five
differences are positive: Smol+0.041246[+0.003834,+0.078659],
Qwen+0.066603[+0.030970,+0.102237]ms. Single-request latency superiority is
therefore contradicted. Smol also retains native losses in gen64/c1
completion/TPS/TPOT and gen64/c8 TTFT/completion/TPS/TPOT; all secondary
signed rows remain in full.analysis.json, without selection or exclusions.

Known-worker process/TX CPU decreases versus old in gen1/c8 for both models
and versus native for Qwen, but native long-output known-worker CPU remains
higher for the candidate in several cells. This attribution includes process
clock time and attributable syscall time; it omits separately unaccounted
kernel/BPF/softirq/client work and energy. It is not total CPU elimination or
universal CPU saving.

## Correctness, shutdown and scope

Each candidate model passes622 protocol requests/22224 token IDs,
259 rejections and5000 empty connections, including wrap/reuse, binary/HTTP,
pipeline and half-close. Trace/history/KV replay reruns reused vLLM graphs;
it is not fresh independent eager-HF arithmetic parity. Ordinary timing uses
unchanged frozen whole-output-pool membership. Finite pools and protocol
coverage are not arbitrary-model/context/input quality. Prior AMK strict-HF
failure and rejected policy transfer remain unchanged.

Each model's32-action lifecycle run checks652 complete-or-prefix token IDs,
13 connections,3 aborts,32 kernel completions/recycles, zero admission bitmap,
eight physical model slots FREE, balanced SQ/CQ and released buffers/links.
Reset and signal-stop intentionally check prefixes rather than all long
responses. Stop counters admit32/retire31 model requests, consistent with
the in-progress stop/abort path; that is not a full model-completion claim.
Model quiescence is supported by retained shutdown source and successful
termination, not direct sampling of the freed quiescence field.

The selected path has no steady userspace accept/recv/send worker and uses
module-free BPF-loop I/O on this tested host. Linux TCP still consumes CPU.
The experiment does not prove portability to arbitrary kernel builds.
The global ordered final frontier is retained: a backpressured earlier final
SEND can stall fresh admission across peers. These finite tests prove no
arbitrary-peer fairness, tail bound, TCP ACK completion or2^32 rollover.

Host before/during/mid/after observations at15:16:38.821197,
15:17:45.427416,15:28:02.605630 and15:43:33.590481 UTC retain the same boot
and33 older selected NVRM warnings, latest10:50:43, with no new selected fault.
During/mid observations each show one compute application; endpoints show
none. Sparse brackets do not prove continuous isolation, a clean journal or
harmlessness of the older warning.

## Replay and next decision

[Raw archive and standalone replay](../../bench/results/final_drain_20261014/)
retain sources, all commands/versions, raw traces/client records, fixed
analysis and preflight/protocol/lifecycle evidence. Full/protocol archive
replays produce byte-equal analysis stdout; lifecycle substantive fields
match excluding its fresh replay timestamp. Temporary runtime/vendor/ELF
files are not archived. Selected main keeps the exact collected vLLM condition in existing experimental
targets, with AMK/default/noncoalesced behavior unchanged.
[Source selection](../../bench/results/final_drain_20261014/selected_source.json)
and [owned-resource restoration](../../bench/results/final_drain_20261014/final_restoration.json)
record that selection and cleanup; this is not general/default promotion.

The current comparison adds local scheduling evidence and closes the large
old concurrent-short-output gap without establishing superiority to native.
Further performance work must resolve a distinct remaining uncertainty;
repeating this unchanged matrix is not another contribution.
