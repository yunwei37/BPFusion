# Third actual preflight: passed, full acquisition eligible

2026-10-16 UTC. All3x128 requests/24576tokens succeed,24 excluded checked gen1
warmups. All3 frozen-pool matches128/128, not general/exact trajectory proof.
Actual K/N graph/network counters and all terminals/drains/pins pass. Official
optimized FLASH_ATTN, compilation/CUDA graphs and enabled default prefix cache
engage; short prompt lengths5/8/5/2 produce reported cache hit0% in these logs.
Do not attribute an unmeasured cache benefit or cap default capacity.

Actual common two-process client gives K/N/O scheduling lagP99
1.242847/1.114800/9.354880ms, maximum1.439749/2.058250/10.767158ms.
Lag minima-1.027964/-1.059235/-0.945072ms remain: uvloop timer wakes can be
early, and no clipping/rewriting of actual client scheduling stamps occurs.
Each worker reaches its scheduler before the common future monotonic epoch;
archive analysis independently checks schedules, parity-union indices,
byte-exact request joins, actual childCPU and last-close denominator.

Per-worker CPU fractions K0.655/0.638,N0.643/0.638,O0.827/0.827;
two processes reduce the single-loop ceiling risk but do not prove unlimited
client capacity. Total acquisition client CPU/attempt8.026/7.873/9.876ms
includes actual child deltas plus supervisor startup/wait/merge
(22.223/15.743/64.333ms supervisor per cell), separately retained. Real full
lag/CPU still bounds any capacity interpretation; protocol costs differ.
This is dependency acceptance, not server throughput ranking or a full result.

Original worker and merged JSONL, server logs, auth receipts, warmups/resources
and terminal records are archived. CPU replay of archived lossless gzip exactly
matches acquisition stdout, stderr empty, exit0. No measured source/default
adoption. Original PIDs/WIP/GPU absence/pins remain preserved; no new core.
Official parent exits0/no children, but own shutdown force-kill/semaphore
warnings remain explicit. Client Job is held only for the immediately following
fixed full15cells, then actualUID cleanup and fresh result review are required.
No fourth preflight, unchanged rerun/largerN/primary switch.
