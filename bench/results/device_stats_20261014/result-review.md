# Independent result review: GPU-local I/O bookkeeping

Reviewed on 2026-10-14 by a fresh independent RESULT REVIEW reviewer, separate from the plan reviewer. No desired verdict was supplied. Evidence root: `/tmp/bpfusion-device-stats-o8xxqd_q` in the original `yunwei356/bpfusion-dev` Workspace; repository `/workspaces/repository`, main, base `34eb2b0b7b1d282d47766a4125df2e216c952c09`.

## Final judgments

| Judgment | Result |
|---|---|
| Run status | **valid, completed**, within the fixed finite workload and oracle scope |
| Tested bookkeeping-placement hypothesis, candidate vs old | **inconclusive for both models** on the declared primary gen64/c8 output TPS |
| Candidate superiority over native, Smol | **contradicted** on primary gen64/c8 TPS |
| Candidate superiority over native, Qwen | **inconclusive** on primary gen64/c8 TPS |
| Research value | **supporting**, because this is a new component discriminator with a useful bounded negative/inconclusive outcome; qualification/setup alone are dependencies |
| Paper impact | **mechanism/workload boundary**, with additional evidence toward the retained serving question; **no direct thesis challenge** |
| Next paper decision | Do not report a demonstrated bookkeeping-placement TPS gain or native superiority. Prefer retaining the already-selected host-stats constructor absent a separate rationale for accepting added allocation/control complexity. Preserve the full signed evidence and direct the next research decision toward a new causal discriminator, rather than an unchanged repetition or a rounded positive claim. |

The retained question is the user's complete Linux TCP/HTTP + eBPF/sockmap → shared queue → resident real-model GPU → asynchronous kernel TCP reply path, without a steady userspace request worker and with reused model computation. `docs/evaluation.md` states there is no formal paper RQ or thesis contract; `docs/idea-story.md` is absent. I have not invented or rewritten one. This valid local experiment does not settle the whole serving question. Its correctness success and native comparison bound this constructor on these models, prompts, concurrency and fixed-output budgets.

## Primary decision, without substituting secondary latency

Primary means and paired differences below are client output tokens/s for gen64/c8. The difference is candidate minus the named comparator. Each nominal t95 interval uses five paired process blocks, df4 and coefficient 2.776445105.

| Model | Candidate mean | Old host-stats mean | Native epoll mean | Candidate minus old [t95] | Candidate minus native [t95] |
|---|---:|---:|---:|---:|---:|
| SmolLM2-135M | 5408.676747165 | 5362.058559261 | 5616.194252586 | +46.618187904 [-0.127399764, +93.363775571] | -207.517505421 [-233.892259036, -181.142751806] |
| Qwen2.5-0.5B | 4628.035685146 | 4601.192658397 | 4757.707057853 | +26.843026748 [-4.781485089, +58.467538586] | -129.671372708 [-295.373505738, +36.030760323] |

Smol's candidate-minus-old interval is **[-0.127399764, +93.363775571]**, not strictly positive, even though every paired TPS difference is positive. Rounding the lower bound to zero or replacing the decision with its positive completion/TPOT results would violate the plan. The mean is approximately +0.8694% of old, but no equivalence/non-regression or material-gain conclusion follows. Qwen's old-control interval also crosses zero; one block loses to old. Relative to native, Smol loses approximately 3.6950% in mean TPS with all five blocks negative and a strictly negative interval. Qwen's mean is lower by approximately 2.7255%, but its interval crosses zero and its first block is positive. That block remains in the estimate; it is not an exclusion candidate merely because it differs from the other four.

Smol old-control completion (-0.815584ms) and TPOT (-0.012270ms) have negative nominal intervals. Qwen short/c8 TTFT improves over native (-0.171856ms, [-0.238178,-0.105534]). These are useful secondary observations. They do not turn either old-control primary TPS interval into support. Smol's native long/c8 completion and TPOT are adverse, as are its serial gen1 and gen64 native TPS comparisons. Qwen gen64/c1 TTFT and known-worker CPU are adverse versus native even though its TPS remains inconclusive. Every secondary signed row, including those with zero-crossing intervals, is retained below.

## Completion, commands and deviations

I read the complete plan and 230-line `plan-review.md` before judging results. The review admits the supporting experiment and asks for ordinary long-round analysis in addition to the short-only primary analyzer. That missing analysis has now been supplied as `long_counter_analysis.py` with retained terminal receipt and stdout; this adds the predeclared secondary computation without changing the measurement contract.

The actual full PID412412 is absent from `/proc`. `full.pid.json` starts at 17:20:31.329820 UTC; `full.exit.json` is exit0 at **17:47:25.139737 UTC**. `full.stdout` contains all20 driver terminal successes in planned order; all20 separate exits are0 and driver stderr files are empty. Expanded `full.commands.json` matches the exit receipt. The collection command is `python3 TEMP/run.py full`, with TEMP the evidence root. It expands source-native adapters under TEMP's Python runtime, `--backend vllm --block 0..4 --loop-comparison --untraced --reference-path TEMP/frozen_references.json`, the exact cached model revision and per-driver output path. Commands were frozen before collection; no failure replacement or partial prefix is used.

