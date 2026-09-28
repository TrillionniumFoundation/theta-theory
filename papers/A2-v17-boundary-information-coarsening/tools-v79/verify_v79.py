#!/usr/bin/env python3
"""Algebraic/numerical diagnostics for A2 v79; not proof certification.

Requires Python 3.10+, numpy, scipy, sympy. No network or credentials used.
Writes a JSON result only when --output is explicitly supplied.
"""
from __future__ import annotations
import argparse
import json
import platform
from pathlib import Path
from typing import Callable
import numpy as np
import scipy
from scipy.optimize import root, brentq
import sympy as sp

TESTS: dict[str, Callable[[], dict[str, float | str]]] = {}

def test(name: str):
    def register(fn: Callable[[], dict[str, float | str]]):
        TESTS[name] = fn
        return fn
    return register

def require(condition, message="diagnostic condition failed"):
    if not condition:
        raise AssertionError(message)

def assert_close(a, b, tol=2e-9):
    err = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    if err > tol:
        raise AssertionError(f"max error {err:g} exceeds {tol:g}")
    return err

T = np.array([4., 6., 9., 12.])
x, y = np.meshgrid(np.linspace(-1, 1, 21), np.linspace(-1, 1, 23), indexing="ij")
x, y = x.ravel(), y.ravel()
W = 1 + .35*x + .2*y + .15*x*y
A = np.exp(.7*x-.3*y+.2*x*y)
i0, i1 = 0, len(W)-1

def gamma(w: np.ndarray) -> np.ndarray:
    k = np.log(T[1:, None]-w)-np.log(T[0]-w)
    return k-k[:, i0:i0+1]

def laws(w: np.ndarray, a=A, eta=None) -> np.ndarray:
    raw = a[None, :]*(T[:, None]-w)
    if eta is not None:
        raw *= np.exp(eta)
    # Equal discrete weights suffice for testing normalization identities.
    return raw/raw.sum(axis=1, keepdims=True)

def contrasts(f: np.ndarray) -> np.ndarray:
    q=np.log(f[1:])-np.log(f[0])
    return q-q[:, i0:i0+1]

def recover(z: np.ndarray) -> np.ndarray:
    c=np.exp(z); tau=T[1:]-T[0]
    D=c[0, i1]-c[1, i1]
    if abs(D) < 1e-12:
        raise ValueError("degenerate anchor")
    u0=((1-c[0,i1])/tau[0]-(1-c[1,i1])/tau[1])/D
    u=(c[0]*(1+tau[0]*u0)-1)/tau[0]
    if np.min(u) <= 0:
        raise ValueError("outside positive inverse chart")
    return T[0]-1/u

def residual(z):
    return z-gamma(recover(z))

@test("symbolic_rational_inverse")
def symbolic_inverse():
    u,v,a,b=sp.symbols("u v a b", nonzero=True)
    c2=(1+a*u)/(1+a*v);c3=(1+b*u)/(1+b*v)
    vhat=((1-c2)/a-(1-c3)/b)/(c2-c3)
    require(sp.cancel(vhat-v)==0, 'failed: sp.cancel(vhat-v)==0')
    require(sp.cancel((c2*(1+a*vhat)-1)/a-u)==0, 'failed: sp.cancel((c2*(1+a*vhat)-1)/a-u)==0')
    require(sp.cancel(c2-c3-(a-b)*(u-v)/((1+a*v)*(1+b*v)))==0, 'failed: sp.cancel(c2-c3-(a-b)*(u-v)/((1+a*v)*(1+b*v)))==0')
    return {"identities":"3 exact rational identities"}

@test("absolute_action_and_common_reweighting")
def inverse_and_reweight():
    f=laws(W);z=contrasts(f)
    e=assert_close(z,gamma(W))
    e=max(e,assert_close(recover(z),W))
    b=np.exp(.9*x*x-.7*y)
    fb=f*b;fb/=fb.sum(axis=1,keepdims=True)
    e=max(e,assert_close(contrasts(fb),z))
    return {"max_abs_error":e}

@test("split_coordinates_off_model")
def split():
    r=np.zeros_like(gamma(W))
    r[1]=.13*np.sin(np.pi*(x+1)/2)*np.cos(y)
    r[2]=.08*(x-x[i0])*(y+.4)
    r[:,i0]=0;r[1,i1]=0
    z=gamma(W)+r
    e=max(assert_close(recover(z),W),assert_close(residual(z),r))
    return {"max_abs_error":e,"nonzero_residual":float(np.max(abs(r)))}

@test("complete_exact_action_confounding")
def confounding():
    v=W+.025*np.sin(1.2*x+.7*y)
    eta=np.log((T[:,None]-v)/(T[:,None]-W))
    e=assert_close(laws(W,eta=eta),laws(v))
    e=max(e,assert_close(recover(contrasts(laws(W,eta=eta))),v))
    return {"max_abs_error":e,"action_separation":float(np.max(abs(v-W)))}

