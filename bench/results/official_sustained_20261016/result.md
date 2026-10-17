# Sustained remote official vLLM comparison

2026-10-17 UTC. Completed five paired process blocks /15 ordinary cells.
The fixed N-minus-O delivered-token throughput effect is -599.430021
[-623.509431,-575.350611] tokens/s: resident native delivers about4.90% less
at this offered load. Official vLLM also has much lower completion/TTFT P99.
The current resident design therefore does not keep up with this optimized
official reference in the tested whole-service workload. Neither transport
establishes a general faster-server claim.

The same-executor K-minus-N effect is -0.003212 [-6.499599,6.493175] tokens/s,
with completionP99 -9.929469 [-64.178327,44.319389]ms. Crossing0 establishes
neither superiority nor equivalence. K's lower mean TPOT is a secondary local
observation; it cannot replace the fixed primary or establish a throughput win.

## Execution and reproducibility

[Reviewed plan](plan.md), [acquisition/deviations](acquisition.md),
[all ordinary raw and analysis](official_remote_full_retry2/),
[analysis source](official_remote_analysis.py), [full archive replay](full_archive_replay.json),
[resource ledger](resource_context.jsonl), [fresh result review](result-review.md).
Frozen serving/client/analysis input main8d565c7fbdfb8ce87835cd86676d5ad294db2c51.
Later8e88d46/4309883 publish completed raw and repair post-serving transfer only;
they do not change request injection, GPU code, server settings or metrics.
No runtime/client change or measured-cell replacement during retry2.

Same RTX5090/Qwen2.5-0.5B-Instruct revision7ae557604adf67be50417f59c2c2f167def9a775,
FP16, gen64, temperature0/ignoreEOS, four frozen prompts of5,8,5,2 token IDs.
192 requests/s for60s plus full drain,11520 requests/cell; five seeded identical
arrival schedules reused across K/N/O, process order fixed in plan.
172800/172800 successful measured requests,11059200 tokens,0 failures/timeouts/
invalid outcomes/close errors/partial outputs.120 checked gen1 warmups excluded.
All original worker rows, common future epochs, original indices, terminal exits,
resource brackets and server lifecycle receipts remain in gzip JSONL.

K is unselected0077 kernel-owned BPF TCP network; N is efficient C++epoll with
the same resident16-slot upstream-vLLM GPU computation. O is official vLLM0.31.0
tokens-only JSON/SSE server, normal FLASH_ATTN/compilation/CUDAgraphs/chunked
prefill/prefixcache/default capacity. Its actual non-default args are only
model/tokens-only/dtype/host/port. Source-native command is in plan and every
server-start receipt. No max-sequence/token/memory/context/eager tuning or
CPU affinity. Normal32768 context and multi-million-token KV allocation differ
from resident16. Repeated prompts are short; sampled prefix hits remain0%.
Missing/invalid API auth401 controls pass; the ephemeral key is never archived.

Reproduce acquisition in the owning environment using
run_official_remote_matrix.ps1 -ClientPod POD -ServerIP IP, with the actual
runtime/build/model paths recorded in scripts/environment. Offline replay:
python3 official_remote_analysis.py official_remote_full_retry2
and python3 resource_context.py official_remote_full_retry2.
Original analysis and independent archived-gzip replay must match byte-for-byte.
GPU is not needed for analysis. No partial prefix contributes to these numbers.

## Complete results

| Metric (mean of five cell summaries) | K: BPF network | N: native epoll | O: official vLLM |
|---|---:|---:|---:|
| Delivered successful output tokens/s | 11645.240383 | 11645.243595 | 12244.673615 |
| Connect-origin TTFT P99, ms | 3217.459093 | 3229.029330 | 362.924899 |
| Connect-origin completion P99, ms | 3304.045033 | 3313.974502 | 610.729840 |
| Scheduled-origin completion P99, ms | 3304.090344 | 3314.184599 | 615.142820 |
| TPOT mean, ms | 1.357705 | 1.361343 | 2.790111 |
| Client per-token receive-gap P99, ms | 3.589142 | 4.651052 | 18.742483 |
| Client arrival lag P99, ms | 1.403716 | 2.234435 | 14.132452 |
| Owned service-group CPU, ms/attempt | 0.834701 | 0.812080 | 8.544668 |
| Remote client CPU, ms/attempt | 10.205948 | 9.766258 | 12.332928 |
| Workspace cgroup CPU, ms/attempt | 1.244097 | 1.216383 | 8.890619 |
| Shared GPU energy, J/attempt | 1.737697 | 1.727752 | 1.284943 |
| Zero receive-gap fraction | 0.051767 | 0.109715 | 0.285484 |