Coverage independently reconstructs **20 drivers /60 terminal executors /120 measured cells /3840 measured requests /124800 measured output tokens**, plus **480 sequential one-token warmups**, hence4320 complete replies125280 output tokens. Each cell has32 measured requests, each executor eight warmups. Four real preflight1 drivers and their fixed analysis exit0 precede collection; no later preflight attempt or modified oracle/timeout is present. Two qualification drivers and two lifecycle drivers also exit0. Primary, qualification, long-counter and lifecycle analyses all have terminal exit0 receipts; full analysis completes at17:47:37.436673 UTC.

I inspected setup/build/control-rebuild/candidate receipts and recipes. Setup exit0 at16:50:07; saved old-source reconstruction/rebuild exit0 at17:04:25; implementation and candidate build complete at17:04:34, prior to frozen-source capture17:13:46 and full collection. The retained preparation note records a parse-time seed error before any state mutation. Compiler stderr contains the recorded user-space kernel-header warnings, not a hidden failed performance cell. No source/metric/oracle/timeout repair after measurement is evidenced. The experimental source is exactly29 insertions/2 deletions in the existing shared header; git remains on main at the base commit with that dirty header and unrelated `tools/setup_env.sh`.

## Independent recomputation and completeness audit

I independently reconstructed every request's TTFT, completion and TPOT from client start/arrival timestamps and recomputed every finite-cell TPS as `32*gen / ((last_arrival-first_send)/1e9)`. I checked all120 cells against saved values, all24 means and all72 signed metric contrasts with their five paired vectors and nominal t95 intervals. Known-worker CPU subtraction is checked against before/after executor and attributable kernel-task samples; timestamp bracketing is additionally checked by replaying the existing analyzer. No request count is treated as the statistical sample count: inference uses five paired blocks.

I replayed `analysis.analyze` on all20 ordinary raw JSONLs without executing its writing main. Its raw checks cover terminals, executor exits, pool membership, all requested tokens, zero graph/model trace errors, admitted=retired, native completed/published accounting, ring pending/error/reservation/drop/overflow, separately balanced SQ/CQ, actual BPF FREE slots/bitmap and recorded result consistency. Every raw stdout file matches the corresponding captured executor stdout. I independently reran the long-counter computation in memory and matched all30 rows, six path summaries and four round contrasts byte-for-value against retained stdout. All30 short counters and four short contrasts were checked against the raw executor counters; all three contexts' captured source and request timestamp authentication support the deductions.

The report's tables are renderings of these verified quantities, not a second experiment-control format. No number, cell or block was removed for being adverse/inconclusive. There is no proposed paper figure claiming unverified GPU time, mediation, PCIe transactions, equivalence, energy or overall SOTA. The mean/contrast tables below are the appropriate paper-facing numerical support for this bounded comparison.

## Treatment engagement, control separation and resource lifetime

`candidate.diff`, candidate header, source snapshot and actual `executor/io_uring_tcp.h` agree. Every captured source path in `source_frozen.json` remains byte-identical to the post-run repository. I checked the ordinary metadata captures against current client, vLLM backend/dispatcher, candidate header and captured original source. Model CUDA source equals the captured original; the only production change is bookkeeping placement/control indirection, not math/admission/timer changes.

The mapped `IoStats` report starts with the unchanged `bf_uring_loop_control`. `io_memory` zero-initializes/registers that report. Bootstrap creates the60us multishot timeout, sets report pending=1, submits it and attaches the kernel loop **before** allocation/upload of private stats. `cudaMalloc(sizeof(IoStats))` followed by the full initial host-to-device copy therefore retains the timeout pending count. The private copy's loop prefix is unused for coordination. `IoState.out` points to private stats, while `IoState.control` points to the original mapped `dreport->loop`; ordinary GPU accounting/pending/error/records use out.

GPU abort/quiescence checks read live `control->model_quiesced`, and completion writes live `control->finished`. Host signal/stop/deadline/drain and BPF region registration/read paths all use the original report's control prefix. BPF reads only that control structure and ring offsets, not the private bookkeeping suffix. The model dispatcher still advances io_progress after publication/before fresh admission and retains its final-response/SQ drain rule. FIFO tagged final SEND/abort recycling and physical reservation release are unchanged. No stale private stop/finished flag is substituted.

On shutdown, vLLM first synchronizes the model stream, then sets mapped model_quiesced and launches the shutdown-only network worker. Host/BPF drains until mapped finished; device synchronization and `uring_finish`'s network-stream synchronization precede the final copy. `cudaMemcpy` downloads only `[offsetof(IoStats,accepted), sizeof(IoStats))`, preserving live loop control. Report printing precedes freeing state/stats; loop link/object and ring are released, signal_control is nulled before unregistering report, mapped regions are unregistered/unmapped and stream destroyed. Successful runtime receipts agree with these lifetimes. This is source-plus-successful-shutdown evidence; there is **no direct after-free sampling of quiescence**, and abnormal early exits do not inherit a successful cleanup guarantee.

Scope is small and justified by the placement test: one internal control pointer, one private stats allocation, initial upload, suffix download/free and control-access substitutions, with a cstddef include. No public flag, new abstraction layer, persistent entity/configuration or permission change was introduced. Existing default/noncoalesced paths use the original report pointer and are unchanged by preprocessing. The common BF_IO_COALESCED header also changes optional AMK coalesced construction; AMK source behavior cannot be described as entirely unchanged. AMK is unqualified by this run and its older strict eager-HF failure remains failed. A suffix-only private struct might avoid copying unused loop bytes, but adds an ABI/refactor and is not needed for this test; no untested source change is recommended as a result-review repair.

## Main baseline and comparison fairness

