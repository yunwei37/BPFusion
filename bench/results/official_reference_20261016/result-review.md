# Independent result review: current official serving reference

2026-10-16 UTC. Fresh RESULT REVIEW of the completed five-block experiment.
Read the admitted plan and focused follow-up, frozen acquisition/API readers,
analysis, source, failed first preflight and complete second preflight, all
full raw request/cell/executor records and all fifteen server logs. No new
benchmark, GPU execution, source modification or Git publication performed.
This review writes only this file.

## Separate judgments

- **Run status: valid** for the declared finite, token-only, loopback,
  whole-service comparison, including the explicitly adapted client per-token
  observation metric.
- **Tested hypothesis: supported in the narrow frozen primary contrasts.**
  Resident-native has higher closed16 delivered token throughput and lower
  offered192 client-observed per-token-gap P99 than official in these five
  blocks. Broader competitiveness is mixed: closed16 streaming gaps are much
  worse in both resident paths, and several other uncertainty intervals cross
  zero. This is not universal latency or serving superiority.
- **Research value: supporting.** This updates the older HF-backed external
  reference with the actual source-selected resident mixed implementation.
  Preflight and archive checks remain dependencies, not extra contributions.
- **Paper impact: additional RQ evidence and workload/mechanism boundary.**
  No direct thesis challenge or eBPF superiority follows.
- **Next paper decision:** publish the bounded external-reference results and
  tradeoffs; retain the same-executor native baseline for mechanism attribution.
  The current data still do not establish an eBPF speed or total-CPU win.
  Continue the separately requested full-resource and sustained-remote work;
  no replacement experiment or additional baseline is a validity condition.

## Completion, provenance and executable path

The raw terminal record is exit0 at10:22:29UTC, with15 executors,30 cells,
7680 measured attempts,7680 successes,491520 measured tokens and120 excluded,
checked gen1 warmups. Every cell contains exactly256 indexed attempts; all
measured replies contain64 in-vocabulary integer token IDs. All120 warmups
match the frozen reference set. No failed or censored measured request, partial
output, hidden timeout or favorable replacement block occurs.

All five declared three-method orders and alternating regime orders execute.
Offered192 uses the same normalized arrival offsets within each paired block;
closed16 uses16 persistent client connections,16 attempts per lane. Offered192
connects independently per attempt. The full-window throughput denominator
includes workload drain, as planned; no startup or model-load throughput claim
is made. The sixty-second request timeout and reference pool are unchanged.

Metadata records documentation/preflight commit
f04d8bc662d3f649d9dc21133bac8067a8ae01a9. Independently compared all seven
frozen compute/transport/Make source contents with the raw embedded source and
with source-selection commit45f0ec2: all equal. In particular, the speculative
close-scan change is absent. Actual commands use ordinary sourcebuild16 mixed
kernel/native binaries, not BF_TRACE binaries. The exact model snapshot is
Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775.
Raw versions are vLLM0.31.0, Torch2.13.0+cu129, Transformers5.17.0 and numpy2.3.5;
GPU RTX5090 UUID7eb74118-ee90-99c7-6567-e2d50fdf1d5a, driver610.57.04,400W,
same boot04dc0087-5ccc-4c46-9997-b9a92f0e5167.

The first preflight retains a completed kernel prefix, then a collector-only
duplicate utc keyword failure at stop-receipt logging, with repeated cleanup
logging failure. The corrected stop_utc/finally cleanup is followed by a full
three-method second preflight, exit0 and analysis0. No workload, numerical
oracle, timeout or metric was changed to accept outputs. This is a disclosed
executable repair within the admitted preflight allowance.

## Independent recomputation

Read authoritative TEMP/official_full/full.jsonl and independently reconstructed
per-cell throughput, linear percentiles, per-token gap and positive-gap
distributions, zero fractions, reference matches and stable process-group CPU
deltas. **630 cell fields and all36 five-block paired effects, means and nominal
t95df4 intervals agree** with the supplied analysis to floating-point precision.
Also executed the archived CPU-only analyzer against full/full.jsonl.gz:
exit0, empty stderr, byte-identical full.analysis.stdout. Decompressed archived
full JSONL equals the authoritative raw bytes; frozen driver/API source equals
the metadata-embedded executed source.

The following are arithmetic means of five process-level statistics, not
percentiles pooled across processes:

