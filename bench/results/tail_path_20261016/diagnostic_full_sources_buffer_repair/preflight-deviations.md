# Diagnostic preflight notes
The first real preflight completes both40-request paths with exact replay and
no trace/ring/graph errors. Its initial CPU analysis rejects standard ftrace
sys_sendmsg enter/exit print layout, which differs from ordinary event text.
The narrow parser repair retains every line and all strict joins. CPU replay
of the same raw two paths passes; failed output and initial analyzer remain.
No GPU rerun or oracle/metric/timeout change is used to fix a text parser.

The preflight shows millisecond post-send/client residuals alongside microsecond
kernel send intervals. Full diagnostic adds existing recvfrom tracepoints and
one private trace_marker write/client to associate client host TID with its
request and distinguish blocked receive, runnable delay and post-syscall Python
delay. GPU instrumentation/model/wire/oracle/matrix stay unchanged. This is
additional diagnostic observation, not a claimed performance improvement.
Full sources are frozen separately; first preflight sources remain intact.
