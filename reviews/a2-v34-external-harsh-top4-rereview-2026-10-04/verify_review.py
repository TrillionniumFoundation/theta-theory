#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v34 external review.

This script imports no author code.  It checks finite algebra and discrete
models behind the fixed-footprint stationary-jitter theorem and retained
period arithmetic.  It is not a continuum proof certificate, a TeX build,
a physical sensor test, or an editorial decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
import math

CHECKS: Counter[str] = Counter()


def require(ok: bool, group: str, detail: object = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def reciprocal_truth_table() -> None:
    # Endpoint solidity and an optional interior hit exhaust the pointwise cases.
    for solid_start, solid_end, interior_hit in product([0, 1], repeat=3):
        forward = 0 if solid_start else int(bool(solid_end or interior_hit))
        reverse = 0 if solid_end else int(bool(solid_start or interior_hit))
        require(
            forward - reverse == solid_end - solid_start,
            "reciprocal_truth_table",
            (solid_start, solid_end, interior_hit, forward, reverse),
        )


def interval_blur_support() -> None:
    # K=[-1,1], j_theta(z)=(1+theta*z)/2.  All tested densities are positive.
    def mass(lo: F, hi: F, theta: F) -> F:
        lo = max(lo, F(-1))
        hi = min(hi, F(1))
        if hi <= lo:
            return F(0)
        return (hi - lo) / 2 + theta * (hi * hi - lo * lo) / 4

    bodies = [(F(-2), F(3)), (F(0), F(1)), (F(-3, 2), F(7, 3))]
    for left_body, right_body in bodies:
        for theta in (F(-3, 4), F(0), F(2, 3)):
            left_blur = left_body - 1
            right_blur = right_body + 1
            for m in range(-80, 81):
                x = F(m, 10)
                value = mass(left_body - x, right_body - x, theta)
                require(
                    (value > 0) == (left_blur < x < right_blur),
                    "one_dimensional_support_identity",
                    (left_body, right_body, theta, x, value),
                )
            require(
                left_blur + 1 == left_body and right_blur - 1 == right_body,
                "one_dimensional_minkowski_subtraction",
            )


def support_function_algebra() -> None:
    # Fourier coefficient order: constant, cos1, sin1, cos2, sin2, ...
    degrees = [0, 1, 1, 2, 2, 3, 3, 4, 4]
    for seed in range(1, 401):
        body = [F(3), F(seed % 17, 101), F(-(seed % 13), 103)]
        body += [F((seed * (i + 3)) % 11 - 5, 1000 * (i + 1)) for i in range(6)]
        footprint = [F(1, 2), F((seed + 3) % 19, 211), F(-(seed + 5) % 17, 223)]
        footprint += [F((seed * (i + 5)) % 13 - 6, 1300 * (i + 1)) for i in range(6)]
        reflected = [((-1) ** degree) * value for degree, value in zip(degrees, footprint)]
        expanded = [c + k for c, k in zip(body, reflected)]
        require(
            [p - k for p, k in zip(expanded, reflected)] == body,
            "minkowski_support_subtraction",
        )
        centered_body = body.copy()
        centered_expanded = expanded.copy()
        centered_footprint = reflected.copy()
        centered_body[1] = centered_body[2] = F(0)
        centered_expanded[1] = centered_expanded[2] = F(0)
        centered_footprint[1] = centered_footprint[2] = F(0)
        require(
            [p - k for p, k in zip(centered_expanded, centered_footprint)] == centered_body,
            "centering_commutes_with_subtraction",
        )


def lens_rectangles_and_exponents() -> None:
    for r_body, r_noise, denominator, numerator in product(
        [F(1, 5), F(1, 3), F(1, 2), F(1), F(2), F(5)],
        [F(1, 6), F(1, 4), F(2, 3), F(1), F(3)],
        [20, 50, 100, 500, 1000],
        [1, 2, 3],
    ):
        depth = min(r_body, r_noise) * F(numerator, denominator)
        tangent_square = min(r_body, r_noise) * depth / 32
        for normal in (-3 * depth / 4, -depth / 2, -depth / 4):
            require(
                tangent_square + (normal + r_body) ** 2 <= r_body**2,
                "lens_rectangle_first_disk",
                (r_body, r_noise, depth, normal),
            )
            require(
                tangent_square + (normal - r_noise + depth) ** 2 <= r_noise**2,
                "lens_rectangle_second_disk",
                (r_body, r_noise, depth, normal),
            )
        require(depth - depth / 4 == 3 * depth / 4, "erosion_depth_reserve")

    betas = [F(1, 10), F(1, 5), F(1, 3), F(1, 2), F(2, 3), F(4, 5), F(1)]
    gammas = [F(0), F(1, 4), F(1, 2), F(1), F(3, 2), F(2), F(5)]
    for beta, gamma in product(betas, gammas):
        smoothness = 6 + beta
        boundary_power = gamma + F(3, 2)
        attempt_power = ((2 * gamma + 3) * smoothness + 1) / (smoothness - 2)
        require(2 * boundary_power == 2 * gamma + 3, "cap_mass_exponent")
        require(
            attempt_power == (1 + 2 * boundary_power * smoothness) / (smoothness - 2),
            "attempt_exponent_identity",
        )
        require(attempt_power > 0, "fixed_spread_power_positive")
        require(1 / boundary_power > 0, "inverse_Hausdorff_exponent")
        require(
            (smoothness - 2) / (smoothness * boundary_power) > 0,
            "inverse_C2_exponent",
        )
        h_power = 1 / (smoothness - 2)
        layer_power = smoothness * h_power
        require(layer_power * (smoothness - 2) / smoothness == 1, "localization_balance")
        require(
            h_power + (2 * gamma + 3) * layer_power == attempt_power,
            "query_count_power",
        )
        require(
            gamma != 0 or attempt_power == (3 * smoothness + 1) / (smoothness - 2),
            "gamma_zero_specialization",
        )


def killed_green_models() -> None:
    shifts = ((1, 0), (-1, 0), (0, 1), (0, -1))
    for side in (3, 5, 7):
        half = side // 2
        states = list(product(range(-half, half + 1), repeat=2))
        index = {point: i for i, point in enumerate(states)}
        neighbors: list[list[int]] = []
        for x, y in states:
            neighbors.append(
                [
                    index[q]
                    for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                    if q in index
                ]
            )

        def transition(values: list[F]) -> list[F]:
            return [sum((values[j] for j in row), F(0)) / 4 for row in neighbors]

        occupations = [
            [F(1) if abs(x) + abs(y) <= 1 else F(0) for x, y in states],
            [
                F(2 + x * x + y * y, 12)
                if max(abs(x), abs(y)) <= max(0, half - 1)
                else F(0)
                for x, y in states
            ],
            [
                F((x + half + 1) * (y + half + 1), (side + 1) ** 2)
                if abs(x) + abs(y) <= max(1, half)
                else F(0)
                for x, y in states
            ],
        ]
        for occupation_index, occupation in enumerate(occupations):
            forcing = [a - b for a, b in zip(transition(occupation), occupation)]
            exact = [F(0)] * len(states)
            noisy = [F(0)] * len(states)
            forcing_error = F(1, 10000)
            update_error = F(1, 20000)
            tail = [F(1)] * len(states)
            green = [F(0)] * len(states)
            for depth in range(1, 61):
                green = [a + b for a, b in zip(green, tail)]
                tail = transition(tail)
                exact_transition = transition(exact)
                noisy_transition = transition(noisy)
                next_exact: list[F] = []
                next_noisy: list[F] = []
                for i, (te, tn, g) in enumerate(zip(exact_transition, noisy_transition, forcing)):
                    e = max(F(0), te - g)
                    signed_forcing_error = forcing_error if (i + depth + occupation_index) % 2 == 0 else -forcing_error
                    n = max(F(0), tn - (g + signed_forcing_error))
                    n += update_error if i % 2 == 0 else -update_error
                    n = min(F(1), max(F(0), n))
                    next_exact.append(e)
                    next_noisy.append(n)
                    require(F(0) <= e <= occupation[i] + F(1, 10**12), "bellman_monotone_bounded")
                    require(
                        abs(n - e) <= (forcing_error + update_error) * green[i],
                        "green_perturbation_bound",
                        (side, occupation_index, depth, i),
                    )
                    require(
                        green[i] <= F((2 * side + 1) ** 2),
                        "fixed_aperture_green_bound",
                    )
                exact, noisy = next_exact, next_noisy
            require(
                max(abs(a - b) for a, b in zip(exact, occupation)) < F(1, 100),
                "bellman_residual_control",
            )

    for exit_bound in (1, 2, 5, 10, 100, 1000):
        h = F(exit_bound)
        for k in range(1, 21):
            boundary_mass = F(1, 2**k)
            mean_error = boundary_mass / (256 * h)
            update_error = boundary_mass / (128 * h)
            survival_tail = boundary_mass / 64
            total = survival_tail + h * (2 * mean_error + update_error)
            require(total < boundary_mass / 8, "query_error_allocation")
            require(total < boundary_mass / 2 < boundary_mass - total, "support_threshold_separation")


def relaxed_bisection() -> None:
    for boundary in (F(k, 64) for k in range(1, 64)):
        for ambiguity in (F(0), F(1, 256), F(1, 64), F(1, 16)):
            states = {(F(0), F(1))}
            for depth in range(1, 10):
                next_states: set[tuple[F, F]] = set()
                for lower, upper in states:
                    midpoint = (lower + upper) / 2
                    allowed: list[bool] = []
                    if midpoint <= boundary + ambiguity:
                        allowed.append(True)
                    if midpoint >= boundary - ambiguity:
                        allowed.append(False)
                    for inside in allowed:
                        new_lower, new_upper = (midpoint, upper) if inside else (lower, midpoint)
                        require(
                            new_lower - ambiguity <= boundary <= new_upper + ambiguity,
                            "relaxed_bisection_invariant",
                        )
                        require(
                            abs((new_lower + new_upper) / 2 - boundary)
                            <= ambiguity + F(1, 2 ** (depth + 1)),
                            "relaxed_bisection_error",
                        )
                        next_states.add((new_lower, new_upper))
                states = next_states


def determinant(u: tuple[int, int], v: tuple[int, int]) -> int:
    return u[0] * v[1] - u[1] * v[0]


def period_arithmetic() -> None:
    integer_sets: list[list[tuple[int, int]]] = []
    for a, b, c, d in product(range(1, 9), repeat=4):
        if a * d - b * c == 0:
            continue
        integer_sets.append([(a, b), (c, d), (a + c, b - d), (2 * a - c, 2 * b + d)])
        if len(integer_sets) >= 600:
            break

    for columns in integer_sets:
        minors = [abs(determinant(u, v)) for u, v in combinations(columns, 2)]
        subgroup_index = 0
        for minor in minors:
            subgroup_index = math.gcd(subgroup_index, minor)
        require(subgroup_index > 0, "period_rank_two")
        for i, j in combinations(range(len(columns)), 2):
            first, second = columns[i], columns[j]
            pair_det = determinant(first, second)
            if pair_det == 0:
                continue
            coordinates = [
                (F(determinant(column, second), pair_det), F(determinant(first, column), pair_det))
                for column in columns
            ]
            denominator = 1
            for x, y in coordinates:
                denominator = math.lcm(denominator, x.denominator, y.denominator)
            require(
                abs(pair_det) % denominator == 0,
                "common_denominator_divides_pair_index",
            )
            integer_columns = [(denominator, 0), (0, denominator)] + [
                (int(denominator * x), int(denominator * y)) for x, y in coordinates
            ]
            hermite_index = 0
            for u, v in combinations(integer_columns, 2):
                hermite_index = math.gcd(hermite_index, abs(determinant(u, v)))
            require(
                F(abs(pair_det) * hermite_index, denominator**2) == subgroup_index,
                "reference_free_covolume",
            )
            require(1 <= hermite_index <= denominator**2, "hermite_index_bounds")


def binary_caps() -> None:
    for model_count in (2, 3, 4, 5, 8, 16, 32, 64, 128, 256, 1024):
        for delta in (F(0), F(1, 10), F(1, 4)):
            threshold = math.log2(float(model_count * (1 - delta)))
            minimum = math.ceil(threshold - 1e-12)
            require(
                (2**minimum) / model_count + 1e-15 >= float(1 - delta),
                "binary_cap_necessary",
            )
            if minimum > 0:
                require(
                    (2 ** (minimum - 1)) / model_count < float(1 - delta) + 1e-15,
                    "binary_cap_minimal",
                )


def main() -> None:
    reciprocal_truth_table()
    interval_blur_support()
    support_function_algebra()
    lens_rectangles_and_exponents()
    killed_green_models()
    relaxed_bisection()
    period_arithmetic()
    binary_caps()
    result = {
        "schema": "a2-v34-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "arithmetic": "exact integer/rational except finite binary logarithm thresholds",
        "imports_author_code": False,
        "physical_sensor_executed": False,
        "tex_build": False,
        "continuum_proof_certificate": False,
    }
    canonical = json.dumps(result, sort_keys=True).encode()
    result["result_sha256"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
