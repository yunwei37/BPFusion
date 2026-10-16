# First actual application qualification: passed

2026-10-16 UTC. [Plan/review](plan-review.md), source/ and compiled_controls.json
precede actual runtime. Qualification attempt1 succeeds without runtime source
repair: all4 protocol/ordinary stages exit0 and pass their existing checks.

At default8, Qwen and Smol each640 protocol requests and23376 exact token IDs,
259 expected rejections, actual tensor batches1..8, no padded query tokens.
Each actual current trajectory passes captured graph/KV and fresh upstream
attention-metadata replay/client joins; GPU graph/trace overflow and ring/drop errors0.
The bounded network reply-record buffer retains128 of640 request records per
model (trace_count=640, trace_overflow=512); this truncation is retained and is
not GPU trace overflow. It prevents complete per-reply transport tracing, not
the complete client token joins or two GPU trajectory replays.
Kernel-owned BPF struct_ops really attaches and serves TCP/HTTP: verifier-only
acceptance is no longer the strongest evidence. Strace retains no steady
userspace accept/recv/send worker and the existing single serving enter check.

Ordinary builds each execute the unchanged144-frame lifecycle fixture:
78accepted/78closed connections,88admitted/completed,58aborts,
56queued at stop cleaned (88+56=144), no pending/reserved/error/drop/overflow,
balanced SQ/CQ and no remaining pins. All observable checked output prefixes
match the fixed pool; cancelled outputs remain explicitly unobserved.
These cover idle/reuse/reject/backlog/partial-output stop/drain without GPU trace.

All originals are in qualification/, with lossless gzip where appropriate.
Unchanged source-native protocol analysis is replayed from archive bytes
decompressed only to OS TEMP; both stdout byte-match acquisition and stderr
is empty. analyze.py is the unchanged required verify_mixed dependency.
Original Workspace/PIDs/WIP remain; qualification leaves no GPU app/pins.
The declared remote-client Job is held for the immediately following matrix.

This is dependency acceptance, not a throughput/tail result or general protocol/
model/plugin guarantee. The untraced16-bank remote comparison still needs its
fixed3-condition preflight/full15cells, review, owned-client cleanup and source
decision. No production code/default/host setting is adopted.
