# Fresh combined result review: chained device-graph dispatch

Observed 2026-10-13 UTC in the original /workspaces/repository Workspace on main33337adffd0975e7542c359a966cb4a759695742. This is the single fresh result review of the completed experiment. Read the plan and fresh plan-review, all145 archived files, current source plus the fdcd111→33337ad implementation diff, and independently reconstructed raw outputs, trace ownership, frozen-reference provenance and all numerical summaries. Reviewer did not serve a model, mutate source/default/runtime or change the plan/oracle. Only this report is written.

## Separate judgments

- Run status: valid and complete for the declared local matched matrix, exact traced setup and pre-observation finite complete-output-set qualification. Final removal of owned temporary runtime/build output is still pending root closure.
- Tested hypothesis: inconclusive. All eight declared primaries cross zero; none supports or contradicts a scoped performance effect at the stated nominal interval. This is neither equivalence nor proof of no effect.
- Research value: supporting. A new correct mechanism A/B bounds a previously untested orchestration candidate; setup/build/provenance checks alone are dependency evidence.
- Paper impact: implementation/workload boundary. It does not challenge a necessary novelty thesis or prove an eBPF advantage.
- Next paper decision: retain the ordinary separate dispatcher default; publish the full inconclusive result and close adoption of this candidate on these measurements. Do not present halved successful launch calls as measured latency/throughput improvement. A separate service-attributed CPU/interference comparison can address the unresolved CPU-path value; an unchanged repeat of this matrix has no newly identified causal discriminator.

## Completion, commands and source identity

Runtime construction uses official python3 -m venv --without-pip and python3 -m pip --python VENV/bin/python with vLLM0.31.0, Torch2.13.0+cu129 and Transformers5.17.0. Both install statuses and the build are0. Exact commands/environment and package inventory remain in tail_chain_20261012/. CUDA13 NVCC links the pinned Torch CUDA12 runtime through the existing qualified route; there is no arithmetic compatibility patch. Eight binaries are freshly built: separate/chained x kernel/native x traced/untraced. BF_PAD_PREFILL and BF_PREFIX_RELEASE are shared; only the chained four have BF_CHAINED_DISPATCH, native controls add BF_USER_NETWORK/BF_USER_NETWORK_WAIT, and tracing is shared only during setup.

Every one of the145 top-level durable files was read and matched byte-for-byte to its retained temporary counterpart at review. JSON/JSONL parse, all15 runtime/build/driver/analysis status receipts are0, all six benchmark raw terminals are0 and every executor is terminal successful. All six analyses were independently rerun with base python3 and stdout was byte-identical to the archived stdout. Separate raw reconstruction below does not rely on those success markers.

All seven sources in sources.json match current files exactly. Each raw metadata embeds driver/client/backend/native bytes matching those snapshots. The before snapshots and Git diff show source growth restricted to Makefile5 additions/2 removals, driver8/3, analyzer9/0, native29/15; backend model/head/greedy sampling and userspace transport source are unchanged. No BPF/module/wire/precision/checkpoint/KV policy change was introduced. The common bootstrap allocation ordering and counters affect both A/B sides. Candidate build names and --dispatch-comparison are opt-in; ordinary default stays separate.

The qualification commit33337ad was made00:30:03UTC. Qwen full metadata was emitted00:29:51 on fdcd111, but the first measured request was00:30:11, after that commit. Smol metadata records33337ad. This is publication of already captured/used identical source, not source drift: snapshots and all four embedded source fields are exact. Keep both metadata revisions instead of rewriting them. Frozen source_commit likewise legitimately records fdcd111 with the actual uncommitted candidate source in sources.json.

| Stage | Metadata UTC | Terminal UTC | Requests | Tokens |
|---|---|---|---:|---:|
| traced_preflight | 2026-10-13T00:17:20Z | 2026-10-13T00:21:17Z | 160 | 4192 |
| qwen_correctness | 2026-10-13T00:21:21Z | 2026-10-13T00:24:50Z | 2488 | 88896 |
| smol_correctness | 2026-10-13T00:24:54Z | 2026-10-13T00:28:03Z | 2488 | 88896 |
| untraced_preflight | 2026-10-13T00:28:08Z | 2026-10-13T00:29:46Z | 160 | 4192 |
| qwen_performance | 2026-10-13T00:29:51Z | 2026-10-13T00:39:48Z | 5280 | 166560 |
| smol_performance | 2026-10-13T00:39:53Z | 2026-10-13T00:48:46Z | 5280 | 166560 |

