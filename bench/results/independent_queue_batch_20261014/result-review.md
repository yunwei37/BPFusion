# Independent RESULT REVIEW: batched publication in independent GPU I/O

Reviewed UTC: 2026-10-14T22:09:31.741462+00:00

## Separate judgments

- Run status: **valid** and complete for the approved integrated collection. No invalidating scientific, command, correctness or baseline defect was found. Archiving, source restoration and publication are subsequent orchestrator actions, not already completed here.
- Tested hypothesis: **inconclusive** for improvement of gen64/c8 TPS over the original independent worker, separately for both models. Neither original-control interval is wholly positive or negative. Smol superiority over efficient native is **contradicted** by the negative native contrast; Qwen superiority is **inconclusive**, with all five observed differences negative but its nominal interval crossing zero.
- Research value: **supporting**. This fills the previously absent independent-worker plus batched-publication counterfactual and makes a source-selection decision; it is neither headline evidence nor a separate contribution from qualification.
- Paper impact: **mechanism/workload boundary**, with additional supporting evidence toward the retained serving objective. No formal paper RQ/thesis exists in the repository, and this result is not a direct thesis challenge or full-goal completion.
- Next paper decision: close this tested combination and restore the exact uncommitted original header under the plan's predeclared rule. Neither model supplies a supported primary improvement, so select no model-specific or universal batched-independent source scope and change no defaults. Preserve the complete negative/inconclusive evidence. Prefer the predeclared long-output timeline/capacity discriminator over repeating the unchanged matrix if further research is undertaken; this review itself authorizes no new run, instrumentation or redesign.

## Review method and evidence

This is one fresh result review under research-experiment-design/SKILL.md, with no desired verdict supplied. I read plan.md and plan-review.md completely, execution-notes.md, setup/run/qualification/lifecycle and fixed analysis recipes; inspected the current header/model/BPF/native/client/Make paths, original_io_uring_tcp.h, candidate.diff, frozen references, source_snapshot, build/linkage receipts and stored ordinary dispatch SASS. Current docs/evaluation.md and findings0051/0055 supply the retained objective and prior boundaries, not numerical substitutes for this run.

I independently parsed every full raw JSONL, all executor stdout, expanded starts, driver exits and fixed full/long analyses. A separately written in-memory Python reconstruction computed all 120 cell windows and metrics, 24 means, 72 signed block effects and nominal t95 intervals; every value exactly equaled full.analysis.json. It also authenticated all 30 short and 30 long raw counter rows and eight short/long round effects, including timestamp-based serial deductions and all whole-transfer CQ summaries. No raw observation was removed. I parsed both protocol model/reference/network files and independently reconstructed admission/ownership/history/release token equality. I decoded every lifecycle request_hex/reply_hex/post_stop_extra_hex, and inspected actual syscall transcripts and physical slot/ring state, rather than accepting pass flags alone. Pure-function CPU replay of the fixed preflight and protocol analyzer also passed, without overwriting any analysis output or executing GPU code.

Only this result-review.md was written. No source, default, Git commit, model/GPU run, cleanup, publication or original session was changed. A review-only glob initially also selected protocol GPU JSONL files, which have no metadata, causing StopIteration in the CPU analyzer; explicit protocol paths corrected that read-only selection. No experimental child was launched or data altered, and this was not a run/cell retry.

## Completion, commands and deviations

Full collection terminates exit0 at2026-10-14T22:01:00.740563+00:00, wrapper exit0 at22:01:00.746506. All20 driver exits,60 executor exits and120 cells are present. There are3840 measured replies/124800 output tokens,480 checked excluded one-token warmups,4320 total replies/125280 tokens. Fixed full analysis exits0 at22:01:07.946374; fixed long-counter analysis exits0 at22:01:08.064233. Driver/wrapper and relevant analysis stderr files are empty. Real preflight1 completes4 drivers/12 executors/24 cells,192 measured requests/6240 tokens plus96 warmups. No preflight2/3, full failure, exclusion, substitution, replacement or cell restart is used.

The executable command is `python3 TEMP/run.py full`, where TEMP is `/tmp/bpfusion-independent-batch-a3l3l2uo`; all20 expanded driver commands are in full.commands.json and identical full.exit.json records. Every raw start binds `uring_loop_original` to TEMP/control-build/vllm_graph_uring_loop, `userspace` to TEMP/build/vllm_graph_user_network_wait, and `uring_loop` to TEMP/build/vllm_graph_uring_loop, with the same model snapshot and300-second source-native serve argument. All60 paths/arguments and saved stdout match the actual raw start/executor records. Five process blocks use five of six path permutations; odd blocks reverse model/context/cell order as planned. This reduces order bias but leaves incomplete balance and within-block temporal drift.

setup.py builds the original control first at21:04:04.674563 before modifying the header; candidate/native/trace are then freshly built. Build logs retain actual NVCC13.0.88 sm_120 O3 compilation, matching padding/prefix flags and dynamic CUDA linkage; no saved serving ELF is substituted. Existing root BPF loader/object are reused read-only. System libbpf1.3 headers/linker search remain compile inputs; all applicable actual ldd receipts resolve temporary libbpf1.6.3 at runtime. Native does not require libbpf dynamic linkage. Pinned packages are vLLM0.31.0, Torch2.13.0+cu129 and Transformers5.17.0. Kernel-UAPI user-space compilation warnings are retained and builds exit0; they are not silently relabeled as failures.

