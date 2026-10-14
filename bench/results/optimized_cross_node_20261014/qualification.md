# Cross-node preflight qualification

Actual g10 client10.42.6.216 to original lab Workspace10.42.1.238 completes
both Qwen paths/four cells,80 requests2096 checked tokens including16 excluded
gen1 warmups. Both actual clients and servers exit0; source-native output-set
checks and direct analyzer reconstruction pass. Candidate has one steady
io_uring_enter, no userspace serving socket calls or SQPOLL thread, separate
SQ/CQ queues drained, all reservations/pending/errors/drops0. Native accepts/
receives/sends actual requests and reports timed epoll policy; this selected
strace does not capture epoll_pwait2, so no new direct wait-syscall-count claim.

The test-local server wrapper initially omitted source-native post-detach
pin cleanup. Native bootstrap fails before model launch or client samples;
the traceback and receipt are retained. Add the existing three pin unlinks,
then run native normally. Valid candidate output is preserved; no timing,
oracle or production-source change. This is a runner repair, not an observed
candidate delivery loss or scientific performance result.

One Windows artifact-transfer command exceeded the process command-line
length before execution; chunked transfer preserves the original completed
client logs. No serving restart or row replacement follows from that observer
failure. Record future transfers using gzip/chunks.

This completes only the admitted real preflight. Its profiled traces/brief
cells are not full-run performance estimates. Full untraced comparison and
fresh result review remain pending.
