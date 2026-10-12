# Independent result review: official token-only vLLM comparison

Reviewed 2026-10-12 in the retained bpfusion-dev Workspace. This review read the
approved plan and plan review, published/actual driver, frozen production
sources, installed official protocol and package metadata, actual model weights,
both preflight attempts, complete full raw/stdout, primary replay analysis,
secondary source/output, and shutdown receipt. It independently reconstructed
metrics from raw timestamps/tokens/counters rather than adopting the analysis
verdict. No GPU/model/server run, production change, process signal, Git action
or extra agent was performed. Only this requested report was written.

## Separate judgments

- run status: valid for the planned finite fixed-length token-stream comparison,
  complete; not an identical-output or isolated-control-path experiment.
- tested hypothesis: mixed across declared primary metrics and loads. TTFT
  advantage is supported at gen64/clients1 and8; gen64/clients1 throughput
  advantage is supported, but concurrent gen64 throughput/TPOT advantage is
  contradicted. No general throughput/latency advantage is established.
- research value: supporting engineering evidence, not setup/dependency-only.
- paper impact: mechanism/workload boundary and useful engineering evidence;
  no formal paper RQ/thesis exists, and no direct thesis challenge is invented.
- next paper decision: retain the measured request/first-token advantage with
  its interface limits, and prioritize reusable upstream optimized computation
  and batching/scheduling integration for concurrent generation. Repeating
  unchanged dispatch ablations or tuning one model's arithmetic would not
  resolve the observed concurrent-generation gap.

This result materially changes the next implementation priority. It does not
establish that eBPF caused the gains or losses, and it does not finish the
full Linux TCP/HTTP worker-free service objective.

## Artifacts and completion

The plan is [qwen_vllm_plan_20261012.md](qwen_vllm_plan_20261012.md);
the actual adapter is [qwen_vllm_compare_20261012.py](qwen_vllm_compare_20261012.py).
The complete collection is [qwen_vllm_20261012.jsonl](qwen_vllm_20261012.jsonl),
with [stdout](qwen_vllm_20261012.stdout.txt),
[primary replay](qwen_vllm_analysis_20261012.txt),
[secondary source](qwen_vllm_secondary_20261012.py) and
[secondary output](qwen_vllm_secondary_20261012.txt).

Independent reconstruction confirms:

- 2706 rows: one metadata,2560 measured requests,40 cells,80 declared warmups,
  ten idle records,ten executor records and five authentication records.
- 40 unique (pair,mode,gen,concurrency) keys cover the exact planned5x2x2x2
  matrix once. Every cell has index0..63 once, case=index%4, and16 requests
  per prompt. No failure event, exclusion or missing cell exists.
- 83200 actual measured output tokens; each requested length is fulfilled
  with integer IDs inside the151936-token vocabulary. Warmups add2600 tokens,
  excluded from measurement as planned.
- Mode order is BPFusion/vLLM in pairs0,2,4 and vLLM/BPFusion in1,3.
  Both modes use the same cell rotation inside each pair. All five pairs remain.
- Five native process receipts each report264 publications,8580 model graphs,
  launches1,graph_error0,banks8,max_active8. All have zero drops/registration
  failures/parser invalids, llm_reserved0, and eight final FREE slots.
- All ten launching-parent wait codes are explicitly0. Child lifetime and
  upstream shutdown caveats are recorded below; parent0 is not every-child0.
- Independently observed --analyze replay has exit0. The detached collection
  wrapper's wait code was not retained; no wrapper exit status is inferred.

All request TTFT/completion/TPOT values were recomputed from start_ns and
arrival_ns. Each cell TPS was recomputed as actual tokens divided by elapsed
first-send to last-token-arrival. Stored results agree exactly with those
formulas. Request timestamps are monotonic and not earlier than request start.

## Preflight and deviations

[Default attempt](qwen_vllm_preflight_default_20261012.jsonl) preserves the
startup failure and its [stdout](qwen_vllm_preflight_default_20261012.stdout.txt).
FlashInfer sampling JIT could not find the already-installed ninja because
the absolute venv invocation did not expose venv/bin on child PATH. It
produced no competitive measurement and is not counted as BPFusion winning.

