# Result review: packed mixed prefill/decode

## Independent verdict

- Run status: **valid and complete for the admitted, equally BF_TRACE, finite completed-request comparison**.
- Tested primary hypothesis: **supported for Qwen and supported for Smol at 96 requests/s**.
- Research value: **supporting** constructor/execution-adapter evidence.
- Paper impact: **additional evidence within the existing serving/performance question, with a mechanism/workload boundary**. It is not a direct thesis challenge and does not establish eBPF performance superiority.
- Next decision: retain this qualified packed constructor as a useful candidate, preserve the equally improved native comparator, and report the actual TPOT benefit and adverse/inconclusive secondary effects. Adoption requires the separately unresolved changed-constructor lifecycle/integration coverage. Do not promote default16, ordinary-build fidelity, a general latency/throughput win, or arbitrary-model support from this run.

This is the single fresh result review of the completed run. I read the approved plan and plan-review follow-up, actual and frozen sources, build and alignment receipts, command/status/exit receipts, preflight, both complete protocol runs, all 40 full executors and all 80 cells, traces, reference files, fresh-metadata sidecars, and both full analyses. No GPU rerun, package change, production-source edit, paper edit, or Git action was performed by this reviewer.

## Completion, source binding, and deviations

The source parent is main cf6bfeecc8cbe002350846b8772a23f7f631c01f. Original C++ is byte-identical to that commit. All corresponding actual files compare byte-for-byte equal to frozen_sources. Both private launchers in each variant point to that variant's actual Python source; both conditions use16 banks and BF_TRACE through the same Make recipes, precision and pinned upstream packages. The package comparison contains no difference. Setup and initial original/mixed builds exited0; the candidate's pre-execution trace-layout rebuild exited0. The preflight, Qwen qualification, Smol qualification and full stages all exited0, with full terminal at2026-10-15T19:09:42.442525UTC.

The trace alignment was made before GPU execution. Actual/frozen Trace reuses the admission gen word for compute input_tokens via a kind-tagged union; record payload layout is equal. The earlier mixed.cu.diff still describes the pre-alignment extra field. This is a documentation/reproduction discrepancy, not an executed-source ambiguity: preserve its historical identity or regenerate the derived final diff before publication. Actual/frozen source and trace_alignment.diff/md are authoritative.

The plan-review follow-up explicitly narrowed newly executed lifecycle scope before execution. New correctness covers completed mixed requests and normal helper-thread SIGTERM after work completes. Existing unchanged transport RST/mid-generation-stop evidence is reused only for that transport scope. This run does not newly qualify mixed partial-output cancellation; no prefix acceptance relaxation occurred. No post-result primary, workload, timeout, oracle or output-pool change was found.

Full coverage is exactly40 executors,80 cells,20,480 attempts,20,480 successes,0 failed/censored requests,1,310,720 measured output tokens,plus320 checked gen1 warmups. Each model has5 paired blocks ×4 conditions ×2 rates ×256 attempts. Conditions follow the prescribed Williams-style order and rate rotation; normalized arrival offsets are identical across conditions within each block/rate. All four conditions, both models, both rates and all five blocks are retained, including outliers.

Preflight has4 executors/128 measured requests/8,192 measured tokens/32 warmups, zero failures. The four new protocol executors have5,136 outcomes including2,060 intended rejects and188,800 generated output tokens. Every actual batch width1..16 appears in each protocol executor. Each protocol executor additionally has5,000 empty-connection attempts in its driver procedure; these are connection qualification, not generated-token outcomes.

## Correctness and mechanism engagement

I independently joined every full wire request to the reference using its unique client marker, checked prompt/gen/full token equality, and reconstructed physical owner, complete generation history and FIFO releases from every admission/compute/release. All full executors have520 admissions (512 measured+8 warmups),32,776 generated tokens, zero trace overflow and complete release. Raw native FIFO and loop ring/slot counters pass the complete analyzers; no pending native admission or kernel reservation remains at each executor's terminal check.

The candidate audit performs two post-serving passes, each after zeroing this bootstrap's owned KV tensors without changing addresses. The first rebuilds histories/query offsets/positions/pages from request starts and previous reference outputs and replays the captured body/head. The second independently derives CPU query/sequence/computed/prefill state, calls source-native InputBatch/prepare_attn(for_capture=False), runs the ordinary model forward, and applies the same official logits/sampler at the same padded request geometry. Candidate-observed KV bytes are not the expected state. Exact sampled-token agreement is required; there is no tolerance, expanded accepted-output union or near-greedy criterion.

