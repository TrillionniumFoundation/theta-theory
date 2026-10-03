#!/usr/bin/env python3
"""Independent finite diagnostics for the external A2 v24 rereview.

The script imports no author module.  It checks finite algebra used in the
new local-gate, registration, discovery, subgroup, defect and resource
arguments.  It is not a proof certificate, a physical-probe execution, a
TeX build, a priority search or an editorial decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
import math

REVIEWED_COMMIT = "f5754f7eacc5b2bde9450de154a4e4c0093b3e23"
COUNTS: Counter[str] = Counter()


def check(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def determinant(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def lcm_many(values: list[int]) -> int:
    result = 1
    for value in values:
        result = math.lcm(result, value)
    return result


def normal_hessian_checks() -> None:
    gaps = [F(1, 4), F(1, 3), F(1, 2), F(1), F(3, 2), F(2), F(5, 2)]
    curvatures = [F(1, 7), F(1, 4), F(1, 2), F(1), F(2), F(3)]
    vectors = [(F(x), F(y)) for x in range(-3, 4) for y in range(-3, 4)
               if (x, y) != (0, 0)]

    for gap, k0, k1 in product(gaps, curvatures, curvatures):
        inv_gap = 1 / gap
        h00 = inv_gap + k0
        h11 = inv_gap + k1
        h01 = -inv_gap
        minimum = min(k0, k1)

        check(h00 * h11 - h01 * h01 > 0, "normal_hessian_positive")
        check(h00 - minimum >= 0 and h11 - minimum >= 0,
              "curvature_lower_bound_diagonal")
        shifted_det = (h00 - minimum) * (h11 - minimum) - h01 * h01
        check(shifted_det >= 0, "curvature_lower_bound_determinant")

        for x, y in vectors:
            quadratic = h00 * x * x + 2 * h01 * x * y + h11 * y * y
            check(quadratic >= minimum * (x * x + y * y),
                  "normal_hessian_quadratic_lower_bound",
                  str((gap, k0, k1, x, y)))


def registry_checks() -> None:
    for chi in [F(1, 5), F(1, 2), F(1), F(2), F(5)]:
        threshold = chi / 2
        for denominator in range(17, 41):
            error = chi / denominator
            same_class_distance = 2 * error
            different_class_distance = chi - 2 * error

            check(error < chi / 16, "registry_error_margin")
            check(same_class_distance < threshold, "registry_true_match")
            check(different_class_distance > threshold, "registry_false_match_excluded")
            check(different_class_distance > same_class_distance,
                  "registry_bands_disjoint")
            check(chi - 2 * error > 7 * chi / 8,
                  "registry_stated_seven_eighths_margin")


def square_and_registration_checks() -> None:
    for h, ratio in product(
        [F(1, 4), F(1, 8), F(1, 16), F(1, 32), F(1, 64)],
        [F(1, 4), F(1, 8), F(1, 16), F(1, 32)],
    ):
        nu = h * ratio
        expanded = (h + 2 * nu) ** 2
        contracted = (h - 2 * nu) ** 2
        band = expanded - contracted

        check(nu <= h / 4, "registration_shift_admissible")
        check(band == 8 * h * nu, "square_boundary_band_exact")
        check(band <= 8 * h * nu + 4 * nu * nu,
              "square_boundary_band_upper_bound")
        check((nu * h) * h ** -4 == nu * h ** -3,
              "registration_C2_amplification")

    for b, multiplier, a0, v1 in product(
        [F(1, 4), F(1, 2), F(1), F(2)],
        [F(2), F(3), F(4), F(8), F(16)],
        [F(1, 4), F(1, 2), F(1)],
        [F(1), F(2), F(5)],
    ):
        length = multiplier * b
        omitted_ratio_bound = 2 * length * b * v1 / (a0 * (length - b) ** 2)
        displayed_bound = 8 * v1 * b / (a0 * length)
        free_fraction_lower = (a0 / v1) * (1 - b / length) ** 2

        check(length >= 2 * b, "square_size_condition")
        check(omitted_ratio_bound <= displayed_bound, "square_TV_bound")
        check(free_fraction_lower >= a0 / (4 * v1),
              "free_launch_probability_bound")

    for shift_x, shift_y, px, py, qx, qy in product(
        range(-3, 4), range(-3, 4),
        [F(-1, 3), F(0), F(2, 5)],
        [F(-2, 7), F(1, 4)],
        [F(3, 8), F(5, 4)],
        [F(-1, 5), F(7, 6)],
    ):
        sx, sy = F(shift_x), F(shift_y)
        check(((qx + sx) - (px + sx), (qy + sy) - (py + sy)) ==
              (qx - px, qy - py), "translation_invariant_relative_contact")


def discovery_and_witness_checks() -> None:
    for mu, grid_size, epoch in product(
        [F(1, 100), F(1, 50), F(1, 20), F(1, 10), F(1, 4), F(1, 2)],
        range(1, 13),
        range(1, 51),
    ):
        probability = mu / (2 * grid_size)
        exact_tail = float((1 - probability) ** epoch)
        exponential_tail = math.exp(-float(probability) * epoch)
        check(0 < probability <= F(1, 4), "discovery_hazard_range")
        check(exact_tail <= exponential_tail + 2e-15,
              "coupon_exponential_bound")

    for integer in range(2, 501):
        proper_divisors = [d for d in range(1, integer) if integer % d == 0]
        for divisor in proper_divisors:
            check(2 * divisor <= integer, "proper_divisor_halving",
                  str((integer, divisor)))

        current = integer
        steps = 0
        while current > 1:
            next_value = max(d for d in range(1, current) if current % d == 0)
            current = next_value
            steps += 1
        check(steps <= integer.bit_length() - 1,
              "logarithmic_witness_steps", str(integer))


def subgroup_and_defect_checks() -> None:
    # Deterministic pseudo-random integer column families.
    for seed in range(1, 401):
        columns: list[tuple[int, int]] = []
        for index in range(5):
            x = ((11 * seed + 7 * index + 3 * index * index) % 19) - 9
            y = ((13 * seed + 5 * index + 2 * index * index) % 23) - 11
            columns.append((x, y))
        minors = [abs(determinant(a, b)) for a, b in combinations(columns, 2)]
        subgroup_index = math.gcd(*minors)
        if subgroup_index == 0:
            continue

        for i, j in combinations(range(len(columns)), 2):
            d0, d1 = columns[i], columns[j]
            det_d = determinant(d0, d1)
            if det_d == 0:
                continue

            coordinates = [
                (F(determinant(column, d1), det_d),
                 F(determinant(d0, column), det_d))
                for column in columns
            ]
            q = lcm_many([value.denominator
                          for coordinate in coordinates for value in coordinate])
            integer_columns = [(q, 0), (0, q)] + [
                (int(q * x), int(q * y)) for x, y in coordinates
            ]
            det_h = math.gcd(*[
                abs(determinant(a, b)) for a, b in combinations(integer_columns, 2)
            ])

            check(abs(det_d) % q == 0, "common_denominator_divides_pair_index")
            check(1 <= det_h <= q * q, "Hermite_index_bounds")
            check(F(abs(det_d) * det_h, q * q) == subgroup_index,
                  "reference_free_covolume")
            for x, y in coordinates:
                check(x.denominator <= abs(det_d) and y.denominator <= abs(det_d),
                      "bounded_denominator_coordinates")

        for cell_volume, free_area, hidden_area in product(
            [F(1), F(3, 2), F(2), F(5, 2)],
            [F(1, 5), F(1, 2), F(3, 4)],
            [F(0), F(1, 20), F(1, 4)],
        ):
            if free_area + hidden_area >= cell_volume:
                continue
            visible_area = cell_volume - free_area - hidden_area
            defect = subgroup_index * cell_volume - free_area - visible_area
            expected = (subgroup_index - 1) * cell_volume + hidden_area
            check(defect == expected, "completion_defect_identity")
            check((defect == 0) == (subgroup_index == 1 and hidden_area == 0),
                  "completion_zero_characterization")
            if defect != 0:
                check(defect >= min(cell_volume, hidden_area or cell_volume),
                      "completion_positive_gap_control")


def rate_and_resource_checks() -> None:
    betas = [F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(1)]
    for beta in betas:
        exponent = 1 / (2 * beta + 6)
        check(F(1, 2) - 3 * exponent == beta * exponent,
              "variance_bias_balance")
        check((beta + 4) * exponent - 4 * exponent == beta * exponent,
              "square_bias_balance")
        check((beta + 3) * exponent - 3 * exponent == beta * exponent,
              "registration_bias_balance")
        check((beta + 3) * exponent == F(1, 2),
              "probe_precision_half_power")
        check(1 - 4 * exponent >= beta * exponent,
              "linear_Bernstein_term_smaller")
        check(2 * (beta + 4) * exponent == (beta + 4) / (beta + 3),
              "apparatus_range_power")

    for probe_power in range(0, 9):
        fixed_a_works = 3 + probe_power - 6 < -1
        check(fixed_a_works == (probe_power < 2),
              "fixed_a_equals_six_scope", str(probe_power))
        chosen_a = 5 + probe_power
        check(3 + probe_power - chosen_a < -1,
              "adjustable_error_spending_summability")
        check(chosen_a > 4 + probe_power,
              "adjustable_error_spending_condition")

    for m in range(1, 1001):
        accepted = m + 2 * sum(k * (k + 1) ** 2 for k in range(1, m + 1))
        check(accepted <= 2 * (m + 1) ** 4,
              "finite_epoch_preparation_budget", str(m))


def main() -> None:
    normal_hessian_checks()
    registry_checks()
    square_and_registration_checks()
    discovery_and_witness_checks()
    subgroup_and_defect_checks()
    rate_and_resource_checks()
    result = {
        "schema": "a2-v24-independent-review-diagnostics-1",
        "reviewed_commit": REVIEWED_COMMIT,
        "status": "passed",
        "arithmetic": "exact rational/integer except the displayed exponential comparison",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "imports_author_code": False,
        "physical_probe_executed": False,
        "uniform_fingerprint_constant_certified": False,
        "tex_build": False,
        "formal_proof_certificate": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