Efficient native epoll is the one main competing delivery mechanism; old host-mapped stats is a component control. All20 native executors engage `vllm_graph_user_network_wait`, print `epoll_pwait2 timeout_ns=60000`, complete40 short or104 transfer requests (including warmups), and exit0 with model errors0. Source inspection confirms nonblocking accept4/recv/sendmsg, real epoll readiness and identical page ABI/resident GPU dispatcher. This is a credible CPU request/reply alternative, not an avoidably broken or definitionally losing baseline. Primary runs omit tracing to avoid contaminating timing; mechanism engagement is grounded in exact commands, build definitions, native marker/source and completed work, not an invented per-request native syscall trace.

All paths load the same cached Smol revision `93efa2f097d58c2a74874c7e644dbc9b0cee75a2` or Qwen revision `7ae557604adf67be50417f59c2c2f167def9a775`, same four token-ID prompts, FP16 weights/KV, captured vLLM math, packed prefill/prefix release policy, eight warmups and request/token budgets. vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0/libbpf1.6.3, Python3.12.3, sm_120 build, RTX5090, driver610.57.04 and kernel7.3.0-070300rc3 are retained. Existing protocol-cache sizing and in-process graph bootstrap are identical across conditions; neither is a treatment-specific tuning concession. Different transport-driven scheduling and round shape are possible outcomes; identical source/reused kernels do not mean identical dynamic batches or fixed model elapsed time.

I independently re-extracted normalized SASS from the saved pre-rebuild OLD ELF and rebuilt original coalesced ELF using cuobjdump: three functions,4888 normalized instruction lines, equal. This validates reconstructing the old component control. It does **not** assert instruction equality of candidate and old or native; placement/control-pointer changes may affect compiled layout. Raw full commands use no BF_TRACE suffix or --trace-output. The five path permutations cover five of six orders; odd blocks reverse contexts/models/transfer cells. This mitigates but does not eliminate order/drift confounding. No native failure is counted as a candidate win.

## Correctness, oracle independence and lifecycle boundary

For each model I reprocessed the entire qualification driver JSONL, GPU compute/admission/release trace and reference JSONL. Smol and Qwen each check **622 requests/22224 valid tokens/259 deliberate rejections**, plus **5000 empty connections**. Actual batch sizes cover1..8, compute histories reproduce request token sequences, release histories preserve physical ownership/order, whole-output membership matches the pre-observation frozen pools, and both terminal model traces report no overflow. Smol has6939 compute graphs216 prefill6723 decode,153 release rounds; Qwen7057 graphs189 prefill6868 decode,116 releases; max release8 for both. The finite reply-record buffer's expected diagnostic truncation494 beyond128 is separate from zero model-trace overflow and zero ring CQ overflow.

I read the qualification network trace after the actual ready marker: neither model shows steady userspace accept/receive/send syscalls; each has exactly one steady io_uring_enter before the stop signal. Initial bootstrap, kernel execution and shutdown remain real CPU work. This supports the specified no-steady-userspace-request-worker mechanism only on the traced qualification workload.

The oracle is not defined by accepting the current run's own output as truth: ordinary timing is checked against the previously frozen finite sequence pools, with source_commit8323c32 and pre-performance freeze provenance. Traced qualification rebuilds histories/KV and reruns upstream vLLM graph computation using the same reused arithmetic. Thus it independently checks transport/dispatcher trajectory delivery, but it is **not fresh eager-HF arithmetic parity** and does not validate arbitrary prompts, checkpoints, precision or general text quality. Ordinary untraced dynamic trajectories remain unobserved; membership in a finite known set is the honest fidelity bound. No AMK HF/performance acceptance follows.

For each raw lifecycle tree I decoded actual reply bytes against frozen complete/prefix sequences, instead of trusting pass/exact booleans. Each has32 actions and652 checked complete-or-prefix tokens: repeated idle reconnects, explicit rejects, binary close, half-close, reset after one real token and SIGTERM during inference. Both have accepted=closed13, completed=head32, three aborts, pending/error/reserved/drop/overflow0; SQ740/740 and CQ325700/325700 Smol or330608/330608 Qwen. BPF raw stats report recycle32, bitmap0, llm_head32 and all eight physical slots state0/FREE. Model admitted32/retired31 is intentional stop-active inference accounting, not falsely claimed complete model retirement. No remaining pins and cleanup stdout support ring/connection/buffer release. Post-ready lifecycle strace has no userspace network accept/receive/send syscalls. Only652 checked tokens are claimed; post-stop extra bytes and aborted suffixes are not promoted to complete oracle coverage.

## Counters, environment and uncertainty

Captured successful nonempty graph launch increments once per model round, and each selected active valid request produces one token per round. Sequential warmup timestamps, nonoverlapping serial requests, publication/final-send/recycle ordering and identical captured source authenticate the deductions: short rounds minus8; transfer rounds minus(8 +32 +32*64)=2088, leaving gen64/c8. Aggregate round counts cannot measure batch membership, padding cost, GPU time or mediate TPS.

Short candidate vs old round intervals cross0 for both models; candidate uses fewer aggregate rounds than native (Smol -3, Qwen -2.6 with negative nominal intervals) without a supported short TPS gain. Long candidate vs old counters also cross0. Smol candidate long/c8 uses1.8 fewer rounds than native with a negative interval but still loses primary TPS, bounding the explanation that extra aggregate rounds cause its loss. Qwen long-round native contrast crosses0. Whole-transfer excess CQ fractions range87.9422–92.3438%; they count multishot timeout traffic across warmup/serial/concurrent/shutdown time, not an88–92% GPU-cost fraction or a per-cell performance attribution.

