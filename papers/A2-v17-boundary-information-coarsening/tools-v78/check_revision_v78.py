#!/usr/bin/env python3
"""Deterministic diagnostics for A2 v78. These are not proof certification.
Run from the manuscript directory; requires numpy, scipy, sympy and mpmath.
No check depends on Python assert, so python -O runs the same checks.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Any
import mpmath as mp
import numpy as np
import scipy
from scipy.optimize import brentq
import sympy as sp

RESULTS: dict[str, Any] = {}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def near(a: Any, b: Any, tol: float, message: str) -> float:
    err = float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
    scale = 1.0 + float(np.max(np.abs(np.asarray(b))))
    require(math.isfinite(err) and err <= tol * scale, f"{message}: {err:g}")
    return err

def symbolic_checks() -> None:
    t1,t2,t3,w,w0,b,lam,a = sp.symbols('t1 t2 t3 w w0 b lam a')
    c=[t2-t3,t3-t1,t1-t2]; ts=[t1,t2,t3]
    g=[b*(t-w)/(t-w0) for t in ts]
    den=sum(ci*gi for ci,gi in zip(c,g))
    num=sum(ci*ti*gi for ci,ti,gi in zip(c,ts,g))
    require(sp.factor(num-w0*den)==0, 'three-clock anchor identity')
    q=g[0]/g[1]; d1=t1-w0; d2=t2-w0
    inverse=w0+d1*d2*(1-q)/(d2-d1*q)
    require(sp.factor(inverse-w)==0, 'absolute action identity')
    r=(t1-w)/(t2-w); wl=(t1-lam*t2*r)/(1-lam*r)
    al=a*(t2-w)/(t2-wl)
    require(sp.factor(al*(t1-wl)-lam*a*(t1-w))==0, 'two-clock first gauge')
    require(sp.factor(al*(t2-wl)-a*(t2-w))==0, 'two-clock second gauge')
    RESULTS['symbolic']={'identities':4,'status':'passed'}

MU=1.3

def potential(x: Any) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    x=np.asarray(x,dtype=float)
    b=np.zeros_like(x); b1=np.zeros_like(x); b2=np.zeros_like(x)
    inside=np.abs(x)<1
    z=x[inside]; d=1-z*z; e=np.exp(-1/d)
    b[inside]=e
    b1[inside]=-2*z*e/d**2
    b2[inside]=e*(4*z*z/d**4-2/d**2-8*z*z/d**3)
    return .65*x*x+.05*x+.15+.005*b, 1.3*x+.05+.005*b1, 1.3+.005*b2

def action(n: int, s: float, t: float) -> dict[str, Any]:
    require(n>=1,'positive word length')
    x=np.linspace(s,t,n+1)
    for _ in range(30):
        if n==1:
            break
        _,p1,p2=potential(x[1:-1])
        grad=MU*(2*x[1:-1]-x[:-2]-x[2:])+p1
        if np.max(np.abs(grad)) <= 2e-12*(1+np.max(np.abs(x))):
            break
        h=np.diag(2*MU+p2)
        if n>2:
            h+=np.diag(np.full(n-2,-MU),1)+np.diag(np.full(n-2,-MU),-1)
        x[1:-1]-=np.linalg.solve(h,grad)
    p,p1,p2=potential(x)
    value=float(np.sum(MU/2*np.diff(x)**2+p[:-1]))
    ws=float(MU*(s-x[1])+p1[0]); wt=float(MU*(t-x[-2]))
    if n==1:
        h=np.zeros((0,0)); det=1.; mineig=math.inf
        wss=MU+p2[0]; wst=-MU; wtt=MU
    else:
        residual=MU*(2*x[1:-1]-x[:-2]-x[2:])+p1[1:-1]
        require(np.max(np.abs(residual))<=1e-9*(1+np.max(np.abs(x))), 'stationary residual')
        h=np.diag(2*MU+p2[1:-1])
        if n>2:
            h+=np.diag(np.full(n-2,-MU),1)+np.diag(np.full(n-2,-MU),-1)
        inv=np.linalg.inv(h); det=float(np.linalg.det(h)); mineig=float(np.linalg.eigvalsh(h)[0])
        wss=MU+p2[0]-MU**2*inv[0,0]
        wst=-MU**2*inv[0,-1]; wtt=MU-MU**2*inv[-1,-1]
        require(mineig>=1.,'uniform convexity')
    near(wst,-MU**n/det,1e-11,'corner-cofactor identity')
    return dict(value=value,s=ws,t=wt,ss=float(wss),st=float(wst),tt=float(wtt),path=x,mineig=mineig)

def backwards(n: int, t: float, v: float) -> float:
    current,following=t,v
    for _ in range(n):
        previous=2*current-following+float(potential(current)[1])/MU
        following,current=current,previous
    return current

def fixed_design(n: int) -> dict[str,float]:
    # The same class constants are used for all fixtures.
    r0=r1=1.5
    for _ in range(n):
        r0,r1=r1,(2+1.6)*r1+r0+.1
    S=r1+1
    lower=-(n+1)*(.2+.1**2/2)
    upper=2*1.6*S*S+(n+1)*(.2+.1*S+1.6*S*S/2)
    return dict(S=S,lower=lower,upper=upper,A=upper-lower+4)

def mechanical_checks() -> None:
    # |b''| <= 4*4^4 exp(-4)+2*2^2 exp(-2)+8*3^3 exp(-3).
    bump_bound=4*4**4*math.exp(-4)+2*2**2*math.exp(-2)+8*3**3*math.exp(-3)
    require(1.3-.005*bump_bound>1 and 1.3+.005*bump_bound<1.6,'certified nonanalytic potential class')
    residuals=[]; root_errors=[]; schur_errors=[]; mass_errors=[]; counts=0
    for n in range(1,7):
        design=fixed_design(n); S=design['S']; D=2*1.6+1.6; u=(1/D)**(n-1)
        for t in [-.3,0.,.3]:
            for v in [-.2,.2]:
                exact_s=backwards(n,t,v)
                def match(s: float) -> float:
                    return action(n+1,s,v)['s']-action(n,s,t)['s']
                require(match(-S)>0 and match(S)<0,'fixed gate root signs')
                root=brentq(match,-S,S,xtol=1e-10,rtol=1e-12)
                root_errors.append(near(root,exact_s,1e-7,'data-derived root'))
                U=action(n,root,t); V=action(n+1,root,v)
                p,p1,p2=potential(t); expected=MU/2*(v-t)**2+float(p)
                residuals.append(near(V['value']-U['value'],expected,2e-8,'nonlinear one-step action'))
                B=U['tt']+MU+float(p2)
                require(0<B<=D,'Schur upper bound')
                require(abs(U['st'])>=u*(1-1e-12),'mechanical twist lower bound')
                schur_errors.append(near(V['ss']-U['ss'],-U['st']**2/B,2e-10,'root Schur derivative'))
                require(abs(V['ss']-U['ss'])>=u*u/D*(1-1e-6),'root derivative lower bound')
                K=max(S,.1)
                require(np.max(np.abs(U['path']))<=K+1e-7,'maximum principle range')
                require(abs(U['s'])<=2*1.6*K+.1+1.6*K,'fixed source momentum bound')
                for A in [U,V]:
                    require(design['lower']-1e-7<=A['value']<=design['upper']+1e-7,'uniform action bracket')
                counts+=1
        recovered=[]
        for v in [-.2,0.,.2]:
            root=brentq(lambda z: action(n+1,z,v)['s']-action(n,z,0.)['s'],-S,S,xtol=1e-10)
            recovered.append(action(n+1,root,v)['value']-action(n,root,0.)['value'])
        mass=(recovered[2]-2*recovered[1]+recovered[0])/.2**2
        mass_errors.append(near(mass,MU,2e-7,'finite-difference mass recovery'))
    RESULTS['nonanalytic_mechanics']={'matched_fixtures':counts,'prefix_lengths':list(range(1,7)),
        'max_action_error':max(residuals),'max_root_error':max(root_errors),
        'max_schur_identity_error':max(schur_errors),'max_mass_error':max(mass_errors),
        'analytic_bump_second_derivative_bound':bump_bound,'status':'passed'}


def clock_checks() -> None:
    mp.mp.dps=100
    errors=[]; anchor_sizes=[]
    # Large fixed-class thresholds test the cancellation cost, not just friendly clocks.
    for n in range(1,7):
        d=fixed_design(n)
        W=[mp.mpf(str(action(n,s,t)['value'])) for s,t in [(-.2,-.2),(.2,-.2),(-.2,.2),(.2,.2),(.11,-.07)]]
        T=[mp.mpf(str(d['upper']))+j for j in (1,2,3)]
        a=[mp.exp(mp.mpf('.17')*i+mp.mpf('.03')*i*i) for i in range(len(W))]
        Z=[mp.mpf('1.7'),mp.mpf('2.9'),mp.mpf('4.3')]
        f=[[a[i]*(T[j]-W[i])/Z[j] for i in range(len(W))] for j in range(3)]
        for reweight in [False,True]:
            F=[[val*(mp.exp(mp.mpf('.08')*i*i) if reweight else 1) for i,val in enumerate(row)] for row in f]
            g=[[val/row[0] for val in row] for row in F]
            c=[T[1]-T[2],T[2]-T[0],T[0]-T[1]]
            den=[sum(c[j]*g[j][i] for j in range(3)) for i in range(1,4)]
            idx=1+max(range(3),key=lambda k:abs(den[k]))
            denominator=sum(c[j]*g[j][idx] for j in range(3)); anchor_sizes.append(abs(denominator))
            w0=sum(c[j]*T[j]*g[j][idx] for j in range(3))/denominator
            for i in range(len(W)):
                q=g[0][i]/g[1][i]; d1=T[0]-w0; d2=T[1]-w0
                out=w0+d1*d2*(1-q)/(d2-d1*q)
                err=abs(out-W[i]); require(err<mp.mpf('1e-55'),'high-precision action inversion')
                errors.append(err)
    RESULTS['clock_and_nuisance']={'evaluations':len(errors),'decimal_precision':100,
        'max_absolute_error':mp.nstr(max(errors),8),'smallest_anchor_denominator':mp.nstr(min(anchor_sizes),8),
        'normalizers':'arbitrary positive scalars; cancellation tested independently of quadrature',
        'status':'passed'}


def point(side: int,x: float) -> tuple[np.ndarray,np.ndarray,np.ndarray]:
    # Facing arcs of two disjoint radius-one-half circles.
    if side==0:
        return np.array([-2+.5*math.cos(x),.5*math.sin(x)]),np.array([-.5*math.sin(x),.5*math.cos(x)]),np.array([-.5*math.cos(x),-.5*math.sin(x)])
    return np.array([2-.5*math.cos(x),.5*math.sin(x)]),np.array([.5*math.sin(x),.5*math.cos(x)]),np.array([.5*math.cos(x),-.5*math.sin(x)])

def chord(sa:int,s:float,sb:int,t:float) -> dict[str,float]:
    A,As,Ass=point(sa,s); B,Bt,Btt=point(sb,t); r=B-A; length=float(np.linalg.norm(r)); e=r/length
    ss=(As@As-(e@As)**2)/length-e@Ass
    tt=(Bt@Bt-(e@Bt)**2)/length+e@Btt
    st=-(As@Bt-(e@As)*(e@Bt))/length
    return dict(value=length,s=float(-e@As),t=float(e@Bt),ss=float(ss),st=float(st),tt=float(tt))

def extended(s:float,v:float) -> dict[str,float]:
    z=brentq(lambda t:chord(0,s,1,t)['t']+chord(1,t,0,v)['s'],-.4,.4)
    U=chord(0,s,1,z); E=chord(1,z,0,v); B=U['tt']+E['ss']
    require(B>0,'actual billiard interior Hessian')
    return dict(value=U['value']+E['value'],s=U['s'],ss=U['ss']-U['st']**2/B,join=z,B=B)

def billiard_checks() -> None:
    errors=[]; roots=[]; signs=[]
    for t in [-.01,0.,.01]:
        for v in [-.02,0.,.02]:
            H=lambda s:extended(s,v)['s']-chord(0,s,1,t)['s']
            require(H(-.3)>0>H(.3),'whole common interval billiard signs')
            root=brentq(H,-.3,.3,xtol=1e-13)
            V=extended(root,v); U=chord(0,root,1,t); E=chord(1,t,0,v)
            near(V['join'],t,1e-10,'same actual prefix path')
            errors.append(near(V['value']-U['value'],E['value'],1e-11,'actual billiard last flight'))
            deriv=V['ss']-U['ss']; near(deriv,-U['st']**2/(U['tt']+E['ss']),1e-10,'actual billiard Schur sign')
            require(deriv<0,'actual billiard downward root'); signs.append(deriv); roots.append(root)
    RESULTS['physical_billiard']={'matched_fixtures':9,'max_last_flight_error':max(errors),
        'root_derivative_range':[min(signs),max(signs)],'status':'passed'}


def distance_checks() -> None:
    def curve(t:Any,shift:np.ndarray)->np.ndarray:
        t=np.asarray(t); h=.46+.006*np.cos(3*t); hp=-.018*np.sin(3*t)
        return np.stack([h*np.cos(t)-hp*np.sin(t),h*np.sin(t)+hp*np.cos(t)],axis=-1)+shift
    s=np.array([0,.7,1.8,2.8,4.,5.2]); t=np.array([.2,2.2,4.2])
    A=curve(s,np.array([-1.,0.])); B=curve(t,np.array([1.,.2]))
    D=np.sum((A[:,None,:]-B[None,:,:])**2,axis=2)
    X=-.5*(D[1:,1:]-D[1:,:1]-D[:1,1:]+D[0,0])
    x,y=X[:,0],X[:,1]; M=np.column_stack([x*x,2*x*y,y*y,-2*x,-2*y])
    vals=np.linalg.solve(M,D[1:,0]-D[0,0]); G=np.array([[vals[0],vals[1]],[vals[1],vals[2]]]); h=vals[3:]
    eig,V=np.linalg.eigh(G); require(min(eig)>0,'positive recovered metric')
    P=(V*np.sqrt(eig))@V.T
    AA=np.vstack([np.zeros(2),X@P.T]); BB=np.linalg.solve(P.T,h[:,None]+np.array([[0,1,0],[0,0,1]])).T
    err=near(np.sum((AA[:,None,:]-BB[None,:,:])**2,axis=2),D,1e-10,'all distance certificate identities')
    C=np.column_stack([BB[1]-BB[0],BB[2]-BB[0]])
    sample=np.linspace(0,2*math.pi,101); true=curve(sample,np.array([-1.,0.]))
    dd=np.sum((true[:,None,:]-B[None,:,:])**2,axis=2)
    rhs=np.column_stack([np.sum(BB[j]**2)-np.sum(BB[0]**2)-(dd[:,j]-dd[:,0]) for j in [1,2]])/2
    out=np.linalg.solve(C.T,rhs.T).T
    Q=np.linalg.solve((A[1:3]-A[0]),AA[1:3]).T
    near(Q.T@Q,np.eye(2),1e-9,'common Euclidean gauge')
    err2=near(out,(true-A[0])@Q.T,1e-9,'whole-function trilateration samples')
    RESULTS['distance_certificate']={'rank_two_min_singular_value':float(np.linalg.svd(X,compute_uv=False)[-1]),
       'rank_five_min_singular_value':float(np.linalg.svd(M,compute_uv=False)[-1]),
       'max_squared_distance_error':err,'whole_curve_evaluations':101,'max_curve_error':err2,'status':'passed'}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    symbolic_checks(); mechanical_checks(); clock_checks(); billiard_checks(); distance_checks()
    RESULTS['scope']='Symbolic identities and finite numerical fixtures; not formal verification, an independent referee decision, minimax validation, or a complete statistical implementation.'
    RESULTS['versions']={'numpy':np.__version__,'scipy':scipy.__version__,'sympy':sp.__version__,'mpmath':mp.__version__}
    text=json.dumps(RESULTS,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
