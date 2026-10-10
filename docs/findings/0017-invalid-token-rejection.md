# 0017: reject invalid token IDs without ending resident inference

Observed 2026-10-10 UTC on the RTX 5090 / CUDA 13 / Linux 7.3-rc3 path.
Previously a token ID outside the loaded model's vocabulary returned from the
resident CUDA kernel, leaving the request PENDING and all subsequent requests
unserved. This was a model-input failure with service-wide consequences.

The GPU now checks the complete prompt against the loaded model's vocabulary
before any forward pass. A rejected request publishes DONE and advances the
queue; all CTAs continue together. Existing slot padding carries transport,
validation-pending and rejection bits, so the page layout is unchanged.
The stream producer marks validation pending. Kernel TX waits for validation
before sending a success header, then sends HTTP 400 Bad Request with an empty
body for a rejection. Binary token replies have no status header; the kernel
ends the owned peer connection so the client observes EOF. No host request
worker, per-request CUDA launch, extra queue or model-vocabulary override is
introduced. Ordinary HTTP connections remain usable after an error.

```sh
make probes tools qwen
make -C module CC=gcc-15
python3 tests/resident_qwen.py
PYTHONPATH=executor python3 tests/kernel_tx.py
```

[The real-model regression](../../bench/results/resident_qwen_rejection_20261010.txt)
passes 29 valid requests / 232 tokens against the eager HF fp16 oracle and
three explicit rejection cases. It places invalid IDs at the first and last
prompt positions, including an ID equal to the vocabulary size and UINT_MAX.
Alternating invalid and valid HTTP requests on one persistent stream return
400/200/400/200 in order; both valid replies remain exact. An invalid binary
request yields EOF and a later independent valid request remains exact.
The original concurrent, split-write, ring-wrap, half-close and 5,000 empty
connection controls still pass. Strace finds no steady executor-thread
accept/receive/send calls, and the test unloads the module, detaches its hooks
and removes its map pins.

Kernel counters: 32 stream publications, 5,024 successful socket registrations,
zero registration failures/drops, 2,366 reply bytes, 31 sent completions and
one intentionally abandoned binary reply, zero TX retries, and all 5,024
accepted sockets closed. The existing
[TX regression](../../bench/results/kernel_tx_rejection_regression_20261010.txt)
passes 24 exact replies, two resets and 26 DONE/recycle cycles with PENDING
ownership preserved.

This is a model-vocabulary error contract for otherwise well-framed token
requests. It does not add general malformed-HTTP responses, overload/503
handling, text/JSON input, or long-decode numerical agreement. The failed
64-token oracle and other open serving work from finding 0016 remain open.