Strict totals are4976 requests/177792 valid output tokens,2072 deliberate rejections and40000 empty connections across eight executors. Each has622 requests/22224 valid tokens/259 rejects/5000 empty connects and helper-thread SIGTERM evidence. Fragmented requests, prompt/block edges, all concurrency levels1..8, wrap/reuse, mixed output lengths, pipelines/half-close and subsequent validity after rejection are actual declared cases, not merely generated fixtures. This is bounded protocol coverage, not universal TCP/HTTP correctness.

Both preflights each have four executors,160 requests and4192 tokens. Each full model has20 executors/80 measured cells/5120 measured requests/166400 measured tokens plus160 checked gen1 warmups. Combined full timing has40 executors/160 cells/10240 measured requests/332800 tokens plus320 warmups; actual checked total10560 requests/333120 tokens. No performance failures, discarded cells, exclusions or retries were found. All rows/outliers remain. Pipeline commands record all intended stages to the last Smol analysis; no partial prefix is treated as complete.

## Fidelity, trace/cache ownership and frozen-pool provenance

In all12 traced qualification executors (eight strict plus four traced preflight), independently joined actual replies to references by unique client_ns. Prompt/gen/bad flag and complete token sequences agree exactly. Reconstructed every admission/compute/release event: each id owns id%8 without overlapping ownership; compute touches a live non-released owner; packed prefill query equals the selected maximum prompt; prefill starts an empty history; decode follows nonempty unfinished history; every traced output token accumulates into the matching complete reference; releases are consecutive FIFO prefixes and happen only after all expected tokens; final owner maps are empty. Trace terminals have zero overflow and accurate record counts. Native model_steps equal independent compute-event counts. Every replay log reports the exact request/token counts with exit0.

The unchanged host replay independently reconstructs positions, sequence lengths, row metadata, pages/block tables, padding and cache slots from the observed admission/compute order and reference history. It executes upstream body/head graphs, compares computed outputs to trace, and then advances history from its own computed output. It does not inject served tokens as future reference inputs. KV pages map persistent physical slot ownership; new prefill rewrites the relevant live prefix. Numerical GPU replay was executed by the original qualification processes; this reviewer audited their source/raw/logs and reconstructed ownership/client equality, and did not launch a second model replay.

Freeze timestamp00:28:04.805780UTC precedes untraced preflight metadata00:28:08 and both timing matrices. Independently loaded every contributing previous/current reference file and rebuilt the whole-sequence union, rather than accepting the frozen file because the method produced it. The resulting set equals frozen_references.json exactly. No untraced observation contributes. Checkpoint path/vocab and explicit FP16 precision match.

| Model | Prior qualified files / valid / rejects | Current qualified files / valid / rejects | Prompt-gen keys | Distinct complete sequences |
|---|---|---|---:|---:|
| qwen | 24 / 6732 / 1036 | 8 / 1612 / 1036 | 17 | 22 |
| smol | 24 / 6732 / 1036 | 4 / 1452 / 1036 | 17 | 19 |

Qwen current sources are four strict plus four traced-preflight files; Smol current sources are four strict files. Earlier sources are24 per model from the independently qualified finding0034 collection. Intentional rejects are omitted from valid sequence pools. Current qualification adds samples but no new distinct sequence to the previous22/19 sets. Embedded pools in each untraced raw equal the frozen asset.

Every actual untraced valid reply, including all preflight and warmup replies, has exact requested length and matches one WHOLE frozen sequence for its exact prompt/gen. No tokenwise union, prefix-only gen64, served-history forcing, changed tolerance or post-observation pool extension is used. This proves finite previously qualified complete-output-set membership, not replay of this unobserved timing batch/cache/ownership trajectory. A wrong implementation returning a previously valid alternative could pass. Production scheduling changed, so retain this material limit alongside the stronger current traced qualification. Neither universal numerical correctness, batch invariance nor task quality is established. Per-cell graph/batch/prefill/decode/padding observations stay null in untraced analyses.

Concurrent transport outputs actually differ even with identical arithmetic. Independently recomputed diagnostics below pair same process block/prompt index between kernel/native within each policy; these are output-agreement diagnostics, not identical trajectory claims.

| Model | Policy | gen1/c1 | gen64/c1 | gen1/c8 | gen64/c8 complete / first-token |
|---|---|---:|---:|---:|---|
| qwen | chained | 320/320 | 320/320 | 288/320 | 284/320 / 284/320 |
| qwen | separate | 320/320 | 320/320 | 296/320 | 289/320 / 289/320 |
| smol | chained | 320/320 | 320/320 | 320/320 | 293/320 / 320/320 |
| smol | separate | 320/320 | 320/320 | 320/320 | 288/320 / 320/320 |

