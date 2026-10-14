#!/usr/bin/env python3
"""Finite algebra and Fourier models, never continuum proof certification."""
from fractions import Fraction as F
from itertools import product
from math import comb
import numpy as np


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def compositions(s, cap, d=4):
    if cap < 0:
        return int(s == 0) if d == 0 else 0
    return sum((-1)**j * comb(d,j) * comb(s-j*(cap+1)+d-1,d-1)
               for j in range(d+1) if s-j*(cap+1) >= 0)


def shell_count(t):
    # Decompose uniquely by the maximal coordinate, not by one attaining index.
    return sum(compositions(t-j,j)-compositions(t-j,j-1)
               for j in range(t+1))


def chi(x):
    x=np.abs(np.asarray(x,dtype=float))
    out=np.zeros_like(x)
    out[x<=1]=1
    good=(x>1)&(x<2)
    y=x[good]-1
    aa=np.exp(-1/(1-y)); bb=np.exp(-1/y)
    out[good]=aa/(aa+bb)
    return out


def phi(j,x):
    return chi(np.asarray(x)/2**j) if j==0 else chi(np.asarray(x)/2**j)-chi(np.asarray(x)/2**(j-1))


def finite_checks():
    tau=F(1,200); cap=F(9,100); budget=F(67,280)
    vol=budget-tau; eta=F(1,4)-budget; alpha=F(19,100)
    P,Q,beta=26,29,F(32)
    margins={
       'volume':vol,'stopping':eta,
       'analytic':F(1,2)-cap-2*alpha,
       'spectral':(Q-1)*(F(1,2)-cap)-2*alpha*(Q+1),
       'fine_insertion':beta-vol,
       'fine_residual':beta-vol-(2*P-1)*(F(1,2)+cap),
       'worst_residual':P*(alpha-2*cap)-vol}
    expect={'volume':F(41,175),'stopping':F(3,280),'analytic':F(3,100),
            'spectral':F(2,25),'fine_insertion':F(5559,175),
            'fine_residual':F(1173,700),'worst_residual':F(9,350)}
    require(margins==expect,'incorrect exponent ledger')
    require(margins['worst_residual']-eta==F(3,200),'lost logarithmic slack')
    residuals=[P-2*P*cap-vol-(1-alpha)*b for b in range(1,P+1)]
    require(min(residuals)==F(9,350) and len(residuals)==26,'incomplete residual sum')
    for b in range(P-1):
        require(residuals[b]-residuals[b+1]==F(81,100),'block count decrement')
    require(2*cap+3*tau<budget,'four-axis reach not feasible')
    rho=[F(1,25)]*3+[F(1,20)]
    require(sum(rho)+max(rho)==F(11,50)<budget,'mixed example not feasible')
    require(5*F(3,50)>budget and F(3,50)>F(67,1400),'missed-region example')
    require(F(1,2)+tau==F(101,200),'wrong count-coordinate tail scale')
    require(4**4 == 256, 'four-dimensional box volume')
    # Independent shell enumeration through cost 13, including tied maxima.
    direct=[0]*14
    for j in product(range(14),repeat=4):
        t=sum(j)+max(j)
        if t<=13:direct[t]+=1
    for t in range(14):require(shell_count(t)==direct[t],'dyadic shell enumeration')
    cumulative=0
    for K in range(97):
        count=shell_count(K)
        require(0<=count<=4*(K+2)**3,'shell cubic bound')
        cumulative += count*2**K
        require(cumulative<=64*2**K*(K+1)**3,'weighted sum bound')
    # Partition tests at a finite budget, independent of the asymptotic scale.
    K,maxj=11,5
    D=[j for j in product(range(maxj+1),repeat=4) if sum(j)+max(j)<=K]
    rng=np.random.default_rng(2607)
    points=np.vstack((rng.uniform(-20,20,(256,4)),rng.uniform(-1,1,(128,4)),
                      rng.uniform(-2,2,(128,4))))
    values=np.zeros(len(points)); has_box=np.zeros(len(points),dtype=bool)
    for js in D:
        scale=2.**np.array(js)
        has_box |= np.all(np.abs(points)<=2*scale,axis=1)
        values += np.prod(np.stack([phi(js[i],points[:,i]) for i in range(4)],axis=1),axis=1)
    require(np.all(values>=-1e-13) and np.all(values<=1+1e-13),'partition not in [0,1]')
    x=np.maximum(1,np.abs(points)); mx=x.max(axis=1)
    inner=(mx<=2**maxj/2)&(x.prod(axis=1)*mx<=2**K/32)
    require(np.allclose(values[inner],1,rtol=0,atol=2e-13),'missing inner plateau')
    center=np.all(np.abs(points)<=1,axis=1)
    require(np.allclose(values[center],1,rtol=0,atol=2e-13),'missing central plateau')
    require(np.all(values[~has_box]==0),'cutoff outside union support')
    # All nonzero pieces at an inner point must meet the index budget.
    for point in points[inner][:32]:
        for js in product(range(8),repeat=4):
            if all(float(phi(js[i],point[i]))>1e-14 for i in range(4)):
                require(sum(js)+max(js)<=K and max(js)<=maxj,'inner point uses inadmissible piece')
    # Count-coordinate decay is on the third coordinate, all scales at least base.
    weights=[2**sum(j) for j in D]
    base_weight=sum(weights)
    for order in range(1,5):
        lhs=sum(F(w,(1+16*2**j[2])**order) for j,w in zip(D,weights))
        require(lhs<=F(base_weight,16**order),'count decay sum')
    # A four-dimensional finite Fourier surrogate for the exact signed identity.
    # This checks normalization/sign algebra, not the continuous billiard law.
    maxerr=0.0; trials=0
    for size in (3,4,5):
        shape=(size,)*4
        for unused in range(4):
            e=rng.normal(size=shape)+1j*rng.normal(size=shape)
            q=rng.normal(size=shape)+1j*rng.normal(size=shape)
            c=rng.uniform(0,1,shape); p=rng.uniform(0,1,shape)
            conv=lambda mask,data:np.fft.ifftn(mask*np.fft.fftn(data))
            rc=e-conv(c,e)+conv(1-c,q)
            rp=e-conv(p,e)+conv(1-p,q)
            rhs=conv(p-c,e+q)
            err=float(np.max(np.abs(rc-rp-rhs)))
            maxerr=max(maxerr,err); trials+=1
            require(err<2e-12,'raw signed cancellation failed')
            require(np.max(np.abs((rc-rp)+rhs))>1e-3,'wrong-sign negative control')
            require(np.max(np.abs(rc-rp-conv(p-c,e)))>1e-3,'omitted-residual negative control')
    # Omitting connected blocks is not a uniform bound when m*delta is small.
    x=F(1,1000)
    require(sum(x**b for b in range(1,P+1))>10*x**P,'connected-block negative control')
    return {'exact_margins':{k:str(v) for k,v in margins.items()},
      'residual_half_order':P,'residual_degree':2*P-1,'spectral_degree':Q,
      'residual_block_counts_checked':P,'max_multipliers':2*P,'max_collision_powers':2*P+1,
      'shell_enumeration_levels':14,'weighted_shell_budgets_checked':97,
      'partition_points':len(points),'inner_plateau_points':int(inner.sum()),
      'dyadic_boxes_in_finite_partition':len(D),'count_tail_orders_checked':4,
      'four_dimensional_fourier_trials':trials,'max_fourier_identity_error':maxerr,
      'negative_control_types':3,'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
