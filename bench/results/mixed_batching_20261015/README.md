# Packed mixed prefill/decode experiment

The complete independently reviewed comparison ends2026-10-15UTC.
All40 executors/80 cells finish20,480 measured requests with0 failures and
1,310,720 measured tokens,plus320 warmups. Four protocol executors additionally
verify188,800 tokens and2,060 intended rejections.

- [Plan](plan.md),[plan review](plan-review.md),[result review](result-review.md).
- [Terminal](run.exit.json),[commands/status](run.statuses.json).
- [Executed sources](frozen_sources/),[executed C++ diff](mixed.executed.cu.diff).
- [Qwen raw](full_qwen.jsonl),[Smol raw](full_smol.jsonl).
- [Qwen all metrics](full_qwen.analysis.stdout),[Smol all metrics](full_smol.analysis.stdout).
- [Figure](mixed_batching_results.png),[PDF](mixed_batching_results.pdf),[plot](plot_results.py).

Recompute all metrics with standard-library Python from the checkout:

~~~sh
python3 bench/results/mixed_batching_20261015/analyze.py bench/results/mixed_batching_20261015/full_qwen.jsonl
python3 bench/results/mixed_batching_20261015/analyze.py bench/results/mixed_batching_20261015/full_smol.jsonl
python3 bench/results/mixed_batching_20261015/protocol_analysis.py bench/results/mixed_batching_20261015/protocol_qwen.jsonl
python3 bench/results/mixed_batching_20261015/protocol_analysis.py bench/results/mixed_batching_20261015/protocol_smol.jsonl
~~~

For the figure,install matplotlib and run plot_results.py in this directory.
Acquisition scripts retain the exact original paths/model caches,pinned
environment and source guard of the qualified Workspace. They are historical
acquisition records,not a portable installer. Recollection requires matching
the source/runtime and adapting host paths without changing the admitted
conditions,oracle,timeout or primary metric. Public service setup is separate.
No weights,binaries,virtualenv or third-party build trees are committed.

mixed.cu.diff is the original preparation diff before Trace-layout alignment.
mixed.executed.cu.diff and frozen_sources/mixed_vllm_graph.cu describe the actual
executed code;execution-notes.md preserves the distinction. Plotting dependencies
were installed after collection and existing measured versions did not change.
Host observations are sparse;continuous isolation and absence of faults are
unknown. Owned temporary runtime/build dependencies are removed after process/mapping/fd/cwd checks; five copied analyses still match bytewise. See [restoration](final_restoration.json).

Both networks benefit from this common scheduler improvement. Same-mixed
native is the strongest competitor. No general eBPF speedup,ordinary gain,
default16 selection or universal backend/fidelity claim follows. Adverse Qwen
ITL P99 and active CPU rows remain included.