Sparse host preflight/before/during/mid/after snapshots share boot ID04dc0087-5ccc-4c46-9997-b9a92f0e5167. All retain the same33 selected NVRM reference-state fault messages; no new selected fault appears in these receipts. Before/after GPU app lists are empty; during/mid list one Python GPU process. Preflight lists another Python observation. These snapshots are neither continuous exclusivity nor all-fault-free proof, and do not identify every unobserved competing task or energy cost. No host tuning or other-workload interruption was done by this reviewer. Known-worker CPU is partial executor/kernel-task attribution, excluding total BPF/RX/TCP/softirq/client activity; even a zero recorded kernel-task term is not kernel CPU elimination.

Intervals are nominal paired t95 at N5, sensitive to distribution/drift and without simultaneous familywise coverage over72 contrasts. Zero-crossing is inconclusive, not equivalence/noninferiority. Many secondary positive observations coexist with negative/unresolved rows; selecting favorable latency/CPU/round rows to override the predeclared primary would be a reporting defect. Nothing in these limits invalidates the bounded completed run, but they constrain its claims.

## Research decision and residual uncertainties

No blocking execution or correctness defect was found for the declared finite vLLM experiment. The decisive claim defect would be describing either old-control TPS comparison as supported, Smol native superiority, Qwen equivalence/non-regression, total CPU freedom, isolated PCIe/cache mediation, fresh eager-HF parity, AMK correctness transfer or universally unchanged AMK coalesced behavior. Those claims are unsupported by this record and must not appear in publication.

For source selection I recommend the already-selected host-stats path: the candidate adds a resource/control split while its primary gain is inconclusive in both models, and there is no correctness need requiring that addition. This is evidence-based advice, **not an authorization or a demand to undo a commit**. A maintainer may retain an explicitly experimental candidate for a separately stated reason, but cannot label retention proof of performance benefit; no model-specific knob is justified by these data. The source correction/selection/publication belongs to the owning workflow; this review edits none of it.

The experiment is supporting, not dependency-only/redundant: changing bookkeeping residence was not settled by earlier round-count data or CUDA guidance and it meaningfully limits that explanation/constructor. It does not directly challenge a necessary thesis prediction because no such formal contract is present and the tested intervention is optional. No idea-story rewrite or iterative redesign is required. The next scientific choice should discriminate remaining per-round shape/padding, mandatory ring/CQ work, synchronization/wait cadence or client delivery overhead using matched reused computation, only when that new evidence outranks competing experiments. Existing raw evidence should be reused first; an unchanged rerun solely to move Smol's nearly-zero confidence bound is not a new causal discriminator.

Residuals are small-N inference/order drift, finite frozen-pool fidelity and unobserved ordinary trajectories, only two small checkpoints/four prompts/local token-ID HTTP-binary scope, sparse host state, partial CPU accounting, unmeasured dynamic shape/GPU timing and indirect quiescence lifetime proof. These are boundaries to retain, not authority to expand this completed experiment.

## Numerical appendix: every mean and signed contrast

CPU entries are known-worker **microseconds/request**; other latency entries are ms and TPS is output tokens/s. Five process blocks determine means. TTFT and completion are identical for gen1 by definition; both rows remain because the declared analysis retains them. Primary rows appear here as well as above with their unrounded signed lower bounds.

### All24 cell/path means

| Model | gen/c | Path | TTFT ms | Completion ms | Output TPS | Known CPU us/request | TPOT ms |
|---|---|---|---:|---:|---:|---:|---:|
| SmolLM2-135M | 1/1 | old host-stats | 1.177719287 | 1.177719287 | 842.399163013 | 44.690075000 | n/a |
| SmolLM2-135M | 1/1 | native epoll | 1.125205863 | 1.125205863 | 881.459504523 | 40.418350000 | n/a |
| SmolLM2-135M | 1/1 | candidate | 1.199574225 | 1.199574225 | 823.609585666 | 48.334768750 | n/a |
| SmolLM2-135M | 64/1 | old host-stats | 1.142349194 | 47.534428062 | 1345.494839961 | 1531.880706250 | 0.736382204 |
| SmolLM2-135M | 64/1 | native epoll | 1.138603400 | 46.128990544 | 1386.411810877 | 1269.347518750 | 0.714133129 |
| SmolLM2-135M | 64/1 | candidate | 1.146674463 | 47.779844606 | 1339.233309239 | 1556.387850000 | 0.740209050 |
| SmolLM2-135M | 1/8 | old host-stats | 2.095576106 | 2.095576106 | 3480.786645168 | 16.930762500 | n/a |
| SmolLM2-135M | 1/8 | native epoll | 2.177631619 | 2.177631619 | 3357.170093823 | 24.018500000 | n/a |
| SmolLM2-135M | 1/8 | candidate | 2.050389681 | 2.050389681 | 3555.963482869 | 17.617681250 | n/a |
| SmolLM2-135M | 64/8 | old host-stats | 1.960560338 | 95.439328613 | 5362.058559261 | 456.788793750 | 1.483789973 |
| SmolLM2-135M | 64/8 | native epoll | 1.821615138 | 91.085781388 | 5616.194252586 | 402.355400000 | 1.416891528 |
| SmolLM2-135M | 64/8 | candidate | 1.917993031 | 94.623744663 | 5408.676747165 | 449.240618750 | 1.471519867 |
| Qwen2.5-0.5B | 1/1 | old host-stats | 1.450528150 | 1.450528150 | 680.335401636 | 52.591706250 | n/a |
| Qwen2.5-0.5B | 1/1 | native epoll | 1.408872306 | 1.408872306 | 703.118834857 | 43.415400000 | n/a |
| Qwen2.5-0.5B | 1/1 | candidate | 1.432671750 | 1.432671750 | 689.764763877 | 49.850037500 | n/a |
| Qwen2.5-0.5B | 64/1 | old host-stats | 1.374621600 | 79.586490156 | 803.793399011 | 2571.396687500 | 1.241458231 |
| Qwen2.5-0.5B | 64/1 | native epoll | 1.361908513 | 78.511704025 | 814.884663002 | 2234.844056250 | 1.224599929 |
| Qwen2.5-0.5B | 64/1 | candidate | 1.396060006 | 79.844870187 | 801.284037175 | 2618.034512500 | 1.245219209 |
| Qwen2.5-0.5B | 1/8 | old host-stats | 2.472094644 | 2.472094644 | 2892.514184773 | 21.794056250 | n/a |
| Qwen2.5-0.5B | 1/8 | native epoll | 2.643541700 | 2.643541700 | 2849.462206726 | 21.867712500 | n/a |
| Qwen2.5-0.5B | 1/8 | candidate | 2.471685387 | 2.471685387 | 2960.528189725 | 21.317031250 | n/a |
| Qwen2.5-0.5B | 64/8 | old host-stats | 2.414627956 | 111.123680631 | 4601.192658397 | 530.024987500 | 1.725540519 |
| Qwen2.5-0.5B | 64/8 | native epoll | 2.379900937 | 107.537215850 | 4757.707057853 | 488.231712500 | 1.669163729 |
| Qwen2.5-0.5B | 64/8 | candidate | 2.350319350 | 110.560973875 | 4628.035685146 | 533.971850000 | 1.717629437 |