I checked all full fresh-metadata sidecars against independently reconstructed query lengths, sequence lengths, input-token counts, request padding and output tokens, including complete sidecar round counts and final checked totals. Both protocol analyzers independently reran byte-identical, as did both full analyzers. The new protocol raw compute rows also match fresh sidecar rows exactly. The protocol fresh passes check47,200 tokens per executor, with mixed-round counts Qwen loop/native170/111 and Smol217/93. This establishes finite traced exact execution on these checkpoints and histories, not arbitrary numerical equivalence or general task quality.

Mechanism engagement is real: all20 mixed full executors have actual combined prefill/decode rounds. No candidate prefill round withheld an active runnable decode request in my history reconstruction. Original constructors have zero combined rounds and many withheld decode steps. Counts below combine both rate cells and8 warmups per executor; they are logical opportunity counts, not measured GPU time or exclusive causal attribution.

## Measurement brackets and strongest baseline audit

Full-run load timing starts after resident readiness and checked warmups, includes connection creation/request handling and final cell drain, and ends before model teardown and post-serving numerical replay. Process CPU snapshots span the same service window. Neither variant's bootstrap/capture nor its replay cost is counted as service latency; this does not establish cold-start time or capture-memory efficiency. Full timing has no strace wrapper; the protocol qualification uses strace separately.

The native competitor is the actual eligible-frame-FIFO socket path with the identical mixed adapter/model/precision/capacity, not a sleeping or serialized proxy. Its protocol traces contain accept4, recvfrom and sendmsg activity and it completes every planned request. Kernel mixed protocol traces contain none of those ordinary user network calls between ready and stopped, and exactly one io_uring_enter before SIGTERM (a second enter in the wider stopped interval belongs to shutdown). Python fresh-metadata replay occurs after the stopped boundary. These receipts support the finite no-steady-userspace-network-worker path; they do not imply the Linux TCP stack, kernel progress work or all host CPU disappeared.

The interventions deliberately change graph shapes/round histories between original and mixed; claim only reuse of the same upstream operators and matched computation across transports within each constructor. It is not literally the identical kernel-launch sequence in the original-versus-mixed ablation. Actual engagement, requests, precision and oracle all remain matched. I found no comparator interface failure, omitted cell, failed-request censoring or unfair per-transport model tuning that would justify counting a baseline failure as a win.

## Independent metric recomputation

I recomputed all80 cells directly from raw nanosecond client arrivals, schedule origins, cell timing windows and CPU before/after clocks, using a separate inline calculation rather than trusting the analyzer's reported fields. All means, P50/P95/P99 values, flattened adjacent-token ITL percentiles, throughput, CPU and scheduling-lag values agree within floating-point roundoff. I separately recomputed each planned paired effect from the5 process-block statistics and nominal t95(df4); every reported primary and planned secondary contrast agrees. Full/protocol analyzer reruns additionally reproduce their saved output byte for byte.

TPOT is mean over requests of(last arrival−first arrival)/63. TTFT below is connection-begin-to-first-token; completion uses the same origin. Scheduled-origin metrics are retained separately. ITL percentiles flatten adjacent token-arrival gaps in each cell and retain zero gaps from TCP recv coalescing; they are client-observed stalls, not isolated GPU kernel times. TPS is16,384 delivered output tokens divided by the finite cell schedule-to-finish window, including drain. It is not a saturation capacity estimate. CPU is executor process CPU only and excludes complete kernel/network/host accounting.

Intervals below use5 paired process blocks, not256 supposedly independent requests. They are nominal intervals, fragile with5 blocks and not corrected across exploratory secondary metrics. P99 percell has only256 requests; averages of block P99 values are not pooled P99 and establish neither P99.9 nor a production SLO.

## Primary decision

At96/s, Qwen loop mean TPOT falls1.434478→1.230084ms (14.25%); paired delta−0.204394ms [−0.303490,−0.105298]. Smol falls1.106505→0.951180ms (14.04%); delta−0.155325 [−0.279908,−0.030742]. Every primary block effect is negative for both models. These support the declared per-model generation-latency hypothesis in this traced workload.

The native constructor also benefits: Qwen96 delta−0.244511ms [−0.415654,−0.073367], Smol96−0.193002 [−0.334299,−0.051704]. Thus the improvement belongs to shared constructor scheduling/packing, not an eBPF-exclusive mechanism.

At192/s, Smol loop TPOT additionally improves−0.237751ms [−0.357005,−0.118498], while Qwen loop's−0.126561 [−0.382055,+0.128932] is inconclusive. These are secondary scope checks; the fixed primary remains96/s.

## Tail latency, throughput and strongest competitor

