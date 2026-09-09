#!/usr/bin/env python3
"""Finite diagnostics for A2 v5; no repository imports or network access.
Exact identities and ordinary floating diagnostics are classified separately.
Neither kind verifies the infinite-dimensional or statistical theorems.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as s

checks: list[dict] = []

def require(name: str, condition: bool, kind: str, **data) -> None:
    if not bool(condition):
        raise RuntimeError(f"{name}: FAILED; {data}")
    checks.append(dict(name=name, kind=kind, passed=True, **data))

def exact(name: str, difference) -> None:
    reduced = s.factor(s.cancel(difference))
    require(name, reduced == 0, "exact", residual=str(reduced))

def symbolic_checks() -> None:
    c, r, g = s.symbols('c r g', positive=True)
    functions = [s.Integer(1), 1/(2*c), 1/(4*c*c-1), 1/(4*c*(2*c*c-1))]
    W = s.det(s.Matrix([[s.diff(f,c,k) for k in range(4)] for f in functions]))
    numerator = 12*(64*c**8+32*c**6+116*c**4+4*c*c+1)
    formula = numerator/(c**4*(4*c*c-1)**4*(2*c*c-1)**4)
    exact('four-function Wronskian', W-formula)
    for gv,rv in [(s.Rational(1),s.Rational(1)),(s.Rational(1,2),s.Rational(1,4)),(s.Rational(2,5),s.Rational(3,4))]:
        cr=1+gv/r
        phis=[(f/s.sqrt(c*c-1)).subs(c,cr) for f in functions]
        mat=s.Matrix([[s.diff(f,r,k).subs(r,rv) for k in range(4)] for f in phis])
        expected=(gv/rv**2)**6/(((1+gv/rv)**2-1)**2)*formula.subs(c,1+gv/rv)
        exact(f'Wronskian chain factors g={gv},R={rv}',mat.det()-expected)
        jac=mat*s.diag(-3,1,-1,s.Rational(1,2))
        exact(f'area coefficient Jacobian g={gv},R={rv}',jac.det()-s.Rational(3,2)*expected)
    e1,e2,e3=s.symbols('e1 e2 e3')
    p={0:s.Integer(3),1:e1,2:e1**2-2*e2,3:e1**3-3*e1*e2+3*e3}
    for n in range(4,11):
        p[n]=s.expand(e1*p[n-1]-e2*p[n-2]+e3*p[n-3])
        for i,e in enumerate((e1,e2,e3),1):
            exact(f'Newton sum p{n} differential e{i}',s.diff(p[n],e).subs({e1:0,e2:0,e3:0}))
    lam=s.symbols('lam', positive=True)
    av=s.Rational(7,5)
    t=s.symbols('t')
    for m in range(2,9):
        k=m-1
        D=lam**(2*k)/(1-lam**(2*k))-lam**(2*m)/(1-lam**(2*m))
        action=(1+lam**(2*m))/(1-lam**(2*m))
        beta=-D/(av*s.factorial(2*k))
        angular=s.factorial(2*k)/(4**k*s.factorial(k)**2)
        radial=s.integrate(t**k*(1-t),(t,0,1))/s.integrate(1-t,(t,0,1))
        amp=2*angular*radial*(2/av)**k*beta
        K=4/(2**m*(m+1)*s.factorial(m)**2*av**m)
        exact(f'jet diagonal moment assembly m={m}',-K*action+amp+K*(action+2*m*D))
        for lv in (s.Rational(1,3),s.Rational(2,5)):
            value=(-K*(action+2*m*D)).subs(lam,lv)
            require(f'jet diagonal sign m={m},lambda={lv}',value<0,'exact',value=str(value))
        exact(f'residual polar moment k={k}',angular*radial*2**k-2*s.binomial(2*k,k)/(2**k*(k+1)*(k+2)))
    D2=lam**2/(1-lam**2)-lam**4/(1-lam**4)
    sinh2=(lam**-2-lam**2)/2
    cosh2=(lam**-2+lam**2)/2
    exact('quartic diagonal agrees with v4',-(1+lam**4)/(12*av**2*(1-lam**4))-D2/(3*av**2)+(cosh2+2)/(12*av**2*sinh2))
    nu=s.Rational(2,3)
    one=-4*nu**2/(4*3*s.factorial(2)**2)
    exact('one-flight quartic derivative',one+s.Rational(1,27))
    exact('one-flight family derivative',one*(-24)-s.Rational(8,9))
    limit=-(7+2)/(12*3*4*s.sqrt(3))
    exact('half-line family derivative',limit*(-24)-s.sqrt(3)/2)
    phi=r/s.sqrt(g*(g+2*r))
    third=3*(3*g+r)/(s.sqrt(g)*(g+2*r)**s.Rational(7,2))
    exact('third radius derivative',s.diff(phi,r,3)-third)
    exact('cubic path coefficient',(s.Integer(36)**3+2*(-s.Integer(18))**3)/3-11664)
    R=s.Rational(1,4)
    for ss in (s.Rational(1,10000),s.Rational(1,20000),s.Rational(1,40000)):
        plus=[1/(R+36*ss),1/(R-18*ss),1/(R-18*ss)]
        minus=[1/(R-36*ss),1/(R+18*ss),1/(R+18*ss)]
        best=min(max(abs(a-b) for a,b in zip(plus,perm)) for perm in itertools.permutations(minus))
        exact(f'multiplicity-respecting matching s={ss}',best-36*ss/(R*R-324*ss*ss))
    for m in range(1,11):
        weights=[(-1)**(l-1)*s.binomial(m,l) for l in range(1,m+1)]
        exact(f'extrapolation constant m={m}',sum(weights)-1)
        exact(f'harmonic coefficient m={m}',sum(w/s.Integer(l) for l,w in enumerate(weights,1))-s.harmonic(m))
        for k in range(1,m):
            exact(f'extrapolation cancellation m={m},k={k}',sum(w*l**k for l,w in enumerate(weights,1)))


def one_flight_F(d: float, q6: float, angular: int = 192, radial: int = 40) -> float:
    """Actual local one-flight length and twist; no asserted jet formula used."""
    nodes,weights=np.polynomial.legendre.leggauss(radial)
    total=0.0
    def psi(x): return x*x/2+q6*x**6/720
    def der(x): return x+q6*x**5/120
    for theta in np.arange(angular)*(2*math.pi/angular):
        co,si=math.cos(theta),math.sin(theta)
        def excess(rho):
            u,v=rho*co,rho*si
            D=1+psi(u)+psi(v)
            # Stable subtraction of 1 from the length.
            z=(D-1)*(D+1)+(v-u)**2
            return z/(math.sqrt(1+z)+1)
        radius=brentq(lambda rr:excess(rr)-d,0.0,2*math.sqrt(d),xtol=5e-15)
        rr=(nodes+1)*radius/2
        u,v=rr*co,rr*si
        D=1+psi(u)+psi(v)
        length=np.sqrt(D*D+(v-u)**2)
        pu,pv=der(u),der(v)
        twist=((D*pu+u-v)*(D*pv+v-u)-(pu*pv-1)*length**2)/length**3
        z=(D-1)*(D+1)+(v-u)**2
        E=z/(length+1)
        total+=float(np.dot(weights,(d-E)*twist*rr))*radius/2
    integral=total*(2*math.pi/angular)
    return math.sqrt(3)*integral/(math.pi*d*d)


def floating_checks() -> None:
    expected=-1/972
    errors=[]
    for d in (0.02,0.01,0.005):
        derivative=(one_flight_F(d,32)-one_flight_F(d,-32))/(64*d*d)
        error=abs(derivative-expected)
        errors.append(error)
        require(f'actual length sixth-jet diagnostic d={d}',derivative<0 and error<0.00015,'ordinary floating, non-interval',value=derivative,limit=expected,error=error)
    require('sixth-jet errors decrease',errors[2]<0.65*errors[1] and errors[1]<0.65*errors[0],'ordinary floating, non-interval',errors=errors)
    # Extrapolate d*H(d), with a known simple zero; no billiard input is used.
    for m in range(1,6):
        ratio_errors=[]
        for h in (0.04,0.02,0.01):
            tau=h/5
            nodes=np.arange(1,m+2)*h
            vals=(nodes-tau)*np.exp(0.2*(nodes-tau))
            scaled=np.polynomial.polynomial.polyfit(nodes/h,vals/h,m)
            roots=np.polynomial.polynomial.polyroots(scaled)
            good=[r.real*h for r in roots if abs(r.imag)<1e-9 and abs(r.real)<=0.5]
            require(f'calibration root unique m={m},h={h}',len(good)==1,'ordinary floating, non-interval')
            err=abs(good[0]-tau)
            ratio_errors.append(err)
            require(f'calibration Taylor rate m={m},h={h}',err/h**(m+1)<10,'ordinary floating, non-interval',error=err,scaled_error=err/h**(m+1))
        require(f'calibration bias decreases m={m}',ratio_errors[-1]<ratio_errors[0],'ordinary floating, non-interval',errors=ratio_errors)
    # Safe fallback/clamp keeps every endpoint-stage offset positive, even on failure.
    for true in (-0.25,0.25):
        for fitted in (-0.5,0.0,0.5):
            require(f'clamped offset true={true},fitted={fitted}',1+fitted-true>=0.25,'exact',minimum_offset_in_h=1+fitted-true)


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=None)
    args=parser.parse_args()
    symbolic_checks()
    floating_checks()
    result=dict(
        scope='Finite algebra and non-interval diagnostics; not a theorem certificate.',
        source_revision='A2-v5-statistical-contact-rigidity',
        versions=dict(numpy=np.__version__,scipy=scipy.__version__,sympy=s.__version__),
        counts={kind:sum(c['kind']==kind for c in checks) for kind in sorted(set(c['kind'] for c in checks))},
        total=len(checks),checks=checks)
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding='utf-8')
    else:
        print(text,end='')

if __name__=='__main__':
    main()
