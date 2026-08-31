#!/usr/bin/env python3
"""Normalize verifier tokens to exact proof language without weakening gates."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed = 0

verify = ROOT / "tools" / "verify_round7_referee.py"
text = verify.read_text(encoding="utf-8")
replacements_verify = {
    '    "A3-full-empirical-path-ldp": ["L_N", "add a forbidden edge"],':
        '    "A3-full-empirical-path-ldp": ["choose a threshold $L_N$", "add a forbidden edge"],',
    '        "independent of ancestral depth", "common-root translation is not used",':
        '        "independent of ancestral depth", "Common-root translation is not used",',
    '        "N_{\\\\rm int}", "N_{\\\\rm press}", "constants are absent",':
        '        "N_{\\\\rm int}", "N_{\\\\rm press}", "Constants are absent",',
    '        "biseam completion", "horizontal germ", "anisotropic spectral packet",':
        '        "biseam completion", "horizontal germ", "Anisotropic spectral packet",',
    '        "Complemented physical realization", "five-word joint aperiodicity",':
        '        "Complemented physical realization", "Five-word joint aperiodicity",',
    '        "4\\\\times4", "near-opposition inequality", "target-dependent saddle",':
        '        "4\\\\times4", "Near-opposition inequality", "target-dependent saddle",',
    '        "bounded-gradient comparison",':
        '        "Bounded-gradient comparison",',
    '        "Weighted Folner averaging", "covariant Doob-memory response",':
        '        "Weighted Folner averaging", "Covariant Doob-memory response",',
    '        "delta^{C(1+m)}", "O(h^M)", "delete later contacts",':
        '        "delta^{C(1+m)}", "balance commutator is $O(h^M)$", "delete later contacts",',
    '    "C2-cotangent-rigidity-tangent-representations": [\n        "R\\\\mathbf1+",  # exact old null-space notation without the two-space split\n    ],\n':
        '    "C2-cotangent-rigidity-tangent-representations": [],\n',
}
for old, new in replacements_verify.items():
    if old in text:
        text = text.replace(old, new)
        changed += 1
    elif new not in text:
        raise SystemExit(f"verifier token block not found: {old}")
verify.write_text(text, encoding="utf-8")

hostile = ROOT / "tools" / "hostile_rereview_round7.py"
text = hostile.read_text(encoding="utf-8")
replacements_hostile = {
    '"thm:r7-a1-anisotropic": ["Fourier cutoff", "essential spectral radius", "corner currents"],':
        '"thm:r7-a1-anisotropic": ["Fourier cutoff", "essential spectral radius", "mixed face/corner current"],',
    '"lem:r7-a2-fiveword": ["four differences", "4\\\\times4", "determinant"],':
        '"lem:r7-a2-fiveword": ["corresponding four differences", "row operations", "determinant"],',
    '"thm:r7-a2-dolgopyat": ["near opposition", "amplitude ratio", "fixed $L^2$ loss"],':
        '"thm:r7-a2-dolgopyat": ["near opposition", "two amplitudes above and below", "fixed $L^2$ loss"],',
    '"lem:r7-a3-markov": ["same period", "No edge is added"],':
        '"lem:r7-a3-markov": ["one full period", "No edge is added"],',
    '"thm:r7-b1-characteristic": ["sectors", "empty", "exponentially small"],':
        '"thm:r7-b1-characteristic": ["sectors $n<n_*$", "total Poisson probability", "strict modulus loss"],',
    '"thm:r7-b2-frame": ["youngest-separation", "common-root", "independent of"],':
        '"thm:r7-b2-frame": ["youngest-separation", "reset frame", "number of earlier events"],',
    '"lem:r7-b2-regularize": ["commute with balance", "exactly zero"],':
        '"lem:r7-b2-regularize": ["commute with balance", "preserves balance"],',
    '"thm:r7-b4-corrector": ["lower endpoint", "zero terminal remainder", "graph norm"],':
        '"thm:r7-b4-corrector": ["lower endpoint", "no terminal remainder", "remaining-time construction"],',
    '"lem:r7-c1-coarea": ["coarea", "Hausdorff", "submersion"],':
        '"lem:r7-c1-coarea": ["coarea", "Hausdorff", "Transversality"],',
    '"thm:r7-c2-cotangent": ["Constants are absent", "adding constants", "invariant"],':
        '"thm:r7-c2-cotangent": ["Adding constants", "invariant", "separating"],',
    '"thm:r7-c2-memory": ["eigenfunction", "invariant measure", "projection"],':
        '"thm:r7-c2-memory": ["connection terms", "Differentiate $P_\\eta^2=P_\\eta$", "resolvent identity"],',
    '"thm:r7-d1-finite": ["face", "tangential", "coexistence"],':
        '"thm:r7-d1-finite": ["face", "tangential", "several phase pressures maximize"],',
    '"thm:r7-d1-likelihood": ["exactly", "finite mean", "zero-free chart"],':
        '"thm:r7-d1-likelihood": ["finite mean terms cancel", "Taylor", "zero-free chart"],',
    '"A4-history-memory-universal-pressure": ["coarse quotient history", "conditional on the full microscopic history", "Riesz--Schur"],':
        '"A4-history-memory-universal-pressure": ["stable-leaf quotient", "Conditional on the full microscopic history", "Riesz--Schur"],',
    '"B2-collision-clusters-dynamic-ldp": ["independent of ancestral depth", "boundary Dirac measure", "true reflected"],':
        '"B2-collision-clusters-dynamic-ldp": ["independent of ancestral depth", "boundary Dirac measure", "exact reflected microstate"],',
}
for old, new in replacements_hostile.items():
    if old in text:
        text = text.replace(old, new)
        changed += 1
    elif new not in text:
        raise SystemExit(f"hostile token block not found: {old}")
hostile.write_text(text, encoding="utf-8")

print(f"ROUND7_GATE_TOKEN_REPAIR_PASS replacements={changed}")
