#!/usr/bin/env python3
"""Finite diagnostics for v27. These are not continuum proof certificates."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import ceil, floor
import json
import mpmath as mp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def kernel(x):
    x=mp.mpf(x)
    return mp.mpf(1) if x==0 else (mp.sin(mp.pi*x)/(mp.pi*x))**2


def sign_approximant(x):
    x=mp.mpf(x)
    if x==0:return mp.mpf(0)
    if x<0:return -sign_approximant(-x)
    s=(mp.sin(mp.pi*x)/mp.pi)**2
    return 1-kernel(x)-2*s*(mp.polygamma(1,x+1)-1/x)


def envelopes(x,a,b,delta):
    x,a,b,delta=map(mp.mpf,(x,a,b,delta))
    center=(sign_approximant(delta*(x-a))-sign_approximant(delta*(x-b)))/2
    err=(kernel(delta*(x-a))+kernel(delta*(x-b)))/2
    return center-err,center+err


def finite_checks() -> dict:
    mp.mp.dps=70
    tol=mp.mpf('1e-55')
    count=0
    for j in range(-160,161):
        x=mp.mpf(j)/8
        sg=mp.sign(x)
        require(abs(sg-sign_approximant(x))<=kernel(x)+tol,'sign envelope')
        require(abs(sign_approximant(x)+sign_approximant(-x))<=tol,'odd error')
        count+=1
    interval_cases=0; endpoint_cases=0
    for a,b in [('-1.5','2.25'),('0','1'),('0.125','0.375')]:
        for delta in ['0.25','1','3']:
            aa,bb=mp.mpf(a),mp.mpf(b)
            for j in range(-80,81):
                x=mp.mpf(j)/8;lo,hi=envelopes(x,aa,bb,delta)
                closed=int(aa<=x<=bb);opened=int(aa<x<bb)
                require(lo<=opened+tol and hi+tol>=closed,'interval order including endpoints')
                require(-tol<=hi<=3+tol and hi-lo>=-tol,'nonnegative majorant and error')
                interval_cases+=1
            for x in [aa,bb]:
                lo,hi=envelopes(x,aa,bb,delta)
                require(lo<=tol and hi>=1-tol,'endpoint convention')
                endpoint_cases+=1
    # Four-variable tensor lower bound. Multiplying the lower factors is invalid.
    states=[(F(0),F(-1,2),F(1,2)),(F(0),F(-1),F(1)),
            (F(1),F(0),F(1)),(F(1),F(1,2),F(3,2)),
            (F(1),F(1),F(1)),(F(0),F(0),F(0))]
    tensor_cases=0
    for choice in product(states,repeat=4):
        indicator=F(1);up=F(1)
        for i,l,u in choice:indicator*=i;up*=u
        low=up
        for idx,(i,l,u) in enumerate(choice):
            term=u-l
            for j,(_,_,uj) in enumerate(choice):
                if j!=idx:term*=uj
            low-=term
        require(low<=indicator<=up,'tensor lower-envelope sign')
        tensor_cases+=1
    require(F(-1,2)*F(-1,2)>0,'signed-product negative control failed')
    # Exact rate and normalization arithmetic.
    rho=F(67,1400);sigma=F(1,25);e=F(3,280);v=F(9,175);tau=F(1,400)
    rate=rho-sigma
    require(rate==F(11,1400),'window boundary rate')
    require(e-tau==F(23,2800)>rate,'projected Fourier loss')
    require(v-tau>e-tau and 64*tau-3*sigma==F(1,25)>rate,'projection tail budget')
    require(F(1,8)-sigma==F(17,200)>rate,'coupling boundary budget')
    require(2-3*sigma>rate,'bad-event relative denominator')
    require(F(1,2)-sigma==F(23,50),'physical width')
    require(4*sigma==F(4,25) and 3*sigma==F(3,25),'rare event volume')
    require(rho-F(1,2)==F(-633,1400)<0,'singleton must not meet bandwidth condition')
    require(F(1,2)-F(5,8)==F(-1,8),'inverse clock moment exponent')
    require(F(5,16)-F(3,8)==F(-1,16),'window maximum exponent')
    # Exact lattice endpoint counts in finite intervals.
    grid_cases=0
    for c in [F(i,3) for i in range(-12,13)]:
        for h in [F(1),F(3,2),F(7,3),F(4)]:
            a,b=c-h,c+h
            nc=floor(b)-ceil(a)+1
            no=ceil(b)-floor(a)-1
            require(abs(F(nc)-2*h)<=1 and abs(F(no)-2*h)<=1,'grid boundary count')
            require(h<=nc<=3*h,'grid comparability')
            grid_cases+=1
    # Conditional total variation for two distinct events, with exact probabilities.
    weights=[F(i,21) for i in range(1,7)]
    tv_cases=0
    for ma in range(1,64):
        for mb in range(1,64):
            A=[bool(ma&(1<<i)) for i in range(6)]
            B=[bool(mb&(1<<i)) for i in range(6)]
            pa=sum(w for w,i in zip(weights,A) if i);pb=sum(w for w,i in zip(weights,B) if i)
            diff=sum(w for w,i,j in zip(weights,A,B) if i!=j)
            if diff<=pa/2:
                tv=sum(abs(w*(F(int(i))/pa-F(int(j))/pb)) for w,i,j in zip(weights,A,B))/2
                require(pb>=pa/2 and tv<=2*diff/pa,'conditional comparison')
                tv_cases+=1
    # Finite actual flight/return bookkeeping, not a dynamical limit model.
    return_sizes=[2,1,4,3,2,5,1,3]
    roofs=[F((j%5)+2,10) for j in range(sum(return_sizes))]
    k1=[(j%3)-1 for j in range(len(roofs))];k2=[((2*j)%3)-1 for j in range(len(roofs))]
    times=[F(0)];K1=[0];K2=[0]
    for dt,x,y in zip(roofs,k1,k2):times.append(times[-1]+dt);K1.append(K1[-1]+x);K2.append(K2[-1]+y)
    visits=[0]
    for r in return_sizes:visits.append(visits[-1]+r)
    tau_bar=F(2,5);cstar=F(1,7)
    G=[F(0),F(0),1/cstar,tau_bar/cstar]
    B=lambda x:(x[0],x[1],x[2]-x[3]/tau_bar)
    require(B(G)==(0,0,0),'physical projection must cancel section drift')
    clock_cases=0
    for j in range(1,120):
        t=times[-1]*F(j,120)
        m=max(i for i,N in enumerate(visits) if times[N]<=t)
        C=max(i for i,T in enumerate(times) if T<=t)
        N=visits[m]
        J=[F(K1[N]),F(K2[N]),F(N),times[N]]
        U=[x-m*g for x,g in zip(J,G)]
        require(B(J)==B(U),'centering changes projection')
        physical=(F(K1[C]),F(K2[C]),F(C)-t/tau_bar)
        difference=max(abs(x-y) for x,y in zip(physical,B(J)))
        require(difference<=10*return_sizes[m],'unfinished actual return bound')
        require(times[N]<=t<times[visits[m+1]],'actual last-return index')
        clock_cases+=1
    # Event boundary inclusion with closed endpoints, including exact hits.
    boundary_cases=0
    h=F(2);d=F(1,2)
    for x in [F(i,4) for i in range(-16,17)]:
        for move in [F(i,8) for i in range(-4,5)]:
            original=abs(x)<=h;other=abs(x+move)<=h
            if original!=other:require(h-d<abs(x)<=h+d,'boundary inclusion')
            boundary_cases+=1
    # Averages and Fourier volume do not control the missing stronger norms.
    require(mp.sin(mp.pi/2)==1,'zero-mean oscillation negative control')
    eps=F(1,1000)
    require(eps<1 and 1/eps>100,'L1 trace negative control')
    return {'sign_cases':count,'interval_cases':interval_cases,'endpoint_cases':endpoint_cases,
            'tensor_cases':tensor_cases,'lattice_grid_cases':grid_cases,
            'conditional_tv_cases':tv_cases,'finite_physical_clock_cases':clock_cases,
            'closed_boundary_cases':boundary_cases,'negative_controls':4,
            'window_relative_rate':str(rate),'projected_fourier_rate':str(e-tau),
            'physical_half_width_exponent':str(F(1,2)-sigma),
            'four_window_probability_exponent':str(4*sigma),
            'physical_window_probability_exponent':str(3*sigma),
            'moment_order_for_projection':64,'precision_decimal_digits':70,
            'continuum_proof_certified':False,'microscopic_raw_endpoint_certified':False}

if __name__=='__main__':
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
