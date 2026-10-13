#!/usr/bin/env python3
"""Finite checks of constants and interfaces; never a continuum proof substitute."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json, math
import numpy as np
COUNTS:dict[str,int]={}
def check(group:str, condition:bool)->None:
    if not condition: raise RuntimeError('finite regression failure: '+group)
    COUNTS[group]=COUNTS.get(group,0)+1
def matvec(A,x):return [sum((a*b for a,b in zip(row,x)),F(0)) for row in A]
def sub(A,B):return [[x-y for x,y in zip(a,b)] for a,b in zip(A,B)]
def inv(A):
    n=len(A);a=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for k in range(n):
        j=next((j for j in range(k,n) if a[j][k]),None)
        if j is None:raise ValueError('singular matrix')
        a[k],a[j]=a[j],a[k];t=a[k][k];a[k]=[x/t for x in a[k]]
        for i in range(n):
            if i!=k:
                t=a[i][k];a[i]=[x-t*y for x,y in zip(a[i],a[k])]
    return [r[n:] for r in a]
def occupation(P,a):return matvec(inv([[F(i==j)-P[i][j] for j in range(len(P))] for i in range(len(P))]),a)
def norm(x):return sum(abs(t) for t in x)
def main():
    for t in range(1,31):
        for den in [2,4,8,16]:
            for num in [1,den//2,den]:
                rho=F(num,den);mean=sum(((1-rho)**k for k in range(t)),F(0));bad=1-(1-rho)**(t-1)
                check('mean_margin',mean<=1+(1-rho)*(t-1))
                check('risk_margin',bad<=rho*(t-1))
    for n2 in range(2,20):
        for n1 in range(1,n2+1):
            rho=F(n2-n1,n2-1)
            check('exact_budget_reserve',1+(1-rho)*(n2-1)==n1)
    # Positive two-live/two-terminal ensemble maps, exact rational defects.
    for i,j,k in product(range(1,6),repeat=3):
        p=F(i,8);r=F(j,9);rho=F(k,8)
        P=[[p/2,r/3],[p/2,2*r/3]];Q=[[1-p,F(0)],[F(0),1-r]]
        Pt=[[x*(1-rho) for x in row] for row in P]
        Qt=[[Q[0][u]+rho*sum(P[v][u] for v in range(2)) for u in range(2)],Q[1][:]]
        a=[F(i,6),1-F(i,6)];at=[F(j,6),1-F(j,6)]
        z=occupation(P,a);zt=occupation(Pt,at);d=matvec(Q,z);dt=matvec(Qt,zt)
        Dz=norm([x-y for x,y in zip(at,a)])+norm(matvec(sub(Pt,P),z))+norm(matvec(sub(Qt,Q),z))
        check('terminal_resolvent',norm([x-y for x,y in zip(dt,d)])<=Dz)
        check('mean_resolvent',abs(sum(zt)-sum(z))<=Dz/rho)
        check('terminal_mass',sum(d)==sum(dt)==1)
        for costs in [[F(0),F(1)],[F(1,3),F(4,5)]]:
            check('risk_resolvent',abs(sum(c*x for c,x in zip(costs,dt))-sum(c*x for c,x in zip(costs,d)))<=Dz)
    for den in range(2,19):
        for i in range(1,den):
            p=F(i,den);u=(1-p)/2
            check('mean_denominator',1/p-1/(p+u)==u/(p*(p+u)))
    for d in range(2,8):
        for Q in [2,4,8,16]:
            for offset in range(1,11):
                v=[F(offset+i, sum(offset+j for j in range(d))) for i in range(d)]
                rounded=[F((x*Q).numerator//(x*Q).denominator,Q) for x in v[:-1]]
                rounded.append(1-sum(rounded))
                check('simplex_rounding',sum(rounded)==1 and min(rounded)>=0 and norm([x-y for x,y in zip(v,rounded)])<=F(2*(d-1),Q))
    for N in [F(3,2),F(2),F(7,2),F(10)]:
        for rho in [F(1,2),F(1,8),F(1,32)]:
            sigma=rho*(N-1);eta=sigma*rho/(8*N);mean=N-sigma+eta*N/rho
            check('strict_feasibility',mean+sigma/4<N)
            check('budget_sensitivity_margin',eta*N/rho==sigma/8)
    # Common report averaging really sums model-dependent instrument error after common rows.
    for a,b in product(range(1,8),repeat=2):
        L=[F(a,8),F(b,8)];r=[F(1,3),F(4,5)];rbar=sum(r)/2;Lbar=sum(L)/2
        error=abs(sum(r[u]*L[u] for u in range(2))/2-rbar*Lbar)
        bound=sum(abs(L[u]-Lbar) for u in range(2))/2
        check('common_reference_averaging',error<=bound)
    # Small dyadic table search: exact one-live/two-terminal laws across two models.
    Q=2;rows=[(F(a,Q),F(b,Q),F(Q-a-b,Q)) for a in range(Q+1) for b in range(Q-a+1)]
    rho=F(1,4);accepted=0
    for row0,row1 in product(rows,repeat=2):
        Ts=[];Rs=[]
        for prob in [F(1,3),F(2,3)]:
            live=(1-prob)*row0[0]+prob*row1[0];left=(1-prob)*row0[1]+prob*row1[1]
            livek=(1-rho)*live;leftk=left+rho*live
            T=1/(1-livek);d0=leftk*T;d1=1-d0
            check('finite_table_mass',0<=d0<=1 and 0<=d1<=1 and T<=1/rho)
            Ts.append(T);Rs.append(d1)
        Tplus=max(Ts)+F(1,16);Rplus=max(Rs)+F(1,32)
        if Tplus<=F(2):
            accepted+=1;check('certified_table_acceptance',max(Ts)<=2 and max(Rs)<=Rplus)
    check('nonempty_finite_certificate',accepted>0)
    # Rank-changing positive matrices: numerical sanity, not proof of Holder continuity.
    rng=np.random.default_rng(48013)
    for q in [2,3,4]:
        for it in range(50):
            X=rng.normal(size=(q,q))+1j*rng.normal(size=(q,q));Y=rng.normal(size=(q,q))+1j*rng.normal(size=(q,q))
            if it%2==0:X[:,-1]=0
            A=X@X.conj().T;B=Y@Y.conj().T
            def root(T):
                v,U=np.linalg.eigh(T);return (U*np.sqrt(np.maximum(v,0)))@U.conj().T
            lhs=np.linalg.norm(root(A)-root(B),2);rhs=math.sqrt(np.linalg.norm(A-B,2))
            check('quantum_rank_holder_numeric',lhs<=rhs+1e-10)
    print(json.dumps({'status':'PASS','checks':sum(COUNTS.values()),'groups':COUNTS,'accepted_toy_tables':accepted,'arithmetic':'rational except 150 explicitly marked finite-matrix numerical checks','limitations':'finite examples and constants only; no continuum proof, efficient synthesis, or numerical Gaussian optimum claimed'},sort_keys=True,indent=2))
if __name__=='__main__':main()