| Regime | Method | Output token/s | Client token-gap P99 ms | TTFT P99 ms | Completion P99 ms | Zero-gap fraction |
|---|---|---:|---:|---:|---:|---:|
| offered192 | kernel |10771.094|3.46775|148.995|234.638|3.119%|
| offered192 | native |11019.771|3.38985|108.378|193.724|1.982%|
| offered192 | official |11167.040|10.79498|126.672|385.353|7.982%|
| closed16 | kernel |8718.357|40.45747|4.380|122.306|83.408%|
| closed16 | native |8861.996|40.42406|3.764|121.057|83.419%|
| closed16 | official |8528.025|4.87280|29.081|175.365|2.672%|

The frozen external primaries are native minus official:

- Closed16 output token/s: block effects446.478,221.751,231.710,134.151,635.763;
  mean **+333.971**, nominal paired95% interval **[+80.480,+587.461]**.
- Offered192 client-observed per-token-gap P99: block effects
  -8.606770,-8.124434,-8.933889,-7.361823,-3.998734ms;
  mean **-7.405130ms**, interval **[-9.880985,-4.929275]ms**.

These intervals describe five block differences under nominal t assumptions.
They are not population-P99 confidence, equivalence tests, a multiplicity-adjusted
joint claim, maximum-capacity estimates or evidence of host isolation.
Offered192 delivered native-minus-official throughput is -147.269token/s,
interval[-390.632,+96.094]; the external throughput advantage is specific to
the declared closed16 regime.

Same-executor kernel minus native remains separate:

- Offered192 token-gap P99:+0.077903ms,[-0.656335,+0.812141];
  throughput:-248.677token/s,[-627.924,+130.569].
- Closed16 token-gap P99:+0.033408ms,[-0.039531,+0.106347];
  throughput:-143.638token/s,[-375.184,+87.907].

None demonstrates kernel superiority or equivalence.

## Tails and coalescing are material results

The admitted primary is a client-observed **per-token** gap, retaining zero
samples when several IDs receive one arrival stamp. It is not official
stream-output ITL and must not be relabeled as that metric in tables or claims.
The official reader timestamps read1 chunks before parsing SSE frames; multiple
frames in the same read can share a stamp. The binary reader timestamps recv
chunks. Their framing, bytes and parsing work differ.

Reconstructed all2560 measured official streams from retained frames: token
sequence and arrival stamps exactly reproduce the recorded arrays; prompt IDs,
choice index0,64 output IDs and length finish all check. Official chunks include
multiple tokens; SSE frame count is not token count. The retained zero fractions
and positive-gap distributions prevent a low percentile from obscuring this.

Closed16 resident token-gap P99 is about40.4ms despite very fast TTFT and modest
finite throughput advantage. Positive receive-gap P99 means are41.202ms kernel,
41.092ms native,4.905ms official. Approximately83.4% zero gaps in both resident
paths show strongly bursty client delivery. This is an adverse streaming result,
not a harmless plotting artifact, and is not exclusive to eBPF.

Frozen server accepted-socket paths contain no TCP_NODELAY or TCP_QUICKACK
setsockopt, while the client sets TCP_NODELAY. This is a concrete candidate
discriminator for Nagle/ACK interaction; the existing raw data lack server TCP
state, ACK traces and a controlled socket-option contrast. Therefore neither
the40ms pattern nor its source-code opportunity proves that mechanism, GPU
production delay or scheduling delay caused it. Do not silently repair this
inside the completed comparison, retroactively reinterpret its metric, or call
the old6.36ms kernel-specific tail problem solved by these external results.

Mean TPOT at closed16 is1.81450/1.79067/1.56172ms for kernel/native/official;
native minus official is+0.228947ms,[+0.162170,+0.295724].
The finite throughput result therefore does not imply faster sustained token
production or smoother delivery for every latency measure. TTFT, completion
and each defined gap must remain separately visible.

## Correctness and baseline fairness

The frozen finite sequence pool was not expanded. Measured gen64 reference-set
matches out of1280 per method/regime are:

| Regime | Kernel | Native | Official |
|---|---:|---:|---:|
| offered192 |1262|1259|1250|
| closed16 |1259|1265|1277|

All mismatches remain successful, valid-length/vocabulary protocol outputs
under the predeclared numerical-agreement policy. No task-quality or identical
greedy-output claim follows. The finite reference set is not a complete oracle
for arbitrary mixed trajectories; prior qualification supports the resident
implementation, while this comparison reports agreement rather than disguising
disagreement or claiming full numerical parity.

