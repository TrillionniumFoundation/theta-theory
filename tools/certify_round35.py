#!/usr/bin/env python3
"""Exact rational C1 certificate for the infinite-lattice two-duration map.

Taylor coefficients are local: J applications of the banded generator cannot
reach the boundary of a truncation with J+2 sites. An operator-norm tail bound
then covers ALL remaining powers on the infinite Hilbert space. This certifies
only the stated finite-time embedding inequality, not the statistical proofs.
No floating-point decision is used by the certificate.
"""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path
from typing import Dict, Tuple
Poly = Dict[Tuple[int, int], F]
ONE: Poly = {(0, 0): F(1)}
C: Poly = {(1, 0): F(1)}
K: Poly = {(0, 1): F(1)}

def add(*ps: Poly) -> Poly:
    out: Poly = {}
    for p in ps:
        for a, x in p.items():
            out[a] = out.get(a, F(0)) + x
    return {a: x for a, x in out.items() if x}

def scale(p: Poly, x: F) -> Poly:
    return {a: x * y for a, y in p.items() if x * y}

def mul(p: Poly, q: Poly) -> Poly:
    out: Poly = {}
    for (i, j), x in p.items():
        for (k, l), y in q.items():
            a = (i + k, j + l)
            out[a] = out.get(a, F(0)) + x * y
    return {a: x for a, x in out.items() if x}

def deriv(p: Poly, axis: int) -> Poly:
    out: Poly = {}
    for a, x in p.items():
        if a[axis]:
            b = list(a); b[axis] -= 1
            out[tuple(b)] = x * a[axis]
    return out

def evaluate(p: Poly, c: F, k: F) -> F:
    return sum((x * c**i * k**j for (i, j), x in p.items()), F(0))

def box_bound(p: Poly) -> F:
    """Upper bound on |p| for c,k in [1,2], using centered monomials."""
    centered: Poly = {}
    for (i, j), a in p.items():
        for r in range(i + 1):
            for s in range(j + 1):
                coefficient = (a * math.comb(i, r) * math.comb(j, s)
                    * F(3, 2)**(i+j-r-s) * F(1, 2)**(r+s))
                centered[(r, s)] = centered.get((r, s), F(0)) + coefficient
    return sum(map(abs, centered.values()), F(0))

def coefficients(order: int = 9, sites: int | None = None) -> list[Poly]:
    if order < 4:
        raise ValueError('order must be at least four')
    sites = order + 2 if sites is None else sites
    if sites < order + 2:
        raise ValueError('insufficient sites for the stated locality proof')
    eps, cb, kb = F(1, 10), F(3, 2), F(1)
    q: list[Poly] = [{} for _ in range(sites)]
    v: list[Poly] = [{} for _ in range(sites)]
    v[0] = ONE.copy()
    out = []
    for _ in range(order + 1):
        out.append(q[0].copy())
        new_v = []
        for j in range(sites):
            stiff = K if j == 0 else scale(ONE, kb)
            damp = C if j == 0 else scale(ONE, cb)
            value = add(scale(mul(stiff, q[j]), F(-1)),
                        scale(mul(damp, v[j]), F(-1)),
                        scale(q[j], -eps * (1 if j == 0 else 2)))
            if j:
                value = add(value, scale(q[j-1], eps))
            if j+1 < sites:
                value = add(value, scale(q[j+1], eps))
            new_v.append(value)
        q, v = v, new_v
    return out

def certificate(tau: F = F(1, 32), order: int = 9) -> dict:
    if tau <= 0:
        raise ValueError('tau must be positive')
    D = F(27, 5)  # 1 + max damping 2 + max stiffness (2+4/10)
    if 2*D*tau >= 1:
        raise ValueError('geometric exponential bound requires 2*D*tau < 1')
    cs = coefficients(order)
    def h(t: F) -> Poly:
        return add(*(scale(p, t**(j+1)/math.factorial(j+1))
                     for j, p in enumerate(cs)))
    h1, h2 = h(tau), h(2*tau)
    f1 = scale(add(h2, scale(h1, F(-16)), scale(ONE, 6*tau*tau)),
               F(3, 4)/tau**3)
    f2 = scale(add(h2, scale(h1, F(-8)), scale(ONE, 2*tau*tau)),
               F(3)/tau**4)
    fk = add(mul(f1, f1), scale(f2, F(-1)), scale(ONE, F(-1, 10)))
    def tail(t: F) -> F:
        return (2*D**(order+1)*t**(order+2)
                / (math.factorial(order+1)*(1-D*t)))
    e1 = F(3, 4)/tau**3*(tail(2*tau)+16*tail(tau))
    e2 = F(3)/tau**4*(tail(2*tau)+8*tail(tau))
    f1max = box_bound(f1)
    bounds = []
    for row, p in enumerate((f1, fk)):
        bs = []
        for axis in range(2):
            error_poly = add(deriv(p, axis), scale(ONE, F(-int(row == axis))))
            err = e1 if row == 0 else (2*e1*box_bound(deriv(f1, axis))
                         +2*f1max*e1+2*e1*e1+e2)
            bs.append(box_bound(error_poly)+err)
        bounds.append(bs)
    f2bound = sum((x*x for row in bounds for x in row), F(0))
    return {
        'scope': 'C1 two-duration embedding on the infinite half-line lattice',
        'parameter_rectangle': {'c': ['1','2'], 'k': ['1','2']},
        'bath': {'c_b':'3/2','k_b':'1','epsilon':'1/10'},
        'tau': str(tau), 'order': order, 'sites_for_local_coefficients': order+2,
        'decision_arithmetic': 'fractions.Fraction; exact rational inequalities',
        'derivative_error_bounds_exact': [[str(x) for x in row] for row in bounds],
        'derivative_error_bounds_decimal': [[float(x) for x in row] for row in bounds],
        'frobenius_bound_squared_exact': str(f2bound),
        'frobenius_bound_squared_decimal': float(f2bound),
        'threshold_squared': '1/4',
        'f1_absolute_bound_exact': str(f1max+e1),
        'f1_absolute_bound_decimal': float(f1max+e1),
        'f1_absolute_threshold': '3',
        'embedding_certified': f2bound < F(1, 4) and f1max+e1 <= 3 and tau <= 1,
        'all_statistical_theorems_formally_verified': False,
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--tau', default='1/32')
    args = parser.parse_args()
    report = certificate(F(args.tau))
    text = json.dumps(report, indent=2, sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    print(text)
    return 0 if report['embedding_certified'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
