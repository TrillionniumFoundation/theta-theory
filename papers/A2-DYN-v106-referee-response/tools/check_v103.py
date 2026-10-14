#!/usr/bin/env python3
"""Finite algebraic fixtures for the endpoint-distance comparison; not proof certification."""
from fractions import Fraction as F
from itertools import product
import json
import math
from check_v100 import require


def relative_clock(theta, upper, speed, r):
    if speed==0:return F(0)
    speed=abs(speed)
    lo=max(F(0),theta-r/speed); hi=min(upper,theta+r/speed)
    mid=min(hi,theta)
    below=(mid*mid-lo*lo)/(2*theta) if lo<mid else F(0)
    above=max(F(0),hi-max(lo,theta))
    return speed*(below+above)/r


def checks():
    counts={'unit_roof_fields':0,'gap_invariance':0,'density_jacobian':0,
            'critical_corner_recovery':0,'opposite_slope_recovery':0,
            'clock_disjointization':0,'certificate_ratio':0,'schedule':0}
    vals=(F(-3),F(-1),F(1,2),F(2),F(4))
    positions=(F(1,1000),F(1,7),F(1,2),F(6,7),F(999,1000))
    for ap,bp,s in product(vals,vals,positions):
        lp=bp-ap;v=(1-s)*ap+s*bp
        require(v/ap-s*lp/ap==1,'incoming unit roof speed')
        require(v/bp+(1-s)*lp/bp==1,'outgoing unit roof speed')
        counts['unit_roof_fields']+=2
        ell=F(2);h=F(1,100)
        for side,ep in ((-1,ap),(1,bp)):
            dt=h/ep;newell=ell+lp*dt
            oldgap=s*ell if side==-1 else (1-s)*ell
            news=oldgap/newell if side==-1 else 1-oldgap/newell
            newgap=news*newell if side==-1 else (1-news)*newell
            require(newgap==oldgap,'endpoint gap not conserved')
            counts['gap_invariance']+=1
            c0=F(3);c1=F(4)
            jac=c1*newell/(c0*ell)*(ell/newell)
            require(jac==c1/c0,'affine physical density Jacobian')
            counts['density_jacobian']+=1
    # Nonlinear monotone endpoints: density ratio includes endpoint speeds.
    for theta,h in product((.1,.3,.8),(.001,.01,.07)):
        e0=theta+theta*theta
        th=(-1+math.sqrt(1+4*(e0+h)))/2
        ell0=.2+theta;ell1=.2+th
        c0=1+theta*theta;c1=1+th*th
        coordinate_jac=(1+2*theta)/(1+2*th)*ell0/ell1
        physical=c1*ell1/(c0*ell0)*coordinate_jac
        expected=(c1/(1+2*th))/(c0/(1+2*theta))
        require(abs(physical-expected)<1e-12,'nonlinear target/source ratio')
        counts['density_jacobian']+=1
    delta=F(1);q=F(1,8)
    for ell,s in product((F(1,100),F(1,4),F(1)),positions):
        # a is constant, b=theta: every relative position has gap reach r.
        theta=ell;r=delta;upper=4*delta
        clock=relative_clock(theta,upper,s,r)
        require(clock<=4*s,'critical relative-clock reach cap')
        require(theta+r<upper,'full gap reach at critical entrance')
        gap=(1-s)*ell
        require(0<gap<ell+r,'critical corner gap remains interior')
        if s<q/4:require(clock<q,'positive old-failure corner strip')
        counts['critical_corner_recovery']+=3+int(s<q/4)
    for ell,s in product((F(1,100),F(1,4),F(1)),
                         (F(49,100),F(1,2),F(51,100),F(1,7),F(6,7))):
        theta=ell/2;speed=2*s-1
        clock=relative_clock(theta,2*delta,speed,delta)
        require(clock<=2*abs(speed),'fold relative-clock reach cap')
        require(ell+2*delta<4*delta,'full expanding gap reach at fold')
        if abs(speed)<q/2:require(clock<q,'positive old-failure fold strip')
        counts['opposite_slope_recovery']+=2+int(abs(speed)<q/2)
    for km,kp,cut in product((F(0),F(1,4),F(1,2),F(1),F(2)),repeat=3):
        if cut<=0 or cut>1:continue
        gm=int(km>=cut);gp=int(km<cut and kp>=cut)
        require(gm+gp==int(max(km,kp)>=cut),'gap admissions not disjoint')
        require(cut*(gm+gp)<=gm*km+gp*kp,'clock lower bound')
        counts['clock_disjointization']+=2
    for cost in (0.,.1,.3,math.log(2)/2):
        ratio=math.exp(-2*cost)
        require(ratio>=.5-1e-15,'two-factor certificate bound')
        counts['certificate_ratio']+=1
    require(F(1,16)-F(1,32)==F(1,32),'recovered source exponent')
    require(F(4)-1-F(1,32)==F(95,32),'collar exponent')
    require(F(1,32)/12==F(1,384),'outer recovered rate')
    require(F(1,16)/12==F(1,192),'certified source rate')
    counts['schedule']+=4
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite algebra, model clocks and exponent bookkeeping only',
            'models_are_verified_physical_realizations':False,
            'full_raw_return_LLT_proved':False,'formal_proof_certificate':False,
            'independent_human_review':False}
if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
