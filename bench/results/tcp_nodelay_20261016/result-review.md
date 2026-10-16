# Fresh result review: persistent TCP delivery stalls

2026-10-16 UTC. Independent RESULT REVIEW under research-experiment-design,
separate from plan review. Reviewed the approved plan/review, frozen client and
analysis, source/build records, diagnostic raw TCP headers/TCP_INFO, all full-run
raw observations, and terminal/cleanup receipts. Performed CPU-only
recomputation; no GPU/load experiment, source change or Git publication.

## Separate judgments

- **Run status: valid.** The planned diagnostic and full timing matrix are
  terminal and interpretable within their stated scope. Ordinary default8
  adoption qualification is a separate, concurrently running dependency and
  is not represented here as already complete.
- **Tested hypothesis: supported.** Server Nagle/delayed-ACK interaction is a
  material cause of the persistent16 delivery stall. The single listener
  TCP_NODELAY intervention removes the observed queued-data hold and strongly
  reduces the declared client token-gap P99 on both transports.
- **Research value: supporting.** This is a consequential shared transport
  correction, not evidence of an additional eBPF contribution.
- **Paper impact: mechanism or workload boundary.** This establishes a cause
  and remedy for the reproducible shared persistent-connection stall. It
  neither explains the historical unreproduced kernel-specific6.36ms
  difference nor constitutes a direct thesis challenge.
- **Next paper decision:** select the minimal mixed-server NODELAY correction
  after its declared ordinary protocol/cancellation qualification passes;
  retain the corrected efficient native comparator. Continue the requested
  full-resource and sustained-remote work. No current eBPF speedup claim is
  justified.

## Completion, provenance and fairness

I independently counted20 executors,40 cells,10240 measured requests,655360
returned tokens and160 excluded gen1 warmups. Every measured request succeeds;
there are no timeouts, partial-error outputs, validation-error exclusions or
replacement blocks. Every executor exits0 without forced kill or remaining
group members. All10 kernel detach operations exit0. At this review's live
observation all20 recorded full-run server PIDs are absent and no BPFusion pins
remain; original Coder PID1/start8626595 and PID10909/start8662925 persist.
Later qualification owns its own lifecycle and is outside those receipts.

Compressed full raw bytes equal the authoritative TEMP raw file. Running the
archived full analyzer against the archive returns0 and reproduces its
analysis output byte for byte. Diagnostic analysis also reproduces all
semantics: only the input filename gains .gz when replaying the archive.

Full metadata source_commit is2645165f0406186d000c51360422ec53573a034f.
All frozen relevant source files still equal that source; Git shows no change
to those files from45f0ec2. Candidate source differs only by netinet/tcp.h and
a checked listener TCP_NODELAY before listen. Build relocation adds the
original executor include search directory and changes the source pathname;
normal compile flags, model revision7ae55760, FP16, CUDA computation,
transport headers,16-slot capacity, client and timeout remain matched.
Both full paths use ordinary binaries without BF_TRACE. Traced libraries
are built for separate qualification, not silently used in the timing matrix.

The original efficient timed-epoll native path engages its intended mechanism,
and each transport's old build is a valid component intervention control.
Official vLLM is not in this run; its previous result remains a dated,
different whole-service reference. A post-fix versus old-official table would
not be a newly matched official comparison.

Frozen per-block offered schedules match across all four conditions. The
five-block order repeats the first Williams sequence and is not perfectly
balanced across all five blocks; it is transparent and unchanged. The two
nominal primary intervals are not multiplicity-adjusted, and describe paired
variation of block-level P99 statistics, not a population quantile interval.

## Independent primary and critical secondary recomputation

I recomputed linear token-gap P99 directly from request arrival_ns,
throughput from cell begin/end and all returned tokens, TTFT/completion from
raw timestamps, and high-resolution process-group CPU differences. CPU
process identities, including start ticks, agree before/after each cell.

The table gives means of the five process-level statistics; it is not a
pooled global percentile.

| Persistent16 | Kernel before | Kernel after | Native before | Native after |
| --- | ---: | ---: | ---: | ---: |
| Client token-gap P99 ms |40.459794|2.287216|40.466041|2.713494|
| Positive receive-gap P99 ms |41.241182|2.289202|41.207206|2.728220|
| Coalesced-token zero fraction |0.833929|0.003336|0.834400|0.013294|
| Output token/s |8841.740|11260.440|8780.373|11358.343|
| Completion P99 ms |120.843583|93.225301|122.158931|91.535581|
| Process-group CPU ms/attempt |0.387381|0.519097|0.274653|0.391687|

Candidate-minus-before primary effects are:

- Kernel **−38.172577ms**, nominal t95 **[−38.550854,−37.794300]**.
- Native **−37.752547ms**, nominal t95 **[−38.667032,−36.838063]**.

All five within-path paired primary effects are negative. This is a large
bounded streaming benefit, not a conclusion drawn from a small favorable
point estimate. Companion zero fractions/positive gaps show that the change
removes long burst holds rather than merely manipulating zero token gaps.

Persistent throughput improves by **2418.700 token/s
[2059.492,2777.908]** kernel and **2577.970
[2008.595,3147.345]** native. Completion P99 falls by
**27.618282ms [23.771157,31.465406]** kernel and
**30.623349ms [26.682945,34.563754]** native, expressed here as positive
reduction magnitudes. TTFT effects cross zero.

