# Candidate preparation, not adoption

Private modified files live in TEMP/reclamation_source, not another checkout.
Shared-page tail appends4096 u32 conservative pending buckets (16KiB); existing
field offsets remain. This is no connection limit or runtime tuning flag.
Producer increments before queue publication, rolls back failed push; sole
consumer publishes slot/head before decrement. GPU only uses peer-local count
on actual RECV EOF; other dead sockets retain global guard. Pending count is
acquired before fresh head/seen comparison. Hash collisions only defer close.
Global ablation has the same counters/ABI and fresh ordering, with compile-only
BF_IO_GLOBAL_PENDING_GUARD; untouched2c source remains historical control.
No model math change. Stop override and no pending-reset remain existing
behavior: maps are removed after all transport/model shutdown. No live zeroing.
Candidate requires qualification and full comparison before adoption.
