# Client timer repair before restarting screening

Both initial matmul/repeat1/unrestricted1000/s6s cells complete6000requests
with0failures. Kernel/native scheduled-responseP99 are3.567/3.112ms,while
timer-dispatchP99 are0.884/1.239ms. Native exceeds the preregistered1ms gate.
This is an invalid client-fairness prefix for ranking small-request servers,
not a confirmed kernel/native result. Both originals and all workers/resources
remain in client_timer_initial/. No row is excluded within a completed matrix.

The original strict asyncio/uvloop-sleep loop prevents early release but still
has millisecond timer granularity and extra short-delay wakeups. Replace only
client waiting with one ordinary Linux timerfd per worker,absolute
CLOCK_MONOTONIC deadlines and an asyncio FD callback/min-heap. No busy release,
per-request server change,library optimization,arrival/timeout/oracle/metric
change or criterion relaxation. Record every missed1ms monitor tick as before.
This dependency repair is an implementation hypothesis; the real new prefix
must show whether its dispatch lag meets the unchanged gate.

Restart screening under screen_hrtimer_* tags with the same predetermined
case/rate/order/seeds. Do not combine the old timer prefix with new source.
All code and a fresh real matched pair will be committed before continuing.
No LLM comparison is reopened; its few-ms client lag remains explicit against
hundreds/thousands-ms completion tails in0080.

## Startup publication race found and repaired

The timerfd kernel cell completes6000requests with0failures and monitorP99
0.687ms,meeting the original gate. Its responseP99 is8.399ms,P99.9 41.485ms;
retain this adverse tail. The native timerfd cell fails in worker7 before
request execution:the coordinator creates the epoch file before writing its
digits,so an existence check can read an empty string and int() raises.
This is a real startup publication race,not a timerfd/network service failure.
Other workers' actual rows and all stderr/resources remain. The incomplete
pair is archived in client_epoch_initial/,not mixed with subsequent source.

Publish the epoch through same-directory atomic rename after the file is
closed. The only change is startup coordination before the future epoch.
Restart both paths under screen_ready_* labels to keep client source identical.
The strict1ms gate and all arrival/rate/oracle/timeout/metric definitions remain.
The observed~41ms delivered outliers need investigation if they recur after
client qualification; they are not erased by this startup repair.

## Qualified repaired client

The matched screen_ready_*pair now completes12000requests with0failures,
identical timerfd/atomic-publication/client source and original offsets.
Kernel/native timer-dispatchP99 .725/.652ms pass the original1ms gate;
connection-waitP99 .676/.537ms. All32warmups per path also pass.
This validates the repair locally,not arbitrary high-rate client capacity.

Kernel scheduled-responseP99 is22.006ms versus native2.864ms,with send counts
7229for6032warm+measured requests. The network tail remains adverse after the
client repair. This pair is retained as nodelay_before/,not promoted as a
transport result. The prespecified nodelay-plan.md tests a concrete shared
TCP policy repair before the final matrix. No GPU arithmetic changes.
