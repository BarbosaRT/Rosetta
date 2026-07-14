#!/usr/bin/env bash
# Starts the Rosetta API (FastAPI/uvicorn) with the real model, from the repo root.
# Usage:  ./scripts/serve_api.sh  [--ckpt path.ckpt] [--device cpu|cuda] [--port 8000]

set -euo pipefail

CKPT="checkpoints/crohme_rs/last.ckpt"
DEVICE="cpu"
PORT=8000

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ckpt)   CKPT="$2";   shift 2 ;;
    --device) DEVICE="$2"; shift 2 ;;
    --port)   PORT="$2";   shift 2 ;;
      *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

if [[ -f "$REPO/.venv/bin/python" ]]; then
  PYTHON="$REPO/.venv/bin/python"
elif [[ -f "$REPO/venv/bin/python" ]]; then
  PYTHON="$REPO/venv/bin/python"
else
  echo "ERROR: no Python venv found. Run 'uv sync' or 'python -m venv .venv' first." >&2
  exit 1
fi

if [[ ! -f "$CKPT" ]]; then
  echo "WARNING: checkpoint '$CKPT' not found — API will start in stub mode (501)." >&2
else
  export HMER_CKPT="$CKPT"
fi

export HMER_DEVICE="$DEVICE"
export PYTHONPATH="api/src:ml/src"

exec "$PYTHON" -m uvicorn hmer_api.main:app --host 127.0.0.1 --port "$PORT"