## Mechanism engagement and lifecycle

Source candidate appends the existing dispatcher after the body/head dependency and tail-launches the next combined graph. Queue/device/control/input pointers are allocated before instantiation; upload and initial synchronization precede host submission. Each dispatcher enqueues at most one tail step, including legal self-tail relaunch. The separate alternative fire-and-forgets unchanged model/head and independently tail-launches its dispatcher. Counters increment after successful launch calls. All traced steps independently agree with2 successful calls/step in separate and1/step in chained. Untraced counters retain the same aggregate ratio with graph_error0 and trace_overflows0; aggregate self-reported counts are not substitute per-cell trace evidence.

Model/head completion precedes dispatcher reading all batch outputs. Per-token publication uses system fence before produced, and FIFO DONE uses system fence after output consumption. TX retains each slot reservation until its final slot access. Shutdown synchronizes graph execution before releasing graph/control/shared allocations. No model arithmetic or steady host scheduler is inserted. Decreasing calls also changes graph environment/dependencies; any performance effect would belong to the complete scheduling change, not be uniquely attributable to one removed launch instruction.

After-ready strict strace traces all threads. Counts reconstructed directly from the retained network text:

| Model | Condition | accept4 | recvfrom | sendmsg |
|---|---|---:|---:|---:|
| qwen | chained-kernel | 0 | 0 | 0 |
| qwen | chained-userspace | 5155 | 12832 | 22421 |
| qwen | separate-kernel | 0 | 0 | 0 |
| qwen | separate-userspace | 5149 | 12842 | 22407 |
| smol | chained-kernel | 0 | 0 | 0 |
| smol | chained-userspace | 5152 | 12844 | 22386 |
| smol | separate-kernel | 0 | 0 | 0 |
| smol | separate-userspace | 5156 | 12841 | 22407 |

Kernel conditions contain none of the searched accept/receive/send network calls; efficient native controls actually engage all intended calls. This supports absence of a steady userspace request worker in the qualified kernel path, not host-CPU-free networking or measured CPU reduction. All native controls have published=completed=actual requests and expected rejected counts. Every kernel stats receipt has exact llm_head, reserved0 and all eight FREE states; attach/detach are0, and all native processes exit0. Reserved/FREE reflects local TX copy/send/recycle completion, not remote TCP acknowledgement. Actual complete client bytes provide the end-to-end reply evidence.

Endpoint owner_receipt at00:52:07UTC reports unchanged boot04dc0087-5ccc-4c46-9997-b9a92f0e5167/kernel7.3rc3, empty GPU compute-app list, unloaded module, no BPF pins, original Coder PIDs1/10909 and base Torch2.14.1+cu130/Transformers5.19.0. Workspace receipt reports original UID3e8994f8-77ba-4a73-a3a5-35ed69a0a8a2 Running/Ready/zero restarts on lab, with node Ready. Unrelated tools/setup_env.sh is preserved. At this review the temporary runtime and build products are STILL present; root must archive and remove its owned artifacts and record restoration separately. This report makes no premature cleanup/publication claim.

## Host exposure and comparison fairness

host_journal.json preserves00:16:00–00:52:08UTC, not an isolation certificate. Direct journal evidence includes NVRM allocation failures00:17:29 and a host global OOM00:19:11 killing unrelated Lean/Coder/Python groups, plus other-device filesystem/storage faults. First separate-Qwen traced-preflight bootstrap is00:17:20→ready00:19:52, so this substantial setup disruption overlaps bootstrap. Subsequent setup processes have much shorter capture startup; do not hide the exposure.

Finding0036 documents a transient NotReady and failed Tailscale/campus SSH with existing Cloudflare SSH retained. Neither archived kernel journal nor setup_fault_window text directly contains the Kubernetes NotReady event; distinguish that documented operator observation from the directly archived OOM and current Ready receipt. Same boot/Pod UID and terminal pipeline show this experiment survived; they do not prove clean runtime resource exposure. The full measured matrix starts00:30:11, well after the recorded OOM, but unequal temporal contention remains unknown. All endpoint evidence and rotating process order limit drift; neither proves host/GPU isolation. No automatic exclusion or superior-baseline claim follows from the fault.

