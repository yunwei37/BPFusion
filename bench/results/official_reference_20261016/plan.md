# Current resident backend versus official vLLM server

2026-10-16 UTC. Original bpfusion-dev Workspace and RTX5090 only.
User performance question: where does the current reused-compute TCP server
stand against official optimized serving, while retaining the efficient
same-executor native baseline that isolates the transport mechanism?

## Admission and decision
Finding0031 compares the older HF backend at about1408 vs4714 token/s; it cannot
rank the current upstream-vLLM mixed backend now delivering about11000 at192
offered requests/s. Findings0065/0066 provide matched transport evidence and an
inconclusive close-scan retest, not a current external serving reference.
The strongest runnable competitor is official vLLM0.31.0 server on the same
GPU, checkpoint and FP16 runtime. No additional compute project or weaker
Python/token-step baseline is needed. This supporting whole-service comparison
tests whether the current design's measured throughput and client tails are
competitive with that official implementation; it does not redefine the
project's full Linux TCP/eBPF/shared-queue/resident execution objective.

Positive/negative/mixed outcomes change the performance positioning and identify
whether a competitive whole-service result is even plausible on this finite
workload. They cannot establish an eBPF speedup against official vLLM, because
scheduler/capacity/cache/HTTP framing differ. If native matches or beats kernel,
the eBPF superiority claim remains unproven regardless of the official result.
This is independent of generic-backend engineering acceptance and full-resource
or sustained-remote studies; it does not count those tasks as completed.

## Conditions and competing implementations
Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775,
FP16, existing pinned vLLM0.31.0/Torch2.13.0+cu129/Transformers5.17.0,
same RTX5090 and Linux7.3rc3. Four existing short tokenized prompts,
gen64, temperature0, ignoreEOS, no text/tokenizer work in serving.
Three conditions:
- Normal-source resident mixed vLLM graph + BPF/io_uring loop,16 slots.
- Identical mixed graph executor + efficient native timed epoll,16 slots:
  the main competing mechanism / causal component baseline.
- Official optimized vLLM token-only server, unmodified defaults:
  strongest external whole-service reference.

Official command is runtime/bin/vllm serve MODEL --tokens-only --dtype half
--host127.0.0.1 --port39404 (actual CLI uses separate arguments).
Remove the capture-only VLLM_ENABLE_V1_MULTIPROCESSING=0 from the official child
environment. Preserve normal optimized scheduler/compile/graph/cache defaults:
no eager-only, sequence/batch/cache/utilization/context limit or affinity tuning.
Record actual logs/configuration and verify intended optimized mechanism.
Official adaptive capacity and default cache differ from resident16 slots;
do not artificially weaken it to mimic an internal implementation.
Native/kernel use ordinary non-BF_TRACE source-selected mixed libraries and the
unchanged transport header: the close-scan candidate is not adopted.

Official endpoint /inference/v1/generate uses token IDs and JSON/SSE. Resident
HTTP carries binary token IDs. Reuse the project's already qualified official
API reader and socket client, adapting only the common workload/arrival glue.
Retain token IDs, prompt, stream finish, lengths, vocabulary checks and all
failures. Compare exact outputs with the unchanged finite pre-observation
reference pool and report agreement separately for every condition. Different
optimized batch trajectories may change greedy IDs. No same-output, task-quality
or universal-fidelity claim follows; malformed/short/invalid-vocab/incorrect
prompt or finish is a protocol/correctness failure. Do not expand the reference
pool after seeing output or discard disagreement rows.

## One integrated comparison
Five process blocks, all three conditions each, order:
[kernel,native,official], [native,official,kernel],
[official,kernel,native], [official,native,kernel], [native,kernel,official].
Two gen64 regimes,256 attempted requests/cell:
1. the existing normalized-gamma192 requests/s schedule, seed20261015+block;
2. closed-loop16 concurrent clients, matching the existing serving comparator.
Alternate regime order across blocks. Exclude exactly8 declared checked gen1
warmups per process. Keep all blocks; no favorable replacement.

