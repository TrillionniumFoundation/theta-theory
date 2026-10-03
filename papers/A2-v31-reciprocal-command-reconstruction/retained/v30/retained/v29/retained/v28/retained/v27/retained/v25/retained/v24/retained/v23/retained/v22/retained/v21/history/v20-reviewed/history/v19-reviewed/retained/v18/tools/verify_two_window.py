#!/usr/bin/env python3
"""Finite diagnostics for A2 v18; neither proof certification nor a sampler.

Exact tests need the standard library. --geometry adds independent numerical
stationary-ray tests and needs numpy/scipy. Explicit checks survive python -O.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import itertools
import json
import math

COUNTS: Counter[str] = Counter()

def check(ok: bool, group: str, detail: str = '') -> None:
    if not ok:
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] += 1

# Ordinary bivariate Taylor coefficients, truncated after total degree two.
KEYS = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
def add(a, b):
    return {k: a.get(k, F(0)) + b.get(k, F(0)) for k in KEYS}
def scale(a, c):
    return {k: c*a.get(k, F(0)) for k in KEYS}
def mul(a, b):
    out = dict.fromkeys(KEYS, F(0))
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            if (i+k,j+l) in out:
                out[i+k,j+l] += x*y
    return out
def inv(a):
    c = a.get((0,0), F(0))
    if c == 0:
        raise ZeroDivisionError('zero constant term')
    z = scale(a, 1/c); z[(0,0)] -= 1
    return scale(add(add({(0,0): F(1)}, scale(z,-1)), mul(z,z)),1/c)

def exact_geometry() -> None:
    for g, k, ko, t in itertools.product(
        [F(1,3),F(2,3),F(1),F(5,2)],
        [F(1,5),F(1,2),F(1),F(3)],
        [F(1,4),F(2,3),F(2),F(7,3)],
        [F(0),F(1,7),F(-1,5),F(1,3),F(-2,5)]):
        a=2*t/(1+t*t); v=(1-t*t)/(1+t*t)
        dss=v*v/g+k*v; dsu=-v/g; duu=1/g+ko
        wst=-dsu*dsu/(2*duu); wss=dss+wst
        check((wss-wst-v*v/g)/v==k,'source_curvature')
        check((v*v/(-2*g*wst)-1)/g==ko,'opposite_curvature')
        check(-dsu/duu==v/(1+g*ko),'foot_arclength_speed')
        check(wst<0 and v>0,'twist_and_frame_margins')
    for g,k,ko in itertools.product([F(1,2),F(1),F(3)],repeat=3):
        st=-1/(2*g*(1+g*ko)); ss=(1+g*k)/g+st
        check(ss-st==(1+g*k)/g,'normal_hessian_compatibility')


def density_jets() -> None:
    for n in range(1,241):
        W={key:F(((n*(i+3))%19)-9,17+i) for i,key in enumerate(KEYS)}
        W[(0,0)]=F(1+n%7,5)
        weight={key:F(((n*(i+5))%13)-6,29+i) for i,key in enumerate(KEYS)}
        weight[(0,0)]=F(3+n%5,7)
        T1=F(4+n%3); T2=T1+F(1+n%4,6)
        f1=mul(weight,add({(0,0):T1},scale(W,-1)))
        f2=mul(weight,add({(0,0):T2},scale(W,-1)))
        gap=add(f2,scale(f1,-1))
        rec=mul(add(scale(f2,T1),scale(f1,-T2)),inv(gap))
        for key in KEYS:
            check(rec[key]==W[key],'two_window_C2_jet_identity',str((n,key)))
        check(scale(gap,1/(T2-T1))==weight,'flux_factor_recovery')
        def reflect(j): return {k:(-1)**sum(k)*v for k,v in j.items()}
        rec_ref=mul(add(scale(reflect(f2),T1),scale(reflect(f1),-T2)),inv(reflect(gap)))
        check(rec_ref==reflect(W),'coherent_reflection')
    for wst,A,dt in itertools.product([F(-1,5),F(-3,4),F(-2)],
                                      [F(1,3),F(1),F(5)],
                                      [F(1,7),F(1,2),F(2)]):
        # Use lambda=2*pi*A as the normalized area; no rational proxy for pi.
        lam=A
        df=dt*(-wst)/lam
        check(dt*(-wst)/df==lam,'normalization_recovery')


def invert_matrix(a):
    n=len(a); b=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
    for j in range(n):
        pivot=next(i for i in range(j,n) if b[i][j])
        b[j],b[pivot]=b[pivot],b[j]
        c=b[j][j]; b[j]=[x/c for x in b[j]]
        for i in range(n):
            if i!=j:
                c=b[i][j]; b[i]=[x-c*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]

def cell_averages() -> None:
    nodes=[-1,0,1]
    mat=[[F(1),F(i),F(i*i)+F(1,12)] for i in nodes]
    im=invert_matrix(mat)
    for i,j in itertools.product(range(3),repeat=2):
        check(sum(im[i][k]*mat[k][j] for k in range(3))==F(i==j),
              'cell_average_matrix_inverse')
    for p,q in itertools.product(range(3),repeat=2):
        vals=[[mat[i][p]*mat[j][q] for j in range(3)] for i in range(3)]
        recovered=[[sum(im[a][i]*im[b][j]*vals[i][j]
                         for i,j in itertools.product(range(3),repeat=2))
                    for b in range(3)] for a in range(3)]
        for a,b in itertools.product(range(3),repeat=2):
            check(recovered[a][b]==F(a==p and b==q),'tensor_polynomial_reproduction')
    # Exhaust all 512 extremal error signs for the center second derivative.
    weights=[2*im[2][i]*im[0][j] for i,j in itertools.product(range(3),repeat=2)]
    bound=sum(abs(x) for x in weights)
    for signs in itertools.product([-1,1],repeat=9):
        err=abs(sum(w*s for w,s in zip(weights,signs)))
        check(err<=bound,'second_derivative_error_bound')
    for beta in [F(1),F(1,2),F(1,3),F(2,3)]:
        r=1/(beta+4)
        check(beta*r==1-4*r,'histogram_rate_balance')
    for theta,beta in itertools.product([F(1,5),F(1,2),F(3,4)],
                                       [F(1),F(1,2),F(2,3)]):
        rate=theta*beta/(beta+4)
        check(rate>0 and rate<theta,'conditional_rate_range')


def numerical_geometry() -> None:
    import numpy as np
    from scipy.integrate import quad
    from scipy.optimize import brentq
    # Smooth asymmetric local graphs; computations do not invoke the displayed
    # curvature inversion or its Schur complement to construct W.
    families=[(.7,.4,.11,-.07,.03,.06,1.1),
              (1.3,.8,-.16,.13,.08,.04,.7),
              (.5,.5,.09,-.12,.02,.07,1.4)]
    maxerr=0.0
    for k0,k1,c0,c1,d0,d1,g in families:
        def ps(y,b):
            k,c,d=(k0,c0,d0) if b==0 else (k1,c1,d1)
            return k*y*y/2+c*y**3/6+d*y**4/24
        def dp(y,b):
            k,c,d=(k0,c0,d0) if b==0 else (k1,c1,d1)
            return k*y+c*y*y/2+d*y**3/6
        def ddp(y,b):
            k,c,d=(k0,c0,d0) if b==0 else (k1,c1,d1)
            return k+c*y+d*y*y/2
        def arc(y,b): return quad(lambda z: math.sqrt(1+dp(z,b)**2),0,y,
                                  epsabs=2e-13,epsrel=2e-13)[0]
        def yy(s,b): return brentq(lambda y:arc(y,b)-s,-.7,.7,xtol=5e-15)
        def source(s):
            y=yy(s,0); return np.array([-ps(y,0),y])
        def other(w): return np.array([g+ps(w,1),w])
        def action(s,t,returnfoot=False):
            x=source(s); z=source(t)
            def station(w):
                q=other(w); tangent=np.array([dp(w,1),1.])
                return np.dot(q-x,tangent)/np.linalg.norm(q-x)+np.dot(q-z,tangent)/np.linalg.norm(q-z)
            w=brentq(station,-.7,.7,xtol=5e-15)
            W=np.linalg.norm(x-other(w))+np.linalg.norm(z-other(w))
            return (W,w) if returnfoot else W
        for s in [-.22,-.11,0.,.13,.24]:
            h=0.001
            W,foot=action(s,s,True)
            # Richardson extrapolation of independent finite differences.
            def derivatives(h):
                ss=(action(s+h,s)-2*W+action(s-h,s))/h**2
                st=(action(s+h,s+h)-action(s+h,s-h)-action(s-h,s+h)+action(s-h,s-h))/(4*h*h)
                a=(action(s+h,s)-action(s-h,s))/(2*h)
                return np.array([a,ss,st])
            a,ss,st=(4*derivatives(h/2)-derivatives(h))/3
            ell=W/2; v=math.sqrt(1-a*a)
            rec0=(ss-st-v*v/ell)/v
            rec1=(v*v/(-2*ell*st)-1)/ell
            y0=yy(s,0)
            true0=ddp(y0,0)/(1+dp(y0,0)**2)**1.5
            true1=ddp(foot,1)/(1+dp(foot,1)**2)**1.5
            err0=abs(rec0-true0); err1=abs(rec1-true1)
            maxerr=max(maxerr,err0,err1)
            check(err0<2e-6,'nonquadratic_stationary_source',str((s,err0)))
            check(err1<2e-6,'nonquadratic_stationary_opposite',str((s,err1)))
    print(json.dumps({'numerical_max_curvature_error':maxerr},sort_keys=True))


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--geometry',action='store_true')
    args=parser.parse_args()
    exact_geometry(); density_jets(); cell_averages()
    if args.geometry: numerical_geometry()
    print(json.dumps({'status':'passed','finite_checks':sum(COUNTS.values()),
                      'groups':dict(sorted(COUNTS.items())),
                      'formal_proof_certificate':False},sort_keys=True))

if __name__=='__main__':
    main()
