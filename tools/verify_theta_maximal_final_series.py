#!/usr/bin/env python3
"""Structural verifier for the final θ-Theory strengthening bindings.

This verifier checks files, paper bindings, exact-scope guardrails and selected
formula anchors.  It does not certify analytical proofs or replace review.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = ROOT / "papers" / "theta-program" / "maximal-strengthening"
SERIES = ROOT / "papers" / "theta-program" / "five-paper-series"

REQUIRED_MAX = {
    "FINAL_LATEST_WINS_CLOSURE.md": (
        "Theorem S-RADIAL-U3",
        "Theorem HF-SIMILARITY-BDL",
        "Theorem OPT-RWIP-GAUSS",
        "Theorem PURE-SADDLE-IFF",
        "Theorem THETA-MAXIMAL-FINAL-CLOSURE",
    ),
    "FINAL_SCOPE_CORRECTIONS.md": (
        "generic noncoboundary operator U3",
        "full W_1",
        "one-step prediction forgetting",
    ),
    "final_maximal_closure_packet_v2.yaml": (
        "remaining_internal_mathematical_gaps: 0",
        "external_peer_review: NOT_PERFORMED",
    ),
    "FINAL_PAPER_BINDING_MANIFEST.yaml": (
        "bound_into_papers: 5",
        "unresolved_named_imports: 0",
    ),
    "FINAL_FORMULA_AUDIT_RECEIPT.json": (
        "period_two_monodromy_trace_matrix_multiplication",
        "Cole_Hopf_quadratic_gradient_cancellation",
    ),
}

REQUIRED_PAPERS = {
    "paper-I-cm2-u3/FINAL_ADDENDUM_SPECULAR_RADIAL_U3.md": (
        "P1-SINAI-RADIAL-U3-EXACT",
        "not a claim of arbitrary noncoboundary",
    ),
    "paper-II-pressure-diffusion/FINAL_ADDENDUM_EXACT_HIGH_FREQUENCY_BDL.md": (
        "P2-BDL-HF-SIMILARITY",
        "exact identity",
    ),
    "paper-III-rough-theta/FINAL_ADDENDUM_OPTIMAL_GAUSSIAN_RWIP.md": (
        "P3-RWIP-OPTIMAL-WETA-P",
        "Kantorovich duality",
    ),
    "paper-IV-filter-games/FINAL_ADDENDUM_PURE_WEIGHTED_ACTUAL.md": (
        "P4-PURE-ISAACS-MAXIMAL",
        "exactly after one prediction-update cycle",
    ),
    "paper-V-representations/FINAL_ADDENDUM_ENTROPIC_PATH_ACTUAL.md": (
        "P5-PATH-ACTUAL",
        "Cole-Hopf transform",
    ),
}

FORBIDDEN_OVERCLAIMS = {
    "arbitrary noncoboundary full reduced resolvent is proved",
    "generic nonconjugate BDL follows from compactness alone",
    "pure saddle exists for every continuous game",
    "same optimal rate in every rough path topology",
}


def inspect(path: Path, anchors: tuple[str, ...], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    for anchor in anchors:
        if anchor not in text:
            errors.append(f"missing anchor {anchor!r}: {path.relative_to(ROOT)}")
    for bad in FORBIDDEN_OVERCLAIMS:
        if bad in text:
            errors.append(f"forbidden overclaim {bad!r}: {path.relative_to(ROOT)}")


def main() -> int:
    errors: list[str] = []
    for name, anchors in REQUIRED_MAX.items():
        inspect(MAX / name, anchors, errors)
    for name, anchors in REQUIRED_PAPERS.items():
        inspect(SERIES / name, anchors, errors)

    formula_script = ROOT / "tools" / "verify_theta_maximal_final_closure.py"
    if not formula_script.is_file():
        errors.append("missing formula verifier")
    else:
        proc = subprocess.run(
            [sys.executable, str(formula_script), "--formula-only"],
            check=False,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            errors.append("formula verifier failed: " + proc.stdout + proc.stderr)

    result = {
        "schema": "THETA_MAXIMAL_FINAL_SERIES_VERIFY_V1",
        "status": "PASS" if not errors else "FAIL",
        "former_strengthening_frontiers": 5,
        "paper_addenda": 5,
        "errors": errors,
        "mathematical_proof_verified": False,
        "external_peer_review": "NOT_PERFORMED",
        "formal_credit": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
