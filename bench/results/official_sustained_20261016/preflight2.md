# Second actual preflight: protocol passed, single-client uncertainty remains

All3x128 requests succeed,24576 output tokens,24 excluded gen1 warmups;
K/N/O frozen pool flags0/1/4 retained. Archive CPU replay exactly matches
acquisition; all terminals/drain/auth checks pass. Common uvloop0.23.0 lowers
client lagP99 to4.623/3.508/26.992ms; CPUms/attempt5.426/5.203/5.227.
CPU fractions0.893/0.850/0.872 reflect different drain durations, not proof
of greater official CPU demand. Last due0.619764s, last starts
0.620718/0.620255/0.626699s. No full performance conclusion.

At192 requests/s,~5.2ms clientCPU/attempt approaches one core; protocol-specific
arrival lag remains a risk. Before full collection, use the same two-process
client layout for every condition, split original request indices even/odd
against one future monotonic epoch. Preserve both raw worker files and all
outcomes. No changed server/parser/oracle/offsets/primary or concurrency cap.
This is a necessary common client repair, not a favorable server-prefix rerun.
single_uvloop_client/ preserves this actual initial one-process source.

Official shutdown ERROR/EngineDeadError occurs only after completed requests,
SIGTERM/abort teardown and official process-manager force killing EngineCore.
Parent exits0, no children/GPU apps/pins/cores remain. Retain these logs and
the semaphore warning; do not call teardown fully graceful.
Client Job is held only for the immediate third preflight/full benchmark.
