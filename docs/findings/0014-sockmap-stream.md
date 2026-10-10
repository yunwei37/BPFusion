# 0014: sockmap TCP stream ingress to resident Qwen

Observed 2026-10-10 UTC. The real-model path now uses sockops + sockhash
SK_SKB stream parser/verdict instead of tc segment parsing. TCP performs
sequencing/reassembly before the BPF parser frames a binary token request.
The existing kernel module owns accept/drain and TCP TX; the same resident
CUDA Qwen kernel consumes the page. No host request worker was added.

## Implementation and lifecycle

`bpfusion_load stream-attach` discovers its current Workspace cgroup v2 from
/proc/self/cgroup, attaches sockops only there, and attaches parser/verdict
to the sockhash. Only server sockets on the token port are registered.
`stream-detach` removes the link and sockhash pin. The tc baseline still uses
`attach lo`; loader autoload selection keeps the two frontends separate.
The stream verdict reserves FREE->WRITING before advancing head with CAS,
copies the complete request, then publishes PENDING. This prevents concurrent
producers or ring wraparound from taking an in-flight producer's slot. CUDA
waits for PENDING, so reservation does not expose an incomplete payload.
The build uses BPF v3 because the default LLVM target rejected 32-bit CAS.

The first real stream run timed out with zero published requests even though
5,001 sockets had been registered. Instrumentation showed zero parser calls.
The sockhash had no remaining userspace reference when the loader exited;
[Linux sock_map.c](https://github.com/torvalds/linux/blob/v7.3-rc3/net/core/sock_map.c)
uses map_release_uref to release its attached programs. Pinning the sockhash
retains that necessary reference. A real full/split request diagnostic then
published exactly one request per connection. This is lifecycle evidence,
not a verifier or attach-only acceptance claim.

The first fixed real-model run matched 96 tokens but reported 94 sockhash
registration failures during 5,000 empty connection churns: the initial
64-entry map was insufficient for transient established/closing sockets.
The loader now discovers /proc/sys/net/core/somaxconn and sizes its socket
registration table to that existing capacity (4096 in the recorded run),
rather than introducing a separately configured connection cap. The request
ring still has its existing eight slots; a full ring drops admission. No
claim of unbounded capacity or overload handling follows from this test.

## Reproduce and results

```sh
make probes tools qwen
make -C module CC=gcc-15
# weights from finding 0013, outside Git; strace installed
python3 tests/resident_qwen.py
```

The test cleans up its module, process, stream link, sockhash and tc hook.
Every header/payload byte is sent separately with TCP_NODELAY and a delay.
The final test runs four prompts, eight tokens each, three serial repetitions
and an eight-client concurrent cohort. All 20 replies/160 generated token IDs
match the independent eager-HF fp16 oracle. The cohort is queued/serialized
by the single resident CTA; this is not GPU continuous batching.

Raw logs preserve failures as well as successes:

- [initial timeout](../../bench/results/resident_qwen_stream_20261010.txt)
- [pin fix, insufficient table](../../bench/results/resident_qwen_stream_fixed_20261010.txt)
- [concurrent control](../../bench/results/resident_qwen_stream_concurrent_20261010.txt)
- [final slot-reservation control](../../bench/results/resident_qwen_stream_owned_20261010.txt)

Final counters: stream publish=20, parser calls=480, parser invalid=0,
sockhash linked=5020, sockhash failed=0, admission drops=0. Module exit:
640 output bytes, completed=20, accepted=5020, closed=5020, abandoned=0.
Strace of every executor thread again records no accept/receive/send calls
after ready. The host boot ID remains unchanged. No physical loss injection,
TCP retransmission trace, overload response contract, HTTP, text tokenization,
GPU batching or performance advantage is established by this result.
