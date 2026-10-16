# Public onboarding validation

A fresh isolated Python3.12 virtualenv installs the public requirements.txt;
a new default8 build uses the ordinary main Makefile. Existing original root
builds,WIP and Coder sessions are preserved. The libbpf1.6.3 runtime is reused
from its prior qualified private installation;this is not a fresh OS image.

All four real serving cases finish:Qwen kernel/native and Smol kernel/native.
Each serves HTTP gen1,HTTP gen32 and binary TCP gen32 through the public CLI:
12 complete requests/260 output tokens. HTTP and binary gen32 decoded text
agree per case;one-token TPOT reports n/a. Server stop returns0,queues drain,
and kernel hooks/maps are removed. Invalid gen0/rounds0 exit2 before connecting.
These are installation/usage smoke checks,not a new performance experiment or
independent numerical-quality oracle.

- entry.json,install.py/install_status.json:actual scope/dependency commands.
- requirements.txt.validated:the exact file consumed by fresh installation.
- build.py/build.exit.json:ordinary Make invocation,with a private BUILD path
  to preserve existing builds. Production computation/transport source is unchanged.
- run.py,commands.json,run.exit.json:actual downloads,server/client commands,
  process statuses and cleanup. Downloaded checkpoints reuse the existing HF cache.
- *.server.stdout and *_http_*/ *_tcp_* outputs:actual server/reply/client logs.
- packages.json,pip_check.json,nvcc_version.txt:installed versions and no broken requirements.
- *.current:public source and final runbook;the guide's dependency variable names
  are portable examples rather than the recorded Workspace temporary paths.

The compiler is CUDA toolkit13.0(nvcc13.0.88);the driver's reported CUDA13.3
is not its compiler version. This qualifies the tested Linux7.3-rc3/RTX5090
stack,not arbitrary Linux/GPU compatibility or production readiness.

The README is condensed from a chronological experiment log into an overview
and links to the retained findings/evaluation/raw archives. Existing contribution
and licensing sections are preserved. The client grows6 lines(net),adding HTTP,
bounded protocol-length validation,one-token TPOT and nonzero short-read
failure behavior,without introducing a new runtime service/helper.
