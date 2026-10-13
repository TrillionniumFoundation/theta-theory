#!/usr/bin/env python3
"""Finite algebraic, cap, segment and local-norm regressions; not proof certification."""
from __future__ import annotations
import itertools,json,math,random
from fractions import Fraction as F
from scipy.integrate import quad
from check_v77 import require

def checks() -> dict:
    counts=dict(physical_depth=0,positive_cap=0,residence_layer_cake=0,
                pulse_overlap=0,full_segment_trace=0,radial_payment=0,
                norm_exponents=0,endpoint_order=0)
    q0=F(47,53)
    for n,s in itertools.product((2,3,8,29,100),(F(1,10),F(1,100),F(1,10000))):
        contact=sum(q0**min(i,n-i) for i in range(n+1))
        flight=sum(q0**min(i,n-1-i) for i in range(n))
        require(contact<=2/(1-q0) and flight<=2/(1-q0),'complete depth cap')
        require(contact*s+flight*s<=4*s/(1-q0),'no collision-count union factor')
        counts['physical_depth']+=2
    # The cap is on the full positive source, not on the spectral remainder.
    vals=[F(0),F(1,100),F(1,2),F(1),F(4)]
    for A,D,V in itertools.product(vals,repeat=3):
        x=min(A+D,V)
        require(x<=A+min(D,V),'positive cap must precede negative moment')
        counts['positive_cap']+=1
    for theta,D,s in itertools.product((.001,1/64,1/40,.031),(.0001,.04,.4,1.),(.00001,.01,.3,.8)):
        # Evaluate the two elementary antiderivatives independently.
        cut=min(s,D*D)
        integral=cut**(.5-theta)/(.5-theta)
        if s>cut:integral+=D*(cut**(-theta)-s**(-theta))/theta
        lhs=s**(-theta)*min(D,math.sqrt(s))+theta*integral
        rhs=min(s**(.5-theta),D**(1-2*theta))/(1-2*theta)
        require(math.isclose(lhs,rhs,rel_tol=2e-11,abs_tol=1e-12),'capped residence integral')
        require(F(1,32)-F(str(theta))>0,'leading residence integral converges')
        counts['residence_layer_cake']+=2
    rng=random.Random(880206)
    # Arbitrary overlapping interval pulses and arbitrary finite measurable test sets.
    for theta,n in itertools.product((1/64,1/40,.03),(1,3,10,40)):
        for _ in range(30):
            intervals=[]
            for i in range(n):
                a=rng.uniform(-1,1);ell=10**rng.uniform(-4,-.1)
                intervals.append((a,a+ell,10**rng.uniform(-3,2)))
            cells=[j for j in range(100) if rng.random()<.23]
            E=[(-1+2*j/100,-1+2*(j+1)/100) for j in cells]
            measure=sum(b-a for a,b in E)
            if not measure:continue
            lhs=sum(T*sum(max(0.,min(b,y)-max(a,x)) for x,y in E) for a,b,T in intervals)/measure**theta
            rhs=sum(T*(b-a)**(1-theta) for a,b,T in intervals if b>-1 and a<1)
            require(lhs<=rhs*(1+1e-11),'overlapping complete pulse trace')
            counts['pulse_overlap']+=1
    # Full angular-density trace, including z(a)=0, without a first inverse-gradient moment.
    eta=.25;kappa=(1-eta)/2
    for theta,ell,z0,k in itertools.product((1/64,1/40),(.01,.2,1.),(0.,.001,.2),(-3.,0.,.7,3.)):
        density=lambda u:math.exp(k*u)
        z=lambda u:math.sqrt(z0*z0+u)
        energy=lambda u:density(u)*max(1.,abs(k)*z(u))*z(u)**(-eta)
        mass=quad(density,0,ell,epsabs=1e-10)[0]
        vmass=quad(energy,0,ell,epsabs=1e-10)[0]
        lhs=density(ell)*ell**(1-theta)
        rhs=ell**(-theta)*mass+ell**(1-kappa-theta)*vmass
        require(lhs<=rhs*(1+1e-9),'whole segment weighted optical payment')
        counts['full_segment_trace']+=1
        for fraction in (.001,.1,.5,.99):
            u=ell*fraction
            require(u/z(u)<=ell**(1-kappa)*z(u)**(-eta)*(1+1e-12),'radial triangle factor')
            counts['radial_payment']+=1
    a=F(1,32)
    for theta in (F(1,128),F(1,64),F(1,40),F(3,100)):
        q=1/(1-theta);nu=a-theta
        require(1<q<F(32,31) and nu>0,'weak exponent interval')
        require(F(1)-F(3,8)-theta>nu,'potential exponent is higher order')
        require(1/q-F(31,32)==nu,'surface decay exponent')
        counts['norm_exponents']+=3
    require(1/(1-F(1,64))==F(64,63),'explicit weak norm')
    require(a-F(1,64)==F(1,64),'explicit surface decay')
    counts['norm_exponents']+=2
    # Finite-norm convergence must not be promoted to height convergence.
    for q in (1.01,64/63,1.03):
        for n in (10,100,1000):
            width=n**(-2*q);height=float(n)
            weak=height*width**(1/q)
            require(math.isclose(weak,1/n,rel_tol=1e-12),'spike counterfixture')
            require(height>1 and weak<1,'finite norm leaves height unresolved')
            counts['endpoint_order']+=2
    require(F(1,12)*F(1,16)==F(1,192),'scalar reconstruction exponent')
    counts['endpoint_order']+=1
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite cap identities, complete-overlap pulses, seeded segment traces and exponent regressions only',
            'full_raw_return_LLT_proved':False,'formal_proof_certificate':False,
            'independent_human_review':False}
if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
