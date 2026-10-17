# Owner-only pre-acquisition design review

This is the same thread's self-review, not an independent reviewer or agent.
The next hypothesis follows a user decision; no formal paper claim is adopted.

The strongest internal comparator already shares graph dispatch and library
compute. Repetition changes actual library work instead of using an empty GPU
kernel or a simulated delay. Both cuBLAS and cuFFT keep a256-byte numerical
output verified by independent analytic inputs; capture repetition must pass
actual lifecycle qualification before any performance run.

Persistent connections isolate per-request transfer/admission/reply rather
than connection setup. This does not answer connection-churn workloads, larger
payloads, LLMs, TLS or general kernels. Default8 is an explicit matched finite
constructor, not a maximum-capacity configuration search.

The remote client's scheduled-origin tail must include its connection backlog.
Timer-dispatch lag is separately observable; monitor lag is not zero merely
because successful responses are fast. Failed/unsent/partial requests remain
in counts and raw traces. Raw successful quantiles alongside all-attempt
failure-aware P99 avoid hiding overload. Client ceiling is not server capacity.

Unrestricted and1/2CPU cases apply only to owned service threads. Kernel/IRQ
work outside them remains visible in shared-host totals; a process-affinity
restriction cannot cap global networking CPU. This is part of the question,
not exclusive resource attribution. Confirm actual thread masks and stable
group identities and retain shared-host idle/pressure context.

Screening is exploratory, not confidence evidence. Selection rule and new-seed
five-pair confirmation are fixed first, with an explicit negative exit.
P99/CPU co-primary criteria preserve both objectives. Nominal five-pair intervals
remain small-sample, selected-cell evidence. No general superiority claim.
Existing io_uring BPF-loop target must never be mislabeled userspace io_uring.
No immediate need for another baseline, hand-optimized arithmetic, a new
framework, scheduler, agent or infrastructure entity.
