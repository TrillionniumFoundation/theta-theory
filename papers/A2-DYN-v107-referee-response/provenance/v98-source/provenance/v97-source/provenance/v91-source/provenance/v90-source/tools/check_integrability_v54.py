#!/usr/bin/env python3
"""Finite checks of exponent, source, layer-cake and likelihood algebra only."""
from fractions import Fraction as F
import itertools
import math


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    alpha, K = F(1,16), 9
    delta = F(3)
    require(3+2*delta == 9 and 2*delta == 6, 'flow/collar scales')
    require(alpha/K == F(1,144), 'density-tail exponent')
    exponents=[]
    for kappa, Gamma in [(F(1,10000),F(10)),(F(1,10),F(10)),(F(2),F(1,3)),(F(9,10),F(100))]:
        star=min(alpha/K,kappa/Gamma)/2
        require(star>0 and star<alpha/K and star*Gamma<kappa,'empty admissible exponent range')
        for sigma in [star/4,star/2,3*star/4]:
            theta=1-sigma/star
            require(0<theta<1 and theta+(1-theta)*(1+star)==1+sigma,'interpolation powers')
        exponents.append({'kappa':str(kappa),'Gamma':str(Gamma),'s_star':str(star),
                          'error_margin':str(kappa-Gamma*star)})
    comparisons=0
    # Pointwise implication used before integrating a density superlevel.
    for L in [F(1,2),F(1),F(2),F(5),F(10)]:
        for ai,bi in itertools.product(range(21),repeat=2):
            A,B=F(ai,4),F(bi,4);P=A+B
            if A<=L/2 and P>L:
                require(P<=2*B,'positive source domination at a density level')
                comparisons+=1
    # The positive source partition includes transition values, not just zeros.
    partitions=0
    for factors in itertools.product([F(0),F(1,3),F(1)],repeat=5):
        product=math.prod(factors)
        rhs=sum(math.prod(factors[:j])*(1-factors[j]) for j in range(5))
        require(1-product==rhs,'smooth-factor telescoping')
        require(1-product<=sum(v<1 for v in factors),'union bound omitted a transition')
        partitions+=1
    # The finite positive majorant always pays its inverse window length.
    window_cases=0
    for e in [F(1,2),F(1,4),F(1,8),F(1,16)]:
        h=e**9;r=e**6
        require(r>=h and (1+h)/h>=1/h,'inverse short-window payment')
        require((1+r)/r <= (1+h)/h,'critical collar no worse than flow box')
        window_cases+=1
    require((1+F(1,1024))/F(1,1024)>1000,'fixed-band short-window negative control failed')
    # Exact layer cake for a step density, using s=1 and rational weights.
    layer_cases=0
    for values in itertools.product([F(0),F(1,2),F(1),F(2),F(5)],repeat=3):
        weights=[F(1,5),F(3,10),F(1,2)]
        integral=sum(w*p*p for w,p in zip(weights,values))
        rhs=sum(w*p for w,p in zip(weights,values))
        rhs+=sum(w*p*max(F(0),p-1) for w,p in zip(weights,values))
        require(integral<=rhs,'finite layer-cake upper bound')
        layer_cases+=1
    # The cap/error competition; never integrate an error floor to infinity.
    for kap, gam in [(F(1,7),F(3)),(F(2),F(9)),(F(1,100),F(100))]:
        s=min(F(1,144),kap/gam)/2
        require(-kap+s*gam<0,'truncated finite-error term does not decay')
        m=int(kap/s)+2
        require(-kap*m+s*m*m>0,'superexponential-cap negative control')
    # Entropy is controlled by a finite-order likelihood norm, not by height.
    entropy_cases=0
    q=1+1/1024
    C=16/(q-1)
    for x in [0.,1e-20,1e-8,.01,.1,.5,.9,1.,1.1,2.,10.,1e4,1e8,1e16]:
        phi=1. if x==0 else x*math.log(x)-x+1
        require(phi>=-1e-12 and phi<=C*abs(x-1)**q+1e-10,'entropy/Lq comparison')
        entropy_cases+=1
    for vals in [[.2,1.,3.],[10.,.5,1.],[.9,1.,1.1]]:
        Q=[.2,.3,.5];z=sum(a*b for a,b in zip(Q,vals));r=[v/z for v in vals]
        require(abs(sum(a*b for a,b in zip(Q,r))-1)<1e-14,'likelihood normalization')
        ent=sum(a*b*math.log(b) for a,b in zip(Q,r))
        cost=sum(a*abs(b-1)**q for a,b in zip(Q,r))
        require(ent>=-1e-14 and ent<=C*cost,'forward normalized entropy')
    # L^q and entropy convergence do not imply an essential-height theorem.
    spike=[]
    qstar=1.25
    for j in [20,200,2000]:
        w=j**(-(qstar+1));normalizer=1+j*w
        high,low=(1+j)/normalizer,1/normalizer
        moment=w*high**qstar+(1-w)*low**qstar
        entropy=w*high*math.log(high)+(1-w)*low*math.log(low)
        spike.append((high,moment,entropy))
    require(spike[-1][0]>1000 and max(x[1] for x in spike)<2,'height countermodel')
    require(spike[-1][2]<spike[0][2],'forward entropy countermodel')
    # A signed convolution is controlled by kernel total variation.
    vector=[F(0),F(1),F(3),F(2),F(5)]
    convolution=[F(3,2)*vector[i]-F(1,2)*vector[(i-1)%len(vector)] for i in range(len(vector))]
    require(sum(x*x for x in convolution)<=4*sum(x*x for x in vector),'signed-kernel L2 bound')
    return {'alpha':str(alpha),'protection_height_power':K,'density_tail_power':'1/144',
       'admissible_exponent_cases':exponents,'positive_superlevel_cases':comparisons,
       'guard_partition_cases':partitions,'window_cases':window_cases,'layer_cake_cases':layer_cases,
       'entropy_cases':entropy_cases,'negative_controls':3,
       'finite_models_are_not_continuum_proofs':True}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