The source-local separate scheduler is the fair main competing implementation for this hypothesis: same pinned model, compute/head, FP16, catalogue, client/wire/KV limits, packed prefill/prefix release and native60us epoll wait. Kernel/native are transport strata and controls, not extra external SOTA baselines. Both arithmetic work budgets and four prompt/token lengths are matched; concurrent trajectories and output alternatives are not identical. No baseline interface failures or avoidable weak-proxy failures were found. A CUDA graph control A/B does not answer the full eBPF novelty or stock host-serving efficiency question.

## Metrics and all eight declared primaries

Recomputed every raw arrival timestamp and each of160 cells: TTFT=(first token arrival−start)/1e6; completion=(last arrival−start)/1e6; TPOT=(last−first)/(gen−1)/1e6 for gen>1; throughput=64*gen divided by cell earliest send to latest delivery. Arrival order/lengths, index0..63, fixed prompt index%4, complete-cell timestamps/request/token counts all pass. Warmups are excluded from timing. All32 model/mode/cell summaries, nearest-rank pooled p50/p99 and the five per-cell process throughputs match archived analysis.

Each paired unit is one of five process blocks. Recomputed differences independently from requests and cell timestamps; positive favors chained (separate-minus-chained for latency, chained-minus-separate for throughput). Nominal two-sided t95=df4 uses2.776445105*sample_sd/sqrt(5). These are exploratory five-block intervals, not familywise-adjusted claims.320 request samples per condition do not become320 independent process repetitions.

| Model | Transport | Primary | Separate | Chained | Gain | Nominal95% interval |
|---|---|---|---:|---:|---:|---|
| qwen | kernel | ttft_ms gen1/c1 | 1.475002841 | 1.437113094 | 0.037889747 | [-0.011647432, 0.087426926] |
| qwen | userspace | ttft_ms gen1/c1 | 1.432011725 | 1.400746937 | 0.031264787 | [-0.038345491, 0.100875066] |
| qwen | kernel | tokens_per_s gen64/c8 | 4747.698381063 | 4647.218259002 | -100.480122061 | [-268.954763666, 67.994519544] |
| qwen | userspace | tokens_per_s gen64/c8 | 4689.774038575 | 4748.051888156 | 58.277849581 | [-78.796811914, 195.352511076] |
| smol | kernel | ttft_ms gen1/c1 | 1.153345241 | 1.171663813 | -0.018318572 | [-0.117197081, 0.080559937] |
| smol | userspace | ttft_ms gen1/c1 | 1.195710025 | 1.192011378 | 0.003698647 | [-0.089044573, 0.096441867] |
| smol | kernel | tokens_per_s gen64/c8 | 5495.636932429 | 5410.104201605 | -85.532730824 | [-533.342583055, 362.277121407] |
| smol | userspace | tokens_per_s gen64/c8 | 5580.360945957 | 5578.130518982 | -2.230426975 | [-23.766157327, 19.305303376] |

All eight cross zero, including mean regressions in four primary throughput/latency rows. None is supported or statistically contradicted under the predeclared rule. No model/transport-wide improvement, equivalence or zero-effect claim follows. Five block-level primary differences, in collection block order:

- qwen chained-kernel ttft_ms gen1/c1: 0.099745578, 0.034849937, -0.008497797, 0.019381656, 0.043969359.
- qwen chained-userspace ttft_ms gen1/c1: 0.049493281, 0.098891672, -0.020672234, -0.032563766, 0.061174984.
- qwen chained-kernel tokens_per_s gen64/c8: 17.552455008, -1.636170235, -260.153864073, -22.292922413, -235.870108591.
- qwen chained-userspace tokens_per_s gen64/c8: 6.988231182, 254.761406917, 16.024469417, 21.451879838, -7.836739449.
- smol chained-kernel ttft_ms gen1/c1: 0.116930844, -0.023197219, -0.053375422, -0.040690625, -0.091260437.
- smol chained-userspace ttft_ms gen1/c1: 0.087543672, -0.100344094, 0.059266641, -0.033322719, 0.005349734.
- smol chained-kernel tokens_per_s gen64/c8: -25.295045258, -437.452708239, -407.982088454, -2.357148580, 445.423336411.
- smol chained-userspace tokens_per_s gen64/c8: 19.480444630, -22.166655590, -14.461025688, 11.066806585, -5.071704815.

## Complete client summaries

All values are the independent request/cell reconstruction; TTFT/completion/TPOT in ms, throughput in output token/s. Each row has320 measured requests across five blocks. p50/p99 are pooled nearest-rank request quantiles; no interval is manufactured for them.

