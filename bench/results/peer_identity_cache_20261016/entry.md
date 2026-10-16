# Bounded test entry
2026-10-16 UTC. Base9341a19, original Workspace and sessions unchanged,
foreign tools/setup_env.sh retained. lab/g10 Ready, DiskPressure false;
Workspace /tmp free291393359872bytes before preparation. No GPU process or
BPF pins. Only canonical io_uring_tcp.h becomes the archived candidate WIP.
All runtime/build/source testing stays in the owning Workspace. Reuse private
pinned runtime; no host tuning or model changes. Temporary client recreated
from client_job.json, removed after data recovered; no service paused.
Restore before header if candidate rejected, forward-only if later committed;
keep qualified source only on reviewed benefit. Stop/detach owning test
servers, delete owning Job/Pod and verify original state on closure.