The improvement has an adverse CPU cost: candidate-minus-before
process-group CPU increases **0.131716ms/attempt
[0.097310,0.166122]** kernel and **0.117034
[0.097963,0.136105]** native. Shorter wall time and more immediate small-packet
delivery can change CPU per attempt; this is not a free CPU improvement and
no total host CPU, energy or IRQ attribution is available in this matrix.

Offered192 gives no established NODELAY throughput or token-gap benefit:
kernel gap effect **−0.432030ms [−1.133188,+0.269128]** and native
**+0.053941ms [−0.786271,+0.894152]**. Both throughput intervals cross
zero. Native_before block3 retains client scheduling-lag P99
**133.515557ms**, maximum139.678808ms. Its large adverse TTFT/completion
exposure is not a clean server-option effect; that block must remain and
must not be dropped or replaced. All offered schedules and lag observations
remain available. These short256-request cells do not establish sustained
load stability or a remote SLO.

After the correction, kernel-minus-native persistent gap P99 is
**−0.426277ms [−1.333559,+0.481004]**, and throughput is
**−97.903 token/s [−303.692,+107.886]**. Offered192 counterparts are
**−0.075657ms [−1.016694,+0.865380]** and
**−145.462 token/s [−512.881,+221.958]**.
There is still no eBPF speedup or equivalence result.
Kernel process-group CPU remains higher:
**+0.127410ms/attempt [0.101754,0.153066]** persistent and
**+0.459753 [0.262323,0.657184]** offered.

## Mechanism evidence and competing explanations

This is stronger than a forty-millisecond packet-gap correlation. All16 own
accepted sockets in each diagnostic show NODELAY0 before and1 after; CORK0
throughout. TCP_INFO returns256 bytes and raw field bytes reproduce the
decoded notsent/bytes_sent values. The fixed kernel ABI layout is consistent
with the plan's version-specific source. Before,1214 kernel and1341 native
samples show positive notsent_bytes with unacked data. Constant-bytes_sent
sampled holds reach at least40.484560ms and38.057984ms respectively.
After, no such sampled queue/unacked hold is observed. Absence at a finite
sampling cadence is not proof that every shorter hold disappears.

Concrete kernel accepted FD69/peer48924 has bytes_sent636 and one unacked
packet while queued bytes grow4 to36 across40.484560ms. Packet sequence
1002651675 carries4 bytes; the peer's pure ACK covers1002651679
**41.564492ms** later; the next36-byte server packet follows
**12.502 microseconds** after that ACK. The covering ACK carries zero payload
and no later request, so it is not an ACK piggybacked on client work.
For each before diagnostic, the16 descriptive ACK-delay episodes exceeding
30ms are likewise pure ACKs. The30ms description is not a primary cutoff
or a selected success criterion.

No diagnostic TCP_INFO sample reports retransmission or a zero send window.
The example has cwnd10, one unacked packet and positive send window;
retransmission or exhausted congestion/receive windows do not explain it.
Positive queued bytes with unchanged bytes_sent show that transport data
already existed, ruling out solely late GPU production for that episode.
The isolated option intervention plus matched performance effects support
Nagle/delayed-ACK as a material cause. They do not say all remaining client
latency is TCP delay or partition every delay into GPU/softirq/io-wq/TX.

Capture uses own-port headers, no payload, and actual packets all have
PACKET_HOST, so outgoing/incoming duplicates are not counted twice.
Packet drop counters are0, while kernel packet counters exceed persisted
packets by5 kernel-before and1 kernel-after at capture boundaries. This
precludes a claim of complete boundary coverage. Poll medians are about
1.28–1.41ms, with maxima3.35–7.46ms depending on condition. Kernel packet
realtime and TCP_INFO monotonic observations are distinct clocks;
the packet ACK/send intervals use one clock and sampled hold intervals
use the other. No exact cross-clock stage sum is supported.

The own-socket observer duplicates server FDs and retains them until stop;
this can extend socket lifetime and its threads perturb scheduling.
It is confined to diagnostic preflight. The uninstrumented full matrix
has observers disabled and its20 normal shutdowns are independently clean.
The mechanism is therefore supported in an instrumented observation and
the performance effect in a separate uninstrumented matched acquisition,
rather than diagnostic timings being presented as the primary measurement.

## Correctness and scope limits

The unchanged pre-observation finite reference pool matches10137/10240
outputs. By persistent/offered respectively:
kernel_before1271/1274, kernel_after1252/1272,
native_before1260/1256, native_after1278/1274, each denominator1280.
I recomputed membership against the frozen pool; the outputs are not added
to it after observation. All outputs still have64 valid vocabulary IDs,
expected inputs, ordered arrivals and valid framed binary replies.
Finite-set disagreements are preserved; no universal exact numerical parity
or model-quality claim follows from this timing run. Default8 independent
trajectory replay/cancellation checks remain the explicit adoption dependency.

Each kernel full-run legacy128-entry sample truncates392 of520 entries.
The separate model trace_overflows is0; neither number means a complete
per-request stage trace exists. Ring accepted/closed counts agree, pending,
error, reserved, dropped and overflow are0, and SQ/CQ cursors drain.
Do not conflate legacy diagnostic truncation with corrupt replies, or use
those128 entries to allocate all request-tail causes.

Shared host exposure is substantial (ready load averages roughly18.85–27.71)
and workloads are short, local and finite. Source and metrics are valid for
the supporting question, not isolated-host or sustained-remote inference.
The largest old6.36ms eBPF-specific discrepancy remains unreproduced;
this shared transport repair cannot retrospectively divide or erase it.
No additional source changes, generic backend guarantees, total-resource
claims or official-baseline wins are validated by this report.