| Model | Condition | gen/c | TTFT mean | p50 | p99 | Completion | TPOT | Throughput |
|---|---|---|---:|---:|---:|---:|---:|---:|
| qwen | separate-kernel | 1/1 | 1.475003 | 1.471973 | 1.612765 | 1.475003 | — | 667.112821 |
| qwen | chained-kernel | 1/1 | 1.437113 | 1.422995 | 1.592703 | 1.437113 | — | 688.029108 |
| qwen | separate-userspace | 1/1 | 1.432012 | 1.441447 | 1.618954 | 1.432012 | — | 690.062353 |
| qwen | chained-userspace | 1/1 | 1.400747 | 1.369726 | 1.679573 | 1.400747 | — | 708.783897 |
| qwen | separate-kernel | 64/1 | 1.351640 | 1.325725 | 1.702970 | 78.107216 | 1.218342 | 818.999293 |
| qwen | chained-kernel | 64/1 | 1.382177 | 1.376555 | 1.603300 | 78.910620 | 1.230610 | 810.807812 |
| qwen | separate-userspace | 64/1 | 1.352611 | 1.355464 | 1.591030 | 78.549474 | 1.225347 | 814.477709 |
| qwen | chained-userspace | 64/1 | 1.324117 | 1.313704 | 1.503222 | 78.027414 | 1.217513 | 819.830905 |
| qwen | separate-kernel | 1/8 | 2.485740 | 2.503377 | 3.384380 | 2.485740 | — | 3087.947949 |
| qwen | chained-kernel | 1/8 | 2.556396 | 2.584705 | 3.059954 | 2.556396 | — | 3012.742454 |
| qwen | separate-userspace | 1/8 | 2.505389 | 2.536713 | 3.184197 | 2.505389 | — | 3044.356091 |
| qwen | chained-userspace | 1/8 | 2.462368 | 2.496069 | 3.044574 | 2.462368 | — | 3099.147464 |
| qwen | separate-kernel | 64/8 | 2.177577 | 2.333785 | 2.907608 | 107.740302 | 1.675599 | 4747.698381 |
| qwen | chained-kernel | 64/8 | 2.280674 | 2.449623 | 3.264742 | 110.127085 | 1.711848 | 4647.218259 |
| qwen | separate-userspace | 64/8 | 2.171690 | 2.280200 | 3.013899 | 109.100618 | 1.697285 | 4689.774039 |
| qwen | chained-userspace | 64/8 | 2.147084 | 2.247115 | 2.965888 | 107.714126 | 1.675667 | 4748.051888 |
| smol | separate-kernel | 1/1 | 1.153345 | 1.121535 | 1.420800 | 1.153345 | — | 859.596453 |
| smol | chained-kernel | 1/1 | 1.171664 | 1.170792 | 1.441057 | 1.171664 | — | 844.965172 |
| smol | separate-userspace | 1/1 | 1.195710 | 1.191339 | 1.480205 | 1.195710 | — | 827.547606 |
| smol | chained-userspace | 1/1 | 1.192011 | 1.169024 | 1.641570 | 1.192011 | — | 830.979630 |
| smol | separate-kernel | 64/1 | 1.137481 | 1.126936 | 1.468143 | 46.443271 | 0.719140 | 1377.869240 |
| smol | chained-kernel | 64/1 | 1.157284 | 1.154604 | 1.401417 | 46.979679 | 0.727340 | 1362.511672 |
| smol | separate-userspace | 64/1 | 1.126526 | 1.120088 | 1.402986 | 45.962456 | 0.711681 | 1391.528220 |
| smol | chained-userspace | 64/1 | 1.110956 | 1.109403 | 1.289590 | 45.941565 | 0.711597 | 1392.122294 |
| smol | separate-kernel | 1/8 | 1.968592 | 1.959485 | 2.752232 | 1.968592 | — | 3898.961943 |
| smol | chained-kernel | 1/8 | 1.998398 | 2.033825 | 2.793912 | 1.998398 | — | 3818.684969 |
| smol | separate-userspace | 1/8 | 1.865177 | 1.887328 | 2.358283 | 1.865177 | — | 4098.962669 |
| smol | chained-userspace | 1/8 | 1.897960 | 1.896438 | 2.487520 | 1.897960 | — | 4016.110927 |
| smol | separate-kernel | 64/8 | 1.786518 | 1.850277 | 2.610051 | 93.168342 | 1.450505 | 5495.636932 |
| smol | chained-kernel | 64/8 | 1.796604 | 1.851865 | 2.714363 | 94.659646 | 1.474017 | 5410.104202 |
| smol | separate-userspace | 64/8 | 1.722794 | 1.817773 | 2.497163 | 91.614852 | 1.426858 | 5580.360946 |
| smol | chained-userspace | 64/8 | 1.690106 | 1.758566 | 2.406663 | 91.684882 | 1.428489 | 5578.130519 |

