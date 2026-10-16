# Sustained remote official vLLM reference

2026-10-16 UTC, source entry main d843e92. research-experiment-design supporting
whole-service comparison; benchmark only, not deployment. Retained objective:
"a complete Linux TCP/HTTP + eBPF/shared queue to resident real-model inference
and asynchronous kernel TX, with reproducible matched correctness and
throughput/latency evidence." No formal paper RQ/thesis/idea-story exists.

## Admission and decision

User explicitly requires same-model/GPU official server throughput/P99 and a
credible same-executor native baseline. Completed0077 tests ordinary network
placement and finds local TPS+0.22%/completionP99-124ms at+28.5% owned CPU,
without native advantage or historical6.36ms repair. Official0069 instead uses
only256 requests (~1.33s offered load) and loopback/threaded clients; its drain
and cache/schedule/protocol behavior cannot rank current60s remote saturation.
No existing valid raw dataset or published number supplies that missing match.

This integrated comparison tests whether current resident serving keeps up with
official optimized vLLM on the sustained workload already exposing queue tails.
Positive, negative or mixed results change external performance positioning
and whether subsequent optimization should target common scheduling/compute
rather than just the eBPF transport. Neither result proves eBPF novelty or
intrinsic advantage. It outranks another small cache/wait sweep or generic
interface dependency test by answering the user's missing strongest competitor.
No changed scientific claim, model-kernel rewrite or broader workload matrix.

## Strongest comparisons and fixed primary

O: official vLLM0.31.0 optimized server, strongest external whole-service
competitor; normal scheduler, chunked prefill, prefix cache, compilation and
CUDA graphs, with actual startup config logged. Do not cap sequences/tokens/
memory/context or force eager. Its capacity/cache differ from resident16.
N: efficient native C++ epoll with the identical reused resident GPU executor,
main alternative mechanism/causal component comparison.
K:0077 kernel-owned BPF network candidate, currently unselected, same compiled
GPU dispatch as N. Selected old GPU-I/O loop has its complete matched0077
ablation and is omitted here as redundant. Do not convert official differences
in scheduler/KV/API/bytes into an eBPF attribution.

Fixed primary N-minus-O delivered successful output tokens/s under192/s offered
load, five paired blocks, nominal paired95%t(df4,2.776445105). Positive interval
supports better delivery at this fixed load; negative contradicts it; crossing0
is inconclusive, not equivalence. Report K-N and K-O separately. Capacity above
this offered load is unidentifiable; no maximum-throughput/general-SOTA claim.
TTFT/completion/TPOT P50/P95/P99, client receive-gap P99, scheduled-origin tails,
all-attempt failures/partial outputs/timeouts, client lag/CPU and server cost
views remain mandatory secondary context, not post-hoc replacement primaries.
Correctness/unfair baseline engagement can invalidate the comparison; adverse
secondary metrics remain disclosed.

Definitions reuse https://docs.vllm.ai/en/stable/benchmarking/cli/ (opened
2026-10-16). Tokens receive their client receive-chunk timestamp; SSE frames
are not tokens and coalesced tokens get equal stamps/zero gaps. This is a
client-observed per-token gap, not official per-stream-output ITL. Both original
zero and positive-only gap views remain. Protocol/client parsing differs;
do not attribute gap differences exclusively to GPU or kernel. Compare
connect-origin plus scheduled-origin latencies; official connect-origin includes
the aiohttp HTTP setup and is explicitly not a measured send-done interval.

## Frozen workload and correctness

Same original lab RTX5090/Linux7.3rc3, pinned vLLM0.31/Torch2.13cu129 runtime,
Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775 FP16,
four frozen short token-ID prompts,gen64,temperature0,ignoreEOS.
Reuse exact remote_offsets.json seeds20261015+block,11520 arrivals at192/s
over60s plus full drain, five blocks and3 fresh processes/block:
K,N,O; N,O,K; O,K,N; O,N,K; N,K,O.
15cells172800attempts11059200 output tokens if all succeed. Eight sequential
checked gen1 warmups/process excluded. No changed client/oracle/metric/timer
during full acquisition, no profiler/GPU trace/heavy builds/Git in serving windows.