### All72 candidate-minus-comparator contrasts

Classification is directional only at nominal t95: throughput above0 supports this row; latency/CPU below0 supports it; the reverse is adverse; a zero-crossing interval is inconclusive. Secondary classifications do not override the primary. Paired vectors are linked in `full.analysis.json`; all72 vectors were recomputed and checked. Units match the preceding table.

| Model | gen/c | Comparator | Metric | Signed mean | Nominal t95 | Row judgment |
|---|---|---|---|---:|---|---|
| SmolLM2-135M | 1/1 | old host-stats | TTFT ms | +0.021854937 | [-0.041353288, +0.085063163] | inconclusive |
| SmolLM2-135M | 1/1 | old host-stats | completion ms | +0.021854937 | [-0.041353288, +0.085063163] | inconclusive |
| SmolLM2-135M | 1/1 | old host-stats | output TPS | -18.789577347 | [-67.719969784, +30.140815090] | inconclusive |
| SmolLM2-135M | 1/1 | old host-stats | known CPU us/request | +3.644693750 | [-0.989967197, +8.279354697] | inconclusive |
| SmolLM2-135M | 1/1 | native epoll | TTFT ms | +0.074368363 | [+0.037989612, +0.110747113] | adverse |
| SmolLM2-135M | 1/1 | native epoll | completion ms | +0.074368363 | [+0.037989612, +0.110747113] | adverse |
| SmolLM2-135M | 1/1 | native epoll | output TPS | -57.849918858 | [-83.342289673, -32.357548042] | adverse |
| SmolLM2-135M | 1/1 | native epoll | known CPU us/request | +7.916418750 | [+6.426380384, +9.406457116] | adverse |
| SmolLM2-135M | 64/1 | old host-stats | TTFT ms | +0.004325269 | [-0.038396233, +0.047046770] | inconclusive |
| SmolLM2-135M | 64/1 | old host-stats | completion ms | +0.245416544 | [-1.308008619, +1.798841706] | inconclusive |
| SmolLM2-135M | 64/1 | old host-stats | output TPS | -6.261530722 | [-48.531622484, +36.008561040] | inconclusive |
| SmolLM2-135M | 64/1 | old host-stats | known CPU us/request | +24.507143750 | [-94.453560481, +143.467847981] | inconclusive |
| SmolLM2-135M | 64/1 | old host-stats | TPOT ms | +0.003826846 | [-0.020261303, +0.027914994] | inconclusive |
| SmolLM2-135M | 64/1 | native epoll | TTFT ms | +0.008071062 | [-0.011546039, +0.027688164] | inconclusive |
| SmolLM2-135M | 64/1 | native epoll | completion ms | +1.650854062 | [+0.225619305, +3.076088820] | adverse |
| SmolLM2-135M | 64/1 | native epoll | output TPS | -47.178501638 | [-85.721073671, -8.635929605] | adverse |
| SmolLM2-135M | 64/1 | native epoll | known CPU us/request | +287.040331250 | [+220.389942173, +353.690720327] | adverse |
| SmolLM2-135M | 64/1 | native epoll | TPOT ms | +0.026075921 | [+0.003339186, +0.048812656] | adverse |
| SmolLM2-135M | 1/8 | old host-stats | TTFT ms | -0.045186425 | [-0.160768340, +0.070395490] | inconclusive |
| SmolLM2-135M | 1/8 | old host-stats | completion ms | -0.045186425 | [-0.160768340, +0.070395490] | inconclusive |
| SmolLM2-135M | 1/8 | old host-stats | output TPS | +75.176837701 | [-240.847413842, +391.201089244] | inconclusive |
| SmolLM2-135M | 1/8 | old host-stats | known CPU us/request | +0.686918750 | [-0.368948831, +1.742786331] | inconclusive |
| SmolLM2-135M | 1/8 | native epoll | TTFT ms | -0.127241937 | [-0.381901761, +0.127417886] | inconclusive |
| SmolLM2-135M | 1/8 | native epoll | completion ms | -0.127241937 | [-0.381901761, +0.127417886] | inconclusive |
| SmolLM2-135M | 1/8 | native epoll | output TPS | +198.793389047 | [-227.174223525, +624.761001618] | inconclusive |
| SmolLM2-135M | 1/8 | native epoll | known CPU us/request | -6.400818750 | [-8.590314625, -4.211322875] | supportive |
| SmolLM2-135M | 64/8 | old host-stats | TTFT ms | -0.042567306 | [-0.251840219, +0.166705607] | inconclusive |
| SmolLM2-135M | 64/8 | old host-stats | completion ms | -0.815583950 | [-1.586499618, -0.044668282] | supportive |
| SmolLM2-135M | 64/8 | old host-stats | output TPS | +46.618187904 | [-0.127399764, +93.363775571] | inconclusive |
| SmolLM2-135M | 64/8 | old host-stats | known CPU us/request | -7.548175000 | [-51.875193251, +36.778843251] | inconclusive |
| SmolLM2-135M | 64/8 | old host-stats | TPOT ms | -0.012270105 | [-0.021940897, -0.002599314] | supportive |
| SmolLM2-135M | 64/8 | native epoll | TTFT ms | +0.096377894 | [-0.049639473, +0.242395260] | inconclusive |
| SmolLM2-135M | 64/8 | native epoll | completion ms | +3.537963275 | [+3.033280916, +4.042645634] | adverse |
| SmolLM2-135M | 64/8 | native epoll | output TPS | -207.517505421 | [-233.892259036, -181.142751806] | adverse |
| SmolLM2-135M | 64/8 | native epoll | known CPU us/request | +46.885218750 | [-12.858369974, +106.628807474] | inconclusive |
| SmolLM2-135M | 64/8 | native epoll | TPOT ms | +0.054628339 | [+0.046631163, +0.062625516] | adverse |
| Qwen2.5-0.5B | 1/1 | old host-stats | TTFT ms | -0.017856400 | [-0.119235243, +0.083522443] | inconclusive |
| Qwen2.5-0.5B | 1/1 | old host-stats | completion ms | -0.017856400 | [-0.119235243, +0.083522443] | inconclusive |
| Qwen2.5-0.5B | 1/1 | old host-stats | output TPS | +9.429362241 | [-43.081067012, +61.939791493] | inconclusive |
| Qwen2.5-0.5B | 1/1 | old host-stats | known CPU us/request | -2.741668750 | [-10.603340664, +5.120003164] | inconclusive |
| Qwen2.5-0.5B | 1/1 | native epoll | TTFT ms | +0.023799444 | [-0.066379924, +0.113978812] | inconclusive |
| Qwen2.5-0.5B | 1/1 | native epoll | completion ms | +0.023799444 | [-0.066379924, +0.113978812] | inconclusive |
| Qwen2.5-0.5B | 1/1 | native epoll | output TPS | -13.354070980 | [-65.136639570, +38.428497610] | inconclusive |
| Qwen2.5-0.5B | 1/1 | native epoll | known CPU us/request | +6.434637500 | [-2.080095901, +14.949370901] | inconclusive |
| Qwen2.5-0.5B | 64/1 | old host-stats | TTFT ms | +0.021438406 | [-0.046585795, +0.089462607] | inconclusive |
| Qwen2.5-0.5B | 64/1 | old host-stats | completion ms | +0.258380031 | [-1.001221820, +1.517981883] | inconclusive |
| Qwen2.5-0.5B | 64/1 | old host-stats | output TPS | -2.509361836 | [-14.962143085, +9.943419412] | inconclusive |
| Qwen2.5-0.5B | 64/1 | old host-stats | known CPU us/request | +46.637825000 | [-89.596966157, +182.872616157] | inconclusive |
| Qwen2.5-0.5B | 64/1 | old host-stats | TPOT ms | +0.003760978 | [-0.015407437, +0.022929393] | inconclusive |
| Qwen2.5-0.5B | 64/1 | native epoll | TTFT ms | +0.034151494 | [+0.004286897, +0.064016091] | adverse |
| Qwen2.5-0.5B | 64/1 | native epoll | completion ms | +1.333166162 | [-0.555561922, +3.221894247] | inconclusive |
| Qwen2.5-0.5B | 64/1 | native epoll | output TPS | -13.600625827 | [-32.495991406, +5.294739753] | inconclusive |
| Qwen2.5-0.5B | 64/1 | native epoll | known CPU us/request | +383.190456250 | [+176.598957468, +589.781955032] | adverse |
| Qwen2.5-0.5B | 64/1 | native epoll | TPOT ms | +0.020619280 | [-0.009077169, +0.050315730] | inconclusive |
| Qwen2.5-0.5B | 1/8 | old host-stats | TTFT ms | -0.000409256 | [-0.102886838, +0.102068325] | inconclusive |
| Qwen2.5-0.5B | 1/8 | old host-stats | completion ms | -0.000409256 | [-0.102886838, +0.102068325] | inconclusive |
| Qwen2.5-0.5B | 1/8 | old host-stats | output TPS | +68.014004952 | [-364.399832627, +500.427842531] | inconclusive |
| Qwen2.5-0.5B | 1/8 | old host-stats | known CPU us/request | -0.477025000 | [-4.036869141, +3.082819141] | inconclusive |
| Qwen2.5-0.5B | 1/8 | native epoll | TTFT ms | -0.171856313 | [-0.238178394, -0.105534231] | supportive |
| Qwen2.5-0.5B | 1/8 | native epoll | completion ms | -0.171856313 | [-0.238178394, -0.105534231] | supportive |
| Qwen2.5-0.5B | 1/8 | native epoll | output TPS | +111.065982999 | [-145.603360948, +367.735326947] | inconclusive |
| Qwen2.5-0.5B | 1/8 | native epoll | known CPU us/request | -0.550681250 | [-8.185572271, +7.084209771] | inconclusive |
| Qwen2.5-0.5B | 64/8 | old host-stats | TTFT ms | -0.064308606 | [-0.268321206, +0.139703993] | inconclusive |
| Qwen2.5-0.5B | 64/8 | old host-stats | completion ms | -0.562706756 | [-1.285058890, +0.159645377] | inconclusive |
| Qwen2.5-0.5B | 64/8 | old host-stats | output TPS | +26.843026748 | [-4.781485089, +58.467538586] | inconclusive |
| Qwen2.5-0.5B | 64/8 | old host-stats | known CPU us/request | +3.946862500 | [-13.480813820, +21.374538820] | inconclusive |
| Qwen2.5-0.5B | 64/8 | old host-stats | TPOT ms | -0.007911082 | [-0.021646621, +0.005824458] | inconclusive |
| Qwen2.5-0.5B | 64/8 | native epoll | TTFT ms | -0.029581587 | [-0.134976715, +0.075813540] | inconclusive |
| Qwen2.5-0.5B | 64/8 | native epoll | completion ms | +3.023758025 | [-0.747384297, +6.794900347] | inconclusive |
| Qwen2.5-0.5B | 64/8 | native epoll | output TPS | -129.671372708 | [-295.373505738, +36.030760323] | inconclusive |
| Qwen2.5-0.5B | 64/8 | native epoll | known CPU us/request | +45.740137500 | [-0.129560899, +91.609835899] | inconclusive |
| Qwen2.5-0.5B | 64/8 | native epoll | TPOT ms | +0.048465708 | [-0.010589266, +0.107520682] | inconclusive |

