# Kernel-loop qualification history

The first BPF compile fails on the BPF_PROG macro's reserved ctx argument name;
renaming the typed argument to loop_ctx compiles successfully. Initial compiler
logs remain archived. Native ordinary/traced builds all succeed, with retained
running-kernel UAPI export warnings. Original base packages are unchanged.

Real preflight attempt1 fails before NET_READY or any model request. The model
graphs capture, but libbpf1.3 returns no struct_ops initial-value pointer.
The later object-only diagnosis records initial_value_present=false,size0,
while actual BTF has the correct24-byte io_uring_bpf_ops and ring_fd at64bits.
It therefore never invokes bpf_object__load; this is not a verifier rejection.
The initial raw/log/status,successful detach and executor failure remain in
preflight_initial/. No serving/timing success is inferred.

Upstream libbpf1.6.3 supplies the documented struct_ops shadow value through
bpf_map__initial_value. Build it under the owned temporary directory and use
its LD_LIBRARY_PATH for all three experimental conditions. The original system
libbpf1.3,base Torch/Transformers and host/kernel remain unchanged. This is a
common temporary dependency correction, not a compatibility shim or oracle/
client/polling/model change. Exact source URL/build/versions are retained in
libbpf_dependency.json and build logs. Source condition and primaries stay fixed.

Attempt2 completes all40 Qwen loop replies with fixed-reference agreement but
cannot exit:all19 connections close,completed40,error0,model_quiesced1,
pending1. Live CQ snapshots show continuing tag8 TIMEOUT/-ETIME/MORE records
while SQ is drained; the final SQE is cancel-all flags5. This records an
uncanceled multishot timer, not a model/output fault. Only its confirmed owned
faulty PID260640 is killed after preserving report/ring/CQ/SQ evidence; the
parent records exit failure and detaches. Original Coder/host/other work is
untouched. Add standard TIMEOUT_REMOVE after cancel-all completes,retrying
ENOENT while the timer has no terminal CQE. No user helper or pacing change.
Loop SQ/CQ checks now balance each queue separately:multishot CQEs legitimately
make total CQ count differ from SQ count. The old all-four-equal assertion
remains for single-shot SQPOLL; this is a required multishot adapter correction,
not relaxed wire/oracle/pending/error/lifecycle checks. Third preflight remains
the last admitted real preflight attempt.

Real preflight attempt3 passes all3 paths/12 cells:120 requests/3144 tokens
including24 excluded checked gen1 warmups. Exit/analysis0 and normal transport
counters/lifetimes. Explicit timer removal completes shutdown,with separately
balanced SQ and CQ pairs. This concludes the three-attempt real preflight;
full protocol/idle/helper-thread validation and timing remain incomplete.

All12 vLLM protocol executors pass:7464 requests/266688 valid tokens,
3108 expected rejects and60000 empty connections. Traced runs replay actual
batch/KV history; ordinary runs keep frozen complete-output-set checks.
All after-ready traces engage the intended networking; loop has no SQPOLL
task and exactly one steady blocking kernel entry. Compiled loop/stock model
dispatcher SASS remains byte-identical; both older0043 analyses replay
byte-identically after the analyzer extension.

Initial HF lifecycle attempt fails before NET_READY or requests because
qwen_graph.py's explicit launcher-name mapping omits qwen_graph_uring_loop
and selects the existing default module library. Read-only diagnosis finds
no io_uring FD and the default module loaded. SIGTERM only confirmed owned
executor266195; normal exit removes its module and GPU app, then the driver
records failed-before-READY and removes its pins. This is a launcher adapter
failure, not an HF model or kernel-loop correctness failure. Add the one
launcher name and rerun affected HF qualification with identical cases,
oracle and pacing. Original failed artifacts remain in hf_entry_failed/.

The corrected HF launcher completes both unchanged lifecycle workloads:
32 requests/652 independently checked complete or prefix tokens per model,
13 accepted/closed sockets and3 expected aborts. Both exit0,graph_error0,
pending/error/drop/overflow0 and no remaining pins. Actual ring flags are
SINGLE_ISSUER/DEFER_TASKRUN without SQPOLL. Each trace shows two zero-submit
loop entries:one covering all steady serving and one after SIGTERM for
shutdown. Steady serving has no userspace socket calls. Raw traces and the
explicit interval audit are in hf_loop/ and hf_network_audit.json.

Full qualification is now complete; the original wrapper's failed HF record
is retained rather than rewritten. hf_loop/pipeline.status.json supplies the
successful affected retry. qualification_endpoint.json is a separately timed
no-own-module/pins/GPU-app endpoint before performance, not continuous host
isolation. Performance collection and its result review remain pending.
