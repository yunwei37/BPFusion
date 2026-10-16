# Invalid candidate acquisition: nvcc -dc source selection defect

2026-10-16 UTC, discovered when the local remote preflight still fails498/4608
with E2BIG. The private build adapter applied candidate source/include rewrites
only when argv contained -c, but nvcc compiles with -dc. Thus both8/16 mixed
GPU libraries were built from canonical old executor/io_uring_tcp.h, whereas
BPF used the candidate counters. Archived candidate_build.statuses.json exposes
the actual commands; source receipts naming private headers do not prove those
headers were compiled. This is an agent build error, not a negative effect of
the proposed local-guard implementation.

All affected mixed-source qualifications and candidate remote comparisons are
invalid for candidate acceptance. Preserve them and rerun after correcting
actual source/include selection. Both generic graph builds used unconditional
include/source rewrite and are independently valid for their changed transport
surface, but are not mixed-server acceptance. Earlier model-dispatch SASS
identity did not distinguish a transport-only build and was insufficient.

The first trace-less finite-membership failure and subsequent105-request traced
success were acquired with the old mixed GPU guard too; preserve both without
attributing either to the candidate. The claim that the traced test established
local close while global40 remained is withdrawn: its blocking EOF read did not
record queue state at the time EOF was actually received. Fix the targeted
check to obtain EOF with MSG_DONTWAIT/short polling and recheck global pending
at observed EOF. Do not change model oracle/timeouts/metrics to pass.

No canonical application source or foreign workload/session was changed.
The queued remote full matrix never started. Keep preflight raw cells marked
invalid for the declared candidate implementation. Corrected builds use a new
explicit directory, actual -dc source/include argv, and all affected engineering
checks repeat before the next real preflight. This systematic execution defect
requires rerunning comparisons, not dropping inconvenient outcomes.