[Repaired-path preflight](qwen_vllm_preflight_path_20261012.jsonl), with
[stdout](qwen_vllm_preflight_path_20261012.stdout.txt), completes8 cells,
64 measured requests,2080 actual measured tokens and16 warmups/520 tokens.
Each mode serves40 total requests and1300 total generated tokens/model steps;
the native log independently reports1300 model graphs and no graph errors.
The earlier plan-review paragraph saying1040 total measured tokens and780
graphs/engine is an arithmetic error; it is superseded by the actual raw
counts here. The actual plan's2080 count and executed matrix are correct.

The repair adds venv/bin only to the vLLM child PATH, like ordinary activation.
No utilization0.35 fallback, eager mode, oracle alteration, precision change,
scheduler restriction or post-hoc subset was applied. Full collection uses
the same repaired path and planned workload. Preflight is executability
evidence, not a separate performance result.

## Frozen source, weights and optimization engagement

Collection metadata identifies production442ab452b38680fb4bd6aa58ff21b7ab68be4d31.
I compared every archived production source with git show at442ab45 and the
current actual file: executor/qwen_graph.py/.cu, module/bfusion_tx.c,
bpf/fusion.bpf.c and bpf/include/bpfusion_queue.h are identical. Driver_source
in raw is byte-identical to the published adapter and actual
/tmp/bpfusion-vllm-uapngodu/compare_current.py. Publication85c77fa changes no
executor/module/BPF/native computation or resident_dispatch.py source.

The [weight receipt](qwen_vllm_weight_match_20261012.json) has290 parameters
and494032768 elements. Beyond receipt consistency, this reviewer CPU-only
reopened the actual pinned safetensors checkpoint and exported binary,
converted each checkpoint parameter to fp16 and compared its uint16 bits
with the corresponding binary range. All290 parameters/all494032768
elements match; the32-byte header also matches. The tied head uses the
shared embedding. No GPU inference was used for this check.

The single external competitor is official installed vLLM0.31.0,
Torch2.13.0+cu129,Transformers5.17.0 and flashinfer-python0.7.0.post1.
BPFusion retains its own Torch2.14.1+cu130/Transformers5.19.0 distribution.
The command uses the pinned Qwen2.5-0.5B-Instruct snapshot, --tokens-only,
--dtype half, and private127.0.0.1:39404; no eager/quantized/custom-scheduler
slowdown or reduced utilization was selected.

All five actual vLLM logs confirm FlashAttention2, VLLM_COMPILE,
enforce_eager=False, FULL_AND_PIECEWISE CUDA graph configuration and
completed graph capture. Prefix caching and chunked prefill are enabled.
Actual cache sizing is2374096 tokens with max sequence length32768 and
default gpu_memory_utilization0.92. Logs report prefix hit rate0.0%;
enabling caching is not proof of cache benefit for these short prompts.
The saved engine config does not establish an actual async_scheduling=True
selection, so this review makes no claim that a particular asynchronous
scheduler was proven active. The optimized attention/compile/graph path
did engage; startup failure or disabled optimization does not explain the
full-run competitor's result.

The competitor legitimately has a larger context/cache and tensor batching,
whereas BPFusion progresses private batch1 banks. These belong to this
strongest whole-system comparison; disabling them would weaken the baseline.
They prevent attribution to just eBPF, a particular kernel, or dispatch.

## Authentication, streaming and sampling

Installed token-only sources are now preserved in
[qwen_vllm_protocol_sources_20261012.json](qwen_vllm_protocol_sources_20261012.json).
The client requests the actual /inference/v1/generate endpoint with explicit
token_ids,max_tokens1/64,temperature0,ignore_eos true,detokenize false and
stream true. Missing/invalid authentication returns401 in every vLLM
process; authenticated requests200 complete. The ephemeral API key stays
in runtime environment/headers, not benchmark commands or saved key values.

The official token-only serving function uses request.sampling_params
directly; generation_config max_tokens defaulting applies only when that
field is omitted. SamplingParams defaults repetition_penalty1.0.
Consequently the generic startup warning about the model's text-generation
repetition_penalty1.1 does not demonstrate its application to these explicit
token-only greedy requests. This inspection supports ordinary greedy argmax
semantics here, not arbitrary numerical equality between optimized kernels.

