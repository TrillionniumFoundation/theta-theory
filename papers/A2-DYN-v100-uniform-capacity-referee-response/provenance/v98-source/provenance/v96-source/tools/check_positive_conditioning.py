#!/usr/bin/env python3
"""Finite algebra and quadrature checks; none certifies continuum billiard claims."""
from __future__ import annotations
from fractions import Fraction as F
import math
import numpy as np
import sympy as sp


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def finite_checks() -> dict:
    x = sp.symbols('x', real=True)
    inner = 1 - 6*x**2 + 6*x**3
    outer = 2*(1-x)**3
    for order in range(3):
        require(sp.diff(inner,x,order).subs(x,sp.Rational(1,2)) ==
                sp.diff(outer,x,order).subs(x,sp.Rational(1,2)), 'spline join')
        require(sp.diff(outer,x,order).subs(x,1) == 0, 'support-edge derivatives')
    require(inner.subs(x,0)==1 and sp.diff(inner,x).subs(x,0)==0 and
            -sp.diff(inner,x,2).subs(x,0)==12, 'kernel moments')
    require(sp.integrate(inner,(x,0,sp.Rational(1,2)))+
            sp.integrate(outer,(x,sp.Rational(1,2),1))==sp.Rational(3,8), 'kernel value at zero')
    # The fixed-table determinant in the invariant coordinates.
    v,c,cp=sp.symbols('v c cp', positive=True)
    P=sp.Matrix([[(v+c)/cp,v/(c*cp)],[v+c+cp,(v+cp)/c]])
    require(sp.simplify(P.det()-1)==0,'collision determinant')
    # Translation/Taylor optimisation is an identity at every positive scale.
    a,b=sp.symbols('a b', positive=True)
    h=2*sp.sqrt(a/b)
    require(sp.simplify(2*a/h+h*b/2-2*sp.sqrt(a*b))==0,'all-label interpolation')
    # Polynomial compact source used below is normalised and W^{2,1}.
    q=sp.Rational(35,32)*(1-x*x)**3
    require(sp.integrate(q,(x,-1,1))==1,'source mass')
    for side in (-1,1):
        for order in range(3):require(sp.diff(q,x,order).subs(x,side)==0,'source boundary jet')
    a1=sp.Rational(35,16)
    a2=4*abs(sp.diff(q,x).subs(x,1/sp.sqrt(5)))
    require(bool(a1*a1 <= 4*a2),'interpolation model')
    A2=float(a2)
    # Check inverse Fourier normalisation of the piecewise cubic multiplier.
    gn,gw=np.polynomial.legendre.leggauss(160)
    bs=np.concatenate(((gn+1)/4,(gn+3)/4))
    bw=np.concatenate((gw/4,gw/4))
    eta=np.where(bs<=.5,1-6*bs*bs+6*bs**3,2*(1-bs)**3)
    ts=np.linspace(-18,18,91)
    inverse=(np.cos(np.outer(ts,bs))@(bw*eta))/math.pi
    direct=3/(8*math.pi)*np.sinc(ts/(4*math.pi))**4
    err=float(np.max(np.abs(inverse-direct)))
    require(err<3e-14,'kernel Fourier identity')
    # Original-space event likelihood, including strongly oscillating W.
    def rule(lo,hi):
        return lo+(gn+1)*(hi-lo)/2,gw*(hi-lo)/2
    cases=0;min_lik=1.;max_lik=0.;worst_event=0.;worst_fourier=0.
    for B in (2.,7.,20.):
        for lo,hi in ((-.25,.3),(.65,.67),(1.2,1.6)):
            cuts=sorted(set([-1.,1.]+[z for z in (lo,hi) if -1<z<1]))
            ss=[];ww=[]
            for aa,bb in zip(cuts[:-1],cuts[1:]):
                nodes,weights=rule(aa,bb);ss.extend(nodes);ww.extend(weights)
            source=np.array(ss);weights=np.array(ww)*35/32*(1-source**2)**3
            y,yw=rule(lo,hi)
            kb=B*3/(8*math.pi)*np.sinc(B*(y[:,None]-source[None,:])/(4*math.pi))**4
            likelihood=yw@kb
            indicator=((source>=lo)&(source<=hi)).astype(float)
            event_error=float(np.dot(weights,np.abs(indicator-likelihood)))
            require(event_error <= 2*math.sqrt(12)*math.sqrt(A2)/B+1e-12,'event boundary budget')
            require(np.min(likelihood)>-1e-14 and np.max(likelihood)<1+1e-12,'likelihood positivity')
            W=np.exp(1j*(31*source+11*source**2))
            true=np.dot(weights,W*indicator);soft=np.dot(weights,W*likelihood)
            require(abs(true-soft)<=event_error+1e-12,'arbitrary selector contraction')
            # Fubini identity checked against the full source weighted transform.
            bpos=B*bs;bweights=B*bw
            H=np.where(bpos!=0,(np.exp(-1j*bpos*lo)-np.exp(-1j*bpos*hi))/(1j*bpos),hi-lo)
            phip=np.exp(1j*np.outer(bpos,source))@(weights*W)
            phim=np.exp(-1j*np.outer(bpos,source))@(weights*W)
            spectral=np.dot(bweights*eta,H*phip+np.conj(H)*phim)/(2*math.pi)
            require(abs(spectral-soft)<2e-12,'weighted finite-band equality')
            mass=float(np.dot(weights,indicator));massb=float(np.dot(weights,likelihood))
            if mass>0 and massb>0:
                post=float(np.dot(weights,np.abs(indicator/mass-likelihood/massb)))
                require(post<=2*event_error/mass+1e-12,'posterior normalisation')
            cases+=1;min_lik=min(min_lik,float(np.min(likelihood)));max_lik=max(max_lik,float(np.max(likelihood)))
            worst_event=max(worst_event,event_error);worst_fourier=max(worst_fourier,float(abs(spectral-soft)))
    # Exact finite tower verifies the entrance roof bias, not the collision marginal.
    prob=[F(1,2),F(1,4),F(1,4)];roof=[F(1),F(2),F(4)]
    mean=sum(p*t for p,t in zip(prob,roof));rho=[t/mean for t in roof]
    require(sum(p*r for p,r in zip(prob,rho))==1,'stationary bias normalisation')
    require([p*r for p,r in zip(prob,rho)]!=prob,'stationary/section negative control')
    for mask in range(8):
        selected=[bool(mask&(1<<j)) for j in range(3)]
        removed=sum(p*r for p,r,s in zip(prob,rho,selected) if s)
        unweighted=sum(p for p,s in zip(prob,selected) if s)
        require(removed**2 <= unweighted*sum(p*r*r for p,r in zip(prob,rho)),'bias Cauchy-Schwarz')
    exponent_cases=0
    for target in (F(1,10),F(1),F(7)):
        d=32*(target+6)
        for kappa in (F(0),F(1,3),F(5)):
            require(F(1,2)-d/32<=-target-4,'stationary removed-mass exponent')
            require(kappa-(target+kappa+4)==-target-4,'selector bandwidth exponent')
            require(-2*(target+kappa+4)<=-target-4,'density bandwidth exponent')
            exponent_cases+=1
    # Sharp Fourier truncation is not a positive conditional likelihood.
    import mpmath as mp
    sharp=(mp.si(.1-1.5*mp.pi)-mp.si(-.1-1.5*mp.pi))/mp.pi
    require(sharp<0,'sharp-truncation negative control')
    # Small discarded mass alone cannot imply small density supremum.
    for power in range(2,8):
        delta=F(1,10**power);width=delta**3
        require(delta/width>1/delta,'L1-to-Linfinity negative control')
    return {'spline_join_orders':3,'kernel_mass':1,'kernel_second_moment':12,
      'inverse_kernel_samples':len(ts),'inverse_kernel_error':format(err,'.3e'),
      'weighted_interval_cases':cases,'likelihood_range':[round(min_lik,12),round(max_lik,12)],
      'weighted_Fourier_error':format(worst_fourier,'.3e'),'stationary_tower_masks':8,
      'exact_exponent_cases':exponent_cases,'negative_control_families':3,
      'continuum_proof_certified':False}

if __name__=='__main__':
    import json
    print(json.dumps(finite_checks(),indent=2,sort_keys=True))
