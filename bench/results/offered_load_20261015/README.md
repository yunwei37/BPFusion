# Offered-load service comparison

Complete collection is now preserved:20 executors,80 cells,20480 measured
attempts and160 warmups. Both model drivers, fixed analyses and full wrapper
exit0. These include709 failed service attempts. Independent result review
confirms valid complete negative service evidence. Owned old temporary state
is removed and all seven copied-data analyzers replay byte for byte after that
removal. This main publication is not a performance-win or full-goal-completion
claim. See result-review.md, final_restoration.json and final_replay.json.

The reviewed plan tests first-token P99 at64 requests/s for the adaptive
kernel/eBPF loop against event-driven native TCP, with the same optimized FP16
vLLM computation. Rates4/32/64/96,256 attempts per cell, five paired blocks per
model, alternating path order, rotating rate order and identical per-pair
absolute arrival schedules are fixed before collection. All failures remain
in the denominator. This is loopback token-ID HTTP and a finite traced study,
not an arbitrary-model or full-service CPU result.

## Source and evidence

- plan.md and plan-review.md: pre-observation agreement and review.
- source/: source-native client/backend/benchmark inputs.
- kernel/: actual private adaptive-wait kernel inputs, inherited from0060.
- native/: actual event-driven native baseline inputs.
- setup.py, qualification.py, preflight.py and full.py: actual commands.
- packages.json, environment.json, build/install logs: runtime provenance.
- protocol_*.jsonl, lifecycle_*/ and idle files: qualification dependencies.
- full_<model>.jsonl: measured requests/errors, schedules, counters and exits.
- full_<model>_p<block>_<mode>.*: actual logs, GPU history and independently
  replayed references, including requests not delivered to a client.
- *.analysis.stdout: fixed primary/secondary analysis.
- tail_censoring.py and *.tail_bounds.stdout: supplemental all-attempt
  identification bounds; neither changes the primary analysis nor assigns
  a timeout an exact completed latency.
- preservation_checkpoint*.json: historical partial-copy receipts.
- replay_checkpoint.json: byte-identical replay of completed copied inputs.
- host_*.json: sparse actual host/PID/boot/fault observations. These do not
  prove continuous exclusivity or absence of every possible host fault.

The ring RESULT trace_overflow is the overflow count of its bounded128-entry
reply diagnostic. Actual BF_TRACE history overflow is a different field and
must remain0 for independent model replay. Likewise ring dropped/overflow
does not include model-admission drops: page drops/llm busy track that boundary.

## Offline analysis

Run from this directory with ordinary Python3; no CUDA/runtime dependencies
are needed for these analyzers. Commands requiring a complete model file will
reject an in-progress prefix.

    python3 protocol_analysis.py protocol_qwen.jsonl
    python3 protocol_analysis.py protocol_smol.jsonl
    python3 analyze.py preflight_qwen.jsonl
    python3 analyze.py full_qwen.jsonl
    python3 analyze.py full_smol.jsonl
    python3 tail_censoring.py full_qwen.jsonl
    python3 tail_censoring.py full_smol.jsonl

Each sidecar path is derived from the supplied raw filename, so copied-data
analysis does not need the original temporary directory. Source-native GPU
replay was performed by the original backend before executor exit; a CPU
analysis replay checks the saved evidence, not a new model execution.

The primary analysis reports success-conditioned timing and an explicit
failed_request_censoring flag. Do not read a negative P99 difference as a
service win when failed attempts have been omitted from that timing sample.
The supplemental bounds include every attempt: an unknown first-token time
is at least the observed no-token duration and has no established finite
upper bound. These are descriptive finite-sample bounds, not confidence
intervals, an SLO or a new primary metric.

Model reruns use the exact recorded source/version/model revisions and normal
make entrypoints through setup.py. Captured absolute temporary paths identify
the original run; rebind those source/build paths to the rerun directory.
Keep backend arithmetic, KV precision, eight model slots and baseline
mechanism identical. A different source/configuration is a new comparison.
The original repository source remains selected after this study.

## Arrival limitation

These are actual Python-thread loopback arrivals. The largest cell scheduling-lag
P99 is19.241940ms for Qwen; Smol pair2/kernel/64req/s has107.677338ms.
Configured rates therefore do not mean ideal achieved arrivals. Original
scheduled-origin metrics and all unfavorable cells remain; millisecond tail
differences cannot be attributed exclusively to the server mechanism.
