#!/usr/bin/env python3
"""Executed finite diagnostics, not interval certificates or continuum proofs.

No repository implementation is imported. Exact identities, finite stationary
segments, relative cofactors, and physical residual-time quadratures are checked
separately. All failure conditions remain active in optimized Python.
"""
from __future__ import annotations
import json
import math
import platform
from fractions import Fraction
from collections import Counter
import numpy as np
import scipy
import sympy as sp
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

CHECKS=[]

def require(ok, name, category, value=None):
    if not bool(ok):
        raise RuntimeError(f'{category}: {name}: {value}')
    item={'name':name,'category':category,'passed':True}
    if value is not None: item['value']=value
    CHECKS.append(item)


def graph(y, params):
    k,a,q=params
    return k*y*y/2+a*y**3/6+q*y**4/24, k*y+a*y*y/2+q*y**3/6, k+a*y+q*y*y/2


def edges(y,g,coeff,start=0):
    idx=(np.arange(len(y))+start)%2
    k=np.array([coeff[i][0] for i in idx]); aa=np.array([coeff[i][1] for i in idx]); q=np.array([coeff[i][2] for i in idx])
    p=k*y*y/2+aa*y**3/6+q*y**4/24
    dp=k*y+aa*y*y/2+q*y**3/6
    ddp=k+aa*y+q*y*y/2
    s=p[:-1]+p[1:]; x=g+s; v=y[1:]-y[:-1]
    L=np.sqrt(x*x+v*v)
    nu=x*dp[:-1]-v; nv=x*dp[1:]+v
    gu=nu/L; gv=nv/L
    huu=(dp[:-1]**2+x*ddp[:-1]+1)/L-nu*nu/L**3
    hvv=(dp[1:]**2+x*ddp[1:]+1)/L-nv*nv/L**3
    huv=(dp[:-1]*dp[1:]-1)/L-nu*nv/L**3
    excess=(2*g*s+s*s+v*v)/(L+g)
    return excess,gu,gv,huu,hvv,huv


def quadratic(g,coeff,j,start=0):
    cs=np.array([1+g*c[0] for c in coeff]); c=math.sqrt(cs.prod()); gam=math.acosh(c)
    ids=(np.arange(j+1)+start)%2; sig=np.sqrt(cs[1-ids])
    def sr(n):
        n=np.asarray(n,dtype=float)
        return np.exp((n-j)*gam)*(-np.expm1(-2*n*gam))/(-math.expm1(-2*j*gam))
    il=np.arange(j+1)
    L=np.stack((sig/sig[0]*sr(j-il),sig/sig[j]*sr(il)),axis=1)
    coth=1+2*math.exp(-2*j*gam)/(-math.expm1(-2*j*gam))
    csch=2*math.exp(-j*gam)/(-math.expm1(-2*j*gam))
    H=c*math.sinh(gam)/g*np.array([[coth/sig[0]**2,-csch/(sig[0]*sig[j])],[-csch/(sig[0]*sig[j]),coth/sig[j]**2]])
    return gam,L,H


def bridge(g,coeff,j,u,v,start=0):
    gam,L,H=quadratic(g,coeff,j,start)
    y=L@np.array([u,v]); y[0]=u; y[-1]=v
    for it in range(30):
        ex,gu,gv,huu,hvv,huv=edges(y,g,coeff,start)
        if j==1: break
        grad=gv[:-1]+gu[1:]
        if np.max(abs(grad))<2e-15: break
        diag=hvv[:-1]+huu[1:]; off=huv[1:-1]
        ab=np.zeros((3,j-1)); ab[1]=diag
        if j>2: ab[0,1:]=off; ab[2,:-1]=off
        y[1:-1]-=solve_banded((1,1),ab,grad,check_finite=False)
    else: raise RuntimeError('Newton iteration failed')
    ex,gu,gv,huu,hvv,huv=edges(y,g,coeff,start)
    grad=gv[:-1]+gu[1:]
    if len(grad) and np.max(abs(grad))>8e-14: raise RuntimeError('Stationarity tolerance')
    # Relative determinant by positive tridiagonal pivots, not W_uv / a rounded Schur entry.
    diag=hvv[:-1]+huu[1:]; off=huv[1:-1]
    z=edges(np.zeros(j+1),g,coeff,start)
    diag0=z[4][:-1]+z[3][1:]; off0=z[5][1:-1]
    ldet=0.0; last=last0=0.0
    for i in range(j-1):
        pp=diag[i]-(off[i-1]**2/last if i else 0)
        pp0=diag0[i]-(off0[i-1]**2/last0 if i else 0)
        if min(pp,pp0)<=0: raise RuntimeError('Nonpositive Hessian pivot')
        ldet+=math.log(pp/pp0); last,last0=pp,pp0
    if np.min(-huv)<=0: raise RuntimeError('Nonpositive edge twist')
    logb=float(np.log(g*(-huv)).sum())-ldet
    return {'y':y,'E':float(ex.sum()),'logb':logb,'b':math.exp(logb),'grad':float(np.max(abs(grad))) if len(grad) else 0.0,'H':H}


