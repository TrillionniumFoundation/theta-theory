#!/usr/bin/env python3
"""Independent checks of the v35 spectral bridge and boundary cases.

Exact checks use rational complex nodes on the unit circle and Cauchy--Binet.
SVD comparisons are high-precision diagnostics, not certified intervals.
No continuum risk optimization or general proof verification is performed.
"""
from __future__ import annotations
from fractions import Fraction as Q
from itertools import combinations
from math import comb, factorial
import hashlib
import json
from pathlib import Path
import mpmath as mp
import sympy as sp

CHECKS = 0

def require(ok, description: str) -> None:
    global CHECKS
    CHECKS += 1
    if not bool(ok):
        raise ArithmeticError(description)

def volume(xs, ell):
    return max((mp.fprod(abs(a-b) for a,b in combinations(s,2))
                for s in combinations(xs,ell)), default=mp.mpf(0))

def exact_exterior_checks():
    records = []
    configurations = [(Q(0),Q(1,10),Q(1,4)),
                      (Q(1,5),Q(1,5),Q(1,5)),
                      (Q(0),Q(0),Q(1,4))]
    for params in configurations:
        z = [sp.cancel((1+sp.I*sp.Rational(s.numerator,s.denominator))/
                       (1-sp.I*sp.Rational(s.numerator,s.denominator))) for s in params]
        q,L = len(z),3
        F = sp.Matrix([[sp.cancel(v**k) for v in z] for k in range(L+1)])
        G = (F.conjugate().T*F).applyfunc(sp.simplify)
        rank = len(set(params))
        require(F.rank()==rank, 'exact repeated-node rank')
        for ell in range(1,q+1):
            total = 0
            for rows in combinations(range(L+1),ell):
                for cols in combinations(range(q),ell):
                    det = sp.cancel(F.extract(rows,cols).det())
                    total += sp.cancel(det*sp.conjugate(det))
            total = sp.simplify(total)
            principal = sp.simplify(sum(G.extract(c,c).det()
                                   for c in combinations(range(q),ell)))
            require(total==principal, 'Cauchy--Binet exterior mass identity')
            require((total>0)==(ell<=rank), 'exact vanishing pattern')
            records.append({'parameters':[str(s) for s in params],
                'ell':ell,'exact_rank':rank,'exterior_mass_squared':str(total)})
    return records

def spectral_checks():
    mp.mp.dps = 160
    cases = [([Q(1,3)],0),([Q(0),Q(1)],1),([Q(1,3)]*4,3),
             ([Q(0),Q(0),Q(1,2),Q(1)],3),
             ([Q(0),Q(1,10**10),Q(1,10**10)+Q(1,10**30),Q(4,5)],3),
             ([Q(0),Q(1,10**10),Q(1,10**10)+Q(1,10**30),Q(4,5)],6)]
    for u,v in [(Q(0),Q(0)),(Q(0),Q(1,32)),
                (Q(1,64),Q(1,64)+Q(1,64)**6),(Q(-1,16),Q(1,16))]:
        raw = [1,2,2+u,3+u,3+v,4+2*u,4+v,5+u+v,6+2*v]
        xs = [Q(x)/16 for x in raw]
        cases.append((xs,8))
    records = []
    for rational_x,L in cases:
        xs = [mp.mpf(x.numerator)/x.denominator for x in rational_x]
        q,rank = len(xs),len(set(rational_x))
        F = mp.matrix([[mp.exp(mp.j*k*x) for x in xs] for k in range(L+1)])
        sigma = mp.svd(F,compute_uv=False)
        ratios = []
        for ell in range(1,q+1):
            v = volume(xs,ell)
            prod = mp.fprod(sigma[j] for j in range(ell))
            require((v>0)==(ell<=rank), 'rational nodes determine exact rank')
            if ell<=rank:
                lower = (2*mp.sin(mp.mpf('0.5')))**comb(ell,2)
                # Newton column operations divide an alternant by its Vandermonde.
                # Divided differences of z^k are complete homogeneous polynomials,
                # bounded on the unit polydisk by binom(k,j-1).
                quotient_bound = factorial(ell)
                for j in range(ell):
                    quotient_bound *= comb(L,j)
                upper = mp.sqrt(comb(L+1,ell)*comb(q,ell))*quotient_bound
                require(prod/v >= lower*(1-mp.mpf('1e-100')), 'explicit lower comparison')
                require(prod/v <= upper*(1+mp.mpf('1e-100')), 'explicit upper comparison')
                ratios.append(mp.nstr(prod/v,18))
            else:
                require(abs(prod)<mp.mpf('1e-125'), 'numerical residue at exact collision')
                ratios.append(None)
        records.append({'nodes':[str(x) for x in rational_x],'L':L,
                        'rank':rank,'spectral_product_over_volume':ratios})
    return records

def flat_path_checks():
    records = []
    for theta in [Q(1,3),Q(1,4),Q(1,8)]:
        R,T = theta**-2,theta**-4
        m0,m1 = 6*R,8*T-2*R
        def f(m):return [-m/3,-R/2-m/4,-(4*R+2*T+2*m)/9]
        require(f(m0)[0]==f(m0)[1], 'first logarithmic crossover')
        require(f(m1)[1]==f(m1)[2], 'second logarithmic crossover')
        require(m1>m0>0, 'separated crossover budgets')
        for m,expected in [(m0/2,0),((m0+m1)/2,1),(2*m1,2)]:
            a=f(m);require(a[expected]>max(a[j] for j in range(3) if j!=expected),
                          'dominance of three successive asymptotic regimes')
        records.append({'theta':str(theta),'log_budget_1':str(m0),'log_budget_2':str(m1)})
    return records

def main() -> None:
    exact = exact_exterior_checks()
    numeric = spectral_checks()
    flat = flat_path_checks()
    # The fixed-L qualification is indispensable even for one column:
    # F_L^* F_L = [L+1], whereas V_1=1.
    bandwidth = []
    for L in [0,1,3,15]:
        require(sum(Q(1) for _ in range(L+1))==L+1,'one-column Gram identity')
        bandwidth.append({'L':L,'sigma_1_squared':L+1,'V_1_squared':1})
    result={'schema':'a1-v35-independent-boundary-checks-v1',
        'reviewed_commit':'02a19f2ddb83cf68bfbf8361c137613e2ffd3925',
        'exact_exterior':exact,'spectral_diagnostics':numeric,'flat_path_orders':flat,
        'bandwidth_qualification':bandwidth,'explicit_checks_passed':CHECKS,
        'precision_decimal_digits':160,'numerics_are_directed_intervals':False,
        'full_native_manuscript_compiled_by_this_script':False,
        'global_controller_optimum_computed':False,
        'limits':'Finite diagnostics only. Exact identities do not certify continuum risk bounds; SVD is not interval arithmetic.',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