Dots in the [PNG](official_remote_full_retry2/official_remote_comparison.png)
and [PDF](official_remote_full_retry2/official_remote_comparison.pdf) are five
cell values; gray lines connect paired blocks and short bars are arithmetic
means, not confidence intervals. These are means of per-cell quantiles, not a
pooled requestP99. All69 paired effects, full P50/P95/P99/means and
scheduled/connect-origin rows are in analysis.stdout.

| Contrast | Metric | Signed mean | Nominal paired t95 |
|---|---|---:|---|
| native minus official | connect_completion_ms_p99 | 2703.244661 | [2315.942202, 3090.547121] |
| native minus official | owned_group_cpu_ms_per_attempt | -7.732588 | [-7.86681, -7.598366] |
| native minus official | output_tokens_per_s (fixed primary) | -599.430021 | [-623.509431, -575.350611] |
| native minus official | client_token_gap_ms_p99 | -14.091431 | [-22.11515, -6.067712] |
| native minus official | connect_ttft_ms_p99 | 2866.104432 | [2559.758054, 3172.450809] |
| native minus official | tpot_ms_mean | -1.428768 | [-1.924446, -0.933089] |
| candidate minus native | connect_completion_ms_p99 | -9.929469 | [-64.178327, 44.319389] |
| candidate minus native | owned_group_cpu_ms_per_attempt | 0.022621 | [-0.056175, 0.101417] |
| candidate minus native | output_tokens_per_s | -0.003212 | [-6.499599, 6.493175] |
| candidate minus native | client_token_gap_ms_p99 | -1.061911 | [-2.196733, 0.072912] |
| candidate minus native | connect_ttft_ms_p99 | -11.570237 | [-62.316099, 39.175624] |
| candidate minus native | tpot_ms_mean | -0.003639 | [-0.006788, -0.000489] |
| candidate minus official | connect_completion_ms_p99 | 2693.315192 | [2343.775119, 3042.855266] |
| candidate minus official | owned_group_cpu_ms_per_attempt | -7.709967 | [-7.865918, -7.554016] |
| candidate minus official | output_tokens_per_s | -599.433233 | [-622.958894, -575.907572] |
| candidate minus official | client_token_gap_ms_p99 | -15.153342 | [-22.594364, -7.712319] |
| candidate minus official | connect_ttft_ms_p99 | 2854.534194 | [2580.033554, 3129.034834] |
| candidate minus official | tpot_ms_mean | -1.432406 | [-1.925321, -0.939492] |


## Client fairness, correctness and adverse evidence

All three clients use four unrestricted OS workers, common uvloop0.23.0,
identical original offsets/indices and no application concurrency cap. Official
uses aiohttp3.14.5 and raw SSE payloads; binary uses its existing request branch.
Official connect-origin includes HTTP setup; it is not measured send-done.
Binary connect/drain/read each use60s I/O bounds; official connect/socket-read
have60s bounds with default small-body write handling and no separate write
timeout. Neither uses total-deadline censorship. Official output cannot be
attributed to eBPF: API/serialization/scheduler/KV/capacity differ.

Client lagP99 values by block (ms): K1.475/1.349/1.400/1.347/1.447;
N3.685/1.385/1.360/1.514/3.229;
O4.475/3.359/41.992/16.995/3.841. Official residual client stalls remain
material to receive-gap/TTFT tails; the repaired client is not an ideal
instantaneous injector. All11520 attempts/cell still use their fixed original
scheduled origins, and scheduled-origin completionP99 preserves the large
external difference. No baseline failure is converted into a proposed-method
win. This measures delivered service under the recorded client, not maximum
official capacity or a protocol-independent server/GPU latency.

Client receive-gap P99 assigns every token its receive-chunk timestamp,
including zero/coalesced stamps (table); it is not official per-stream-output
ITL, GPU decode latency or evidence that official's model kernels are slower.
Official's worse receive gaps/mean TPOT coexist with much better TTFT/completion
and throughput. Different batching/streaming/client scheduling are competing
explanations; this run does not isolate their shares.

Frozen reference-pool disagreement flags: K222,N462,O1061 (1745 total),
all retained without exclusions or expanding the pool. Prompt, vocabulary,
count, finish reason and DONE checks pass; all3436757 retained official raw SSE data
payloads is independently decoded to reproduce prompt/finish/token IDs/arrival
stamps. The pool is finite; these flags mean full ordinary exact trajectory
parity is unproven. Prior two-model default8 dual graph replay is finite support,
not exactness of all untraced16-slot paths or arbitrary models.

