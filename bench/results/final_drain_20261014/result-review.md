# Independent result review: completed-response drain before fresh admission

## Separate judgments

- **Run status: valid**, completed for the declared finite local shared-host comparison. Every planned ordinary, real-preflight, candidate protocol and lifecycle run reached terminal status; no invalid baseline interface or correctness failure was found.
- **Tested hypothesis: supported locally** for both vLLM models' gen1/c8 client TTFT versus matched SQ-only, together with fewer aggregate model rounds in the same untraced primary processes. Primary TTFT superiority to native is **inconclusive**. Universal throughput improvement is unsupported; Smol long-output superiority to native and both gen1/c1 superiority-to-native predictions are **contradicted**.
- **Research value: supporting**, as admitted. The completion-frontier intervention adds decision-relevant evidence; preflight/replay/packaging/lifecycle are dependency evidence inside this experiment.
- **Paper impact: mechanism or workload boundary** under the retained user serving objective. No formal paper RQ is invented and no necessary central thesis is challenged.
- **Next paper decision:** retain this evidence for the experimental completion/admission policy, close the unchanged matrix, and keep native, backpressure/fairness, generic-input/backend and full-resource/performance acceptance open. Owner source-selection/publication decisions follow existing authorization; this diagnostic verdict authorizes no new experiment, runtime delta or default promotion.

This is the one fresh independent RESULT REVIEW. No desired verdict was supplied. Only this report was written; no source/raw edits, installation, build, GPU workload/replay, serving restart, session replacement, cleanup, publication, configuration change or delegation occurred.

## Evidence, commands and completion

Source is /workspaces/repository on main, base f232b475a4663731636067c0d2a95fc52603cd82, original yunwei356/bpfusion-dev. TEMP is /tmp/bpfusion-final-drain-woo07fic. The owner prepared bench/results/final_drain_20261014 concurrently; this review uses original TEMP evidence and independent raw recomputation, not archive replay verdicts.

Read complete plan.md/plan-review.md, REPLAY.md, candidate.diff, source_frozen.json, all original/candidate/source_snapshot CUDA/I/O/BPF sources, native userspace_tcp.h, setup/prepare/rebuild/build/environment/package receipts, adapter/client/model sources embedded in raw metadata, all four preflight and twenty full driver files and their executor stdout/terminal records, both protocol trace/reference/network logs, both lifecycle result/stdout/BPF-slot records, host/preservation observations and retained evaluation history. AMK's prior strict eager-HF failure and rejected transfer remain closed/failed; no AMK timing condition exists here.

The authoritative command is /usr/bin/python3 TEMP/run.py full. full.commands.json matches the complete command list in full.exit.json. All twenty actual invocations use TEMP/runtime/bin/python with the declared short_serving.py or transfer_serving.py, --backend vllm --block N --loop-comparison --untraced --reference-path TEMP/frozen_references.json, exact model revision and raw output. Per-executor starts name precisely ./build/vllm_graph_uring_loop_coalesced_original, ./build/vllm_graph_user_network_wait or ./build/vllm_graph_uring_loop_coalesced with the same matching model and bounded300-second service duration. Duration is not a latency acceptance threshold.

All20 drivers/60 executors/120 cells exit0:3840 measured requests/124800 tokens plus480 one-token warmups,4320 complete responses/125280 tokens. Short contexts contribute960 measured one-token requests, transfer2880 requests/123840 tokens. Preflight1 was the sole actual attempt:4 drivers/12 executors/24 cells,192 measured requests/6240 tokens plus96 warmups. No failed, excluded, restarted or replaced serving cell was found. Full wrapper PID391025 is absent, terminal0 at2026-10-14T15:43:07.790518+00:00; preflight/qualification/lifecycle PIDs386630/389771/390528 are also absent.

Blocks0..4 use SQ/native/drain; SQ/drain/native; native/SQ/drain; native/drain/SQ; drain/SQ/native, five of six permutations. Even blocks run short then transfer, Smol then Qwen; odd blocks reverse context/model order and transfer cell order. Every cell has32 requests, identical four literal prompts and index-modulo4 assignment; startup and eight sequential warmups precede timing. Residual order imbalance, drift and contention remain; five blocks are a small uncertainty sample.

The retained observer KeyError came from selecting graph-reference JSONL as status events and was corrected to literal driver files without any executor/raw/oracle rerun. Review-only list-versus-tuple assertion and unavailable libbpf metadata/pkg-config probes were corrected without artifact or workload changes; they are not failed experimental cells.

## Source scope, engagement and fairness

The production diff changes only the existing BF_IO_COALESCED vLLM fresh-admission condition after io_progress, net one line plus comment wording. At retired==seen it now waits for next_final==retired and SQ head==tail. Model arithmetic, AMK, I/O header/BPF/ABI, default/noncoalesced targets, timers, knobs, graph CTA and worker structure are unchanged. Live Makefile,qwen_graph.cu,vllm_graph.py,io_uring_tcp.h,fusion.bpf.c,uring_loop.bpf.c equal HEAD; every captured snapshot equals live source. Raw metadata embeds identical candidate/original CUDA and unchanged network sources.

