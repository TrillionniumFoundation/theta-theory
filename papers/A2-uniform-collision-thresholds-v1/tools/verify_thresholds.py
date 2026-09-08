#!/usr/bin/env python3
"""Finite diagnostics for the collision-threshold revision.

Exact identities are separated from non-interval floating checks. No check
certifies a continuum parameter set or replaces the analytical proofs.
The explicit require() checks remain active with python -O.
"""
from __future__ import annotations
from fractions import Fraction as Q
from math import acosh, cos, exp, log, pi, sin, sqrt
import json
import platform
from typing import Any
import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

COUNTS: dict[str, int] = {}

def require(ok: bool, message: str, group: str) -> None:
    if not ok:
        raise RuntimeError(message)
    COUNTS[group] = COUNTS.get(group, 0) + 1


def cheb(c: Q, j: int) -> tuple[Q, Q]:
    """Return T_j(c), U_{j-1}(c) with exact rational arithmetic."""
    t0, t1, u0, u1 = Q(1), c, Q(0), Q(1)
    for _ in range(1, j):
        t0, t1 = t1, 2*c*t1-t0
        u0, u1 = u1, 2*c*u1-u0
    return t1, u1


def schur_exact(R: Q, j: int) -> list[list[Q]]:
    g = 1-2*R; c = (1-R)/R
    H = [[Q(0) for _ in range(j+1)] for _ in range(j+1)]
    for i in range(j):
        H[i][i] += c/g; H[i+1][i+1] += c/g
        H[i][i+1] -= 1/g; H[i+1][i] -= 1/g
    # Eliminate the first remaining interior coordinate repeatedly.
    while len(H) > 2:
        keep = [i for i in range(len(H)) if i != 1]
        pivot = H[1][1]
        H = [[H[i][k]-H[i][1]*H[1][k]/pivot for k in keep] for i in keep]
    return H


def sinhratio(i: np.ndarray | float, j: int, chi: float) -> np.ndarray:
    i = np.asarray(i, dtype=float)
    return np.exp((i-j)*chi)*(-np.expm1(-2*i*chi))/(-np.expm1(-2*j*chi))


def quadratic(R: float, j: int) -> tuple[np.ndarray, np.ndarray, float]:
    g = 1-2*R; chi = acosh((1-R)/R); s = sqrt(g)/R
    den = -np.expm1(-2*j*chi)
    csch = 2*exp(-j*chi)/den
    coth = (1+exp(-2*j*chi))/den
    H = (s/g)*np.array([[coth,-csch],[-csch,coth]])
    d, U = np.linalg.eigh(H)
    invsqrt = (U/np.sqrt(d))@U.T
    logd0 = log(2*s/g)-j*chi-log(den)
    return H, invsqrt, logd0


def flight_jet(R: float, u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, ...]:
    a = np.sqrt(R*R-u*u); b = np.sqrt(R*R-v*v)
    d = 1-a-b; delta = v-u
    L = np.sqrt(d*d+delta*delta)
    du=u/a; dv=v/b
    nu=d*du-delta; nv=d*dv+delta
    gu=nu/L; gv=nv/L
    huu=(du*du+d*R*R/a**3+1)/L-nu*nu/L**3
    hvv=(dv*dv+d*R*R/b**3+1)/L-nv*nv/L**3
    huv=(du*dv-1)/L-nu*nv/L**3
    # Avoid subtracting j*g from the total length in tiny-energy tests.
    excess=u*u/(R+a)+v*v/(R+b)+delta*delta/(L+d)
    return L, excess, gu, gv, huu, hvv, huv


