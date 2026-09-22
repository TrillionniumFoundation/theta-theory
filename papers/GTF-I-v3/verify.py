#!/usr/bin/env python3
"""Finite regressions for v3; these are diagnostics, not formal theorem proofs."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def tr(a):
    return [list(x) for x in zip(*a)]


def add(a, b, sign=1):
    return [[x + sign*y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def inv2(a):
    det = a[0][0]*a[1][1] - a[0][1]*a[1][0]
    require(det != 0, 'Singular test matrix')
    return [[a[1][1]/det, -a[0][1]/det], [-a[1][0]/det, a[0][0]/det]]


def tree_risk(b: int, q: F, mutant: str | None) -> F:
    p = 1-q
    factor = b if q == F(1, 4) else sum(((4*q)**k for k in range(b)), F(0))
    if mutant == 'erase-critical-log' and q == F(1, 4):
        factor = 1 if b else 0
    return (p*F(1, 4**b)*factor + q**b)/12


def run(mutant: str | None) -> dict:
    counts = {}
    checked = 0
    for m in range(1, 513):
        b = 0
        while 2**(b+2)-1 <= m:
            b += 1
        states = [(length, value) for length in range(b+1) for value in range(2**length)]
        require(len(states) == 2**(b+1)-1 <= m, 'Uncharged tree labels')
        for length, value in states:
            next_state = (length-1, value % 2**(length-1)) if length else (0, 0)
            require(next_state in states, 'Transition escapes charged label set')
            checked += 1
    counts['charged_tree_transitions'] = checked
    counts['integer_budgets'] = 512

    checked = 0
    for b in range(9):
        for q in [F(1,10), F(1,4), F(2,5), F(3,4), F(9,10)]:
            target = tree_risk(b, q, mutant)
            for t in range(b+4):
                direct = sum(((1-q)*q**k*F(1, 12*4**max(b-k, 0)) for k in range(t)), F(0))
                direct += q**t*F(1, 12*4**max(b-t, 0))
                require(direct <= target, 'Exact transient risk exceeds claimed supremum')
                if t >= b:
                    require(direct == target, 'Exact age sum disagrees with stationary formula')
                checked += 1
    counts['exact_rational_age_sums'] = checked

    checked = 0
    for bits in range(8):
        # Integrate exactly on each dyadic interval, not by sampled quadrature.
        for j in range(2**bits):
            a, z = F(j, 2**bits), F(j+1, 2**bits)
            centre = (a+z)/2
            integral = ((z-centre)**3-(a-centre)**3)/3
            require(integral/(z-a) == F(1,12*4**bits), 'Cylinder variance mismatch')
            checked += 1
    counts['exact_cylinder_integrals'] = checked

    checked = 0
    for q in [.05, .25, .4, .8, .95]:
        p = 1-q
        kappa = math.log(1/q)/math.log(2)
        for i in range(1, 128, 2):
            for j in range(i+2, 128, 2):
                u, v = i/128, j/128
                delta = v-u
                observed = 0.0
                x, y = u, v
                for k in range(16):
                    observed += p*q**k*(x-y)**2
                    x, y = (2*x) % 1, (2*y) % 1
                profile = delta**2 if q < .25 else (delta**2*(1+math.log(1/delta)) if q == .25 else delta**kappa)
                require(observed + 1e-13 >= p*profile/32, 'Orbit-separation diagnostic failed')
                checked += 1
    counts['finite_orbit_separation_cases'] = checked

    a = [[F(1,2), F(-1,3)], [F(1,5), F(2,3)]]
    v = [[F(2), F(1,3)], [F(1,3), F(3)]]
    r = [[F(1), F(1,4)], [F(1,4), F(2)]]
    ident = [[F(1), F(0)], [F(0), F(1)]]
    ia = add(ident, a)
    yy, ww = add(mm(mm(ia,v),tr(ia)),r), add(mm(mm(a,v),tr(a)),r)
    yw = add(mm(mm(ia,v),tr(a)),r)
    observed_v = add(yy,ww) if mutant == 'omit-cross-covariance' else add(add(add(yy,ww),yw,-1),tr(yw),-1)
    require(observed_v == v, 'Correlated difference covariance mismatch')
    c = add(tr(yw),ww,-1)
    require(mm(c,inv2(v)) == a, 'Gaussian regression coefficient mismatch')
    require(add(ww,mm(mm(c,inv2(v)),tr(c)),-1) == r, 'Schur residual mismatch')
    counts['exact_correlated_matrix_identities'] = 3

    checked = 0
    for d in range(1, 5):
        widths = [2.0**(-j*j) for j in range(d)]
        for m in range(1, 257):
            product = 1.
            profile = 0.
            for l, width in enumerate(widths, 1):
                product *= width
                profile = max(profile, (product/m)**(2/l))
            delta = 2*math.sqrt(profile)
            ns = [max(1, math.floor(x/delta)) for x in widths]
            require(math.prod(ns) <= m, 'Anisotropic cover exceeds budget')
            radius2 = sum((width/n/2)**2 for width,n in zip(widths,ns))
            require(radius2 <= 4*d*profile*(1+1e-12), 'Anisotropic radius bound failed')
            checked += 1
    counts['anisotropic_cover_cases'] = checked
    for k in range(1, 13):
        for i in range(17):
            for j in range(i,17):
                x,y=F(i,16),F(j,16)
                require((y-x)**k <= y**k-x**k, 'Contact power inequality failed')
    counts['exact_contact_power_cases'] = 12*153

    old = (ROOT.parent/'GTF-I-v2/revision.tex').read_text()
    marker = '\\section{Acquired geometry and nonuniform causal resolution}'
    require((ROOT/'retained-results.tex').read_text() == old[old.index(marker):], 'Retained quantitative body changed')
    counts['complete_v2_quantitative_body_preserved'] = True
    return {'status': 'passed', 'diagnostics': counts,
            'scope': 'Finite exact identities, finite numerical regressions, and source preservation; not formal proof or independent referee approval.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutant', choices=['erase-critical-log','omit-cross-covariance'])
    args = parser.parse_args()
    try:
        print(json.dumps(run(args.mutant), indent=2, sort_keys=True))
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