Native timed epoll_pwait2 is a credible strongest runnable competing delivery mechanism with the same resident per-model vLLM computation. Its actual logs engage timeout_ns60000 and account for all published/completed requests with zero rejection; source implements accept/recv/parse/shared-page publish/streaming/recycle. It is functioning competition, not an interface-failure win or definitionally weak proxy. It is not an official whole-vLLM text/API serving benchmark. Captured f232 SQ-only is a component control, not external SOTA.

All conditions hold model revision,FP16,real prompt/output workload,eight slots,packed prefill,prefix release,graph/head,KVs and greedy sampling fixed. Revisions are SmolLM2-135M93efa2f097d58c2a74874c7e644dbc9b0cee75a2 and Qwen2.5-0.5B-Instruct7ae557604adf67be50417f59c2c2f167def9a775. Realized batches and complete transport resource work differ, as intended; identical realized model rounds are not assumed. No condition gets future requests/reference tokens/additional prompt information at serving time. Frozen pools are correctness checks, not model generators.

Build recipes use -O3 -std=c++17 -arch=sm_120, common cudart, BF_PAD_PREFILL/BF_PREFIX_RELEASE; both coalesced libraries add BF_URING_NETWORK/BF_URING_BPF_LOOP/BF_IO_COALESCED. Independent CPU cuobjdump reconstruction check confirms old ELF normalized SASS equality:3 functions/4888 instruction lines. This authenticates the old control, not candidate/control SASS equality. Candidate trace build uses changed source plus BF_TRACE; four unowned noncoalesced loop_trace artifacts are not candidate receipts.

Common TEMP runtime is Torch2.13.0+cu129/Transformers5.17.0/vLLM0.31.0/libbpf1.6.3 with TEMP LD_LIBRARY_PATH. Raw metadata/bootstrap/entry/build receipts confirm version/source/intended-library engagement. Unchanged vllm_graph.py chooses the library from the entry suffix. Per-process ELF maps were not separately archived; this is source/build/entry/bootstrap provenance, not retrospective maps proof.

short_serving.py and transfer_serving.py differ from matched_serving.py only in literal workload subsets. qualification.py selects the one candidate, fixes one-mode permutation indexing and additionally checks unchanged frozen pools. Wrappers/adapters/analysis/snapshots/raw logs are necessary evidence, not production scaffolding. No new production helper/controller/worker/timer/permanent dependency/configuration layer was found. All source/build work stayed in original Workspace; owned TEMP/runtime/vendor/builds await owner cleanup.

## Independent numerical audit

Direct reconstruction uses raw client start_ns and arrival_ns, not analyzer verdicts:
TTFT=(first arrival-start)/1e6; completion=(last arrival-start)/1e6; TPOT=(last-first)/(gen-1)/1e6, undefined at gen1. One recv can give multiple tokens the same timestamp. These are client observations, not GPU-token durations, and agree with [official vLLM TTFT/TPOT definitions](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics).

Source-native TPS=count*gen*1e9/(last client arrival-first request start), then mean over five process blocks. This fixed finite-wave estimator is not automatically official benchmark overall-duration throughput or open-arrival capacity/SLO. Known-worker CPU is raw executor process-clock plus attributed TX delta divided by32; brackets independently enclose each client window. TX is0 in all these module-free/native cells. Process clocks include attributed syscall time; separately unaccounted kernel/BPF/softirq/client work and energy remain excluded.

Independent stdlib checks rebuilt120 full cell summaries,24 means,72 paired metric effects,30 ordinary short-process round counts and4 round effects from complete raw timestamp/token/counter records. Checks included every cell index/prompt/frozen sequence/source/version/order/actual executor log/model/native/ring terminal/physical slot/bitmap/queue receipt. Every full.analysis.json value agrees within floating tolerance (absolute1e-12 and relative up to1e-11). No effect sign reversed, adverse sample excluded, fixed oracle/timeout/metric/evaluation path changed or original analysis overwritten. Appendix tables are generated from independent reconstruction.

Differences are always Drain-minus-control per paired process block. Nominal two-sided t95df4=mean(d) +/-2.776445105*sample_sd(d)/sqrt(5). These are marginal intervals, not simultaneous familywise coverage. Crossing zero proves neither equivalence/noninferiority nor no effect; means cannot establish arbitrary-peer fairness/tail bounds.

Primary gen1/c8 SQ/native/drain means are5.211340/2.139125/2.188197ms Smol and6.368539/2.638576/2.545532ms Qwen. Drain-minus-SQ is-3.023143[-4.652360,-1.393925] and-3.823006[-4.731456,-2.914557]ms, negative in every block. Ratios of means imply about58.01%/60.03% reductions; ratios are descriptive and lack their own interval. Native contrasts+0.049072[-0.153749,+0.251894] and-0.093044[-0.333415,+0.147328]ms have mixed signs. Prior gap is substantially reduced in point estimates; native equivalence/superiority is unestablished.

## Same-process rounds

