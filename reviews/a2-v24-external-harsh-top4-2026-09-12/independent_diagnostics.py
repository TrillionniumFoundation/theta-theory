#!/usr/bin/env python3
"""Finite referee diagnostics for A2 v24; not a proof certificate.

Run with Python 3.10+; only the standard library is required.  All checks use
explicit exceptions, so python -O executes the same checks.  This file neither
imports nor modifies manuscript code.  Scope limits are part of the output.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F

SOURCE_SHA = "c35b31b1924a1621374eab72ee60e4cb5ab37df5"
Matrix = tuple[tuple[F, F], tuple[F, F]]
I: Matrix = ((F(1), F(0)), (F(0), F(1)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))


def transpose(a: Matrix) -> Matrix:
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def det(a: Matrix) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse(a: Matrix) -> Matrix:
    d = det(a)
    require(d != 0, "singular test matrix")
    return ((a[1][1] / d, -a[0][1] / d),
            (-a[1][0] / d, a[0][0] / d))


def last_jet_blocks() -> dict[str, object]:
    cases = 0
    for x in (F(1, 4), F(1, 3), F(1, 2), F(2, 3)):
        for r in (F(1), F(3, 2), F(2, 3)):
            # Both physical first-hit linear multipliers must be below one.
            if not (r * x < 1 and x / r < 1):
                continue
            for n in range(3, 13):
                z = x ** n
                c = (1 + z * z) / (1 - z * z)
                s = 2 * z / (1 - z * z)
                block: Matrix = ((c, r ** n * s), (s / r ** n, c))
                proposed_inv: Matrix = ((c, -r ** n * s),
                                       (-s / r ** n, c))
                require(det(block) == 1, "last-jet determinant")
                require(matmul(block, proposed_inv) == I, "last-jet inverse")
                # Independently count the boundary once and interior sites twice.
                N = 12
                own = 1 + 2 * sum(x ** (2 * n * i) for i in range(1, N + 1))
                own += 2 * x ** (2 * n * (N + 1)) / (1 - x ** (2 * n))
                cross = 2 * r ** n * sum(x ** (n * (2 * i + 1))
                                          for i in range(N))
                cross += 2 * r ** n * x ** (n * (2 * N + 1)) / (1 - x ** (2 * n))
                require(own == block[0][0] and cross == block[0][1],
                        "half-line multiplicity sums")
                cases += 1
    return {"cases": cases, "arithmetic": "exact rational", "status": "passed"}


def lattice_recovery() -> dict[str, object]:
    Ls: tuple[Matrix, ...] = (
        ((F(3), F(1)), (F(0), F(2))),
        ((F(5, 2), F(-1, 3)), (F(1, 4), F(7, 3))),
    )
    Ms: tuple[Matrix, ...] = (
        I,
        ((F(2), F(1)), (F(0), F(3))),  # non-unimodular deck pair
        ((F(1), F(2)), (F(-1), F(1))),
    )
    rotation: Matrix = ((F(3, 5), F(-4, 5)), (F(4, 5), F(3, 5)))
    cases = 0
    for L in Ls:
        for M in Ms:
            V = matmul(L, M)
            Mi = inverse(M)
            recovered = matmul(V, Mi)
            gram = matmul(matmul(transpose(Mi), matmul(transpose(V), V)), Mi)
            require(recovered == L, "rank-two lattice recovery")
            require(gram == matmul(transpose(L), L), "Gram formula")
            Vr = matmul(rotation, V)
            rotated_gram = matmul(matmul(transpose(Mi), matmul(transpose(Vr), Vr)), Mi)
            require(rotated_gram == gram, "global-rotation invariance")
            cases += 1
    return {"cases": cases, "arithmetic": "exact rational", "status": "passed"}


def hyperbolic_derivative() -> dict[str, object]:
    cases = 0
    for g, k0, k1 in ((0.7, 1.2, 0.8), (1.0, 1.0, 1.0), (2.0, 0.4, 1.5)):
        c0, c1 = 1 + g * k0, 1 + g * k1
        gamma = math.acosh(math.sqrt(c0 * c1))
        for which in (0, 1):
            def gamma_at(t: float) -> float:
                a, b = (t, k1) if which == 0 else (k0, t)
                return math.acosh(math.sqrt((1 + g * a) * (1 + g * b)))
            base = k0 if which == 0 else k1
            eps = 1e-5
            numerical = (gamma_at(base + eps) - gamma_at(base - eps)) / (2 * eps)
            numerator = g * (c1 if which == 0 else c0)
            formula = numerator / (2 * math.sqrt(c0 * c1) * math.sinh(gamma))
            require(formula > 0, "nonzero hyperbolic differential")
            require(math.isclose(formula, numerical, rel_tol=1e-7, abs_tol=1e-9),
                    "curvature derivative formula")
            cases += 1
    return {"cases": cases, "arithmetic": "floating-point finite difference",
            "relative_tolerance": 1e-7, "status": "passed"}


def gap_quadratic_witness() -> dict[str, object]:
    # Same symmetric action Hessian a=1, but different gaps and curvatures.
    # This is NOT a pair of equal full nonlinear conditional boundary laws.
    for g, curvature, cosh_gamma in ((F(3, 4), F(1, 3), F(5, 4)),
                                    (F(4, 3), F(1, 2), F(5, 3))):
        require(1 + g * curvature == cosh_gamma, "quadratic contact relation")
        require(cosh_gamma ** 2 - 1 == g ** 2, "same action Hessian a=1")
    return {"cases": 2, "arithmetic": "exact rational", "status": "passed",
            "scope": "Action Hessians alone do not recover onset. No full-law nonidentifiability claim."}


def finite_signature_witness() -> dict[str, object]:
    # Analytic convex oval: support h(theta)=3-cos(2theta)/3-cos(3theta)/16.
    # Its radius of curvature is 3+cos(2theta)+cos(3theta)/2 >= 3/2.
    # The curvature minimum 2/9 is unique, but nearby scalar curvature targets
    # have two in-arc matches at +/-theta. Higher signatures distinguish them.
    require(F(3) - F(1) - F(1, 2) == F(3, 2), "positive curvature-radius bound")
    def curvature(theta: float) -> float:
        return 1 / (3 + math.cos(2 * theta) + 0.5 * math.cos(3 * theta))
    cases = 0
    for theta in (0.01, 0.02, 0.03, 0.04, 0.06, 0.08):
        positive, negative = curvature(theta), curvature(-theta)
        require(positive == negative, "two equal scalar finite signatures")
        require(positive > 2 / 9 and theta < 0.1, "two matches inside arc")
        cases += 1
    return {"cases": cases, "status": "passed",
            "scope": "Witness against an outside-arc margin implying unique noisy in-arc matching; not a counterexample to full analytic rigidity."}


def one_flight_reconstruction() -> dict[str, object]:
    # Exact algebra for signed mixed-type endpoint support, NOT for a
    # same-type long-bridge limiting law.
    def rational_sqrt(x: F) -> F:
        a, b = math.isqrt(x.numerator), math.isqrt(x.denominator)
        require(a * a == x.numerator and b * b == x.denominator,
                "test value must have a rational square root")
        return F(a, b)
    cases = 0
    for g in (F(3, 4), F(4, 3)):
        for u in (F(-1, 4), F(-1, 8), F(0), F(1, 8), F(1, 4)):
            for graph in (u*u + u**3/F(10) + u**4/F(20),
                          F(3, 4)*u*u - u**3/F(12) + u**4/F(15)):
                length_squared = (g + graph)**2 + u*u
                recovered = rational_sqrt(length_squared - u*u) - g
                require(recovered == graph, "one-flight signed support inverse")
                cases += 1
    return {"cases": cases, "arithmetic": "exact rational", "status": "passed",
            "scope": "Mixed-type one-flight benchmark only; no equivalence to limiting same-type observations asserted."}


def main() -> None:
    result = {
        "source_commit": SOURCE_SHA,
        "all_diagnostics_passed": True,
        "last_jet_blocks": last_jet_blocks(),
        "rank_two_lattice": lattice_recovery(),
        "hyperbolic_derivative": hyperbolic_derivative(),
        "gap_quadratic_witness": gap_quadratic_witness(),
        "one_flight_reconstruction": one_flight_reconstruction(),
        "finite_signature_witness": finite_signature_witness(),
        "not_certified": ["Full manuscript correctness", "Uniform global physical acquisition",
                          "Complete source graph or native TeX build", "Journal acceptance"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
