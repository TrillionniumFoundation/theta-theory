#!/usr/bin/env python3
"""Finite regressions for the new formulas; not proofs about the billiard."""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial

def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

@lru_cache(None)
def partitions(n: int):
    if n == 0: return ((),)
    out=[]
    for p in partitions(n-1):
        out.append(p+((n-1,),))
        for j in range(len(p)):
            out.append(p[:j]+(p[j]+(n-1,),)+p[j+1:])
    return tuple(out)

def cumulant_from_moments(n: int, moment) -> F:
    ans=F(0)
    for p in partitions(n):
        term=F((-1)**(len(p)-1)*factorial(len(p)-1))
        for block in p: term *= moment(block)
        ans+=term
    return ans

# All series are exact Taylor coefficients, not derivatives, through order N.
def add(a,b): return [x+y for x,y in zip(a,b)]
def scale(a,s): return [s*x for x in a]
def mul(a,b):
    n=len(a)-1
    return [sum((a[j]*b[k-j] for j in range(k+1)),F(0)) for k in range(n+1)]
def div(a,b):
    require(b[0]!=0,'division by a zero formal constant')
    out=[a[0]/b[0]]
    for k in range(1,len(a)):
        out.append((a[k]-sum((b[j]*out[k-j] for j in range(1,k+1)),F(0)))/b[0])
    return out
def power(a,k):
    out=[F(1)]+[F(0)]*(len(a)-1)
    while k:
        if k&1:out=mul(out,a)
        a=mul(a,a);k//=2
    return out
def logarithm(a):
    require(a[0]==1,'logarithm is normalized at one')
    g=[F(0)]
    for k in range(1,len(a)):
        g.append(a[k]-sum((F(j,k)*g[j]*a[k-j] for j in range(1,k)),F(0)))
    return g

