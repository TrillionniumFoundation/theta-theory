#!/usr/bin/env python3
"""Independent finite diagnostics for the September 10 A2 source-pinned review.

No GitHub access, author diagnostic code, or exact nonlinear probability oracle is
used. Symbolic identities and ordinary 60-digit arithmetic are distinguished.
Explicit checks survive python -O; these diagnostics are not a formal certificate.
"""
from __future__ import annotations
import argparse
import itertools
import json
import platform
from collections import Counter
from pathlib import Path
from typing import Any
import mpmath as mp
import sympy as sp

mp.mp.dps = 60
RESULTS: list[dict[str, Any]] = []


def require(name: str, condition: bool, kind: str, detail: str = "") -> None:
    if not bool(condition):
        raise RuntimeError(f"FAILED: {name}: {detail}")
    RESULTS.append({"name": name, "kind": kind, "passed": True, "detail": detail})


def exact(name: str, expression: Any) -> None:
    if isinstance(expression, sp.MatrixBase):
        ok = all(sp.simplify(x) == 0 for x in expression)
    elif isinstance(expression, (tuple, list)):
        ok = all(sp.simplify(x) == 0 for x in expression)
    else:
        ok = sp.simplify(expression) == 0
    require(name, ok, "exact_algebra")


def close(name: str, x: Any, y: Any, tolerance: str = "1e-48") -> None:
    error = abs(mp.mpf(x) - mp.mpf(y))
    require(name, error <= mp.mpf(tolerance), "ordinary_high_precision",
            f"absolute error={mp.nstr(error, 8)}; tolerance={tolerance}")


def jacobi_checks() -> None:
    # Build and eliminate the original (j+1)-site Hessian, rather than merely
    # evaluating the claimed endpoint formula.
    families = [(sp.Rational(1), sp.Rational(2), sp.Rational(2)),
                (sp.Rational(2, 3), sp.Rational(2), sp.Rational(3)),
                (sp.Rational(3, 2), sp.Rational(5, 4), sp.Rational(9, 5))]
    for family, (g, c0, c1) in enumerate(families):
        c = sp.sqrt(c0 * c1)
        sigma = lambda i: sp.sqrt(c1 if i % 2 == 0 else c0)
        for j in range(1, 8):
            H = sp.zeros(j + 1)
            for i in range(j + 1):
                H[i, i] = (1 if i in (0, j) else 2) * (c0 if i % 2 == 0 else c1) / g
            for i in range(j):
                H[i, i + 1] = H[i + 1, i] = -1 / g
            ends = [0, j]
            interior = list(range(1, j))
            effective = H.extract(ends, ends)
            if interior:
                Hint = H.extract(interior, interior)
                G = Hint.inv()
                effective -= H.extract(ends, interior) * G * H.extract(interior, ends)
                expected_G = sp.Matrix(j - 1, j - 1, lambda i, k:
                    g * sigma(i + 1) * sigma(k + 1) / c *
                    sp.chebyshevu(min(i, k), c) *
                    sp.chebyshevu(j - max(i, k) - 2, c) /
                    sp.chebyshevu(j - 1, c))
                exact(f"Green family={family}, j={j}", G - expected_G)
                determinant = Hint.det()
            else:
                determinant = sp.Integer(1)
            invD = sp.diag(1 / sigma(0), 1 / sigma(j))
            expected_H = c / (g * sp.chebyshevu(j - 1, c)) * invD * sp.Matrix(
                [[sp.chebyshevt(j, c), -1], [-1, sp.chebyshevt(j, c)]]) * invD
            exact(f"endpoint Schur family={family}, j={j}", effective - expected_H)
            exact(f"cofactor family={family}, j={j}", -effective[0, 1] - g**(-j) / determinant)
            exact(f"twist/determinant ratio squared family={family}, j={j}",
                  effective[0, 1]**2 / effective.det() -
                  1 / ((c*c - 1) * sp.chebyshevu(j - 1, c)**2))


