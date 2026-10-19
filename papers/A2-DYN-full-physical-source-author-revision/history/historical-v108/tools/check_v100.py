#!/usr/bin/env python3
"""Finite algebra/grid/assignment fixtures only, not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools, json, math, random

def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def checks() -> dict:
    count={k:0 for k in ('grid_transversality','injective_test_sums','capacity_depth',
                        'two_cap_integral','moment_exponents','fixed_block_margin',
                        'scalar_schedule','negative_controls')}
    rng=random.Random(100241)
    # Finite graphs illustrate the transverse-grid mechanism. These are not billiard cells.
    for _ in range(800):
        slope=rng.uniform(.25,5);length=rng.uniform(.02,.7);stable=-rng.uniform(.3,2)
        dx=length/math.sqrt(1+slope*slope);x=rng.uniform(-1,1);y=rng.uniform(-1,1)
        a=y-stable*x; b=(y+slope*dx)-stable*(x+dx)
        mesh=(b-a)/3.1;shift=rng.random()*mesh
        j=math.floor((a-shift)/mesh)+1
        require(a<shift+j*mesh<b,'transverse grid fails on linear cone graph')
        count['grid_transversality']+=1
    # Each backward cell is assigned once, while its final subcells are charged at most D times.
    for n,D in itertools.product(range(1,30),range(1,8)):
        weights=[F(rng.randrange(1,100),100) for _ in range(n)]
        labels=[rng.randrange(5) for _ in range(n)]
        mult=[rng.randrange(1,D+1) for _ in range(n)]
        final=sum((w*d for w,d in zip(weights,mult)),F(0))
        grouped=sum((sum((w for w,j in zip(weights,labels) if j==k),F(0)) for k in range(5)),F(0))
        require(final<=D*grouped and grouped==sum(weights,F(0)),'injective assignment budget')
        count['injective_test_sums']+=2
    q=F(47,53);depth_bound=2*q/(1-q)
    for m in range(1,120):
        total=sum((q**min(i,m-i) for i in range(1,m)),F(0))
        require(total<=depth_bound,'complete depth sum')
        count['capacity_depth']+=1
    # Exact primitive of the capped power integral, evaluated on both sides of its crossover.
    pvals=[1,1+1/1024,1+1/512,1+7/1024]
    for p,loge,logh,logb in itertools.product(pvals,range(-4,5),range(-4,5),range(-4,3)):
        E,H,b=10.**loge,10.**logh,10.**logb;v0=(E/H)**(2/3)
        if b<=v0:
            val=2*H*b**(2-p)/(2-p)
        else:
            val=E*b**(.5-p)+p*H*v0**(2-p)/(2-p)+p*E*(v0**(.5-p)-b**(.5-p))/(p-.5)
        C=max(2/(2-p),1+p/(2-p)+p/(p-.5))
        bound=C*min(H*b**(2-p),E**((4-2*p)/3)*H**((2*p-1)/3))
        require(0<=val<=bound*(1+1e-11),'complete two-cap moment integral')
        count['two_cap_integral']+=1
    alpha=F(129,128)
    for p in [F(1),F(1025,1024),F(513,512),F(1031,1024)]:
        a=(4-2*p)/3;b=(2*p-1)/3
        require(a+b==1 and a>0 and b>0 and alpha-p>0,'moment powers/collision normalization')
        count['moment_exponents']+=1
    require((4-2*F(1))/3==F(2,3),'first moment spectral exponent')
    count['moment_exponents']+=1
    for Q,theta in itertools.product((1.,2.,20.,1000.),(.1,.5,.8,.95,.999)):
        L=math.floor(math.log(max(1,Q))/(-2*math.log(theta)))+2
        margin=math.exp(math.log(max(1,Q))/L)*theta**2
        require(margin<1,'fixed block strict margin')
        count['fixed_block_margin']+=1
    require(4*F(257,256)==F(257,64) and 4-1==3,'retained outer schedule')
    require(F(1,12)*F(1,16)==F(1,192),'positive scalar remainder power')
    count['scalar_schedule']+=2
    # Equal positive traces have zero difference but nonzero minimum.
    for w in (F(1,5),F(1),F(7)):
        require(abs(w-w)==0 and min(w,w)>0,'paired minimum must not be erased')
        count['negative_controls']+=1
    require(alpha-F(129,128)==0,'endpoint moment has no strict leading integrability gain')
    count['negative_controls']+=1
    return {'counts':count,'total_checks':sum(count.values()),
            'scope':'finite synthetic cone graphs, injective weighted assignments, capped power integrals and exact exponents only',
            'continuum_geometric_pressure_certified_by_tests':False,
            'full_raw_return_LLT_proved':False,'independent_human_review':False,'formal_proof_certificate':False}
if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