### Primary paired vectors, blocks0..4

| Model | Comparator | Candidate-minus TPS vector |
|---|---|---|
| SmolLM2-135M | old host-stats | +95.306616467, +63.433729765, +56.931465623, +4.494679160, +12.924448504 |
| SmolLM2-135M | native epoll | -196.212177766, -185.061848023, -197.615791802, -221.555537042, -237.142172473 |
| Qwen2.5-0.5B | old host-stats | +50.135936462, -13.263887950, +41.638054141, +17.299828677, +38.405202412 |
| Qwen2.5-0.5B | native epoll | +108.535736972, -180.129727454, -202.748158836, -182.904162693, -191.110551528 |

### All30 short and30 long ordinary model-round counters

Each vector contains the five rows for blocks0..4, so the six paths below account for all30 rows per context. These are successfully launched nonempty model rounds after the authenticated deductions, not isolated GPU elapsed time.

| Model | Path | Short gen1/c8 rounds after -8 | Mean | Long gen64/c8 rounds after -2088 | Mean |
|---|---|---|---:|---|---:|
| SmolLM2-135M | old host-stats | [6, 5, 5, 5, 5] | 5.200 | [261, 259, 259, 259, 260] | 259.600 |
| SmolLM2-135M | native epoll | [8, 8, 9, 8, 8] | 8.200 | [263, 261, 261, 260, 263] | 261.600 |
| SmolLM2-135M | candidate | [5, 6, 5, 5, 5] | 5.200 | [260, 259, 259, 260, 261] | 259.800 |
| Qwen2.5-0.5B | old host-stats | [6, 5, 6, 5, 5] | 5.400 | [260, 259, 259, 259, 260] | 259.400 |
| Qwen2.5-0.5B | native epoll | [8, 8, 8, 8, 8] | 8.000 | [260, 261, 260, 260, 260] | 260.200 |
| Qwen2.5-0.5B | candidate | [5, 6, 5, 6, 5] | 5.400 | [259, 262, 260, 260, 259] | 260.000 |

