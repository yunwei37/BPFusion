# Actual source and stage boundaries

Ordinary expanded build source:0074 active_wait_source_build16.stdout. Both
BF_IO_COALESCED and BF_CHAINED_DISPATCH are absent. The instrumented Makefile
preserves this, redirects only mixed .cu and its private .h dependency, and uses
-I/workspaces/repository/executor for unchanged userspace_tcp.h. All ordinary
model/BPF/shared ABI source files stay untouched. Private context structs grow;
code generation/register use can differ. This is explicitly instrumentation.

Dispatch rows0/1/2 denote launching/nonlaunching/stop iterations. Columns are
publication+retirement, admission+packing, launch API residence. A final stop
iteration may publish completed model outputs and is retained separately.
Histogram equals actual launched graph input-token counts. Outside interval
anchor is after stage counter updates but before a final stored timestamp and
CTA return; interval includes unbracketed bookkeeping/return, child model/head
and scheduling. No exact model duration or exhaustive controller partition.

Network rows0/1/2 denote had-owned-request/no-owned-request/stopping. Row1 is
not proof of inactivity: producer work and first claim can occur there. Columns:
CQ drain (including initial control reads), claim and cancellation bookkeeping,
reply preparation/submission, connection RX/reclaim/accept, timer/SQ-CQ publish/
termination checks, existing sleep. Classification uses local ownership only,
adds no mapped state probe. All ordinary branches remain; early cancel-wait
charges its CQ/post-CQ/sleep to stopping, final return charges no sleep.
Counter stores/time reads themselves are outside some brackets. Network stream
sync precedes downloading private counters, so final writes are visible.

These independent CTA times overlap. Do not sum them into wall-clock/token time,
exclusive GPU busy time, CPU cost or the old token-gap P99. Unknown causes of
observed stage residence include actual shape/history, memory/issue stalls,
scheduling and changed codegen. A later ordinary intervention needs its own
matched performance evidence before source selection.