Each untraced primary executor contains exactly8 sequential gen1/c1 warmups and32 measured gen1/c8 requests. Raw timestamps show each warmup completes before the next starts. Source zero-initializes Control and increments launches only after successful actual device model rounds; bootstrap graph capture precedes and does not increment this Control. A complete valid gen1 reply requires one model computation and request phase/release prevents a second. Eight warmups therefore contribute exactly8 rounds.

All primary counters admitted==retired==40,graph_error0,trace_overflows0. device_graph_launches minus8 authenticates aggregate measured rounds in the same processes as TTFT. Smol SQ/native/drain vectors are[20,21,12,20,11]/[9,8,9,8,8]/[6,6,5,6,5], means16.8/8.4/5.6. Qwen vectors[17,21,18,14,16]/[8,8,8,8,8]/[6,7,6,5,6], means17.2/8.0/6.0. All candidate round contrasts against both controls are negative; complete signed intervals are appended.

Aggregate counters do not authenticate individual batch membership,GPU duration,per-round cost,ordinary KV trajectory or exclusive causal mediation. Fewer rounds than native coexist with inconclusive client TTFT differences. Joint SQ latency/round changes support the local prediction; attribution exclusively to batching or a particular CQ remains incomplete.

## Transfer and negative evidence

Smol gen64/c8 improves versus SQ+70.946330[+35.366252,+106.526409]TPS, positive every block (about1.35% ratio-of-means), but loses versus native-274.989286[-298.534115,-251.444458], negative every block. Qwen versus SQ+56.200732[-43.628973,+156.030438] and native-133.107826[-275.972521,+9.756869] are inconclusive; adverse SQ block1 and favorable native block0 remain.

Gen1/c1 versus SQ+0.028103[-0.041868,+0.098073] Smol,+0.033352[-0.058582,+0.125285] Qwen are inconclusive. Versus native both lose every block,+0.041246[+0.003834,+0.078659],+0.066603[+0.030970,+0.102237]ms. Smol also loses native gen64/c1 completion/TPS/TPOT and gen64/c8 TTFT/completion/TPS/TPOT with intervals excluding zero.

Known-worker CPU improves against SQ for both primary cells and against native for Qwen primary. All four native long-output candidate CPU contrasts are positive with intervals excluding zero. This is partial attribution, not CPU elimination,total CPU or energy saving. Realized batching,parent/child scheduling,global ordered SEND,loopback transport,order/drift and contention remain competing explanations; no pure PCIe/kernel-vs-userspace or formal mediation effect follows.

## Protocol and lifecycle raw audit

Both candidate protocol runs independently contain622 requests/22224 tokens,259 rejects,5000 empty connections. Every client marker/prompt/gen/reject/token maps to trace references and unchanged frozen pools. Trace622 admissions/releases maintain unique physical ownership id%8,FIFO release,complete histories and no compute-after-release/owner alias. Compute batch cardinality and per-request token history match. Batches1..8 and prompt lengths1,2,5,8,15,16,17,32,64 occur. Cases include30 fragmented requests,all concurrency1..8,256 wrap successes+256 wrap rejects,32 mixed,pipeline half-close/reject,binary reject and recovery.

Replayed packed padding/history/positions/KV pages invoke the reused vLLM graphs/head; each retained replay receipt checks22224 tokens. This is transport/trajectory consistency, not fresh eager-HF arithmetic parity; same graph arithmetic is reused. Reviewer did no GPU replay. Ordinary timing uses unchanged finite whole-output membership and does not observe current batch/KV histories. No post-observation pool widening occurred. Prior AMK strict-HF failure/transfer rejection remain intact.

Protocol strace after readiness has no userspace accept/recv/send-family calls and exactly one steady io_uring_enter before signal; source confirms host kernel BPF-loop/GPU coalesced I/O engagement. Kernel TCP/BPF still consumes CPU and bootstrap threads exist; evidence is no steady userspace request worker on this tested path, not zero userspace activity/arbitrary-kernel portability.

Each protocol ring accepted==closed5086,head==completed622,aborted1; pending/error/reserved/dropped/overflow0,balanced SQ/CQ. The128-record reply diagnostic truncates494 records by design; model trace overflow separately0 and full client/model evidence is retained. Do not call this complete per-request SEND tracing. Physical slots0..7 FREE,bitmap0x0.

Both32-action lifecycle result payloads were checked independently from request_hex/reply_hex/frozen tokens, not pass/exact booleans. Each has652 checked complete-or-prefix tokens,13 connections,32 completions/recycles,3 aborts,zero bitmap,8 FREE slots,zero pending/error/reserved/dropped/overflow/trace_overflow and balanced queues. Smol SQ737/737,CQ323944/323944; Qwen SQ741/741,CQ329422/329422. Raw BPF says uring recycled32,stream publish32,llm_head32,llm_reserved0x0.

