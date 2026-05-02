#!/usr/bin/env bash
set -euo pipefail
PORT=1717
BIND=0.0.0.0
HOST_IP="${HUGO_HOST_IP:-192.168.100.159}"
exec hugo server --bind "$BIND" --port "$PORT" --baseURL "http://${HOST_IP}:${PORT}/" "$@"
