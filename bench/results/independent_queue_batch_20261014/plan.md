# Experiment Plan: batched publication in independent GPU I/O

## Research Question

Retain the user's full Linux TCP/HTTP + eBPF/sockmap -> shared queue -> resident
real-model GPU -> asynchronous kernel TCP reply path without a steady userspace
request worker, improving latency/TPS while reusing model computation.
No formal paper RQ exists; do not invent one.

Specific uncertainty: does reusing the already-qualified finite CQ snapshot and
batched SQ/CQ publication inside the existing independent GPU I/O worker improve
gen64/c8 output TPS relative to its current per-entry publication, and what
remains against efficient native userspace TCP?

## Paper-Value Admission

Role: supporting. The credible story is a model-independent driver improvement
that combines independent progress with existing batched queue handling, with
zero new public flags/targets/abstractions and no model arithmetic optimization.
The reviewer objection is that the claimed CPU-path removal still fails to beat
efficient native serving; the driver must be tested against that strongest
competitor rather than report a win over a weak implementation.

Reuse first: finding0055 demonstrates Smol independent-I/O recovery over current
coalesced (5566 versus5175TPS), with native5619; Qwen4689 versus4614 and native4811
is inconclusive, while Qwen concurrent short TTFT regresses. Finding0051 tested
batched publication only inside coalesced dispatch; that result is not a test of
the independent worker. Current independent source still performs per-entry
system-scope CQ head publication and SQ fence/tail publication. Existing traces/
counters cannot reconstruct the result of this untested combination. No unchanged
constructor rerun, historical numerical substitution, AMK rerun or tuning search.

Independent evidence is the same-worker publication intervention. A positive
primary result can select this existing algorithm for current kernel-loop builds;
negative/inconclusive result restores the exact pre-edit header and closes this
combination. Model or full-server superiority is not inferred. The intervention
changes publication frequency, finite-drain behavior, state layout and associated
scheduling collectively; it does not independently prove PCIe-access mediation.

Best alternative is a long-output GPU timeline/capacity study. The existing
publication algorithm supplies a direct, executable and low-growth intervention
before adding instrumentation or another model. Success/failure changes source
selection, and the resulting native boundary informs subsequent workload work.
This is not a new novelty claim for batching, merely supporting driver evidence.

## Expected And Alternative Outcomes

Expected: batched independent publication can reduce redundant cursor/system
ordering work while retaining independent progression. Competing explanation:
finite CQ snapshots and conservative SQ head snapshots defer critical progress,
erase a tiny gain or change request/batch timing unfavorably. No expected numeric
effect is assumed. A negative primary interval contradicts local TPS recovery;
an interval crossing0 is inconclusive and not a selection by mean alone.

## Published Precedent And Real Assets

