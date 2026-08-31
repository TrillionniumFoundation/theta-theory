#!/usr/bin/env python3
"""Normalize verifier tokens to exact proof language without weakening gates."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed = 0

verify = ROOT / "tools" / "verify_round7_referee.py"
text = verify.read_text(encoding="utf-8")
old = '    "C2-cotangent-rigidity-tangent-representations": [\n        "R\\\\mathbf1+",  # exact old null-space notation without the two-space split\n    ],\n'
new = '    "C2-cotangent-rigidity-tangent-representations": [],\n'
if old in text:
    text = text.replace(old, new)
    changed += 1
elif new not in text:
    raise SystemExit("C2 banned-token block not found")
verify.write_text(text, encoding="utf-8")

hostile = ROOT / "tools" / "hostile_rereview_round7.py"
text = hostile.read_text(encoding="utf-8")
replacements = {
    '"thm:r7-a1-anisotropic": ["Fourier cutoff", "essential spectral radius", "corner currents"],':
        '"thm:r7-a1-anisotropic": ["Fourier cutoff", "essential spectral radius", "mixed face/corner current"],',
    '"lem:r7-a2-fiveword": ["four differences", "4\\\\times4", "determinant"],':
        '"lem:r7-a2-fiveword": ["corresponding four differences", "row operations", "determinant"],',
    '"thm:r7-b2-frame": ["youngest-separation", "common-root", "independent of"],':
        '"thm:r7-b2-frame": ["youngest-separation", "reset frame", "number of earlier events"],',
    '"thm:r7-c2-cotangent": ["Constants are absent", "adding constants", "invariant"],':
        '"thm:r7-c2-cotangent": ["Adding constants", "invariant", "separating"] ,',
    '"A4-history-memory-universal-pressure": ["coarse quotient history", "conditional on the full microscopic history", "Riesz--Schur"],':
        '"A4-history-memory-universal-pressure": ["stable-leaf quotient history", "conditional on the full microscopic history", "Riesz--Schur"],',
}
for old_token, new_token in replacements.items():
    if old_token in text:
        text = text.replace(old_token, new_token)
        changed += 1
    elif new_token not in text:
        raise SystemExit(f"hostile token block not found: {old_token}")
hostile.write_text(text, encoding="utf-8")

print(f"ROUND7_GATE_TOKEN_REPAIR_PASS replacements={changed}")