def bridge(R: float, j: int, u: float, v: float) -> tuple[np.ndarray, float, float, float]:
    chi=acosh((1-R)/R)
    inds=np.arange(j+1)
    y=sinhratio(j-inds,j,chi)*u+sinhratio(inds,j,chi)*v
    for _ in range(20):
        L, ex, gu, gv, huu, hvv, huv=flight_jet(R,y[:-1],y[1:])
        grad=gv[:-1]+gu[1:]
        if j==1 or np.max(np.abs(grad)) < 2e-15:
            break
        diag=hvv[:-1]+huu[1:]
        off=huv[1:-1]
        band=np.zeros((3,j-1)); band[1]=diag
        band[0,1:]=off; band[2,:-1]=off
        y[1:-1] -= solve_banded((1,1),band,grad,check_finite=True)
    else:
        raise RuntimeError('Stationary bridge Newton iteration did not converge')
    L, ex, gu, gv, huu, hvv, huv=flight_jet(R,y[:-1],y[1:])
    residual=float(np.max(np.abs(gv[:-1]+gu[1:]))) if j>1 else 0.0
    logdet=0.0
    if j>1:
        diag=hvv[:-1]+huu[1:]; off=huv[1:-1]
        p=diag[0]; logdet=log(float(p))
        for i in range(1,j-1):
            p=diag[i]-off[i-1]**2/p
            if p<=0: raise RuntimeError('Nonpositive Dirichlet pivot')
            logdet+=log(float(p))
    logD=float(np.log(-huv).sum())-logdet
    return y,float(ex.sum()),logD,residual


def physical_residual(R: float, y: np.ndarray) -> tuple[float,float]:
    j=len(y)-1; side=np.arange(j+1)%2
    arc=np.sqrt(R*R-y*y)
    q=np.column_stack((np.where(side==0,arc,1-arc),y))
    n=np.column_stack((np.where(side==0,arc,-arc)/R,y/R))
    vec=np.diff(q,axis=0); lens=np.linalg.norm(vec,axis=1)
    vel=vec/lens[:,None]
    if j>1:
        reflected=vel[:-1]-2*np.sum(vel[:-1]*n[1:-1],axis=1)[:,None]*n[1:-1]
        error=float(np.max(np.linalg.norm(reflected-vel[1:],axis=1)))
    else: error=0.0
    cosines=np.concatenate((np.sum(vel*n[:-1],axis=1),-np.sum(vel*n[1:],axis=1)))
    return error,float(cosines.min())


def integral_ratio(R: float, j: int, eps: float, angular: int=24, radial: int=12) -> float:
    """Endpoint quadrature of the full maximal-count tail / leading formula."""
    _, invsqrt, logd0=quadratic(R,j)
    ar,aw=leggauss(angular); rr,rw=leggauss(radial)
    total=0.0
    for theta,wtheta in zip(pi*(ar+1),pi*aw):
        direction=sqrt(2*eps)*(invsqrt@np.array([cos(theta),sin(theta)]))
        def level(r: float) -> float:
            return bridge(R,j,*(r*direction))[1]/eps-1
        rmax=brentq(level,.5,1.5,xtol=1e-13)
        inner=0.0
        for r,wr in zip(rmax*(rr+1)/2,rmax*rw/2):
            _,energy,logD,_=bridge(R,j,*(r*direction))
            inner+=wr*(1-energy/eps)*exp(logD-logd0)*r
        total+=wtheta*inner
    return 2*total/pi


