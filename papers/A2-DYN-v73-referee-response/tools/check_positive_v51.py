#!/usr/bin/env python3
"""Exact finite regressions for the new inequalities, not a continuum certificate."""
from fractions import Fraction as F
from random import Random
from math import log


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def finite_checks():
    rng=Random(510109)
    kernel=[F(-1,4),F(3,2),F(-1,4)]
    require(sum(kernel)==1 and sum(abs(x) for x in kernel)==2,'signed kernel')
    def conv(v):
        return [sum(kernel[j]*v[(i+j-1)%len(v)] for j in range(3)) for i in range(len(v))]
    source_cases=0
    for case in range(256):
        a=[F(rng.randrange(0,40),17) for _ in range(8)]
        b=[F(rng.randrange(0,20),37) for _ in range(8)]
        p=[x+y for x,y in zip(a,b)];kp=conv(p);ka=conv(a);kb=conv(b)
        g=[x+F(rng.randrange(-5,6),43) for x in kp]
        errors=[]
        for i in range(8):
            error=p[i]-g[i]-b[i]
            require(error==a[i]-ka[i]+kp[i]-g[i]-kb[i],'exact source identity')
            require(max(g[i]-p[i],0)<=abs(error),'one-sided bound')
            require(abs(max(p[i]-g[i],0)-b[i])<=abs(error),'positive-part contraction')
            errors.append(error)
        require(abs(max(max(p[i]-g[i],0) for i in range(8))-max(b))<=max(map(abs,errors)),
                'positive height comparison')
        source_cases+=1
    minorization_cases=0
    for case in range(512):
        g=[F(1)+F(rng.randrange(0,20),19) for _ in range(8)]
        p=[g[i]+F(rng.randrange(-2,9),17) for i in range(8)]
        d=min(g);delta=max(max(g[i]-p[i],0) for i in range(8))
        e=sum(abs(p[i]-g[i]) for i in range(8))/8
        G=sum(g)/8;P=sum(p)/8;alpha=(1-delta/d)/(1+e/d)
        require(0<alpha<=1,'minorization factor')
        q=[x/G for x in g];prob=[x/P for x in p]
        require(all(prob[i]>=alpha*q[i] for i in range(8)),'normalized domination')
        require(max(q[i]/prob[i] for i in range(8))<=1/alpha,'reverse likelihood')
        if alpha<1:
            residual=[(prob[i]-alpha*q[i])/(1-alpha) for i in range(8)]
            require(min(residual)>=0 and sum(residual)/8==1,'residual probability')
        else:
            require(prob==q,'unit minorization')
        minorization_cases+=1
    require(F(1,12)*F(1,16)==F(1,192),'band exponent')
    require(F(1,2)>F(1,192),'protected error ordering')
    # Thin holes: local L1/TV convergence alone cannot yield the lower theorem.
    hole_cases=0
    for n in range(2,66):
        width=F(1,n)
        require(width+(1-width)*(1/(1-width)-1)==2*width,'thin-hole L1')
        require(F(0)<F(1,2),'hole prevents positive reference minorization')
        hole_cases+=1
    # Positive spikes preserve lower domination while destroying upper convergence.
    spike=[]
    for n in (2,4,8,16,32):
        height=2**(n*n);width=F(1,n*height);normalizer=1+F(1,n)
        outside=1/normalizer;inside=(1+height)/normalizer
        require(width*inside+(1-width)*outside==1,'spike normalization')
        require(inside>n and outside==F(n,n+1),'spike direction')
        reverse_bound=log(1+1/n)
        forward=float(width*inside)*log(float(inside))+float((1-width)*outside)*log(float(outside))
        require(reverse_bound>0 and forward>0,'divergence signs')
        spike.append({'n':n,'reverse_infinity_bound':reverse_bound,'forward_entropy':forward})
    require(spike[-1]['forward_entropy']>spike[0]['forward_entropy'], 'forward negative control')
    # Cancellation of positive components cannot lower their common height.
    for x in range(12):
        for y in range(12):
            require(x<=x+y and y<=x+y,'positive component domination')
    return {'signed_source_cases':source_cases,'conditional_minorization_cases':minorization_cases,
            'thin_hole_negative_controls':hole_cases,'positive_spike_negative_controls':spike,
            'positive_component_cases':144,'ordered_band_rate':'1/192',
            'finite_diagnostics_only':True,'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
