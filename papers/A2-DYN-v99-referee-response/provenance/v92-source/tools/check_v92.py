#!/usr/bin/env python3
"""Finite normalization and entropy regressions; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json
import math


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def bl(v: tuple[F,F]) -> F:
    tests=((-1,-1),(-1,0),(0,-1),(0,1),(1,0),(1,1))
    return max(abs(v[0]*a+v[1]*b) for a,b in tests)


def weak_norm(values: tuple[float,...], widths: tuple[float,...], q: float) -> float:
    mass=volume=answer=0.0
    for value,width in sorted(zip(values,widths),reverse=True):
        mass+=value*width; volume+=width
        answer=max(answer,mass/volume**(1-1/q))
    return answer


def checks() -> dict:
    counts={'positive_lower':0,'physical_path_mixture':0,'bounded_critical':0,
            'entropy':0,'moving_roof_normalization':0,'exponents_and_scope':0}
    vals=tuple(map(F,(-2,-1,0,1,2,4)))
    for G,b,e in product(vals,(F(0),F(1,8),F(1),F(6)),(F(-1,8),F(0),F(1,8))):
        P=G+b+e
        if P<0: continue
        require(max(F(0),G-P)<=abs(e),'one-sided positive scalar bound')
        counts['positive_lower']+=1
        if G>=1:
            require(P>=F(1,2),'reference-floor denominator')
            require(max(F(0),G/P-1)<=2*abs(e),'one-sided reciprocal')
            require(abs(1-G/P)<=1 and abs(1-G/P)<=2*abs(P-G),'bounded reciprocal')
            counts['positive_lower']+=3
    for G,w,e0,e1,b0,b1 in product((F(1),F(2)),(F(0),F(1,3),F(1)),
                                  (F(-1,16),F(0),F(1,16)),
                                  (F(-1,16),F(0),F(1,16)),
                                  (F(0),F(1,4),F(2)),(F(0),F(1,4),F(2))):
        W=(w,1-w); E=(e0,e1); A=(G*w+e0,G*(1-w)+e1)
        if min(A)<0: continue
        B=(b0,b1); V=(A[0]+b0,A[1]+b1); P=sum(V); a=sum(A); b=sum(B)
        if not P or not a: continue
        eta=bl(E); discrepancy=bl((V[0]-G*w,V[1]-G*(1-w)))
        require(abs(P-G)<=discrepancy<=abs(P-G)+2*eta,'positive numerator gap')
        beta=b/P; good=(A[0]/a,A[1]/a); actual=(V[0]/P,V[1]/P)
        require(0<=beta<=1,'posterior is a probability')
        require(bl((good[0]-w,good[1]-(1-w)))<=4*eta,'good kernel normalization')
        require(bl((actual[0]-w,actual[1]-(1-w)))<=2*beta+4*eta,'mixture BL bound')
        require(abs(beta-(1-G/P))<=2*eta,'exact posterior/reciprocal comparison')
        if b:
            bad=(b0/b,b1/b)
            require(all(actual[i]==(1-beta)*good[i]+beta*bad[i] for i in range(2)),
                    'exact physical positive mixture')
        counts['physical_path_mixture']+=6
    for values,widths,q in product(product((0.,.2,1.,3.),repeat=3),
                                   ((.1,.3,.6),(.02,.03,.05)),(32/31,1.5,2.5)):
        H=max(values); L=sum(widths); A=weak_norm(values,widths,q)
        for p in (1.,(1+q)/2,q,q+.5,4.):
            actual=sum(w*v**p for w,v in zip(widths,values))
            if not A: bound=0.
            elif p<q: bound=q/(q-p)*A**p*L**(1-p/q)
            elif p>q: bound=p/(p-q)*A**q*H**(p-q)
            else: bound=A**q*(1+q*max(0.,math.log(H*L**(1/q)/A)))
            require(actual<=bound+1e-10*max(1.,bound),'bounded weak-to-strong fixture')
            counts['bounded_critical']+=1
    for p in (1.01,1.02,1.5,1.9):
        C=100+20/(p-1)
        for exponent in range(-120,121):
            x=10.**(exponent/10)
            phi=x*math.log(x)-x+1
            require(phi<=C*abs(x-1)**p+1e-10,'forward entropy fixture')
            counts['entropy']+=1
            if x>=1/3:
                psi=x-1-math.log(x)
                require(psi<=C*abs(x-1)**p+1e-10,'reverse entropy fixture')
                counts['entropy']+=1
        require(1<=C,'entropy continuous value at zero'); counts['entropy']+=1
    for G,P in product(((1.,2.,1.),(2.,1.,3.)),
                       ((1.,2.,1.),(1.2,1.9,1.1),(3.,1.,2.))):
        w=(.2,.3,.5); H=sum(a*b for a,b in zip(G,w)); Fm=sum(a*b for a,b in zip(P,w))
        ref=[a*b/H for a,b in zip(G,w)]; act=[a*b/Fm for a,b in zip(P,w)]
        ratio=[a/b for a,b in zip(act,ref)]; err=sum(c*abs(a-b) for a,b,c in zip(P,G,w))
        tv=sum(abs(a-b) for a,b in zip(act,ref))
        require(tv<=2*err/Fm+1e-12,'moving-roof total-variation bound')
        kl1=sum(a*math.log(a/b) for a,b in zip(act,ref))
        kl2=sum(b*math.log(b/a) for a,b in zip(act,ref))
        phi=sum(b*(r*math.log(r)-r+1) for b,r in zip(ref,ratio))
        psi=sum(b*(r-1-math.log(r)) for b,r in zip(ref,ratio))
        require(abs(kl1-phi)<1e-12 and abs(kl2-psi)<1e-12,'two entropy normalizations')
        require(kl1>=-1e-12 and kl2>=-1e-12,'nonnegative roof relative entropies')
        counts['moving_roof_normalization']+=3
    Q=F(32,31); eta=F(31,4096)
    require(Q*eta==F(1,128),'posterior high-moment exponent')
    require(F(1,12)*F(1,16)==F(1,192),'outer reconstruction exponent')
    require(F(1,2)*F(1)/Q==F(31,64),'diffusive weak-norm scaling')
    # A fixed upper pulse is compatible with every new bounded-ratio conclusion.
    widths=(.1,.01,.001)
    reciprocal_norms=[.5*d**(1/float(Q)) for d in widths]
    require(all(a>b for a,b in zip(reciprocal_norms,reciprocal_norms[1:])),
            'bounded reciprocal may vanish while the raw upper height stays one')
    counts['exponents_and_scope']+=4
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational normalization, finite probability and entropy identities, sampled weak-norm bounds',
            'full_raw_return_LLT_proved':False,'independent_human_review':False,
            'formal_proof_certificate':False}

if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
