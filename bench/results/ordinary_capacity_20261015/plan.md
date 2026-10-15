# Plan: ordinary capacity with an independent per-token numerical audit

## Retained question and paper-value admission

The user asks for complete Linux TCP/HTTP + eBPF/sockmap -> shared queue ->
resident reused real-model GPU -> asynchronous kernel TCP TX without a steady
userspace request worker, improving throughput/latency with reproducible correct
matched comparisons. There is no formal paper RQ, thesis, idea-story or
user-instruction document in this repository.

Role: supporting. Finding0064 establishes a positive BF_TRACE capacity effect,
but neither ordinary default-mode performance nor ordinary adoption. This
experiment asks whether that capacity effect survives unchanged default FP16
computation with BF_TRACE absent, while an independent model-based check
qualifies every delivered token under the explicitly limited contract below.
A positive result would provide ordinary, computation-matched evidence for
capacity integration; a fidelity failure would prohibit adoption, and absent
performance gains would retain the current capacity. A native16 win would
withhold transport-superiority claims regardless of the capacity effect.

Finding0058 already disproves completeness of the old frozen output pool.
Finding0059's batch-invariant mode is finite exact evidence but changes the
compute mode and does not answer this default-mode question. We will not
enlarge the old pool, change serving arithmetic/precision or enable batch
invariance to obtain a pass. This new proposed audit is not an exact batch-history
oracle and must be scientifically reviewed before any GPU observation.
The largest credible result is useful ordinary serving capacity with bounded
numerical/near-greedy fidelity, not universal correctness, determinism or task
quality. If that scope is insufficient for the retained correctness requirement,
reject this proposal rather than treating a weaker check as a pass.

The strongest alternative is a residency/control counterfactual for the residual
native16 gap. That is valuable, but ordinary qualification is the immediate
acceptance uncertainty for the already-positive capacity candidate. Repeating
the traced matrix or porting another model does not resolve it.

## Fixed proposed fidelity contract, requiring review

Serve both paths with the same pinned upstream vLLM default FP16 graphs, weights,
KV layout per capacity, packing/prefix release and eligible-frame FIFO native
policy as0064. No BF_TRACE, profiler or numerical audit is in timed serving.

After each serving process has exited, use the unchanged checkpoint with official
Transformers AutoModelForCausalLM in eager FP32 as an independent reference.
For every response, evaluate the prompt plus actual generated prefix causally.
At token t, compute reference logits from prompt+y[:t], independently of the
candidate token being checked. Record the reference argmax, chosen-token logit,
maximum logit, margin, rank and exact-argmax agreement. The actual previous
candidate tokens condition the reference: this is a per-prefix near-greedy
contract, NOT independent greedy-sequence equality or current FP16 batch replay.
Do not describe it as either. All prefixes are checked, not just the first token.

The proposed acceptance condition is finite logits and
max_logit - chosen_logit <= 1e-5 + 1e-3*abs(max_logit) at every step, including
warmups. These constants are fixed before observation, using PyTorch's published
FP16 tensor-comparison tolerances as an engineering numerical convention.
IMPORTANT: that convention is NOT a published end-to-end model/argmax error
bound. Its adequacy is the main scientific risk to review; it cannot be justified
merely because it accepts the previously unseen response. Exact agreement rates
and all margins remain visible, including accepted near-ties. No task-quality,
PPL, universal FP16-error or exact-execution claim follows.

A full causal forward over prompt+generated[:-1] may compute all positions at
once; causal masking and shifted indices must be checked against sequential
prefix forwards in the real preflight. Repeated identical prompt/output pairs
may reuse identical reference results, with each occurrence linked explicitly;
the cache is output checking only and never feeds serving.
The audit is offline outside all serving metric brackets, after GPU release.

Any rejected token/nonfinite reference, accounting error or complete output
mismatch under the fixed contract retains all raw results and prevents a valid
capacity-superiority/adoption claim. Stop for diagnosis; never widen tolerance,
switch mode, enlarge an accepted-output pool, exclude the row or repeat until
favorable. Preserve0058's original failure classification independently.

## Sources and reused assets

- Existing normal Makefile, dispatcher, client and source snapshots in
  bench/results/batch_capacity_20261015. Rebind paths into the new owned test
  directory; only the8/16header difference and matching builds are reused.
- vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0, NumPy2.3.5, libbpf1.6.3;
  same pinned Qwen2.5-0.5B and SmolLM2-135M revisions as0064.
- Official throughput/latency precedent:
  https://raw.githubusercontent.com/vllm-project/vllm/v0.31.0/vllm/benchmarks/serve.py
- Official numerical caveat (batching need not be bitwise identical):
  https://docs.pytorch.org/docs/2.14/notes/numerical_accuracy.html
- Testing convention, not an end-to-end guarantee:
  https://docs.pytorch.org/docs/2.14/testing.html
  Installed base torch/testing/_comparison.py confirms float16(0.001,1e-5);
  verify the pinned test runtime source before use and record it.
- Official causal logits:
  https://huggingface.co/docs/transformers/main_classes/output

The last two are a proposed engineering check, not a new standard model score
or scientific contribution. No GPU kernel arithmetic is authored or tuned.

## Comparison, workloads and metrics

Kernel16 is the candidate; kernel8 is the capacity ablation; native16 with
eligible-frame FIFO is the one strong competing serving mechanism.
Native8 is omitted because the separate native-capacity effect is already
established in0064 and is not necessary for this adoption question.

Both models, the same four short prompts, gen64, rates96/192,256 scheduled
attempts/cell, five paired process blocks:30executors60cells15360measured attempts,
983040 requested measured tokens plus240gen1warmups.
Order uses five of the six permutations of(K8,K16,N16):
(K8,K16,N16),(K16,N16,K8),(N16,K8,K16),(N16,K16,K8),(K8,N16,K16).
Each appears in all positions in the first three blocks; each pairwise
precedence is2/3 across five. Rate order rotates by block. Keep the normalized
gamma(shape1) absolute arrival schedule, seed20261015+pair, uncapped client
threads, all failures and scheduling lags. No foreign work is paused.

Primary per model: kernel16-minus-kernel8 delivered output token/s at192/s,
five paired nominal t95df4 intervals. Positive requires interval>0,zero failed
primary attempts and every delivered token qualified by the admitted fixed
fidelity contract. A CI crossing zero is inconclusive, not equivalence.
Native16 transport differences are secondary and must remain visible.
96/192connect/scheduled-origin TTFT/completion P50/P95/P99,TPOT,executor CPU,
failures and exact-reference agreement/margins are retained. TPOT and CPU
regressions cannot be hidden by throughput gains. No precise P99.9,SLO,
total CPU/energy,exclusive-bottleneck or arbitrary-backend claim.

## Execution and completion

Only original yunwei356/bpfusion-dev Workspace,/workspaces/repository/main.
Preserve original sessions,WIP,build files,base packages and defaults.
All steps are bounded test-local; no retained runtime concurrency/default
change is selected. The prior capacity TEMP is removed and must not be resumed.

After admission, adapt the existing source-native setup/load/analysis scripts:
setup.py builds matching ordinary8/16 variants with the normal Makefile;
preflight.py runs actual Qwen all three conditions at both rates,32attempts/cell;
full.py runs the complete fixed two-model matrix plus offline auditors and
analyses. Workflow:/usr/bin/python3 -u run.py in the owned test directory.
Necessary adapters will be inspectable source,not a new control framework.
Do not claim these future scripts already execute or pass.

Fold the oracle eligibility check into real preflight: independently check
the known0058 outside-pool response, existing known traced/ordinary responses,
and causal full-forward versus sequential-prefix indexing. Report exact
agreements/margins regardless of outcome. These are diagnostics,not retroactive
qualification of the old failed execution. If the fixed proposed criterion
cannot qualify the real workload, retain that result rather than tune it.

Complete all admitted serving and offline numerical checks; every process and
analysis must reach terminal. No competing GPU run. Record actual resource
bindings,ordinary startup settings and zero trace/profiler evidence.
Keep all raw outcomes and commands in one archive with plan/review, then one
different fresh result review. Sparse host samples have actual phase/time;
global CPU is not attributed service CPU. After required work,remove only
owned temporary state,verify preserved originals,replay archived CPU analyses,
document honestly and main commit/push. Target figure:TPS192 and TTFTP99 at96,
with every block,plus a table of native16/adverse TPOT/CPU/fidelity results.

This proposal authorizes no ordinary-default adoption. Its scientific
admissibility,especially the new correctness scope,is unresolved until review.
