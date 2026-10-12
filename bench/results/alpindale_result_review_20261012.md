# Independent terminal result review: AlpinDale backend qualification

Reviewer: retained independent result reviewer, with no participation in this candidate's plan review or implementation. Observation: 2026-10-12T18:43:41.769382+00:00. Original Workspace /workspaces/repository, main cc2409992601c4b840f3883cb350a61777805195.

## Verdict and next decision

- Run status: **valid / complete**.
- Tested strict-replacement hypothesis: **contradicted for both tested importer conditions**.
- Research value: **dependency-only**, with no standalone paper-performance or novelty value.
- Paper impact: **backend/checkpoint/workload boundary**; no formal RQ or direct thesis challenge.
- Next decision: close this strict replacement candidate, retain the qualified backend, and do not admit same-backend serving performance with this unqualified candidate. No unchanged rerun or numerical tuning follows from this review.
- Invalidating defects: none found.

The native extension builds and produces complete deterministic autoregressive sequences. That is distinct from qualification: **0 of32 complete sequences match the fixed eager reference**, and **0 of32 match the separately declared default-HF diagnostic**. Mode and repeat agreement do not establish correctness.

## Evidence and independent recomputation

Reviewed the [plan](alpindale_plan_20261012.md), [plan review](alpindale_plan_review_20261012.md), [actual qualifier](alpindale_qualify_20261012.py), [complete JSONL](alpindale_qualification_20261012.jsonl), [stdout](alpindale_stdout_20261012.txt), [build archive](alpindale_build_20261012.txt), and retained source/build/logs under /tmp/bpfusion-alpindale-8dv7jm6x. The archived qualifier, metadata qualifier text and actual temporary qualify.py are identical; archived stdout matches retained stdout.

Independent CPU reconstruction verifies all47 rows: metadata1, reference8, loader_compatibility1, native_build1, importer2, generation32, summary1, terminal1. No failure row exists. Terminal records exit0, consistent with the reported successful process completion and complete stdout. Numerical mismatches are preserved results rather than execution exceptions.

Generation keys exactly cover two conditions x two modes x two repeats x four prompts in the declared order, without duplicates or omissions. Every actual/eager/default array has64 IDs, all actual IDs are in vocabulary range, and every row's prompt and reference arrays match the separately archived references. Positions equal prompt_length-1+64:64,68,72,74 for prompt lengths1,5,9,11. Total actual generated IDs are2048; this is not a count of correct IDs.

| Importer condition | Eager-exact sequences | Default-exact sequences | Step/bulk agreement | Repeat agreement | Strict qualified |
|---|---:|---:|---|---|---|
| upstream theta10000 | 0/16 | 0/16 | all8 comparisons agree | all8 comparisons agree | false |
| checkpoint theta1000000 | 0/16 | 0/16 | all8 comparisons agree | all8 comparisons agree | false |

First eager mismatch indices are zero-based and identical across both modes and both repeats within each condition:

| Prompt | Prompt IDs | theta10000: first mismatch, actual/expected | theta1000000: first mismatch, actual/expected |
|---|---|---|---|
| Hello | [9707] | index3,1184/2776 | index3,1184/2776 |
| The capital of France is | [785,6722,315,9625,374] | index0,32671/12095 | index0,1112/12095 |
| Write a Python function to add two numbers. | [7985,264,13027,729,311,912,1378,5109,13] | index4,220/1378 | index4,220/1378 |
| Explain why the sky appears blue in one sentence. | [840,20772,3170,279,12884,7952,6303,304,825,11652,13] | index2,3410/10339 | index2,3410/10339 |

The two theta conditions produce different complete sequences for every prompt; neither qualifies. All suffixes remain archived. No prefix pass, EOS removal, tolerance, prompt shortening or successful-repeat selection occurred.

## Oracle independence and invocation

All reference weights and tokenizer IDs use the local frozen Qwen/Qwen3-0.6B snapshot c1899de289a04d12100db370d81485cdf75e47ca. Current config exactly equals archived config. Reference and candidate use BF16 and the declared model dimensions/tied embeddings.

