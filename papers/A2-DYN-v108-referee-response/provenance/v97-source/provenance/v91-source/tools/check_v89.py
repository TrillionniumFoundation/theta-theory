#!/usr/bin/env python3
"""Finite regression checks for critical dyadic sums; not a proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
from check_v77 import require


def checks() -> dict:
    count=dict(exponents=0,dyadic_pulses=0,capped_remainders=0,
               trace_triangle=0,log_interpolation=0,gluing=0,scale_factors=0)
    g=F(1,32);Q=1/(1-g);k=F(3,8);d=1-k
    require(Q==F(32,31) and d-g==F(19,32),'critical exponent')
    require((1-2*g)/2==F(15,32),'capped collision exponent')
    require(F(129,128)/8>F(1,128) and F(1,4)*g==F(1,128),'residual union powers')
    count['exponents']+=3
    for th in (F(1,32),F(1,4),F(1,2),F(5,8)):
        t=float(th);C=2/(1-2**(-(1-t)))+1/(1-2**(-t))
        for s,v in itertools.product((2.**-1,2.**-5,2.**-12),(2.**-18,2.**-7,.03,.7,2.)):
            actual=sum(min(1.,2*v/(s*2**-j))*(s*2**-j)**t for j in range(500))
            # The omitted tail is nonnegative and bounded by the full geometric tail.
            tail=s**t*2**(-500*t)/(1-2**-t)
            require(actual+tail<=C*min(v**t,s**t)*(1+1e-12),'complete pulse fixture')
            count['dyadic_pulses']+=1
    for D,x in itertools.product((F(1),F(1,4),F(1,256),F(1,65536)),
                                  (F(1),F(1,2),F(1,32),F(1,1000000))):
        actual=min(float(D),float(x)**.5)
        bound=float(D)**float(1-2*g)*float(x)**float(g)
        require(actual<=bound*(1+1e-12),'physical cap interpolation')
        count['capped_remainders']+=1
    for ell in (.25,1.,3.):
        for slope in (-.8,0.,.8,3.):
            # Positive affine densities on a unit segment and their exact variation.
            base=2+abs(slope)*ell
            integral=base*ell+slope*ell**2/2
            triangular=abs(slope)*ell**2/2
            require((base+slope*ell)*ell<=integral+triangular+1e-12,'whole-segment trace triangle')
            count['trace_triangle']+=1
    # Test the logarithmic interpolation on weighted interval pulses.
    for length,height,width,sigma in itertools.product((1.,3.),(.1,2.,20.),
                     (1e-7,.001,.1),(0.1,.5,2.)):
        width=min(width,length)
        A=height*width**float(1-g)
        mass=height*width;ratio=mass/(A*length**float(g))
        upper=A*(math.sqrt(ratio)+(1+math.log(1/ratio)/float(2*g))**(-sigma))
        grid=[length*math.exp(-i/4) for i in range(401)]+[width]
        actual=max(height*min(v,width)*v**(-float(g))/(1+math.log(length/v))**sigma for v in grid)
        require(actual<=upper*(1+1e-11),'logarithmic mass interpolation')
        count['log_interpolation']+=1
    for N in range(1,13):
        for seed in range(10):
            vals=[((j+3)*(seed+7)%19+1)/23 for j in range(N)]
            lhs=sum(v**float(g) for v in vals)
            rhs=N**float(1-g)*sum(vals)**float(g)
            require(lhs<=rhs*(1+1e-12),'finite-partition weak norm gluing')
            count['gluing']+=1
    for m,p in itertools.product((2,9,100,10000),(F(1),F(65,64),F(33,32))):
        M=2.;N=math.ceil(2*M*math.sqrt(m))+1
        require(N/math.sqrt(m)<=2*M+2/math.sqrt(m)+1e-12,'diffusive interval count')
        factor=m**(-.5)*m**(float(g)/2)*N**float(1-g)
        require(abs(factor-(N/math.sqrt(m))**float(1-g))<1e-10,'critical scaling factor')
        count['scale_factors']+=2
    return {'counts':count,'total_checks':sum(count.values()),
            'scope':'finite rational exponents and numerical inequality fixtures only',
            'full_pointwise_LLT_proved':False,'formal_proof_certificate':False,
            'independent_human_review':False}

if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
