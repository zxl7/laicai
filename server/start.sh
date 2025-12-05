#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

VENV_DIR="${VENV_DIR:-server/.venv}"
PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
RELOAD="${RELOAD:-}"

if [ ! -x "$VENV_DIR/bin/python" ]; then
  python3 -m venv "$VENV_DIR"
fi

REQ_FILE="${REQ_FILE:-server/requirements.txt}"
"$VENV_DIR/bin/pip" install -r "$REQ_FILE" >/dev/null

if [ -f ".env" ]; then
  set -a
  . ".env"
  set +a
fi
if [ -f "server/.env" ]; then
  set -a
  . "server/.env"
  set +a
fi

export THIRD_PARTY_BASE_URL="${THIRD_PARTY_BASE_URL:-}"
export THIRD_PARTY_API_KEY="${THIRD_PARTY_API_KEY:-}"

ARGS=("--host" "$HOST" "--port" "$PORT")
if [ -n "$RELOAD" ]; then
  ARGS+=("--reload")
fi

exec "$VENV_DIR/bin/python" -m uvicorn main:app "${ARGS[@]}"