Each lifecycle has two intentional one-token prefixes before RST/SIGTERM; post-stop extra bytes are empty.652 checked tokens do not imply all long replies completed. Both model counters admitted32,retired31,device_graph_launches654,graph_error0; last physical slot produced2,then quiesced shutdown abort/recycle. This is an interrupted request, not complete model retirement. Successful terminal/CLEANUP ring_connections_buffers_released establishes finite shutdown/release; the model-quiescence field was not directly sampled after freeing state.

Shutdown source sets page stop,synchronizes model root/children,publishes model_quiesced,launches existing shutdown-only io_network worker,drains kernel loop until finished,then synchronizes that stream before freeing ring/state/registered buffers. No steady network worker is added. Source plus terminal evidence supports this scope without replacing the missing direct quiescence sample.

Control.retired/seen and IoState.next_final/seen count common zero-based admitted FIFO sequences. Model DONE does not release TX ownership. BPF recycle requires owning ring/final tag/exact completion result then FREE/bitmap release; GPU CQ checks active/busy/tag before advancing next_final. Unfinished model work stays eligible and the gate waits only when all admitted work is complete; no tested-path circular wait was found.

Global ordered final SEND remains: backpressure on an earlier final send can stall fresh admission across peers. Finite tests do not prove arbitrary-peer fairness,bounded tails,TCP ACK completion or2^32 rollover. Final SEND CQ is kernel-operation completion,not peer ACK. New equality/inequality adds no ordered-rollover comparison,but physical-slot wraps do not establish full-counter rollover.

## Host, preservation and proposed findings

Host observations at15:04:40.900797,15:16:38.821197,15:17:45.427416,15:28:02.605630,15:43:33.590481 UTC retain lab boot04dc0087-5ccc-4c46-9997-b9a92f0e5167,RTX5090,driver610.57.04,kernel7.3.0-070300rc3-generic. nvcc13.0.88. Inherited400W current GPU limit versus575W default is unchanged; no optimality claim or mutation. Endpoint compute queries empty,during/mid each show one python compute application,Xorg remains; clocks/temperatures vary. These sparse brackets do not prove continuous isolation.

All selected journal observations retain33 older NVRM status0x56 warnings,latest10:50:43UTC,no new selected fault. This is not clean-journal or harmlessness proof and cannot rule out unselected/intermediate faults. No known in-run OOM/storage discontinuity is established in these brackets. Validity is qualified by shared host and sparse evidence.

Default qwen_graph.so remains inode262875,size1032248,mtime1791861786400049402. setup_env.sh and all4 unowned loop_trace artifacts retain inode/size/mtime/symlink equality with preserved_before.json. Coder PIDs1/10909 remain coder. Base Torch2.14.1/Transformers5.19.0 metadata and system libbpf1.3.0 remain; TEMP does not overwrite them. Source/main/snapshots agree; BPF pins and bfusion_tx module are absent after completion. Original Workspace/PVC/session ownership was not changed by reviewer.

The owner supplied concrete draft docs/findings/0053-final-response-drain-before-admission.md during review. All proposed tables,percentages,signs,intervals and adverse secondary claims match independent reconstruction at published rounding. Correctness/pool/replay/32-versus31 stop/partial CPU/host/global-frontier limitations are supported. Owner clarified opening to 'Candidate superiority over native ... not established', avoiding ambiguity with established secondary native wins. No blocking scientific/numeric defect found. Selection/restoration/publication remained pending; reviewer does not certify future actions.

## Release and uncertainty

Review complete; all TEMP/runtime/vendor/build/raw references are released for owner archive/cleanup after preserving this report/replay evidence. No cleanup/publication performed here. Preserve original source/main,setup_env.sh,default qwen_graph.so,4 unowned trace artifacts,base packages,Coder PIDs1/10909,original Workspace/PVC/session.

Remaining uncertainty: native primary TTFT superiority/equivalence,ordinary batch/GPU timing/mediation,Qwen long-output transfer,total CPU/energy,arbitrary traffic/backpressure/tails/rollover,generic text/model/kernel portability. Select a distinct load-bearing discriminator with better decision value than unchanged reruns/packaging/weak controls.

## Appendix: all independent means and signed contrasts

SQ=captured f232 component control; Native=epoll competitor; Drain=candidate. Latency/TPOT ms,TPS output tokens/s,CPU partial known-worker us/request. Block vectors retain0..4 order; effects always Drain-minus-control.

