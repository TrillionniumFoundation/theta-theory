#!/usr/bin/env python3
"""Exact finite bookkeeping for the stationary-window argument; not a billiard proof."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations, product
import json


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def must_reject(fn, message: str) -> None:
    try:
        fn()
    except RuntimeError:
        return
    raise RuntimeError('negative control did not reject: '+message)


def normalize(values):
    total = sum(values, F(0))
    require(total > 0, 'zero mass')
    return [v / total for v in values]


def tv(a, b):
    return sum((abs(x-y) for x,y in zip(a,b)), F(0))/2


def finite_checks() -> dict:
    theta, alpha, beta = F(9,100), F(19,100), F(50)
    P, Q, rate = 40, 29, F(3,280)
    margins = [F(1,2)-theta-2*alpha,
               (Q-1)*(F(1,2)-theta)-2*alpha*(Q+1)]
    require(margins == [F(3,100),F(2,25)], 'analytic margins')
    residual = [4*theta-P+2*P*theta+(1-alpha)*b for b in range(1,P+1)]
    require(max(residual)==-F(1,25), 'integrated small-mass residual')
    require(all(x < -rate for x in residual), 'residual block omitted or nondecaying')
    require(-max(residual)-rate == F(41,1400), 'logarithm absorption margin')
    fine=[beta-4*theta,beta-4*theta-(2*P-1)*(F(1,2)+theta)]
    require(fine==[F(1241,25),F(303,100)], 'fine errors')
    sigma, trunc, moment, outdim = F(2,25), F(1,400), 128, 3
    rates = [rate-trunc, theta-sigma, moment*trunc-outdim*sigma]
    require(rates==[F(23,2800),F(1,100),F(2,25)],'projection and tail rates')
    require(F(1,2)-sigma == F(21,50) and outdim*sigma==F(6,25),'physical window scale')
    require(F(1,8)-sigma==F(9,200) and F(2)-outdim*sigma==F(44,25),'relative shell powers')
    require(min(rates)==F(23,2800),'final rate')
    # The collision theorem has no stopping term. It must not be read as
    # a return theorem on the same isotropic ball.
    must_reject(lambda: require(F(1,4)-5*theta>0, 'return stopping loss'), 'collision/return distinction')
    must_reject(lambda: require(F(64)*trunc-outdim*sigma>0, '64th moment fails here'), 'insufficient projection moment')

    tower_tests=0; bias_tests=0
    for size,section in [(11,[0,3,7]),(17,[0,2,8,12]),(23,[0,5,9,17])]:
        roofs=[F(2+(3*j*j+5*j)%13,7) for j in range(size)]
        total=sum(roofs,F(0)); nu=F(1,size); cstar=F(len(section),size)
        meanroof=total/size; intervals=[]
        for i,y in enumerate(section):
            nxt=section[(i+1)%len(section)]
            length=(nxt-y)%size
            intervals.append([(y+j)%size for j in range(length)])
        bigroofs=[sum((roofs[j] for j in js),F(0)) for js in intervals]
        meanbig=sum(bigroofs,F(0))/len(section)
        require(cstar*meanbig==meanroof,'Kac roof normalization')
        require(sorted(j for js in intervals for j in js)==list(range(size)), 'tower partition')
        for degree in range(6):
            # Integral of state-dependent polynomial times elapsed-flight age^degree.
            vals=[F((j+1)**2+degree) for j in range(size)]
            direct=sum((vals[j]*roofs[j]**(degree+1)/F(degree+1) for j in range(size)),F(0))/total
            lifted=sum((sum((vals[j]*roofs[j]**(degree+1)/F(degree+1) for j in js),F(0))
                        for js in intervals),F(0))/(len(section)*meanbig)
            require(direct==lifted,'full suspension versus return suspension')
            tower_tests+=1
        induced=[v/total for v in bigroofs]
        bycount=[F(len(js),size) for js in intervals]
        uniform=[F(1,len(section))]*len(section)
        require(induced!=uniform and induced!=bycount,'model must detect both wrong biases')
        must_reject(lambda: require(induced==uniform,'unbiased section law'), 'missing roof bias')
        must_reject(lambda: require(induced==bycount,'count bias substituted for roof bias'), 'wrong bias')
        for mask in product((0,1),repeat=len(section)):
            weighted=sum((p for p,z in zip(induced,mask) if z),F(0))
            basic=F(sum(mask),len(section))
            constant=sum((x*x for x in bigroofs),F(0))/len(section)/(meanbig*meanbig)
            require(weighted*weighted <= constant*basic, 'Holder event transfer')
            bias_tests+=1
        # Current outgoing collision is roof biased, not uniform on collisions.
        current=[F(0)]*size
        for js in intervals:
            for j in js: current[j]+=roofs[j]/total
        require(current==[v/total for v in roofs], 'current outgoing collision marginal')

    conditional_tests=0; shell_tests=0
    mu=normalize([F(1),F(2),F(4),F(7),F(11)])
    masks=list(product((0,1),repeat=len(mu)))
    for a in masks:
        p=sum((v for v,z in zip(mu,a) if z),F(0))
        if not p:continue
        for b in masks:
            q=sum((v for v,z in zip(mu,b) if z),F(0))
            if not q:continue
            delta=sum((v for v,x,y in zip(mu,a,b) if x!=y),F(0))
            left=tv([v*z/p for v,z in zip(mu,a)],[v*z/q for v,z in zip(mu,b)])
            require(left<=2*delta/p,'conditional TV normalization')
            # Selection can depend on the full state; its mass must remain explicit.
            w=[F(1),F(0),F(3,2),F(1,4),F(2)]
            wp=sum((v*z*weight for v,z,weight in zip(mu,a,w)),F(0))
            wq=sum((v*z*weight for v,z,weight in zip(mu,b,w)),F(0))
            if wp and wq:
                wtv=tv([v*z*weight/wp for v,z,weight in zip(mu,a,w)],
                       [v*z*weight/wq for v,z,weight in zip(mu,b,w)])
                require(wtv<=2*max(w)*delta/wp,'weighted conditional normalization')
            conditional_tests+=1
    h,d=F(1),F(1,4)
    for x in product([F(j,4) for j in range(-6,7)],repeat=3):
        inside=lambda z,half:all(abs(v)<=half for v in z)
        for change in product((-d,F(0),d),repeat=3):
            y=tuple(a+b for a,b in zip(x,change))
            if inside(x,h)!=inside(y,h):
                require(inside(x,h+d) and not inside(x,h-d),'boundary shell inclusion')
            shell_tests+=1
    # An absolute rare-event error can tend to zero while the conditional
    # laws stay completely separated: the reciprocal denominator matters.
    rare=F(1,1000)
    must_reject(lambda:require(F(1)<=2*(2*rare),'absolute error used as TV'), 'missing rare denominator')
    return {'analytic_margins':[str(x) for x in margins], 'residual_block_cases':len(residual),
            'residual_max_power':str(max(residual)), 'fine_error_rates':[str(x) for x in fine],
            'projection_rates':[str(x) for x in rates], 'projection_moment_order':moment,
            'physical_half_width':'21/50','physical_probability_power':'6/25',
            'relative_error_rate':'23/2800','finite_tower_integral_cases':tower_tests,
            'finite_bias_transfer_cases':bias_tests,'conditional_measure_cases':conditional_tests,
            'boundary_shell_cases':shell_tests,'negative_controls':9,
            'continuum_proof_certified':False, 'microscopic_raw_endpoint_certified':False}


if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
