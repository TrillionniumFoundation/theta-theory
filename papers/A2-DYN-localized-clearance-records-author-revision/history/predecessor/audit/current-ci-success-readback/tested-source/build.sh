#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1
python3 -B tools/validate_revision.py all --output "$PWD/build/current"
python3 -B tools/rebuild_preserved_history.py --output "$PWD/build/current-history"