execution-notes.md correctly records extra idle SQ head/tail reads from the reused algorithm and the first lifecycle observer NameError before any wrapper/child launch. Its corrected observer imports do not constitute a lifecycle run retry. No oracle, timeout, metric or condition-source change was made during collection. The root's untracked background literature document is unrelated work added during collection; raw metadata sources,12 current source snapshots, main base212a15775e924ea6b2447b3efa046ca6889022a8 and conditions remain identical. Untracked tools/setup_env.sh and the eight original preserved path metadata are unchanged.

## Intervention and mechanism engagement

The exact production candidate is7 added/7 removed lines, net0, in executor/io_uring_tcp.h. Replacing its seven extended conditions back with literal BF_IO_COALESCED reconstructs original_io_uring_tcp.h byte-for-byte. It reuses local SQ cursors, conservative SQ snapshot capacity, one system fence/release tail publication, finite acquire CQ snapshot and one release head publication, including both cancel-wait and normal-return publication. Global coalesced state, startup selection and shutdown-only launch remain BF_IO_COALESCED only. Thus both original and candidate retain the independent io_network worker on a nonblocking stream and existing stop/model-quiesced/drain/finish resource lifetime. BF_IO_COALESCED dispatcher work is absent from both standalone builds. No new mode, flag, timer, queue ABI, helper, entity or runtime default is introduced.

The existing model dispatch, graph capture/sampling/KV packing, BPF stream parser/sockmap ingress redirect, FIFO final-send/recycle and ordinary client paths were inspected. Native and loop targets have matching padding/prefix model macros and identical model source. The three saved normalized ordinary dispatch SASS files are byte-identical,1864 instructions each. This supports static dispatcher equivalence only, not equal whole binaries, dynamic model rounds, elapsed GPU work or causal PCIe mediation. Actual ordinary rounds below differ with scheduling/batching and remain part of the constructor effect rather than proof of equal dynamic work.