| Model | gen | c | Path | TTFT | Completion | TPS | CPU us/req | TPOT |
|---|---:|---:|---|---:|---:|---:|---:|---:|
| Smol | 1 | 1 | SQ | 1.164022438 | 1.164022438 | 851.386340238 | 42.679512500 | n/a |
| Smol | 1 | 1 | Native | 1.150878537 | 1.150878537 | 863.254254070 | 42.764581250 | n/a |
| Smol | 1 | 1 | Drain | 1.192124962 | 1.192124962 | 830.502820632 | 41.975381250 | n/a |
| Smol | 64 | 1 | SQ | 1.141678706 | 47.341677356 | 1351.011972931 | 1519.468325000 | 0.733333312 |
| Smol | 64 | 1 | Native | 1.136148494 | 46.162824063 | 1385.518366122 | 1317.324368750 | 0.714709136 |
| Smol | 64 | 1 | Drain | 1.132448969 | 47.393050125 | 1349.615747067 | 1534.276843750 | 0.734295256 |
| Smol | 1 | 8 | SQ | 5.211339606 | 5.211339606 | 1574.393584757 | 27.532781250 | n/a |
| Smol | 1 | 8 | Native | 2.139124744 | 2.139124744 | 3382.005106613 | 21.066875000 | n/a |
| Smol | 1 | 8 | Drain | 2.188196875 | 2.188196875 | 3310.210928260 | 19.070481250 | n/a |
| Smol | 64 | 8 | SQ | 1.967116819 | 97.042454400 | 5272.601679342 | 469.293493750 | 1.509132343 |
| Smol | 64 | 8 | Native | 1.808891494 | 91.059925237 | 5618.537296153 | 418.967068750 | 1.416683075 |
| Smol | 64 | 8 | Drain | 1.962336656 | 95.731076188 | 5343.548009822 | 458.582837500 | 1.488392691 |
| Qwen | 1 | 1 | SQ | 1.420325944 | 1.420325944 | 698.092009650 | 51.547706250 | n/a |
| Qwen | 1 | 1 | Native | 1.387074394 | 1.387074394 | 714.372799088 | 46.666975000 | n/a |
| Qwen | 1 | 1 | Drain | 1.453677588 | 1.453677588 | 679.918742141 | 53.961706250 | n/a |
| Qwen | 64 | 1 | SQ | 1.348405862 | 79.576434156 | 803.933244315 | 2511.667900000 | 1.241714735 |
| Qwen | 64 | 1 | Native | 1.355202487 | 78.473334119 | 815.312627239 | 2198.753837500 | 1.224097327 |
| Qwen | 64 | 1 | Drain | 1.372450250 | 79.571891662 | 803.949985731 | 2518.793168750 | 1.241260975 |
| Qwen | 1 | 8 | SQ | 6.368538531 | 6.368538531 | 1234.915464121 | 33.154562500 | n/a |
| Qwen | 1 | 8 | Native | 2.638576106 | 2.638576106 | 2808.793080860 | 24.849987500 | n/a |
| Qwen | 1 | 8 | Drain | 2.545532125 | 2.545532125 | 2733.707343470 | 18.490056250 | n/a |
| Qwen | 64 | 8 | SQ | 2.423142869 | 112.047001556 | 4560.647843886 | 528.803562500 | 1.740061249 |
| Qwen | 64 | 8 | Native | 2.319000275 | 107.650907231 | 4749.956402141 | 465.918956250 | 1.671935031 |
| Qwen | 64 | 8 | Drain | 2.377219694 | 110.795062044 | 4616.848576232 | 512.606231250 | 1.720918133 |

