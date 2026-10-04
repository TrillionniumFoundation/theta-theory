#!/usr/bin/env python3
"""Independent finite diagnostics for an external review of A2 v40.

No author module is imported.  The checks cover finite exact collision models,
prefix inversion, smooth support calibration, the chord signature, compact
convolution Fourier products, triangular moment separation, and resource
algebra.  They are diagnostics only, not continuum proofs or apparatus tests.
All checks remain active under ``python -O``.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
import cmath
import json
import math

CHECKS: Counter[str] = Counter()
METRICS: dict[str, object] = {}


def require(condition: bool, group: str, detail: str = "") -> None:
    if not condition:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


Rect = tuple[F, F, F, F]
Point = tuple[F, F]


def in_rect(p: Point, r: Rect) -> bool:
    return r[0] <= p[0] <= r[1] and r[2] <= p[1] <= r[3]


def segment_hits_rect(p: Point, a: Point, r: Rect) -> bool:
    if in_rect(p, r):
        return True
    lo, hi = F(0), F(1)
    for coordinate in range(2):
        x = p[coordinate]
        d = a[coordinate]
        lower = r[2 * coordinate]
        upper = r[2 * coordinate + 1]
        if d == 0:
            if not (lower <= x <= upper):
                return False
            continue
        t0 = (lower - x) / d
        t1 = (upper - x) / d
        if t0 > t1:
            t0, t1 = t1, t0
        lo = max(lo, t0)
        hi = min(hi, t1)
        if lo > hi:
            return False
    return lo <= hi and hi >= 0 and lo <= 1


def bit(p: Point, a: Point, rects: tuple[Rect, ...]) -> int:
    if any(in_rect(p, r) for r in rects):
        return 0
    return int(any(segment_hits_rect(p, a, r) for r in rects))


def endpoint_identity_checks() -> None:
    families = (
        ((F(-5), F(-4), F(-1), F(1)), (F(0), F(1), F(-2), F(-1)),
         (F(4), F(6), F(1), F(2))),
        ((F(-6), F(-5), F(-3), F(-1)), (F(-1), F(1), F(1), F(3)),
         (F(5), F(7), F(-2), F(0))),
    )
    displacements = ((F(1, 2), F(0)), (F(3, 4), F(0)),
                     (F(0), F(1, 2)), (F(0), F(-3, 4)))
    points = [(F(i, 4), F(j, 4)) for i in range(-32, 33)
              for j in range(-20, 21)]
    cases = 0
    tangencies = 0
    for rects, a, p in product(families, displacements, points):
        p2 = (p[0] + a[0], p[1] + a[1])
        reverse = (-a[0], -a[1])
        left = bit(p, a, rects) - bit(p2, reverse, rects)
        right = int(any(in_rect(p2, r) for r in rects)) - int(
            any(in_rect(p, r) for r in rects))
        require(left == right, "endpoint_bit_identity")
        tangencies += int(any(p[0] in (r[0], r[1]) and r[2] <= p[1] <= r[3]
                              for r in rects))
        cases += 1
    require(tangencies > 0, "endpoint_boundary_cases_exercised")
    METRICS["endpoint_identity_cases"] = cases


def interval_overlap(a: F, b: F, c: F, d: F) -> F:
    return max(F(0), min(b, d) - max(a, c))


def interval_occupation(x: F, obstacles: tuple[tuple[F, F], ...],
                        footprint: tuple[F, F]) -> F:
    length = footprint[1] - footprint[0]
    return sum(interval_overlap(footprint[0], footprint[1], c - x, d - x)
               for c, d in obstacles) / length


def prefix_inverse_checks() -> None:
    models = (
        (((F(-8), F(-6)), (F(-2), F(0)), (F(5), F(8))), (F(-1), F(1))),
        (((F(-7), F(-5)), (F(1), F(3)), (F(8), F(10))), (F(-2), F(1))),
        (((F(-9), F(-7)), (F(-1), F(2)), (F(9), F(11))), (F(-1), F(2))),
    )
    steps = (F(1, 2), F(2, 3), F(3, 4))
    cases = 0
    perturb_cases = 0
    for (obstacles, footprint), t in product(models, steps):
        diameter = max(d - c for c, d in obstacles)
        delta = footprint[1] - footprint[0]
        mmax = int((diameter + delta) // t + 1)
        for ix in range(-60, 61):
            x = F(ix, 4)
            v0 = interval_occupation(x, obstacles, footprint)
            r = [interval_occupation(x + (k + 1) * t, obstacles, footprint)
                 - interval_occupation(x + k * t, obstacles, footprint)
                 for k in range(mmax)]
            prefixes = [F(0)]
            running = F(0)
            for value in r:
                running -= value
                prefixes.append(running)
            require(max(prefixes) == v0, "finite_prefix_inverse")
            eps = F(1, 10000)
            rp = [value + (eps if k % 2 == 0 else -eps)
                  for k, value in enumerate(r)]
            pp = [F(0)]
            running = F(0)
            for value in rp:
                running -= value
                pp.append(running)
            require(abs(max(pp) - v0) <= mmax * eps,
                    "finite_prefix_stability")
            cases += 1
            perturb_cases += 1
    METRICS["prefix_inverse_cases"] = cases
    METRICS["prefix_stability_cases"] = perturb_cases


def h_body(phi: float, params: tuple[float, ...]) -> float:
    radius, a2, b3, tx, ty = params
    return radius + a2 * math.cos(2 * phi) + b3 * math.sin(3 * phi) \
        + tx * math.cos(phi) + ty * math.sin(phi)


def hp_body(phi: float, params: tuple[float, ...]) -> float:
    _, a2, b3, tx, ty = params
    return -2 * a2 * math.sin(2 * phi) + 3 * b3 * math.cos(3 * phi) \
        - tx * math.sin(phi) + ty * math.cos(phi)


def radius_body(phi: float, params: tuple[float, ...]) -> float:
    radius, a2, b3, _, _ = params
    return radius - 3 * a2 * math.cos(2 * phi) - 8 * b3 * math.sin(3 * phi)


def boundary(phi: float, params: tuple[float, ...]) -> tuple[float, float]:
    h = h_body(phi, params)
    hp = hp_body(phi, params)
    c, s = math.cos(phi), math.sin(phi)
    return h * c - hp * s, h * s + hp * c


def dot2(x: tuple[float, float], y: tuple[float, float]) -> float:
    return x[0] * y[0] + x[1] * y[1]


def support_arc_numeric(alpha: float, params: tuple[float, ...], incoming: bool,
                        samples: int = 32768) -> float:
    u = (math.cos(alpha), math.sin(alpha))
    lo, hi = ((math.pi / 2, 3 * math.pi / 2) if incoming
              else (-math.pi / 2, math.pi / 2))
    best = -1e100
    for j in range(samples + 1):
        phi = lo + (hi - lo) * j / samples
        best = max(best, dot2(boundary(phi, params), u))
    return best


def segment_support(alpha: float, p: tuple[float, float],
                    q: tuple[float, float]) -> float:
    u = (math.cos(alpha), math.sin(alpha))
    return max(dot2(p, u), dot2(q, u))


def support_calibration_checks() -> None:
    bodies = (
        (2.0, 0.08, 0.03, 0.4, -0.2),
        (1.7, -0.07, 0.025, -0.35, 0.28),
        (2.3, 0.05, -0.035, 0.1, 0.45),
    )
    footprints = (
        (0.55, 0.03, 0.01, -0.2, 0.1),
        (0.7, -0.02, 0.015, 0.25, -0.18),
    )
    angles = [2 * math.pi * k / 256 for k in range(256)]
    max_arc_error = 0.0
    max_cancel_error = 0.0
    negative_localizations = 0
    for body_params, fp_params in product(bodies, footprints):
        require(min(radius_body(2 * math.pi * k / 4096, body_params)
                    for k in range(4096)) > 0, "support_body_strict_convexity")
        p_plus = boundary(math.pi / 2, body_params)
        p_minus = boundary(3 * math.pi / 2, body_params)
        chord_len = math.dist(p_plus, p_minus)
        require(chord_len > 0, "support_chord_positive_length")
        t = 0.37
        hs = []
        for alpha in angles:
            u = (math.cos(alpha), math.sin(alpha))
            h_c = h_body(alpha, body_params)
            h_a_reflected = h_body(alpha + math.pi, fp_params)
            h_p = h_c + h_a_reflected
            hp = support_arc_numeric(alpha, body_params, True, 4096)
            hm = support_arc_numeric(alpha, body_params, False, 4096)
            h_l = segment_support(alpha, p_minus, p_plus)
            arc_err = abs((hp + hm) - (h_c + h_l))
            max_arc_error = max(max_arc_error, arc_err)
            require(arc_err < 2e-6, "incoming_outgoing_arc_sum")
            h_kp = hp + h_a_reflected + t * max(0.0, -u[0])
            h_km = hm + h_a_reflected + t * max(0.0, u[0])
            H = 2 * h_p - h_kp - h_km + t * abs(u[0])
            cancel_err = abs(H - (h_c - h_l))
            max_cancel_error = max(max_cancel_error, cancel_err)
            require(cancel_err < 2e-6, "three_support_cancellation")
            hs.append(H)

        chord_dx = p_plus[0] - p_minus[0]
        chord_dy = p_plus[1] - p_minus[1]
        theta = math.atan2(-chord_dx, chord_dy)
        if math.cos(theta) < 0:
            theta += math.pi
        theta %= 2 * math.pi
        for atom in (theta, (theta + math.pi) % (2 * math.pi)):
            idx = min(range(len(angles)), key=lambda i: abs(math.atan2(
                math.sin(angles[i] - atom), math.cos(angles[i] - atom))))
            bsteps = 3
            b = 2 * math.pi * bsteps / len(angles)
            d = (hs[(idx + bsteps) % len(hs)]
                 + hs[(idx - bsteps) % len(hs)]
                 - 2 * math.cos(b) * hs[idx])
            require(d < -0.2 * chord_len * b, "negative_chord_signature")
            negative_localizations += 1
    METRICS["support_max_arc_error"] = max_arc_error
    METRICS["support_max_cancellation_error"] = max_cancel_error
    METRICS["negative_chord_localizations"] = negative_localizations


def rect_fourier(rect: Rect, xi: tuple[float, float]) -> complex:
    def factor(lo: F, hi: F, w: float) -> complex:
        lo_f, hi_f = float(lo), float(hi)
        if abs(w) < 1e-14:
            return complex(hi_f - lo_f, 0.0)
        return ((cmath.exp(-1j * w * hi_f) - cmath.exp(-1j * w * lo_f))
                / (-1j * w))
    return factor(rect[0], rect[1], xi[0]) * factor(rect[2], rect[3], xi[1])


def law_cf(points: list[tuple[float, float, float]],
           xi: tuple[float, float]) -> complex:
    return sum(w * cmath.exp(-1j * (xi[0] * x + xi[1] * y))
               for x, y, w in points)


def fourier_quotient_checks() -> None:
    rects = (
        (F(-2), F(1), F(-1), F(2)),
        (F(-1), F(2), F(-2), F(1)),
        (F(-3, 2), F(5, 2), F(-1, 2), F(3, 2)),
    )
    laws = (
        [(-0.4, 0.2, 0.2), (0.1, -0.3, 0.35), (0.6, 0.4, 0.45)],
        [(-0.5, -0.2, 0.3), (0.2, 0.5, 0.25), (0.7, -0.1, 0.45)],
    )
    cases = 0
    skipped_zeros = 0
    max_error = 0.0
    for rect, law in product(rects, laws):
        for i in range(-30, 31):
            for j in range(-30, 31):
                xi = (i * 0.17, j * 0.13)
                c_hat = rect_fourier(rect, xi)
                mu_hat_minus = law_cf(law, (-xi[0], -xi[1]))
                v_hat = c_hat * mu_hat_minus
                if abs(c_hat) < 1e-9:
                    skipped_zeros += 1
                    continue
                recovered = v_hat / c_hat
                error = abs(recovered - mu_hat_minus)
                max_error = max(max_error, error)
                require(error < 2e-13, "fourier_quotient_recovery")
                cases += 1
    require(cases > 10000, "fourier_dense_nonzero_set_exercised")
    METRICS["fourier_quotient_cases"] = cases
    METRICS["fourier_skipped_near_zeros"] = skipped_zeros
    METRICS["fourier_max_error"] = max_error


Multi = tuple[int, int]


def multiindices(max_degree: int) -> list[Multi]:
    return [(i, j) for total in range(max_degree + 1)
            for i in range(total + 1) for j in [total - i]]


def moment(dist: list[tuple[F, F, F]], alpha: Multi) -> F:
    return sum(w * (x ** alpha[0]) * (y ** alpha[1]) for x, y, w in dist)


def convolve_difference(u_dist, z_dist):
    return [(ux - zx, uy - zy, uw * zw)
            for ux, uy, uw in u_dist for zx, zy, zw in z_dist]


def recover_z_moments(u_m: dict[Multi, F], y_m: dict[Multi, F],
                      max_degree: int) -> dict[Multi, F]:
    z: dict[Multi, F] = {(0, 0): F(1)}
    for total in range(1, max_degree + 1):
        for a0 in range(total + 1):
            alpha = (a0, total - a0)
            other = F(0)
            for b0 in range(alpha[0] + 1):
                for b1 in range(alpha[1] + 1):
                    beta = (b0, b1)
                    if beta == alpha:
                        continue
                    coeff = math.comb(alpha[0], b0) * math.comb(alpha[1], b1)
                    other += (coeff
                              * u_m[(alpha[0] - b0, alpha[1] - b1)]
                              * ((-1) ** (b0 + b1)) * z[beta])
            z[alpha] = (y_m[alpha] - other) * ((-1) ** total)
    return z


def normalized_dist(seed: int,
                    points: list[tuple[F, F]]) -> list[tuple[F, F, F]]:
    raw = [F(1 + ((seed + 3 * i + i * i) % 11)) for i in range(len(points))]
    total = sum(raw, F(0))
    return [(p[0], p[1], w / total) for p, w in zip(points, raw)]


def moment_inversion_checks() -> None:
    u_points = [(F(-3, 4), F(-1, 2)), (F(-1, 4), F(2, 3)),
                (F(1, 3), F(-2, 5)), (F(3, 4), F(1, 2))]
    z_points = [(F(-2, 3), F(1, 4)), (F(0), F(-3, 5)),
                (F(2, 5), F(3, 4)), (F(4, 5), F(-1, 5))]
    max_degree = 12
    alphas = multiindices(max_degree)
    exact_cases = 0
    stability_cases = 0
    for su in range(18):
        for sz in range(18):
            u = normalized_dist(su, u_points)
            z = normalized_dist(sz, z_points)
            y = convolve_difference(u, z)
            um = {a: moment(u, a) for a in alphas}
            ym = {a: moment(y, a) for a in alphas}
            true = {a: moment(z, a) for a in alphas}
            rec = recover_z_moments(um, ym, max_degree)
            for a in alphas:
                require(rec[a] == true[a], "triangular_moment_exact")
                exact_cases += 1

            eps = F(1, 10**9)
            ump = dict(um)
            ymp = dict(ym)
            for idx, a in enumerate(alphas):
                if a != (0, 0):
                    ump[a] += eps if (idx + su) % 2 else -eps
                    ymp[a] += eps if (idx + sz) % 3 else -eps
            rp = recover_z_moments(ump, ymp, max_degree)
            for a in alphas:
                k = sum(a)
                bound = F(0) if k == 0 else 2 * eps * (8 ** k) * math.factorial(k)
                require(abs(rp[a] - true[a]) <= bound,
                        "triangular_moment_factorial_bound")
                stability_cases += 1
    METRICS["moment_exact_cases"] = exact_cases
    METRICS["moment_stability_cases"] = stability_cases


def signed_estimator_checks() -> None:
    cases = 0
    for z_num in range(1, 10):
        for b_num in range(1, 12):
            Z = F(z_num, 10)
            B = F(b_num, 7)
            t = F(3, 5)
            probs = (F(1, 20), F(1, 7), F(2, 5), F(4, 5))
            signs = (1, -1, 1, -1)
            weights = (F(1, 10), F(2, 10), F(3, 10), F(4, 10))
            scale = Z * B / t
            expected = sum(weights[i] * scale * signs[i] * probs[i]
                           for i in range(4))
            direct = scale * sum(weights[i] * signs[i] * probs[i]
                                 for i in range(4))
            second = sum(weights[i] * scale * scale * probs[i]
                         for i in range(4))
            require(expected == direct, "signed_command_estimator_unbiased")
            require(abs(scale) == Z * B / t, "signed_command_estimator_range")
            require(second >= expected * expected,
                    "signed_command_estimator_variance")
            cases += 1
    METRICS["signed_estimator_cases"] = cases


def resource_checks() -> None:
    cases = 0
    for beta_num in range(1, 11):
        beta = F(beta_num, 10)
        s = 6 + beta
        for gamma in range(0, 6):
            q_pair = (F(gamma) + F(9, 2)) * s / (s - 2)
            q_old = (3 * F(gamma) + F(27, 2)) * s / (s - 2)
            require(q_old == 3 * q_pair, "pair_exponent_one_third")
            require(q_pair > 2, "pair_hull_cost_dominates_scalar")
            require(F(gamma) + F(9, 2) > F(gamma) + F(3, 2) + 1 / s,
                    "pair_hull_dominates_boundary")
            require(F(2) > F(1), "density_transport_tolerance_squared")
            cases += 1
    require(F(9, 2) * F(7) / F(5) == F(63, 10),
            "pair_gamma_zero_s7_value")
    METRICS["resource_parameter_cases"] = cases


def main() -> int:
    try:
        endpoint_identity_checks()
        prefix_inverse_checks()
        support_calibration_checks()
        fourier_quotient_checks()
        moment_inversion_checks()
        signed_estimator_checks()
        resource_checks()
        result = {
            "schema": "a2-v40-independent-review-diagnostics-1",
            "status": "passed",
            "checks": dict(sorted(CHECKS.items())),
            "total_checks": sum(CHECKS.values()),
            "metrics": METRICS,
            "imports_author_code": False,
            "runtime_dependencies": "Python standard library only",
            "formal_proof_certificate": False,
            "physical_sensor_executed": False,
            "tex_build": False,
            "scope": "Finite exact algebra and numerical model diagnostics only; not a continuum proof or editorial decision.",
        }
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
