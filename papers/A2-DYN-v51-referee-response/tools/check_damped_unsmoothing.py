#!/usr/bin/env python3
"""Finite algebra and finite-state regressions, never continuum proof certification."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
from math import comb
import numpy as np


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def centered_binomial_moments(m: int, prob: F, order: int) -> list[F]:
    return [sum((F(comb(m,k))*prob**k*(1-prob)**(m-k)*(F(k)-m*prob)**j
                 for k in range(m+1)),F(0)) for j in range(order+1)]


def cumulants(mom: list[F]) -> list[F]:
    out=[F(0)]
    for n in range(1,len(mom)):
        out.append(mom[n]-sum((F(comb(n-1,j-1))*out[j]*mom[n-j]
                              for j in range(1,n)),F(0)))
    return out


def moments_from_cumulants(cum: list[F]) -> list[F]:
    out=[F(1)]
    for n in range(1,len(cum)):
        out.append(sum((F(comb(n-1,j-1))*cum[j]*out[n-j]
                        for j in range(1,n+1)),F(0)))
    return out


def finite_checks() -> dict:
    eps,theta,alpha=F(1,21),F(1,5),F(3)
    Q,p=19,10
    rate=F(p,4*p+1)
    margins={
      'analytic_disk':F(1,2)-eps-2*theta,
      'spectral_remainder':(Q-1)*(F(1,2)-eps)-2*(Q+1)*theta,
      'insertion':alpha-4*eps,
      'fine_product_replacement':alpha-F(3,2)-7*eps,
      'quartic_pair_term':2*theta-8*eps,
      'quartic_single_cumulant':1+theta-8*eps,
      'clock_probability_integrated':rate-4*eps,
      'clock_phase_integrated':rate-5*eps,
    }
    expected={'analytic_disk':F(11,210),'spectral_remainder':F(1,7),
      'insertion':F(59,21),'fine_product_replacement':F(7,6),
      'quartic_pair_term':F(2,105),'quartic_single_cumulant':F(86,105),
      'clock_probability_integrated':F(46,861),'clock_phase_integrated':F(5,861)}
    require(margins==expected and all(x>0 for x in margins.values()),'incorrect scale margin')
    b=F(2*p+1,4*p+1)
    require(2*p*b-p==(1-b)/2==rate,'clock optimization')
    require(F(1,2)-eps==F(19,42) and 2-4*F(1,2)==0,'raw Jacobian or cutoff')
    require(4*eps==F(4,21) and F(1,2)+eps==F(23,42),'Schwartz prefactors')
    require(2*eps==F(2,21),'Gaussian tail exponent')
    require(F(3,280)>F(5,861)>F(1,200),'old/new central rates')
    require(F(59,21)>F(9,175) and F(2,105)>F(5,861),'variation/log absorption')
    general=[]
    for e in [F(1,30),F(1,25),F(1,21),F(49,1000),F(499,10000)]:
        t=(4*e+F(1,4)-e/2)/2
        pp=2
        while F(pp,4*pp+1)<=5*e: pp+=1
        qq=3
        while (qq-1)*(F(1,2)-e)<=2*(qq+1)*t: qq+=1
        require(4*e<t<F(1,4)-e/2,'empty coarse-scale interval')
        require(F(3,2)-7*e>F(pp,4*pp+1)-5*e,'fine scale insufficient')
        general.append({'epsilon':str(e),'theta':str(t),'fixed_clock_moment':2*pp,'fixed_spectral_degree':qq})
    # Independent exact finite generating-polynomial checks through degree 20.
    moment_cases=0
    for prob in [F(1,2),F(1,7),F(1,100)]:
        single=cumulants(centered_binomial_moments(1,prob,20))
        for m in [1,2,5,8,16]:
            mom=centered_binomial_moments(m,prob,20);cum=cumulants(mom)
            require(cum==[m*x for x in single],'independent cumulant length identity')
            require(moments_from_cumulants(cum)==mom,'moment/cumulant reconstruction')
            require(mom[1]==0,'residual not centered')
            moment_cases+=20
    residual_cases=0
    for delta in [F(1,10),F(1,100),F(1,1000)]:
        for m in [1,2,8,32,64]:
            fourth=centered_binomial_moments(m,delta,4)[4]
            var=delta*(1-delta)
            require(fourth==m*var*(1-6*var)+3*m*m*var*var,'small residual fourth identity')
            require(fourth<=m*delta+3*m*m*delta*delta,'finite small-mass fourth bound')
            residual_cases+=1
    # A nonreversible doubly stochastic Markov chain: a finite test of the
    # chronological algebra only, not a replacement for billiard dynamics.
    P=np.array([[.6,.3,.1],[.2,.5,.3],[.2,.2,.6]])
    pi=np.ones(3)/3
    h=np.array([-.4,.1,.3]);u=np.array([-.06,.03,.03])
    mark=np.array([1+.2j,-.4+.1j,.7-.3j])
    require(np.max(np.abs(pi@P-pi))<1e-14 and not np.allclose(P,P.T),'finite model identity')
    word_cases=0;max_word=0.;remainder_cases=0;max_ratio=0.;wrong_chronology=0.
    for m in range(1,5):
        paths=np.array(list(product(range(3),repeat=m+1)),dtype=int)
        weights=pi[paths[:,0]].copy()
        for j in range(m):weights*=P[paths[:,j],paths[:,j+1]]
        phase=np.exp(.37j*h[paths[:,:m]].sum(axis=1))
        L=P.T@np.diag(np.exp(.37j*h))
        powers=[np.linalg.matrix_power(L,j) for j in range(m+1)]
        for k in range(m+1):
            for degree in range(4):
                for times in product(range(m),repeat=degree):
                    point=mark[paths[:,k]].copy()
                    for t in times:point*=u[paths[:,t]]
                    brute=np.sum(weights*phase*point)
                    ins=[(k,mark)]+[(t,u) for t in times]
                    ins.sort(key=lambda x:x[0])
                    vec=pi.astype(complex);last=0
                    for t,fac in ins:
                        vec=fac*(powers[t-last]@vec);last=t
                    value=np.sum(powers[m-last]@vec)
                    err=abs(value-brute);max_word=max(max_word,float(err))
                    require(err<3e-13,'chronological word mismatch')
                    if k==m and degree==0:
                        wrong=np.sum(powers[m]@(mark*pi))
                        wrong_chronology=max(wrong_chronology,float(abs(wrong-brute)))
                    word_cases+=1
            for z in [.03,.37,1.1]:
                coarse=np.exp(1j*z*h[paths[:,:m]].sum(axis=1))
                X=z*u[paths[:,:m]].sum(axis=1)
                poly=1+1j*X-X*X/2-1j*X**3/6
                actual=np.sum(weights*mark[paths[:,k]]*coarse*np.exp(1j*X))
                approx=np.sum(weights*mark[paths[:,k]]*coarse*poly)
                bound=float(np.max(np.abs(mark))*np.sum(weights*X**4)/24)
                err=float(abs(actual-approx))
                require(err<=bound+2e-14,'quartic remainder violated in finite model')
                if bound>1e-12:max_ratio=max(max_ratio,err/bound)
                remainder_cases+=1
    # Explicit negative controls reject the missing single-cumulant term,
    # the old first-order loss, old stopping order, and wrong time ordering.
    require(centered_binomial_moments(1,F(1,1000),4)[4]>10*F(1,1000)**2,'missing lower moment term not detected')
    require(theta/2-5*eps<0,'old first-order loss would incorrectly pass')
    require(F(2,9)-5*eps<0,'old stopping order would incorrectly pass')
    require(F(1,4)-5*F(1,10)<0,'full target falsely covered by stopping family')
    require(wrong_chronology>1e-4,'wrong endpoint chronology not detected')
    return {'exact_margins':{k:str(v) for k,v in margins.items()},
       'general_feasible_fixed_order_choices':general,'moment_cumulant_degree_checks':moment_cases,
       'small_residual_fourth_cases':residual_cases,'chronological_word_cases':word_cases,
       'max_chronological_error':format(max_word,'.3g'),'cubic_remainder_cases':remainder_cases,
       'max_remainder_to_bound_ratio':format(max_ratio,'.6g'),'negative_controls':5,
       'finite_models_are_not_continuum_proofs':True}


if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