K GPU dispatch errors/trace_overflows are0 and model admitted=retired=11528
including warmups. Network error/pending/reserved/drop/overflow are0, accepted=
closed and SQ/CQ balance. Network reply-record capacity is128: each cell
trace_count11528/trace_overflow11400, separate from GPU trace_overflows0.
Do not call the whole acquisition trace-loss-free.

## Resource accounting and mechanism limits

Owned service process-group CPU includes charged kernel/io-wq time and all
official child TGIDs; it is stable across each measured observer bracket.
O's larger CPU includes its API/scheduler/EngineCore work, so the roughly
tenfold service-group difference is a whole-system design/protocol difference,
not an eBPF saving. Client CPU is recorded separately. Observer/control and
post-drain merge fall within the broad resource bracket; throughput timing
instead runs common epoch through last original request close.

The resource ledger separates group user/system tick views, stable primary
threads' schedstat/runtime/runnable wait, visible io-wq and kernel workers,
shared host softirq and GPU counters. These views overlap and never add.
Primary-thread views omit child-TGID threads and churn; invisible io-wq is
unknown, not zero. No visible kernel worker does not imply no kernel work.
Runnable wait is not request critical-path time. Model dispatch/admission/send
counts measure work, not per-stage delay. Foreign host CPU work remained
active; no exclusive total CPU, softirq or energy reduction is established.
Shared GPU energy is lower for O here, adverse to a general resource win.

The resident paths accumulate a larger queue while delivering~11645 below the
offered12288 outputtokens/s; O delivers~12245 and drains sooner. Their
completion-tail difference appears mostly before the first token. This is
consistent with backlog/capacity/scheduling effects, but it is not an isolated
causal breakdown. Old6.36ms remains unreproduced/unallocated; no sum of
unrelated stageP99s or new receive-gap result repairs that historical number.

| Existing raw resource subset (mean ms/attempt) | K | N | O |
|---|---:|---:|---:|
| Group user tick time | 0.066146 | 0.301736 | 7.799306 |
| Group system tick time | 0.768403 | 0.510590 | 0.745486 |
| Shared host softirq, unattributed | 1.256597 | 1.083333 | 1.225347 |

All15 cells record no visible io-wq or kernel-worker thread in the Workspace
PID namespace. This is missing coverage, not zero cost; TGID system accounting
and shared host softirq remain. Stable primary thread views have133--134
threads for K,133 for N,53 for O; O's child TGID threads are not enumerated by
that subset. User/system tick precision100Hz differs from group CPU-clock ns.

## Preserved failures and repairs

Three real preflights and both incomplete sustained prefixes remain separate.
The two-worker first full block and four-worker retry1 each complete34560
requests, but official client lagP99~417/~209ms makes them unsuitable for
server ranking. No primary-prefix comparison is selected or mixed into retry2.

Client-only diagnosis finds395--473ms default generation2 GC pauses covering
89.37% of the worst1% task-start delay time. Replacing retained decoded SSE
object trees with lossless raw payload text reduces instrumented lagP99
211.219ms to3.257ms, maximum GC472.670ms to48.791ms under identical default GC,
same schedule/parser/oracle and durable logging. Both diagnostic controls and
raw frame reconstructions are preserved under client_diagnosis/. They are
dependency repairs, not server speedups or extra preflights. Ordinary retry2
contains no GC timing callback.

Post-serving whole-file WebSocket transfer failed; recovered originals use
1MiB chunks. After window8, SSH acknowledgment loss replayed an already-written
chunk; fixed-offset verified pwrite makes retries harmless, as actual replay
shows byte-identical5193475-byte output. All8 original cells were recovered
and the same matrix resumed at9 without remeasurement. Details and failed
receipts remain in transfer_recovery.md. Artifact-only checkpoint publication
happened with GPU absent and is documented separately.

## Decision and cleanup

Independent result review: valid completed run for recorded-client finite workload; fixed hypothesis
contradicted at this workload; research value supporting; paper impact additional
serving-objective evidence and workload/design boundary. Official is stronger
on delivered throughput and completion/TTFT tails, while resident has lower
group CPU and lower per-generation TPOT/client receive gaps. These tradeoffs
do not establish a general faster server, total resource saving, native
equivalence or novelty. Kernel candidate remains unselected.

Exact owned client Job/Pod UID deletion and actual absence, final frozen-source/
original-PID/empty-pin/empty-GPU checks and ephemeral-key removal are complete in
cleanup.json. PNG visual QA and the one fresh result review are complete;
PDF is the same-savefig vector artifact, not separately rasterized. No scientific
blocker or measured rerun is requested by result-review.md. Follow the current finite backend implementation
goal; do not repeat closed capacity/cache/wait sweeps or hand-optimize model math
merely to seek a favorable transport result.
