#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec python3 tools/qualify_revision.py "${1:-all}"