@test("third_and_fourth_clock_validation")
def validation():
    r=np.zeros_like(gamma(W));r[1]=.05*(x*x-1)
    require(np.max(abs(residual(gamma(W)+r)))>.04, 'failed: np.max(abs(residual(gamma(W)+r)))>.04')
    q=np.zeros_like(r);q[2]=.03*(y-y[i0])
    e=assert_close(residual(gamma(W)+q),q)
    return {"max_abs_error":e,"third_clock_residual":float(np.max(abs(r)))}

@test("small_misspecification_bias")
def misspec():
    # Test the analytic first derivative, not an unjustified universal
    # condition number. The theorem's constant depends on the clock anchor.
    z=gamma(W)
    base=np.array([np.sin(x+y),np.cos(x)-np.cos(x[i0]),x*y,y*y])
    E=base[1:]-base[0]
    E-=E[:,i0:i0+1]
    c=np.exp(z);tau=T[1:]-T[0];dc=c*E
    D=c[0,i1]-c[1,i1]
    N=(1-c[0,i1])/tau[0]-(1-c[1,i1])/tau[1]
    u0=N/D
    dD=dc[0,i1]-dc[1,i1]
    dN=-dc[0,i1]/tau[0]+dc[1,i1]/tau[1]
    du0=(dN*D-N*dD)/(D*D)
    u=(c[0]*(1+tau[0]*u0)-1)/tau[0]
    du=(dc[0]*(1+tau[0]*u0)+c[0]*tau[0]*du0)/tau[0]
    derivative=du/(u*u)
    remainders=[]
    for eps in [1e-4,5e-5,2.5e-5,1.25e-5]:
        dz=contrasts(laws(W,eta=eps*base))
        assert_close(dz,z+eps*E,1e-12)
        err=float(np.max(abs((recover(dz)-W)/eps-derivative)))
        remainders.append(err)
    contraction=max(remainders[j+1]/remainders[j] for j in range(3))
    if contraction >= .55:
        raise AssertionError(f"first-order remainder does not halve: {remainders}")
    relative=remainders[-1]/max(1.,float(np.max(abs(derivative))))
    if relative >= .005:
        raise AssertionError(f"analytic derivative mismatch: {relative}")
    return {"anchor_denominator":float(abs(D)),
            "directional_condition_number":float(np.max(abs(derivative))),
            "max_remainder_contraction":float(contraction),
            "final_relative_derivative_error":float(relative)}

@test("tangent_left_inverse_and_normal_kernel")
def tangent():
    z=gamma(W);h=.2*np.sin(x)+.1*y
    kp=1/(T[0]-W)-1/(T[1:,None]-W)
    dg=kp*h-(kp*h)[:,i0:i0+1]
    eps=1e-5
    derivative=(recover(z+eps*dg)-recover(z-eps*dg))/(2*eps)
    err=assert_close(derivative,h,3e-7)
    normal=np.zeros_like(z);normal[1]=.1*(x*x-1);normal[2]=.1*(y-y[i0])
    dn=(recover(z+eps*normal)-recover(z-eps*normal))/(2*eps)
    err=max(err,assert_close(dn,0,3e-7))
    return {"max_abs_error":err}

@test("constant_action_chart_rejected")
def constant_reject():
    try: recover(gamma(np.full_like(W,1.)))
    except ValueError: return {"result":"degenerate chart correctly rejected"}
    raise AssertionError("constant action must not enter inverse chart")

# A genuinely nonseparable convex twist example, globally bounded Hessian.
# L = (y-x)^2/2 + .6*(x^2+y^2) + .05 sin(x) sin(y).
# Eigenvalues of the quadratic Hessian are 1.2,3.2; perturbation norm <= .1.
# Hence lambda=1.1, Lambda=3.3, b=.95 are valid global bounds.
def lf(a,b): return .5*(b-a)**2+.6*(a*a+b*b)+.05*np.sin(a)*np.sin(b)
def lx(a,b): return a-b+1.2*a+.05*np.cos(a)*np.sin(b)
def ly(a,b): return b-a+1.2*b+.05*np.sin(a)*np.cos(b)
def lxx(a,b): return 2.2-.05*np.sin(a)*np.sin(b)
def lyy(a,b): return 2.2-.05*np.sin(a)*np.sin(b)
def lxy(a,b): return -1+.05*np.cos(a)*np.cos(b)

