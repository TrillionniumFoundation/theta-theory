#!/usr/bin/env python3
"""Independent finite diagnostics for the A2 v27 referee report.

Standard library only. Exact arithmetic is used where indicated. A finite
Dirichlet bridge check is not a proof of an infinite half-line theorem.
No assertions are used: all checks remain active under python -O.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

COUNTS: Counter[str] = Counter()
MAXIMA: dict[str, float] = {}


def require(condition: bool, group: str, description: str) -> None:
    if not condition:
        raise RuntimeError(f"{group}: {description}")
    COUNTS[group] += 1


def record_max(key: str, value: float) -> None:
    MAXIMA[key] = max(MAXIMA.get(key, 0.0), abs(value))


def density_checks() -> None:
    d = F(3, 2)
    points = [F(i, 20) for i in range(-4, 5)]
    anchor = F(1, 5)
    for beta in (F(-1, 7), F(0), F(2, 9)):
        def action(u: F) -> F:
            return F(3, 4)*u*u + beta*u**3 + F(1, 10)*u**4
        def amplitude(u: F) -> F:
            return 2 + u + F(1, 3)*u*u
        def density(u: F, v: F) -> F:
            return amplitude(u)*amplitude(v)*(d-action(u)-action(v))/7
        def ratio(u: F, v: F) -> F:
            return density(u, v)*density(F(0), F(0))/(density(u, F(0))*density(F(0), v))
        def t(u: F) -> F:
            return action(u)/(d-action(u))
        for u in points:
            for v in points:
                require(1-ratio(u, v) == t(u)*t(v), 'exact_density_rank_one', str((beta,u,v)))
            recovered_t = (1-ratio(u, anchor))/t(anchor)
            recovered_s = d*recovered_t/(1+recovered_t)
            recovered_b = density(u,F(0))/density(F(0),F(0))*(1+recovered_t)
            require(recovered_s == action(u) and recovered_b == amplitude(u)/amplitude(F(0)),
                    'exact_fixed_anchor_inverse', str((beta,u)))
        require(1-ratio(anchor, anchor) == t(anchor)**2 and t(anchor)>0,
                'exact_positive_anchor', str(beta))


def block_checks() -> None:
    # x represents exp(n gamma); r and r^-1 represent the opposite contact ratios.
    for n in range(3, 11):
        for x in (F(3,2), F(2), F(7,2)):
            for r in (F(2,3), F(1), F(5,4)):
                c=(x*x+1)/(x*x-1)
                s=2*x/(x*x-1)
                b=r**n*s
                e=r**(-n)*s
                require(c*c-b*e == 1, 'exact_last_jet_determinant', str((n,x,r)))
                require(c*c-b*e == 1 and -c*b+b*c == 0 and e*c-c*e == 0,
                        'exact_last_jet_inverse', str((n,x,r)))
    for g in (0.4, 1.0, 1.7):
        for k0,k1 in ((0.5,0.9),(1.2,0.7),(1.1,1.1)):
            c0,c1=1+g*k0,1+g*k1
            c=math.sqrt(c0*c1)
            gamma=math.acosh(c)
            a0=c*math.sinh(gamma)/(g*c1)
            a1=c*math.sinh(gamma)/(g*c0)
            gamma2=math.asinh(g*math.sqrt(a0*a1))
            rec0=(math.cosh(gamma2)*math.sqrt(a0/a1)-1)/g
            rec1=(math.cosh(gamma2)*math.sqrt(a1/a0)-1)/g
            error=max(abs(gamma2-gamma),abs(rec0-k0),abs(rec1-k1))
            record_max('leading_geometry_error', error)
            require(error<5e-14, 'floating_leading_geometry', str((g,k0,k1)))


def support_checks() -> None:
    grid=[F(i,20) for i in range(21)]
    for eps in (F(1,100), F(1,20), F(1,10)):
        def phi(s: F) -> F:
            return s+eps*s*(1-s)*(s-F(1,2))
        for s in grid:
            require(phi(1-s)==1-phi(s), 'exact_support_reflection', str((eps,s)))
            derivative=1+eps*(-3*s*s+3*s-F(1,2))
            curvature=1+eps*(-15*s*s+9*s-F(1,2))
            require(derivative>0 and curvature>0, 'exact_grid_convexity', str((eps,s)))
            for t in grid:
                require((s+t<1)==(phi(s)+phi(t)<1), 'exact_support_grid', str((eps,s,t)))
        u=F(1,4)
        raw=(u*u)/(1-u*u)
        changed=phi(u*u)/(1-phi(u*u))
        require(raw*raw != changed*changed, 'exact_distinct_density_invariant', str(eps))


def remainder_and_finite_support_checks() -> None:
    for m in range(2,8):
        for rho in (F(1,3),F(2,3),F(4,5)):
            for n in (3,12,40):
                a=rho**(m+1)
                partial=sum((a**i for i in range(n)),F(0))
                require(partial==(1-a**n)/(1-a) and partial<1/(1-a),
                        'exact_geometric_remainder_majorant',str((m,rho,n)))
    # This is only a finite analogue of the countability obstruction, not
    # a computational proof of the uncountable deficiency-one conclusion.
    for n in (2,3,5,11):
        weights=[F(2*(i+1),n*(n+1)) for i in range(n)]
        worst=max(1-q for q in weights)
        require(sum(weights)==1 and worst>=1-F(1,n),
                'finite_disjoint_support_analogue',str(n))
        require(max(1-F(1,n) for _ in range(n))==1-F(1,n),
                'finite_uniform_output_benchmark',str(n))


def psi(b: int, y: float, t: float, degree: int) -> tuple[float,float,float]:
    k=(0.8,1.3)[b]
    cubic=(0.03,-0.02)[b]
    coeff=(0.04,-0.025)[b]
    value=k*y*y/2+cubic*y**3+0.05*y**4+t*coeff*y**degree
    first=k*y+3*cubic*y*y+0.2*y**3+t*coeff*degree*y**(degree-1)
    second=k+6*cubic*y+0.6*y*y+t*coeff*degree*(degree-1)*y**(degree-2)
    return value,first,second


def flight(b: int,y: float,z: float,t: float,degree: int) -> tuple[float,...]:
    g=1.0
    py,ay,by=psi(b,y,t,degree)
    pz,az,bz=psi(1-b,z,t,degree)
    h=g+py+pz
    delta=z-y
    length=math.hypot(h,delta)
    vy=h*ay-delta
    vz=h*az+delta
    # Stable subtraction of the unit gap for very small tail coordinates.
    excess=((py+pz)*(h+g)+delta*delta)/(length+g)
    return (excess, vy/length, vz/length,
            (ay*ay+h*by+1)/length-vy*vy/length**3,
            (az*az+h*bz+1)/length-vz*vz/length**3,
            (ay*az-1)/length-vy*vz/length**3,
            h/length*((0.04,-0.025)[b]*y**degree+(0.04,-0.025)[1-b]*z**degree))


def solve_bridge(start: int,u: float,t: float,degree: int,n: int=28) -> tuple[float,float,float]:
    x=[u*(0.3**i) for i in range(n)]+[0.0]
    residual=math.inf
    for _ in range(25):
        f=[flight((start+i)%2,x[i],x[i+1],t,degree) for i in range(n)]
        grad=[f[i-1][2]+f[i][1] for i in range(1,n)]
        residual=max(abs(v) for v in grad)
        if residual<2e-16:
            break
        diag=[f[i-1][4]+f[i][3] for i in range(1,n)]
        off=[f[i][5] for i in range(1,n-1)]
        rhs=[-v for v in grad]
        for i in range(1,n-1):
            ratio=off[i-1]/diag[i-1]
            diag[i]-=ratio*off[i-1]
            rhs[i]-=ratio*rhs[i-1]
        step=[0.0]*(n-1)
        step[-1]=rhs[-1]/diag[-1]
        for i in range(n-3,-1,-1):
            step[i]=(rhs[i]-off[i]*step[i+1])/diag[i]
        for i,s in enumerate(step,1):
            x[i]+=s
    else:
        raise RuntimeError('Finite bridge Newton iteration did not converge')
    f=[flight((start+i)%2,x[i],x[i+1],t,degree) for i in range(n)]
    return sum(v[0] for v in f),sum(v[6] for v in f),residual


def finite_envelope_checks() -> None:
    # Simpson integration of the exact finite stationary-envelope integrand.
    # Both endpoints are fixed. This checks a finite analogue, not the N -> infinity limit.
    steps=12
    for start in (0,1):
        for degree in (3,4,5):
            for u in (-0.12,0.08):
                data=[solve_bridge(start,u,i/steps,degree) for i in range(steps+1)]
                integral=(data[0][1]+data[-1][1]+sum((4 if i%2 else 2)*data[i][1]
                           for i in range(1,steps)))/(3*steps)
                difference=data[-1][0]-data[0][0]
                error=abs(difference-integral)
                residual=max(z[2] for z in data)
                record_max('finite_envelope_absolute_error',error)
                record_max('finite_stationarity_residual',residual)
                require(error<2e-13 and residual<2e-15,
                        'floating_finite_envelope',str((start,degree,u)))


def main() -> None:
    density_checks()
    block_checks()
    support_checks()
    remainder_and_finite_support_checks()
    finite_envelope_checks()
    result={
        'status':'passed',
        'reviewed_commit':'17d71b721f0c5b006b52ec3fbe244866221ee93f',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'groups':dict(sorted(COUNTS.items())),
        'total_checks':sum(COUNTS.values()),
        'floating_diagnostic_maxima':dict(sorted(MAXIMA.items())),
        'scope':'Independent exact finite algebra, rational grids, and finite stationary bridges; not a proof assistant, continuum proof, native build, or whole-paper certification.',
        'author_suite_rerun':False,
        'native_build_performed':False,
    }
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
