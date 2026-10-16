# Kernel-owned TCP source: initial engineering checks

2026-10-16 UTC. These are source-preparation/build dependencies, not a new
admitted performance experiment, protocol qualification or source selection.
The current20-cell controller-stage acquisition remains unchanged.

Pure BPF compilation initially fails because config conflicts with a target-BTF
typedef; after renaming it, BPF_PROG's hidden ctx argument conflicts with our
explicit argument. Both are corrected using project-specific/context names.
Original failing source/stdout/stderr/commands remain in build_records.
BPF compile2 exits0 (2507 disassembled instructions). Host C++ syntax0 exits0,
with the existing UAPI-header warning preserved. No program was attached/run.

The initial normal8/16 Make invocation exits0 and produces the libraries,
loader and parser, but OMITs kernel_tcp.bpf.o: its explicit state dependency
has no source recipe and the generic BPF pattern cannot find this private
source. Thus those exits do NOT establish a complete candidate build.
The first verifier-only diagnostic cannot open the missing object; it never
reaches the verifier. Its ring/memory/object are closed and no link/listener/
I/O submission occurs. Treating that failure as verifier rejection would be wrong.

A minimal corrected Makefile redirects only selected mixed targets and gives
the new BPF object its explicit canonical clang recipe. Corrected8/16 output,
object symbols and actual .so binding are still pending at this entry.
The initial Makefile and incomplete-build receipts remain separate.

Offline SASS comparison is valid for the actual initial libraries: at each
capacity8/16 all emitted device function instruction streams equal candidate,
native and selected before-native. The sole dispatch has1464 instructions and
there is no io_network function. Parser/admission/completion-recycle BPF
instructions/relocations equal selected before. This establishes compiled
controller equality only, not captured-model execution or TCP correctness.

Private prototype source remains unselected. Verifier acceptance, attachment,
full TCP/HTTP behavior/lifetimes, actual reused-model fidelity and matched
performance all remain unproven. Current production source has not changed.

## Subsequent real build/verifier checks

Corrected normalr1 emits both actual kernel_tcp.bpf.o files, symbols and the
.so path binding. Buildr2..r8 retain ordinary8/16 target commands and exits0.
These are build dependencies, not a completed performance comparison.

The actual verifier then finds:
- load1: open CQ loop hits8193-jump sequence complexity after86019 instructions.
- load2: helper-based CQ/peer/connection walks reach a TX-header bounds proof
  failure. A checked local header replaces later unbounded struct reloads.
- load3/load4: the remaining reply/token loop paths hit1000001 examined
  instructions. Reply and token walks become bpf_loop callbacks with unchanged
 16-slot/64-token and connection/CQ capacities.
- load5: CQ-derived connection index has a 32-bit bound but the generated64-bit
  pointer operand is not proven bounded. Explicit zero extension and checking
  the actual wide index repair this; later RX/peer accesses get their own same-
  operand bounds rather than relying on a separately transformed pointer.
- load6/load7 preserve the remaining RX/peer bounds failures.
- load8: actual16-bank load succeeds. Its errno95 is stale on successful
  libbpf return0, not a failing return. The helper now prints errno0 on success.

Final banks8/16 verifier diagnostics each compile their own matching helper,
create a temporary normal ring and registered memory region, load the actual
matching new object successfully, close object/ring/region, and attach nothing.
Both use real capacity4096 and entries8192; registered bytes17199104/17203200.
No listener, I/O submission, BPF link, GPU model or application operation runs.
All failure histories/commands/stdout/stderr/exact sources remain in build_records.
The initial uncompiled source draft is preserved separately and unchanged.

verifier_accepted_source is the current private source/build entry, not selected
production. GPU controller SASS and old parser/admission/recycle objects retain
the earlier independently compared instruction streams: sole1464-instruction
dispatch, no io_network. That is compilation equality only. This candidate has
NOT established attachment, TCP/HTTP/lifetime/cancellation/model correctness or
speed/CPU improvement. Those require the next evidence-backed admitted run.
Current source, timer, client/oracle and all20 timing cells remain unchanged.