The first regime connects each request independently and retains scheduled,
thread-start, connect, send/recv completion and token-arrival times, errors,
partial bytes/tokens and original60s request timeout. Record scheduling lag
and scheduled-origin TTFT/completion. The closed-loop regime retains16 worker
connections and all256 outcomes, including failures; no success-only time
window. Every cell is complete only after all attempts terminal.

## Standard metrics and uncertainty
TTFT, completion, TPOT excluding first token, request throughput and delivered
output token/s follow the official
[benchmark CLI](https://github.com/vllm-project/vllm/blob/main/docs/benchmarking/cli.md).
The frozen primary gap metric is explicitly client-observed per-token gap P99,
matching the existing BPFusion comparison: for per-token receive stamps a[j],
gap[j]=(a[j+1]-a[j])/1e6 ms. It is not official stream-output ITL.
Each token in a coalesced receive/frame gets that receive timestamp, so zero
gaps are retained. Report zero-gap/token-coalescing exposure and a separate
positive receive-gap distribution; do not equate this primary with the official
benchmark's streamed-output ITL. SSE chunks are not tokens. Retain client bytes
and parser/protocol differences rather than attributing them to eBPF.
Use linear percentiles, per-process P50/P95/P99, and arithmetic block means.
Primary external contrasts are resident-native minus official:
output token/s in closed16, and ITLP99 at offered192. Report nominal paired
t95df4 across the five complete process blocks. Crossing zero proves neither
superiority nor equivalence. Kernel/native contrasts are reported separately
and cannot be replaced by the official comparison.
Also report TTFT/completion/TPOT P50/P95/P99, achieved throughput, all-attempt
failures/timeouts, partial results, scheduling lag, scheduled-origin latencies,
and owned-process CPU (explicitly not total service cost).

Timing denominator spans each complete workload including drain, not only
successful replies or the offered interval. Standard output throughput counts
successful-request tokens, with this definition explicit; also report partial
tokens and all-observed-token throughput, never hide partially delivered work. Failure-censored successful tails
remain identified; do not count timeout60s as a completed request or a valid
populationP99. No SLO threshold, universal max throughput or production claim.
Shared-hostCPU/GPU/boot observations and time-window journal are exposure,
not proof of isolation. No foreign workload is stopped to improve numbers.

## Execution, preflight and cleanup
Engineering dependency: normal-source default8 qualification/integration,
ordinary16 compilation and complete ownership/cancellation checks precede
this collection. Freeze actual source/Make/runtime/driver and final commit
before preflight. One real3-condition preflight uses16 requests in each regime
and exercises the actual API/client/metric path. At most3 preflight attempts;
retain failures and deviations, repair only executable defects, then run all
15 processes/30cells/7680attempts plus120excluded warmups to terminal.
Fresh plan review precedes preflight; one fresh result review follows full run.

Bounded benchmark only, not deployment: lab/owning Workspace, loopback ports
39403/39404, ephemeral environment-only official API key (never logged),
missing/invalid-key denial checked. Each child group is stopped after its
two cells by SIGTERM with exit/remaining children recorded. Forced cleanup is
retained if needed. No service/scheduler/host tuning or persistent entity.
No GPU overlap with ordinary-source qualification or another own run.
Remove owned pins after each kernel process, and all temporary processes at
the end; preserve the original Workspace/Coder sessions/builds/WIP.

Runnable acquisition will be TEMP/official_reference.py --output PATH
[--preflight]; CPU reanalysis uses TEMP/official_analysis.py PATH. Actual frozen script and
commands/raw/source/logs stay in this directory. All timing outputs, failed
prefixes, reviews and interpretation are committed/pushed on main after each
complete validated stage. No paper, thesis or RQ text is rewritten.
