#!/usr/bin/env python3
"""Normalize one exact-rereview installation marker in both driver and verifier."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = '"all primitive triangular-lattice direction"'
NEW = '"For a primitive lattice direction"'
changed = 0
for rel in (
    "tools/apply_round3_exact_rereview_fixes.py",
    "tools/verify_round3_rereview.py",
):
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if OLD in text:
        text = text.replace(OLD, NEW)
        changed += 1
    if OLD in text or NEW not in text:
        raise SystemExit(f"exact-rereview marker normalization failed in {rel}")
    compile(text, str(path), "exec")
    path.write_text(text, encoding="utf-8")
print(f"ROUND3_REREVIEW_MARKER_REPAIR_PASS changed={changed}")