Both HF reference sets are generated before native import and the loader rewrite. Eager uses full-prompt forward followed by63 cached autoregressive forwards, each selecting its own argmax. Expected outputs are never passed to native computation. The default diagnostic actually uses SDPA; it agrees with eager for cases2/3 but diverges first at index17 for Hello and index12 for France. Native failures occur earlier, so switching the reference does not rescue either condition.

Before every actual generation, Decoder.reset sets position0 and zeros both KV buffers. All prompt IDs except the last are ingested via step, then the last prompt ID enters64 native autoregressive steps. Step feeds back selected tokens. Bulk passes the same weight/cache/scratch argument order and starting position as upstream Decoder.generate, directly calls generate_nosync and retains every output ID, avoiding the text/EOS-truncating convenience API. Binding and launch inspection confirms the selected token is logged and used as the next input. No teacher forcing occurs.

The first complete Hello/step call serves as real preflight inside the fixed32-sequence collection. Its numerical mismatch did not change or truncate the remaining matrix, as the plan requires. There is no selected performance run.

Concrete invocation: HF_HOME=/workspaces/.cache/huggingface python3 /tmp/bpfusion-alpindale-8dv7jm6x/qualify.py. The archived qualifier derives apparatus root from its own filename; replay requires placing it beside the pinned upstream/deps/build apparatus, rather than running the repository archive in place.

## Source, loader and build identity

Independently fetched all ten author files from revision5030e154d39ecd054df03eb4dd9c8aa8185414d1 and compared contents to the metadata pre-execution archive. All match, including CUDA, bindings, importer, build script and license. Retained actual CUDA, bindings and build source match that archive.

The only on-disk source delta is the predeclared importer loader replacement of BF16 device_map="cuda" with BF16 load followed by .to("cuda"), avoiding absent accelerate. Both conditions use it. The checkpoint-theta importer is executed in a separate Python module namespace and differs from the compatible upstream importer by exactly one10000.0 ** to1000000.0 ** literal replacement. Decoder resolves its namespace's load_weights, avoiding a cached-import condition error. CUDA arithmetic, bindings, sampling and launch sizes are unchanged.

Actual build.ninja confirms upstream defaults: sm_120a,-O3,--use_fast_math, body128blocks/512threads, head1280blocks/384threads, attention8blocks and default LDG_* settings. Official Torch extension loading produced both objects and the shared extension; .ninja_log agrees with the approximately9.398-second import/build event. Build time is diagnostic. Torch2.14.1+cu130, Transformers5.19.0 and CUDA13.0 are archived.

Setup installed only ninja1.13.2 under owned OS-temp deps, with exact pip command/output preserved. Existing CUDA and Torch extension paths are exposed only to the qualifier child. No replacement of the measured Python environment or numerical/compiler tuning is evidenced.

Pinned [author source](https://github.com/AlpinDale/qwen_megakernel/tree/5030e154d39ecd054df03eb4dd9c8aa8185414d1).

## Scope, limits and cleanup handoff

This falsifies exact-generation qualification for the frozen source, two importer conditions, checkpoint, installed stack, four prompts and sequential protocol. It does not locate a unique numerical cause or establish universal upstream failure. Arithmetic/precision, serial-prefill and model-implementation differences are not isolated. The real theta mismatch is insufficient to repair the observed qualification.

No TCP/HTTP/eBPF/shared-queue serving, device-launch eligibility, online admission, concurrent safety, worker removal, matched throughput/latency or total-CPU benefit was tested. Bulk native code still submits body/head/update kernels from a host loop and synchronizes at the binding boundary; process-global barrier/token/position state remains. Its no-sync name does not prove persistent worker-free serving. Decode-call durations exclude prefix ingestion and remain diagnostics; no cross-model gain versus Qwen2.5 FP16 is supported.

The empty before-run compute-apps observation is an endpoint receipt, not continuous isolation evidence. At review no process using this apparatus remains, no bfusion module/bpfusion pins remain, production source has no diff, and main remains frozen. Original Workspace, model cache and unrelated WIP including tools/setup_env.sh are preserved.

Temporary source/build/deps intentionally remain available for this review. Their removal is the owner's next cleanup step after complete archiving and this report; this reviewer does not delete them. Cleanup completion should not be claimed while the apparatus remains.

This review writes only this report, with no GPU run, build, production edit or Git mutation.