def quartic_finite(g,k,j):
    cf=((k,0,3),(k,0,3)); gam,L,H=quadratic(g,cf,j)
    M=np.linalg.inv(H); vals=np.einsum('ij,jk,ik->i',L,M,L)
    i=np.arange(1,j)
    Gdiag=g*(-np.expm1(-2*i*gam))*(-np.expm1(-2*(j-i)*gam))/(2*math.sinh(gam)*(-math.expm1(-2*j*gam)))
    return -float(Gdiag@vals[1:-1])/3-float(vals[0]**2+vals[-1]**2+2*(vals[1:-1]**2).sum())/24


def probability_normalized(g,cf,j,d,na=40,nr=14):
    _,_,H=quadratic(g,cf,j); w,Q=np.linalg.eigh(H)
    trans=Q@np.diag(1/np.sqrt(w))@Q.T
    rr,ww=leggauss(nr); total=0.
    for th in np.arange(na)*(2*math.pi/na):
        ray=math.sqrt(2*d)*trans@np.array([math.cos(th),math.sin(th)])
        def ev(r): return bridge(g,cf,j,*(r*ray))
        bound=brentq(lambda r:ev(r)['E']/d-1,.5,1.5,xtol=5e-14)
        radii=(rr+1)*bound/2; weights=ww*bound/2
        for r,wt in zip(radii,weights):
            ans=ev(r);total+=(2*math.pi/na)*wt*r*(1-ans['E']/d)*ans['b']
    return 2*total/math.pi


