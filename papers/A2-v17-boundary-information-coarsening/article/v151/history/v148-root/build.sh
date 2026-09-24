#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
python revision_v148.py build
