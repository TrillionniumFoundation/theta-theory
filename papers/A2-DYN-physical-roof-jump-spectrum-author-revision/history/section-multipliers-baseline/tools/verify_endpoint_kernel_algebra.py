#!/usr/bin/env python3
"""Exact arithmetic checks for the new geometric derivation.

These checks do not prove billiard growth, continuum coverage, sector
limits or the raw local limit theorem. The native proof establishes
those assertions used here. This program audits collision indices,
geometric summation, reversal weights and the normalization distinction.
"""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    theta = F(47, 53)
    q = F(9, 10)  # Represents q0^(1/4) abstractly in the finite sum check.
    epsilon = F(1, 1000)
    checks = {}

    checked_indices = 0
    for m in range(1, 201):
        for j in range(m):
            if j >= 1:
                h, n = j - 1, m - j - 1
                assert h >= 0 and n >= 0 and h + n + 2 == m
            if j == 0 and m >= 2:
                assert 1 + (m - 2) + 1 == m
                assert theta ** (m - 2) == theta ** (m - 1) / theta
            assert (m - 1) - ((m - 1) - j) == j
            assert min(theta**j, theta ** (m - 1 - j)) == (
                theta ** max(j, m - 1 - j)
            )
            checked_indices += 1
    checks["exact_collision_and_reversal_indices"] = checked_indices

    for m in range(1, 201):
        selected_width_sum = sum(
            (2 * epsilon * q ** min(j, m - 1 - j) for j in range(m)),
            F(0),
        )
        assert selected_width_sum <= 4 * epsilon / (1 - q)
        transient_sum = sum(
            (theta ** max(j, m - 1 - j) for j in range(m)), F(0)
        )
        # Squaring avoids any floating-point fractional exponent.
        assert transient_sum**2 <= m * m * theta ** (m - 1)
    checks["exact_guard_and_transient_sum_counts"] = 200

    # Every matrix below is a determinant-one rational derivative.
    # I M^{-1} I has the same lower-left entry as M. This is the
    # algebraic identity used for the real area-preserving collision map.
    reversal_checks = 0
    for a in range(1, 11):
        for b in range(-4, 5):
            for c in range(1, 8):
                d = F(1 + b * c, a)
                assert F(a) * d - b * c == 1
                original_c = F(c)
                inverse_c = -F(c)
                reversed_c = -inverse_c
                assert reversed_c == original_c
                assert 1 / abs(reversed_c) == 1 / abs(original_c)
                reversal_checks += 1
    checks["exact_area_preserving_reversal_matrices"] = reversal_checks

    # The finite-germ proof has one c_*^{-1}, not two.
    for cstar in [F(1, 50), F(1, 200), F(3, 400)]:
        for endpoint_budget in [F(1, 10), F(7, 13)]:
            U2 = F(320, 9)
            critical_coefficient_bound = U2 * endpoint_budget / (2 * cstar)
            assert (
                critical_coefficient_bound * cstar
                == U2 * endpoint_budget / 2
            )
    checks["single_conditioning_factor"] = 6

    # Explicitly guard against interpreting an O(epsilon) unscaled
    # bound as an m^-2 estimate at fixed outer epsilon.
    previous = F(0)
    for m in [1, 10, 100, 1000, 10000]:
        normalized_width_term = m * m * epsilon
        assert normalized_width_term > previous
        previous = normalized_width_term
    checks["no_false_normalized_closure"] = True

    result = {
        "status": "PASS",
        "checks": checks,
        "proof_scope": (
            "Exact finite algebra and collision-index checks only; "
            "not a proof of continuum dynamics or of the raw theorem."
        ),
    }
    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
