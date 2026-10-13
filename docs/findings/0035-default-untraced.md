# Ordinary untraced optimized serving

The normal packed/prefix vLLM adapter now has a complete matched untraced
comparison against the efficient native network alternative. All four
predeclared primary intervals contain zero: the tested implementation does not
establish a kernel transport latency/throughput advantage or equivalence.
The unchanged upstream computation and qualified scheduler remain useful;
their benefit must stay separate from eBPF.

[Plan](../../bench/results/default_untraced_plan_20261012.md),
[fresh plan review](../../bench/results/default_untraced_plan_review_20261012.md)
and [fresh combined result review](../../bench/results/default_untraced_result_review_20261012.md)
define and independently audit the narrow result. Source is main bd6a0a0 plus
the recorded ordinary benchmark adaptation; production native/backend/BPF/module
and compute remain unchanged. Both binaries compile BF_PAD_PREFILL and
BF_PREFIX_RELEASE with no BF_TRACE. The native60000ns wait,checkpoint/FP16/KV/
catalogue/head/sampling,wire/client and request budgets stay matched.

## Fixed output-set fidelity and its limit

Before observing any new output,the complete independent references from
finding0034 are frozen by exact prompt/gen. Each model's24 historical files
contain6732 valid and1036 rejected sequences. The valid unions contain17 keys,
Qwen22 complete sequences andSmol19. Earlier references independently advance
their own upstream histories and match actual client/compute traces.
[Frozen references](../../bench/results/default_untraced_20261012/frozen_references.json)
record pre-observation time,FP16,pinned model paths,source revision/files.

Every valid warmup/preflight/strict/measured reply must equal one complete frozen
sequence for its exact prompt/gen. No tokenwise union,prefix-only long-output
check,tolerance,served-history forcing or post-observation set expansion occurs.
All actual replies pass. This demonstrates finite qualified output-set fidelity
and lifecycle behavior with unchanged qualified production source. It is weaker
than replay of the current unobserved batching/cache/ownership trajectory: an
implementation returning another previously valid sequence could pass. Do not
call this current-batch replay,universal numerical correctness,task quality or
batch/output equivalence. Actual per-cell graph/batch/release counts remain
unobserved; analysis reports them null instead of inventing trace evidence.

## Setup,repair and complete qualification

The initial venv setup fails before serving because ensurepip is absent.
Reuse python3 -m venv --without-pip and official pip --python into the temporary
environment; original base packages remain unchanged. Installation pins
vLLM0.31.0,Torch2.13.0+cu129,Transformers5.17.0. All resolved package versions
and actual source/build/pipeline commands are archived.

The first kernel preflight passes40 requests/1048 tokens and native/page
checks,but its driver then fails on an undefined traced-only PASS-log variable.
Raw/status are retained. Setting batches=None repairs reporting only; the whole
two-transport preflight is rerun as retry1. It completes80 requests/2096 tokens
and analysis0 before strict/full collection. Numerical checks,reference values,
model/transport/cell/time formulas never change.

Four untraced strict executors complete622 requests/22224 valid tokens,
259 intentional invalid-ID rejections and5000 empty connections each:
2488 requests/88896 tokens/1036 rejections/20000 empty connects total.
Fragmentation,prompt/block edges,client concurrency1..8,wrap/reuse,mixed1/64,
pipeline/half-close,binary EOF/HTTP400,subsequent valid output and helper-thread
SIGTERM pass. Kernel after-ready all-thread traces have no serving accept/recv/
send calls; native controls engage the intended operations. Every kernel page
is reserved0/eight FREE; native published=completed=622/rejected259. All
admitted=retired,zero graph errors/overflow and normal native exits.
Executor-wide max_active is8; this is not per-cell trace reconstruction.

Both full stages complete once:Qwen23:55:40UTC2026-10-12 and
Smol00:00:31UTC2026-10-13. All20 executors/80 cells pass5120 measured requests/
166400 tokens plus160 checked gen1 warmups excluded from timing. Both analyses
exit0. No missing,failed,excluded,retried full timing cell. Initial setup/
preflight failures remain separate rather than being counted as timing rows.

## Matched client results

Each condition has320 measured requests across five alternating process blocks.
Primaries are gen1/c1 user-minus-kernel TTFT and gen64/c8 kernel-minus-user TPS.
Five blocks are the paired units,nominal two-sided t95 df4; pooled requests
do not manufacture more independent repetitions. All samples/outliers remain.

| Model | Primary | Kernel | Native | Gain favoring kernel [nominal t95] |
|---|---|---:|---:|---|
|qwen|gen1/c1 TTFT ms|1.429292|1.406550|-0.022742 [-0.066119,0.020636]|
|qwen|gen64/c8 token/s|4752.622861|4755.702361|-3.079500 [-16.750507,10.591507]|
|smol|gen1/c1 TTFT ms|1.206509|1.201046|-0.005463 [-0.042637,0.031712]|
|smol|gen64/c8 token/s|5583.712958|5571.513146|+12.199812 [-10.879697,35.279321]|


All four primary intervals contain zero. Among exploratory secondary TTFT cells,
gen64/c1 nominally favors kernel forSmol by0.025713ms[0.006852,0.044574]
and native forQwen by0.006540ms[kernel-favoring interval-0.013005,-0.000076].
These opposing tiny scoped outcomes do not imply broad superiority. Other
metrics and all five differences remain in raw analysis and independent review.
Do not subtract earlier traced means to claim a causal tracing-removal gain.

