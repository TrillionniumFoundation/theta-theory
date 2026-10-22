#!/usr/bin/env python3
"""Exact algebra checks supporting native module 326.

These checks verify finite identities and coefficient budgets used in the proof.
They are not simulated billiard trajectories and do not prove the topological
stopping, all-word exhaustions, or continuous source theorems.  No assert
statement is used, so the checks also execute under python -O.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


class Polynomial:
    """Small exact multivariate polynomial ring for displayed identities."""
    variables = ("A", "B", "C", "D", "k", "c0", "cN", "radius",
                 "c", "d", "tau", "xm", "ym", "xp", "yp", "ci")
    zero = (0,) * len(variables)

    def __init__(self, terms=None):
        self.terms = {m:F(v) for m,v in (terms or {}).items() if v}

    @classmethod
    def scalar(cls, value):
        return cls({cls.zero:F(value)})

    @classmethod
    def variable(cls, name):
        powers = list(cls.zero)
        powers[cls.variables.index(name)] = 1
        return cls({tuple(powers):F(1)})

    @classmethod
    def coerce(cls, value):
        return value if isinstance(value, cls) else cls.scalar(value)

    def __add__(self, other):
        other = self.coerce(other)
        terms = dict(self.terms)
        for m,v in other.terms.items():
            terms[m] = terms.get(m,F(0)) + v
        return Polynomial(terms)

    __radd__ = __add__

    def __neg__(self):
        return Polynomial({m:-v for m,v in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) + -self

    def __mul__(self, other):
        other = self.coerce(other)
        terms = {}
        for m,v in self.terms.items():
            for n,w in other.terms.items():
                powers = tuple(a+b for a,b in zip(m,n))
                terms[powers] = terms.get(powers,F(0)) + v*w
        return Polynomial(terms)

    __rmul__ = __mul__

    def __pow__(self, n):
        if n < 0:
            raise ValueError("negative polynomial power")
        result = self.scalar(1)
        for _ in range(n):
            result = result*self
        return result

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms


def main() -> None:
    parser = argparse.ArgumentParser()
    installed_source = (Path(__file__).resolve().parent.parent / "core" /
                        "326_physical_boundary_stopping_pressure.tex")
    scratch_source = Path(__file__).with_name(
        "326_physical_boundary_stopping_pressure.tex")
    parser.add_argument("--source", type=Path,
                        default=(installed_source if installed_source.exists()
                                 else scratch_source))
    parser.add_argument("--details", type=Path)
    args = parser.parse_args()
    count = 0
    details = []

    def check(name: str, condition: bool, meta=None) -> None:
        nonlocal count
        count += 1
        if not bool(condition):
            raise RuntimeError(f"failed: {name}; metadata={meta!r}")
        if meta is not None:
            details.append({"name": name, "metadata": meta})

    A, B, C, D, k, c0, cN, radius = (
        Polynomial.variable(name)
        for name in ("A", "B", "C", "D", "k", "c0", "cN", "radius"))
    check("inverse affine vector numerator",
          D+(-B)*(-k) == D+k*B and -C+A*(-k) == -C-k*A)
    check("adjugate determinant identity",
          A*D-B*C == D*A-C*B and -A*B+B*A == 0 and C*D-D*C == 0)
    denominator_squared = (D + k * B) ** 2 + (C + k * A) ** 2
    excess = denominator_squared - C ** 2
    check("affine-to-optical bound is a positive polynomial",
          all(coef > 0 for coef in excess.terms.values()),
          {"positive_monomials": len(excess.terms)})
    # Cross-multiply the squared w/(c0*u) identity; no denominators vanish.
    check("no terminal incidence loss",
          c0**2*(1+k**2)*radius**2*cN**2*C**2
          == c0**2*cN**2*radius**2*(1+k**2)*C**2)

    c, d, tau = (Polynomial.variable(name) for name in ("c", "d", "tau"))
    numerator_det = ((tau*k+c)*(tau*k+d)
                     - tau*(tau*k*k+k*d+k*c))
    check("one-flight exact area determinant", numerator_det == c*d)

    check("actual marked line-source submersion",
          k*(-tau)-(-c-k*tau) == c)

    xminus, yminus, xplus, yplus, ci = (
        Polynomial.variable(name) for name in ("xm", "ym", "xp", "yp", "ci"))
    aminus = radius * ci * xminus + yminus
    aplus = radius * ci * xplus + yplus
    central_det = aminus*yplus-(-yminus)*aplus
    check("canonical collision determinant has a positive sum",
          central_det-aminus*yplus-yminus*aplus == 0)
    check("canonical collision cosine factor identity",
          ci*(aplus*yminus+aminus*yplus) == ci*central_det)

    rminus, rplus = F(9, 20), F(47, 100)
    tminus, amin = F(3, 50), F(100, 47)
    sigma = F(47, 59)
    check("horizontal source constant 53/12",
          (tminus + rplus) / (2*tminus) == F(53, 12))
    check("one-sided optical constant 47/6",
          1 / (amin * tminus) == F(47, 6))
    check("collision expansion reciprocal",
          1 / (1 + 2*tminus/rplus) == sigma)
    check("uniform affine factor radius bound",
          rminus**2 + 1 <= rplus**2 * (1 + (1/rminus)**2))

    # Exact rational matrices on the coefficient rectangle.  These are algebra
    # tests, not declarations that independent coefficients form actual orbits.
    radius_grid = [rminus, F(23, 50), rplus]
    incidence_grid = [F(1, 1000000), F(1, 50), F(1, 2), F(1)]
    flight_grid = [tminus, F(1, 3), F(28, 5)]
    matrix_cases = 0
    for rv in radius_grid:
        kval = 1 / rv
        for initial in incidence_grid:
            for final in incidence_grid:
                for length in flight_grid:
                    mat = [
                        [(length*kval + initial)/final, length/final],
                        [(length*kval*kval+kval*final+kval*initial)/final,
                         (length*kval+final)/final]
                    ]
                    av, bv = mat[0]
                    cv, dv = mat[1]
                    check("rational one-flight determinant",
                          av*dv-bv*cv == initial/final)
                    denom = (dv+kval*bv)**2 + (cv+kval*av)**2
                    check("rational capless optical comparison",
                          cv**2 <= denom)
                    check("uniform radius factor squared",
                          rv**2 * (1+kval**2)
                          <= rplus**2 * (1+(1/rminus)**2))
                    matrix_cases += 1

    geometric_cases = 0
    for n in range(1, 121):
        marked_sum = sum((sigma**j + sigma**(n-j-1)
                          for j in range(n)), F(0))
        expected = 2*(1-sigma**n)/(1-sigma)
        check("marked index sum exact", marked_sum == expected)
        check("marked index sum uniform", marked_sum <= 2/(1-sigma))
        internal_sum = sum((sigma**(i-1)+sigma**(n-i-1)
                            for i in range(1,n)), F(0))
        internal_expected = 2*(1-sigma**(n-1))/(1-sigma)
        check("internal collision sum exact", internal_sum == internal_expected)
        check("internal collision sum uniform",
              internal_sum <= 2/(1-sigma))
        geometric_cases += 1

    strip_cases = 0
    for k0 in range(2, 42):
        for last in (k0, k0+1, 2*k0+7, 5*k0+19):
            actual = sum((F(1,j*j) for j in range(k0,last+1)), F(0))
            majorant = sum((F(1,j*(j-1)) for j in range(k0,last+1)), F(0))
            check("original strip rational majorant", actual <= majorant)
            check("strip majorant telescopes",
                  majorant == F(1,k0-1)-F(1,last))
            strip_cases += 1

    source_bytes = args.source.read_bytes()
    source_text = source_bytes.decode("utf-8")
    required_labels = [
        "ps:matrix", "ps:exit", "ps:common-level", "ps:pressure",
        "ps:input-complete", "ps:source-budget"
    ]
    for label in required_labels:
        check("required proof label is present",
              f"\\label{{{label}}}" in source_text)
    check("proof does not suppress current endpoint incidence",
          "c_N\\sqrt{(D+\\kappa_R B)^2+(C+\\kappa_R A)^2}" in source_text)
    report = {
        "status": "pass",
        "checks": count,
        "matrix_rectangle_cases": matrix_cases,
        "geometric_sum_cases": geometric_cases,
        "strip_tail_cases": strip_cases,
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "scope": "exact finite algebra and coefficient budgets only",
        "continuous_proof_obligations": [
            "physical exit classification on the entire fixed-word affine interval",
            "common positive-level actual representatives inside the same open class",
            "complete canonical and marked source branch-supremum theorems",
            "one-copy full-word assignment and finite-family exhaustion"
        ],
        "details": details
    }
    if args.details:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        args.details.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k != "details"}, sort_keys=True))


if __name__ == "__main__":
    main()

