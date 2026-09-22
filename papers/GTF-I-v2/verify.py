#!/usr/bin/env python3
"""Finite regression checks; these are not a verification of the proofs."""
from __future__ import annotations
from fractions import Fraction as F
import argparse
import itertools
import json
import math
import random


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--mutant', choices=['omit-calibration-noise','wrong-projective-rate'])
    mutant = parser.parse_args().mutant
    checks = {}
    count = 0
    # The least-favourable nuisance minimizes the divergence of the paired data.
    for sig2, tau2, m in itertools.product([F(0),F(1,9),F(1),F(4)], repeat=3):
        if sig2+tau2 == 0:
            continue
        v2 = sig2+tau2
        eta = -tau2*m/v2
        divergence = F(0)
        if sig2:
            divergence += (m+eta)**2/(2*sig2)
        else:
            require(m+eta == 0, 'Degenerate signal must have equal means')
        if tau2:
            divergence += eta**2/(2*tau2)
        else:
            require(eta == 0, 'Degenerate calibration must have equal means')
        expected = m*m/(2*v2)
        if mutant == 'omit-calibration-noise' and sig2:
            expected = m*m/(2*sig2)
        require(divergence == expected, 'Paired calibration KL identity')
        count += 1
    checks['exact_paired_gaussian_divergences'] = count
    # Cross-ratio computation, including arbitrarily weak positive refresh.
    count = 0
    for d in range(1,7):
        n=d+1
        for gamma in [F(1,10000),F(1,50),F(1,5),F(4,5),F(1)]:
            a,b=1-gamma,gamma/n
            matrix=[[a+b if i==j else b for j in range(n)] for i in range(n)]
            cross=max(matrix[i][k]*matrix[j][l]/(matrix[i][l]*matrix[j][k])
                      for i,j,k,l in itertools.product(range(n),repeat=4))
            require(cross == ((a+b)/b)**2, 'Refresh cross ratio')
            rho=a/(a+2*b)
            if mutant == 'wrong-projective-rate':
                rho=1-gamma
            require(rho == ((a+b)/b-1)/((a+b)/b+1), 'Projective coefficient')
            require(0 <= rho < 1, 'Strict positive refresh contraction')
            count += 1
    checks['exact_refresh_cross_ratios'] = count
    # The integer-budget anisotropic cover works also for small budgets.
    count = 0
    for d in range(1,6):
        for widths in [tuple([1.0]*d),tuple(2.0**(-4*j) for j in range(d)),
                       tuple(3.0**j for j in range(d))]:
            a=sorted(widths,reverse=True)
            for M in list(range(1,101))+[257,1024,10001]:
                product=1.0
                terms=[]
                for ell,x in enumerate(a,1):
                    product*=x
                    terms.append((product/M)**(2.0/ell))
                delta=2*math.sqrt(max(terms))
                subdivisions=[max(1,math.floor(x/delta)) for x in widths]
                require(math.prod(subdivisions) <= M, 'Integer cover exceeds labels')
                require(all(x/k <= 2*delta*(1+1e-12) for x,k in zip(widths,subdivisions)),
                        'Coordinate cover radius')
                count += 1
    checks['anisotropic_integer_covers'] = count
    # Projective contraction and invariant domains: sampled diagnostics only.
    rng=random.Random(20260922)
    count=0
    def h(p,q):
        x=[math.log(a/b) for a,b in zip(p,q)]
        return max(x)-min(x)
    def normalized(x):
        z=sum(x); return [a/z for a in x]
    for d in range(1,6):
        n=d+1
        for gamma in [0.0001,0.02,0.2,0.8,1.0]:
            rho=(1-gamma)/(1-gamma+2*gamma/n)
            for _ in range(20):
                p=normalized([math.exp(rng.uniform(-4,4)) for _ in range(n)])
                q=normalized([math.exp(rng.uniform(-4,4)) for _ in range(n)])
                u=[rng.uniform(-1,1) for _ in range(d)]
                eps=0.25*rng.random(); sign=rng.choice([-1,1])
                r=[1]+[1+sign*eps*math.tanh(x) for x in u]
                def step(x):
                    return normalized([((1-gamma)*x[i]+gamma/n)*r[i] for i in range(n)])
                require(h(step(p),step(q)) <= rho*h(p,q)+1e-11, 'Sampled projective contraction')
                count += 1
    checks['sampled_projective_contractions'] = count
    # Exact two-mode product expectation; independent case is one regression.
    count=0
    for p,rho in itertools.product([F(1,5),F(1,2),F(1)], [F(0),F(1,3),F(4,5)]):
        q=1-p*(1-rho*rho)
        for m in range(1,7):
            expectation=sum(p**sum(w)*(1-p)**(m-sum(w))*rho**(2*sum(w))
                            for w in itertools.product([0,1],repeat=m))
            require(expectation == q**m, 'Block second-moment product')
            count += 1
    checks['exact_block_product_moments'] = count
    # Explicit expanding/cancelling maps exercise the exact-suffix telescope.
    factors=[2.0,0.1,3.0,0.2,1.0,0.3]
    perturbations=[0.01,-0.02,0.005,0.006,-0.01,0.01]
    exact=approx=0.0
    for t,(a,e) in enumerate(zip(factors,perturbations),1):
        exact=a*exact+1; approx=a*approx+1+e
        bound=sum(abs(perturbations[j])*math.prod(abs(x) for x in factors[j+1:t]) for j in range(t))
        require(abs(exact-approx) <= bound+1e-12, 'Hybrid suffix telescope')
    checks['expanding_suffix_telescope'] = len(factors)
    print(json.dumps({'status':'passed','checks':checks,'total':sum(checks.values()),
                      'scope':'Finite algebraic and numerical regressions, not formal proof verification.'},
                     sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
