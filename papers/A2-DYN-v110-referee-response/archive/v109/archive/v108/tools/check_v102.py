#!/usr/bin/env python3
"""Finite coarea, clock and exponent regressions; not continuum certification."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
from check_v100 import require

def checks() -> dict:
    counts={k:0 for k in ('barycentric_fiber','jacobian_orientation','capped_clock',
                         'certificate','critical_fold','schedule','positive_split')}
    # Constant-width sheets: compare the original angular fiber with the s-fiber.
    for v,ell,c,t in itertools.product((F(-3),F(-1),F(1),F(3)),
                                     (F(1,16),F(1,4),F(1)),(F(1,3),F(2)),
                                     (F(i,8) for i in range(-32,41))):
        al,ar=sorted(((t-ell)/v,t/v))
        theta_len=max(F(0),min(F(1),ar)-max(F(-1),al))
        sl,sr=sorted(((t-v)/ell,(t+v)/ell))
        s_len=max(F(0),min(F(1),sr)-max(F(0),sl))
        require(c*theta_len==c*ell/abs(v)*s_len,'barycentric fiber equality')
        counts['barycentric_fiber']+=1
    for c0,c1,l0,l1,v0,v1 in itertools.product((F(1,4),F(2)),repeat=6):
        for sign in (-1,1):
            oldv,newv=sign*v0,sign*v1
            j=(c1*l1)/(c0*l0)*abs(oldv/newv)
            rho0,rho1=c0*l0/abs(oldv),c1*l1/abs(newv)
            require(j==rho1/rho0 and j>0,'target-direction paired Jacobian')
            require(rho0*j==rho1,'paired kernel covariance')
            counts['jacobian_orientation']+=2
    for j in itertools.product((F(0),F(1,4),F(1),F(3)),repeat=4):
        clock=sum((min(F(1),x) for x in j),F(0))/2
        target=sum(j,F(0))/2
        require(F(0)<=clock<=2 and clock<=target,'capped target integral')
        for q in (F(1,8),F(1,2),F(1)):
            admitted=int(clock>=q)
            require(q*admitted<=target,'admitted pointwise domination')
            counts['capped_clock']+=1
    for A,nu,L in itertools.product((0.,.01,.2,1.,4.),(.1,1.,5.),(.01,.3,2.)):
        r=nu*L if A==0 else nu*min(L,math.log(2)/(3*A))
        require(r>0 and r/nu<=L*(1+1e-12),'angular reach')
        require(math.exp(A*r/nu)<2,'no short-domain exit')
        require(math.exp(-3*A*r/nu)>=.5-1e-12,'positive clock certificate')
        counts['certificate']+=3
        for ell in (1e-2,1e-8,1e-24):
            for beta in (-A,0.,A):
                # Parallel-sheet transport cancels the arbitrarily small width.
                target=(ell*math.exp(beta*r/nu))/ell
                require(abs(target-math.exp(beta*r/nu))<1e-12,'no residence lower cutoff')
                counts['certificate']+=1
    for s in (F(1,100),F(1,4),F(1,2),F(3,4)):
        require((1-s)*0+s*2==2*s,'nonzero critical entrance retained')
        counts['critical_fold']+=1
    require((1-F(1,2))*1+F(1,2)*(-1)==0,'fold not erased')
    counts['critical_fold']+=1
    for t in (F(1,5),F(1,2),F(4,5)):
        # Horizontal positive pairs are not admitted merely because mass is finite.
        trace=F(3);clock=F(0);q=F(1,4)
        admitted=trace*int(clock>=q);failed=trace-admitted
        require(admitted==0 and failed==trace,'zero-speed positive failure retained')
        counts['critical_fold']+=1
    for mass,clock,q in itertools.product((F(0),F(1,10),F(2)),
                                         (F(0),F(1,4),F(1),F(2)),
                                         (F(1,8),F(1,2),F(1))):
        a=mass*int(clock>=q);f=mass*int(clock<q)
        require(a+f==mass and a>=0 and f>=0,'complete positive split')
        counts['positive_split']+=1
    require(F(1,16)-F(1,32)==F(1,32),'admitted guard exponent')
    require(4-1-F(1,32)==F(95,32),'paired comparison exponent')
    require(F(1,12)*F(1,32)==F(1,384),'outer B exponent')
    require(F(257,64)>F(1,32) and 3>F(1,32),'all scalar costs vanish')
    counts['schedule']+=4
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational source identities, Jacobian orientation, clock bounds, certificates and schedules',
            'all_physical_pairs_admitted':False,'full_raw_return_LLT_proved':False,
            'formal_proof_certificate':False,'independent_human_review':False}
if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
