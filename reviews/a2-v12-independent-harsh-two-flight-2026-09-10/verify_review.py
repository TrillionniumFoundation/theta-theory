#!/usr/bin/env python3
"""Finite exact-rational diagnostics for the independent A2 v12 review.

No manuscript code is imported. The two-flight check expands the varying
stationary action and its mixed derivative, then integrates monomials using
a Gaussian-moment recurrence and exact ellipse-to-Gaussian conversion.
The report contains the all-order proof. These checks are not that proof,
a nonlinear billiard simulation, or a verification of all manuscript claims.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from math import comb, factorial
from pathlib import Path
from typing import Callable

CHECKS: list[dict[str, str]] = []


def check(name: str, condition: bool, category: str) -> None:
    if not condition:
        raise RuntimeError(f"Failed diagnostic: {name}")
    CHECKS.append({"name": name, "category": category, "status": "pass"})


def inverse2(a: list[list[F]]) -> list[list[F]]:
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if not det:
        raise ValueError("Singular matrix")
    return [[a[1][1] / det, -a[0][1] / det],
            [-a[1][0] / det, a[0][0] / det]]


def gaussian_moments(cov: list[list[F]]) -> Callable[[int, int], F]:
    @lru_cache(None)
    def moment(i: int, j: int) -> F:
        if i < 0 or j < 0:
            return F(0)
        if i == j == 0:
            return F(1)
        if (i + j) % 2:
            return F(0)
        if i:
            return ((i - 1) * cov[0][0] * moment(i - 2, j)
                    + j * cov[0][1] * moment(i - 1, j - 1))
        return (j - 1) * cov[1][1] * moment(0, j - 2)
    return moment


def ellipse_average(poly: dict[tuple[int, int], F], cov: list[list[F]],
                    residual: bool) -> F:
    """At d=1 divide the integral by pi/sqrt(det H), with H=cov^{-1}.

    For total degree 2k, radial integration gives 2/(k+2)! times the
    Gaussian moment with residual weight, and 2/(k+1)! without it.
    """
    gm = gaussian_moments(cov)
    out = F(0)
    for (i, j), coefficient in poly.items():
        if (i + j) % 2:
            continue
        k = (i + j) // 2
        out += coefficient * gm(i, j) * F(2, factorial(k + (2 if residual else 1)))
    return out


def mixed_derivative(poly: dict[tuple[int, int], F]) -> dict[tuple[int, int], F]:
    return {(i - 1, j - 1): i * j * v
            for (i, j), v in poly.items() if i and j}


def direct_two_flight_row(g: F, cb: F, co: F, m: int) -> tuple[list[F], list[list[F]]]:
    # Eliminate the single interior coordinate of the quadratic action.
    h = [[(cb - 1 / (2 * co)) / g, -1 / (2 * co * g)],
         [-1 / (2 * co * g), (cb - 1 / (2 * co)) / g]]
    cov = inverse2(h)
    d0 = F(1) / (2 * g * co)
    own = {(2 * m, 0): F(1, factorial(2 * m)),
           (0, 2 * m): F(1, factorial(2 * m))}
    # Envelope identity: the middle site occurs in each of the two lengths.
    middle = {(i, 2 * m - i):
              F(2 * comb(2 * m, i), factorial(2 * m)) / (2 * co) ** (2 * m)
              for i in range(2 * m + 1)}
    row = []
    for action in (own, middle):
        twist = {key: -value / d0 for key, value in mixed_derivative(action).items()}
        row.append(-ellipse_average(action, cov, False)
                   + ellipse_average(twist, cov, True))
    return row, cov


def sinh(lam: F, n: int) -> F:
    return (lam ** (-n) - lam ** n) / 2


def cosh(lam: F, n: int) -> F:
    return (lam ** (-n) + lam ** n) / 2


def run() -> dict:
    CHECKS.clear()
    # Direct finite action and twist computation, including unequal curvatures.
    for g in (F(1, 2), F(1), F(3, 2)):
        for c0, c1 in ((F(2), F(2)), (F(3, 2), F(7, 4)),
                       (F(5, 4), F(3)), (F(101, 100), F(103, 100)),
                       (F(4), F(6, 5))):
            z = c0 * c1 - 1
            ls = [g / (2 * c0 * z), g / (2 * c1 * z)]
            for m in range(2, 11):
                tag = f"g={g},c0={c0},c1={c1},m={m}"
                k = F(4, 2 ** m * (m + 1) * factorial(m) ** 2)
                u, v = (1 + 2 * z) ** m, 1 + 2 * m * z
                expected = [[-u * k * ls[0] ** m, -v * k * ls[1] ** m],
                            [-v * k * ls[0] ** m, -u * k * ls[1] ** m]]
                actual = []
                for b, (cb, co) in enumerate(((c0, c1), (c1, c0))):
                    row, cov = direct_two_flight_row(g, cb, co, m)
                    actual.append(row if b == 0 else list(reversed(row)))
                    check(f"endpoint_covariance:{tag},b={b}",
                          cov[0][0] == ls[b] * (1 + 2 * z), "two_flight")
                    middle_variance = sum(sum(r) for r in cov) / (2 * co) ** 2
                    check(f"middle_covariance:{tag},b={b}",
                          middle_variance == ls[1 - b], "two_flight")
                check("expanded_action_twist_block:" + tag, actual == expected, "two_flight")
                check("positive_binomial_gap:" + tag,
                      u - v == sum(F(comb(m, r)) * (2 * z) ** r for r in range(2, m + 1)) > 0,
                      "two_flight")
                det = actual[0][0] * actual[1][1] - actual[0][1] * actual[1][0]
                check("positive_determinant:" + tag,
                      det == k * k * ls[0] ** m * ls[1] ** m * (u * u - v * v) > 0,
                      "two_flight")
                inv = inverse2(actual)
                check("inverse_identity:" + tag,
                      all(sum(inv[i][r] * actual[r][j] for r in (0, 1)) == int(i == j)
                          for i in (0, 1) for j in (0, 1)), "two_flight")
    r0, _ = direct_two_flight_row(F(1), F(2), F(2), 2)
    check("disk_quartic_row", r0 == [-F(49, 1728), -F(13, 1728)], "two_flight")
    check("disk_quartic_antisymmetric", -r0[0] + r0[1] == F(1, 48), "two_flight")

    # Checks on the manuscript's limiting-block algebra; not an independent
    # reconstruction of the half-line analytic estimates.
    for lam in (F(1, 3), F(1, 2), F(2, 3), F(4, 5)):
        for m in range(2, 11):
            e = (lam ** (4 * (m - 1)) / (1 - lam ** (4 * (m - 1)))
                 - lam ** (4 * m) / (1 - lam ** (4 * m)))
            o = 1 / (2 * sinh(lam, 2 * (m - 1))) - 1 / (2 * sinh(lam, 2 * m))
            p = cosh(lam, 2 * m) / sinh(lam, 2 * m) + 2 * m * e
            q = 1 / sinh(lam, 2 * m) + 2 * m * o
            difference = (m * sinh(lam, m - 1) / cosh(lam, m - 1)
                          - (m - 1) * sinh(lam, m) / cosh(lam, m))
            check(f"limiting_antisymmetric_identity:{lam},{m}", p - q == difference > 0,
                  "limiting_block_algebra")
            plus = (cosh(lam, m) / sinh(lam, m)
                    + 2 * m * (lam ** (2 * (m - 1)) / (1 - lam ** (2 * (m - 1)))
                               - lam ** (2 * m) / (1 - lam ** (2 * m))))
            check(f"limiting_symmetric_identity:{lam},{m}", p + q == plus,
                  "limiting_block_algebra")

    # Integrated beta kernels for polynomial profiles.
    def poch_half(n: int) -> F:
        value = F(1)
        for i in range(n):
            value *= F(2 * i + 1, 2)
        return value
    for r in range(9):
        for s in range(9):
            h = 2 * poch_half(r) * poch_half(s) / factorial(r + s + 2)
            second = 2 * poch_half(r) * poch_half(s) / factorial(r + s)
            check(f"integrated_flux_second_derivative:{r},{s}",
                  h * (r + s + 2) * (r + s + 1) == second, "acquisition_algebra")
    for m in range(4, 13):
        nu = F(2 * m - 1, 2)
        check(f"profile_power:{m}", 2 + 1 / nu + 5 / nu == 2 + 6 / nu, "acquisition_algebra")
        check(f"modulus_balance:{m}", nu / (m + 2) == 1 - F(5, 2 * (m + 2)), "acquisition_algebra")
        check(f"pilot_power_gap:{m}", 2 + 6 / nu > 2 + F(2, m), "acquisition_algebra")
        # Positive-node extrapolation of constant terms for the retained pilot.
        for degree in range(m):
            total = sum(F((-1) ** (j - 1) * comb(m, j)) * j ** degree for j in range(1, m + 1))
            check(f"pilot_extrapolation:{m},{degree}", total == int(degree == 0), "acquisition_algebra")
    check("m4_profile_power", 2 + F(6) / F(7, 2) == F(26, 7), "acquisition_algebra")
    counts = dict(sorted(Counter(item["category"] for item in CHECKS).items()))
    return {
        "schema": "a2-v12-independent-review-diagnostics-v1",
        "status": "pass",
        "source_commit": "2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86",
        "counts": {"total": len(CHECKS), **counts},
        "two_flight_example": {"g": "1", "c0": "2", "c1": "2", "m": 2,
                               "row": [str(x) for x in r0], "antisymmetric_eigenvalue_magnitude": "1/48"},
        "check_list_sha256": hashlib.sha256(json.dumps(CHECKS, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest(),
        "limitations": [
            "Finite exact arithmetic does not prove the all-order statements or function-space estimates.",
            "No manuscript code was imported or author verification suite rerun.",
            "No nonlinear billiard simulation, PDF build, formal proof checking, or remote CI execution.",
            "The two-flight benchmark uses known labelled leading geometry and individually even contact graphs.",
            "No experiment domination, full-profile minimax bound, or stable global analytic continuation is asserted.",
            "The author's finite-bridge diagnostic uses related Jacobi and ellipse ingredients; this is a separate implementation, not a claim of independent mathematical foundations."
        ]
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("checks.json"))
    args = parser.parse_args()
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "counts": result["counts"]}, sort_keys=True))


if __name__ == "__main__":
    main()
