#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PORT="${PORT:-8000}"
HOST="${HOST:-0.0.0.0}"
RELOAD="${RELOAD:-}"
ENV_FILE="${ENV_FILE:-}"
APP="${APP:-main:app}"
FIND_PORT="${FIND_PORT:-}"

while [ "${1-}" != "" ]; do
  case "$1" in
    --port) PORT="$2"; shift 2;;
    --host) HOST="$2"; shift 2;;
    --reload) RELOAD=1; shift;;
    --env) ENV_FILE="$2"; shift 2;;
    --app) APP="$2"; shift 2;;
    --find-port) FIND_PORT=1; shift;;
    *) shift;;
  esac
done

if [ -f ".env" ]; then
  set -a; . ".env"; set +a
fi
if [ -n "$ENV_FILE" ] && [ -f "$ENV_FILE" ]; then
  set -a; . "$ENV_FILE"; set +a
fi

export THIRD_PARTY_BASE_URL="${THIRD_PARTY_BASE_URL:-}"
export THIRD_PARTY_API_KEY="${THIRD_PARTY_API_KEY:-}"

if [ -n "$FIND_PORT" ]; then
  TRY="$PORT"
  while lsof -i ":$TRY" >/dev/null 2>&1; do
    TRY="$((TRY+1))"
  done
  PORT="$TRY"
fi

ARGS=("--host" "$HOST" "--port" "$PORT")
if [ -n "$RELOAD" ]; then
  ARGS+=("--reload")
fi

echo "Launching $APP on http://$HOST:$PORT"
exec python3 -m uvicorn "$APP" "${ARGS[@]}"