| Model / mode | gen / clients | TTFT ms | Completion ms | TPOT ms | token/s |
|---|---:|---:|---:|---:|---:|
|qwen / kernel|1 / 1|1.429292|1.429292|n/a|692.702|
|qwen / userspace|1 / 1|1.406550|1.406550|n/a|704.174|
|qwen / kernel|64 / 1|1.326702|78.031029|1.217529|819.765|
|qwen / userspace|64 / 1|1.320161|78.050122|1.217936|819.562|
|qwen / kernel|1 / 8|2.475763|2.475763|n/a|3123.462|
|qwen / userspace|1 / 8|2.480569|2.480569|n/a|3098.626|
|qwen / kernel|64 / 8|2.170073|107.646454|1.674228|4752.623|
|qwen / userspace|64 / 8|2.159406|107.588372|1.673476|4755.702|
|smol / kernel|1 / 1|1.206509|1.206509|n/a|818.011|
|smol / userspace|1 / 1|1.201046|1.201046|n/a|823.565|
|smol / kernel|64 / 1|1.114949|45.949603|0.711661|1391.768|
|smol / userspace|64 / 1|1.140662|45.935751|0.711033|1392.196|
|smol / kernel|1 / 8|1.945366|1.945366|n/a|3963.465|
|smol / userspace|1 / 8|1.903253|1.903253|n/a|4041.512|
|smol / kernel|64 / 8|1.750315|91.607218|1.426300|5583.713|
|smol / userspace|64 / 8|1.740009|91.787001|1.429317|5571.513|


TTFT measures first complete client-token arrival minus send start; completion
uses last arrival; TPOT is first-to-last divided by gen-1; throughput uses first
send to last arrival for the whole cell. TCP/client coalescing remains included.
Definitions follow [official vLLM metrics](https://docs.vllm.ai/en/v0.31.0/design/metrics/).
These are client deliveries,not GPU-ready or decode-kernel timers.

Cross-transport full sequences match320/320 in both c1 lengths for each model.
Qwen gen1/c8 is297/320 andgen64/c8 is294/320. Actual concurrent output/batch
trajectories can differ; every actual output is a previously independently
qualified complete sequence. Smol and both first-token counts are in the
[Qwen diagnostics](../../bench/results/default_untraced_20261012/qwen_output_agreement.json)
and [Smol diagnostics](../../bench/results/default_untraced_20261012/smol_output_agreement.json).
Do not turn membership success into identical-output timing or task quality.

## Receipts,reproduce and decision

The bounded host kernel-journal search23:36:58→00:01:51UTC finds no listed
fault matches. This is not continuous host/GPU isolation or absence of
interference. Post-run receipt records no own process/module/pins/GPU app,
same boot/base runtime and original Workspace UID Running/Ready with0 restarts.
No attributed total service CPU,energy,physical-network,external SOTA,
arbitrary-backend or full-text/API claim follows.

- [Qwen full raw](../../bench/results/default_untraced_20261012/qwen_performance.jsonl)
  and [complete reconstruction](../../bench/results/default_untraced_20261012/qwen_performance_analysis.stdout.txt).
- [Smol full raw](../../bench/results/default_untraced_20261012/smol_performance.jsonl)
  and [complete reconstruction](../../bench/results/default_untraced_20261012/smol_performance_analysis.stdout.txt).
- [Serving/build source snapshots](../../bench/results/default_untraced_20261012/serving_sources.json)
  and [repaired actual pipeline commands](../../bench/results/default_untraced_20261012/pipeline_retry1_commands.json).
- [Initial preflight raw](../../bench/results/default_untraced_20261012/preflight.jsonl)
  and [complete real retry](../../bench/results/default_untraced_20261012/preflight_retry1.jsonl).
- [Qwen strict](../../bench/results/default_untraced_20261012/qwen_correctness.jsonl)
  and [Smol strict](../../bench/results/default_untraced_20261012/smol_correctness.jsonl).
- [Resolved runtime](../../bench/results/default_untraced_20261012/resolved_packages.json),
  [bounded journal](../../bench/results/default_untraced_20261012/host_journal.json),
  [owner](../../bench/results/default_untraced_20261012/owner_receipt.json)
  and [Workspace](../../bench/results/default_untraced_20261012/workspace_receipt.txt) receipts.

After fresh result review, the
[final restoration receipt](../../bench/results/default_untraced_20261012/final_restoration.json)
records removal of this run's temporary runtime and eight owned build outputs,
with no serving GPU process, module or pins and unchanged base packages/boot.
Original Coder processes and unrelated tools/setup_env.sh remain preserved.

Use the documented temporary pinned runtime and build the ordinary two binaries.
From the repository root:

    python3 bench/vllm_serving.py --untraced --reference-path bench/results/default_untraced_20261012/frozen_references.json --model PINNED_MODEL_PATH --correctness --output /tmp/fresh-correctness.jsonl
    python3 bench/vllm_serving.py --untraced --reference-path bench/results/default_untraced_20261012/frozen_references.json --model PINNED_MODEL_PATH --output /tmp/fresh-performance.jsonl
    python3 bench/vllm_serving_analysis.py RAW

Model paths and exact working commands are in the frozen asset and pipeline;
older traced archives still analyze byte-identically. --preflight is setup
evidence only and does not fabricate paired timing statistics.

Run valid/complete for this finite-set untraced contract; transport prediction
inconclusive; research role supporting; impact implementation/workload boundary.
Close this unchanged matrix. Earlier dynamic traced replay/prefix-policy gains
remain separate. Full-service CPU/strong host scheduling/general service evidence
remain open under the retained objective; do not manufacture novelty from this
qualification or request more unchanged matrix repetitions.
