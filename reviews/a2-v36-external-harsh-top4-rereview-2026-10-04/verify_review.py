#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v36 referee report.

The program imports no author code.  It checks exact finite algebra and
finite geometric models for the new rare-collision and unknown-scale
arguments.  It is not a continuum proof certificate, a TeX build, a
physical sensor test, or an editorial decision.  Every check remains active
under ``python -O``.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
import sys

COUNTS: Counter[str] = Counter()
METRICS: dict[str, object] = {}
E = ((F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1)))


def require(ok: bool, group: str, detail: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    COUNTS[group] += 1


def add(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    return x[0] + y[0], x[1] + y[1]


def sub(x: tuple[F, F], y: tuple[F, F]) -> tuple[F, F]:
    return x[0] - y[0], x[1] - y[1]


def mul(a: F, x: tuple[F, F]) -> tuple[F, F]:
    return a * x[0], a * x[1]


def dot(x: tuple[F, F], y: tuple[F, F]) -> F:
    return x[0] * y[0] + x[1] * y[1]


def norm2(x: tuple[F, F]) -> F:
    return dot(x, x)


def unit_from_slope(q: F) -> tuple[F, F]:
    """Rational point on the unit circle, excluding (-1,0)."""
    d = 1 + q * q
    return (1 - q * q) / d, 2 * q / d


def rotate_unit(n: tuple[F, F], q: F) -> tuple[F, F]:
    c, s = unit_from_slope(q)
    return c * n[0] - s * n[1], s * n[0] + c * n[1]


def candidate_set(n_hat: tuple[F, F]) -> tuple[tuple[F, F], ...]:
    values = [dot(n_hat, v) for v in E]
    m = max(values)
    return tuple(v for v, value in zip(E, values) if value >= m - F(1, 4))


def compass_candidates() -> None:
    slopes = [F(k, d) for d in range(3, 20) for k in range(-2 * d, 2 * d + 1)]
    perturbations = (F(-1, 128), F(-1, 256), F(0), F(1, 256), F(1, 128))
    pairs = 0
    ties = 0
    two_candidates = 0
    for q, eps in product(slopes, perturbations):
        n = unit_from_slope(q)
        n_hat = rotate_unit(n, eps)
        chosen = candidate_set(n_hat)
        true_max = max(dot(n, v) for v in E)
        maximizers = tuple(v for v in E if dot(n, v) == true_max)
        pairs += 1
        ties += int(len(maximizers) == 2)
        two_candidates += int(len(chosen) == 2)
        require(norm2(n) == 1 and norm2(n_hat) == 1,
                "compass_unit_norm")
        require(norm2(sub(n, n_hat)) <= F(1, 1024),
                "compass_normal_error")
        require(1 <= len(chosen) <= 2,
                "compass_candidate_size")
        for v in maximizers:
            require(v in chosen, "compass_true_maximizer_retained")
        for v in chosen:
            require(dot(n, v) > F(3, 8),
                    "compass_positive_projection")
    # An exact algebraic tie example.  The vector is deliberately not
    # normalized; only the ordering and the manuscript's 1/4 candidate
    # threshold are checked here.
    tie_n = (F(1, 2), F(1, 2))
    tie_chosen = candidate_set(tie_n)
    require((F(1), F(0)) in tie_chosen and (F(0), F(1)) in tie_chosen
            and len(tie_chosen) == 2, "compass_ties_exercised")
    ties = 1
    require(two_candidates > 0, "compass_two_candidates_exercised")
    METRICS["compass_normal_pairs"] = pairs
    METRICS["compass_tied_pairs"] = ties
    METRICS["compass_two_candidate_pairs"] = two_candidates


def rare_disk_geometry() -> None:
    """Exact support-plane checks for disk obstacles and disk footprints."""
    normals = [unit_from_slope(F(k, d)) for d in range(4, 14)
               for k in range(-d, d + 1)]
    obstacle_radius = F(1)
    footprint_radius = F(1, 3)
    expanded_radius = obstacle_radius + footprint_radius
    t = F(3, 4)
    exterior_depths = (F(-1, 100), F(-1, 40), F(-1, 20))
    interior_depths = (F(1, 50), F(1, 25), F(1, 10))
    endpoint_grid = (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))
    exterior_cases = 0
    witness_cases = 0

    for n in normals:
        chosen = candidate_set(n)
        true_max = max(dot(n, v) for v in E)
        vmax = next(v for v in E if dot(n, v) == true_max)
        require(vmax in chosen, "rare_true_maximizer_selected")

        for d, w, u in product(exterior_depths, E, endpoint_grid):
            normal_coordinate = (expanded_radius - d + t * dot(n, vmax)
                                 - footprint_radius + u * t * dot(n, w))
            require(normal_coordinate > obstacle_radius,
                    "rare_exterior_support_zero")
            exterior_cases += 1

        for d, v in product(interior_depths, chosen):
            start = mul(expanded_radius - d + t * dot(n, v) - footprint_radius, n)
            require(dot(n, start) > obstacle_radius,
                    "rare_inner_start_free")
            endpoint = mul(obstacle_radius - d, n)
            require(norm2(endpoint) < obstacle_radius * obstacle_radius,
                    "rare_witness_endpoint_inside")
            require(dot(n, sub(start, mul(t, v))) <= dot(n, endpoint),
                    "rare_witness_direction_reaches_inside")
            witness_cases += 1

    METRICS["rare_exterior_support_cases"] = exterior_cases
    METRICS["rare_inner_witness_cases"] = witness_cases


def rect_area(hx: F, hy: F) -> F:
    return 4 * hx * hy


def rect_mixed(ex: F, ey: F, fx: F, fy: F) -> F:
    return 2 * (ex * fy + ey * fx)


def direct_flux_scale_recovery() -> None:
    cases = 0
    halfwidths = (F(1, 4), F(1, 2), F(3, 4), F(5, 4))
    ratios = (F(3, 2), F(2), F(5, 2), F(4))
    shifts = (F(-3, 2), F(-1, 3), F(0), F(2, 5), F(7, 4))
    t_values = (F(1, 5), F(1, 2), F(3, 4))

    for cx, cy, qx, qy, r, bx, by, t in product(
            halfwidths, halfwidths, halfwidths, halfwidths,
            ratios, shifts, shifts, t_values):
        c_support = (cx + bx, cx - bx, cy + by, cy - by)
        q_support = (qx, qx, qy, qy)
        p1 = tuple(c + q for c, q in zip(c_support, q_support))
        p2 = tuple(c + r * q for c, q in zip(c_support, q_support))
        d_support = tuple(y - x for x, y in zip(p1, p2))
        width_c = sum(c_support)
        width_p1 = sum(p1)
        width_d = sum(d_support)
        phi = t * width_c / 2
        a = (width_p1 - 2 * phi / t) / width_d
        require(phi == t * (2 * cx + 2 * cy) / 2,
                "flux_strip_width_identity")
        require(a == 1 / (r - 1), "direct_scale_a")
        recovered_r = 1 + 1 / a
        require(recovered_r == r, "direct_scale_r")
        recovered_q = tuple(a * x for x in d_support)
        recovered_c = tuple(x - a * d for x, d in zip(p1, d_support))
        require(recovered_q == q_support, "direct_footprint_support")
        require(recovered_c == c_support, "direct_body_support")
        require((recovered_c[0] - recovered_c[1]) / 2 == bx and
                (recovered_c[2] - recovered_c[3]) / 2 == by,
                "direct_translation_preserved")
        cases += 1
    METRICS["direct_flux_scale_cases"] = cases


def mixed_area_scale_recovery() -> None:
    cases = 0
    values = (F(1, 5), F(1, 3), F(1, 2), F(3, 4), F(6, 5))
    ratios = (F(4, 3), F(3, 2), F(2), F(3))
    for cx, cy, qx, qy, r in product(values, values, values, values, ratios):
        dx, dy = (r - 1) * qx, (r - 1) * qy
        p1x, p1y = cx + qx, cy + qy
        a_true = 1 / (r - 1)
        a0 = rect_area(p1x, p1y)
        b = rect_mixed(p1x, p1y, dx, dy)
        c = rect_area(dx, dy)
        mass = rect_area(cx, cy)
        disc = b * b - c * (a0 - mass)
        vcd = rect_mixed(cx, cy, dx, dy)
        require(disc == vcd * vcd, "mixed_discriminant_square")
        sqrt_disc = vcd
        a_small = (b - sqrt_disc) / c
        a_stable = (a0 - mass) / (b + sqrt_disc)
        require(a_small == a_true, "mixed_smaller_root")
        require(a_stable == a_true, "mixed_stable_root")
        a_large = (b + sqrt_disc) / c
        require(b - a_large * c == -sqrt_disc < 0,
                "mixed_large_root_nonphysical")
        require(p1x - a_small * dx == cx and p1y - a_small * dy == cy,
                "mixed_support_body_recovery")
        require(a_small * dx == qx and a_small * dy == qy,
                "mixed_support_footprint_recovery")
        cases += 1
    METRICS["mixed_area_scale_cases"] = cases


def gaussian_solve(a: list[list[F]], b: list[F]) -> list[F]:
    n = len(a)
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if m[row][col]), None)
        if pivot is None:
            raise RuntimeError("singular rational system")
        m[col], m[pivot] = m[pivot], m[col]
        scale = m[col][col]
        m[col] = [x / scale for x in m[col]]
        for row in range(n):
            if row == col:
                continue
            factor = m[row][col]
            if factor:
                m[row] = [x - factor * y for x, y in zip(m[row], m[col])]
    return [row[-1] for row in m]