The official competitor engages its intended optimized mechanism in all five
logs: separate EngineCore, FP16, FLASH_ATTN version2, torch.compile/AOT cache,
FULL_AND_PIECEWISE CUDA graphs, chunked prefill, default prefix cache enabled,
default max context32768 and capacity up to512 capture size. Reported KV cache
capacity is2374096 tokens. The actual CLI does not impose resident16 capacity,
disable compilation/caching, force eager mode or apply host tuning. The
capture-only multiprocessing=0 variable is removed from the official child.
Missing/invalid API key checks return401 in each process.

Logs contain a chat-template warmup warning/traceback because token-only mode
skips tokenizer initialization. The actual token-ID endpoint succeeds for all
requests, so this is not an avoidable measured API failure counted as a win.
The global generation-config warning also appears, but installed token endpoint
source uses request SamplingParams and only defaults omitted max_tokens here;
actual requests explicitly supply64,temperature0,ignore_eos and detokenizeFalse.
Do not infer a repetition-penalty mismatch merely from the generic warning.

Actual prefix-cache hit statistics are absent from these short logs. Enabled
configuration is established; actual hit rate is **unknown**, not assumed zero.
Four repeated short prompts, compiled/cache initialization, eight gen1 warmups,
fixed gen64 budget and the two regime orders define a warm finite workload,
not cold-cache or sustained steady state. Official scheduler, capacity, cache,
compute trajectories and JSON/SSE framing differ from resident. The valid
external conclusion is whole-service positioning; it cannot attribute a gain
to eBPF. The efficient same-compute native path independently prevents that
attribution.

## CPU, interference and cleanup

Independent CPU accounting checks all30 before/after process-group PID sets,
same /proc/stat start times and group identity, monotonic per-process POSIX
clock deltas, and exact equality with recorded sums. Official includes its API
parent, resource tracker and EngineCore; resident has one executor process.
Mean owned-group CPU ms/attempt is:

| Regime | Kernel | Native | Official |
|---|---:|---:|---:|
| offered192 |0.895807|0.453231|8.936414|
| closed16 |0.393422|0.274547|10.130406|

Kernel-minus-native owned CPU is **higher** here: offered192+0.442575ms,
interval[+0.267646,+0.617504]; closed16+0.118876ms,
[+0.104885,+0.132866]. Neither these counters nor official-process savings
measure complete CPU cost: io-wq/softirq/BPF, other TCP work and clients are
outside the attributed group. This is not the full-resource experiment.

Ready snapshots show host load averages roughly22-27 on24 logical CPUs.
Scheduled-origin latency and client lag remain in raw/analysis; the offered
schedule does not guarantee actual arrivals on time. Pairing and alternating
order help but do not isolate host interference. No foreign workload was
stopped; no clean-host or production-SLO conclusion is warranted.

All ten resident executors exit0, admitted=retired=520, max_active16,
graph_error0, GPU trace_overflows0. Kernel ring drains check with accepted=closed,
pending/reserved/dropped/overflow/error0 and matched SQ/CQ heads/tails.
**Legacy admission trace_overflow=392 occurs in every kernel process** because
its128-entry sampling buffer is exceeded. This is distinct from ring overflow
and GPU trace overflow. Request timings/counts use complete client records;
no complete internal per-request timing claim uses that truncated legacy trace.

All fifteen parent stop receipts exit0, outer forced=false, remaining empty;
all five detach receipts exit0. This does **not** mean graceful official child
shutdown: every official log explicitly reports its own forced EngineCore kill
and a one-semaphore resource-tracker warning. These occur after both completed
cells, remain preserved and do not invalidate the measured timing windows.

At review observation, none of the recorded parent/group PIDs remains;
nvidia-smi compute-apps is empty, no bpfusion pins remain, and neither benchmark
port39403/39404 is listening in /proc/net/tcp or tcp6. These support bounded
cleanup, not a general assertion that every unrelated Workspace process or
all possible OS resources have been audited. No extra experiment, code change,
baseline or re-review is required to publish this valid bounded result.

## Post-review accounting clarification,2026-10-16
Subsequent real remote preflight verifies an io-wq worker with the server's
TGID, consistent with Linux7.3 create_io_thread(CLONE_THREAD). Its execution
is included in the process/group CPU clock. The earlier sentence listing io-wq
among work outside that group was too broad; do not add its CPU a second time.
This correction changes no recorded timing/CPU arithmetic or review verdict.
Other softirq/IRQ/TCP work remains incompletely attributable. See the
[socket/thread resource receipt](../sustained_remote_resources_20261016/preflight.md).
