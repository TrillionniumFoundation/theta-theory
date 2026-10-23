#!/usr/bin/env python3
"""Auxiliary exact/algebraic checks for the unsmoothed interval theorem.

These checks do not prove any billiard-geometric or spectral input.
The theorem proof is in 334_exact_unsmoothed_interval_inversion.tex.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys

import mpmath as mp
import sympy as sp


def run():
    mp.mp.dps = 90
    checks = []

    d, s, j = sp.symbols("d s j", positive=True)
    first = d * (1 + sp.log(2 * j / (d * s)))
    second = 2 * j / s
    assert sp.simplify(first.subs(s, 2 * j / d) - second.subs(s, 2 * j / d)) == 0
    assert sp.simplify(sp.diff(first, s) + d / s) == 0
    assert sp.simplify(sp.diff(second, s) + 2 * j / s**2) == 0
    checks.append({"name": "piecewise positive tail antiderivative and matching", "status": "PASS"})

    # Original scaling: interval length d, Fourier cutoff m^(P+2)/d.
    # Rational choices make this a direct arithmetic identity, not sampling.
    for count in (1, 2, 17, 100):
        for degree in (1, 3, 8):
            for width in (Fraction(1), Fraction(1, 10**8), Fraction(1, 10**40)):
                cutoff = Fraction(count ** (degree + 2), 1) / width
                assert Fraction(count**2, 1) / (width * cutoff) == Fraction(1, count**degree)
    checks.append({"name": "m^2 divided by true window length normalization", "status": "PASS"})

    # Torus orthogonality normalization, no missing collision/occupation mark.
    pi = sp.pi
    assert sp.simplify((2 * pi) ** -4 * (2 * pi) ** 3 - 1 / (2 * pi)) == 0
    checks.append({"name": "four-coordinate Fourier factor after three torus integrals", "status": "PASS"})

    def primitive(x, cutoff):
        # Integral_0^cutoff (1-cos(x*s))/s^2 ds, with its exact continuous value.
        return x * mp.si(x * cutoff) - (1 - mp.cos(x * cutoff)) / cutoff

    def box_cutoff(a, b, c, e, cutoff):
        return (primitive(b - c, cutoff) - primitive(b - e, cutoff)
                - primitive(a - c, cutoff) + primitive(a - e, cutoff)) / mp.pi

    def tail_function(width, cutoff, components):
        if width * cutoff <= 2 * components:
            return width * (1 + mp.log(2 * components / (width * cutoff)))
        return 2 * components / cutoff

    # Positive and signed/complex endpoint-test densities on finite interval unions.
    # Each component is a linear combination of exact boxes. The Fourier integral
    # is evaluated by a closed formula using Si, independently of the tail formula.
    examples = [
        [(mp.mpf(0), mp.mpf(1), mp.mpf(1))],
        [(mp.mpf(-2), mp.mpf(-1), mp.mpf("0.3")),
         (mp.mpf("0.1"), mp.mpf("0.8"), mp.mpf("0.7"))],
        [(mp.mpf(-1), mp.mpf(0), mp.mpc("0.2", "0.4")),
         (mp.mpf("0.5"), mp.mpf("0.50000000000000000001"), mp.mpc("-0.3", "0.1"))],
    ]
    windows = [
        [(mp.mpf(0), mp.mpf(1))],
        [(mp.mpf("-0.3"), mp.mpf("0.02"))],
        [(mp.mpf("-1.5"), mp.mpf("-0.8")), (mp.mpf("0.4"), mp.mpf("0.6"))],
        [(mp.mpf("0.5"), mp.mpf("0.500000000000000000001"))],
    ]
    cutoffs = [mp.mpf("0.01"), mp.mpf(1), mp.mpf(17), mp.mpf("1e8"), mp.mpf("1e24")]
    worst_ratio = mp.mpf(0)
    evaluated = 0
    for density in examples:
        variation_budget = 2 * sum(abs(weight) for a, b, weight in density)
        for window in windows:
            width = sum(e - c for c, e in window)
            exact = sum(weight * max(mp.mpf(0), min(b, e) - max(a, c))
                        for a, b, weight in density for c, e in window)
            for cutoff in cutoffs:
                truncated = sum(weight * box_cutoff(a, b, c, e, cutoff)
                                for a, b, weight in density for c, e in window)
                bound = variation_budget * tail_function(width, cutoff, len(window)) / mp.pi
                error = abs(exact - truncated)
                assert error <= bound * (1 + mp.mpf("1e-55")) + mp.mpf("1e-75"), (
                    density, window, cutoff, error, bound)
                if bound:
                    worst_ratio = max(worst_ratio, error / bound)
                evaluated += 1
    checks.append({
        "name": "unsmoothed exact inversion tail against closed box integrals",
        "status": "PASS", "cases": evaluated,
        "precision_decimal_digits": mp.mp.dps,
        "largest_observed_error_to_bound_ratio": mp.nstr(worst_ratio, 25),
        "scope": "auxiliary high-precision formula checks, not a continuous proof",
    })

    # Conditional ratio bound is algebraic and includes complex observations.
    for actual_mass in (Fraction(1, 100), Fraction(1, 2), Fraction(1)):
        for perturbation in (Fraction(-1, 1000), Fraction(0), Fraction(1, 1000)):
            approximate_mass = actual_mass + perturbation
            if approximate_mass <= abs(perturbation):
                continue
            for observable in (Fraction(-1), Fraction(-1, 3), Fraction(0), Fraction(1)):
                exact_numerator = actual_mass * observable
                numerator_error = Fraction(1, 1000)
                approximate_numerator = exact_numerator + numerator_error
                lhs = abs(exact_numerator / actual_mass - approximate_numerator / approximate_mass)
                rhs = (numerator_error + abs(perturbation)) / approximate_mass
                assert lhs <= rhs
    checks.append({"name": "actual denominator certificate and conditional ratio", "status": "PASS"})

    # Spike proof: height, variation and mass are exact symbolic formulae.
    m = sp.symbols("m", positive=True)
    height = m**-2
    width = sp.exp(-m)
    assert sp.simplify(m**2 * height - 1) == 0
    assert sp.simplify(m**2 * (height * width) - sp.exp(-m)) == 0
    assert sp.simplify(m**2 * (2 * height) - 2) == 0
    assert sp.limit(m**10 * sp.exp(-m), m, sp.oo) == 0
    checks.append({
        "name": "raw-height counterexample with vanishing polynomial-band interval error",
        "status": "PASS",
        "scope": "abstract inference counterexample, not a claimed billiard source",
    })

    # Independently integrate the Gaussian majorants in the inherited-window
    # addendum, including the four-dimensional Fourier normalization.
    a = sp.symbols("a", positive=True)
    v = sp.symbols("v", real=True)
    h = sp.symbols("h", positive=True)
    gaussian_1d = sp.integrate(sp.exp(-a * v**2 / 2), (v, -sp.oo, sp.oo))
    absolute_moment_1d = 2 * sp.integrate(v * sp.exp(-a * v**2 / 2), (v, 0, sp.oo))
    gaussian_bound = (2 * pi) ** -2 * a**-2
    derivative_bound = gaussian_bound * sp.sqrt(2 / (pi * a))
    assert sp.simplify(gaussian_1d**4 / (2 * pi)**4 - gaussian_bound) == 0
    assert sp.simplify(absolute_moment_1d * gaussian_1d**3 / (2 * pi)**4 - derivative_bound) == 0
    assert sp.simplify(2 * sp.integrate(v, (v, 0, h)) / (2 * h) - h / 2) == 0
    checks.append({
        "name": "finite-peak Gaussian majorants and symmetric-window reference modulus",
        "status": "PASS",
        "scope": "exact integral constants only; compactness and inherited spectral hypotheses are proved or qualified in the text",
    })
    return {
        "status": "PASS", "checks": checks,
        "python_version": sys.version.split()[0], "platform": platform.platform(),
        "mpmath_version": mp.__version__, "sympy_version": sp.__version__,
        "scope": "Finite algebra, normalization and formula verification only; no geometric or spectral qualification.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    result["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    encoded = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
