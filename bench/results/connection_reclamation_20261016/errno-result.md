# E2BIG and retained EOF diagnostic

Both real192/s24s-prefix servers accept/close4616 connections including8 warmups,
4608 measured attempts each. Kernel fails368 read operations without a token;
native has0 failures. Both ordinary servers exit0 and remove pins. This is
diagnostic engagement, not an observer-free performance confirmation.

First snapshot:3385 links, no failure yet;3142 owned socket FDs,2947 owned
CLOSE_WAIT, llm_queued173. Later snapshot:4248 links,368 failures, first errno7
(E2BIG), llm_queued0,368 owned ESTABLISHED. The later snapshot is after queue
drain, not simultaneous proof of a full map. Terminal max_connections4096,
and general/ring drops/overflow zero. The finite first errno is not a failure
errno distribution. Snapshot durations36.253ms/5.950ms; sequential read-only
census not atomic. Creator stack empty/syscall running, not function profile.

Together with actual global-queue close guard, owned EOF accumulation and
capacity boundary support the reclamation hypothesis. Qualified local-reference
intervention/full common-overhead ablation remain before causal repair claim.
Archive errno/ keeps all outcomes/resources/server/commands/source receipts;
initial diagnostic BPF source/loader modifications and builds retained at root.
Native capture overlapped make -n flag discovery (Torch CPU import), so neither
diagnostic timing/cost is used as a paper performance row.
