# Preflight attempt1 setup failure

2026-10-16 UTC. First before cell's eight checked warmups completed.
Measured client then exited1 before scheduling any actual request:
FileNotFoundError /tmp/cpu_profile_preflight_offsets.json. Original client
JSONL contains metadata and client_failure only. No throughput/tail result
is inferred and no response failure fraction is substituted for missing load.
Observer and server terminate normally0, pins empty and no GPU process.
Full original client, warmup, resource, source/argv and terminal records are
archived in peer_identity_preflight; first driver snapshot retained there.

Cause: recreated bounded Job received the three full-run assets but I omitted
the existing128-prefix preflight offsets asset. Copied that unchanged file
from the owning Workspace. Independently verified its0_192 list is exactly
the first128 values of the frozen full schedule. Source, oracle, timeout,
arrival values and metrics are unchanged. This is preflight attempt2, not a
new budget or replacement of a valid performance result. Retry stage name is
peer_identity_preflight_retry1 so the terminal but invalid first before cell
cannot be resumed/skipped as a pass. Full-run stage/commands unchanged.
