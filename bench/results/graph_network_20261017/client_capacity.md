# Replace the measured client hot-path bottleneck

The final-source Python prefix is retained in client_capacity_initial/:
two1000/s cells and one4000/s kernel cell,all successful application replies.
At4000/s the client uses0.961424CPU-ms/attempt (~3.846cores),with eight workers
each using~2.45CPU-s for3000requests. MonitorP992.315ms exceeds the unchanged
max(1ms,10%responseP99)=1.468ms gate. Do not call this server saturation.
The remote host is x86_64 Ryzen5 3500U,four physical/eight logical CPUs;
cpu.max is max100000,nr_throttled0. No foreign workload or CPU policy changes.

Replace Python per-request scheduling/JSON encoding with a native epoll/
timerfd worker,keeping eight workers,128connections,the exact binary frames,
input/oracles,scheduled offsets,30sdeadline and metric origins. Python remains
the coordinator and generates the same schedules/patterns; raw native
records are converted/analyzed only after timing. Log every partial read and
failed/unsent attempt. New source is validated against real backend replies
and the same timing gate,then all screening restarts under screen_cpp_* labels.
No server/GPU arithmetic change or criterion relaxation.

Native qualification:matched1000/s and4000/s kernel/native pairs complete
60000measured requests and128checked warmups,0failures,with independently
decoded original binary records/oracles/schedules. All original timer gates
pass. At4000/s kernel clientCPU .187557ms/attempt (~.750core) versus oldPython
.961424ms/attempt (~3.846cores); timerP99 .491ms versus2.315ms.
Native-server clientCPU .180065ms/attempt,timerP99 .259ms. The kernel server
still has an adverse144.800ms responseP99 versus native2.461ms in this one
screening pair; native client qualification does not fix or hide server tails.
These are exploratory cells,not confirmed transport claims.
