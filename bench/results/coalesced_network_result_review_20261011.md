# Coalesced network comparison: independent result review

Review target: [approved plan](coalesced_network_plan_20261011.md), frozen source
cc07226eb9680c90134279bce0d58fc0b730280e, both complete retry1 JSONLs and
[native analysis plus independent reconstruction](coalesced_network_analysis_20261011.stdout.txt).
Reviewer: fresh read-only agent coalesced_network_result_review. No source,
configuration or GPU experiment was changed by the reviewer. Observation date:
2026-10-11 UTC. The original full research objective remains active.

## Initial independent review

Run status: valid completed raw measurements and correctness evidence.
Tested hypothesis: inconclusive. Research value: supporting.
Paper impact: mechanism/workload boundary, not a direct thesis challenge.
The initial health interpretation is corrected below; it must not be used
to describe the comparison as interference-free.

The reviewer read the plan and all three plan-review discussions, retained
goal/handoffs, evaluation/finding documents, benchmark/oracle and transport
sources, six production-file repair diffs, qualification and trace receipts,
both retry1 raw files, and the analysis receipt. An independent reconstruction
through stdin reproduced all measured request timings, cell throughput,
global CPU work, order, token agreement, and all twenty executor counters.

| Model | Primary effect | Mean | Nominal paired t95 interval |
|---|---|---:|---:|
| SmolLM2-135M | User minus kernel TTFT, gen1/client1 | -0.130363 ms | [-0.490798, 0.230071] ms |
| Qwen2.5-0.5B | User minus kernel TTFT, gen1/client1 | -0.042867 ms | [-0.116078, 0.030344] ms |
| SmolLM2-135M | Kernel minus user TPS, gen64/client8 | +1.229153 tokens/s | [-9.310734, 11.769040] |
| Qwen2.5-0.5B | Kernel minus user TPS, gen64/client8 | +78.277177 tokens/s | [-132.336242, 288.890597] |

All four intervals cross zero: neither superiority nor equivalence follows.
These are five-pair descriptive t95(df4) intervals, without a family-wide
significance claim. Exact paired differences are retained in the native
analysis and independent reconstruction receipt.

Each model has 40 complete cells, 2560 measured requests and 83200 exact
measured tokens, ten bootstrap/idle/executor records, and no failure row.
Combined totals are 80 cells, 5120 requests, 166400 tokens and twenty normal
executor exits. Complete request-index coverage, case=index mod4, sixteen
requests per prompt per cell, alternating mode order, rotated cell order,
monotonic arrivals and exact independent eager FP16 HF oracle agreement pass.
The oracle is released before measurement and does not derive expected outputs
from the measured executor.

Every executor has one resident launch, 8580 model graph steps, graph_error=0,
eight banks and max_active=8. Every kernel record has 264 stream publications,
head=264, busy=0, reserved=0 and eight FREE slots. Every user control has
accepted=19, published=264, completed=264, rejected=0. Each process's 264
requests are 256 measured requests plus eight warmups.

Both transports wait for available output and submit remaining header/body
together with vector sends, retaining byte-level partial-send accounting and
DONE-before-recycle ownership. Native epoll uses the same resident device
dispatcher/model graphs, without a Python per-token loop. This is a credible
component ablation, not an external SOTA baseline. Polling, page backing and
other path work still differ. Kernel TCP/eBPF/TX consumes host CPU; no
syscall-only causation or CPU-free-system claim is supported.

The first failed full prefix remains separate: 17 cells, 1144 exact replies,
one timeout/busy refusal at head72/WRITING/head_changed0; Qwen did not begin.
No rows are stitched into retry1. Repair qualification covers atomic slot and
sequence reservation, release after FREE/old accesses, unchanged ABI layout,
four graph cases, explicit-release kernel reruns, the retained bridge cleanup
failure and its complete corrected rerun, and actual-main delayed publication.
The model graphs, benchmark/oracle, timeouts and primary estimators are unchanged.
Six production files grew by net19 lines, plus net3 test-cleanup lines; no new
map, service or experiment-control interface was added. Qualification is not
an exhaustive race/overload proof.

