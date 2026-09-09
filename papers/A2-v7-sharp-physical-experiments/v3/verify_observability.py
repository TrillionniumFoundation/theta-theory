#!/usr/bin/env python3
"""Finite exact and non-interval diagnostics for the v3 observability proofs.

No repository modules are imported. The local graph quadratures do not simulate
full-phase equilibrium in the complete periodic billiard. The uniform theorems
are proved in the manuscript, not inferred from this finite suite.
Dependencies: numpy, scipy, sympy. All checks survive python -O.
"""
from __future__ import annotations
from fractions import Fraction as Q
import json
import math
import platform
import numpy as np
import scipy
import sympy as sp
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

COUNTS: dict[str, int] = {}

def check(condition: bool, label: str, group: str) -> None:
    if not bool(condition):
        raise RuntimeError(f'{group}: {label}')
    COUNTS[group] = COUNTS.get(group, 0) + 1


def schur(g: Q, c0: Q, c1: Q, j: int) -> np.ndarray:
    """Eliminate all interior nodes of the exact tridiagonal action."""
    a = c0/g
    e = -1/g
    pivot = (c1 if j == 1 else 2*c1)/g
    for i in range(1, j):
        a -= e*e/pivot
        e = e/(g*pivot)
        nxt = c0 if (i+1) % 2 == 0 else c1
        pivot = (nxt if i+1 == j else 2*nxt)/g - 1/(g*g*pivot)
    return np.array([[a, e], [e, pivot]], dtype=object)


def chebyshev(c: Q, j: int) -> tuple[Q, Q]:
    t0,t1=Q(1),c
    u0,u1=Q(0),Q(1)
    for _ in range(1,j):
        t0,t1=t1,2*c*t1-t0
        u0,u1=u1,2*c*u1-u0
    return t1,u1


def coth(x: float) -> float:
    return 1.0 + 2.0*math.exp(-2*x)/(-math.expm1(-2*x))


def observation(g: float, k0: float, k1: float, j: int) -> np.ndarray:
    c0,c1=1+g*k0,1+g*k1
    gamma=math.acosh(math.sqrt(c0*c1))
    f=g*coth(j*gamma)/(3*math.sinh(gamma))
    return f*np.array([math.sqrt(c1/c0), math.sqrt(c0/c1)])


def recover(g: float, v: np.ndarray, j: int) -> np.ndarray:
    target=3*math.sqrt(v[0]*v[1])/g
    f=lambda z:coth(j*z)/math.sinh(z)-target
    hi=1.0
    while f(hi)>0:
        hi *= 2
        if hi>128: raise RuntimeError('Cannot bracket inverse')
    gamma=brentq(f,1e-10,hi,xtol=2e-14)
    r=math.sqrt(v[1]/v[0]);c=math.cosh(gamma)
    return np.array([(r*c-1)/g,(c/r-1)/g])


def graph(y, coefficients):
    k,a,b=coefficients
    return k*y*y/2+a*y**3/6+b*y**4/24, k*y+a*y*y/2+b*y**3/6, k+a*y+b*y*y/2


