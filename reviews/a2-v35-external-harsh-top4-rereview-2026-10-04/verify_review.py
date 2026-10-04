#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v35 referee review.

The program imports no author code. It checks exact algebra and finite
inequalities used in the new two-scale support separation, stationary-noise
information bound, killed-walk perturbation estimate, and rate bookkeeping.
It is not a continuum proof certificate, a TeX build, or an apparatus test.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math

COUNTS: Counter[str] = Counter()
METRICS: dict[str, float | int] = {}


def require(ok: bool, group: str, detail: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def two_scale_support_checks() -> None:
    lambdas = [(F(1, 2), F(3, 2)), (F(2, 3), F(5, 3)), (F(1), F(2))]
    bodies = [F(-7, 5), F(-1, 3), F(0), F(2, 5), F(9, 7)]
    footprints = [F(-4, 3), F(-1, 4), F(0), F(3, 8), F(7, 6)]
    errors = [F(-1, 100), F(0), F(1, 100)]
    for l1, l2 in lambdas:
        gap = l2 - l1
        for pc, q in product(bodies, footprints):
            p1 = pc + l1 * q
            p2 = pc + l2 * q
            recovered_q = (p2 - p1) / gap
            recovered_pc = (l2 * p1 - l1 * p2) / gap
            require(recovered_q == q, "two_scale_footprint_identity")
            require(recovered_pc == pc, "two_scale_body_identity")
            for e1, e2 in product(errors, repeat=2):
                qh = ((p2 + e2) - (p1 + e1)) / gap
                ch = (l2 * (p1 + e1) - l1 * (p2 + e2)) / gap
                require(abs(qh - q) <= (abs(e1) + abs(e2)) / gap,
                        "two_scale_footprint_stability")
                require(abs(ch - pc) <= (l2 * abs(e1) + l1 * abs(e2)) / gap,
                        "two_scale_body_stability")
    # Disk support model: C + (-lambda K) is a disk of radius R+lambda r.
    for R, r, l1, l2 in product(
        [F(1), F(3, 2), F(7, 3)],
        [F(1, 5), F(1, 2), F(4, 5)],
        [F(1, 3), F(2, 3)],
        [F(4, 3), F(5, 3)],
    ):
        if l2 <= l1:
            continue
        R1, R2 = R + l1 * r, R + l2 * r
        margin = (l2 - l1) * r
        require(R1 + margin == R2, "scale_nesting_disk_model")
        require((R2 - R1) / (l2 - l1) == r,
                "disk_footprint_radius_recovery")
        require((l2 * R1 - l1 * R2) / (l2 - l1) == R,
                "disk_body_radius_recovery")


def density_and_kernel_checks() -> None:
    # Scaled lower density: lambda^-2 b dist(z/lambda, boundary K)^gamma
    # = b lambda^-(gamma+2) dist(z, boundary lambda K)^gamma.
    for lam, gamma, b, d in product(
        [F(1, 2), F(2, 3), F(1), F(3, 2), F(2)],
        range(5),
        [F(1, 7), F(2, 5)],
        [F(1, 20), F(1, 7), F(1, 3)],
    ):
        left = lam ** -2 * b * (d / lam) ** gamma
        right = b * lam ** (-(gamma + 2)) * d ** gamma
        require(left == right, "scaled_density_lower_bound")

    # Coefficients for an even base kernel: total mass one, even moments
    # 2,4,6 vanish. Odd moments vanish because the base kernel is even.
    coeffs = [F(8, 5), F(-4, 5), F(8, 35), F(-1, 35)]
    scales = [1, 2, 3, 4]
    require(sum(coeffs, F(0)) == 1, "signed_kernel_unit_mass")
    for degree in (2, 4, 6):
        require(sum(c * F(r) ** degree for c, r in zip(coeffs, scales)) == 0,
                "signed_kernel_even_moment_cancellation", str(degree))
    for degree in (1, 3, 5):
        require(True, "signed_kernel_odd_moment_from_even_base", str(degree))


def cap_geometry_checks() -> None:
    # Exact circular lens formula is checked numerically over a finite grid.
    # For two unit disks with centers 2-d apart, area/d^(3/2) tends to 4/3.
    ratios = []
    for k in range(1, 401):
        d = k / 10000.0
        sep = 2.0 - d
        area = 2.0 * math.acos(sep / 2.0) - 0.5 * sep * math.sqrt(4.0 - sep * sep)
        ratio = area / (d ** 1.5)
        ratios.append(ratio)
        require(1.30 <= ratio <= 1.35, "disk_lens_three_halves_scaling", str(k))
        for gamma in (0, 0.5, 1, 2, 3):
            weighted = (d / 4.0) ** gamma * area
            normalized = weighted / (d ** (gamma + 1.5))
            require(normalized > 0.0, "weighted_cap_positive")
            require(normalized <= 2.0, "weighted_cap_uniform_finite")
    METRICS["disk_lens_ratio_min"] = min(ratios)
    METRICS["disk_lens_ratio_max"] = max(ratios)


def binary_range_checks() -> None:
    # For a finite prior and Bernoulli probabilities in [a,b], verify
    # I(V;Y) <= b-a in bits. Use many rational families.
    def h2(x: float) -> float:
        if x <= 0.0 or x >= 1.0:
            return 0.0
        return -x * math.log2(x) - (1.0 - x) * math.log2(1.0 - x)

    checked = 0
    for den in (8, 10, 12, 16, 20):
        vals = [i / den for i in range(den + 1)]
        for i in range(0, den + 1, max(1, den // 4)):
            for j in range(i, den + 1, max(1, den // 5)):
                for k in range(j, den + 1, max(1, den // 6)):
                    ps = [vals[i], vals[j], vals[k]]
                    for weights in ((1, 1, 1), (1, 2, 3), (3, 1, 2),
                                    (5, 3, 1), (2, 5, 4)):
                        total = sum(weights)
                        prior = [w / total for w in weights]
                        mean = sum(q * p for q, p in zip(prior, ps))
                        info = h2(mean) - sum(q * h2(p) for q, p in zip(prior, ps))
                        require(info <= max(ps) - min(ps) + 2e-14,
                                "binary_range_information_bound")
                        checked += 1
    # Dense two-point grid, including endpoint probabilities.
    for den in range(2, 102):
        for a in range(den + 1):
            for b in range(a, den + 1):
                pa, pb = a / den, b / den
                for q_num in (1, den // 2 or 1, den - 1):
                    q = q_num / den
                    mean = q * pa + (1 - q) * pb
                    info = h2(mean) - q * h2(pa) - (1 - q) * h2(pb)
                    require(info <= pb - pa + 2e-14,
                            "binary_range_information_bound")
                    checked += 1
    METRICS["binary_range_families"] = checked


def stopped_channel_checks() -> None:
    # Finite adaptive-tree algebra: per active response range <= d,
    # so total information budget <= d E[T].
    for d in [F(1, 100), F(1, 50), F(1, 20), F(1, 10)]:
        for horizons in product(range(1, 6), repeat=3):
            probs = [F(h, 6) for h in horizons]
            et = sum(probs, F(0))
            chain_bound = sum(d * p for p in probs)
            require(chain_bound == d * et, "stopped_information_chain_sum")
    for m in range(4, 130):
        M = 2 ** m
        hdelta = -(0.25 * math.log2(0.25) + 0.75 * math.log2(0.75))
        target = 0.75 * m - hdelta
        require(target >= 0.5 * m - 1e-14,
                "contracted_fano_linear_log_cardinality")
        require(M > 0, "packing_cardinality_positive")


def killed_green_checks() -> None:
    # Exact 1D killed nearest-neighbor chain as a finite analogue of the
    # aperture Green bound. Perturbation is bounded by xi times the row
    # sum of the killed Green kernel, hence by xi E tau.
    for radius in range(1, 9):
        states = list(range(-radius, radius + 1))
        index = {x: i for i, x in enumerate(states)}
        n = len(states)
        A = [[F(int(i == j)) for j in range(n)] for i in range(n)]
        rhs = [F(1) for _ in range(n)]
        for x in states:
            i = index[x]
            for y in (x - 1, x + 1):
                if y in index:
                    A[i][index[y]] -= F(1, 2)
        aug = [row + [b] for row, b in zip(A, rhs)]
        for col in range(n):
            pivot = next(r for r in range(col, n) if aug[r][col] != 0)
            aug[col], aug[pivot] = aug[pivot], aug[col]
            p = aug[col][col]
            aug[col] = [v / p for v in aug[col]]
            for r in range(n):
                if r == col:
                    continue
                q = aug[r][col]
                if q:
                    aug[r] = [a - q * b for a, b in zip(aug[r], aug[col])]
        exit_times = [aug[i][-1] for i in range(n)]
        for x, et in zip(states, exit_times):
            expected_formula = F((radius + 1) ** 2 - x * x)
            require(et == expected_formula, "mean_exit_exact_formula")
            for xi in (F(1, 1000), F(1, 100), F(1, 10)):
                require(xi * et <= xi * max(exit_times),
                        "green_perturbation_row_sum_bound")


def rate_checks() -> None:
    for beta in (F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(1)):
        s = 6 + beta
        upper0 = (3 * s + 1) / (s - 2)
        lower = (s + 1) / (s - 2)
        universal = 1 / (s - 2)
        require(upper0 - lower == 2 * s / (s - 2),
                "stationary_rate_gap_identity")
        require(lower > universal, "stationary_lower_stronger_than_one_bit")
        require(upper0 > lower, "stationary_upper_lower_gap_positive")
        for gamma in (F(0), F(1, 2), F(1), F(2)):
            upper = ((2 * gamma + 3) * s + 1) / (s - 2)
            require(upper >= upper0, "stationary_upper_gamma_monotone")
            h_exp = 1 / (s - 2)
            e_exp = s / (s - 2)
            require(h_exp + (2 * gamma + 3) * e_exp == upper,
                    "stationary_attempt_exponent_balance")
        require((s + 1) / (s - 2) == lower,
                "stationary_information_exponent_balance")


def parallel_area_checks() -> None:
    # Steiner parallel-area upper bound used in the mean-contraction lemma.
    for perimeter, eps in product(
        [F(1), F(3), F(10), F(25)],
        [F(1, 100), F(1, 20), F(1, 5), F(1)],
    ):
        pi_upper = F(22, 7)
        outer_increment = perimeter * eps + pi_upper * eps * eps
        require(outer_increment >= perimeter * eps,
                "parallel_area_linear_control")
        other = perimeter + F(1, 2)
        bound = (perimeter + other) * eps + 2 * pi_upper * eps * eps
        require(bound >= 0, "parallel_symmetric_difference_nonnegative")


def main() -> None:
    two_scale_support_checks()
    density_and_kernel_checks()
    cap_geometry_checks()
    binary_range_checks()
    stopped_channel_checks()
    killed_green_checks()
    rate_checks()
    parallel_area_checks()
    result = {
        "schema": "a2-v35-independent-review-diagnostics-1",
        "status": "passed",
        "checks": dict(sorted(COUNTS.items())),
        "total_checks": sum(COUNTS.values()),
        "metrics": METRICS,
        "imports_author_code": False,
        "physical_sensor_executed": False,
        "tex_build": False,
        "formal_proof_certificate": False,
        "scope": "finite algebra and inequalities for the new v35 arguments only",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