Reuse source-native BPFusion Makefile, vllm_graph.py/.cu, current I/O algorithm,
client/protocol/lifecycle recipes and frozen output pools from finding0055.
[liburing CQ advance/iterator](https://github.com/axboe/liburing/blob/master/src/include/liburing.h)
and [SQ flush](https://github.com/axboe/liburing/blob/master/src/queue.c) batch
release publication after appropriate consumption/writes. The CUDA
[mapped-memory guide](https://docs.nvidia.com/cuda/cuda-programming-guide/02-basics/understanding-memory.html)
requires preserving host/device ordering; existing system-scope acquire/release
and the SQ system fence remain. Precedent motivates the algorithm, not a measured
GPU speedup. [Official vLLM metrics](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics)
define TTFT/TPOT; finite client token/s remains this source-native window.

Original yunwei356/bpfusion-dev /workspaces/repository/main base
212a15775e924ea6b2447b3efa046ca6889022a8. Same exact checkpoints Smol
93efa2f097d58c2a74874c7e644dbc9b0cee75a2 and Qwen
7ae557604adf67be50417f59c2c2f167def9a775, FP16 weights/KV, current padding/prefix
policy, four literal prompts, eight slots/max64 tokens, loopback token-ID
HTTP/binary. Common private vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0/
libbpf1.6.3, NVCC13.0.88 sm_120, Linux7.3rc3/RTX5090, existing400W limit.
Do not change clocks/power/kernel/driver or retain a runtime setting.

## Comparison And Source Scope

Candidate: current standalone vllm_graph_uring_loop with existing batch
publication enabled for BF_URING_BPF_LOOP. Component control: same current
standalone with exact original header/per-entry policy, built before edit using
a separate private BUILD. Main competitor: existing efficient
vllm_graph_user_network_wait native epoll TCP with identical model math.

The implementation changes only seven existing publication conditionals in
executor/io_uring_tcp.h from BF_IO_COALESCED to BF_IO_COALESCED OR
BF_URING_BPF_LOOP: ring-local fields, batched submit/publish implementation,
SQ snapshot, finite CQ snapshot/consume, CQ head publication, cancel-return SQ
publication and normal-return SQ publication. The three residency/coalesced
conditionals (global state, worker startup, shutdown-only launch) retain their
literal policy. Expected production diff7 additions/7 deletions, net0 lines.
No new macro/mode/public target/schema, timer, model dispatcher, queue ABI,
buffer ownership, TCP operation or runtime default change. SQPOLL builds and
module/native paths remain outside this candidate. Both loop-before/after BPF
targets share the algorithm, but after-CQ variant is not rerun/promoted here.

Private control BUILD creates existing vllm_graph_uring_loop targets under
TEMP/control-build. Candidate/native/trace targets use TEMP/build. Harness-only
raw labels uring_loop_original/userspace/uring_loop bind those actual paths;
they are not new public CLI modes. Freeze original and candidate source, diff,
build commands and expanded run commands before collection. All paths are
freshly built, with no saved ELF substitution. Source-native entry-relative .so
lookup supports private directories. Existing root bpfusion_load/uring_loop.bpf.o
are reused read-only; original unowned root trace artifacts are not overwritten.

Native represents the strongest runnable competing CPU request/reply mechanism;
a win bounds the driver claim. It requires this fresh matched run since source/
context/arrival patterns are not settled by published or prior local numbers.
Control is an ablation, not a second main external baseline. Equal computation/
information/precision/output/warmup/measurement budgets; no condition-specific
tuning or oracle expansion.

## Workloads And Metrics

Primary: gen64/c8 client output token/s, candidate-minus-original and
candidate-minus-native, separately per model. Secondary: gen1/c8 TTFT and all
gen1/c1,gen64/c1 TTFT/completion/TPS/TPOT/partial known-worker CPU; ordinary
short/long round counters. Retain every signed effect and negative row.

Five paired process blocks, short-only((1,8),) and transfer((1,1),(64,1),(64,8)),
32 measured requests/cell,8 checked sequential gen1 warmups/executor, odd-block
context/model/cell reversal and five-of-six path permutations. Nominal paired
t95 df4/2.776445105, not pooled-request/familywise/equivalence inference.
Short model rounds deduct8; transfer gen64/c8 deduct2088 authenticated serial/
warmup rounds with client timestamps. Whole-transfer CQ-SQ excess is descriptive
timer traffic, not per-cell GPU time or dynamic cursor counts.

Fixed correctness: ordinary untraced frozen whole-output membership and reply
status/length/arrival/accounting; candidate-only traced622-request22224-token
259-reject5000-empty-connection protocol per model, actual batch/history/KV replay;
candidate two32-action lifecycle suites with652 complete-or-prefix tokens each,
13 connections32 completed transport requests3aborts, raw bytes, all8 FREE
physical slots/bitmap0/recycle32, pending/error/drop/overflow0 and SQ/CQ each empty.
Keep intentional stop admitted32/retired31. Preserve fixed128-entry I/O diagnostic
trace truncation separately from full model-trace overflow; no criterion change.
Reviewer independently decodes raw bytes/syscalls, not only booleans.

No new fresh eager-HF parity claim: ordinary trajectories unobserved, traced
replay uses reused graph math, and prior AMK eager-HF failure stays failed.
Finite current vLLM qualification does not prove arbitrary backend/text/fairness,
total CPU/energy, offered-load/SLO or kernel portability. Static/source equivalence
is not dynamic access-count or isolated PCIe/GPU-time mediation.

## Planned Runs

| Group | Role | Workload | Paths | Repetitions | Decision |
|---|---|---|---|---:|---|
| Short+transfer | candidate/native/component control | 2 models,4 cells | batched independent/per-entry independent/native | 5 paired blocks | source selection and native boundary |
| Protocol/lifecycle | integrated qualification | candidate,2 models | batched independent | one reused suite each | invalidate incorrect publication/ownership |

Full20 drivers60 executors120 cells3840 measured requests124800 tokens plus
480 gen1 warmups =4320 complete replies125280 tokens. Real preflight4 drivers/
12 executors24 cells192 measured requests6240 tokens+96 warmups.
Cost estimate common setup/qualification plus roughly30min full collection;
this is not a deadline or runtime budget.

## Execution

All development/build/test/analysis stays in original Workspace/main. TEMP path
is recorded next to this plan. Before manifest captures eight original preserved
paths: tools/setup_env.sh, qwen_graph.so, four loop_trace artifacts, bpfusion_load,
uring_loop.bpf.o; base packages and Coder1/10909 remain.

After fresh independent plan review, setup.py installs/builds private runtime
and original control before applying the seven-line candidate, then builds
candidate/native/trace in private BUILD. Freeze source/recipe/diff before GPU
run. Run python3 TEMP/run.py preflight1 with fixed analysis, then
run_qualification.py and run_lifecycle.py/fixed analyses. After real preflight
and integrated qualification pass, python3 TEMP/run.py full writes all20 expanded
commands before execution. Keep actual live process handle through terminal;
observer timeout is not restart permission. No correctness/metric/oracle/
timeout change to pass. Preserve any failure/exclusion/deviation.

Sparse actual host before/during/mid/after snapshots retain boot/fault/app
context without continuous-isolation claims. Full completion requires all20
drivers60 executors and fixed full/long-counter analyses, plus qualification/
lifecycle. Fresh independent RESULT REVIEW follows complete collection.

## Interpretation And Reproducibility

Candidate-minus-original primary interval above0 supports this finite local
publication improvement; below0 contradicts it; crossing0 is inconclusive.
Native superiority requires candidate-minus-native above0; crossing0 proves
neither parity nor noninferiority. Model-specific outcomes stay separate.
Secondary short latency/CPU informs scoped selection and cannot replace primary
unless it invalidates correctness/fairness/exact claim.

Target table: both models' gen64/c8 TPS with all signed original/native intervals,
linked secondary rows and ordinary counters. This is a constructor/workload
boundary or additional supporting evidence, not a thesis rewrite. No repeated
unchanged tuning matrix follows.

Only after full review choose the supported source scope or restore the exact
uncommitted original header, archive complete recipes/source/raw analyses/reviews,
remove only owned TEMP, replay archived CPU analyses, verify original resources,
then commit/push main and verify public artifacts. No persistent entity/config/
credential/network/storage/model change is proposed.
