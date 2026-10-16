# Actual normal-rule instrumentation build

2026-10-16 UTC. controller_stage_build.py exits0. Actual expanded commands,
UAPI header warnings and exit receipt are in build_records/normal16.*.
The redirected source-native Make rule preserves -dc, device-link, FP16 upstream
runtime and absolute BUILD BPF binding. No BF_IO_COALESCED/BF_CHAINED_DISPATCH.
Source/controller layout instrumentation changes are private, not adoption.

Both fusion.bpf.o and uring_loop.bpf.o instructions/relocations match selected
active_wait_sourcebuild16 after normalizing only disassembly filename headers.
The loop library embeds the actual controller_stage_build16/uring_loop.bpf.o.
Compiled loop SASS has8 globaltimer reads in dispatch and10 in io_network;
native has8 in dispatch and no network kernel. The actual timer contexts,
original NANOSLEEP and generated instruction streams are archived in
build_controls.json and compressed build_records/*.sass.txt.gz. Timer reads
remain around the intended sections; no new synchronization is added.
This is build/mechanism engagement only; real preflight must still validate
clock/count identities, complete outputs and unchanged source-native replay.

Before preflight, initial SASS inspection found that a sleep-end clock read in
a function argument could follow other argument-delta arithmetic. Explicit
end timestamp locals are now taken before stage-record argument evaluation
on sleep/nonlaunch/stop paths. This changes only observation ordering, not the
workload, policy, metric or oracle. Initial build/SASS controls are retained
with initial prefixes. Rebuild r1 must provide the actual preflight binaries;
no serving or preflight used the initial binary.

Rebuild r1 exits0. The two actual NANOSLEEP paths are followed by their end
GLOBALTIMER read (one has an emitted NOP). An initial CPU inspection asserted
literal next instruction and rejected that NOP; ignoring only NOP confirms
ordered clocks without another build or GPU run. Complete r1 instruction
streams/contexts and both initial streams remain. This is not runtime failure
or a plan/oracle change. Normal16 records now refer to actual r1 binaries.