Qwen loop96 completion P99 improves−16.577ms [−24.797,−8.357] and client ITL P99 improves−1.354ms [−2.336,−0.372]; its TTFT P99 change is inconclusive. Smol loop96 completion, TTFT and ITL P99 changes are inconclusive. At192/s Smol loop completion P99 improves−39.969ms [−74.208,−5.731], while its TTFT/ITL P99 changes are inconclusive. None of the loop constructor TPS effects excludes zero at either rate. Do not advertise a broad throughput or tail-latency win.

Against the strongest same-mixed native competitor, loop-versus-native TPOT/TPS/TTFT P99/completion P99 intervals cross zero at both rates for both models. This is absence of demonstrated superiority, not an equivalence test. In Qwen192, loop ITL P99 is14.722896 vs8.363234ms: delta+6.359661ms [+2.113625,+10.605697], an adverse client stall-tail result that must stay visible.

Process CPU is also adverse in important same-mixed comparisons: Qwen loop−native+0.164611ms/attempt [+0.091916,+0.237306] at96 and+0.262106 [+0.157675,+0.366537] at192; Smol192+0.104921 [+0.064064,+0.145777]. This run does not establish totalCPU/energy savings. Idle CPU reduction from an earlier mechanism cannot substitute for these active-load costs.

Qwen includes large outliers: original-loop block1/192 TTFT P99 is629.184ms and completion P99 717.682ms; original-native block4/96 scheduling-lag P99 is331.960ms. They remain in the matrix and uncertainty. Scheduled-origin latency captures client lag; connection-origin alone does not. No outlier is silently treated as a method failure or removed.

The available host_before_preflight.json is a short time-bounded read-only ownership snapshot with no listed compute app. It does not prove continuous GPU isolation, stable clocks/thermals/power, absence of host faults, or absence of competing workloads throughout the multi-hour run. Those exposure questions remain unknown in this review. Balanced ordering reduces order bias but does not repair missing continuous exposure evidence or identify the cause of outliers.

## Source growth and public scope

Original serving sources contain317 C++ +183 Python=500 lines. Candidate serving sources contain314 C++ +124 Python=438 lines; new independent replay adds118, for556 total(+56,11.2%). This intervention changes adapter metadata/packing/scheduling, uses official upstream model/attention/logits/sampling operators, and adds no locally optimized model arithmetic, new production flag, runtime plugin framework or default16. Private experiment/build/analysis code is artifact support, not an additional scientific contribution.

FlashAttention2 still advertises its upstream support level; this candidate does not override that declaration or patch attention kernels. Successful finite exact replay supports the particular mixed descriptor and graph geometry on this host, not upstream-certified arbitrary mixed-graph compatibility.

A defensible public statement is: “A traced packed mixed constructor reduces mean request TPOT by about14% at96 requests/s for both tested checkpoints; equally improved native serving also benefits, and no general eBPF performance advantage is demonstrated.” Tail tradeoffs and finite correctness limitations must accompany it.

Unsupported public claims include arbitrary-model/general-server support, drop-in vLLM/OpenAI-server compatibility, ordinary-build exact fidelity/timing, model/task-quality parity, default16 selection, full mixed cancellation safety, P99.9/SLO guarantees, saturation throughput gains, continuous host isolation, totalCPU/energy savings or exclusive eBPF novelty. Protocol limits, cache assumptions, pinned private upstream APIs, required platform/device capabilities and token-ID HTTP framing remain material user-facing setup facts.

## Next research and engineering decision

The run settles its admitted supporting question positively for generation latency, while constraining the broader performance story. Preserve the qualified candidate and raw evidence; do not repeat this same matrix to seek a better sign. If selected for main, finish changed-constructor partial-stop/reset lifecycle integration and assess ordinary default8 behavior through the existing qualification path before claiming it generally usable. OSS documentation and a clear reproducible invocation are worthwhile engineering work, not proof that performance novelty has been established.

For the original eBPF thesis, the next informative work would distinguish I/O/progress and scheduling costs against the identical improved native computation, or test an independently justified backend/workload where host dispatch lies on the critical path. Logical round counts alone do not identify that cost. Nothing in this result warrants model-specific operator optimization, deleting the strongest native baseline, broadening accepted outputs or declaring the overall goal complete.

## Complete numeric audit

Notation: KO/NO=original loop/native; KM/NM=mixed loop/native. All aggregate rows below average the five block statistics; latency/CPU units arems and TPS is output tokens/s. Signed contrast rows are candidate−baseline, with nominal paired95% interval. The all-cell table includes every planned cell, including adverse/noisy rows. Detailed additional percentiles and request-level records remain in the raw files and byte-reproduced analyses.

