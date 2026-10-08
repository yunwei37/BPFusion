#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# BPFusion LLM-path bench: packet -> tc/eBPF -> pinned page -> resident Qwen
# executor -> tokens back through the page, vs a direct in-process baseline.
#
#   ./bench/run_llm.sh [seconds] [gen] [rounds] [model]
set -u
SECS=${1:-60}
GEN=${2:-32}
ROUNDS=${3:-8}
MODEL=${4:-Qwen/Qwen2.5-0.5B-Instruct}
PORT=39400
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT="$ROOT/bench/results/llm_$(date -u +%Y%m%dT%H%M%SZ).txt"

cd "$ROOT"
export HOME=/root
export PYTHONPATH="$ROOT/executor"

pkill -f llm_executor 2>/dev/null; sleep 0.3
./build/bpfusion_load detach lo >/dev/null 2>&1
./build/bpfusion_load attach lo >/dev/null 2>&1 || exit 1

stdbuf -oL -eL python3 executor/llm_executor.py --model "$MODEL" --seconds "$SECS" \
  > /tmp/bpfusion_llm_exec.log 2>&1 &
EXEC=$!
for _ in $(seq 1 60); do
  grep -q "model loaded" /tmp/bpfusion_llm_exec.log && break
  sleep 1
done

{
  echo "=== BPFusion LLM path, $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  echo "model=$MODEL gen=$GEN rounds=$ROUNDS"
  echo "executor: $(grep 'model loaded' /tmp/bpfusion_llm_exec.log)"
  echo
  python3 tools/llm_bench.py --model "$MODEL" --gen "$GEN" --rounds "$ROUNDS"
  echo
  echo "=== executor tail ==="
  tail -3 /tmp/bpfusion_llm_exec.log
} | tee "$OUT"

kill "$EXEC" 2>/dev/null
echo "saved $OUT"
