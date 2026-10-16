# Streaming-tail investigation (in progress)

User priority on2026-10-16: diagnose Qwen192 adverse inter-token P99,
repair a demonstrated cause and retest matched conditions before complete
resource/remote-load experiments. Then qualify ordinary mixed scheduling and
a real reusable backend; add an official vLLM server whole-service reference.

[Plan](plan.md) and [fresh plan review](plan-review.md) admit the staged
diagnostic. No root cause, repair or new speedup has been established yet.
The original f56d0ee serving sources remain selected.

## First completed step: existing-data discriminator
Run from the repository root:

    python3 bench/results/tail_path_20261016/existing_tail.py

[Script](existing_tail.py), [all per-block results](existing_tail.json).
This post-hoc reanalysis retains every Qwen192 mixed request from0065.
It reproduces all ten block ITLP99 values. The kernel's slowest1% intervals
include final-token gaps in12..50 of162 cases/block (7.4%..30.9%).
Interior gaps therefore account for most of that tail. Final retirement
ordering is a candidate contributor, not a complete explanation.

Zero-arrival-gap fractions are32.45%..52.33% for loop and19.89%..36.35%
for native. These measure recv-observed token coalescing; they do not isolate
TCP buffering, GPU pauses, kernel queueing or client scheduling.
Native also retains rare229.86/280.42ms maxima; an improved P99 does not erase
these larger outliers. No new GPU experiment or causal conclusion is implied.

## Default8 and timeline preflight (completed dependencies)
[Default8 protocol archive](default8/README.md):2560 outcomes/93504 exact
tokens across both models/transports, including1036 intended rejects.
Ordinary cancellation/source adoption remain pending.
[Timeline preflight](preflight/):both paths32 measured gen64 attempts plus8
gen1 warmups each, total80 replies/4112 tokens, exact dual replays pass.
Original CPU analysis fails on ftrace syscall print syntax; the narrow parser
repair reruns the same data successfully. Failure and fixed outputs remain.
This is preflight, not a confirmed performance effect or root cause.
The full two-pair timeline diagnostic is now running with additional client
TID/recvfrom observation, as documented in preflight-deviations.md.
The host exposure snapshots record another Pod's busy processes; no other
workload is paused and no ownership or causal claim follows from the snapshot.

## Complete timestamp diagnostic (awaiting independent result review)
[Result and boundaries](diagnostic-result.md),[full compressed raw](full/),
[retained failed capture](failed_full_trace_overrun/),[capture repair](full-trace-repair.md).
Four full executors/1056 replies65568 tokens pass exact dual replays and coverage.
Large observed waits are after production, including kernel submit-thread
runnable delay and client delivery/recording delay. No fix or speedup selected.
Gzip stores the original raw text losslessly; no runtime/build/weights enter Git.
Independent CPU replay (paths without.gz automatically discover compressed text):

    python3 analyze_timeline.py full/tail_full.jsonl
    python3 scheduler_attribution.py full/tail_full.jsonl

Replay writes the derived per-token/gap reports beside its input. Original
results are compressed; compare uncompressed JSON/text, not gzip timestamps.
Source snapshots preserve actual collection and earlier parser versions.

## Ordinary8 and concrete next intervention
All4 ordinary default8 lifecycle cases pass;[wire,syscall,freeze and cancellation
records](ordinary_before/README.md) distinguish complete answers from observed
prefixes and unobserved cancellations. This is engineering acceptance, not
a latency/throughput result or source promotion.
[Independent diagnostic review](diagnostic-result-review.md) finds the
two-pair timestamp run valid/supporting, with explicit signed-CQ/clock/sample
limits. The unchanged complete throughput/latency objective remains open.

[Connection-progress association](connection_progress.json) motivates the
[small close-scan candidate](candidate-close-guard.diff); recompute with:

    python3 connection_progress.py full/tail_full.jsonl

The same[plan review](plan-review.md) admits the candidate's exact frozen
before/fixed/native confirmation after safety/preflight. It does not establish
a causal improvement. Candidate ordinary8/16 builds pass; runtime regressions
are in progress. No serving source/default has changed.
