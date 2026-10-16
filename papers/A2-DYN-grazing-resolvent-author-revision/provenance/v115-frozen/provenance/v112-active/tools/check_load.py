#!/usr/bin/env python3
"""Exact finite checks of v112 algebra; no continuum or physical LLT certification."""
from fractions import Fraction as F
from itertools import combinations, product
from math import prod, log, sqrt, ceil
import json


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def elementary(values):
    out = [F(1)]
    for x in values:
        out.append(F(0))
        for i in range(len(out)-1, 0, -1):
            out[i] += x*out[i-1]
    return out


def run():
    counts = dict(depth_coefficients=0, balanced_depth_minima=0,
                  exact_fractional_load_products=0, exact_chernoff_optimizers=0,
                  positive_source_identities=0, threshold_boundary_cases=0,
                  negative_controls=0, asymptotic_classifications=0)
    for r in (F(1,4), F(1,2), F(3,4), F(47,53)):
        for m in range(1,15):
            depths = [min(i,m-i) for i in range(1,m)]
            es = elementary([r**d for d in depths])
            for s in range(m):
                f = (s+1)**2//4
                poch = lambda n: prod((1-r**j for j in range(1,n+1)), start=F(1))
                convolution = sum((r**(a*(a+1)//2+(s-a)*(s-a+1)//2)
                                   / (poch(a)*poch(s-a)) for a in range(s+1)), F(0))
                finite_upper = F(s+1)*r**f/poch(s)**2
                require(r**f <= es[s] <= convolution <= finite_upper,
                        ('depth coefficient',r,m,s))
                counts['depth_coefficients'] += 1
                if m <= 9:
                    sums = [sum(depths[i] for i in S)
                            for S in combinations(range(m-1),s)]
                    require(min(sums) == f, ('balanced minimum',m,s))
                    require(es[s] == sum((r**d for d in sums),F(0)), 'direct enumeration')
                    counts['balanced_depth_minima'] += 1
    # Fractional exponents are exact: r=t^b and y_i=t^{-b(d_i+h_i)}.
    for t in (F(1,2),F(2,3)):
        for a,b in ((1,2),(1,3),(2,3)):
            r=t**b
            for eps in (F(1,10),F(1,2)):
                for m in range(1,7):
                    depths=[min(i,m-i) for i in range(1,m)]
                    for hs in product((-1,0,1,3),repeat=m-1):
                        left=F(1); rhs_factors=[]; load_depth=0
                        for d,h in zip(depths,hs):
                            y=t**(-b*(d+h)); c=2*eps/y; threshold=2*eps*r**d
                            witness=c<threshold
                            require(witness == (h>0),'strict incidence witness')
                            require(0<c<=1,'synthetic incidence outside physical range')
                            if h==0:
                                require(c==threshold and not witness,'equality is not a witness')
                                counts['threshold_boundary_cases']+=1
                            if witness:
                                left*=t**(-a*(d+h))
                                load_depth+=d
                            ai=2*eps*t**((b-a)*d)
                            rhs_factors.append(ai/c)
                        rhs=prod((1+x for x in rhs_factors),start=F(1))
                        require(left<=rhs,'fractional exponential product domination')
                        require(rhs==sum(elementary(rhs_factors),F(0)),'finite positive expansion')
                        counts['exact_fractional_load_products']+=1
    for b0 in (F(1,100),F(1),F(100)):
        for v in (F(1,10),F(1,3),F(1,2),F(3,4),F(9,10)):
            u=b0/v**2
            require(u>b0 and 0<v<1,'optimizer domain')
            require(-u+v*u+b0/v == -u+2*b0/v,'exact optimizer value')
            for w in (F(1,20),F(1,4),F(2,3),F(19,20)):
                require(w*u+b0/w >= 2*b0/v,'AM-GM optimization')
            counts['exact_chernoff_optimizers']+=1
    for exc,load,low,capacity in product((F(0),F(1,4),F(1),F(7,3)),repeat=4):
        original=exc+load+low
        loc=load+low
        rloc=max(F(0),loc-capacity); rlow=max(F(0),low-capacity)
        require(original==exc+loc and loc==load+low,'exact source preservation')
        require(0<=rloc-rlow<=load,'same-capacity residual comparison')
        counts['positive_source_identities']+=1
    # Omitting one collision-end copy is not a valid coefficient majorant.
    r=F(1,4)
    require(2*r > r/(1-r),'negative control must detect missing second end')
    counts['negative_controls']+=1
    # A bound carrying the count exponent twice would fail even at m=2,s=1.
    require(r > r**2,'negative control must detect spurious doubled depth exponent')
    counts['negative_controls']+=1
    # Classification only: these are not claimed to be realized billiard orbits.
    alpha=abs(log(47/53))/4
    for ell in (1e6,1e8,1e10):
        u=3*ell
        s=ceil(2*sqrt(u/alpha))
        old_count=4*ell/log(ell)
        old_max_depth=3*ell/alpha
        require(s<old_count and ceil(s/2)<old_max_depth,'asymptotic strengthening')
        require(alpha*((s+1)**2//4)>=u,'new joint-load classification')
        counts['asymptotic_classifications']+=1
    return dict(status='passed',revision=112,**counts,
                total_checked=sum(counts.values()),
                arithmetic='Fraction for all finite algebra; floats only for stated asymptotic illustrations',
                scope='finite algebra and classification diagnostics, not physical realizability, pressure proof, or LLT certification',
                formal_proof_certificate=False,full_raw_return_LLT_proved=False)


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
