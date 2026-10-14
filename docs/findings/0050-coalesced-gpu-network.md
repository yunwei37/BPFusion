# Coalesced network progression recovers AMK throughput with tradeoffs

Advancing network state inside the existing model dispatcher recovers much of
AMK's eight-connection throughput loss. It remains slower than efficient native
TCP, increases AMK short-output latency, and reduces throughput on both tested
vLLM workloads. This optional driver intervention is not a universal default.

## Comparison and implementation

The [plan](../../bench/results/coalesced_network_20261014/plan.md) and
[plan review](../../bench/results/coalesced_network_20261014/plan-review.md)
retain finding0030's CPU-path-removal/reusable-computation question. Finding0049
showed that a non-network resident control could reproduce AMK's c8 loss.
This experiment changes network progression rather than model arithmetic.

Shared io_uring state is made durable in GPU memory. Both existing dispatchers
call one network progression round between model rounds; there is no separate
steady io_network kernel. After model quiescence, the original network worker
drains cancellation and closes using the same state. Model math, weights,
eight-bank policy, BPF/protocol, queue ABI and 60000ns timer remain unchanged.
Allocation, parent-dispatch work and launch arrangement change collectively:
this is not a pure SM-occupancy ablation or an established overlap mechanism.
The production change is 80 added/17 removed lines across the shared header,
two dispatchers and optional Make targets. Compiled dispatcher instruction
counts grow AMK 768→2328 and vLLM 1864→3536; small source size does not imply
zero GPU overhead.

All source/build/tests run in the original bpfusion-dev Workspace/main on its
RTX5090/170SMs. Candidate source is 6f15068d591f7e53469b233ae44799990866a5ea.
The component control is the actual pre-edit loop captured from 82d31c8, not
a newly refactored legacy build. Saved sources and source-native rebuild recipes
reproduce its normalized GPU SASS. Efficient native epoll TCP is the strongest
competing mechanism, with the same backend computation per workload.

AMK uses unmodified AutoMegaKernel884534c4, SmolLM2-135M93efa2f0, FP16/cpasync0,
K=1 nodes and eight private banks. vLLM uses the same Smol revision and
Qwen2.5-0.5B-Instruct7ae55760. The common temporary runtime is
Torch2.13+cu129/Transformers5.17/vLLM0.31; AMK JIT uses CUDA13 and vLLM links
CUDA12.9. Cross-backend differences are not a pure fusion comparison.

## Complete ordinary results

Five paired process blocks, three workloads, three paths and four cells
(gen1/64 × c1/c8) complete 45 executors, 180 cells, 5760 measured requests,
187200 output tokens and 360 checked excluded warmups. All actual children
exit0; no cell is excluded, replaced or restarted. Five of six path permutations
are used; cell/model order reverses on odd blocks. Residual order and shared-host
drift are uncontrolled. These are finite persistent localhost request waves,
not offered-load capacity, tail/SLO or representative arbitrary-text serving.

Means of five blocks; TTFT is client first arrival minus request send.

| Backend/model | Path | gen1/c1 TTFT ms | gen64/c8 output token/s |
|---|---|---:|---:|
| AMK Smol135M | Original loop |18.368444|158.207999|
| AMK Smol135M | Native TCP |18.233191|304.387436|
| AMK Smol135M | Coalesced |18.855103|292.745398|
| vLLM Smol135M | Original loop |1.166619|5592.135316|
| vLLM Smol135M | Native TCP |1.168969|5630.454317|
| vLLM Smol135M | Coalesced |1.224151|5070.857739|
| vLLM Qwen0.5B | Original loop |1.388454|4758.150868|
| vLLM Qwen0.5B | Native TCP |1.377194|4806.615252|
| vLLM Qwen0.5B | Coalesced |1.468127|4373.107613|

Primary AMK c8 throughput candidate-minus-original is +134.537399 token/s,
nominal paired t95 df4 [133.700193,135.374605], about85% recovery in the ratio
of means. Candidate-minus-native is −11.642038 [−12.943016,−10.341060],
about3.8% below native. AMK gen1/c1 TTFT increases +0.486659 ms versus original
[0.463594,0.509723] and +0.621911 versus native [0.588508,0.655315].
Recovery is partial and has a measured latency cost.

