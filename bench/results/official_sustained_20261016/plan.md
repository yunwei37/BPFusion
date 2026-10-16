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

## Preflight-driven common client repair, before full acquisition

Initial preflight1 is retained in preflight1.md/official_remote_preflight/:
all protocol/outcomes pass, but official client lagP99~49ms versus6--11ms on
binary and clientCPU near one core exposes a comparison risk. Full not started.
Replace only asyncio.run with uvloop0.23.0.run for all3 clients and record actual
event-loop version in metadata. Installed official vLLM throughput benchmark
uses this upstream event-loop library; serve benchmark uses asyncio.run.
No parser/request/schedule/oracle/timeout/analysis change or extra concurrency
setting. initial_client/ preserves old client/driver/context. Second real
preflight uses official_remote_preflight2 and the same128 offsets; evaluate
actual lag/CPU before full collection. At most3 total preflight attempts still
applies. This is a necessary client repair, not a new scientific hypothesis or
a favorable-prefix rerun of server performance.

## Final preflight-driven client repair, before full acquisition

Second uvloop preflight preserves384 successes but official lagP99~27ms
versus3.5--4.6ms, and~5.2ms clientCPU/attempt approaches one core at192/s.
This does not prove official SSE costs more CPU or the server is slower.
preflight2.md and single_uvloop_client/ retain all data and actual source.
For allK/N/O, two ordinary OS processes in the same client Pod split original
request indices even/odd, each with unlimited async tasks and the same future
monotonic epoch/full offsets. No request/parser/oracle/timeout/server change.
This adds no persistent dispatcher/helper, experiment-control schema or cap.

Keep both original worker JSONL files. The existing client merges original
request rows after both terminals, validates exact indices/common schedule,
and uses common epoch through the last original request close for elapsed
time; startup/worker exit skew is not serving time. This refines the prior
post-gather end by only final bookkeeping and is applied identically before
full acquisition; do not mix metrics across preflight versions. Merge/analysis
after drain is outside delivered-throughput timing. Active-request peak is
derived from task-start/close intervals (close before start at equal timestamps). Client CPU records actual child deltas
plus supervisor startup/wait/merge separately, with worker counters retained.
Resource observer bracket includes the post-drain transfer/merge context and
is still not exclusive service cost.

Third and last real preflight official_remote_preflight3 uses identical128
offsets and all3 real backends before any full cell. Fixed primary,5blocks,
original full schedule,finite oracle and adverse retention do not change.
Fresh same-plan final follow-up audits actual source. No more unchanged
preflight/largerN or favorable client-prefix selection is authorized by this
plan. If a scientifically usable path is not established, preserve results
and return the actual dependency/comparison boundary.

Owner implementation receipt for final review condition: after serializing/
writing the complete arrival_schedule event and before any worker request
loop, the actual source asserts now()<epoch. A late worker records the existing
client_failure/terminal failure and raw worker file; it cannot silently qualify
late injected traffic. Parent and archive analysis also check readiness stamps.
The final review's conditional executable concern is therefore addressed
before the third real preflight; no additional review round or run occurred.

## Full-acquisition repair after the first sustained block

first_full.md retains the incomplete3-cell/34560-success prefix and
two_worker_client/ its exact source. Sustained official arrival-lagP99~415ms
(max796ms) exposes a client-fairness defect absent from the128-request
preflight. No server defeat/paired primary is claimed. After all server
groups exited0, stop only the verified Windows driver/tool descendants in
raw recovery, preserve/recover all originals, and leave the original
Workspace/PIDs/Job intact.

Repair only common client distribution from2 to4 unrestricted OS processes
for allK/N/O. Original indices/offsets are partitioned modulo actual worker
count; client owns the one count, raw transfer/analysis discover metadata.
Same request/parser/oracle/timeout/epoch/last-close denominator/primary.
This changes no backend computation, default or persistent configuration.
The full-run systematic-defect rule requires all affected comparisons to
restart: official_remote_full_retry1 runs the complete15 planned cells from
block0; original cells remain separate, no mixing/favorable replacements.
This is not a fourth preflight. Full eligibility uses already-qualified
actual API/parser/worker-join path; fixed full matrix and result review
determine the repaired comparison's validity. No additional preflight or
review round is introduced. Client lag/CPU can still invalidate an external
ranking, and must remain explicit rather than calling a client limit a win.

Post-serving acquisition-only change: remove the inherited256KiB chunk cap
from raw gzip recovery and send the remaining original file through the
existing stdin stream. Fleet's existing Invoke-FleetSsh/Invoke-Kubectl path
already streams pipeline data without command-argument embedding. Actual
initial11.36MB official gzip recovery took minutes of repeated SSH/API calls.
This changes only after-stop archival, not any measured client/server/clock/
metric. Durable prefix lengths, original byte counts and lossless gzip checks
remain. No new transfer helper, checksum gate, persistent setting or runtime
configuration. Initial chunked driver remains in two_worker_client/.

## Client root cause and necessary repair

The actual client-only instrumented60s control is complete. Default generation2
GC pauses up to395--473ms overlap89.37% of the worst1% actual client task-start
delay time; exclusive non-GC logging2.38%, residual8.25%. See
client_diagnosis/original_result.md and raw analysis. This is same-worker
interval coverage, not summed P99s or GPU/Linux stage attribution. Merely adding
workers did not fix the retained decoded SSE object graphs.

Keep4 common workers, default GC enabled/thresholds unchanged, synchronous
durable per-request output and all parser/oracle/timeout/arrival/primary
semantics. Store complete raw SSE data payload text plus its receive timestamp,
decode only transiently, and stop retaining nested decoded response trees.
Lossless payload text also permits independent archive reconstruction of
prompt/finish/token/arrival fields; existing full correctness checks remain.
No decoded model-output disagreement is excluded or added to the frozen pool.
One instrumented same-workload payload control tests this fault repair before
the ordinary full restart. It is a diagnostic causal control, not an extra
preflight or changed scientific primary. All earlier incomplete prefixes,
transfer failures and instrumented values remain distinct and preserved.
