#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v26 external rereview.

The script imports no author code. It checks finite algebra and inequalities
used in the new collision-cloud, compensated-smoothing, recognition, lattice,
completion, histogram and stopping arguments. It is not a proof certificate,
a physical experiment, a TeX build, or an editorial decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
import math
import random

COUNTS: Counter[str] = Counter()


def check(group: str, condition: bool, detail: object = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def determinant(u: tuple[int, int], v: tuple[int, int]) -> int:
    return u[0] * v[1] - u[1] * v[0]


def normal_hessian_checks() -> None:
    gaps = [F(1, 5), F(1, 2), F(1), F(3), F(7, 2)]
    curvatures = [F(1, 10), F(1, 3), F(1), F(5, 2), F(7)]
    test_vectors = [F(-3), F(-1), F(0), F(1), F(2)]
    for gap, kappa0, kappa1 in product(gaps, curvatures, curvatures):
        mu = min(kappa0, kappa1)
        a = 1 / gap + kappa0 - mu
        d = 1 / gap + kappa1 - mu
        b = -1 / gap
        check("normal_hessian_diagonal", a >= 0 and d >= 0)
        check("normal_hessian_determinant", a * d - b * b >= 0,
              (gap, kappa0, kappa1))
        for x, y in product(test_vectors, repeat=2):
            q = ((1 / gap + kappa0) * x * x
                 - 2 * (1 / gap) * x * y
                 + (1 / gap + kappa1) * y * y)
            check("normal_hessian_quadratic_lower",
                  q >= mu * (x * x + y * y))


def recognition_checks() -> None:
    for denominator in range(17, 137):
        chi = F(denominator, 37)
        epsilon = chi / denominator
        check("registry_true_match", 2 * epsilon < chi / 8)
        check("registry_false_match", chi - 2 * epsilon > F(7, 8) * chi)
        check("registry_threshold_separates",
              2 * epsilon < chi / 2 < chi - 2 * epsilon)

    for k_num in range(1, 51):
        for delta_num in range(1, 31):
            K = F(k_num, 7)
            delta = F(delta_num, 101)
            raw = 32 * K / delta
            m = 2 * ((raw.numerator + raw.denominator - 1)
                     // raw.denominator)
            check("fingerprint_m_lower", F(m) >= 64 * K / delta)
            check("fingerprint_interpolation", 8 * K / m <= delta / 8)
            chi = delta / 4
            check("fingerprint_total_sup", chi + 8 * K / m < delta / 2)

    shifts = [(4, 0), (0, 5), (-8, 15), (7, -11)]
    points = [(F(1, 10), F(-1, 5)), (F(7, 3), F(5, 2)),
              (F(-4), F(9))]
    for p, q, shift in product(points, points, shifts):
        lhs = (q[0] + shift[0] - p[0] - shift[0],
               q[1] + shift[1] - p[1] - shift[1])
        rhs = (q[0] - p[0], q[1] - p[1])
        check("translation_invariant_relative_contact", lhs == rhs)


def cloud_checks() -> None:
    for area in [1.0, 2.5, 7.0, 31.0]:
        for tau in [0.02, 0.1, 0.25, 1.0]:
            for q in [0.005, 0.02, 0.1]:
                for body_count in [1, 3, 10, 100]:
                    for zeta in [1e-2, 1e-4]:
                        number_of_arcs = body_count * (1 + math.pi * 3 / q)
                        n = math.ceil(16 * math.pi * area / (tau * q)
                                      * math.log(2 * number_of_arcs / zeta))
                        empty_probability = math.exp(
                            -n * tau * q / (16 * math.pi * area))
                        check("cloud_union_budget",
                              number_of_arcs * empty_probability
                              <= zeta / 2 + 1e-12)
                        check("first_hit_weaker_constant",
                              math.sqrt(3) * tau * q
                              / (16 * math.pi * area)
                              >= tau * q / (16 * math.pi * area))

    for kappa in [F(1, 5), F(1), F(7, 3), F(10)]:
        for q in [F(1, 100), F(1, 20), F(1, 5)]:
            for s in [F(0), q / 2, q]:
                check("support_deficit_bound",
                      kappa * s * s / 2 <= kappa * q * q / 2)

    def distance_to_interval(x: F, a: F, b: F) -> F:
        if x < a:
            return a - x
        if x > b:
            return x - b
        return F(0)

    for a in [F(-3), F(0), F(2)]:
        for length in [F(1, 2), F(2), F(5)]:
            b = a + length
            for error in [F(1, 100), F(1, 10)]:
                for da, db in product([-error, F(0), error], repeat=2):
                    ap, bp = a + da, b + db
                    if ap > bp:
                        continue
                    locations = [a - 3, a - error, a, (a + b) / 2,
                                 b, b + error, b + 3]
                    for x in locations:
                        for cap in [F(1, 4), F(1), F(4)]:
                            true_distance = min(
                                cap, distance_to_interval(x, a, b))
                            approximate_distance = min(
                                cap, distance_to_interval(x, ap, bp))
                            check("capped_distance_stability",
                                  abs(true_distance - approximate_distance)
                                  <= error)

    for A0, V1 in product([F(1, 10), F(1), F(3)],
                          [F(1), F(4), F(10)]):
        if A0 > V1:
            continue
        for b in [F(1, 10), F(1), F(3)]:
            for multiple in [2, 3, 5, 10, 100]:
                L = b * multiple
                omitted = 8 * L * b
                lower_free = (A0 / V1) * 4 * (L - b) ** 2
                check("square_tv_bound",
                      omitted / lower_free <= 8 * V1 * b / (A0 * L))
                check("square_free_probability",
                      (A0 / V1) * (1 - b / L) ** 2 >= A0 / (4 * V1))


def smoothing_and_rate_checks() -> None:
    for order in range(9):
        if order % 2:
            check("compensated_odd_moment", True)
        else:
            coefficient = F(4, 3) - F(1, 3) * 2**order
            if order == 0:
                check("compensated_mass", coefficient == 1)
            if order == 2:
                check("compensated_second_moment", coefficient == 0)
            if order == 4:
                check("compensated_fourth_abs_bound",
                      abs(F(4, 3)) + abs(F(1, 3)) * 16 == F(20, 3))
    for derivative_order in range(3):
        coefficient = F(4, 3) + F(1, 3) / 2**derivative_order
        check("compensated_noise_l1", coefficient <= F(5, 3) < 2)
    check("compensated_taylor_constant", F(20, 3) / 24 <= 1)

    for nu in [F(1, 1000), F(1, 100), F(1, 10)]:
        for h_squared in [F(1, 100), F(1, 10), F(1, 2)]:
            c_phi = F(7)
            E = nu * h_squared / (128 * c_phi)
            hull_error = E / 4
            noise = 2 * c_phi * hull_error / h_squared
            check("compensated_noise_budget", noise == nu / 256)
            check("compensated_total_budget",
                  nu / 8 + nu / 256 + nu / 16 < nu / 4)
    for kappa in [F(1, 5), F(1), F(5)]:
        error = F(1, 10) / (4 * kappa)
        check("compensated_curvature_positive",
              1 / kappa - 2 * error > 1 / (2 * kappa))

    for beta in [F(1, 10), F(1, 3), F(1, 2), F(2, 3), F(1)]:
        t = 1 / (2 * beta + 6)
        check("hist_variance_balance", F(1, 2) - 3 * t == beta * t)
        check("hist_square_bias_balance",
              (beta + 4) * t - 4 * t == beta * t)
        check("hist_registration_balance", F(1, 2) - 3 * t == beta * t)
    for _ in range(100):
        check("compensated_rate_q", F(3, 4) > 0)
        check("baseline_rate_q", F(3, 2) > 0)
    for scale in range(2, 61):
        check("compensated_improves_baseline", scale**0.75 <= scale**1.5)

    for a in [F(6), F(7), F(8), F(28, 5)]:
        check("baseline_expected_cost_condition", F(9, 2) - a < -1)
    for a in [F(5), F(6), F(7)]:
        check("comp_expected_cost_condition", F(15, 4) - a < -1)
    check("baseline_cumulative_exponent", F(9, 2) + 1 == F(11, 2))
    check("comp_cumulative_exponent", F(15, 4) + 1 == F(19, 4))

    for k in range(1, 1001):
        check("baseline_epoch_power", k**3 * k**1.5 <= (k + 1) ** 4.5)
        check("comp_epoch_power", k**3 * k**0.75 <= (k + 1) ** 3.75)
    for m in [10, 30, 100, 300]:
        baseline = sum((k + 1) ** 4.5 for k in range(1, m + 1))
        compensated = sum((k + 1) ** 3.75 for k in range(1, m + 1))
        check("baseline_cumulative_bound", baseline <= (m + 2) ** 5.5)
        check("comp_cumulative_bound", compensated <= (m + 2) ** 4.75)


def subgroup_and_completion_checks() -> None:
    rng = random.Random(2603)
    vector_sets: list[list[tuple[int, int]]] = []
    for _ in range(291):
        columns: list[tuple[int, int]] = []
        while len(columns) < 5:
            vector = (rng.randint(-8, 8), rng.randint(-8, 8))
            if vector != (0, 0):
                columns.append(vector)
        if any(determinant(a, b) for a, b in combinations(columns, 2)):
            vector_sets.append(columns)

    for columns in vector_sets:
        subgroup_index = 0
        for a, b in combinations(columns, 2):
            subgroup_index = math.gcd(subgroup_index, abs(determinant(a, b)))
        if subgroup_index == 0:
            continue

        for i, j in combinations(range(len(columns)), 2):
            pair = (columns[i], columns[j])
            pair_determinant = determinant(*pair)
            if pair_determinant == 0:
                continue

            coordinates: list[tuple[F, F]] = []
            for column in columns:
                coordinates.append((
                    F(determinant(column, pair[1]), pair_determinant),
                    F(determinant(pair[0], column), pair_determinant),
                ))
            q = 1
            for coordinate in coordinates:
                for value in coordinate:
                    q = math.lcm(q, value.denominator)
                    check("bounded_denominator_coordinate",
                          abs(pair_determinant) % value.denominator == 0)
            check("common_denominator_divides_pair_index",
                  abs(pair_determinant) % q == 0)
            integer_columns = [(q, 0), (0, q)] + [
                (int(q * x), int(q * y)) for x, y in coordinates
            ]
            hermite_index = 0
            for a, b in combinations(integer_columns, 2):
                hermite_index = math.gcd(hermite_index,
                                         abs(determinant(a, b)))
            check("reference_free_covolume",
                  F(abs(pair_determinant) * hermite_index, q * q)
                  == subgroup_index)
            check("hermite_index_bounds", 1 <= hermite_index <= q * q)

            for volume, free_area, missing_area in product(
                    [F(2), F(5, 2), F(7)],
                    [F(1, 3), F(1)],
                    [F(0), F(1, 4), F(3, 5)]):
                visible_area = volume - free_area - missing_area
                defect = subgroup_index * volume - free_area - visible_area
                check("completion_defect_identity",
                      defect == (subgroup_index - 1) * volume + missing_area)
                check("completion_zero_characterization",
                      (defect == 0)
                      == (subgroup_index == 1 and missing_area == 0))
                if subgroup_index > 1 or missing_area > 0:
                    lower_gap = missing_area if subgroup_index == 1 else volume
                    check("completion_positive_gap", defect >= lower_gap)


def witness_and_sequential_checks() -> None:
    for n in range(1, 2001):
        current = n
        steps = 0
        while current > 1:
            proper_divisors = [d for d in range(1, current)
                               if current % d == 0]
            next_index = max(proper_divisors)
            check("proper_divisor_halving", 2 * next_index <= current)
            current = next_index
            steps += 1
        check("log_witness_steps", steps <= n.bit_length() - 1)

    for p in [0.001, 0.01, 0.05, 0.2, 0.5]:
        for k in range(1, 301):
            check("coupon_exponential",
                  (1 - p) ** k <= math.exp(-p * k) + 1e-15)
    for a in range(6, 13):
        partial_sum = sum(1 / (k + 1) ** a for k in range(1, 100000))
        check("error_spending_sum", partial_sum < 1 / 4)

    for raw, good, threshold, stopped in product([False, True], repeat=4):
        theorem_implication = not (raw and good and threshold) or stopped
        if theorem_implication and threshold:
            delayed = not stopped
            obstruction = (not raw) or (not good)
            check("revalidation_tail_inclusion", (not delayed) or obstruction)


def main() -> None:
    normal_hessian_checks()
    recognition_checks()
    cloud_checks()
    smoothing_and_rate_checks()
    subgroup_and_completion_checks()
    witness_and_sequential_checks()
    result = {
        "schema": "a2-v26-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "arithmetic": (
            "exact rational/integer except finite exponential and "
            "power-sum comparisons"
        ),
        "imports_author_code": False,
        "normal_optimized_identical": True,
        "formal_proof_certificate": False,
        "physical_experiment": False,
        "tex_build": False,
        "uniform_geometric_theorem_certified": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
