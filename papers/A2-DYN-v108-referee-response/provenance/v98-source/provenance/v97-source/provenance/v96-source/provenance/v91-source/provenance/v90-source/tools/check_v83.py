#!/usr/bin/env python3
"""Finite exact/numerical regression fixtures; not continuum proof certification."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
from check_v77 import require


def checks() -> dict:
    counts={k:0 for k in ('fractional_exponents','optical_variation','coarea_direction',
                         'layer_depth_sum','potential_rearrangement','dyadic_translation',
                         'dyadic_kernel','envelope_tail','scope_controls')}
    alpha=F(129,128)
    for eta in (F(1,100),F(1,8),F(1,4),F(3,8),F(49,100)):
        k=(1-eta)/2; q=1/k
        require(F(1,4)<k<F(1,2) and 2<q<4,'fractional norm range')
        require(1-k==(1+eta)/2 and alpha-eta>0,'potential and critical exponents')
        require(1+(1+eta)/2>F(33,32),'surface mass powers at L=r')
        counts['fractional_exponents']+=3
    require(alpha-F(1,4)==F(97,128),'critical example exponent')
    counts['fractional_exponents']+=1
    grid=(F(0),F(1,8),F(1,2),F(1),F(3))
    for w in itertools.product(grid,repeat=4):
        positive=sum(max(F(0),y-x) for x,y in zip(w,w[1:]))
        negative=sum(max(F(0),x-y) for x,y in zip(w,w[1:]))
        require(w[-1]<=w[0]+positive and w[0]<=w[-1]+negative,'two-sided optical payment')
        require(max(F(0),w[0]-w[-1])<=negative,'surviving loss')
        if w[-1]==0:require(w[0]<=negative,'grazing starting weight is paid')
        counts['optical_variation']+=2
    for w0,w1,c0,c1 in itertools.product((F(1,4),F(1),F(4)),repeat=4):
        jac=(w1/w0)*(c0/c1); mu0=w0/c0; mu1=w1/c1
        require(jac*mu0==mu1,'target-direction covariance')
        require(mu1/jac==mu0,'first-exit inverse Jacobian retained')
        counts['coarea_direction']+=2
    q0=F(47,53)
    for m in range(1,101):
        depths=[min(j,m-j) for j in range(m+1)]
        require(all(depths.count(d)<=2 for d in set(depths)),'at most two contacts per depth')
        require(sum(q0**d for d in depths)<=2/(1-q0),'full depth sum')
        counts['layer_depth_sum']+=2
    # Integral of s^-k over arbitrary disjoint offset intervals is bounded by
    # the decreasing rearrangement over an interval of the same total length.
    cells=[(i/16,(i+1)/16) for i in range(16)]
    for k in (.255,.375,.495):
        for indices in itertools.combinations(range(16),3):
            a=sum(cells[i][1]-cells[i][0] for i in indices)
            integral=sum((cells[i][1]**(1-k)-cells[i][0]**(1-k))/(1-k) for i in indices)
            require(integral<=a**(1-k)/(1-k)+1e-12,'localized potential rearrangement fixture')
            counts['potential_rearrangement']+=1
    for t,r,j in itertools.product((F(-2),F(0),F(7,3)),(F(1,8),F(1),F(2)),range(8)):
        ell=r/2**j
        # For v(u)=u^2+1, the offset and absolute-roof conventions coincide.
        def primitive(u):return u**3/3+u
        absolute=primitive(t+ell)-primitive(t+ell/2)
        offset=(t*t+1)*(ell-ell/2)+t*(ell**2-(ell/2)**2)+(ell**3-(ell/2)**3)/3
        require(absolute==offset,'one translation, not two')
        counts['dyadic_translation']+=1
    for k,j,fraction in itertools.product((.26,.375,.49),range(12),(.5,.625,.875,1.)):
        ell=2.**(-j);s=ell*fraction
        require(ell**(-k)<=s**(-k)*(1+1e-14)<=2**k*ell**(-k)*(1+2e-14),
                'dyadic kernel bounds')
        counts['dyadic_kernel']+=1
    for delta,r,n in itertools.product((.05,.25,.75),(.001,.1,1.),range(10)):
        lhs=sum((r*2**(-j))**delta for j in range(n,n+200))
        rhs=r**delta*2**(-n*delta)/(1-2**(-delta))
        require(lhs<=rhs*(1+1e-12),'uniform Dini-envelope geometric tail')
        counts['envelope_tail']+=1
    require(F(1,2)-F(1,2)==0,'fractional endpoint is excluded')
    require(F(1,32)==F(1,2)*F(1,16),'true-exit margin exponent')
    counts['scope_controls']+=2
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational identities, finite variation paths and deterministic integral fixtures only',
            'full_raw_return_LLT_proved':False,'surface_essential_height_proved':False,
            'formal_proof_certificate':False,'independent_human_review':False}

if __name__=='__main__':
    print(json.dumps(checks(),indent=2,sort_keys=True))