def local_segment(g, coeffs, j, u, v):
    """Newton Dirichlet solve; stable excess and log-relative cofactor."""
    c0,c1=(1+g*cf[0] for cf in coeffs)
    c=math.sqrt(c0*c1);gamma=math.acosh(c)
    index=np.arange(j+1)
    sigma=np.sqrt(np.where(index%2==0,c1,c0))
    ratio=lambda n:np.exp(-gamma*(j-n))*(-np.expm1(-2*gamma*n))/(-math.expm1(-2*gamma*j))
    y=sigma*(ratio(j-index)*u/sigma[0]+ratio(index)*v/sigma[-1])
    cf=np.array([coeffs[i%2] for i in range(j+1)]).T
    def jets():
        p,dp,ddp=graph(y,cf)
        w=g+p[:-1]+p[1:];dv=y[1:]-y[:-1]
        length=np.hypot(w,dv)
        au=w*dp[:-1]-dv;av=w*dp[1:]+dv
        gu=au/length;gv=av/length
        huu=(1+dp[:-1]**2+w*ddp[:-1])/length-au**2/length**3
        hvv=(1+dp[1:]**2+w*ddp[1:])/length-av**2/length**3
        cross=(dp[:-1]*dp[1:]-1)/length-au*av/length**3
        sums=p[:-1]+p[1:]
        excess=(2*g*sums+sums*sums+dv*dv)/(length+g)
        return excess,gu,gv,huu,hvv,cross
    for iteration in range(20):
        ex,gu,gv,huu,hvv,cross=jets()
        residual=gu[1:]+gv[:-1]
        if not len(residual) or np.max(abs(residual))<3e-15: break
        band=np.zeros((3,j-1));band[1]=huu[1:]+hvv[:-1]
        if j>2:
            band[0,1:]=cross[1:-1];band[2,:-1]=cross[1:-1]
        y[1:-1]-=solve_banded((1,1),band,residual)
    else: raise RuntimeError('Stationary bridge failed to converge')
    ex,gu,gv,huu,hvv,cross=jets()
    residual=gu[1:]+gv[:-1]
    if len(residual) and np.max(abs(residual))>1e-12:
        raise RuntimeError('Nonstationary quadrature segment')
    if np.any(cross>=0):raise RuntimeError('Nonpositive local twist')
    logdet=0.
    if j>1:
        diagonal=huu[1:]+hvv[:-1]
        pivot=diagonal[0]
        if pivot<=0: raise RuntimeError('Nonpositive first pivot')
        logdet=math.log(pivot)
        for i in range(1,j-1):
            pivot=diagonal[i]-cross[i]**2/pivot
            if pivot<=0:raise RuntimeError('Nonpositive pivot')
            logdet+=math.log(pivot)
    logtwist=float(np.log(-cross).sum())-logdet
    logsinh=j*gamma+math.log1p(-math.exp(-2*j*gamma))-math.log(2)
    logtwist0=math.log(c*math.sinh(gamma)/(g*sigma[0]*sigma[-1]))-logsinh
    csch=2*math.exp(-j*gamma)/(-math.expm1(-2*j*gamma))
    hfactor=c*math.sinh(gamma)/g
    H=hfactor*np.array([[coth(j*gamma)/sigma[0]**2,-csch/(sigma[0]*sigma[-1])],
                       [-csch/(sigma[0]*sigma[-1]),coth(j*gamma)/sigma[-1]**2]])
    return float(ex.sum()),logtwist-logtwist0,H


def conditional_variances(g, coefficients, j, d):
    _,_,H=local_segment(g,coefficients,j,0.,0.)
    eig,U=np.linalg.eigh(H);T=(U/np.sqrt(eig))@U.T
    points,weights=leggauss(12)
    integral=np.zeros(9)
    for theta in (np.arange(24)+.5)*2*np.pi/24:
        direction=T@np.array([np.cos(theta),np.sin(theta)])
        energy=lambda radius:local_segment(g,coefficients,j,*(radius*direction))[0]
        upper=brentq(lambda radius:energy(radius)-d,.5*math.sqrt(2*d),2*math.sqrt(2*d),xtol=1e-14)
        for node,weight in zip(points,weights):
            rad=(node+1)*upper/2
            u,v=rad*direction
            excess,logb,_=local_segment(g,coefficients,j,u,v)
            p=graph(u,coefficients[0])[0];q=graph(v,coefficients[j%2])[0]
            vector=np.array([1,u,v,u*u,v*v,p,q,p*p,q*q])
            integral+=weight*upper/2*rad*(d-excess)*math.exp(logb)*vector
    # Common polar Jacobian and angular weights cancel exactly from the ratio.
    mean=integral/integral[0]
    var=np.array([mean[3]-mean[1]**2+mean[7]-mean[5]**2,
                  mean[4]-mean[2]**2+mean[8]-mean[6]**2])/d
    target=np.diag(np.linalg.inv(H))/3
    return var,target