def action(n:int,s:float,t:float):
    def stationarity(z):
        a=np.r_[s,z,t]
        return np.array([ly(a[i-1],a[i])+lx(a[i],a[i+1]) for i in range(1,n)])
    if n>1:
        sol=root(stationarity,np.linspace(s,t,n+1)[1:-1],tol=1e-11)
        if np.max(abs(stationarity(sol.x)))>2e-10:
            raise RuntimeError(f"stationary solve failed: {sol.message}")
        a=np.r_[s,sol.x,t]
        H=np.diag([lyy(a[i-1],a[i])+lxx(a[i],a[i+1]) for i in range(1,n)])
        for i in range(n-2): H[i,i+1]=H[i+1,i]=lxy(a[i+1],a[i+2])
    else: a=np.array([s,t]);H=np.empty((0,0))
    det=float(np.linalg.det(H)) if n>1 else 1.
    twist=-float(np.prod([-lxy(a[i],a[i+1]) for i in range(n)]))/det
    value=sum(lf(a[i],a[i+1]) for i in range(n))
    us=lx(a[0],a[1]);ut=ly(a[-2],a[-1])
    uss=lxx(a[0],a[1])
    utt=lyy(a[-2],a[-1])
    if n>1:
        inv=np.linalg.inv(H)
        uss-=lxy(a[0],a[1])**2*inv[0,0]
        utt-=lxy(a[-2],a[-1])**2*inv[-1,-1]
    return dict(path=a,value=value,ds=us,dt=ut,dss=uss,dtt=utt,dst=twist,H=H)

@test("convex_nonseparable_hessian_and_twist")
def convex_bounds():
    low=10.;high=0.;mingap=10.
    for a in np.linspace(-8,8,17):
        for b in np.linspace(-8,8,17):
            h=np.array([[lxx(a,b),lxy(a,b)],[lxy(a,b),lyy(a,b)]])
            ev=np.linalg.eigvalsh(h);low=min(low,float(ev[0]));high=max(high,float(ev[-1]))
    for n in range(1,7):
        z=action(n,-.3,.7)
        bound=.95*(.95/6.6)**(n-1)
        require(abs(z['dst'])>=bound, "failed: abs(z['dst'])>=bound")
        mingap=min(mingap,abs(z['dst'])/bound)
    require(low>=1.1-1e-12 and high<=3.3+1e-12, 'failed: low>=1.1-1e-12 and high<=3.3+1e-12')
    return {"sample_min_eigenvalue":low,"sample_max_eigenvalue":high,"minimum_twist_to_lower_bound_ratio":mingap}

@test("physical_prefix_subtraction_and_schur_sign")
def prefix():
    maxerr=0.;slopes=[]
    for n in [1,2,3,5]:
        t,v=.17,-.21
        # Backward construction of actual initial state, not arbitrary stationary continuation.
        prev,nxt=t,v
        for _ in range(n):
            rootx=brentq(lambda a:ly(a,prev)+lx(prev,nxt),-1000,1000,xtol=1e-13)
            nxt,prev=prev,rootx
        s=prev
        u=action(n,s,t);w=action(n+1,s,v)
        maxerr=max(maxerr,assert_close(u['ds'],w['ds'],2e-8))
        maxerr=max(maxerr,assert_close(w['value']-u['value'],lf(t,v),2e-8))
        B=u['dtt']+lxx(t,v)
        hs=w['dss']-u['dss']
        maxerr=max(maxerr,assert_close(hs,-u['dst']**2/B,2e-8))
        require(B>0 and B<=6.6 and hs<0, 'failed: B>0 and B<=6.6 and hs<0')
        slopes.append(float(hs))
    return {"max_abs_error":maxerr,"most_negative_matching_slope":min(slopes)}

@test("symbolic_contact_form_sign")
def contact_sign():
    a,b,c=sp.symbols('x y c',real=True)
    L=(b-a)**2/2+sp.Rational(3,5)*(a*a+b*b)+sp.sin(a)*sp.sin(b)/20
    p=-sp.diff(L,a);q=sp.diff(L,b)
    # G*alpha-alpha = -d(c+L)+q dy-p dx.
    require(sp.simplify(-sp.diff(c+L,a)-p)==0, 'failed: sp.simplify(-sp.diff(c+L,a)-p)==0')
    require(sp.simplify(-sp.diff(c+L,b)+q)==0, 'failed: sp.simplify(-sp.diff(c+L,b)+q)==0')
    return {"identities":"both coefficients of G*(dz+theta)-(dz+theta) vanish"}

@test("deadline_integration")
def deadline():
    delay_width=9.;c=2.3;n=4;actionval=1.7;threshold=4.1
    deadline=n*c+threshold
    cutoff=deadline-(n*c+actionval)
    require(0<cutoff<delay_width, 'failed: 0<cutoff<delay_width')
    e=assert_close(cutoff/delay_width,(threshold-actionval)/delay_width)
    return {"max_abs_error":e}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    results={};ok=True
    for name,fn in TESTS.items():
        try: results[name]={"status":"PASS",**fn()}
        except Exception as ex:
            ok=False;results[name]={"status":"FAIL","error":str(ex)}
    report={"kind":"diagnostics_not_proof_certification","status":"PASS" if ok else "FAIL",
            "python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
            "sympy":sp.__version__,"tests":results}
    text=json.dumps(report,indent=2,ensure_ascii=False)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text+'\n')
    raise SystemExit(0 if ok else 1)

if __name__=='__main__': main()