I reconstructed every vLLM request's tokens and arrival_ns by concatenating
choice.token_ids from the saved frames. They equal the stored request arrays,
prompt echoes equal the actual input and finish_reason is length. No prompt,
metadata or DONE frame is counted as an output token. DELTA semantics match
the installed protocol. stdlib HTTP transfer framing, frame fragmentation
and multiple frames/read are handled; tokens returned together share the
read timestamp. Binary BPF tokens analogously use completed four-byte tokens.
JSON/SSE framing, authentication and client/server CPU paths differ from
binary HTTP; this remains a measured interface difference, not isolated
GPU-ready latency or text/tokenization cost.

## Independent primary reconstruction

Means use320 measured requests/row for latency and five aggregate cell TPS
measurements/row for throughput. Gains are BPFusion-minus-vLLM TPS and
vLLM-minus-BPFusion latency; positive favors BPFusion. Intervals use five
paired block mean differences, df4 and two-sided t critical2.776445105.
The [planned NVIDIA definitions](https://docs.nvidia.com/nim/benchmarking/llm/metrics)
define client arrival TTFT/TPOT/completion and aggregate output throughput.

| gen | clients | mode | TTFT ms | TPOT ms | completion ms | output tok/s | exact reference requests |
|---|---|---|---:|---:|---:|---:|---:|
|1|1|BPFusion|2.263|--|2.263|439.923|320/320|
|1|1|vLLM|7.029|--|7.029|145.929|320/320|
|64|1|BPFusion|2.185|1.759|113.027|566.153|320/320|
|64|1|vLLM|8.954|1.750|119.194|536.485|80/320|
|1|8|BPFusion|14.957|--|14.957|531.275|320/320|
|1|8|vLLM|16.815|--|16.815|479.891|277/320|
|64|8|BPFusion|10.067|5.593|362.398|1407.718|320/320|
|64|8|vLLM|14.845|1.501|109.416|4713.694|161/320|

| gen/clients | metric | mean gain | nominal paired95% interval |
|---|---|---:|---:|
|1/1|TPS|+293.993|[242.449,345.538]|
|1/1|TTFT/completion ms|+4.766|[2.812,6.720]|
|64/1|TPS|+29.667|[12.636,46.699]|
|64/1|TTFT ms|+6.769|[5.644,7.893]|
|64/1|TPOT ms|-0.010|[-0.054,0.035]|
|64/1|completion ms|+6.167|[2.661,9.673]|
|1/8|TPS|+51.384|[-37.729,140.497]|
|1/8|TTFT/completion ms|+1.858|[-1.495,5.210]|
|64/8|TPS|-3305.976|[-3920.097,-2691.855]|
|64/8|TTFT ms|+4.778|[0.461,9.095]|
|64/8|TPOT ms|-4.091|[-4.316,-3.867]|
|64/8|completion ms|-252.982|[-271.206,-234.759]|

For the load-bearing concurrent gen64 condition, independently recomputed
paired TPS gains are[-3588.253698,-3449.734267,-3544.295279,-3521.827717,
-2425.769796]. TTFT gains are[2.200041,3.511127,3.241824,4.058905,10.879012].
TPOT gains are[-4.149018,-4.103333,-4.206900,-4.218927,-3.778998].
All pairs are retained. The positive TTFT effect coexists with approximately
3.35x vLLM aggregate throughput and much lower TPOT/completion; it cannot
be summarized as a broad serving win. Gen1/clients8 effects are inconclusive.
The analysis replay's signs/intervals match independent reconstruction.

## Output agreement, leakage and uncertainty

BPFusion matches the frozen independent eager-HF reference1280/1280 measured
requests. vLLM matches838/1280. At gen64/clients1, cases0/1/2 first diverge
at13/20/62 respectively; case3 matches. At gen1/clients8,43 greeting requests
first diverge at0. At gen64/clients8, case0 always first diverges at13,
case1/3 match, while greeting has58 first-token divergences,21 divergences
at62 and one exact sequence. All actual outputs/mismatches remain in raw.

Reference cases are frozen from the existing independent eager-fp16 oracle;
expected arrays only validate client output and are not fed into dispatcher
generation. No output-dependent cell exclusion, replacement oracle or
weakened BPF correctness threshold exists. Precision/kernel/batching
differences may explain vLLM disagreement, but no logit-error/quality
evaluation here proves that causal explanation or equivalent task quality.

Requested lengths, greedy semantics, IDs, prompts and checkpoint are matched.
Because actual sequences differ, the timing comparison is valid only for
the requested fixed-length token service under each implementation's actual
outputs. It cannot support identical-output superiority or quality/fidelity
equivalence. Gen1/clients1 has identical measured outputs and still has
binary-vs-SSE/runtime differences.

Five adjacent paired process blocks, four short repeated prompts, warm
compile caches and closed-loop clients bound the inference. Pair4 has
longer startup and larger vLLM latency effects, but is correctly retained.
Small nominal intervals are not familywise correction, robust P99 evidence,
production diversity, open-loop load capacity or continuous GPU isolation.
Endpoint observations do not establish isolation for the full run.
No new paper RQ, safety threshold or composite score is inferred.

## Planned secondary metrics and CPU scope

I independently recomputed all50 cell/idle CPU brackets: before/after keys
are equal, values do not decrease, and saved deltas equal the difference of
owned-group sums. The100Hz counters cover launcher process groups including
API/engine/compile children visible at read endpoints. They exclude benchmark
clients, kernel TCP/softirq and unrelated work. Equal endpoint keys do not
prove that no transient child existed between reads; do not label this a
complete system CPU/energy accounting or literal zero work.

| gen/clients | BPFusion mean group CPU us/request | vLLM mean group CPU us/request |
|---|---:|---:|
|1/1|0.000|7187.500|
|64/1|93.750|105062.500|
|1/8|31.250|2500.000|
|64/8|62.500|15531.250|

Startup means are53.031807s BPFusion and23.866430s vLLM; block ranges
49.721112-62.071191/21.985344-28.816757s. Idle group CPU seconds are
[0,0,0,0,0.01]/[0.01,0,0.01,0,0.01] over roughly one-second windows.
This contrasts with an artificial busy-poll control: official vLLM can also
sleep nearly idle. Process CPU reduction is observed in active serving but
not a total-host or kernel-inclusive savings claim.

I independently recomputed every secondary p50/p99 using sorted pooled320
requests and rank interpolation at(n-1)q, agreeing with the saved inclusive
percentiles to floating rounding. These remain descriptive. For gen64/clients8:
TTFT p50/p99 is10.954/11.792ms BPFusion versus13.692/22.856ms vLLM;
completion362.747/373.578 versus103.876/247.365ms; TPOT5.588/5.820 versus
1.431/3.648ms. No tail confidence or general P99 superiority follows.

## Lifecycle caveat and kernel receipts

The [shutdown audit](qwen_vllm_shutdown_20261012.json) correctly preserves
all launching-parent wait0 receipts and distinguishes them from child exits.
All five official vLLM logs say its process manager force-killed the remaining
EngineCore during upstream abort-style shutdown; all five BPF logs contain
Torch SubprocPool unclean exit. These happen after measurement and do not
invalidate complete requests, but contradict wholly graceful/all-child0
wording. No adapter timeout-triggered SIGKILL is observed in full raw/stdout.
The repaired stop() only handles the owned group and requires its disappearance
before executor emission. Parent0 and empty group do not erase warnings.
The detached wrapper's wait status remains unavailable.

The root-owned saved journal observation supports five full native exits,
each55176 bytes,264 completions,zero abandons/retries and19 accepted/closed
connections. Preflight has8360 bytes/40 completions. These are concrete
kernel-TX lifecycle receipts matching native/raw request counts; this reviewer
read the durable receipt and did not perform host recovery or cleanup.
Root retains final Pod/host/process/module/pin audit and temporary-env cleanup
ownership.

## Review disposition

No execution or scientific defect blocks reporting the completed scoped
comparison. Corrections required for honest reporting are: preserve the
first failed preflight; use2080/1300 for measured preflight tokens/per-engine
graphs; say ten parent exits0 rather than all engine children normally0;
disclose framework shutdown warnings; and keep numerical agreement,
interface differences, process-only CPU and missing wrapper status explicit.

The official optimized mechanism engaged; its concurrent-generation advantage
is not a startup failure or weakened-baseline artifact. Conversely lower
BPFusion first-token latency does not isolate eBPF or the removal of CPU
network work. Integrating a reusable optimized backend and then measuring
the same computation through credible userspace versus kernel/resident
request paths is a stronger next discriminator than another model-specific
math tuning campaign. The current full objective remains unfinished.
