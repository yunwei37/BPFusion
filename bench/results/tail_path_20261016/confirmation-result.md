# Close-scan candidate: complete matched confirmation

Observed 2026-10-16T09:20:05..09:37:53 UTC. Source parent f397f83; the
before/fixed/native executors and all workloads were frozen before collection.
This is the planned five-block follow-up, with no timeline/ftrace, equally
BF_TRACE, Qwen2.5-0.5B-Instruct revision7ae55760, FP16, 16 slots, gen64,
256 normalized gamma arrivals per cell at96/192 requests/s. Same pinned
vLLM0.31.0/Torch2.13.0 runtime and RTX5090 as the diagnostic.

## Result and adoption decision

**Inconclusive benefit; do not adopt the close-scan candidate.** The primary
after-minus-before ITLP99 at192 is **-0.167588 ms**, nominal paired t95df4
**[-1.533927, +1.198750] ms**. The five block effects are
+0.165075, -1.131296, +1.607038, -0.761900, -0.716859 ms.
The interval crosses zero; this is neither superiority nor equivalence.

Mean of each process block's P99 (ms), not a pooled request percentile:

| Rate | Before kernel loop | Candidate kernel loop | Efficient native |
| --- | ---: | ---: | ---: |
| 96 | 3.754489 | 3.790730 | 3.629037 |
| 192 | 4.608287 | 4.440699 | 4.718439 |

The candidate/native192 difference is -0.277740[-3.583043,+3.027563]ms.
The old0065 14.723/8.363ms difference did not reproduce even in the unchanged
before condition. No cross-run improvement is attributable to this candidate,
and no exact additive allocation of the historical6.36ms has been established.
The complete diagnostic supports distinct GPU iteration, runnable scheduling,
and client delivery/observation delays, with shared-host exposure; it does not
identify a single exclusive root cause for a marginal historical quantile.

## Throughput and adverse evidence

| 192 metric (mean of process blocks) | Before | Candidate | Native |
| --- | ---: | ---: | ---: |
| Delivered output token/s | 10764.320 | 10955.967 | 11072.221 |
| Executor process CPU ms/attempt | 0.909721 | 0.766951 | 0.508810 |
| Connect-origin TTFT P99 ms | 139.808954 | 113.555680 | 95.234675 |
| Connect-origin completion P99 ms | 225.004769 | 198.678192 | 179.315514 |
| Client scheduling lag P99 ms | 5.486507 | 8.492538 | 12.398506 |

Candidate-before output token/s difference +191.647[-395.092,+778.387];
candidate-native -116.255[-403.394,+170.885]. Neither establishes throughput
superiority. At96 output rates are5963.520/5963.772/5967.079 token/s.
All reported windows include drain after the offered schedule.

An adverse finding is retained: candidate-native executor process CPU is
+0.258141[+0.177460,+0.338822]ms/attempt at192 and
+0.135698[+0.098944,+0.172452] at96. This process clock excludes some kernel
workers/softirq and does not measure GPU cost. It contradicts a process-CPU
saving claim for these particular conditions; do not carry earlier CPU-saving
numbers into this run. It is not the full resource experiment.

All TPOT, TTFT/completion P50/P95/P99, scheduled-origin latencies, per-block
throughput, CPU, failures, timeouts and client lag are in the complete
confirmation/full.analysis.stdout; there are no favorable block exclusions.
Nominal five-block t intervals assume the usual paired-process model and do not
establish generality across machines, shared-host conditions, models or rates.

## Completion and correctness

All15 executors and30 cells completed; **7680/7680 measured attempts** succeeded,
with **491520 exact measured output tokens**, plus120 excluded checked gen1
warmups. Every actual trajectory passed both captured-history and independently
rebuilt source-native attention-metadata replay, ownership/FIFO retirement,
zero graph/trace/ring errors and complete cleanup. The only changed execution
source is the published +5/-1 conservative close-scan predicate. Native shares
the identical mixed constructor and its unchanged efficient epoll transport.

The real three-condition32-arrival preflight also passed. Candidate safety:
Qwen and Smol default8 traced protocol each640 outcomes/23376 checked tokens,
plus ordinary non-BF_TRACE loop lifecycle each144 outcomes, including idle,
HTTP400/recovery, binaryEOF, half-close, RST/backlog RST and mid-output SIGTERM.
The ordinary oracle is the finite exact pre-observation output set, not a
universal numerical correctness proof. Unobserved cancels remain incomplete.
Before native ordinary lifecycle remains in ordinary_before/, unchanged.

Large raw files are losslessly gzip-compressed (mtime0). The archive analyzer
only adds transparent original/.gz reading; its preflight and full stdout were
independently rerun and byte-equal to the original analyzer. Executed analyzer
is also retained as confirmation/analyze_original.py. CPU replay from repo:
python3 bench/results/tail_path_20261016/confirmation/analyze.py
bench/results/tail_path_20261016/confirmation/full.jsonl
(the logical .jsonl name resolves its .gz sidecar). Exact commands and original
runtime paths remain in confirmation.statuses.json and candidate_safety/.

## Interpretation and remaining work

This is valid supporting evidence if independent review confirms its validity;
the narrow candidate benefit remains inconclusive. Keep the root close scan
unchanged, publish the negative result, and do not tune a timer or repeat the
unchanged collection until it looks positive. Mixed scheduling has passed the
default8 engineering checks but still needs ordinary source integration.

The requested full resource accounting, sustained remote/client tails, current
official vLLM server reference and non-LLM CUDA Graph integration remain open.
They must preserve these adverse findings. The next work will distinguish
shared-host/client scheduling exposure and whole-service cost from the
particular repeated-load hypothesis rejected as a demonstrated fix here.
