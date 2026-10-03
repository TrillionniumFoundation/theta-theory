#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v29 referee report.

The script imports no author module. It checks exact finite algebra behind
reversal balance, finite-chain inversion, zero witnesses, grid constants,
period arithmetic, and the displayed rate exponents. It is not a proof
certificate, a physical sensor experiment, a TeX build, or an editorial
judgment.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
import json
import math

COUNTS: Counter[str] = Counter()


def require(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def bit_identity(x0: int, x1: int, hit: int) -> bool:
    forward = (1 - x0) * hit
    reverse = (1 - x1) * hit
    return forward - reverse == x1 - x0


def reversal_checks() -> None:
    endpoint_cases = [(0, 0, 0), (0, 0, 1), (0, 1, 1),
                      (1, 0, 1), (1, 1, 1)]
    for x0, x1, hit in endpoint_cases:
        require(bit_identity(x0, x1, hit), "reversal_endpoint_cases")

    # Finite segment patterns include endpoint hits, interior-only hits,
    # multiple intersections, and empty segments.
    for n in range(122_940):
        length = 3 + (n % 9)
        state = (1103515245 * (n + 1) + 12345) & ((1 << length) - 1)
        bits = [(state >> j) & 1 for j in range(length)]
        hit = int(any(bits))
        require(bit_identity(bits[0], bits[-1], hit),
                "reversal_finite_segments", f"n={n}")

    # Discrete weighted analogue of the integrated balance identity.
    for n in range(16_324):
        state = (1664525 * (n + 7) + 1013904223) & ((1 << 10) - 1)
        chi = [(state >> j) & 1 for j in range(10)]
        lhs = Q(0)
        rhs = Q(0)
        for j in range(9):
            interior = (state >> ((j + 3) % 10)) & 1
            hit = int(bool(chi[j] or chi[j + 1] or interior))
            weight = Q(1 + ((n + 3 * j) % 11), 1 + ((2 * n + j) % 13))
            forward = (1 - chi[j]) * hit
            reverse = (1 - chi[j + 1]) * hit
            lhs += weight * (forward - reverse)
            rhs += weight * (chi[j + 1] - chi[j])
        require(lhs == rhs, "weighted_probability_balance", f"n={n}")


def chain_checks() -> None:
    for n in range(16_368):
        m = 1 + (n % 17)
        state = (22695477 * (n + 1) + 1) & ((1 << (m + 1)) - 1)
        values = [(state >> j) & 1 for j in range(m + 1)]
        values[n % (m + 1)] = 0
        diffs = [values[j + 1] - values[j] for j in range(m)]
        partial = [0]
        for d in diffs:
            partial.append(partial[-1] + d)
        recovered = -min(partial)
        require(recovered == values[0], "binary_chain_inverse", f"n={n}")

    for n in range(18_564):
        m = 1 + (n % 19)
        values = [Q(((n + 5) * (j + 3) + j * j) % 23,
                    1 + ((n + j) % 7)) for j in range(m + 1)]
        minimum = min(values)
        values = [v - minimum for v in values]
        diffs = [values[j + 1] - values[j] for j in range(m)]
        partial = [Q(0)]
        for d in diffs:
            partial.append(partial[-1] + d)
        require(-min(partial) == values[0],
                "nonnegative_chain_inverse", f"n={n}")

    for n in range(24_606):
        m = 1 + (n % 21)
        values = [Q(((3 * n + 7) * (j + 1) + 2 * j * j) % 29,
                    2 + ((n + 2 * j) % 9)) for j in range(m + 1)]
        minimum = min(values)
        values = [v - minimum for v in values]
        diffs = [values[j + 1] - values[j] for j in range(m)]
        b = Q(1, 10_000 + n % 97)
        noisy = [d + (b if (n + j) % 2 == 0 else -b)
                 for j, d in enumerate(diffs)]
        partial = [Q(0)]
        for d in noisy:
            partial.append(partial[-1] + d)
        recovered = -min(partial)
        require(abs(recovered - values[0]) <= m * b,
                "chain_noise_bound", f"n={n}")

    for n in range(20):
        c0 = Q(n + 1, 7)
        c1 = c0 + Q(1, 11)
        delta0 = [Q(0)] * (2 + n)
        delta1 = [Q(0)] * (2 + n)
        require(delta0 == delta1 and c0 != c1,
                "zero_witness_necessity", f"n={n}")


def interval_occupied(x: Q, components: list[tuple[Q, Q]]) -> bool:
    return any(left <= x <= right for left, right in components)


def zero_witness_checks() -> None:
    for n in range(4_480):
        diameter = Q(8 + n % 7, 8)
        separation = Q(17 + n % 5, 8)
        t = separation / (3 + n % 3)
        m = int(diameter // t) + 2
        components = []
        cursor = Q(-12)
        for _ in range(6):
            components.append((cursor, cursor + diameter))
            cursor += diameter + separation
        x = Q((37 * n) % 200 - 100, 9)
        chain = [x + k * t for k in range(m + 1)]
        require(not all(interval_occupied(y, components) for y in chain),
                "component_zero_witness", f"n={n}")

    for n in range(17_360):
        diameter = Q(10 + n % 9, 10)
        separation = Q(25 + n % 7, 10)
        sigma = separation / (10 + n % 5)
        expanded_diameter = diameter + 2 * sigma
        expanded_separation = separation - 2 * sigma
        t = expanded_separation / (3 + n % 4)
        m = int(expanded_diameter // t) + 2
        components = []
        cursor = Q(-15)
        for _ in range(7):
            components.append((cursor - sigma, cursor + diameter + sigma))
            cursor += diameter + separation
        x = Q((53 * n) % 300 - 150, 11)
        chain = [x + k * t for k in range(m + 1)]
        require(not all(interval_occupied(y, components) for y in chain),
                "expanded_component_zero_witness", f"n={n}")


def grid_and_rate_checks() -> None:
    for m in range(1, 1001):
        eps0 = Q(1, 256 * m)
        require(3 * eps0 < Q(1, 32 * m), "candidate_mean_tolerance")
        require(2 * m * 3 * eps0 < Q(1, 16),
                "occupation_grid_tolerance")
        # A grid discrepancy of 1/16 plus Lipschitz transport of 1/16.
        require(Q(1, 16) + Q(1, 16) == Q(1, 8),
                "covering_lipschitz_tolerance")

    require(Q(3, 2) * Q(2, 3) == 1, "C2_smoothing_exponent")
    require(1 - Q(2, 6) == Q(4, 6) == Q(2, 3),
            "compensated_smoothing_balance")
    require(-2 * Q(3, 2) == -3, "scalar_command_exponent")

    for n in range(2, 32):
        nu = Q(1, n)
        sigma_squared = nu ** 3
        # If sigma=nu^(3/2), then sigma^(-2)=nu^(-3).
        require(Q(1, sigma_squared) == nu ** -3,
                "scalar_attempt_power")


def det(u: tuple[int, int], v: tuple[int, int]) -> int:
    return u[0] * v[1] - u[1] * v[0]


def period_checks() -> None:
    # Two-sided finite motif checks on cyclic grids.
    for n in range(56_217):
        width = 3 + (n % 4)
        height = 2 + ((n // 4) % 3)
        size = width * height
        state = 6364136223846793005 * (n + 1) + 1442695040888963407
        motif = [((state >> (j % 61)) ^
                  (state >> ((3 * j + 7) % 61))) & 1 for j in range(size)]
        dx = 1 + ((n // 17) % (width - 1))
        dy = (n // 29) % height

        def value(x: int, y: int) -> int:
            return motif[(y % height) * width + (x % width)]

        global_period = all(value(x + dx, y + dy) == value(x, y)
                            for y in range(height) for x in range(width))
        two_sided = all(value(x + s * dx, y + s * dy) == value(x, y)
                        for y in range(height) for x in range(width)
                        for s in (-1, 1))
        require(global_period == two_sided,
                "two_sided_motif_period", f"n={n}")

    for n in range(400):
        a = 1 + n % 9
        d = 1 + (n // 9) % 11
        b = (3 * n) % 13 - 6
        D = ((a, 0), (b, d))
        index = abs(det(D[0], D[1]))
        require(index == a * d and index >= 1, "period_pair_index")

        scale_x = Q(2 + n % 5, 3 + n % 7)
        scale_y = Q(3 + n % 7, 4 + n % 5)
        z1 = (1 + n % 7, (2 * n) % 9 - 4)
        z2 = ((5 * n) % 11 - 5, 1 + (n // 7) % 8)
        multiple = det(z1, z2)
        physical_det = scale_x * scale_y * multiple
        covol = scale_x * scale_y
        require(physical_det / covol == multiple, "determinant_gap")

    for n in range(300):
        eta = Q(1 + n % 13, 10)
        e = eta / (100 + n % 17)
        measured_true = 14 * e + 6 * e
        measured_false = eta - 14 * e - 6 * e
        require(measured_true < eta / 2, "period_true_acceptance")
        require(measured_false > eta / 2, "nonperiod_rejection")

    matrices: list[tuple[tuple[int, int], tuple[int, int], int]] = []
    for idx in range(496):
        a = 1 + idx % 8
        d = 1 + (idx // 8) % 8
        b = (idx // 64) % 9 - 4
        c1 = (a, 0)
        c2 = (b, d)
        matrices.append((c1, c2, a * d))

    for matrix_index, (c1, c2, index) in enumerate(matrices):
        denominators: list[int] = []
        determinant = det(c1, c2)
        require(abs(determinant) == index,
                "common_denominator_divides_pair_index")
        for x in range(-3, 4):
            for y in range(-3, 4):
                w = (x, y)
                coord1 = Q(det(w, c2), determinant)
                coord2 = Q(det(c1, w), determinant)
                denominators.extend((coord1.denominator, coord2.denominator))
                require(index % coord1.denominator == 0 and
                        index % coord2.denominator == 0,
                        "bounded_denominator_coordinates",
                        f"matrix={matrix_index}, w={w}")
        common = 1
        for denominator in denominators:
            common = math.lcm(common, denominator)
        if index % common != 0:
            raise RuntimeError(
                f"common denominator {common} does not divide {index}")


def main() -> None:
    reversal_checks()
    chain_checks()
    zero_witness_checks()
    grid_and_rate_checks()
    period_checks()
    result = {
        "schema": "a2-v29-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "imports_author_code": False,
        "arithmetic": "exact integer/rational",
        "physical_sensor_executed": False,
        "uniform_continuum_proof_certified": False,
        "tex_build": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
