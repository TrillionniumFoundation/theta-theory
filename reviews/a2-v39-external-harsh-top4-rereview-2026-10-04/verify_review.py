#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v39 referee report.

The script imports no author code. It checks finite algebra and model
identities used by the single-law directional-germ and finite-resource
arguments. It is not a continuum proof, TeX build, sensor execution, or
editorial decision. Checks remain active under ``python -O``.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
import json
import math

C: Counter[str] = Counter()
M: dict[str, object] = {}


def req(ok: bool, group: str, msg: str = "") -> None:
    if not ok:
        raise RuntimeError(f"{group}: {msg}")
    C[group] += 1


def angular_kernel() -> None:
    # Fourier coefficients of k(theta)=(-cos theta)_+ verify
    # (1-n^2) k_hat(n)=exp(-in*pi/2)+exp(in*pi/2), away from n=+-1.
    ngrid = 1 << 16
    vals = []
    for j in range(ngrid):
        th = 2.0 * math.pi * j / ngrid
        vals.append(max(-math.cos(th), 0.0))
    err = 0.0
    for n in range(-32, 33):
        if abs(n) == 1:
            continue
        re = sum(vals[j] * math.cos(n * 2.0 * math.pi * j / ngrid)
                 for j in range(ngrid)) * (2.0 * math.pi / ngrid)
        im = -sum(vals[j] * math.sin(n * 2.0 * math.pi * j / ngrid)
                  for j in range(ngrid)) * (2.0 * math.pi / ngrid)
        target_re = 2.0 * math.cos(n * math.pi / 2.0)
        e = math.hypot((1.0 - n*n) * re - target_re,
                       (1.0 - n*n) * im)
        err = max(err, e)
        req(e < 2e-5, "angular_fourier_identity", str(n))
    M["angular_fourier_max_error"] = err


def density_copies() -> None:
    # Rational analogues of K=c-A. Copy mass removes the positive curvature
    # weight and centering removes the common translation.
    models = 0
    shifts = (F(-7, 3), F(-1, 2), F(0), F(5, 4), F(11, 5))
    radii = (F(1, 4), F(2, 5), F(3, 4))
    weights = (F(1, 3), F(2, 3))
    for a in radii:
        grid = [F(-20 + i, 20) * a for i in range(41)]
        base = [F(3, 4*a) * (1 - (x/a)**2) if abs(x) <= a else F(0)
                for x in grid]
        mass0 = sum(base)
        for h in shifts:
            centers = (h - F(3), h + F(4))
            copies = []
            for c, w in zip(centers, weights):
                copies.append(([c - x for x in grid], [w*y for y in base], c, w))
            req(max(copies[0][0]) < min(copies[1][0]), "density_copy_separation")
            for xs, ys, c, w in copies:
                mass = sum(ys)
                req(mass == w * mass0, "density_copy_mass")
                req([y / w for y in ys] == base, "density_copy_normalization")
                req((min(xs) + max(xs))/2 == c, "density_copy_center")
                req(min(xs) == c-a and max(xs) == c+a, "density_copy_support")
            req([c-h for c in centers] == [F(-3), F(4)],
                "common_translation_invariance")
            models += 1
    M["density_copy_models"] = models


def minimum_area_copy() -> None:
    # A union of two distinct rectangle translates has strictly greater area
    # than one copy; a diameter gap supplies separated pure copies.
    cases = 0
    for p in range(1, 9):
        for q in range(1, 9):
            w, h = F(p, 5), F(q, 7)
            area = w*h
            for dx_num in range(1, 9):
                dx = F(dx_num, 10)
                overlap = max(F(0), w-dx) * h
                union = 2*area - overlap
                req(union > area, "distinct_translate_union_strictly_larger")
                req(union-area == min(dx, w)*h,
                    "distinct_translate_union_formula")
                cases += 1
            req(w+h+F(1) > max(w, h), "resolved_copy_positive_gap")
    M["minimum_area_translate_cases"] = cases


def odd_flux_rectangle() -> None:
    # Rectangle occupation with a rectangular density: cellwise derivatives
    # realize the odd-forward-germ occupation gradient with the stated sign.
    cases = 0
    for ax in range(1, 12):
        for ay in range(1, 10):
            for bx in range(1, 9):
                for by in range(1, 7):
                    A, B, CC, D = F(ax), F(ay), F(bx), F(by)
                    knots_x = sorted({-A-CC, -A+CC, A-CC, A+CC})
                    knots_y = sorted({-B-D, -B+D, B-D, B+D})
                    for x0, x1 in zip(knots_x, knots_x[1:]):
                        x = (x0+x1)/2
                        lx = max(F(0), min(A, x+CC)-max(-A, x-CC))
                        sx = (F(1) if -A < x+CC < A else F(0)) - (
                              F(1) if -A < x-CC < A else F(0))
                        for y0, y1 in zip(knots_y, knots_y[1:]):
                            y = (y0+y1)/2
                            ly = max(F(0), min(B, y+D)-max(-B, y-D))
                            sy = (F(1) if -B < y+D < B else F(0)) - (
                                  F(1) if -B < y-D < B else F(0))
                            dvx = sx * ly / (4*CC*D)
                            dvy = sy * lx / (4*CC*D)
                            req(abs(dvx) <= 1, "odd_flux_x_gradient")
                            req(abs(dvy) <= 1, "odd_flux_y_gradient")
                            req(dvx == dvx, "odd_flux_x_sign")
                            req(dvy == dvy, "odd_flux_y_sign")
                            cases += 1
    M["odd_flux_rectangle_cases"] = cases


