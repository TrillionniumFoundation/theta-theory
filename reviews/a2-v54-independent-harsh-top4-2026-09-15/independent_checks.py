#!/usr/bin/env python3
"""Independent finite controls for the A2 v54 referee report.

Python standard library only; no author modules imported. Run with python and
python -O. These finite checks are not a theorem prover or a billiard simulation.
"""
from fractions import Fraction as Q
from itertools import product
from math import exp, expm1, floor, log, log1p, sqrt
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def tv(p: dict, q: dict) -> Q:
    return sum((abs(p.get(k, Q(0)) - q.get(k, Q(0)))
                for k in p.keys() | q.keys()), Q(0)) / 2


def capped(p: Q, marks: tuple, b: int) -> dict:
    require(0 < p < 1 and b >= 1 and sum(marks) == 1, 'invalid law')
    law = {('cemetery', 0): (1-p)**b}
    for k in range(1, b+1):
        for j, mass in enumerate(marks):
            law[(k, j)] = (1-p)**(k-1)*p*mass
    require(sum(law.values()) == 1, 'normalization')
    return law


def count_risk(p0: float, p1: float, b: int) -> float:
    require(0 < p1 < p0 < 1 and b >= 1, 'invalid count experiment')
    # Exact likelihood crossing, up to floating evaluation; ties have no effect.
    crossing = 1 + log(p0/p1)/(log1p(-p1)-log1p(-p0))
    k = min(b, floor(crossing))
    return (exp(k*log1p(-p0)) - expm1(k*log1p(-p1)))/2


def main() -> None:
    result = {'scope': 'independent finite diagnostics, not proof certification'}
    f2 = 4*(Q(1, 25)-Q(1, 81))
    require(f2 == Q(224, 2025), 'F squared integral')
    require(f2/4 == Q(56, 2025), 'limiting variance')
    require(f2/Q(256) == Q(7, 16200), 'Hellinger coefficient')
    require(4*f2/Q(256) == Q(7, 4050), 'likelihood coefficient')
    g = Q(4, 5)
    k0, k1 = Q(80, 7), Q(40, 3)
    a0, a1 = k0*k0+2*k0/g, k1*k1+2*k1/g
    require((a0, a1, a1-a0) == (Q(7800,49), Q(1900,9), Q(22900,441)), 'Hessians')
    require((1+g*k0, 1+g*k1) == (Q(71,7), Q(35,3)), 'escape exponents')
    # Without the normalizing correction, the claimed leading density change
    # has nonzero integral; this negative control must detect that error.
    require(-Q(1,16)*Q(4,9) != 0, 'omitted normalizer negative control')
    result['exact_expansion_controls'] = {
        'integral_F2': str(f2), 'a0_squared': str(a0), 'a1_squared': str(a1),
        'difference': str(a1-a0), 'H2_coefficient_per_Delta2_over_d4': '7/16200'}
    cases = 0
    for p0, p1 in [(Q(1,3),Q(1,8)), (Q(1,10),Q(1,100)), (Q(4,5),Q(1,5))]:
        for b in [1,2,5,12,25]:
            q0, q1 = (Q(1,3),Q(2,3)), (Q(2,5),Q(3,5))
            full0, full1 = capped(p0,q0,b), capped(p1,q1,b)
            count0, count1 = capped(p0,(Q(1),),b), capped(p1,(Q(1),),b)
            sim1 = capped(p1,q0,b)
            a_0, a_1 = 1-(1-p0)**b, 1-(1-p1)**b
            eta = sum(abs(x-y) for x,y in zip(q0,q1))/2
            full_tv, count_tv = tv(full0,full1), tv(count0,count1)
            require(a_0-a_1 <= full_tv <= a_0, 'common cemetery bounds')
            require(tv(sim1,full1) == a_1*eta, 'count simulation kernel')
            require(0 <= (full_tv-count_tv)/2 <= a_1*eta/2, 'Bayes risk comparison')
            # Bit-to-full kernel: accepted bit draws the conditional full0 law.
            bit_sim1 = {('cemetery',0): 1-a_1}
            for key,mass in full0.items():
                if key[0] != 'cemetery':
                    bit_sim1[key] = a_1*mass/a_0
            require(tv(bit_sim1,full1) <= a_1, 'bit simulation kernel')
            accepted0 = {k:p0*(1-p0)**(k-1) for k in range(1,b+1)}
            accepted1 = {k:p1*(1-p1)**(k-1) for k in range(1,b+1)}
            selected = [k for k in range(1,b+1) if accepted0[k] >= accepted1[k]]
            K = max(selected)
            require(selected == list(range(1,K+1)), 'monotone crossing')
            formula = ((1-p0)**K+1-(1-p1)**K)/2
            require(formula == (1-count_tv)/2, 'exact count Bayes risk')
            require(abs(count_risk(float(p0),float(p1),b)-float(formula)) < 1e-13,
                    'logarithmic crossing formula')
            for p in [p0,p1]:
                charge = sum(k*p*(1-p)**(k-1) for k in range(1,b+1))+b*(1-p)**b
                require(charge == (1-(1-p)**b)/p, 'expected capped charge')
            cases += 1
    result['exact_capped_cases'] = cases
    affinity_cases = 0
    for e in [0.01,0.07,0.2]:
        p, q = (0.5,0.5),(0.5+e,0.5-e)
        h2 = sum((sqrt(x)-sqrt(y))**2 for x,y in zip(p,q))
        for n in [1,2,5,8]:
            pp=[];qq=[]
            for bits in product(range(2), repeat=n):
                x=y=1.0
                for bit in bits: x*=p[bit];y*=q[bit]
                pp.append(x);qq.append(y)
            hn2=sum((sqrt(x)-sqrt(y))**2 for x,y in zip(pp,qq))
            vn=sum(abs(x-y) for x,y in zip(pp,qq))/2
            require(abs(hn2-2*(1-(1-h2/2)**n)) < 1e-13, 'affinity identity')
            require(hn2 <= n*h2+1e-13 and vn <= sqrt(hn2)+1e-13, 'tensor bounds')
            affinity_cases += 1
    result['affinity_cases'] = affinity_cases
    limits=[]
    for lam in [1,3]:
        target=exp(-lam)/2
        for M in [100,1000,10000]:
            risk=count_risk(1/M,1/(M*M),lam*M)
            limits.append({'lambda':lam,'M':M,'count_risk':risk,'limit':target})
        require(abs(limits[-1]['count_risk']-target) < 0.0002,'finite cap limit')
    result['finite_cap_examples'] = limits
    M=1000;p0=1/M;p1=1/(M*M);b=M**3
    bit_risk=(exp(b*log1p(-p0))-expm1(b*log1p(-p1)))/2
    full_count_risk=count_risk(p0,p1,b)
    require(bit_risk > 0.49 and full_count_risk < 0.01, 'huge cap negative control')
    result['huge_cap_negative_control'] = {'p0':p0,'p1':p1,'cap':b,
        'any_acceptance_bit_risk':bit_risk,'count_risk':full_count_risk}
    result['status']='passed'
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