## All secondary and transport-control effects

All84 paired effects, including the eight primaries, were independently recomputed. EVERY interval crosses zero. The76 remaining secondary/control effects are retained below, rather than cherry-picking a tail/long-output row. Positive gain favors the named candidate. Chained kernel versus native is a mechanism control and remains inconclusive; it is not evidence of eBPF superiority. The complete original arrays for each row remain in the linked model analysis outputs.

| Model | Baseline → candidate | gen/c | Metric | Gain | Nominal95% interval |
|---|---|---|---|---:|---|
| qwen | separate-kernel → chained-kernel | 1/1 | completion_ms | 0.037889747 | [-0.011647432, 0.087426926] |
| qwen | separate-kernel → chained-kernel | 1/1 | tokens_per_s | 20.916286913 | [-6.227415958, 48.059989784] |
| qwen | separate-userspace → chained-userspace | 1/1 | completion_ms | 0.031264787 | [-0.038345491, 0.100875066] |
| qwen | separate-userspace → chained-userspace | 1/1 | tokens_per_s | 18.721544616 | [-17.745136098, 55.188225330] |
| qwen | chained-userspace → chained-kernel | 1/1 | ttft_ms | -0.036366156 | [-0.093286124, 0.020553811] |
| qwen | chained-userspace → chained-kernel | 1/1 | completion_ms | -0.036366156 | [-0.093286124, 0.020553811] |
| qwen | chained-userspace → chained-kernel | 1/1 | tokens_per_s | -20.754789760 | [-52.654655247, 11.145075727] |
| qwen | separate-kernel → chained-kernel | 64/1 | ttft_ms | -0.030536231 | [-0.093083461, 0.032010999] |
| qwen | separate-kernel → chained-kernel | 64/1 | completion_ms | -0.803404013 | [-2.286869648, 0.680061623] |
| qwen | separate-kernel → chained-kernel | 64/1 | tokens_per_s | -8.191480772 | [-23.326569894, 6.943608350] |
| qwen | separate-kernel → chained-kernel | 64/1 | tpot_ms | -0.012267743 | [-0.034845671, 0.010310186] |
| qwen | separate-userspace → chained-userspace | 64/1 | ttft_ms | 0.028494784 | [-0.027753236, 0.084742804] |
| qwen | separate-userspace → chained-userspace | 64/1 | completion_ms | 0.522060609 | [-0.700543227, 1.744664446] |
| qwen | separate-userspace → chained-userspace | 64/1 | tokens_per_s | 5.353195529 | [-7.131624042, 17.838015100] |
| qwen | separate-userspace → chained-userspace | 64/1 | tpot_ms | 0.007834378 | [-0.010691137, 0.026359893] |
| qwen | chained-userspace → chained-kernel | 64/1 | ttft_ms | -0.058060081 | [-0.127493824, 0.011373662] |
| qwen | chained-userspace → chained-kernel | 64/1 | completion_ms | -0.883206647 | [-2.376880283, 0.610466989] |
| qwen | chained-userspace → chained-kernel | 64/1 | tokens_per_s | -9.023092286 | [-24.280162934, 6.233978362] |
| qwen | chained-userspace → chained-kernel | 64/1 | tpot_ms | -0.013097565 | [-0.035713543, 0.009518414] |
| qwen | separate-kernel → chained-kernel | 1/8 | ttft_ms | -0.070656125 | [-0.164063623, 0.022751373] |
| qwen | separate-kernel → chained-kernel | 1/8 | completion_ms | -0.070656125 | [-0.164063623, 0.022751373] |
| qwen | separate-kernel → chained-kernel | 1/8 | tokens_per_s | -75.205495009 | [-181.029544913, 30.618554895] |
| qwen | separate-userspace → chained-userspace | 1/8 | ttft_ms | 0.043021250 | [-0.004861646, 0.090904146] |
| qwen | separate-userspace → chained-userspace | 1/8 | completion_ms | 0.043021250 | [-0.004861646, 0.090904146] |
| qwen | separate-userspace → chained-userspace | 1/8 | tokens_per_s | 54.791372923 | [-30.671981493, 140.254727340] |
| qwen | chained-userspace → chained-kernel | 1/8 | ttft_ms | -0.094028375 | [-0.211352112, 0.023295362] |
| qwen | chained-userspace → chained-kernel | 1/8 | completion_ms | -0.094028375 | [-0.211352112, 0.023295362] |
| qwen | chained-userspace → chained-kernel | 1/8 | tokens_per_s | -86.405009353 | [-244.964855608, 72.154836902] |
| qwen | separate-kernel → chained-kernel | 64/8 | ttft_ms | -0.103097747 | [-0.253921998, 0.047726504] |
| qwen | separate-kernel → chained-kernel | 64/8 | completion_ms | -2.386782638 | [-6.393250847, 1.619685572] |
| qwen | separate-kernel → chained-kernel | 64/8 | tpot_ms | -0.036248967 | [-0.097972316, 0.025474383] |
| qwen | separate-userspace → chained-userspace | 64/8 | ttft_ms | 0.024606716 | [-0.104800321, 0.154013753] |
| qwen | separate-userspace → chained-userspace | 64/8 | completion_ms | 1.386492050 | [-1.841084586, 4.614068686] |
| qwen | separate-userspace → chained-userspace | 64/8 | tpot_ms | 0.021617228 | [-0.028418504, 0.071652959] |
| qwen | chained-userspace → chained-kernel | 64/8 | ttft_ms | -0.133590753 | [-0.276934185, 0.009752679] |
| qwen | chained-userspace → chained-kernel | 64/8 | completion_ms | -2.412958425 | [-6.340422097, 1.514505247] |
| qwen | chained-userspace → chained-kernel | 64/8 | tokens_per_s | -100.833629154 | [-264.325034262, 62.657775953] |
| qwen | chained-userspace → chained-kernel | 64/8 | tpot_ms | -0.036180439 | [-0.096694294, 0.024333415] |
| smol | separate-kernel → chained-kernel | 1/1 | completion_ms | -0.018318572 | [-0.117197081, 0.080559937] |
| smol | separate-kernel → chained-kernel | 1/1 | tokens_per_s | -14.631280310 | [-95.358966269, 66.096405649] |
| smol | separate-userspace → chained-userspace | 1/1 | completion_ms | 0.003698647 | [-0.089044573, 0.096441867] |
| smol | separate-userspace → chained-userspace | 1/1 | tokens_per_s | 3.432024141 | [-66.926173298, 73.790221580] |
| smol | chained-userspace → chained-kernel | 1/1 | ttft_ms | 0.020347566 | [-0.062510117, 0.103205248] |
| smol | chained-userspace → chained-kernel | 1/1 | completion_ms | 0.020347566 | [-0.062510117, 0.103205248] |
| smol | chained-userspace → chained-kernel | 1/1 | tokens_per_s | 13.985542365 | [-49.172014545, 77.143099274] |
| smol | separate-kernel → chained-kernel | 64/1 | ttft_ms | -0.019802616 | [-0.142632579, 0.103027348] |
| smol | separate-kernel → chained-kernel | 64/1 | completion_ms | -0.536408497 | [-3.283739352, 2.210922358] |
| smol | separate-kernel → chained-kernel | 64/1 | tokens_per_s | -15.357568241 | [-93.981694674, 63.266558192] |
| smol | separate-kernel → chained-kernel | 64/1 | tpot_ms | -0.008200093 | [-0.049881126, 0.033480939] |
| smol | separate-userspace → chained-userspace | 64/1 | ttft_ms | 0.015569475 | [-0.005717783, 0.036856733] |
| smol | separate-userspace → chained-userspace | 64/1 | completion_ms | 0.020891650 | [-0.080666561, 0.122449861] |
| smol | separate-userspace → chained-userspace | 64/1 | tokens_per_s | 0.594074402 | [-2.515691570, 3.703840374] |
| smol | separate-userspace → chained-userspace | 64/1 | tpot_ms | 0.000084479 | [-0.001403991, 0.001572949] |
| smol | chained-userspace → chained-kernel | 64/1 | ttft_ms | -0.046327250 | [-0.138878828, 0.046224328] |
| smol | chained-userspace → chained-kernel | 64/1 | completion_ms | -1.038114534 | [-2.903737340, 0.827508272] |
| smol | chained-userspace → chained-kernel | 64/1 | tokens_per_s | -29.610622476 | [-82.957155985, 23.735911032] |
| smol | chained-userspace → chained-kernel | 64/1 | tpot_ms | -0.015742655 | [-0.043985012, 0.012499702] |
| smol | separate-kernel → chained-kernel | 1/8 | ttft_ms | -0.029805894 | [-0.147923139, 0.088311352] |
| smol | separate-kernel → chained-kernel | 1/8 | completion_ms | -0.029805894 | [-0.147923139, 0.088311352] |
| smol | separate-kernel → chained-kernel | 1/8 | tokens_per_s | -80.276973792 | [-312.017231245, 151.463283661] |
| smol | separate-userspace → chained-userspace | 1/8 | ttft_ms | -0.032782131 | [-0.154928336, 0.089364073] |
| smol | separate-userspace → chained-userspace | 1/8 | completion_ms | -0.032782131 | [-0.154928336, 0.089364073] |
| smol | separate-userspace → chained-userspace | 1/8 | tokens_per_s | -82.851742582 | [-300.899026548, 135.195541383] |
| smol | chained-userspace → chained-kernel | 1/8 | ttft_ms | -0.100438334 | [-0.220828058, 0.019951390] |
| smol | chained-userspace → chained-kernel | 1/8 | completion_ms | -0.100438334 | [-0.220828058, 0.019951390] |
| smol | chained-userspace → chained-kernel | 1/8 | tokens_per_s | -197.425957370 | [-484.946920402, 90.095005663] |
| smol | separate-kernel → chained-kernel | 64/8 | ttft_ms | -0.010086031 | [-0.231389758, 0.211217695] |
| smol | separate-kernel → chained-kernel | 64/8 | completion_ms | -1.491304575 | [-9.499398369, 6.516789219] |
| smol | separate-kernel → chained-kernel | 64/8 | tpot_ms | -0.023511405 | [-0.147471957, 0.100449146] |
| smol | separate-userspace → chained-userspace | 64/8 | ttft_ms | 0.032687572 | [-0.064919795, 0.130294939] |
| smol | separate-userspace → chained-userspace | 64/8 | completion_ms | -0.070030287 | [-0.414885583, 0.274825008] |
| smol | separate-userspace → chained-userspace | 64/8 | tpot_ms | -0.001630442 | [-0.005803149, 0.002542265] |
| smol | chained-userspace → chained-kernel | 64/8 | ttft_ms | -0.106497912 | [-0.244519494, 0.031523669] |
| smol | chained-userspace → chained-kernel | 64/8 | completion_ms | -2.974764397 | [-8.103646791, 2.154117997] |
| smol | chained-userspace → chained-kernel | 64/8 | tokens_per_s | -168.026317376 | [-452.077627075, 116.024992322] |
| smol | chained-userspace → chained-kernel | 64/8 | tpot_ms | -0.045528039 | [-0.124878078, 0.033821999] |