def main() -> None:
    # Exact Schur identities and the Hill/Jacobi algebra.
    for R in [Q(1,5),Q(9,20),Q(23,50),Q(47,100)]:
        g=1-2*R; c=(1-R)/R
        for j in range(1,13):
            t,U=cheb(c,j)
            require(t*t-(c*c-1)*U*U==1,'Chebyshev determinant identity','exact_hessian')
            diag=t/(g*U); off=-1/(g*U)
            require(diag*diag-off*off==1/(R*R*g),'Effective determinant','exact_hessian')
            if j<=8:
                H=schur_exact(R,j)
                require(H==[[diag,off],[off,diag]],'Exact endpoint Schur matrix','exact_hessian')
        require((3/(2*R))/(2*c) == 3/(4*(1-R)),
                'Three-hit coefficient simplification','exact_coefficients')
    # Polynomial in c whose roots are the two multipliers.
    for c in [Q(3,2),Q(27,23),Q(53,47)]:
        require((2*c)**2-4==4*(c*c-1),'Jacobi discriminant','exact_coefficients')
    for R in [Q(9,20),Q(23,50),Q(47,100)]:
        T=Q(11,100); C=(1-2*R+T*T)/(2*T*(1-R))
        require(0<C<1 and (1-R)*C-T>0,'Terminal witness incoming root','exact_witness')
        require((R-1)**2+T*T+2*(R-1)*T*C==R*R,'Terminal witness root equation','exact_witness')
    # Uniform-in-j stress examples: these are finite, floating diagnostics.
    stress=[]
    for R in [.2,.45,.47]:
        max_rel=0.0; max_quartic=0.0; max_reflect=0.0
        for j in [1,2,3,8,32,64,128]:
            H,_,logd0=quadratic(R,j)
            for u,v in [(1e-3,-.7e-3),(.2e-3,.9e-3),(0.0,1e-3)]:
                y,energy,logD,res=bridge(R,j,u,v)
                rel=exp(logD-logd0)
                a2=u*u+v*v; quad=.5*np.array([u,v])@H@np.array([u,v])
                ratio=abs(rel-1)/a2; err4=abs(energy-quad)/(a2*a2)
                er,cosmin=physical_residual(R,y)
                require(res<1e-12 and er<2e-12,'Physical specular stationarity','floating_bridge')
                require(cosmin>.99,'Both impact traces transverse','floating_bridge')
                require(ratio<2e4 and err4<2e4,'Relative twist/quartic bounds on sampled configurations','floating_bridge')
                require(energy>0 and np.max(np.abs(y))<=max(abs(u),abs(v))*(1+1e-10),
                        'Positive energy and boundary-layer bridge','floating_bridge')
                max_rel=max(max_rel,ratio); max_quartic=max(max_quartic,err4); max_reflect=max(max_reflect,er)
        stress.append({'R':R,'max_relative_twist_error_divided_by_endpoint_square':max_rel,
                       'max_quartic_error_ratio':max_quartic,'max_reflection_residual':max_reflect})
    quadratures=[]
    for R in [.2,.46]:
        for j in [1,2,3,8]:
            vals=[integral_ratio(R,j,eps) for eps in [1e-4,2.5e-5]]
            require(abs(vals[1]-1)<.003,'Onset integral leading coefficient','floating_quadrature')
            require(abs(vals[1]-1)<=.35*abs(vals[0]-1)+1e-8,'Linear relative remainder convergence','floating_quadrature')
            quadratures.append({'R':R,'j':j,'epsilons':[1e-4,2.5e-5],'tail_to_leading_ratios':vals})
    # Two representations of the coefficient generating function, tested inside its disk.
    for R in [.2,.46]:
        chi=acosh((1-R)/R); z=.7*exp(chi)
        left=sum(z**j*(2*exp(-j*chi)/(1-exp(-2*j*chi))) for j in range(1,151))
        right=2*sum(z*exp(-(2*m+1)*chi)/(1-z*exp(-(2*m+1)*chi)) for m in range(80))
        require(abs(left-right)<1e-11,'Lambert coefficient identity','floating_series')
    result={'status':'PASS','schema':'a2-uniform-threshold-diagnostics-v1',
            'checks':COUNTS,'total_checks':sum(COUNTS.values()),
            'normal_and_optimized_comparison':'Recorded by execution wrapper, not presumed by this program',
            'python':platform.python_version(),'numpy':np.__version__,
            'bridge_stress':stress,'quadrature':quadratures,
            'limits':'Exact algebra and finite non-interval floating diagnostics. Not a proof assistant, continuum validation, or general long-time transfer estimate.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
