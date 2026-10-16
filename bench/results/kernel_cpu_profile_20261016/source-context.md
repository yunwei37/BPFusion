# Current coordination source context, before full profile interpretation
Running kernel7.3-rc3 source:
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/loop.c
https://github.com/torvalds/linux/blob/v7.3-rc3/io_uring/bpf-ops.c

io_loop_nr_cqes returns requested cq_wait_idx minus current CQ tail.
__io_run_loop calls loop_step repeatedly. Only a positive remaining count
enters io_loop_wait/schedule; a reached target can run the next iteration
without sleeping. The BPF kfunc submits SQEs synchronously in this context.
A sampled __io_run_loop ancestor alone therefore includes both waiting logic
and actual submitted socket operations; those cannot be called pure spin.

Current own bpf/uring_loop.bpf.c snapshots may_idle, cq_seen and current CQ
tail before SQ submission. Its wait expression usually asks one more CQE,
but admitted!=admission_seen selects the observed tail, allowing immediate
iterations until GPU acknowledges admission. In active mode the existing
timer remains60000ns; idle updates can instead defer it to the service
deadline. Correct waiting must preserve that distinction and avoid losing
an idle-to-active wakeup. This source observation suggests a candidate
discriminator if full sampling finds substantial coordination work; it is
not a measured cause, admissible optimization or reason to skip profiling.

The io_uring_complete tracepoint in fusion.bpf.c is the selected slot-recycle
mechanism. Its visibility in perf is expected service work, not by itself
evidence of a leaked diagnostic. Creator-TID samples can also include
softirq processing of unrelated packets. Raw stack context must distinguish
nested socket/softirq operations from standalone coordination work.