def physical_inverse_checks() -> None:
    R, alpha, beta, zeta = sp.symbols("R alpha beta zeta", real=True)
    roots = [36*(alpha + beta),
             36*(alpha - beta/2 + sp.sqrt(3)*zeta/2),
             36*(alpha - beta/2 - sp.sqrt(3)*zeta/2)]
    e1 = sum(roots)
    e2 = sum(roots[i]*roots[k] for i in range(3) for k in range(i+1, 3))
    area_direct = sp.sqrt(3)/2 - sp.pi*(R**2 + 2*R*alpha - sp.Rational(33,2)*alpha**2
                                                - sp.Rational(45,4)*(beta**2+zeta**2))
    area_coeff = sp.sqrt(3)/2 - sp.pi*R**2 - sp.pi*R*e1/54 + 41*sp.pi*e1**2/7776 - 5*sp.pi*e2/432
    exact("physical area constraint", sp.expand(area_direct - area_coeff))
    s = sp.symbols("s", real=True)
    split = [36*s, -18*s, -18*s]
    exact("splitting elementary coordinates", [sum(split),
          sum(split[i]*split[k] for i in range(3) for k in range(i+1, 3)) + 972*s**2,
          sp.prod(split) - 11664*s**3])
    r = sp.symbols("r", positive=True)
    g = sp.Rational(1,2)
    phi1 = r/sp.sqrt(g*(g+2*r))
    phi = [phi1, phi1/(2*(1+g/r)), phi1/(4*(1+g/r)**2-1)]
    table = [[sp.Rational(1,4),sp.Rational(3,4),-sp.Rational(5,4),sp.Rational(21,4)],
             [sp.Rational(1,24),sp.Rational(17,72),sp.Rational(35,216),-sp.Rational(491,216)],
             [sp.Rational(1,140),sp.Rational(297,4900),sp.Rational(36243,171500),-sp.Rational(4458537,6002500)]]
    derivatives = [[sp.simplify(sp.diff(f,r,k).subs(r,sp.Rational(1,4))) for k in range(4)] for f in phi]
    for j in range(3):
        exact(f"amplitude derivatives j={j+1}", [derivatives[j][k]/sp.sqrt(2)-table[j][k] for k in range(4)])
    A = sp.symbols("A", positive=True)
    D = sp.Matrix([[ (row[1]+sp.pi*sp.Rational(1,4)*row[0]/(18*A))/A,
                     (-row[2]+5*sp.pi*row[0]/(144*A))/A, row[3]/(2*A)] for row in derivatives])
    claimed = -2*sp.sqrt(2)*(15804720*A+64253*sp.pi)/(72930375*A**4)
    exact("physical three-amplitude determinant", sp.factor(D.det()-claimed))
    C1,C2,C3 = sp.symbols("C1 C2 C3")
    block = sp.zeros(4)
    block[:,0] = sp.Matrix([C1,-2*C1,-4*C2,-6*C3])
    block[1:4,1:4] = D
    exact("four-window limiting block", sp.factor(block.det()-C1*D.det()))
    # Sorted reciprocal roots give the stated distance for sufficiently small s.
    Rm = mp.mpf('0.25')
    for text in ['0.00001','0.0001','0.001']:
        sm = mp.mpf(text)
        left = sorted([1/(Rm+36*sm),1/(Rm-18*sm),1/(Rm-18*sm)])
        right = sorted([1/(Rm-36*sm),1/(Rm+18*sm),1/(Rm+18*sm)])
        close(f"splitting matching distance s={text}", max(abs(a-b) for a,b in zip(left,right)),
              36*sm/(Rm**2-324*sm**2))


def quartic_checks() -> None:
    c,g = sp.symbols("c g", positive=True)
    inverse = (sp.Matrix([[c,-1],[-1,c]])/g).inv()
    derivative = -sum(inverse[i,i]**2 for i in (0,1))/24
    formula = -g**2*c**2/(12*(c*c-1)**2)
    exact("one-flight quartic derivative general", derivative-formula)
    exact("one-flight fixed-area family derivative 8/9", -24*derivative.subs({c:2,g:1})-sp.Rational(8,9))
    lam,a = sp.symbols("lam a", positive=True)
    tprime = (1+lam**4)/(1-lam**4)
    betaprime = -(lam**2/(1-lam**2)-lam**4/(1-lam**4))/(2*a)
    Rprime = 2*betaprime/(3*a)-tprime/(12*a*a)
    cosh2 = (lam**-2+lam**2)/2
    sinh2 = (lam**-2-lam**2)/2
    exact("half-line quartic formula from geometric sums", Rprime+(cosh2+2)/(12*a*a*sinh2))
    exact("fixed-area family boundary derivative sqrt(3)/2",
          -24*(-sp.Rational(9,1)/(12*3*4*sp.sqrt(3)))-sp.sqrt(3)/2)
    gamma = mp.acosh(2)
    limit = -1/(16*mp.sqrt(3))
    def finite(j: int) -> mp.mpf:
        H = mp.matrix([[2, -1],[-1,2]]) if j == 1 else mp.matrix(
            [[mp.sqrt(3)*mp.coth(j*gamma),-mp.sqrt(3)/mp.sinh(j*gamma)],
             [-mp.sqrt(3)/mp.sinh(j*gamma),mp.sqrt(3)*mp.coth(j*gamma)]])
        M = H**-1
        v = []
        for i in range(j+1):
            L = mp.matrix([[mp.sinh((j-i)*gamma)/mp.sinh(j*gamma),mp.sinh(i*gamma)/mp.sinh(j*gamma)]])
            v.append((L*M*L.T)[0])
        interior = mp.fsum(mp.sinh(i*gamma)*mp.sinh((j-i)*gamma)/(mp.sinh(gamma)*mp.sinh(j*gamma))*v[i] for i in range(1,j))
        return -interior/3-(v[0]**2+v[j]**2+2*mp.fsum(v[i]**2 for i in range(1,j)))/24
    close("finite quartic j=1 direct normalization", finite(1),-mp.mpf(1)/27)
    close("finite quartic j=16 approaches half-line",finite(16),limit,"1e-15")


