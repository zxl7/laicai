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
PY_BIN="${PY_BIN:-}"
RELOAD_INCLUDE="${RELOAD_INCLUDE:-}"
RELOAD_EXCLUDE="${RELOAD_EXCLUDE:-}"

while [ "${1-}" != "" ]; do
  case "$1" in
    --port) PORT="$2"; shift 2;;
    --host) HOST="$2"; shift 2;;
    --reload) RELOAD=1; shift;;
    --env) ENV_FILE="$2"; shift 2;;
    --app) APP="$2"; shift 2;;
    --find-port) FIND_PORT=1; shift;;
    --py) PY_BIN="$2"; shift 2;;
    --reload-include) RELOAD_INCLUDE="$2"; shift 2;;
    --reload-exclude) RELOAD_EXCLUDE="$2"; shift 2;;
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

if [ -n "${REQUESTS_CA_BUNDLE:-}" ] && [[ "$REQUESTS_CA_BUNDLE" == */.venv/* ]]; then unset REQUESTS_CA_BUNDLE; fi
if [ -n "${SSL_CERT_FILE:-}" ] && [[ "$SSL_CERT_FILE" == */.venv/* ]]; then unset SSL_CERT_FILE; fi
CERT_PATH=$(python3 -c 'import certifi,sys; print(certifi.where())' 2>/dev/null || true)
if [ -n "$CERT_PATH" ]; then
  export REQUESTS_CA_BUNDLE="$CERT_PATH"
  export SSL_CERT_FILE="$CERT_PATH"
fi

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
  if [ -n "$RELOAD_INCLUDE" ]; then
    ARGS+=("--reload-include" "$RELOAD_INCLUDE")
  fi
  if [ -n "$RELOAD_EXCLUDE" ]; then
    ARGS+=("--reload-exclude" "$RELOAD_EXCLUDE")
  else
    ARGS+=("--reload-exclude" ".venv|__pycache__|.git|*.log")
  fi
fi

echo "Launching $APP on http://$HOST:$PORT"
# choose python interpreter
if [ -z "$PY_BIN" ]; then
  if command -v python3.11 >/dev/null 2>&1; then
    PY_BIN="python3.11"
  elif [ -x "/usr/local/opt/python@3.11/bin/python3.11" ]; then
    PY_BIN="/usr/local/opt/python@3.11/bin/python3.11"
  else
    PY_BIN="python3"
  fi
fi
exec "$PY_BIN" -m uvicorn "$APP" "${ARGS[@]}"