Review written at 2026-10-16T07:37:44.037237+00:00.

### Aggregate four-condition outcomes

|Model|Rate|Mode|TPOT mean|TPS|TTFT P99|Completion P99|ITL P99|CPU/attempt|Lag P99|
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
|qwen|96|KO|1.434478|5943.561891|21.711218|112.312047|7.792803|0.767070|10.478856|
|qwen|96|NO|1.488997|5949.583747|39.466469|163.557654|7.199641|0.614840|73.846896|
|qwen|96|KM|1.230084|5958.024750|19.611715|95.735014|6.438708|0.746678|10.520379|
|qwen|96|NM|1.244486|5821.138098|46.211046|156.602042|6.240425|0.582067|8.531889|
|qwen|192|KO|1.537976|9606.589973|323.825152|414.381382|12.887509|0.811328|15.098792|
|qwen|192|NO|1.458961|10318.044971|200.150318|289.485618|8.493752|0.455615|21.256160|
|qwen|192|KM|1.411414|10191.298810|216.896940|303.612361|14.722896|0.709861|20.927593|
|qwen|192|NM|1.407479|10517.335900|182.494170|266.003136|8.363234|0.447755|105.156571|
|smol|96|KO|1.106505|6000.144242|11.021831|83.304792|5.533276|0.698904|7.267964|
|smol|96|NO|1.137332|5995.248300|11.519060|85.414566|6.254499|0.571049|8.857394|
|smol|96|KM|0.951180|6007.005325|14.287855|75.205636|5.603806|0.706102|8.096396|
|smol|96|NM|0.944331|6010.865506|12.272031|74.012327|5.760050|0.641987|8.698877|
|smol|192|KO|1.192607|11609.950360|59.690239|133.381915|9.875637|0.532247|18.025513|
|smol|192|NO|1.209932|11529.708920|50.490329|125.389313|8.332884|0.388485|17.246160|
|smol|192|KM|0.954856|11676.170698|33.556077|93.412552|8.384659|0.466722|16.556911|
|smol|192|NM|0.966583|11708.232305|22.091160|82.496550|7.910267|0.361802|25.377680|

### All planned contrast summaries