### All eight round contrasts

| Context | Model | Comparator | Paired differences | Mean | Nominal t95 |
|---|---|---|---|---:|---|
| short | SmolLM2-135M | old host-stats | [-1, 1, 0, 0, 0] | +0.000 | [-0.877989033, +0.877989033] |
| short | SmolLM2-135M | native epoll | [-3, -2, -4, -3, -3] | -3.000 | [-3.877989033, -2.122010967] |
| short | Qwen2.5-0.5B | old host-stats | [-1, 1, -1, 1, 0] | +0.000 | [-1.241663998, +1.241663998] |
| short | Qwen2.5-0.5B | native epoll | [-3, -2, -3, -2, -3] | -2.600 | [-3.280087381, -1.919912619] |
| long | SmolLM2-135M | old host-stats | [-1, 0, 0, 1, 1] | +0.200 | [-0.838850634, +1.238850634] |
| long | SmolLM2-135M | native epoll | [-3, -2, -2, 0, -2] | -1.800 | [-3.160174761, -0.439825239] |
| long | Qwen2.5-0.5B | old host-stats | [-1, 3, 1, 1, -1] | +0.600 | [-1.477701267, +2.677701267] |
| long | Qwen2.5-0.5B | native epoll | [-1, 1, 0, 0, -1] | -0.200 | [-1.238850634, +0.838850634] |