| Model | gen | c | Control | Metric | Block differences 0..4 | Mean | t95 |
|---|---:|---:|---|---|---|---:|---|
| Smol | 1 | 1 | SQ | ttft_ms | -0.011643188, +0.009664500, +0.127479594, +0.012909594, +0.002102125 | +0.028102525 | [-0.041868106, +0.098073156] |
| Smol | 1 | 1 | SQ | completion_ms | -0.011643188, +0.009664500, +0.127479594, +0.012909594, +0.002102125 | +0.028102525 | [-0.041868106, +0.098073156] |
| Smol | 1 | 1 | SQ | tokens_per_s | +12.255293629, -9.582478458, -97.074209522, -7.998569963, -2.017633716 | -20.883519606 | [-74.838282704, +33.071243492] |
| Smol | 1 | 1 | SQ | CPU us/req | +5.315250000, +6.696718750, -0.661625000, -11.950718750, -2.920281250 | -0.704131250 | [-9.962740817, +8.554478317] |
| Smol | 1 | 1 | Native | ttft_ms | +0.023216312, +0.036687094, +0.067567250, +0.003423813, +0.075337656 | +0.041246425 | [+0.003834302, +0.078658548] |
| Smol | 1 | 1 | Native | completion_ms | +0.023216312, +0.036687094, +0.067567250, +0.003423813, +0.075337656 | +0.041246425 | [+0.003834302, +0.078658548] |
| Smol | 1 | 1 | Native | tokens_per_s | -17.723425773, -32.654490264, -51.777403545, -2.311386065, -59.290461542 | -32.751433438 | [-61.994890613, -3.507976263] |
| Smol | 1 | 1 | Native | CPU us/req | -2.775281250, +10.963625000, -1.310750000, -6.566937500, -4.256656250 | -0.789200000 | [-9.295978880, +7.717578880] |
| Smol | 64 | 1 | SQ | ttft_ms | -0.034016500, +0.016158625, -0.002148219, -0.021979125, -0.004163469 | -0.009229738 | [-0.033252923, +0.014793448] |
| Smol | 64 | 1 | SQ | completion_ms | +0.165237906, -0.016686000, -0.131185219, +0.083585813, +0.155911344 | +0.051372769 | [-0.104319566, +0.207065104] |
| Smol | 64 | 1 | SQ | tokens_per_s | -4.515597767, +0.488000065, +3.847695440, -2.334361777, -4.466865284 | -1.396225865 | [-5.833695030, +3.041243300] |
| Smol | 64 | 1 | SQ | CPU us/req | -9.672937500, +51.010375000, -40.264968750, +74.582906250, -1.612781250 | +14.808518750 | [-43.383153157, +73.000190657] |
| Smol | 64 | 1 | SQ | tpot_ms | +0.003162768, -0.000521343, -0.002048206, +0.001675634, +0.002540870 | +0.000961945 | [-0.001751818, +0.003675707] |
| Smol | 64 | 1 | Native | ttft_ms | +0.019276250, -0.046535688, -0.005976688, -0.001569875, +0.016308375 | -0.003699525 | [-0.036391267, +0.028992217] |
| Smol | 64 | 1 | Native | completion_ms | +1.169779375, +1.136898031, +1.134910781, +1.188325469, +1.521216656 | +1.230226063 | [+1.026313122, +1.434139003] |
| Smol | 64 | 1 | Native | tokens_per_s | -33.839120174, -33.403490015, -32.853279759, -34.861564801, -44.555640527 | -35.902619055 | [-41.977919929, -29.827318182] |
| Smol | 64 | 1 | Native | CPU us/req | +259.352687500, +200.353000000, +180.391250000, +246.038437500, +198.627000000 | +216.952475000 | [+174.882872053, +259.022077947] |
| Smol | 64 | 1 | Native | tpot_ms | +0.018261954, +0.018784662, +0.018109325, +0.018887228, +0.023887433 | +0.019586120 | [+0.016572276, +0.022599965] |
| Smol | 1 | 8 | SQ | ttft_ms | -3.947386250, -4.393878000, -1.506926781, -3.514498031, -1.753024594 | -3.023142731 | [-4.652360409, -1.393925054] |
| Smol | 1 | 8 | SQ | completion_ms | -3.947386250, -4.393878000, -1.506926781, -3.514498031, -1.753024594 | -3.023142731 | [-4.652360409, -1.393925054] |
| Smol | 1 | 8 | SQ | tokens_per_s | +1958.266907486, +1984.486462255, +1500.876406825, +1462.570872154, +1772.886068792 | +1735.817343502 | [+1430.058304155, +2041.576382849] |
| Smol | 1 | 8 | SQ | CPU us/req | -10.167312500, -17.852531250, -5.310531250, -8.200843750, -0.780281250 | -8.462300000 | [-16.317700023, -0.606899977] |
| Smol | 1 | 8 | Native | ttft_ms | +0.095703000, +0.089908312, +0.012504969, +0.247512625, -0.200268250 | +0.049072131 | [-0.153749459, +0.251893721] |
| Smol | 1 | 8 | Native | completion_ms | +0.095703000, +0.089908312, +0.012504969, +0.247512625, -0.200268250 | +0.049072131 | [-0.153749459, +0.251893721] |
| Smol | 1 | 8 | Native | tokens_per_s | -57.913967766, -336.183992780, +238.794927690, -494.154970029, +290.487111120 | -71.794178353 | [-500.211712865, +356.623356159] |
| Smol | 1 | 8 | Native | CPU us/req | -2.034968750, -4.254718750, -5.157656250, +2.495187500, -1.029812500 | -1.996393750 | [-5.731908566, +1.739121066] |
| Smol | 64 | 8 | SQ | ttft_ms | +0.150888094, -0.087108375, -0.052127281, -0.028060625, -0.007492625 | -0.004780162 | [-0.118921485, +0.109361160] |
| Smol | 64 | 8 | SQ | completion_ms | -1.111143844, -0.809574594, -1.894936688, -1.284954687, -1.456281250 | -1.311378212 | [-1.813499005, -0.809257420] |
| Smol | 64 | 8 | SQ | tokens_per_s | +61.325241741, +43.098395524, +114.727220097, +52.303088951, +83.277706088 | +70.946330480 | [+35.366251973, +106.526408987] |
| Smol | 64 | 8 | SQ | CPU us/req | -36.736906250, +16.491468750, -24.066718750, +8.560906250, -17.802031250 | -10.710656250 | [-38.595527257, +17.174214757] |
| Smol | 64 | 8 | SQ | tpot_ms | -0.020032253, -0.011467718, -0.029250943, -0.019950699, -0.022996645 | -0.020739652 | [-0.028705381, -0.012773922] |
| Smol | 64 | 8 | Native | ttft_ms | +0.285252563, +0.073245062, +0.147505906, +0.100056594, +0.161165688 | +0.153445162 | [+0.051904550, +0.254985775] |
| Smol | 64 | 8 | Native | completion_ms | +4.800254281, +4.764715656, +4.194927687, +4.896120281, +4.699736844 | +4.671150950 | [+4.329051126, +5.013250774] |
| Smol | 64 | 8 | Native | tokens_per_s | -294.221856785, -253.012009305, -263.472366110, -268.871530349, -295.368669105 | -274.989286331 | [-298.534114632, -251.444458030] |
| Smol | 64 | 8 | Native | CPU us/req | +64.949656250, +34.234218750, +3.790906250, +32.642656250, +62.461406250 | +39.615768750 | [+8.420982983, +70.810554517] |
| Smol | 64 | 8 | Native | tpot_ms | +0.071666694, +0.074467787, +0.064244790, +0.076127995, +0.072040812 | +0.071709616 | [+0.066054769, +0.077364463] |
| Qwen | 1 | 1 | SQ | ttft_ms | +0.005461813, +0.039918281, -0.043791437, +0.010792375, +0.154377187 | +0.033351644 | [-0.058582070, +0.125285358] |
| Qwen | 1 | 1 | SQ | completion_ms | +0.005461813, +0.039918281, -0.043791437, +0.010792375, +0.154377187 | +0.033351644 | [-0.058582070, +0.125285358] |
| Qwen | 1 | 1 | SQ | tokens_per_s | -0.822303480, -24.324986334, +22.683790311, -7.230716853, -81.172121186 | -18.173267508 | [-66.649051886, +30.302516869] |
| Qwen | 1 | 1 | SQ | CPU us/req | +2.494625000, +8.760812500, +1.283093750, -1.926906250, +1.458375000 | +2.414000000 | [-2.447719666, +7.275719666] |
| Qwen | 1 | 1 | Native | ttft_ms | +0.050751469, +0.068383500, +0.043386531, +0.055200062, +0.115294406 | +0.066603194 | [+0.030969786, +0.102236602] |
| Qwen | 1 | 1 | Native | completion_ms | +0.050751469, +0.068383500, +0.043386531, +0.055200062, +0.115294406 | +0.066603194 | [+0.030969786, +0.102236602] |
| Qwen | 1 | 1 | Native | tokens_per_s | -26.963181055, -40.145410292, -15.179512914, -31.334851093, -58.647329380 | -34.454056947 | [-54.619695682, -14.288418212] |
| Qwen | 1 | 1 | Native | CPU us/req | +4.193281250, +8.572937500, +13.290593750, +12.129468750, -1.712625000 | +7.294731250 | [-0.352102722, +14.941565222] |
| Qwen | 64 | 1 | SQ | ttft_ms | +0.024034750, +0.000976937, +0.074663750, +0.008324750, +0.012221750 | +0.024044387 | [-0.012586326, +0.060675101] |
| Qwen | 64 | 1 | SQ | completion_ms | -0.087699844, -0.010070781, +0.026000969, +0.010750531, +0.038306656 | -0.004542494 | [-0.066465736, +0.057380748] |
| Qwen | 64 | 1 | SQ | tokens_per_s | +0.821473488, +0.141468116, -0.340798789, -0.127600809, -0.410834930 | +0.016741415 | [-0.602425036, +0.635907867] |
| Qwen | 64 | 1 | SQ | CPU us/req | -29.821625000, +71.112687500, -19.270781250, -14.687906250, +28.293968750 | +7.125268750 | [-45.113760368, +59.364297868] |
| Qwen | 64 | 1 | SQ | tpot_ms | -0.001773565, -0.000175361, -0.000772425, +0.000038504, +0.000414046 | -0.000453760 | [-0.001513975, +0.000606455] |
| Qwen | 64 | 1 | Native | ttft_ms | -0.054613031, +0.016040094, +0.068399281, +0.028648281, +0.027764188 | +0.017247763 | [-0.038359093, +0.072854618] |
| Qwen | 64 | 1 | Native | completion_ms | -0.702458719, +1.530510312, +1.565621344, +1.540130625, +1.558984156 | +1.098557544 | [-0.151670911, +2.348785999] |
| Qwen | 64 | 1 | Native | tokens_per_s | +7.005121089, -15.709677244, -16.141295906, -15.898678526, -16.068676951 | -11.362641508 | [-24.113590143, +1.388307127] |
| Qwen | 64 | 1 | Native | CPU us/req | +149.535562500, +373.292625000, +306.715750000, +452.460562500, +318.192156250 | +320.039331250 | [+181.740365996, +458.338296504] |
| Qwen | 64 | 1 | Native | tpot_ms | -0.010283265, +0.024039210, +0.023765430, +0.023991783, +0.024305079 | +0.017163647 | [-0.001889052, +0.036216347] |
| Qwen | 1 | 8 | SQ | ttft_ms | -3.927976000, -4.775062594, -4.150780281, -2.849999375, -3.411213781 | -3.823006406 | [-4.731455927, -2.914556885] |
| Qwen | 1 | 8 | SQ | completion_ms | -3.927976000, -4.775062594, -4.150780281, -2.849999375, -3.411213781 | -3.823006406 | [-4.731455927, -2.914556885] |
| Qwen | 1 | 8 | SQ | tokens_per_s | +1512.807687628, +1460.625943005, +1540.664756747, +1602.272156401, +1377.588852964 | +1498.791879349 | [+1393.424487587, +1604.159271111] |
| Qwen | 1 | 8 | SQ | CPU us/req | -14.873093750, -11.579781250, -13.938875000, -18.029812500, -14.900968750 | -14.664506250 | [-17.540960894, -11.788051606] |
| Qwen | 1 | 8 | Native | ttft_ms | -0.274157687, +0.235791875, -0.136617812, -0.116410375, -0.173825906 | -0.093043981 | [-0.333415493, +0.147327531] |
| Qwen | 1 | 8 | Native | completion_ms | -0.274157687, +0.235791875, -0.136617812, -0.116410375, -0.173825906 | -0.093043981 | [-0.333415493, +0.147327531] |
| Qwen | 1 | 8 | Native | tokens_per_s | -98.999766968, -376.484203647, -148.368300961, +163.015206287, +85.408378339 | -75.085737390 | [-337.921158843, +187.749684064] |
| Qwen | 1 | 8 | Native | CPU us/req | -4.023062500, -5.581375000, -7.944843750, -5.866875000, -8.383500000 | -6.359931250 | [-8.591214581, -4.128647919] |
| Qwen | 64 | 8 | SQ | ttft_ms | -0.102348969, +0.167161469, +0.041433781, -0.315767688, -0.020094469 | -0.045923175 | [-0.269511798, +0.177665448] |
| Qwen | 64 | 8 | SQ | completion_ms | -1.693387156, +2.167355531, -2.668311812, -1.947790531, -2.117563594 | -1.251939513 | [-3.666495459, +1.162616434] |
| Qwen | 64 | 8 | SQ | tokens_per_s | +82.153782237, -85.588494532, +112.700499909, +77.924615594, +93.813258520 | +56.200732345 | [-43.628973222, +156.030437913] |
| Qwen | 64 | 8 | SQ | CPU us/req | +15.160375000, +25.291343750, -27.242093750, -50.981562500, -43.214718750 | -16.197331250 | [-59.059406305, +26.664743805] |
| Qwen | 64 | 8 | SQ | tpot_ms | -0.025254574, +0.031749112, -0.043011835, -0.025905125, -0.033293161 | -0.019143116 | [-0.055571902, +0.017285669] |
| Qwen | 64 | 8 | Native | ttft_ms | +0.047846438, +0.272038594, +0.192780219, -0.126499750, -0.095068406 | +0.058219419 | [-0.158228630, +0.274667468] |
| Qwen | 64 | 8 | Native | completion_ms | -1.790144344, +4.760276687, +4.062263250, +4.777803875, +3.910574594 | +3.144154812 | [-0.315739730, +6.604049355] |
| Qwen | 64 | 8 | Native | tokens_per_s | +72.420454096, -194.359887852, -184.136391465, -181.874689172, -177.588615152 | -133.107825909 | [-275.972520916, +9.756869098] |
| Qwen | 64 | 8 | Native | CPU us/req | +35.967000000, +65.810187500, +51.436781250, +51.201687500, +29.020718750 | +46.687275000 | [+28.740450907, +64.634099093] |
| Qwen | 64 | 8 | Native | tpot_ms | -0.029174457, +0.071241875, +0.061420366, +0.077846089, +0.063581635 | +0.048983101 | [-0.005864627, +0.103830830] |

