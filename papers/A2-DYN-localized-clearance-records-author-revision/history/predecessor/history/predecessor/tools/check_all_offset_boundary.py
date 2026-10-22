#!/usr/bin/env python3
"""Exact auxiliary checks for the physical all-offset boundary proof.

These computations verify finite algebraic identities, normalization factors,
and geometric-series budgets used in native modules 319--320.  They do not
certify the billiard growth theorem, continuum variation proof, physical
pairing construction, or the full raw pointwise local limit theorem.
No assertions are used, so optimized Python retains all checks.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import sys


def run_checks() -> dict:
    counts = defaultdict(int)

    def check(group: str, condition: bool, context: object = None) -> None:
        if not condition:
            raise ArithmeticError(f"{group}: failed at {context!r}")
        counts[group] += 1

    radius_min, radius_max = F(9, 20), F(47, 100)
    tau_min, sigma = F(3, 50), F(47, 59)
    k_min, foot_squared = F(100, 47), F(1827, 40000)
    check("family_constants", 1 + 2 * tau_min / radius_max == 1 / sigma)
    check("family_constants", 1 / (k_min * k_min * foot_squared) == F(94**2, 1827))
    check("family_constants", (F(28, 5) + radius_max) / (2 * radius_min) == F(607, 90))
    check("family_constants", 1 - F(1, 4)**2 / 2 > F(9, 10))
    check("family_constants", F(19, 100) == 1 - F(9, 10)**2)

    # Direct differentiation of A_1 = kappa*a+c using the independently
    # stated physical first-image a_s and c_s identities.
    for radius in (F(9, 20), F(23, 50), F(47, 100)):
        kappa = 1 / radius
        for clearance in (F(0), F(1, 2000), F(1, 100), F(3, 200)):
            for side in (-1, 1):
                b = side * (radius + clearance)
                for distance in (F(1, 4), F(1, 2), F(1), F(2), F(28, 5)):
                    for t in (F(i, 20) for i in range(-19, 20)):
                        p = 2 * t / (1 + t*t)
                        c = (1 - t*t) / (1 + t*t)
                        slope = kappa + c / distance
                        a_s = p + b*c / distance
                        c_s = -p * slope
                        derivative_direct = kappa*a_s + c_s
                        derivative_reduced = c*(kappa*b-p) / distance
                        check("first_momentum_derivative", derivative_direct == derivative_reduced)
                        check("positive_first_derivative", kappa*distance+c >= k_min*distance)

    # The tangent angle derivative as a function of the logarithmic slope
    # ratio is ab/(a^2+b^2), bounded by 1/2 without a scale condition.
    for a in range(1, 81):
        for b in range(1, 81):
            sensitivity = F(a*b, a*a+b*b)
            check("tangent_log_sensitivity", F(0) < sensitivity <= F(1, 2))
            check("tangent_log_defect", F(1, 2)-sensitivity == F((a-b)**2, 2*(a*a+b*b)))

    # Coordinate-invariant cofactor identity and the precise inverse metric.
    for a in range(1, 8):
        for d in range(1, 8):
            for b in range(-6, 7):
                determinant = a*d-b*b
                if determinant <= 0:
                    continue
                for x, y in ((1, 0), (0, 1), (1, 1), (2, -3), (-3, 4)):
                    norm2 = x*x+y*y
                    transverse = F(d*x*x-2*b*x*y+a*y*y, norm2)
                    inverse_metric = F(d*x*x-2*b*x*y+a*y*y, determinant*norm2)
                    check("gauss_cofactor", transverse / determinant == inverse_metric)
                    # lambda_max <= trace is enough to test the upper-bound
                    # conversion 1/h_x <= Lambda/R^2 at a valid Lambda.
                    check("inverse_metric_bound", inverse_metric >= F(1, a+d))

    # Exact local identity underlying the triangular-angle turning proof.
    # h'(delta)=sign(sin(delta))*(psi'-alpha') away from its corners.
    for x in range(-3, 4):
        for y in range(-3, 4):
            if x == y == 0:
                continue
            for u in range(-3, 4):
                for v in range(-3, 4):
                    if u == v == 0:
                        continue
                    cross = x*v-y*u
                    if not cross:
                        continue
                    alpha_prime = F(cross, x*x+y*y)
                    sign = 1 if cross > 0 else -1
                    for a, b in ((0, 0), (1, 0), (0, 1), (-2, 3)):
                        psi_prime = F(u*b-v*a, u*u+v*v)
                        h_prime = sign*(psi_prime-alpha_prime)
                        check("turning_differential_identity", abs(alpha_prime) == sign*psi_prime-h_prime)

    # The complete flight-depth sum has factor 2, including m=1 and empty
    # depth ranges.  This uses exact rational arithmetic at every count.
    for m in range(1, 121):
        for depth in range(0, m+2):
            actual = sum((sigma**j+sigma**(m-1-j)
                          for j in range(m) if min(j, m-1-j) >= depth), F(0))
            upper = 2*sigma**depth/(1-sigma)
            check("complete_depth_series", actual <= upper, (m, depth))
            if 2*depth <= m-1:
                exact = 2*sigma**depth*(1-sigma**(m-2*depth))/(1-sigma)
                check("finite_depth_series_identity", actual == exact, (m, depth))
            else:
                check("empty_depth_series", actual == 0, (m, depth))

    # Analytic normal form: an offset can have unbounded pointwise turning
    # while its full positive turning is bounded.  These values illustrate
    # the proof's measure distinction; they are not Lorentz trajectory data.
    offset_examples = []
    for exponent in (0, 2, 4, 8, 12):
        offset = 10.0**(-exponent)
        total_turning = 2*math.atan(1/offset)
        check("affine_offset_turning", 0 < total_turning < math.pi)
        offset_examples.append({"offset": offset, "peak_turning_density": 1/offset,
                                "turning_on_minus_one_one": total_turning})

    return {
        "status": "passed",
        "scope": "finite exact algebra and normalization checks; analytic illustrative offset values",
        "continuum_proof_certification": False,
        "full_raw_pointwise_llt_proved": False,
        "counts": dict(sorted(counts.items())),
        "total_checks": sum(counts.values()),
        "offset_normal_form_only": offset_examples,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source", type=Path)
    args = parser.parse_args()
    result = run_checks()
    result.update({
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "optimized": not __debug__,
        "program_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    })
    if args.source:
        result["native_source"] = str(args.source)
        result["native_source_sha256"] = hashlib.sha256(args.source.read_bytes()).hexdigest()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