### Whole-transfer multishot CQ descriptions, every coalesced row

Native has no io_uring CQ/SQ counterpart. These20 rows cover both coalesced paths/five blocks/two models; the30-row long-counter analysis also retains the10 native model-round/TPS rows.

| Model | Block | Path | SQ | CQ | CQ-SQ | Excess fraction |
|---|---:|---|---:|---:|---:|---:|
| Qwen2.5-0.5B | 0 | old host-stats | 4268 | 53201 | 48933 | 0.919775944 |
| Qwen2.5-0.5B | 0 | candidate | 4277 | 50855 | 46578 | 0.915898142 |
| Qwen2.5-0.5B | 1 | old host-stats | 4278 | 54559 | 50281 | 0.921589472 |
| Qwen2.5-0.5B | 1 | candidate | 4278 | 55876 | 51598 | 0.923437612 |
| Qwen2.5-0.5B | 2 | old host-stats | 4277 | 54442 | 50165 | 0.921439330 |
| Qwen2.5-0.5B | 2 | candidate | 4277 | 53640 | 49363 | 0.920264728 |
| Qwen2.5-0.5B | 3 | candidate | 4275 | 53512 | 49237 | 0.920111377 |
| Qwen2.5-0.5B | 3 | old host-stats | 4276 | 54126 | 49850 | 0.920999150 |
| Qwen2.5-0.5B | 4 | candidate | 4278 | 51766 | 47488 | 0.917358884 |
| Qwen2.5-0.5B | 4 | old host-stats | 4276 | 51721 | 47445 | 0.917325651 |
| SmolLM2-135M | 0 | old host-stats | 4241 | 35429 | 31188 | 0.880295803 |
| SmolLM2-135M | 0 | candidate | 4274 | 35446 | 31172 | 0.879422220 |
| SmolLM2-135M | 1 | old host-stats | 4261 | 35420 | 31159 | 0.879700734 |
| SmolLM2-135M | 1 | candidate | 4268 | 38003 | 33735 | 0.887693077 |
| SmolLM2-135M | 2 | old host-stats | 4266 | 36785 | 32519 | 0.884028816 |
| SmolLM2-135M | 2 | candidate | 4267 | 36030 | 31763 | 0.881570913 |
| SmolLM2-135M | 3 | candidate | 4274 | 35880 | 31606 | 0.880880713 |
| SmolLM2-135M | 3 | old host-stats | 4274 | 36710 | 32436 | 0.883573958 |
| SmolLM2-135M | 4 | candidate | 4277 | 35789 | 31512 | 0.880494007 |
| SmolLM2-135M | 4 | old host-stats | 4267 | 35819 | 31552 | 0.880873280 |

## Evidence locations and references

The complete reproducibility path remains ordinary files: `plan.md`, `plan-review.md`, `run.py`, `full.commands.json`, `full.exit.json`, all `full_{short,transfer}_{smol,qwen}_b{0..4}.jsonl` and corresponding exits/driver logs/executor stdout; `analysis.py`, `full.analysis.json/stdout/exit`, `long_counter_analysis.py` and its stdout/exit; `qualification.py`, both qualification driver/GPU/network/reference files and `qualification.analysis.stdout/exit`; both lifecycle raw trees, `lifecycle.py`, `analysis_lifecycle.py` and analysis stdout/exit. Source/build/oracle/environment paths are `candidate.diff`, `candidate_io_uring_tcp.h`, `original_io_uring_tcp.h`, `source_snapshot/`, `source_frozen.json`, `post_run_source.json`, `original_rebuild.*`, `candidate_step_*`, `setup.*`, `environment.json`, `packages.json`, frozen references and host snapshots. The actual source is `/workspaces/repository/executor/io_uring_tcp.h`.

Live official [CUDA zero-copy guidance](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html#zero-copy) motivates caching repeated mapped-memory accesses in device memory; it does not establish this workload's bottleneck or gain. Official [vLLM benchmark metric definitions](https://docs.vllm.ai/en/stable/benchmarking/cli/#understanding-the-latency-metrics) support client TTFT and per-request TPOT excluding the first token. This experiment uses its explicitly retained source-native finite output-token throughput boundary and binary token-arrival observations; it did not execute the official vLLM OpenAI benchmark or measure GPU kernel latency.

## Reviewer scope and handle release

I wrote only this complete ordinary Markdown report under the original Workspace TEMP. I did not modify the plan, production source, raw outputs or existing analysis; run GPU serving/builds/installs; clean resources; change runtime/configuration/permissions; create any entity/branch/clone/worktree/scheduler; publish; or interrupt original sessions. `tools/setup_env.sh`, default qwen_graph.so and all four unowned loop_trace artifacts match their retained inode/size/mtime/symlink observations. Coder PIDs1/10909 remain present. The report supplies advice without authorizing mutations.

All read/CPU-recomputation/cuobjdump subprocesses used by this review have returned; all opened files are closed on return. I retain **no active subprocess, GPU/session resource or file handle** in this evidence root or build directory. The owning agent may continue its authorized source-selection/archival workflow. This is the final result review, not an interim placeholder or pending appendix.
