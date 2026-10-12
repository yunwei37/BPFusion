# Mixed-length prefill packing: independent plan review

## Verdict and inspected state

Verdict: **pass for implementation and real qualification; no invalidating
scientific or source-semantic defect found in the proposed experiment**.
This is a plan verdict, not evidence that the not-yet-served candidate works,
preserves model fidelity, improves latency, or completes BPFusion.

Reviewed the supplied plan, finding0032, current main dispatcher/bootstrap,
native make rules, service driver/analyzer, and the pinned installed vLLM
source in the existing bpfusion-dev Workspace. Main was verified before this
review file was written. Only this review file was written; no models,
workloads, source edits, Git mutation or infrastructure action was performed.
Original untracked tools/setup_env.sh remains outside this review.

The installed distribution reports vLLM0.31.0, source commit db9527a46.
Source inspection included v1/attention/backends/fa_utils.py, flash_attn.py,
vllm_flash_attn/flash_attn_interface.py, _custom_ops.py, graph capture
preparation, and the Qwen2/Llama model layers. The actual CUDA cache-writer
source was checked at the wheel's commit:
https://raw.githubusercontent.com/vllm-project/vllm/db9527a46/csrc/libtorch_stable/cache_kernels.cu
The initial historical cache_kernels.cu URL without libtorch_stable returned
404; the corrected pinned source supplied the relevant implementation.

## Admission and decisions

The experiment adds a real serving-policy intervention. Current dispatch
selects the first pending prefill length and admits only phase-3 requests
matching it. Grouped serving therefore offers a credible current competing
implementation. Prior identical-compute transport results cannot reconstruct
a mixed-length packing intervention. The observed concurrent short-output
latency and low prefill consolidation make this a decision-relevant next
experiment, rather than another unchanged transport comparison.

The largest justified outcome is a local optimization of the upstream-compute
adapter. Positive grouped-minus-packed gen1/c8 intervals support that policy
within the model/transport cell; negative or crossing-zero intervals bound
or contradict it. Throughput and long-output latency expose tradeoffs. A
mixed result must remain model/transport-specific, rather than automatically
promoting packed serving everywhere. Nominal df4 intervals are separate local
comparisons, not a multiple-comparison-adjusted family-wide success claim.

The main comparison is current grouped scheduling versus packed scheduling.
Kernel and native timed-network conditions are controls for whether the
benefit belongs to GPU scheduling across transports. They cannot attribute a
common gain to eBPF, and the matrix is not an external-vLLM superiority result.
Broader baselines are not an execution gate for this admitted mechanism test.

## Padding and cache semantics

The proposed transformation is source-consistent for the specified full
causal-attention models. Let a real prompt have n tokens, graph query width
Q>=n, and d=Q-n leading dummy query rows. Installed FA2 passes the actual
seq_lens as seqused_k and uniform query_start_loc as query boundaries.
Bottom-right causal alignment gives real row j=d+t the key limit
j+n-Q=t. Thus real token t retains its original causal prefix when its Q
row is shifted right but its KV index and position remain t. The official
interface also documents zero output for fully masked leading query rows:
https://github.com/Dao-AILab/flash-attention#how-to-use-flashattention

The CUDA path imports reshape_and_cache_flash from _custom_ops, which
dispatches _C_cache_ops.reshape_and_cache_flash. The pinned actual
reshape_and_cache_flash_kernel reads slot_mapping and returns for
slot_idx<0 before calculating cache addresses or copying K/V. The installed
Triton fallback also skips negative slots, but it was not treated as proof
for the CUDA path.

Qwen2 and Llama-family source uses original positions for RoPE and token-local
normalization/MLP operations. Dummy token0/position0 computations do not
mathematically mix with real tokens when their KV writes are skipped and
attention sequence lengths remain real. This source argument does not promise
bitwise FP16 equality across different batch/query shapes.