def main():
    z=sp.symbols('z',positive=True)
    f=z*z/(4-z*z)
    require(sp.simplify(sp.diff(f,z,2)-8*(4+3*z*z)/(4-z*z)**3)==0,'strict convexity derivative','exact_symbolic')
    lam,a=sp.symbols('lambda a',positive=True)
    db=-(lam**2/(1-lam**2)-lam**4/(1-lam**4))/(2*a)
    require(sp.simplify(db+lam**2/(2*a*(1-lam**4)))==0,'halfline log determinant coefficient','exact_symbolic')
    t=(1+lam**4)/(1-lam**4)
    target=-(1+lam**4+4*lam**2)/(12*a*a*(1-lam**4))
    require(sp.simplify(2*db/(3*a)-t/(12*a*a)-target)==0,'quartic total coefficient','exact_symbolic')
    lam0=2-sp.sqrt(3)
    require(sp.simplify(-24*target.subs({a:sp.sqrt(3),lam:lam0})-sp.sqrt(3)/2)==0,'physical fiber derivative sqrt3/2','exact_symbolic')
    th,s,b=sp.symbols('theta s b',real=True)
    support=1+s*sp.sin(th)**4+b*sp.sin(th)**6
    for theta in [0,sp.pi]:
        for der,expected in [(0,1),(1,0),(2,0),(4,24*s)]:
            require(sp.simplify(sp.diff(support,th,der).subs(th,theta)-expected)==0,f'support contact {theta} jet {der}','exact_symbolic')
    for pow_,integral in [(4,3*sp.pi/4),(6,5*sp.pi/8)]:
        require(sp.integrate(sp.sin(th)**pow_,(th,0,2*sp.pi))==integral,f'area compensator integral {pow_}','exact_symbolic')
    require(sp.Rational(-6,5)*(5*sp.pi/8)+3*sp.pi/4==0,'analytic area tangent','exact_symbolic')
    for m in range(1,9):
        weights=[Fraction((-1)**(l-1)*math.comb(m,l)) for l in range(1,m+1)]
        for r in range(m):
            val=sum(weights[l-1]*l**r for l in range(1,m+1))
            require(val==int(r==0),f'offset weights m={m},degree={r}','exact_rational')
        require(sum(weights[l-1]/l for l in range(1,m+1))==sum(Fraction(1,l) for l in range(1,m+1)),f'timing harmonic sum m={m}','exact_rational')
    nonlinear=[]
    for case,(g,cf) in enumerate([(.4,((1.3,.7,3.),(2.1,-.9,4.))),(.25,((.8,-.2,4.),(1.5,.5,6.))),(1.,((1.,0.,3.),(1.,0.,3.))) ]):
        u,v=.07,-.055
        for parity in [0,1]:
            # Separate long segments with a zero remote endpoint approximate each half-line.
            left=bridge(g,cf,96,u,0.,start=0)
            right=bridge(g,cf,96,v,0.,start=parity)
            targetE=left['E']+right['E'];targetB=left['logb']+right['logb']
            records=[]
            for basej in [4,8,12,20,32,48]:
                j=basej+parity
                q=bridge(g,cf,j,u,v)
                e=abs(q['E']-targetE); bb=abs(q['logb']-targetB)
                records.append({'j':j,'action_error':e,'log_relative_flux_error':bb})
                require(q['grad']<8e-14,f'nonlinear stationary residual case={case} j={j}','floating_nonlinear',q['grad'])
                require(e<.1*math.exp(-.2*j)+2e-12,f'boundary action gluing case={case} j={j}','floating_nonlinear',e)
                require(bb<.5*math.exp(-.2*j)+2e-11,f'relative determinant gluing case={case} j={j}','floating_nonlinear',bb)
            require(records[-1]['action_error']<1e-10,f'long action split case={case} parity={parity}','floating_nonlinear')
            require(records[-1]['log_relative_flux_error']<1e-9,f'long relative split case={case} parity={parity}','floating_nonlinear')
            nonlinear.append({'case':case,'parity':parity,'records':records,'halfline_cutoff':96})
    quartic=[]
    for g,k in [(.2,.8),(.4,1.3),(1.,1.),(2.,3.)]:
        gam=math.acosh(1+g*k);a=math.sinh(gam)/g
        target=-(math.cosh(2*gam)+2)/(12*a*a*math.sinh(2*gam))
        vals=[]
        for j in [1,2,3,8,17,32,63,128]:
            q=quartic_finite(g,k,j); vals.append([j,q])
            require(q<0,f'quartic sensitivity sign g={g} j={j}','floating_algebra',q)
        require(abs(vals[-1][1]-target)<2e-12,f'quartic halfline limit g={g}','floating_algebra',vals[-1][1]-target)
        quartic.append({'g':g,'kappa':k,'finite':vals,'limit':target})
    quadrature=[]
    for j in [1,3,9]:
        pred=quartic_finite(1.,1.,j)
        errors=[]
        for d in [3e-4,1e-4]:
            dq=.1
            plus=probability_normalized(1.,((1.,0.,3+dq),)*2,j,d)
            minus=probability_normalized(1.,((1.,0.,3-dq),)*2,j,d)
            observed=(plus-minus)/(2*dq*d)
            err=abs(observed-pred)
            require(err<.05*d+3e-8,f'full residual-time quartic derivative j={j} d={d}','floating_quadrature',err)
            errors.append(err)
            quadrature.append({'j':j,'offset':d,'predicted':pred,'measured':observed,'absolute_error':err})
        require(errors[1]<.35*errors[0]+2e-8,f'integer-power quartic bias j={j}','floating_quadrature')
        refined=(probability_normalized(1.,((1.,0.,3.1),)*2,j,1e-4,64,20)-probability_normalized(1.,((1.,0.,2.9),)*2,j,1e-4,64,20))/(2e-5)
        require(abs(refined-quadrature[-1]['measured'])<2e-8,f'quadrature refinement j={j}','floating_quadrature',abs(refined-quadrature[-1]['measured']))
    # Nonlinear response is not inserted into the integration density.
    R=.3;g=1-2*R;A0=math.sqrt(3)/2-math.pi*R*R;xstar=R/(R+g)
    baseline=np.array([3/(A0*math.sinh(j*math.acosh(1+g/R))) for j in range(1,65)])
    coalescence=[]
    for s0 in [2e-4,1e-4,5e-5,2e-5,-1e-4]:
        radii=R+np.array([36,-18,-18])*s0; ks=1/radii;gamma=np.arccosh(1+g/radii);A=A0+45*math.pi*s0*s0/4
        C=np.array([np.sum(1/np.sinh(j*gamma))/A for j in range(1,65)])
        m=2*C[1]/C[0]; J=C[2]/C[0]-m*m/(4-m*m)
        x=1/(1+g*ks);weights=(1/np.sinh(gamma));weights/=weights.sum()
        variance=float(weights@((x-m)**2));proxy=abs(m-xstar)+math.sqrt(max(J,0));distance=float(np.max(abs(ks-1/R)))
        require(J>0,f'positive amplitude dispersion s={s0}','floating_algebra',J)
        require(abs(m-float(weights@x))<2e-15,f'amplitude first ratio s={s0}','floating_algebra')
        require(.01<J/variance<1.,f'Jensen dispersion bounds s={s0}','floating_algebra',J/variance)
        require(1<distance/proxy<300,f'circular-reference conditioning s={s0}','floating_algebra',distance/proxy)
        norm=float(np.max(np.exp(.2*np.arange(1,65))*abs(C-baseline)))
        require(1e3<norm/s0**2<1e7,f'weighted quadratic loss s={s0}','floating_algebra',norm/s0**2)
        coalescence.append({'s':s0,'dispersion':J,'curvature_distance':distance,'finite_weighted_norm':norm,'quadratic_ratio':norm/s0**2,'prefix':64})
    counts=dict(sorted(Counter(x['category'] for x in CHECKS).items()))
    print(json.dumps({'status':'PASS','total_checks':len(CHECKS),'counts':counts,'checks':CHECKS,
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
        'nonlinear_factorization':nonlinear,'quartic_sensitivity':quartic,'physical_quadrature':quadrature,'coalescence':coalescence,
        'limits':['Finite checks do not prove the continuum theorems.','Numerical calculations are not interval certified.','The half-line comparison uses a stated finite cutoff, not an infinite computation.','The sequence test covers a finite prefix; the proof of the infinite bound is analytical.','The local stationary-segment quadrature is not a full periodic-equilibrium simulation.']},indent=2,sort_keys=True))

if __name__=='__main__': main()