def finite_checks() -> dict:
    eps=F(1,50);theta=F(21,100);Q=19;old=F(1,200)
    margins={'analytic_radius':F(1,2)-eps-2*theta,
      'Taylor_remainder_relative_to_quadratic':(Q-1)*(F(1,2)-eps)-2*(Q+1)*theta,
      'insertion_L1_integrated':theta-4*eps,
      'observable_L2_integrated':theta/2-5*eps,
      'actual_stopping_integrated':F(2,9)-5*eps}
    require(margins=={'analytic_radius':F(3,50),'Taylor_remainder_relative_to_quadratic':F(6,25),
      'insertion_L1_integrated':F(13,100),'observable_L2_integrated':F(1,200),
      'actual_stopping_integrated':F(11,90)},'fixed-count exponents')
    require(all(x>0 for x in margins.values()),'infeasible fixed-count scale')
    require(2-4*F(1,2)==0,'raw Jacobian normalization')
    require(F(1,2)-eps==F(12,25) and eps-old==F(3,200),'cutoff conversion')
    require(4*eps==F(2,25) and F(1,2)+eps==F(13,25),'Schwartz count exponents')
    require(F(13,100)>F(9,175) and F(3,280)>F(1,200),'central/shell splice')
    choices=[]
    for e in (F(1,180),F(1,100),F(1,80),F(1,60),F(1,50),F(1,45)):
        t=(10*e+(F(1,4)-e/2))/2
        q=3
        while (q-1)*(F(1,2)-e)<=2*(q+1)*t:q+=2
        require(10*e<t<F(1,4)-e/2 and F(2,9)>5*e,'general band range')
        choices.append({'epsilon':str(e),'theta':str(t),'degree':q})
    # Negative controls reject the old cubic argument at the new scale,
    # degree 15 at this theta, and a vacuous endpoint choice.
    require(6*theta+3*eps-F(1,2)>0,'old cubic unexpectedly covers new band')
    require((15-1)*(F(1,2)-eps)-2*(15+1)*theta==0,'degree-15 strictness control')
    require(10*F(1,40)>=F(1,4)-F(1,80),'endpoint control')

    # Independent block cumulants must vanish, including repeated copies
    # within a block; compare the diagonal with the scalar recurrence.
    p=F(1,3); scalar=[F(0)]*9;mom=[F(1)]+[p]*8
    from math import comb
    for n in range(1,9):
        scalar[n]=mom[n]-sum((F(comb(n-1,k-1))*scalar[k]*mom[n-k] for k in range(1,n)),F(0))
    independent_cases=0
    for q in range(2,8):
        require(cumulant_from_moments(q,lambda block:p)==scalar[q],'partition/scalar cumulant')
        for split in range(1,q):
            def moment(block):
                return p**int(any(j<split for j in block))*F(2,5)**int(any(j>=split for j in block))
            require(cumulant_from_moments(q,moment)==0,'independent connected cumulant')
            independent_cases+=1

    # Every ordered tuple has exactly (m-diameter)_+ admissible translates
    # after anchoring its first coordinate; no q! factor is inserted.
    anchored_cases=0
    for q in range(2,6):
        for m in range(1,7):
            counts={}
            for t in product(range(m),repeat=q):
                k=tuple(t[j]-t[0] for j in range(1,q));counts[k]=counts.get(k,0)+1
            for k,count in counts.items():
                require(count==m-(max((0,)+k)-min((0,)+k)),'anchored translation multiplicity')
                anchored_cases+=1
            require(sum(counts.values())==m**q,'all ordered collision tuples retained')

    # A two-state stationary Markov model is only an algebraic regression.
    # Compute the leading eigenvalue to degree 19 by its quadratic equation,
    # and compare finite-time transfer products with the exact spectral split.
    N=19;one=[F(1)]+[F(0)]*N;zero=[F(0)]*(N+1)
    ep=[F(1,factorial(j)) for j in range(N+1)]
    em=[F((-1)**j,factorial(j)) for j in range(N+1)]
    ch=scale(add(ep,em),F(1,2));a=F(3,4);rho=F(1,2)
    rad=add(scale(mul(ch,ch),a*a),scale(one,-rho))
    sq=[F(1,4)]
    for k in range(1,N+1):sq.append((rad[k]-sum((sq[j]*sq[k-j] for j in range(1,k)),F(0)))/(2*sq[0]))
    lp=add(scale(ch,a),sq);lm=add(scale(ch,a),scale(sq,-1));psi=logarithm(lp)
    require(add(add(mul(lp,lp),scale(mul(ch,lp),-2*a)),scale(one,rho))==zero,'eigenvalue equation jet')
    require(2*psi[2]==3 and all(psi[j]==0 for j in range(1,N+1,2)),'variance or symmetry of spectral jet')
    amp=div(add(ch,scale(lm,-1)),add(lp,scale(lm,-1)))
    logamp=logarithm(amp)
    row0=scale(one,F(1,2));row1=scale(one,F(1,2));transfer_cases=0
    for m in range(1,7):
        row0,row1=mul(add(scale(row0,a),scale(row1,1-a)),ep),mul(add(scale(row0,1-a),scale(row1,a)),em)
        fm=add(row0,row1)
        spectral=add(mul(amp,power(lp,m)),mul(add(one,scale(amp,-1)),power(lm,m)))
        require(fm==spectral,'finite-time transfer/spectral jet')
        transfer_cases+=1
    finite=add(mul(amp,power(lp,128)),mul(add(one,scale(amp,-1)),power(lm,128)))
    logfinite=logarithm(finite)
    require(max(abs(logfinite[j]-128*psi[j]-logamp[j]) for j in range(2,7))<F(1,10**20),
            'fixed-scale spectral derivative identification model')
    return {'fixed_count_margins':{k:str(v) for k,v in margins.items()},'general_range_examples':choices,
      'independent_block_cumulant_cases':independent_cases,'anchored_tuple_cases':anchored_cases,
      'spectral_model_jet_degree':N,'exact_transfer_spectral_comparisons':transfer_cases,
      'spectral_identification_model_length':128,'negative_controls':3,
      'raw_four_dimensional_normalization_verified':True,
      'return_count_averages_not_used_as_fixed_count_proof':True,
      'finite_models_are_not_continuum_proofs':True}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
