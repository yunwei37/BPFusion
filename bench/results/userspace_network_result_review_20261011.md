# Native userspace network comparison: independent result review

Fresh reviewer: userspace_network_result_review. Read-only review completed
2026-10-11 07:37UTC against source9983198d6f41e34730d7fa193775f62cf9674a99.
Recorded by root from the reviewer's final Markdown response. The reviewer
performed no GPU workload, build, file mutation or restart.

Verdict: complete, correct supporting component ablation; no required
scientific repair. Primary single-client one-token TTFT has a small nominal
kernel advantage in both models. Primary eight-client64-token throughput
remains inconclusive. No broad serving or isolated syscall-removal claim.

## Independent reconstruction

The reviewer read the approved finding0025 plan and plan review, both raw
JSONL/stdout receipts, benchmark, eager oracle, graph loader/dispatcher,
native reactor and kernel TX source. Independently reconstructed80 unique
cells,5120 measured requests,166400 exact tokens and zero failed/excluded rows.
Per model: metadata1,bootstrap10,idle10,request2560,cell40,executor10.

Five paired blocks alternate mode order, with identical rotated cell order
within each pair. Every cell has indices0--63 once and each prompt16 times.
All oracle prefixes, arrival order, TTFT, TPOT, completion, TPS, closed-loop
worker ordering and descriptive global CPU arithmetic agree. CPU windows
encompass the request span. Frozen benchmark source matches current source.

Each of20 processes reports one resident launch,8580 model graphs,error0,
banks8,max_active8,264 requests including eight excluded warmups. Each native
user process has accepted19,published264,completed264,rejected0. Each kernel
process has stream publication264,sockhash linked19,parser calls264,head264,
zero parser/registration/admission errors and eight FREE slots. Normal child
return codes are checked. Smol terminal exit0:07:18:33.584300UTC; Qwen terminal
exit0:07:32:40.071122UTC.

Qualification inspection independently confirms all78 printed64-token
expected/actual arrays and positive after-ready accept/receive/send traces.
The current native header matches its frozen qualification source.
Independent cuobjdump inspection confirms1536 identical dispatcher
instruction/encoding lines.

At07:35:55UTC, read-only libbpf queries find zero current-cgroup sockops,
no BPFusion named programs/maps, empty bpffs and absent module/processes.
Tracked source has no diff; unrelated tools/setup_env.sh remains untracked,
2012bytes. At07:37:03UTC, boot remains04dc0087-5ccc-4c46-9997-b9a92f0e5167,
original SGLang2762187 is running/GPU resident and journal read succeeds with
no NVRM Xid since07:01UTC. Residency is not SGLang service acceptance.

## Paired results

Positive values favor kernel in both columns. Intervals independently use
five paired differences, df4, two-sided critical value2.776445105.
Primary effects are gen1/clients1 TTFT and gen64/clients8 TPS.

| Model | Gen | Clients | User minus kernel TTFT ms [nominal t95] | Kernel minus user TPS [nominal t95] |
|---|---:|---:|---:|---:|
| SmolLM2-135M | 1 | 1 | 1.054 [0.949, 1.160] | 0.627 [0.569, 0.686] |
| SmolLM2-135M | 64 | 1 | 0.680 [0.544, 0.816] | -2.473 [-5.983, 1.036] |
| SmolLM2-135M | 1 | 8 | 0.306 [-0.333, 0.945] | -1.970 [-8.109, 4.169] |
| SmolLM2-135M | 64 | 8 | 0.072 [-0.873, 1.017] | -5.899 [-13.040, 1.242] |
| Qwen2.5-0.5B | 1 | 1 | 1.107 [0.923, 1.292] | 0.656 [0.544, 0.769] |
| Qwen2.5-0.5B | 64 | 1 | 0.461 [-0.048, 0.971] | -0.796 [-2.740, 1.148] |
| Qwen2.5-0.5B | 1 | 8 | 0.927 [0.269, 1.586] | 3.150 [-3.931, 10.231] |
| Qwen2.5-0.5B | 64 | 8 | -0.334 [-1.530, 0.862] | -3.194 [-10.281, 3.894] |

Both primary TPS intervals cross zero. Primary pair0--4 values:
Smol TTFT[0.972409,1.108832,1.169921,1.039965,0.979506]ms;
Qwen TTFT[1.119715,1.212246,1.191578,1.163868,0.849208]ms;
Smol TPS[-9.378501,-4.546925,1.523421,-3.583045,-13.509359];
Qwen TPS[-9.111063,-9.498693,1.755522,-1.075637,1.962061].

All independently reconstructed long-output completion/TPOT difference
intervals cross zero. Mean user-minus-kernel completion/TPOT:
Smol clients1 -2.237ms/-0.0463ms, clients8 -3.524ms/-0.0571ms;
Qwen clients1 -0.625ms/-0.0172ms, clients8 -3.359ms/-0.0480ms.
These secondary effects do not replace the declared primaries.

## Fairness and limitations

Model weights/precision, capture, eight private banks, sampling and resident
GPU dispatch match. The control has no Python or per-token host-compute
strawman. The treatment changes transport, page backing, completion polling
and write grouping together: user busy-polls and can send both parts in one
loop; kernel sends one part per poll then sleeps60--120us. Do not attribute
effects solely to syscall elimination, eBPF or a single CPU transition.

Both modes retain roughly40ms TTFT plateaus. This run has no per-request
packet/GPU-ready trace establishing their cause. Finding0018's older packet
and bounded NODELAY observations support ACK/Nagle as a next hypothesis,
not as an explanation proven for every new request.

Scope: loopback/canonical binary token-ID HTTP, four short prompts, two small
FP16 checkpoints, closed-loop clients1/8, independent batch1 graph concurrency,
shared RTX5090. Five adjacent pairs supply nominal local intervals, not
familywise superiority, equivalence, robust tails or interference-free runs.
Finite small replies do not prove exhaustive backpressure behavior.

The user reactor consumes about one process CPU second per wall second,
including idle. Kernel executor CPU excludes TX and softirq;100Hz accounting
makes zero quantized, not proof of zero work. Global CPU includes client and
unrelated work. Neither metric establishes total service CPU savings.

## Judgments and decision

- Run status: complete and valid within admitted scope.
- Tested hypothesis: narrowly supported primary gen1/clients1 TTFT;
  primary concurrent long-output throughput inconclusive.
- Research value: supporting evidence filling the absent exact-compute
  native network control and directing work to transport/completion.
- Paper impact: bounded supporting ablation; no novelty or external
  optimized-serving superiority established.
- Next decision: publish complete results with negative estimates and
  crossing-zero intervals. Qualify header/first-token coalescing in both
  transports, then use matched before/after measurements without changing
  computation, oracle or TCP defaults. Do not repeat the unchanged matrix.

No required repair or follow-up result review for this completed comparison.