K/N binary HTTP client branch is unchanged except mode/official branching.
O reuses qualified0069 tokens-only request/SSE validation via necessary async
adapter and aiohttp3.14.5 HTTP/chunk framing, unlimited connector/one new
connection per attempt. No application concurrency cap. Binary connect/drain/read each has60s I/O timeout. Official aiohttp connect
and socket-read use60s timeouts with no separately exposed socket-write
timeout; the small request body follows aiohttp defaults. No total-deadline
censoring on either path. This client timeout difference is explicit, not an
invented equivalent send bound. No retries/replaced cells.
Retain all requests, malformed/short/vocabulary/prompt/finish failures, partial
tokens and decoded SSE frame objects. Frozen pool agreement remains a flag, never expanded
after observation or used to exclude optimized trajectory disagreement.
Gen1 warmups must match the frozen pool.0077 two-model dual replay is finite
prior correctness support, not exact untraced full-run or universal parity.
Official request values match its installed source-native protocol. Its normal
cache remains enabled and four repeated prompts limit generalization.

Reuse current resource_observer.py and analysis definitions. Owned TGID may
include io-wq, cgroup includes observer/control, host softirq/device include
foreign work: nested views never sum and no exclusive total CPU/energy claim.
Client CPU/lag/context are recorded. One client event loop could limit either
protocol; delivered throughput is not an exclusive GPU/server capacity ceiling.
If preflight reveals a client/protocol failure, repair it before full collection;
do not reinterpret a broken or bottlenecked external baseline as a win.

## Executable path, lifetime and cleanup

Original yunwei356/bpfusion-dev Workspace only; no new service/Workspace/host
setting. Own private Workspace IP ports39403(K/N)/39404(O), no public routing.
Official command:
TEMP/runtime/bin/vllm serve MODEL --tokens-only --dtype half --host WORKSPACE_IP
--port39404. Remove capture-only VLLM_ENABLE_V1_MULTIPROCESSING=0 for O.
Existing runtime/GPU/model files reused. Ephemeral VLLM_API_KEY stays only in
OS TEMP/client memory/file, never args/logs/Git; actual missing/invalid auth401
and successful requests checked. No auth for native binary protocol is invented.

Bounded disposable Python3.12.12 client Job reuses previous name and source-
qualified manifest after actual oldUID removal. No CPU/memory quota/node pin;
anti-affinity excludes actual GPU Workspace placement. Install only aiohttp
3.14.5 for official HTTP/chunk decoding; snapshot package versions. It ends
with exactUID Job deletion and verified Pod absence. No persistent dependency.
Outer agent owns cleanup; server child groups receive SIGTERM after each cell.
Record parent exit/graceful wait, remaining EngineCore and any necessary owned
group SIGKILL as cleanup, never hide previous0069 shutdown behavior. Require
no remaining GPU processes/pins before another cell. Original PID1/10909
and foreign setup_env.sh preserved.

Actual scripts in this directory:
run_official_remote_matrix.ps1 -ClientPod POD -ServerIP IP [-Preflight],
official_remote_server.py, official_remote_client.py, official_remote_analysis.py.
TEMP scripts use the same runtime/environment/build paths as archived. Preflight
uses first128 exact block0 offsets and all3 real conditions. At most3 preflight
attempts; failures/deviations retained, only necessary executable repairs.
After successful real preflight, run all15cells unchanged, save original
client/server/warmup/resource/log/terminal receipts after each stopped process.
CPU replay of archived gzip must reproduce acquisition analysis exactly.
Fresh plan reviewer before execution; fresh result reviewer after complete data;
actual cleanup, review, final result/navigation and main commit/push close run.
Target figure:5 paired TPS/completionP99/receive-gapP99/ownedCPU values, all
adverse rows retained. No primary switch, larger N or unchanged retry.

Research value supporting, paper impact additional serving-objective evidence
and workload/method boundary. Old6.36ms allocation, total service CPU and generic
plugin compatibility remain open; this experiment does not claim to solve them.
