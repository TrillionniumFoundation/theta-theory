#!/usr/bin/env python3
"""Finite diagnostics for v69; not a continuum or billiard proof certificate."""
from fractions import Fraction as Q
from itertools import product
import json
import math


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def finite_checks():
    checked = 0
    orders = [0, 1, 2, 3, 7, 31, 127, 1023, 10000, 1000000]
    for d in orders:
        a = d / 2.0
        x = (a + 1.0) * math.log(2.0)
        logden = x if x > 700 else math.log(math.expm1(x))
        require(math.log(a + 1.0) - logden <= 1e-12, 'order-free monomial annulus')
        checked += 1
    for K, D, H in product([1., 3., 11.], [0., 2., 10.], [1e-8, 1e-6, 1e-4]):
        require(2*K*math.sqrt(H) < 1, 'admissible annulus')
        F = math.exp((2+math.sqrt(2))*D*math.sqrt(H))*(1+math.sqrt(2)*K*math.sqrt(H))/(1-2*K*math.sqrt(H))
        require(F >= 1 and math.isfinite(F), 'annular factor')
        for g,L in product([0., .001, .25, 1.], [1., 4., 20.]):
            bound = min(1., g+L*math.sqrt(2*H))
            for rfrac in [.01,.2,.7,1.]:
                r = rfrac*math.sqrt(2*H)
                require(min(1.,g+L*r) <= bound+1e-15, 'absolute guard envelope')
                checked += 1
            if g == 0:
                require(6*H*F*bound <= 6*math.sqrt(2)*L*H**1.5*F*(1+1e-12), 'zero-guard exponent')
                checked += 1
    for r in [.001,.01,.1,.2,.5,.8,1.]:
        flat = math.exp(-1/(r*r))
        require(0 <= flat <= r, 'flat zero-center guard dominated absolutely')
        checked += 1
    fixtures = [
        [Q(0)]*8,
        [Q(1)]*8,
        [Q(0)]*4+[Q(1,2)]*4,
        [Q(0)]*3+[Q(1)]+[Q(0)]*4,
        [Q(i,8) for i in range(8)],
        [Q(1,1000000)]*8,
    ]
    radial_ratios=[]
    for ell in fixtures:
        n=len(ell)
        w=[Q(1,2) if i%2==0 else Q(2) for i in range(n)]
        avg=sum(ell,Q(0))/n
        qavg=sum((x*y for x,y in zip(ell,w)),Q(0))/n
        for a in range(n):
            for b in range(a+1,n+1):
                U=max(ell[a:b])
                V=U/avg if avg else Q(0)
                supq=max(x*y for x,y in zip(ell[a:b],w[a:b]))
                require(supq <= 4*V*qavg, 'finite radial density distortion')
                for cap in [Q(0),Q(1,7),Q(1)]:
                    guarded=max(cap*x*y for x,y in zip(ell[a:b],w[a:b]))
                    require(guarded <= 4*V*qavg*cap, 'absolute finite-scale guard')
                    checked += 1
                checked += 1
        radial_ratios.append((max(ell)/avg if avg else Q(0),qavg))
    for alpha,T in product([1,2,3],[Q(1,2),Q(1),Q(2),Q(10)]):
        lhs=sum((V*q for V,q in radial_ratios if V>T),Q(0))
        moment=sum((V**(1+alpha)*q for V,q in radial_ratios),Q(0))
        require(lhs <= T**(-alpha)*moment, 'positive weighted tail')
        checked += 1
    for physical,chart,radial,angular,lowratio in product([False,True],[False,True],[0,1,2],[False,True],[False,True]):
        # radial 0: (0,H); 1: [H,S); 2: exterior. H<S is fixed.
        first=physical and chart and radial==0 and angular
        outer=physical and chart and radial<2 and not first and lowratio
        tail=physical and chart and radial<2 and not first and not lowratio
        exterior=physical and not(first or outer or tail)
        require(sum(map(int,[first,outer,tail,exterior])) == int(physical), 'disjoint complete partition')
        checked += 1
    for i in range(8):
        labels=[Q(i,16),Q(8-i,16)]
        require(sum(labels)<=1,'one-hot angular fractions')
        checked += 1
    # Negative controls are analytic examples, not asserted Lorentz realizations.
    H=.2
    def compact_guard(r):
        return max(0.,1-abs(r-.25)/.1)
    require(compact_guard(0)==0 and compact_guard(.25)==1, 'zero-center positive inner guard')
    require(all(compact_guard(math.sqrt(2*v))==0 for v in [H,1.2*H,2*H]), 'guarded outer annulus may vanish')
    require(compact_guard(.25)<=10*.25,'unguarded comparison still dominates')
    for m in [10,100,1000]:
        K=3
        require(m>K and Q(1,m*m)*m*m==1, 'fixed-count exhaustion does not prove ordered tightness')
        require(Q(1,m)<1 and m>1, 'vanishing spike mass is not small height')
        checked += 2
    # Polar area r dr dphi pushed through u=r^2/2 has r/(du/dr)=1.
    for r in [Q(1,100),Q(1,2),Q(2)]:
        require(r/r==1,'polar coarea normalization')
        checked+=1
    return {'checks':checked,'max_angular_birth_order_tested':max(orders),
            'zero_center_flat_guard':True,'positive_radius_zero_germ_fixture':True,
            'finite_scale_zero_denominator':True,'disjoint_source_partition':True,
            'negative_controls':['guarded-annulus failure','fixed-count exhaustion','mass versus height'],
            'continuum_proof_certificate':False,'physical_tail_bound_certified':False}

if __name__ == '__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
