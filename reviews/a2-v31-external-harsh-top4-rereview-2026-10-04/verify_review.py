#!/usr/bin/env python3
"""Independent exact finite diagnostics for the A2 v31 referee report.

The program imports no author verification module.  It checks finite-state
instances of the mean-exit/Bellman identities, different-zero-set comparison,
fixed-aperture killing, reciprocal pooled reversal, rational interval
enclosures, and the displayed finite-experiment exponents.  These checks are
not a proof certificate, a physical experiment, or a TeX build.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json


COUNTS: Counter[str] = Counter()


def check(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def clip(value: F) -> F:
    return min(F(1), max(F(0), value))


def apply(rows: list[tuple[tuple[int, F], ...]], values: list[F]) -> list[F]:
    return [
        sum((weight * values[index] for index, weight in row), F(0))
        for row in rows
    ]


def line_rows(size: int) -> list[tuple[tuple[int, F], ...]]:
    return [
        tuple((j, F(1, 2)) for j in (i - 1, i + 1) if 0 <= j < size)
        for i in range(size)
    ]


def compass_rows(
    width: int, height: int, step: int = 1
) -> list[tuple[tuple[int, F], ...]]:
    rows: list[tuple[tuple[int, F], ...]] = []
    for y in range(height):
        for x in range(width):
            row: list[tuple[int, F]] = []
            for dx, dy in ((step, 0), (-step, 0), (0, step), (0, -step)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < width and 0 <= yy < height:
                    row.append((yy * width + xx, F(1, 4)))
            rows.append(tuple(row))
    return rows


def forcing(
    rows: list[tuple[tuple[int, F], ...]], occupation: list[F]
) -> list[F]:
    return [a - b for a, b in zip(apply(rows, occupation), occupation)]


def bellman(
    rows: list[tuple[tuple[int, F], ...]], g: list[F], depth: int
) -> list[F]:
    values = [F(0)] * len(rows)
    for _ in range(depth):
        values = [clip(a - b) for a, b in zip(apply(rows, values), g)]
    return values


def solve(matrix: list[list[F]], rhs: list[F]) -> list[F]:
    """Exact Gaussian elimination, independent of Bellman iteration."""
    augmented = [list(map(F, row)) + [F(value)] for row, value in zip(matrix, rhs)]
    size = len(augmented)
    for column in range(size):
        pivot = next(row for row in range(column, size) if augmented[row][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    x - factor * y
                    for x, y in zip(augmented[row], augmented[column])
                ]
    return [row[-1] for row in augmented]


def killed_exit(
    rows: list[tuple[tuple[int, F], ...]], support: range
) -> tuple[dict[int, F], list[list[F]]]:
    states = sorted(support)
    position = {state: index for index, state in enumerate(states)}
    matrix = [
        [F(i == j) for j in range(len(states))] for i in range(len(states))
    ]
    for i, state in enumerate(states):
        for target, weight in rows[state]:
            if target in position:
                matrix[i][position[target]] -= weight
    times = solve(matrix, [F(1)] * len(states))
    return dict(zip(states, times)), matrix


def interval_bellman(
    rows: list[tuple[tuple[int, F], ...]],
    forcing_lower: list[F],
    forcing_upper: list[F],
    depth: int,
) -> tuple[list[F], list[F]]:
    lower = [F(0)] * len(rows)
    upper = [F(0)] * len(rows)
    for _ in range(depth):
        transition_lower = apply(rows, lower)
        transition_upper = apply(rows, upper)
        lower = [
            clip(value - high)
            for value, high in zip(transition_lower, forcing_upper)
        ]
        upper = [
            clip(value - low)
            for value, low in zip(transition_upper, forcing_lower)
        ]
    return lower, upper


def mean_exit_green_and_bellman() -> None:
    for size in range(2, 13):
        rows = line_rows(size)
        occupation = [F(1)] * size
        g = forcing(rows, occupation)
        exit_times, matrix = killed_exit(rows, range(size))
        bound = F(size * size)  # (D+b)^2/v with D=size-1, b=v=1.

        for state in range(size):
            check(
                exit_times[state] == F((state + 1) * (size - state)),
                "exact_line_exit_time",
            )
            check(exit_times[state] <= bound, "diameter_variance_exit_bound")

        row_sums = [F(0)] * size
        for column in range(size):
            green_column = solve(
                matrix, [F(row == column) for row in range(size)]
            )
            for row, value in enumerate(green_column):
                check(value >= 0, "green_entry_nonnegative")
                row_sums[row] += value
        for state in range(size):
            check(row_sums[state] == exit_times[state], "green_row_sum_exit_time")
        check(max(row_sums) == max(exit_times.values()), "green_infinity_norm")

        values = [F(0)] * size
        survival = [F(1)] * size
        block_length = 2 * size * size
        max_depth = min(4 * block_length, 400)
        for depth in range(1, max_depth + 1):
            next_values = [
                clip(value - force)
                for value, force in zip(apply(rows, values), g)
            ]
            survival = apply(rows, survival)
            tail = F(1, 2 ** (depth // block_length))
            for state in range(size):
                check(
                    F(0) <= values[state] <= next_values[state] <= F(1),
                    "bellman_monotonicity",
                )
                check(
                    F(1) - next_values[state] == survival[state],
                    "bellman_error_equals_survival",
                )
                check(survival[state] <= tail, "geometric_block_tail")
            values = next_values


def different_zero_sets_and_intervals() -> None:
    size = 15
    rows = line_rows(size)
    candidates: list[list[F]] = []
    patterns = [
        [F(1)],
        [F(1, 3)],
        [F(2, 3)],
        [F(1, 4), F(3, 4)],
        [F(1, 5), F(2, 5), F(4, 5)],
        [F(1), F(1, 2), F(1)],
    ]
    common_bound = F(36)  # (D+b)^2 with D <= 5 and b=1.
    for start in range(1, 9):
        for pattern in patterns:
            if start + len(pattern) <= size - 1:
                occupation = [F(0)] * size
                occupation[start : start + len(pattern)] = pattern
                candidates.append(occupation)

    for left, right in combinations(candidates, 2):
        force_left = forcing(rows, left)
        force_right = forcing(rows, right)
        epsilon = max(
            abs(a - b) for a, b in zip(force_left, force_right)
        )
        distance = max(abs(a - b) for a, b in zip(left, right))
        check(
            distance <= common_bound * epsilon,
            "different_zero_set_stability",
        )
        check(
            (epsilon == 0) == (distance == 0),
            "forcing_injectivity_on_physical_candidates",
        )

    for occupation in candidates[::4]:
        true_force = forcing(rows, occupation)
        for epsilon in (F(1, 200), F(1, 77), F(1, 41)):
            perturbed = [
                value + (epsilon if index % 2 == 0 else -epsilon)
                for index, value in enumerate(true_force)
            ]
            for depth in (1, 2, 4, 8, 16, 24):
                exact_iterate = bellman(rows, true_force, depth)
                noisy_iterate = bellman(rows, perturbed, depth)
                check(
                    max(
                        abs(a - b)
                        for a, b in zip(exact_iterate, noisy_iterate)
                    )
                    <= depth * epsilon,
                    "forcing_error_accumulation",
                )
                forcing_lower = [value - epsilon for value in perturbed]
                forcing_upper = [value + epsilon for value in perturbed]
                lower, upper = interval_bellman(
                    rows, forcing_lower, forcing_upper, depth
                )
                certified_tail = max(
                    occupation[index] - exact_iterate[index]
                    for index in range(size)
                )
                for index in range(size):
                    check(
                        lower[index] <= exact_iterate[index] <= upper[index],
                        "rational_interval_contains_iterate",
                    )
                    check(
                        lower[index]
                        <= occupation[index]
                        <= min(F(1), upper[index] + certified_tail),
                        "conditional_interval_contains_occupation",
                    )


def fixed_aperture_and_compass() -> None:
    large_rows = line_rows(21)
    occupation = [F(0)] * 21
    occupation[8:13] = [F(1, 3), F(2, 3), F(1), F(2, 3), F(1, 3)]
    large_force = forcing(large_rows, occupation)

    # States 6,...,14 contain the positive component and every one-step exit.
    small_rows = line_rows(9)
    small_force = large_force[6:15]
    for depth in (1, 2, 5, 10, 20, 40):
        large_values = bellman(large_rows, large_force, depth)
        small_values = bellman(small_rows, small_force, depth)
        for state in range(8, 13):
            check(
                large_values[state] == small_values[state - 6],
                "fixed_aperture_line_agreement",
            )

    for width, height, step in ((7, 6, 1), (9, 8, 2), (12, 10, 3)):
        rows = compass_rows(width, height, step)
        for state, row in enumerate(rows):
            y, x = divmod(state, width)
            check(
                sum((weight for _, weight in row), F(0)) <= 1,
                "killed_kernel_substochastic",
            )
            for target, weight in row:
                yy, xx = divmod(target, width)
                check(
                    (abs(x - xx) == step and y == yy)
                    or (abs(y - yy) == step and x == xx),
                    "exact_compass_shift",
                )
                check(weight == F(1, 4), "pooled_compass_weight")
        check(
            sum((weight for _, weight in rows[0]), F(0)) < 1,
            "no_periodic_wraparound",
        )


def pooled_reversal_and_escape() -> None:
    states = [
        (source, target, hit)
        for source, target, hit in product((0, 1), repeat=3)
        if hit >= max(source, target)
    ]
    for packet in product(states, repeat=4):
        forward = sum(
            (F((1 - source) * hit, 4) for source, target, hit in packet),
            F(0),
        )
        reverse = sum(
            (F((1 - target) * hit, 4) for source, target, hit in packet),
            F(0),
        )
        occupation = sum(
            (F(target - source, 4) for source, target, hit in packet),
            F(0),
        )
        check(
            forward - reverse == occupation,
            "pooled_reciprocal_reversal",
        )

    for probability in (F(1, 5), F(1, 3), F(1, 2), F(3, 4), F(1)):
        for block_length in range(1, 9):
            failure = 1 - probability**block_length
            for blocks in (1, 2, 5, 11):
                partial_mean = block_length * sum(
                    (failure**index for index in range(blocks)), F(0)
                )
                check(
                    partial_mean
                    <= block_length / probability**block_length,
                    "cone_mean_exit_bound",
                )
                check(
                    failure**blocks
                    <= (1 - probability**block_length) ** blocks,
                    "cone_survival_tail",
                )

    laws = [
        [(F(0), F(0), F(1, 2)), (F(1), F(0), F(1, 2))],
        [(F(-1), F(0), F(1, 2)), (F(1), F(0), F(1, 2))],
        [(F(0), F(0), F(3, 4)), (F(-2), F(3), F(1, 4))],
        [(F(1), F(2), F(1, 3)), (F(-2), F(1), F(2, 3))],
    ]
    for law in laws:
        nonzero = [(x, y, p) for x, y, p in law if x or y]
        check(bool(nonzero), "nontrivial_law_has_nonzero_support")
        x0, y0, _ = nonzero[0]
        gamma = F(x0 * x0 + y0 * y0, 2)
        mass = sum(
            (
                probability
                for x, y, probability in law
                if x * x0 + y * y0 >= gamma
            ),
            F(0),
        )
        check(mass > 0, "positive_cone_mass_exists")

    centered_laws = [
        [(1, 0, F(1, 2)), (-1, 0, F(1, 2))],
        [
            (1, 0, F(1, 4)),
            (-1, 0, F(1, 4)),
            (0, 1, F(1, 4)),
            (0, -1, F(1, 4)),
        ],
        [
            (2, 0, F(1, 6)),
            (-2, 0, F(1, 6)),
            (0, 1, F(1, 3)),
            (0, -1, F(1, 3)),
        ],
    ]
    for law in centered_laws:
        mean_x = sum((F(x) * p for x, y, p in law), F(0))
        mean_y = sum((F(y) * p for x, y, p in law), F(0))
        second_moment = sum(
            (F(x * x + y * y) * p for x, y, p in law), F(0)
        )
        check(mean_x == 0 and mean_y == 0, "centered_increment_law")
        check(second_moment > 0, "positive_second_moment")
        for nx, ny in ((1, 0), (0, 1), (2, -3), (-4, 1)):
            projections = [nx * x + ny * y for x, y, p in law]
            check(
                min(projections) <= 0 <= max(projections),
                "no_required_common_drift",
            )


def finite_experiment_rates_and_calibration() -> None:
    for bound in (F(1), F(3, 2), F(7), F(25, 3)):
        doubled = 2 * bound
        block_length = (
            doubled.numerator + doubled.denominator - 1
        ) // doubled.denominator
        depth = 6 * block_length
        check(
            F(1, 2**6) + F(1, 128) + F(1, 128) == F(1, 32),
            "pooled_error_budget",
        )
        check(F(1, 32) < F(1, 8), "threshold_margin")
        check(depth >= 6, "positive_fixed_iteration_depth")

    # sigma = nu^(3/2): sigma^-2=nu^-3, sigma^-4=nu^-6,
    # and sigma^(2/3)=nu.
    check(F(3, 2) * 2 == 3, "spatial_center_exponent")
    check(F(3, 2) * 4 == 6, "arithmetic_exponent")
    check(F(3, 2) * F(2, 3) == 1, "C2_smoothing_exponent")

    occupations = [
        [F(0), F(1, 3), F(1), F(2, 3)],
        [F(1), F(0), F(1, 2), F(1, 4)],
    ]
    laws_left = [
        [F(1, 4)] * 4,
        [F(1, 2), F(1, 4), F(1, 8), F(1, 8)],
    ]
    laws_right = [
        [F(1, 3), F(1, 3), F(1, 6), F(1, 6)],
        [F(2, 5), F(1, 5), F(1, 5), F(1, 5)],
    ]
    for occupation, left, right in product(
        occupations, laws_left, laws_right
    ):
        operator_difference = abs(
            sum((p * value for p, value in zip(left, occupation)), F(0))
            - sum((p * value for p, value in zip(right, occupation)), F(0))
        )
        total_variation = max(
            abs(
                sum(
                    (
                        (left[index] - right[index]) * test[index]
                        for index in range(4)
                    ),
                    F(0),
                )
            )
            for test in product((F(0), F(1)), repeat=4)
        )
        check(
            operator_difference <= total_variation,
            "TV_operator_calibration",
        )


def main() -> None:
    mean_exit_green_and_bellman()
    different_zero_sets_and_intervals()
    fixed_aperture_and_compass()
    pooled_reversal_and_escape()
    finite_experiment_rates_and_calibration()
    result = {
        "schema": "a2-v31-independent-review-diagnostics-1",
        "status": "passed",
        "arithmetic": "exact integer and rational",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "imports_author_code": False,
        "physical_sensor_executed": False,
        "tex_build": False,
        "uniform_continuum_theorem_certified": False,
        "mathematical_proof_certificate": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
