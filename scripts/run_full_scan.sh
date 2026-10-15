#!/usr/bin/env bash
# Offline scan of the older repositories. Local only (Ollama on 127.0.0.1); read-only on the scanned trees.
# Resumable: rerun the same command and finished files are skipped. Stop with Ctrl-C or `pkill -f "bvp scan"`.
#   MODEL=qwen3:14b scripts/run_full_scan.sh      # slower, a bit better (about 2x time)
set -euo pipefail
cd "$(dirname "$0")/.."
MODEL="${MODEL:-qwen3:8b}"
mkdir -p outputs/scan
LOG=outputs/scan/run.log
{
  echo "== $(date -Is) start model=$MODEL"
  curl -sf http://127.0.0.1:11434/api/tags >/dev/null || { echo "Ollama is not running: start it with 'ollama serve'"; exit 1; }
  uv run bvp scan inventory
  uv run bvp scan summarise --model "$MODEL"
  uv run bvp scan folders --model "$MODEL"
  uv run bvp scan embed
  uv run bvp scan results
  uv run bvp scan render
  uv run bvp scan status
  echo "== $(date -Is) done"
} 2>&1 | tee -a "$LOG"