Both full metadata records identify frozen cc07226 source; terminal exits are
Smol09:28:06 UTC and Qwen09:42:08 UTC. Reviewer live cleanup checks near
09:53-09:56 UTC find wrapper89640 absent, TX module absent, bpffs empty, no
loopback ingress/egress filters and no bpftool net attachments. Original
SGLang PID2762187/start time and 18368 MiB GPU residency remain; boot ID matches.
These are preservation and cleanup observations, not a service acceptance test.

Historical passive traces retain sixteen headers with 79 header bytes plus
four token bytes, followed by roughly40.397-42.255 ms before ACK and
0.013-0.037 ms before remaining28 bytes. They are observer-limited mechanism
diagnostics for the earlier candidate, not matched old/new optimization
measurements or GPU-ready timestamps. Current concurrent one-token delays
remain; no all-transport-latency-removed claim follows.

## Follow-up 1: verified OOM and corrected interpretation

The root compared the initial health assertion with its full post-run host
receipt, which contained OOM messages. The reviewer repeated journal queries
with explicit UTC and OOM patterns. Its initial statement that there were
no host fault entries is withdrawn: the initial query omitted OOM patterns
and used --since without an explicit timezone.

| Evidence | Time or window |
|---|---|
| Journal displays global OOM and kills | 2026-10-11 09:37:40 UTC |
| Qwen user pair3/gen64/client8 GPU observations | 09:37:28.538-09:37:42.526 UTC |
| Paired kernel cell GPU observations | 09:39:02.903-09:39:08.992 UTC |
| User cell measured monotonic interval | 142820616074123-142834495866302 ns |
| OOM kill kernel source monotonic timestamp | 142828604210 us |
| OOM reaper kernel source monotonic timestamp | 142831619252 us |

Both source timestamps are inside the measured user cell, about7.988 s and
11.003 s after the first request start. Journal ingestion timestamps differ
from kernel source timestamps; the monotonic comparison establishes overlap
without assuming a precise wall/monotonic clock calibration.

Global OOM killed repl PID3768997 (anon-rss:88120172kB) and its cgroup siblings
under memory.oom.group. It does not establish which workload caused pressure
or that BPFusion caused OOM. The exact explicit-UTC commands, source journal
records, current host observations and raw measured interval are appended to
the analysis receipt.

The user cell contains eight roughly9.87-10.45 s requests spanning this episode.
Its 295.105 TPS and247.94 s global CPU work have a concrete coincident host
pressure confound. Other user blocks deliver681.010-689.601 TPS; the paired
kernel cell occurs about80 s later without the same recorded OOM exposure.
Alternating order does not remove this unequal exposure.

Corrected verdict:

- Run status: valid completed raw measurements and correctness evidence.
- Tested hypothesis: inconclusive; Qwen primary throughput cannot identify
  a transport-only effect under unequal OOM exposure.
- Research value: supporting, with an explicitly documented shared-host event.
- Paper impact: tested mechanism/workload boundary.
- Next decision: keep all blocks and report unchanged descriptive estimates
  alongside the incident; close this matrix.

All exact-token checks, counters and terminal exits remain intact. No sample
was removed and no selective retry was performed. The Qwen primary estimate
remains +78.277 [-132.336,288.891] tokens/s; the interval does not resolve the
confound. Replace unexplained-variability wording with large variability
coincident with verified global OOM and unequal paired exposure. OOM/reclaim/
scheduling is a supported competing explanation, but the logs do not quantify
its contribution or separate client, reactor and GPU progress.

The next decisive uncertainty is service-attributed host work and sensitivity
under explicitly matched or measured host interference. Existing process/global
CPU counters cannot establish it. Strong external serving, physical networking,
full text processing and online batching remain separate open requirements;
this valid raw result does not complete the full objective.
