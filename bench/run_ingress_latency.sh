#!/usr/bin/env bash
# Measure the ingress->userspace wake chain on this host, three variants.
# Writes a table to stdout and the raw output to bench/results/ingress_*.txt
set -eu
cd "$(dirname "$0")/.."
make -s all
mkdir -p bench/results
stamp=$(date -u +%Y%m%dT%H%M%SZ)
out=bench/results/ingress_$stamp.txt
n=${N:-20000}
pace=${PACE:-50}

for mode in 1 2 0; do
  case $mode in
    1) name=ringbuf_epoll;;
    2) name=ringbuf_spin;;
    0) name=recvfrom_block;;
  esac
  for rep in 1 2 3; do
    echo "### $name rep$rep" | tee -a "$out"
    ./build/wake_probe build/wake_probe.bpf.o "$n" "$pace" "$mode" | tee -a "$out"
    echo | tee -a "$out"
  done
done

echo "raw results: $out"
echo
echo "host:"
grep -m1 'model name' /proc/cpuinfo
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>/dev/null || true
uname -r
