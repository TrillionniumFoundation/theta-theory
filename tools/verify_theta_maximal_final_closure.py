#!/usr/bin/env python3
"""Fail-closed verifier for the final θ-Theory maximal-strengthening layer.

The script checks required files, latest-wins scope anchors and several exact
algebraic identities.  It does not verify analytical estimates, certify proofs,
or grant external theorem credit.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "papers" / "theta-program" / "maximal-strengthening"

REQUIRED = {
    "FINAL_LATEST_WINS_CLOSURE.md",
    "FINAL_SCOPE_CORRECTIONS.md",
    "final_maximal_closure_packet_v2.yaml",
}

SCOPE_ANCHORS = {
    "ACTUAL_NONCONJUGATE_PROJECTOR_SOURCE_U3",
    "generic noncoboundary operator U3",
    "HF-SIMILARITY-BDL",
    "full W_1",
    "pure saddle exists  <=>  H_minus = H_plus",
    "one-step prediction forgetting",
}


def matmul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def inv2(a: list[list[float]]) -> list[list[float]]:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if abs(det) < 1e-12:
        raise ValueError("singular 2x2 matrix")
    return [[a[1][1] / det, -a[0][1] / det], [-a[1][0] / det, a[0][0] / det]]


def matsub(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[a[i][j] - b[i][j] for j in range(2)] for i in range(2)]


def matscale(c: float, a: list[list[float]]) -> list[list[float]]:
    return [[c * a[i][j] for j in range(2)] for i in range(2)]


def eye_shift(z: float, a: list[list[float]]) -> list[list[float]]:
    return [[z - a[0][0], -a[0][1]], [-a[1][0], z - a[1][1]]]


def maxerr(a: list[list[float]], b: list[list[float]]) -> float:
    return max(abs(a[i][j] - b[i][j]) for i in range(2) for j in range(2))


def formula_checks() -> list[str]:
    errors: list[str] = []

    # Period-two monodromy trace.
    d, k1, k2 = 1.7, 0.8, 1.1
    F = [[1.0, d], [0.0, 1.0]]
    S1 = [[1.0, 0.0], [2.0 * k1, 1.0]]
    S2 = [[1.0, 0.0], [2.0 * k2, 1.0]]
    M = matmul(matmul(matmul(S1, F), S2), F)
    observed = M[0][0] + M[1][1]
    expected = 2.0 + 4.0 * d * (k1 + k2) + 4.0 * d * d * k1 * k2
    if abs(observed - expected) > 1e-12:
        errors.append("period-two trace identity")

    # Analytic radial derivative is strictly negative.
    R1, R2, d0 = 1.25, 0.9, 1.6
    derivative = (
        -4.0 * (1.0 / R1 + 1.0 / R2)
        -4.0 * d0 / (R1 * R1)
        -8.0 * d0 / (R1 * R2)
        -4.0 * d0 * d0 / (R1 * R1 * R2)
    )
    if not derivative < 0.0:
        errors.append("radial nonconjugacy derivative")

    # Exact similarity-resolvent identity in a finite-dimensional test.
    A = [[0.2, 0.7], [-0.4, 0.1]]
    C = [[1.3, 0.2], [0.1, 0.9]]
    Ci = inv2(C)
    s, z = 1.4, 2.3
    Aa = matscale(1.0 / s, matmul(matmul(C, A), Ci))
    lhs = inv2(eye_shift(z, Aa))
    rhs = matscale(s, matmul(matmul(C, inv2(eye_shift(s * z, A))), Ci))
    if maxerr(lhs, rhs) > 1e-11:
        errors.append("similarity resolvent identity")

    # Pure-game saddle and cross-term cancellation.
    mu, nu, K, p = 2.0, 3.0, 4.5, 1.7
    u, v = p / mu, -p / nu
    value = p * (u + v) - 0.5 * mu * u * u + 0.5 * nu * v * v
    expected_value = p * p / (2.0 * mu) - p * p / (2.0 * nu)
    if abs(value - expected_value) > 1e-12:
        errors.append("quadratic pure saddle value")
    du, dv = 0.31, -0.27
    monotone = (mu * du - K * dv) * du + (nu * dv + K * du) * dv
    if abs(monotone - (mu * du * du + nu * dv * dv)) > 1e-12:
        errors.append("saddle mixed-term cancellation")

    # Safe rough-path Sobolev window and exponent.
    p_s, eta = 12.0, 0.43
    if not (p_s > 6.0 and eta - 1.0 / p_s > 1.0 / 3.0 and eta < 0.5):
        errors.append("rough-path Sobolev window")
    rate = 0.5 - eta
    if not rate > 0.0:
        errors.append("positive optimal rough rate")

    # Cole-Hopf coefficient for sigma=1.
    c = 0.17
    theta = 2.0 * c
    residual_coefficient = -theta * c + 0.5 * theta * theta
    if abs(residual_coefficient) > 1e-14:
        errors.append("Cole-Hopf cancellation")

    # Observation likelihood is bounded and normalized by Gaussian symmetry.
    eps = 0.4
    if not (0.0 < (1.0 - eps) / 2.0 < (1.0 + eps) / 2.0 < 1.0):
        errors.append("observation nondegeneracy")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--formula-only", action="store_true")
    args = parser.parse_args()

    errors = formula_checks()
    observed: list[str] = []

    if not args.formula_only:
        for name in sorted(REQUIRED):
            path = BASE / name
            if not path.is_file():
                errors.append(f"missing required file: {name}")
            else:
                observed.append(name)
        correction = BASE / "FINAL_SCOPE_CORRECTIONS.md"
        if correction.is_file():
            text = correction.read_text(encoding="utf-8")
            for anchor in sorted(SCOPE_ANCHORS):
                if anchor not in text:
                    errors.append(f"missing scope anchor: {anchor}")

    result = {
        "schema": "THETA_MAXIMAL_FINAL_VERIFY_V1",
        "status": "PASS" if not errors else "FAIL",
        "mode": "formula-only" if args.formula_only else "full-checkout",
        "observed_files": observed,
        "errors": errors,
        "mathematical_proof_verified": False,
        "external_peer_review": "NOT_PERFORMED",
        "formal_credit": 0,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
