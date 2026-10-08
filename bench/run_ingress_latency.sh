#!/usr/bin/env bash
# Measure the ingress->userspace wake chain on this host, three variants.
# Writes a table to stdout and the raw output to bench/results/ingress_*.txt
# PIN=1 adds a fourth argument to wake_probe: pin consumer+sender with
# SCHED_FIFO + affinity (control experiment for finding 0001's p99 outliers).
set -eu
cd "$(dirname "$0")/.."
make -s all
mkdir -p bench/results
stamp=$(date -u +%Y%m%dT%H%M%SZ)
out=bench/results/ingress_$stamp.txt
n=${N:-20000}
pace=${PACE:-50}
pin=${PIN:-0}

for mode in 1 2 0; do
  case $mode in
    1) name=ringbuf_epoll;;
    2) name=ringbuf_spin;;
    0) name=recvfrom_block;;
  esac
  for rep in 1 2 3; do
    echo "### $name rep$rep pin=$pin" | tee -a "$out"
    ./build/wake_probe build/wake_probe.bpf.o "$n" "$pace" "$mode" "$pin" | tee -a "$out"
    echo | tee -a "$out"
  done
done

echo "raw results: $out"
echo
echo "host:"
grep -m1 'model name' /proc/cpuinfo
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>/dev/null || true
uname -r
