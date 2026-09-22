#!/usr/bin/env python3
"""Finite exact/high-precision diagnostics for the new comparison statements.

Analytical proofs are in v35/spectral_comparison.tex. These checks are not a
proof assistant or a substitute for the all-configuration arguments.
Dependencies: sympy and mpmath. Checks remain enabled under python -O.
"""
from fractions import Fraction as Q
from itertools import combinations
import json
from math import comb
from pathlib import Path
import mpmath as mp
import sympy as sp


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def determinant_volume(nodes, ell):
    if ell == 1:
        return nodes[0]*0+1
    best = nodes[0]*0
    for subset in combinations(nodes, ell):
        value = nodes[0]*0+1
        for a,b in combinations(subset,2):
            value *= abs(a-b)
        best = max(best,value)
    return best


def main():
    symbolic = 0
    bounds = {}
    for q in range(1,5):
        L = q
        for ell in range(1,q+1):
            z = sp.symbols('z:'+str(ell))
            vand = sp.prod(z[b]-z[a] for a,b in combinations(range(ell),2))
            maximum = 1
            for rows in combinations(range(L+1),ell):
                alternate = sp.det(sp.Matrix([[z[b]**k for b in range(ell)] for k in rows]))
                quotient,remainder = sp.div(alternate,vand,*z)
                require(remainder == 0, 'Alternating minor did not factor')
                maximum = max(maximum,sum(abs(c) for c in sp.Poly(quotient,*z).coeffs()))
                symbolic += 1
            bounds[q,ell] = int(maximum)
    mp.mp.dps = 110
    spectral = 0
    configurations = [
        [Q(1,3)], [Q(0),Q(1)], [Q(1,4),Q(1,4)],
        [Q(1,5),Q(1,5)+Q(1,10**8),Q(1,5)+Q(2,10**8)],
        [Q(0),Q(1,4),Q(1,2),Q(1)],
        [Q(0),Q(1,10**7),Q(3,4),Q(3,4)+Q(1,10**7)],
        [Q(1,3)]*4,
        [Q(1,3),Q(1,3),Q(2,3),Q(1)],
        [Q(1),Q(1,2),Q(0),Q(1,4)],
    ]
    for config in configurations:
        x = [mp.mpf(v.numerator)/v.denominator for v in config]
        q = len(x); L = q
        F = mp.matrix([[mp.exp(1j*k*y) for y in x] for k in range(L+1)])
        sigma = mp.svd(F,compute_uv=False)
        for ell in range(1,q+1):
            vol = determinant_volume(x,ell)
            product = mp.fprod(sigma[j] for j in range(ell))
            if not vol:
                require(abs(product) < mp.mpf('1e-90'), 'Repeated-node rank diagnostic')
            else:
                lower = (2*mp.sin(mp.mpf('0.5')))**(ell*(ell-1)//2)*vol
                upper = mp.sqrt(comb(L+1,ell)*comb(q,ell))*bounds[q,ell]*vol
                require(product >= lower*(1-mp.mpf('1e-70')), 'Exterior lower bound')
                require(product <= upper*(1+mp.mpf('1e-70')), 'Exterior upper bound')
            spectral += 1
    arrangements = 0
    points = [(Q(0),Q(0)),(Q(0),Q(1,32)),(Q(1,32),Q(1,32)),
              (Q(1,64),Q(1,32)),(Q(1,32),Q(-1,32)),
              (Q(1,64),Q(1,64)+Q(1,64)**4),
              (Q(-1,16),Q(1,16)),(Q(1,16),Q(-1,16))]
    for u,v in points:
        raw = [Q(1),Q(2),2+u,3+u,3+v,4+2*u,4+v,5+u+v,6+2*v]
        nodes = [a/16 for a in raw]
        gaps = sorted([abs(u),abs(v-u),abs(v-2*u)],reverse=True)
        rank = len(set(nodes))
        expected = 6 if not u and not v else (8 if 0 in gaps else 9)
        require(rank == expected, 'Two-parameter exact rank')
        for ell in range(1,10):
            vol = determinant_volume(nodes,ell)
            j = max(0,ell-6)
            thin = Q(1)
            for g in gaps[:j]:
                thin *= g/16
            lower = Q(1,32)**(ell*(ell-1)//2-j)*thin
            require(lower <= vol <= thin, 'Exact rational volume bracket')
            require((vol != 0) == (ell <= rank), 'Exact zero-volume pattern')
            arrangements += 1
    rho,tau = sp.symbols('rho tau',positive=True)
    M0 = rho**(-6); M1 = rho**2*tau**(-8)
    f0 = lambda M:M**(-sp.Rational(1,3))
    f1 = lambda M:rho**sp.Rational(1,2)*M**(-sp.Rational(1,4))
    f2 = lambda M:(rho**2*tau)**sp.Rational(2,9)*M**(-sp.Rational(2,9))
    require(sp.simplify(f0(M0)/f1(M0)) == 1,'First crossover')
    require(sp.simplify(f1(M1)/f2(M1)) == 1,'Second crossover')
    result = {'status':'PASS','assertions_used':False,
        'exact_alternating_factorizations':symbolic,
        'high_precision_exterior_comparisons':spectral,
        'precision_decimal_digits':110,
        'exact_arrangement_volume_brackets':arrangements,
        'exact_crossover_identities':2,
        'scope':'Finite diagnostics only; full proofs and fixed-dimension constants are in the manuscript'}
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
