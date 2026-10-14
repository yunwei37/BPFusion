# Replaying the final-response-drain experiment

This directory retains one matched serving experiment and its setup/preflight.
The ordinary performance measurements reuse vLLM model graphs for SmolLM2-135M
and Qwen2.5-0.5B, with the same model revisions, precision, packed/prefix
policies and source-native token-ID input path across all three conditions.
The old SQ-only coalesced path is a component control; efficient userspace TCP
with the same model computation is the competing delivery mechanism.

From the repository root, recompute the complete ordinary matrix using only
Python's standard library:

    python3 bench/results/final_drain_20261014/analysis.py bench/results/final_drain_20261014 full

The output reconstructs client arrival metrics, fixed-wave throughput, partial
known-worker CPU attribution and five-block signed paired intervals. It also
checks same-process ordinary short-output model rounds after the eight
sequential warmup rounds are excluded. Aggregate round count is not observed
batch membership or GPU time.

Protocol trace/history replay verification is separate from ordinary timing:

    python3 -c 'import sys,pathlib; p=pathlib.Path("bench/results/final_drain_20261014"); sys.path.insert(0,str(p)); import analysis; [analysis.analyze(p/n) for n in ["qualification_vllm_smol.jsonl","qualification_vllm_qwen.jsonl"]]'

The traced qualification reconstructs transport/history/KV and reuses vLLM
graphs for replay; it is not a fresh independent eager-HF arithmetic oracle.
Ordinary timing retains the unchanged finite frozen whole-sequence pools. No
claim is made that tracing preserves the ordinary scheduling/timing.

Independently check lifecycle raw slot/recycle/queue receipts:

    python3 bench/results/final_drain_20261014/analysis_lifecycle.py bench/results/final_drain_20261014

Lifecycle checked-token totals include complete responses and intentional
prefixes before reset/stop; they do not mean all long responses completed.
Model quiescence is evidenced by retained shutdown source and successful
shutdown; the freed I/O field was not directly sampled afterwards.

plan.md, plan-review.md and result-review.md describe the hypothesis, scope,
review and decisions. full.commands.json records all twenty driver commands
before collection; each driver records the actual per-condition command,
loaded-library provenance, source/version bootstrap, stdout, cleanup and
terminal status. run.py and the source-native short_serving.py /
transfer_serving.py adapters retain the collection path. Original and
candidate source, build flags/receipts and common package versions retain
reconstruction provenance. Operational publication/cleanup helpers, model
weights, runtime/extension caches, vendor dependencies and ELF binaries are
not part of this archive.

Setup and execution recipes are historical exact-path receipts, not a
portable installer. A fresh real collection must use a matching existing
development environment, rebuild the archived conditions and provide a fresh
temporary output directory. The standalone replay commands above do not
require the original temporary runtime or GPU.

The experiment retains global ordered final-send retirement. Waiting for a
backpressured earlier final send can delay fresh model admission on all peers;
finite protocol/lifecycle tests do not establish arbitrary-peer fairness,
bounded tails, TCP-ACK completion or 32-bit counter rollover.
