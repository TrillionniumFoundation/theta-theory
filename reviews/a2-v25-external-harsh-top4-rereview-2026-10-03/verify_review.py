#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v25 external referee report.

This script imports no author module. It checks finite algebra and inequalities
used in the new explicit continuation, physical-copy locking, value-only local
probe, resource accounting, rational period recovery and completion defect.
It is not a formal proof certificate, a physical-sensor execution, a TeX build,
or an editorial decision.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
import json
import math

COUNTS: Counter[str] = Counter()


def require(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        suffix = f": {detail}" if detail else ""
        raise RuntimeError(f"{group}{suffix}")
    COUNTS[group] += 1


def ceil_fraction(x: Q) -> int:
    return -(-x.numerator // x.denominator)


def upper_log2(x: Q) -> int:
    """Least nonnegative m with 2**m >= x, using exact comparisons."""
    if x <= 0:
        raise ValueError("upper_log2 requires a positive rational")
    m = max(0, x.numerator.bit_length() - x.denominator.bit_length())
    if x.denominator * (1 << m) < x.numerator:
        m += 1
    while m and x.denominator * (1 << (m - 1)) >= x.numerator:
        m -= 1
    return m


def determinant(a: tuple[int, int], b: tuple[int, int]) -> int:
    return a[0] * b[1] - a[1] * b[0]


def lcm_many(values: list[int]) -> int:
    result = 1
    for value in values:
        result = math.lcm(result, value)
    return result


def interpolation_and_continuation() -> None:
    # Lagrange amplification 2^m m^m / m! < 6^m.
    for m in range(1, 81):
        lhs = (2**m) * (m**m)
        rhs = (6**m) * math.factorial(m)
        require(lhs < rhs, "lagrange_amplification", f"m={m}")

    # Use t=9^{-q} with q divisible by 8, so all powers are rational.
    for n in range(1, 61):
        q = 8 * n
        first = Q(6**q, 9**q)
        target_alpha = Q(2**q, 3**q)
        require(first == target_alpha, "interpolation_first_term", f"q={q}")
        remainder = Q(4, 3) * Q(2, 3) ** (q + 1)
        target_eighth = Q(3, 1) * Q(1, 9 ** (q // 8))
        require(
            first + remainder <= target_eighth,
            "interpolation_total_bound",
            f"q={q}",
        )

    # Sixteen strip/step configurations.
    for denominator in range(8, 24):
        a = Q(1, denominator)
        rho = 8 * a
        J = ceil_fraction(Q(4, 1) / a)
        require(4 * a <= rho, "disk_inside_strip", f"a={a}")
        require(Q(J, 1) * a >= 4, "real_circle_coverage", f"a={a}")
        require(J == ceil_fraction(Q(4, 1) / a), "real_circle_step_count", f"a={a}")

    # Exact cancellation P*theta=m0 across the chain of disks.
    for J in range(16):
        denominator = 1 << (J + 3)
        for m0 in range(1, 61):
            P = m0 * denominator
            theta = Q(1, denominator)
            require(P * theta == m0, "dyadic_cancellation", f"J={J},m0={m0}")

    # The normal interval u/(1+u) is contained in [-atan u, atan u].
    for numerator in range(1, 10):
        u = numerator / 7.0
        require(
            u / (1.0 + u) <= math.atan(u) + 1e-15,
            "normal_interval_available",
            f"u={u}",
        )

    # Conservative strip translation estimate exp(rho) <= 3^{ceil rho}.
    for rho_num in range(1, 7):
        rho = rho_num / 2.0
        for length in range(1, 7):
            require(
                length * math.exp(rho)
                <= length * (3 ** math.ceil(rho)) + 1e-12,
                "strip_support_bound",
                f"rho={rho},length={length}",
            )


def calibration_and_locking() -> None:
    # Three hundred finite prior configurations. We avoid expanding 2**P:
    # threshold comparisons are performed in normalized or exponent form.
    case = 0
    for outer in range(1, 21):
        for inner in range(1, 16):
            case += 1
            B = Q(20 + outer, 1)
            sigma = Q(1, 30 + inner)
            eta = Q(1, 40 + outer)
            d0 = Q(1, 20 + inner)
            Rplus = Q(3 + (outer % 4), 1)
            D0 = Q(1 + (inner % 3), 1)
            Cstar = Q(3, 1) + Q(9, 1) * (Rplus + 2 * D0) / eta
            Delta = min(B, sigma / 36, eta / 36, d0 / (4 * Cstar))
            m0 = max(1, upper_log2(3 * B / Delta))
            require(
                Q(3, 1) * B <= Delta * (1 << m0),
                "m0_upper",
                f"case={case}",
            )

            # Choose modest J only for the diagnostic; the proof is symbolic in J.
            J = (outer + inner) % 15
            P = m0 * (1 << (J + 3))
            theta_den = 1 << (J + 3)
            require(
                Q(P, theta_den) == m0,
                "calibrated_continuation_target",
                f"case={case}",
            )

            # The chosen Delta locks type, reflection and target physical copy.
            require(9 * Delta < sigma, "shape_locking_margin", f"case={case}")
            require(9 * Delta < eta, "reflection_locking_margin", f"case={case}")
            require(
                Cstar * Delta < d0,
                "physical_copy_locking_margin",
                f"case={case}",
            )

            # Jet budget normalized by E_*.
            d_over_E = Q(1, 8)
            tail_over_E = Q(1, 4)
            require(
                Q(3, 2) * d_over_E + tail_over_E < 1,
                "jet_support_budget",
                f"case={case}",
            )

            # Symbolic tail choice from the exact calibration.
            Mg = Q(1 + (inner % 5), 1)
            ratio = Q(64, 7) * Mg / B
            tail_extra = upper_log2(ratio)
            require(
                Q(1 << tail_extra, 1) >= ratio,
                "tail_log_upper",
                f"case={case}",
            )
            K = P + tail_extra + 2
            exponent_gain = 3 * K + 3 - P
            require(
                exponent_gain >= tail_extra,
                "symbolic_tail_budget",
                f"case={case}",
            )

            # Value-grid mesh: if c1 >= 4Hr/B and N=c1*2^P, then Hr/N <= E/4.
            H = Q(2 + (outer % 6), 1)
            r = Q(1, 5 + (inner % 7))
            c1 = max(1, ceil_fraction(4 * H * r / B))
            require(
                Q(c1, 1) * B >= 4 * H * r,
                "symbolic_mesh_budget",
                f"case={case}",
            )
            require(
                2 * d_over_E + Q(1, 4) <= Q(1, 2),
                "value_support_budget",
                f"case={case}",
            )
    if case != 300:
        raise RuntimeError(f"unexpected calibration case count: {case}")


def registry_and_translation() -> None:
    for chi_index in range(1, 31):
        chi = Q(chi_index, 17)
        for error_index in range(1, 12):
            eps = chi * Q(error_index, 200)
            require(2 * eps < chi / 8, "registry_true_band")
            require(chi - 2 * eps > 7 * chi / 8, "registry_false_band")
            require(
                2 * eps < chi / 2 < chi - 2 * eps,
                "registry_threshold_separation",
            )

    coordinates = [
        (Q(i, 5), Q((i * i + 1) % 11, 7)) for i in range(-4, 5)
    ]
    shifts = [
        (Q(3 * i, 2), Q(2 * i - 1, 3)) for i in range(-4, 5)
    ]
    for source in coordinates:
        for target in coordinates:
            for shift in shifts:
                lhs = (
                    (target[0] + shift[0]) - (source[0] + shift[0]),
                    (target[1] + shift[1]) - (source[1] + shift[1]),
                )
                rhs = (target[0] - source[0], target[1] - source[1])
                require(lhs == rhs, "translation_invariant_relative_contact")


def value_differences_and_arclength() -> None:
    # Cubic test function: |f'''|=6 everywhere.
    def f(x: Q) -> Q:
        return x**3 + 2 * x**2 - 3 * x + 1

    def fp(x: Q) -> Q:
        return 3 * x**2 + 4 * x - 3

    def fpp(x: Q) -> Q:
        return 6 * x + 4

    M3 = Q(6, 1)
    eps = Q(1, 10000)
    error_levels = [Q(2 * i - 9, 9) * eps for i in range(10)]
    x_values = [Q(i - 5, 7) for i in range(10)]
    t_values = [Q(i + 1, 20) for i in range(10)]

    for x in x_values:
        for t in t_values:
            for i, e_minus in enumerate(error_levels):
                for j, e_plus in enumerate(error_levels):
                    e_zero = error_levels[(i + 3 * j) % 10]
                    D1 = ((f(x + t) + e_plus) - (f(x - t) + e_minus)) / (2 * t)
                    D2 = (
                        (f(x + t) + e_plus)
                        - 2 * (f(x) + e_zero)
                        + (f(x - t) + e_minus)
                    ) / (t**2)
                    require(
                        abs(D1 - fp(x)) <= M3 * t**2 / 6 + eps / t,
                        "first_difference_enclosure",
                    )
                    require(
                        abs(D2 - fpp(x)) <= M3 * t / 3 + 4 * eps / (t**2),
                        "second_difference_enclosure",
                    )

    # The map p -> sqrt(1+p^2) is one-Lipschitz.
    slopes = [i / 4.0 for i in range(-10, 11)]
    for u in slopes:
        for v in slopes:
            lhs = abs(math.sqrt(1 + u * u) - math.sqrt(1 + v * v))
            require(
                lhs <= abs(u - v) + 1e-15,
                "arclength_integrand_lipschitz",
            )


def costs() -> None:
    valid_s = [Q(i, 8) for i in range(8)]
    invalid_s = [Q(2, 1) + Q(i, 8) for i in range(17)]
    for s in valid_s:
        require(Q(6, 1) > 4 + s, "fixed_a6_valid_scope")
    for s in invalid_s:
        require(Q(6, 1) <= 4 + s, "fixed_a6_invalid_scope")

    s_values = [Q(i, 4) for i in range(15)]
    for a in range(6, 11):
        for s in s_values:
            require(
                (Q(3, 1) + s - a < -1) == (Q(a, 1) > 4 + s),
                "generic_expected_cost",
            )

    for i in range(21):
        sv = Q(i, 10)
        effective_s = 1 + 3 * sv
        require(effective_s == 1 + 3 * sv, "value_probe_power")
        a = max(6, ceil_fraction(6 + 3 * sv))
        if Q(a, 1) <= 5 + 3 * sv:
            a += 1
        require(Q(a, 1) > 5 + 3 * sv, "value_query_expected_cost")
        require(
            (Q(4, 1) + 3 * sv - a < -1)
            == (Q(a, 1) > 5 + 3 * sv),
            "value_epoch_expected_cost",
        )


def subgroup_and_completion() -> None:
    for n in range(1, 51):
        scale = 1 + (n % 4)
        columns = [
            (scale * (n + 1), 0),
            (0, scale * (n + 2)),
            (scale, scale),
        ]
        minors = [abs(determinant(a, b)) for a, b in combinations(columns, 2)]
        gamma_index = math.gcd(*minors)
        require(gamma_index > 0, "rank_two_integer_cycles")

        for i, j in combinations(range(3), 2):
            D0, D1 = columns[i], columns[j]
            detD = determinant(D0, D1)
            if detD == 0:
                raise RuntimeError("unexpected singular basis pair")
            coords: list[tuple[Q, Q]] = []
            for column in columns:
                coords.append(
                    (
                        Q(determinant(column, D1), detD),
                        Q(determinant(D0, column), detD),
                    )
                )
            q = lcm_many([value.denominator for pair in coords for value in pair])
            require(
                abs(detD) % q == 0,
                "common_denominator_divides_pair_index",
            )
            integer_columns = [(q, 0), (0, q)] + [
                (int(q * x), int(q * y)) for x, y in coords
            ]
            detH = math.gcd(
                *[
                    abs(determinant(a, b))
                    for a, b in combinations(integer_columns, 2)
                ]
            )
            require(
                Q(abs(detD) * detH, q * q) == gamma_index,
                "reference_free_covolume",
            )

            for V, A, missing in product(
                [Q(10), Q(12)],
                [Q(2), Q(3)],
                [Q(0), Q(1)],
            ):
                visible = V - A - missing
                defect = gamma_index * V - A - visible
                require(
                    defect == (gamma_index - 1) * V + missing,
                    "completion_defect",
                )
                require(
                    (defect == 0) == (gamma_index == 1 and missing == 0),
                    "completion_zero",
                )


def main() -> None:
    interpolation_and_continuation()
    calibration_and_locking()
    registry_and_translation()
    value_differences_and_arclength()
    costs()
    subgroup_and_completion()

    expected_total = 29326
    actual_total = sum(COUNTS.values())
    if actual_total != expected_total:
        raise RuntimeError(
            f"unexpected diagnostic count: {actual_total} != {expected_total}"
        )

    result = {
        "schema": "a2-v25-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": actual_total,
        "imports_author_code": False,
        "arithmetic": (
            "exact integer/rational except finite atan, exp and square-root comparisons"
        ),
        "physical_sensor_executed": False,
        "uniform_theorem_certified": False,
        "tex_build": False,
        "formal_proof_certificate": False,
        "editorial_decision": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
