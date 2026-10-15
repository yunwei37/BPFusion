# Read-only admission observation during unchanged full

2026-10-15T08:10:06.974580+00:00

Qwen block0 kernel measured cell successes/failures:4rps256/0,32rps254/2,64rps229/27,96rps189/67. All96 failed requests receive zero tokens and hit unchanged60s socket timeout. The finished executor transports936 requests including8warmups, matching1032attempts minus96. Read-only stats observed page drops96 / llm busy96 / parser calls1032 / parser invalid0; all8modelslots are FREE at that observation. Main bpf/fusion.bpf.c stream_publish line395 returns SK_DROP when llm_reserve cannot reserve a slot; no retry/backpressure is implemented there. Aggregate counts and source identify admission-capacity loss rather than prove a per-marker event trace or a timer wakeup failure. Native block0 completed rows are retained below; do not exclude errors, alter timeout/source, or infer primary latency superiority from conditional successes. Full proceeds unchanged to its planned terminal, with all records retained.

[
  {
    "pair": 0,
    "mode": "uring_loop",
    "rate": 4,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 4
  },
  {
    "pair": 0,
    "mode": "uring_loop",
    "rate": 32,
    "requests": 256,
    "successful": 254,
    "failed": 2,
    "max_in_flight": 10
  },
  {
    "pair": 0,
    "mode": "uring_loop",
    "rate": 64,
    "requests": 256,
    "successful": 229,
    "failed": 27,
    "max_in_flight": 35
  },
  {
    "pair": 0,
    "mode": "uring_loop",
    "rate": 96,
    "requests": 256,
    "successful": 189,
    "failed": 67,
    "max_in_flight": 75
  },
  {
    "pair": 0,
    "mode": "userspace",
    "rate": 4,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 4
  },
  {
    "pair": 0,
    "mode": "userspace",
    "rate": 32,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 10
  },
  {
    "pair": 0,
    "mode": "userspace",
    "rate": 64,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 16
  },
  {
    "pair": 0,
    "mode": "userspace",
    "rate": 96,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 36
  },
  {
    "pair": 1,
    "mode": "userspace",
    "rate": 32,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 8
  },
  {
    "pair": 1,
    "mode": "userspace",
    "rate": 64,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 13
  },
  {
    "pair": 1,
    "mode": "userspace",
    "rate": 96,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 23
  },
  {
    "pair": 1,
    "mode": "userspace",
    "rate": 4,
    "requests": 256,
    "successful": 256,
    "failed": 0,
    "max_in_flight": 3
  }
]

Final first-kernel ring:
{
  "accepted": 1025,
  "closed": 1025,
  "received": 936,
  "sends": 55000,
  "bytes": 312464,
  "completed": 936,
  "aborted": 0,
  "max_connections": 75,
  "max_requests": 8,
  "pending": 0,
  "error": 0,
  "head": 936,
  "reserved": 0,
  "dropped": 0,
  "overflow": 0,
  "sqhead": 61180,
  "sqtail": 61180,
  "cqhead": 289608,
  "cqtail": 289608,
  "trace_count": 936,
  "trace_overflow": 808
}

2026-10-15T08:10:57.146006+00:00

Exact marker cross-check after first kernel exit: all96 timeout markers are absent from936 independently replayed model admission references, and all received token prefixes are empty. Thus the observed failed attempts were not admitted to model computation. Block0 native completes all1024 measured attempts with no error at the same four rates. This remains a first-block observation, not a completed full-matrix performance claim.
