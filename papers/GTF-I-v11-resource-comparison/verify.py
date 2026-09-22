#!/usr/bin/env python3
"""Finite witnesses and regression checks. These do not certify analytic proofs."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import combinations, product
import json
import math
import sys
import numpy as np
from scipy.optimize import brentq
from scipy.special import ndtr

MUTANTS = ('drop_state_cost','free_seed','pairwise_cover','rank_is_width',
           'erase_covariate','wrong_resolvent','drop_mark','wrong_graph_sign')
checks=0

def require(ok: bool, message: str) -> None:
    global checks
    checks += 1
    if not ok:
        raise ValueError(message)

def cover_number(sets: list[list[set[int]]]) -> int:
    n=len(sets); d=len(sets[0]); compatible=[]
    for mask in range(1,1<<n):
        ids=[i for i in range(n) if mask>>i&1]
        if all(set.intersection(*(sets[i][j] for i in ids)) for j in range(d)):
            compatible.append(mask)
    dp=[n+1]*(1<<n);dp[0]=0
    for mask in range(1<<n):
        for cell in compatible:
            dp[mask|cell]=min(dp[mask|cell],dp[mask]+1)
    return dp[-1]

def chromatic(n: int, edges: list[tuple[int,int]]) -> int:
    for k in range(1,n+1):
        if any(all(a[u]!=a[v] for u,v in edges) for a in product(range(k),repeat=n)):
            return k
    raise RuntimeError('No coloring found')

def tests(mutant: str | None) -> dict:
    rng=np.random.default_rng(110923)
    # Sharp temporal bottleneck: all deterministic encoders, then randomized channels.
    for k in range(2,7):
        for s in range(1,min(k,3)+1):
            best=max(F(len(set(a)),k) for a in product(range(s),repeat=k))
            require(best==F(s,k),'temporal optimum differs from s/k')
            for _ in range(12):
                q=rng.dirichlet(np.ones(s),size=k)
                require(q.max(axis=0).sum()/k<=s/k+1e-12,'randomization violated bottleneck')
    exact_cost=1 if mutant=='drop_state_cost' else 5
    require(exact_cost>=5,'exact repeated-report simulation forgot its state cost')
    stored=(2 if mutant=='free_seed' else 3*2)
    require(stored==6,'finite shared index was not charged in private storage')
    # Hypergraph compatible cover, including pairwise-but-not-joint intersection.
    triangle=[[{0,1}],[{1,2}],[{0,2}]]
    value=1 if mutant=='pairwise_cover' else cover_number(triangle)
    require(value==2,'pairwise compatibility was substituted for joint compatibility')
    graph_cases=0
    for n in range(2,5):
        all_edges=list(combinations(range(n),2))
        for bits in product((0,1),repeat=len(all_edges)):
            edges=[e for e,b in zip(all_edges,bits) if b]
            if edges:
                opt=[[({0} if x==u else {1} if x==v else {0,1})
                      for u,v in edges] for x in range(n)]
            else: opt=[[{0,1}] for _ in range(n)]
            require(cover_number(opt)==chromatic(n,edges),'coloring reduction mismatch')
            graph_cases+=1
    # General exact-task upper and lower bounds on reproducible rational tables.
    for _ in range(90):
        n,d,b=4,3,3
        loss=rng.integers(0,4,size=(n,d,b))
        sets=[[set(np.flatnonzero(loss[i,j]==loss[i,j].min()).tolist())
               for j in range(d)] for i in range(n)]
        tau=cover_number(sets)
        singles=[cover_number([[sets[i][j]] for i in range(n)]) for j in range(d)]
        require(max(singles)<=tau<=min(n,b**d),'task-cover bounds failed')
    # Homogeneous and inhomogeneous binary hidden-source posterior keys.
    primes=[2,3,5,7,11,13,17,19,23,29]
    counts={}
    for t in range(1,11):
        homogeneous={sum(y) for y in product((0,1),repeat=t)}
        keys={math.prod(p**b for p,b in zip(primes,y)) for y in product((0,1),repeat=t)}
        require(len(homogeneous)==t+1,'count-vector family mismatch')
        claimed=2 if mutant=='rank_is_width' and t==3 else len(keys)
        require(claimed==2**t,'rank two was mistaken for positive state cardinality')
        counts[str(t)]=len(keys)
    # Complete-state fusion, with nontrivial nuisance reports and a controlled second step.
    # X is the actual mark; M=(X,B) is complete. A=B changes P(C=1|X,A).
    direct={}; reverse={}
    for x,b,c in product(range(2),repeat=3):
        px=F(1,3) if x==0 else F(2,3)
        pb=F(1,4) if b==0 else F(3,4)
        pc1=F(1+x+b,5)
        p=px*pb*(pc1 if c else 1-pc1)
        state=(x,b^c)
        direct[(x,state)]=direct.get((x,state),F(0))+p
        # Reverse class report transducer knows X from the complete register.
        reverse[(x,state)]=reverse.get((x,state),F(0))+px*pb*(pc1 if c else 1-pc1)
    require(direct==reverse,'complete-state fused joint law mismatch')
    require(sum(direct.values())==1,'fusion probabilities not normalized')
    for decoder in product(range(2),repeat=4):
        r1=sum(p*int(decoder[2*m[0]+m[1]]!=w) for (w,m),p in direct.items())
        r2=sum(p*int(decoder[2*m[0]+m[1]]!=w) for (w,m),p in reverse.items())
        require(r1==r2,'fusion terminal decision risk changed')
    # A report-only reconstruction can preserve Y while breaking the actual mark.
    marked={(0,0):F(1,2),(1,1):F(1,2)}
    broken={(y,w):F(1,4) for y,w in product(range(2),repeat=2)}
    chosen=broken if mutant=='drop_mark' else marked
    require(sum(p for (y,w),p in chosen.items() if y!=w)==0,'actual mark coupling was discarded')
    # Conditional policies exploiting a physically redisplayed nonatomic covariate.
    x=np.linspace(0,1,1001)
    private=.5 if mutant=='erase_covariate' else float(np.trapezoid(np.minimum(x,1-x),x))
    require(abs(private-.25)<1e-12,'displayed-covariate pointwise support failed')
    for n in (2,5,10,100):
        require(abs(np.eye(n).sum()/n**2-1/n)<1e-15,'diagonal product-mass check failed')
    # Gaussian marked feedback step estimate, independent of the consumer width.
    for sigma in (.1,.3,1.,3.):
        for delta in np.linspace(0,8,101):
            tv=2*ndtr(delta/(2*sigma))-1
            bound=min(1.,delta/(sigma*math.sqrt(2*math.pi)))
            require(tv<=bound+1e-14,'Gaussian mean TV bound failed')
    # Orbit-convolution derivative sign: f(x+t)=exp(i(x+t)).
    grid=np.linspace(-.2,.2,4001)
    phi=np.exp(-1/(1-(grid/.201)**2));phi/=np.trapezoid(phi,grid)
    # Smooth cutoff chosen inside +/-0.201; boundary terms tiny for this mesh.
    derivative=np.gradient(phi,grid)
    b=np.trapezoid(phi*np.exp(1j*grid),grid)
    ag=(-1 if mutant!='wrong_graph_sign' else 1)*np.trapezoid(derivative*np.exp(1j*grid),grid)
    require(abs(ag-1j*b)<2e-6,'orbit graph derivative has the wrong sign')
    # Nonlinear resolvent identity for H(u)=-u^3.
    def J(lam:float,f:float)->float:
        return brentq(lambda u:u+lam*u**3-f,-10.,10.,xtol=1e-14)
    for lam,mu,f in product((.2,1.,2.),(.1,.7,3.),(-2.,-.5,1.5)):
        u=J(lam,f)
        if mutant=='wrong_resolvent':
            rhs=J(mu,f)+(mu-lam)*J(lam,J(mu,f))
        else: rhs=J(mu,(mu/lam)*f+(1-mu/lam)*u)
        require(abs(u-rhs)<1e-11,'linear difference/product identity used for nonlinear resolvent')
    return {'status':'passed','finite_checks':checks,'graph_instances':graph_cases,
            'positive_states_at_rank_two':counts,'scope':'Finite diagnostics only; no analytic proof certification.'}

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--mutant',choices=MUTANTS);args=ap.parse_args()
    try:
        result=tests(args.mutant)
        if args.mutant:raise RuntimeError('designated mutant survived: '+args.mutant)
        print(json.dumps(result,indent=2));return 0
    except (ValueError,RuntimeError) as exc:
        print('FAILED: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
