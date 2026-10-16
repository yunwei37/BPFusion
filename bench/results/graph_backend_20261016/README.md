# Opaque graph adapter engineering acceptance
Original Workspace, RTX5090, same pinned runtime as tail_path_20261016.
Normal Make builds default8 ordinary libraries, no BF_TRACE. Captured graphs
are upstream torch.mm/cuBLAS and torch.fft.fft/cuFFT; no math kernel is authored.
Four repaired lifecycle cases pass,182 outcome checks each. See
[scope/report](../../../docs/findings/0067-opaque-graph-backend.md).
All input/output bytes and independent analytic oracles are retained in
graph_acceptance/*/result.json. Scalars are checked numerically exactly;
FFT controls use analytically exact zero/impulse/constant/alternating inputs.
Observed stop tails end at full words in all4 runs; incomplete responses
remain prefixes, not successful full requests.

Initial build omitted fcntl.h for the native transport; repaired include and
normal rebuild exit0 are retained. Initial matmul/native and matmul/loop pass,
but the next case stops because the harness called legacy detach and left its
own stream pins. Initial artifacts are retained. Repaired harness unlinks all
owned pins after process exit; the full4-case rerun passes with no remaining
pins. User walkthrough uses the correct stream-detach command. No model math,
oracle, protocol or waiting parameter was adjusted. The finite128-entry reply
diagnostic truncates71/86 loop records; complete request checks and ring cursors
are independently retained, so do not claim zero diagnostic truncation.

Actual executable source and Make/environment commands are under sources/.
These historical acceptance drivers retain original TEMP paths. The portable
user path is docs/graph-backends.md. No performance superiority is tested.
