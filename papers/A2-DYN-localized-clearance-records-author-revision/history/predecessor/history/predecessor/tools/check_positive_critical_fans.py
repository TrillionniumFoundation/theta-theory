#!/usr/bin/env python3
"""Finite exact algebra checks for the positive marked critical-fan proof.

The rational optical inputs below verify matrix algebra in the proved
physical parameter ranges; they are not claimed to be realized collision
words.  Analytic continuation, actual source coverage, and limit arguments
are supplied by the native proof, not certified by this finite program.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys


COUNTS: Counter[str] = Counter()


def check(name: str, condition: bool) -> None:
    if not condition:
        raise RuntimeError("Mathematical check failed: " + name)
    COUNTS[name] += 1


def mul(a: tuple[F, F, F, F], b: tuple[F, F, F, F]) -> tuple[F, F, F, F]:
    aa, ab, ac, ad = a
    ba, bb, bc, bd = b
    return aa * ba + ab * bc, aa * bb + ab * bd, ac * ba + ad * bc, ac * bb + ad * bd


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sigma, t_min = F(47, 59), F(3, 50)
    r_min, r_max, k_min = F(9, 20), F(47, 100), F(100, 47)
    e_star_sq = F(94**2, 1827)
    check("physical_constants", 1 + 2 * t_min / r_max == 1 / sigma)
    check("physical_constants", e_star_sq * k_min**2 * F(1827, 40000) == 1)
    check("physical_constants", (F(28, 5) + r_max) / (2 * r_min) == F(607, 90))
    check("physical_constants", F(170, 18) == F(170, 9) / 2)

    halves = []
    for radius in (r_min, F(23, 50), r_max):
        for first in (F(1, 4), F(1, 2), F(1), F(2)):
            check("first_foot_standoff", first**2 >= F(1827, 40000))
            for length in range(1, 9):
                matrix = (F(1), first, F(0), F(1))
                for i in range(length - 1):
                    flight = (F(3, 50), F(1, 10), F(2, 5), F(1))[i % 4]
                    incidence = (F(1), F(1, 2), F(1, 7), F(1, 31))[i % 4]
                    kick = 2 / (radius * incidence)
                    matrix = mul((1 + flight * kick, flight, kick, F(1)), matrix)
                a, b, c, d = matrix
                terminal_c = (F(1), F(1, 3), F(1, 11))[length % 3]
                ap, bp = b / radius + terminal_c * d, a / radius + terminal_c * c
                check("optical_determinant_one", a * d - b * c == 1)
                check("positive_optical_scalars", ap > 0 and bp > 0 and b > 0)
                check("half_expansion", b >= first * sigma ** (-(length - 1)))
                check("terminal_momentum_lower_bound", ap >= k_min * first * sigma ** (-(length - 1)))
                check("half_ratio", F(1) / (F(28, 5) + r_max) <= bp / ap <= 1 / first)
                halves.append((radius, ap, bp))

    for index, (radius, am, bm) in enumerate(halves):
        _, ap, bp = halves[(17 * index + 13) % len(halves)]
        for mark_sign in (-1, 1):
            for initial_sign in (-1, 1):
                for terminal_sign in (-1, 1):
                    determinant = (initial_sign * am) * (-mark_sign * terminal_sign * bp) - (mark_sign * initial_sign * bm) * (terminal_sign * ap)
                    positive_sum = am * bp + ap * bm
                    check("signed_two_half_determinant", abs(determinant) == positive_sum)
                    ux = 1 / (radius * positive_sum)
                    check("true_inverse_weight", ux == 1 / (radius * am * ap * (bm / am + bp / ap)))
                    check("physical_foot_upper_bound", ux <= F(607, 90) / (am * ap))

    for a in range(2, 12):
        for d in range(2, 12):
            for off in range(-4, 5):
                determinant = F(a * d - off**2)
                if determinant <= 0:
                    continue
                for radius in (r_min, F(23, 50), r_max):
                    omega = F(1, 3)
                    ux = radius**2 * omega / determinant
                    j_squared_first = omega**2 / (4 * determinant)
                    j_squared_inverse = determinant * ux**2 / (4 * radius**4)
                    check("one_conditioning_factor_normalization", j_squared_first == j_squared_inverse)
                for slope in (F(-3, 2), F(-1, 3), F(0), F(2, 5), F(7, 3)):
                    x, y = F(1), slope
                    gx, gy = a * x + off * y, off * x + d * y
                    lhs = a * gy**2 - 2 * off * gx * gy + d * gx**2
                    rhs = determinant * (a * x**2 + 2 * off * x * y + d * y**2)
                    check("gauss_angle_cofactor", lhs == rhs)

    for m in range(1, 81):
        exact_sum = sum((sigma ** max(j, m - 1 - j) for j in range(m)), F(0))
        half = m // 2
        if m % 2 == 0:
            formula = 2 * sigma**half * (1 - sigma**half) / (1 - sigma)
        else:
            formula = sigma**half + 2 * sigma ** (half + 1) * (1 - sigma**half) / (1 - sigma)
        check("all_mark_finite_series", exact_sum == formula)
        check("all_mark_geometric_normalization", exact_sum**2 <= m**2 * sigma ** (m - 1))
        for j in range(m):
            check("correct_half_collision_counts", (j + 1) + (m - j) == m + 1)
            check("minimum_uses_maximum_depth", min(sigma**j, sigma ** (m - 1 - j)) == sigma ** max(j, m - 1 - j))
            h, e = F(7), F(4)
            for count in (1, 3, 8):
                a_cap = min(e * sigma**j, h / count)
                b_cap = min(e * sigma ** (m - 1 - j), h / count)
                aa = [a_cap * F(i + 1, count) for i in range(count)]
                bb = [b_cap * F(count - i, count) for i in range(count)]
                check("finite_two_half_sum_transfer", sum(a * b for a, b in zip(aa, bb)) <= h * e * sigma ** max(j, m - 1 - j))

    # An explicit analytic cone with a collapsed zero-level slice, solely
    # illustrating the sign-cell mechanism.  This is not a Lorentz orbit.
    for numerator in range(-9, 10):
        slope = F(numerator, 10)
        for power in range(1, 25):
            clearance = F(1, 2**power)
            angle = slope * clearance
            check("illustrative_collapsed_slice_representative", clearance > 0 and clearance - angle > 0 and clearance + angle > 0)

    result = {
        "status": "passed",
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "optimized": sys.flags.optimize > 0,
        "source": str(args.source),
        "source_sha256": digest(args.source),
        "program_sha256": digest(Path(__file__)),
        "counts": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "scope": "finite exact rational optical, coarea, half-count, and full-index algebra; one explicitly illustrative analytic cone",
        "optical_input_cases_are_realized_orbits": False,
        "continuum_proof_certification": False,
        "full_raw_pointwise_llt_proved": False,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
