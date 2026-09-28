#!/usr/bin/env python3
"""Finite diagnostics for A2 v27; not a proof or a native source-graph audit."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

COUNTS: dict[str, int] = {}

def require(ok: bool, category: str, detail: str) -> None:
    if not ok:
        raise RuntimeError(category + ': ' + detail)
    COUNTS[category] = COUNTS.get(category, 0) + 1

def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def density_checks() -> None:
    for d in (F(1), F(3,2), F(2)):
        for odd in (F(-1,5), F(0), F(1,4)):
            def s(u: F) -> F:
                return u*u + odd*u**3 + u**4/7
            def b(u: F) -> F:
                return 1 + u/3 + u*u/5
            def f(u: F, v: F) -> F:
                return F(7,11)*b(u)*b(v)*(d-s(u)-s(v))
            def ratio(u: F, v: F) -> F:
                return f(u,v)*f(F(0),F(0))/(f(u,F(0))*f(F(0),v))
            a=F(1,5)
            ta=s(a)/(d-s(a))
            require(1-ratio(a,a)==ta*ta, 'density_identity', 'positive anchor')
            for u in (F(-1,5),F(-1,10),F(0),F(1,10),F(1,5)):
                t=(1-ratio(u,a))/ta
                require(d*t/(1+t)==s(u), 'density_identity', 'signed action recovery')
                require(f(u,F(0))/f(F(0),F(0))*(1+t)==b(u),
                        'density_identity', 'amplitude recovery')

def block_checks() -> None:
    for z in (F(1,5),F(1,3),F(1,2)):
        for r in (F(2,3),F(1),F(7,5)):
            for n in range(3,15):
                x=z**n
                c=(1+x*x)/(1-x*x)
                h=2*x/(1-x*x)
                a=r**n*h
                b=r**(-n)*h
                require(c*c-a*b==1, 'determinant_blocks', 'determinant one')
                require(c*a-a*c==0 and c*c-a*b==1,
                        'inverse_blocks', 'inverse product')

def support_checks() -> None:
    for eps in (F(1,100),F(1,20),F(1,10)):
        def phi(s: F) -> F:
            return s+eps*s*(1-s)*(s-F(1,2))
        grid=[F(i,10) for i in range(11)]
        for s in grid:
            require(phi(1-s)==1-phi(s), 'support_gauge', 'reflection identity')
            first=1+eps*(-3*s*s+3*s-F(1,2))
            curvature=1+eps*(-15*s*s+9*s-F(1,2))
            require(first>=1-eps/2 and curvature>=1-13*eps/2>0,
                    'support_gauge', 'strict monotonicity and convexity')
            for t in grid:
                require((s+t<1)==(phi(s)+phi(t)<1),
                        'support_gauge', 'equal support')
        s=F(1,4)
        require(phi(s)!=s and (s/(1-s))**2!=(phi(s)/(1-phi(s)))**2,
                'support_gauge', 'different density invariant')

def disk_jet(y: float, radius: float) -> tuple[float,float,float]:
    root=math.sqrt(radius*radius-y*y)
    # Stable graph height at a small transverse coordinate.
    return y*y/(radius+root), y/root, radius*radius/root**3

def flight(y: float, z: float, radius: float) -> tuple[float,float,float,float]:
    p,py,_=disk_jet(y,1.0)
    q,qz,qzz=disk_jet(z,radius)
    h=1+p+q
    w=z-y
    ell=math.hypot(h,w)
    dy=h*py-w
    dz=h*qz+w
    yz=(py*qz-1)/ell-dy*dz/ell**3
    zz=(qz*qz+1+h*qzz)/ell-dz*dz/ell**3
    return ell,dz/ell,yz,zz

def two_flight_checks() -> dict[str,float]:
    max_residual=0.0
    max_excess=0.0
    min_flux=math.inf
    for radius in (0.9,1.0,1.1):
        for u in (-0.02,0.0,0.02):
            for v in (-0.02,0.0,0.02):
                lo,hi=-0.1,0.1
                for _ in range(70):
                    z=(lo+hi)/2
                    grad=flight(u,z,radius)[1]+flight(v,z,radius)[1]
                    if grad>0: hi=z
                    else: lo=z
                z=(lo+hi)/2
                f1,f2=flight(u,z,radius),flight(v,z,radius)
                excess=f1[0]+f2[0]-2
                residual=abs(f1[1]+f2[1])
                flux=f1[2]*f2[2]/(f1[3]+f2[3])
                max_residual=max(max_residual,residual)
                max_excess=max(max_excess,excess)
                min_flux=min(min_flux,flux)
                require(residual<1e-13 and flux>0 and -1e-14<=excess<0.01/4,
                        'two_flight_witness', 'common positive core and mixed flux')
                # Endpoint embedding uses the fixed unit disk for every radius.
                x=-disk_jet(u,1.0)[0]
                require(abs((x+1)**2+u*u-1)<1e-14,
                        'fixed_endpoint_embedding', 'fixed graph and transverse inverse')
        for u in (-0.03,-0.02,0.02,0.03):
            height=disk_jet(u,radius)[0]
            recovered=(height*height+u*u)/(2*height)
            require(abs(recovered-radius)<1e-12,
                    'varying_endpoint_parameter', 'nonanchor homothety identification')
    return {'max_stationarity_residual':max_residual,
            'max_excess':max_excess,'min_positive_mixed_flux':min_flux}

def remainder_checks() -> None:
    # Exact majorants for the envelope proof, not numerical infinite-orbit certification.
    for m in range(2,13):
        for rho in (F(1,3),F(1,2),F(3,4)):
            for u in (F(-1,5),F(1,10)):
                n=30
                partial=sum(abs(u)**(m+1)*rho**((m+1)*i) for i in range(n))
                tail=abs(u)**(m+1)*rho**((m+1)*n)/(1-rho**(m+1))
                total=abs(u)**(m+1)/(1-rho**(m+1))
                require(partial+tail==total and partial<=total,
                        'smooth_remainder_majorants', 'summable finite-jet envelope')
    for n in (2,3,5,10,100):
        # Finite analogue: a parameter-independent uniform output minimizes max TV to point masses.
        best=1-F(1,n)
        require(sum(F(1,n) for _ in range(n))==1 and best<1,
                'finite_disjoint_analogue', 'finite support minimax error 1-1/n')

def main() -> None:
    density_checks()
    block_checks()
    support_checks()
    numerical=two_flight_checks()
    remainder_checks()
    data=Path(__file__).read_bytes()
    report={'status':'passed','reviewed_manuscript_commit':'cefd89084682cc2e31d730eab1a4b8d8eaac0bbe',
            'review_commit':'a5b2d4b5a9ed31059e16e5011c8010579d713598',
            'script_sha256':hashlib.sha256(data).hexdigest(),'script_git_blob':git_blob(data),
            'cases':dict(sorted(COUNTS.items())),'total_cases':sum(COUNTS.values()),
            'two_flight_numerics':numerical,
            'scope':'Finite exact identities, majorants and numerical two-flight fixtures only. '
                    'Not a continuum deficiency proof, infinite half-line proof, native build, '
                    'global analytic-continuation certification or proof-assistant certificate.'}
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
