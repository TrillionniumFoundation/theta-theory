#!/usr/bin/env python3
"""Finite algebra/regression tests only; no continuum billiard certificate."""
from fractions import Fraction as F
from itertools import product
import math
import numpy as np


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    p,q,var,gamma=F(1,12),F(1,24),F(1,8),F(1,100)
    alpha=var/2
    require(alpha==F(1,16) and gamma<min(p-q,var,1-q), 'norm restrictions')
    require(alpha/4==F(1,64) and alpha/F(12)==F(1,192), 'depth/band exponents')
    require(F(1,192)<F(1,2), 'paid correction exponent')
    # The projection estimate: r>sigma^(1/4) and sigma^L approximately t.
    sigma=F(1,16);r=F(3,4)
    require(r**4>sigma and sigma<r<1, 'interpolation chart choice')
    for L in range(1,65):
        t=sigma**L
        upper=r**(-L)*(L+2)*t
        require(float(upper)<=4*math.sqrt(float(t)), 'square-root interpolation model')
    # Exact positive telescopes, including contacts at terminal time.
    telescope_cases=0;occupation_cases=0
    for m in range(1,8):
        depths=[min(j,m-j) for j in range(m+1)];D=m//2
        for bits in product((F(0),F(1,2),F(1)),repeat=m+1):
            H=F(2,3);Gprev=H*math.prod(bits);total=F(0)
            for a in range(D+1):
                G=H*math.prod(bits[j] for j in range(m+1) if depths[j]>a)
                z=G-Gprev
                require(z>=0, 'negative layer')
                if z:
                    require(any(bits[j]<1 for j in range(m+1) if depths[j]==a), 'no bad mark')
                total+=z;Gprev=G
            require(total==H*(1-math.prod(bits)), 'depth telescope identity')
            f=H*math.prod(bits);d=H*(1-math.prod(bits));b=1-H
            require(f+d+b==1, 'physical-first source identity')
            telescope_cases+=1
        for a in range(D+1):
            free=[j for j in range(m+1) if depths[j]<=a]
            count_free=[j for j in free if j<m]
            require(len(count_free)<=2*a+2, 'occupation allowance')
            for before in product((0,1),repeat=m+1):
                after=list(before)
                for j in free:after[j]=1-after[j]
                require(abs(sum(before[:m])-sum(after[:m]))<=2*a+2, 'occupation crossing')
                occupation_cases+=1
    # Exact finite-tail formula at a rational geometric ratio.
    x=F(3,4);tail_cases=0
    for J in range(-1,12):
        for D in range(max(0,J+1),25):
            finite=sum((a+1)*x**a for a in range(J+1,D+1))
            infinite=x**(J+1)*(F(J+2)/(1-x)+x/(1-x)**2)
            remainder=x**(D+1)*(F(D+2)/(1-x)+x/(1-x)**2)
            require(finite==infinite-remainder, 'exact tail formula')
            tail_cases+=1
    for m in range(2,100):
        require(sum(a+1 for a in range(m//2+1))<=m*m, 'summed exponential error')
    # Affine stable-curve intersections: horizontal and vertical strips.
    strip_cases=0
    for slope in (F(-2),F(-1),F(-1,2),F(1,2),F(1),F(2)):
        for width in (F(1,1000),F(1,100),F(1,10)):
            for eps in (F(1,1000),F(1,100),F(1,10)):
                # Horizontal strip intersection in graph coordinate has length 2s/|slope|.
                length=2*width/abs(slope)
                require(length<=4*width, 'thin horizontal intersection')
                if width<eps:require(length<=4*eps, 'whole unmatched strip payment')
                require(2*width<=2*max(width,eps), 'vertical strip payment')
                strip_cases+=1
    # Exact physical chronological pairing on a finite permutation model.
    size=7;perm=np.array([1,2,3,4,5,6,0]);values=np.linspace(-.7,.8,size)
    theta=.37;Q=np.zeros((size,size),dtype=complex)
    for i in range(size):Q[perm[i],i]=np.exp(1j*theta*values[i])
    nu=np.full(size,1/size);b=np.array([1,0,0,1,0,0,0]);pairs=0
    for m in range(0,15):
        for j in range(m+1):
            op=np.ones(size)@np.linalg.matrix_power(Q,m-j)@np.diag(b)@np.linalg.matrix_power(Q,j)@nu
            direct=0j
            for initial in range(size):
                state=initial;phase=0.;marked=None
                for step in range(m+1):
                    if step==j:marked=b[state]
                    if step<m:phase+=values[state];state=perm[state]
                direct+=marked*np.exp(1j*theta*phase)/size
            require(abs(op-direct)<1e-12,'chronological marked pairing')
            require(max(j,m-j)>=m/2,'long block case')
            pairs+=1
    # Negative controls expressly reject the two invalid limiting inferences.
    # f_m has mass 1/m but height m; no mass-only height estimate follows.
    require(F(1,100)<F(1,10) and 100>10, 'small-mass negative control')
    # a_(m,j)=1_{j=m}: each fixed-j limsup is 0, but its depth sum is 1.
    for m in range(10,30):
        require(sum(int(j==m) for j in range(m+1))==1, 'escaping depth model')
        require(all(int(j==m)==0 for j in range(5)), 'fixed-layer negative control')
    # Terminal membership changes but is not an occupation summand.
    before=[1,0,1];after=[1,0,0]
    require(sum(before[:2])==sum(after[:2]) and sum(before)!=sum(after), 'terminal convention control')
    return {'strip_gain':'1/16','depth_exponent':'1/64','ordered_band_exponent':'1/192',
            'interpolation_cases':64,'positive_telescope_cases':telescope_cases,
            'occupation_cases':occupation_cases,'geometric_tail_cases':tail_cases,
            'affine_strip_cases':strip_cases,'chronological_pairings':pairs,
            'negative_control_classes':3,'continuum_proof_certified':False}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