def erasure_checks() -> None:
    # Independent overlap quadrature, not just substitution in arcsin.
    for text in ['0.05','0.2','0.5','0.8']:
        q = mp.mpf(text)
        lam = (1-q)/(1+q)
        angle = mp.atan(mp.sqrt(lam))
        overlap = 2*(angle + mp.quad(lambda x: 1/(lam*mp.cos(x)**2+mp.sin(x)**2/lam),[angle,mp.pi/2]))/mp.pi
        close(f"disk/ellipse overlap q={text}",1-overlap,2*mp.asin(q)/mp.pi)
    # Finite exact product experiments on {erasure,0,1}.
    for n in range(1,6):
        r = [sp.Rational(i+1,2*(n+2)) for i in range(n)]
        probabilities = [{0:[1-x,x,0],1:[1-x,0,x]} for x in r]
        variation = sp.Rational(0)
        affinity = sp.Rational(0)
        for outcome in itertools.product(range(3),repeat=n):
            p = sp.prod(probabilities[i][0][outcome[i]] for i in range(n))
            q = sp.prod(probabilities[i][1][outcome[i]] for i in range(n))
            variation += abs(p-q)/2
            affinity += sp.sqrt(p*q)
        common = sp.prod(1-x for x in r)
        exact(f"erasure product TV n={n}",variation-(1-common))
        exact(f"erasure product Hellinger affinity n={n}",affinity-common)
    for n in [5,20,100,1000]:
        r = [mp.mpf(1)/(n+3)*(1+mp.mpf(i)/n) for i in range(n)]
        intensity = mp.fsum(r)
        common = mp.fprod(1-x for x in r)
        error = mp.exp(-intensity)-common
        bound = mp.fsum(x*x for x in r)/(2*(1-max(r)))
        require(f"Poisson erasure bound n={n}",0 <= error <= bound,"ordinary_high_precision",
                f"error={mp.nstr(error,12)}; bound={mp.nstr(bound,12)}")
    require("fixed-offset tangent error is not o(q)",
            mp.sqrt(mp.mpf('0.01'))/mp.exp(-20) > 1e6,"ordinary_high_precision",
            "Illustration only: d=0.01 is fixed, q=exp(-20).")


def nuisance_and_entropy_checks() -> None:
    u = sp.symbols('u')
    for m in range(1,6):
        cutoff = (1-u)**(m+1)
        exact(f"cutoff splice derivatives through m={m}", [sp.diff(cutoff,u,k).subs(u,1) for k in range(m+1)])
        exact(f"smooth-envelope exponent balances m={m}",
              [sp.Rational(3,m)*(2*m+2)-(6+sp.Rational(6,m)),sp.Rational(2*m+2,m+1)-2])
    for text in ['0.00000001','0.001','0.01','0.1','0.249']:
        eta = mp.mpf(text)
        left = (1-2*eta)*mp.log((1-eta)/eta)
        require(f"confidence logarithm eta={text}",left >= mp.log(1/eta)/4,"ordinary_high_precision")
    # This is an explicitly synthetic constant-amplitude onset model, not an
    # asserted exact finite-offset billiard probability computation.
    for text in ['0.0001','0.005','0.02']:
        delta = mp.mpf(text)
        p0 = delta**2
        finite_KL = -mp.log(1-p0)  # KL(Ber(0) || Ber(p0)); reverse is infinite.
        require(f"one-sided onset KL delta={text}",finite_KL <= p0/(1-p0),"ordinary_high_precision",
                "Synthetic p0=delta^2, pDelta=0; only higher-gap to lower-gap KL is finite.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    jacobi_checks()
    physical_inverse_checks()
    quartic_checks()
    erasure_checks()
    nuisance_and_entropy_checks()
    result = {"status":"pass", "checks":len(RESULTS),
              "counts":dict(sorted(Counter(x['kind'] for x in RESULTS).items())),
              "python":platform.python_version(),"sympy":sp.__version__,"mpmath":mp.__version__,
              "mpmath_decimal_precision":mp.mp.dps,
              "scope":"Finite algebra and ordinary high-precision diagnostics, not interval or formal certification; no author script or exact nonlinear probability oracle.",
              "results":RESULTS}
    text = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')
    else:
        print(text,end='')

if __name__ == '__main__':
    main()
