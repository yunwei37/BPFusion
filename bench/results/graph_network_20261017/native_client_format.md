# Native client log format1

Each worker retains original little-endian records in .records.bin:
<6Q4I256s (320bytes):globalindex,scheduled/begin/sent/complete/end CLOCK_MONOTONIC
nanoseconds,pattern,status,captured byte count,errno,256-byte reply buffer.
Only the first captured-byte-count bytes are observed payload; remaining zeros
are padding. status0success,1scheduled deadline,2connect,3short EOF,4receive,
5send,6numeric mismatch. Incremental recv preserves actual partial data even
on timeout. No JSON encoding or Python request callback runs on this path.

.timers.bin is <3Q (24bytes):observed time,planned1ms timer tick,lag.
All missed ticks are retained. .ready.json and .terminal.json retain actual
worker PID/affinity/connections/counts/CPU. stderr is original. Main JSONL has
coordinator/source/worker metadata and terminal; it references the exact binary
schedule and input/independent-oracle files consumed by native workers.

Python coordinator generates the same sorted uniform fixed-count schedules,
seeds,16patterns,280/256-byte frames,eight workers and128connections as before.
Epoch publication stays atomic; requests cannot begin early; deadline stays
30s from original schedule. Complete/partial/failed/unsent attempts retain
one fixed record each. Numeric validation is inline and independently repeated
offline. Workload/server/metric/acceptance criteria do not change.

A post-stop lossless archive transfers original files once and stores each
as gzip where appropriate. Analysis reads format1 directly; it does not need
a generated hot-path JSON replica. Original Python prefixes remain readable
by the same analysis tool and are separate from the fresh screen_cpp matrix.
Static Linux x86-64 client is built only in the owning Workspace through normal
Make,then copied to the bounded remote Job; no client Pod build/dev environment.