## Interpretation and return

The candidate genuinely halves successful device launch calls and passes both exact traced integration qualification and the fixed pre-observation untraced output-set contract. That causal mechanism engagement did not establish the predicted latency/throughput advantage. GPU compute, dependency/environment overhead and time-varying shared-resource exposure remain plausible explanations; this matrix does not isolate their individual costs. Correctness passes support retaining the opt-in research variant, but optional default adoption lacks measured benefit under the predeclared rule.

Keep the full result as a supporting implementation boundary and retain the existing separate default. Do not promote setup counts, a less complex launch sequence or selected positive means into a performance win. The experiment is finished scientifically; root still owns final honest finding/README/evaluation closure, artifact cleanup and authorized main commit/push. Future work should answer a distinct high-value uncertainty, such as total service CPU attribution/interference, without redefining this tested hypothesis to make its null-inclusive outcome successful.

Plan: [tail_chain_plan_20261012.md](tail_chain_plan_20261012.md). Fresh admission: [tail_chain_plan_review_20261012.md](tail_chain_plan_review_20261012.md). Raw/source/command/lifecycle archive: [tail_chain_20261012/](tail_chain_20261012/). Recomputed model analysis outputs: [Qwen](tail_chain_20261012/qwen_performance_analysis.stdout.txt), [Smol](tail_chain_20261012/smol_performance_analysis.stdout.txt). Frozen asset: [frozen_references.json](tail_chain_20261012/frozen_references.json).

Final same-review draft audit: independently checked every numerical primary table cell in docs/findings/0036-tail-chain.md against the raw-derived summaries/effects; all eight means/gains/intervals match at six decimal places. README/evaluation completion counts and eight-primary interpretation match the complete raw matrix. All56 executor bootstrap logs independently confirm520 graphs, batches1..8, queries1..64, eight disjoint physical page rows,128-token context and65 cache blocks. The root draft journal wording should distinguish archived OOM from documented live NotReady observation; no new scientific rerun is required for that wording.
