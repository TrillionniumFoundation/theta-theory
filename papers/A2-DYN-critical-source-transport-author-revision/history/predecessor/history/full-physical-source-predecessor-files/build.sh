#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 tools/validate_revision.py all --output "$PWD/build/current"
python3 history/historical-v108/rebuild_history.py
