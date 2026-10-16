# First real preflight: executable
2026-10-16 UTC. Both normal16 paths complete128 measured requests/8192 tokens
each, plus8 excluded gen1 warmups each. All256 requests succeed with correct
shape/vocabulary/protocol. Native retains1 finite frozen-set disagreement;
kernel0. No oracle expansion. Source unchanged from7495930.

Actual creator-TID kernel cpu-clock samples: native24, kernel41; each sample
period2004008ns at requested499Hz. perf reports total lost samples0; meaningful
kernel callchains include TCP, netfilter/bridge/VXLAN and kernel/BPF loop
symbols, with unknown trampoline/userspace frames retained. This tiny
preflight does not identify the dominant full-load cost or an end-to-end gap.
Both profiler processes intentionally receive SIGINT after client drain,
flush complete data, then perf re-raises that signal (subprocess return-2).
This is a recorded intentional stop, not exit0 or a server failure.
All10 perf report/script/header/dump decode commands exit0, empty stderr.
Both servers exit0 with no pins. Archive client/resource analysis replay is
byte-identical, stderr empty. Full two60-second cells remain. No source tuning.
