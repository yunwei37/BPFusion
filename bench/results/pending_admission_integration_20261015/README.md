# Ordinary-source pending-admission integration

2026-10-15 UTC. This is implementation/regression evidence, not a new
performance experiment or another independent result review.

The ordinary Makefile and application source now select the reviewed finite
pending queue for the io_uring BPF loop. The native event-driven wait and
shutdown wakeup are synchronized too; model arithmetic is unchanged. Source
binding records match the reviewed snapshots, with only the loop/loader object
paths replaced by the Makefile's existing BUILD location. The shared HF/AMK
adapter adds the same native shutdown interrupt as vLLM.

## Actual build and regression

The standard root Makefile builds into an owned temporary BUILD directory,
preserving original build artifacts and WIP. build_command.json and commands.json
record the real commands. The first build was launched without a terminal
receipt; build_validation subsequently exits 0 and confirms every target is
up to date. Both logs remain. This is not a fabricated exit for the first launch.

Nine shared libraries build: five serving variants and four shared-adapter/
after-submit compile controls, plus loader and three BPF objects. Other backend
builds establish compilation only, not new numerical or performance coverage.
compiled_object_paths.json checks the exact BPF paths embedded in the binaries.

Qwen and Smol each run loop/native protocol regression from these newly compiled
ordinary sources: four executors,2,560 protocol outcomes,93,504 replayed model
tokens,including 1,036 intended rejections. All actual batches 1..8, fragmentation,
mixed 1/64 outputs,reuse/wrap,24-request half-close pipeline and helper-thread stop
pass. Trace/history/client bytes and final ownership checks pass. These are not
2560 successful inference responses: intended rejections are included.

The fixed qualification driver and oracle are reused with only loader/build
directory bindings changed. Its independent upstream graph/KV/history replay
remains unchanged. Root default build artifacts are deliberately not overwritten.
The root kernel_tx.py default-path invocation is not newly claimed: the previous
same-header module compatibility test and source identity remain its evidence.

## Performance and ordering scope

The full performance result remains
[finding0062](../../../docs/findings/0062-pending-admission-tails.md):
primary 64/s P99 superiority inconclusive, secondary Qwen/96 tails better but median
and process CPU worse,no established throughput advantage. Selecting the finite
admission repair does not turn that result into a general performance claim.
Finite queue overflow still drops; normal EOF waits for the global backlog,
and stop explicitly cancels unadmitted requests.

admission_order.py is a post-review exploratory CPU analysis of those saved full
traces, not another GPU execution or part of the earlier independent review:

    python3 admission_order.py ../pending_admission_20261015

At Qwen96,the maximum number of later-client-stamped requests admitted first
is 149/175/165/72/159 per native block,versus 1/2/2/1/1 for the kernel FIFO.
The corresponding native worst-TTFT requests are bypassed 143/175/165/72/159
times. Client stamps precede sends; they are not exact kernel ingress times
or measured queue-residence durations. This supports a scheduling/fairness
explanation, but cannot identify syscall removal as the tail cause. A stronger
comparison must align native admission policy before claiming a driver advantage.

## Restoration and reproduction

See final_restoration.json for the actual removal/preservation state and
final_replay.json for saved-data replay after owned temporary directories are
removed. Original Workspace processes, unowned tools/setup_env.sh and eight
preserved setup/build artifacts stay untouched. Base packages are preserved.

Recreate the pinned runtime from ../pending_admission_20261015/setup.py and
packages.json, or use equivalent existing dependencies. Rebind recorded temporary
paths in this regression driver to the rerun's ordinary BUILD directory; no
private source snapshots are needed. Build with the normal root Makefile and
VLLM_PYTHON pointing to that runtime. BPF object paths follow the same BUILD
authority. Rebuild any exact-size-checking module for the new page header;
its KDIR override must point to the running-kernel headers.

The two protocol analyses need ordinary Python3 and saved sidecars, not CUDA:

    python3 protocol_analysis.py protocol_qwen.jsonl
    python3 protocol_analysis.py protocol_smol.jsonl

These CPU checks validate saved evidence and are not repeated GPU numerical runs.