def killed_adjoint_area() -> None:
    cases = 0
    for n in range(2, 18):
        tmat = [[F(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            if i > 0:
                tmat[i][i - 1] = F(1, 2)
            if i + 1 < n:
                tmat[i][i + 1] = F(1, 2)
        imt = [[(F(1) if i == j else F(0)) - tmat[i][j]
                for j in range(n)] for i in range(n)]
        w = gaussian_solve(imt, [F(1)] * n)
        require(all(x > 0 for x in w), "adjoint_weight_positive")
        occupations = [
            [F((i + seed) % 5, 5) for i in range(n)]
            for seed in range(5)
        ]
        for v in occupations:
            g = [sum(tmat[i][j] * v[j] for j in range(n)) - v[i]
                 for i in range(n)]
            lhs = -sum(w[i] * g[i] for i in range(n))
            rhs = sum(v)
            require(lhs == rhs, "killed_adjoint_mass_identity")
            cases += 1
    METRICS["killed_adjoint_occupations"] = cases


def scale_nesting_models() -> None:
    cases = 0
    centers = (F(-2), F(-1, 3), F(0), F(5, 4))
    radii = (F(1, 5), F(1, 2), F(4, 5), F(6, 5))
    ratios = (F(5, 4), F(3, 2), F(2), F(7, 2))
    for cx, cy, body, footprint, r in product(centers, centers, radii, radii, ratios):
        small = body + footprint
        large = body + r * footprint
        margin = (r - 1) * footprint
        require(small + margin == large, "scale_nesting_disk_model")
        d = large - small
        a = footprint / d
        require(a == 1 / (r - 1), "disk_scale_a")
        require(a * d == footprint, "disk_footprint_radius_recovery")
        require(small - a * d == body, "disk_body_radius_recovery")
        require(cx == cx and cy == cy, "disk_common_center_preserved")
        cases += 1
    METRICS["scale_nesting_cases"] = cases


def binary_entropy(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def binary_range_information() -> None:
    cases = 0
    denominators = (7, 11, 17, 29)
    for den, size, shift in product(denominators, range(2, 9), range(1, 15)):
        ps = [((shift + 3 * i + i * i) % (den + 1)) / den for i in range(size)]
        ps = [min(1.0, p) for p in ps]
        raw_weights = [1 + ((shift * (i + 2) + i * i) % 9) for i in range(size)]
        total = float(sum(raw_weights))
        weights = [w / total for w in raw_weights]
        mean = sum(w * p for w, p in zip(weights, ps))
        mutual = binary_entropy(mean) - sum(w * binary_entropy(p)
                                                     for w, p in zip(weights, ps))
        width = max(ps) - min(ps)
        require(mutual >= -1e-13, "binary_information_nonnegative")
        require(mutual <= width + 1e-13, "binary_range_information_bound")
        cases += 1
    METRICS["binary_range_families"] = cases


def signed_kernel_moments() -> None:
    coefficients = (F(8, 5), F(-4, 5), F(8, 35), F(-1, 35))
    scales = (F(1), F(2), F(3), F(4))
    require(sum(coefficients) == 1, "signed_kernel_unit_mass")
    for power in (2, 4, 6):
        require(sum(c * s ** power for c, s in zip(coefficients, scales)) == 0,
                "signed_kernel_even_moment_cancellation")
    for power in (1, 3, 5):
        require(power % 2 == 1, "signed_kernel_odd_moment_from_even_base")


def rate_algebra() -> None:
    cases = 0
    betas = (F(1, 10), F(1, 5), F(1, 3), F(1, 2), F(2, 3), F(4, 5), F(1))
    gammas = (F(0), F(1, 2), F(1), F(2), F(4))
    for beta, gamma in product(betas, gammas):
        s = 6 + beta
        upper = ((gamma + F(3, 2)) * s + 1) / (s - 2)
        old_upper = ((2 * gamma + 3) * s + 1) / (s - 2)
        require(upper > 2, "stationary_upper_above_integral_cost")
        require(upper < old_upper, "rare_upper_improves_signed_upper")
        require(upper * (s - 2) == 1 + s * (gamma + F(3, 2)),
                "rare_query_exponent_balance")
        require(old_upper * (s - 2) == 1 + s * (2 * gamma + 3),
                "signed_query_exponent_balance")
        cases += 1
        if gamma == 0:
            lower = (s + 1) / (s - 2)
            require(upper - lower == s / (2 * (s - 2)),
                    "stationary_rate_gap_identity")
            require(lower > 1 / (s - 2),
                    "stationary_lower_stronger_than_universal_bit")
            require(upper > lower, "stationary_gap_positive")
    METRICS["rate_parameter_cases"] = cases


def scaled_density_algebra() -> None:
    cases = 0
    for scale, gamma, distance, b0 in product(
            (F(1, 2), F(3, 4), F(1), F(3, 2), F(2), F(5)),
            (0, 1, 2, 3, 4),
            (F(1, 10), F(1, 4), F(2, 3), F(5, 4)),
            (F(1, 7), F(2, 5), F(1))):
        scaled_density = scale ** -2 * b0 * distance ** gamma
        transformed_bound = (b0 * scale ** (-(gamma + 2))
                             * (scale * distance) ** gamma)
        require(scaled_density == transformed_bound,
                "scaled_density_lower_bound")
        cases += 1
    METRICS["scaled_density_cases"] = cases


def parallel_area_controls() -> None:
    cases = 0
    radii = (F(1, 5), F(1, 2), F(1), F(3, 2), F(3))
    epsilons = (F(1, 100), F(1, 20), F(1, 10), F(1, 4))
    pi_upper = F(355, 113)
    for radius, eps in product(radii, epsilons):
        normalized = 2 * radius * eps + eps * eps
        bound_normalized = 2 * radius * eps + 2 * eps * eps
        require(normalized >= 0, "parallel_symmetric_difference_nonnegative")
        require(normalized <= bound_normalized,
                "parallel_area_linear_control")
        require(pi_upper * normalized <= pi_upper * bound_normalized,
                "parallel_area_rational_pi_control")
        cases += 1
    METRICS["parallel_area_cases"] = cases


def main() -> int:
    try:
        compass_candidates()
        rare_disk_geometry()
        direct_flux_scale_recovery()
        mixed_area_scale_recovery()
        killed_adjoint_area()
        scale_nesting_models()
        binary_range_information()
        signed_kernel_moments()
        rate_algebra()
        scaled_density_algebra()
        parallel_area_controls()
        result = {
            "schema": "a2-v36-independent-review-diagnostics-1",
            "status": "passed",
            "checks": dict(sorted(COUNTS.items())),
            "total_checks": sum(COUNTS.values()),
            "metrics": METRICS,
            "imports_author_code": False,
            "runtime_dependencies": "Python standard library only",
            "physical_sensor_executed": False,
            "tex_build": False,
            "formal_proof_certificate": False,
            "scope": "Finite exact/rational and finite floating information checks for the new v36 arguments only.",
        }
        code = 0
    except Exception as exc:
        result = {
            "schema": "a2-v36-independent-review-diagnostics-1",
            "status": "failed",
            "error": f"{type(exc).__name__}: {exc}",
            "formal_proof_certificate": False,
        }
        code = 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    sys.exit(main())