Execution must preserve all of the proposed invariants: real seq_lens=n,
real positions0..n-1, real KV slots for those positions, dummy slot=-1,
padding flags only for dummy rows, uniform Q boundaries, unchanged physical
request-to-KV ownership, and official head selection at each row's real last
token. Decode position remains n after prefill, not Q. Dummy rows must never
increase context length, overwrite real KV, or advance a request's generation
history. Unsupported attention/cache semantics must remain rejected.

## Reference independence and real qualification

The existing replay cannot run the packed candidate unchanged: it currently
requires len(prompt)==query and fills every padding flag false. The plan
correctly calls for necessary metadata reconstruction rather than changing
the token oracle to fit GPU output. The adapted replay must derive d, dummy
IDs/positions/slots/flags, real lengths and block rows independently from
original client prompts, recorded graph width and its own generated history.
Served tokens may be compared afterward, never used to advance that history.

Agreement with padded replay proves metadata/control fidelity to upstream
graphs. Retaining ordinary unpadded upstream diagnostics and the attention/KV
source analysis is essential because equally incorrect CPU/GPU padding could
otherwise agree. Record any padded/unpadded output differences and numerical
diagnostics without silently treating arbitrary deviations as equivalent
model semantics. Known FP16 shape-sensitive trajectories are an explicit
boundary, not permission to change checks after observing failures.

The first real mixed-length/gen64 TCP preflight must show an actual compute
event joining differing prompt lengths, not merely eight concurrent sockets.
The declared mixed2/5/8 and 1/15/16/17/32/64 prompt coverage, invalid tokens,
reuse and mixed output lengths must be visible in real qualification evidence.
Both models and both candidate transports must then complete the fixed
622-request protocol with independent replay, zero overflow/errors and actual
batch-count coverage1..8. If a planned batch count is not observed, report
that coverage as missing rather than substituting client concurrency for it.

The additional untraced default validation is correctly folded into setup.
Freeze independent batch1 upstream references before serving those requests;
check repeated real gen1/64 requests and prompt edges in both default
transports/models. This proves the tested single-client default condition
only. It does not establish arbitrary untraced dynamic-batch equivalence.

## Matrix, executable path and evidence

The declared matrix arithmetic is consistent: two models times four
conditions times five process blocks times four cells equals160 cells,
10240 measured requests,332800 measured output tokens and40 executors.
Eight gen1 warmups per executor add320 excluded warmup tokens. All conditions
retain identical BF_TRACE, upstream catalogue, precision, cache/context
budget, client definitions and no new admission wait.

The existing make/bootstrap/service/replay workflow supplies a native path.
Candidate compile flags/binary selection and four-condition driver/analysis
adapters remain implementation work; the current published driver itself
selects only two transports. Before actual execution, record the runnable
commands, exact selected variants and source snapshots in the promised raw
artifacts. Necessary small native adapters are justified; no new control
framework, promotion system or persistent scheduler is required.

Use the original request checks, socket/driver timeouts and evaluation path
throughout a run. Any necessary change is a disclosed deviation with affected
comparisons rerun. Rotate/reverse and record condition order, pair grouped
and packed within model/transport/block, retain all planned rows and failures,
and recompute each primary estimate from independent process-block means.
First/last client arrivals, TPOT and output TPS remain the inherited native
definitions; their official metric context is documented in earlier findings:
https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html
Client coalescing, padding work, finite-request tails, shared-GPU scheduling
and distinct FP16 trajectories limit interpretation. Graph-count reduction
alone cannot establish a latency gain.

Final result review must verify actual mixed-prefill engagement, request/cell
counts, complete references and client bytes, all normal shutdowns, graph
errors/overflows, and the claimed paired estimates. Preserve prior results,
the original session/Workspace/PVC/base runtime/model caches and unrelated
WIP. Cleanup owns only experiment processes, lifecycle resources and declared
temporary artifacts. A positive traced result still leaves broader default,
network, complete CPU-cost and full retained-goal acceptance unproven.

## Blocking findings

None identified at plan review. The execution requirements above preserve
the supplied plan's validity; they are not requests for wider baselines,
additional paper RQs or optional polish. Candidate implementation and runtime
qualification remain unproven until their authoritative evidence exists.
