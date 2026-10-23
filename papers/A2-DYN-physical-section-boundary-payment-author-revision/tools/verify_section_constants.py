#!/usr/bin/env python3
"""Exact arithmetic certificates for the original-section reconstruction.

The geometric arguments that turn these bounds into multiplier estimates
are in native module 333. This program verifies their constants and finite
combinatorics. It does not certify a Banach-space realization, the DZ
dynamical hypotheses, spectral estimates, or a raw local limit theorem.

Usage:
  python3 verify_section_constants.py
  python3 verify_section_constants.py --output section_constants_results.json
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction as Q
import json
from pathlib import Path
import sys


def rational(x: Q) -> dict[str, str]:
    """The exact fraction is authoritative; decimal text is only a preview."""
    return {"exact": str(x), "decimal_preview": format(float(x), ".15g")}


def verify() -> dict:
    R_lo, R_hi = Q(9, 20), Q(47, 100)
    q_lo, q_hi = Q(49, 100), Q(53, 100)
    h0 = Q(1, 200)
    checks: dict = {}

    # All quantities used in the actual proof are rational bounds.
    # sqrt(3)>17/10, and the tighter bracket below independently checks
    # the existence of the root throughout the original radius interval.
    sqrt3_lo, sqrt3_hi = Q(1732, 1000), Q(1733, 1000)
    assert Q(17, 10) ** 2 < 3
    assert sqrt3_lo**2 < 3 < sqrt3_hi**2
    negative_factor_upper = -12 * q_lo + 4 * q_hi**3
    assert negative_factor_upper < 0
    F_q_upper = (
        8 * R_hi * (1 + 3 * q_hi**2)
        - 4
        + 12 * q_hi**2
        + Q(17, 10) * negative_factor_upper
    )
    F_R_upper = 8 * q_hi * (1 + q_hi**2)
    assert F_q_upper == Q(-6710711, 2500000) < -2
    assert 0 < F_R_upper == Q(678877, 125000) < 6
    q_prime_upper = F_R_upper / 2
    theta_prime_upper = 2 * q_prime_upper / (1 + q_lo**2)
    assert q_prime_upper < 3 and theta_prime_upper < 6
    checks["implicit_root_derivative_bounds"] = {
        "sqrt3_lower_used": rational(Q(17, 10)),
        "negative_factor_upper": rational(negative_factor_upper),
        "F_q_upper": rational(F_q_upper),
        "F_R_upper": rational(F_R_upper),
        "q_prime_upper": rational(q_prime_upper),
        "theta_prime_upper": rational(theta_prime_upper),
        "interval_argument": (
            "Positive q,R polynomial terms are bounded at their upper "
            "endpoints; -12q+4q^3 is bounded above by "
            "-12q_lo+4q_hi^3<0. Multiplication by sqrt(3)>17/10 "
            "therefore gives the stated upper bound throughout the rectangle."
        ),
    }

    def poly_base(R: Q, q: Q) -> Q:
        return 8 * R * q * (1 + q * q) - 4 * q * (1 - q * q)

    def sqrt_coefficient(q: Q) -> Q:
        return 1 - 6 * q * q + q**4

    assert sqrt_coefficient(q_lo) < 0
    assert sqrt_coefficient(q_hi) < 0
    # F increases with R. Hence these endpoint certificates establish
    # F(R,q_lo)>0 and F(R,q_hi)<0 for every R in [R_lo,R_hi].
    left_root_sign_lower = poly_base(R_lo, q_lo) + (
        sqrt_coefficient(q_lo) * sqrt3_hi
    )
    right_root_sign_upper = poly_base(R_hi, q_hi) + (
        sqrt_coefficient(q_hi) * sqrt3_lo
    )
    assert left_root_sign_lower > 0 > right_root_sign_upper
    checks["whole_radius_root_bracket"] = {
        "sqrt3_bracket": [rational(sqrt3_lo), rational(sqrt3_hi)],
        "F_Rlo_qlo_lower": rational(left_root_sign_lower),
        "F_Rhi_qhi_upper": rational(right_root_sign_upper),
        "certificate": (
            "Intermediate value plus F_q<-2 gives a unique root in the "
            "original q interval at every original radius; no sampled "
            "floating-point roots are used."
        ),
    }

    # sin(2 arctan q)=2q/(1+q^2), increasing for 0<q<1.
    assert 0 < q_lo < q_hi < 1
    momentum_cap_upper = 2 * q_hi / (1 + q_hi**2) + h0
    cap_gap = Q(5, 6) - momentum_cap_upper
    assert momentum_cap_upper == Q(2132809, 2561800)
    assert cap_gap == Q(6073, 7685400) > 0
    # A vertical center speed <6 also bounds the momentum center speed.
    # In phi=arcsin(p), the derivative loss is at most 6/sqrt(11).
    phi_side_speed_squared_upper = Q(6) ** 2 / (1 - Q(5, 6) ** 2)
    assert phi_side_speed_squared_upper == Q(1296, 11) < 11**2
    checks["section_cap_and_motion"] = {
        "momentum_cap_upper": rational(momentum_cap_upper),
        "gap_below_five_sixths": rational(cap_gap),
        "alpha_side_speed_upper": 6,
        "phi_side_speed_squared_upper": rational(phi_side_speed_squared_upper),
        "phi_side_speed_upper": 11,
        "moving_rectangles": 2,
        "moving_sides_per_orientation": 4,
        "total_swept_strips": 8,
    }

    # Common-coordinate cone contains all arclength-coordinate cones.
    a, K = Q(100, 47), Q(170, 9)
    a_common, K_common = R_lo * a, R_hi * K
    assert a_common == Q(45, 47)
    assert K_common == Q(799, 90)
    assert Q(1, 2) < a_common < 1 < K_common
    for R in [R_lo, R_hi]:
        for magnitude in [a, K]:
            assert a_common <= R * magnitude <= K_common
    sine_squared_lower = a_common**2 / (1 + K_common**2)
    vertical_sine_squared_lower = 1 / (1 + K_common**2)
    horizontal_sine_squared_lower = a_common**2 / (1 + a_common**2)
    assert 0 < sine_squared_lower <= vertical_sine_squared_lower
    assert sine_squared_lower <= horizontal_sine_squared_lower
    checks["cone_and_transversality"] = {
        "arclength_a": rational(a),
        "arclength_K": rational(K),
        "common_a": rational(a_common),
        "common_K": rational(K_common),
        "common_angle_sine_squared_lower": rational(sine_squared_lower),
        "vertical_sine_squared_lower": rational(vertical_sine_squared_lower),
        "horizontal_sine_squared_lower": rational(horizontal_sine_squared_lower),
        "qualification": (
            "This checks cone containment and transverse coordinate sides. "
            "Invariance of the enlarged test-curve family under every T_R "
            "is not asserted."
        ),
    }

    rectangles = 4 + 1
    side_values_per_coordinate = 2 * rectangles
    cells = (side_values_per_coordinate + 1) ** 2
    combined_side_values = 2 * side_values_per_coordinate
    intervals_per_chart = 2 * combined_side_values + 1
    intervals_with_seam = 2 * intervals_per_chart
    assert cells == 121
    assert intervals_with_seam == 82
    # A stable arc has total phi range <=pi. Its alpha range <=pi/a_common
    # is less than 2pi, so it crosses the fixed angular seam at most once.
    assert 1 / a_common < 2
    # 0<theta<2q_hi; 3<pi<22/7. These rational bounds place every
    # section rectangle in (-3,3) inside the chart (-pi,pi).
    section_alpha_lower = -(2 * q_hi + h0)
    section_alpha_upper = Q(22, 21) + h0
    assert -3 < section_alpha_lower < section_alpha_upper < 3
    checks["partition_and_weak_arc_counts"] = {
        "rectangles": rectangles,
        "side_values_each_coordinate": side_values_per_coordinate,
        "cell_bound": cells,
        "combined_radius_side_values_each_coordinate": combined_side_values,
        "intervals_per_monotone_chart_piece": intervals_per_chart,
        "maximum_chart_pieces": 2,
        "weak_arc_bound": intervals_with_seam,
        "fixed_seam": "alpha=pi, on the chart (-pi,pi)",
        "section_alpha_lower": rational(section_alpha_lower),
        "section_alpha_upper": rational(section_alpha_upper),
    }

    # s=R alpha changes curve coordinates but leaves the normalized
    # collision measure exactly the same: (R d alpha)/(4 pi R).
    conversion_values = [R_lo, R_hi, (R_lo + R_hi) / 2]
    for R in conversion_values:
        assert R / (4 * R) == Q(1, 4)
        assert R_lo <= R <= R_hi
        assert 1 / R_hi <= 1 / R <= 1 / R_lo
    checks["coordinate_and_measure_conversion"] = {
        "s_alpha_derivative_interval": [rational(R_lo), rational(R_hi)],
        "alpha_s_derivative_interval": [
            rational(1 / R_hi),
            rational(1 / R_lo),
        ],
        "exact_normalized_measure_identity": (
            "cos(phi) ds dphi/(4 pi R) = "
            "cos(phi) dalpha dphi/(4 pi)"
        ),
        "p_phi_relation": "p=sin(phi), dp=cos(phi) dphi",
        "measure_embedding": "The element h represents h dnu; 1 represents nu.",
        "section_normalizations_in_transfer_formula": 1,
        "occupation_indices": "0,...,m-1; terminal section at m is separate",
    }

    # A constructive admissible exponent family for every varsigma0 in (0,1).
    # This verifies algebraic compatibility, not a dynamical summability claim.
    exponent_samples = 0
    p, q, gamma_extra = Q(1, 3), Q(1, 6), Q(1, 12)
    for j in range(1, 101):
        varsigma0 = Q(j, 101)
        alpha = (1 - varsigma0) / 2
        beta = min(alpha, p - q) / 2
        gamma = max(p, 2 * beta + gamma_extra)
        assert 0 < q < p <= Q(1, 3)
        assert 0 < alpha < 1 - varsigma0
        assert 0 < beta <= min(alpha, p - q)
        assert gamma > 2 * beta and gamma >= p and gamma < 1
        exponent_samples += 1
    checks["norm_exponent_compatibility"] = {
        "exact_rational_instances": exponent_samples,
        "family": {
            "p": "1/3",
            "q": "1/6",
            "alpha": "(1-varsigma0)/2",
            "beta": "min(alpha,p-q)/2",
            "gamma_extra": "1/12",
            "gamma": "max(p,2 beta+gamma_extra)=1/3",
        },
        "qualification": (
            "Compatibility of the stated norm parameters only. "
            "A qualifying dynamical varsigma0 and H1--H5 are not "
            "inferred from these finite algebra checks."
        ),
    }

    return {
        "status": "PASS",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version.split()[0],
        "arithmetic": "fractions.Fraction; all comparisons exact",
        "check_groups": checks,
        "evidence_scope": (
            "Exact constants, polynomial interval certificates, finite "
            "partition counts, coordinate normalization and parameter "
            "compatibility. This is auxiliary verification of the native "
            "proof; no new theorem status, full functional analytic "
            "qualification, spectral gap, CI result or raw local limit "
            "is claimed by this program."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write the JSON receipt here.")
    args = parser.parse_args()
    result = verify()
    serialized = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
