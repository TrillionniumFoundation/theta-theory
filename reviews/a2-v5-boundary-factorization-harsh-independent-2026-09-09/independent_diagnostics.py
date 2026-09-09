#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v5 referee report.

No repository modules, network calls, removable asserts, interval claims,
or claims to certify a continuum theorem. Run: python independent_diagnostics.py
"""
from __future__ import annotations

import hashlib
import itertools
import json
import platform
from collections import Counter
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import solve_banded
import sympy as sp

CHECKS: list[dict[str, Any]] = []
DETAILS: dict[str, Any] = {}


def check(name: str, condition: bool, kind: str, detail: Any = None) -> None:
    if not bool(condition):
        raise RuntimeError(f"FAILED: {name}; detail={detail!r}")
    item: dict[str, Any] = {"name": name, "kind": kind, "passed": True}
    if detail is not None:
        item["detail"] = detail
    CHECKS.append(item)


def exact(name: str, expression: sp.Expr) -> None:
    residual = sp.factor(sp.together(expression))
    check(name, residual == 0, "exact_symbolic", str(residual))


def det3(matrix: list[list[sp.Expr]]) -> sp.Expr:
    answer = sp.S.Zero
    for p in itertools.permutations(range(3)):
        inversions = sum(p[i] > p[j] for i in range(3) for j in range(i + 1, 3))
        answer += (-1) ** inversions * sp.prod(matrix[i][p[i]] for i in range(3))
    return sp.factor(sp.together(answer))


def symbolic_checks() -> None:
    c, q = sp.symbols("c q", positive=True)
    gs = [sp.S.One, 1 / (2 * c), 1 / (4 * c**2 - 1), 1 / (4 * c * (2 * c**2 - 1))]
    wronskian = det3([[sp.diff(f, c, k) for k in (1, 2, 3)] for f in gs[1:]])
    poly = 64 * c**8 + 32 * c**6 + 116 * c**4 + 4 * c**2 + 1
    den = c**4 * (4 * c**2 - 1)**4 * (2 * c**2 - 1)**4
    exact("four_amplitude_rational_wronskian", wronskian - 12 * poly / den)
    exact("four_amplitude_collision_determinant", (-3 * q**3 / 2) * wronskian / (c**2 - 1)**2 + 18 * q**3 * poly / ((c**2 - 1)**2 * den))

    r, g, R, A = sp.symbols("r g R A", positive=True)
    phi1 = r / sp.sqrt(g * (g + 2 * r))
    target_third = 3 * (3 * g + r) / (sp.sqrt(g) * (g + 2 * r)**sp.Rational(7, 2))
    exact("third_radius_derivative", sp.diff(phi1, r, 3) - target_third)
    exact("two_sided_cubic_coefficient", sp.Rational(36**3 + 2 * (-18)**3, 3) - 11664)
    s = sp.symbols("s", positive=True)
    exact("middle_sorted_matching_distance", 1 / (R - 18 * s) - 1 / (R + 18 * s) - 36 * s / (R**2 - 324 * s**2))
    exact("one_flight_jet_derivative", -sp.Rational(1, 27) * (-24) - sp.Rational(8, 9))
    exact("half_line_jet_derivative", -sp.Rational(9, 1) / (12 * 3 * 4 * sp.sqrt(3)) * (-24) - sp.sqrt(3) / 2)

    x = sp.symbols("x", real=True)
    mass = sp.integrate((1 - x) / 2, (x, 0, 1))
    residual_numerator = sp.integrate((1 - x)**2 / 4, (x, 0, 1))
    exact("latent_mean_residual_fraction", residual_numerator / mass - sp.Rational(1, 3))
    exact("latent_coordinate_second_moment", sp.integrate(x * (1 - x) / 4, (x, 0, 1)) / mass - sp.Rational(1, 6))
    for m in range(1, 9):
        ws = [(-1)**(l - 1) * sp.binomial(m, l) for l in range(1, m + 1)]
        identities = [sum(ws) - 1] + [sum(ws[l - 1] * l**k for l in range(1, m + 1)) for k in range(1, m)]
        check(f"richardson_m_{m}", all(v == 0 for v in identities), "exact_symbolic")
        exact(f"harmonic_m_{m}", sum(ws[l - 1] / sp.Integer(l) for l in range(1, m + 1)) - sp.harmonic(m))

    E1, E2 = sp.symbols("E1 E2")
    alpha = E1 / 108
    beta_zeta_squared = E1**2 / 2916 - E2 / 972
    area_from_shape = A - sp.pi * (2 * R * alpha - sp.Rational(33, 2) * alpha**2 - sp.Rational(45, 4) * beta_zeta_squared)
    area_coefficients = A - sp.pi * R * E1 / 54 + 41 * sp.pi * E1**2 / 7776 - 5 * sp.pi * E2 / 432
    exact("physical_area_in_radius_symmetric_coordinates", area_from_shape - area_coefficients)

    # Factor phi_j(r)=h(r) p_j(r). These recurrences differentiate in r
    # with g held fixed, before specializing R=1/4, g=1/2.
    cr = 1 + g / r
    ps = [sp.S.One, 1 / (2 * cr), 1 / (4 * cr**2 - 1)]
    hlog = 1 / r - 1 / (g + 2 * r)
    values: list[list[sp.Expr]] = []
    for p in ps:
        ds = [p]
        for _ in range(3):
            ds.append(sp.cancel(sp.diff(ds[-1], r) + hlog * ds[-1]))
        values.append([sp.factor(d.subs({r: sp.Rational(1, 4), g: sp.Rational(1, 2)})) for d in ds])
    physical = [[v[1] + sp.pi * v[0] / (72 * A), -v[2] + 5 * sp.pi * v[0] / (144 * A), v[3] / 2] for v in values]
    actual = det3(physical) / (2 * sp.sqrt(2) * A)**3
    certificate = -4 * (15804720 * A + 64253 * sp.pi) / (72930375 * sp.sqrt(2) * A**4)
    exact("three_physical_amplitudes_R_quarter_determinant", actual - certificate)
    DETAILS["three_amplitude_certificate"] = str(certificate)
    DETAILS["three_amplitude_scope"] = "Local physical family at R=1/4, g=1/2; no all-R claim, no claim that four-amplitude sufficiency is false."

    # Endpoint coboundaries telescope and preserve every interior Hessian.
    u, v, y, a0, a1, a2 = sp.symbols("u v y a0 a1 a2")
    gauge = (a0 * u**2 - a1 * y**2 + a1 * y**2 - a2 * v**2) / 2
    exact("endpoint_coboundary_telescoping", gauge - (a0 * u**2 - a2 * v**2) / 2)
    exact("endpoint_coboundary_mixed_twist_invariance", sp.diff(gauge, u, v))


def coefficients(indices: np.ndarray) -> tuple[np.ndarray, ...]:
    i = np.asarray(indices, dtype=float)
    return (1 + .15 * np.cos(np.sqrt(2) * i),
            .8 + .1 * np.sin(np.sqrt(3) * i),
            .9 + .1 * np.cos(np.sqrt(5) * i),
            .1 * np.sin(np.sqrt(7) * i),
            .3 + .05 * np.cos(np.sqrt(11) * i),
            .03 * np.sin(np.sqrt(13) * i))


def chain_terms(x: np.ndarray, m: int) -> tuple[np.ndarray, ...]:
    u, v = x[:-1], x[1:]
    b, a, at, k, t, chi = coefficients(np.arange(m, m + len(x) - 1))
    action = b * (v - u)**2 / 2 + a * u**2 / 2 + at * v**2 / 2 + k * (u**3 + .7 * v**3) / 6 + t * (u**4 + v**4) / 24 + chi * u**2 * v**2
    lu = b * (u - v) + a * u + k * u**2 / 2 + t * u**3 / 6 + 2 * chi * u * v**2
    lv = b * (v - u) + at * v + .35 * k * v**2 + t * v**3 / 6 + 2 * chi * u**2 * v
    luu = b + a + k * u + t * u**2 / 2 + 2 * chi * v**2
    lvv = b + at + .7 * k * v + t * v**2 / 2 + 2 * chi * u**2
    luv = -b + 4 * chi * u * v
    return action, lu, lv, luu, lvv, luv, b


def tridiagonal(diagonal: np.ndarray, off: np.ndarray) -> np.ndarray:
    return np.diag(diagonal) + np.diag(off, 1) + np.diag(off, -1)


def solve_segment(m: int, n: int, u: float, v: float) -> tuple[float, float, float]:
    if n <= m:
        raise ValueError("A chain must have positive length")
    x = np.zeros(n - m + 1)
    x[0], x[-1] = u, v
    residual = 0.0
    for _ in range(15):
        terms = chain_terms(x, m)
        grad = terms[2][:-1] + terms[1][1:]
        residual = float(np.max(np.abs(grad))) if len(grad) else 0.0
        if residual < 1e-14:
            break
        diag = terms[4][:-1] + terms[3][1:]
        off = terms[5][1:-1]
        band = np.zeros((3, len(diag)))
        band[1] = diag
        band[0, 1:] = off
        band[2, :-1] = off
        x[1:-1] -= solve_banded((1, 1), band, grad)
    else:
        raise RuntimeError("Newton iteration failed")
    terms = chain_terms(x, m)
    zero_terms = chain_terms(np.zeros_like(x), m)
    H = tridiagonal(terms[4][:-1] + terms[3][1:], terms[5][1:-1])
    H0 = tridiagonal(zero_terms[4][:-1] + zero_terms[3][1:], zero_terms[5][1:-1])
    sign, logdet = np.linalg.slogdet(np.eye(len(H)) + np.linalg.solve(H0, H - H0))
    if sign != 1 or np.any(terms[5] >= 0):
        raise RuntimeError("Lost positive Hessian / negative twist")
    logb = float(np.sum(np.log((-terms[5]) / terms[6])) - logdet)
    return float(np.sum(terms[0])), logb, residual


def chain_checks() -> None:
    # Uniform bounds on |u|,|v|<=.1 give positive margins analytically:
    # Luu-|Luv| >= .7-.01-.0006-.0012; similarly Lvv.
    # The numerical experiment below samples, and does not prove, the theorem.
    records = []
    for m in (3, 17):
        for length in (4, 8, 12, 16, 24):
            n = m + length
            finite = solve_segment(m, n, .05, -.04)
            left = solve_segment(m, m + 96, .05, 0.)
            right = solve_segment(n - 96, n, 0., -.04)
            action_error = abs(finite[0] - left[0] - right[0])
            logb_error = abs(finite[1] - left[1] - right[1])
            residual = max(finite[2], left[2], right[2])
            check(f"nonperiodic_stationarity_m{m}_N{length}", residual < 1e-13, "floating_noninterval", residual)
            records.append({"m": m, "length": length, "action_error": action_error, "log_relative_twist_error": logb_error})
        subset = records[-5:]
        check(f"nonperiodic_boundary_agreement_m{m}", subset[-1]["action_error"] < 1e-11 and subset[-1]["log_relative_twist_error"] < 1e-10, "floating_noninterval")
        # No monotonicity test: an early-length cancellation can make an
        # individual discrepancy much smaller than its exponential envelope.
        L64 = solve_segment(m, m + 64, .05, 0.)
        L96 = solve_segment(m, m + 96, .05, 0.)
        R64 = solve_segment(m + 24 - 64, m + 24, 0., -.04)
        R96 = solve_segment(m + 24 - 96, m + 24, 0., -.04)
        cutoff_error = max(abs(L64[i] - L96[i]) for i in (0, 1))
        cutoff_error = max(cutoff_error, *(abs(R64[i] - R96[i]) for i in (0, 1)))
        check(f"finite_halfline_cutoff_comparison_m{m}", cutoff_error < 1e-11, "floating_noninterval", cutoff_error)
    DETAILS["nonperiodic_chain"] = {"endpoints": [.05, -.04], "halfline_cutoff": 96, "comparison_cutoff": 64, "records": records, "warning": "Finite truncations and ordinary floating point; not an infinite-operator or derivative certificate."}


def high_precision_checks() -> None:
    mp.mp.dps = 70
    R, g = mp.mpf(1) / 4, mp.mpf(1) / 2
    A = mp.sqrt(3) / 2 - mp.pi * R**2
    gamma_weight = mp.mpf(".4")

    def amplitude(j: int, s: mp.mpf) -> mp.mpf:
        radii = (R + 36 * s, R - 18 * s, R - 18 * s)
        return sum(1 / mp.sinh(j * mp.acosh(1 + g / r)) for r in radii) / (A + 45 * mp.pi * s**2 / 4)

    samples = []
    for text in ("0.0001", "0.00005", "0.00001"):
        s = mp.mpf(text)
        prefix = max(mp.exp(gamma_weight * j) * abs(amplitude(j, s) - amplitude(j, -s)) for j in range(1, 129))
        match = max(abs(x - y) for x, y in zip(sorted(1 / r for r in (R + 36 * s, R - 18 * s, R - 18 * s)), sorted(1 / r for r in (R - 36 * s, R + 18 * s, R + 18 * s))))
        exact_match = 36 * s / (R**2 - 324 * s**2)
        check(f"high_precision_sorted_matching_s{text}", abs(match - exact_match) < mp.mpf("1e-60"), "high_precision_noninterval")
        samples.append({"s": text, "weighted_prefix_discrepancy_over_s_cubed": mp.nstr(prefix / s**3, 20), "curvature_matching_over_s": mp.nstr(match / s, 20)})
    ratios = [mp.mpf(t["weighted_prefix_discrepancy_over_s_cubed"]) for t in samples]
    check("high_precision_cubic_prefix_consistency", max(ratios) / min(ratios) < mp.mpf("1.001"), "high_precision_noninterval")

    def phi(j: int, r: mp.mpf) -> mp.mpf:
        return 1 / mp.sinh(j * mp.acosh(1 + g / r))
    J = mp.matrix([[mp.diff(lambda r: phi(j, r), R) / A + mp.pi * R * phi(j, R) / (18 * A**2), -mp.diff(lambda r: phi(j, r), R, 2) / A + 5 * mp.pi * phi(j, R) / (144 * A**2), mp.diff(lambda r: phi(j, r), R, 3) / (2 * A)] for j in (1, 2, 3)])
    formula = -4 * (15804720 * A + 64253 * mp.pi) / (72930375 * mp.sqrt(2) * A**4)
    determinant = mp.det(J)
    check("high_precision_three_amplitude_determinant", abs(determinant - formula) < mp.mpf("1e-60"), "high_precision_noninterval")
    DETAILS["high_precision"] = {"decimal_digits": 70, "weighted_prefix_length": 128, "weight_a": ".4", "two_sided_path": samples, "three_amplitude_determinant_R_quarter": mp.nstr(determinant, 30), "warning": "High precision is not interval certification. A prefix check is not a whole-sequence proof."}


def main() -> None:
    symbolic_checks()
    chain_checks()
    high_precision_checks()
    output = {"schema": "a2-v5-independent-diagnostics/1", "manuscript_commit": "ee879236d0fae1f84c685bef4ff27326403d4b2d", "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "sympy": sp.__version__, "mpmath": mp.__version__}, "passed": len(CHECKS), "by_kind": dict(Counter(c["kind"] for c in CHECKS)), "checks": CHECKS, "details": DETAILS, "limitations": ["No continuum theorem or editorial conclusion follows from this finite test count.", "No manuscript build, full equilibrium simulation, remote CI, interval arithmetic, proof assistant, or replay of author or older referee suites.", "No sensor-noise or unknown-gap learning experiment is simulated."]}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
