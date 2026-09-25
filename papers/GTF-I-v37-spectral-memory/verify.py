#!/usr/bin/env python3
"""Finite regression tests for GTF-I v37; analytic proofs are in the article.

Exact arithmetic checks are separate from explicitly labelled numerical
quadrature diagnostics. No finite test certifies a spherical L2 spectral gap.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import logsumexp
import sympy as sp


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError('CHECK_REJECTED: '+message)


def add(x, y): return tuple(a+b for a,b in zip(x,y))
def scale(a,x): return tuple(a*b for b in x)
def dot(x,y): return sum((a*b for a,b in zip(x,y)),F(0))
def rotate(x,c):
    return x if c==0 else ((3*x[0]-4*x[1])/5,(4*x[0]+3*x[1])/5)


def centroid_checks() -> int:
    # A full joint law is propagated, including private stochastic states.
    joint={((F(1),F(0)),0):F(1,3),((F(1),F(0)),1):F(2,3)}
    previous_v=F(1);total=F(0);checks=0
    for t in range(10):
        old={}
        for (y,s),mass in joint.items():
            p,z=old.get(s,(F(0),(F(0),F(0))))
            old[s]=(p+mass,add(z,scale(mass,y)))
        z={s:scale(1/p,u) for s,(p,u) in old.items()}
        v=sum((p*dot(z[s],z[s]) for s,(p,_) in old.items()),F(0))
        require(v==previous_v,'Conditional second moment inconsistent')
        K=2+(t%4);nxt={};pred={};terms=[]
        for s,(p,_) in old.items():
            for c,pc in [(0,F(1,3)),(1,F(2,3))]:
                weights=[1+((s+2*j+3*c+t)%7) for j in range(K)]
                denominator=sum(weights)
                for j,w in enumerate(weights):
                    mass=p*pc*F(w,denominator);x=rotate(z[s],c)
                    pp,zz=pred.get(j,(F(0),(F(0),F(0))))
                    pred[j]=(pp+mass,add(zz,scale(mass,x)))
                    terms.append((mass,x,j))
        for (y,s),p in joint.items():
            for c,pc in [(0,F(1,3)),(1,F(2,3))]:
                weights=[1+((s+2*j+3*c+t)%7) for j in range(K)]
                for j,w in enumerate(weights):
                    key=(rotate(y,c),j)
                    nxt[key]=nxt.get(key,F(0))+p*pc*F(w,sum(weights))
        actual={}
        for (y,j),mass in nxt.items():
            pp,zz=actual.get(j,(F(0),(F(0),F(0))))
            actual[j]=(pp+mass,add(zz,scale(mass,y)))
        require(pred==actual,'Tower identity fails for a hidden successor')
        zp={j:scale(1/p,u) for j,(p,u) in pred.items()}
        vp=sum((p*dot(zp[j],zp[j]) for j,(p,_) in pred.items()),F(0))
        loss=sum((p*dot(add(x,scale(-1,zp[j])),add(x,scale(-1,zp[j])))
                  for p,x,j in terms),F(0))
        require(v-vp==loss and loss>=0,'Quadratic loss identity fails')
        total+=loss;require(total==1-vp and total<=1,'Quadratic loss does not telescope')
        joint=nxt;previous_v=vp;checks+=len(pred)+3
    return checks


def algebra_checks() -> dict:
    y,a,t=sp.symbols('y a t',real=True,positive=True)
    logf=-y*y/(2*t*t)+sp.log(sp.cosh(a*y/(t*t)))
    h=sp.diff(logf,y,2)
    require(sp.simplify(h+1/t**2-a**2/(t**4*sp.cosh(a*y/t**2)**2))==0,
            'Gaussian-mixture Hessian identity')
    # Constant calculation is tested algebraically for several dimensions.
    for d in range(2,9):
        kap,A,k=sp.symbols('kap A k',positive=True)
        m=d-1;r=(kap/(16*A*k))**sp.Rational(1,m)
        tau=kap*r/(8*sp.sqrt(2*d))
        B=2048*d*(16*A)**sp.Rational(2,m)
        target=B*kap**(-3-sp.Rational(2,m))*k**sp.Rational(2,m)
        require(sp.simplify(16/kap/tau**2-target)==0,'Occupation coefficient')
    require(2048*3*16==98304,'Three-dimensional constant')
    # Radial-cone Hellinger separation uses the full L2 norm, not probability variance.
    kap=sp.symbols('kap',positive=True)
    require(sp.simplify((sp.sqrt(kap/4)-sp.sqrt(kap/16))**2-kap/16)==0,'Cone separation')
    Rx=sp.Matrix([[1,0,0],[0,sp.Rational(-7,25),sp.Rational(-24,25)],
                  [0,sp.Rational(24,25),sp.Rational(-7,25)]])
    Rz=sp.Matrix([[sp.Rational(-7,25),sp.Rational(-24,25),0],
                  [sp.Rational(24,25),sp.Rational(-7,25),0],[0,0,1]])
    require(Rx.T*Rx==sp.eye(3) and Rz.T*Rz==sp.eye(3),'Orthogonal rational gates')
    require(Rx*Rz!=Rz*Rx,'The displayed commands commute')
    sx=sp.Matrix([[0,1],[1,0]]);sy=sp.Matrix([[0,-sp.I],[sp.I,0]]);sz=sp.diag(1,-1)
    pauli=[sx,sy,sz]
    for Q,R in [((3*sp.eye(2)-4*sp.I*sx)/5,Rx),((3*sp.eye(2)-4*sp.I*sz)/5,Rz)]:
        require((Q.H*Q).applyfunc(sp.simplify)==sp.eye(2),'Unitary lift')
        for j in range(3):
            for i in range(3):
                require(sp.simplify(sp.trace(pauli[i]*Q*pauli[j]*Q.H)/2-R[i,j])==0,
                        'Bloch adjoint convention')
    return {'gaussian_hessian_identities':1,'dimension_constant_identities':7,
            'three_dimensional_B':98304,'bloch_entries':18}


def compare_bits(bits, threshold, b):
    # Every bit is consumed, even after a relation has been decided.
    relation=0;used=0
    for i,u in enumerate(bits):
        q=(threshold>>(b-1-i))&1
        if relation==0 and u!=q: relation=-1 if u<q else 1
        used+=1
    require(used==b,'Comparator duration')
    return relation<0,used


def timing_checks() -> tuple[int,int]:
    comparisons=0;trees=0
    for b in range(1,8):
        for threshold in range(2**b):
            accepts=0
            for U in range(2**b):
                bits=[(U>>(b-1-i))&1 for i in range(b)]
                ok,duration=compare_bits(bits,threshold,b)
                require(ok==(U<threshold) and duration==b,'Padded comparison incorrect')
                accepts+=ok;comparisons+=1
            require(accepts==threshold,'Threshold law not exact')
    # Three conditional choices and one exit leaf. Padding after a leaf
    # consumes the same total nine bits without changing that stored leaf.
    b=3;den=2**b;thresholds=[1,3,6];count=[0]*4;durations=set()
    for word in itertools.product([0,1],repeat=3*b):
        leaf=None;consumed=0
        for node,threshold in enumerate(thresholds):
            block=word[node*b:(node+1)*b]
            ok,used=compare_bits(block,threshold,b);consumed+=used
            if leaf is None and ok: leaf=node
        if leaf is None: leaf=3
        count[leaf]+=1;durations.add(consumed);trees+=1
    expected=[];mass=F(1)
    for threshold in thresholds:
        expected.append(mass*F(threshold,den));mass*=1-F(threshold,den)
    expected.append(mass)
    require([F(c,2**(3*b)) for c in count]==expected and durations=={3*b},
            'Padded categorical law or duration failed')
    return comparisons,trees


def mixture_entropy(w,x,tau):
    w=np.asarray(w,dtype=float);x=np.asarray(x,dtype=float)
    def term(y):
        lf=logsumexp(np.log(w)-(y-x)**2/(2*tau*tau))-math.log(tau*math.sqrt(2*math.pi))
        return -math.exp(lf)*lf
    result,error=quad(term,float(min(x)-12*tau),float(max(x)+12*tau),epsabs=2e-10,limit=200)
    require(error<2e-7,'Entropy quadrature failed to converge')
    return result


def diagnostics() -> dict:
    rng=np.random.default_rng(371);margins=[]
    for j in range(20):
        x=rng.uniform(-1,1,8);w=rng.dirichlet(np.ones(8));cat=np.arange(8)%3
        p=np.array([w[cat==c].sum() for c in range(3)])
        m=np.array([np.dot(w[cat==c],x[cat==c])/p[c] for c in range(3)])
        tau=[.1,.25,.6,1.2][j%4]
        cost=float(np.dot(w,(x-m[cat])**2))
        gap=cost/(2*tau*tau)-(mixture_entropy(w,x,tau)-mixture_entropy(p,m,tau))
        require(gap>=-1e-7,'Smoothed entropy diagnostic inequality')
        margins.append(gap)
    # Finite homogeneous-space analogues of the Hellinger-gap step.
    cases=0
    for n in [3,5,7]:
        for i in range(10):
            f=rng.dirichlet(np.ones(n));r=np.sqrt(f);lazy=.4
            g=lazy*f+(1-lazy)/n
            inc=-np.dot(g,np.log(g))+np.dot(f,np.log(f))
            variance=float(np.dot(r-r.mean(),r-r.mean()))
            require(inc+1e-12>=(1-lazy**2)*variance,'Finite entropy spectral inequality')
            cases+=1
    return {'centroid_quadrature_cases':20,'finite_gap_cases':cases,
            'arithmetic':'double-precision quadrature with stated tolerances; not exact proof',
            'scope':'Only finite diagnostics; no infinite-dimensional spectral gap or universal theorem is numerically certified.'}


def negative(name: str) -> None:
    if name=='wrong-centroid':
        X=sp.Matrix([1,0]);M=sp.Matrix([0,0]);v=sp.Matrix([1,0])
        require((v.dot(X-M))==0,'Taylor term only cancels for a conditional centroid')
    elif name=='missing-smoothing-scale':
        k=8;r=F(1,2);kap=F(1,10)
        require(k*r*r<=kap/16,'An arbitrary smoothing radius does not give small cap union')
    elif name=='reversed-loss':
        old=F(1);new=F(0);variance=F(1)
        require(new-old==variance,'Quadratic loss has the opposite sign')
    elif name=='fake-state-gap':
        R=sp.Matrix([[1,0,0],[0,0,-1],[0,1,0]])
        require(R*sp.Matrix([1,0,0])!=sp.Matrix([1,0,0]),
                'A defining matrix check cannot certify a full sphere gap; this axis is invariant')
    elif name=='wrong-hessian-sign':
        posterior_variance=F(1,4);tau=F(1,2)
        claimed=-1/tau**2-posterior_variance/tau**4
        require(claimed>=-1/tau**2,'Mixture log Hessian includes positive covariance')
    elif name=='unpaid-noise':
        actual_state_dimension=0;gaussian_state_dimension=3
        require(actual_state_dimension==gaussian_state_dimension,'Gaussian smoothing is proof-side, not a free physical register')
    elif name=='early-ready':
        threshold=4;b=3;durations=set()
        for word in itertools.product([0,1],repeat=b):
            used=0
            for i,u in enumerate(word):
                used+=1
                if u!=((threshold>>(b-1-i))&1): break
            durations.add(used)
        require(len(durations)==1,'Early readiness leaks private comparison timing')
    elif name=='wrong-binary-tv':
        eps=F(1,10);actual_mean_error=2*eps
        require(actual_mean_error<=eps,'Binary means differ by twice row TV')
    else: raise ValueError('Unknown negative control '+name)


def main() -> None:
    p=argparse.ArgumentParser();p.add_argument('--negative-control');p.add_argument('--export',type=Path)
    args=p.parse_args()
    if args.negative_control:
        negative(args.negative_control)
        raise RuntimeError('A negative control unexpectedly passed')
    exact=algebra_checks();exact['hidden_centroid_checks']=centroid_checks()
    a,b=timing_checks();exact['padded_bit_comparisons']=a;exact['padded_tree_words']=b
    numerical=diagnostics()
    if args.export:
        args.export.parent.mkdir(parents=True,exist_ok=True)
        args.export.write_text(json.dumps({'schema':'gtf37.rows/1','three_dimensional_B':98304,
          'Rx':[[1,0,0],[0,'-7/25','-24/25'],[0,'24/25','-7/25']],
          'Rz':[['-7/25','-24/25',0],['24/25','-7/25',0],[0,0,1]],
          'padded_example':{'b':3,'thresholds':[1,3,6],'duration':9,'denominator':512,
                           'leaf_counts':[64,168,210,70]},
          'spectral_gap':'External analytic hypothesis; no numerical value asserted'},indent=2)+'\n')
    print(json.dumps({'schema':'gtf37.checks/1','exact_checks':exact,'numerical_diagnostics':numerical,
       'analytic_claims':{'sharp_spectral_width':'Theta(N^((d-1)/2)) at fixed positive calibrated signal',
         'occupation':'sum_{K_t<=k}(1-lambda_t^2) <= B_d*k^(2/(d-1))*kappa^(-3-2/(d-1))',
         'explicit_rational_labels':'Theta(N); one qubit versus log2 N+O(1) atomic classical bits',
         'padded_duration':'Exactly (L-1)*b fair-bit microsteps per macro update',
         'gap_numerically_evaluated':False,'independent_priority_certification':False},
       'scope':'Finite exact regressions and labelled numerical diagnostics, not independent proof verification or a spectral-gap computation.'},indent=2,sort_keys=True))

if __name__=='__main__': main()