|Model|Rate|Contrast|Metric|Signed mean|Nominal t95 low|high|
|---|---:|---|---|---:|---:|---:|
|qwen|96|kernel_schedule|tpot_ms_mean|-0.204394|-0.303490|-0.105298|
|qwen|96|kernel_schedule|connect_ttft_ms_p99|-2.099503|-11.441690|7.242684|
|qwen|96|kernel_schedule|connect_completion_ms_p99|-16.577034|-24.796655|-8.357413|
|qwen|96|kernel_schedule|scheduled_ttft_ms_p99|-1.348797|-9.227789|6.530196|
|qwen|96|kernel_schedule|request_throughput|0.225982|-0.258032|0.709996|
|qwen|96|kernel_schedule|output_tokens_per_s|14.462860|-16.514027|45.439747|
|qwen|96|kernel_schedule|executor_cpu_ms_per_attempt|-0.020392|-0.141652|0.100867|
|qwen|96|kernel_schedule|itl_ms_p99|-1.354095|-2.336121|-0.372070|
|qwen|96|native_schedule|tpot_ms_mean|-0.244511|-0.415654|-0.073367|
|qwen|96|native_schedule|connect_ttft_ms_p99|6.744577|-113.190710|126.679865|
|qwen|96|native_schedule|connect_completion_ms_p99|-6.955612|-264.240548|250.329324|
|qwen|96|native_schedule|scheduled_ttft_ms_p99|-35.259486|-245.705152|175.186180|
|qwen|96|native_schedule|request_throughput|-2.006963|-8.004116|3.990189|
|qwen|96|native_schedule|output_tokens_per_s|-128.445649|-512.263421|255.372123|
|qwen|96|native_schedule|executor_cpu_ms_per_attempt|-0.032774|-0.103315|0.037768|
|qwen|96|native_schedule|itl_ms_p99|-0.959216|-2.575396|0.656963|
|qwen|96|mixed_transport|tpot_ms_mean|-0.014403|-0.053025|0.024220|
|qwen|96|mixed_transport|connect_ttft_ms_p99|-26.599331|-110.781853|57.583191|
|qwen|96|mixed_transport|connect_completion_ms_p99|-60.867028|-234.256069|112.522013|
|qwen|96|mixed_transport|scheduled_ttft_ms_p99|-24.965882|-110.058695|60.126930|
|qwen|96|mixed_transport|request_throughput|2.138854|-3.495234|7.772941|
|qwen|96|mixed_transport|output_tokens_per_s|136.886652|-223.694946|497.468250|
|qwen|96|mixed_transport|executor_cpu_ms_per_attempt|0.164611|0.091916|0.237306|
|qwen|96|mixed_transport|itl_ms_p99|0.198283|-0.975490|1.372055|
|qwen|192|kernel_schedule|tpot_ms_mean|-0.126561|-0.382055|0.128932|
|qwen|192|kernel_schedule|connect_ttft_ms_p99|-106.928212|-425.341355|211.484932|
|qwen|192|kernel_schedule|connect_completion_ms_p99|-110.769022|-432.832409|211.294366|
|qwen|192|kernel_schedule|scheduled_ttft_ms_p99|-108.394979|-424.111353|207.321396|
|qwen|192|kernel_schedule|request_throughput|9.136076|-15.626022|33.898173|
|qwen|192|kernel_schedule|output_tokens_per_s|584.708837|-1000.065429|2169.483103|
|qwen|192|kernel_schedule|executor_cpu_ms_per_attempt|-0.101467|-0.338593|0.135660|
|qwen|192|kernel_schedule|itl_ms_p99|1.835386|-8.390363|12.061135|
|qwen|192|native_schedule|tpot_ms_mean|-0.051482|-0.129045|0.026080|
|qwen|192|native_schedule|connect_ttft_ms_p99|-17.656148|-81.201726|45.889430|
|qwen|192|native_schedule|connect_completion_ms_p99|-23.482482|-85.633875|38.668910|
|qwen|192|native_schedule|scheduled_ttft_ms_p99|-15.059302|-92.777905|62.659302|
|qwen|192|native_schedule|request_throughput|3.113921|-6.338713|12.566554|
|qwen|192|native_schedule|output_tokens_per_s|199.290928|-405.677617|804.259474|
|qwen|192|native_schedule|executor_cpu_ms_per_attempt|-0.007860|-0.017686|0.001966|
|qwen|192|native_schedule|itl_ms_p99|-0.130518|-2.545134|2.284099|
|qwen|192|mixed_transport|tpot_ms_mean|0.003936|-0.195556|0.203428|
|qwen|192|mixed_transport|connect_ttft_ms_p99|34.402770|-160.168403|228.973943|
|qwen|192|mixed_transport|connect_completion_ms_p99|37.609225|-168.063699|243.282148|
|qwen|192|mixed_transport|scheduled_ttft_ms_p99|30.148593|-170.581228|230.878414|
|qwen|192|mixed_transport|request_throughput|-5.094330|-25.935753|15.747093|
|qwen|192|mixed_transport|output_tokens_per_s|-326.037090|-1659.888163|1007.813984|
|qwen|192|mixed_transport|executor_cpu_ms_per_attempt|0.262106|0.157675|0.366537|
|qwen|192|mixed_transport|itl_ms_p99|6.359661|2.113625|10.605697|
|smol|96|kernel_schedule|tpot_ms_mean|-0.155325|-0.279908|-0.030742|
|smol|96|kernel_schedule|connect_ttft_ms_p99|3.266025|-0.678094|7.210143|
|smol|96|kernel_schedule|connect_completion_ms_p99|-8.099156|-20.008251|3.809940|
|smol|96|kernel_schedule|scheduled_ttft_ms_p99|2.727499|-0.499829|5.954827|
|smol|96|kernel_schedule|request_throughput|0.107204|-0.195622|0.410031|
|smol|96|kernel_schedule|output_tokens_per_s|6.861083|-12.519834|26.242001|
|smol|96|kernel_schedule|executor_cpu_ms_per_attempt|0.007198|-0.137004|0.151400|
|smol|96|kernel_schedule|itl_ms_p99|0.070530|-0.659081|0.800140|
|smol|96|native_schedule|tpot_ms_mean|-0.193002|-0.334299|-0.051704|
|smol|96|native_schedule|connect_ttft_ms_p99|0.752970|-6.144199|7.650140|
|smol|96|native_schedule|connect_completion_ms_p99|-11.402239|-25.425267|2.620788|
|smol|96|native_schedule|scheduled_ttft_ms_p99|0.821980|-6.017860|7.661819|
|smol|96|native_schedule|request_throughput|0.244019|0.059554|0.428483|
|smol|96|native_schedule|output_tokens_per_s|15.617206|3.811468|27.422944|
|smol|96|native_schedule|executor_cpu_ms_per_attempt|0.070938|0.021654|0.120222|
|smol|96|native_schedule|itl_ms_p99|-0.494449|-1.265447|0.276550|
|smol|96|mixed_transport|tpot_ms_mean|0.006849|-0.087805|0.101504|
|smol|96|mixed_transport|connect_ttft_ms_p99|2.015825|-3.669420|7.701069|
|smol|96|mixed_transport|connect_completion_ms_p99|1.193310|-11.402071|13.788690|
|smol|96|mixed_transport|scheduled_ttft_ms_p99|0.004602|-8.312586|8.321790|
|smol|96|mixed_transport|request_throughput|-0.060315|-0.291661|0.171031|
|smol|96|mixed_transport|output_tokens_per_s|-3.860181|-18.666323|10.945961|
|smol|96|mixed_transport|executor_cpu_ms_per_attempt|0.064115|-0.017107|0.145338|
|smol|96|mixed_transport|itl_ms_p99|-0.156244|-0.535357|0.222868|
|smol|192|kernel_schedule|tpot_ms_mean|-0.237751|-0.357005|-0.118498|
|smol|192|kernel_schedule|connect_ttft_ms_p99|-26.134161|-59.623904|7.355582|
|smol|192|kernel_schedule|connect_completion_ms_p99|-39.969363|-74.208152|-5.730574|
|smol|192|kernel_schedule|scheduled_ttft_ms_p99|-24.429004|-53.827934|4.969926|
|smol|192|kernel_schedule|request_throughput|1.034693|-1.886216|3.955602|
|smol|192|kernel_schedule|output_tokens_per_s|66.220338|-120.717826|253.158502|
|smol|192|kernel_schedule|executor_cpu_ms_per_attempt|-0.065525|-0.129293|-0.001758|
|smol|192|kernel_schedule|itl_ms_p99|-1.490979|-3.556668|0.574711|
|smol|192|native_schedule|tpot_ms_mean|-0.243349|-0.401354|-0.085344|
|smol|192|native_schedule|connect_ttft_ms_p99|-28.399169|-53.376290|-3.422049|
|smol|192|native_schedule|connect_completion_ms_p99|-42.892763|-72.982005|-12.803521|
|smol|192|native_schedule|scheduled_ttft_ms_p99|-19.758987|-46.514829|6.996855|
|smol|192|native_schedule|request_throughput|2.789428|-2.233974|7.812830|
|smol|192|native_schedule|output_tokens_per_s|178.523385|-142.974352|500.021122|
|smol|192|native_schedule|executor_cpu_ms_per_attempt|-0.026683|-0.085400|0.032034|
|smol|192|native_schedule|itl_ms_p99|-0.422617|-2.894419|2.049185|
|smol|192|mixed_transport|tpot_ms_mean|-0.011727|-0.140066|0.116613|
|smol|192|mixed_transport|connect_ttft_ms_p99|11.464917|-3.211132|26.140967|
|smol|192|mixed_transport|connect_completion_ms_p99|10.916003|-8.386050|30.218055|
|smol|192|mixed_transport|scheduled_ttft_ms_p99|4.585724|-11.068429|20.239877|
|smol|192|mixed_transport|request_throughput|-0.500963|-2.668857|1.666932|
|smol|192|mixed_transport|output_tokens_per_s|-32.061607|-170.806876|106.683662|
|smol|192|mixed_transport|executor_cpu_ms_per_attempt|0.104921|0.064064|0.145777|
|smol|192|mixed_transport|itl_ms_p99|0.474391|-2.750263|3.699046|

