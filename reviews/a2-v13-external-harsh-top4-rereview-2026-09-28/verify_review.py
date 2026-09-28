#!/usr/bin/env python3
"""Independent exact-rational diagnostics for the A2 v13 rereview.

This script is intentionally narrow.  It checks the printed two-flight
Schur/action/twist block on a positive-rational grid.  It does not import
the manuscript's verification modules and is not a proof certificate,
a nonlinear billiard simulation, a TeX build, or a journal decision.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
from typing import Any


def block(c0: F, c1: F, g: F, m: int) -> list[list[F]]:
    z = c0 * c1 - 1
    scales = [g / (2 * c0 * z), g / (2 * c1 * z)]
    k = F(4, 2**m * (m + 1) * math.factorial(m) ** 2)
    u = (1 + 2 * z) ** m
    v = 1 + 2 * m * z
    return [
        [-u * k * scales[0] ** m, -v * k * scales[1] ** m],
        [-v * k * scales[0] ** m, -u * k * scales[1] ** m],
    ]


def schur_row(c0: F, c1: F, g: F, m: int, orientation: int) -> tuple[list[F], F, F, F]:
    cb, co = [c0, c1][orientation], [c0, c1][1 - orientation]
    h = (cb - F(1, 2) / co) / g
    off = -F(1, 2) / (co * g)
    det = h * h - off * off
    inv00, inv01 = h / det, -off / det
    nu_endpoint = inv00
    nu_middle = (inv00 + inv01) / (2 * co * co)

    k = F(4, 2**m * (m + 1) * math.factorial(m) ** 2)
    own = -k * nu_endpoint**m
    other_action = -k * nu_middle**m
    other_twist = (
        -(g / co)
        * F(4, 2**m * (m + 1) * math.factorial(m) * math.factorial(m - 1))
        * nu_middle ** (m - 1)
    )
    row = [F(0), F(0)]
    row[orientation], row[1 - orientation] = own, other_action + other_twist
    return row, det, nu_endpoint, nu_middle


def require(name: str, condition: bool, category: str, checks: list[dict[str, str]]) -> None:
    if not condition:
        raise RuntimeError(f"failed exact check: {name}")
    checks.append({"name": name, "category": category, "status": "pass"})


def run() -> dict[str, Any]:
    checks: list[dict[str, str]] = []
    cases = 0
    for c0 in [F(11, 10), F(3, 2), F(2), F(4)]:
        for c1 in [F(11, 10), F(3, 2), F(2), F(4)]:
            for g in [F(1, 2), F(1), F(3, 2)]:
                z = c0 * c1 - 1
                for m in range(2, 16):
                    cases += 1
                    tag = f"c0={c0};c1={c1};g={g};m={m}"
                    u = (1 + 2 * z) ** m
                    v = 1 + 2 * m * z
                    remainder = sum(F(math.comb(m, r)) * (2 * z) ** r for r in range(2, m + 1))
                    require(f"separation_identity:{tag}", u - v == remainder, "separation_identity", checks)
                    require(f"separation_positive:{tag}", u - v > 0, "separation_positive", checks)

                    matrix = block(c0, c1, g, m)
                    require(
                        f"block_determinant:{tag}",
                        matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0] > 0,
                        "block_determinant",
                        checks,
                    )

                    for orientation in (0, 1):
                        row, det, nu_endpoint, nu_middle = schur_row(c0, c1, g, m, orientation)
                        cb, co = [c0, c1][orientation], [c0, c1][1 - orientation]
                        require(
                            f"schur_row:{tag};b={orientation}",
                            row == matrix[orientation],
                            "schur_row",
                            checks,
                        )
                        require(
                            f"schur_det:{tag};b={orientation}",
                            det == cb * z / (co * g * g),
                            "schur_det",
                            checks,
                        )
                        require(
                            f"endpoint_variance:{tag};b={orientation}",
                            nu_endpoint == g * (1 + 2 * z) / (2 * cb * z),
                            "endpoint_variance",
                            checks,
                        )
                        require(
                            f"middle_variance:{tag};b={orientation}",
                            nu_middle == g / (2 * co * z),
                            "middle_variance",
                            checks,
                        )

                    a, b = matrix[0]
                    c, d = matrix[1]
                    determinant = a * d - b * c
                    inverse = [[d / determinant, -b / determinant], [-c / determinant, a / determinant]]
                    require(
                        f"inverse_identity:{tag}",
                        all(
                            sum(inverse[i][k] * matrix[k][j] for k in (0, 1)) == int(i == j)
                            for i in (0, 1)
                            for j in (0, 1)
                        ),
                        "inverse_identity",
                        checks,
                    )

    grid_count = len(checks)
    require(
        "printed_quartic_example",
        block(F(2), F(2), F(1), 2)
        == [[-F(49, 1728), -F(13, 1728)], [-F(13, 1728), -F(49, 1728)]],
        "printed_example",
        checks,
    )
    identifiers = "\n".join(check["name"] for check in checks) + "\n"
    categories = dict(sorted(Counter(check["category"] for check in checks).items()))
    return {
        "schema": "a2-v13-external-review-exact-checks-v1",
        "status": "pass",
        "source_commit": "0e54099f079232df233316ae6fe7986fc51b7ea1",
        "grid": {
            "c0_values": ["11/10", "3/2", "2", "4"],
            "c1_values": ["11/10", "3/2", "2", "4"],
            "g_values": ["1/2", "1", "3/2"],
            "orders": [2, 15],
            "cases": cases,
            "grid_checks": grid_count,
        },
        "counts": {"total": len(checks), **categories},
        "identifier_sha256": hashlib.sha256(identifiers.encode()).hexdigest(),
        "limitations": [
            "These exact-rational diagnostics check only the displayed finite two-flight block.",
            "They do not certify the stationary implicit-function theorem, common Morse-domain argument, or all-order proof.",
            "They are not a TeX build, nonlinear billiard simulation, exhaustive literature search, or remote CI run.",
            "They do not support the abstract's universal finite-dimensional-family quantifier.",
        ],
        "_checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--full", action="store_true", help="include all individual check identifiers")
    args = parser.parse_args()
    result = run()
    checks = result.pop("_checks")
    if args.full:
        result["checks"] = checks
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(json.dumps({key: result[key] for key in ("status", "grid", "counts", "identifier_sha256") }, sort_keys=True))


if __name__ == "__main__":
    main()