def main() -> None:
    exact_configurations=[(Q(1,5),Q(3,2),Q(8,3),Q(2)),
                          (Q(2,7),Q(4,3),Q(3),Q(2)),
                          (Q(1,10),Q(5,4),Q(5,4),Q(5,4))]
    for g,c0,c1,c in exact_configurations:
        for j in [1,2,3,7,8,31,63,127]:
            H=schur(g,c0,c1,j)
            determinant=H[0,0]*H[1,1]-H[0,1]**2
            inv=np.array([[H[1,1],-H[0,1]],[-H[1,0],H[0,0]]],dtype=object)/determinant
            t,u=chebyshev(c,j)
            sigma0=c1; sigma1=c0 if j%2 else c1
            expected0=g*sigma0*t/(3*c*(c*c-1)*u)
            expected1=g*sigma1*t/(3*c*(c*c-1)*u)
            check(inv[0,0]/3==expected0,'first covariance diagonal','exact_metric')
            check(inv[1,1]/3==expected1,'last covariance diagonal','exact_metric')
            if j%2:
                check(expected1/expected0==c0/c1,'curvature ratio','exact_metric')
                check(expected0*expected1==(g*t/(3*(c*c-1)*u))**2,'curvature product','exact_metric')
            else:check(expected0==expected1,'even parity coincidence','exact_metric')
    c0,c1,g=sp.symbols('c0 c1 g',positive=True)
    vv=sp.Matrix([g*c1/(3*(c0*c1-1)),g*c0/(3*(c0*c1-1))])
    det=sp.factor(vv.jacobian([c0,c1]).det())
    check(sp.simplify(det-g*g*(c0*c1+1)/(9*(c0*c1-1)**3))==0,'one-flight Jacobian','exact_symbolic')
    rr=sp.symbols('r',nonnegative=True)
    check(sp.integrate(4*rr*(1-rr**2),(rr,0,1))==1,'disk normalization','exact_symbolic')
    check(sp.integrate(4*rr**3*(1-rr**2),(rr,0,1))/2==sp.Rational(1,6),'disk second moment','exact_symbolic')
    R,al,be,ze=sp.symbols('R alpha beta zeta',real=True)
    area=(R+al)**2+( -35*al**2+(-3-sp.Rational(15,4)-sp.Rational(63,4))*(be**2+ze**2))/2
    expected=R**2+2*R*al-sp.Rational(33,2)*al**2-sp.Rational(45,4)*(be**2+ze**2)
    check(sp.expand(area-expected)==0,'area Fourier coefficients','exact_symbolic')
    bvals=[al+be,al-be/2+sp.sqrt(3)*ze/2,al-be/2-sp.sqrt(3)*ze/2]
    check(sp.simplify(sum(bvals)/3-al)==0,'curvature mean','exact_symbolic')
    check(sp.simplify(sp.Rational(2,3)*sum((b-al)**2 for b in bvals)-be**2-ze**2)==0,'curvature symmetric variance','exact_symbolic')
    theta=sp.symbols('theta',real=True)
    ch0=(1+sp.cos(theta))*sp.sin(theta)**2/4
    ch1=(1-sp.cos(theta))*sp.sin(theta)**2/4
    chs=sp.sin(theta)**4
    for i,chi in enumerate([ch0,ch1,chs]):
        for k,point in enumerate([0,sp.pi]):
            for order in [0,1,2]:
                target=1 if order==2 and i==k else 0
                check(sp.simplify(sp.diff(chi,theta,order).subs(theta,point)-target)==0,'fiber contact jet','exact_symbolic')
    A,B,C=sp.symbols('A B C',real=True)
    normalized_area=(1+(A+B)/8+3*C/8)**2-sp.Rational(3,2)*((A+B)/8+C/2)**2-4*((A-B)/16)**2-sp.Rational(15,2)*(C/8)**2
    check(sp.diff(normalized_area,C).subs({A:0,B:0,C:0})==sp.Rational(3,4),'area compensation transversality','exact_symbolic')
    h=1+A*ch0+B*ch1+C*chs
    hf=1+(A+B)/8+3*C/8+(A-B)*sp.cos(theta)/16-((A+B)/8+C/2)*sp.cos(2*theta)-(A-B)*sp.cos(3*theta)/16+C*sp.cos(4*theta)/8
    # Numeric evaluation is not used to assert the trigonometric identity.
    check(sp.trigsimp(sp.expand_trig(h-hf))==0,'explicit fiber Fourier expansion','exact_symbolic')
    ph=sp.Function('Phi');s=sp.symbols('s',real=True);A0=sp.symbols('A0',positive=True)
    amplitude=(ph(R+36*s)+2*ph(R-18*s))/(A0+45*sp.pi*s*s/4)
    check(sp.simplify(sp.diff(amplitude,s).subs(s,0))==0,'unlabelled circular first derivative','exact_symbolic')
    inversion=[]
    for gf,k0,k1 in [(.05,.5,.5),(.12,2.1,2.5),(.12,2.5,2.1),(.8,.3,12.),(.3,4.,4.+1e-8)]:
        maximum=0.
        for j in [1,3,9,31,127,511]:
            value=observation(gf,k0,k1,j);estimate=recover(gf,value,j)
            error=float(np.max(abs(estimate-np.array([k0,k1]))))
            check(error<1e-9,'explicit inverse','floating_inverse')
            maximum=max(maximum,error)
            eps=1e-6
            J=np.column_stack([(observation(gf,k0+(i==0)*eps,k1+(i==1)*eps,j)-observation(gf,k0-(i==0)*eps,k1-(i==1)*eps,j))/(2*eps) for i in range(2)])
            check(np.min(np.linalg.svd(J,compute_uv=False))>1e-6,'finite Jacobian lower bound','floating_inverse')
        inversion.append({'g':gf,'curvatures':[k0,k1],'max_inverse_error':maximum})
    fiber=[]
    area_function=sp.lambdify((A,B,C),normalized_area,'numpy')
    curvature_function=sp.lambdify((theta,A,B,C),h+sp.diff(h,theta,2),'numpy')
    for sf in [-.015,-.0075,0.,.0075,.015]:
        c0f,c1f=2*math.exp(sf),2*math.exp(-sf)
        af,bf=1/(c0f-1)-1,1/(c1f-1)-1
        cf=brentq(lambda z:float(area_function(af,bf,z)-1),-.05,.05,xtol=1e-14)
        check(abs(area_function(af,bf,cf)-1)<1e-13,'constant exact target area','floating_fiber')
        rad=curvature_function(np.linspace(0,2*np.pi,4001),af,bf,cf)
        check(np.min(rad)>.8,'sampled positive curvature radius','floating_fiber')
        # The continuum positivity is by openness in the proof, not this grid.
        for j in [1,3,17,127]:
            vf=observation(1.,c0f-1,c1f-1,j)
            check(abs(vf[1]/vf[0]-math.exp(2*sf))<1e-13,'record separates scalar fiber','floating_fiber')
            check(abs(c0f*c1f-4)<2e-14,'scalar product fixed','floating_fiber')
        fiber.append({'s':sf,'area_compensator':cf,'sampled_min_curvature_radius':float(min(rad))})
    quadrature=[]
    for case in [(.12,((2.1,.8,40.),(2.5,-.5,30.))),(.2,((3.,1.,20.),(3.,-.6,25.)))]:
        gf,cf=case
        for j in [1,3,31]:
            values=[];errors=[]
            for d in [1e-4,2.5e-5]:
                var,target=conditional_variances(gf,cf,j,d)
                err=float(np.max(abs(var-target)))
                check(err<.001,'physical variance leading coefficient','floating_quadrature')
                check(np.max(abs(recover(gf,var,j)-np.array([cf[0][0],cf[1][0]])))<.03,'finite-offset inversion','floating_quadrature')
                values.append({'offset':d,'variance':var.tolist(),'limit':target.tolist(),'absolute_error':err})
                errors.append(err)
            check(errors[1]<.35*errors[0]+1e-9,'integer-power bias reduction','floating_quadrature')
            quadrature.append({'g':gf,'curvatures':[cf[0][0],cf[1][0]],'j':j,'values':values})
    print(json.dumps({'status':'PASS','schema':'a2-v3-observability-checks-v1','checks':COUNTS,
        'total_checks':sum(COUNTS.values()),'python':platform.python_version(),
        'libraries':{'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__},
        'inverse_checks':inversion,'realized_fiber_checks':fiber,'endpoint_quadratures':quadrature,
        'limitations':['Finite diagnostics, not a continuum proof or formal certificate.',
            'Floating inversions and quadratures are not interval-certified.',
            'Local graph quadrature is not a full-equilibrium periodic billiard simulation.',
            'Curvature positivity on the full family follows analytically from openness, not the sampled grid.']},indent=2,sort_keys=True))

if __name__=='__main__': main()
