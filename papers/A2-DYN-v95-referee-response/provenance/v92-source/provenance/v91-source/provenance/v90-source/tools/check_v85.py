#!/usr/bin/env python3
"""Finite regression fixtures for v85, never a continuum proof certificate."""
from fractions import Fraction as F
import itertools
import json
import math
from check_v77 import require


def kernel(t, a, b, r):
    return max(F(0), 1-(b-t)/r) if a<t<b else F(0)


def integral_kernel(lo, hi, a, b, r):
    lo=max(lo,a,b-r);hi=min(hi,b)
    if hi<=lo:return F(0)
    return (1-b/r)*(hi-lo)+(hi*hi-lo*lo)/(2*r)


def checks():
    counts={k:0 for k in ['band_persistence','complete_band_cover','residence_tail',
                          'cutoff_constants','critical_exponents','logarithmic_sum',
                          'physical_trace','radial_interpolation','borel_slice_fixture',
                          'order_of_limits_regression']}
    for s in [F(1,128),F(1,16),F(1),F(3,2)]:
        for a in [F(-2),F(0),F(7,3)]:
            for length in [s*(1+F(i,16)) for i in range(1,17)]:
                b=a+length
                for frac in [F(i,16) for i in range(-2,19)]:
                    t=a+frac*length
                    lhs=F(int(a<t<b))
                    rhs=2/s*integral_kernel(t-2*s,t+2*s,a,b,4*s)
                    require(lhs<=rhs,'complete band persistence, including edge roofs')
                    counts['band_persistence']+=1
    for N in range(1,13):
        r=F(1,4);delta=r/(2**N)
        for length in [delta/2,delta,3*delta/2,r,2*r,3*r]:
            bands=sum(int(r/(2**j)<length<=2*r/(2**j)) for j in range(N+1))
            require(bands==int(delta<length<=2*r),'disjoint finite band covering')
            counts['complete_band_cover']+=1
    for r in [F(1,16),F(1,4),F(2)]:
        for ratio in [F(1,16),F(1,4),F(3,4)]:
            delta=r*ratio
            for length in [delta/4,delta/2,delta]:
                for t in [length*F(i,9) for i in range(1,9)]:
                    k=kernel(t,F(0),length,r)
                    require(1-delta/r<=k<=1,'complete zero-residence trace comparison')
                    require(F(1)<=2*kernel(t,F(0),length,2*delta),'fixed-count local finiteness comparison')
                    counts['residence_tail']+=2
    alpha=F(129,128)
    require(1+1/(alpha-1)==129,'explicit lower-cutoff independent leading coefficient')
    counts['cutoff_constants']+=1
    for a,b in [(F(1,1024),F(1,16)),(F(1,64),F(1,4)),(F(1,4),F(1))]:
        x=1/math.sqrt(float(a));y=1/math.sqrt(float(b))
        require(0<2*x-y<=2*x,'explicit cutoff dependent remainder')
        counts['cutoff_constants']+=1
    for eta in [F(1,8),F(1,4),F(3,8)]:
        k=(1-eta)/2
        require(alpha/2==F(129,256),'critical band height exponent')
        require((1+eta)/2+(alpha-eta)/2==F(257,256),'critical band drift exponent')
        require(F(1,32)<alpha/2 and k<F(1,2),'summable positive-scale exponents')
        counts['critical_exponents']+=3
    q=2**(-1/32)
    for r in [2.**(-j) for j in [2,8,32,64,128]]:
        R=r**(1/32)
        for T in [r**float(alpha/2), R/3,2*R]:
            actual=sum(min(R*q**j,T) for j in range(2048))
            if T>=R:bound=R/(1-q)
            else:bound=T*(1+math.log(R/T)/(-math.log(q)))+T/(1-q)
            require(actual<=bound*(1+1e-12),'numeric logarithmic-head/geometric-tail bound')
            counts['logarithmic_sum']+=1
    for a0,slope,length in itertools.product([F(1),F(2),F(5)],
                                            [F(-1,4),F(0),F(1,3)],
                                            [F(1,16),F(1,4),F(1)]):
        for t in [length*F(i,8) for i in range(1,8)]:
            initial=a0+slope*t;out=a0+slope*length
            require(initial>0 and out>0,'positive physical-density fixture')
            require(abs(out-initial)<=abs(slope)*(length-t),'trace-to-volume variation fixture')
            counts['physical_trace']+=2
    for eta,s,z in itertools.product([.125,.25,.375],[.0001,.01,1.],[.5,1.,2.,8.]):
        lam=.2
        if z*z<2*lam*s:continue
        require(1/z<=(2*lam*s)**(-(1-eta)/2)*z**(-eta)*(1+1e-12),'radial fractional interpolation')
        counts['radial_interpolation']+=1
    rationals=[F(0),F(1),F(-1),F(1,2),F(-1,2),F(2),F(-2),F(1,4),F(-1,4)]
    segments=[('word-a',F(-1),F(1)),('word-b',F(0),F(2)),('word-c',F(-1,2),F(1,2)),
              ('word-d',F(1,4),F(3,4))]
    image={}
    for word,a,b in segments:
        i=next(i for i,q in enumerate(rationals) if a<q<b)
        require(not any(a<q<b for q in rationals[:i]),'first-rational representative')
        counts['borel_slice_fixture']+=1
        for theta in [F(0),F(1,3)]:
            for u in [a+(b-a)*F(i,8) for i in range(1,8)]:
                state=(word,theta,u)
                require(state not in image,'physical sheets disjoint even at equal angle')
                image[state]=(word,theta,rationals[i],u)
                require(image[state][-1]==u,'inverse roof coordinate')
                counts['borel_slice_fixture']+=2
    # A shrinking residence family validates the prohibition on exchanging limits.
    # It is not asserted to be a Lorentz family or a counterexample to the target.
    for N in range(2,12):
        delta=F(1,2**N);m=N+10;length=F(1,2**m)
        require(length<delta and int(length>=delta)==0,'fixed-cutoff family eventually absent')
        require(kernel(length/2,F(0),length,F(1))>F(3,4),'untruncated height need not vanish from cutoff estimates alone')
        counts['order_of_limits_regression']+=2
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite exact kernel, cutoff, disintegration-model and summation regressions only',
            'independent_human_review':False,'formal_proof_certificate':False,
            'full_raw_return_LLT_proved':False,'zero_residence_surface_charge_zero_proved':False}


if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
