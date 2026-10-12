# Release completed GPU requests without serial local TX reclamation

Retain the full BPFusion goal and original Workspace/main/owners. This is a
supporting causal service-scheduler experiment; it does not introduce model
arithmetic, a new transport, queue ABI, retained service or batching wait.
The current prefill-packing matrix must finish and receive its combined review
before mutating the serving source or starting this experiment.

## Evidence and hypothesis

Qwen's complete packing comparison passes all80cells and independent replay.
Packed kernel gen1/c8 TTFT remains8.701889ms versus1.424515ms atc1;64 requests
use56..58 prefill graphs. Packed gen64/c8 TTFT is2.155560ms. These differing
closed-loop workloads do not by themselves identify a causal retirement cost.

Actual native source publishes only one phase2 request as BF_DONE, sets a global
reclaim flag, waits for that slot's local TX reclamation before publishing the
next DONE, and can select a newly pending model prefill in between.
Both existing TCP paths intentionally withhold the final token until BF_DONE.
DONE departure means local sendmsg/tcp_sendmsg accepted/copied the full response
and TX released slot ownership; it does not mean remote TCP acknowledgement.
The request-ring reservation bitmap independently protects every physical slot
until TX finishes all old slot accesses and clears its bit.

Hypothesis: publishing the entire already-complete consecutive FIFO prefix in
one GPU scheduling turn, without waiting for local TX reclamation between those
publications, reduces gen1/c8 response latency and permits actual prefill batching.
Keep FIFO publication, final-token protection, system fences, actual per-slot
reservation release and per-peer TCP ordering. This isolates release policy,
rather than changing all ordering or model behavior at once. A global wait on
one completed slot is redundant only if actual source/ownership review and real
reuse tests establish that per-slot reservation plus local phase ownership suffice.

## Candidate and matched baseline

Freeze one already-qualified common prefill policy after the current complete
matrix is reviewed. Prefer the stronger measured qualified alternative, record
its identity and reason before first serving, and use it unchanged in both
retirement policies and both transports. Do not compare different model math,
precision, KV budgets, graph catalogues or sampling.

Candidate replaces reclamation-serialized single-prefix retirement with a
loop publishing all consecutive completed phase2 requests before admission/
compute selection. Local request phase clears only after the last graph token
has been consumed and system-published. No old released-slot/KV access may occur
after ownership release. New admission still requires the physical slot's
published PENDING state and an unused local request record; TX reservation bits
remain untouched by GPU release. Reserved producers paused before WRITING
publication remain protected.

Keep the original release path as the explicit component control. Ordinary
temporary compile variants and the existing driver lifecycle suffice; final
source/build naming should avoid retaining unnecessary combinations. Diagnostic release-round/max-prefix counters must be shared in both compared
builds, export only on normal stop, and be reported as instrumentation. They
must demonstrate max-prefix1 in the control and an actual multi-request
publication in the candidate, rather than assume source engagement.

## Integrated qualification and experiment

Fresh independent plan review precedes execution. Actual mixed eight-client
gen1 andgen64 TCP preflight must exercise multi-request completion publication
and independently replay every returned token with zero errors/overflow.
Then both cached architectures and both transports complete the existing strict
622-request protocol, allB1..8, fragmentation, prompt/KV edges, invalid IDs,
persistent wrap/reuse, mixed1/64 output lengths, pipelining, half-close, binary
EOF and helper-thread shutdown. Require received bytes, independently advanced
host replay, normal exits, actual counters, terminal reserved0/FREE slots and
kernel-versus-userspace after-ready network-call distinction. Frozen upstream
fidelity diagnostics remain explicit; no served-token teacher forcing.

One matched full experiment, same existing gen1/64 × clients1/8 conditions,
five alternating process blocks,64 measured requests/cell,eight checked warmups:
two release policies × two transports × two models =160cells,
10240 measured requests/332800 tokens, plus320 warmup tokens.
Freeze the actual selected prefill policy in the admitted plan before starting.
Do not add a model-specific tuning campaign or another unchanged packing matrix.

Primary: reclamation-serialized minus prefix-release gen1/c8 mean TTFT
within each transport, nominal paired t95 df4. Report every pair, all long-output
TTFT/TPS/TPOT/completion and single-client tradeoffs, finite-request p50/p99,
actual prefill/mixed-batch/padding counts and completion publication counters.
Keep all failures/outliers; a startup/readiness pass or graph-count change alone
is not a performance result. Positive actual paired evidence supports only the
tested release policy and workload; negative/inconclusive evidence is retained
without favorable reruns. No equivalence, physical network, total CPU/energy,
arbitrary model, task quality or eBPF-only gain follows.

After complete replay and fresh combined result review, apply the qualified
beneficial release behavior to the ordinary serving implementation if evidence
supports it, with necessary real untraced default checks. Keep only controls
needed for reproduction. Archive exact commands/sources/raw/trace/references/
wait statuses and uncertainty, update OSS docs, validate owned paths, commit
and push main, then remove only owned temporary processes/runtime-linked
artifacts. Preserve original base runtime, Workspace/PVC/caches and unrelated
tools/setup_env.sh. The broader goal remains active until its full acceptance
audit is proved.

## Frozen common policy and outcome interpretation

Select packed prefill (BF_PAD_PREFILL) in every release/transport build for both
models. Finding0033's complete matrix qualifies exact service/replay/semantics
and positive gen64/c8 TTFT intervals in both models/transports. This is a stronger
qualified long-output control; its mixed gen1/c8 primary result is retained,
not relabeled a universal short-output win. Keep its current graph/catalogue/
KV/precision/math/head binding unchanged. Neither policy selection nor an
inconclusive c1 interval establishes equivalence or task quality.

Predeclare each primary nominal paired df4 interval: wholly above0 supports the
tested release-policy benefit; wholly below0 contradicts it; crossing0 is
inconclusive. Mixed model/transport outcomes remain mixed. Retain all secondary
tradeoffs/outliers and the strongest control rather than favorable reruns.

Implement release request-ID events and common release-round/max-prefix counters
in both compared variants, and join release events to actual client cells.
Diagnostic trace capacity derives from admission + at most64 compute + one
release event per request. Validate complete one-time release after each valid
request's final computed token (or zero computed tokens for intentional rejects),
FIFO ID order and release-before-physical-slot reuse. This direct evidence will
distinguish actual gen1/c8 prefix publication from an unrelated long-output max.
Final actual binary/compile/driver mapping and invocations follow implementation
and precede the first candidate serve. No serving source is changed before the
prior study's combined review report is complete.
