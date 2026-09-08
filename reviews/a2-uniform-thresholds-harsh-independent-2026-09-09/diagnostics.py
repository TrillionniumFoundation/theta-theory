#!/usr/bin/env python3
"""Independent finite checks of A2 at 500cf06faccb6eadd6c122abeb63c60a0cb7522e.
No repository imports, network access, assertions, or formal-proof claims.
Run: python diagnostics.py > diagnostics.json
Dependencies: numpy, scipy, mpmath. Both exact and floating checks are labelled.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
import math
import platform
import sys
import mpmath as mp
import numpy as np
import scipy
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from numpy.polynomial.legendre import leggauss

CHECKS: list[dict] = []
DETAILS: dict = {}

def check(name: str, ok: bool, kind: str, **values) -> None:
    CHECKS.append(dict(name=name, passed=bool(ok), kind=kind, **values))
    if not ok:
        raise RuntimeError(f"Diagnostic failed: {name}: {values}")

def exact_schur(R: F, j: int):
    g, c = 1-2*R, (1-R)/R
    a, coupling, pivot, prod = c/g, -1/g, 2*c/g, F(1)
    if j == 1:
        return a, coupling, a, prod
    for i in range(1, j):
        prod *= pivot
        a -= coupling*coupling/pivot
        coupling = coupling/(g*pivot)
        pivot = (c/g if i == j-1 else 2*c/g) - 1/(g*g*pivot)
    return a, coupling, pivot, prod

def exact_checks() -> None:
    for R in (F(1,5), F(1,3), F(23,50), F(49,100)):
        g, c = 1-2*R, (1-R)/R
        for j in (1,2,3,4,8,16,32,64,128):
            a,b,d,prod = exact_schur(R,j)
            prev, cur = F(0), F(1)
            for _ in range(1,j):
                prev,cur = cur, 2*c*cur-prev
            target_a = (c*cur-prev)/(g*cur)
            ok = (a == d == target_a and b == -1/(g*cur)
                  and a*d-b*b == 1/(R*R*g)
                  and -b == (1/g)**j/prod)
            check(f"rational_schur_R{R}_j{j}",ok,"exact-rational")
    # Identifiability is already supplied by g; no stochastic inference needed.
    for R in (F(1,5), F(1,3), F(23,50), F(49,100)):
        g=1-2*R
        c=(1-R)/R
        check(f"gap_already_identifies_R{R}", (1-g)/2 == R and c == (1+g)/(1-g),
              "exact-rational")

# This is a physical ray-shooting check in initial collision angles, not the
# manuscript's effective-action formula. Every positive incoming intersection
# with a finite patch of the triangular lattice is compared before reflection.
def mp_length(R, j: int, alpha, phi):
    rt3=mp.sqrt(3)
    centers=[(mp.mpf(m)+mp.mpf(n)/2, mp.mpf(n)*rt3/2)
             for m in range(-2,3) for n in range(-2,3)]
    current=(mp.mpf(0),mp.mpf(0))
    q=(R*mp.cos(alpha), R*mp.sin(alpha))
    v=(mp.cos(alpha+phi),mp.sin(alpha+phi))
    length=mp.mpf(0)
    for _ in range(j):
        candidates=[]
        for center in centers:
            if center == current:
                continue
            dx,dy=q[0]-center[0],q[1]-center[1]
            a=dx*v[0]+dy*v[1]
            disc=a*a-(dx*dx+dy*dy-R*R)
            if disc <= 0:
                continue
            t=-a-mp.sqrt(disc)
            if t > 0:
                candidates.append((t,center))
        if not candidates:
            raise RuntimeError("Ray left the checked lattice patch")
        t,current=min(candidates,key=lambda x:x[0])
        q=(q[0]+t*v[0],q[1]+t*v[1])
        n=((q[0]-current[0])/R,(q[1]-current[1])/R)
        nv=n[0]*v[0]+n[1]*v[1]
        if nv >= 0:
            raise RuntimeError("Nonincoming selected intersection")
        v=(v[0]-2*nv*n[0],v[1]-2*nv*n[1])
        length += t
    return length

def ray_hessian(R, j: int):
    fun=lambda a,p: mp_length(R,j,a,p)
    k00=mp.diff(fun,(mp.mpf(0),mp.mpf(0)),(2,0))
    k01=mp.diff(fun,(mp.mpf(0),mp.mpf(0)),(1,1))
    k11=mp.diff(fun,(mp.mpf(0),mp.mpf(0)),(0,2))
    return k00,k01,k11

def ray_hessian_checks() -> None:
    mp.mp.dps=65
    rows=[]
    for rs in ("0.2","0.35","0.46","0.49"):
        R=mp.mpf(rs)
        for j in (1,2,3,6):
            a,b,d=ray_hessian(R,j)
            root=mp.sqrt(a*d-b*b)
            target=R*mp.sinh(j*mp.acosh((1-R)/R))
            err=abs(root/target-1)
            # Probability coefficient in (alpha,phi) is 3*lambda/(2*root).
            check(f"physical_ray_hessian_R{rs}_j{j}",err<mp.mpf('1e-35'),
                  "non-interval-high-precision",relative_error=float(err))
            rows.append(dict(R=rs,j=j,coefficient_ratio=mp.nstr(target/root,22),
                             hessian_determinant=mp.nstr(root*root,22)))
    DETAILS['physical_ray_hessians']=rows

# Closed derivatives of Euclidean chord lengths, independently differentiated.
def chord(R: float, u: np.ndarray, v: np.ndarray):
    a=np.sqrt(R*R-u*u); b=np.sqrt(R*R-v*v)
    D=1-a-b; E=v-u; ell=np.sqrt(D*D+E*E)
    Du=u/a; Dv=v/b
    fu=(D*Du-E)/ell; fv=(D*Dv+E)/ell
    uu=(Du*Du+D*R*R/a**3+1-fu*fu)/ell
    vv=(Dv*Dv+D*R*R/b**3+1-fv*fv)/ell
    uv=(Du*Dv-1-fu*fv)/ell
    return ell,fu,fv,uu,uv,vv

def nonlinear_bridge(R: float,j: int,u: float,v: float):
    g=1-2*R; chi=np.arccosh((1-R)/R)
    i=np.arange(j+1,dtype=float)
    den=-np.expm1(-2*j*chi)
    L=np.exp(-i*chi)*(-np.expm1(-2*(j-i)*chi))/den
    M=np.exp(-(j-i)*chi)*(-np.expm1(-2*i*chi))/den
    y=L*u+M*v
    for iteration in range(12):
        ell,fu,fv,uu,uv,vv=chord(R,y[:-1],y[1:])
        if j == 1:
            break
        gradient=fv[:-1]+fu[1:]
        diag=vv[:-1]+uu[1:]
        if np.max(np.abs(gradient))<2e-16:
            break
        band=np.zeros((3,j-1)); band[1]=diag
        if j>2:
            band[0,1:]=uv[1:-1]; band[2,:-1]=uv[1:-1]
        y[1:-1] -= solve_banded((1,1),band,gradient)
    else:
        raise RuntimeError("Newton iteration did not converge")
    ell,fu,fv,uu,uv,vv=chord(R,y[:-1],y[1:])
    logdet=0.0
    if j>1:
        diag=vv[:-1]+uu[1:]
        pivot=diag[0]; logdet=math.log(pivot)
        for h in range(1,j-1):
            pivot=diag[h]-uv[h]**2/pivot
            if pivot<=0:
                raise RuntimeError("Nonpositive interior Hessian pivot")
            logdet+=math.log(pivot)
    logtwist=float(np.log(-uv).sum())-logdet
    logd0=math.log(math.sinh(chi)/g)-(j*chi+math.log1p(-math.exp(-2*j*chi))-math.log(2))
    ratio=math.exp(logtwist-logd0)
    residual=0.0 if j==1 else float(np.max(np.abs(fv[:-1]+fu[1:])))
    # Verify mechanical reflection directly at interior impact positions.
    xs=np.where(np.arange(j+1)%2==0,np.sqrt(R*R-y*y),1-np.sqrt(R*R-y*y))
    pts=np.column_stack((xs,y)); vel=np.diff(pts,axis=0)/ell[:,None]
    reflection_error=0.0
    for h in range(1,j):
        center=np.array([float(h%2),0.0]); normal=(pts[h]-center)/R
        reflected=vel[h-1]-2*np.dot(vel[h-1],normal)*normal
        reflection_error=max(reflection_error,float(np.linalg.norm(reflected-vel[h])))
    return ratio,residual,reflection_error

def relative_twist_checks() -> None:
    rows=[]
    for R in (.2,.46,.49):
        for j in (1,2,3,8,32,128):
            coefficients=[]
            for amp in (1e-3,5e-4):
                u,v=amp,-.63*amp
                ratio,residual,refl=nonlinear_bridge(R,j,u,v)
                scaled=(ratio-1)/(u*u+v*v)
                check(f"nonlinear_relative_twist_R{R}_j{j}_a{amp}",
                      ratio>0 and math.isfinite(scaled) and residual<1e-12 and refl<1e-11,
                      "non-interval-floating",relative_ratio=ratio,
                      scaled_quadratic_error=scaled,reflection_error=refl)
                coefficients.append(scaled)
            check(f'quadratic_scale_R{R}_j{j}',
                  abs(coefficients[1]-coefficients[0])<.02*max(1.0,abs(coefficients[0])),
                  'non-interval-floating-two-scale',
                  relative_change=abs(coefficients[1]-coefficients[0])/max(1.0,abs(coefficients[0])))
            rows.append(dict(R=R,j=j,scaled_errors=coefficients))
    DETAILS['relative_twist_stress']=rows

CENTERS=np.array([(m+n/2,n*math.sqrt(3)/2) for m in range(-2,3) for n in range(-2,3)])
ORIGIN=int(np.flatnonzero(np.all(CENTERS==0,axis=1))[0])

def float_record(R: float,j: int,alpha: float,phi: float):
    q=R*np.array([math.cos(alpha),math.sin(alpha)])
    v=np.array([math.cos(alpha+phi),math.sin(alpha+phi)])
    current=ORIGIN; total=0.0
    # f(alpha,phi)=cos(phi)^2 + sin(phi)/2; axial value is exactly one.
    deviation=math.cos(phi)**2+.5*math.sin(phi)-1
    for _ in range(j):
        disp=q-CENTERS
        dot=disp@v
        discr=dot*dot-np.einsum('ij,ij->i',disp,disp)+R*R
        roots=-dot-np.sqrt(np.maximum(discr,0))
        roots[(discr<=0)|(roots<=1e-12)]=np.inf
        roots[current]=np.inf
        nxt=int(np.argmin(roots)); t=float(roots[nxt])
        if not math.isfinite(t):
            raise RuntimeError("Ray left finite lattice patch")
        q=q+t*v; normal=(q-CENTERS[nxt])/R
        nv=float(np.dot(v,normal))
        if nv>=0:
            raise RuntimeError("Nonincoming first hit")
        v=v-2*nv*normal
        c=float(np.dot(v,normal)); s=float(normal[0]*v[1]-normal[1]*v[0])
        deviation+=c*c+.5*s-1
        total+=t; current=nxt
    return total,deviation

def ray_integral(R: float,j: int,eps: float,ntheta: int=48,nrad: int=16):
    # Independent physical-section integral; no endpoint-action or Morse map.
    a,b,d=ray_hessian(mp.mpf(str(R)),j)
    K=np.array([[float(a),float(b)],[float(b),float(d)]])
    eig,U=np.linalg.eigh(K)
    if np.min(eig)<=0:
        raise RuntimeError("Nonpositive physical Hessian")
    whitening=(U/np.sqrt(eig))@U.T
    nodes,weights=leggauss(nrad)
    total=np.zeros(2); g=1-2*R
    for theta in (np.arange(ntheta)+.5)*(2*math.pi/ntheta):
        direction=math.sqrt(2*eps)*(whitening@np.array([math.cos(theta),math.sin(theta)]))
        def excess(r):
            x=direction*r
            return float_record(R,j,float(x[0]),float(x[1]))[0]-j*g
        root=brentq(lambda r:excess(r)-eps,.65,1.35,xtol=2e-12)
        for node,weight in zip(nodes,weights):
            r=(node+1)*root/2
            x=direction*r
            length,dev=float_record(R,j,float(x[0]),float(x[1]))
            value=(1-(length-j*g)/eps)*math.cos(float(x[1]))*r*weight*root/2
            total += value*np.array([1.0,math.exp(.1*dev)])
    return total*(2*math.pi/ntheta)*(2/math.pi)

def integral_checks() -> None:
    rows=[]
    for j in (1,2,3):
        for eps in (1e-4,5e-5,1e-5):
            ratios=ray_integral(.46,j,eps)
            check(f"physical_section_integral_j{j}_eps{eps}",
                  bool(np.max(np.abs(ratios-1))<100*eps),
                  "non-interval-floating-quadrature",
                  unweighted_ratio=float(ratios[0]),source_normalized_ratio=float(ratios[1]))
            rows.append(dict(R=.46,j=j,epsilon=eps,
                             unweighted_ratio=float(ratios[0]),source_normalized_ratio=float(ratios[1])))
    coarse=ray_integral(.46,3,5e-5,24,12)
    fine=ray_integral(.46,3,5e-5,64,24)
    check('quadrature_resolution_j3',bool(np.max(np.abs(coarse-fine))<2e-8),
          'non-interval-floating-quadrature',max_difference=float(np.max(np.abs(coarse-fine))))
    DETAILS['independent_collision_angle_integrals']=rows

# Exact leading conditional cut law: eta has density 2(1-eta), 0<eta<1.
# The next checks record a limitation, NOT a counterexample to Theorem 6.1.
def scope_checks() -> None:
    for kappa in (F(1,4),F(1,2),F(3,4)):
        cut=2*kappa-kappa*kappa
        check(f"paraboloid_initial_cut_{kappa}",0<cut<1,
              'exact-rational',before_first_impact_probability=str(1-cut))
    # With two auxiliary Bernoulli laws p_eps(R)=1/2+eps*sin(R/eps**2),
    # TV<=eps but the derivative at R=0 is 1/eps. Scope test only.
    for eps in (F(1,10),F(1,100)):
        check(f"TV_does_not_imply_response_{eps}",1/eps>1,
              'exact-symbolic-scope-test',TV_bound=str(eps),derivative_at_zero=str(1/eps))

def main() -> None:
    exact_checks(); ray_hessian_checks(); relative_twist_checks(); integral_checks(); scope_checks()
    report=dict(source_commit='500cf06faccb6eadd6c122abeb63c60a0cb7522e',
        scope='Finite diagnostics, not continuum, formal proof, or priority certification.',
        environment=dict(python=platform.python_version(),numpy=np.__version__,
                         scipy=scipy.__version__,mpmath=mp.__version__),
        checks_total=len(CHECKS),checks_passed=sum(c['passed'] for c in CHECKS),
        checks=CHECKS,details=DETAILS)
    print(json.dumps(report,indent=2,sort_keys=True,allow_nan=False))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps(dict(error=str(exc),completed_checks=CHECKS),indent=2),file=sys.stderr)
        raise