The finite CQ iterator/release-head policy has an upstream [liburing precedent](https://github.com/axboe/liburing/blob/master/src/include/liburing.h); that precedent does not establish GPU speedup. The reviewed SQ-flush queue.c location was already identified as stale, and the captured existing implementation is the intervention authority. Publication, layout, finite drain/availability and resulting scheduling form one tested bundle. Extra per-progress SQ reads can offset publication savings; no dynamic cursor count or per-round timeline identifies that explanation here.

## Independent main-baseline audit and metric fairness

Native is the single main competitor, representing efficient userspace TCP orchestration with reused resident model computation. The original per-entry worker is a component ablation, not a second main baseline or external SOTA. All native logs explicitly engage the timed epoll_pwait2 path with60000ns waits and complete published/completed accounting; model graph launches/admissions/retirements and outputs are present, with no avoidable serving/interface failure. Source performs nonblocking accept/receive and scatter/gather sendmsg. Native is not the known weak busy-poll or Python request-worker proxy. Its same captured graphs, checkpoint, FP16 weights/KV, four literal prompts, eight slots, context/output budget, warmups, preopened connections and measurement count make it a credible matched mechanism comparison. No extra native penalty, condition-specific tuning or information advantage was found. Native ordinary execution is not syscall-traced, so its engagement is established by compiled path, logs and accounting rather than an invented native raw syscall trace.

Checkpoint revisions are Smol93efa2f097d58c2a74874c7e644dbc9b0cee75a2 and Qwen7ae557604adf67be50417f59c2c2f167def9a775. Raw metadata embeds exactly the expanded current driver/client/backend/native/candidate/original sources and unchanged frozen-reference model records. Graph/bootstrap source gives the same model and greedy sampling policy across all paths. Batch trajectories are unobserved during ordinary timing and need not be identical; neither arithmetic source equality nor SASS equality removes scheduling-dependent dynamic-work effects.

Primary TPS is32*gen divided by last token arrival minus first request send for each cell. TTFT is first arrival minus send, completion is last arrival minus send, and TPOT excludes the first token per request. These definitions agree with the client and analysis; [official vLLM metric documentation](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics) supports client TTFT and per-request TPOT concepts. This finite source-native token-ID window is not the official text-serving benchmark duration, saturation capacity, offered-load/SLO or tail-latency measurement. Tokens in one recv share arrival timestamps; TPOT is not independent per-token latency.

Uncertainty uses five signed paired process-block differences and2.776445105*sample_std/sqrt(5), nominal two-sided t95 df4. Every signed row, including long-round332/319/324 and adverse/variable short blocks, is retained. The120 cells and individual requests are not independent replicate units. Intervals are not familywise corrected; crossing zero proves neither equality, noninferiority nor positive selection. Known-worker CPU is the POSIX executor process clock plus available module TX counter, bracketed around each client window; TX is zero for these loop/native conditions. It excludes unaccounted kernel/BPF/RX/softirq/TCP and client work, and cannot support total CPU or energy savings.

## Primary throughput decision

Means and nominal intervals are independently reconstructed below. All throughput differences are candidate minus the named path; ratios describe ratios of means only.

| Model | Original TPS | Native TPS | Candidate TPS | Candidate-original TPS (t95) | Candidate-native TPS (t95) |
|---|---:|---:|---:|---|---|
| SmolLM2-135M |5355.164798|5620.980727|5480.395554|+125.230756 [-103.272869,353.734381]|-140.585173 [-267.251262,-13.919083]|
| Qwen2.5-0.5B |4601.707617|4742.796741|4575.192846|-26.514771 [-270.340498,217.310955]|-167.603895 [-374.057244,38.849453]|

Smol's mean original-control increase is about2.338%; Qwen's mean decrease is about0.576%. Both original-control intervals cross zero and contain substantial favorable and adverse effects. Smol is about2.501% below native by ratio of means and all five native block differences are negative; its negative interval directly supports a finite native throughput advantage. Qwen is about3.534% below native by ratio of means and all five differences are negative, but uncertainty crosses zero, so a statistically established native advantage or parity cannot be claimed. These data supply no supported batched-independent source selection under the plan.

## Secondary results and ordinary counters

All72 performance contrasts are retained in Appendix B. Every candidate-original secondary interval crosses zero. All gen1/c8 TTFT contrasts, serial TTFT/TPS/completion contrasts and all TPOT contrasts cross zero; no secondary latency improvement or harm is established. Positive or negative point estimates remain descriptive. Significant partial CPU penalties relative to native remain: Smol gen64/c1 +175.118us/request [82.395,267.842], Smol gen64/c8 +39.838us [0.589,79.088], Qwen gen64/c8 +64.473us [41.756,87.190]. These nominal secondary rows cannot replace the primary or imply total CPU.

Short-only32-request counters subtract exactly8 checked sequential gen1 warmups. Long transfer counters subtract2088 rounds:8 warmups,32 gen1/c1 and32*64 gen64/c1 tokens. Raw request timestamps independently establish no overlap in these serial groups; remaining model graph count belongs to gen64/c8. All30 rows of each type match stored analyses. Ordinary rounds are not isolated GPU time or batch-membership traces. All eight short/long candidate-original/native round-effect intervals cross zero. Appendix C retains all per-block counts and effects, rather than trimming the large raw counts or attributing them to an unverified cause.

Whole-transfer CQ-SQ excess reflects descriptive multishot-timeout traffic over warmup and all three cells. Both SQ and CQ are individually empty at exit; their cursor totals need not equal because multishot timeout CQEs exceed SQ entries. Appendix D retains all20 loop path/context rows. This is not per-cell GPU cost, dynamic mapped-access count or proof that timer/cursor traffic mediated TPS.

## Correctness, lifecycle bytes and actual syscall evidence

All4320 ordinary whole outputs/125280 tokens match the frozen pre-observation finite complete-output pools, with valid reply status/body length and arrival/accounting checks in the fixed client. The asset's source8323c32e19a1fcdf326beba405a411a6276aa8dc and freeze2026-10-13T04:16:47.805543 predate this collection; current metadata pools are identical and no result-derived expansion occurred. These sets contain historical batch-dependent sequences, so membership is not fresh eager-HF parity or arbitrary-input/backend correctness. The older AMK eager-HF exact-output failure remains failed. Ordinary raw data stores tokens/timestamps, not every HTTP wire header; byte-level independent header decoding is available for lifecycle, while ordinary/protocol headers rely on the preserved client checks.

Each candidate traced protocol completes622 client requests,22224 tokens,259 expected rejects and5000 empty connections. Admission markers, prompt/gen/reject flags, trace tokens, references and clients agree; full model trace overflows are0. I reconstructed physical owners=id%8, token history, non-rejected compute, prefill query=max actual prompt length, ordered releases and no post-release use. Actual batch sizes1..8 engage the real path. Smol has6624 graph rounds,190 prefill/6434 decode,5374 real prompt tokens/3851 padded tokens and175 release rounds/max8; Qwen has6991 graph rounds,187 prefill/6804 decode,5374/3947 real/padded and124 releases/max8. Stored successful replay reconstructs actual batch/history/KV using the same graph math; it is not an independent fresh eager-HF arithmetic oracle. No GPU replay was run by this reviewer.

Each protocol ring has accepted=closed5086 and head=completed622, zero pending/error/reserved/drop/queue overflow. Its1 transport abort corresponds to the expected invalid binary close. The fixed128-record I/O diagnostic reports trace_count622/trace_overflow494, independently checked and kept separate from complete full-model trace overflow0. Smol SQ38443/CQ186618, Qwen SQ38960/CQ221759 are each independently drained. Physical slots and admission bitmap are free; client/history coverage remains complete despite diagnostic truncation.

All32 lifecycle request wires per model decode the correct little-endian magic0x514c4d51, prompt count, generation, zero flags, client marker and exact token IDs. HTTP request Content-Length equals actual payload. Every normal response decodes exactly HTTP/1.1 200 OK, application/octet-stream and gen*4 Content-Length; invalid HTTP has400 Bad Request and0 length, and invalid binary returns EOF. Complete body or one-token RST/stop prefix belongs to the unchanged frozen pool. Both post_stop_extra_hex fields are empty, so no unverified suffix is discarded. Checked652 complete-or-prefix tokens per model do not turn interrupted generations into complete replies.

Lifecycle has13 accepted/closed connections,32 transport completions and three aborts at IDs27 invalid binary,29 RST and31 SIGTERM. Each abort's recorded bytes is respectively0,4,84 (stop header plus first token). Smol sends644/4973 bytes and SQ726/CQ289831; Qwen sends656/4973 and SQ737/CQ293630. Every ring has zero pending/error/reserved/dropped/overflow/diagnostic overflow; SQhead=SQtail and CQhead=CQtail. Actual BPF stats show llm_head32,bitmap0,all eight physical states FREE and recycle32. Model counters are admitted32/retired31,654 graph rounds,graph_error0 in each suite: the intentional interrupted model request remains unretired while transport ownership is safely released. Cleanup records release ring/connections/buffers. Source and shutdown receipts support quiescence, but no direct live sampling after I/O state free is claimed.

Protocol network traces after resident-ready contain no userspace accept/recv/send request calls and one steady kernel-loop io_uring_enter before SIGTERM; bootstrap netlink/model work occurs earlier. Lifecycle raw strace totals are Smol4 and Qwen5 io_uring_enter calls: two bootstrap entries, one steady entry interrupted by SIGTERM, and respectively one/two cleanup entries. The Qwen signal arrives on a helper thread, after which the source-native wait/drain path re-enters; these cleanup calls are not steady userspace request processing. After NET_READY timestamps, neither lifecycle has userspace accept/recv/send calls. Setup memory registration and loop attach are present. This supports removal of the selected steady userspace request worker, not zero kernel CPU or a generic transport-speed claim.

## Environment, leakage and scope limits

Sparse host_entry/preflight/before/during/mid/after snapshots share boot04dc0087-5ccc-4c46-9997-b9a92f0e5167 and the same33 selected older NVRM refcnt/status0x56 lines, latest10:50:43UTC (`journalctl --utc`) retained verbatim. No new selected fault line is observed; this is not a completely clean-journal or harmless-warning conclusion. Existing current400W GPU limit, device default575W, is common and unchanged. Snapshot temperatures span41..50C. Mid snapshot at21:38:09UTC contains one python3 compute application; endpoint app lists are empty. Sparse observations do not prove continuous isolation, identify all interference, or justify removing slow blocks. After snapshot22:02:14.069147 is about73 seconds after full terminal, not exactly simultaneous.

Post-run22:02:19.392127 receipts plus current read-only verification show main/base unchanged, all12 captured source bytes equal, and all eight preserved original path metadata equal. Current WIP remains candidate header plus root literature document and pre-existing tools/setup_env.sh. This report does not infer continuous absence of another writer from endpoint checks, and it leaves original sessions, checkout and runtime state untouched.

The valid scope is one Linux7.3rc3/RTX5090 host, two small FP16 vLLM checkpoints, token-ID loopback HTTP/binary, four finite prompts, gen1/64,c1/8 and five blocks. It excludes arbitrary text/API/backend acceptance, physical-NIC transport, offered-load/SLO/capacity generalization, total CPU/energy, isolated overlap/PCIe/cursor mediation and universal defaults. Prior coalesced positive evidence is not contradicted for its own constructor; this separate independent combination simply fails its local positive-selection criterion. The retained full serving/performance goal remains open.

## Reproduction and handoff

Preserve plan/review, original header and source snapshot, build/linkage/environment/package receipts, full.commands.json, raw JSONL/stdout/exits, qualification trace/reference/network files, lifecycle bytes/strace/state, full.analysis.json, long_counter.analysis.stdout, execution notes and host/preservation receipts as one integrated archive. Recipe rebuild uses the source-native Makefile with private BUILD: original control before applying candidate.diff, then native/candidate/trace. Absolute historical TEMP/model paths identify the original run and require ordinary relocation when replaying elsewhere; do not copy credentials, model weights/runtime/vendor dependencies into Git.

Fixed CPU reanalysis commands are `python3 analysis.py ARCHIVE full`, `python3 long_counter_analysis.py ARCHIVE`, and `python3 analysis_lifecycle.py ARCHIVE`; for protocol use analysis.analyze on the two explicit qualification_vllm_smol.jsonl and qualification_vllm_qwen.jsonl paths. Original metadata sources and prior failure boundaries must accompany the numbers. No new run is needed to make this completed local decision. Restore only the exact owned uncommitted header, retain unrelated work, then archive/replay/verify/commit/push through the orchestrator's existing authorized workflow; those steps are not performed by this review.

## Appendix A: all24 independently verified means

CPU units are us/request for this table; other latency units are ms and TPS is output tokens/s.

| Model | gen/c | Path | TTFT | Completion | TPS | TPOT | Known-worker CPU |
|---|---|---|---:|---:|---:|---:|---:|
|SmolLM2-135M|1/1|original independent|1.239148|1.239148|807.249816|n/a|51.949825|
|SmolLM2-135M|1/1|native epoll|1.177659|1.177659|844.006484|n/a|38.818238|
|SmolLM2-135M|1/1|batched independent|1.165012|1.165012|851.124014|n/a|49.305937|
|SmolLM2-135M|64/1|original independent|1.221845|47.257041|1353.605461|0.730717|1503.365600|
|SmolLM2-135M|64/1|native epoll|1.267170|46.937598|1362.969803|0.724927|1347.912238|
|SmolLM2-135M|64/1|batched independent|1.199397|46.731887|1368.372000|0.722738|1523.030619|
|SmolLM2-135M|1/8|original independent|2.677916|2.677916|2490.745812|n/a|28.310075|
|SmolLM2-135M|1/8|native epoll|2.422762|2.422762|2787.627535|n/a|27.430712|
|SmolLM2-135M|1/8|batched independent|2.657209|2.657209|2793.488981|n/a|27.152844|
|SmolLM2-135M|64/8|original independent|2.045229|94.743750|5355.164798|1.471405|493.695519|
|SmolLM2-135M|64/8|native epoll|2.513970|90.934814|5620.980727|1.403505|434.208350|
|SmolLM2-135M|64/8|batched independent|1.863739|92.757062|5480.395554|1.442751|474.046819|
|Qwen2.5-0.5B|1/1|original independent|1.474603|1.474603|676.429454|n/a|62.313631|
|Qwen2.5-0.5B|1/1|native epoll|1.556757|1.556757|644.602139|n/a|60.530681|
|Qwen2.5-0.5B|1/1|batched independent|1.448930|1.448930|685.704733|n/a|62.114113|
|Qwen2.5-0.5B|64/1|original independent|1.607029|79.251152|807.171656|1.232446|2583.759844|
|Qwen2.5-0.5B|64/1|native epoll|1.468253|78.209697|817.860148|1.218118|2334.035769|
|Qwen2.5-0.5B|64/1|batched independent|1.463918|79.142946|808.280196|1.233000|2503.833744|
|Qwen2.5-0.5B|1/8|original independent|2.823275|2.823275|2456.414336|n/a|28.861887|
|Qwen2.5-0.5B|1/8|native epoll|3.195950|3.195950|2256.572096|n/a|27.957187|
|Qwen2.5-0.5B|1/8|batched independent|2.862127|2.862127|2547.876794|n/a|29.212575|
|Qwen2.5-0.5B|64/8|original independent|2.591697|108.586426|4601.707617|1.682456|572.147738|
|Qwen2.5-0.5B|64/8|native epoll|2.434037|107.435391|4742.796741|1.666688|488.169737|
|Qwen2.5-0.5B|64/8|batched independent|2.510740|110.145730|4575.192846|1.708492|552.642450|

## Appendix B: all72 independently verified signed performance effects

Candidate minus named control. All five block differences remain in order0..4. CPU is converted to us/request; all other values retain metric units. Intervals are nominal paired t95, not simultaneous confidence intervals.

| Model | gen/c | Control | Metric | Blocks0..4 | Mean | t95 |
|---|---|---|---|---|---:|---|
|SmolLM2-135M|1/1|original independent|ttft_ms|-0.013858, -0.110309, -0.056268, 0.096741, -0.286984|-0.074136|[-0.249475, 0.101204]|
|SmolLM2-135M|1/1|original independent|completion_ms|-0.013858, -0.110309, -0.056268, 0.096741, -0.286984|-0.074136|[-0.249475, 0.101204]|
|SmolLM2-135M|1/1|original independent|tokens_per_s|6.959371, 87.219435, 35.620086, -82.400946, 171.973045|43.874198|[-73.370004, 161.118400]|
|SmolLM2-135M|1/1|original independent|known_worker_cpu_s_per_request|1.213875, -1.090625, -6.844219, 8.386812, -14.885281|-2.643888|[-13.512275, 8.224500]|
|SmolLM2-135M|1/1|native epoll|ttft_ms|0.042573, -0.215641, 0.101708, 0.020220, -0.012096|-0.012647|[-0.162695, 0.137401]|
|SmolLM2-135M|1/1|native epoll|completion_ms|0.042573, -0.215641, 0.101708, 0.020220, -0.012096|-0.012647|[-0.162695, 0.137401]|
|SmolLM2-135M|1/1|native epoll|tokens_per_s|-34.936294, 155.147948, -75.144611, -13.473178, 3.993787|7.117530|[-101.983557, 116.218617]|
|SmolLM2-135M|1/1|native epoll|known_worker_cpu_s_per_request|20.844906, -4.854719, 24.075000, 10.446031, 1.927281|10.487700|[-4.726595, 25.701995]|
|SmolLM2-135M|64/1|original independent|ttft_ms|-0.068737, -0.264424, 0.355517, -0.084213, -0.050383|-0.022448|[-0.305691, 0.260795]|
|SmolLM2-135M|64/1|original independent|completion_ms|-2.387637, -0.614697, -0.325241, 0.927604, -0.225798|-0.525154|[-2.009572, 0.959264]|
|SmolLM2-135M|64/1|original independent|tokens_per_s|66.521272, 18.095225, 9.258793, -26.735873, 6.693277|14.766539|[-26.915271, 56.448348]|
|SmolLM2-135M|64/1|original independent|known_worker_cpu_s_per_request|-57.670000, 112.480312, 86.909437, -52.073781, 8.679125|19.665019|[-77.280917, 116.610954]|
|SmolLM2-135M|64/1|original independent|tpot_ms|-0.036808, -0.005560, -0.010806, 0.016061, -0.002784|-0.007979|[-0.031619, 0.015660]|
|SmolLM2-135M|64/1|native epoll|ttft_ms|-0.288099, -0.212979, 0.183806, 0.018160, -0.039755|-0.067773|[-0.300970, 0.165423]|
|SmolLM2-135M|64/1|native epoll|completion_ms|-2.291920, -0.218650, 0.205483, 1.346896, -0.070363|-0.205711|[-1.842451, 1.431030]|
|SmolLM2-135M|64/1|native epoll|tokens_per_s|63.977851, 6.435695, -6.274072, -39.235497, 2.107007|5.402197|[-40.939877, 51.744270]|
|SmolLM2-135M|64/1|native epoll|known_worker_cpu_s_per_request|111.796938, 279.605656, 228.153437, 119.961719, 136.074156|175.118381|[82.394629, 267.842133]|
|SmolLM2-135M|64/1|native epoll|tpot_ms|-0.031807, -0.000090, 0.000344, 0.021091, -0.000486|-0.002189|[-0.025690, 0.021311]|
|SmolLM2-135M|1/8|original independent|ttft_ms|0.465586, 0.112952, 0.928515, -1.611917, 0.001333|-0.020706|[-1.212930, 1.171518]|
|SmolLM2-135M|1/8|original independent|completion_ms|0.465586, 0.112952, 0.928515, -1.611917, 0.001333|-0.020706|[-1.212930, 1.171518]|
|SmolLM2-135M|1/8|original independent|tokens_per_s|75.920373, -11.741288, -704.013314, 1928.336774, 225.213299|302.743169|[-909.465788, 1514.952125]|
|SmolLM2-135M|1/8|original independent|known_worker_cpu_s_per_request|0.230500, 5.221781, 1.817906, -15.287719, 2.231375|-1.157231|[-11.218204, 8.903741]|
|SmolLM2-135M|1/8|native epoll|ttft_ms|-0.040734, 0.511760, 0.691690, -0.086422, 0.095941|0.234447|[-0.197395, 0.666289]|
|SmolLM2-135M|1/8|native epoll|completion_ms|-0.040734, 0.511760, 0.691690, -0.086422, 0.095941|0.234447|[-0.197395, 0.666289]|
|SmolLM2-135M|1/8|native epoll|tokens_per_s|404.646728, 175.327711, -431.363831, 118.139455, -237.442834|5.861446|[-410.937335, 422.660227]|
|SmolLM2-135M|1/8|native epoll|known_worker_cpu_s_per_request|1.422656, -0.019000, -3.450906, -3.195875, 3.853781|-0.277869|[-4.135642, 3.579904]|
|SmolLM2-135M|64/8|original independent|ttft_ms|-0.336697, 0.090508, -0.895194, 0.199921, 0.034011|-0.181490|[-0.736557, 0.373577]|
|SmolLM2-135M|64/8|original independent|completion_ms|-6.467837, -3.891568, 3.078083, -0.015398, -2.636720|-1.986688|[-6.534879, 2.561503]|
|SmolLM2-135M|64/8|original independent|tokens_per_s|390.100102, 213.723674, -59.172923, -27.084420, 108.587346|125.230756|[-103.272869, 353.734381]|
|SmolLM2-135M|64/8|original independent|known_worker_cpu_s_per_request|-67.988531, -19.135500, 52.265281, -72.492281, 9.107531|-19.648700|[-85.139821, 45.842421]|
|SmolLM2-135M|64/8|original independent|tpot_ms|-0.097320, -0.063208, 0.063068, -0.003418, -0.042393|-0.028654|[-0.105063, 0.047755]|
|SmolLM2-135M|64/8|native epoll|ttft_ms|-1.261044, 0.115828, -2.460225, 0.093573, 0.260710|-0.650232|[-2.121888, 0.821425]|
|SmolLM2-135M|64/8|native epoll|completion_ms|2.145689, 3.906141, 3.195745, 0.571461, -0.707794|1.822248|[-0.525392, 4.169889]|
|SmolLM2-135M|64/8|native epoll|tokens_per_s|-147.035788, -236.953144, -242.077598, -62.158867, -14.700466|-140.585173|[-267.251262, -13.919083]|
|SmolLM2-135M|64/8|native epoll|known_worker_cpu_s_per_request|-10.352437, 58.519312, 55.882687, 66.958750, 28.184031|39.838469|[0.589052, 79.087886]|
|SmolLM2-135M|64/8|native epoll|tpot_ms|0.054075, 0.060164, 0.089777, 0.007586, -0.015373|0.039246|[-0.013421, 0.091912]|
|Qwen2.5-0.5B|1/1|original independent|ttft_ms|-0.098785, -0.034984, -0.070484, 0.033646, 0.042243|-0.025673|[-0.103144, 0.051798]|
|Qwen2.5-0.5B|1/1|original independent|completion_ms|-0.098785, -0.034984, -0.070484, 0.033646, 0.042243|-0.025673|[-0.103144, 0.051798]|
|Qwen2.5-0.5B|1/1|original independent|tokens_per_s|43.059648, 19.689446, 25.922474, -19.195308, -23.099860|9.275280|[-26.848883, 45.399442]|
|Qwen2.5-0.5B|1/1|original independent|known_worker_cpu_s_per_request|-15.190750, -3.812625, 1.724344, 6.764687, 9.516750|-0.199519|[-12.371608, 11.972571]|
|Qwen2.5-0.5B|1/1|native epoll|ttft_ms|0.055574, -0.048637, -0.343069, -0.172576, -0.030427|-0.107827|[-0.299910, 0.084255]|
|Qwen2.5-0.5B|1/1|native epoll|completion_ms|0.055574, -0.048637, -0.343069, -0.172576, -0.030427|-0.107827|[-0.299910, 0.084255]|
|Qwen2.5-0.5B|1/1|native epoll|tokens_per_s|-28.451373, 25.563845, 107.471254, 87.441160, 13.488085|41.102594|[-28.013129, 110.218317]|
|Qwen2.5-0.5B|1/1|native epoll|known_worker_cpu_s_per_request|9.581969, -3.875594, 4.206188, -5.876750, 3.881344|1.583431|[-6.308492, 9.475354]|
|Qwen2.5-0.5B|64/1|original independent|ttft_ms|-0.185383, -0.145742, -0.504219, -0.061593, 0.181384|-0.143111|[-0.449864, 0.163643]|
|Qwen2.5-0.5B|64/1|original independent|completion_ms|-2.345364, 0.084962, -0.348488, -0.255524, 2.323389|-0.108205|[-2.170478, 1.954068]|
|Qwen2.5-0.5B|64/1|original independent|tokens_per_s|23.822926, -0.846535, 3.515081, 2.547261, -23.496031|1.108541|[-19.788815, 22.005896]|
|Qwen2.5-0.5B|64/1|original independent|known_worker_cpu_s_per_request|-36.396813, -11.686219, -266.846688, -36.408031, -48.292750|-79.926100|[-210.721829, 50.869629]|
|Qwen2.5-0.5B|64/1|original independent|tpot_ms|-0.034285, 0.003662, 0.002472, -0.003078, 0.034000|0.000554|[-0.029599, 0.030707]|
|Qwen2.5-0.5B|64/1|native epoll|ttft_ms|-0.029828, -0.136962, 0.141482, -0.085994, 0.089631|-0.004334|[-0.149932, 0.141264]|
|Qwen2.5-0.5B|64/1|native epoll|completion_ms|0.042917, 0.273730, 0.814435, 0.917220, 2.617945|0.933249|[-0.320806, 2.187304]|
|Qwen2.5-0.5B|64/1|native epoll|tokens_per_s|-0.487514, -2.858754, -8.447232, -9.487400, -26.618861|-9.579952|[-22.295085, 3.135181]|
|Qwen2.5-0.5B|64/1|native epoll|known_worker_cpu_s_per_request|377.004844, 253.881656, 269.603125, -263.576156, 212.076406|169.797975|[-140.348729, 479.944679]|
|Qwen2.5-0.5B|64/1|native epoll|tpot_ms|0.001155, 0.006519, 0.010682, 0.015924, 0.040132|0.014882|[-0.003894, 0.033658]|
|Qwen2.5-0.5B|1/8|original independent|ttft_ms|0.027740, -0.343327, 0.252243, 0.485699, -0.228093|0.038852|[-0.383429, 0.461133]|
|Qwen2.5-0.5B|1/8|original independent|completion_ms|0.027740, -0.343327, 0.252243, 0.485699, -0.228093|0.038852|[-0.383429, 0.461133]|
|Qwen2.5-0.5B|1/8|original independent|tokens_per_s|641.957799, 568.800501, -518.258693, -423.980419, 188.793102|91.462458|[-582.307957, 765.232874]|
|Qwen2.5-0.5B|1/8|original independent|known_worker_cpu_s_per_request|-1.469625, 2.850687, 1.244750, 2.616063, -3.488438|0.350688|[-3.062968, 3.764343]|
|Qwen2.5-0.5B|1/8|native epoll|ttft_ms|-0.547729, -0.944240, -0.562215, 0.528427, -0.143357|-0.333823|[-1.028012, 0.360366]|
|Qwen2.5-0.5B|1/8|native epoll|completion_ms|-0.547729, -0.944240, -0.562215, 0.528427, -0.143357|-0.333823|[-1.028012, 0.360366]|
|Qwen2.5-0.5B|1/8|native epoll|tokens_per_s|523.259753, 808.478446, 710.607703, -448.583902, -137.238510|291.304698|[-396.719257, 979.328653]|
|Qwen2.5-0.5B|1/8|native epoll|known_worker_cpu_s_per_request|1.930656, 1.684344, -3.763937, 5.139625, 1.286250|1.255388|[-2.716087, 5.226862]|
|Qwen2.5-0.5B|64/8|original independent|ttft_ms|0.148440, -0.345641, -0.293447, -0.071039, 0.156904|-0.080957|[-0.375122, 0.213208]|
|Qwen2.5-0.5B|64/8|original independent|completion_ms|-3.546428, 4.075854, 1.665982, -0.412895, 6.014007|1.559304|[-3.092665, 6.211273]|
|Qwen2.5-0.5B|64/8|original independent|tokens_per_s|246.641099, -57.439509, -151.092072, 82.339162, -253.022537|-26.514771|[-270.340498, 217.310955]|
|Qwen2.5-0.5B|64/8|original independent|known_worker_cpu_s_per_request|-35.007406, 27.318094, -135.382125, 36.722125, 8.822875|-19.505288|[-106.917447, 67.906872]|
|Qwen2.5-0.5B|64/8|original independent|tpot_ms|-0.058649, 0.070182, 0.031102, -0.005426, 0.092970|0.026036|[-0.049021, 0.101093]|
|Qwen2.5-0.5B|64/8|native epoll|ttft_ms|0.279984, -0.458720, 0.760027, -0.445675, 0.247901|0.076703|[-0.573578, 0.726985]|
|Qwen2.5-0.5B|64/8|native epoll|completion_ms|0.189593, 0.613800, 4.467719, 1.489641, 6.790942|2.710339|[-0.800489, 6.221167]|
|Qwen2.5-0.5B|64/8|native epoll|tokens_per_s|-62.887151, -64.729358, -348.121185, -13.684775, -348.597007|-167.603895|[-374.057244, 38.849453]|
|Qwen2.5-0.5B|64/8|native epoll|known_worker_cpu_s_per_request|59.631656, 55.119063, 90.389188, 74.226000, 42.997656|64.472713|[41.755903, 87.189522]|
|Qwen2.5-0.5B|64/8|native epoll|tpot_ms|-0.001435, 0.017024, 0.058852, 0.030719, 0.103858|0.041804|[-0.009195, 0.092802]|

## Appendix C: independently authenticated ordinary rounds and eight effects

Short deducts8 warmups. Long deducts2088 authenticated sequential warmup/serial rounds. Counts are rounds, not elapsed GPU work.

| Model | Scope | Path | Blocks0..4 | Mean |
|---|---|---|---|---:|
|SmolLM2-135M|short|original independent|[8, 12, 8, 16, 9]|10.600000|
|SmolLM2-135M|short|native epoll|[8, 16, 9, 8, 8]|9.800000|
|SmolLM2-135M|short|batched independent|[8, 15, 11, 8, 8]|10.000000|
|Qwen2.5-0.5B|short|original independent|[11, 9, 8, 8, 9]|9.000000|
|Qwen2.5-0.5B|short|native epoll|[8, 9, 11, 8, 8]|8.800000|
|Qwen2.5-0.5B|short|batched independent|[8, 8, 10, 8, 9]|8.600000|
|SmolLM2-135M|long|original independent|[270, 264, 332, 266, 267]|279.800000|
|SmolLM2-135M|long|native epoll|[260, 260, 260, 273, 259]|262.400000|
|SmolLM2-135M|long|batched independent|[260, 270, 262, 263, 263]|263.600000|
|Qwen2.5-0.5B|long|original independent|[287, 319, 276, 271, 268]|284.200000|
|Qwen2.5-0.5B|long|native epoll|[260, 261, 259, 262, 261]|260.600000|
|Qwen2.5-0.5B|long|batched independent|[266, 264, 324, 267, 272]|278.600000|

| Model | Scope | Candidate minus | Blocks0..4 | Mean | t95 |
|---|---|---|---|---:|---|
|SmolLM2-135M|short|original independent|[0, 3, 3, -8, -1]|-0.600000|[-6.194382, 4.994382]|
|SmolLM2-135M|short|native epoll|[0, -1, 2, 0, 0]|0.200000|[-1.160175, 1.560175]|
|Qwen2.5-0.5B|short|original independent|[-3, -1, 2, 0, 0]|-0.400000|[-2.655595, 1.855595]|
|Qwen2.5-0.5B|short|native epoll|[0, -1, -1, 0, 1]|-0.200000|[-1.238851, 0.838851]|
|SmolLM2-135M|long|original independent|[-10, 6, -70, -3, -4]|-16.200000|[-54.211957, 21.811957]|
|SmolLM2-135M|long|native epoll|[0, 10, 2, -10, 4]|1.200000|[-7.856490, 10.256490]|
|Qwen2.5-0.5B|long|original independent|[-21, -55, 48, -4, 4]|-5.600000|[-52.245930, 41.045930]|
|Qwen2.5-0.5B|long|native epoll|[6, 3, 65, 5, 11]|18.000000|[-14.827868, 50.827868]|

## Appendix D: all20 descriptive whole-transfer ring rows

Warmup and all transfer cells combined; multishot CQ excess, not per-cell GPU overhead. SQ and CQ each independently drain.

| Model | Block | Path | SQ | CQ | CQ-SQ | Excess/CQ |
|---|---:|---|---:|---:|---:|---:|
|Qwen2.5-0.5B|0|original independent|4213|42675|38462|0.901277|
|Qwen2.5-0.5B|0|batched independent|4204|43562|39358|0.903494|
|Qwen2.5-0.5B|1|original independent|4175|42976|38801|0.902853|
|Qwen2.5-0.5B|1|batched independent|4241|43257|39016|0.901958|
|Qwen2.5-0.5B|2|original independent|4167|37570|33403|0.889087|
|Qwen2.5-0.5B|2|batched independent|3820|33568|29748|0.886201|
|Qwen2.5-0.5B|3|batched independent|4149|34062|29913|0.878193|
|Qwen2.5-0.5B|3|original independent|4040|33155|29115|0.878148|
|Qwen2.5-0.5B|4|batched independent|4255|46100|41845|0.907701|
|Qwen2.5-0.5B|4|original independent|4253|44617|40364|0.904678|
|SmolLM2-135M|0|original independent|4185|33241|29056|0.874101|
|SmolLM2-135M|0|batched independent|4038|28659|24621|0.859102|
|SmolLM2-135M|1|original independent|3906|26531|22625|0.852776|
|SmolLM2-135M|1|batched independent|4155|29940|25785|0.861222|
|SmolLM2-135M|2|original independent|3796|27055|23259|0.859693|
|SmolLM2-135M|2|batched independent|4053|27024|22971|0.850022|
|SmolLM2-135M|3|batched independent|4133|29259|25126|0.858744|
|SmolLM2-135M|3|original independent|4215|30026|25811|0.859622|
|SmolLM2-135M|4|batched independent|4223|31193|26970|0.864617|
|SmolLM2-135M|4|original independent|4154|29872|25718|0.860940|
