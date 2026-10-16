# Streaming-tail investigation (in progress)

User priority on2026-10-16: diagnose Qwen192 adverse inter-token P99,
repair a demonstrated cause and retest matched conditions before complete
resource/remote-load experiments. Then qualify ordinary mixed scheduling and
a real reusable backend; add an official vLLM server whole-service reference.

[Plan](plan.md) and [fresh plan review](plan-review.md) admit the staged
diagnostic. No root cause, repair or new speedup has been established yet.
The original f56d0ee serving sources remain selected.

## First completed step: existing-data discriminator
Run: ~~~/usr/bin/python3 existing_tail.py~~~ (remove Markdown delimiters).
[Script](existing_tail.py), [all per-block results](existing_tail.json).
This post-hoc reanalysis retains every Qwen192 mixed request from0065.
It reproduces all ten block ITLP99 values. The kernel's slowest1% intervals
include final-token gaps in12..50 of162 cases/block (7.4%..30.9%).
Interior gaps therefore account for most of that tail. Final retirement
ordering is a candidate contributor, not a complete explanation.

Zero-arrival-gap fractions are32.45%..52.33% for loop and19.89%..36.35%
for native. These measure recv-observed token coalescing; they do not isolate
TCP buffering, GPU pauses, kernel queueing or client scheduling.
Native also retains rare229.86/280.42ms maxima; an improved P99 does not erase
these larger outliers. No new GPU experiment or causal conclusion is implied.
