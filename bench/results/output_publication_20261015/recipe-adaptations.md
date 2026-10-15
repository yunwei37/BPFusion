# Source-native recipe adaptations
serving.py derives from current bench/vllm_serving.py. Changes are absolute
Workspace import/root; original/candidate mode labels; five paired blocks,
32 requests/cell; rotated condition order; private build paths and explicit
publisher metadata. Existing --loop-comparison enables the existing kernel-
loop worker/CPU/cell-order checks. Strict correctness selects candidate loop/
native only. Request protocol, timers, token checks and fixed oracle unchanged.
analysis.py derives from current bench/vllm_serving_analysis.py. It recognizes
the publication comparison for existing CPU/order checks, rotates four modes,
replaces named contrasts and retains five-pair t95df4. Metric formulas and all
protocol/token/ownership/arrival checks are unchanged.

lifecycle.py derives from the previously completed AMK lifecycle2 with both
native/loop branches. Only backend/name/path/readiness and model-error log
parsing change to current vLLM. All32 request/actions, raw wire/prefix checks,
timeouts,13connection/32publication/31native-completion/10reject and loop
32completion/3abort conservation remain unchanged. Historical interrupted
native criterion is retained, not weakened after a new run.
