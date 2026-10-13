# Qualification and failure investigation

Initial unchanged-client qualification completed Qwen preflight (three paths,
48 total requests /1560 tokens) and Qwen traced strict (three paths,
1866 requests/66672 checked tokens). Smol candidate traced strict passed
622 requests/22224 tokens. Smol full-copy control then returned EOF before
the first pipelined half-close response. Its final native/model records show
all six pipeline requests admitted/computed/retired, six aborts, no graph error,
no BPF drop, all slots FREE, ring counters balanced. The driver terminates
the model after its receive assertion; final abort counters alone do not prove
when those aborts began. No native Smol control, ordinary strict, HF lifecycle
or performance matrix completed in that initial pipeline.

The failing raw/trace/stdout/source are retained under initial_qualification/.
No output-reference or client-pacing change was made. This is not a candidate
performance win.

A temporary BF_TRACE-only GPU close record diagnostic subsequently completed
all three Smol strict paths:1866 requests/66672 independently replayed tokens.
It did not reproduce the failure. Close records show pipeline closure after
seen=head=616, with no pending reply. Cached/system peer ports agree in this
run. The diagnostic is archived under diagnostic/ and removed from source.

A second diagnosis kept the ordinary GPU network logic unchanged and inserted
temporary kernel BPF printk records for receive/close CQ events and request
publication after admission600. It completed all three Smol strict paths,
1866 requests/66672 tokens. The observed six pipeline publications precede
RECV EOF. The original BPF object was rebuilt afterwards (restore exit0);
the diagnostic is archived under kernel_diagnostic/. Printk may affect timing,
so this also does not explain or repair the original failure.

Disassembly of the diagnostic stock binary shows CQ user_data/res loads before
CQ-head publication and system-acquire loads followed by CCTL.IVALL. This
does not establish a stale-CQE cause. Production CQ/close logic remains unchanged.

A source-native temporary strict driver now exercises 64 consecutive six-request
half-close pipelines, retaining the entire original preceding strict prefix,
unchanged wire/receive functions, independent upstream history replay and all
terminal checks. Only this diagnostic uses the longer lifecycle workload and
larger trace budget. Its full-copy control precedes candidate. Ordinary BPF and
GPU close code are used. It is a fault reproduction exercise, not a timing cell
or altered acceptance workload for the approved performance comparison.

The initial failure remains unexplained. No full performance result exists.

The noninstrumented 64-pipeline stress completed both full-copy and candidate:
1000 requests/46416 independently replayed tokens per condition, 384 complete
pipeline replies each, all original lifecycle checks passing. This bounds
observed reproduction; it does not establish a root cause or erase the failure.
The approved unchanged ordinary qualification is now continuing. HF lifecycle
will use the original /usr/bin/python3 and base child PATH, preserving the
previous HF CUDA13 runtime rather than mixing the vLLM CUDA12 runtime.

All designated noninstrumented vLLM strict checks passed: initial Qwen traced,
new Smol traced, and both ordinary model triples,7464 requests/266688 tokens.
The subsequent HF lifecycle did not complete: Qwen timed out reading its
invalid HTTP response after the first valid request; final counts show two
replies only after teardown. A shutdown-only SQ snapshot diagnosis later
passed Qwen but failed Smol on its first HTTP request with early EOF. Smol
shutdown snapshot had SQ head=tail6, flags0, completed0, sends0; final native
head/completed1, aborted1, graph errors0. That does not establish SQPOLL sleep
as the cause. A kernel-CQ printk diagnosis then passed the Smol lifecycle.
These unsuccessful and subsequent passing observations are all retained under
hf_initial/,hf_idle_diagnostic/,hf_cq_diagnostic/. HF correctness remains
unqualified; no production lifecycle repair or full timing has occurred.
Current temporary CQ load instrumentation compares ordinary versus system
loads before releasing each CQ slot; no permanent source fix is claimed.

## Captured cause and common repair

The eight-idle-cycle reproduction fails on its first Qwen request with early
HTTP EOF. Before CQ slot release, the device records CQ sequence2, receive
user_data144115192370823168, cached_res=-11 and system_res=-11. The matching
reads rule out a stale-field mismatch for this failure: EAGAIN is a genuine
transient completion. Original code set connection dead on every negative
RECV, closed it before the delayed request publication, and finally aborted
the admitted model request. Native accepted/closed1, received/sends0, final
head/completed1, aborted1 and graph errors0 agree with that causal sequence.
The source-native driver and complete receipt are retained under hf_idle_stress/.

Production now rearms RECV after EAGAIN or EINTR, while keeping actual EOF,
other errors, cancellation and shutdown behavior. This common lifecycle fix
applies identically to incremental/full-copy conditions. All temporary
CQ/shutdown diagnostics are removed. The initial six-pipeline failure lacked
its CQ errno, so its cause is not retrospectively asserted. All affected
preflight/strict/HF comparisons will be rerun under the corrected common source
without changing client pacing, reference assets or the performance matrix.

## Repaired normal qualification and repeated-idle boundary

The EAGAIN-repaired twelve traced/ordinary strict executors all pass:7464 requests and266688 valid tokens, plus3108 intentional rejects and60000 empty connections. Both original HF lifecycle workloads also pass. The later eight-cycle idle regression still stalls before request admission; this is not a model-compute failure. Archived hf_idle_repaired, hf_idle_fdinfo, hf_idle_page, hf_idle_tcp and hf_psock_diagnostic retain the real failures and observations. The psock snapshot records TCP copied_seq3003861898 versus psock copied_seq3003861823 (75 bytes), raw queue1, ingress_bytes0 and an active/unpaused parser. IOSQE_ASYNC did not fix the stall and was removed. Temporary same-socket ingress redirect passes both HF eight-cycle workloads,32 requests/652 checked tokens per model, with original protocol/oracle/pacing. Full vLLM protocol qualification is running; no completed copy timing or general reliability claim follows. See finding0043 for the exact candidate and upstream receive sources.

Final production-source qualification completes: both model module/native
strict workloads pass (four executors,2488 requests/88896 valid tokens), as
does the final three-path copy preflight (24 measured gen64 requests/1536
tokens plus24 excluded gen1 warmups). Final commands, raw outputs, analyses
and build receipts are in final_qualification/. Original boot/base/Coder/WIP
remain; endpoint checks find no own BPF pins, loaded module or GPU application.
This completes integration dependencies only. Full copy timing has not started;
all conditions will use one published source revision and unchanged references.