| Model | Path | Measured rounds by block | Mean |
|---|---|---|---:|
| Smol | SQ | [20, 21, 12, 20, 11] | 16.800000000 |
| Smol | Native | [9, 8, 9, 8, 8] | 8.400000000 |
| Smol | Drain | [6, 6, 5, 6, 5] | 5.600000000 |
| Qwen | SQ | [17, 21, 18, 14, 16] | 17.200000000 |
| Qwen | Native | [8, 8, 8, 8, 8] | 8.000000000 |
| Qwen | Drain | [6, 7, 6, 5, 6] | 6.000000000 |

| Model | Control | Round differences by block | Mean | t95 |
|---|---|---|---:|---|
| Smol | SQ | [-14, -15, -7, -14, -6] | -11.200000000 | [-16.569389291, -5.830610709] |
| Smol | Native | [-3, -2, -4, -2, -3] | -2.800000000 | [-3.838850634, -1.761149366] |
| Qwen | SQ | [-11, -14, -12, -9, -10] | -11.200000000 | [-13.588388388, -8.811611612] |
| Qwen | Native | [-2, -1, -2, -3, -2] | -2.000000000 | [-2.877989033, -1.122010967] |

Independent counts: {'preflight1_executors': 12, 'preflight1_warmups': 96, 'preflight1_cells': 24, 'preflight1_requests': 192, 'preflight1_tokens': 6240, 'full_executors': 60, 'full_warmups': 480, 'full_cells': 120, 'full_requests': 3840, 'full_tokens': 124800}.

Review completed UTC: 2026-10-14T15:58:51.249340+00:00.

Lifecycle strace final audit: each full file contains53 startup network-family calls; independently filtering at retained ready_time_ns leaves zero accept/recv/send-family calls. Each active trace retains the stop/drain io_uring_enter; complete trace tails exit0. Both native stderr files contain no Error/error/Failed/failed/Traceback lines. Startup communication is not mislabeled steady request processing.