### Logical schedule engagement

Counts combine both rates plus8 warmups per executor.

|Model|Mode|Mean combined mixed rounds|Mean prefill rounds withholding decode|Mean deferred decode request-steps|
|---|---|---:|---:|---:|
|qwen|KO|0.0|381.2|3793.8|
|qwen|NO|0.0|365.0|3733.0|
|qwen|KM|400.8|0.0|0.0|
|qwen|NM|428.4|0.0|0.0|
|smol|KO|0.0|416.4|3751.4|
|smol|NO|0.0|435.8|4117.6|
|smol|KM|442.8|0.0|0.0|
|smol|NM|470.6|0.0|0.0|

### Every full cell

|Model|Block|Rate|Mode|TPOT mean|TPS|TTFT P99|Completion P99|ITL P99|CPU/attempt|Lag P99|
|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
|qwen|0|96|KO|1.414028|5954.918295|26.550557|120.139016|6.922272|0.708413|12.709334|
|qwen|0|192|KO|1.471871|9877.721971|253.973865|353.643827|9.652708|0.825982|9.153303|
|qwen|0|96|NO|1.413801|5955.198284|21.405350|115.502350|7.064312|0.621014|12.910638|
|qwen|0|192|NO|1.450075|10373.157835|212.292710|305.021926|7.106960|0.491252|17.900177|
|qwen|0|96|KM|1.316960|5930.974606|22.448656|106.140663|6.157164|0.810575|7.253675|
|qwen|0|192|KM|1.591192|9063.850562|422.414796|526.327815|19.116998|0.847070|33.997142|
|qwen|0|96|NM|1.386870|5274.804501|169.019979|416.644497|7.291224|0.603772|10.575090|
|qwen|0|192|NM|1.328318|11061.043910|157.726676|241.965488|9.314479|0.478610|12.376855|
|qwen|1|192|KO|1.774011|8188.221103|629.184402|717.681697|24.878746|0.575738|19.735239|
|qwen|1|96|KO|1.406607|5929.591882|18.026891|106.482386|7.924185|0.722512|13.281540|
|qwen|1|192|NO|1.502430|10088.800347|224.503288|317.998088|9.725298|0.431102|31.779899|
|qwen|1|96|NO|1.551638|5924.083424|15.923548|113.303172|6.832871|0.599859|6.286230|
|qwen|1|192|KM|1.350590|10648.570157|125.687564|209.107515|13.456594|0.730672|24.587966|
|qwen|1|96|KM|1.207249|5968.561338|28.626349|94.577725|6.097817|0.684043|11.530994|
|qwen|1|192|NM|1.465509|10047.525113|242.743136|337.368261|7.682474|0.436267|213.884863|
|qwen|1|96|NM|1.207882|5956.045836|13.003454|88.189002|5.783994|0.610490|8.460590|
|qwen|2|96|KO|1.529097|5936.292445|23.970331|116.102183|8.141740|0.853308|7.069818|
|qwen|2|192|KO|1.580846|9436.638271|326.299615|417.244256|9.779172|0.992872|14.291592|
|qwen|2|96|NO|1.398565|5963.297444|10.353598|101.369168|6.172334|0.633295|8.240331|
|qwen|2|192|NO|1.397532|10632.996846|132.210047|212.287798|8.705607|0.476536|16.670596|
|qwen|2|96|KM|1.206729|5962.600632|14.429762|89.167033|6.292628|0.690846|9.018494|
|qwen|2|192|KM|1.358235|10663.054772|130.561062|212.552990|9.892061|0.718582|17.266149|
|qwen|2|96|NM|1.210420|5945.201560|16.717244|91.088982|6.580900|0.549018|8.189918|
|qwen|2|192|NM|1.338041|10889.501441|87.936964|170.376115|6.979525|0.470353|15.434985|
|qwen|3|192|KO|1.447663|10187.675310|202.642044|285.781452|10.201945|0.738271|11.285974|
|qwen|3|96|KO|1.414778|5936.938522|15.269693|105.363550|7.302987|0.781329|10.629451|
|qwen|3|192|NO|1.512334|10061.435905|248.993500|340.651467|8.865627|0.491918|12.817116|
|qwen|3|96|NO|1.556114|5943.757396|13.947044|116.588563|7.923313|0.693741|9.837426|
|qwen|3|192|KM|1.413891|10165.983123|198.161182|281.131190|13.796376|0.617440|14.978483|
|qwen|3|96|KM|1.213153|5964.080486|12.040419|94.504847|7.036796|0.810653|10.838593|
|qwen|3|192|NM|1.557378|9558.973552|303.185499|380.265078|10.497614|0.480823|261.923566|
|qwen|3|96|NM|1.210744|5963.697344|21.705727|99.375628|6.208876|0.593590|8.398251|
|qwen|4|96|KO|1.407879|5960.068309|24.738620|113.473103|8.672832|0.769789|8.704138|
|qwen|4|192|KO|1.415489|10342.693209|207.025833|297.555680|9.924975|0.923776|21.027850|
|qwen|4|96|NO|1.524866|5961.582188|135.702807|371.025016|8.005377|0.526293|331.959855|
|qwen|4|192|NO|1.432435|10433.833924|182.752046|271.468813|8.065269|0.387268|27.113012|
|qwen|4|96|KM|1.206327|5963.906689|20.513392|94.284800|6.609135|0.737273|13.960138|
|qwen|4|192|KM|1.343165|10415.035437|207.660096|288.942295|17.352450|0.635543|13.808225|
|qwen|4|96|NM|1.206515|5965.941249|10.608829|87.712099|5.337133|0.553462|7.035595|
|qwen|4|192|NM|1.348148|11029.635483|120.878577|200.040738|7.342081|0.372723|22.162589|
|smol|0|96|KO|1.074912|5998.150507|12.716845|82.361666|5.990526|0.706902|10.801324|
|smol|0|192|KO|1.151834|11678.914292|100.834848|169.762652|11.328552|0.577983|10.766609|
|smol|0|96|NO|1.074953|5987.669976|9.493919|79.762110|5.543864|0.475519|10.659714|
|smol|0|192|NO|1.137468|11577.319071|63.548053|132.570054|8.166276|0.363663|16.012963|
|smol|0|96|KM|0.965031|5998.889443|12.762410|76.919741|5.317469|0.570969|8.455944|
|smol|0|192|KM|0.934876|11719.765005|46.092854|112.001232|10.507662|0.460943|13.100627|
|smol|0|96|NM|0.925383|6006.309972|17.576097|79.025522|4.966103|0.567159|8.357204|
|smol|0|192|NM|0.927248|11739.751467|23.078865|87.096752|6.711114|0.303963|23.178379|
|smol|1|192|KO|1.166009|11669.518537|34.125053|106.941612|10.021575|0.467195|25.127296|
|smol|1|96|KO|1.066408|5992.485124|9.627926|78.895573|5.124593|0.715414|5.489018|
|smol|1|192|NO|1.296778|11538.171072|48.254013|127.879363|9.115776|0.428299|10.321764|
|smol|1|96|NO|1.237245|5982.748536|13.249293|92.242302|6.102355|0.636193|6.547590|
|smol|1|192|KM|0.928899|11663.837624|19.543272|79.273242|6.695156|0.455071|9.056259|
|smol|1|96|KM|0.917686|6006.396915|11.989656|71.356251|4.733120|0.784432|7.121322|
|smol|1|192|NM|0.923211|11749.950441|12.665984|70.860637|6.616546|0.381375|16.963059|
|smol|1|96|NM|0.918724|6006.142059|8.787004|66.311349|4.935323|0.753953|4.838663|
|smol|2|96|KO|1.083726|6002.130596|9.603672|81.358558|5.594226|0.650824|7.168948|
|smol|2|192|KO|1.150804|11548.512926|31.054885|102.497961|8.680137|0.569565|22.106282|
|smol|2|96|NO|1.231592|5982.137819|8.860954|90.317407|6.007903|0.632509|6.464862|
|smol|2|192|NO|1.299225|11088.637197|67.006357|143.017033|8.905473|0.467757|26.840344|
|smol|2|96|KM|1.034489|5985.507612|18.038965|84.235511|6.088437|0.817363|8.542551|
|smol|2|192|KM|1.060487|11488.206173|39.409154|100.739986|9.596012|0.510108|18.480332|
|smol|2|96|NM|0.931851|6007.140953|10.977566|70.406551|6.536571|0.644005|9.962432|
|smol|2|192|NM|0.917962|11681.500340|17.512012|71.906505|7.327982|0.398350|24.413041|
|smol|3|192|KO|1.234886|11708.208748|58.453758|134.562870|9.565645|0.460152|16.011453|
|smol|3|96|KO|1.069934|5999.416394|11.379334|80.406166|5.828197|0.736612|6.898274|
|smol|3|192|NO|1.170642|11685.008593|29.122197|104.077160|7.216090|0.361039|16.208710|
|smol|3|96|NO|1.069035|6007.329345|15.674349|80.099554|7.002048|0.561459|8.491480|
|smol|3|192|KM|0.928020|11738.339199|41.161733|95.236487|8.041028|0.440528|17.671987|
|smol|3|96|KM|0.920402|6011.172761|15.098833|73.558930|6.035159|0.680214|7.284215|
|smol|3|192|NM|1.038257|11679.622511|29.899851|96.635250|9.081438|0.359836|18.893825|
|smol|3|96|NM|0.920765|6012.548899|10.529213|70.615327|6.358465|0.635934|8.668984|
|smol|4|96|KO|1.237543|6008.538587|11.781376|93.501996|5.128838|0.684771|5.982257|
|smol|4|192|KO|1.259504|11444.597298|73.982650|153.144482|9.782277|0.586343|16.115926|
|smol|4|96|NO|1.073836|6016.355825|10.316787|84.651458|6.616325|0.549567|12.123324|
|smol|4|192|NO|1.145544|11759.408668|44.521027|119.402954|8.260807|0.321665|16.847016|
|smol|4|96|KM|0.918291|6033.059894|13.549414|69.957748|5.844844|0.677534|9.077949|
|smol|4|192|KM|0.921998|11770.705490|21.573374|79.811814|7.083435|0.466961|24.475353|
|smol|4|96|NM|1.024930|6022.185647|13.490273|83.702884|6.003789|0.608884|11.667102|
|smol|4|192|NM|1.026235|11690.336767|27.299087|85.983606|9.814256|0.365484|43.440098|
