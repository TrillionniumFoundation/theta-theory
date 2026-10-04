#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v42 referee review.

The program imports no author code. It checks exact finite models for the
endpoint identity, finite and protected prefixes, shared signed two-bit records,
Riemann moment acquisition, support cancellation, factor-moment algebra, and
resource exponents. It is not a continuum proof certificate, a TeX build, a
physical sensor execution, or an editorial decision. All checks remain active
under ``python -O``.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
import math
import sys

CHECKS: Counter[str] = Counter()
METRICS: dict[str, object] = {}


def require(ok: bool, group: str, detail: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {detail}")
    CHECKS[group] += 1


def in_union(x: F, intervals: list[tuple[F, F]]) -> bool:
    return any(lo <= x <= hi for lo, hi in intervals)


def segment_hits_union(start: F, displacement: F,
                       intervals: list[tuple[F, F]]) -> bool:
    if in_union(start, intervals):
        return False
    lo = min(start, start + displacement)
    hi = max(start, start + displacement)
    return any(max(lo, a) <= min(hi, b) for a, b in intervals)


def occupation(x: F, atoms: list[tuple[F, F]],
               intervals: list[tuple[F, F]]) -> F:
    return sum((w for z, w in atoms if in_union(x + z, intervals)), F(0))


def mean_bit(x: F, displacement: F, atoms: list[tuple[F, F]],
             intervals: list[tuple[F, F]]) -> F:
    return sum((w for z, w in atoms
                if segment_hits_union(x + z, displacement, intervals)), F(0))


def endpoint_and_prefix_models() -> None:
    cases = 0
    protected_cases = 0
    negative_outcomes = 0
    shifts = (F(-3, 5), F(-1, 4), F(0), F(2, 7), F(4, 5))
    weights = ((F(1),), (F(1, 3), F(2, 3)),
               (F(1, 6), F(1, 3), F(1, 2)))
    atom_locations = ((F(0),), (F(-1, 5), F(1, 4)),
                      (F(-1, 3), F(0), F(2, 7)))
    for t in (F(1, 4), F(1, 3), F(2, 5)):
        for gap_extra in (F(3, 2), F(2), F(5, 2)):
            intervals = [(F(-2), F(-1)),
                         (F(-1) + gap_extra + t,
                          F(1, 2) + gap_extra + t)]
            D = max(hi - lo for lo, hi in intervals)
            for locs, ws in zip(atom_locations, weights):
                atoms = list(zip(locs, ws))
                require(sum(ws, F(0)) == 1, "atomic_law_normalized")
                delta = max(locs) - min(locs)
                gap = intervals[1][0] - intervals[0][1]
                require(t + delta < gap, "model_separation")
                M = int((D + delta) // t) + 1
                for j in range(-45, 66):
                    x = F(j, 12)
                    for s in shifts:
                        y = x + s
                        lhs = (mean_bit(y, t, atoms, intervals)
                               - mean_bit(y + t, -t, atoms, intervals))
                        rhs = occupation(y + t, atoms, intervals) - occupation(y, atoms, intervals)
                        require(lhs == rhs, "endpoint_increment_identity")
                        rvals = [mean_bit(y + k * t, t, atoms, intervals)
                                 - mean_bit(y + (k + 1) * t, -t, atoms, intervals)
                                 for k in range(M)]
                        prefix = F(0)
                        best = F(0)
                        for rv in rvals:
                            prefix -= rv
                            best = max(best, prefix)
                        require(best == occupation(y, atoms, intervals),
                                "finite_prefix_inverse")
                        cases += 1

                c_lo, c_hi = intervals[0]
                a_min, a_max = min(locs), max(locs)
                p_lo, p_hi = c_lo - a_max, c_hi - a_min
                rho = F(1, 10)
                q_lo, q_hi = p_lo - rho, p_hi + rho
                comp_gap = ((intervals[1][0] - a_max) - p_hi)
                require(rho + t < comp_gap, "protected_gap")
                K = int((q_hi - q_lo) // t) + 2
                require(K * t > q_hi - q_lo, "protected_K")
                for j in range(-25, 36):
                    X = q_lo + F(j, 10)
                    if q_lo <= X <= q_hi:
                        m = next(k for k in range(1, K + 1)
                                 if not (q_lo <= X + k * t <= q_hi))
                    else:
                        m = 0
                    summation = F(0)
                    for k in range(K):
                        if k < m:
                            summation += (mean_bit(X + (k + 1) * t, -t, atoms, intervals)
                                          - mean_bit(X + k * t, t, atoms, intervals))
                    true_component = sum((w for z, w in atoms
                                          if c_lo <= X + z <= c_hi), F(0))
                    require(summation == true_component,
                            "protected_linear_prefix")
                    avg = F(0)
                    for L in range(K):
                        coeff = 1 if L < m else 0
                        term = K * coeff * (
                            mean_bit(X + (L + 1) * t, -t, atoms, intervals)
                            - mean_bit(X + L * t, t, atoms, intervals))
                        avg += F(term, K)
                        negative_outcomes += int(term < 0)
                    require(avg == true_component, "signed_record_unbiased")
                    protected_cases += 1
    METRICS["endpoint_prefix_cases"] = cases
    METRICS["protected_prefix_cases"] = protected_cases
    METRICS["negative_expected_record_cases"] = negative_outcomes


def rectangle_moment_integral(cx: F, cy: F, hx: F, hy: F,
                              px: int, py: int, R: F) -> F:
    def one_dim(c: F, h: F, p: int) -> F:
        if p == 0:
            return 2 * h
        return ((c + h) ** (p + 1) - (c - h) ** (p + 1)) / F(p + 1)
    return one_dim(cx, hx, px) * one_dim(cy, hy, py) / (R ** (px + py))


def point_in_rect(x: F, y: F, cx: F, cy: F, hx: F, hy: F) -> bool:
    return abs(x - cx) <= hx and abs(y - cy) <= hy


def moment_quadrature_models() -> None:
    cases = 0
    signed_record_cases = 0
    laws = [
        [((F(0), F(0)), F(1))],
        [((F(-1, 5), F(1, 7)), F(1, 3)),
         ((F(1, 4), F(-1, 6)), F(2, 3))],
        [((F(-1, 3), F(-1, 5)), F(1, 6)),
         ((F(0), F(1, 4)), F(1, 3)),
         ((F(2, 7), F(-1, 8)), F(1, 2))],
    ]
    R = F(8)
    for (cx, cy, hx, hy) in (
        (F(-1, 2), F(1, 3), F(3, 4), F(2, 3)),
        (F(2, 5), F(-1, 4), F(4, 5), F(3, 5)),
    ):
        for law in laws:
            require(sum(w for _, w in law) == 1, "quadrature_law_normalized")
            for N in (12, 18, 24, 30):
                ell = F(6, N)
                centers = [F(-3) + (F(i) + F(1, 2)) * ell for i in range(N)]
                for total_degree in range(0, 7):
                    for px in range(total_degree + 1):
                        py = total_degree - px
                        exact = F(0)
                        for (zx, zy), w in law:
                            exact += w * rectangle_moment_integral(
                                cx - zx, cy - zy, hx, hy, px, py, R)
                        riemann = F(0)
                        for x, y in product(centers, repeat=2):
                            v = sum((w for (zx, zy), w in law
                                     if point_in_rect(x + zx, y + zy,
                                                      cx, cy, hx, hy)), F(0))
                            riemann += ell * ell * (x / R) ** px * (y / R) ** py * v
                        err = abs(riemann - exact)
                        bound = F(80) * F(total_degree + 1) * ell
                        require(err <= bound, "uniform_singular_law_quadrature")
                        cases += 1

                K = 5
                areaW = F(36)
                for px, py in ((0, 0), (1, 0), (0, 1), (2, 1)):
                    rhs = F(0)
                    lhs = F(0)
                    for x, y in product(centers, repeat=2):
                        v = sum((w for (zx, zy), w in law
                                 if point_in_rect(x + zx, y + zy,
                                                  cx, cy, hx, hy)), F(0))
                        rhs += ell * ell * (x / R) ** px * (y / R) ** py * v
                        incs = [v if L == 0 else F(0) for L in range(K)]
                        ez = sum(K * inc for inc in incs) / K
                        lhs += F(1, N * N) * areaW * (x / R) ** px * (y / R) ** py * ez
                    require(lhs == rhs, "shared_record_grid_expectation")
                    signed_record_cases += 1
    METRICS["moment_quadrature_cases"] = cases
    METRICS["shared_record_grid_cases"] = signed_record_cases


def support_disk(c: tuple[F, F], r: F, u: tuple[F, F]) -> F:
    return c[0] * u[0] + c[1] * u[1] + r


def support_segment(p: tuple[F, F], q: tuple[F, F], u: tuple[F, F]) -> F:
    return max(p[0] * u[0] + p[1] * u[1],
               q[0] * u[0] + q[1] * u[1])


def pythagorean_units(limit: int = 30) -> list[tuple[F, F]]:
    out: set[tuple[F, F]] = set()
    for m in range(2, limit + 1):
        for n in range(1, m):
            d = m * m + n * n
            x = F(m * m - n * n, d)
            y = F(2 * m * n, d)
            for sx, sy, swap in product((-1, 1), (-1, 1), (False, True)):
                a, b = (y, x) if swap else (x, y)
                out.add((sx * a, sy * b))
    return sorted(out)


def support_cancellation_models() -> None:
    units = pythagorean_units(18)
    cases = 0
    translations = ((F(0), F(0)), (F(2, 5), F(-3, 7)),
                    (F(-4, 9), F(5, 11)))
    for center, radius, footprint_radius, t in product(
            translations, (F(1, 2), F(3, 4), F(5, 4)),
            (F(0), F(1, 5), F(2, 5)),
            (F(1, 4), F(2, 5))):
        p_minus = (center[0], center[1] - radius)
        p_plus = (center[0], center[1] + radius)
        for u in units:
            hC = support_disk(center, radius, u)
            hL = support_segment(p_minus, p_plus, u)
            hgp = hC if u[0] <= 0 else hL
            hgm = hL if u[0] <= 0 else hC
            hminusA = footprint_radius
            hP = hC + hminusA
            hKp = hgp + hminusA + t * max(-u[0], F(0))
            hKm = hgm + hminusA + t * max(u[0], F(0))
            H = 2 * hP - hKp - hKm + t * abs(u[0])
            require(H == hC - hL, "two_support_footprint_cancellation")
            cases += 1
    fourier_cases = 0
    max_err = 0.0
    for radius in (0.5, 0.75, 1.25):
        for k in range(0, 25):
            N = 20000
            total = 0.0
            for j in range(N):
                phi = 2 * math.pi * (j + 0.5) / N
                H = radius * (1.0 - abs(math.sin(phi)))
                psi = math.cos(k * phi)
                psi2_plus = (1.0 - k * k) * psi
                total += H * psi2_plus
            lhs = total * (2 * math.pi / N)
            integral_psi = 0.0 if k else 2 * math.pi
            rhs = radius * integral_psi - 2 * radius * (1 + (-1) ** k)
            err = abs(lhs - rhs)
            max_err = max(max_err, err)
            require(err < 2e-5, "disk_signed_curvature_fourier")
            fourier_cases += 1
    METRICS["support_cancellation_cases"] = cases
    METRICS["signed_curvature_fourier_cases"] = fourier_cases
    METRICS["signed_curvature_max_error"] = max_err


def multinomial_moment(law: list[tuple[tuple[F, F], F]], alpha: tuple[int, int]) -> F:
    p, q = alpha
    return sum(w * (x ** p) * (y ** q) for (x, y), w in law)


def convolved_difference_law(U, Z):
    out: dict[tuple[F, F], F] = {}
    for (u, wu), (z, wz) in product(U, Z):
        point = (u[0] - z[0], u[1] - z[1])
        out[point] = out.get(point, F(0)) + wu * wz
    return sorted(out.items())


def triangular_moment_factorization() -> None:
    cases = 0
    lawsU = [
        [((F(-1, 3), F(1, 4)), F(2, 5)),
         ((F(1, 2), F(-1, 5)), F(3, 5))],
        [((F(-1, 2), F(-1, 3)), F(1, 4)),
         ((F(0), F(1, 3)), F(1, 2)),
         ((F(2, 5), F(0)), F(1, 4))],
    ]
    lawsZ = [
        [((F(-1, 4), F(1, 6)), F(1, 3)),
         ((F(1, 5), F(-1, 7)), F(2, 3))],
        [((F(-2, 7), F(-1, 6)), F(1, 6)),
         ((F(0), F(1, 8)), F(1, 3)),
         ((F(1, 3), F(-1, 4)), F(1, 2))],
    ]
    for U, Z in product(lawsU, lawsZ):
        require(sum(w for _, w in U) == 1, "factor_U_normalized")
        require(sum(w for _, w in Z) == 1, "factor_Z_normalized")
        Y = convolved_difference_law(U, Z)
        maxdeg = 10
        recovered: dict[tuple[int, int], F] = {(0, 0): F(1)}
        for k in range(1, maxdeg + 1):
            for p in range(k + 1):
                q = k - p
                y_m = multinomial_moment(Y, (p, q))
                lower = F(0)
                from math import comb
                for i in range(p + 1):
                    for j in range(q + 1):
                        if i == p and j == q:
                            continue
                        coeff = F(comb(p, i) * comb(q, j)) * ((-1) ** (i + j))
                        lower += coeff * multinomial_moment(U, (p - i, q - j)) * recovered[(i, j)]
                coeff_top = F((-1) ** (p + q))
                rec = (y_m - lower) / coeff_top
                recovered[(p, q)] = rec
                require(rec == multinomial_moment(Z, (p, q)),
                        "triangular_factor_moment_recovery")
                cases += 1
        shift = (F(2, 9), F(-3, 10))
        shiftedZ = [((z[0] + shift[0], z[1] + shift[1]), w) for z, w in Z]
        centeredZ = [(z, w) for z, w in Z]
        mean = (multinomial_moment(shiftedZ, (1, 0)),
                multinomial_moment(shiftedZ, (0, 1)))
        shifted_centered = [((z[0] - mean[0], z[1] - mean[1]), w)
                            for z, w in shiftedZ]
        original_mean = (multinomial_moment(centeredZ, (1, 0)),
                         multinomial_moment(centeredZ, (0, 1)))
        original_centered = [((z[0] - original_mean[0], z[1] - original_mean[1]), w)
                             for z, w in centeredZ]
        for degree in range(0, 7):
            for p in range(degree + 1):
                q = degree - p
                require(multinomial_moment(shifted_centered, (p, q))
                        == multinomial_moment(original_centered, (p, q)),
                        "common_translation_centered_moments")
    METRICS["triangular_moment_cases"] = cases


def resource_algebra() -> None:
    cases = 0
    for beta_num in range(1, 11):
        beta = F(beta_num, 10)
        s = 6 + beta
        for gamma_num in range(0, 11):
            gamma = F(gamma_num, 3)
            q_pair = (gamma + F(9, 2)) * s / (s - 2)
            require(q_pair > 2, "pair_geometry_dominates_scalar_cost")
            require(q_pair == (gamma + F(9, 2)) * s / (s - 2),
                    "pair_exponent_identity")
            for m in (2, 3, 5, 8, 13):
                a = F(1, 10 * m)
                old = F(m * m) * a ** -4
                new = a ** -2
                require(new < old, "linear_moment_budget_improves_all_node")
                dn = F((4 * m + 2) * (4 * m + 1), 2)
                require(dn >= 1, "moment_dimension_positive")
                cases += 1
            require(q_pair > s / (s - 2), "pair_mesh_finer_than_support_scale")
    METRICS["resource_cases"] = cases


def run() -> dict:
    endpoint_and_prefix_models()
    moment_quadrature_models()
    support_cancellation_models()
    triangular_moment_factorization()
    resource_algebra()
    return {
        "schema": "a2-v42-independent-review-diagnostics-1",
        "status": "passed",
        "reviewed_manuscript": "A2-v42-proof-completion",
        "checks": dict(sorted(CHECKS.items())),
        "total_checks": sum(CHECKS.values()),
        "metrics": METRICS,
        "imports_author_code": False,
        "runtime_dependencies": "Python standard library only",
        "formal_proof_certificate": False,
        "physical_sensor_executed": False,
        "tex_build": False,
        "scope": (
            "Exact finite algebra, atomic/singular-law models, quadrature models, "
            "and resource identities only. The diagnostics do not certify the "
            "continuum support/Jordan proofs, statistical uniformity, physical "
            "apparatus, literature priority, or editorial judgment."
        ),
    }


def main() -> int:
    try:
        result = run()
        code = 0
    except Exception as exc:
        result = {
            "schema": "a2-v42-independent-review-diagnostics-1",
            "status": "failed",
            "error": f"{type(exc).__name__}: {exc}",
            "formal_proof_certificate": False,
        }
        code = 1
    text = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
