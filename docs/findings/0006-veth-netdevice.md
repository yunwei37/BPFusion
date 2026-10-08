# Finding 0006 — offline from loopback: the path over a real netdevice

Status: measured on 2026-10-08, same host as `bench/results/HOST.md`.
Raw log: `bench/results/veth_20261008T060717Z.txt`.

`0004`/`0005` ran the `tc` hook on `lo`, where a datagram never crosses a
device driver. This finding moves the identical BPF program and executor onto a
**real netdevice**: a veth pair split across two network namespaces, so every
datagram is transmitted by `bfv0` in one namespace and received by `bfv1` in the
other through the `tc/clsact` ingress hook at `bfv1`'s RX — the same hook a
NIC's RX path would hit.

```
  bfns1: client sendto 10.99.0.2  ──►  bfv0 (TX)  ══veth driver══►  bfv1 (RX)
                                                                     │
                                              tc/clsact ingress eBPF │
                                                                     v
                                             pinned page → resident CUDA kernel
                                                                     │
                                    responder sendto 10.99.0.1 ◄─────┘
                                     bfv1 (TX) ══veth══► bfv0 (RX) → client
```

## Results (resident MLP executor, `work=4`)

| metric | loopback (`0004`) | veth netdevice | delta |
|---|---|---|---|
| RTT p50 | 41.3 µs | **40.8 µs** | −0.5 µs |
| RTT p90 | 43.4 µs | 43.0 µs | — |
| parse → GPU start p50 | 2.5 µs | 0.5 µs | — |
| GPU start → done p50 | 25.5 µs | 25.6 µs | — |
| `own` goodput | 22 286 req/s | 22 483 req/s | — |
| `burst` depth 8 | 26 765 req/s | 26 779 req/s | — |
| requests served / drops | — | 5 201 / 0 | — |

`verify` on the veth path: `max |GPU - CPU| = 2.602e-17 (OK)`, magic and
`client_ns` echoed. There is **no measurable latency penalty** for leaving
loopback: the veth driver adds far less than the ~41 µs the path already spends
on ingress scheduling + GPU visibility waiting.

(`parse → GPU start` reads lower here because the client happens to see the
completion on the same poll iteration more often; it is a sampling artifact of
the zero-crossing, not a device effect.)

## What is and is not proven

- **Proven:** the BPF ingress program and the resident-GPU queue work on a
  device whose datagrams are actually handed to a driver as skbs, with a real
  L2/L3/L4 header layout (`bfv0`'s Ethernet frame), not the loopback shortcut.
- **Not proven:** hardware RX. veth has no DMA, no RX ring, no MSI-X/NAPI
  interrupt; and the host's `eth0` is itself a container veth, so it cannot
  serve as a physical reference. The remaining gap to a NIC is the driver's
  RX/DMA interrupt latency, which veth cannot model.
- **Not measured:** AES/checksum/XDP offloads, RSS queue steering, and
  multi-queue TX — a single veth pair is single-queue.

## Reproduce

```
./bench/run_veth.sh 12
```

The script creates the two namespaces, mounts bpffs inside `bfns2` (a netns
gets a fresh `/sys`, so the pinned maps must be mounted there), attaches the tc
hook to `bfv1`, runs the executor bound to `10.99.0.2`, and drives the client
from `bfns1` with `BF_DEST=10.99.0.2`. `BF_BIND`/`BF_DEST` were added to
`executor`/`client` so either end can be moved off loopback.