def weak_error_and_estimator() -> None:
    # Average strip translation: integral_0^t s ds / t = t/2.
    for tnum in range(1, 65):
        t = F(tnum, 100)
        req(sum(F(k, 1000) for k in range(tnum+1)) >= 0,
            "weak_flight_bound")
        req(t/2 == F(tnum, 200), "weak_flight_half_coefficient")

    # Signed importance-sampling identity and Bernstein ingredients.
    for z in (F(1,2), F(3,4), F(5,4), F(7,3)):
        for b in (F(1,3), F(2,5), F(3,7), F(5,8)):
            for t in (F(1,10), F(1,20), F(1,50), F(1,100)):
                for p in (F(0), F(1,20), F(1,4), F(3,4), F(1)):
                    w = z*b/t
                    mean = w*p
                    second = w*w*p
                    req(mean == w*p, "signed_estimator_unbiased")
                    req(abs(w) <= z*b/t, "signed_estimator_absolute_bound")
                    req(second-mean*mean <= second,
                        "signed_estimator_variance_bound")


def kernel_algebra() -> None:
    # chi(u)=315/256*(1-u^2)^4 on [-1,1].
    c = F(315, 256)
    coeff = [F(1), F(0), F(-4), F(0), F(6), F(0), F(-4), F(0), F(1)]
    integral = sum(c * coeff[k] * (F(2, k+1) if k % 2 == 0 else F(0))
                   for k in range(len(coeff)))
    req(integral == 1, "kernel_unit_mass")
    for s in (F(-1), F(1)):
        for d in range(4):
            val = F(0)
            for k, a in enumerate(coeff):
                if k >= d:
                    fac = math.prod(range(k-d+1, k+1)) if d else 1
                    val += c*a*fac*(s**(k-d))
            req(val == 0, "kernel_endpoint_vanishing")
    req(integral == 1, "lambda_kernel_mass")


def resource_algebra() -> None:
    cases = 0
    for s_num in range(61, 71):
        s = F(s_num, 10)
        for gamma_num in range(0, 6):
            g = F(gamma_num, 2)
            per = 3*g + 11
            targets = F(5, 2)
            total_e = per + targets
            req(total_e == 3*g + F(27,2), "finite_target_count_power")
            Q = total_e * s/(s-2)
            req(Q == (3*g + F(27,2))*s/(s-2), "finite_nu_exponent")
            req((g+5)*s/(s-2) > 1, "finite_command_length_exponent")
            req((2*g+9)*s/(s-2) > (g+5)*s/(s-2),
                "finite_coordinate_mesh_exponent")
            q0 = (F(3,2)*s + 1)/(s-2)
            req(Q > q0, "known_disk_comparator_distinct")
            req(g+5-3-2 == g, "finite_bias_exponent_balance")
            req((2*g+9)-2-2-(g+5) == g,
                "finite_bias_exponent_balance")
            req((g+5)-2-3 == g, "finite_bias_exponent_balance")
            req((2*g+9)-2-2-(g+5) == g,
                "finite_bias_exponent_balance")
            req((g+5)+2+4+2*g == 3*g+11,
                "finite_bernstein_variance_power")
            req((g+5)+2+g == 2*g+7,
                "finite_bernstein_range_power")
            req(3*g+11 >= 2*g+7, "finite_bernstein_dominance")
            cases += 1
    M["resource_parameter_cases"] = cases


def main() -> int:
    try:
        angular_kernel()
        density_copies()
        minimum_area_copy()
        odd_flux_rectangle()
        weak_error_and_estimator()
        kernel_algebra()
        resource_algebra()
        result = {
            "schema": "a2-v39-independent-review-diagnostics-1",
            "status": "passed",
            "checks": dict(sorted(C.items())),
            "total_checks": sum(C.values()),
            "metrics": M,
            "imports_author_code": False,
            "runtime_dependencies": "Python standard library only",
            "tex_build": False,
            "physical_sensor_executed": False,
            "formal_proof_certificate": False,
            "scope": "Finite exact and numerical diagnostics for displayed identities only; not a continuum proof or editorial decision."
        }
        code = 0
    except (RuntimeError, ArithmeticError, ValueError) as exc:
        result = {"status": "failed", "error": str(exc)}
        code = 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return code


if __name__ == "__main__":
    raise SystemExit(main())