vLLM Smol c8 throughput changes −521.277577 versus original
[−569.818801,−472.736354], about9.3% lower, and −559.596578 versus native
[−627.945871,−491.247286]. Qwen changes −385.043254 versus original
[−411.624696,−358.461813], about8.1% lower, and −433.507639 versus native
[−471.167979,−395.847300]. Qwen gen1/c1 TTFT versus native increases
+0.090933 ms [0.027904,0.153961]. Smol latency intervals and Qwen versus
original include zero; that does not establish equivalence or non-regression.

Short-output c8 is an important secondary regression: vLLM Smol TTFT grows
2.037207→6.746152 ms and Qwen 2.635009→8.250531 versus original. Paired
increases are +4.708945 [4.080145,5.337745] and +5.615522
[4.934244,6.296800] ms. AMK improves147.890898→133.795118 ms versus original
but remains above native129.926763; its native gap is+3.868355
[1.964964,5.771745] ms. Long-output recovery must not hide these short-output
costs. These secondary results further reject a universal latency benefit.

The [full analysis](../../bench/results/coalesced_network_20261014/full.analysis.json)
retains all cells, signed block contrasts, completion, TPOT and known-worker CPU
brackets. Output TPS uses total tokens/(last arrival−first send); completion
uses last arrival−request send and TPOT=(completion−TTFT)/(gen−1).
Worker CPU is not total host/kernel CPU or energy.

## Qualification and limits

All full outputs match unchanged finite whole-output pools; model/graph errors,
ownership counters and independently empty SQ/CQ checks pass. The old stronger
AMK eager-HF exact equality failure remains failed. Ordinary batch trajectories
are not observed, and pool membership does not establish all-input parity.

Candidate protocol qualification passes 622 requests/22224 tokens/259 rejects
and 5000 empty connections per workload, including fragmentation, invalid
tokens, wrap, pipeline and halfclose. Selected vLLM traces independently replay
actual batch/KV history. Three 32-action lifecycle runs retain idle, RST/reuse,
inflight stop, pending accept/recv and 652 checked complete/prefix tokens each.
strace shows no steady userspace accept/recv/send request worker.

Two standard CUPTI/HES observations place io_initialize before model work and
the sole io_network after model-region activity for shutdown. This establishes
the observed worker arrangement, not authenticated bank/node identity or
overlap mediation. Instrumented runs do not replace ordinary performance rows.
The first preflight fails at missing vLLM in-process configuration, before CUDA;
the repaired preflight completes all nine paths. Both receipts remain.

Because the shared header also changes ordinary noncoalesced builds, a separate
source-native legacy compatibility check rebuilds current code and completes
three workloads, 40 checked replies/1048 tokens each. This is bounded backward
compatibility evidence, not the primary original-loop baseline or qualification
of every full-copy/stock variant.

Host observations before collection and after completion retain the same boot
04dc0087 and 33 selected historical/preflight NVRM status0x56 warnings, with no
additional selected fault and empty endpoint GPU application lists. The observer
at11:33UTC is explicitly late: full collection ended11:21UTC. There is no valid
in-run host snapshot, no continuous isolation or clean-journal/harmlessness claim.

## Review, reproduction and decision

The [fresh result review](../../bench/results/coalesced_network_20261014/result-review.md)
audits the full raw collection, independent outputs, intervals, implementation,
baseline reconstruction and qualification. The
[archive](../../bench/results/coalesced_network_20261014/) retains exact commands,
environment/package/source snapshots, failures, client arrivals and analyses.
Rebuild original controls with archived Makefile.original/rebuild_original.py;
build optional candidates with source-native make targets and the pinned
temporary runtime described in setup.py/environment.json. Full collection uses /usr/bin/python3 run.py full, with all model drivers
using runtime/bin/python; analysis is python3 analysis.py ARCHIVE full.
Absolute historical paths identify the original run; reproduce with a fresh
temporary directory by adapting those explicit paths.

Keep current defaults and the faster measured vLLM path. Coalescing is useful
supporting evidence for an AMK driver/resource boundary, with remaining native
gap and latency costs. The vLLM transfer rejects a universal speedup claim.
Close this unchanged matrix. Future work needs a distinct source-backed driver
hypothesis or missing generic serving capability, not an unchanged rerun or model
arithmetic sweep. Generic text/backend/SLO/performance acceptance remains open.

[Restoration](../../bench/results/coalesced_network_20261014/final_restoration.json)
records removal of owned temporary runtime/builds, preservation of default
library/base packages/Coder/PVC/unrelated WIP and byte-identical archive replay.
No new persistent service, scheduler or model runtime is retained.
